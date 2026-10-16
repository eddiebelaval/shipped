---
issue: 01
slug: the-shadow-release
title: "The Shadow Release"
date: 2026-04-16
period: 2026-03-27 to 2026-04-16
masthead: Shipped.
deck: "Three weeks of Anthropic, in one read. The model they shipped. The model you can't have."
byline: Reporting by Eddie Belaval
status: reconstructed-draft
ship_date: 2026-04-16
weather: "Build accordingly."
reconstructed_from: id8labs/public/shipped/01/index.html
reconstructed_at: 2026-10-15
---


## The Open

*There's a thing Anthropic does now that doesn't have a name. They release a flagship model, and in the same breath, they tell you about a better one you can't have.*

Three weeks of Anthropic, in one read. The model they shipped. The model you can't have. And the distance between them — the new normal.

Opus 4.6 in November. Opus 4.7 today. Mythos in between, gated, available only to a handful of security partners.

Call it the *shadow release*. The model that ships sets the floor. The model that doesn't reveals the ceiling. The space between them is where everyone who builds with this stuff now lives.

Three weeks of velocity below. Fifty-six releases — models, agents, infrastructure, a security pact with twelve names you'd recognize, twenty-six versions of Claude Code, a tokenizer change you'll feel in your bill. Plus the shadow.

## The Lead Story

# The chart that wasn't about Opus 4.7.

**Opus 4.7 ships. Same price. Better vision. Sharper coding. And then, on the fourth bar of the launch chart, a model you cannot buy — taller than everything else.**

*Report · Opus 4.7 launch · Apr 16, 2026 Floor & ceiling · 2,576 px vision · xhigh default · 1.0 – 1.35× tokenizer*

**Why this matters:** First flagship where Anthropic explicitly conceded a stronger internal model (*Mythos*) exists. Precedent set. The next time the lab invokes "too dangerous to ship in the standard channel," the chart will look familiar..

Opus 4.7 went generally available this morning. Same pricing as 4.6 — five dollars per million input, twenty-five per million output. Better at coding, sharper on hard software engineering, with the kind of self-verification that previously required you to paper over with scaffolding. Vision tripled in resolution: 2,576 pixels on the long edge, more than three times what prior versions could see. The model can now read dense screenshots and pixel-perfect references without you down-sampling first.

A new effort level called `xhigh` slotted in between `high` and `max`. Claude Code now defaults to `xhigh` on every plan. If you're paying attention to your bills, that change matters as much as anything else in the launch — `xhigh` produces more thinking tokens than `high`, and Anthropic raised the default before most users will notice.

The migration notes mention a tokenizer change: the same input may consume 1.0 to 1.35× more tokens depending on what you feed it. Re-tune your prompts. The bill will tell you which way it broke.

The vision change deserves its own paragraph. At 2,576 pixels on the long edge — roughly 3.75 megapixels — Opus 4.7 can read a full-density desktop screenshot without you cropping or scaling. Diagrams that used to need OCR pre-processing can now go in raw. UI mockups can be referenced pixel-for-pixel for code generation. This isn't a knob; it's a workflow change for anyone who's been hand-feeding the model lower-resolution slices.

**But the headline isn't the model.**

The headline is the chart Anthropic published next to the model.

## Also Shipped

### Glasswing.

**On April 7, twelve organizations agreed to use a model none of their customers can touch. The precedent starts here.**

*Consortium 12 founders · 40+ in talks AWS · Apple · Broadcom · Cisco · CrowdStrike · Google · JPMorgan Chase · Linux Foundation · Microsoft · NVIDIA · Palo Alto Networks · Anthropic*

**The money:** **$100M** in Anthropic model credits to partners. **$2.5M** to Alpha-Omega and OpenSSF. **$1.5M** to the Apache Software Foundation. Funding routed to the open-source maintainers who don't have security teams..

Project Glasswing is the consortium Anthropic announced alongside Mythos Preview's gated release. The founders: Amazon Web Services, Apple, Broadcom, Cisco, CrowdStrike, Google, JPMorgan Chase, the Linux Foundation, Microsoft, NVIDIA, Palo Alto Networks, and Anthropic itself. Forty-plus additional organizations are in early conversation. The goal, stated plainly: harden the world's most critical software infrastructure against a class of vulnerabilities that AI can now find faster than humans can patch them.

