---
issue: 02
slug: presence
title: TBD
term_of_issue: Presence
status: drafting
ship_date: 2026-04-24
grade_override: true
grade_override_reason: "This is the front-of-book draft file for the issue itself, not a source article. It assembles the final magazine prose from the graded source articles. Rubric v2 does not apply: the scoring dimensions (counter-frame, attribution caveats, operator takeaway, named evidence, voice notes, stake) belong in the source articles, not in the compiled issue body. Graded OVR by intent."
sources:
  - https://www.anthropic.com/news/claude-design-anthropic-labs
  - https://www.anthropic.com/news/claude-opus-4-7
  - https://x.com/amolavasare/status/2046724659039932830
  - https://vercel.com/kb/bulletin/vercel-april-2026-security-incident
  - https://www.theregister.com/2026/04/20/lovable_denies_data_leak/
  - https://openai.com/news/
  - https://www.googlecloudpresscorner.com/2026-04-22-Google-Cloud-Commits-750-Million-to-Accelerate-Partners-Agentic-AI-Development
---

# Issue 02: Draft

> Working draft. Do NOT push to the WIP on GitHub without Eddie's review.
> Section order matches STYLE.md: Open → Lead → Also Shipped → Quiet on the Wire → Close → Release Log.

---

## Open

There's a word I once put on an old film-set lesson. The best assistants knew what was needed before the ask. They were there before you knew to call. I called it presence.

Last Friday, Issue 01 hit at 9 AM. Four minutes later, the WhatsApp group asked for three things we didn't deliver: a translation, a podcast, and less recap. I read it twice before I saw what was really in the ask. *Tell us what's arriving, not what already did.*

Here's what's arriving. Claude Design shipped ninety seconds before Issue 01 hit, Anthropic's new product turn in the wild. And a codename called Conway, caught in a source-code leak, describing an agent that doesn't wait to be summoned.

Two shapes. One frequency. This issue tunes to it.

---

## Lead Story: Claude Design (with Conway third act)

_[next]_

---

## Also Shipped

_[pending. 3 to 5 sections, Trust Week material lives here unless it gets its own slot]_

---

## Quiet on the Wire

_[pending]_

---

## The Close

_[pending. rhythm closer, three beats]_

---

## Release Log

_[pending, pulls from `release-log-research.md` on Thursday PM, final pass Friday 7 AM]_

---

## Draft scaffolding (not for print)

> This section is a pre-flight checklist for the writer. Does not ship. The rubric v2 dimensions are scored on the source articles; this file compiles the final prose.

### Section readiness

| Section | Word budget | Source article(s) | Status |
|---|---|---|---|
| Open | 80 to 150 | front-of-book-draft.md (this file) | Drafted. Four paragraphs. Voice-locked. |
| Lead Story (Claude Design) | 200 to 300 | claude-design-reception.md (A 28/28) | Distilled draft in WIP. 214 words. |
| Lead third-act or B-story (Conway) | 200 to 300 or 400 to 700 | conway-leak-analysis.md (A 28/28) | Locked as B-story / Feature slot, Wed PM. |
| Companion to the Lead | 150 to 250 | presence-as-category.md (A 28/28) | Locked as Companion, Wed PM. Prose pending Thursday. |
| Companion (alternative) | 150 to 250 | counter-signal-field-moved.md (scaffolded) | Placement open. Pick Thursday. |
| Investigation (Trust Week) | 400 to 700 | trust-week-lovable.md (A 28/28) + trust-week-vercel.md (A 25/28) | Scaffolded, prose pending Thursday. |
| Also Shipped (3 items) | 3 × 60 to 100 | openclaw-anthropic-return.md (A 25/28), also-shipped-vercel-sensitive-default.md (A 28/28), also-shipped-claude-performance-backlash.md (A 28/28) | Scaffolded, prose pending Thursday. |
| Quiet on the Wire | 50 to 80 | quiet-claude-code-pro-test.md (A 28/28) | Scaffolded. Avasare quote captured. |
| Term of the Issue (Presence) | 100 to 150 | term-of-issue-presence.md | Scaffolded Wed PM. |
| The Close | approx 120 to 200 (3 beats) | close-prep.md | Scaffolded Wed PM. Anchor picked Thursday. |
| Release Log | unbounded, 150w per entry cap | release-log-research.md | 10 entries captured. Top-off Thursday PM. |

