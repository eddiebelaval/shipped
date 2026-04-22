# RUBRIC.md — Shipped.

> The grading rubric for source articles. Seven dimensions, twenty-eight points, one letter grade.
> If an article is below **B (21/28)**, it's not ready for prose.

**Read order:** [VISION.md](../VISION.md) (identity) · [STYLE.md](./STYLE.md) (voice) · [FORMULA.md](./FORMULA.md) (volume/shape) · **RUBRIC.md** (readiness).

STYLE.md governs how the magazine sounds. FORMULA.md governs how an issue is shaped. **RUBRIC.md governs whether an individual source article does what Shipped. does.**

Authored 2026-04-22 by Eddie Belaval (with Claude). Rewritten same day after audit against VISION.md — the v1 rubric was internally consistent but identity-shallow. This v2 grades substance, not scaffolding.

---

## What the rubric is measuring

A source article is *ready for prose* when it lets the draft-phase writer produce the thing Shipped. actually is:

> *"A weekly magazine for builders who can't — or won't — stay glued to social media, aggregating the week's Anthropic releases into one read that's worth the time."* — VISION.md

That sentence contains the whole assignment:

- **Weekly magazine.** Not a feed, not a digest. An edited product with an editorial identity.
- **Builders who can't stay glued.** An audience with limited attention and technical fluency.
- **Aggregating the week.** Tying threads together; not stenographing announcements.
- **One read worth the time.** Signal, not noise. Every section earns its slot.

Every rubric dimension below traces back to one of those demands. If a dimension doesn't, it got cut.

---

## The seven dimensions

Each article is scored 0–4 on seven dimensions. Total: 28 points. The grader looks for machine-readable signals (section headers, frontmatter, specific vocabulary). The editor (Eddie) makes the final call — this is an advisory layer, not an auto-gate.

### 1 · Sourcing & primary link (0–4)

**Identity anchor:** VISION moat #1 — *"Every claim passes through an attestation gate."*

How load-bearing are the facts? Is there at least one primary source (the originating company announcement, research paper, official bulletin, release notes)? Is there independent verification from a second outlet?

| Score | What it looks like |
|---|---|
| **4** | ≥1 primary source (Anthropic, company bulletin, research paper) + ≥3 total sources + ≥2 unique outlets |
| **3** | ≥1 primary + ≥2 total sources |
| **2** | ≥2 sources, no primary — coverage-only |
| **1** | Single-source dependency |
| **0** | No sources listed |

**Machine signal:** count of `sources:` entries in frontmatter + URL pattern-match against primary-source domain allowlist (anthropic.com, red.anthropic.com, platform.claude.com, support.claude.com, transformer-circuits.pub, github.com/anthropics, vercel.com/kb, openai.com, etc.) + count of unique hostnames.

### 2 · Attribution discipline (0–4)

**Identity anchor:** VISION moat #1 + the ShinyHunters lesson — *softened attribution must be logged, not silently accepted.*

Are "reported by" vs. "confirmed by" vs. "claimed by" distinctions made explicit? When coverage credits an attribution that's been retracted, is the softening captured?

| Score | What it looks like |
|---|---|
| **4** | `## Attribution caveats` section with ≥3 specific caveats, each naming an entity (company, outlet, source) |
| **3** | Section with 2 specific caveats |
| **2** | Section exists with ≥1 caveat OR inline softening language throughout |
| **1** | No section but some attribution vocabulary inline |
| **0** | No attribution discipline visible |

**Machine signal:** presence of `## Attribution caveats` heading + bullet count within + detection of named-entity capitalization patterns + softening vocabulary (`reported`, `claimed`, `denied`, `initially credited`, `per `, `confirmed by`, `softened`).

### 3 · The counter-frame (0–4)

**Identity anchor:** Issue 00's Lead Story — *"The chart that wasn't about Opus 4.7."* The house move: the headline isn't the announcement.

Does the article find the story that *isn't* the announcement? Every strong Shipped. piece has a second read — what the launch reveals, what gets ignored, what the next chart is actually showing. A piece that only reports *what shipped* is a press release.

