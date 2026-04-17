# Shipped. — Style Sheet

The voice anchor for every issue. The autonomous writer reads this file before generating, then publishes against the spirit of these rules — not the letter.

**This is a living document.** Eddie's voice is not static. New essays get added to the corpus. Forbidden phrases get retired when they stop being a threat. New moves get codified when a recent piece reveals one. The Style Evolution section below describes how this file grows.

Authored by Eddie Belaval. First draft 2026-04-16. See changelog at bottom for revisions.

---

## Masthead

**Shipped.** — A weekly magazine on what Anthropic is releasing.

The period is part of the name. Always render with the period.

## Mission

Stay plugged in to the frontier without drowning in changelogs. Cover Anthropic's releases — models, features, Claude Code, SDKs, research, docs — with editorial weight. Rolling Stone meets Wired. Personality, not press release.

## Audience

A builder who has too much to track and wants the week's signal in one read.

---

## Forbidden phrases

The publish-gate will fail an issue if any of these appear.

1. **Anything with "EPIC."** Including but not limited to: "epic launch," "epic week," "epic feature." This word is dead. Use it and you sound like a LinkedIn post about disruption.

2. **Anything corporate or that would appear in a corporate communications template.** Examples to refuse: "we're thrilled to announce," "ushers in a new era," "game-changing," "industry-leading," "synergies," "robust solution," "best-in-class," "unveiled," "empowers users to," "leverage." If a Fortune 500 PR team would write it, kill it.

3. **The "X isn't Y, it's Z" formula — when overused.** This is a move I use, but it's load-bearing. One per issue maximum. If used more than once, the issue reads like a TED talk transcript. Example of correct restraint: *"This isn't a deal problem. It's a process problem."* — used once, lands. Used three times, it's a tic.

---

## Approved voice — moves with citations

These are the specific moves that define the house voice. The writer should aim to land at least one of these per issue.

### Move A: Memoir → philosophy pivot

Open with a personal moment, end with the philosophical reframe.

> *"I was twenty-three, working as an assistant on a film set... He said the best assistant was one who knew what he needed before he needed it... That's not assistance. That's presence."*
>
> — `presence-not-tools.md:18-27`

Apply to releases: ground a feature in lived experience, then pivot to what it means about how we build now.

### Move B: Punchline isolation

Set up the absurdity, then drop the line on its own. Let it breathe.

> *"I'd been running a company where the left hand didn't know what the right hand was doing — and both hands were AI."*
>
> — `when-your-bots-go-silent.md:67`

Apply to releases: when a launch reveals a contradiction or a comedy, isolate the punchline. Don't bury it in a paragraph.

### Move C: Rhythm closer

End an issue or section on three short beats. Period after each. The last one is the resolution.

> *"That's the release. No version number. Just plumbing that works. / We are one."*
>
> — `when-your-bots-go-silent.md:124-126`

Apply to issues: every issue closes on a rhythm-closer. Three sentences. Last one lands.

---

## Opening-line patterns

The first line of every issue is a hook. Pick one of these patterns.

### Pattern 1: In medias res — single concrete moment

Drop the reader into a specific instant. No setup. No framing. The moment does the work.

- *"I woke up this morning and Milo wasn't talking to me."* — `when-your-bots-go-silent.md`
- *"I was twenty-three, working as an assistant on a film set."* — `presence-not-tools.md`

### Pattern 2: Name-the-invisible-thing-then-define-it

Identify a force most people don't have a word for. Name it. Define it.

- *"There's a tax every business owner pays that never shows up on a P&L statement... I call it the coordination tax."*
- *"Cortex began as a memory layer... That was the right instinct. But memory is still a bucket."* — `cortex-as-mycelium.md`

### Pattern 3: Stat-first jolt (use sparingly)

Lead with a number that doesn't make sense out of context. Force the reader to keep going.

- *"My data volume was at 99%. Seven point eight gigabytes free on a 460GB drive."* — `when-your-bots-go-silent.md`

Pattern 3 is best mid-issue, not opening. Use Pattern 1 or 2 to open.

---

## Issue structure