The financial structure is unusual for a security consortium. $100M in model credits committed by Anthropic to Glasswing participants — meaning the partners pay nothing for the inference. $2.5M donated to Alpha-Omega and OpenSSF. $1.5M to the Apache Software Foundation. The donations matter because they answer the obvious objection: this isn't a private security tool for big vendors. The funding is meant to flow to open-source maintainers who don't have security teams.

### The agent stack got serious.

**Managed Agents. The advisor tool. The `ant` CLI. All three shipped inside April 8–9. The era of writing your own loop is closing — Anthropic is taking that work in-house.**

*Apr 08 Managed Agents public beta · ant CLI launch Apr 09 Advisor tool public beta · Cowork GA · SDK parity*

**Four primitives, all shipped:** Sandbox. Tool harness. Context manager. Streaming loop. If your competitive moat was the loop, your moat just shrank..

For the past year, every team building agents on Claude has been writing the same code. A sandbox, a tool harness, a context manager, a streaming loop. The interfaces varied. The components didn't. Anyone who's built an agent in production has shipped some version of all four.

April 8 and 9 was the week Anthropic shipped all four primitives. The era of writing your own loop is closing. Anthropic is taking that work in-house.

**Managed Agents** went into public beta on April 8 (header `managed-agents-2026-04-01`). Fully managed harness with secure sandboxing, built-in tools, and server-sent event streaming. You create agents and configure containers through the API — what used to be a Kubernetes problem, an IAM problem, and a tool-routing problem becomes one HTTP call. The pricing model is unannounced; the implication is that Anthropic intends to compete with whatever your in-house agent platform looks like, on its own infrastructure.

**The advisor tool** shipped April 9 (`advisor-tool-2026-03-01`). The pattern is simple and overdue: pair a faster executor model with a higher-intelligence advisor that provides strategic guidance mid-generation. Long-horizon agentic workloads get close to advisor-solo quality at executor-model cost. If you've been running Sonnet 4.6 for the bulk work and bouncing to Opus 4.6 for the hard turns, the advisor tool just made that pattern a primitive instead of an architecture.

**The `ant` CLI** dropped the same day. A command-line client for the Claude API with native Claude Code integration and YAML-based versioning of API resources — skills, agents, deployments. The implication is bigger than the tool: agents are becoming versionable, declarative configurations rather than code. Treat your agent definitions like Terraform.

### Claude Code grew a body.

**Twenty-six versions in twenty-one days. The CLI is becoming an IDE, and the IDE is becoming a control plane. When does saying “Claude Code is a CLI” stop being true?**

*Versions v2.1.85 → v2.1.111 · Cadence 1.24 releases/day*

**The arc:** Routines. /ultrareview. /team-onboarding. Multi-session UI. Push notifications. PowerShell. PID namespaces. Plugins with binaries. A diff viewer faster than your IDE's..

Twenty-six versions shipped between v2.1.85 (March 27) and v2.1.111 (today). Most were point releases: bug fixes, env var additions, plugin tweaks. But woven through them is a clear arc — the CLI is becoming an IDE, and the IDE is becoming a control plane.

**Routines** are the most consequential addition (v2.1.101 area). A routine is a saved Claude Code configuration — prompt, repos, connectors — packaged once and run automatically on Anthropic's cloud. If you've been wondering when “agent that ships code on a schedule” stops being a custom build, the answer is: now. The infrastructure is hosted. The scheduling is configurable. The cost model is “you pay for the inference” — same as your interactive sessions.

**The UI redesign** (v2.1.110-111) is the most visible shift. Multiple Claude sessions side by side in one window, with a sidebar. Integrated terminal. File editing. HTML and PDF preview. A faster diff viewer. Anthropic is not subtle about the trajectory. The CLI is becoming the work environment.

**`/ultrareview`** (v2.1.111) is comprehensive parallel-analysis code review using cloud compute. Pro and Max users get three free per month. The implication: code review is now a heavyweight LLM task that shouldn't run on your local terminal — it should run on Anthropic's compute and stream back. A pattern other heavy commands will follow.

