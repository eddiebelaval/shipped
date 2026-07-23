# Shipped. — nightly daily routine prompt

This is the canonical prompt for the claude.ai cloud routine that generates the
nightly Shipped. daily (`trig_01Pevcq2DMteCYHW8dnYFXpT`, fires ~21:00 ET, commits
the rendered page to the `daily-pages` branch).

**This file is the intent doc. The live generator is the claude.ai routine's own
prompt** (`trig_01Pevcq2DMteCYHW8dnYFXpT`), edited directly via the remote-trigger
API, not by pasting from here.

**STATUS 2026-07-23 (subscribe block):** every page on `daily-pages` was
published with no way to subscribe: no form, no CTA, 88 pages going back to
2026-05-06, on the most current surface Shipped. has. The 88 were backfilled,
and the routine prompt now carries a Step 4 item 6 that pastes
`pipeline/src/render/subscribe-block.html` (the block lives in the repo, so
future edits to it land with no routine edit; only the instruction is in the
prompt). Step 4 previously said "no JS" and "do not add an inverted dark close
block", both of which would have made the routine reject the block, so both were
narrowed rather than deleted. Publishing is now gated on a third self-audit
alongside the word floor and the dash grep.

The weekly (`trig_011aW3YwQpj2oS9joyjyTxwQ`) and monthly
(`trig_01DGxYL9x9wyWhaSULzznuQN`) routine prompts were NOT edited. Instead
`pipeline/scripts/ensure-subscribe.sh` (launchd, 23:00 daily) sweeps the branch
and adds the block to anything published without it. That is deliberate: three
prompts each remembering to paste a block is the same bet this file already
records losing. Enforcing at the branch covers all three routines and any future
one, and self-heals when a prompt drifts.

**STATUS 2026-07-07 (length fix):** the routine prompt was rewritten in place to
(1) sweep all six frontier labs, not Anthropic only; (2) **read `content/DAILY.md`
as its BINDING depth authority** so future depth/floor edits to that file actually
take effect; and (3) enforce a **hard word-floor gate** (a `wc -w` self-audit that
refuses to publish under the tier floor and loops back to dig, mirroring the dash
self-audit). Diagnosis: the old routine had zero word floor and Anthropic-only
scope, so a quiet day faithfully produced two paragraphs (445 words on 07-06).

**Where to make changes now:**
- Depth / word floors / the six Dig levers -> edit `content/DAILY.md`. The routine
  reads it live every run, so the change lands with no routine edit.
- Scope, render, publish, or distribution mechanics -> edit the routine prompt via
  the API (`RemoteTrigger update trig_01Pevcq2DMteCYHW8dnYFXpT`) and mirror it here.

Why this history matters: every prior "make the dailies beefier / go multi-lab"
change was made to repo files (DAILY.md, scrape/sources.ts, FORMULA.md) that the
routine did not read. The routine kept running its own old "Anthropic sweep"
instructions. The generator is the prompt. That is now fixed by binding DAILY.md.

What changed 2026-06-27: the floors are no longer advisory. The verifier now has a
**depth gate** and a **lab-coverage gate** (`pipeline/src/verify/gates/`). A daily
whose front-of-book (everything before the Release Log) falls below ~1,000 words
**FAILs verification and cannot publish** — padding the Release Log does not help,
the gate measures the front-of-book only. A single-lab daily draws a coverage
**warning**. Step 6 below makes the routine run that gate on itself before it
commits, so a collapsed daily never reaches the branch again.

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

2. **Depth per `content/DAILY.md` (enforced floor).** Run every real item through
   the SIX Dig levers: mechanism, blast radius, pattern, the read, **the contrast**
   (what a move says against the other labs — this is the lead lever now), and the
   move. Hit the DAILY.md word floors: one real item 700, quiet day 1,000–1,400,
   normal day 1,400–2,000, heavy day up to 2,800. **The 1,000-word front-of-book
   floor is now a hard gate** — measured before the Release Log, so the Release Log
   does not count toward it. A quiet Anthropic day is not a thin daily, because the
   frontier is six labs wide — lead with whatever moved the frontier most,
   regardless of which lab. If you are tempted to ship two paragraphs, dig; that is
   the exact failure this floor exists to stop.

3. **Voice per `content/STYLE.md`.** Dry, confident, Rolling Stone × Wired. No
   forbidden phrases, max one "X isn't Y, it's Z," no em dashes in prose,
   "Shipped." always with the period.

4. **Sourcing discipline (the verifier is real).** Every number sits in the same
   sentence as a source link that contains it. No clock timestamps, no bare HTTP
   codes. If a figure isn't on a reachable source, rephrase rather than fake it.

5. **Self-verify before you commit (do not skip).** After writing the daily
   markdown, run the verifier on it:

   ```
   cd pipeline && pnpm verify ../content/anthropic-daily/<YYYY-MM-DD>.md --offline
   ```

   If the verdict is **FAIL** (the depth gate will say "Issue too short:
   front-of-book Nw"), the daily is too thin to publish — go back to step 2, dig
   the items deeper, and re-run until it passes. Do not commit a FAIL. If you get a
   single-lab **WARN**, either work in the cross-lab contrast or keep it only if
   Anthropic genuinely owned the day; say so in one honest line. The full
   `pnpm publish` path runs this same gate, so a thin daily will be rejected there
   too — catching it here saves the round trip.

6. **Render and publish exactly as you do today** — same render step, same
   `daily-pages` branch, same commit-and-notify mechanics. Only the scope (all
   frontier labs), the depth (six levers, enforced floors), and the self-verify
   step change.
