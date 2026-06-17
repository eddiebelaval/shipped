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

## Investigation

# The letter that turned off the frontier

The most consequential thing that happened to Anthropic this week was not something it shipped. It was something it had to un-ship, on a government order, for the entire planet at once.

Here is the sequence, because the sequence is the story. Fable 5 and Mythos 5 went generally available on June 9. On the evening of Thursday, June 12, Commerce Secretary Howard Lutnick sent Anthropic an export control directive ordering it to suspend all access to both models for any foreign national, inside or outside the United States, including Anthropic's own foreign-national employees ([Anthropic](https://www.anthropic.com/news/fable-mythos-access)). Anthropic disabled both models for every customer worldwide. By the end of the weekend, both were still dark. Seventy-two hours separated launch from grounding. The unlock window Anthropic was using to turn a frontier into a baseline and the kill switch that ended it were the same model, the same long weekend apart.

The mechanism is worth getting exactly right, because the breadth of the order is what forced the breadth of the response. The directive did not say "block this region" or "block these accounts." It followed a *nationality*, everywhere on earth, employees included. A restriction wired to citizenship rather than geography cannot be enforced with a regional toggle or an IP fence. There is no clean way to serve a model to some people in a building and not others, or to a US-based engineer but not the foreign national at the next desk. So Anthropic did the only thing the order left it room to do. It cut both models off for everyone. All other Claude models stayed up; Sonnet, Opus, Haiku kept answering. The grounding was surgical at the model level and total at the access level, which is the worst combination for the people who had wired Fable 5 into something the day after launch and watched the model ID stop responding by the weekend.

The blast radius runs straight through the operator layer. Anyone who read last week's general availability as a green light, swapped a production call over to Fable 5, and shipped against it spent this weekend staring at a dead endpoint with no published timeline for its return. The free-access window that made the swap so tempting is exactly what maximized the damage. Anthropic spent three days encouraging the world to depend on a model and then, through no decision of its own, had to pull it from every one of them. The cost did not land on Anthropic's quarter. It landed on every roadmap that took the launch at its word.