**`/team-onboarding`** (v2.1.101) generates a teammate ramp-up guide from your local Claude Code usage. It's a small feature with a quietly large implication: your AI usage patterns are themselves documentation. Future hires read your transcript shape to learn how to use the tools.

The closing question, after twenty-six versions in twenty-one days: when does Claude Code stop being a CLI? The answer is not far. The diff viewer is faster than your IDE's. The terminal is integrated. The file editor is in the sidebar. The cloud routines are running while you sleep. At some point — probably this year — saying “Claude Code is a CLI” will be technically true and effectively obsolete.

### The fifth bar, the Mythos bar.

It shows Opus 4.7 beating Opus 4.6. Beating GPT-5.4. Beating Gemini 3.1 Pro across the relevant benchmarks. And then it shows Opus 4.7 losing to a fourth bar labeled *Mythos Preview*. The fourth bar is taller than every other bar. The fourth bar is the model you can't use.

The frontier is in a vault, working on the OSS-Fuzz corpus, finding 27-year-old vulnerabilities in OpenBSD. Opus 4.7 is the floor of what you can buy this week. Mythos is the ceiling of what exists. The distance between them is the new normal — and Anthropic has decided that the distance, for now, is a feature, not a bug.

The implication is institutional, not technical. For the first time, the lab has an internal precedent for "we found something too dangerous to ship in the standard channel." That precedent will be invoked again. Probably soon. The next time it happens, the chart will look familiar.

### The pattern is the news.

“The window between vulnerability discovery and exploitation has collapsed — what took months now happens in minutes.”

Mythos has already produced results. The model has identified zero-day vulnerabilities in every major operating system and every major web browser tested against it. The depth is what gets attention from people who've spent careers in this work: the bugs aren't surface-level. Many are subtle, old, and survived prior automated tooling. A 27-year-old OpenBSD bug. A 16-year-old FFmpeg flaw. Linux kernel privilege escalation chains that no published fuzzer has caught. The Firefox exploit Mythos wrote chained four separate vulnerabilities into a sandbox escape — the kind of compound exploit that a senior offensive security researcher might produce in a multi-week engagement.

“The old ways of hardening systems are no longer sufficient.”

The benchmark Mythos is being judged against is CyberGym, an academic vulnerability-reproduction suite. Mythos hits 83.1%. Opus 4.6 — the previous publicly available frontier model — hits 66.6%. The Firefox-specific test is more dramatic: Opus 4.6 produced two working JavaScript shell exploits across several hundred attempts. Mythos produced **181**.

Opus 4.6

2

Working exploits across several hundred attempts

vs

Mythos Preview

181

Same trial. Same browser.

“This initiative offers a credible path to making AI-augmented security a trusted tool for every maintainer, not just those with expensive teams.”

The hard question is institutional, not technical. Anthropic has now established an internal precedent: a model that passes evaluations can still be held back from public release on safety grounds. The Glasswing framing is “defensive use only.” But the model exists. The capability exists. The concession in the Opus 4.7 launch chart was that the capability can't be reproduced by you, no matter how much you pay.

The next time Anthropic invokes this precedent, what will the criteria be? What does the second Glasswing look like? When does the cybersecurity rationale extend to other categories — biological, cognitive, financial — and what's the institutional process for making that call? Anthropic has 90 days to publish the first Glasswing progress report. Read it carefully. The methodology will be precedent.

### The pattern is the news.

python · messages.create advisor-tool-2026-03-01

The week's three releases compose. You can run a Managed Agent that uses the advisor tool internally, with the agent definition versioned as YAML through `ant`. None of this is theoretical — the docs ship with examples that combine all three.

What this means for the people who built their own agent loops: most of that code is now a glue layer. Some of it remains differentiated — your prompt library, your domain-specific tools, your retrieval pipeline. The harness, the sandbox, the streaming, the context window management — those are commodity now. If your competitive moat was the loop, your moat just shrank.

### 26 versions of Claude Code, v2.1.85 → v2.1.111

