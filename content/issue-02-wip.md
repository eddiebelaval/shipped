---
issue: 02
slug: wip
title: TBD
status: draft
ship_date: 2026-04-24
running_order_locked: false
running_order_decision_at: 2026-04-23  # Thursday — allow the week to play out
---

# Issue 02 — Working Document

> This file is the canonical Issue 02 scratchpad until Thursday 2026-04-23.
> At that point we lock the running order, pick the slug, and start prose.
> Until then: collect facts, refine angles, catch anything the week throws.

---

## Editorial Decisions (locked Mon 2026-04-20 PM; updated Tue 2026-04-21 AM)

- **Lead story (A):** Claude Design. Anthropic shipped it Apr 17, same morning Shipped. Issue 01 went live.
- **Secondary story (B):** **Conway** — Anthropic's codename for an always-on, containerized Claude agent with extension UI. Reported by testingcatalog.com from unreleased build analysis (Tue 2026-04-21). _Tentative B slot pending Thursday confirmation; promotes to lead if it ships this week._
- **Investigation:** The Trust Week — Lovable + Vercel, as builder warnings with Anthropic-compatible SOPs tied back.
- **Editorial frame for security piece:** warn builders + tie back to Anthropic + ship vetted SOPs from pros we research. Not news-for-news-sake; action layer.
- **Thematic spine:** Anthropic landed one product (Claude Design) and is about to ship another (Conway). Two ecosystem platforms broke (Lovable + Vercel). Here's what builders should do. What shipped → what's coming → what broke → what to do.
- **Opening meta beat:** how Issue 01's readers (WhatsApp group) shaped this issue — translation asks, podcast ask, and what we decided to do with each (ES pocketed to 03; podcast in VISION roadmap; this piece leans into "action layer" signal).
- **ES pilot:** POCKETED to Issue 03. Reason: editorial load already heavy; splitting focus breaks quality bar.
- **Running order:** NOT locked until Thursday 2026-04-23. The week may surface something bigger.

---

## Proposed Skeleton

| Section | Content | Status |
|---|---|---|
| Open | Meta: Issue 01 dropped same morning as Claude Design; WhatsApp group shaped this issue | to write |
| Lead Story (A) | Claude Design: what it is, who it's for, Figma drop, "Anthropic ships products not just models" read | researching |
| Secondary Story (B) | Conway: reported always-on containerized Claude agent with extensions, connectors, webhooks. Pre-launch. | researching |
| Investigation: Trust Week | Lovable BOLA + Vercel via Context.ai — two failure modes, same weekend | researching |
| Builder SOPs | Vetted actionable tips — rotate env vars, audit third-party OAuth scopes, etc. | needs pro interviews |
| Release Log | Full weekly dump (scraper populates Thursday) | blocked on scrape |
| Close / Term of Issue | "Trust" as the week's term; counterpoint between Claude Design reading your codebase and the breaches showing platform risk | to write |

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

## Story 2 — Conway (B STORY — reported, pre-launch)

> **Confidence caveat.** This is reported-from-unreleased-builds, not an Anthropic announcement. Attribute carefully. Use "reported codename" not "announced product." Issue 01's Mythos beat is precedent. If Anthropic ships or confirms it by Thursday, it promotes to lead and Claude Design slides to B.

**The facts (as reported by testingcatalog.com Tue 2026-04-21):**
- Codename: **Conway**.
- Description: always-on Claude agent running in a **containerized Claude environment**, persistent alongside standard conversations.
- **UI surface observed in builds:**
  - Custom UI tabs extensions can provide
  - Extension install + management
  - Connector and webhook configuration
  - Model selection for the agent
  - Container lifecycle control
  - Fine-grained tool-call management
  - Separate chat tab for agent interaction
  - "Installed" and "Built-in" sidebar sections (web)
- **Cross-platform parity:** iOS reached parity with the desktop settings interface in recent builds — manage extensions/connectors/webhooks/model selection on mobile.
- **Status:** confirmed in active development via build evidence. Pre-launch, no public release window.
- The **"extension platform"** framing is the reporter's analytical interpretation, not a disclosed capability.

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
- TestingCatalog (original report): https://www.testingcatalog.com/anthropics-works-on-its-always-on-agent-with-new-ui-extensions/

**TODO before Thursday:**
- [ ] Check @claudedevs for any Conway-adjacent hints (teaser tweets, docs preview, research drops)
- [ ] Search X for the Conway codename tweet the article references — archive it in case it gets deleted
- [ ] Look at the iOS build version history if possible (App Store update notes) for corroboration
- [ ] Decide by Thursday: run the B story on reporting-only with clear attribution, or hold for Issue 03 if Anthropic ships it meanwhile

---

## Story 3 — The Trust Week (INVESTIGATION)

### 2a. Lovable BOLA vulnerability

**The facts:**
- **BOLA** (Broken Object Level Authorization) flaw in `/projects/{id}/*` endpoints.
- Endpoints verify Firebase auth tokens but skip ownership checks — any free account can access any other user's project data.
- **Exposed:** source code, hardcoded DB credentials, AI chat histories.
- Bug reported **48 days ago** and not fixed. Marked as duplicate and left open.
- Researchers demonstrated live admin-panel access to **Connected Women in AI** (Danish nonprofit): pulled real names, job titles, LinkedIn profiles, Stripe customer IDs via hardcoded Supabase creds in the source.
- **Lovable's response:** "We did not suffer a data breach" — despite the documented exposure.
- Affected projects created before Nov 2025.

