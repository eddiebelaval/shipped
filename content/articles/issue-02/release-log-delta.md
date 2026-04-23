---
title: "Release Log delta: 2026-04-23 scrub"
issue: 2
section: release-log
status: research
created: 2026-04-23
updated: 2026-04-23
parent_doc: release-log-research.md
sources:
  - https://x.com/claudeai/status/2046328619249684989
  - https://blockchain.news/ainews/claude-cowork-update-live-artifacts-for-real-time-dashboards-and-trackers-2026-analysis
  - https://yourstory.com/ai-story/claude-cowork-live-dashboards-ai-bi-disruption
  - https://phemex.com/news/article/claude-launches-live-artifacts-for-autorefreshing-dashboards-in-cowork-74713
  - https://blockchain.news/ainews/claude-app-launches-cowork-on-all-paid-plans-latest-availability-update-and-business-impact-analysis
  - https://medium.com/ai-analytics-diaries/claude-cowork-just-went-ga-how-agentic-ai-agents-are-automating-data-science-workflows-in-2026-433ed86b0727
  - https://code.claude.com/docs/en/changelog
  - https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
  - https://platform.claude.com/docs/en/release-notes/overview
---

# Release Log delta: 2026-04-23 scrub

> Eddie flagged on 2026-04-23 AM that the existing 10-entry research file was missing real Anthropic releases this week — specifically Cowork dashboard features and "other great functionality." This delta adds the three entries the original scrub missed. Merge into `release-log-research.md` per its existing per-day structure.

## New entries

### 2026-04-23 (Thursday)

#### 2026-04-23: Claude Code 2.1.118 ([changelog](https://code.claude.com/docs/en/changelog))

Vim visual mode (`v`) and visual-line mode (`V`) added with selection, operators, and visual feedback. Fixed message duplication when scrolling in fullscreen mode. Category: `[RELEASE]`.

### 2026-04-20 (Monday)

#### 2026-04-20: Claude Cowork live artifacts — dashboards and trackers that auto-refresh ([@claudeai on X](https://x.com/claudeai/status/2046328619249684989))

Cowork can now build live artifacts: dashboards and trackers connected to apps and files. Open any of them later and they refresh with current data. Shifts artifacts from one-shot snapshots to persistent surfaces with data bindings — closer to a Notion or Retool block than the previous Claude artifact format. Category: `[LAUNCH]`. Pairs with the Cowork GA + Enterprise feature push the same day.

#### 2026-04-20: Claude Cowork goes GA on macOS and Windows desktop, expanded analytics, OpenTelemetry support, RBAC for Enterprise ([Medium / Data Mind](https://medium.com/ai-analytics-diaries/claude-cowork-just-went-ga-how-agentic-ai-agents-are-automating-data-science-workflows-in-2026-433ed86b0727), [Phemex](https://phemex.com/news/article/claude-launches-live-artifacts-for-autorefreshing-dashboards-in-cowork-74713))

Cowork moves from public beta to GA on Claude Desktop (macOS + Windows). Bundled with: expanded usage analytics, OpenTelemetry export support, role-based access controls for Enterprise plans, custom charts, and inline visualizations in responses. Category: `[LAUNCH]`. Cowork was previously preview-status as recently as Issue 01's coverage; this is the formal exit.

## Notes for the editor

- **Same-day stack on Apr 20.** Two `[LAUNCH]` entries land on the same day. Editorial choice: keep them as two entries (the artifacts surface is technically distinct from the GA push), OR collapse into one if the back-of-book runs long. Default keep separate — the live-artifacts beat is the *thematic-fit* item (it's a presence-flavored capability) and deserves its own line.
- **Why the original scrub missed these.** The original release-log-research.md was built from `releasebot.io` + Anthropic's `news.anthropic.com` page + the `docs.claude.com` API release notes. None of those three include Cowork-specific announcements (Cowork lives in `support.claude.com` / `@claudeai` X account / third-party coverage). Add `support.claude.com/en/articles/12138966-release-notes` and `@claudeai` X feed to the standing source list for Issue 03 onward.
- **2.1.117 enrichment.** The existing 2.1.117 entry in research is thin ("Faster startup, stronger plugin management..."). The actual changelog adds: experimental Advisor tool updates, safer auth handling, more reliable context and subagent behavior. Worth a small in-place enrichment when merging.
- **Total after merge:** 13 entries across the Apr 17–23 window. Distribution: 3 `[LAUNCH]`, 1 `[MODEL]`, 5 `[RELEASE]`, 2 `[FIX]`, 1 `[POLICY]`, 1 `[NEWS]`, 0 `[ECOSYSTEM]` (still). 13 entries fit the back-of-book without trim.

## Attribution caveats

- **The Apr 20 Cowork live-artifacts post** — primary source is `@claudeai` X. Archive that URL (X URLs decay) before press.
- **Cowork GA + Enterprise feature push** — coverage is third-party (Medium, Phemex, BlockchainNews aggregator). Anthropic's official Cowork release-notes URL would be ideal; if not surfaced before Friday 7 AM scrape, attribute as "per third-party coverage of the Apr 20 Cowork update."
- **2.1.118 changelog URL** — `code.claude.com/docs/en/changelog` is the canonical home; the `github.com/anthropics/claude-code/blob/main/CHANGELOG.md` mirror should match.

## TODO before press merge

- [ ] Append these 3 entries into `release-log-research.md` under the proper date headings (2026-04-23 section is currently empty above 2026-04-22)
- [ ] Enrich the 2.1.117 entry in research with the additional functionality (advisor tool, auth, context/subagent reliability)
- [ ] Archive `x.com/claudeai/status/2046328619249684989` via Internet Archive
- [ ] Update TRACKER.md "Release Log" row to note Apr 23 scrub completed (delta merged)
