# Edition Desk runbook

The Edition Desk gives every daily, weekly and monthly edition the newspaper front (DESIGN.md Rev 6).
The cloud routines publish each edition on time in the locked chrome; the desk converts that page,
finds fresh images, has Claude QC grade them, gates the result, and re-publishes it to `daily-pages`.

- Code: `scripts/edition-desk.py` (orchestrator), `scripts/edition-to-paper.py` (converter),
  `src/render/edition-cli.ts` (render), `scripts/image-desk.py` (sources), `scripts/image-qc.py` (QC).
- Runs from: a clean worktree at `~/Development/.worktrees/shipped/edition-desk`, pinned to the
  pushed `origin/main` by `scripts/edition-desk-launch.sh`. The main checkout is never the release surface.
- State: `content/editions/<section>/<stem>/` (gitignored): `source.html`, `edition.md`, `images/`, `edition.json`.
- Log: `~/Library/Logs/shipped/edition-desk.log`. Alerts: `ops/EDITION-DESK-ALERT.md` (Night Desk escalates it).

## Go-live card (2026-10-11): what each step does, in order

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
push (main only feeds the desk; nothing publishes from a push alone).

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
**From then on, every 30 minutes and with no one watching, the desk re-publishes every new edition to the
public site with images Claude QC approved.** Its first run also converts weekly 2026-41 (already past the
cutover; it passes both gates in preview). Stop signal: Night Desk escalates an Edition Desk alert. Undo:
`launchctl unload` it, or `touch ops/EDITION-DESK-PAUSED`.

Known limits: block order is not gated (the paper front reorders blocks by design). The launcher itself runs
from the main checkout and only bootstraps the clean worktree; everything after it runs pushed origin/main.

**What Eddie is trusting (disclosed):** Claude QC's bar was set by calibration on the same 7 issue-10 images he
approved: the first run scored 5/12 (it rejected his favourites), the bar was then loosened (legibility,
relevance, caption truth gate at 3 of 5; look and taste advisory) and re-run on those same 7 plus 6 decoys:
13/13 twice. Out of sample, unchanged rules: 3/3 correct rejections (his own rejected logo photo, a real
person's portrait, an irrelevant photo). Small n. QC also corrects captions it doubts and never approves one
unfixed. Optional: Eddie skims the first week of edition images (`edition-desk.py review <section>/<stem>`);
any note he leaves becomes calibration data.

## Install

```bash
cp pipeline/scripts/com.id8labs.shipped-edition-desk.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.id8labs.shipped-edition-desk.plist
```

## Pause (everything, immediately)

```bash
touch ~/Development/id8/shipped/ops/EDITION-DESK-PAUSED     # the next run does nothing
```

One edition only: set `"paused": true` in its `content/editions/<section>/<stem>/edition.json`.

## Roll back an edition (this order matters)

Reverting first does not work: the next run sees the routine page again and re-publishes the paper front.

1. **Stop it:** `touch ops/EDITION-DESK-PAUSED`, or set `"paused": true` in that edition's `edition.json`.
2. **Revert on daily-pages:** in a worktree of `origin/daily-pages`, `git revert <Edition Desk commit>` and push
   (plain push, never force). The routine's page comes back byte for byte.
3. **Keep it paused** until the cause is fixed. Then remove the pause and run
   `edition-desk.py run --retry --only <section>/<stem>`.

## Unload

```bash
launchctl unload ~/Library/LaunchAgents/com.id8labs.shipped-edition-desk.plist
```

## Image QC

Claude QC holds the image gate for editions (Eddie, 2026-10-11). Before changing the rubric, the model or the
press, and after any change, run `image-qc.py calibrate`: it must agree with every image Eddie approved and reject
every decoy (13/13). Anything less and editions run text-only until it is fixed.
`edition-desk.py review <section>/<stem>` opens the human desk for a spot check; it is not a gate.
