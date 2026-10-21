#!/usr/bin/env python3
"""Edition Desk, the markdown route: the routine pushes <section>/src/<stem>.md and no HTML page.

Same harness as test_edition_pipeline.py (a throwaway bare origin, the real converter, renderer and
gates, the git tripwire); only notify, verify_live and the image sourcing are mocked.

run:  /usr/bin/python3 test/test-edition-md-route.py
"""
import argparse, re, subprocess, sys, unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from test_edition_pipeline import World, ed, args, sh  # noqa: E402

FIX = HERE / "fixtures" / "shadow"
SEC, STEM = "anthropic-daily", "2026-10-15"
ONLY = f"{SEC}/{STEM}"
BODY = (FIX / "edition.md").read_text().split("\n---\n", 1)[1]
GOOD = ('---\ndate: 2026-10-15\ntitle: "Shipped., Thursday, October 15, 2026"\n'
        'deck: "Meta releases 816 billion parameters for free, and the rest of the frontier recalibrates."\n'
        'period: "Oct 14 to Oct 15"\nweather: "The race is not only about who ships the best model anymore."\n---\n' + BODY)
FREEFORM = (FIX / "routine-2026-10-12.md").read_text()
GROK_URL = "https://siliconangle.com/2026/10/14/grok-voice-3-0-from-spacexsi-outscores-openai-and-google-on-speech-to-speech-index/"


class MdWorld(World):
    def push_md(self, text, stem=STEM, msg="routine md"):
        seed = self.tmp / "seed"
        sh("git", "pull", "-q", "--ff-only", "origin", "daily-pages", cwd=seed)  # the desk may have pushed
        (seed / SEC / "src").mkdir(parents=True, exist_ok=True)
        (seed / SEC / "src" / f"{stem}.md").write_text(text)
        sh("git", "add", "-A", cwd=seed)
        sh("git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", msg, cwd=seed)
        sh("git", "push", "-q", "origin", "HEAD:daily-pages", cwd=seed)

    def head(self):
        sh("git", "fetch", "-q", "origin", "daily-pages", cwd=self.repo)
        return subprocess.run(["git", "rev-parse", "origin/daily-pages"], cwd=self.repo,
                              capture_output=True, text=True).stdout.strip()

    def page(self, stem=STEM):
        return self.live(f"{SEC}/{stem}.html")

    def run_desk(self, **kw):
        ed.cmd_run(args(only=kw.pop("only", ONLY), **kw))


