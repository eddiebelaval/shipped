---
issue: 06
slug: the-toolmaker
title: "The Toolmaker"
date: 2026-05-22
period: 2026-05-16 to 2026-05-22
masthead: Shipped.
deck: "Anthropic bought the factory that builds SDKs for OpenAI, Google, and Meta, then announced it would close it."
byline: Edited by Eddie Belaval. Reported with the assistance of Claude.
term_of_issue: The Toolmaker
status: draft
ship_date: 2026-05-22
running_order_locked: true
fob_content: editorial
log_content: reference
---

# Shipped.

**Issue #06: The Toolmaker**
*A magazine of what Anthropic ships.*
*Period: 2026-05-16 to 2026-05-22. Volume I.*

---

## The Open

Monday morning, Anthropic bought a small company most builders had never heard of and every builder had already used. Stainless generated the official SDK for Anthropic's own API. It also generated the Python, TypeScript, Go, Java, Kotlin, and Ruby libraries that OpenAI, Google, Cloudflare, and Meta ship to their developers. One startup quietly built the scaffolding under the whole frontier.

Then Anthropic said it would shut the service down.

No model shipped this week. No flagship. The headline was a $300-million-plus acquisition of a tool nobody talked about, and the decision to switch it off. The rest of the week was Claude Code patching itself in public, version after version, sometimes twice a day. The center of gravity moved from what the model can do to who owns the machinery that builds with it.

---

---

## The Lead Story

# The factory that built everyone's tools

The frontier race had a quiet move this week, and it wasn't a benchmark. It was an acquisition most people couldn't place.

