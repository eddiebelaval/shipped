# Edition Desk runbook

The Edition Desk gives every daily, weekly and monthly edition the newspaper front (DESIGN.md Rev 6).
The cloud routines publish each edition on time in the locked chrome; the desk converts that page,
finds fresh images, has Claude QC grade them, gates the result, and re-publishes it to `daily-pages`.

- Code: `scripts/edition-desk.py` (orchestrator), `scripts/edition-to-paper.py` (converter),
  `src/render/edition-cli.ts` (render), `scripts/image-desk.py` (sources), `scripts/image-qc.py` (QC).
- Runs from: a clean worktree at `~/Development/.worktrees/shipped/edition-desk`, pinned to the
  pushed `origin/main` by `scripts/edition-desk-launch.sh`. The main checkout is never the release surface.
- State: `content/editions/<section>/<stem>/` (gitignored): `source.html`, `edition.md`, `images/`, `edition.json`.
- Log: `~/Library/Logs/shipped/edition-desk.log`. Alerts: `ops/EDITION-DESK-ALERT.md` (the desk's; stands while any
  edition is held, clears when none is) and `ops/EDITION-DESK-LAUNCHER-ALERT.md` (the launcher's: failures and stale
  locks; sticky, delete it by hand once read). Night Desk escalates both every night.

## Status

LIVE since 2026-10-11 17:26 ET. Op 1 pushed 29b0862 (7th Prometheus poll, 6/6 GO); op 2 published daily 10-10
with 6 QC-approved images (verified live, every image 200); op 3 loaded the launchd job. Weekly 2026-41 was held
at 17:59 by an apostrophe alt-text bug (fail-safe; routine page stayed live); fix 1755a1f (poll 6/6 GO) pushed
18:54 on Eddie's go. A successful publish sends no notification: look for `published ... live check: OK` in the
log and the alert file clearing.

## Go-live card (2026-10-11, executed): what each step did, in order

Whose hands: Claude runs every step, in this order, only after Eddie's explicit go on THIS card.

**Op 0 (done).** Revert the 3 commits an Edition Desk test pushed to daily-pages at 13:18 ET. The revert commits
were created locally at 13:19:50 ET under the git identity "Edition Desk" while the fix was prepared, and pushed
at 13:24:33 ET by Claude after Eddie's explicit "revert" (13:24). daily-pages d09b906; live daily 10-10 and
weekly 2026-41 verified byte-identical to 2338810; the test image returns 404.

**Op 1.** Push the polled code.
```bash
git -C ~/Development/id8/shipped push origin main
```
Expect: `origin/main` = the polled SHA. Stop if the push is rejected. Undo: `git revert` the commits on main and
push. Before op 3 nothing publishes from a push alone; after op 3 the next timer run uses whatever main holds.