**Cowork shipped, finally.**

Claude Cowork went generally available on macOS and Windows on April 9, ending what felt like a long beta. The headline is GA itself. Cowork is Anthropic's bet on AI-native team collaboration — not a shared document with AI features bolted on, but a shared agent that works alongside the team and persists across members.

Three additions made the GA more than a milestone. **Role-based access controls for Enterprise plans** mean admins can carve up which teams get which Cowork capabilities. The pattern is familiar from any enterprise SaaS, but the implication for AI access control is new — what does it mean to scope an autonomous agent to one department's data and not another's? Cowork is the first product that has to answer.

**Cowork analytics in the API** exposes engagement and adoption data programmatically. **OpenTelemetry support** is the second half of the same move — Cowork activity becomes telemetry like any other production system. Whether teams use Cowork as a persistent collaborator, not a chat sidebar, depends on whether teams reorganize their workflows to give the agent something to persist. Two quarters from now, we'll know whether Cowork is Slack's AI replacement or Microsoft Bob.

**Two papers worth your Friday.**

**Automated Alignment Researchers** (April 14). Anthropic on using LLMs to scale scalable oversight. The paper benchmarks the technique. Read it next to the Mythos disclosure: the same week the lab publicly held a model back for safety, they're publishing on how to use models to do the safety work faster. The two are not unrelated. If you're scaling capability, you have to scale oversight at the same rate or the gap becomes the story.

**Emotion Concepts in Large Language Models** (March, on `transformer-circuits.pub`). Researchers found internal representations of emotion concepts in Claude that generalize across contexts and behaviors. The wrong question is whether the models *have* emotions. The right question is whether they have *coherent internal representations* of emotions that change what they output. The answer the paper supports is yes.

Both papers point at the same underlying program: the lab is trying to do interpretability and oversight at the speed of capability. Whether they can keep pace is the question that matters most this decade.

### The Mythos Bar, in detail.

Where Opus 4.6 hits 66.6% on the CyberGym vulnerability-reproduction benchmark, Mythos Preview hits 83.1%. Where Opus 4.6 produced two working Firefox shell exploits in several hundred attempts, Mythos produced **181**. On the OSS-Fuzz corpus, Mythos achieved full control-flow hijack on ten separate, fully patched targets.

The vulnerabilities Mythos has surfaced are subtle, old, or both:

27 *yr*Memory-corruption bug in OpenBSD. Survived decades of human review.

16 *yr*FFmpeg flaw. Automated fuzzing missed it across 5M prior test hits.

10 *tgt*Linux-kernel privilege escalation chains. Race conditions + KASLR bypass.

4 *chn*Firefox JIT heap-spray. Escaped both renderer and OS sandboxes.

You can't have it. Mythos is gated to twelve security partners under Project Glasswing. Anthropic's stated reason is risk: a model that finds zero-days in OpenBSD that survived twenty-seven years of human review is a model you don't put on the open API. Whether that calculus holds — for how long, and under what pressure — is the open question of the year.

## Quiet on the Wire

*Quiet on the wire.*

Mythos broad release — no date, no signal, no roadmap visible. Project Glasswing's first 90-day report will be the next read on whether the gating posture holds. The Bedrock Messages API research preview is **us-east-1** only; regional rollout unannounced.

Sonnet 4 and Opus 4 retire from the API on **June 15, 2026** — if you haven't migrated, the clock started two days ago. Sonnet 4.5's 1M-context beta dies **April 30**. The Long-Term Benefit Trust appointed Vas Narasimhan to the Board of Directors on April 14; the pharma-and-policy axis of governance is worth watching over the next quarter for biotech and regulated-industry deal flow.

Notable absences: no fast-mode preview for Opus 4.7 yet, no Haiku 5 signal, no Opus 4.7 on Vertex AI's edge regions, no public roadmap for the `ant` CLI's Windows binary. All gaps. All worth watching.

## The Close

Three weeks. Fifty-six releases. One model you can buy, one you can't.

The shadow is the news.

Build accordingly.

Build accordingly.

## A. Models

*The flagship shipped — and the launch chart conceded a stronger model in the vault.*

