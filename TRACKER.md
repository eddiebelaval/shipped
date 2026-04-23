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
| Vercel sensitive:on default | 02 | also-shipped | research | 2026-04-22 | `articles/issue-02/also-shipped-vercel-sensitive-default.md` |
| Claude performance backlash | 02 | also-shipped | research | 2026-04-22 | `articles/issue-02/also-shipped-claude-performance-backlash.md` |
| Presence as a product category | 02 | companion (placement open) | research | 2026-04-22 | `articles/issue-02/presence-as-category.md` |
| Claude Code $20 Pro plan test | 02 | quiet-wire | research | 2026-04-22 | `articles/issue-02/quiet-claude-code-pro-test.md` |
| Release Log research 04-17 to 04-22 | 02 | release-log | research | 2026-04-22 | `articles/issue-02/release-log-research.md` |
| Counter-signal: OpenAI and Google | 02 | companion (placement open) | research | 2026-04-22 | `articles/issue-02/counter-signal-field-moved.md` |
| Close scaffolding | 02 | close | research | 2026-04-22 | `articles/issue-02/close-prep.md` |
| Term of Issue: Presence (definition block) | 02 | term-of-issue | research | 2026-04-22 | `articles/issue-02/term-of-issue-presence.md` |
| Launch copy scaffold | 02 | launch | research | 2026-04-22 | `articles/issue-02/launch-copy.md` |
| Ship-day checklist | 02 | ops | research | 2026-04-22 | `articles/issue-02/ship-checklist.md` |
| Post-ship retrospective scaffold | 02 | post-ship | pending | 2026-04-22 | `articles/issue-02/post-ship.md` |

> **"not yet captured"** = the research exists (in the WIP, in signal reports, in conversation) but hasn't been pulled into a standalone article file yet. Capturing it is step one of making it trackable.

---

## Per-issue rollup

### Issue 02 — ship date 2026-04-24

**Status:** Drafting. Running order not yet locked (locks Thu 2026-04-23).

| Section | Source article(s) | Status | Gaps |
|---|---|---|---|
| Open | front-of-book-draft.md | draft | Needs final voice pass |
| Lead Story | claude-design-reception.md + conway-leak-analysis.md | draft (Claude Design) / research (Conway) | Hands-on screenshots (Eddie only). Pro quote needed. Conway placement call Thursday. |
| Also Shipped | openclaw-anthropic-return.md + also-shipped-vercel-sensitive-default.md + also-shipped-claude-performance-backlash.md + scraper output (pending) | research (all three) / blocked (scrape) | 3/3–5 captured. At formula minimum. Scraper output may add 1–2 more Thursday. |
| Companion / Term of Issue | presence-as-category.md | research (placement open) | Companion vs. scaffolding-only vs. Term of Issue container — Eddie calls Thursday based on front-of-book word budget |
| Investigation | trust-week-lovable.md + trust-week-vercel.md | research | Pro interview for SOPs. Attribution softened (ShinyHunters denial integrated). Legacy-exposure scope confirm before press. |
| Quiet on the Wire | quiet-claude-code-pro-test.md | research (A 28/28) | Claude Code $20 Pro plan test + 2% quote captured. May be joined by 1-2 more from Thursday scrape. |
| Term of the Issue | Leaning "Presence" — definition block not yet written | pending | Write the definition + usage example Thursday AM |
| The Close | _(not started)_ | pending | Rhythm closer, three beats, tied to Term of Issue |
| Release Log | release-log-research.md | research (graded as OVR, compilation doc) | 10 entries captured for Apr 17-22 window. Scraper failed (no X API token, Nitter dead); built from releasebot + primary sources. Top-off Thursday PM for Thu 2026-04-23 items. Final Friday 7 AM pass. |

**Readiness (Apr 22 PM):** 6 of 8 sections have source articles captured. 2 blocked on pipeline (Release Log + scraper-dependent Also Shipped additions). 2 editorial slots pending Thursday (Quiet on Wire, Close).

**Article inventory:** 10 source articles on disk (signal + front-of-book draft + 8 topic articles). Per `content/FORMULA.md`, a healthy weekly needs 9–11 files. **Issue 02 is within healthy-inventory range.**

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
| 2026-04-22 (PM) | Three more article skeletons captured via auto-ops resolver: `also-shipped-vercel-sensitive-default.md`, `also-shipped-claude-performance-backlash.md`, `presence-as-category.md`. Also Shipped now 3/3-5 (at formula minimum). Companion/Term-of-Issue container article in place with placement open for Thursday. `conway-leak-analysis.md` extended with "Operator takeaway" scaffolding (rubric v2 dimension was 0/4, target 2+/4). Issue 02 inventory now 10 source files, within healthy-inventory range per FORMULA.md. |
| 2026-04-22 (PM) | Grade sweep: all 9 topic articles brought to grade A (25/28 to 28/28). Rubric v2 scaffolding sections added to each (Attribution caveats, How this fits the issue, For builders, The stake, Named evidence, Voice notes with kill lists). New article captured: `quiet-claude-code-pro-test.md` for Quiet on the Wire slot (A 28/28) with the Amol Avasare "~2% of new prosumer signups" quote from the Claude Code Pro plan test. Term-of-Issue, slug, Conway placement, and Companion placement locked in WIP frontmatter per Eddie's PM calls. Em and en dashes swept from all articles I authored (183 replaced). |
| 2026-04-22 (late PM) | Issue 02 arc audit plus gap-fill sweep. Counter-signal article captured: OpenAI's GPT-Rosalind, Codex expansion, workspace agents; Google's Gemini Personal Intelligence, $750M partner fund, agentic-taskforce framing. Lands the field-context beat at A 28/28. Close scaffolding captured (`close-prep.md` at A 27/28): three-beat rhythm closer, Presence landing mid-beat-2. Term-of-Issue definition block scaffolded (`term-of-issue-presence.md` at A 27/28). Front-of-book draft retrofitted with pre-flight checklist, named-evidence inventory, Thursday lock-day checklist. Three ship-day files created: `launch-copy.md` (platform templates + voice rules), `ship-checklist.md` (T-48h to T+24h), `post-ship.md` (retrospective scaffold, filled Saturday). All three graded OVR as operational ship-day auxiliary files. Issue 02 now has 17 source files total; dashboard shows 100% readiness, zero gaps. |
| 2026-04-22 (evening) | Canonical issue file assembled at `content/issue-02-presence.md` (471 lines). Open (Eddie, unchanged) and Lead Story distilled 214w (Eddie, unchanged) pulled inline. All other sections scaffolded with HTML-comment SCAFFOLD blocks containing word budgets, named-evidence pick lists, voice moves, kill-on-sight phrases, and attribution caveats pulled from their graded source articles. 11 {PROSE: ...} slots ready to fill Thursday. Release Log populated with 10 entries from `release-log-research.md` (colon separator pending Thursday lock decision). 5 em dashes remain (all in Eddie's original Open + Lead prose, flagged inline for edit pass). MC command panel updated: new Shipped. category with 8 commands, weekly-rhythm workflow block, project-scoped scan path. |