**Op 2 (after op 1).** Publish daily 10-10 in the paper layout, nothing else.
```bash
curl -s -o /dev/null -w '%{http_code}\n' https://eddiebelaval.github.io/shipped/   # Pages healthy: 200
~/Development/id8/shipped/pipeline/scripts/edition-desk-launch.sh --only anthropic-daily/2026-10-10
```
Expect: the log says `published anthropic-daily/2026-10-10 (6 approved images); live check: OK`. Six images are
drawn; QC approved seven (the lead's halftone is not drawn because QC picked the Atkinson print). Stop if the
gate holds, the live check is UNVERIFIED, or Pages is not 200. Undo: the rollback section below.

**Op 3 (after op 1).** Load the scheduled job.
```bash
cp ~/Development/id8/shipped/pipeline/scripts/com.id8labs.shipped-edition-desk.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.id8labs.shipped-edition-desk.plist
```
**From then on, every 5 minutes and with no one watching, the desk re-publishes every new edition to the
public site with images Claude QC approved.** Its first run also PUBLISHES weekly 2026-41 to the public site, unattended (it is past the
cutover and passes every gate in preview). Stop signal: Night Desk escalates an Edition Desk alert. Undo:
`launchctl unload ~/Library/LaunchAgents/com.id8labs.shipped-edition-desk.plist`, or
`touch ~/Development/id8/shipped/ops/EDITION-DESK-PAUSED`; roll back an edition with the
rollback section below.

Known limits: block order is not gated beyond story and log titles keeping their order (the paper front reorders
blocks by design). No whole-run timeout. An image-desk failure is logged, not escalated (the edition runs text-only). The launcher itself runs
from the main checkout and only bootstraps the clean worktree; everything after it runs pushed origin/main.

**What Eddie is trusting (disclosed):** Claude QC's bar was set by calibration on the same 7 issue-10 images he
approved: the first run scored 5/12 (it rejected his favourites), the bar was then loosened (legibility,
relevance, caption truth gate at 3 of 5; look and taste advisory) and re-run on those same 7 plus 6 decoys:
13/13 twice. Out of sample, unchanged rules: 3/3 correct rejections (his own rejected logo photo, a real
person's portrait, an irrelevant photo). Small n. QC also corrects captions it doubts and never approves one
unfixed. Optional: Eddie skims the first week of edition images (`edition-desk.py review <section>/<stem>`);
any note he leaves becomes calibration data.

## Layout changes republish

The desk stores a hash of the render code per edition. When the renderer changes (a pushed layout fix), the
next run rebuilds every live edition since the cutover and republishes it through every gate; a gate failure
holds that edition and leaves its live page alone (re-try with `run --retry`). Undo: revert the change on main
and push (the next run republishes without it), or roll back one edition as below.

## Install

```bash
cp pipeline/scripts/com.id8labs.shipped-edition-desk.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.id8labs.shipped-edition-desk.plist
```

## Pause (everything, immediately)

```bash
touch ~/Development/id8/shipped/ops/EDITION-DESK-PAUSED     # the next run, timer or hand, does nothing
```

One edition only: set `"paused": true` in `~/Development/id8/shipped/content/editions/<section>/<stem>/edition.json`.

## Roll back an edition

```bash
/usr/bin/python3 ~/Development/id8/shipped/pipeline/scripts/edition-desk.py rollback anthropic-daily/2026-10-10
```

First `touch ~/Development/id8/shipped/ops/EDITION-DESK-PAUSED` (stops every run while you work). The command
then pauses the edition, restores `<section>/<stem>.html` from the newest daily-pages version WITHOUT the paper
marker (the routine's page; a 23:00 sweep that rewrote the paper page is skipped, whoever committed it), removes
`<section>/img/<stem>/`, and pushes one plain commit. If the routine's page is already live it pauses and pushes
nothing. Never revert the newest "Edition Desk" commit by hand: on 10-10 that commit is the op 0 revert, and
reverting it would put the leaked test page back. Tested: one publish (A), text then images (B), after a desk
revert (C), after a bot sweep of a text-only and of an image edition (D). To resume: set `"paused": false` in that edition's `edition.json`, then
`~/Development/id8/shipped/pipeline/scripts/edition-desk-launch.sh --retry --only <section>/<stem>`.

Markdown-route editions (`"route": "md"` in `edition.json`, built from `<section>/src/<stem>.md` with no
routine page) have no routine page to restore: rollback only pauses the edition, says so, and pushes nothing.
The live paper page stays until someone replaces or removes it.

## Markdown route

When the routine pushes `<section>/src/<stem>.md` and no `<section>/<stem>.html`, the desk builds `edition.md`
straight from that markdown after `edition-md-check` passes. A shape failure holds the edition (no page at
all), escalates once per markdown version, and keeps a `HELD` line in the alert until a good markdown lands or
`--retry`. The md route runs the text, link, dash, front, inside, image and figure gates against the markdown;
the source.html gates do not apply. While the routine still pushes HTML, nothing changes: an edition with a
routine page (or a paper page built from one) stays on the HTML route and the shadow keeps comparing.

## Unload

```bash
launchctl unload ~/Library/LaunchAgents/com.id8labs.shipped-edition-desk.plist
```

## Image QC

Claude QC holds the image gate for editions (Eddie, 2026-10-11). Before changing the rubric, the model or the
press, and after any change, run `image-qc.py calibrate`: it must agree with every image Eddie approved and reject
every decoy (13/13). Anything less and editions run text-only until it is fixed.
`edition-desk.py review <section>/<stem>` opens the human desk for a spot check; it is not a gate.
