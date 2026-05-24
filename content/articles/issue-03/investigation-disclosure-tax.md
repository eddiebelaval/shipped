---
title: "The Disclosure Tax"
issue: 03
section: investigation
status: research
created: 2026-05-24
updated: 2026-05-24
placement_decision: "Investigation. Drafted in WIP 2026-04-30 PM as B-story under the Disclosure Tax umbrella. Scaffolded 2026-05-24."
sources:
  - https://www.schneier.com/blog/archives/2026/04/what-anthropics-mythos-means-for-the-future-of-cybersecurity.html
  - https://securityboulevard.com/2026/04/what-anthropics-mythos-means-for-the-future-of-cybersecurity/
  - https://www.thenationalnews.com/news/us/2026/04/29/what-is-mythos-cybersecurity-vulnerabilities/
  - https://www.anthropic.com/research/Evaluating-Claude-For-Bioinformatics-With-BioMysteryBench
  - https://huggingface.co/datasets/Anthropic/BioMysteryBench-preview
  - https://www.bloomberg.com/news/articles/2026-04-29/goldman-staff-in-hong-kong-lose-access-to-anthropic-s-claude
  - https://finance.yahoo.com/sectors/technology/articles/goldman-sachs-bars-hong-kong-bankers-from-using-anthropic-ai-source-says-005320282.html
  - https://techcrunch.com/2026/04/29/sources-anthropic-could-raise-a-new-50b-round-at-a-valuation-of-900b/
  - https://www.bloomberg.com/news/articles/2026-04-29/anthropic-considering-funding-offers-at-over-900-billion-value
  - https://www.anthropic.com/glasswing
---

# The Disclosure Tax

> Investigation scaffolding. Four threads (Schneier on Mythos, BioMystery caveat, Goldman HK, $50B unconfirmed) read as one shape — the press cycle that turned. Schneier is load-bearing; the others reinforce.

## Research notes (raw, not prose)

**Thread 1 — Schneier on Mythos (load-bearing).**
- 2026-04-28: Bruce Schneier publishes "What Anthropic's Mythos Means for the Future of Cybersecurity." Calls the rollout "very much a PR play by Anthropic that worked, with lots of reporters breathlessly repeating Anthropic's talking points without engaging with them critically."
- Specific complaints: no disclosure of false-positive rates; no independent reproduction; comparable open-source models "hallucinate vulnerabilities in already-patched code."
- Republished in Security Boulevard same day.
- The National (2026-04-29) ran parallel "experts worry" piece picking up the same disclosure-gap thread.
- Editorially pointed: Schneier is part of the same security establishment Anthropic courted three weeks earlier with Project Glasswing (AWS, Apple, Cisco, CrowdStrike, Google, JPMC, Linux Foundation, Microsoft, NVIDIA, Palo Alto Networks; partner list set April 7).

**Thread 2 — BioMysteryBench caveat.**
- 2026-04-29: Anthropic publishes BioMysteryBench. Headline: Claude Mythos Preview solved 30% of 23 expert-unsolvable bioinformatics questions; Sonnet 4.6 onward on par with experts overall.
- The caveat in the paper: on hard problems, success rate is one or two of five attempts. Suggests lucky paths rather than reproducible strategies.
- The caveat was tucked into methodology; press coverage led with the 30% headline.

**Thread 3 — Goldman Hong Kong.**
- 2026-04-28-29: FT/Bloomberg/Reuters report Goldman Sachs removed Claude access for Hong Kong staff "in recent weeks." Goldman cites a strict reading of its Anthropic contract "following consultation with [Anthropic]."
- ChatGPT and Gemini remain available to the same staff. Hong Kong is not a market where Anthropic officially supports the API or Claude.ai.
- Bloomberg frames in US-China AI-tensions context.
- The mechanism — an enterprise contract being interpreted strictly to enforce Anthropic's geographic restrictions — is itself a precedent.

**Thread 4 — $50B round unconfirmed.**
- 2026-04-29: TechCrunch + Bloomberg report multiple preemptive offers at $850B–$900B. One institutional investor prepared to commit $5B unable to secure a meeting with CFO Krishna Rao.
- Reports cite ~$40B run rate against $30B disclosed ARR.
- Anthropic has not confirmed any of this.

