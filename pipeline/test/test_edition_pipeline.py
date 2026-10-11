#!/usr/bin/env python3
"""Edition Desk + image QC, end to end against a throwaway origin. Only the network, Claude and the
image sourcing are mocked; git, the converter, the renderer and the gates run for real.

run:  /usr/bin/python3 -m coverage run --include='*/edition-desk.py,*/image-qc.py,*/edition-to-paper.py' \
        test/test_edition_pipeline.py && /usr/bin/python3 -m coverage report
"""
import argparse, importlib.util, io, json, os, shutil, subprocess, sys, tempfile, unittest
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

    def test_tripwire_catches_the_original_bug(self):
        """Re-introduce the import-time default: the tripwire, not luck, must stop it."""
        real_repo = HERE.parent.parent
        bad = lambda *a, repo=real_repo, check=False: ed.subprocess.run(["git", *a], cwd=repo, capture_output=True, text=True)
        with mock.patch.object(ed, "git", bad):
            with self.assertRaises(AssertionError):
                ed.branch_pages()

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
                "<b>Claude Haiku 5.5</b> Body here. <section id=\"subscribe\">https://id8labs.app/api/newsletter/subscribe</section>")
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


class TestConverter(unittest.TestCase):
    def test_dates_and_fact_box(self):
        self.assertEqual(e2p.iso_date("anthropic-weekly", "2026-41"), "2026-10-09")
        self.assertEqual(e2p.iso_date("anthropic-monthly", "2026-09"), "2026-09-30")
        md, summary = e2p.convert(FIXTURE.read_text(), "anthropic-daily", "2026-10-10")
        self.assertIn("**By the numbers:** 4 behavior types disclosed;", md)
        self.assertRegex(md, r"\*Source:\*?\*? \[?Yahoo Finance")
        self.assertIn("*What is next*", md)
        self.assertEqual(summary["log_entries"], 8)

    def test_empty_page_refused(self):
        with self.assertRaises(SystemExit):
            e2p.convert("<html><body><p>x</p></body></html>", "anthropic-daily", "2026-10-10")


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
