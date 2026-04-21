# EDITORIAL.md — Shipped.

> How an issue moves from signal to ship. The human + AI collaboration pattern.

---

## The lifecycle of an issue

Every issue passes through six phases. Each phase has a clear artifact, a decision point, and a handoff. Think of it like a river system — water flows one direction, and each phase is a pool where work collects before spilling into the next.

```
SIGNAL → WIP → DRAFT → VERIFY → STAGE → SHIP
  Mon      Tue-Wed   Thu-Fri    Fri AM   Fri 8:55   Fri 9:00
```

---

## Phase 1 — Signal (Monday–Tuesday)

**Purpose:** Collect the raw material. What did Anthropic ship this week? What broke? What's rumored? What do readers care about?

**Artifact:** Signal report — captured as `content/articles/issue-NN/signal-report.md` with frontmatter linking it to the issue. Update `TRACKER.md` when created.

**Who does what:**

| Actor | Responsibility |
|---|---|
| Claude | Scrapes sources, synthesizes findings, produces the signal report with sourced facts and editorial angles |
| Eddie | Reviews, adds context from WhatsApp group / X / direct conversations, makes editorial calls |

**What the signal report contains:**
- Headline verdict — what's the week's shape?
- One section per story thread with sourced facts, angles, and open TODOs
- Proposed running order with trade-off analysis
- Term-of-issue candidates
- Full source list with URLs

**Rules:**
- Every claim has a primary source URL. No exceptions.
- Relative dates converted to absolute (YYYY-MM-DD) so the doc doesn't decay.
- Confidence level stated for pre-announcement stories ("reported by [outlet]" not "confirmed").
- The signal report is decision input, not prose. Keep it scannable.

---

## Phase 2 — WIP (Tuesday–Thursday)

**Purpose:** Shape the issue. Refine angles, lock the running order, assign the slug.

**Artifact:** `content/issue-NN-wip.md` — the canonical working document in the repo

**Who does what:**

| Actor | Responsibility |
|---|---|
| Claude | Updates WIP with new facts, refines story angles, drafts skeleton sections, tracks open TODOs |
| Eddie | Makes editorial decisions (lead story, running order, what gets cut), resolves open questions |

**What the WIP contains:**
- Frontmatter with `status: draft`, `running_order_locked: false`
- Editorial decisions log (what was decided, when, why)
- Proposed skeleton with section status (researching / to write / blocked)
- Per-story fact sheets with sources
- Thursday decision checklist

**The Thursday lock:**

Thursday is the decision point. By end of Thursday:
- Running order is locked
- Slug is assigned (WIP file renamed to `issue-NN-{slug}.md`)
- Title is chosen
- Term of Issue is picked
- All open TODOs are resolved or explicitly deferred to next issue
- Frontmatter updated: `running_order_locked: true`

After Thursday lock, the structure doesn't change. Only prose and polish.

---

## Phase 3 — Draft (Thursday PM–Friday morning)

**Purpose:** Write the magazine. Front-of-book prose, Release Log entries, the close.

**Artifact:** `content/issue-NN-{slug}.md` — the canonical issue file with actual copy

**Who does what:**

| Actor | Responsibility |
|---|---|
| Claude | Drafts front-of-book sections following STYLE.md, populates Release Log from scraper output, writes the close |
| Eddie | Reviews every section, rewrites in his voice where needed, makes final editorial calls on tone and framing |

**Section order (from STYLE.md):**
1. Cover line — masthead, issue number, date, subhead
2. Open — 80–150 words, opening-line pattern, ends with a turn
3. Lead Story — 200–300 words, editorial
4. Also Shipped — 3–5 short sections, 60–100 words each
5. Quiet on the Wire — rumors, hints, expectations, 50–80 words
6. The Close — rhythm closer, three short beats
7. Release Log — comprehensive, per-entry format from STYLE.md

**Source material:** Before drafting, read all source articles in `content/articles/issue-NN/` — these are the researched, fact-checked inputs. The `TRACKER.md` rollup shows which articles map to which sections and flags any gaps.

**Voice check before drafting:**
- Re-read `content/STYLE.md` (the full doc, not a summary)
- Re-read at least one essay from the voice training corpus
- Run the forbidden-phrase list through your head as a pre-filter
- Budget check: max 1 "X isn't Y, it's Z" in the front-of-book

**Length targets:**
- Lean week front-of-book: 600–800 words
- Heavy week front-of-book: 1,000–1,400 words
- Hard ceiling: 1,500 words (split into sidebar if exceeded)
- Release Log: no ceiling, but per-entry cap of 150 words including code blocks

---

## Phase 4 — Verify (Friday morning)

**Purpose:** Prove the issue doesn't lie. Every claim attested to its source.

**Artifact:** Verification pass/fail report from the pipeline

**Who does what:**

| Actor | Responsibility |
|---|---|
| Pipeline | Runs all verification gates automatically via `pnpm verify` or as part of `pnpm publish` |
| Eddie | Reviews any failures, fixes the markdown, re-runs |

**The five gates:**