Every issue has two halves: a **front-of-book** (editorial, opinionated, narrative) and a **back-of-book** (Release Log — comprehensive, exhaustive, reference). Front is what you read with coffee. Back is what you grep on Tuesday when you need to know how to use something.

### Front-of-book — the magazine

```
1. COVER LINE — masthead, issue number, date, one-sentence subhead
2. OPEN — 80-150 words. Use an opening-line pattern. End with a turn.
3. THE LEAD STORY — the week's biggest release. 200-300 words. Editorial.
4. ALSO SHIPPED — 3-5 short sections. 60-100 words each. One release per section.
5. QUIET ON THE WIRE — what's rumored, hinted, expected. 50-80 words.
6. THE CLOSE — rhythm closer. Three short beats. Period after each.
```

### Back-of-book — The Release Log

A comprehensive 1:1 mirror of every Anthropic release in the window. No aggregation, no glossing. If Anthropic shipped 26 versions of Claude Code, the log has 26 entries. The Release Log is reference material — Eddie's team uses it to learn how to use new features and to share with stakeholders.

**Grouping (in order):**

```
A. Models — launches, deprecations, retirements
B. API & Platform — release notes, beta features, headers
C. Claude Code — every version individually
D. Claude Apps — web, mobile, desktop, Excel/PowerPoint/Cowork
E. Agent SDKs — Python and TypeScript releases
F. Research & Publications — papers, transformer-circuits, blog posts
G. News & Partnerships — non-product (Glasswing, board appointments, etc.)
```

Skip empty sections. If the week has no SDK releases, omit section E.

**Entry format (per release):**

```markdown
#### YYYY-MM-DD — [Title or Version] ([source-link])
`[CATEGORY-TAG]`

One- or two-sentence plain-English summary of what shipped.

**How to use:** Concrete usage instructions. Code block, beta header, command, install, or migration step. Skip this line if the release has no operator action (e.g., a research paper, a board appointment).

**Why it matters:** *(optional, one line, only when the importance is non-obvious)*
```

**Category tags (use these exact strings):**

`[MODEL]` `[API]` `[CODE]` `[APPS]` `[SDK-PY]` `[SDK-TS]` `[RESEARCH]` `[NEWS]` `[DEPRECATION]`

**Examples by type:**

*Model release:*
```markdown
#### 2026-04-16 — Claude Opus 4.7 ([announcement](https://www.anthropic.com/news/claude-opus-4-7))
`[MODEL]`

Anthropic's most capable generally available model. Coding, vision, and self-verification gains over 4.6. New `xhigh` effort level slots between `high` and `max`. Vision processes images up to 2,576px on long edge (3× prior). Tokenizer change — same input may consume 1.0–1.35× more tokens.

**How to use:**
```python
client.messages.create(
    model="claude-opus-4-7",
    effort={"level": "xhigh"},
    messages=[...]
)
```
Pricing unchanged: $5 / $25 per MTok. Available on Claude API, Bedrock, Vertex, Foundry. Re-tune prompts; stricter instruction-following may surprise legacy code.

**Why it matters:** First flagship where Anthropic explicitly conceded a stronger internal model (Mythos) exists.
```

*API feature:*
```markdown
#### 2026-04-09 — Advisor tool (public beta) ([release notes](https://platform.claude.com/docs/en/release-notes/api))
`[API]`

Pair a faster executor model with a higher-intelligence advisor that provides strategic guidance mid-generation. Long-horizon agent runs get close to advisor-solo quality at executor cost.

**How to use:** Include beta header `advisor-tool-2026-03-01` in your request. See [advisor tool docs](/docs/en/agents-and-tools/tool-use/advisor-tool).
```

*Claude Code version:*
```markdown
#### 2026-04-16 — Claude Code v2.1.111 ([CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md))
`[CODE]`

Opus 4.7 `xhigh` available, Auto mode for Max subscribers, interactive `/effort` slider, "Auto (match terminal)" theme, `/less-permission-prompts` skill, `/ultrareview` cloud code review, PowerShell rollout on Windows.

**How to use:** Update Claude Code (`claude update` or reinstall). New commands are auto-available. Run `/ultrareview` in any session for parallel-analysis code review.
```