#### 2026-04-16 - Claude Opus 4.7 — generally available ([source](https://www.anthropic.com/news/claude-opus-4-7))
`[MODEL]`

Anthropic's most capable generally available model. Coding, vision, and self-verification gains over 4.6. New `xhigh` effort level slots between `high` and `max`. Vision processes images up to 2,576px on the long edge (3× prior). Tokenizer change — same input may consume 1.0–1.35× more tokens.

**How to use:** `client.messages.create(model="claude-opus-4-7", effort={"level": "xhigh"}, messages=[...])` · Pricing unchanged: $5 / $25 per MTok. Available on Claude API, Bedrock, Vertex, Foundry, GitHub Copilot. Re-tune prompts; stricter instruction-following may surprise legacy code.

**Why it matters:** First flagship where Anthropic explicitly conceded a stronger internal model (Mythos) exists.

#### 2026-04-07 - Claude Mythos Preview (gated) ([source](https://www.anthropic.com/glasswing))
`[NEWS]`

Unreleased frontier model with strikingly capable cybersecurity performance. 83.1% on CyberGym (vs. Opus 4.6's 66.6%). Found zero-days in every major OS and browser including a 27-year-old OpenBSD bug.

**How to use:** Invitation-only, defensive cybersecurity work only, via Project Glasswing. Not available on the public API.

## B. API & Platform

*Managed Agents and the advisor tool entered public beta. Sonnet 4 + Opus 4 retire June 15, the 1M-context beta dies April 30.*

#### 2026-04-16 - Opus 4.7 API release + tokenizer change ([source](#))
`[API]`

Includes API breaking changes vs. Opus 4.6. New tokenizer means token counts shift 1.0–1.35×. Migration guide published.

**How to use:** Read the Opus 4.7 migration guide before upgrading. Audit your prompt tokenizer counts before swapping model IDs.

#### 2026-04-14 - Sonnet 4 / Opus 4 deprecation ([source](#))
`[DEPRECATION]`

`claude-sonnet-4-20250514` and `claude-opus-4-20250514` retire **June 15, 2026**.

**How to use:** Migrate Sonnet 4 → `claude-sonnet-4-6`, Opus 4 → `claude-opus-4-7`. After June 15 these model IDs return errors.

#### 2026-04-09 - Advisor tool — public beta ([source](#))
`[NEWS]`

Pair a faster executor with a higher-intelligence advisor that provides strategic guidance mid-generation. Long-horizon agent runs approach advisor-solo quality at executor cost.

**How to use:** Add beta header `advisor-tool-2026-03-01` to requests.

#### 2026-04-08 - Claude Managed Agents — public beta ([source](#))
`[NEWS]`

Fully managed agent harness — secure sandboxing, built-in tools, SSE streaming, container configuration via API.

**How to use:** Add beta header `managed-agents-2026-04-01`. Create agents and run sessions via the new endpoints.

#### 2026-04-08 - ant CLI — launch ([source](#))
`[NEWS]`

Command-line client for the Claude API with native Claude Code integration and YAML-based versioning of API resources (skills, agents, deployments).

**How to use:** Install per the CLI reference. Script API resource lifecycle outside the console.

#### 2026-04-07 - Messages API on Amazon Bedrock (research preview) ([source](#))
`[NEWS]`

First-party Claude API request shape now available on Bedrock at `/anthropic/v1/messages` endpoint. Runs on AWS-managed infrastructure with zero operator access.

**How to use:** Available in `us-east-1` only. Contact your Anthropic account executive for access.

#### 2026-03-30 - Message Batches API max_tokens raised to 300k ([source](#))
`[API]`

For Opus 4.6 and Sonnet 4.6 only. Long-form content, structured data, large code generation now supported in single batch turns.

**How to use:** Add beta header `output-300k-2026-03-24` to batch requests.

## C. Claude Code

*Twenty-six versions in twenty-one days. Routines, the UI redesign, /ultrareview cloud reviews, /team-onboarding, push notifications, PowerShell on Windows.*

#### 2026-04-16 - v2.1.111 ([source](#))
`[CODE]`

Opus 4.7 `xhigh` available, Auto mode for Max subscribers, interactive `/effort` slider, “Auto (match terminal)” theme, `/less-permission-prompts` skill, `/ultrareview` cloud code review, PowerShell rollout on Windows, Plan files named after user prompts, `Ctrl+U` / `Ctrl+Y` clear/restore input buffer.

**How to use:** `claude update`. Run `/ultrareview` in any session for parallel-analysis cloud code review. `/effort` opens the slider for reasoning depth.

#### 2026-04-15 - v2.1.110 ([source](#))
`[CODE]`

`/tui` flicker-free fullscreen rendering, push notification tool for mobile alerts, `Ctrl+O` toggles transcript verbosity, `/focus` toggles focus view, `/plugin` Installed tab with priority sorting, session recap for telemetry-disabled users.

**How to use:** Run `/tui` for fullscreen mode. Configure push notifications via `/config`. Use `/focus` to hide non-essential UI during deep work.

#### 2026-04-14 - v2.1.109 · v2.1.108 · v2.1.107 ([source](#))
`[NEWS]`

Rotating progress hint on extended thinking. `ENABLE_PROMPT_CACHING_1H` env var for 1-hour cache TTL. Recap feature for session context. Model can discover and invoke built-in slash commands via Skill tool. `/undo` as alias for `/rewind`.

**How to use:** `export ENABLE_PROMPT_CACHING_1H=1` to enable 1-hour cache. Use `/undo` interchangeably with `/rewind`.

#### 2026-04-13 - v2.1.105 ([source](#))
`[CODE]`

`path` parameter added to EnterWorktree tool, PreCompact hook with blocking capability, plugin background monitor support via manifest key, `/proactive` alias for `/loop`, 5-minute abort timeout for stalled API streams.

**How to use:** Configure PreCompact hook in `.claude/settings.json` to block compaction. Plugins can declare `monitors` in their manifest for background processes.

#### 2026-04-09 - v2.1.101 ([source](#))
`[CODE]`

`/team-onboarding` generates teammate ramp-up guide from your local usage, OS CA certificate store trusted by default, `/ultraplan` auto-creates cloud environment, improved brief mode retry logic.

**How to use:** Run `/team-onboarding` to produce a markdown ramp-up doc tailored to your codebase usage patterns.

#### 2026-04-09 - v2.1.98 ([source](#))
`[CODE]`

Interactive Vertex AI setup wizard, `CLAUDE_CODE_PERFORCE_MODE` env var for Perforce support, Monitor tool for streaming background script events, subprocess sandboxing with PID namespace on Linux.

**How to use:** Run `/setup-vertex` for the wizard. Set `CLAUDE_CODE_PERFORCE_MODE=1` if you use Perforce. Linux users get tighter subprocess isolation by default.

#### 2026-04-08 - v2.1.97 ([source](#))
`[CODE]`

Focus view toggle in `NO_FLICKER` mode, `refreshInterval` status line setting for periodic command re-runs.

**How to use:** Set `refreshInterval` in your status line config to auto-refresh expensive checks.

#### 2026-01-01 - v2.1.92 → v2.1.96 ([source](#))
`[NEWS]`

`forceRemoteSettingsRefresh` fail-closed remote config, interactive Bedrock setup wizard, per-model and cache-hit breakdown in `/cost`, `/release-notes` as interactive version picker. Mantle-routed Bedrock via `CLAUDE_CODE_USE_MANTLE=1`. Default effort bumped to `high` for most tiers. Fixed Bedrock auth failures with `AWS_BEARER_TOKEN_BEDROCK`.

#### 2026-01-01 - v2.1.85 → v2.1.91 ([source](#))
`[NEWS]`

Opening week. `CLAUDE_CODE_MCP_SERVER_NAME/URL`, conditional `if` field for hooks, session-id headers, `.jj` and `.sl` excluded from VCS scans. Cowork Dispatch message delivery fixed. MCP tool result persistence overrides. `disableSkillShellExecution` locks down inline shell. Plugins can ship binaries under `bin/`. `/powerup` feature lessons. Rate-limit infinite loop fixed. “defer” permission decisions for PreToolUse hooks in headless mode. `CLAUDE_CODE_NO_FLICKER=1` for alt-screen rendering. `PermissionDenied` hook after auto-mode denials. Named subagents in `@` mentions.

## D. Claude Apps

*Cowork went generally available on macOS and Windows after a long beta. Computer use opened in research preview to Pro and Max plans.*

#### 2026-04-16 - Opus 4.7 in Claude apps ([source](#))
`[APPS]`

Opus 4.7 available across web, mobile, and desktop with vision and SWE improvements.

**How to use:** Update mobile/desktop. Web auto-uses latest. Select Opus 4.7 in the model picker.

#### 2026-04-09 - Claude Cowork — GA on macOS and Windows ([source](#))
`[APPS]`

Cowork out of beta. RBAC for Enterprise plans, OpenTelemetry support, Cowork analytics in the Analytics API, custom roles per group.

**How to use:** Enterprise admins: configure groups and assign roles in Console. Pipe Cowork telemetry to your existing observability stack via OTel.

#### 2026-03-25 - Interactive apps in Claude mobile (iOS / Android) ([source](#))
`[APPS]`

Live charts, sketches, and shareable assets render visually in conversations.

**How to use:** Update the iOS/Android app. Visualizations now render inline.

#### 2026-03-23 - Computer use research preview for Pro / Max ([source](#))
`[NEWS]`

Claude can access screens and perform tasks independently. Plus Claude Code Dispatch improvements.

**How to use:** Pro/Max users opt in to the computer use preview from settings. Read the computer use guide before granting screen access.

#### 2026-03-17 - Persistent agent thread for Cowork on mobile ([source](#))
`[APPS]`

Manage Cowork tasks from phones via Claude Desktop or mobile.

**How to use:** Cowork tasks now persist across mobile sessions — no need to start fresh.

#### 2026-01-01 - Inline charts · Claude for Excel and PowerPoint enhancements ([source](#))
`[NEWS]`

Claude creates custom charts and diagrams inline in responses on web. Excel and PowerPoint add-ins share conversation context across docs, support skills, and connect to Bedrock / Vertex AI / Foundry via LLM gateway.

**How to use:** Update the add-ins. Skills authored in Console show up inside Excel/PowerPoint.

## E. Agent SDKs · Python + TypeScript

*Twenty SDK releases — ten Python, ten TypeScript. Opus 4.7 support, distributed tracing helpers, and a security update worth installing.*

#### 2026-04-16 - claude-agent-sdk v0.1.60 ([source](#))
`[NEWS]`

`list_subagents()` and `get_subagent_messages()` session helpers, W3C trace context propagation to CLI subprocess (OpenTelemetry), cascading session deletion. Bug fix: `setting_sources=[]` no longer silently dropped. Bundled CLI to v2.1.111.

**How to use:** `pip install -U "claude-agent-sdk[otel]"` for distributed tracing.

#### 2026-04-16 - @anthropic-ai/claude-agent-sdk v0.2.111 ([source](#))
`[NEWS]`

Opus 4.7 support, `mcp_set_servers` per-tool `permission_policy` for HTTP/SSE servers, `startup()` and `WarmQuery` now public API, `options.env` overlays `process.env` instead of replacing.

**How to use:** `npm install -D @anthropic-ai/claude-agent-sdk@latest`. Use `WarmQuery` for pre-warmed sessions.

#### 2026-04-10 - @anthropic-ai/claude-agent-sdk v0.2.101 ([source](#))
`[NEWS]`

Security: bumped `@anthropic-ai/sdk` to `^0.81.0` and `@modelcontextprotocol/sdk` to `^1.29.0` (GHSA-5474-4w2j-mq4c). Fixed Windows resume-session temp directory leak. Fixed `MaxListenersExceededWarning` with 11+ concurrent `query()` calls.

**How to use:** Security update — upgrade. `npm update @anthropic-ai/claude-agent-sdk`.

#### 2026-04-09 - claude-agent-sdk v0.1.57 · v0.1.58 ([source](#))
`[NEWS]`

`exclude_dynamic_sections` option on `SystemPromptPreset` for cross-user cache hits, `"auto"` PermissionMode, fixed `thinking={"type":"adaptive"}` mapping. Bundled CLI to v2.1.97.

**How to use:** Use `exclude_dynamic_sections=True` to maximize cache hits across users with different dynamic content.

#### 2026-01-01 - claude-agent-sdk v0.1.52 → v0.1.56 ([source](#))
`[NEWS]`

`get_context_usage()` on `ClaudeSDKClient`. `typing.Annotated` parameter descriptions in JSON schema. `ToolPermissionContext` exposes `tool_use_id` and `agent_id`. `session_id` option on `ClaudeAgentOptions`. Fixed `--setting-sources` empty string when not provided. Fixed `query()` deadlock with string prompt + hooks/MCP. Fixed silent truncation of MCP tool results >50K chars.

#### 2026-03-27 - claude-agent-sdk v0.1.51 ([source](#))
`[NEWS]`

`fork_session()`, `delete_session()`, offset-based pagination, `task_budget` option, `SystemPromptFile` support, AgentDefinition gets `disallowedTools` / `maxTurns` / `initialPrompt`. Plus 10+ fixes to async generator cleanup, MCP tool handling, env filtering, process cleanup.

**How to use:** Use `fork_session(session_id)` to branch a session. Pass `task_budget={"input_tokens": N}` to cap a run.

#### 2026-01-01 - @anthropic-ai/claude-agent-sdk v0.2.97 → v0.2.110 ([source](#))
`[NEWS]`

Parity with Claude Code v2.1.97 through v2.1.110. `SDKStatus` includes `'requesting'`. `system/memory_recall` event. `memory_paths` on `system/init`. `unstable_v2_createSession` now respects `cwd` / `settingSources` / `allowDangerouslySkipPermissions`. New `shouldQuery: false` field on `SDKUserMessage` to append without triggering a turn.

**How to use:** Send `{ shouldQuery: false }` to inject context without burning a model turn. Subscribe to `system/memory_recall` events to see when the agent reads from memory.

## F. Research & Publications

*Two papers worth a Friday — automated alignment researchers, and the internal representations of emotion concepts in Claude.*

#### 2026-04-14 - Automated Alignment Researchers (paper) ([source](#))
`[RESEARCH]`

“Using large language models to scale scalable oversight.” Anthropic on having LLMs perform alignment work, with benchmarks for whether the technique holds.

**How to use:** Read the paper if you work on agent guardrails. Citations are useful for justifying LLM-based eval pipelines.

**Why it matters:** Same week Anthropic held Mythos back for safety, they're publishing on automating the safety work itself. The two are connected.

#### 2026-01-01 - Emotion Concepts in Large Language Models (transformer-circuits.pub) ([source](#))
`[RESEARCH]`

Internal representations of emotions in Claude that generalize across contexts and shape behavior.

**Why it matters:** The wrong question is whether the models have emotions. The right one is whether they have coherent internal representations that change output.

## G. News & Partnerships

*Glasswing launched with twelve founding orgs and $100M in model credits. Vas Narasimhan joined the Long-Term Benefit Trust board.*

#### 2026-04-14 - Vas Narasimhan appointed to Long-Term Benefit Trust Board ([source](#))
`[NEWS]`

The LTBT appointed Vas Narasimhan (former Novartis CEO) to the Board of Directors.

**Why it matters:** Adds pharma-and-policy weight to Anthropic governance. Worth watching for biotech and regulated-industry deal flow.

#### 2026-04-07 - Project Glasswing launched ([source](#))
`[NEWS]`

12-organization consortium using Claude Mythos Preview to harden critical software infrastructure. Founders: AWS, Apple, Google, Microsoft, NVIDIA, Cisco, CrowdStrike, JPMorgan Chase, Linux Foundation, Palo Alto Networks, Broadcom, Anthropic. $100M in model credits. $4M to OpenSSF, Apache, Alpha-Omega.

**How to use:** Open-source maintainers of critical infrastructure can apply for Mythos access via Glasswing partners. Participation by application.

**Why it matters:** First time Anthropic explicitly held a model back, post-evaluation, on safety grounds that survived peer review. Sets a precedent.
