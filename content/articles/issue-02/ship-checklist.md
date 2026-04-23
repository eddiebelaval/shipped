---
title: "Issue 02 ship checklist"
issue: 2
section: ops
status: research
created: 2026-04-22
updated: 2026-04-22
ship_target: "2026-04-24 09:00 ET"
grade_override: true
grade_override_reason: "Operational ship-day checklist. Not an editorial article; rubric v2 does not apply. Graded OVR."
sources:
  - content/STYLE.md
  - content/FORMULA.md
  - content/articles/issue-02/launch-copy.md
  - content/articles/issue-02/release-log-research.md
  - SPEC.md
  - CLAUDE.md
---

# Issue 02 ship checklist

> Ship day is Friday 2026-04-24, 09:00 ET. Every item below has a time, an owner, and a verification step. If an item cannot pass its verification, ship is blocked until resolved. No exceptions.

## T-48h (Wednesday PM)

Status: in progress as of 2026-04-22 PM.

- [x] All source articles captured and graded.
- [x] Running order candidates identified.
- [x] Term of Issue locked (Presence).
- [x] Slug locked (`presence`).
- [x] Conway placement locked (B-story, Feature slot).
- [x] Companion placement locked (Presence-as-category).
- [ ] Counter-signal article placement pending.
- [x] Quiet on the Wire article captured.
- [x] Release Log research populated (Apr 17 to 22).
- [ ] Title assignment.

## T-24h (Thursday AM, 09:00 ET)

Owner: Eddie.

- [ ] **Running order frozen.** No new sections added after this point. Logged in `issue-02-wip.md`.
- [ ] **Title assigned.** One line, under 60 characters. Logged in WIP frontmatter.
- [ ] **Open anchor confirmed.** One of: time-stamp rhythm, WhatsApp reader signal, or action-layer meta beat.
- [ ] **Close anchor confirmed.** One concrete scene for beat 1 of the Close.
- [ ] **Hands-on Claude Design screenshots captured.** Eddie's own session. Minimum 3. Saved to `articles/issue-02/assets/`.
- [ ] **Pro interview for Trust Week:** booked, or explicitly deferred. Deferral logged in WIP.
- [ ] **Companion choice:** one, two, or collapsed into Close. Decision logged.

## T-20h (Thursday 13:00 ET)

Owner: Eddie + Claude.

- [ ] **`pnpm scrape` Thursday afternoon run.** X API token set up, or fallback to web research. Output appended to `release-log-research.md`.
- [ ] **Front-of-book prose draft.** Lead distilled to 200 to 300 words (already 214 in WIP, voice-check it). Conway B-story drafted to 400 to 700 words. Trust Week Investigation drafted to 400 to 700 words (paired with Vercel). Also Shipped items drafted to 60 to 100 each. Quiet on the Wire drafted to 50 to 80. Term of Issue block drafted to 100 to 150. Close drafted to 120 to 200.
- [ ] **Companion prose drafted.** One or two, based on the Thursday AM call.

## T-14h (Thursday 19:00 ET)

Owner: Eddie.

- [ ] **First voice-gate pass.** Scan for forbidden phrases per STYLE.md. Scan for em and en dashes (kill all). Scan for the "X isn't Y, it's Z" budget (max one, spent in the Lead). Log any kills.
- [ ] **First attribution pass.** Every number has a source link within 3 paragraphs. Every quote has named attribution. Every "per" or "reportedly" lines up with a source on disk.
- [ ] **Read the front-of-book aloud.** Rhythm is the product. Flag anywhere the voice slips.
- [ ] **Release Log final research window.** Any Anthropic news between Wed PM and Thu PM gets added.

## T-12h (Thursday 21:00 ET)

Owner: Claude.

- [ ] **`/verify-shipped` dry run.** Run the verifier on the current draft. Every gate must pass or be explicitly green-lit.
- [ ] **Source-article status flip.** Any article whose content is now in the front-of-book flips from `draft` or `research` to `used`.
- [ ] **Dashboard regen.** Confirm readiness at 100%, zero gaps.

## T-2h (Friday 07:00 ET)

Owner: Eddie + Pipeline.

- [ ] **Final `pnpm scrape` run.** Catches anything shipping Thursday night or early Friday.
- [ ] **Release Log finalized in the issue body.** Entries pulled from `release-log-research.md`, stripped of category tags, ordered newest first.
- [ ] **Full issue read aloud, top to bottom.** One sitting. Flag anywhere the voice slips.

