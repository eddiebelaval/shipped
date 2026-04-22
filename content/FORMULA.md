# FORMULA.md — Shipped.

> The weekly build formula. How many articles, which sections, what word budgets.
> If you're writing an issue and don't know where something goes, this file is the answer.

**Read order:** [VISION.md](../VISION.md) → [SPEC.md](../SPEC.md) → [STYLE.md](./STYLE.md) → **FORMULA.md** (this file) → [TRACKER.md](../TRACKER.md).

STYLE.md governs **voice**. FORMULA.md governs **volume and shape**. Together they define what a healthy weekly issue looks like before prose begins.

Authored 2026-04-22 by Eddie Belaval (with Claude). Derived from Issue 00 (the founding dry-run) and the STYLE.md section budgets.

---

## The weekly skeleton

Every weekly issue has two halves: **front-of-book** (editorial, written) and **back-of-book** (Release Log, compiled). The front-of-book has a **mandatory core** of 7 sections and an **optional shelf** of 5 sections that appear only when the week earns them.

### Mandatory core — every issue, no exceptions

| # | Section | Word budget | Input needed |
|---|---|---|---|
| 1 | Cover Line | masthead + issue # + date + 1-sentence subhead | none |
| 2 | The Open | 80–150 | none (editorial hook) |
| 3 | The Lead Story | 200–300 distilled | 1 source article (~800–1,200w) |
| 4 | Also Shipped | 3–5 items × 60–100w each | 3–5 source articles (~300–500w each) |
| 5 | Quiet on the Wire | 50–80 | compiled from signal report |
| 6 | The Close | 3-beat rhythm closer | none (editorial) |
| 7 | Release Log | unbounded (per-entry 150w cap) | scraper output |

### Optional shelf — include only when the week earns the slot

| Section | Include when | Word budget | Input needed |
|---|---|---|---|
| By the Numbers | Week has ≥3 releases with publishable stats | ~15 bullet stats | compiled from signal + scrape |
| Companion to the Lead | Lead story has comparable cross-model/cross-product data worth tabling | 150–250 | 1 data table + ~3 paragraphs |
| Feature | A product family shipped a coherent multi-release arc (like Apr 8–9 agent stack in Issue 00) | 400–700 | 1 source article (~800–1,500w) |
| Investigation | A multi-source story with a reporting angle beyond "what shipped" — breaches, leaks, policy shifts | 400–700 | 1 source article (~1,000–1,500w) + ≥3 primary sources |
| Term of the Issue | The week has a new concept worth naming (e.g., "shadow release" in Issue 00, candidate "presence" in Issue 02) | 100–150 definition block | none (editorial naming act) |

**Rule of thumb:** a typical weekly uses **mandatory core + 1–2 shelf items**. Issue 00 used the full shelf because it covered three weeks. Lean weeks may ship with just the core.

### Front-of-book length ceilings (from STYLE.md)

- Lean week: **600–800 words**
- Heavy week: **1,000–1,400 words**
- Hard ceiling: **1,500 words**

If the week needs more, split into a sidebar. If the sidebar also overflows, something should have been a separate post.

---

## The weekly article inventory

Source articles are the raw material that feeds the prose. They live in `content/articles/issue-NN/` and move through three states: **research → draft → used**. Every source article is registered in TRACKER.md.

### Minimum viable inventory (lean week)

For a week that ships **mandatory core only**, the article inventory is:

- `signal-report.md` — Monday research sweep (always)
- `lead-story-{topic}.md` — the lead source article (~800–1,200w research)
- 3 × `also-shipped-{topic}.md` — one per Also Shipped item (~300–500w each)
- `launch-copy.md` — Friday launch copy
- `ship-checklist.md` — operational ship-day notes
- `post-ship.md` — lessons captured after publish

**Total: 8 files minimum** (1 signal + 1 lead + 3 also-shipped + 3 ops). If you have fewer, you don't have enough to ship.

### Healthy inventory (typical week with 1–2 shelf items)

Add one of:

- `feature-{topic}.md` (~800–1,500w research) — for a Feature slot
- `investigation-{topic}.md` (~1,000–1,500w research, ≥3 sources) — for an Investigation slot
- 1–2 more `also-shipped-{topic}.md` — if the week had more than 3 meaningful minor releases

**Total: 9–11 files.** This is the pace Shipped. runs at sustainably.

### Heavy inventory (multiple shelf items — rare)

Add multiple shelf-item articles + Companion to the Lead data table + By the Numbers compilation notes.

**Total: 12–15 files.** Issue 00 is an example; this is not the weekly default.

---

## The decision tree — what goes where

When a week's signal is collected, run this decision tree on Thursday before the running-order lock.

```
1. Pick the lead.
   → One story carries the spine of the week.
   → Must have enough material for 200–300 distilled words + a ~1,000-word source article.
   → If two stories compete, the one that absorbs a wider range of releases wins.

2. Pick the shelf (0–2 items typical, 3 max).
   → Is there a product-family arc this week? → FEATURE
   → Is there a multi-source story beyond "what shipped"? → INVESTIGATION
   → Is the lead data-heavy with cross-competitor comparisons? → COMPANION TO THE LEAD
   → Did the week produce a new concept worth naming? → TERM OF THE ISSUE
   → Are there ≥3 releases with publishable stats? → BY THE NUMBERS

3. Fill Also Shipped (3–5 items).
   → Everything that matters but isn't lead or shelf.
   → Policy signals, smaller product updates, partnerships with operator impact.
   → Each item needs its own source article before prose begins.

4. Compile Quiet on the Wire.
   → What's rumored, hinted, expected. Not announced.
   → Pulled from signal report, no new article needed.

5. Write the Close.
   → Rhythm closer. Three beats. Last one lands.
   → Tied back to the Term of the Issue if one was named.

6. Run the scraper for the Release Log.
   → Thursday PM + Friday 7 AM scrapes.
   → Everything released in the window, grouped A–G per STYLE.md.
```

