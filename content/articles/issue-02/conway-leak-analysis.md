---
title: Project Conway. The Always-On Agent in the Leaked Source
issue: 2
section: feature
status: research
created: '2026-04-22'
updated: '2026-04-22'
placement_decision: Standalone B-story (Feature slot). Eddie 2026-04-22 PM.
sources:
  - 'https://www.anthropic.com/'
  - 'https://docs.anthropic.com/en/api/agents'
  - 'https://github.com/anthropics/claude-code'
  - 'https://www.testingcatalog.com/exclusive-anthropic-tests-its-own-always-on-conway-agent/'
  - 'https://www.testingcatalog.com/anthropics-works-on-its-always-on-agent-with-new-ui-extensions/'
  - 'https://x.com/testingcatalog/status/2039490365414048182'
  - 'https://thehackernews.com/2026/04/claude-code-tleaked-via-npm-packaging.html'
  - 'https://venturebeat.com/technology/claude-codes-source-code-appears-to-have-leaked-heres-what-we-know'
  - 'https://layer5.io/blog/engineering/the-claude-code-source-leak-512000-lines-a-missing-npmignore-and-the-fastest-growing-repo-in-github-history/'
  - 'https://alex000kim.com/posts/2026-03-31-claude-code-source-leak/'
  - 'https://dataconomy.com/2026/04/03/anthropic-tests-conway-platform-for-continuous-claude/'
hero_image: 'https://placehold.co/1200x600/0b0b0b/FF6B35/png?text=Project+Conway'
---

# Conway, caught in the leak

The fastest-growing repo in GitHub history this month wasn't open-sourced. It was leaked. `@anthropic-ai/claude-code` v2.1.88 shipped on March 31 with a 59.8 MB source map packed by mistake, an `.npmignore` entry that wasn't there. Roughly 512,000 lines of TypeScript across 1,906 files. Anthropic confirmed a packaging error, not a breach. The mirrors did the rest.

What emerged is a catalog of unshipped product.

The editorially significant one is **Project Conway**. An always-on, persistent background agent. Three UI panes, Search, Chat, System. Webhook-triggered execution. Browser control. GitHub subscription hooks. As of this week, TestingCatalog reports the iOS build of Claude carries a hidden feature flag for managed 24/7 agents. The leak is old. The staging is current.

Conway is a daemon.

The leak surfaced 44 hidden feature flags. `KAIROS`, Greek for *the right moment*, is a fully-built autonomous daemon mode. `EPITAXY` names a Claude Code integration. `VOICE_MODE`. `BRIDGE_MODE`. `PROACTIVE`. Internal names, may not survive to launch. The shape of what's in the binary won't change.

Conway is not Cowork. Issue 01 covered Cowork GA, Anthropic's team-collaboration app, live on macOS and Windows. Admins can deploy Cowork on Amazon Bedrock, Google Cloud Vertex AI, Azure AI Foundry, or any LLM gateway that forwards the right headers. That's bring-your-own-cloud. The prompts still hit Claude underneath. Conway is a layer above, unshipped, codename-only, with a model picker in the leak that selects between Claude-family models (Opus, Sonnet, Haiku, Mythos). No third-party models. The direction of travel is consolidation, not openness.

The editorial beat is not the leak. It's the product move the leak reveals.

Anthropic shipped Claude Design on April 17 and is staging Conway for consumer rollout. Two products, one month, both orthogonal to the API. Read together, they define a product portfolio that sits beside the API, not derived from it. Claude Design colonizes design workflows. Conway colonizes always-on ops.

The counterweight is the Trust Week. Conway's surface, webhook triggers, browser control, GitHub subscriptions, OAuth-everywhere, is precisely the trust surface the Lovable and Vercel stories are cracking open. The same week Vercel got pivoted via an OAuth-connected AI tool, Anthropic is staging a product that multiplies OAuth surface by orders of magnitude. The question stops being "will Conway ship" and becomes "what does Anthropic's Vercel-proof posture look like for a product with ten times the surface."

Zero Anthropic public statements on Conway between the leak and this week's ship date. The silence is part of the pattern. The leak is the roadmap.

