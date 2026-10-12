#!/usr/bin/env python3
"""Edition Desk + image QC, end to end against a throwaway origin. Only the network, Claude and the
image sourcing are mocked; git, the converter, the renderer and the gates run for real.

run:  /usr/bin/python3 -m coverage run --include='*/edition-desk.py,*/image-qc.py,*/edition-to-paper.py' \
        test/test_edition_pipeline.py && /usr/bin/python3 -m coverage report
"""
import argparse, importlib.util, io, json, os, re, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent / "scripts"
FIXTURE = HERE / "fixtures" / "routine-daily.html"
ISSUE10 = HERE.parent.parent / "content" / "articles" / "issue-10" / "images"


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ed = load("edition_desk", "edition-desk.py")
qc = load("image_qc", "image-qc.py")
e2p = load("e2p", "edition-to-paper.py")


def sh(*args, cwd=None):
    subprocess.run(args, cwd=cwd, check=True, capture_output=True)


def args(**kw):
    base = dict(dry_run=False, no_images=True, only=None, retry=False)
    base.update(kw)
    return argparse.Namespace(**base)


class World(unittest.TestCase):
    """A bare origin with daily-pages holding the 10-10 routine page, a clone as REPO, temp content/ops."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="edition-e2e-"))
        origin, seed, repo = self.tmp / "origin.git", self.tmp / "seed", self.tmp / "repo"
        sh("git", "init", "-q", "--bare", str(origin))
        sh("git", "init", "-q", "-b", "daily-pages", str(seed))
        (seed / "anthropic-daily").mkdir()
        shutil.copy(FIXTURE, seed / "anthropic-daily" / "2026-10-10.html")
        shutil.copy(FIXTURE, seed / "anthropic-daily" / "2026-10-01.html")  # before the cutover
        for c in (["add", "-A"], ["-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "seed"],
                  ["remote", "add", "origin", str(origin)], ["push", "-q", "origin", "daily-pages"]):
            sh("git", *c, cwd=seed)
        sh("git", "clone", "-q", str(origin), str(repo))
        self.repo, self.origin = repo, origin
        self.patches = [mock.patch.object(ed, "REPO", repo), mock.patch.object(ed, "EDITIONS", self.tmp / "editions"),
                        mock.patch.object(ed, "PAUSE", self.tmp / "ops" / "PAUSED"),
                        mock.patch.object(ed, "ALERT", self.tmp / "ops" / "ALERT.md"),
                        mock.patch.object(ed, "LOG", self.tmp / "desk.log"),
                        mock.patch.object(ed, "notify", lambda *a: self.toasts.append(a)),
                        mock.patch.object(ed, "verify_live", lambda *a, **k: True)]
        for p in self.patches:
            p.start()
        # Tripwire (2026-10-11 incident): no subprocess in a test may run git inside the real repo,
        # whatever path the code computed, and the real SSH remote is unreachable.
        real_root = str(HERE.parent.parent.resolve())
        real_run = subprocess.run
        def guarded_run(cmd, *a, **kw):
            cwd = str(Path(kw.get("cwd") or os.getcwd()).resolve())
            if cmd and cmd[0] == "git" and (cwd == real_root or cwd.startswith(real_root + os.sep)):
                raise AssertionError(f"test ran git in the real repo: {' '.join(map(str, cmd))}")
            return real_run(cmd, *a, **kw)
        self.patches += [mock.patch.object(ed.subprocess, "run", guarded_run),
                         mock.patch.dict(os.environ, {"GIT_SSH_COMMAND": "false"})]
        for p in self.patches[-2:]:
            p.start()
        url = real_run(["git", "remote", "get-url", "origin"], cwd=repo, capture_output=True, text=True).stdout.strip()
        assert url == str(origin), f"test origin must be the local bare repo, got {url}"
        self.toasts = []
        ed.ESCALATIONS.clear()

    def tearDown(self):
        for p in self.patches:
            p.stop()
        shutil.rmtree(self.tmp, ignore_errors=True)

    def live(self, path="anthropic-daily/2026-10-10.html"):
        sh("git", "fetch", "-q", "origin", "daily-pages", cwd=self.repo)
        return subprocess.run(["git", "show", f"origin/daily-pages:{path}"], cwd=self.repo,
                              capture_output=True, text=True).stdout


class TestDesk(World):
    def test_cutover_filter_skips_earlier_editions(self):
        self.assertEqual(ed.branch_pages()["anthropic-daily"], ["2026-10-10"])

    def test_text_only_publish_end_to_end(self):
        ed.cmd_run(args())
        page = self.live()
        self.assertIn(ed.MARKER, page)
        self.assertIn("The Paper Trail", page)
        self.assertEqual(self.live("anthropic-daily/2026-10-01.html"), FIXTURE.read_text())  # untouched
        st = ed.load_state("anthropic-daily", "2026-10-10")
        self.assertEqual(st["published_images"], [])
        self.assertFalse(ed.ALERT.exists())
        # Second run: nothing to do, no new commit.
        head = subprocess.run(["git", "rev-parse", "origin/daily-pages"], cwd=self.repo, capture_output=True, text=True).stdout
        ed.cmd_run(args())
        self.assertEqual(head, subprocess.run(["git", "rev-parse", "origin/daily-pages"], cwd=self.repo,
                                              capture_output=True, text=True).stdout)

    def test_a_renderer_change_republishes_live_editions(self):
        ed.cmd_run(args())
        real_build = ed.build
        calls = []
        def counting(*a, **k):
            calls.append(a[:2])
            return real_build(*a, **k)
        with mock.patch.object(ed, "build", counting):
            ed.cmd_run(args())
            self.assertEqual(calls, [])  # nothing changed: no rebuild
            with mock.patch.object(ed, "render_key", return_value="new-layout"):
                ed.cmd_run(args())
            self.assertEqual(calls, [("anthropic-daily", "2026-10-10")])  # renderer changed: rebuilt and gated
        self.assertEqual(ed.load_state("anthropic-daily", "2026-10-10")["render_key"], "new-layout")

    def test_approved_images_upgrade_and_are_scoped(self):
        ed.cmd_run(args())
        imgs = ed.folder("anthropic-daily", "2026-10-10") / "images"
        imgs.mkdir()
        shutil.copy(ISSUE10 / "story-3-atkinson.png", imgs / "lead-atkinson.png")
        (imgs / "slots.json").write_text(json.dumps({"lead": {"caption": "A meter.", "alt": "meter", "treatment": "atkinson"}}))
        (imgs / "manifest.json").write_text(json.dumps({"images": {"lead-atkinson.png": {
            "credit": "Public domain", "treatment": "atkinson", "width": 1200, "flags": [],
            "review": {"status": "approved", "by": "Claude QC"}}}}))
        ed.cmd_run(args())
        page = self.live()
        self.assertIn('src="img/2026-10-10/lead-atkinson.png"', page)
        self.assertEqual(subprocess.run(["git", "cat-file", "-e", "origin/daily-pages:anthropic-daily/img/2026-10-10/lead-atkinson.png"],
                                        cwd=self.repo).returncode, 0)
        self.assertEqual(ed.load_state("anthropic-daily", "2026-10-10")["published_images"], ["lead-atkinson.png"])

    def test_pending_image_never_ships(self):
        ed.cmd_run(args())
        imgs = ed.folder("anthropic-daily", "2026-10-10") / "images"
        imgs.mkdir()
        shutil.copy(ISSUE10 / "story-3-atkinson.png", imgs / "lead-atkinson.png")
        (imgs / "slots.json").write_text(json.dumps({"lead": {"caption": "x", "alt": "x"}}))
        (imgs / "manifest.json").write_text(json.dumps({"images": {"lead-atkinson.png": {
            "credit": "Public domain", "treatment": "atkinson", "width": 1200, "flags": [], "review": {"status": "pending"}}}}))
        ed.cmd_run(args())
        self.assertNotIn("img/2026-10-10", self.live())

    def test_routine_republish_is_reconverted(self):
        ed.cmd_run(args())
        seed = self.tmp / "seed"
        page = FIXTURE.read_text().replace("The Small Model Argument", "The Small Model Thesis")
        sh("git", "fetch", "-q", "origin", "daily-pages", cwd=seed)
        sh("git", "reset", "-q", "--hard", "origin/daily-pages", cwd=seed)
        (seed / "anthropic-daily" / "2026-10-10.html").write_text(page)  # the routine overwrites its page
        sh("git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qam", "routine rerun", cwd=seed)
        sh("git", "push", "-q", "origin", "HEAD:daily-pages", cwd=seed)
        ed.cmd_run(args())
        self.assertIn("The Small Model Thesis", self.live())
        self.assertIn(ed.MARKER, self.live())

    def test_gate_failure_holds_alerts_and_does_not_retry(self):
        with mock.patch.object(ed, "parity_gate", return_value=["text missing: x"]):
            ed.cmd_run(args())
            ed.cmd_run(args())
        self.assertNotIn(ed.MARKER, self.live())
        st = ed.load_state("anthropic-daily", "2026-10-10")
        self.assertEqual(st["gate_failure"]["problems"], ["text missing: x"])
        self.assertEqual(len([t for t in self.toasts if "held" in t[1]]), 1)  # held once, not every run
        self.assertTrue(ed.ALERT.exists())
        ed.ESCALATIONS.clear()
        ed.cmd_run(args(retry=True))  # gate now real and passing
        self.assertIn(ed.MARKER, self.live())
        self.assertFalse(ed.ALERT.exists())

    def test_source_parity_failure_holds_the_publish(self):
        with mock.patch.object(ed, "source_parity", return_value=["feature-right: 20 visa forms submitted"]):
            ed.cmd_run(args())
        self.assertNotIn(ed.MARKER, self.live())
        st = ed.load_state("anthropic-daily", "2026-10-10")
        self.assertEqual(st["gate_failure"]["problems"], ["feature-right: 20 visa forms submitted"])
        self.assertTrue(any("gate held" in e for e in ed.ESCALATIONS))
        self.assertTrue(ed.ALERT.exists())

    def test_rollback_case_a_one_publish(self):
        ed.cmd_run(args())
        self.assertIn(ed.MARKER, self.live())
        ed.cmd_rollback(argparse.Namespace(edition="anthropic-daily/2026-10-10"))
        self.assertEqual(self.live(), FIXTURE.read_text())
        self.assertTrue(ed.load_state("anthropic-daily", "2026-10-10")["paused"])
        ed.cmd_run(args())  # paused: the next run must not re-publish
        self.assertEqual(self.live(), FIXTURE.read_text())

    def test_rollback_case_b_text_then_images(self):
        ed.cmd_run(args())
        imgs = ed.folder("anthropic-daily", "2026-10-10") / "images"
        imgs.mkdir()
        shutil.copy(ISSUE10 / "story-3-atkinson.png", imgs / "lead-atkinson.png")
        (imgs / "slots.json").write_text(json.dumps({"lead": {"caption": "A meter on a wall.", "alt": "meter", "treatment": "atkinson"}}))
        (imgs / "manifest.json").write_text(json.dumps({"images": {"lead-atkinson.png": {
            "credit": "Public domain", "treatment": "atkinson", "width": 1200, "flags": [], "review": {"status": "approved"}}}}))
        ed.cmd_run(args())
        self.assertIn("img/2026-10-10/", self.live())
        ed.cmd_rollback(argparse.Namespace(edition="anthropic-daily/2026-10-10"))
        self.assertEqual(self.live(), FIXTURE.read_text())
        self.assertNotEqual(subprocess.run(["git", "cat-file", "-e", "origin/daily-pages:anthropic-daily/img/2026-10-10/lead-atkinson.png"],
                                           cwd=self.repo).returncode, 0)

    def test_rollback_case_c_after_a_desk_revert(self):
        """The 10/11 shape: a desk publish, then a desk-authored revert on top. Rollback must not resurrect the publish."""
        ed.cmd_run(args())
        sh("git", "fetch", "-q", "origin", "daily-pages", cwd=self.repo)
        wt = self.tmp / "rev"
        sh("git", "worktree", "add", "-q", "--detach", str(wt), "origin/daily-pages", cwd=self.repo)
        sh("git", "-c", "user.name=Edition Desk", "-c", "user.email=e@e", "revert", "--no-edit", "HEAD", cwd=wt)
        sh("git", "push", "-q", "origin", "HEAD:daily-pages", cwd=wt)
        self.assertEqual(self.live(), FIXTURE.read_text())
        out = io.StringIO()
        with mock.patch("sys.stdout", out):
            ed.cmd_rollback(argparse.Namespace(edition="anthropic-daily/2026-10-10"))
        self.assertIn("already is the routine's page", out.getvalue())
        self.assertEqual(self.live(), FIXTURE.read_text())

    def sweep(self, extra="<!-- swept -->"):
        """What the 23:00 sweep does: a 'Shipped. bot' commit that rewrites the (paper) page."""
        seed = self.tmp / "sweeper"
        if not seed.exists():
            sh("git", "clone", "-q", "-b", "daily-pages", str(self.origin), str(seed), cwd=self.tmp)
        sh("git", "pull", "-q", "origin", "daily-pages", cwd=seed)
        f = seed / "anthropic-daily" / "2026-10-10.html"
        f.write_text(f.read_text() + extra)
        sh("git", "-c", "user.name=Shipped. bot", "-c", "user.email=b@b", "commit", "-qam", "chore(pages): branch sweep", cwd=seed)
        sh("git", "push", "-q", "origin", "HEAD:daily-pages", cwd=seed)

    def test_rollback_case_d_after_a_bot_sweep_text_only(self):
        ed.cmd_run(args())
        self.sweep()
        self.assertIn(ed.MARKER, self.live())
        ed.cmd_rollback(argparse.Namespace(edition="anthropic-daily/2026-10-10"))
        self.assertEqual(self.live(), FIXTURE.read_text())

    def test_rollback_case_d_after_a_bot_sweep_with_images(self):
        ed.cmd_run(args())
        imgs = ed.folder("anthropic-daily", "2026-10-10") / "images"
        imgs.mkdir()
        shutil.copy(ISSUE10 / "story-3-atkinson.png", imgs / "lead-atkinson.png")
        (imgs / "slots.json").write_text(json.dumps({"lead": {"caption": "A meter on a wall.", "alt": "meter", "treatment": "atkinson"}}))
        (imgs / "manifest.json").write_text(json.dumps({"images": {"lead-atkinson.png": {
            "credit": "Public domain", "treatment": "atkinson", "width": 1200, "flags": [], "review": {"status": "approved"}}}}))
        ed.cmd_run(args())
        self.sweep()
        ed.cmd_rollback(argparse.Namespace(edition="anthropic-daily/2026-10-10"))
        page = self.live()
        self.assertEqual(page, FIXTURE.read_text())
        self.assertNotIn("img/2026-10-10/", page)  # never a page pointing at images that were removed

    def test_rollback_is_wired_into_the_cli(self):
        with mock.patch.object(sys, "argv", ["ed", "rollback", "anthropic-daily/2026-10-10"]), \
             mock.patch.object(ed, "cmd_rollback") as rb:
            ed.main()
        rb.assert_called_once()

    def test_every_gate_in_build_can_hold(self):
        """Deleting any gate call from build() must fail this test."""
        for gate in ("image_gate", "front_check", "link_check", "source_parity", "parity_gate",
                     "front_structure", "inside_structure"):
            with self.subTest(gate=gate):
                shutil.rmtree(ed.EDITIONS, ignore_errors=True)
                with mock.patch.object(ed, gate, return_value=[f"{gate} says no"]):
                    ed.cmd_run(args())
                self.assertNotIn(ed.MARKER, self.live())
                self.assertEqual(ed.load_state("anthropic-daily", "2026-10-10")["gate_failure"]["problems"], [f"{gate} says no"])

    def test_tripwire_catches_the_original_bug(self):
        """Re-introduce the import-time default: the tripwire, not luck, must stop it."""
        real_repo = HERE.parent.parent
        bad = lambda *a, repo=real_repo, check=False: ed.subprocess.run(["git", *a], cwd=repo, capture_output=True, text=True)
        with mock.patch.object(ed, "git", bad):
            with self.assertRaises(AssertionError):
                ed.branch_pages()

    def test_alert_stands_while_an_edition_is_held(self):
        with mock.patch.object(ed, "parity_gate", return_value=["text missing: x"]):
            ed.cmd_run(args())
            ed.ESCALATIONS.clear()
            ed.cmd_run(args())  # quiet run: nothing new escalates, but the edition is still held
        self.assertIn("HELD anthropic-daily/2026-10-10", ed.ALERT.read_text())

    def test_build_crash_persists_hold_and_caps(self):
        with mock.patch.object(ed, "render", side_effect=RuntimeError("boom")):
            ed.cmd_run(args())
            ed.cmd_run(args())
        st = ed.load_state("anthropic-daily", "2026-10-10")
        self.assertTrue(st["gate_failure"]["problems"][0].startswith("build failed: boom"))
        self.assertTrue(st["source_sha"])

    def test_image_attempts_are_capped_across_failures(self):
        calls = []
        def desk(md):
            calls.append(md)
            return False, "no sources"
        with mock.patch.object(ed, "run_image_desk", desk), mock.patch.object(ed, "render", side_effect=RuntimeError("x")):
            for _ in range(6):
                ed.cmd_run(args(no_images=False, retry=True))
        self.assertEqual(len(calls), 3)

    def test_pause_switches(self):
        ed.PAUSE.parent.mkdir(parents=True, exist_ok=True)
        ed.PAUSE.write_text("")
        ed.cmd_run(args())
        self.assertNotIn(ed.MARKER, self.live())
        ed.PAUSE.unlink()
        ed.save_state("anthropic-daily", "2026-10-10", {"paused": True})
        ed.cmd_run(args())
        self.assertNotIn(ed.MARKER, self.live())

    def test_dry_run_writes_preview_only(self):
        ed.cmd_run(args(dry_run=True))
        self.assertNotIn(ed.MARKER, self.live())
        self.assertTrue((ed.folder("anthropic-daily", "2026-10-10") / "preview.html").exists())

    def test_only_filter_and_status_and_review(self):
        ed.cmd_run(args(only="anthropic-daily/2099-01-01"))
        self.assertFalse(ed.folder("anthropic-daily", "2026-10-10").exists())
        ed.cmd_run(args())
        out = io.StringIO()
        with mock.patch("sys.stdout", out):
            ed.cmd_status(args())
        self.assertIn("anthropic-daily/2026-10-10: published_images=[]", out.getvalue())
        with self.assertRaises(SystemExit):
            ed.cmd_review(argparse.Namespace(edition="anthropic-daily/2026-10-10"))
        imgs = ed.folder("anthropic-daily", "2026-10-10") / "images"
        imgs.mkdir()
        (imgs / "manifest.json").write_text('{"images": {}}')
        with mock.patch.object(ed.subprocess, "Popen") as popen, mock.patch.object(ed.os, "execv") as execv:
            ed.cmd_review(argparse.Namespace(edition="anthropic-daily/2026-10-10"))
        self.assertIn("--port", execv.call_args[0][1])
        self.assertIn("openfront", popen.call_args[0][0][2])

    def test_images_then_qc_runs_and_redo_once(self):
        ed.cmd_run(args())
        imgs = ed.folder("anthropic-daily", "2026-10-10") / "images"
        def desk(md):
            imgs.mkdir(exist_ok=True)
            shutil.copy(ISSUE10 / "story-3-atkinson.png", imgs / "lead-atkinson.png")
            (imgs / "slots.json").write_text(json.dumps({"lead": {"caption": "x", "alt": "x", "treatment": "atkinson"}}))
            (imgs / "manifest.json").write_text(json.dumps({"images": {"lead-atkinson.png": {
                "credit": "Public domain", "treatment": "atkinson", "width": 1200, "flags": [], "review": {"status": "pending"}}}}))
            return True, "ok"
        verdicts = iter(["rejected", "approved"])
        def fake_qc(section, stem, st):
            m = json.loads((imgs / "manifest.json").read_text())
            m["images"]["lead-atkinson.png"]["review"]["status"] = next(verdicts)
            (imgs / "manifest.json").write_text(json.dumps(m))
        with mock.patch.object(ed, "run_image_desk", desk), mock.patch.object(ed, "qc", fake_qc):
            ed.cmd_run(args(no_images=False))   # desk + QC rejects
            ed.cmd_run(args(no_images=False))   # one redo + QC approves, publishes with the image
        self.assertIn("img/2026-10-10/lead-atkinson.png", self.live())
        self.assertEqual(ed.load_state("anthropic-daily", "2026-10-10")["redos"], 1)

    def test_qc_wrapper_logs_and_survives_failure(self):
        ed.cmd_run(args())
        imgs = ed.folder("anthropic-daily", "2026-10-10") / "images"
        imgs.mkdir()
        st = {}
        with mock.patch.object(qc, "review", side_effect=RuntimeError("claude down")), \
             mock.patch.object(ed.importlib.util, "module_from_spec", return_value=qc), \
             mock.patch.object(ed.importlib.util, "spec_from_file_location", return_value=mock.Mock()):
            ed.qc("anthropic-daily", "2026-10-10", st)
        self.assertTrue(any("image QC failed" in e for e in ed.ESCALATIONS))
        with mock.patch.object(qc, "review", return_value={"a.png": (True, "ok")}), \
             mock.patch.object(ed.importlib.util, "module_from_spec", return_value=qc), \
             mock.patch.object(ed.importlib.util, "spec_from_file_location", return_value=mock.Mock()):
            ed.qc("anthropic-daily", "2026-10-10", st)
        self.assertIn("qc_at", st)


class TestDeskUnits(unittest.TestCase):
    def test_git_reads_repo_at_call_time(self):
        with mock.patch.object(ed, "REPO", Path("/nonexistent-shipped-repo")):
            with self.assertRaises(FileNotFoundError):
                ed.git("status")


    def test_run_image_desk_flags_and_timeout(self):
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("OPENAI_API_KEY", None)
            with mock.patch.object(ed.subprocess, "run", return_value=mock.Mock(returncode=0, stdout="a\nb\nok", stderr="")) as r:
                ok, tail = ed.run_image_desk(Path("/x/edition.md"))
        self.assertTrue(ok)
        self.assertIn("--no-generate", r.call_args_list[-1][0][0])
        with mock.patch.object(ed.subprocess, "run", side_effect=[mock.Mock(returncode=0), subprocess.TimeoutExpired("x", 1)]):
            self.assertEqual(ed.run_image_desk(Path("/x/edition.md")), (False, "timed out after 30 minutes"))

    def test_press_python_and_free_port(self):
        self.assertTrue(os.path.exists(ed.press_python()))
        with mock.patch.object(ed.subprocess, "run", return_value=mock.Mock(returncode=1)):
            with self.assertRaises(RuntimeError):
                ed.press_python()
        self.assertGreaterEqual(ed.free_port(), 8794)

    def test_render_failure_raises(self):
        with mock.patch.object(ed.subprocess, "run", return_value=mock.Mock(returncode=1, stderr="bad", stdout="")):
            with self.assertRaises(RuntimeError):
                ed.render(Path("a"), Path("b"))

    def test_gates_catch_every_drop(self):
        md = ("---\ntitle: x\n---\n## The Open\n\nAlpha beta gamma delta epsilon zeta eta theta.\n\n"
              "## A. Models\n\n#### 2026-10-07 - Claude Haiku 5.5 ([source](https://x))\n`[MODEL]`\n\nBody here.\n")
        good = ("<title>t</title>" + ed.MARKER + "<p>Alpha beta gamma delta epsilon zeta eta theta.</p>"
                "<a href=\"https://x\"><b>Claude Haiku 5.5</b></a> Body here. <section id=\"subscribe\">https://id8labs.app/api/newsletter/subscribe</section>")
        self.assertEqual(ed.parity_gate(md, good), [])
        self.assertEqual(ed.parity_gate(md, good.replace("https://id8labs.app/api/newsletter/subscribe", "/api/x")),
                         ["subscribe POST url missing"])
        self.assertEqual(ed.parity_gate(md, good.replace("<title>t</title>", "")), ["no <title>"])
        self.assertEqual(ed.parity_gate(md, good.replace('id="subscribe"', "")), ["0 subscribe forms, expected 1"])
        self.assertEqual(ed.parity_gate(md, good.replace("Alpha", "Omega")), ["text missing: Alpha beta gamma delta epsilon zeta eta theta."])

    def test_source_parity_catches_a_converter_drop(self):
        src = FIXTURE.read_text()
        self.assertTrue(any(m.startswith("feature-right") for m in ed.source_parity(src, "<p>nothing</p>")))

    def test_verify_live(self):
        with mock.patch.object(ed, "verify_live", ed.verify_live):
            pass
        real = load("edition_desk_live", "edition-desk.py")
        with mock.patch.object(real.urllib.request, "urlopen",
                               return_value=io.BytesIO(real.MARKER.encode())):
            self.assertTrue(real.verify_live("anthropic-daily", "2026-10-10", wait=5))
        with mock.patch.object(real.urllib.request, "urlopen", side_effect=OSError("down")), \
             mock.patch.object(real.time, "sleep"), mock.patch.object(real.time, "time", side_effect=[0, 1, 99]):
            self.assertFalse(real.verify_live("anthropic-daily", "2026-10-10", wait=5))

    def test_main_dispatch(self):
        with mock.patch.object(sys, "argv", ["ed", "status"]), mock.patch.object(ed, "cmd_status") as st:
            ed.main()
        st.assert_called_once()


class TestGateMutants(unittest.TestCase):
    """The Prometheus L2 mutations (2026-10-11): each must trip a gate. Block ORDER is out of scope:
    the paper front reorders blocks by design (teaser, columns, rail), so order cannot be a rule."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="mutants-"))
        cls.src = FIXTURE.read_text()
        md, _ = e2p.convert(cls.src, "anthropic-daily", "2026-10-10")
        (cls.tmp / "edition.md").write_text(md)
        subprocess.run(["npx", "tsx", "src/render/edition-cli.ts", str(cls.tmp / "edition.md"), str(cls.tmp / "out.html")],
                       cwd=HERE.parent, check=True, capture_output=True)
        cls.page = (cls.tmp / "out.html").read_text()
        cls.md = md

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def problems(self, page):
        return (ed.parity_gate(self.md, page) + ed.source_parity(self.src, page)
                + ed.front_check(ed.split_front(page)[0], self.src, self.md) + ed.link_check(page, self.src, self.md))

    def test_faithful_render_is_clean(self):
        self.assertEqual(self.problems(self.page), [])

    def mutate(self, old, new, count=-1):
        self.assertIn(old, self.page)
        return self.page.replace(old, new) if count < 0 else self.page.replace(old, new, count)

    def test_changed_figure_everywhere(self):
        self.assertTrue(self.problems(self.mutate("72.4%", "74.2%")))

    def test_changed_figure_only_in_the_teaser(self):
        self.assertTrue(self.problems(self.mutate("72.4%", "79.9%", 1)))

    def test_removed_figure(self):
        self.assertTrue(self.problems(self.mutate("20 visa forms submitted", "visa forms submitted")))

    def test_swapped_figures(self):
        swapped = self.page.replace("4 behavior types disclosed", "TMP").replace("1 police tip filed", "4 police tip filed")
        self.assertTrue(self.problems(swapped.replace("TMP", "1 behavior types disclosed")))

    def test_changed_link_and_dropped_duplicate_link(self):
        href = "https://www.anthropic.com/news"
        self.assertTrue(self.problems(self.mutate(f'href="{href}"', 'href="https://example.com"')))
        self.assertTrue(self.problems(self.mutate(f'href="{href}"', 'href="https://example.com"', 1)))

    def test_cut_last_sentence(self):
        self.assertTrue(self.problems(self.mutate(" The small-model tier is a contested space now.", "")))

    def test_front_teaser_figure_changed_only_on_the_front(self):
        front, inside = ed.split_front(self.page)
        self.assertIn("$0.10", front)
        bad = self.page.replace(front, front.replace("$0.10", "$0.50", 1))
        self.assertTrue(ed.front_check(ed.split_front(bad)[0], self.src, self.md))

    def test_front_headline_and_log_box_edits(self):
        front = ed.split_front(self.page)[0]
        for old, new in (("The Paper Trail", "The Paper Trial"), ("Claude Haiku 5.5", "Claude Haiku 6")):
            bad = front.replace(old, new)
            self.assertNotEqual(bad, front)
            self.assertTrue(ed.front_check(bad, self.src, self.md), old)
        self.assertEqual(ed.front_check(front, self.src, self.md), [])

    def test_sentence_cut_inside_but_kept_in_the_teaser(self):
        front, inside = ed.split_front(self.page)
        sent = "The mechanism. The report describes four behavior types."
        self.assertIn(sent, front)
        bad = self.page.replace(inside, inside.replace(sent, "", 1)) if False else front.join(
            [self.page.split(front)[0].replace(sent, ""), self.page.split(front)[1].replace(sent, "")])
        self.assertTrue(ed.source_parity(self.src, bad))

    def test_foreign_link(self):
        href = "https://finance.yahoo.com/technology/ai/articles/anthropic-cites-ai-misbehavior-government-002120323.html"
        bad = self.page.replace(f'href="{href}"', 'href="https://evil.example/x"', 1)
        self.assertEqual(ed.link_check(self.page, self.src, self.md), [])
        self.assertIn("link not in the edition: https://evil.example/x", ed.link_check(bad, self.src, self.md))

    def test_front_structure_mutants(self):
        front = ed.split_front(self.page)[0]
        self.assertEqual(ed.front_structure(front, self.md), [])
        h2 = re.search(r'<header class="pf-head">.*?<h2>(.*?)</h2>', front, re.S).group(1)
        rows = re.findall(r'<div class="pf-row">.*?</div>', front)
        muts = {
            "headline swapped for a story's": front.replace(f"<h2>{h2}</h2>", "<h2>The Small Model Argument</h2>", 1),
            "log date": front.replace("<b>10-08</b>", "<b>10-09</b>", 1),
            "log title cut": front.replace("Anthropic Cyber Mission Launch", "Anthropic Cyber Mission", 1),
            "log rows swapped": front.replace(rows[0], "TMP").replace(rows[1], rows[0]).replace("TMP", rows[1]),
            "log row dropped": front.replace(rows[2], ""),
            "log count": front.replace("8 releases in the log", "9 releases in the log"),
            "ears date": front.replace("Oct 10, 2026", "Oct 11, 2026", 1),
            "deck": front.replace("Every other lab has not.", "Every other lab has.", 1),
        }
        for name, bad in muts.items():
            self.assertNotEqual(bad, front, name)
            self.assertTrue(ed.front_structure(bad, self.md), name)
        blocks = re.findall(r'<div class="pf-story">.*?<h3>(.*?)</h3>', front, re.S)
        swapped = front.replace(f"<h3>{blocks[0]}</h3>", "<h3>TMP</h3>").replace(f"<h3>{blocks[1]}</h3>", f"<h3>{blocks[0]}</h3>").replace("<h3>TMP</h3>", f"<h3>{blocks[1]}</h3>")
        self.assertTrue(ed.front_structure(swapped, self.md), "story headlines swapped")

    def test_wrong_article_link_and_inside_title_swap(self):
        # Point one link at ANOTHER URL this edition really uses: only the pair check can see it.
        hrefs = sorted(h for h in set(re.findall(r'href="(https://[^"]+)"', self.src)) - ed.CHROME_HREFS
                       if f'href="{h}"' in self.page)
        a_href, b_href = hrefs[0], hrefs[1]
        bad = self.page.replace(f'href="{a_href}"', f'href="{b_href}"', 1)
        self.assertNotEqual(bad, self.page)
        self.assertTrue(any("points elsewhere" in x for x in ed.link_check(bad, self.src, self.md)))
        a, b = "The Small Model Argument", "The Offense-Defense Budget"
        front = ed.split_front(self.page)[0]
        cut = self.page.index(front) + len(front)
        after = self.page[cut:]
        swapped = self.page[:cut] + after.replace(a, "TMP").replace(b, a).replace("TMP", b)
        self.assertNotEqual(swapped, self.page)
        self.assertTrue(any("out of order" in x for x in ed.source_parity(self.src, swapped)))

    def test_shared_figure_and_alt(self):
        imgs = self.tmp / "imgs3"
        imgs.mkdir(exist_ok=True)
        (imgs / "slots.json").write_text(json.dumps({"lead": {"caption": "C.", "alt": "a stamp"}, "cover": {"caption": "D."}}))
        (imgs / "manifest.json").write_text(json.dumps({"images": {"lead-atkinson.png": {"credit": "PD"}}}))
        fig = '<figure class="pf-fig "><img src="img/lead-atkinson.png" alt="a stamp"><img src="img/cover-atkinson.png"><figcaption>C. <i>PD.</i></figcaption></figure>'
        self.assertTrue(any("shares a figure" in x for x in ed.image_gate(fig, ["lead-atkinson.png"], imgs)))
        ok = fig.replace('<img src="img/cover-atkinson.png">', "")
        self.assertEqual(ed.image_gate(ok, ["lead-atkinson.png"], imgs), [])
        self.assertTrue(any("alt text" in x for x in ed.image_gate(ok.replace("a stamp", "a meter"), ["lead-atkinson.png"], imgs)))
        # Apostrophes: every spelling a renderer may use passes; a different alt still holds.
        (imgs / "slots.json").write_text(json.dumps({"lead": {"caption": "C.", "alt": "the judge's chair"}}))
        for spelled in ("the judge&apos;s chair", "the judge&#x27;s chair", "the judge's chair"):
            self.assertEqual(ed.image_gate(ok.replace('alt="a stamp"', f'alt="{spelled}"'), ["lead-atkinson.png"], imgs), [], spelled)
        self.assertTrue(ed.image_gate(ok.replace('alt="a stamp"', 'alt="the judge&apos;s desk"'), ["lead-atkinson.png"], imgs))

    def test_inside_binding_mutants(self):
        """Words in the right place: swaps between log entries or stories, with nothing added or lost."""
        self.assertEqual(ed.inside_structure(self.page, self.md), [])
        cut = self.page.index(ed.split_front(self.page)[0]) + len(ed.split_front(self.page)[0])
        head, inside = self.page[:cut], self.page[cut:]
        def swap(text, a, b):
            self.assertIn(a, text); self.assertIn(b, text)
            return text.replace(a, "\x00").replace(b, a).replace("\x00", b)
        bodies = re.findall(r'<p class="log-entry-body">(.*?)</p>', inside, re.S)
        titles = re.findall(r'<h3 class="log-entry-title">(.*?)</h3>', inside, re.S)
        dates = re.findall(r'<span class="log-entry-date">(.*?)</span>', inside, re.S)
        story = re.findall(r"<h3 style=[^>]*>(.*?)</h3>", inside)
        muts = {
            "log bodies swapped": swap(inside, bodies[0], bodies[1]),
            "log titles+links swapped": swap(inside, titles[0], titles[3]),
            "log date changed": inside.replace(dates[0], dates[0].replace("07", "08"), 1),
            "log tag changed": re.sub(r'(<span class="log-tag[^"]*">)[^<]*', r"\1News", inside, count=1),
            "story headings swapped": swap(inside, story[0], story[1]),
        }
        hows = re.findall(r'<div class="log-entry-how">(.*?)</div>', inside, re.S)
        if len(hows) > 1:
            muts["how-to swapped"] = swap(inside, hows[0], hows[1])
        lead_p = re.search(r'<div class="prose drop-cap[^"]*">\s*<p>(.*?)</p>', inside, re.S).group(1)
        also_p = re.search(r"<h3 style=[^>]*>.*?</h3>\s*<p>(.*?)</p>", inside, re.S).group(1)
        muts["lead paragraph swapped with a story's"] = swap(inside, lead_p, also_p)
        for name, bad in muts.items():
            self.assertNotEqual(bad, inside, name)
            self.assertTrue(ed.inside_structure(head + bad, self.md), name)

    def test_figures_swapped_or_recaptioned(self):
        imgs = self.tmp / "imgs2"
        imgs.mkdir(exist_ok=True)
        (imgs / "slots.json").write_text(json.dumps({"story-1": {"caption": "A gear train."}, "story-2": {"caption": "A substation."}}))
        (imgs / "manifest.json").write_text(json.dumps({"images": {"story-1-atkinson.png": {"credit": "R. S., CC BY 2.0"},
                                                                   "story-2-atkinson.png": {"credit": "N., CC BY 4.0"}}}))
        fig = lambda f, cap: f'<figure class="pf-fig "><img src="img/{f}"><figcaption class="pf-cap">{cap}</figcaption></figure>'
        good = fig("story-1-atkinson.png", "A gear train. <i>R. S., CC BY 2.0.</i>") + fig("story-2-atkinson.png", "A substation. <i>N., CC BY 4.0.</i>")
        want = ["story-1-atkinson.png", "story-2-atkinson.png"]
        self.assertEqual(ed.image_gate(good, want, imgs), [])
        swapped = good.replace("story-1-atkinson", "TMP").replace("story-2-atkinson", "story-1-atkinson").replace("TMP", "story-2-atkinson")
        self.assertEqual(len(ed.image_gate(swapped, want, imgs)), 2)
        self.assertTrue(ed.image_gate(good.replace("R. S., CC BY 2.0", "Unknown"), want, imgs))
        self.assertTrue(ed.image_gate(good.replace(" <i>R. S., CC BY 2.0.</i>", ""), want, imgs))

    def test_image_gate(self):
        imgs = self.tmp / "images"
        imgs.mkdir(exist_ok=True)
        (imgs / "slots.json").write_text(json.dumps({"lead": {"caption": "A stamp with 12 wheels."}}))
        (imgs / "manifest.json").write_text(json.dumps({"images": {"lead-atkinson.png": {"credit": "Public domain"}}}))
        fig = '<figure class="pf-fig "><img src="img/lead-atkinson.png"><figcaption class="pf-cap">A stamp with 12 wheels. <i>Public domain.</i></figcaption></figure>'
        self.assertEqual(ed.image_gate(self.page + fig, ["lead-atkinson.png"], imgs), [])
        self.assertTrue(ed.image_gate(self.page + fig.replace("12 wheels", "13 wheels"), ["lead-atkinson.png"], imgs))
        self.assertEqual(ed.image_gate(self.page, ["lead-atkinson.png"], imgs), ["image missing: lead-atkinson.png"])