**Sources:**
- Superblocks (detailed technical breakdown): https://www.superblocks.com/blog/lovable-vulnerabilities
- Cyber Kendra: https://www.cyberkendra.com/2026/04/lovable-left-thousands-of-projects.html
- CybersecurityNews: https://cybersecuritynews.com/lovable-ai-app-builder-customer-data/
- Sifted (Lovable's denial): https://sifted.eu/articles/lovable-denies-data-breach
- Polymarket on X: https://x.com/Polymarket/status/2046248814290387129

### 2b. Vercel breach via Context.ai

**The facts:**
- Weekend incident disclosed **Sun 2026-04-19**.
- **Root cause:** Context.ai was breached first. Attackers used a Vercel employee's Context.ai → Vercel OAuth integration to pivot in.
- The Context.ai integration had **deployment-level Google Workspace OAuth scopes** — privileged foothold once Context.ai fell.
- **Affected:** hundreds of users across many orgs.
- Sensitive-marked env vars: encrypted, believed safe. Non-sensitive env vars: need rotation.
- **Threat actor:** ShinyHunters. Claims selling access. Alleged $2M ransom discussion per Telegram messages.
- Crypto/API keys most at-risk — CoinDesk reports developers scrambling to rotate.

**Sources:**
- Vercel official bulletin: https://vercel.com/kb/bulletin/vercel-april-2026-security-incident
- TechCrunch (Context.ai tie): https://techcrunch.com/2026/04/20/app-host-vercel-confirms-security-incident-says-customer-data-was-stolen-via-breach-at-context-ai/
- BleepingComputer (ShinyHunters): https://www.bleepingcomputer.com/news/security/vercel-confirms-breach-as-hackers-claim-to-be-selling-stolen-data/
- SecurityWeek: https://www.securityweek.com/next-js-creator-vercel-hacked/
- The Hacker News: https://thehackernews.com/2026/04/vercel-breach-tied-to-context-ai-hack.html
- CoinDesk (developer scramble): https://www.coindesk.com/tech/2026/04/20/hack-at-vercel-sends-crypto-developers-scrambling-to-lock-down-api-keys
- iTnews (secrets rotation): https://www.itnews.com.au/news/cloud-deployment-firm-vercel-breached-advises-secrets-rotation-625197

### 2c. The through-line

Two failure modes, same weekend:
- **Lovable** — platform-level security debt + denial. 48 days of unfixed BOLA. Then "we didn't have a breach."
- **Vercel** — supply-chain compromise via third-party integration. Didn't exploit a Vercel bug — exploited a privileged OAuth scope granted to an integrated AI platform (Context.ai).

The frame: **"The platform under your app can fail in ways you didn't model."** Builders assume the platform is secure; the platform assumes the integration is secure; the integration wasn't.

**TODO before Thursday:**
- [ ] One pro interview for SOPs — who? (Candidates: an infosec engineer at a YC-backed AI co; an Anthropic DevRel; a known builder who rotated in response)
- [ ] Check if Anthropic's Claude Code / Skills spec has a prescribed pattern for OAuth scope minimization
- [ ] Monitor for updates — Lovable may ship a fix; Vercel may clarify scope; ShinyHunters may release data
- [ ] Check if any Shipped. readers were affected (ask in WhatsApp group?)

---

## Story 3 — Opening Meta Beat

Not a full section — one paragraph in the open, maybe 150 words.

**Beats to hit:**
- Issue 01 dropped Friday 2026-04-17, 9 AM ET. Claude Design dropped the same morning.
- WhatsApp group started asking for ES + PT translations, a video, a podcast.
- We decided: ES pocketed to 03 (quality over quantity this week), podcast in roadmap, video low-priority.
- The signal that mattered most: readers wanted **action**, not summary. This issue's secondary piece leans into that — SOPs, not recaps.
- "This is what 01 taught us about 02: the magazine works better when it pushes from 'what happened' to 'what to do about it.'"

---

## Term of Issue candidates

- **"Trust"** — obvious but strong. The platform-risk frame.
- **"Context"** — Claude Design reads your context; Context.ai was the attack vector; context is the week's double-edged sword.
- **"Scope"** — OAuth scopes are the Vercel story; scope is the VISION.md concept for Shipped.; scope fence is the editorial discipline.
- **"Always-on"** — Conway is always-on. Breaches are always-on risk. The week argues the builder stack is always-on and needs to be treated as such.

Pick Thursday.

---

## Thursday Decision Checklist (2026-04-23)

- [ ] Running order: Claude Design (A) → Conway (B) → Trust Week (investigation) → SOPs. Still right?
- [ ] **Conway promotion check:** did Anthropic ship/announce Conway this week? If yes → Conway becomes lead, Claude Design slides to B.
- [ ] **Conway hold check:** if build evidence weakened or Anthropic pushed back, hold Conway for Issue 03 and restore Trust Week to co-lead with Claude Design.
- [ ] Slug for issue-02-*.md (rename from `wip`)
- [ ] Title
- [ ] Term of Issue locked
- [ ] All TODOs above resolved or explicitly deferred
- [ ] Scraper output reviewed for anything bigger I'm missing
- [ ] Pro interview booked for SOPs section