Now the dispute, attributed precisely because the accounts diverge and the stakes are national security. The trigger, per Axios, was a claim from another company that it had jailbroken Mythos, which alarmed the administration; the Commerce Department's working position was that a technique existed to bypass Fable 5's safety classifiers, the layer that gates access to Mythos's cybersecurity capabilities. Anthropic's account is flatter and it disputes the characterization directly. It says it reviewed a demonstration of the technique, that the demonstration surfaced a small number of previously known, minor vulnerabilities, and that other publicly available models can find the same ones with no bypass at all ([Anthropic](https://www.anthropic.com/news/fable-mythos-access)). Anthropic called the finding a misunderstanding and promised an update. The department, for its part, has not disclosed the specifics of the national security concern behind the order, which is the detail that turns a technical disagreement into something the company cannot simply argue its way out of in public. You cannot rebut a classified rationale with a benchmark.

The story got sharper over the weekend, and it got sharper from more than one direction. Senior Anthropic technical staff traveled to Washington to meet White House officials, per Axios. A Semafor report over the weekend added an edge the Commerce letter never stated outright: that the order stemmed in part from suspicion that a China-linked group had accessed the model. And the criticism arrived from inside the tent. The day after the letter, former White House AI czar David Sacks accused Anthropic in a social media post of being reckless with the Fable 5 rollout. So inside a single long weekend Anthropic was defending the same launch to two audiences with opposite complaints: a government that judged the model too dangerous to leave reachable, and a critic who judged the company too cavalier to have shipped it. The lab that spent the spring being lectured for moving too slowly on safety got grounded for moving too fast.

The cross-lab read is where this stops being one company's bad week and becomes a precedent every frontier lab now has to price in. For two years the load-bearing assumption of the industry was that the lab decided what stayed behind glass. Anthropic held Mythos back; OpenAI staged its own releases; the gate was the company's to open. Export control built for chips and centrifuges has now been pointed at a commercial software product served over an API, and the broadest version of it: not "you may not sell this abroad" but "you may not let a foreign national touch it, anywhere, including the one you employ." Every lab serving a frontier model to a global user base just learned that the access decision is not theirs alone, and that the override can arrive with no advance notice and no published reason. The chip-export regime took years of rulemaking to build. This took one letter and one weekend.

That is the read, stated plainly. For a year the running argument was about whether Anthropic was too cautious with the gate. This week proved the company was never the only hand on it. The switch exists, it sits in Washington, and it works in under three days.

The builder's move is unglamorous and it is the whole point of reading this magazine instead of the headline. If you put Fable 5 or Mythos 5 on a critical path this week, get off it tonight; route to Opus 4.8 or Sonnet 4.6, both of which stayed up throughout, and treat the two grounded models as unavailable with no return date until Anthropic says otherwise. The deeper move is architectural. A model ID is now a dependency that a government can revoke without warning, which means a frontier model on a production path needs the same treatment as any single point of failure: a tested fallback, a config switch, and a plan that does not assume the most capable model you called yesterday will answer today. Last week the lesson was to watch the meter. This week the lesson is to keep a second model warm.

---

## Also Shipped

### What nearly 52,000 Americans actually fear

The same day the directive landed, Anthropic published the first wave of a survey series, the Anthropic Public Record, polling nearly 52,000 Americans on how they feel about AI, one of the largest national polls on the question to date ([Anthropic](https://www.anthropic.com/news/anthropic-public-record)). The dominant fear, in every single state, is job loss, held by 64% of respondents. Cognitive dependency follows at 56%, misinformation at 52%. Only 15% say they trust AI companies to regulate themselves, and over 70% want the government to play a role in regulating AI, with bipartisan support behind that number. The hope side is narrower and more specific than the fear: 48% rank curing diseases like cancer or Alzheimer's among their top hopes, the single most common one. Read the survey against the calendar and the timing is almost too neat. A week that opened with the government overriding a company's own access controls is a strange week to learn that most of the country wanted the government in the room all along. The public asked for a hand on the switch. This week they got a demonstration of what that looks like.

### The retirement clock ran out

The deadline that has sat on the calendar since April 14 finally hit. On June 15, `claude-sonnet-4-20250514` and `claude-opus-4-20250514` reached end of life after a 60-day notice window ([model deprecations](https://docs.anthropic.com/en/about-claude/model-deprecations)). Requests to those IDs now return errors, full stop. The migration itself is a one-line change: move to `claude-sonnet-4-6` for Sonnet and `claude-opus-4-8` for Opus. Consumer Claude.ai and Claude Code managed environments are untouched; this is an API-caller's deadline. The thing worth noticing is the company you kept if you missed it. Anyone still pinned to a 4-series ID this week had two outages stacked on the same model layer: one ordered by Commerce with no warning, and one written into their own dependency file back in April with sixty days of warning. One of those was avoidable. And the cleanup is not finished, `claude-opus-4-1` is separately deprecated, with retirement set for August 5. The move is mechanical: grep your codebase for the dated IDs tonight, not on the morning a customer reports errors.

### Programmatic usage gets its own meter

The other thing that hit June 15 was a billing line, not a model. The restructuring Anthropic announced in May went live: Agent SDK and headless `claude -p` calls now draw from a dedicated monthly credit, metered at standard API list prices, no longer sharing the subscription rate-limit pool ([Anthropic](https://www.anthropic.com/news)). Each plan tier gets its own monthly credit, metered at standard API prices, reset each cycle with no rollover. Interactive Claude Code at a terminal and Claude.ai chat are untouched, still under standard subscription limits. The logic is clean and worth internalizing before your next invoice, because it tells you how Anthropic now thinks about its own product line: a human typing at a terminal is a subscription, an agent running in a loop is metered. The move is to budget your agent fleets against the credit, not the seat, and to check the allotment before you point an overnight loop at it.

### Claude Code keeps its own counsel

While the front page burned, the CLI shipped on schedule, and it shipped fixes shaped exactly to the new world order. On June 12, v2.1.176 fixed a real one: auto mode was failing on Fable 5 for organizations without Opus 4.8 enabled, and now falls back to the best available Opus, which is precisely the kind of graceful degradation that matters more this week than it would have last week. The same release hardened `availableModels` so an alias model pick cannot redirect to a blocked model through `ANTHROPIC_DEFAULT_*` environment variables. June 13's v2.1.177 was changelog housekeeping, no functional changes. By June 15, v2.1.178 added `Tool(param:value)` permission rules with wildcard support, so a rule like `Agent(model:opus)` can block Opus subagents outright, plus nested `.claude/skills` loading with closest-wins resolution and pre-launch classification of subagent spawns. The drumbeat does not check the news. While Washington decided which models the world could reach, the CLI was quietly shipping the controls to decide which models your own agents can reach. The move: `claude update`, then run `/doctor` to confirm the setup.

---

## Quiet on the Wire

Quiet, this week, was the story. No new SDK feature releases of substance, no new research papers from Anthropic in the window, just the type-definition cleanups that always follow a retirement: Python v0.109.2 and TypeScript v0.104.2 each stripped the dead model IDs ([Python](https://github.com/anthropics/anthropic-sdk-python/releases), [TypeScript](https://github.com/anthropics/anthropic-sdk-typescript/releases)). On a normal week that absence would read as a slow stretch. This week it reads as a company with its full attention pointed at one room in Washington. The loudest signal on the wire was the silence where Fable 5 used to answer. As of the weekend, the only public timeline for its return was Anthropic's promise of an update and a delegation of engineers on their way to the capital.

---

## Term of the Issue

# The Grounding

**The grounding** /ðə ˈɡraʊn.dɪŋ/ *noun*

A government-ordered, provider-executed global shutdown of a commercial AI model, in which the lab itself flips the switch to comply. Distinct from a deprecation, which the lab schedules on its own clock with notice, and from a recall, which targets a defect in the product. A grounding targets *access*, not the artifact: the model still works, the company still stands behind it, and it goes dark anyway because an authority above the company said so. The defining trait is the hand on the switch. In a deprecation the lab decides; in a grounding the lab complies. The breadth of the order sets the breadth of the outage, which is why a restriction written against a nationality produced a shutdown for the entire planet: there was no narrower way to obey it.

**First observable** 2026-06-12, when a US Commerce Department export control directive ordered Anthropic to cut off Fable 5 and Mythos 5 for all foreign nationals, and Anthropic, unable to enforce a citizenship-scoped rule any narrower way, disabled both models worldwide.

**Usage** *"It wasn't deprecated and it wasn't recalled. It was grounded, and the lab held the switch."*

**See also** the retirement that hit the same week (a deprecation, lab-scheduled, sixty days' notice) for the clean contrast: two models went dark on Anthropic's calendar with warning, two went dark on Washington's with none.

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
`claude-sonnet-4-20250514` and `claude-opus-4-20250514` reached end of life on June 15, 2026, after a 60-day notice window that opened April 14. Requests to these model IDs now return errors. Consumer Claude.ai and Claude Code managed environments are unaffected.

**How to use:** Migrate to `claude-sonnet-4-6` (Sonnet) and `claude-opus-4-8` (Opus) in your API calls. `claude-opus-4-1` is separately deprecated, with retirement set for August 5, 2026.

#### 2026-06-12 — Fable 5 and Mythos 5 suspended worldwide ([Anthropic statement](https://www.anthropic.com/news/fable-mythos-access))
`[MODEL]`
Following a US Commerce Department export control directive received the evening of June 12, Anthropic disabled both Fable 5 and Mythos 5 for all customers worldwide. The directive ordered access cut off for any foreign national, inside or outside the United States, including foreign-national Anthropic employees; the breadth forced a global shutdown rather than targeted enforcement. The cited basis was a claimed jailbreak of Fable's safety classifiers, which gate Mythos's cybersecurity capabilities. Anthropic reviewed a demonstration, said it surfaced only a small number of previously known minor vulnerabilities that other public models can also find without a bypass, disputed the characterization, and said it is working to restore access. All other Claude models remained available.

**Why it matters:** The first government-ordered, provider-executed global shutdown of a commercial AI model, arriving three days after general availability with no advance notice.

## B. API & Platform

*1 entry in window.*

#### 2026-06-15 — Programmatic credit billing goes live ([Anthropic](https://www.anthropic.com/news))
`[API]`
Agent SDK and headless `claude -p` usage now draws from a dedicated monthly credit metered at standard API list prices, separate from the subscription rate-limit pool. Each subscription tier gets its own monthly credit, metered at standard API prices, reset each cycle with no rollover. Interactive Claude Code terminal usage and Claude.ai chat continue under standard subscription limits, unchanged. Announced in May, effective the same day as the model retirements.

**How to use:** Programmatic SDK and `claude -p` runs bill against the metered credit; interactive sessions are unaffected. Budget agent loops against the credit, not the subscription.

## C. Claude Code

*3 entries in window.*

#### 2026-06-15 — Claude Code v2.1.178 ([GitHub releases](https://github.com/anthropics/claude-code/releases))
`[CODE]`
Adds `Tool(param:value)` syntax for permission rules to match tool input parameters with wildcard support, so a rule like `Agent(model:opus)` blocks Opus subagents. Nested `.claude/skills` directories now load when working on files there, appearing as `dir:name` on name collisions, with closest-wins resolution for nested `.claude/` directories. Auto mode now classifies subagent spawns before launch. `/doctor` gets a flat tree layout with clearer section status icons. Also fixed: subagent transcript viewing, authentication and session management, MCP server-level specs in subagent `disallowedTools`, vim-mode undo, and VSCode CJK IME candidate-window dismissal.

**How to use:** `claude update` or reinstall. Run `/doctor` to check setup status.

#### 2026-06-13 — Claude Code v2.1.177 ([changelog](https://code.claude.com/docs/en/changelog))
`[CODE]`
Changelog housekeeping only; no functional changes.

#### 2026-06-12 — Claude Code v2.1.176 ([changelog](https://code.claude.com/docs/en/changelog))
`[CODE]`
Session titles now generate in the language of your conversation. Adds a `footerLinksRegexes` setting for regex-matched link badges in the footer row. Improves Bedrock credential caching to respect credential-native expiration rather than a fixed window. Fixes `availableModels` enforcement so an alias model pick cannot redirect to a blocked model via `ANTHROPIC_DEFAULT_*` environment variables. Fixes auto mode failing on Fable 5 for organizations without Opus 4.8 enabled, which now falls back to the best available Opus. Fixes hook `if` conditions for Read/Edit/Write file-path patterns, plus multiple Remote Control and background-session stability fixes.

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
Commerce Secretary Howard Lutnick directed Anthropic to suspend all access to Fable 5 and Mythos 5 for any foreign national, inside or outside the United States, including Anthropic's own employees, citing national security authorities. Anthropic disabled both models for all customers worldwide to comply. The stated reason was a claimed jailbreak of Fable's safety classifiers. Anthropic disputes the characterization, calling the finding a misunderstanding, and is working to restore access. Per Axios, senior Anthropic technical staff traveled to Washington to meet White House officials; a Semafor report cited suspicion that a China-linked group had accessed the model. Former White House AI czar David Sacks accused Anthropic of recklessness with the rollout the day after the letter. As of the weekend, both models remained offline.

**Why it matters:** The broadest application of US export control to a commercial AI product to date, and the first time a lab has flipped its own global kill switch on a flagship under a government order.

#### 2026-06-12 — Results from the first Anthropic Public Record ([announcement](https://www.anthropic.com/news/anthropic-public-record))
`[NEWS]`
Anthropic published the first wave of a national survey series on public attitudes toward AI, fielded in late 2025 with nearly 52,000 Americans, one of the largest national polls on the question to date. Job loss was the most common fear in every state, held by 64% of respondents; cognitive dependency (56%) and misinformation (52%) followed. Curing diseases like cancer or Alzheimer's ranked as the top hope at 48%. Over 70% favor a government role in regulating AI, with bipartisan support; only 15% trust AI companies to self-regulate.
