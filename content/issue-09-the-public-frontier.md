---
issue: 09
slug: the-public-frontier
title: "The Public Frontier"
date: 2026-06-12
period: 2026-06-06 to 2026-06-12
masthead: Shipped.
deck: "The first Mythos-class model went public, priced, and free for three weeks. Anthropic narrated the danger in the same breath."
byline: Edited by Eddie Belaval. Reported with the assistance of Claude.
term_of_issue: The Unlock
status: draft
ship_date: 2026-06-12
running_order_locked: true
fob_content: editorial
log_content: reference
---

# Shipped.

**Issue #09: The Public Frontier**
*A magazine of what Anthropic ships.*
*Period: 2026-06-06 to 2026-06-12. Volume I.*

---

## The Open

For most of a year, "Mythos-class" was the model you couldn't have. Anthropic said it in past flagship launches: a stronger thing exists, and it stays behind glass. The capability ceiling sat there, real and locked, a fact you planned around rather than a model you called.

On June 9, the lock came off the public side. `claude-fable-5` went generally available. No preview, no waitlist, no "rolling out to select customers." Ten dollars per million input tokens. Free on every paid seat through June 22. Generally available on Amazon Bedrock and selectable inside GitHub Copilot the same day.

Then, in the same week, Anthropic committed $350 million to the question of what its own models do to the labor market, and Dario Amodei published an essay sketching government responses to AI-driven unemployment that run all the way to universal basic income. DXC put Fable 5 at the center of the infrastructure that runs banks and airlines. Apple let you set Claude as the brain behind Siri. And four Claude Code patches quietly tightened who, inside a company, is even allowed to call the new ceiling.

Ship the frontier. Narrate the risk. Same breath.

---

---

## The Lead Story

# The unlock

The frontier had a tell this week, and for once it wasn't a benchmark. It was a release channel.

On June 9, Anthropic put `claude-fable-5` into general release. It's the first Mythos-class model anyone outside Project Glasswing can actually call ([Anthropic](https://www.anthropic.com/news/claude-fable-5-mythos-5)). No preview, no waitlist, no "rolling out to select customers." It leads SWE-Bench Pro by double digits over the next model, clears Opus 4.8 by more than two to one on FrontierCode Diamond, and on spatial reasoning nearly tripled Opus 4.8's score. The benchmark line that lands hardest isn't a benchmark at all: Stripe estimated two-plus months of engineering for a 50-million-line Ruby migration; Fable 5 finished it in a day. Pricing is $10 input / $50 output per million tokens, with a large output headroom and a one-million-token context window by default.

Look at the mechanism, because the mechanism is the story. What's public is Fable 5: Mythos-class intelligence with safeguards on, routing roughly one session in twenty to Opus 4.8 when a query hits high-risk ground like cybersecurity or biology. Less than 5% of sessions ever touch the fallback. The fuller Mythos 5 is the same model with some of those safeguards lifted, and it stays behind glass: limited access through Project Glasswing for authorized cyberdefenders and infrastructure providers. One door opened, with a price tag stapled to it. The other stayed shut. AWS, carrying it on Bedrock the same day, described it in its own words as "Mythos-class capabilities with built-in safeguards," which is the polite way of saying the dangerous version is real and you're not getting it.

The number that matters, though, isn't the $50 output rate. It's June 22. Anthropic handed every Pro, Max, Team, and Enterprise seat three free weeks on its most capable public model, which is exactly what you do when you want today's ceiling to become tomorrow's floor before anyone's paying for it. The blast radius is everyone with a paid seat and a hard problem: for three weeks the strongest model Anthropic sells is sitting inside your existing subscription, and the rational move is to throw your gnarliest migration, your worst legacy codebase, your hardest agent run at it now and find out what it can do on someone else's dime. Three free weeks is how you make a frontier feel ordinary, then start the meter.

