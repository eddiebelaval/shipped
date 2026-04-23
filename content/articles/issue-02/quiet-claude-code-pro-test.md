---
title: "Claude Code, briefly removed from the $20 Pro plan"
issue: 2
section: quiet-wire
status: research
created: 2026-04-22
updated: 2026-04-22
sources:
  - https://x.com/amolavasare/status/2046724659039932830
  - https://www.anthropic.com/
  - https://claude.com/pricing
  - https://www.wheresyoured.at/news-anthropic-removes-pro-cc/
  - https://www.theregister.com/2026/04/22/anthropic_removes_claude_code_pro/
  - https://simonwillison.net/2026/Apr/22/claude-code-confusion/
  - https://thenewstack.io/anthropic-claude-code-limits/
  - https://news.ycombinator.com/item?id=47854477
  - https://startupfortune.com/anthropic-quietly-pulls-claude-code-from-pro-plan-and-hands-local-model-advocates-their-strongest-argument-yet/
---

# Claude Code, briefly removed from the $20 Pro plan

Late Tuesday afternoon, the checkmark on Anthropic's pricing page for Claude Code in the Pro column disappeared. The docs page swapped "Pro or Max" for "Max." No announcement. By Wednesday, it was back. Amol Avasare, head of growth, on X: *"we're running a small test on ~2% of new prosumer signups. Existing Pro and Max subscribers aren't affected."* The logged-out landing page update, Avasare said, was the mistake. The test continues. The 2% is cover. The posture is: Claude Code is heading upmarket. Tested quietly. Socialized later.

## Attribution caveats

