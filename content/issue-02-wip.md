---
issue: 02
slug: presence
title: Presence
term_of_issue: Presence
investigation_umbrella: Trust Week
status: draft
ship_date: 2026-04-24
running_order_locked: true
running_order_decision_at: 2026-04-23
slug_locked_at: 2026-04-22
canonical_file: content/issue-02-presence.md  # skeleton assembled Wed PM, 11 prose slots
by_the_numbers:
  head: "By <em>the</em> numbers."
  deck: "The shape of one week — the product turn, the trust margin, the scale Anthropic bought."
  cells:
    - label: "Figma close on Apr 17, the day Claude Design shipped"
      value: "−7.28%"
      size: 4
      accent: true
    - label: "Anthropic products shipped or staged this month"
      value: "2"
      note: "Claude Design (shipped Apr 17) + Conway (staged, per the leak)"
      size: 4
    - label: "Hidden feature flags in the Claude Code source leak"
      value: "44"
      note: "KAIROS, EPITAXY, BRIDGE_MODE, and 41 more"
      size: 4
    - label: "Labs shipped variants of the Presence pattern this week"
      value: "3"
      note: "Anthropic (Claude Design + Conway), OpenAI (Codex workspace agents), Google (Gemini auto-browse)"
      size: 6
    - label: "Regulatory venues engaged on Mythos in 7 days"
      value: "5"
      note: "US Treasury, Bank of England, Financial Stability Board, White House, Pentagon"
      size: 6
    - label: "Days Lovable's BOLA sat unfixed"
      value: "48"
      note: "HackerOne report closed as intended behavior"
      size: 3
    - label: "BreachForums listing for Vercel data"
      value: "$2M"
      note: "Initially credited to ShinyHunters, who denied involvement"
      size: 3
    - label: "Amazon investment in Anthropic"
      value: "$25B"
      note: "$5B now + $20B on commercial milestones"
      size: 3
    - label: "Anthropic compute commitment to AWS over 10 years"
      value: "$100B"
      note: "1 GW via Trainium2/3 by end of 2026; 5 GW target"
      size: 3
    - label: "Additional TPU capacity via Broadcom + Alphabet from 2027"
      value: "3.5 GW"
      size: 6
    - label: "Anthropic run-rate revenue"
      value: "$30B"
      note: "Up from $9B at end of 2025"
      size: 6
    - label: "Bugs confirmed in the Anthropic Claude Code post-mortem, published Apr 23"
      value: "3"
      note: "Default effort (fixed Apr 7), caching with thinking deletion (v2.1.101, Apr 10), system-prompt verbosity cap (v2.1.116, Apr 20). API never touched."
      size: 6
      accent: true
    - label: "Anthropic public statements on Conway between the leak and ship day"
      value: "0"
      note: "The silence is the data"
      size: 6
---

# Issue 02 — Working Document

> This file is the canonical Issue 02 scratchpad until Thursday 2026-04-23.
> At that point we lock the running order, pick the slug, and start prose.
> Until then: collect facts, refine angles, catch anything the week throws.

---

## Editorial Decisions (locked Mon 2026-04-20 PM; updated Tue 2026-04-21 AM + PM)

- **Lead story (A):** Claude Design. Anthropic shipped it Apr 17, same morning Shipped. Issue 01 went live.
- **Secondary story (B) — LOCKED Wed 2026-04-22 PM:** Conway runs as a **standalone B-story (Feature slot)**, not as Lead third-act. Eddie's call. Front-of-book draft + signal report had recommended Lead third-act; overridden in favor of giving Conway its own reporting frame.
  - Trust Week stays in Investigation slot (not promoted to secondary).
  - Front-of-book word budget impact: runs heavier. Close monitoring against the 1,500-word ceiling at Thursday lock.
