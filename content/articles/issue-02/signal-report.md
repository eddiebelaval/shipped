---
title: "Issue 02 — Signal Report"
issue: 02
section: signal-report
status: used
created: 2026-04-21
updated: 2026-04-23
grade_override: true
grade_override_reason: "Signal reports are Monday research sweeps. Frozen decision input for Thursday's lock, not editorial articles. Grading rubric does not apply."
sources:
  - https://www.testingcatalog.com/anthropics-works-on-its-always-on-agent-with-new-ui-extensions/
  - https://vercel.com/kb/bulletin/vercel-april-2026-security-incident
  - https://www.anthropic.com/news
---

# Issue 02 — Signal Report
**Tue 2026-04-21 · T-3 days to ship · T-2 days to running-order lock**

> Research sweep on the state of the week. Not prose. Decision input for Thursday's lock-in.
> Lead story locked: **Claude Design.** Secondary under re-evaluation in light of Project Conway.

---

## Headline verdict

The week got louder, not quieter. Three signals tightened and one new signal — **Project Conway** — may rewrite the editorial spine of the issue.

- **Claude Design stays the lead.** Reception has bifurcated: Brilliant and Datadog case studies are strong; r/ClaudeAI landed on "meh." Figma stock still sits -7.28% from launch day. The bifurcation is itself the story.
- **The Trust Week still holds,** but attribution got murkier: ShinyHunters publicly denied Vercel involvement; the $2M BreachForums listing remains live.
- **Amazon-Anthropic deal** ($25B invested / $100B committed over 10yr) broke Mon-Tue. Big, but Eddie confirmed it does not flip the lead.
- **Project Conway** surfaced as a TestingCatalog scoop — a codename for an unreleased always-on agent revealed by the March 31 Claude Code source-code leak. This may need its own section or be the new "Quiet on the Wire" anchor.

---

## Thread 1 — Claude Design (LEAD)

### What changed since the WIP was written
The reception split is now well-documented enough to quote:

- **Positive signal:** *Brilliant* reports pages that took "20+ prompts in competing design tools" built in "2 prompts" in Claude Design. Framed as "a step change."
- **Positive signal:** *Datadog* product team says Claude Design compressed "a week-long cycle of briefs, mockups, and review rounds into a single conversation" — savings not from speed but from eliminating handoff friction.
- **Negative signal:** r/ClaudeAI reaction — "resounding meh." The community read: every output "screams I just used one Claude prompt" unless you upload reference screenshots or your own design tokens.
- **Confounding factor:** the launch coincided with a broader Claude-performance backlash (Fortune, 04-14) about perceived degradation in model quality — meaning some reception reads are contaminated.

### Implication for the piece
This is a better story than a pure launch writeup. **The tension is the story**: enterprise teams report dramatic gains; individual developers shrug. Two reads, same tool. That's a lead hook.

### Open TODOs still real
- Hands-on first-person screenshots (this one only Eddie can do)
- Confirm research-preview eligibility specifics — who gets it today vs. this week
- Find one designer or PM in the wild to quote (scan X + LinkedIn)

---

## Thread 2 — The Trust Week

### 2a. Lovable — new facts
The Register (04-20) adds texture: Lovable's story has shifted three times.
1. First: "intentional behavior" and "unclear documentation"
2. Then: blame shifted to HackerOne (reports were closed as duplicate because triagers thought it was intended behavior)
3. Then: admitted a February permissions-unification accidentally re-enabled access to public-project chats
4. Now: partial fix shipped — new projects patched, **every pre-existing (pre-Nov 2025) project remains exposed**

Techloy has a headline claiming Lovable "fixes" the vulnerability. Independent coverage says the fix is new-projects-only. That gap — fix announced vs. legacy still exposed — is itself worth stating cleanly in the piece.

### 2b. Vercel — scope clarified
- Vercel Knowledge Base bulletin is the canonical reference
- Mandiant + GitHub + Microsoft + npm + Socket are all engaged
- Vercel confirmed no compromised npm packages published by Vercel
- Environment variable default is changing to `sensitive: on` going forward
- Env vars marked *non-sensitive* were the exposed surface; *sensitive* vars were encrypted at rest and believed safe
- Register calls it "AI-pwned" — traced to stolen employee creds via OAuth-connected Context.ai

### 2c. ShinyHunters — attribution reversal
**This is new.** ShinyHunters told BleepingComputer they are **not** involved in the Vercel breach. Hackread reported the same denial. The BreachForums listing offering Vercel data at $2M is still live, but the group usually credited has distanced themselves.

Why this matters: the WIP currently names ShinyHunters as the actor. That's now a "claimed to be" situation, not a confirmed attribution. Editorial line needs to soften.

### 2d. Crypto scramble intensifying
- CoinDesk: developers locking down API keys
- iTnews: Vercel advising secrets rotation across the board

