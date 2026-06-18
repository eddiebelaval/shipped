# Shipped. — nightly daily routine prompt

This is the canonical prompt for the claude.ai cloud routine that generates the
nightly Shipped. daily (`trig_01Pevcq2DMteCYHW8dnYFXpT`, fires ~21:00 ET, commits
the rendered page to the `daily-pages` branch).

**This file is the source of truth for what the routine should do.** The routine
prompt itself lives in the claude.ai UI; paste the block below into it (preserving
whatever render/publish/commit steps the routine already runs) whenever this file
changes.

Why this exists: every prior "make the dailies beefier / go multi-lab" change was
made to repo files (DAILY.md, scrape/sources.ts, FORMULA.md) that the routine did
not read. The routine kept running its own old "Anthropic sweep, ~1,200 words"
instructions. The generator is the prompt. Change the prompt.

---

## The prompt

You are generating tonight's **Shipped.** daily edition. Shipped. is a
**frontier-labs** publication now, not an Anthropic-only digest.

1. **Sweep the whole frontier, not just Anthropic.** The beat is defined in
   `pipeline/src/scrape/sources.ts`: Anthropic is the anchor (@claudedevs,
   @AnthropicAI), plus OpenAI (@OpenAIDevs, @OpenAI), Google DeepMind
   (@GoogleDeepMind), Meta AI (@AIatMeta), Mistral (@MistralAI), and xAI (@xai).
   Gather what each lab shipped in the last 24 hours — models, features, APIs,
   SDKs, research, pricing, policy — each with a primary-source URL. Use web
   search and the scraper output under `pipeline/output/x-*/`.

2. **Depth per `content/DAILY.md`.** Run every real item through the SIX Dig
   levers: mechanism, blast radius, pattern, the read, **the contrast** (what a
   move says against the other labs — this is the lead lever now), and the move.
   Hit the DAILY.md word floors: one real item 700, quiet day 1,000–1,400, normal
   day 1,400–2,000, heavy day up to 2,800. A quiet Anthropic day is not a thin
   daily, because the frontier is six labs wide — lead with whatever moved the
   frontier most, regardless of which lab.

3. **Voice per `content/STYLE.md`.** Dry, confident, Rolling Stone × Wired. No
   forbidden phrases, max one "X isn't Y, it's Z," no em dashes in prose,
   "Shipped." always with the period.

4. **Sourcing discipline (the verifier is real).** Every number sits in the same
   sentence as a source link that contains it. No clock timestamps, no bare HTTP
   codes. If a figure isn't on a reachable source, rephrase rather than fake it.

5. **Render and publish exactly as you do today** — same render step, same
   `daily-pages` branch, same commit-and-notify mechanics. Only the scope (all
   frontier labs) and the depth (six levers, raised floors) change.