On Monday, May 18, Anthropic announced it had acquired Stainless, the startup that generates production-ready SDKs, CLIs, and MCP servers directly from API specifications ([Anthropic](https://www.anthropic.com/news/anthropic-acquires-stainless)). Founded in 2022 by former Stripe engineer Alex Rattray and backed by Sequoia and Andreessen Horowitz, Stainless sat in a strange place in the toolchain: it generated every official Anthropic SDK since the API's earliest days, and it also generated the libraries OpenAI, Google, Cloudflare, and Meta hand their own developers ([TechCrunch](https://techcrunch.com/2026/05/18/anthropic-has-acquired-the-dev-tools-startup-used-by-openai-google-and-cloudflare/)). Terms weren't disclosed. The Information had reported, before the announcement, that talks valued the company at over $300 million, with part of the consideration potentially in Anthropic equity.

Read the headline and you'd file it as a routine dev-tools tuck-in. Read the second sentence of the press release and the story changes. Anthropic will wind down all hosted Stainless products, the SDK generator included. Existing customers keep the SDKs they've already built, with full rights to modify them. The factory closes. The parts stay where they landed.

That is the move worth naming. Anthropic didn't buy a feature. It bought the machine its rivals quietly relied on to talk to their own customers, and then it pulled the machine off the market. OpenAI and Google won't lose the SDKs they have. They lose the supplier. The next time they regenerate from a spec, they do it without the toolmaker the whole industry had been renting.

It rhymes with the spring's other Anthropic story. Capacity was about owning the compute everyone needs to run. This is about owning the tooling everyone needs to build. Same instinct, smaller check: when the constraint is a dependency you don't control, buy the dependency.

A toolmaker that closes its doors after you've moved in. That's the deal.

---

## Also Shipped

### Anthropic names 2026 the breakaway year

The week opened on a Saturday with a single loud sentence. Anthropic's research team published "2028: Two scenarios for global AI leadership," a paper that puts semiconductors, not capabilities or safety, at the center of the US-China race ([Anthropic Research](https://www.anthropic.com/research/2028-ai-leadership)). In scenario one, democracies tighten chip export controls and hold a 12-to-24-month compute lead through 2028. In scenario two, policymakers defer and the norms get written by authoritarian states. "There is a high likelihood that we will look back on 2026 as the breakaway opportunity for American AI," the paper argues. It published while Trump was in Beijing for the first time in nearly a decade. The timing was not an accident.

### Claude Code patches a permission bypass

On Tuesday, Claude Code v2.1.145 shipped a fix that sat twelve bullets deep in a nineteen-item changelog: bare variable assignments to non-allowlisted environment variables in Bash commands were being auto-approved, slipping past the permission prompt entirely ([GitHub](https://github.com/anthropics/claude-code/releases/tag/v2.1.145)). In an agentic workflow with broad access, that's a real hole, not a cosmetic one. The same release added `claude agents --json` for scripting live sessions and put `agent_id` and `parent_agent_id` on OTEL spans. The understatement was the right call. The fix was the news.

### The API quietly gained three betas

Three API items dated May 18 surfaced through the week, none with an announcement. Cache diagnostics (public beta) reports a `cache_miss_reason` when a prompt-cache prefix diverges from the prior turn, behind the `cache-diagnosis-2026-04-07` header ([API release notes](https://docs.anthropic.com/en/release-notes/api)). Fast mode reached Opus 4.7 in research preview, extending the speed tier up from 4.6. And the built-in web search tool began returning richer SEC filing data, surfacing primary-source citations for financial-research and due-diligence agents. Plumbing, all of it. The kind that ships without a stage.

### The SDKs got self-hosted sandboxes

The builder layer moved in lockstep all week. On May 19, Python v0.103.0 and TypeScript v0.97.0 added self-hosted sandbox support in the Compute Management API, with helper utilities for standing your own sandboxes up ([GitHub](https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.103.0)). Point releases the same day taught `SessionToolRunner` to skip tool calls it doesn't own, closing a dispatch conflict in multi-agent sessions. Two days later, both SDKs added `thinking-token-count`, surfacing estimated token counts in thinking-block deltas during streaming, so agentic loops that lean on extended thinking can budget context instead of guessing.

---

## Quiet on the Wire

Code with Claude London wrapped its two-day run on May 20, with MIT Technology Review and Fortune both covering it ([MIT Technology Review](https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/)). The features on stage, self-hosted sandboxes and MCP tunnels for Managed Agents, had already shipped May 19. No model announcements anywhere in the window. The docs.anthropic.com release-notes pages stayed unreachable on every sweep this week, so anything that moved there silently isn't captured here. Tokyo is next, June 10.

---

## Term of the Issue

# The Toolmaker

**Toolmaker** /ˈtuːlˌmeɪ.kər/ *noun*

The party that owns the machinery others use to build, as distinct from the party with the best product. In a frontier race fought over models, the toolmaker move is to acquire the shared dependency, the SDK generator, the compute, the spec-to-library factory, and decide who keeps renting it.

**First observable** 2026-05-18, the week Anthropic acquired the SDK generator behind OpenAI, Google, Cloudflare, and Meta, then chose to wind it down.

**Usage** *"They didn't ship the better model. They bought the toolmaker."*

---

## The Close

No new model.
A factory bought and closed.
The toolmaker was the story.

---

## Release Log

## A. Research and Policy

*1 entry in window.*

#### 2026-05-15 - 2028: Two scenarios for global AI leadership ([paper](https://www.anthropic.com/research/2028-ai-leadership))
`[RESEARCH]`

Anthropic's research team frames 2028 as the inflection year for US-China AI dominance, placing semiconductors at the center rather than capabilities or safety. Scenario one: democracies defend their compute advantage, tighten chip export controls, and hold a 12-to-24-month frontier lead. Scenario two: policymakers defer, China closes the gap, and AI governance is authored by authoritarian regimes. The paper recommends restricting adversarial-state access to American models and tightening semiconductor supply-chain controls. Published May 15 while Trump made his first trip to Beijing in roughly a decade ([coverage](https://creati.ai/ai-news/2026-05-15/anthropic-publishes-2028-scenarios-for-global-ai-leadership/)).

## B. API and Platform

*3 entries in window. All dated May 18 on the API release notes; the docs domain was unreachable during the sweeps and items were confirmed via web search.*

#### 2026-05-18 - Cache diagnostics, public beta ([API release notes](https://docs.anthropic.com/en/release-notes/api))
`[API]`

Pass `diagnostics.previous_message_id` on a Messages request and the API returns a `cache_miss_reason` field explaining where the prompt-cache prefix diverged from the previous turn. Removes the guesswork from debugging multi-turn cache behavior.

**How to use:** Include beta header `cache-diagnosis-2026-04-07`. Add `diagnostics: { previous_message_id: "<id>" }` to the request body.

#### 2026-05-18 - Fast mode for Claude Opus 4.7, research preview ([API release notes](https://docs.anthropic.com/en/release-notes/api))
`[API]`

Fast mode now supports Opus 4.7, extending the speed tier up from Opus 4.6. Pricing and rate limits match Opus 4.6 fast mode. Waitlist access via the Console.

**How to use:** Set `speed: "fast"` with `model: "claude-opus-4-7"` and the `fast-mode-2026-02-01` beta header.

#### 2026-05-18 - SEC filing data in web search tool ([API release notes](https://docs.anthropic.com/en/release-notes/api))
`[API]`

The built-in web search tool now returns richer SEC filing data, surfacing primary-source citations from filings for financial-research, earnings-analysis, and due-diligence workflows.

## C. Claude Code

*5 entries in window.*

#### 2026-05-22 - Claude Code v2.1.149 ([GitHub releases](https://github.com/anthropics/claude-code/releases/tag/v2.1.149))
`[CODE]`

`/usage` now shows per-category cost breakdown (skills, subagents, plugins, per-MCP-server) instead of a single total. `/diff` gains keyboard navigation (arrows, j/k, PgUp/PgDn, Space, Home/End). Markdown renders GFM task-list checkboxes. Enterprise gets the `allowAllClaudeAiMcps` managed setting for claude.ai cloud MCP connectors. Four security fixes: PowerShell permission bypass via built-in `cd` functions, git-worktree sandbox write allowlist covering the entire repo root instead of scoped paths, PowerShell prefix/wildcard rules pre-approving native executables, and a permission-analysis gap from stale PWD/OLDPWD/DIRSTACK tracking. Also fixes `find` exhausting the macOS file/vnode table on large trees, managed-settings dialog freezes, and `/ultraplan` remote-session creation errors.

**How to use:** `claude update`. The `/usage` breakdown and `/diff` navigation are available immediately. Enterprise admins set `allowAllClaudeAiMcps` in managed settings.

#### 2026-05-22 - Claude Code v2.1.148 ([GitHub releases](https://github.com/anthropics/claude-code/releases/tag/v2.1.148))
`[CODE]`

Critical hotfix: the Bash tool was returning exit code 127 (command not found) on every invocation, a regression introduced in v2.1.147. Any workflow depending on shell command execution was broken until this shipped.

**How to use:** `claude update`. If you're on v2.1.147 and Bash commands are failing, this is why.

#### 2026-05-21 - Claude Code v2.1.147 ([GitHub releases](https://github.com/anthropics/claude-code/releases/tag/v2.1.147))
`[CODE]`

`/simplify` renamed to `/code-review`, with effort-level reporting (`/code-review high`) and a `--comment` flag that posts findings as inline GitHub PR review comments. Pinned background sessions (`Ctrl+T` in `claude agents`) now survive idle and restart in place when an update lands. 28 additional fixes spanning auto-updater retries, diff-rendering performance, enterprise login enforcement, PowerShell on Windows with winget/Microsoft Store installs, MCP server pagination (resources, templates, and prompts past page 1 were being dropped), shell snapshot user-function handling, plugin-agent multi-type declarations, and hook `if` condition matching.

**How to use:** `claude update`. Run `/code-review`, or `/code-review high` for a thorough pass; add `--comment` to post results to a GitHub PR.

#### 2026-05-19 - Claude Code v2.1.145 ([GitHub releases](https://github.com/anthropics/claude-code/releases/tag/v2.1.145))
`[CODE]`

Scripting, observability, plugin discoverability, and a security fix. `claude agents --json` surfaces live sessions as JSON for external tooling. OTEL gains `agent_id` and `parent_agent_id` on `claude_code.tool` spans with corrected trace parenting for background subagents. Status-line JSON now includes GitHub repo and PR context. `/plugin` Discover and Browse show a plugin's full manifest before install. Security fix: bare variable assignments to non-allowlisted env vars in Bash were auto-approved past the permission prompt, now blocked. Also fixes MCP error messaging for missing required arguments, a spinner freeze after terminal resize, the Windows PowerShell `;` separator, task-list ordering on concurrent creation, a `/review` GraphQL regression on Classic Projects repos, and a skill `context: fork` infinite loop.

**How to use:** `claude update`. Script sessions: `claude agents --json | jq '.[] | .id'`

#### 2026-05-19 - Claude Code v2.1.144 ([GitHub releases](https://github.com/anthropics/claude-code/releases/tag/v2.1.144))
`[CODE]`

Released Monday evening. Resume support for background sessions, elapsed-duration notifications when agents complete, and model selection scoped to individual sessions. Fixes startup hangs when the API is unreachable, terminal display corruption, and macOS background-session crashes in protected folders.

**How to use:** `claude update` or `npm i -g @anthropic-ai/claude-code`.

## E. Agent SDKs

*8 entries in window.*

#### 2026-05-22 - anthropic-sdk-python v0.104.1 ([GitHub releases](https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.104.1))
`[SDK-PY]`

Bug fix: `encrypted_content` was not being carried through the beta compaction accumulator during streaming. Affects users of the extended-thinking beta with context compaction enabled.

**How to use:** `pip install anthropic==0.104.1`

#### 2026-05-21 - anthropic-sdk-python v0.104.0 ([GitHub releases](https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.104.0))
`[SDK-PY]`

Adds `thinking-token-count` beta support: when streaming extended thinking, the SDK surfaces estimated token counts in thinking-block deltas. Useful for cost estimation and context-budget management in agentic loops that lean on extended thinking.

**How to use:** Include the `thinking-token-count` beta header. Token estimates arrive as metadata on thinking-block delta events during streaming.

#### 2026-05-21 - anthropic-sdk-typescript v0.98.0 ([GitHub releases](https://github.com/anthropics/anthropic-sdk-typescript/releases/tag/sdk-v0.98.0))
`[SDK-TS]`

Parity release: the same `thinking-token-count` beta as Python v0.104.0 ([releases](https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.104.0)). Both SDKs shipped the capability the same day.

**How to use:** `npm install @anthropic-ai/sdk@0.98.0`. Include the `thinking-token-count` beta header.

#### 2026-05-19 - anthropic-sdk-python v0.103.0 ([GitHub releases](https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.103.0))
`[SDK-PY]`

Adds support for self-hosted sandboxes in the Compute Management API (CMA) with new sandbox helper utilities.

**How to use:** `pip install anthropic==0.103.0`

#### 2026-05-19 - anthropic-sdk-python v0.103.1 ([GitHub releases](https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.103.1))
`[SDK-PY]`

Bug fix: `SessionToolRunner` skips tool calls it does not own, preventing dispatch conflicts in multi-agent sessions.

**How to use:** `pip install anthropic==0.103.1`

#### 2026-05-19 - anthropic-sdk-typescript v0.97.0 ([GitHub releases](https://github.com/anthropics/anthropic-sdk-typescript/releases/tag/sdk-v0.97.0))
`[SDK-TS]`

Self-hosted sandbox support in the CMA, matching the Python SDK release. Upgrades tsc-multi for Node 26 compatibility.

**How to use:** `npm install @anthropic-ai/sdk@0.97.0`

#### 2026-05-19 - anthropic-sdk-typescript v0.97.1 ([GitHub releases](https://github.com/anthropics/anthropic-sdk-typescript/releases/tag/sdk-v0.97.1))
`[SDK-TS]`

Bug fix: `SessionToolRunner` skips tool calls it does not own. Mirrors Python v0.103.1 ([releases](https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.103.1)).

**How to use:** `npm install @anthropic-ai/sdk@0.97.1`

#### 2026-05-19 - bedrock-sdk v0.29.2 and vertex-sdk v0.16.1 ([GitHub releases](https://github.com/anthropics/anthropic-sdk-typescript/releases/tag/vertex-sdk-v0.16.1))
`[SDK-TS]`

`@types/node` aligned across sub-packages to fix CI build failures. No feature changes.

**How to use:** `npm install @anthropic-ai/bedrock-sdk@0.29.2` or `@anthropic-ai/vertex-sdk@0.16.1`

## G. News and Partnerships

*1 entry in window.*

#### 2026-05-18 - Anthropic acquires Stainless ([Anthropic](https://www.anthropic.com/news/anthropic-acquires-stainless))
`[NEWS]`

Anthropic acquired Stainless (founded 2022, backed by Sequoia and a16z), which generates SDKs, CLIs, and MCP servers from API specifications. Stainless generated every official Anthropic SDK to date and also generates the Python, TypeScript, Go, Java, Kotlin, and Ruby libraries used by OpenAI, Google, Cloudflare, and Meta. Post-acquisition, all hosted Stainless products, including the SDK generator, wind down; existing customers retain their generated SDKs with full modification rights. Terms undisclosed; The Information reported talks valuing the company at over $300 million, with part potentially in Anthropic equity ([TechCrunch](https://techcrunch.com/2026/05/18/anthropic-has-acquired-the-dev-tools-startup-used-by-openai-google-and-cloudflare/)).
