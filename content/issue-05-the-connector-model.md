---
issue: 05
slug: connector-model
title: "The Connector Model"
date: 2026-05-15
period: 2026-05-11 to 2026-05-15
masthead: Shipped.
deck: "No new model. Claude landed in small business, the Gates Foundation, and PwC's consulting floor the same way every time: reasoning layer in, integration surface borrowed."
byline: Edited by Eddie Belaval. Reported with the assistance of Claude.
term_of_issue: The Connector Model
status: draft
ship_date: 2026-05-15
running_order_locked: true
fob_content: editorial
log_content: reference
---

# Shipped.

**Issue #05: The Connector Model**
*A magazine of what Anthropic ships.*
*Period: 2026-05-11 to 2026-05-15. Volume I.*

---

## The Open

There's a sentence that shows up three times this week, in three documents that have nothing to do with each other. Small business owners read one version. Gates Foundation grant officers read another. PwC's 30,000 staff got the third ([SiliconAngle](https://siliconangle.com/2026/05/14/pwc-expands-anthropic-alliance-will-train-30000-staff-claude/)). Strip the branding off each and the same line is underneath: Anthropic provides the reasoning layer, the partners carry the integration surface.

That is not a coincidence. It is a strategy with a shape, and once you see the shape you can't unsee it. The week after Anthropic spent itself hoarse buying compute, it stopped talking about power and started talking about reach. No new model. No flagship. The most-discussed model this week was Opus 4.7, and the news about it was that Claude Code quietly made it the default in Fast mode ([release notes](https://github.com/anthropics/claude-code/releases)). Everything else was Claude walking into rooms it had never been in, on someone else's floor.

---

## The Lead Story

# Claude went everywhere, and built nothing to get there

The headline this week isn't a product. It's a posture.

On May 13, Anthropic shipped Claude for Small Business, and the product decision underneath the announcement is that there is no product. No new interface, no separate app, no extra line item. It's a toggle that drops Claude-powered connectors into the software small businesses already run: Intuit QuickBooks, PayPal, HubSpot, Canva, DocuSign, Google Workspace, Microsoft 365 ([Anthropic](https://www.anthropic.com/news/claude-for-small-business)). The covered workloads are the unglamorous spine of every small company: payroll planning, month-end close, cash-flow forecasting, invoice chasing, campaign creation ([Anthropic](https://www.anthropic.com/news/claude-for-small-business)). Anthropic put a number on the room it's pitching: 44% of U.S. GDP, roughly half the private-sector workforce ([Anthropic](https://www.anthropic.com/news/claude-for-small-business)). The gap it's selling against is the distance between "we have a chat window" and "Claude is doing work," and a 10-city free half-day workshop tour opened in Chicago on May 14 to close that gap in person ([Anthropic](https://www.anthropic.com/news/claude-for-small-business)). It comes at no extra cost beyond existing Claude licenses, and it travels with its own access program: a Workday Foundation solopreneurship accelerator and three CDFIs (Accion Opportunity Fund, Community Reinvestment Fund USA, Pacific Community Ventures) seeded with Claude credits ([Anthropic](https://www.anthropic.com/news/claude-for-small-business)).

Now hold that next to a number that does not belong in the same sentence as invoice chasing. On May 13, Anthropic and the Gates Foundation committed $200 million in grant funding, Claude usage credits, and technical support over four years to global health, life sciences, education, and agricultural productivity in low- and middle-income countries ([Gates Foundation](https://www.gatesfoundation.org/ideas/media-center/press-releases/2026/05/ai-anthropic-partnership)). The targets are specific, not abstract: polio, HPV, and eclampsia, the diseases that attract no commercial investment because the patients can't pay ([Gates Foundation](https://www.gatesfoundation.org/ideas/media-center/press-releases/2026/05/ai-anthropic-partnership)). Around 4.6 billion people lack access to essential health services, per the Foundation's framing, and that's the audience ([Gates Foundation](https://www.gatesfoundation.org/ideas/media-center/press-releases/2026/05/ai-anthropic-partnership)). The day after, PwC expanded its alliance to put Claude Code and Claude Cowork in front of 30,000 U.S. professionals, with deployments already in production: insurance underwriting cut from 10 weeks to 10 days, incident response from hours to minutes ([SiliconAngle](https://siliconangle.com/2026/05/14/pwc-expands-anthropic-alliance-will-train-30000-staff-claude/)).

Read the three together and the mechanic is identical. Anthropic brings the reasoning layer and the workflow primitives. The partner brings the integration surface: Intuit's APIs and the install base they sit on, the Gates Foundation's three decades of on-the-ground infrastructure in exactly the places Claude will need it, PwC's client base across 136 countries ([SiliconAngle](https://siliconangle.com/2026/05/14/pwc-expands-anthropic-alliance-will-train-30000-staff-claude/)). Anthropic is not building the QuickBooks connector. It is not building the health pipelines or the vaccine-screening tooling. It is not building the consulting practice. It rents the last mile every time, and the last mile is where every previous AI rollout died on the floor of the demo room.

That is the mechanism, and the mechanism has a tell. When a lab builds the integration itself, it owns the relationship and eats the maintenance: every API change at the partner is now its bug. When it ships only the reasoning layer, the partner owns the surface, the data, and the distribution, and the lab keeps shipping models. The connector model is the choice to never own the doors. It is cheaper, it scales sideways across every customer tier at once, and it concedes something real: Anthropic does not want to be the system of record. It wants to be the intelligence that the systems of record call.

The blast radius is the part that doesn't show up in the press release. A small-business owner who has spent three years ignoring AI because it meant ripping out QuickBooks now gets Claude inside QuickBooks, doing the close, with nothing to migrate. A Gates program officer in sub-Saharan Africa gets a drug-screening assistant grounded in infrastructure that already exists, not a pilot that needs a data center. A PwC manager gets a stalled HR transformation restarted with a working prototype in one week ([SiliconAngle](https://siliconangle.com/2026/05/14/pwc-expands-anthropic-alliance-will-train-30000-staff-claude/)). In all three the friction Anthropic removed is the same friction: the cost of leaving the tool you already trust.

The contrast with the rest of the frontier is the quiet point. The consumer-AI playbook of the last two years was to build the destination, the standalone app you open and switch to. Anthropic spent this week doing the opposite, threading the model into destinations that already have the user. It is the same instinct as last week's compute land-grab, inverted: when intelligence is the thing you have plenty of and distribution is the thing you can't manufacture, you stop building front doors and start renting them. This is the same structure as the enterprise push from two weeks ago, scaled across every customer tier in a single week.

The model didn't move this week. The map did.

---

## Feature

# The PwC deal is the connector model wearing a suit

Of the three doors Anthropic walked through this week, PwC is the one that names the prize out loud. The expanded alliance puts Claude Code and Claude Cowork in front of 30,000 U.S. professionals, establishes a joint Center of Excellence, and stands up a Claude-native finance business group inside PwC's Office of the CFO practice ([SiliconAngle](https://siliconangle.com/2026/05/14/pwc-expands-anthropic-alliance-will-train-30000-staff-claude/)). The headcount is the headline, but it is not the story. The story is what PwC is, and what it is willing to retool around Claude.

PwC sells human hours dressed as judgment. Its product is 364,000 people in 136 countries billing time against problems ([SiliconAngle](https://siliconangle.com/2026/05/14/pwc-expands-anthropic-alliance-will-train-30000-staff-claude/)). When a firm whose entire margin is the price of an hour decides to train 30,000 of those hours on an agent that does the work faster, it is making a bet about its own business model. The bet is that the work moving from billable-human to agent does not shrink the firm; it lets the firm chase a bigger number. PwC named the number: $2 trillion in enterprise technical debt, the backlog of unmodernized systems no consultancy could ever staff its way through ([SiliconAngle](https://siliconangle.com/2026/05/14/pwc-expands-anthropic-alliance-will-train-30000-staff-claude/)).

The proof points are already in production, which is the part that separates this from a memorandum of understanding. Insurance underwriting compressed from 10 weeks to 10 days. A stalled HR transformation restarted with a working prototype in one week and a full application live in under two months. Incident response cut from hours to minutes through agentic vulnerability operations. Clients are reporting delivery improvements of up to 70% ([SiliconAngle](https://siliconangle.com/2026/05/14/pwc-expands-anthropic-alliance-will-train-30000-staff-claude/)). These are not Anthropic's benchmarks. They are PwC's client outcomes, which is exactly the point of the connector model: the lab does not have to prove Claude works in insurance, because the partner already did, on the partner's own clients, with the partner's name on the result.

Set it against the firm Anthropic stood up two weeks ago with Blackstone, Hellman & Friedman, and Goldman Sachs, the standalone enterprise AI-services company built to embed engineers inside mid-sized businesses and redesign their workflows around agents. That was Anthropic building a consulting arm. The PwC deal is Anthropic renting one. Two opposite-looking moves, one logic: the deployment bottleneck, not the model, is the product, and you reach it either by building the deployment muscle or by borrowing the firm that already has it. This week Anthropic borrowed.

The rollout is U.S.-first before extending to PwC's full global workforce ([SiliconAngle](https://siliconangle.com/2026/05/14/pwc-expands-anthropic-alliance-will-train-30000-staff-claude/)). What the reader running an agentic practice should watch is not the 30,000 number. It is whether a Big Four firm retooling its delivery model around Claude becomes the reference customer that drags every other consultancy into the same posture, because once one of them can deliver at a 70% improvement, the rest are negotiating from behind.

---

## By the Numbers

The week measured in customers, dollars, and version bumps.

- **44%**: share of U.S. GDP Anthropic frames as the Claude for Small Business audience, alongside roughly half the private-sector workforce ([Anthropic](https://www.anthropic.com/news/claude-for-small-business)).
- **7**: software surfaces the SMB connector package drops into out of the box (QuickBooks, PayPal, HubSpot, Canva, DocuSign, Google Workspace, Microsoft 365) ([Anthropic](https://www.anthropic.com/news/claude-for-small-business)).
- **10**: cities on the free half-day workshop tour, opening May 14 in Chicago ([Anthropic](https://www.anthropic.com/news/claude-for-small-business)).
- **3**: CDFIs seeded with Claude credits (Accion Opportunity Fund, Community Reinvestment Fund USA, Pacific Community Ventures) ([Anthropic](https://www.anthropic.com/news/claude-for-small-business)).
- **$200M**: Anthropic and Gates Foundation commitment in grant funding, Claude credits, and technical support over four years ([Gates Foundation](https://www.gatesfoundation.org/ideas/media-center/press-releases/2026/05/ai-anthropic-partnership)).
- **4 years**: duration of the Gates Foundation partnership ([Gates Foundation](https://www.gatesfoundation.org/ideas/media-center/press-releases/2026/05/ai-anthropic-partnership)).
- **4.6 billion**: people who lack access to essential health services, per the Foundation's framing ([Gates Foundation](https://www.gatesfoundation.org/ideas/media-center/press-releases/2026/05/ai-anthropic-partnership)).
- **~2 billion**: people whose incomes depend on the smallholder farming the agriculture arm targets ([Gates Foundation](https://www.gatesfoundation.org/ideas/media-center/press-releases/2026/05/ai-anthropic-partnership)).
- **3**: opening disease targets for the health work (polio, HPV, eclampsia) ([Gates Foundation](https://www.gatesfoundation.org/ideas/media-center/press-releases/2026/05/ai-anthropic-partnership)).
- **30,000**: PwC U.S. professionals being trained on Claude ([SiliconAngle](https://siliconangle.com/2026/05/14/pwc-expands-anthropic-alliance-will-train-30000-staff-claude/)).
- **364,000**: PwC's global workforce the rollout extends to, across 136 countries ([SiliconAngle](https://siliconangle.com/2026/05/14/pwc-expands-anthropic-alliance-will-train-30000-staff-claude/)).
- **10 weeks to 10 days**: PwC insurance-underwriting timeline under Claude ([SiliconAngle](https://siliconangle.com/2026/05/14/pwc-expands-anthropic-alliance-will-train-30000-staff-claude/)).
- **up to 70%**: delivery improvement PwC clients report ([SiliconAngle](https://siliconangle.com/2026/05/14/pwc-expands-anthropic-alliance-will-train-30000-staff-claude/)).
- **$2 trillion**: enterprise technical debt PwC names as the target ([SiliconAngle](https://siliconangle.com/2026/05/14/pwc-expands-anthropic-alliance-will-train-30000-staff-claude/)).
- **60 seconds**: the bogus cap `MCP_TOOL_TIMEOUT` was silently enforcing on remote MCP tool calls until v2.1.142 fixed it ([release notes](https://github.com/anthropics/claude-code/releases)).

---

## Also Shipped

### Agent View turns the CLI into a dashboard

On May 11, Claude Code v2.1.139 shipped Agent View as a research preview. Run `claude agents` from any terminal and you get a single list of every Claude Code session, organized by state: running, blocked on you, or done ([release notes](https://github.com/anthropics/claude-code/releases)). The mechanism matters more than the menu. Before this, running multiple sessions meant context-switching blind, with no unified picture of what was working, what was waiting on you, and what had quietly finished. The same build added `/goal`, a command that sets a completion condition and lets Claude work across turns until it's met in interactive, `-p`, and Remote Control modes, plus a `continueOnBlock` hook for PostToolUse that gives operators finer control over automated runs ([release notes](https://github.com/anthropics/claude-code/releases)). The blast radius is anyone running more than one agent at a time, which by now is anyone serious. The direction is consistent with the Code with Claude orchestration push from two weeks ago: the unit of work is a fleet, and the CLI keeps growing the control plane to manage it. The move tonight: run `claude agents` and stop alt-tabbing between terminals.

### Both SDKs open an AWS lane

Also on May 11, both SDKs added an AWS client for Claude Platform on AWS: anthropic-sdk-python v0.101.0 and anthropic-sdk-typescript aws-sdk v0.3.0, with the TypeScript client mirroring the Python feature so both ecosystems get the same AWS compute lane ([anthropic-sdk-python](https://github.com/anthropics/anthropic-sdk-python/releases), [anthropic-sdk-typescript](https://github.com/anthropics/anthropic-sdk-typescript/releases)). This is quiet plumbing, but it's the kind that follows a compute deal. Last week Anthropic was buying capacity by the data center; this week it's wiring the doors that reach it, and Claude Platform on AWS general availability was confirmed the same day ([release notes](https://github.com/anthropics/claude-code/releases)). The pattern is the connector model pointed inward: even Anthropic's own infrastructure story is about meeting builders where their compute already lives rather than forcing them onto a single lane. If you're authenticating through AWS, upgrade the SDK and use the native client instead of hand-rolling the integration.

### Fast mode gets the better brain

Claude Code v2.1.142 (May 14) bumped Fast mode's default model from Opus 4.6 to Opus 4.7 ([release notes](https://github.com/anthropics/claude-code/releases)). The fast lane now runs on the flagship, which is a real concession: the cheap-and-quick tier is no longer the dumb tier. The same build added a fleet of `claude agents` flags for configuring dispatched background sessions (`--add-dir`, `--settings`, `--mcp-config`, `--plugin-dir`, `--permission-mode`, `--model`, `--effort`, `--dangerously-skip-permissions`), turning the new Agent View from a dashboard into a launchpad ([release notes](https://github.com/anthropics/claude-code/releases)). And it fixed a quiet but real bug: `MCP_TOOL_TIMEOUT` had been capping remote HTTP and SSE MCP tool calls at 60 seconds regardless of the configured value ([release notes](https://github.com/anthropics/claude-code/releases)). If you run remote MCP servers and have been blaming your own config for tools that died at the one-minute mark, this was the culprit. Set `CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE=1` to pin Fast mode back to 4.6 if the speed-for-quality trade isn't worth it to you.

### The cache-diagnostics drop, in both flavors

On May 13, anthropic-sdk-python v0.102.0 and anthropic-sdk-typescript v0.96.0 added `BetaManagedAgentsSearchResultBlock` types and support for the cache diagnostics beta ([anthropic-sdk-python](https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.102.0), [anthropic-sdk-typescript](https://github.com/anthropics/anthropic-sdk-typescript/releases/tag/sdk-v0.96.0)). The Managed Agents surface that powered Code with Claude two weeks ago keeps accreting in the builder libraries; search-result blocks now have a typed home, which is what it looks like when a feature graduates from announcement to API. The builder layer moving in lockstep with the product is how you tell a platform from a demo. For anyone profiling token spend on long agent runs, the cache diagnostics beta is the new lever worth wiring in.

### Plugin dependency enforcement closes a footgun

On May 15, Claude Code v2.1.143 added plugin dependency enforcement: `claude plugin disable` now refuses when another enabled plugin depends on the target and prints a copy-pasteable disable-chain hint, while `claude plugin enable` force-enables transitive dependencies ([release notes](https://github.com/anthropics/claude-code/releases)). The mechanism is small and the blast radius is anyone who has ever broken a plugin stack by disabling the one thing three other plugins quietly needed. The same build added projected per-turn and per-invocation token estimates to the `/plugin` marketplace browse pane, a `worktree.bgIsolation: "none"` setting for repos where worktrees are impractical, and made background sessions preserve model and effort level after waking from idle ([release notes](https://github.com/anthropics/claude-code/releases)). The theme across the week's Claude Code builds is unglamorous and consistent: the agent platform is hardening its plumbing, not chasing features. Update and let the dependency graph stop you from shooting your own foot.

---

## Quiet on the Wire

No new model again, and the loudest thing that didn't ship is the round. The $50 billion fundraise targeting an $880 to $900 billion valuation has been in motion since Bloomberg and TechCrunch reported preemptive offers on April 29 ([TechCrunch](https://techcrunch.com/2026/04/30/anthropic-potential-900b-valuation-round-could-happen-within-two-weeks/)), with a board decision expected sometime in May. As of this window, Anthropic had not publicly confirmed a close. And the back wall stayed dark all week: docs.anthropic.com returned a docs error on every direct fetch, so API, Apps, and system-prompt release notes could not be read, which means the absence of news there is the fetch failing, not the lab going quiet. Absence of evidence, not evidence of absence.

---

## Term of the Issue

# The Connector Model

**Connector model** *noun*

The go-to-market shape where the AI lab ships only the reasoning layer and borrows the integration surface from a partner already embedded with the customer. Anthropic provides the brain; QuickBooks, the Gates Foundation, or PwC provides the doors, the data, and the last mile. The lab never builds the integrations and never owns the relationship. It rents reach instead of building it. The trade is deliberate: it gives up the system of record to keep shipping the intelligence the systems of record call.

**First observable** 2026-05-13, the week Claude landed in small business, global health, and a Big Four firm through three partners and zero new products, all wired the same way (see the Lead and the PwC Feature above).

**Usage** *"They didn't build the QuickBooks integration. That's the connector model: the tell is they never do."*

---

## The Close

The week after Anthropic ran out of compute and bought a continent of it, the lab had every reason to brag about power. It talked about reach instead. Claude for Small Business, the Gates Foundation, PwC: three rooms, three audiences with nothing in common, and underneath each one the same wiring. Anthropic brought the brain. Someone else brought the building. The model that would have headlined any other week stayed in the drawer, and the only thing that moved was where Claude could already be found.

No new model.
Three partners. One mechanic.
The lab stopped shipping products and started renting doors.

---

## C. Claude Code

*6 entries in window.*

#### 2026-05-15 — Claude Code v2.1.143 ([release](https://github.com/anthropics/claude-code/releases))
`[CODE]`

Plugin dependency enforcement: `claude plugin disable` now refuses when another enabled plugin depends on the target (and prints a copy-pasteable disable-chain hint); `claude plugin enable` force-enables transitive dependencies. Projected context cost (per-turn and per-invocation token estimates) added to the `/plugin` marketplace browse pane. New `worktree.bgIsolation: "none"` setting for repos where worktrees are impractical. PowerShell tool now passes `-ExecutionPolicy Bypass`. Background sessions preserve model and effort level after waking from idle.

**How to use:** `claude update` or reinstall.

#### 2026-05-14 — Claude Code v2.1.142 ([release](https://github.com/anthropics/claude-code/releases))
`[CODE]`

Fast mode now defaults to Opus 4.7 (was Opus 4.6). New `claude agents` flags for configuring dispatched background sessions: `--add-dir`, `--settings`, `--mcp-config`, `--plugin-dir`, `--permission-mode`, `--model`, `--effort`, `--dangerously-skip-permissions`. Plugins with a root-level `SKILL.md` and no `skills/` subdirectory are now auto-surfaced as a skill. `/plugin` details pane and `claude plugin details` show LSP servers a plugin provides. `/web-setup` warns before replacing an existing GitHub App connection. Fixes: `MCP_TOOL_TIMEOUT` now correctly raises the per-request fetch timeout for remote HTTP and SSE MCP servers (was capped at 60 seconds regardless of config); background sessions not recognizing pre-existing git worktrees; background sessions disappearing and daemon reconnect failing after macOS sleep/wake.

**How to use:** `claude update` or reinstall. Set `CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE=1` to pin Fast mode back to Opus 4.6.

#### 2026-05-13 — Claude Code v2.1.141 ([release](https://github.com/anthropics/claude-code/releases))
`[CODE]`

Agent View (Research Preview) shows all Claude Code sessions in a single list: running, blocked on you, or done. `/goal` sets a completion condition and Claude keeps working across turns until it is met. `/scroll-speed` tunes mouse wheel speed with live preview. `claude plugin details <name>` shows a plugin's component inventory and projected per-session token cost. Auto-mode permission dialog now explains when a `permissions.ask` rule caused the prompt. Rewind menu gains "Summarize up to here." Background agents via `/bg` preserve the current permission mode. Spinner goes amber after 10 seconds of long thinking. Plus reliability fixes across background side-queries, daemon status, the agent dashboard, permission prompts, markdown tables, and editor integrations.

**How to use:** `claude update` or reinstall. `/goal <condition>` starts a persistent multi-turn run.

#### 2026-05-12 — Claude Code v2.1.140 ([release](https://github.com/anthropics/claude-code/releases))
`[CODE]`

Agent tool `subagent_type` matching now accepts case- and separator-insensitive values. Updated agent color palette. Fixes: `/goal` hanging silently when `disableAllHooks` or `allowManagedHooksOnly` is set; settings hot-reload regression for symlinked files; `claude --bg` connection drops; background service startup failures on machines with enterprise endpoint security; event-loop stalls on Windows with missing executables; `Read` tool validation for padded offset values.

**How to use:** `claude update` or reinstall. No config changes required.

#### 2026-05-11 — Claude Code v2.1.139 ([release](https://github.com/anthropics/claude-code/releases))
`[CODE]`

Agent View (research preview) adds `claude agents`, a single-list view of all Claude Code sessions (running, blocked on you, done). New `/goal` command sets a completion condition and Claude works across turns until it is met, in interactive, `-p`, and Remote Control modes. `/scroll-speed` tunes scroll speed with live preview. `claude plugin details <name>` shows plugin component inventory and projected per-session token cost. Transcript navigation: `?` for shortcuts, `{`/`}` to jump between user prompts, `v` to toggle the shortcut panel. Hook improvements: `args: string[]` exec-form field for direct command spawning without a shell; `continueOnBlock` config for PostToolUse. MCP: stdio servers now receive `CLAUDE_PROJECT_DIR`; `/mcp Reconnect` picks up `.mcp.json` edits without restart. Remote Control, `/schedule`, and claude.ai MCP connectors disabled when `ANTHROPIC_API_KEY` is set.

**How to use:** `claude update` or reinstall. Then run `claude agents` to open Agent View.

#### 2026-05-09 — Claude Code v2.1.138 ([CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md))
`[CODE]`

Internal fixes. No user-facing changes documented.

**How to use:** `claude update` or reinstall.

## F. Agent SDKs

*5 entries in window.*

#### 2026-05-13 — anthropic-sdk-python v0.102.0 ([GitHub](https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.102.0))
`[SDK-PY]`

Adds `BetaManagedAgentsSearchResultBlock` types and support for the cache diagnostics beta. Internal: eager validation for Pydantic iterators. API spec updates.

**How to use:** `pip install anthropic==0.102.0`

#### 2026-05-13 — anthropic-sdk-typescript v0.96.0 ([GitHub](https://github.com/anthropics/anthropic-sdk-typescript/releases/tag/sdk-v0.96.0))
`[SDK-TS]`

Adds `BetaManagedAgentsSearchResultBlock` types and cache diagnostics beta support, matching the Python drop. Bug fix: ensures only `zod/v4` types are used.

**How to use:** `npm install @anthropic-ai/sdk@0.96.0`

#### 2026-05-11 — anthropic-sdk-python v0.101.0 ([GitHub](https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.101.0))
`[SDK-PY]`

Adds an AWS client for Claude Platform on AWS. Bug fix: corrected a missing f-string prefix in a file type error message.

**How to use:** `pip install --upgrade anthropic`

#### 2026-05-11 — anthropic-sdk-typescript aws-sdk v0.3.0 ([GitHub](https://github.com/anthropics/anthropic-sdk-typescript/releases/tag/aws-sdk-v0.3.0))
`[SDK-TS]`

Adds an AWS client for Claude Platform on AWS. Mirrors the Python SDK feature, giving TypeScript callers the same AWS compute lane.

**How to use:** `npm install @anthropic-ai/sdk@latest`

#### 2026-05-11 — anthropic-sdk-typescript v0.95.2 ([GitHub](https://github.com/anthropics/anthropic-sdk-typescript/releases/tag/sdk-v0.95.2))
`[SDK-TS]`

Patch release. Full changelog in the GitHub comparison.

**How to use:** `npm install @anthropic-ai/sdk@latest`

## G. Partnerships and Policy

*4 entries in window.*

#### 2026-05-14 — PwC expands Anthropic alliance, 30,000 staff on Claude ([SiliconAngle](https://siliconangle.com/2026/05/14/pwc-expands-anthropic-alliance-will-train-30000-staff-claude/))
`[NEWS]`

PwC and Anthropic announced an expanded alliance putting Claude Code and Claude Cowork in front of PwC's U.S. workforce, training 30,000 professionals on Anthropic models. The deal establishes a joint Center of Excellence and a Claude-native finance group inside PwC's Office of the CFO practice. Deployments already in production: insurance underwriting from 10 weeks to 10 days, a stalled HR transformation restarted with a working prototype in one week, incident response cut from hours to minutes. Clients report delivery improvements of up to 70%. Stated target: $2 trillion in enterprise technical debt. Rollout is U.S.-first before extending to PwC's 364,000-person global workforce in 136 countries. ([PwC](https://www.pwc.com/us/en/about-us/newsroom/press-releases/anthropic-pwc-expand-alliance-agentic-enterprise.html), [Anthropic](https://www.anthropic.com/news/pwc-expanded-partnership))

#### 2026-05-13 — Anthropic and the Gates Foundation, $200M partnership ([Anthropic](https://www.anthropic.com/news/gates-foundation-partnership))
`[NEWS]`

Anthropic and the Gates Foundation committed $200 million in grant funding, Claude credits, and technical support for global health, life sciences, education, and economic mobility programs over four years. Health work begins with polio, HPV, and eclampsia research in low- and middle-income countries; around 4.6 billion people lack access to essential health services per the Foundation's framing. Education targets K-12 tutoring in the U.S. and foundational literacy and numeracy programs in sub-Saharan Africa and India. Agriculture focuses on smallholder farming productivity for nearly two billion people. African-language datasets will be collected, labeled, and released as public goods. ([Gates Foundation](https://www.gatesfoundation.org/ideas/media-center/press-releases/2026/05/ai-anthropic-partnership))

#### 2026-05-13 — Claude for Small Business ([Anthropic](https://www.anthropic.com/news/claude-for-small-business))
`[NEWS]`

A toggle-install package dropping Claude-powered connectors and agentic workflows into software small businesses already run: Intuit QuickBooks, PayPal, HubSpot, Canva, DocuSign, Google Workspace, Microsoft 365. Covered workloads: payroll planning, month-end close, cash-flow forecasting, invoice chasing, campaign creation. No extra cost beyond existing Claude licenses. Anthropic frames the audience as 44% of U.S. GDP and roughly half the private-sector workforce. A 10-city free half-day workshop tour started May 14 in Chicago. Anthropic is also backing a Workday Foundation solopreneurship accelerator and partnering with three CDFIs (Accion Opportunity Fund, Community Reinvestment Fund USA, Pacific Community Ventures) with Claude credits. Reported across TechCrunch and The Register.

#### 2026-05-11 — Claude Platform on AWS, general availability ([release](https://github.com/anthropics/anthropic-sdk-python/releases))
`[NEWS]`

Claude Platform on AWS reached general availability, confirmed May 11, with AWS clients shipping the same day in both the Python and TypeScript SDKs.

**Why it matters:** Last week's compute deals bought the capacity; the AWS lane is one of the doors that reaches it.