1. **URL liveness** — every link fetched, fails on 4xx/5xx (fragile-domain allowlist for known blockers like `red.anthropic.com`, Axios, Medium)
2. **Number attestation** — numeric claims with nearby source links confirmed against the source (formatting-tolerant: `$100M` = `$100 million`)
3. **Quote attestation** — fuzzy match (80% word-overlap threshold) of quoted strings against source text
4. **Date attestation** — "shipped on YYYY-MM-DD" claims confirmed in source
5. **Voice gate** — forbidden phrases scan + "X isn't Y, it's Z" count

**If a gate fails:** the pipeline exits non-zero. Copy must be fixed and verification re-run. There is no override, no skip flag, no "ship it anyway." The verifier is the moat.

---

## Phase 5 — Stage (Friday ~8:55 AM ET)

**Purpose:** Render the final HTML and stage it for publish.

**Artifact:** `../id8labs/public/shipped/NN/index.html` — the rendered magazine page

**Who does what:**

| Actor | Responsibility |
|---|---|
| Pipeline | `pnpm publish <issue-file>` — scrape (cached) + render + verify + stage. Writes HTML to the id8labs deploy target. Runs `git add` in id8labs. |
| Pipeline | **NEVER** runs `git commit`. **NEVER** runs `git push`. |

**Pre-stage checks:**
- Git working tree in `id8labs/` must be clean. If there are unrelated changes, the pipeline refuses to stage.
- Verification must have passed in this same run.

---

## Phase 6 — Ship (Friday 9:00 AM ET)

**Purpose:** Publish. The human gate.

**Artifact:** Live issue at `id8labs.app/shipped/NN/`

**Who does what:**

| Actor | Responsibility |
|---|---|
| Eddie | Reviews the staged HTML one final time. Runs `git commit && git push` from `id8labs/`. |
| Vercel | Auto-deploys ~2 minutes after push. |

**Post-ship:**
- Update `content/index.md` — add the issue to the archive table, set status to `published`
- Update `TRACKER.md` — mark all source articles for this issue as `used`, update the rollup status
- Social copy goes out (see `content/LAUNCH-COPY.md` for the template pattern from Issue 01)
- Monitor WhatsApp group for early reader feedback
- Note any operational lessons in BUILDING.md if something novel happened

---

## The collaboration contract

The division between Claude and Eddie is not about capability — it's about judgment.

**Claude owns:**
- Research and source gathering (with full attribution)
- Signal reports and fact synthesis
- First drafts of all sections (following STYLE.md)
- Release Log population from scraper output
- Verification gate operation
- Pipeline execution up to (but not including) commit

**Eddie owns:**
- Every editorial decision: lead story, running order, what gets cut, what gets promoted
- Final voice — if a section doesn't sound right, Eddie rewrites it
- The Thursday lock — structure decisions are Eddie's call
- The human gate — commit and push
- Reader relationship — WhatsApp group, social, direct feedback
- STYLE.md amendments (between issues only)

**The handoff pattern:**
Claude proposes, Eddie disposes. This means Claude should present options with trade-offs rather than making unilateral editorial calls. "Here are three ways to frame this story, here's what each costs" is better than "I chose this framing."

---

## Issue calendar template

For each new issue, this is the rhythm:

```
WEEK OF ISSUE NN

Mon     Signal collection begins
        Create issue-NN-wip.md with frontmatter
        Start signal report

Tue     Signal report delivered to Eddie
        Eddie makes initial editorial calls (lead, secondary, investigation)
        WIP updated with editorial decisions

Wed     Deep research on locked stories
        Source gathering, fact verification
        WIP skeleton filled in with per-story details

Thu     DECISION DAY
        Running order locks
        Slug assigned, WIP renamed
        Term of Issue picked
        Prose drafting begins (front-of-book)
        PM: scraper run for Release Log data

Fri     7:00 AM  Final scrape run
        8:00 AM  Release Log merged, final copy review
        8:30 AM  Eddie reviews markdown
        8:55 AM  pnpm publish (render + verify + stage)
        9:00 AM  Eddie: git commit && git push (SHIP)
        9:02 AM  Vercel deploys
        9:15 AM  Social copy posted
        Post     Monitor feedback, log lessons
```

---

## When things go wrong

**Verification fails at 8:55 AM:**
Fix the copy. Re-run. The 9 AM target is a target, not a deadline that overrides the verifier. Better to ship at 9:15 with clean copy than at 9:00 with a lie.

**The week is quiet (fewer than 2 Anthropic releases):**
Pivot to ecosystem context — community builds, research citations, competitor moves. The series never skips a Friday. (See VISION.md, "Slow weeks" in index.md.)

**A story breaks after Thursday lock:**
If it's bigger than the locked lead, Eddie can re-lock. The lock is a discipline, not a prison. But the bar is high — the new story has to clearly outweigh the sunk editorial work.

**Eddie is unavailable Friday morning:**
The issue does not ship. The human gate is non-negotiable. Delay to Saturday or skip to next Friday. (This hasn't happened yet. If it does, document the decision in BUILDING.md.)

---

## Changelog

| Date | Change | Reason |
|---|---|---|
| 2026-04-21 | Initial draft. Six-phase lifecycle, collaboration contract, calendar template. | Foundational doc generation — connective tissue for the project. |