- **Investigation:** The Trust Week — Lovable + Vercel, as builder warnings with Anthropic-compatible SOPs tied back. _If Conway moves into Lead as third-act, Trust Week moves up to secondary._
- **Editorial frame for security piece:** warn builders + tie back to Anthropic + ship vetted SOPs from pros we research. Not news-for-news-sake; action layer.
- **Thematic spine:** Anthropic landed one product (Claude Design) and is about to ship another (Conway). Two ecosystem platforms broke (Lovable + Vercel). Here's what builders should do. What shipped → what's coming → what broke → what to do.
- **Opening meta beat:** how Issue 01's readers (WhatsApp group) shaped this issue — translation asks, podcast ask, and what we decided to do with each (ES pocketed to 03; podcast in VISION roadmap; this piece leans into "action layer" signal).
- **ES pilot:** POCKETED to Issue 03. Reason: editorial load already heavy; splitting focus breaks quality bar.
- **Term of Issue — LOCKED PRESENCE** (Wed 2026-04-22 PM, Eddie). _Leading candidate from signal report's Tue PM re-rank confirmed. Slug: `presence`. Title: TBD (pick Thursday). Companion piece `presence-as-category.md` captured as scaffolding for the thesis._
- **Amazon-Anthropic deal ($25B / $100B / 10yr):** Release-log-only (Eddie confirmed Tue AM). Not the lead, not the secondary. One entry under `[NEWS]`. Two or three sentences allowed in front-of-book if word budget permits; not a narrative spine.
- **ShinyHunters attribution — softened.** ShinyHunters publicly denied Vercel involvement (per BleepingComputer + Hackread, Mon/Tue). BreachForums $2M listing still live but the group usually credited has distanced themselves. Magazine copy must read "initially credited to ShinyHunters; group has since denied involvement." _Was: "ShinyHunters / $2M ransom" → now: softened attribution._
- **Signal report absorbed:** Tue 2026-04-21 PM. `content/articles/issue-02/signal-report.md` findings pulled into fact sheets and Thursday checklist below.
- **Running order:** NOT locked until Thursday 2026-04-23. The week may surface something bigger.

---

## Proposed Skeleton

| Section | Content | Status |
|---|---|---|
| Open | Meta: Issue 01 dropped same morning as Claude Design; WhatsApp group shaped this issue. "Presence" frame. | drafted (see `articles/issue-02/front-of-book-draft.md`) |
| Lead Story (A) | Claude Design: what it is, who it's for, Figma drop, "Anthropic ships products not just models" read | distilled draft (214 words — see Story 1 below) |
| Secondary Story (B) / Feature | Conway: reported always-on containerized agent. **Locked standalone B-story (Feature slot) Wed 2026-04-22 PM.** | research — placement resolved |
| Investigation: Trust Week | Lovable 4-stage evolution + Vercel via Context.ai. ShinyHunters attribution softened. | research (expanded with signal report) |
| Also Shipped | OpenClaw Anthropic return + Vercel sensitive-default + Claude performance backlash | 3 research articles captured, all grade A. Thursday scrape may add 1-2 more. |
| Quiet on the Wire | Claude Code briefly removed from $20 Pro plan (Avasare 2% quote) | research article captured at grade A 28/28 |
| Builder SOPs | Vetted actionable tips — rotate env vars, audit third-party OAuth scopes, etc. | needs pro interviews |
| Release Log | release-log-research.md captured Wed PM with 10 entries across Apr 17 to 22 window | research. Scraper tokenless; built from releasebot + primary sources. Top-off Thursday PM for Thu items; final Friday 7 AM. |
| Close / Term of Issue | "Presence" leading; counterpoint between always-on products absorbing context and always-on platforms failing that trust | to write |

---

## Story 1 — Claude Design (LEAD)

> Full source article: `content/articles/issue-02/claude-design-reception.md` (~900 words, drafted 2026-04-21). The prose below is the 200–300 word Lead Story distillation for the magazine. Full article preserves research and Anthropic-pattern analysis that didn't fit the word budget.

### Lead Story — distilled draft (214 words)

Thursday, 9 AM. Anthropic shipped Claude Design — a product, not a model — the same morning Issue 01 hit. Pro, Max, Team, and Enterprise subscribers got access. Everyone else got a waitlist.

Claude Design turns a prompt, a codebase, or a half-written PRD into something you can send somewhere. Pitch decks, prototypes, one-pagers, full design systems. Exports to PDF, URL, PPTX, or Canva, where the artifact stays editable. Powered by Opus 4.7.

Figma closed down 7.28%.