- **"Running a ~2% test on new prosumer signups."** Per *Amol Avasare*, head of growth at Anthropic, on X. Attribute to Avasare by name; do not paraphrase as "Anthropic said" since no official company statement was issued.
- **"$20 → $100 jump."** Speculation from multiple outlets (*byteiota*, *Where's Your Ed At*, *The Register*) based on the Max plan's $100/mo price. Anthropic has not quoted a specific new Claude Code price for Pro users. Do not render this as a confirmed price change.
- **"Mistake on the landing page and docs."** Also per Avasare, same thread. Attribute to him, not to Anthropic corp comms.
- **"Existing Pro and Max subscribers aren't affected."** Per Avasare's quote. The narrower experiment scope is a Avasare claim, not independently verified.
- **"No announcement, no email."** Observed by *Simon Willison* (2026-04-22, 2:07 AM) and *The Register*. Safe to attribute to multiple outlets.
- **Ed Zitron's framing ("Anthropic Briefly Removes").** *Where's Your Ed At*, 2026-04-22. Editorial interpretation, not a neutral report. Attribute to Zitron; do not inherit his "briefly" framing as neutral.
- **Hacker News reaction.** Thread `47854477`. Community sentiment, not a moderator statement or representative sample.
- **Internet Archive snapshot timing.** Per *Simon Willison*. Safe, the archive is the primary timestamp source.

## How this fits the issue

**Quiet on the Wire slot** (50 to 80 words). Position: late in the front-of-book, after Also Shipped, before the Close. Not a standalone beat, a structural mirror to the Claude performance backlash Also Shipped item. Both are signals about Anthropic's communication discipline. The backlash is the user-side read (performance silence); this is the product-side read (pricing silence). Pairs with the Trust Week Investigation as the third instance of a pattern: a platform making load-bearing changes without telling the people they affect. Mirrors the Lovable arc, a product-behavior change, a stealth rollout, a walk-back once the community notices. Ties into the Term of the Issue, **Presence**, inversely: Anthropic's products stay present in the builder's workflow, but the company's communication doesn't match that presence. The signal that matters: the 2% number is cover, not scope. The posture is: premium tiering for Claude Code, sequenced by test cohort, timeline TBD.

## Named evidence

- **2%**. Avasare's test-cohort claim.
- **$20 → $100**, the Pro-to-Max price jump the removal would have forced, per *byteiota* and *The Register*.
- **5×**, magnitude of the price shock, same outlets.
- **~12 hours**, approximate window between the docs change (late afternoon 2026-04-21) and the reversal (during Simon Willison's 2:07 AM 2026-04-22 blog draft).
- **0 announcements**. Anthropic corp comms channels on either the change or the reversal as of 2026-04-22.

## For builders

Vetted moves, imperative, action-layer:

- Audit your Claude Code billing line on Pro; document what you pay for and at what tier, screenshot the pricing page today.
- Verify your team's Claude Code usage is on a plan you can hold. Max, team, or enterprise, if the experiment returns.
- Check whether your CI/CD pipelines depend on Claude Code via Pro-tier auth; if yes, consider a Max upgrade as insurance.
- Monitor Anthropic's `claude.com/pricing` page weekly; the next change may not get reverted.
- Rotate to a direct-API fallback plan for Claude Code workflows in case of tier changes.
- Watch Avasare's X account for future "clarity" threads, they're the channel for price-test disclosure.
- Read this next to the Claude performance backlash piece; same pattern, different surface.
- Treat the reversal as a pause, not a cancellation. The experiment continues on 2% of new signups.

## The stake

The call is: Claude Code is heading upmarket. The tell is: the test was launched without a PR cycle. What this means: Anthropic's pricing discipline is downstream of its product cadence, and the product cadence is running hot. The posture is: premium-tier claim staked now, tested quietly, socialized later. The precedent is: other Anthropic products (Claude Design is already Pro-and-above) will see the same tier discipline if builder adoption tracks the revenue model. The decision was made by what was removed, not what was said. The bet is: the 98% of existing Pro users who don't notice stay, and the 2% who need Claude Code upgrade without friction.

## Voice notes for the distilled prose

House moves for the 50 to 80w Quiet on the Wire item:

- **Pattern 1 (in medias res):** open on the pricing page change itself, "Late Tuesday, the checkmark disappeared."
- **Move B (punchline isolation):** the "~2% of new prosumer signups" quote lands on its own line. Preserve.
- **"X isn't Y, it's Z" formula:** NOT allowed. Issue budget spent in the Lead. Hard kill.
- **Raoul Duke anchor:** single-detail characterization. The `claude.com/pricing` checkmark IS the detail. One visual, one change, one walk-back.
- **Sass budget:** one dry beat on "clarity" (Avasare's word choice IS the beat, name it, don't inherit it). No memelord here; this one stays dry.
- **Second person:** allowed in the "if you pay $20/mo" line; the reader IS the 98%.
- **Third-act tie:** one half-sentence back to the backlash piece. Do not over-thread.

**Kill on sight**, forbidden phrases for this item:

- *"stealth pricing change"*
- *"quietly announced"* (it wasn't announced)
- *"clarifies pricing"* (Avasare's word, do not inherit)
- *"controversy erupts"*
- *"sparks backlash"*
- *"in a statement"*
- *"Anthropic clarified"* (Avasare clarified; Anthropic didn't)
- *"walked back"* (use "reverted")
- *"backpedaled"*
- *"after developer outcry"* (use specifics: X, Hacker News)
- *"in a surprising move"*
- *"u-turn"*

## Open questions / TODOs before press

- [ ] **Pull the Avasare tweet screenshot or archive link** before Thursday lock. X URLs decay; archive it.
- [ ] **Check whether the 2% test is still running**, has the experiment been re-scoped or ended entirely? Monitor between Wed 2026-04-22 and Thu 2026-04-23 PM.
- [ ] **Verify the pricing page state at lock time.** Screenshot `claude.com/pricing` Thursday AM. If it changes again between Wed and Thu, the beat shifts.
- [ ] **Confirm Avasare's title.** "Head of growth" per multiple outlets; confirm via LinkedIn or an Anthropic about page before press.
- [ ] **Ed Zitron framing check.** Zitron's piece is strong but editorial; do not inherit his tone in the 80w compress.
- [ ] **Hacker News thread pull.** Any notable Anthropic employee commenting there? Quote one if present.
- [ ] **Internet Archive snapshot URLs**, pin the before/after `claude.com/pricing` snapshots for the archival record. Add to sources if retrieved.
