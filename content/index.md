---
series: Shipped.
beat: Anthropic releases — models, features, Claude Code, SDK, research, docs
cadence: Weekly, Friday 5 PM ET
voice: Rolling Stone × Wired
created: 2026-04-16
---

# Shipped. — Series Archive

A weekly magazine on what Anthropic is releasing.

The frontier ships at building speed. This is the read that keeps you plugged in.

## Issues

| # | Date | Title | Status |
|---|---|---|---|
| 00 | 2026-04-16 | [The Founding Issue — The Shadow Release](issue-00-the-founding.md) | Dry-run |

## How this series works

- **Source.** Anthropic's news page, API release notes, Claude Code changelog, Claude Apps release notes, GitHub SDK releases, research publications.
- **Cadence.** Friday 5 PM ET, fully autonomous via cron. Issue #00 is a 3-week dry-run; Issue #1 onward is 7-day windows.
- **Voice.** See [STYLE.md](STYLE.md). Living document — evolves with Eddie's writing.
- **Archive.** Every issue lives here as searchable markdown. The public version mirrors at `id8labs.app/shipped/[issue-number]`.
- **Slow weeks.** If Anthropic ships fewer than two items, the issue pivots to ecosystem context (community builds, research citations, competitor moves). The series never skips a Friday.

## Style sheet

The voice anchor for every issue lives in [STYLE.md](STYLE.md). Forbidden phrases, approved moves, opening-line patterns, source essays. Edit it any time — the writer reads from current state.

## Notes for the operator

- Issue files are named `issue-NN-{slug}.md` where `NN` is zero-padded.
- Frontmatter must include: `issue`, `title`, `date`, `period`, `status`, `masthead`.
- Status values: `dry-run`, `published`, `archived`.
- After each issue, append to the table above.
