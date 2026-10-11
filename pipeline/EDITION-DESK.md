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

Whose hands: Claude runs every step, only after Eddie's explicit go on THIS card.

| Op | What it does | Expected result | Stop if |
|---|---|---|---|
| 0 | Revert the 3 commits a test pushed to daily-pages at 13:18 ET | **Done.** Pushed 13:24:33 ET by Claude on Eddie's "revert" (13:24). d09b906; live daily 10-10 and weekly 2026-41 byte-identical to 2338810, test image 404 | n/a |
| 1 | `git push origin main` (shipped) | origin/main = the polled SHA | push rejected |
| 2 | Publish daily 10-10 in the paper layout with its QC-approved images (via the launcher, `--only anthropic-daily/2026-10-10`) | page live with the paper marker; every paragraph, figure and link of the routine page present (gate) | any gate problem, or not live in 5 min |
| 3 | Load the launchd job | **From then on the desk re-publishes every new edition to the public site automatically, every 30 minutes, unattended, with images Claude QC approved.** Op 3 only after op 1, because the job runs pushed origin/main | Night Desk escalates an Edition Desk alert |

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