And read the timing, because the timing is the posture. TechCrunch put it flat: Anthropic shipped its most powerful public model within days of warning that AI is getting too dangerous. The company isn't hiding that seam. It is the seam. The same week it priced the frontier, it committed $350 million to studying what the frontier does to jobs and stood up a fellowship to soften the landing (see Also Shipped). Set Fable 5 against the field and the contrast sharpens: when a rival lab ships a flagship, the press release is a victory lap. When Anthropic ships its strongest public model, the press release is half victory lap, half warning label, and the warning is load-bearing. Agree or don't; that contradiction is the whole of Anthropic's June.

If you build on this, mind two clocks. The free window shuts June 22. And the 4-series you may still be pinned to (`claude-sonnet-4-20250514`, `claude-opus-4-20250514`) retires June 15. Production pinned to either ID starts returning errors on Sunday. Sequence it: clear the retiring IDs first, migrate to `claude-sonnet-4-6` and `claude-opus-4-7`, then chase the capability upgrade, so a blown deadline can't take you down. Some of you have two migrations this week, not one.

The model you couldn't buy is now the model you can't avoid.

---

---

## Investigation

# The other side of the ledger

Ship the frontier, narrate the risk. The Lead is the first half. This is the second, and it cost $350 million.

Start with the sequence, because Anthropic chose it deliberately. June 9: the most capable public model goes on sale. June 10: the mitigation spend starts. The company committed nine figures to an Economic Futures Research Fund, backing trials and policy evaluations on what AI does to work, and Dario Amodei published a policy essay alongside it ([Anthropic](https://www.anthropic.com/research/economic-policy-responses)). The essay doesn't hedge. It proposes tiered government responses keyed to AI-driven unemployment at 5%, 10%, and "unprecedented" levels, the top tier reaching for universal basic income and equity-sharing frameworks. A frontier lab's CEO sketching the welfare state you'd need if his own product worked too well is not a press release. It's a hedge against his own success, written down.

The same drop carried an Advanced AI Framework: a proposal for mandatory testing, independent evaluation, and civil penalties tied to global revenue for frontier model developers. Read that against the model that shipped the day before. Anthropic priced the frontier on Tuesday and on Wednesday asked governments to fine companies like Anthropic, by a percentage of revenue, if they ship frontier models recklessly. You can call that principled. You can call it regulatory capture with a conscience. Both readings survive contact with the facts, and Anthropic seems content to let both stand.

June 11 put a face on the dollars. Claude Corps is a $150 million national fellowship placing 1,000 trained early-career workers inside US nonprofits for a year at $85,000 each plus benefits ([Anthropic](https://www.anthropic.com/news/claude-corps)). The first cohort of 100 starts in October 2026; applications close July 17; no degree required, just over 18, under two years of full-time work experience, and authorization to work in the US. Over 400 nonprofits host in year one, run alongside CodePath and Social Finance. The design is pointed: the cohort is exactly the demographic most exposed to entry-level automation, placed in the part of the economy least able to buy the tools that displace them. Fund the research that measures the damage, then fund the people the damage lands on first.

The pattern is what's new, not the giving. Labs have written checks to nonprofits before; AI companies fund safety institutes as a matter of routine. What hadn't happened until this week is a lab tying a specific dollar figure to economic mitigation inside the same news cycle as a capability launch. $350 million across two days, stapled to the GA of its strongest public model. The reading, stated plainly: Anthropic has decided the honest posture and the marketable posture are the same posture, and that admitting the danger out loud is cheaper than being caught having hidden it. Whether $350 million is a serious down payment on a labor shock or a rounding error against a multibillion-dollar run rate is the question the fund itself was built to answer, and the answer won't arrive on Anthropic's schedule.

The builder's move here is smaller than the dollar figures and more useful. Watch what Anthropic funds, not what it says. The Economic Futures Fund will publish; when it does, it will be the closest thing to a real measurement of which jobs the models you're deploying actually move. That data is worth more to anyone building on this platform than the essay that announced it.

---

## Also Shipped

### A scheduler and a vault for the agent platform

Managed Agents (public beta) stopped being a demo this week. **Cron scheduling** binds an agent to a schedule on the Claude Platform so it fires on its own. Add `cron_schedule` to the definition: no external trigger, no cron box to babysit ([IT Brief](https://itbrief.news)). The quieter half is the better half: a **credential vault** moves secrets out of the system prompt down to the network boundary, binding a key only on outbound requests to a domain you allowlisted, never entering model context. That is the gap between "the model could leak my key" and "the model never sees the key." A scheduler plus a credential boundary plus no separate scheduler fee is the spine of an always-on agent runtime, shipped as two features.

### Claude in your iPhone, and a Swift package to match

Apple opened WWDC 2026 on June 8 with iOS 27's Extensions framework: users can designate Claude, Gemini, or ChatGPT as the AI engine for Siri, Writing Tools, and Image Playground ([Tom's Guide](https://www.tomsguide.com/news/live/wwdc-2026-live-news-updates)). Gemini holds the native default on a reported $1 billion Apple-Google contract; Claude arrives as a user-installed extension layered on top. The day after, Anthropic shipped the developer-side answer: a Swift package making Claude a server-side model in Apple's Foundation Models framework, conforming to the `LanguageModel` protocol so it drops in alongside Apple's on-device model ([Anthropic](https://claude.com/blog/claude-for-foundation-models)). Gemini gets the default. Claude gets the reach, and the SDK to use it.

### $350 million on the other side of the ledger

The day Fable 5 went general, the mitigation spend started. On June 10, Anthropic committed nine figures to an Economic Futures Research Fund and Amodei published a policy essay proposing tiered government responses at 5%, 10%, and "unprecedented" AI-driven unemployment, up to universal basic income and equity-sharing ([Anthropic](https://www.anthropic.com/research/economic-policy-responses)). On June 11 came Claude Corps: a $150 million national fellowship placing 1,000 trained early-career workers inside US nonprofits for a year at $85,000 each ([Anthropic](https://www.anthropic.com/news/claude-corps)). First cohort of 100 starts in October 2026; applications close July 17; no degree required. It's the first time Anthropic has tied a dollar figure to economic mitigation in the same news cycle as a capability launch.

### DXC puts Claude at the center of what it sells

On June 11, DXC Technology, the managed-services firm running back-office infrastructure for banks, airlines, insurers, and government agencies, announced a multi-year global alliance with Anthropic ([Anthropic](https://www.anthropic.com/news/dxc-anthropic-alliance)). Claude wrote more than 95% of the code for DXC OASIS, its new AI-native orchestration platform, with Fable 5 as the default model. DXC tested Claude across its 115,000-person workforce in 70 countries before rolling it to clients, and is now training tens of thousands of Claude-certified forward-deployed engineers to install Claude inside the systems regulated industries have trusted for decades. Not a product launch. An established firm rebuilding what it sells around the model.

### Sub-agents that spawn sub-agents

Claude Code shipped Fable 5 access in v2.1.170 (June 9) and fixed a real papercut: sessions launched from the VS Code integrated terminal weren't saving transcripts, so work was quietly evaporating for the IDE crowd ([GitHub](https://github.com/anthropics/claude-code/releases)). Then v2.1.172 did the structural thing: **sub-agents can now spawn their own sub-agents, up to five levels deep.** A flat fan-out becomes a real tree, an orchestrator delegating to delegators. Powerful, and worth one word of restraint: five levels of recursion is five levels of token spend and five layers to debug. Reach for the depth only when the work genuinely nests.

---

## Quiet on the Wire

Watch the retirement clock. `claude-sonnet-4-20250514` and `claude-opus-4-20250514` retire **June 15**. Production pinned to either ID starts returning errors on Sunday. Migrate to `claude-sonnet-4-6` and `claude-opus-4-7` first. If you're also moving to Fable 5, sequence it: clear the retiring IDs before chasing the capability upgrade, so a blown deadline can't take you down. Two clocks, one week. And the calendar's already crowded: the free Fable 5 window shuts June 22.

---

## Term of the Issue

# The Unlock

**The unlock** /ðiː ˈʌn.lɒk/ *noun*

The moment a held-back capability ceiling becomes a priced, generally available floor. Not a launch. A launch ships something new; an unlock makes public the thing that already existed and was deliberately withheld, usually with a free-access window engineered to turn a frontier into a baseline before the meter starts.

**First observable** 2026-06-09, when the first Mythos-class model, `claude-fable-5`, went generally available at $10 per million input tokens, free on paid seats through June 22, while the fuller Mythos 5 stayed behind glass.

**Usage** *"The model wasn't announced. It was unlocked, and you have until June 22 before it costs you."*

---

## The Close

The model you couldn't have went on sale.
The danger got narrated in the same breath.
The lock came off one door.

---

## A. Models

*1 entry in window.*

#### 2026-06-09 — Claude Fable 5 and Claude Mythos 5 ([Anthropic](https://www.anthropic.com/news/claude-fable-5-mythos-5))
`[MODEL]`
First Mythos-class model in general release. Model ID `claude-fable-5`, $10 input / $50 output per MTok. Safeguards fire in under 5% of sessions; affected queries fall back to Opus 4.8. Benchmarks: SWE-Bench Pro 80.3%, eleven points clear of the next model, FrontierCode Diamond 29.3% vs Opus 4.8's 13.4%, spatial reasoning nearly tripled over Opus 4.8. Available on Claude API, Bedrock, and Vertex (Foundry to follow); free on Pro, Max, Team, and Enterprise through June 22, 2026, then usage credits. Claude Mythos 5 is the same model with some safeguards lifted, deployed through Project Glasswing for authorized cyberdefenders and infrastructure providers in limited access.

**How to use:** Pass `model="claude-fable-5"`. Re-tune prompts — the capability jump over prior flagships is significant. Pricing unchanged from Fable 5 Preview tiers.

## B. API & Platform

*1 entry in window.*

#### 2026-06-09 — Managed Agents: cron schedules and credential vaults (public beta) ([IT Brief](https://itbrief.news))
`[API]`
Managed Agents gained cron-based scheduling: attach an agent to a schedule on the Claude Platform and it fires automatically. Credential vault integration keeps secrets out of model context entirely, binding keys at the network boundary only on requests to customer-allowlisted domains. No separate scheduler fee; billed through existing Claude Platform usage.

**How to use:** Add `cron_schedule` to your agent definition. Store credentials in the platform vault rather than the system prompt; see Claude Platform docs for vault allowlist configuration.

## C. Claude Code

*9 entries in window.*

#### 2026-06-12 — Claude Code v2.1.175 ([release](https://github.com/anthropics/claude-code/releases))
`[CODE]`
Added `enforceAvailableModels` managed setting: when enabled, the `availableModels` allowlist also governs which model `Default` resolves to, giving organizations tighter control over which models org members can access.

**How to use:** Set `enforceAvailableModels: true` in managed settings; `Default` selection is then constrained to your `availableModels` allowlist. Update via `claude update`.

#### 2026-06-12 — Claude Code v2.1.174 ([release](https://github.com/anthropics/claude-code/releases))
`[CODE]`
Added `wheelScrollAccelerationEnabled` setting to disable mouse-wheel scroll acceleration in fullscreen mode. Fixed the `/model` picker hiding the model family that `Default` resolves to.

#### 2026-06-11 — Claude Code v2.1.173 ([release](https://github.com/anthropics/claude-code/releases/tag/v2.1.173))
`[CODE]`
Fable 5 model names with a `[1m]` suffix are now normalized automatically: Fable 5 ships with 1M context by default, and the suffix was causing match failures. Fixed a spurious "sandbox dependencies missing" startup warning on Windows when sandbox was enabled. Thinking summaries in collapsed groups now render as markdown, stay visible at least 3 seconds, and cap at 10 lines; the fullscreen "Thinking for Ns" indicator counts up live while the model is active.

**How to use:** `claude update` or reinstall via npm. Model-name normalization is automatic.

#### 2026-06-10 — Claude Code v2.1.172 ([release](https://github.com/anthropics/claude-code/releases/tag/v2.1.172))
`[CODE]`
Sub-agents can now spawn their own sub-agents, up to 5 levels deep. Amazon Bedrock reads the AWS region from `~/.aws` config when `AWS_REGION` is unset, matching AWS SDK precedence (`/status` shows the source). Added a search bar to the `/plugin` marketplace browser. Added a `model` attribute to the `claude_code.lines_of_code.count` OTEL metric. Fixed sessions using 1M context without usage credits getting permanently stuck (they now auto-compact under the standard limit), JetBrains terminal flicker, Shift+non-ASCII drops in Kitty-protocol terminals, and a PowerShell command-validation hang on Windows. Reduced idle CPU; improved performance in long conversations.

**How to use:** `claude update`. Sub-agent nesting and Bedrock region fallback are on by default.

#### 2026-06-09 — Claude Code v2.1.170 ([release](https://github.com/anthropics/claude-code/releases))
`[CODE]`
Adds Fable 5 access. Fixed session-transcript saving for sessions launched from the VS Code integrated terminal or shells with inherited Claude Code environment variables (they now appear in `--resume`).

**How to use:** `claude update` or reinstall.

#### 2026-06-08 — Claude Code v2.1.169 ([release](https://github.com/anthropics/claude-code/releases))
`[CODE]`
New `--safe-mode` flag (and `CLAUDE_CODE_SAFE_MODE` env var) disables all customizations (CLAUDE.md, plugins, skills, hooks, MCP servers) for clean troubleshooting. `/cd` moves a session to a new working directory without breaking the prompt cache. `disableBundledSkills` hides bundled skills and slash commands from the model. Fixes: enterprise MCP policy enforcement on reconnect, arrow navigation in long wrapped lines, a macOS UI stall for claude.ai-authenticated users, Windows slash-command scan slowness, Remote Control stuck "reconnecting" after resume, Git Credential Manager popups on Windows startup, background agents ignoring project-level env values, untrusted project settings bypassing OTEL trust confirmation. Restored the 5-minute idle timeout on Vertex/Foundry.

**How to use:** `claude update`. Set `CLAUDE_CODE_SAFE_MODE=1` to enforce safe mode in all sessions; `API_FORCE_IDLE_TIMEOUT=0` to opt out of the Vertex/Foundry idle timeout.

#### 2026-06-06 — Claude Code v2.1.166 ([release](https://github.com/anthropics/claude-code/releases))
`[CODE]`
Adds the `fallbackModel` setting to configure up to three fallback models when the primary is overloaded or unavailable. Also: glob-pattern support in deny rules, hardened cross-session messaging, improved thinking-token handling.

**How to use:** `claude update`. Set `fallbackModel` in project or user config to name up to three backup models in priority order.

#### 2026-06-06 — Claude Code v2.1.167 ([release](https://github.com/anthropics/claude-code/releases))
`[CODE]`
Bug fixes and reliability improvements. No feature changes. (v2.1.168 followed the same day at 23:41 UTC with further fixes.)

#### 2026-06-05 — Claude Code v2.1.165 ([release](https://github.com/anthropics/claude-code/releases))
`[CODE]`
Bug fixes and reliability improvements. No feature changes.

## D. Claude Apps

*1 entry in window.*

#### 2026-06-09 — Claude for Apple Foundation Models framework ([claude.com](https://claude.com/blog/claude-for-foundation-models))
`[APPS]`
A Swift package that makes Claude available as a server-side language model in Apple's Foundation Models framework. Conforms to the `LanguageModel` protocol so developers drive it with `LanguageModelSession` alongside Apple's on-device model. Supports multi-step reasoning, code generation, web search, code execution, and SwiftUI streaming. Targets iOS 27, iPadOS 27, macOS 27, visionOS 27, watchOS 27. Announced June 9, available the next day.

**How to use:** Add the Swift package; see the [Apple Foundation Models library docs](https://platform.claude.com/docs/en/cli-sdks-libraries/libraries/apple-foundation-models).

## E. Agent SDKs

*8 entries in window.*

#### 2026-06-09 — anthropic-sdk-python v0.108.0 ([GitHub](https://github.com/anthropics/anthropic-sdk-python/releases))
`[SDK-PY]`
Adds `claude-fable-5` and `claude-mythos-5` model identifiers. Adds server-side fallbacks on refusal and a client-side fallbacks middleware for providers that don't support server-side fallbacks.

**How to use:** `pip install anthropic==0.108.0`

#### 2026-06-09 — anthropic-sdk-python v0.109.0 ([GitHub](https://github.com/anthropics/anthropic-sdk-python/releases))
`[SDK-PY]`
Adds support for Managed Agents deployments and environment-variable credentials.

**How to use:** `pip install anthropic==0.109.0`

#### 2026-06-09 — anthropic-sdk-python v0.109.1 ([GitHub](https://github.com/anthropics/anthropic-sdk-python/releases))
`[SDK-PY]`
Bug fix: adds the `frontier_llm` refusal category.

**How to use:** `pip install anthropic==0.109.1`

#### 2026-06-09 — anthropic-sdk-typescript v0.103.0 plus platform SDKs ([GitHub](https://github.com/anthropics/anthropic-sdk-typescript/releases))
`[SDK-TS]`
Core: adds `claude-fable-5` and `claude-mythos-5` model identifiers, server-side fallbacks on refusal, client-side fallbacks middleware, and `ctx.logger` in middleware. Platform SDKs vertex-sdk v0.17.1, foundry-sdk v0.3.1, bedrock-sdk v0.30.2, and aws-sdk v0.4.2 all fix third-party middleware ordering.

**How to use:** `npm install @anthropic-ai/sdk@0.103.0`

#### 2026-06-09 — anthropic-sdk-typescript v0.104.0 ([GitHub](https://github.com/anthropics/anthropic-sdk-typescript/releases))
`[SDK-TS]`
Adds support for Managed Agents deployments and environment-variable credentials.

**How to use:** `npm install @anthropic-ai/sdk@0.104.0`

#### 2026-06-09 — anthropic-sdk-typescript v0.104.1 ([GitHub](https://github.com/anthropics/anthropic-sdk-typescript/releases))
`[SDK-TS]`
Bug fix: adds the `frontier_llm` refusal category.

**How to use:** `npm install @anthropic-ai/sdk@0.104.1`

#### 2026-06-07 — anthropic-sdk-python v0.107.1 ([GitHub](https://github.com/anthropics/anthropic-sdk-python/releases/tag/v0.107.1))
`[SDK-PY]`
Bug fix: the Foundry client was not sending the `x-api-key` header for API-key authentication, so operators running Claude on Foundry infrastructure with API keys were failing to authenticate. Released 17:18 UTC.

**How to use:** `pip install --upgrade anthropic`

#### 2026-06-06 — anthropic-sdk-python v0.107.0 / anthropic-sdk-typescript v0.102.0 ([GitHub](https://github.com/anthropics/anthropic-sdk-typescript/releases))
`[SDK-PY]` `[SDK-TS]`
Small updates to Managed Agents types in both SDKs. The TypeScript drop (with bedrock-sdk v0.30.1 and aws-sdk v0.4.1) fixes middleware to run before request signing rather than after.

**How to use:** `pip install --upgrade anthropic` / `npm install @anthropic-ai/sdk@latest`

## F. Research & Publications

*1 entry in window.*

#### 2026-06-05 — Making Claude a chemist ([Anthropic](https://www.anthropic.com/research/making-claude-a-chemist))
`[RESEARCH]`
Opus 4.7 evaluated against NMR spectroscopy — reading spectra to infer molecular structure, the analytical step chemists run before any synthesis. The model matches dedicated NMR software and beats it on some tasks. Evaluation led by Anthropic chemist David Kamber. Scope is intentionally narrow: one lab workflow, not a general chemistry credential; the goal is mapping where a general model can displace a specialist tool.

## G. News & Partnerships

*4 entries in window.*

#### 2026-06-11 — DXC Technology multi-year global alliance ([Anthropic](https://www.anthropic.com/news/dxc-anthropic-alliance))
`[NEWS]`
DXC Technology will integrate Claude into the enterprise systems banks, airlines, insurers, manufacturers, and government agencies have relied on for decades. DXC tested Claude across its 115,000-person workforce in 70 countries before rolling out to clients, and collaborated with Claude to write more than 95% of the code for DXC OASIS, its AI-native orchestration platform, with Fable 5 as the default foundation model. DXC is training tens of thousands of Claude-certified forward-deployed engineers.

#### 2026-06-11 — Claude Corps ([Anthropic](https://www.anthropic.com/news/claude-corps))
`[NEWS]`
A $150 million national fellowship placing 1,000 trained fellows inside US nonprofits for one year at $85,000 each plus benefits. First cohort of 100 starts in October 2026; applications close July 17. No degree required: over 18, under two years of full-time work experience, authorized to work in the US. Managed with CodePath and Social Finance, with over 400 nonprofits hosting in year one. Part of a $350 million total social spend announced across two days.

#### 2026-06-10 — Economic Futures Research Fund and policy frameworks ([Anthropic](https://www.anthropic.com/research/economic-policy-responses))
`[NEWS]`
Anthropic committed nine figures to an Economic Futures Research Fund backing trials and policy evaluations on AI's effects on work. Dario Amodei simultaneously published an economic-policy essay proposing tiered government responses at 5%, 10%, and "unprecedented" AI-driven unemployment levels, up to universal basic income and equity-sharing frameworks. Anthropic also published an Advanced AI Framework proposing mandatory testing, independent evaluation, and civil penalties tied to global revenue for frontier model developers.

**Why it matters:** The $350 million combined spend across June 10–11 is the first time Anthropic has tied a dollar figure to economic mitigation alongside a capability launch in the same news cycle.

#### 2026-06-08 — Apple WWDC 2026: iOS 27 Extensions bring Claude to Siri ([Tom's Guide](https://www.tomsguide.com/news/live/wwdc-2026-live-news-updates))
`[NEWS]`
iOS 27 introduces an Extensions framework letting users select Claude, Gemini, or ChatGPT as the AI model for Siri, Writing Tools, and Image Playground. Gemini is the native default, backed by a reported $1 billion annual Apple-Google contract; Claude and ChatGPT arrive as user-installed extensions, activated in Settings under Apple Intelligence. iOS 27, iPadOS 27, and macOS 27 ship fall 2026. Also reported by [TechTimes](https://www.techtimes.com/articles/317985/20260608/apple-wwdc-2026-siri-rebuilt-gemini-homeos-previewed-cook-farewell-keynote.htm).

#### 2026-06-09 — Claude Fable 5 on GitHub Copilot and Amazon Bedrock ([GitHub Changelog](https://github.blog/changelog/2026-06-09-claude-fable-5-is-generally-available-for-github-copilot/))
`[NEWS]`
GitHub Copilot subscribers can select Claude Fable 5 as their model in the Copilot interface as of June 9. Fable 5 is also generally available through Amazon Bedrock, which describes it as "Mythos-class capabilities with built-in safeguards" ([AWS](https://aws.amazon.com/blogs/aws/anthropic-claude-fable-5-on-aws-mythos-class-capabilities-with-built-in-safeguards-now-available/)).