## Attribution caveats

- **"Conway is being developed"**, supported by TestingCatalog + VentureBeat + Dataconomy + Alex Kim + Layer5. Safe.
- **"Conway is coming to consumers"**, softer. The iOS flag is evidence of staging, not a launch commitment. Attribute as "per TestingCatalog, hidden iOS flags suggest Conway is being prepared for consumer rollout."
- **"Anthropic confirmed"**, only confirmed the packaging error + non-breach characterization. No confirmation of Conway as a shipping product. Do not imply otherwise.
- **Feature-flag names**, these are names in source code. They may not survive to launch. `KAIROS` and `Conway` may both be internal names. Hedge: "internal codename."
- **The leak URL on TestingCatalog**, egress-blocked from some networks. Cross-reference with The Hacker News and VentureBeat for the primary leak story; TestingCatalog is the Conway scoop.

## For builders

Vetted moves, imperative, action-layer:

- Audit your `.npmignore` today; Anthropic's packaging error is a reminder, not an edge case.
- Rotate your webhook secrets before Conway ships with webhook triggers as a feature.
- Check your GitHub App scopes. Conway's GitHub-subscription pattern will be the template others copy.
- Watch for `.cnw.zip` or similar extension formats in your dependency tree.
- Configure your OAuth consent screen to expose "can drive browser" scope in plain English.
- Rebuild your incident-response runbook to include "AI-agent pivoted via OAuth" as a first-class scenario.
- Test what happens when an always-on agent loses connectivity for 30 minutes, then reconnects with pending webhooks.
- Treat every long-lived AI-agent session as a trust-surface multiplier, audit accordingly.
- Monitor Anthropic's docs for the `/agents` API, when it lands, Conway's API contract is visible.
- Assume a 10x OAuth scope expansion across your AI toolchain in the next 12 months; plan for it now.

**Named evidence**, data points that ground the argument:

- **59.8 MB** `cli.js.map`, the file that shouldn't have shipped.
- **512,000 lines** of TypeScript, **1,906 files**, the scope of the inadvertent disclosure.
- **44 hidden feature flags**, the backstage of presence as product.
- **$2M**. BreachForums Vercel listing, same quarter Conway leaks. The trust surface Conway inherits has a price.
- **−100%**. Anthropic's public statements on Conway between the leak (2026-03-31) and this issue's ship date. Zero. The silence is the data point.

## Operator-layer implications
## The operator takeaway

> Scaffolding for the rubric v2 "Operator takeaway" dimension. The distilled prose must land an action-layer implication, not just an observation. Structural bullets below; prose is Eddie's.

**For builders reading this week:**

- **If you ship anything that Claude Code touches, read the leak like you'd read your own `.env.example`.** The 44 flags expose Anthropic's internal product direction. Your integration assumptions should update accordingly, particularly around webhook triggers, long-running sessions, and browser-control primitives that are staging, not shipped.
- **Audit your `.npmignore` today.** Anthropic's packaging error is a reminder, not an edge case. Any TypeScript project shipping via npm can leak source maps the same way. One-line fix, industry-wide exposure.
- **If Conway ships with the shape the leak describes, your OAuth posture is a load-bearing wall.** Webhook triggers + GitHub subscriptions + browser control = the same attack surface the Trust Week Investigation just demonstrated failing at Vercel. Reading the two pieces together is the point.
- **Don't wait for the announcement to design for this.** Persistent agents, extension formats (`.cnw.zip`), and webhook-triggered execution are the surface builders will be asked to support within the year. Start thinking about your own trust model for agent-triggered actions now.

**The one-line compress** (pick one for the distilled prose, Eddie calls):

- Option A: "Read the leak like an RFC; update your OAuth posture like a bulletin."
- Option B: "Conway isn't shipped yet. Your integration assumptions should be."
- Option C: "The `.npmignore` fix is trivial. The posture implications aren't."

## How this fits the issue

**Recommended placement: Lead Story third-act (200 to 300 words inside the Lead, or 150 to 200w sidebar).**