## T-1h (Friday 08:00 ET)

Owner: Eddie.

- [ ] **Second voice-gate pass.** Same checks as T-14h. Kill on sight.
- [ ] **Launch copy finalized.** X thread, LinkedIn post, email, WhatsApp message. All saved in `launch-copy.md`.
- [ ] **Hero image in place.** Claude Design's opening page has the image. OG card generated and live.
- [ ] **Subscribe link and share link tested.** Both return 200.

## T-5min (Friday 08:55 ET)

Owner: Pipeline.

- [ ] **`pnpm publish`** runs render + verify + stage. Every verifier gate passes. Any failure is a hard block.
- [ ] **Staged HTML check.** Open the staged file at `../id8labs/public/shipped/02/` and visually scan. Flag any layout break, broken link, missing image.
- [ ] **Backup made.** Latest WIP committed to the repo (not pushed), tagged `issue-02-pre-ship`.

## T-0 (Friday 09:00 ET)

Owner: Eddie.

- [ ] **`git commit && git push` from the `id8labs/` repo.** Human gate. No bypass.
- [ ] **Verify the issue is live.** Load id8labs.app/shipped. Check the URL returns 200. Check OG card renders in a social-card debugger.

## T+5min (Friday 09:05 ET)

Owner: Eddie.

- [ ] **Post X thread.** Copy from `launch-copy.md`. Do not improvise.
- [ ] **Post LinkedIn.** Copy from `launch-copy.md`.
- [ ] **Send email.** Trigger the newsletter send.
- [ ] **WhatsApp message.** Post in the internal group with one specific ask for signal.
- [ ] **Update id8labs.app home page pull-quote.** One line from the issue, rotates.

## T+1h (Friday 10:00 ET)

Owner: Claude.

- [ ] **Monitoring.** X replies and quotes. LinkedIn comments. WhatsApp reactions. Email open rate.
- [ ] **Hot fixes only.** No new features, no copy changes except `[corr]` commits for factual errors.
- [ ] **Issue 03 signal collection begins.** New news in a new `articles/issue-03/signal-report.md`.

## T+24h (Saturday AM)

Owner: Eddie.

- [ ] **`post-ship.md` drafted.** What shipped, what worked, what broke, lessons for Issue 03.
- [ ] **Tracker closed out.** All `draft` / `research` source articles flipped to `used`. TRACKER updated.
- [ ] **Readiness reset for Issue 03.** New dashboard baseline.

## Hard blocks (any of these halt ship)

- Verifier fails on URL, number, quote, date, or voice gate.
- Any source article referenced in the front-of-book is missing from disk.
- Any quote in the front-of-book has no attribution.
- Any stat has no source link within 3 paragraphs.
- Em dashes or en dashes appear in the body.
- Hero image is missing or broken.
- OG card does not render.
- The staged HTML fails a 200 check.

## Rollback procedure

If the issue ships with a material error:

1. Identify the error. One concrete sentence: "X was wrong, Y is right."
2. Create a `[corr]` commit. Edit the markdown, not the HTML.
3. Re-render and re-stage (`pnpm publish`).
4. Push the correction.
5. Post a correction notice in the same channels that posted the launch copy.
6. Log the correction in `post-ship.md` under "Corrections."
7. Never un-ship. Never delete the original commit. The correction is additive.

## Emergency contacts

- Pipeline failures: Claude via slash command.
- CDN or hosting issues: Vercel dashboard.
- Email delivery issues: newsletter platform dashboard.
- Social account issues: direct login only.

## Verification summary table

| Gate | Pass threshold | Owner | Run via |
|---|---|---|---|
| Voice | Zero forbidden phrases, zero em/en dashes, one "X isn't Y" max | Eddie | manual scan + grep |
| Attribution | Every number has a link; every quote has an attribution | Eddie | `/verify-shipped` |
| Source | Every article referenced exists on disk | Pipeline | `/verify-shipped` |
| Render | HTML generates without error | Pipeline | `pnpm publish` |
| Live | URL returns 200 | Eddie | manual |
| Social | OG card renders | Eddie | social-card debugger |

## Open questions / TODOs before ship

- [ ] Set up X API token for the Thursday scrape (or confirm we are running the web-research fallback).
- [ ] Confirm the `../id8labs/` sibling repo is up to date and Vercel is pointed at the correct branch.
- [ ] Confirm the newsletter platform is authenticated.
- [ ] Confirm the WhatsApp group link is current.
