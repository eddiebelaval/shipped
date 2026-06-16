---
issue: 10
slug: the-kill-switch
title: "The Kill Switch"
date: 2026-06-16
period: 2026-06-13 to 2026-06-16
masthead: Shipped.
deck: "Seventy-two hours after Fable 5 and Mythos 5 went public, a letter from Commerce took them offline for every customer on earth."
byline: Edited by Eddie Belaval. Reported with the assistance of Claude.
term_of_issue: The Grounding
status: draft
ship_date: 2026-06-16
running_order_locked: true
fob_content: editorial
log_content: reference
---

# Shipped.

**Issue #10: The Kill Switch**
*A magazine of what Anthropic ships.*
*Period: 2026-06-13 to 2026-06-16. Volume I.*

---

## The Open

Last week the story was a price. The most capable public model anyone could call went generally available, free for three weeks, and the only clock that mattered was the one counting down to the meter.

This week the clock got pulled out of the wall.

A letter reached Dario Amodei on a Thursday evening. By the time the weekend was over, Fable 5 and Mythos 5 were dark for every customer on the planet, and a company that had spent the spring narrating the danger of its own frontier found the government narrating it back. Three days from general availability to global suspension. The frontier didn't slow down. It got switched off.

---

---

## The Lead Story

# The letter that turned off the frontier

The most consequential thing that happened to Anthropic this week was not something it shipped. It was something it had to un-ship.

On the evening of Thursday, June 12, Commerce Secretary Howard Lutnick sent Anthropic an export control directive ordering it to suspend all access to Fable 5 and Mythos 5 for any foreign national, inside or outside the United States, including Anthropic's own foreign-national employees. Anthropic received the directive at 5:21pm ET and says the letter gave no specific details of the national security concern behind it ([Anthropic](https://www.anthropic.com/news/fable-mythos-access)). The scope was the problem. A restriction that follows a nationality everywhere, employees included, cannot be enforced with a regional toggle. So Anthropic did the only thing the order left it room to do: it disabled both models for every customer worldwide. All other Claude models stayed up.

The trigger, per Axios, was a claim from another company that it had jailbroken Mythos, which alarmed the administration. Anthropic's account is flatter. It says it reviewed a demonstration of the technique, that it surfaced a small number of previously known, minor vulnerabilities, and that other publicly available models can find the same ones without any bypass at all ([Anthropic](https://www.anthropic.com/news/fable-mythos-access)). Anthropic disputes the characterization, called the finding a misunderstanding, and promised an update. Then it went quiet and worked the phones.

Read the timing against last week. The two models went public June 9. The letter landed June 12. Three days separate the launch from the grounding, which is roughly the length of the free-access window Anthropic was using to turn a frontier into a baseline. The unlock and the kill switch are the same model, the same week apart.

By Sunday neither model was back. Senior Anthropic technical staff were headed to Washington to meet White House officials, per Axios. A Semafor report the same day added a sharper edge: the order stemmed partly from suspicion that a China-linked group had accessed the model. And the criticism arrived from inside the tent. The day after the letter, former White House AI czar David Sacks accused Anthropic of being reckless with the Fable 5 rollout. Anthropic shipped the most capable public model in the world and, within a long weekend, was defending the decision to two audiences at once: the government that pulled the plug, and the operators left staring at a dead model ID.

There is a version of this story that is about one jailbreak claim and one terse letter. The larger one is about who holds the switch. For a year the running argument was that Anthropic decided what stayed behind glass. This week a single page proved the company was never the only hand on the gate.

---

---

## Also Shipped

### What 52,000 Americans actually fear

