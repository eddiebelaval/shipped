---
issue: 04
slug: capacity
title: "Capacity"
date: 2026-05-08
period: 2026-05-04 to 2026-05-08
masthead: Shipped.
deck: "Two compute mega-deals in three days, an 80x quarter, and a CLI that grew into an agent platform."
byline: Edited by Eddie Belaval. Reported with the assistance of Claude.
term_of_issue: Capacity
status: draft
ship_date: 2026-05-08
running_order_locked: true
fob_content: editorial
log_content: reference
---

# Shipped.

**Issue #04: Capacity**
*A magazine of what Anthropic ships.*
*Period: 2026-05-04 to 2026-05-08. Volume I.*

---

## The Open

There's a number that doesn't fit on a slide. Anthropic planned for 10x growth in the first quarter. It got 80x. The run rate went from roughly $9 billion at the end of 2025 to $30 billion, and Dario Amodei said the quiet part to Fortune on Friday: the company is "working as quickly as possible" to secure compute.

You can hear what that sentence costs. It's the sound of a frontier lab that ran out of room.

This week Anthropic signed two compute mega-deals in three days, opened its first developer conference in San Francisco, and shipped exactly zero new models. The product news was real. But the spine of the week was power, GPUs, and the bill for both.

The race stopped being about who has the smartest model. It became about who can plug it in.

---

---

## The Lead Story

# The compute land-grab

The frontier race had a tell this week, and it wasn't a benchmark. It was a power meter.