### Voice gate pre-flight

Run these checks before prose reaches the WIP file:

- [ ] Scan for "X isn't Y, it's Z" occurrences. Budget: 1 per issue. Currently spent in the Lead ("Anthropic is not building an API company"). Kill any second occurrence.
- [ ] Scan for em dashes and en dashes. Kill all.
- [ ] Scan for forbidden phrases from STYLE.md: EPIC, thrilled, ushers, game-changing, industry-leading, synergies, robust, best-in-class, unveiled, empowers, leverage.
- [ ] Scan for cyber-PR filler: "raises concerns about," "comes on the heels of," "in a statement," "amid growing concerns," "sparks backlash."
- [ ] Scan for hedging language: "arguably," "some might say," "it could be argued," "perhaps," "may be seen as."
- [ ] Verify sentence-length variation. STYLE.md: vary aggressively. Flag any run of three consecutive sentences of similar length.
- [ ] Verify second-person usage is confined to the Open and Close. Kill "you" appearances in Lead, Investigation, Also Shipped, Quiet on the Wire, Term block.

### Named evidence inventory (track to avoid double-spending)

Numbers, quotes, and stats are allocated per section. Reusing a number in two sections dilutes the bite. Track here.

| Number / quote | Article of record | Protected in |
|---|---|---|
| 7.28% (Figma close Apr 17) | Lead Story | Lead; do not re-use in Companion, Close, Counter-signal |
| $100B (Anthropic AWS) | Release Log | Release Log; may appear once in Counter-signal as cross-lab comparison |
| $25B (Amazon investment) | Release Log | Release Log |
| $750M (Google partner fund) | Counter-signal Companion | Counter-signal; do not re-use in Lead third-act |
| 2% (Avasare quote) | Quiet on the Wire | Quiet on the Wire; do not re-use in Lead or Companion |
| $2M (BreachForums listing) | Investigation (Vercel) | Investigation |
| 48 days (Lovable unfixed BOLA) | Investigation (Lovable) | Investigation |
| 4 public positions (Lovable arc) | Investigation (Lovable) | Investigation; may appear once in Close as echo |
| 44 feature flags (Conway leak) | B-story / Feature (Conway) | B-story |
| 59.8 MB cli.js.map | B-story / Feature (Conway) | B-story |
| 512,000 lines of TS | B-story / Feature (Conway) | B-story |
| "evolution of GPTs" (OpenAI) | Counter-signal | Counter-signal |
| "agentic taskforce" (Google) | Counter-signal | Counter-signal |
| 4 minutes (WhatsApp group response to Issue 01) | Open | Open |
| 90 seconds (Claude Design vs. Issue 01 ship) | Open | Open; may rhyme with Close |

### Thursday lock-day checklist (repeats from WIP)

- [ ] Title assigned (currently TBD).
- [ ] Running order frozen.
- [ ] Companion decision: one or two? (Presence-as-category AND Counter-signal, or one of them absorbed.)
- [ ] Open anchor confirmed (time-stamp, WhatsApp, or action-layer).
- [ ] Close scene picked.
- [ ] Term of Issue definition drafted (100 to 150 words).
- [ ] Hands-on Claude Design screenshots (Eddie).
- [ ] Pro interview quote (Trust Week): booked or explicitly deferred.
- [ ] Hero image chosen.
- [ ] OG card designed.
- [ ] Release Log topped off (Thursday PM scrape).
- [ ] Voice gate scans clean.

### Open questions / TODOs before press

- [ ] Decide em-dash / colon separator for Release Log entries (STYLE.md conflict, see release-log-research.md).
- [ ] Confirm all source article cross-references stay tight in the final prose (issue pagination may shift them).
- [ ] Verify the Open's "90 seconds" claim has a source that is not hand-timed.
- [ ] Final reader-voice decision: do we quote the WhatsApp group, or paraphrase?
- [ ] Test read-aloud at Friday 8:45 AM for rhythm.
