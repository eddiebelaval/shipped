---
title: Project Conway — The Always-On Agent in the Leaked Source
issue: 2
section: lead-story
status: research
created: '2026-04-22'
updated: '2026-04-22'
placement_open: Lead-story third-act (recommended) OR standalone B-story. Eddie decides at Thursday lock.
sources:
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

# Project Conway — The Always-On Agent in the Leaked Source

## What happened

On March 31, 2026, Anthropic shipped `@anthropic-ai/claude-code` v2.1.88 with a missing `.npmignore` entry. The package included a 59.8 MB `cli.js.map` file — roughly 512,000 lines of TypeScript across 1,906 files. Anthropic confirmed it was a packaging error, not a security breach. The source code is now the fastest-growing repo in GitHub history (mirrors).

What emerged from the leak is a catalog of unshipped features. The editorially significant one is **Project Conway**: an always-on, persistent background agent with three UI panes (Search, Chat, System), webhook-triggered execution, browser control, and GitHub subscription hooks. Dataconomy (2026-04-03) was first to frame it as "a platform for continuous Claude."

As of this week, TestingCatalog reports the iOS version of Claude now carries a hidden feature flag for managed 24/7 agents. Evidence Conway is being prepared for consumer-facing rollout, not just internal experimentation.

## What's in the leak (the Conway surface)

From combined TestingCatalog + Alex Kim + Layer5 reporting:

- **44 hidden feature flags.** Named: `PROACTIVE`, `KAIROS`, `VOICE_MODE`, `BRIDGE_MODE`.
- **KAIROS** — Greek for *the right moment*. Fully-built autonomous daemon mode. Not shipped. Not announced.
- **Conway** — a sidebar option that launches a "Conway instance" with three panes: **Search, Chat, System**.
- **`.cnw.zip`** — proprietary extension format for custom tools, UI tabs, and context handlers.
- **Webhook triggers** — public URLs that wake the instance. Codepath exists for it.
- **Browser control** — Conway can drive Chrome.
- **Claude Code integration** — codename `EPITAXY` appears in the same cluster.
- **GitHub subscriptions** — Conway watches repo activity and responds proactively.
- **Push notifications** — fire when tasks complete or conditions trigger.

## The editorial beat

This is the product move, not the leak. Anthropic shipped Claude Design (Apr 17) and is staging Conway (codename, not shipped, but in the iOS binary flags as of this week). Two products in one month, both orthogonal to the API.

The Claude Design thesis in the Lead — *"Anthropic ships products, not just models"* — resolves more sharply if Conway is the third act. Claude Design colonizes design workflows. Conway colonizes always-on ops. Together they define a product portfolio that exists beside the API, not derived from it.

**The counterweight:** Conway's surface (webhook triggers + browser control + GitHub subs + OAuth everywhere) is precisely the trust surface the Trust Week stories are cracking open. Same week Vercel gets pivoted via OAuth-connected Context.ai, Anthropic is staging a product that multiplies OAuth surface by a couple orders of magnitude. The question stops being "will Conway ship" and becomes "what's Anthropic's Vercel-proof posture for a product with 10× the trust surface."

## Attribution caveats

- **"Conway is being developed"** — supported by TestingCatalog + VentureBeat + Dataconomy + Alex Kim + Layer5. Safe.
- **"Conway is coming to consumers"** — softer. The iOS flag is evidence of staging, not a launch commitment. Attribute as "per TestingCatalog, hidden iOS flags suggest Conway is being prepared for consumer rollout."
- **"Anthropic confirmed"** — only confirmed the packaging error + non-breach characterization. No confirmation of Conway as a shipping product. Do not imply otherwise.
- **Feature-flag names** — these are names in source code. They may not survive to launch. `KAIROS` and `Conway` may both be internal names. Hedge: "internal codename."
- **The leak URL on TestingCatalog** — egress-blocked from some networks. Cross-reference with The Hacker News and VentureBeat for the primary leak story; TestingCatalog is the Conway scoop.

## How this fits the issue

**Recommended placement: Lead Story third-act (200–300 words inside the Lead, or 150–200w sidebar).**

The prose beat: after establishing Claude Design as a shipped product, pivot to Conway as the staged one. Let the leak function as editorial weight — *"we know this because of a packaging error, but the shape of the product is legible"* — and land the implication: Anthropic now has a product department, and it's shipping faster than its policy department is catching up.

**Alternative placement: standalone B-story (400–700 words).** Stronger if Eddie wants to give Conway its own reporting frame. Cost: extends front-of-book toward the 1,500-word ceiling and may push Trust Week out of its Investigation slot.

## Open questions / TODOs before press

- [ ] **Placement call (Thursday lock).** Lead third-act OR standalone B-story. Both are viable; pick one.
- [ ] **Primary source rotation.** TestingCatalog broke the story but is egress-blocked for some readers. Lead with VentureBeat or The Hacker News as primary, cite TestingCatalog as the scoop.
- [ ] **Language hedge.** Conway vs. Project Conway vs. the codename — pick one usage and hold it.
- [ ] **Confirm the iOS flag claim.** TestingCatalog is the only source for the hidden iOS flag as of research date. If no secondary confirms before Thursday, attribute as "per TestingCatalog."
- [ ] **Anthropic statement.** Check whether Anthropic has said anything publicly about Conway (X, blog, docs) between 2026-04-17 and 2026-04-23. If yes, cite; if silence, that's itself part of the beat.
- [ ] **Connect to Trust Week.** If Conway lands in the Lead, the Trust Week Investigation should reference Conway by name when discussing trust surface — but not redundantly (trust it to the reader).

## Voice notes for the distilled prose

- **Don't lead with the leak mechanics.** The packaging-error story is a background fact; the product shape is the beat. One sentence on "a missing `.npmignore` exposed the source," then pivot to Conway.
- **Avoid the hacker-newsy frame.** This is an editorial magazine; the beat is product strategy, not npm drama.
- **Name the primitive.** Conway is a daemon. It watches, it wakes, it drives a browser. Don't bury that under "persistent assistant" language.
- **Tie back to the Lead.** The Claude Design ↔ Conway arc is the whole point. The third-act paragraph should close on the portfolio thesis, not open a new one.
- **Forbidden adjacent phrases:** "ushers in an era of always-on AI," "the next frontier," "game-changing." Kill on sight.