| Score | What it looks like |
|---|---|
| **4** | Explicit counter-frame articulated — a section or clear passage saying "the beat is not X, it's Y" — supported by specific evidence (a chart, a quote, a price move, a policy precedent) |
| **3** | Counter-frame present, named, but thinly supported |
| **2** | Article implies a second read but doesn't crystallize it |
| **1** | Announcement-centered reporting with mild analytical framing |
| **0** | Straight announcement coverage — reads as a press release |

**Machine signal:** presence of counter-frame vocabulary (`the headline isn't`, `but the story is`, `the implication is`, `the real news`, `the beat is`, `what matters isn't`, `the frame that matters`, `the twist`, `the counter-read`, `not the announcement`, `the tell`, `what's actually`, `the second news`, `that's the news`) + dedicated analytical section + named evidence (charts, prices, quotes).

### 4 · Operator takeaway (0–4)

**Identity anchor:** VISION audience — *"A builder who has too much to track and wants the week's signal."*

What should the reader actually do or know? Every magazine-worthy piece lands an action-layer implication: a check to run, an assumption to revise, a scope to audit, a migration to schedule. Shipped. respects builder time by answering *"so what do I do?"*

| Score | What it looks like |
|---|---|
| **4** | Dedicated section (`## Operator-layer implications` / `## For builders` / `## SOPs`) with ≥3 actionable items, each imperative-verb-led and specific |
| **3** | Section + 1–2 actionable items OR imperatives scattered throughout |
| **2** | Implicit takeaway — reader can infer action but it's not stated |
| **1** | Technical detail relevant to builders, no explicit takeaway |
| **0** | Purely informational — no action implied |

**Machine signal:** presence of sections like `## Operator-layer implications`, `## For builders`, `## SOPs`, `## What to do`, `## If you use` + count of imperative verbs at bullet start (`audit`, `rotate`, `check`, `verify`, `migrate`, `update`, `stop`, `assume`, `re-issue`, `revoke`, `watch`).

### 5 · Stake & stance (0–4)

**Identity anchor:** STYLE tone default — *"Opinions stated, never hedged."*

Does the article state a position? Shipped.'s voice is opinionated. "Neutral reporting" reads as press release; stated stance reads as magazine. The beat often lives in the evaluative claim — *this matters, this doesn't, this is a precedent, this is a one-off.*

| Score | What it looks like |
|---|---|
| **4** | ≥3 declarative/evaluative claims + zero hedging language |
| **3** | ≥2 claims + minimal hedging |
| **2** | ≥1 claim OR stance muddied by hedges |
| **1** | Reporting with reserved posture — stance inferrable |
| **0** | No stance, all neutral — "presents both sides" |

**Machine signal:** declarative-claim patterns (`this matters because`, `the posture is`, `the call is`, `what X chose`, `the answer is`, `that's the news`, `the precedent is`) + strong evaluative verbs (`conceded`, `signals`, `reveals`, `refused`, `doubled down`, `broke`, `cracked`) + **hedging vocabulary that reduces score** (`arguably`, `some might say`, `it could be argued`, `perhaps`, `may be seen as`, `one could`).

### 6 · Throughline (0–4)

**Identity anchor:** VISION — *"Nobody ties the week together. Shipped. is the tie."*

Does the article connect to the issue's thesis, term of the issue, or other articles in the issue? An isolated piece with no thread to the rest of the issue is newsletter filler. Shipped.'s job is the tie.

| Score | What it looks like |
|---|---|
| **4** | Explicit cross-reference to ≥2 other issue elements (other articles, Term of the Issue, portfolio thesis) named by topic |
| **3** | ≥1 cross-reference OR thesis connection |
| **2** | Implicit thread awareness — mentions issue-level concepts without naming the connection |
| **1** | Standalone but thematically adjacent |
| **0** | Isolated — no issue-level connection |

**Machine signal:** cross-reference vocabulary (`ties back to`, `echoes`, `same pattern as`, `same shape as`, `the counterweight`, `the comparand`, `from the Lead`, `alongside`, `in the same issue`) + explicit mention of other article topics (Trust Week, Conway, Claude Design, OpenClaw, etc.) + explicit mention of the Term of the Issue (Presence, Trust, etc.).