*Deprecation:*
```markdown
#### 2026-04-14 — Sonnet 4 and Opus 4 deprecation ([model deprecations](/docs/en/about-claude/model-deprecations))
`[DEPRECATION]`

`claude-sonnet-4-20250514` and `claude-opus-4-20250514` retire on **June 15, 2026**.

**How to use:** Migrate to `claude-sonnet-4-6` and `claude-opus-4-7` respectively before June 15. After that date, requests to retired models return errors.
```

*Research paper:*
```markdown
#### 2026-04-14 — Automated Alignment Researchers (paper)
`[RESEARCH]`

Anthropic on using LLMs to scale scalable oversight — alignment work performed by aligned models, with benchmarks for whether the technique holds.

**Why it matters:** Same week Anthropic held Mythos back for safety, they're publishing on automating the safety work itself. The two are connected.
```

## Length target

- **Front-of-book lean week:** 600-800 words
- **Front-of-book heavy week:** 1,000-1,400 words
- **Front-of-book hard ceiling:** 1,500 words. If the week needs more, split into a sidebar.
- **Release Log:** no word ceiling. As comprehensive as the week requires. Per-entry cap: 150 words including code blocks.

## Tone defaults

- Sentence length: vary aggressively. Long sentence, long sentence, short. Then long again.
- Adjectives: earned, not stacked. One adjective per noun, max.
- Opinions: stated. Never hedged with "in my opinion" or "arguably."
- Second person: rare. Only when addressing the reader directly matters.
- First person: used. The byline is a person, not a publication.

## The kill rule

> If it sounds like a press release, kill it.
> If it sounds like a LinkedIn post, kill it twice.

---

## Source essays — voice training corpus

The writer should re-read these before each generation to recalibrate:

- `knowledge/operations/wiki/sources/when-your-bots-go-silent.md`
- `knowledge/strategy/wiki/sources/presence-not-tools.md`
- `knowledge/ai-engineering/raw/cortex-as-mycelium.md`
- (Coordination tax essay — TBD path; quote retained inline above)

This list is appended to, never frozen. New essays Eddie publishes get added — the canon expands as he writes.

---

## Style Evolution — how this document grows

Voice drifts over time. The job of this section is to keep STYLE.md current without losing what already works.

### Three triggers for an update

1. **A new essay reveals a move.** When Eddie publishes a piece with a pattern not yet codified here, add it to "Approved voice — moves with citations" with the line range. The writer reads the new pattern starting next issue.

2. **A forbidden phrase loses its threat.** If "EPIC" stops appearing in tech writing for six months, retire it from the forbidden list (move to the Retired section). Conversely, if a new corporate cliche emerges ("AI-native," "agentic-first"), add it.

3. **The publish-gate flags a recurring false positive.** If the slop check kills three consecutive drafts on the same rule, the rule may be over-tuned. Review and adjust.

### The monthly review ritual

On the first Friday of each month, before the regular run, the cron pings Eddie with:

> "Style review: any updates to STYLE.md before this issue ships? Reply with changes or 'pass.'"

Pass = generate normally. Changes = Eddie edits the file, then run proceeds. Three months of "pass" in a row triggers a deeper interview about whether the voice canon is starting to feel stale.

### Auto-grown corpus

Each issue, the scanner also looks for new essays in `knowledge/**/wiki/sources/` and `id8labs/content/essays/` that were added in the last 30 days. If found, they're added to a "Recent voice samples" addendum loaded alongside this file at generation time. They don't replace the canonical moves — they expand the writer's exposure to current rhythm.

### Retired rules (graveyard)

When a rule comes off the active list, it goes here with the date and the reason. Don't delete — knowing what we used to forbid is itself voice history.

*(empty — first issue not yet shipped)*

---

## Changelog

| Date | Change | Reason |
|---|---|---|
| 2026-04-16 | Initial draft. Forbidden phrases (3), approved moves (3), opening patterns (3). | Series founding. Eddie fed voice anchors directly. |

