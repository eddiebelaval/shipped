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

## Editorial Decisions (locked Mon 2026-04-20 PM)

- **Lead story:** Claude Design. Anthropic shipped it Apr 17, same morning Shipped. Issue 01 went live.
- **Secondary story / investigation:** The Trust Week — Lovable + Vercel, as builder warnings with Anthropic-compatible SOPs tied back.
- **Editorial frame for security piece:** warn builders + tie back to Anthropic + ship vetted SOPs from pros we research. Not news-for-news-sake; action layer.
- **Opening meta beat:** how Issue 01's readers (WhatsApp group) shaped this issue — translation asks, podcast ask, and what we decided to do with each (ES pocketed to 03; podcast in VISION roadmap; this piece leans into "action layer" signal).
- **ES pilot:** POCKETED to Issue 03. Reason: editorial load already heavy; splitting focus breaks quality bar.
- **Running order:** NOT locked until Thursday 2026-04-23. The week may surface something bigger.

---

## Proposed Skeleton

| Section | Content | Status |
|---|---|---|
| Open | Meta: Issue 01 dropped same morning as Claude Design; WhatsApp group shaped this issue | to write |
| Lead Story | Claude Design: what it is, who it's for, Figma drop, "Anthropic ships products not just models" read | researching |
| Investigation: Trust Week | Lovable BOLA + Vercel via Context.ai — two failure modes, same weekend | researching |
| Builder SOPs | Vetted actionable tips — rotate env vars, audit third-party OAuth scopes, etc. | needs pro interviews |
| Release Log | Full weekly dump (scraper populates Thursday) | blocked on scrape |
| Close / Term of Issue | "Trust" as the week's term; counterpoint between Claude Design reading your codebase and the breaches showing platform risk | to write |

---

## Story 1 — Claude Design (LEAD)

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

## Story 2 — The Trust Week (INVESTIGATION)

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

Pick Thursday.

---

## Thursday Decision Checklist (2026-04-23)

- [ ] Running order: still lead-Claude-Design-investigate-security, or flip?
- [ ] Slug for issue-02-*.md (rename from `wip`)
- [ ] Title
- [ ] Term of Issue locked
- [ ] All TODOs above resolved or explicitly deferred
- [ ] Scraper output reviewed for anything bigger I'm missing
- [ ] Pro interview booked for SOPs section