The market's first read is split almost exactly down the middle. Brilliant and Datadog, on record, call it a step change — twenty prompts compressed to two, week-long cycles collapsed into a conversation. The r/ClaudeAI community landed on what one recap called "a resounding meh" — every application looks the same unless you upload your own design tokens.

Both reads are true. For a team with a design system, Claude Design is a compression engine. For an individual trying to ship something with character, it's a mirror that returns whatever average its training produced.

The distribution choice is the tell. Exports flow to Canva, not Figma. Designers already have their tool. Claude Design is aimed at the team member who opens Canva at 4 PM the Tuesday before an all-hands.

That team member has a name. It might be you.

### Voice budget used in this distillation

- **"X isn't Y, it's Z" formula:** NOT used here (issue budget already spent once in the long article on "Anthropic is not building an API company..." — cannot re-use at issue level).
- **Forbidden phrases:** none.
- **Opening pattern:** specific-moment timing ("Thursday, 9 AM") — matches the Open's "Last Friday, Issue 01 hit at 9 AM" anchor.
- **First person:** avoided. Reserved for the Open per front-of-book structure.
- **Term of issue ("Presence"):** echoed implicitly in the close — "That team member has a name. It might be you." The product arrives before you call for it. Not stated.
- **Rhythm:** period-heavy, short after long, one-sentence paragraph for stock-drop landing beat.

### Research notes

**The facts:**
- Launched **Thu 2026-04-17** — same morning as Shipped. Issue 01.
- Experimental/research preview for Claude Pro, Max, Team, Enterprise.
- Powered by **Opus 4.7** — Anthropic's most capable vision model.
- Turns prompts into prototypes, slides, one-pagers, full design systems.
- Reads your codebase + design files to apply your design system automatically.
- Exports: PDF, URL, PPTX, or send to **Canva** (fully editable there).
- **Figma stock dropped 7.28%** on the launch day.

**Angles to explore by Thursday:**
- The "Anthropic ships products, not just models" read. Claude Code, Claude Design, `ant` CLI — they're going vertical into builder workflows.
- The Canva partnership angle. Why Canva and not Figma? Distribution play.
- Who's actually the user? Designers will scoff; PMs and founders who don't use Figma might not.
- The codebase-reading capability — this is the same axis as Claude Code. Context absorption is becoming the moat.

**Sources (primary):**
- TechCrunch: https://techcrunch.com/2026/04/17/anthropic-launches-claude-design-a-new-product-for-creating-quick-visuals/
- VentureBeat: https://venturebeat.com/technology/anthropic-just-launched-claude-design-an-ai-tool-that-turns-prompts-into-prototypes-and-challenges-figma
- SiliconANGLE: https://siliconangle.com/2026/04/17/anthropic-launches-claude-design-speed-graphic-design-projects/
- Gizmodo (Figma stock): https://gizmodo.com/anthropic-launches-claude-design-figma-stock-immediately-nosedives-2000748071
- MacRumors: https://www.macrumors.com/2026/04/17/anthropic-claude-design/

**TODO before Thursday:**
- [ ] Try Claude Design yourself with a Shipped. mockup. First-hand screenshots.
- [ ] Find one developer or designer using it in the wild to quote (check X, LinkedIn).
- [ ] Confirm exact research-preview eligibility (is it rolling out to all Max subscribers today?).

---

## Story 2 — Conway (PLACEMENT OPEN: B STORY vs Lead third-act)

> **Confidence caveat.** This is reported-from-unreleased-builds + source-code leak, not an Anthropic announcement. Attribute carefully. Use "reported codename" not "announced product." Issue 01's Mythos beat is precedent. If Anthropic ships or confirms it by Thursday, it promotes to lead and Claude Design slides to B.