class TestConverter(unittest.TestCase):
    def test_dates_and_fact_box(self):
        self.assertEqual(e2p.iso_date("anthropic-weekly", "2026-41"), "2026-10-09")
        self.assertEqual(e2p.iso_date("anthropic-monthly", "2026-09"), "2026-09-30")
        md, summary = e2p.convert(FIXTURE.read_text(), "anthropic-daily", "2026-10-10")
        self.assertIn("**By the numbers:** 4 behavior types disclosed;", md)
        self.assertRegex(md, r"\*Source:\*?\*? \[?Yahoo Finance")
        self.assertIn("*What is next*", md)
        self.assertEqual(summary["log_entries"], 8)

    def test_bare_label_fact_box(self):
        page = FIXTURE.read_text()
        i = page.index('<div class="feature-meta">')
        j = page.index("</div>", i) + 6
        page = page[:i] + '<div class="feature-meta"><b>Area:</b> Security &nbsp; <b>Dates:</b> October 8 to 9, 2026</div>' + page[j:]
        md, _ = e2p.convert(page, "anthropic-daily", "2026-10-10")
        self.assertIn("Dates: October 8 to 9, 2026", md.replace("**", ""))

    def test_empty_page_refused(self):
        with self.assertRaises(SystemExit):
            e2p.convert("<html><body><p>x</p></body></html>", "anthropic-daily", "2026-10-10")