The same day the directive landed, Anthropic published the first wave of a survey series, the Anthropic Public Record, polling nearly 52,000 Americans on how they feel about AI ([Anthropic](https://www.anthropic.com/news/anthropic-public-record)). The dominant fear, in every state, is job loss, held by 64% of respondents. Only 15% say they trust AI companies to regulate themselves. Over 70% want the government to play a role in regulating AI, with bipartisan support. The hope side is narrower and more specific: 48% rank curing diseases like cancer or Alzheimer's among their top three. A week that opened with the government overriding a company's own access controls is a strange week to learn that most of the country wanted the government in the room all along.

### The retirement clock ran out

The deadline that has been on the calendar since April finally hit. On June 15, `claude-sonnet-4-20250514` and `claude-opus-4-20250514` reached end of life ([model deprecations](https://docs.anthropic.com/en/about-claude/model-deprecations)). Requests to those IDs now return errors. The migration is a one-line change: move to `claude-sonnet-4-6` for Sonnet and `claude-opus-4-8` for Opus. If you were still pinned to a 4-series ID this week, your week had two outages on it, one ordered by Commerce and one written into your own dependency file in April.

### Programmatic usage gets its own meter

The other thing that hit June 15 was a billing line, not a model. The restructuring Anthropic announced in May went live: Agent SDK and headless `claude -p` calls now draw from a dedicated monthly credit metered at standard API prices, no longer sharing the subscription rate-limit pool ([Anthropic](https://www.anthropic.com/news)). Each plan tier gets its own monthly allotment, and the credits reset each cycle without rolling over. Interactive Claude Code and Claude.ai chat are untouched. The logic is clean and worth internalizing before your next invoice: a human at a terminal is a subscription, an agent in a loop is metered.

### Claude Code keeps its own counsel

While the front page burned, the CLI kept shipping. v2.1.176 fixed a real one for the new world order: auto mode was failing on Fable 5 for organizations without Opus 4.8 enabled, and now falls back to the best available Opus ([changelog](https://code.claude.com/docs/en/changelog)). It also hardened `availableModels` so an alias pick can't redirect to a blocked model through environment variables. By June 15, v2.1.178 added `Tool(param:value)` permission rules with wildcards, so a rule like `Agent(model:opus)` can block Opus subagents outright. The drumbeat doesn't check the news.

---

## Quiet on the Wire

Quiet, this week, was the story. No new SDK feature releases of substance, no new research papers from Anthropic in the window, just the type-definition cleanups that follow a retirement: Python v0.109.2 and TypeScript v0.104.2 each stripped the dead model IDs ([Python](https://github.com/anthropics/anthropic-sdk-python/releases), [TypeScript](https://github.com/anthropics/anthropic-sdk-typescript/releases)). The loudest signal on the wire was the silence where Fable 5 used to answer. As of the weekend, the only public timeline for its return was Anthropic's promise of an update and a delegation on a train to Washington.

---

## Term of the Issue

# The Grounding

**The grounding** /ðə ˈɡraʊn.dɪŋ/ *noun*

A government-ordered, provider-executed global shutdown of a commercial AI model, in which the lab itself flips the switch to comply. Distinct from a deprecation, which the lab schedules, and a recall, which targets defects. A grounding targets access: the model still works, the company still stands behind it, and it goes dark anyway because someone with more authority than the company said so.

**First observable** 2026-06-12, when a US Commerce Department export control directive ordered Anthropic to cut off Fable 5 and Mythos 5 for all foreign nationals, and Anthropic disabled both models worldwide rather than attempt targeted enforcement.

**Usage** *"It wasn't deprecated and it wasn't recalled. It was grounded, and the lab held the switch."*

---

## The Close

The model you couldn't avoid became the model you couldn't reach.
The lab that guarded the gate learned it was never the only guard.
Three days up. Then dark.

---

## A. Models

*2 entries in window.*

#### 2026-06-15 — Sonnet 4 and Opus 4 retire ([model deprecations](https://docs.anthropic.com/en/about-claude/model-deprecations))
`[DEPRECATION]`
`claude-sonnet-4-20250514` and `claude-opus-4-20250514` reached end of life on June 15, 2026, after a 60-day notice window opened in April. Requests to these model IDs now return errors. Consumer Claude.ai and Claude Code managed environments are unaffected.

**How to use:** Migrate to `claude-sonnet-4-6` (Sonnet) and `claude-opus-4-8` (Opus) in your API calls. `claude-opus-4-1` is separately deprecated, retiring later in the summer.

#### 2026-06-12 — Fable 5 and Mythos 5 suspended worldwide ([Anthropic statement](https://www.anthropic.com/news/fable-mythos-access))
`[MODEL]`
Following a US Commerce Department export control directive received at 5:21pm ET on June 12, Anthropic disabled both Fable 5 and Mythos 5 for all customers worldwide. The directive ordered access cut off for any foreign national, inside or outside the United States, including foreign-national Anthropic employees; the breadth forced a global shutdown rather than targeted enforcement. The cited basis was a claimed jailbreak of Fable's safeguards. Anthropic reviewed a demonstration, said it surfaced only a small number of previously known minor vulnerabilities that other public models can also find without a bypass, disputed the characterization, and said it is working to restore access. All other Claude models remained available.

**Why it matters:** The first government-ordered, provider-executed global shutdown of a commercial AI model, arriving three days after general availability with no advance notice.

## B. API & Platform

*1 entry in window.*

#### 2026-06-15 — Programmatic credit billing goes live ([Anthropic](https://www.anthropic.com/news))
`[API]`
Agent SDK and headless `claude -p` usage now draws from a dedicated monthly credit metered at standard API list prices, separate from the subscription rate-limit pool. Each subscription tier carries its own monthly credit allotment; credits reset each billing cycle and do not roll over. Interactive Claude Code terminal usage and Claude.ai chat continue under standard subscription limits, unchanged. Announced in May, effective the same day as the model retirements.

**How to use:** Programmatic SDK and `claude -p` runs bill against the metered credit; interactive sessions are unaffected. Budget agent loops against the credit, not the subscription.

## C. Claude Code

*3 entries in window.*

#### 2026-06-15 — Claude Code v2.1.178 ([GitHub releases](https://github.com/anthropics/claude-code/releases))
`[CODE]`
Adds `Tool(param:value)` syntax for permission rules to match tool input parameters with wildcard support, so a rule like `Agent(model:opus)` blocks Opus subagents. Nested `.claude/skills` directories now load when working on files there, appearing as `dir:name` on name collisions, with closest-wins resolution for nested `.claude/` directories. Auto mode now classifies subagent spawns before launch. `/doctor` gets a flat tree layout with clearer section status icons. Also fixed: subagent transcript viewing, authentication and session management, MCP server-level specs in subagent `disallowedTools`, vim-mode undo, and VSCode CJK IME candidate-window dismissal.

**How to use:** `claude update` or reinstall. Run `/doctor` to check setup status.

#### 2026-06-13 — Claude Code v2.1.177 ([GitHub releases](https://github.com/anthropics/claude-code/releases))
`[CODE]`
Changelog housekeeping only; no functional changes.

#### 2026-06-12 — Claude Code v2.1.176 ([changelog](https://code.claude.com/docs/en/changelog))
`[CODE]`
Session titles now generate in the language of your conversation. Adds a `footerLinksRegexes` setting for regex-matched link badges in the footer row. Improves Bedrock credential caching to respect credential-native expiration rather than a fixed window. Fixes `availableModels` enforcement so an alias model pick cannot redirect to a blocked model via `ANTHROPIC_DEFAULT_*_MODEL` environment variables. Fixes auto mode failing on Fable 5 for organizations without Opus 4.8 enabled, which now falls back to the best available Opus. Fixes hook `if` conditions for Read/Edit/Write file-path patterns, plus multiple Remote Control and background-session stability fixes.

**How to use:** `claude update` or reinstall.

## E. Agent SDKs

*2 entries in window.*

#### 2026-06-15 — anthropic-sdk-python v0.109.2 ([GitHub releases](https://github.com/anthropics/anthropic-sdk-python/releases))
`[SDK-PY]`
Removes `claude-sonnet-4-20250514` and `claude-opus-4-20250514` from the SDK's type definitions, aligned with the model retirements that took effect the same day.

**How to use:** `pip install --upgrade anthropic`

#### 2026-06-15 — anthropic-sdk-typescript v0.104.2 ([GitHub releases](https://github.com/anthropics/anthropic-sdk-typescript/releases))
`[SDK-TS]`
Removes the retired model IDs from the TypeScript SDK's type definitions, aligned with the same-day model retirements.

**How to use:** `npm install @anthropic-ai/sdk@latest`

## G. News & Policy

*2 entries in window.*

#### 2026-06-12 — US export control directive grounds Fable 5 and Mythos 5 ([Anthropic statement](https://www.anthropic.com/news/fable-mythos-access))
`[NEWS]`
Commerce Secretary Howard Lutnick directed Anthropic to suspend all access to Fable 5 and Mythos 5 for any foreign national, inside or outside the United States, including Anthropic's own employees, citing national security authorities. Anthropic disabled both models for all customers worldwide to comply. The stated reason was a claimed jailbreak of Fable. Anthropic disputes the characterization and is working to restore access. Per Axios, senior Anthropic technical staff traveled to Washington to meet White House officials, and a Semafor report cited suspicion that a China-linked group had accessed the model. Former White House AI czar David Sacks accused Anthropic of recklessness with the rollout the day after the letter. As of the weekend, both models remained offline.

**Why it matters:** The broadest application of US export control to a commercial AI product to date, and the first time a lab has flipped its own global kill switch on a flagship under a government order.

#### 2026-06-12 — Results from the first Anthropic Public Record ([announcement](https://www.anthropic.com/news/anthropic-public-record))
`[NEWS]`
Anthropic published the first wave of a national survey series on public attitudes toward AI, fielded in late 2025 with nearly 52,000 Americans. Job loss was the most common fear in every state, held by 64% of respondents; cognitive dependency (56%) and misinformation (52%) followed. Curing diseases like cancer or Alzheimer's ranked as the top hope at 48%. Over 70% favor a government role in regulating AI, with bipartisan support; only 15% trust AI companies to self-regulate.