class TestMdRoute(MdWorld):
    def test_md_only_edition_is_discovered(self):
        self.assertNotIn(STEM, ed.branch_pages()[SEC])
        self.push_md(GOOD)
        self.assertIn(STEM, ed.branch_pages()[SEC])
        self.assertIn("2026-10-10", ed.branch_pages()[SEC])  # the HTML pages are still listed

    def test_md_only_build_publishes(self):
        self.push_md(GOOD)
        self.run_desk()
        page = self.page()
        self.assertIn(ed.MARKER, page)
        self.assertIn("816 Billion Free", page)
        st = ed.load_state(SEC, STEM)
        self.assertEqual(st["route"], "md")
        self.assertTrue(st["source_sha"].startswith("md:"))
        self.assertEqual(st["converted"]["route"], "md")
        self.assertEqual(st["published_images"], [])
        self.assertNotIn("gate_failure", st)
        self.assertFalse((ed.folder(SEC, STEM) / "source.html").exists())
        self.assertFalse(ed.ALERT.exists())
        self.assertEqual(self.toasts, [])
        # A second run with nothing new pushes nothing: our page on the branch is not a reason to rebuild.
        before = self.head()
        self.run_desk()
        self.assertEqual(before, self.head())

    def test_a_new_md_version_rebuilds(self):
        self.push_md(GOOD)
        self.run_desk()
        self.push_md(GOOD.replace("The quiet is the story.", "The silence is the story."), msg="routine re-push")
        self.run_desk()
        self.assertIn("The silence is the story.", self.page())

    def test_shape_failure_holds_once_per_md_version(self):
        self.push_md(FREEFORM)
        calls = []
        real = ed.md_convert
        with mock.patch.object(ed, "md_convert", lambda *a: (calls.append(1), real(*a))[1]):
            self.run_desk()
            self.assertEqual(len(calls), 1)
            self.assertEqual(len(self.toasts), 1)
            self.assertTrue(any("md shape held" in e for e in ed.ESCALATIONS))
            st = ed.load_state(SEC, STEM)
            self.assertEqual(st["shape_failure"]["key"], ed.md_key(FREEFORM))
            self.assertIn("anthropic-daily/2026-10-15: md shape held", ed.ALERT.read_text())
            self.assertEqual(self.page(), "")  # nothing published
            # Same markdown, next tick: no re-check, no new toast, but the alert stands.
            ed.ESCALATIONS.clear()
            self.run_desk()
            self.assertEqual(len(calls), 1)
            self.assertEqual(len(self.toasts), 1)
            self.assertIn("HELD anthropic-daily/2026-10-15", ed.ALERT.read_text())
            # --retry re-checks it once (and holds again).
            self.run_desk(retry=True)
            self.assertEqual(len(calls), 2)
            # A new markdown version in the right shape publishes and clears the hold.
            self.push_md(GOOD, msg="fixed md")
            ed.ESCALATIONS.clear()
            self.run_desk()
        self.assertEqual(len(calls), 3)
        self.assertIn(ed.MARKER, self.page())
        self.assertNotIn("shape_failure", ed.load_state(SEC, STEM))
        self.assertFalse(ed.ALERT.exists())

    def mutated_render(self, old, new):
        real = ed.render

        def render(md, out):
            real(md, out)
            page = Path(out).read_text()
            assert old in page, f"mutation target not in the render: {old[:60]}"
            Path(out).write_text(page.replace(old, new))
        return mock.patch.object(ed, "render", render)

    def assert_held(self, *needles):
        self.assertNotIn(ed.MARKER, self.page())
        st = ed.load_state(SEC, STEM)
        joined = " | ".join(st["gate_failure"]["problems"])
        for n in needles:
            self.assertIn(n, joined)
        self.assertTrue(any("gate held" in e for e in ed.ESCALATIONS))

    def test_dropped_story_text_holds(self):
        self.push_md(GOOD)
        with self.mutated_render("xAI says the model handles millions of conversations per day in Tesla vehicles.", ""):
            self.run_desk()
        self.assert_held("text missing: xAI released Grok Voice 3.0")

    def test_dropped_story_holds(self):
        """The whole Grok Voice story missing from the rendered page (the shadow's DISAGREE case)."""
        self.push_md(GOOD)
        real = ed.render

        def render(md, out):
            real(md, out)
            page = Path(out).read_text()
            cut = re.sub(r"<(h[1-4])[^>]*>[^<]*Grok Voice 3\.0 Ships.*?</\1>", "", page, flags=re.S)
            cut = cut.replace("xAI released Grok Voice 3.0 on October 14 in its Voice Agent API.", "")
            assert cut != page
            Path(out).write_text(cut)
        with mock.patch.object(ed, "render", render):
            self.run_desk()
        self.assert_held()

    def test_dropped_source_link_holds(self):
        self.push_md(GOOD)
        with self.mutated_render(GROK_URL, "https://example.com/elsewhere"):
            self.run_desk()
        self.assert_held()

    def test_every_md_route_gate_can_hold(self):
        """Deleting any gate call from the markdown route of build() must fail this test."""
        self.push_md(GOOD)
        for gate in ("parity_gate", "md_figures", "image_gate", "front_check", "link_check",
                     "front_structure", "inside_structure"):
            with self.subTest(gate=gate):
                import shutil
                shutil.rmtree(ed.EDITIONS, ignore_errors=True)
                with mock.patch.object(ed, gate, return_value=[f"{gate} says no"]):
                    self.run_desk()
                self.assertNotIn(ed.MARKER, self.page())
                self.assertEqual(ed.load_state(SEC, STEM)["gate_failure"]["problems"], [f"{gate} says no"])

    def test_md_route_never_uses_the_source_html_gates(self):
        self.push_md(GOOD)
        with mock.patch.object(ed, "source_parity", side_effect=AssertionError("html gate on md route")), \
             mock.patch.object(ed, "source_coverage", side_effect=AssertionError("html gate on md route")), \
             mock.patch.object(ed, "convert", side_effect=AssertionError("html converter on md route")), \
             mock.patch.object(ed, "shadow", side_effect=AssertionError("shadow on md route")):
            self.run_desk()
        self.assertIn(ed.MARKER, self.page())

    def test_dry_run_on_md_route_previews_and_pushes_nothing(self):
        self.push_md(GOOD)
        before = self.head()
        self.run_desk(dry_run=True)
        self.assertEqual(before, self.head())
        self.assertTrue((ed.folder(SEC, STEM) / "preview.html").exists())
        self.assertNotIn("published_images", ed.load_state(SEC, STEM))

    def test_md_images_are_published_and_scoped(self):
        """Approved images go out with an md-route edition the same way as on the HTML route."""
        self.push_md(GOOD)
        calls = []

        def fake_images(section, stem, st):
            calls.append((section, stem))
        with mock.patch.object(ed, "images", fake_images), \
             mock.patch.object(ed, "ready_set", return_value=[]):
            self.run_desk(no_images=False)
        self.assertEqual(calls, [(SEC, STEM)])
        self.assertIn(ed.MARKER, self.page())