## The editorial beat

The counter-frame: April was a press cycle Anthropic rode (Mythos launch, Glasswing partner list, BioMystery headline numbers, $40B Google deal). This week (04-24 → 04-30), the same press cycle turned. Not because anything broke — because four disclosure gaps surfaced in the same window. Schneier is the critic the safety-forward brand cannot easily dismiss; he is the security establishment Anthropic itself recruited.

What this story IS: a structural read on the cost of being the safety-forward AI lab when the safety establishment publicly grades you down. What this story is NOT: a "gotcha" piece. The disclosure tax is the price of operating in this register; the question is whether Anthropic pays it.

Editorial closing question (draft): *can the safety-forward brand survive a week where the safety establishment publicly grades it down?*

## Attribution caveats

- **Schneier "called the Mythos rollout very much a PR play"** — direct quote from the 04-28 blog post. Safe. Attribute to Schneier, not to "security experts" in aggregate.
- **"Comparable open-source models hallucinate vulnerabilities"** — Schneier's claim, citing independent research. Attribute to Schneier; do not present as established consensus.
- **"$50B round at ~$900B"** — REPORTED by TechCrunch + Bloomberg citing sources. Anthropic has NOT confirmed. Use "reported" throughout. Do not write "announced."
- **"Goldman cites consultation with Anthropic"** — sourced reporting (FT/Bloomberg/Reuters). The contract language was not disclosed. Do not characterize Anthropic's role in the decision beyond the consultation framing.
- **"One or two of five attempts on hard problems"** — directly from Anthropic's own BioMysteryBench paper. Safe. This is a self-disclosed caveat being elevated, not an external critique.
- **"~$40B run rate vs $30B ARR"** — sourced reporting on the $50B round. Anthropic disclosed $30B publicly; higher figure is reporting, not confirmation.
- **Project Glasswing partner list** — confirmed by Anthropic's own announcement (anthropic.com/glasswing). Safe to enumerate.

## Operator-layer implications

- **Disclosure norms are now a competitive surface.** Schneier is naming a gap (false-positive rates on Mythos, methodology on BioMystery) that competitors can fill with their own benchmark releases. Operators relying on Anthropic's safety/eval claims as procurement justification should expect to be asked harder questions.
- **Geographic contract scope is procurement-relevant.** The Goldman-HK precedent means enterprise customers operating in jurisdictions where Anthropic does not officially support the API can have access pulled by their own legal departments. Operators should verify contract scope before deploying Claude in HK, mainland China, sanctioned regions.
- **The $50B round, if it closes, hardens the patron-economy frame.** Cross-reference with lead-patron-economy.md. The Disclosure Tax thread is what makes the Patron Economy lead feel less euphoric.

## Open questions / TODOs before press

- Has Anthropic published Mythos false-positive rates between 04-28 and ship date (2026-05-29)?
- Did the $50B round resolve or stall? Check the 05-06 → 05-22 daily sweeps in `content/anthropic-daily/` for any updates.
- Has Goldman extended the HK policy to other jurisdictions or other banks?
- Did Schneier publish a follow-up? Has Anthropic responded publicly?
- Any movement on the BioMystery methodology critique from independent researchers?

## Voice notes for the distilled prose

- The investigation gets the 400–700-word budget per FORMULA.md. Use it. Multi-source story with reporting angle — that earns the slot.
- Schneier quote is the load-bearing moment. Pull one specific sentence, not the gist.
- Avoid framing this as "Anthropic in trouble." The frame is "the press cycle turned." Structural, not editorial scolding.
- Per STYLE.md: dry, confident, never breathless. The Disclosure Tax is named as a thing, not editorialized as a scandal.
- Voice anchor (Raoul Duke compass): observational, second-read. The story is what's behind the headlines, not the headlines.
- One "X isn't Y, it's Z" budget: candidate goes to The Disclosure Tax (per FORMULA, max 1 per issue — if the Lead spends it, this section does not).
