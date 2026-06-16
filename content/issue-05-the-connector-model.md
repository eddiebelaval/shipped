---
issue: 05
slug: connector-model
title: "The Connector Model"
date: 2026-05-15
period: 2026-05-11 to 2026-05-15
masthead: Shipped.
deck: "No new model. Claude landed in small business, the Gates Foundation, and 30,000 PwC desks the same way every time: reasoning layer in, integration surface borrowed."
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

There's a sentence that shows up three times this week, in three documents that have nothing to do with each other. Small business owners read one version. Gates Foundation grant officers read another. PwC's 30,000 staff got the third. Strip the branding off each and the same line is underneath: Anthropic provides the reasoning layer, the partners carry the integration surface.

That is not a coincidence. It is a strategy with a shape, and once you see the shape you can't unsee it. The week after Anthropic spent itself hoarse buying compute, it stopped talking about power and started talking about reach. No new model. No flagship. Just Claude, walking into rooms it had never been in, on someone else's floor.

---

## The Lead Story

# Claude went everywhere, and built nothing to get there

The headline this week isn't a product. It's a posture.

On May 13, Anthropic shipped Claude for Small Business, and the product decision underneath the announcement is that there is no product. No new interface, no separate app, no extra line item. It's a toggle that drops Claude-powered connectors into the software small businesses already run: QuickBooks, PayPal, HubSpot, Canva, DocuSign, Google Workspace, Microsoft 365. Payroll planning, month-end close, cash-flow forecasting, invoice chasing ([Anthropic](https://www.anthropic.com/news/claude-for-small-business)). Anthropic put a number on the room it's pitching: 44% of U.S. GDP, roughly half the private-sector workforce. A 10-city free workshop tour opened in Chicago on May 14 to close the gap between "we have a chat window" and "Claude is doing work."

The same week, two institutional bets landed that could not be further apart in stakes. On May 13, Anthropic and the Gates Foundation committed $200 million (grant funding, Claude credits, and technical support over four years) to global health, education, and economic mobility in low- and middle-income countries ([Anthropic](https://www.anthropic.com/news/gates-foundation-partnership), [Gates Foundation](https://www.gatesfoundation.org/ideas/media-center/press-releases/2026/05/ai-anthropic-partnership)). The targets are specific, not abstract: polio, HPV, and eclampsia. Around 4.6 billion people lack access to essential health services, per the Foundation's framing, and that's the audience. The day after, PwC expanded its alliance to train 30,000 U.S. professionals on Claude, with deployments already in production: insurance underwriting cut from 10 weeks to 10 days, incident response from hours to minutes ([SiliconAngle](https://siliconangle.com/2026/05/14/pwc-expands-anthropic-alliance-will-train-30000-staff-claude/)).

Read the three together and the mechanic is identical. Anthropic brings the reasoning layer. The partner brings the integration surface: Intuit's APIs, the Gates Foundation's three decades of on-the-ground infrastructure, PwC's client base in 136 countries. Anthropic is not building the SMB connectors itself. It is not building the health pipelines. It rents the last mile every time.

This is the same structure as the enterprise push, scaled across every customer tier at once. The model didn't move this week. The map did.

---

## Also Shipped

### Agent View turns the CLI into a dashboard

On May 11, Claude Code v2.1.139 shipped Agent View as a research preview. Run `claude agents` from any terminal and you get a single list of every Claude Code session: running, blocked on you, or done ([release notes](https://github.com/anthropics/claude-code/releases)). Before this, running multiple sessions meant context-switching blind. The same build added `/goal`, a command that sets a completion condition and lets Claude work across turns until it's met, plus a `continueOnBlock` hook for finer control over automated runs. The direction is consistent: multi-session orchestration, handled natively in the CLI. The command-line tool keeps growing a control plane.

### Both SDKs open an AWS lane

Also on May 11, both SDKs added an AWS client for Claude Platform on AWS: anthropic-sdk-python v0.101.0 and anthropic-sdk-typescript aws-sdk v0.3.0 ([GitHub](https://github.com/anthropics/anthropic-sdk-python/releases)). The TypeScript client mirrors the Python feature, giving both ecosystems the same AWS compute lane. Quiet plumbing, but it's the kind that follows a compute deal. Last week Anthropic was buying the capacity; this week it's wiring the doors to reach it. Platform-on-AWS GA was confirmed the same day.

### Fast mode gets the better brain

Claude Code v2.1.142 (May 14) bumped Fast mode's default model from Opus 4.6 to Opus 4.7 ([release notes](https://github.com/anthropics/claude-code/releases)). The fast lane now runs on the flagship. The same build added a fleet of `claude agents` flags for configuring dispatched background sessions (`--model`, `--effort`, `--permission-mode`, and more), and fixed a quiet but real bug: `MCP_TOOL_TIMEOUT` had been capping remote MCP tool calls at 60 seconds regardless of the configured value. Set `CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE=1` to pin Fast mode back to 4.6 if the speed-for-quality trade isn't worth it to you.

### The cache-diagnostics drop, in both flavors

On May 13, anthropic-sdk-python v0.102.0 and anthropic-sdk-typescript v0.96.0 added `BetaManagedAgentsSearchResultBlock` types and support for the cache diagnostics beta ([GitHub](https://github.com/anthropics/anthropic-sdk-typescript/releases)). The Managed Agents surface that powered Code with Claude two weeks ago keeps accreting in the builder libraries; search-result blocks now have a typed home. The builder layer moving in lockstep with the product is how you tell a platform from a demo.

---

## Quiet on the Wire

No new model again. The $50 billion fundraise targeting an $880 to $900 billion valuation has been in motion since Bloomberg and TechCrunch reported preemptive offers on April 29 ([TechCrunch](https://techcrunch.com/2026/04/30/anthropic-potential-900b-valuation-round-could-happen-within-two-weeks/)), with a board decision expected sometime in May, still unconfirmed as of this window. And docs.anthropic.com returned a docs error on every direct fetch all week, so API, Apps, and system-prompt release notes ran dark. Absence of evidence, not evidence of absence.

---

## Term of the Issue

# The Connector Model

**Connector model** *noun*

The go-to-market shape where the AI lab ships only the reasoning layer and borrows the integration surface from a partner already embedded with the customer. Anthropic provides the brain; QuickBooks, the Gates Foundation, or PwC provides the doors, the data, and the last mile. The lab never builds the integrations and never owns the relationship. It rents reach instead of building it.

**First observable** 2026-05-13, the week Claude landed in small business, global health, and a Big Four firm through three partners and zero new products.

**Usage** *"They didn't build the QuickBooks integration. That's the connector model: the tell is they never do."*

---

## The Close

No new model.
Three partners. One mechanic.
The lab stopped shipping products and started renting doors.

---

## C. Claude Code

*5 entries in window.*

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