The prose beat: after establishing Claude Design as a shipped product, pivot to Conway as the staged one. Let the leak function as editorial weight, *"we know this because of a packaging error, but the shape of the product is legible"*, and land the implication: Anthropic now has a product department, and it's shipping faster than its policy department is catching up.

**Alternative placement: standalone B-story (400 to 700 words).** Stronger if Eddie wants to give Conway its own reporting frame. Cost: extends front-of-book toward the 1,500-word ceiling and may push Trust Week out of its Investigation slot.

## Open questions / TODOs before press

- [ ] **Placement call (Thursday lock).** Lead third-act OR standalone B-story. Both are viable; pick one.
- [ ] **Primary source rotation.** TestingCatalog broke the story but is egress-blocked for some readers. Lead with VentureBeat or The Hacker News as primary, cite TestingCatalog as the scoop.
- [ ] **Language hedge.** Conway vs. Project Conway vs. the codename, pick one usage and hold it.
- [ ] **Confirm the iOS flag claim.** TestingCatalog is the only source for the hidden iOS flag as of research date. If no secondary confirms before Thursday, attribute as "per TestingCatalog."
- [ ] **Anthropic statement.** Check whether Anthropic has said anything publicly about Conway (X, blog, docs) between 2026-04-17 and 2026-04-23. If yes, cite; if silence, that's itself part of the beat.
- [ ] **Connect to Trust Week.** If Conway lands in the Lead, the Trust Week Investigation should reference Conway by name when discussing trust surface, but not redundantly (trust it to the reader).

## The stake

The call is: Conway is the next Anthropic product, even though it hasn't shipped. The tell is: the iOS feature flag, the `.cnw.zip` extension format, the webhook trigger code path, all in source, all in active development. What this means: Anthropic is staging a product the API cannot wrap; Conway lives in its own container, on its own schedule, with its own trust surface. The posture is: Anthropic ships products now, and the next one is always-on. The precedent is: the leak is the roadmap. The decision was made by what was in the `cli.js.map`, a fully-built daemon mode (KAIROS) + a sidebar UI + an extension format + webhook triggers. That's not an experiment. That's a product with a launch date pending. The bet is: Conway lands in Q3 2026, Anthropic frames it as "Claude Agents," and the build-leak becomes legible retroactively as the public's first look.

## Voice notes for the distilled prose

House moves for the 400 to 700w B-story (or 200 to 300w Lead-third-act if placement changes):

- **Pattern 1 (in medias res):** open on the March 31 packaging-error moment, one sentence, then pivot to Conway.
- **Move B (punchline isolation):** "Conway is a daemon.", own line, mid-paragraph. Let the noun land.
- **"X isn't Y, it's Z" formula:** NOT allowed. Issue budget spent in the Lead. Hard kill.
- **Raoul Duke anchor:** single-detail characterization. Pick ONE feature flag name (KAIROS, EPITAXY, PROACTIVE) and let it carry the texture. Don't list all 44.
- **Sass budget:** one dry beat on "packaging error". Anthropic's own framing is pressure-release. Do not inherit the phrase without quoting it.
- **Second person:** reserve for the "your `.npmignore`" line in operator takeaway. Never earlier.
- **Name the primitive.** Conway is a daemon. It watches, it wakes, it drives a browser. Don't bury that under "persistent assistant" language.
- **Don't lead with the leak mechanics.** The packaging-error story is a background fact; the product shape is the beat.
- **Avoid the hacker-newsy frame.** This is an editorial magazine; the beat is product strategy, not npm drama.
- **Tie back to the Lead.** The Claude Design ↔ Conway arc is the whole point. The third-act paragraph should close on the portfolio thesis, not open a new one.

**Kill on sight**, forbidden phrases for this piece:

- *"ushers in an era of always-on AI"*
- *"the next frontier"*
- *"game-changing"*
- *"revolutionary agent"*
- *"always-on future"*
- *"persistent AI assistant"* (use "daemon")
- *"unveiled in a leak"* (it was a packaging error, not a reveal)
- *"Anthropic confirms"* (they confirmed the packaging error, not Conway)
- *"the AI agent wars"*
- *"paradigm shift"*
- *"industry-leading"*
- *"seamless integration"*
