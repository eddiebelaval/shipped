#!/usr/bin/env python3
"""The launcher's alert reflects current state: a blip leaves nothing, an outage escalates.

Runs the real edition-desk-launch.sh against a throwaway HOME (a bare origin, a clone as the main
checkout, a stub desk) with `git fetch` made to fail on demand, then asks the real Night Desk check
whether it would escalate. Run: python3 pipeline/test/test-edition-desk-launch.py
"""
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAUNCHER = HERE.parent / "scripts" / "edition-desk-launch.sh"
NIGHT_DESK = HERE.parent / "scripts" / "night-desk.py"

GIT_WRAPPER = """#!/bin/bash
if [ -e "$FAIL_FETCH" ] && [[ " $* " == *" fetch "* ]]; then echo "fatal: unable to access origin" >&2; exit 128; fi
exec {git} "$@"
"""


class LauncherAlert(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="launcher-test-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.home = self.tmp / "home"
        self.main = self.home / "Development/id8/shipped"
        self.ops = self.main / "ops"
        origin = self.tmp / "origin.git"
        seed = self.tmp / "seed"
        git = shutil.which("git")
        for cmd in (["init", "-q", "--bare", "-b", "main", str(origin)],
                    ["init", "-q", "-b", "main", str(seed)]):
            subprocess.run([git, *cmd], check=True)
        desk = seed / "pipeline/scripts/edition-desk.py"
        desk.parent.mkdir(parents=True)
        desk.write_text("import os, sys\nsys.exit(int(os.environ.get('DESK_EXIT', '0')))\n")
        env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
               "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
        for cmd in (["add", "."], ["commit", "-q", "-m", "seed"], ["push", "-q", str(origin), "main"]):
            subprocess.run([git, "-C", str(seed), *cmd], check=True, env=env)
        self.main.parent.mkdir(parents=True)
        subprocess.run([git, "clone", "-q", str(origin), str(self.main)], check=True)
        (self.main / "pipeline/node_modules").mkdir(parents=True)

        bindir = self.tmp / "bin"
        bindir.mkdir()
        (bindir / "git").write_text(GIT_WRAPPER.format(git=git))
        (bindir / "git").chmod(0o755)
        self.fail_flag = self.tmp / "fail-fetch"
        self.env = {**os.environ, "HOME": str(self.home), "PATH": f"{bindir}:{os.environ['PATH']}",
                    "FAIL_FETCH": str(self.fail_flag), "EDITION_DESK_QUIET": "1"}
        self.env.pop("DESK_EXIT", None)

    def tick(self, fetch_ok=True, desk_exit=0):
        if fetch_ok:
            self.fail_flag.unlink(missing_ok=True)
        else:
            self.fail_flag.touch()
        env = {**self.env, "DESK_EXIT": str(desk_exit)}
        return subprocess.run(["bash", str(LAUNCHER)], env=env, capture_output=True, text=True).returncode

    @property
    def alert(self):
        return self.ops / "EDITION-DESK-LAUNCHER-ALERT.md"

    def night_desk_lines(self):
        """What the real Night Desk check would escalate, read from this HOME's ops/."""
        old = os.environ["HOME"]
        os.environ["HOME"] = str(self.home)
        try:
            spec = importlib.util.spec_from_file_location("nd", NIGHT_DESK)
            nd = importlib.util.module_from_spec(spec)
            sys.argv = ["nd", "--quiet"]
            spec.loader.exec_module(nd)
            nd.check_edition_desk()
            return [m for _, v, m in nd.findings if v == "ESCALATE"]
        finally:
            os.environ["HOME"] = old

    def test_one_failed_fetch_then_a_good_tick_leaves_no_alert(self):
        self.assertEqual(self.tick(), 0)
        self.assertEqual(self.tick(fetch_ok=False), 1)
        self.assertFalse(self.alert.exists(), "one failed tick must not escalate")
        self.assertEqual(self.night_desk_lines(), [])
        self.assertEqual(self.tick(), 0)
        self.assertFalse(self.alert.exists())
        self.assertFalse((self.ops / ".edition-desk-launcher-fails").exists())
        self.assertEqual(self.night_desk_lines(), [])

    def test_failures_must_be_consecutive(self):
        for ok in (False, False, True, False, False):
            self.tick(fetch_ok=ok)
        self.assertFalse(self.alert.exists())

    def test_persistent_failure_escalates_once_and_stays_until_recovery(self):
        for _ in range(2):
            self.tick(fetch_ok=False)
        self.assertFalse(self.alert.exists())
        for _ in range(4):
            self.assertEqual(self.tick(fetch_ok=False), 1)
        lines = [l for l in self.alert.read_text().splitlines() if l.startswith("- ")]
        self.assertEqual(len(lines), 1, "a long outage is one line, not one per tick")
        self.assertIn("ESCALATE", lines[0])
        self.assertIn("6 ticks in a row", lines[0])
        self.assertIn("git fetch origin main", lines[0])
        escalated = self.night_desk_lines()
        self.assertEqual(len(escalated), 1)
        self.assertIn("git fetch origin main", escalated[0])
        self.assertEqual(self.tick(), 0)
        self.assertFalse(self.alert.exists(), "recovery resolves the alert it raised")
        self.assertEqual(self.night_desk_lines(), [])

    def test_a_crashing_desk_counts_as_a_failed_tick(self):
        for _ in range(3):
            self.assertEqual(self.tick(desk_exit=3), 1)
        self.assertIn("edition-desk.py exited 3", self.alert.read_text())

    def test_recovery_keeps_an_unrelated_stale_lock_note(self):
        self.ops.mkdir(parents=True, exist_ok=True)
        self.alert.write_text("# Edition Desk launcher alert\n\n"
                              "- ESCALATE 2026-11-02 03:00 stale lock cleared (a run died holding it)\n")
        for _ in range(3):
            self.tick(fetch_ok=False)
        self.assertEqual(self.tick(), 0)
        text = self.alert.read_text()
        self.assertIn("stale lock cleared", text)
        self.assertNotIn("launcher failed", text)

    def test_a_paused_tick_does_not_touch_the_count(self):
        self.tick(fetch_ok=False)
        (self.ops / "EDITION-DESK-PAUSED").touch()
        self.assertEqual(self.tick(fetch_ok=False), 0)
        (self.ops / "EDITION-DESK-PAUSED").unlink()
        self.tick(fetch_ok=False)
        self.assertFalse(self.alert.exists())
        self.tick(fetch_ok=False)
        self.assertTrue(self.alert.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