### Implication for the piece
The "Trust Week" frame is stronger, not weaker. Two stories now have the **same narrative shape**: a company with a platform-security problem, an evolving public-facing story, and a gap between what was claimed and what was true. Lovable's "intentional behavior → HackerOne's fault → oh we patched it" arc mirrors Vercel's "non-sensitive env vars were not sensitive in the attacker's hands" arc. Both are **trust margins collapsing under pressure.**

---

## Thread 3 — PROJECT CONWAY (new, potentially huge)

### The TL;DR
Conway is an unreleased Anthropic codename for an always-on, persistent background agent. Surfaced through the **March 31, 2026 Claude Code source-code leak** — a missing `.npmignore` entry that shipped a 59.8 MB `cli.js.map` file with `@anthropic-ai/claude-code` v2.1.88. ~512,000 lines of TypeScript across ~1,906 files went public. Anthropic confirmed it was a packaging error, not a security breach.

### What's in the leak
- **44 hidden feature flags.** Named ones include `PROACTIVE`, `KAIROS`, `VOICE_MODE`, `BRIDGE_MODE`
- **KAIROS** — Greek for *the right moment*. Fully-built autonomous daemon mode. Not shipped.
- **Conway** — sidebar option inside Claude's interface that launches a "Conway instance" with three panes: **Search, Chat, System**
- **.cnw.zip** — a proprietary extension format for custom tools, UI tabs, and context handlers
- **Webhook triggers** — public URLs that wake the instance; a section of the codebase exists for this
- **Browser control** — Conway can drive Chrome
- **Claude Code integration** — codename "EPITAXY" appears in the same cluster
- **GitHub subscriptions** — Conway watches repo activity and responds proactively
- **Push notifications** when tasks complete or conditions trigger

### What TestingCatalog added this week (Eddie's link)
The iOS version of Claude now has a **hidden feature flag** related to managed 24/7 agents. Evidence that Conway is being prepared for consumer-facing rollout, not just an internal experiment. That's a meaningful shift from "leaked internal project" to "consumer product being staged."

### The cross-thread thesis
Conway braids cleanly into two existing threads:

1. **Claude Design thesis** ("Anthropic ships products, not just models") — Conway is the next product. Claude Design colonizes design workflows; Conway colonizes always-on ops. Together they mean Anthropic is building a product portfolio orthogonal to the API.
2. **Trust Week thesis** (platform risk) — an always-on agent with GitHub subs, webhook triggers, and browser control is a **massive new trust surface**. Same week Vercel gets pivoted via OAuth, Anthropic is building a product where webhook triggers wake an agent with Chrome control. The question isn't "will this ship" — it's "how will Anthropic secure what the Vercel story just showed fails."

### Where Conway could slot in Issue 02

Three reasonable placements — Eddie decides:

| Placement | Pitch | Cost |
|---|---|---|
| **Quiet on the Wire section** | 50-80 words on "what's rumored, hinted, expected." Keeps running order intact. | Underplays a story that's already broken in trade press for 3 weeks. |
| **Lead-story sidebar / third act** | Pivot Claude Design's "Anthropic ships products" thesis by closing with Conway: *here's the next one, already in the code.* | Extends Lead past 300 words; may unbalance issue. |
| **Its own investigation slot** | Replace or share space with Trust Week secondary. Same investigative spine, Anthropic-native. | Displaces Trust Week, which has the action-layer SOPs angle readers asked for. |

**Recommendation:** sidebar / third act of the Lead Story. It tightens the "Anthropic ships products" thesis and ties the week into a single arc: Claude Design (shipped) → Conway (coming) → the trust surface (Trust Week) that an always-on agent world will inherit.

---

## Thread 4 — Amazon-Anthropic deal

**Not the lead per Eddie's call.** Holding it here for Release Log treatment:
- Mon 2026-04-20 / Tue 2026-04-21 announcement
- Amazon invests up to $25B in Anthropic ($5B now, $20B on commercial milestones)
- Anthropic commits to $100B+ on AWS over 10 years
- Target: 1 GW capacity via Trainium2/Trainium3 by end of 2026; 5 GW total goal
- Ties back to Project Glasswing / Mythos context already in the WIP

**How to handle:** one Release Log entry under `[NEWS]`. Two or three sentences in the front-of-book if word budget allows, but it's not a narrative spine; it's context.

---

## Term-of-issue — re-evaluation

The WIP had three candidates: **Trust**, **Context**, **Scope.**

With Conway in the mix, a fourth emerges: **Presence.** Conway's whole architecture is about Claude being *present* — persistent, watching, responsive to external conditions — vs. being *summoned.* And it echoes Eddie's own `presence-not-tools.md` essay (in the STYLE.md corpus). That'd be a strong resonance move.