---

## The weekly rhythm

| Day | Phase | Slash command | Output |
|---|---|---|---|
| Mon | Signal collection | `/shipped-signal` | `signal-report.md` |
| Tue–Wed | WIP refinement | `/shipped-wip` | `issue-NN-wip.md` updates + per-topic source articles captured |
| Thu AM | Running order lock | (human decision) | running order frozen, slug assigned, Term of Issue named |
| Thu PM | Front-of-book draft | `/shipped-draft` | prose populated into `issue-NN-{slug}.md` |
| Thu PM | Scraper run | `pnpm scrape` | Release Log data |
| Fri 7 AM | Final scrape | `pnpm scrape` | Release Log finalized |
| Fri 8 AM | Review | (human) | Eddie reads, tweaks, approves |
| Fri 8:55 AM | Render + verify + stage | `pnpm publish` → `/verify-shipped` → `/publish-shipped` | HTML staged in `../id8labs/public/shipped/NN/` |
| Fri 9 AM | Ship | (human) | `git commit && git push` from `id8labs/` |

**Invariant:** the Thursday lock is the last point before prose begins. Running order, slug, and Term of Issue are frozen after the lock. If new facts surface Friday, they go in a `[corr]` commit post-ship — not into this issue.

---

## Slot-based decisions — reference cases

### Feature vs. Investigation

Both are 400–700 word slots. They answer different questions.

- **Feature** = *"Here is a product arc that matters. Here is what it composes into."* Editorial-explanatory. Example: Issue 00's "The agent stack got serious" (Managed Agents + advisor tool + `ant` CLI).
- **Investigation** = *"Here is what happened beyond the announcement. Here is who's telling what story, and where the gaps are."* Reporting + attribution. Example: Issue 00's "Glasswing." Candidate for Issue 02: "The Trust Week."

One per issue, not both. If both feel warranted, one becomes a sidebar and the other takes the slot.

### When to name a Term of the Issue

A Term of the Issue is earned, not scheduled. Name one when:

- The week produced a pattern that doesn't have a shorthand yet (Issue 00: "shadow release")
- The term ties ≥2 threads in the issue together (Issue 02 candidate: "presence" ties Conway + Claude Design + trust surface)
- The definition holds outside this week — a reader could use the term in conversation next month

If none of the above, skip the slot. An unearned Term of Issue reads like a ToK chapter heading.

### When to promote to Lead third-act vs. standalone section

When a secondary story tightens the Lead's thesis, fold it into the Lead as a third act instead of giving it its own section. When the secondary story contradicts or pivots away from the Lead's thesis, give it its own slot.

Example (Issue 02): Conway **tightens** the "Anthropic ships products, not just models" thesis → Lead third-act. Trust Week **pivots** to a different thesis ("platforms the products depend on are failing") → standalone Investigation.

---

## What counts as "enough material"

A section is ready to write when:

| Section | Minimum material |
|---|---|
| Open | An opening-line pattern picked (see STYLE.md Pattern 1/2/3) + a turn to land |
| Lead Story | ≥1 source article in `draft` status, ≥3 primary sources cited, at least one concrete quote or number |
| Also Shipped item | ≥1 source article in `research` status, ≥1 primary source URL, the operator-relevance line clear |
| Feature | ≥1 source article in `draft`, ≥2 releases it composes, 1 concrete code/config example |
| Investigation | ≥1 source article in `draft`, ≥3 primary sources, ≥1 attribution softening or caveat resolved |
| Quiet on the Wire | Signal report flags ≥3 items worth mentioning, each with a line-item reason |
| Term of the Issue | Definition holds, ≥1 usage example, ≥1 cross-reference to another section |
| Release Log | Scraper run within the last 24 hours |

If a section doesn't meet its bar by Thursday AM, either **drop it** (skip the slot) or **push the lock** (rare, last resort, logged in the issue file).

---

## Attribution & verification

Every source article captures these before it can leave `research` status:

1. **Primary sources** — direct links to the originating material (Anthropic announcement, company bulletin, research paper, etc.)
2. **Independent coverage** — at least one non-affiliated outlet that verifies the primary claim
3. **Quotes** — attributed to a named human (title, affiliation, source link)
4. **Numbers** — each stat has a source link within 3 paragraphs of its appearance
5. **Attribution caveats** — any "reported by" vs. "confirmed by" distinctions logged explicitly (see `openclaw-anthropic-return.md` for the pattern)

The verifier (`/verify-shipped`) runs these gates on the final prose, but source articles should already be clean before Thursday lock. Catching a missing source at draft time is free; catching it at Friday 8:55 AM is a ship-day fire.

---

## Drift watch — rules for updating this formula

1. **An unearned section shipped anyway.** If a Feature or Investigation slot went out with <400 words or thin sourcing, the bar isn't being held. Raise it, don't lower it.
2. **The inventory grew past 15 articles.** If a typical week needs >15 source articles, the scope has drifted. Either cut items or stop counting them as source articles.
3. **The 1,500-word ceiling broke.** Twice in a row = the formula needs a "big issue" variant. Once is an outlier.
4. **A new section pattern emerged.** Like STYLE.md, the formula grows. Add to the optional shelf, don't replace the mandatory core.

When any of the above fires, amend this file with a changelog entry below. Do not retcon — record what changed and when.

---

## Changelog

| Date | Change | Reason |
|---|---|---|
| 2026-04-22 | Initial draft. Derived from Issue 00 + STYLE.md + Issue 02 WIP work. | First explicit formula doc; previously implicit in the triad. |