class TestLauncher(unittest.TestCase):
    """The real launcher under a fake HOME: args reach the desk, the lock holds, a stale lock clears."""

    def setUp(self):
        self.home = Path(tempfile.mkdtemp(prefix="launcher-home-"))
        origin = self.home / "origin.git"
        main = self.home / "Development" / "id8" / "shipped"
        sh("git", "init", "-q", "--bare", "-b", "main", str(origin))
        (main / "pipeline" / "scripts").mkdir(parents=True)
        (main / "pipeline" / "node_modules").mkdir()
        (main / "pipeline" / "scripts" / "edition-desk.py").write_text(
            "import sys, os, json\nopen(os.environ['SHIPPED_OPS'] + '/argv.json', 'w').write(json.dumps(sys.argv[1:]))\n")
        sh("git", "init", "-q", "-b", "main", str(main))
        for c in (["add", "-A"], ["-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "stub"],
                  ["remote", "add", "origin", str(origin)], ["push", "-q", "origin", "main"]):
            sh("git", *c, cwd=main)
        self.main = main
        self.env = {**os.environ, "HOME": str(self.home), "EDITION_DESK_QUIET": "1"}  # no real notifications from tests
        self.env.pop("GIT_SSH_COMMAND", None)

    def tearDown(self):
        shutil.rmtree(self.home, ignore_errors=True)

    def launch(self, *a):
        return subprocess.run(["/bin/bash", str(SCRIPTS / "edition-desk-launch.sh"), *a], env=self.env,
                              capture_output=True, text=True, timeout=120)

    def test_args_reach_the_desk_from_the_clean_worktree(self):
        r = self.launch("--only", "anthropic-daily/2026-10-10")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads((self.main / "ops" / "argv.json").read_text()), ["run", "--only", "anthropic-daily/2026-10-10"])
        self.assertTrue((self.home / "Development" / ".worktrees" / "shipped" / "edition-desk" / ".git").exists())

    def test_lock_and_stale_lock(self):
        lock = self.main / "ops" / ".edition-desk.lock"
        lock.mkdir(parents=True)
        r = self.launch()
        self.assertIn("another Edition Desk run holds", r.stdout)
        self.assertFalse((self.main / "ops" / "argv.json").exists())
        old = 1_000_000_000
        os.utime(lock, (old, old))
        r = self.launch()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue((self.main / "ops" / "argv.json").exists())
        self.assertIn("stale lock cleared", (self.main / "ops" / "EDITION-DESK-LAUNCHER-ALERT.md").read_text())

    def test_failure_writes_the_sticky_alert(self):
        (self.main / "pipeline" / "scripts" / "edition-desk.py").write_text("import sys; sys.exit(3)\n")
        sh("git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qam", "broken desk", cwd=self.main)
        sh("git", "push", "-q", "origin", "main", cwd=self.main)
        alert = self.main / "ops" / "EDITION-DESK-LAUNCHER-ALERT.md"
        self.assertEqual(self.launch().returncode, 1)
        self.assertEqual(self.launch().returncode, 1)
        self.assertEqual(alert.read_text().count("launcher failed: edition-desk.py exited"), 2)  # appended, not overwritten

    def test_pause(self):
        (self.main / "ops").mkdir()
        (self.main / "ops" / "EDITION-DESK-PAUSED").write_text("")
        self.assertIn("paused", self.launch().stdout)
        self.assertFalse((self.main / "ops" / "argv.json").exists())


