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