> **Placement conflict to resolve Thursday:** front-of-book draft and signal report both recommend Conway as a **Lead-Story third act** (inside Claude Design's section). WIP currently has it as separate B. Editorial call: does Conway tighten the "Anthropic ships products" thesis (third-act inside Lead) or stand on its own (separate B)?

### The March 31 Claude Code source-code leak (primary evidence)

On 2026-03-31, `@anthropic-ai/claude-code` v2.1.88 shipped with a missing `.npmignore` entry. The result: a **59.8 MB `cli.js.map` source map** went public — roughly **512,000 lines of TypeScript across ~1,906 files**. Anthropic confirmed it was a packaging error, not a security breach.

The leak exposed:

- **44 hidden feature flags.** Named ones include `PROACTIVE`, `KAIROS`, `VOICE_MODE`, `BRIDGE_MODE`.
- **KAIROS** (Greek for *the right moment*) — a fully-built autonomous daemon mode. Not shipped.
- **Conway** — sidebar option inside Claude's interface that launches a "Conway instance" with three panes: **Search, Chat, System**.
- **`.cnw.zip`** — a proprietary extension format for custom tools, UI tabs, and context handlers.
- **Webhook triggers** — public URLs that wake the instance.
- **Browser control** — Conway can drive Chrome.
- **GitHub subscriptions** — Conway watches repo activity and responds proactively.
- **Push notifications** when tasks complete or conditions trigger.
- **`EPITAXY`** — Claude Code integration codename, clustered with Conway in the code.

### The TestingCatalog follow-up (Tue 2026-04-21)

The iOS version of Claude now has a **hidden feature flag related to managed 24/7 agents**. Evidence Conway is being prepared for consumer-facing rollout, not just an internal experiment. That's the meaningful shift — from "leaked internal project" to "consumer product being staged."

TestingCatalog's Tue report also documented the visible UI surface in unreleased builds:

- Custom UI tabs extensions can provide
- Extension install + management
- Connector and webhook configuration
- Model selection for the agent
- Container lifecycle control
- Fine-grained tool-call management
- Separate chat tab for agent interaction
- "Installed" and "Built-in" sidebar sections (web)
- iOS reached parity with the desktop settings interface

**Status:** confirmed in active development via build + leak evidence. Pre-launch, no public release window. The **"extension platform"** framing is a reporter's analytical interpretation, not a disclosed capability.

**The editorial argument:**
Anthropic is extending into **always-on, context-absorbing, platform-style products**. Claude Design reads your codebase + design files. Conway runs in a persistent container with extensions and webhooks. The product surface is no longer a chat window — it's a shell that lives next to you and composes with third-party primitives. This is the same axis as Claude Code + Skills + `ant` CLI, just further along.

Connects directly to the Trust Week investigation: as Anthropic's products absorb more context and integrate more third-party surfaces, the OAuth-scope / supply-chain failure modes Lovable and Vercel just demonstrated become *more* relevant, not less. Always-on agents with extension platforms are exactly where this question lands next.

**Angles to explore by Thursday:**
- Is there anything Anthropic-official we can pair with the build-leak? Check @claudedevs, @alexalbert__, the Anthropic blog, the research page.
- Does the codename "Conway" reference John Conway (Game of Life — cellular automata, long-running systems)? That'd be a good detail if confirmed; avoid if speculative.
- Implicit comparison to OpenAI's Operator / Google's agentic assistants — how does "containerized + extensions + webhooks" position differently?
- What does an "extension" in Conway mean for builders? Paying developers? Free market? MCP-style? Anthropic hasn't said.
- Privacy/security: always-on + containerized runs into the exact trust questions Trust Week is asking.

**Sources (primary):**
- TestingCatalog (Conway scoop): https://www.testingcatalog.com/exclusive-anthropic-tests-its-own-always-on-conway-agent/ _(egress-blocked, cited from search)_
- TestingCatalog (UI extensions follow-up): https://www.testingcatalog.com/anthropics-works-on-its-always-on-agent-with-new-ui-extensions/
- The Hacker News (Anthropic confirms packaging error): https://thehackernews.com/2026/04/claude-code-tleaked-via-npm-packaging.html
- VentureBeat (leak analysis): https://venturebeat.com/technology/claude-codes-source-code-appears-to-have-leaked-heres-what-we-know
- Layer5 (512k lines, `.npmignore` story): https://layer5.io/blog/engineering/the-claude-code-source-leak-512000-lines-a-missing-npmignore-and-the-fastest-growing-repo-in-github-history/
- Alex Kim (Conway + KAIROS feature-flag deep dive): https://alex000kim.com/posts/2026-03-31-claude-code-source-leak/
- Dataconomy (Conway as persistent agent platform): https://dataconomy.com/2026/04/03/anthropic-tests-conway-platform-for-continuous-claude/
- TestingCatalog on X (original BREAKING tweet): https://x.com/testingcatalog/status/2039490365414048182

**Sourcing discipline before press:** pick **2 primary sources** to cite in the magazine — TestingCatalog (broke the story) + one secondary verification (VentureBeat, The Hacker News, or Dataconomy). The rest live in the article file for research depth.

**TODO before Thursday:**
- [ ] **Placement decision** — Conway as B story (current WIP) or Lead third-act (signal/front-of-book recommendation)
- [ ] Check @claudedevs for any Conway-adjacent hints (teaser tweets, docs preview, research drops)
- [ ] Capture Conway analysis into its own article file: `content/articles/issue-02/conway-leak-analysis.md`
- [ ] Look at the iOS build version history if possible (App Store update notes) for corroboration
- [ ] Decide by Thursday: run on reporting-only with clear attribution, or hold for Issue 03 if Anthropic ships it meanwhile

---

## Story 3 — The Trust Week (INVESTIGATION)

### 2a. Lovable BOLA vulnerability

**The facts:**
- **BOLA** (Broken Object Level Authorization) flaw in `/projects/{id}/*` endpoints.
- Endpoints verify Firebase auth tokens but skip ownership checks — any free account can access any other user's project data.
- **Exposed:** source code, hardcoded DB credentials, AI chat histories.
- Bug reported **48 days ago** and not fixed. Marked as duplicate and left open.
- Researchers demonstrated live admin-panel access to **Connected Women in AI** (Danish nonprofit): pulled real names, job titles, LinkedIn profiles, Stripe customer IDs via hardcoded Supabase creds in the source.
- Affected projects created before Nov 2025.

**Lovable's shifting public story (4 stages, per Register 2026-04-20):**

1. **First:** "intentional behavior" and "unclear documentation."
2. **Then:** blame shifted to **HackerOne** — reports were closed as duplicate because triagers "thought it was intended behavior."
3. **Then:** admitted a **February 2026 permissions-unification** accidentally re-enabled access to public-project chats.
4. **Now:** partial fix shipped — **new projects patched, every pre-existing (pre-Nov 2025) project remains exposed.**

Techloy ran a headline claiming Lovable "fixes" the vulnerability. Independent coverage confirms: the fix is **new-projects-only**. That gap — fix announced vs. legacy still exposed — is the editorial beat worth stating cleanly in the magazine. A company that restructured its story four times in a week, then shipped a fix that covered only new accounts, is showing you the trust margin of the platform under your app.

**Sources:**
- The Register ("intentional behavior" defense): https://www.theregister.com/2026/04/20/lovable_denies_data_leak/
- Techloy (partial fix claim): https://www.techloy.com/is-your-code-safe-lovable-ai-fixes-vulnerability-that-leaked-database-credentials/
- Computing.co.uk (flaw exposed source + creds + chats): https://www.computing.co.uk/news/2026/security/lovable-flaw-exposed-source-code-credentials-and-ai-chats
- Superblocks (detailed technical breakdown): https://www.superblocks.com/blog/lovable-vulnerabilities
- Cyber Kendra: https://www.cyberkendra.com/2026/04/lovable-left-thousands-of-projects.html
- CybersecurityNews: https://cybersecuritynews.com/lovable-ai-app-builder-customer-data/
- Sifted (Lovable's initial denial): https://sifted.eu/articles/lovable-denies-data-breach
- Polymarket on X: https://x.com/Polymarket/status/2046248814290387129

### 2b. Vercel breach via Context.ai

**The facts:**
- Weekend incident disclosed **Sun 2026-04-19**.
- **Root cause:** Context.ai was breached first. Attackers used a Vercel employee's Context.ai → Vercel OAuth integration to pivot in.
- The Context.ai integration had **deployment-level Google Workspace OAuth scopes** — privileged foothold once Context.ai fell.
- **Affected:** hundreds of users across many orgs.
- Sensitive-marked env vars: encrypted, believed safe. Non-sensitive env vars: need rotation.
- Crypto/API keys most at-risk — CoinDesk reports developers scrambling to rotate.
- **Vendor response (per Vercel bulletin):** Mandiant, GitHub, Microsoft, npm, and Socket engaged. Vercel confirmed no compromised npm packages published by Vercel itself.
- **Policy change going forward:** environment variable default is changing to `sensitive: on`. Non-sensitive was the exposed surface; this flips the default.
- **Framing beat:** The Register called it **"AI-pwned"** — the attack chain was stolen employee creds via an OAuth-connected AI platform (Context.ai). Same category as Lovable: *the platform's dependencies are the attack surface now.*

### 2c. Attribution reversal — ShinyHunters denies

**This is new (Mon/Tue 2026-04-20/21):** ShinyHunters told BleepingComputer they are **not involved** in the Vercel breach. Hackread reported the same denial. The **BreachForums listing offering Vercel data at $2M is still live**, but the group usually credited has distanced themselves.

**Magazine copy implication:** soften the actor line. *Was: "ShinyHunters claimed responsibility / $2M ransom" → now: "initially credited to ShinyHunters; the group has since publicly denied involvement; the $2M BreachForums listing remains live but unattributed."*

This is a case study in press-cycle attribution drift. It also loosens the Vercel story slightly — it's still a supply-chain compromise via Context.ai, but the public-facing actor story is less clean than reporters initially wrote.

**Sources:**
- Vercel official bulletin: https://vercel.com/kb/bulletin/vercel-april-2026-security-incident
- The Register ("AI-pwned"): https://www.theregister.com/2026/04/21/vercel_ceo_points_to_aidriven/
- GitGuardian (non-sensitive env vars still matter): https://blog.gitguardian.com/vercel-april-2026-incident-non-sensitive-environment-variables-need-investigation-too/
- TechCrunch (Context.ai tie): https://techcrunch.com/2026/04/20/app-host-vercel-confirms-security-incident-says-customer-data-was-stolen-via-breach-at-context-ai/
- BleepingComputer (ShinyHunters denial): https://www.bleepingcomputer.com/news/security/vercel-confirms-breach-as-hackers-claim-to-be-selling-stolen-data/
- Hackread (ShinyHunters denial): https://hackread.com/vercel-breach-context-ai-shinyhunters-not-involved/
- SecurityWeek: https://www.securityweek.com/next-js-creator-vercel-hacked/
- The Hacker News: https://thehackernews.com/2026/04/vercel-breach-tied-to-context-ai-hack.html
- CoinDesk (developer scramble): https://www.coindesk.com/tech/2026/04/20/hack-at-vercel-sends-crypto-developers-scrambling-to-lock-down-api-keys
- iTnews (secrets rotation): https://www.itnews.com.au/news/cloud-deployment-firm-vercel-breached-advises-secrets-rotation-625197

### 2d. The through-line

Three failure modes, same weekend:
- **Lovable** — platform-level security debt + denial. 48 days of unfixed BOLA. Four versions of a public story in a week. Fix that covers new accounts only.
- **Vercel** — supply-chain compromise via third-party integration. Didn't exploit a Vercel bug — exploited a privileged OAuth scope granted to an integrated AI platform (Context.ai).
- **Attribution drift** — press credited ShinyHunters. ShinyHunters denied. BreachForums listing still live, unattributed. A small but real story about how breach narratives solidify before facts do.

The frame: **"The platform under your app can fail in ways you didn't model."** Builders assume the platform is secure; the platform assumes the integration is secure; the integration wasn't.

**TODO before Thursday:**
- [ ] One pro interview for SOPs — who? (Candidates: an infosec engineer at a YC-backed AI co; an Anthropic DevRel; a known builder who rotated in response)
- [ ] Check if Anthropic's Claude Code / Skills spec has a prescribed pattern for OAuth scope minimization
- [ ] Monitor for updates — Lovable may ship a full-fleet fix; Vercel may clarify scope; ShinyHunters situation may firm up
- [ ] Check if any Shipped. readers were affected (ask in WhatsApp group?)
- [ ] Capture both Lovable + Vercel into their own article files: `content/articles/issue-02/trust-week-lovable.md` + `trust-week-vercel.md`

---

## Story 4 — Amazon-Anthropic Deal (RELEASE LOG ONLY)

> **Eddie's call Tue AM:** release-log-only, not lead material. One `[NEWS]` entry. Optional two-three sentence mention in front-of-book if word budget allows, but not a narrative spine.

**The facts:**
- Announced **Mon 2026-04-20 / Tue 2026-04-21.**
- Amazon invests **up to $25B in Anthropic** — **$5B now, $20B on commercial milestones.**
- Anthropic commits **$100B+ on AWS over 10 years.**
- Target: **1 GW capacity via Trainium2 / Trainium3 by end of 2026; 5 GW total goal.**
- Ties back to Project Glasswing / Mythos context already referenced in Issue 01.

**Editorial treatment:** Release Log entry, `[NEWS]` tag, standard template. The size of the number matters less than the timing — Anthropic's compute commitments are scaling with their product ambitions (Claude Design, Conway). If front-of-book has room, one line acknowledging "the scale Anthropic is now buying" fits the thematic spine without hijacking it.

**Sources:**
- Rappler: https://www.rappler.com/technology/amazon-investment-anthropic-april-20-2026/
- Meyka (Apr 21 framing): https://meyka.com/blog/amazon-invests-25b-in-anthropic-ai-on-april-21-2026-2104/

---

## Story 5 — OpenClaw Anthropic Return (ALSO SHIPPED)

> Captured as a full article: `content/articles/issue-02/openclaw-anthropic-return.md`. Research-status; 60-100 word compress for Also Shipped.

**The beat:** OpenClaw (multi-provider LLM gateway — unified config across Anthropic, OpenAI, Qwen, MiniMax, Z.AI, Bedrock) has re-enabled full Anthropic support, including Claude CLI backend reuse. Feature matrix is thorough (prompt caching, extended thinking, Fast mode, 1M context). But the real signal is a line in their docs: *"Anthropic staff reportedly told us OpenClaw-style Claude CLI usage is allowed again."*

**Editorial angle:** policy signal, not a feature launch. A previously grey-zone integration path is now sanctioned — per OpenClaw, not per Anthropic. Fits the thematic spine: Anthropic expanding the sanctioned surface area for how builders use Claude, right as the Trust Week shows what happens when platforms mishandle that kind of flexibility.

**Attribution discipline:** magazine copy must read "per OpenClaw's docs" — no public Anthropic statement corroborates the policy reversal. Flag in Thursday checklist.

**TODO before Thursday:**
- [ ] Date-stamp the OpenClaw Anthropic re-enablement (changelog entry on their site or GitHub)
- [ ] Scan whether other gateways (OpenRouter, LiteLLM) got the same update — if yes, the beat is broader than OpenClaw alone

**Source:** https://docs.openclaw.ai/providers/anthropic

---

## Opening Meta Beat

Not a full section — one paragraph in the open, maybe 150 words.

**Beats to hit:**
- Issue 01 dropped Friday 2026-04-17, 9 AM ET. Claude Design dropped the same morning.
- WhatsApp group started asking for ES + PT translations, a video, a podcast.
- We decided: ES pocketed to 03 (quality over quantity this week), podcast in roadmap, video low-priority.
- The signal that mattered most: readers wanted **action**, not summary. This issue's secondary piece leans into that — SOPs, not recaps.
- "This is what 01 taught us about 02: the magazine works better when it pushes from 'what happened' to 'what to do about it.'"

---

## Term of Issue — LOCKED PRESENCE (Wed 2026-04-22 PM)

**Decision:** `term_of_issue: Presence`. Slug: `presence`. Title: TBD (pick Thursday).

**Why it won:** Conway's architecture is *presence* itself — persistent, watching, responsive to conditions vs. summoned. Echoes Eddie's `presence-not-tools.md` essay (voice corpus). Contrasts with Claude Design's one-prompt-one-output mode. Opens Move A (memoir → philosophy) pivot.

**Candidates not taken** (archival, for Issue 03+ consideration):
- **"Trust"** — strong fallback, but Presence absorbs Conway better.
- **"Always-on"** — Conway-native but thinner on Claude Design reception beat.
- **"Scope"** — Vercel-heavy; doesn't absorb Conway or Claude Design.
- **"Context"** — cute tri-meaning but thin once Conway joins.

**Container piece:** `articles/issue-02/presence-as-category.md` — locked as Companion to the Lead (150–250w).

---

## Thursday Decision Checklist (2026-04-23)

**Structure decisions (resolve before drafting):**

- [x] **Conway placement** — LOCKED standalone B-story (Feature slot) Wed 2026-04-22 PM. Trust Week stays in Investigation slot.
- [ ] **Conway promotion check:** did Anthropic ship/announce Conway this week? If yes → Conway becomes Lead, Claude Design slides to B, front-of-book rewrites around the ship.
- [ ] **Conway hold check:** if build evidence weakened or Anthropic pushed back publicly, hold Conway for Issue 03 and restore Trust Week to co-lead with Claude Design.
- [x] **Presence-as-category placement** — LOCKED Companion to the Lead (150–250w) Wed 2026-04-22 PM.
- [ ] **Running order confirmation:** with placements resolved, freeze the section order Thursday AM.

**Editorial decisions:**

- [x] **Term of Issue** — LOCKED Presence Wed 2026-04-22 PM.
- [x] **Slug** — LOCKED `presence` Wed 2026-04-22 PM. File rename (`issue-02-wip.md` → `issue-02-presence.md`) deferred to Thursday lock per WIP doctrine.
- [ ] **Title** — open. No candidates drafted yet. Surface 3 Thursday AM once running order freezes.
- [ ] **Attribution line for Vercel** — soften to "initially credited to ShinyHunters; group has since denied involvement; $2M BreachForums listing remains live, unattributed."
- [ ] **Conway sourcing** — pick the 2 primary sources to cite in the magazine: TestingCatalog (broke it) + one secondary (VentureBeat, The Hacker News, or Dataconomy).
- [ ] **OpenClaw attribution** — confirm "per OpenClaw's docs" framing, not "Anthropic sanctioned."

**Research TODOs (resolve or explicitly defer):**

- [ ] Hands-on Claude Design screenshots (Eddie only — first-person use)
- [ ] Developer/designer quote in the wild for Claude Design (X, LinkedIn, HN scan Apr 18+)
- [ ] Pro interview booked for SOPs section (infosec eng at YC AI co; or Anthropic DevRel on Claude Code safety)
- [ ] Capture Conway analysis into `articles/issue-02/conway-leak-analysis.md`
- [ ] Capture Trust Week into two articles: `trust-week-lovable.md` + `trust-week-vercel.md`
- [ ] Date-stamp the OpenClaw Anthropic re-enablement
- [ ] Scan for other-gateway policy updates (OpenRouter, LiteLLM)

**Pipeline TODOs:**

- [x] **Wednesday PM scrape**. `pnpm scrape` failed (no X_API_BEARER_TOKEN, Nitter mirrors dead). Fallback: web research via releasebot.io + primary sources. 10 Release Log entries captured in `release-log-research.md`.
- [ ] **Thursday PM top-off scrape**. Re-run `pnpm scrape` with a token if set up, or re-run the web-research pass. Focus: Claude Code releases Thursday, docs.anthropic.com updates, Avasare follow-ups, any `/agents` or `/skills` API surfacing. See "Still pending, top off Thursday" section of release-log-research.md.
- [ ] **Friday 7 AM final**. Last pass before ship.
- [ ] **Release Log separator format**. STYLE.md uses em dash in `#### YYYY-MM-DD — Title`. Per 2026-04-22 no-em-dashes rule, entries currently use colon. Pick house format at Thursday lock: keep colon and amend STYLE.md, or carve out em dashes for Release Log only.
- [ ] Scraper output reviewed for anything bigger than already-captured (Amazon deal, Claude Code test, Claude Design, Opus 4.7 rollout).
- [ ] Verify Amazon-Anthropic deal fits the `[NEWS]` entry template cleanly.
- [ ] Find primary Amazon press release or Anthropic blog post for the $25B deal; currently attributed to Rappler + Meyka.
- [ ] Archive Avasare X post via Internet Archive before Thursday; X URLs decay.
