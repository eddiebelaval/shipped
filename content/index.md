---
series: Shipped.
beat: Frontier-lab releases — Anthropic, OpenAI, Google DeepMind, Meta, Mistral, xAI
cadence: Weekly, Friday 9 AM ET
voice: Rolling Stone × Wired
created: 2026-04-16
---

# Shipped. — Series Archive

A weekly magazine on what the frontier AI labs are shipping.

The frontier ships at building speed. This is the read that keeps you plugged in.

## Issues

The canonical public archive (the hub) is **[id8labs.app/shipped](https://id8labs.app/shipped)** — every
issue lives there as a self-contained page. This table mirrors it for repo-local
reference; the hub is the source of truth.

| # | Date | Title | Status |
|---|---|---|---|
| 04 | 2026-05-08 | [Capacity](issue-04-capacity.md) · [read →](https://id8labs.app/shipped/04) | Published |
| 03 | 2026-05-01 | [Patron](issue-03-patron.md) · [read →](https://id8labs.app/shipped/03) | Published |
| 02 | 2026-04-24 | [Presence](issue-02-presence.md) · [read →](https://id8labs.app/shipped/02) | Published |
| 01 | 2026-04-17 | [The chart that wasn't about Opus 4.7](https://id8labs.app/shipped/01) (Founding Issue) | Published |
| 00 | 2026-04-16 | [The Founding Issue — The Shadow Release](issue-00-the-founding.md) | Dry-run |

## Reference

Standing references that live alongside the issues. Not weekly reads, just always-current lookups.

| Page | What | Updates |
|---|---|---|
| [The Command Index](command-index/) | Every slash command in the Claude Code install: Anthropic built-ins, plugin commands and skills, and id8Labs custom commands | Auto, weekly |

## How this series works

- **Source.** Anthropic's news page, API release notes, Claude Code changelog, Claude Apps release notes, GitHub SDK releases, research publications.
- **Cadence.** Friday 9 AM ET. Issue #00 is a 3-week dry-run; Issue #1 onward is 7-day windows.
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