class TestQC(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="qc-test-"))
        self.imgs = self.tmp / "images"
        (self.imgs / "src").mkdir(parents=True)
        for f in ("cover-atkinson.png", "cover-halftone.png", "story-3-atkinson.png"):
            shutil.copy(ISSUE10 / f, self.imgs / f)
        shutil.copy(ISSUE10 / "src" / "cover.jpg", self.imgs / "src" / "cover.jpg")
        (self.imgs / "src" / "credits.json").write_text(json.dumps({"cover": {"title": "A knife switch", "url": "u"}}))
        (self.imgs / "slots.json").write_text(json.dumps({"cover": {"caption": "A knife switch."},
                                                          "story-3": {"caption": "A meter."}}))
        entry = lambda: {"credit": "Public domain", "license": "pd", "treatment": "atkinson", "width": 1200,
                         "flags": [], "review": {"status": "pending"}}
        (self.imgs / "manifest.json").write_text(json.dumps({"images": {
            "cover-atkinson.png": entry(), "cover-halftone.png": {**entry(), "treatment": "halftone", "width": 1600},
            "story-3-atkinson.png": {**entry(), "credit": ""}}}))
        self.md = self.tmp / "edition.md"
        self.md.write_text("---\nt: x\n---\n## The Open\n\nOpen text.\n\n## The Lead Story\n\n# Lead\n\nLead text.\n\n"
                           "## Also Shipped\n\n### One\n\nA.\n\n### Two\n\nB.\n\n### Three\n\nC.\n")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def claude(self, scores):
        return mock.Mock(returncode=0, stdout=json.dumps({"result": "ok " + json.dumps(scores)}), stderr="")

    def test_story_context_and_records(self):
        self.assertIn("Open text", qc.story_context(str(self.md), "cover"))
        self.assertIn("Lead text", qc.story_context(str(self.md), "lead"))
        self.assertEqual(qc.story_context(str(self.md), "story-3").strip(), "Three\n\nC.")
        self.assertEqual(qc.story_context(str(self.md), "story-9"), "")
        self.assertEqual(qc.story_context(None, "cover"), "")
        self.assertEqual(qc.record_for(self.imgs, "cover"), "A knife switch u")
        self.assertIsNone(qc.source_for(self.imgs, "story-3"))

    def test_hard_checks(self):
        self.assertEqual(qc.hard_checks({"flags": ["flooded: 20% of the frame is solid ink"], "credit": "x"}), [])
        self.assertEqual(len(qc.hard_checks({"flags": ["flooded: 30% of the frame is solid ink"], "credit": "x"})), 1)
        self.assertIn("generated image not labeled AI-generated",
                      qc.hard_checks({"credit": "Illustration", "license": "generated"}))

    def test_verdict_gate(self):
        good = {"legibility": 3, "look": 2, "relevance": 3, "caption_truth": 3, "taste": 2, "hard_faults": [], "note": "n"}
        self.assertTrue(qc.verdict(good, [])[0])
        self.assertFalse(qc.verdict({**good, "legibility": 2}, [])[0])
        self.assertFalse(qc.verdict({**good, "look": 1}, [])[0])
        self.assertFalse(qc.verdict({**good, "hard_faults": ["logo"]}, [])[0])

    def test_grade_parses_and_fails_loud(self):
        sc = {"legibility": 5, "look": 4, "relevance": 4, "caption_truth": 5, "taste": 4, "hard_faults": [" "], "note": "n"}
        with mock.patch.object(qc.subprocess, "run", return_value=self.claude(sc)):
            g = qc.grade("p.png", None, "lead", 'a "q"', "c", "")
        self.assertEqual(g["hard_faults"], [])
        with mock.patch.object(qc.subprocess, "run", return_value=mock.Mock(returncode=1, stderr="x", stdout="")):
            with self.assertRaises(RuntimeError):
                qc.grade("p.png", None, "cover", "", "", "")
        with mock.patch.object(qc.subprocess, "run", return_value=mock.Mock(returncode=0, stdout='{"result": "no"}', stderr="")):
            with self.assertRaises(RuntimeError):
                qc.grade("p.png", None, "story-1", "", "", "")

    def test_gate_thresholds_are_the_calibrated_ones(self):
        self.assertEqual(qc.GATE, {"legibility": 3, "relevance": 3, "caption_truth": 3, "look": 2, "taste": 2})

    def test_doubted_caption_without_a_fix_is_capped_and_rejected(self):
        sc = {"legibility": 5, "look": 5, "relevance": 5, "caption_truth": 4, "taste": 5, "hard_faults": [], "note": "n"}
        with mock.patch.object(qc.subprocess, "run", return_value=self.claude(sc)):
            g = qc.grade("p.png", None, "lead", "x", "c", "")
        self.assertEqual(g["caption_truth"], 2)
        self.assertFalse(qc.verdict(g, [])[0])
        with mock.patch.object(qc.subprocess, "run", return_value=self.claude({**sc, "caption_fix": "A better caption."})):
            g = qc.grade("p.png", None, "lead", "x", "c", "")
        self.assertEqual(g["caption_truth"], 4)
        self.assertTrue(qc.verdict(g, [])[0])

    def test_review_writes_the_caption_fix(self):
        sc = {"legibility": 5, "look": 5, "relevance": 5, "caption_truth": 4, "taste": 5, "hard_faults": [],
              "caption_fix": "A knife switch on a panel.", "note": "n"}
        with mock.patch.object(qc.subprocess, "run", side_effect=[self.claude(sc), self.claude(sc)]):
            qc.review(self.imgs, str(self.md), log=lambda *_: None)
        slots = json.loads((self.imgs / "slots.json").read_text())
        self.assertEqual(slots["cover"]["caption"], "A knife switch on a panel.")
        self.assertEqual(slots["cover"]["caption_was"], "A knife switch.")

    def test_review_writes_calls_and_picks(self):
        hi = {"legibility": 5, "look": 5, "relevance": 5, "caption_truth": 5, "taste": 5, "hard_faults": [], "note": "h"}
        lo = {**hi, "look": 4}
        with mock.patch.object(qc.subprocess, "run", side_effect=[self.claude(lo), self.claude(hi)]):
            res = qc.review(self.imgs, str(self.md), log=lambda *_: None)
        self.assertTrue(res["cover-atkinson.png"][0] and res["cover-halftone.png"][0])
        self.assertFalse(res["story-3-atkinson.png"][0])  # no credit: hard reject, no model call
        m = json.loads((self.imgs / "manifest.json").read_text())["images"]
        self.assertEqual(m["cover-halftone.png"]["review"]["by"], "Claude QC")
        self.assertEqual(json.loads((self.imgs / "slots.json").read_text())["cover"]["treatment"], "halftone")
        self.assertEqual(qc.review(self.imgs, str(self.md), log=lambda *_: None), {})  # nothing pending

    def test_review_picks_atkinson_when_halftone_fails_and_dry_run(self):
        ok = {"legibility": 4, "look": 3, "relevance": 4, "caption_truth": 4, "taste": 4, "hard_faults": [], "note": "o"}
        bad = {**ok, "legibility": 1}
        with mock.patch.object(qc.subprocess, "run", side_effect=[self.claude(ok), self.claude(bad)]):
            qc.review(self.imgs, str(self.md), dry=True, log=lambda *_: None)
        self.assertEqual(json.loads((self.imgs / "manifest.json").read_text())["images"]["cover-atkinson.png"]["review"]["status"], "pending")
        with mock.patch.object(qc.subprocess, "run", side_effect=[self.claude(ok), self.claude(bad)]):
            qc.review(self.imgs, str(self.md), log=lambda *_: None)
        self.assertEqual(json.loads((self.imgs / "slots.json").read_text())["cover"]["treatment"], "atkinson")

    def test_decoys_and_calibrate(self):
        out = qc.decoys(self.tmp)
        self.assertEqual(len(out), 6)
        good = {"legibility": 4, "look": 3, "relevance": 4, "caption_truth": 4, "taste": 4, "hard_faults": [], "note": "g"}
        bad = {**good, "legibility": 1}
        def grade(printed, *a, **k):
            return dict(bad if "qc-decoys" in printed else good)
        with mock.patch.object(qc, "grade", grade), mock.patch.object(qc, "OUTPUT", self.tmp / "output"):
            with self.assertRaises(SystemExit) as e, mock.patch("sys.stdout", io.StringIO()):
                qc.cmd_calibrate(argparse.Namespace(model="opus"))
        self.assertEqual(e.exception.code, 0)
        with mock.patch.object(qc, "grade", lambda *a, **k: dict(good)), mock.patch.object(qc, "OUTPUT", self.tmp / "output"):
            with self.assertRaises(SystemExit) as e, mock.patch("sys.stdout", io.StringIO()):
                qc.cmd_calibrate(argparse.Namespace(model="opus"))
        self.assertEqual(e.exception.code, 1)  # a grader that approves decoys fails calibration

    def test_cli(self):
        with mock.patch.object(qc, "review", return_value={"a": (True, ""), "b": (False, "")}), \
             mock.patch.object(sys, "argv", ["qc", "review", str(self.imgs), "--dry-run"]), \
             mock.patch("sys.stdout", io.StringIO()) as out:
            qc.main()
        self.assertIn("1 approved, 1 rejected", out.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=1)
