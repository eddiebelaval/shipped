# TRACKER.md — Shipped.

> The watershed map. Every source article, which issue it feeds, and where it stands.

---

## How this works

Source articles are the raw material. Issues are the finished product. This file tracks the flow between them.

**The lifecycle of a source article:**

```
RESEARCH  →  DRAFT  →  USED
   ↑            ↑         ↑
 raw notes    shaped    pulled into
 + sources    piece     an issue section
```

**Where articles live:** `content/articles/issue-NN/` — one subfolder per issue.

**Naming convention:** `{topic-slug}.md` — e.g., `claude-design-reception.md`, `conway-leak-analysis.md`, `trust-week-lovable.md`

**Frontmatter spec (required for every article):**

```yaml
---
title: "Claude Design Reception Analysis"
issue: 02                          # which issue this feeds
section: lead-story                # which section it maps to (see key below)
status: research | draft | used    # current lifecycle stage
created: 2026-04-21
updated: 2026-04-22
sources:                           # primary source URLs
  - https://techcrunch.com/...
  - https://venturebeat.com/...
---
```

**Section keys:**

| Key | Maps to issue section |
|---|---|
| `open` | The Open (80–150 word hook) |
| `lead-story` | Lead Story |
| `also-shipped` | Also Shipped |
| `quiet-wire` | Quiet on the Wire |
| `close` | The Close |
| `release-log` | Release Log |
| `investigation` | Investigation / special section |
| `sops` | Builder SOPs / action layer |
| `background` | General background research (no specific section yet) |

---

## Article inventory

Every source article across all issues. The master list.

| Article | Issue | Section | Status | Created | File |
|---|---|---|---|---|---|
| Issue 02 Signal Report | 02 | background | used | 2026-04-21 | `articles/issue-02/signal-report.md` |
| Issue 02 Draft (front-of-book) | 02 | open, lead-story | draft | 2026-04-21 | `articles/issue-02/front-of-book-draft.md` |
| Claude Design Reception | 02 | lead-story | draft | 2026-04-21 | `articles/issue-02/claude-design-reception.md` |
| OpenClaw Anthropic Return | 02 | also-shipped | research | 2026-04-21 | `articles/issue-02/openclaw-anthropic-return.md` |
| Conway Leak Analysis | 02 | lead-story (third-act) OR b-story | research | 2026-04-22 | `articles/issue-02/conway-leak-analysis.md` |
| Trust Week — Lovable BOLA | 02 | investigation | research | 2026-04-22 | `articles/issue-02/trust-week-lovable.md` |
| Trust Week — Vercel via Context.ai | 02 | investigation | research | 2026-04-22 | `articles/issue-02/trust-week-vercel.md` |
| Amazon-Anthropic Deal | 02 | release-log | research | 2026-04-21 | _release-log-only; no standalone article_ |

> **"not yet captured"** = the research exists (in the WIP, in signal reports, in conversation) but hasn't been pulled into a standalone article file yet. Capturing it is step one of making it trackable.

---

## Per-issue rollup

### Issue 02 — ship date 2026-04-24

**Status:** Drafting. Running order not yet locked (locks Thu 2026-04-23).

| Section | Source article(s) | Status | Gaps |
|---|---|---|---|
| Open | front-of-book-draft.md | draft | Needs final voice pass |
| Lead Story | claude-design-reception.md + conway-leak-analysis.md | draft (Claude Design) / research (Conway) | Hands-on screenshots (Eddie only). Pro quote needed. Conway placement call Thursday. |
| Also Shipped | openclaw-anthropic-return.md + scraper output (pending) | research (OpenClaw) / blocked (scrape) | OpenClaw needs date/version confirmation; 2–4 more Also Shipped items wait on Thursday scrape |
| Investigation | trust-week-lovable.md + trust-week-vercel.md | research | Pro interview for SOPs. Attribution softened (ShinyHunters denial integrated). Legacy-exposure scope confirm before press. |
| Quiet on the Wire | Compiled from signal report Thursday | pending | Writeup + Conway demotion if promoted to Lead third-act |
| Term of the Issue | Leaning "Presence" — definition block not yet written | pending | Write the definition + usage example Thursday AM |
| The Close | _(not started)_ | pending | Rhythm closer, three beats, tied to Term of Issue |
| Release Log | _(blocked on scraper)_ | blocked | Thursday PM scrape run + Friday 7 AM final |