Re-ranked:
1. **Presence** — ties Conway to Eddie's voice corpus; contrasts with Claude Design's one-prompt-one-output mode; opens a Move A (memoir-to-philosophy) pivot.
2. **Trust** — the frame that still handles both Lovable and Vercel cleanly; loses Conway slightly.
3. **Scope** — strong for OAuth/Vercel but doesn't absorb Conway or Claude Design.
4. **Context** — cute tri-meaning but gets thin once Conway joins.

---

## Updated Thursday checklist (proposed diff vs. WIP)

- [x] **Running order:** lead Claude Design (confirmed) → Trust Week → **Conway sidebar inside Lead** → Release Log → Close
- [ ] **Slug:** open — candidates: `presence`, `the-product-turn`, `what-gets-watched`
- [ ] **Title:** open
- [ ] **Term of Issue:** leaning **Presence**
- [ ] **Hands-on Claude Design screenshots** (Eddie only)
- [ ] **Pro interview for SOPs** (candidate: an infosec eng at a YC AI co; alt: an Anthropic DevRel on Claude Code safety story)
- [ ] **Attribution line for Vercel** — soften to "initially credited to ShinyHunters; group has since denied involvement"
- [ ] **Conway sourcing** — pick 2 primary sources; TestingCatalog (broke it) + one secondary verification (VentureBeat, The Hacker News, or Dataconomy)
- [ ] **Scraper output review** (blocked on Thursday scrape run)

---

## Sources

**Claude Design reception:**
- [TechCrunch — launch](https://techcrunch.com/2026/04/17/anthropic-launches-claude-design-a-new-product-for-creating-quick-visuals/)
- [The Neuron Daily — r/ClaudeAI "meh"](https://www.theneurondaily.com/p/anthropic-s-claude-design-launched-and-reddit-has-thoughts)
- [BuildFastWithAI — Brilliant & Datadog case studies](https://www.buildfastwithai.com/blogs/claude-design-anthropic-guide-2026)
- [Fortune — Claude performance backlash context](https://fortune.com/2026/04/14/anthropic-claude-performance-decline-user-complaints-backlash-lack-of-transparency-accusations-compute-crunch/)

**Lovable updated facts:**
- [The Register — "intentional behavior" defense](https://www.theregister.com/2026/04/20/lovable_denies_data_leak/)
- [Techloy — partial fix claim](https://www.techloy.com/is-your-code-safe-lovable-ai-fixes-vulnerability-that-leaked-database-credentials/)
- [Computing.co.uk — flaw exposed source + creds + chats](https://www.computing.co.uk/news/2026/security/lovable-flaw-exposed-source-code-credentials-and-ai-chats)

**Vercel updates:**
- [Vercel official bulletin](https://vercel.com/kb/bulletin/vercel-april-2026-security-incident)
- [The Register — AI-pwned](https://www.theregister.com/2026/04/21/vercel_ceo_points_to_aidriven/)
- [GitGuardian — non-sensitive env vars matter too](https://blog.gitguardian.com/vercel-april-2026-incident-non-sensitive-environment-variables-need-investigation-too/)
- [Hackread — ShinyHunters denial](https://hackread.com/vercel-breach-context-ai-shinyhunters-not-involved/)

**Amazon-Anthropic deal:**
- [Rappler — $25B / $100B](https://www.rappler.com/technology/amazon-investment-anthropic-april-20-2026/)
- [Meyka — Apr 21 framing](https://meyka.com/blog/amazon-invests-25b-in-anthropic-ai-on-april-21-2026-2104/)

**Project Conway / Claude Code leak:**
- [TestingCatalog — original Conway scoop](https://www.testingcatalog.com/exclusive-anthropic-tests-its-own-always-on-conway-agent/) *(egress-blocked, cited from search results)*
- [TestingCatalog — UI extensions follow-up](https://www.testingcatalog.com/anthropics-works-on-its-always-on-agent-with-new-ui-extensions/) *(Eddie's link)*
- [The Hacker News — Anthropic confirms packaging error](https://thehackernews.com/2026/04/claude-code-tleaked-via-npm-packaging.html)
- [VentureBeat — leak analysis](https://venturebeat.com/technology/claude-codes-source-code-appears-to-have-leaked-heres-what-we-know)
- [Layer5 — 512k lines, .npmignore story](https://layer5.io/blog/engineering/the-claude-code-source-leak-512000-lines-a-missing-npmignore-and-the-fastest-growing-repo-in-github-history/)
- [Alex Kim — Conway+KAIROS feature-flag deep dive](https://alex000kim.com/posts/2026-03-31-claude-code-source-leak/)
- [Dataconomy — Conway tested as persistent agent platform](https://dataconomy.com/2026/04/03/anthropic-tests-conway-platform-for-continuous-claude/)
- [TestingCatalog on X — original BREAKING tweet](https://x.com/testingcatalog/status/2039490365414048182)