class TestBothPresent(MdWorld):
    """A routine HTML page and a routine md for the same edition: today's HTML route plus the shadow."""

    def test_both_present_keeps_the_html_route(self):
        self.push_md(GOOD, stem="2026-10-10")
        conv, shad = [], []
        real_convert = ed.convert
        with mock.patch.object(ed, "convert", lambda *a: (conv.append(1), real_convert(*a))[1]), \
             mock.patch.object(ed, "shadow", lambda *a: shad.append(a[:2])), \
             mock.patch.object(ed, "md_convert", side_effect=AssertionError("md route taken")):
            self.run_desk(only=f"{SEC}/2026-10-10")
            self.assertEqual(len(conv), 1)
            self.assertEqual(shad, [(SEC, "2026-10-10")])
            st = ed.load_state(SEC, "2026-10-10")
            self.assertEqual(st["route"], "html")
            self.assertFalse(st["source_sha"].startswith("md:"))
            self.assertIn(ed.MARKER, self.page("2026-10-10"))
            # Next tick our paper page is on the branch: still the HTML route, nothing re-converted.
            before = self.head()
            self.run_desk(only=f"{SEC}/2026-10-10")
            self.assertEqual(len(conv), 1)
            self.assertEqual(before, self.head())
            self.assertEqual(ed.load_state(SEC, "2026-10-10")["route"], "html")

    def test_md_route_choice(self):
        with mock.patch.object(ed, "routine_md", return_value=GOOD):
            self.assertEqual(ed.md_route(SEC, STEM, "", {}), GOOD)                         # md only
            self.assertEqual(ed.md_route(SEC, STEM, "<html>routine</html>", {}), "")       # routine page
            self.assertEqual(ed.md_route(SEC, STEM, ed.MARKER, {"route": "md"}), GOOD)    # our md page
            d = ed.folder(SEC, STEM)
            d.mkdir(parents=True)
            (d / "source.html").write_text("<html/>")
            self.assertEqual(ed.md_route(SEC, STEM, ed.MARKER, {}), "")                    # legacy HTML edition
            self.assertEqual(ed.md_route(SEC, STEM, ed.MARKER, {"route": "html"}), "")


class TestMdRollback(MdWorld):
    def test_rollback_on_an_md_edition_pauses_and_pushes_nothing(self):
        self.push_md(GOOD)
        self.run_desk()
        live, before = self.page(), self.head()
        self.assertIn(ed.MARKER, live)
        out = []
        with mock.patch("builtins.print", lambda *a, **k: out.append(" ".join(map(str, a)))):
            ed.cmd_rollback(argparse.Namespace(edition=ONLY))
        self.assertEqual(before, self.head())
        self.assertEqual(live, self.page())
        self.assertTrue(ed.load_state(SEC, STEM)["paused"])
        self.assertIn("no routine page to restore", out[0])
        self.assertIn("Paused", out[0])
        # Paused: a new md version does not re-publish.
        self.push_md(GOOD.replace("The quiet is the story.", "The silence is the story."))
        self.run_desk()
        self.assertNotIn("The silence is the story.", self.page())

    def test_rollback_on_an_unpublished_md_edition_pauses(self):
        self.push_md(FREEFORM)
        self.run_desk()  # held on shape, nothing published, no route recorded
        before = self.head()
        with mock.patch("builtins.print"):
            ed.cmd_rollback(argparse.Namespace(edition=ONLY))
        self.assertEqual(before, self.head())
        self.assertTrue(ed.load_state(SEC, STEM)["paused"])

    def test_html_rollback_unchanged(self):
        self.run_desk(only=f"{SEC}/2026-10-10")
        ed.cmd_rollback(argparse.Namespace(edition=f"{SEC}/2026-10-10"))
        self.assertNotIn(ed.MARKER, self.page("2026-10-10"))
        self.assertTrue(ed.load_state(SEC, "2026-10-10")["paused"])


if __name__ == "__main__":
    unittest.main(verbosity=1)