**Readiness (7/Apr/22):** 5 of 8 sections have source articles captured. 2 blocked on pipeline (Release Log + scraper-dependent Also Shipped items). 3 editorial slots pending Thursday (Quiet on Wire, Term of Issue, Close).

**Article inventory:** 7 source articles on disk (signal + front-of-book draft + 5 topic articles). Per `content/FORMULA.md`, a healthy weekly needs 6–8 source articles. **Issue 02 is now at formula.**

---

## Issue 01 — shipped 2026-04-17

**Status:** Published. Canonical copy lives in pre-extraction repo (`id8/knowledge/series/shipped/`). Not yet migrated to `content/`.

| Section | Source article(s) | Status | Notes |
|---|---|---|---|
| Full issue | _(pre-extraction)_ | used | Issue 01 predates the tracking system. Retrospective capture is optional. |

---

## Issue 00 — The Founding (dry run)

**Status:** Published (dry-run). Canonical copy: `content/issue-00-the-founding.md`

| Section | Source article(s) | Status | Notes |
|---|---|---|---|
| Full issue | issue-00-the-founding.md | used | 57KB founding issue. No separate source articles — written as a single document. |

---

## How to use this file

**When starting a new issue:**
1. Create the subfolder: `content/articles/issue-NN/`
2. Add a row to the inventory for each article as it's created
3. Add a new issue rollup section below with the section → article mapping
4. As articles move from research → draft → used, update both the inventory and the rollup

**When capturing scattered material:**
If research exists in a conversation, a signal report, or somewhere outside the repo — create an article file in `content/articles/issue-NN/`, paste the content, add frontmatter, and register it here. That's the moment it becomes trackable.

**When reviewing before Thursday lock:**
Read the rollup for the current issue. Every section should either have a source article in progress or be explicitly marked as blocked/pending. If a section has no material and no plan, that's a gap to resolve before lock.

**When generating the issue:**
The article files in `content/articles/issue-NN/` are the source material. Claude reads them, plus the WIP, plus STYLE.md, and drafts the issue. After the issue ships, mark all consumed articles as `used`.

---

## Changelog

| Date | Change |
|---|---|
| 2026-04-21 | Initial tracker. Cataloged Issue 02 materials from signal report and draft. Retroactive entries for Issues 00 and 01. |
| 2026-04-21 | `claude-design-reception.md` captured as draft. Lead-story section now has a source article. |
| 2026-04-21 | `openclaw-anthropic-return.md` captured as research. Also Shipped section has its first source article. Policy-signal beat — "Anthropic sanctioned CLI-reuse again" (per OpenClaw docs only, needs attribution discipline). |
| 2026-04-21 (PM) | WIP refresh via `/shipped-wip`. Signal report absorbed. Conway placement conflict flagged for Thursday (B story vs Lead third-act). Lovable 4-stage story evolution + ShinyHunters attribution reversal integrated into Trust Week. Amazon-Anthropic deal added as release-log-only entry (Story 4). OpenClaw wired in as Story 5 / Also Shipped. Presence now leading term-of-issue candidate. Thursday checklist expanded with structure/editorial/research/pipeline sections. |
| 2026-04-22 | `content/FORMULA.md` created — weekly skeleton, word budgets, article inventory minimums, slot-based section decision tree. Derived from Issue 00 + STYLE.md + Issue 02 WIP work. |
| 2026-04-22 | Three article skeletons captured: `conway-leak-analysis.md`, `trust-week-lovable.md`, `trust-week-vercel.md`. Flipped three "not yet captured" rows in the inventory to real file paths. Issue 02 now has 7 source articles on disk — at formula per FORMULA.md. |
