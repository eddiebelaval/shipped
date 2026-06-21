# Shipped. Monthly (Anthropic)

The month-scale companion to the daily and weekly Anthropic digests. One issue per calendar month, generated at month-end, covering every Anthropic release that month plus a zoomed-out read on the state of AI.

- **Daily** (`anthropic-daily/YYYY-MM-DD.md`) = the wire, raw and same-day.
- **Weekly** (`anthropic-weekly/YYYY-WW.md`) = the week's signal, front-of-book + release log.
- **Monthly** (`anthropic-monthly/YYYY-MM.md`) = the month's meaning. Big stories, landscape essays, full categorized release log. The zoomed-out picture.

## File convention

```
content/anthropic-monthly/YYYY-MM.md      e.g. 2026-05.md (May 2026)
```

Frontmatter:

```yaml
---
type: anthropic-monthly
month: 2026-05
issue: M01            # M01, M02, ... monthly sequence
ship_date: 2026-06-01 # generated on the 1st of the following month
status: draft         # draft | published | archived
running_order_locked: false
---
```

## Structure

```
1. COVER LINE      one-sentence subhead for the month
2. THE OPEN        80-150 words. Opening-line pattern. End on a turn.
3. THE BIG THREE   the 3 defining releases of the month. Editorial, 200-300 words each.
4. THE LANDSCAPE   2-3 short essays (~150-220 words). The state-of-AI, zoomed out.
                   THIS is what separates monthly from weekly. Sense-making, not aggregation.
5. ALSO SHIPPED    3-5 notable releases not in the Big Three. 60-100 words each.
6. QUIET ON THE WIRE  rumored / gated / unconfirmed. Loose threads.
7. THE CLOSE       rhythm closer. Three short beats. Last one lands.
8. THE RELEASE LOG full 1:1 categorized mirror of every confirmed release in the month.
```

Voice: same STYLE.md as the weekly. Honor the no-em/en-dash house rule, max one "X isn't Y, it's Z" per issue, forbidden-phrase gate.

## Generation recipe (on-demand, human-gated)

Run at month-end (the `com.id8labs.shipped-monthly` launchd job nudges on the 1st). A good monthly needs a Claude session — the daily files don't cover full months, so gaps need a research pass. Steps:

1. **Assemble from the digests.** Read every `anthropic-daily/YYYY-MM-*.md` and the `anthropic-weekly` files for the target month. Extract every release into the categorized inventory (A. Models, B. API & Platform, C. Claude Code, D. Apps, E. SDKs, F. Research, G. News, H. Deprecations).
2. **Fill the gaps with primary-source research.** The daily digest typically misses the first few days and the tail of the month. Web-research the uncovered dates against primary sources: `anthropic.com/news`, `anthropic.com/research`, `github.com/anthropics/*/releases`, and `platform.claude.com/docs/en/release-notes/api` (this URL is accessible; `docs.anthropic.com` often 403s). Mark anything unconfirmed `[UNVERIFIED]`. Never fabricate a URL, version, date, or quote.
3. **Find the throughline.** What did the month mean? That becomes the cover line, the Open, and the Big Three ranking.
4. **Write the Landscape essays.** 2-3 short pieces that zoom out on patterns across the month (distribution strategy, the reasoning-layer-vs-surface split, safety posture, compute constraints, the agent-platform shift). Evidence-backed, opinionated.
5. **Build the Release Log** as categorized tables (`Date | Title | Tag | One-liner`), exhaustive.
6. **Voice gate.** No em/en dashes. Zero forbidden phrases. Max one "isn't Y, it's Z."
7. **Stage, do not ship.** Write to `content/anthropic-monthly/YYYY-MM.md` with `status: draft`. Eddie runs the editorial pass and the `git commit && git push` human gate. Never auto-publish (Shipped invariant #1).

A fast way to drive steps 1-2: delegate the inventory assembly to a research subagent (read the daily files + web-research the gaps, return a categorized month inventory), then write the front-of-book and Landscape in the house voice from that inventory.

## Cron

`com.id8labs.shipped-monthly` (launchd, 1st of month 09:00) runs `pipeline/scripts/monthly-check.sh` — a read-only heartbeat that checks whether the just-ended month's issue exists and posts a macOS notification (missing / draft / published). It does **not** generate content. Install with `bash pipeline/scripts/install-cron.sh`.

## Issue index

| Issue | Month | Status | File |
|-------|-------|--------|------|
| M01 | May 2026 | draft | `2026-05.md` |
| M02 | June 2026 | draft (month-to-date) | `2026-06.md` |