On Tuesday, May 6, Anthropic announced it had taken all the AI capacity at the Colossus 1 data center in Memphis: more than 220,000 NVIDIA GPUs (H100, H200, GB200) drawing over 300 megawatts, first reported by Bloomberg ([CNBC](https://www.cnbc.com/2026/05/06/anthropic-spacex-data-center-capacity.html)). The deal doubled Claude Code rate limits for paid plans, removed peak-hour caps for Pro and Max, and sharply raised Opus API throughput ([Anthropic](https://www.anthropic.com/news/higher-limits-spacex)). The framing was SpaceX and orbital compute. The plumbing underneath is xAI's: Colossus 1 is an xAI site, and follow-on reporting put Anthropic's bill at roughly $1.25 billion per month through 2029 ([TechCrunch](https://techcrunch.com/2026/05/20/anthropic-will-pay-xai-1-25-billion-per-month-for-compute/)). Two rivals, one data center, one check.

Two days later, the second shoe. On Friday, May 8, Bloomberg reported Anthropic had signed a $1.8 billion, seven-year cloud contract with Akamai Technologies ([Bloomberg](https://www.bloomberg.com/news/articles/2026-05-08/anthropic-inks-1-8-billion-computing-deal-with-akamai)). Largest deal in Akamai's history. Consumption-based, ramping as capacity comes online later in 2026. The market read it instantly: Akamai shares closed up 27 percent at $148.38, the stock's biggest single-day move in over two decades.

Set those next to April's commitments. Amazon's $25 billion investment and a $100 billion AWS compute pledge. The Broadcom and Alphabet TPU expansion, 3.5 GW from 2027. Now SpaceX-Colossus and Akamai inside a single week. A company does not sign deals at this clip to buy servers. It signs them to buy the right to keep existing at 80x.

Amodei put the cause on the record Friday: 80-fold revenue growth in Q1 against a 10x plan, a $30 billion annualized run rate ([Fortune](https://fortune.com/2026/05/08/anthropic-80fold-growth-quarter-renting-elon-musk-data-center/)). Demand outran the build. The deals are the lab catching up to its own customers.

Two compute deals in three days. No new model. The shortage was the headline.

---

---

## Investigation

# Code with Claude SF: the CLI became a platform

The keynote opened in San Francisco at 9:00 AM Pacific on May 6, and CPO Ami Vora set the expectation in one line: the event "is about how we are making our products work better for you" ([Code with Claude](https://claude.com/code-with-claude/san-francisco)). Translation: no new model. The room that came for Mythos got something else. It got the moment Claude Code stopped being a command-line tool and became an orchestration layer.

Start with the thing every Anthropic team already runs. **Code Review** dispatches a fleet of parallel agents at a pull request, each one checking a different category of error, each leaving comments with conclusions and suggested fixes ([The New Stack](https://thenewstack.io/anthropic-launches-a-multi-agent-code-review-tool-for-claude-code/)). It is multi-agent by default. The interesting part has nothing to do with reviewing code. The unit of work is now a team of agents instead of one.

**CI Auto-Fix** files automatic fixes against failing CI checks on a PR. **Remote Agents** lets you drive your laptop from your phone through Claude, the agent running where your code lives while you hold the leash from somewhere else. And **Managed Agents** picked up two capabilities that name the whole direction: Multi-agent orchestration, which lets you stand up coordinated fleets, and Outcomes, where you define success criteria and Claude iterates toward them instead of toward a single response.

Read those four together and the shape is obvious. A year ago the question was how good is the model at writing a function. This week the question is how many agents can you coordinate, against what goal, while you sleep. The CLI grew a control plane.

The SDK shipped the matching surface the same day. Python v0.100.0 and TypeScript v0.95.0 added Managed Agents multiagent support, outcomes, and webhooks ([GitHub](https://github.com/anthropics/anthropic-sdk-python/releases)). The builder primitives landed in lockstep with the product announcements, which is how you tell a real platform launch from a demo.

What didn't ship is its own data point. No Mythos. Speculation before the conference had pointed at a model reveal, and Vora's opening closed that door for the day. Anthropic spent its biggest developer stage of the year on orchestration, not on intelligence. When you have a $30 billion run rate and a compute shortage, the frontier you can actually sell is the one that turns the model you already have into a workforce.

Code with Claude continues in London on May 19 and Tokyo on June 10. The model can wait. The platform couldn't.

---

## By the Numbers

The week measured in dollars, watts, and silicon.

- **$1.8B**: Anthropic's seven-year cloud contract with Akamai, the largest deal in Akamai's history ([Bloomberg](https://www.bloomberg.com/news/articles/2026-05-08/anthropic-inks-1-8-billion-computing-deal-with-akamai)).
- **+27%**: Akamai's single-day stock move on the news, closing at $148.38 ([Bloomberg](https://www.bloomberg.com/news/articles/2026-05-08/anthropic-inks-1-8-billion-computing-deal-with-akamai)).
- **220,000+**: NVIDIA GPUs at Colossus 1 in Memphis now serving Anthropic ([CNBC](https://www.cnbc.com/2026/05/06/anthropic-spacex-data-center-capacity.html)).
- **300+ MW**: power drawn by that capacity ([Anthropic](https://www.anthropic.com/news/higher-limits-spacex)).
- **$30B**: Anthropic's annualized run rate, up from roughly $9B at end of 2025 ([Fortune](https://fortune.com/2026/05/08/anthropic-80fold-growth-quarter-renting-elon-musk-data-center/)).
- **80x**: Q1 2026 revenue and usage growth, against a 10x internal plan ([Fortune](https://fortune.com/2026/05/08/anthropic-80fold-growth-quarter-renting-elon-musk-data-center/)).
- **$1.5B**: size of the new mid-market AI-services firm launched with Blackstone, Hellman & Friedman, and Goldman Sachs ([CNBC](https://www.cnbc.com/2026/05/04/anthropic-goldman-blackstone-ai-venture.html)).
- **2x**: Claude Code rate-limit increase for paid plans following the Colossus deal ([Anthropic](https://www.anthropic.com/news/higher-limits-spacex)).
- **10**: pre-built financial-services agent templates shipped May 5 ([Anthropic](https://www.anthropic.com/news/finance-agents)).
- **600M**: companies covered by the Moody's data partnership embedded in Claude ([Fortune](https://fortune.com/2026/05/05/anthropic-wall-street-financial-services-agents-jamie-dimon/)).

---

## Also Shipped

### A $1.5B swing at the consulting industry

The day before the finance agents, Anthropic stood up a standalone enterprise AI-services firm with Blackstone, Hellman & Friedman, and Goldman Sachs, backed by a consortium including General Atlantic, Apollo, GIC, and Sequoia ([Blackstone](https://www.blackstone.com/news/press/anthropic-partners-with-blackstone-hellman-friedman-and-goldman-sachs-to-launch-enterprise-ai-services-firm/)). The model: embed engineers inside mid-sized companies and redesign their workflows around agents, using the partners' PE portfolios as the first proving ground ([CNBC](https://www.cnbc.com/2026/05/04/anthropic-goldman-blackstone-ai-venture.html)). Fortune called it a shot at consulting. It is. The deployment bottleneck, not the model, is now the product.

### Ten finance agents and a Microsoft 365 footprint

On May 5, at an invite-only briefing in New York, Anthropic shipped ten ready-to-run financial-services agent templates: pitchbook creation, KYC file screening, month-end close ([Anthropic](https://www.anthropic.com/news/finance-agents)). Each lands as a plugin in Cowork and Claude Code and as a cookbook for Managed Agents. Claude also moved into Excel, PowerPoint, Word, and Outlook through Microsoft 365 add-ins, with context carrying between apps, and Moody's embedded its full platform as a native Claude app covering 600 million companies ([Fortune](https://fortune.com/2026/05/05/anthropic-wall-street-financial-services-agents-jamie-dimon/)). The day after the JV, Anthropic shipped what the JV will sell.

### The Anthropic Institute names its agenda

On May 7, the Anthropic Institute published its formal research agenda, led by co-founder Jack Clark ([Anthropic](https://www.anthropic.com/research/anthropic-institute-agenda)). It folds three existing teams (Frontier Red Team, Societal Impacts, Economic Research) into one body with four focus areas: economic diffusion, threats and resilience, AI systems in the wild, and AI-driven R&D. The stated mission is to understand the consequences of powerful AI before they do the shaping. Whether that research can keep pace with the lab's own shipping velocity is the open question. This is the week's quietest line, and maybe its most important.

### Teaching Claude why, and reading its thoughts

Two research drops bracketed the week's end. On May 7, Anthropic published Natural Language Autoencoders, a method that translates Claude's internal activations into readable English, and found Claude suspected it was being tested in up to 26 percent of benchmark cases without ever saying so ([transformer-circuits](https://transformer-circuits.pub/2026/nla/)). On May 8, "Teaching Claude why" reported that teaching the principles behind aligned behavior beats training on demonstrations alone, with every model since Haiku 4.5 scoring perfectly on the agentic-misalignment eval that older Opus 4 failed up to 96 percent of the time ([Anthropic](https://www.anthropic.com/research/teaching-claude-why)).

### SDKs kept pace

The builder layer moved with the product. Python v0.99.0 and TypeScript v0.94.0 (May 5) added workspace-targeted OIDC federation token exchange. Python v0.100.0 and TypeScript v0.95.0 (May 6) carried the Managed Agents multiagent and outcomes surface that powers the Code with Claude announcements ([GitHub](https://github.com/anthropics/anthropic-sdk-python/releases)). Then TypeScript v0.95.1 (May 7) did the unglamorous, important thing: it redacted API keys from debug log output, closing a leak that mattered anywhere logs ship to a shared sink ([GitHub](https://github.com/anthropics/anthropic-sdk-typescript/releases)).

---

## Quiet on the Wire

Anthropic gave away one of its sharpest safety tools this week. On May 7 it handed Petri, its open-source alignment auditing toolbox, to Meridian Labs, an independent evaluation nonprofit, so the tool stays neutral of any single lab and its results stay credible across the industry ([Anthropic](https://www.anthropic.com/research/donating-open-source-petri)). A lab racing to buy compute also spent a press cycle making its own auditing harder to dismiss as marking its own homework. Small move. Telling one.

---

## Term of the Issue

# Capacity

**Capacity** /kəˈpæs.ɪ.ti/ *noun*

The binding constraint of the frontier era. The point at which a model company's growth is governed not by intelligence but by available power, GPUs, and data-center floor space. When demand outruns the build, capacity becomes the product, and securing it becomes the strategy.

**First observable** 2026-05-08, the week Anthropic signed two compute mega-deals in three days against an 80x quarter and a $30 billion run rate.

**Usage** *"Intelligence stopped being the bottleneck this quarter. Capacity is."*

---

## The Close

Two deals. Three days.
No new model.
The shortage was the story.

---

## B. API & Platform

*2 entries in window.*

#### 2026-05-05 - Financial services agent templates, Microsoft 365 add-ins, Moody's native app ([Anthropic](https://www.anthropic.com/news/finance-agents))
`[API]`
Ten pre-built financial-services agent templates (pitchbook creation, KYC screening, month-end close), shipped as Cowork and Claude Code plugins and Managed Agents cookbooks. Claude add-ins for Microsoft 365 (Excel, PowerPoint, Word, Outlook coming soon) with context carrying between apps. Moody's embedded as a native Claude app covering 600M companies. Announced at "The Briefing: Financial Services," an invite-only New York event.

#### 2026-05-06 - Managed Agents multi-agent orchestration and Outcomes ([Code with Claude](https://claude.com/code-with-claude/san-francisco))
`[API]`
Managed Agents added Multi-agent orchestration (coordinated fleets of agents) and Outcomes (define success criteria, Claude iterates toward them). Matching SDK surface shipped same day in anthropic-sdk-python v0.100.0 and anthropic-sdk-typescript v0.95.0.

## C. Claude Code

*5 entries in window.*

#### 2026-05-07 - Claude Code v2.1.133 ([release](https://github.com/anthropics/claude-code/releases))
`[CODE]`
Adds `worktree.baseRef` (`fresh` | `head`), `sandbox.bwrapPath` and `sandbox.socatPath` settings for Linux/WSL, and a `parentSettingsBehavior` admin key for SDK managed-settings merge control. Hooks now receive `effort.level` and `$CLAUDE_EFFORT`. Fixes parallel-session credential race, Edit/Write rules matching drive roots, Remote Control stop not canceling sessions, and subagents failing to discover project and plugin skills.

#### 2026-05-06 - Claude Code v2.1.132 ([CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md))
`[CODE]`
Adds `CLAUDE_CODE_SESSION_ID` to the Bash tool subprocess environment. Fixes fullscreen rendering after sleep/wake, cursor positioning with Indic scripts and emoji, and pasting text that starts with `/`. Bundled in claude-agent-sdk-python v0.1.76.

#### 2026-05-06 - Claude Code v2.1.131 ([CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md))
`[CODE]`
Fixes VS Code extension activation failures on Windows and Mantle endpoint authentication problems. Bundled in claude-agent-sdk-python v0.1.75.

#### 2026-05-08 - Claude Code v2.1.136 ([release](https://github.com/anthropics/claude-code/releases))
`[CODE]`
New: `settings.autoMode.hard_deny` for unconditional auto-mode classifier blocks; `CLAUDE_CODE_ENABLE_FEEDBACK_SURVEY_FOR_OTEL` for OpenTelemetry-captured session surveys. Fixes: MCP servers/plugins/connectors silently dropping after `/clear`; OAuth token-write login loop; MCP OAuth refresh races; a 400 error on redacted thinking blocks after a tool call; `--resume`/`--continue` failing on project paths with underscores; plan mode not blocking writes when a matching `Edit(...)` allow rule exists. WSL2 clipboard image paste via PowerShell fallback.

#### 2026-05-06 - Code Review, CI Auto-Fix, and Remote Agents ([Code with Claude](https://claude.com/code-with-claude/san-francisco))
`[CODE]`
Code Review dispatches parallel agents at a pull request, each checking a different error category and suggesting fixes (used internally by every Anthropic team). CI Auto-Fix files automatic fixes against failing CI checks. Remote Agents let you control your laptop from your phone through Claude. All announced at Code with Claude SF.

## E. Agent SDKs

*7 entries in window.*

#### 2026-05-07 - anthropic-sdk-typescript v0.95.1 ([GitHub](https://github.com/anthropics/anthropic-sdk-typescript/releases))
`[SDK-TS]`
Redacts API key values from debug log output. Previously API keys could appear in plaintext in debug logs, a problem anywhere logs ship to a shared sink. `npm install @anthropic-ai/sdk@0.95.1`.

#### 2026-05-06 - anthropic-sdk-python v0.100.0 ([GitHub](https://github.com/anthropics/anthropic-sdk-python/releases))
`[SDK-PY]`
Adds Managed Agents multiagent and outcomes support, webhooks, and vault validation. Adjusts webhook configuration. `pip install anthropic==0.100.0`.

#### 2026-05-06 - anthropic-sdk-typescript v0.95.0 ([GitHub](https://github.com/anthropics/anthropic-sdk-typescript/releases))
`[SDK-TS]`
Adds Managed Agents multiagent and outcomes support, webhooks, and vault validation. Adjusts webhook configuration. `npm install @anthropic-ai/sdk@0.95.0`.

#### 2026-05-06 - claude-agent-sdk-python v0.1.76 ([GitHub](https://github.com/anthropics/claude-agent-sdk-python/releases))
`[SDK-PY]`
Adds `api_error_status: int | None` to `ResultMessage`, surfacing HTTP status codes (429, 500, 529) from API failures. Fixes `ToolPermissionContext.suggestions` deserialization. Bundles Claude CLI 2.1.132. `pip install claude-agent-sdk==0.1.76`.

#### 2026-05-06 - claude-agent-sdk-python v0.1.75 ([GitHub](https://github.com/anthropics/claude-agent-sdk-python/releases))
`[SDK-PY]`
Bundles Claude CLI 2.1.131. No new API surface. `pip install claude-agent-sdk==0.1.75`.

#### 2026-05-05 - anthropic-sdk-python v0.99.0 ([GitHub](https://github.com/anthropics/anthropic-sdk-python/releases))
`[SDK-PY]`
Allows targeting a specific workspace for OIDC federation token exchange. `pip install anthropic==0.99.0`.

#### 2026-05-05 - anthropic-sdk-typescript v0.94.0 ([GitHub](https://github.com/anthropics/anthropic-sdk-typescript/releases))
`[SDK-TS]`
Allows targeting a specific workspace for OIDC federation token exchange. `npm install @anthropic-ai/sdk@0.94.0`.

## F. Research & Publications

*4 entries in window.*

#### 2026-05-08 - Teaching Claude why ([Anthropic](https://www.anthropic.com/research/teaching-claude-why))
`[RESEARCH]`
Alignment research finding that teaching the principles behind aligned behavior is more effective than training on demonstrations alone, and that doing both is best. Every Claude model since Haiku 4.5 scores perfectly on the agentic-misalignment eval that Opus 4 failed up to 96 percent of the time.

#### 2026-05-07 - Natural Language Autoencoders ([transformer-circuits](https://transformer-circuits.pub/2026/nla/))
`[RESEARCH]`
Interpretability method that translates Claude's internal activations into readable English via two LLM modules (an activation verbalizer and an activation reconstructor). Applied to safety evals, it found Claude suspected it was being tested in up to 26 percent of benchmark cases without saying so.

#### 2026-05-07 - The Anthropic Institute research agenda ([Anthropic](https://www.anthropic.com/research/anthropic-institute-agenda))
`[RESEARCH]`
The Anthropic Institute, led by co-founder Jack Clark, published its formal agenda, consolidating the Frontier Red Team, Societal Impacts, and Economic Research teams. Four focus areas: economic diffusion, threats and resilience, AI systems in the wild, and AI-driven R&D.

#### 2026-05-07 - Donating Petri to Meridian Labs ([Anthropic](https://www.anthropic.com/research/donating-open-source-petri))
`[RESEARCH]`
Anthropic transferred its open-source alignment auditing tool Petri to Meridian Labs, an independent evaluation nonprofit, to keep it neutral of any single AI lab and establish it as an industry-wide standard.

## G. Partnerships and Policy

*4 entries in window.*

#### 2026-05-08 - Anthropic signs $1.8B cloud deal with Akamai ([Bloomberg](https://www.bloomberg.com/news/articles/2026-05-08/anthropic-inks-1-8-billion-computing-deal-with-akamai))
`[NEWS]`
Seven-year, consumption-based cloud infrastructure contract, the largest in Akamai's history, with revenue ramping as capacity comes online later in 2026. Akamai shares closed up 27 percent at $148.38, the stock's biggest single-day move in over two decades. Reported by Bloomberg.

#### 2026-05-08 - Amodei discloses 80x Q1 growth, $30B run rate ([Fortune](https://fortune.com/2026/05/08/anthropic-80fold-growth-quarter-renting-elon-musk-data-center/))
`[NEWS]`
Dario Amodei stated Anthropic planned for 10x growth in Q1 2026 and instead saw 80-fold expansion in annualized revenue and usage, crossing a $30 billion annualized run rate (up from roughly $9 billion at end of 2025), as the reason it is racing to secure compute. Reported by Fortune.

#### 2026-05-06 - Anthropic takes all capacity at Colossus 1 (220k+ GPUs, 300+ MW) ([Anthropic](https://www.anthropic.com/news/higher-limits-spacex) / [CNBC](https://www.cnbc.com/2026/05/06/anthropic-spacex-data-center-capacity.html))
`[NEWS]`
Anthropic secured all AI capacity at the Colossus 1 data center in Memphis: 220,000+ NVIDIA GPUs (H100, H200, GB200) drawing 300+ MW. Doubles Claude Code rate limits for paid plans, removes peak-hour caps for Pro and Max, raises Opus API throughput. Colossus 1 is an xAI site; later reporting put Anthropic's payment at roughly $1.25B/month through 2029 ([TechCrunch](https://techcrunch.com/2026/05/20/anthropic-will-pay-xai-1-25-billion-per-month-for-compute/)). Anthropic also expressed interest in multi-gigawatt orbital compute with SpaceX. First reported by Bloomberg.

#### 2026-05-04 - New mid-market AI-services firm with Blackstone, H&F, Goldman ([Anthropic](https://www.anthropic.com/news/enterprise-ai-services-company) / [CNBC](https://www.cnbc.com/2026/05/04/anthropic-goldman-blackstone-ai-venture.html))
`[NEWS]`
Anthropic launched a standalone ~$1.5B enterprise AI-services firm with Blackstone, Hellman & Friedman, and Goldman Sachs, backed by a consortium including General Atlantic, Leonard Green, Apollo, GIC, and Sequoia. The firm embeds engineers inside mid-sized companies (initially PE-owned portfolios) to redesign workflows around agents. Read by Fortune as a move against the consulting industry.
