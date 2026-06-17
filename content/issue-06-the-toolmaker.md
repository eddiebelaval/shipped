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

Monday morning, Anthropic bought a small company most builders had never heard of and every builder had already used. Stainless generated the official SDK for Anthropic's own API. It also generated the Python, TypeScript, Go, Java, Kotlin, and Ruby libraries that OpenAI, Google, Cloudflare, and Meta ship to their own developers. One startup quietly built the scaffolding under the whole frontier, and almost nobody outside the toolchain knew its name.

Then Anthropic said it would shut the service down.

No model shipped this week. No flagship. The headline was a $300-million-plus acquisition of a tool nobody talked about, and the decision to switch it off. The rest of the week was Claude Code patching itself in public, six versions in five days, twice in one Friday. The center of gravity moved from what the model can do to who owns the machinery that builds with it.

---

---

## The Lead Story

# The factory that built everyone's tools

The frontier race had a quiet move this week, and it wasn't a benchmark. It was an acquisition most people couldn't place.

On Monday, May 18, Anthropic announced it had acquired Stainless, the startup that generates production-ready SDKs, CLIs, and MCP servers directly from API specifications ([Anthropic](https://www.anthropic.com/news/anthropic-acquires-stainless)). Founded in 2022 by former Stripe engineer Alex Rattray and backed by Sequoia and Andreessen Horowitz, Stainless sat in a strange place in the toolchain. It generated every official Anthropic SDK since the API's earliest days. It also generated the Python, TypeScript, Go, Java, Kotlin, and Ruby libraries OpenAI, Google, Cloudflare, and Meta hand their own developers ([TechCrunch](https://techcrunch.com/2026/05/18/anthropic-has-acquired-the-dev-tools-startup-used-by-openai-google-and-cloudflare/)). Terms weren't disclosed. The Information had reported, before the announcement, that talks valued the company at over $300 million, with part of the consideration potentially in Anthropic equity.

Read the headline and you'd file it as a routine dev-tools tuck-in. Read the second sentence of the press release and the story changes. Anthropic will wind down all hosted Stainless products, the SDK generator included. Existing customers keep the SDKs they've already built, with full rights to modify them. The factory closes. The parts stay where they landed.

Sit with the mechanism, because the mechanism is the whole story. A spec-to-SDK generator is not a convenience. It is the thing that turns one OpenAPI document into seven idiomatic client libraries, keeps them in sync release after release, and absorbs the unglamorous labor of pagination helpers, retry logic, streaming parsers, and typed errors in six languages at once. A lab ships an API change on Tuesday; the generator re-emits libraries that match it by Wednesday. Stainless was the part of the supply chain nobody photographed because it sat below the layer anyone looks at. It was the loom under the cloth.

So name the blast radius precisely. OpenAI and Google do not lose the SDKs they have today. They keep them, with full rights to modify. What they lose is the supplier. The next time one of them ships an API change and reaches to regenerate, the hosted machine that did it for them is dark. They can fork what Stainless left behind, hire a team to maintain a generator in-house, or build their own from scratch, and any of those is a real engineering cost on a workstream they had been quietly outsourcing to a competitor. The library on disk still works. The conveyor belt that kept it current is gone. That is the difference between buying a feature and buying a chokepoint.

It rhymes with the spring's other Anthropic story. Capacity was about owning the compute everyone needs to run. This is about owning the tooling everyone needs to build. Same instinct, much smaller check: when the constraint is a dependency you don't control, buy the dependency. A $30-billion-run-rate lab paid roughly the price of a few weeks of its Colossus compute bill to take a load-bearing brick out of its rivals' foundations. The Memphis data center cost an estimated $1.25 billion a month ([TechCrunch](https://techcrunch.com/2026/05/20/anthropic-will-pay-xai-1-25-billion-per-month-for-compute/)); Stainless reportedly cost north of $300 million once ([TechCrunch](https://techcrunch.com/2026/05/18/anthropic-has-acquired-the-dev-tools-startup-used-by-openai-google-and-cloudflare/)). One of those is a recurring tax. The other is a permanent subtraction from someone else's stack.

Read against the rest of the frontier, the move has teeth the press release declined to show. Every lab now sells agents, and agents are only as good as the SDKs and MCP servers that let them touch the world. Anthropic just bought the standard tool for generating exactly those surfaces, and then it removed that tool from the market it shares with the labs it competes against. The contrast is the read: while the field races to ship the better model, Anthropic spent the week making sure the field has a harder time shipping the better client. Nobody loses a model over this. Everybody who relied on the generator inherits a maintenance problem they didn't have on Sunday.

For a builder, the move tonight is narrow and worth making. If your pipeline pulls a Stainless-generated SDK for any provider, vendor the current output now and read the wind-down terms while the docs are still up. You keep what you have and the right to modify it; you do not keep the button that regenerated it. Pin the version, check it into a place you control, and stop assuming the upstream loom will be there next quarter.

A toolmaker that closes its doors after you've moved in. That's the deal.

---

## The Self-Patching Week

# Six versions, two security drops, one broken Friday

If the acquisition was the week's headline, Claude Code was its heartbeat. The CLI shipped six numbered releases between Monday night and Friday dinner, two of them on the same Friday, and the arc they trace is the more honest portrait of where the tooling actually is: an agent that runs with broad access on machines next to production, being hardened in public, fast, with the seams showing.

It opened quietly. v2.1.144 landed Monday evening with resume support for background sessions, elapsed-duration notifications when an agent finishes, and per-session model selection, plus fixes for startup hangs when the API is unreachable and macOS background-session crashes in protected folders ([GitHub](https://github.com/anthropics/claude-code/releases)). Housekeeping for people who leave agents running and walk away. Then Tuesday turned serious. v2.1.145 carried a security fix buried at bullet twelve of a nineteen-item changelog: bare variable assignments to non-allowlisted environment variables in Bash were being auto-approved, slipping past the permission prompt entirely ([GitHub](https://github.com/anthropics/claude-code/releases/tag/v2.1.145)). In an agentic loop with shell access, that is not a cosmetic bug. That is a path an attacker walks straight through. The same release added `claude agents --json` for scripting live sessions and put `agent_id` and `parent_agent_id` on OTEL spans with corrected trace parenting for background subagents. The fix was the news; the understatement was the tell.

Thursday's v2.1.147 renamed `/simplify` to `/code-review`, gave it effort levels (`/code-review high`) and a `--comment` flag that posts findings as inline GitHub PR comments, and made pinned background sessions survive idle and restart in place when an update lands ([GitHub](https://github.com/anthropics/claude-code/releases/tag/v2.1.147)). Behind those two visible changes sat 28 more fixes: PowerShell on Windows with winget and Microsoft Store installs, MCP server pagination that had been silently dropping resources and templates past page one, auto-updater retries, diff-rendering performance. Nothing in that list changes what the tool can do. Several things change how reliably it does it, which on a tool this load-bearing is the same thing as a feature.

Then Friday broke. v2.1.148 shipped as a one-line hotfix at the top of the day: the Bash tool was returning exit code 127, command not found, on every invocation, a regression introduced in v2.1.147 ([GitHub](https://github.com/anthropics/claude-code/releases/tag/v2.1.148)). Any workflow that depended on shell execution, which is most agentic workflows, was broken from the moment Thursday's release landed until the morning fix. The blast radius there is anyone who updated on Thursday and woke up to an agent that couldn't run a command. The cause is the cost of shipping a 28-fix release at this clip: move fast enough and one of the fixes breaks the thing it sat next to.

The week closed where it began, on security. Friday evening's v2.1.149 carried four more permission-boundary fixes in a single drop ([GitHub](https://github.com/anthropics/claude-code/releases/tag/v2.1.149)). A PowerShell bypass via built-in `cd` functions. A git-worktree sandbox that was allowlisting writes to the entire repo root instead of scoped paths. PowerShell prefix and wildcard rules that pre-approved native executables. A permission-analysis gap from stale PWD, OLDPWD, and DIRSTACK tracking. Read them together and they describe one anxiety: a sandbox that keeps finding new ways to be wider than it claims. The same release gave `/usage` a per-category cost breakdown across skills, subagents, plugins, and per-MCP-server, which is the first time the tool tells you which part of your agent chain is spending the money.

Step back from the version numbers and the pattern is the read. In one week, two of Claude Code's six releases existed primarily to close permission and sandbox holes, a third broke shell execution outright, and the others hardened reliability around long-running background agents. This is what it looks like when a coding agent grows up in production: not a triumphant feature reel, but a fast, visible, slightly nervous campaign to make the blast radius smaller than the access. The frontier sells the agent that runs while you sleep. The fine print, written six versions deep this week, is that the agent runs with your keys, and the lab is still finding the doors it left unlocked. The move for anyone running it with broad scope is the boring one: update past 2.1.149, and if you pinned to 2.1.147, check whether your Bash tool has been silently failing since Thursday.

---

## By the Numbers

The week measured in versions, dollars, and the size of a changelog.

- **6**: Claude Code releases shipped between May 18 and May 22 (v2.1.144, .145, .147, .148, .149, plus the .146 gap) ([GitHub](https://github.com/anthropics/claude-code/releases)).
- **2**: of those six releases that shipped on Friday, May 22 alone (v2.1.148 and v2.1.149) ([GitHub](https://github.com/anthropics/claude-code/releases/tag/v2.1.149)).
- **$300M+**: reported value of the Stainless acquisition, per The Information ([TechCrunch](https://techcrunch.com/2026/05/18/anthropic-has-acquired-the-dev-tools-startup-used-by-openai-google-and-cloudflare/)).
- **4**: frontier customers Stainless generated SDKs for besides Anthropic: OpenAI, Google, Cloudflare, and Meta ([Anthropic](https://www.anthropic.com/news/anthropic-acquires-stainless)).
- **6**: languages Stainless generated client libraries in: Python, TypeScript, Go, Java, Kotlin, and Ruby ([TechCrunch](https://techcrunch.com/2026/05/18/anthropic-has-acquired-the-dev-tools-startup-used-by-openai-google-and-cloudflare/)).
- **2022**: the year Stainless was founded, by former Stripe engineer Alex Rattray ([Anthropic](https://www.anthropic.com/news/anthropic-acquires-stainless)).
- **12**: the bullet, out of 19, where the Bash permission-bypass fix sat in the v2.1.145 changelog ([GitHub](https://github.com/anthropics/claude-code/releases/tag/v2.1.145)).
- **28**: additional fixes bundled into v2.1.147 alongside the `/code-review` rename ([GitHub](https://github.com/anthropics/claude-code/releases/tag/v2.1.147)).
- **4**: security fixes in the single v2.1.149 drop ([GitHub](https://github.com/anthropics/claude-code/releases/tag/v2.1.149)).
- **127**: the exit code the Bash tool wrongly returned on every command in v2.1.147, fixed by v2.1.148 ([GitHub](https://github.com/anthropics/claude-code/releases/tag/v2.1.148)).
- **3**: API betas dated May 18 that surfaced with no announcement: cache diagnostics, Fast mode for Opus 4.7, and SEC filing data in web search ([API release notes](https://docs.anthropic.com/en/release-notes/api)).
- **12-to-24**: the months of compute lead democracies hold through 2028 in the optimistic scenario of Anthropic's leadership paper ([Anthropic Research](https://www.anthropic.com/research/2028-ai-leadership)).
- **May 14**: the Gates Foundation partnership, the last thing anthropic.com/news moved on before the window opened, four years of grant funding announced and then silence ([Anthropic](https://www.anthropic.com/news/gates-foundation-partnership)).
- **0**: new models shipped in the window.

---

## Also Shipped

### Anthropic names 2026 the breakaway year

The week opened on a Saturday with a single loud sentence. Anthropic's research team published "2028: Two scenarios for global AI leadership," a paper that puts semiconductors, not capabilities or safety, at the center of the US-China race ([Anthropic Research](https://www.anthropic.com/research/2028-ai-leadership)). In scenario one, democracies tighten chip export controls, block adversarial-state access to American frontier models, and hold a 12-to-24-month compute lead through 2028. In scenario two, policymakers defer, China closes the gap, and the norms governing AI globally get written by authoritarian states. "There is a high likelihood that we will look back on 2026 as the breakaway opportunity for American AI," the paper argues, and the rest of it is the case for that sentence. It published on anthropic.com while Trump was in Beijing for the first time in nearly a decade ([coverage](https://creati.ai/ai-news/2026-05-15/anthropic-publishes-2028-scenarios-for-global-ai-leadership/)). A lab that spent the week buying a tool out from under its rivals also spent a Saturday arguing that the real contest is over chips, not capabilities, and that the clock is the policy lever. The timing was not an accident.

### The API quietly gained three betas

Three API items dated May 18 surfaced through the week, none with an announcement, none with a stage. Cache diagnostics, in public beta, reports a `cache_miss_reason` field when a prompt-cache prefix diverges from the prior turn, so you can debug multi-turn cache behavior instead of guessing where the prefix broke; it rides behind the `cache-diagnosis-2026-04-07` header ([API release notes](https://docs.anthropic.com/en/release-notes/api)). Fast mode reached Opus 4.7 in research preview, extending the speed tier up from 4.6 at matching pricing. And the built-in web search tool began returning richer SEC filing data, surfacing primary-source citations from filings for financial-research, earnings-analysis, and due-diligence agents. None of it had a launch. All of it is the kind of plumbing that decides whether an agent built on the platform is cheap to run and easy to trust. Read against the Stainless move, it is the same week's other half: own the tooling, then quietly improve the parts of it you already own.

### The SDKs got self-hosted sandboxes

The builder layer moved in lockstep all week. On May 19, Python v0.103.0 and TypeScript v0.97.0 added self-hosted sandbox support in the Compute Management API, with helper utilities for standing your own sandboxes up ([GitHub](https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.103.0)). That is the surface that lets you run agent code in isolation you control rather than renting it, which matters for anyone who can't ship their code to a managed runtime. Point releases the same day taught `SessionToolRunner` to skip tool calls it doesn't own, closing a dispatch conflict that would otherwise bite multi-agent sessions where two runners fight over the same call. The TypeScript build also picked up Node 26 compatibility. The features Code with Claude London put on stage on May 20, self-hosted sandboxes and MCP tunnels for Managed Agents, had already shipped here the day before the keynote opened.

### Both SDKs learned to count thinking tokens

On May 21, Python v0.104.0 ([releases](https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.104.0)) and TypeScript v0.98.0 ([releases](https://github.com/anthropics/anthropic-sdk-typescript/releases/tag/sdk-v0.98.0)) added `thinking-token-count` beta support on the same day, a parity release surfacing estimated token counts in thinking-block deltas during streaming. The point is budget. Agentic loops that lean on extended thinking have been flying blind on how much context the reasoning is eating until the bill or the context window said otherwise; now the estimate arrives as metadata mid-stream, while there is still time to act on it. A day later, Python v0.104.1 cleaned up the corner the feature exposed: `encrypted_content` wasn't being carried through the beta compaction accumulator during streaming, which bit anyone running the extended-thinking beta with context compaction on ([GitHub](https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.104.1)). Ship the visibility, then patch the leak it surfaced. The whole week ran on that rhythm.

### The bedrock and vertex SDKs got a CI fix

The least glamorous entry in the log, and worth one line for the people it unblocked. On May 19, bedrock-sdk v0.29.2 ([releases](https://github.com/anthropics/anthropic-sdk-typescript/releases/tag/bedrock-sdk-v0.29.2)) and vertex-sdk v0.16.1 ([releases](https://github.com/anthropics/anthropic-sdk-typescript/releases/tag/vertex-sdk-v0.16.1)) aligned `@types/node` across sub-packages to fix CI build failures, with no feature changes. Anyone deploying Claude through Bedrock or Vertex on a pinned TypeScript toolchain had a red pipeline until this landed. No mechanism worth a paragraph, but the blast radius was real, and the move is the obvious one: bump and move on.

---

## Quiet on the Wire

No models. No flagship. anthropic.com/research stayed dark after the May 15 leadership paper ([coverage](https://creati.ai/ai-news/2026-05-15/anthropic-publishes-2028-scenarios-for-global-ai-leadership/)), and anthropic.com/news hadn't moved since the May 14 Gates Foundation partnership, $200 million over four years across global health, life sciences, education, and economic mobility, which sat just outside the window ([Anthropic](https://www.anthropic.com/news/gates-foundation-partnership)). Code with Claude London wrapped its two-day run on May 20, with MIT Technology Review and Fortune both covering it ([MIT Technology Review](https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/)), but the features on stage had already shipped in the SDKs the day before. The docs.anthropic.com release-notes pages returned 403 on every sweep this week, so anything that moved there silently isn't captured here; the three API betas above were confirmed by web search, not by the source. Tokyo is the next stop, June 10.

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
Six patches to make the agent safe to hold.
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