### 7 · Voice setup (0–4)

**Identity anchor:** STYLE kill rule — *"If it sounds like a press release, kill it. If it sounds like a LinkedIn post, kill it twice."*

Does the article give the draft-phase writer what they need to write in Shipped.'s voice? Specifically: named STYLE.md moves, opening-line patterns, phrase-kill list for corporate-comms language found in sources.

| Score | What it looks like |
|---|---|
| **4** | `## Voice notes` section + named STYLE.md move (A/B/C) or opening-line pattern + phrase-kill list with ≥3 specific phrases the article's sources used |
| **3** | Section + (named move OR specific kill list) |
| **2** | Section with generic voice guidance |
| **1** | No section but voice-aware prose inline |
| **0** | No voice consideration |

**Machine signal:** `## Voice notes` heading + named moves (`Move A`, `Move B`, `Move C`, `memoir → philosophy`, `punchline isolation`, `rhythm closer`) + opening-line pattern references (`Pattern 1`, `in medias res`, `stat-first`) + phrase-kill markers (`forbidden phrases`, `kill on sight`, `do not use`).

---

## Letter grades

Total score maps to a letter grade.

| Score | Grade | Status | What it means |
|---|---|---|---|
| **25–28** | **A** | Ship-ready | Move to `draft`. Prose can begin with confidence. |
| **21–24** | **B** | Solid | Move to `draft`. The weakest dimension is the first thing to fix in revision. |
| **15–20** | **C** | Needs work | Stay in `research`. Two weakest dimensions need attention before draft. |
| **9–14** | **D** | Significant gaps | Stay in `research`. Multiple dimensions failing — not safe to draft against. |
| **0–8** | **F** | Not ready | Not a source article — a sketch. Either commit to the reporting or archive. |

**Hard rule:** issue can't ship if any `used` article graded below B at press time.

---

## What the grader is and isn't

**The grader is advisory.** It pattern-matches signals in markdown. It can flag:
- Missing sections that the rubric rewards
- Hedging language that contradicts stance
- Counter-frame vocabulary present or absent
- Cross-references present or absent

**The grader cannot judge:**
- Whether the counter-frame is *correct* (is this actually the right second read?)
- Whether the stance is *defensible* (is this opinion supported by the evidence?)
- Whether the operator takeaway is *actionable in practice* (does this SOP actually work?)
- Whether the throughline is *meaningful* (does this connection add or feel forced?)

Those are editorial calls. The rubric exists so the editor can see readiness at a glance and apply judgment where it matters. The rubric is the floor; the editor is the ceiling.

---

## Overrides

Rare, logged in the article itself:

```yaml
---
grade_override: true
grade_override_reason: "Sidebar-only beat; full RUBRIC doesn't apply"
grade_override_by: Eddie
grade_override_date: 2026-04-23
---
```

Override shows as "OVR" in the dashboard with the reason on hover. Tracked in TRACKER.md changelog. Three overrides in one issue triggers a rubric review.

---

## Drift watch — when to amend the rubric

1. **Three issues in a row with all-A grades.** The bar is too low. Tighten one dimension or add an eighth.
2. **High-graded articles keep failing the voice gate at verify time.** Dimension 7 is under-calibrated. Sharpen its signals.
3. **Low-graded articles keep shipping anyway with Eddie's override.** The rubric is wrong, not the articles. Interview and amend.
4. **The same three dimensions always score low.** Either they're miscalibrated, or the team has a blind spot worth codifying. Investigate.

When any of the above fires, amend this file with a changelog entry. Rubric changes apply to the **next** issue, never retroactively to one in flight.

---

## Changelog

| Date | Change | Reason |
|---|---|---|
| 2026-04-22 | v1 draft. 6 dimensions × 4 points = 24. Structural signals only. | Dashboard surfaced the need — articles needed a readiness proxy. |
| 2026-04-22 | v2 rewrite. 7 identity-aligned dimensions × 4 points = 28. | Audit against VISION.md revealed v1 was grading scaffolding, not substance. v1 was gameable — a press-release-voice article with the right H2s could grade A. v2 grades the house moves (counter-frame, operator takeaway, stake, throughline). |
