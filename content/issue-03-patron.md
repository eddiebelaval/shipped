---
issue: 03
slug: patron
title: "Patron"
date: 2026-05-01
period: 2026-04-24 to 2026-04-30
masthead: Shipped.
deck: "The week the money flowed both ways, the press cycle turned, and patronage became the shape of the whole thing."
byline: Edited by Eddie Belaval. Reported with the assistance of Claude.
term_of_issue: Patron
status: draft
ship_date: 2026-05-01
running_order_locked: true
fob_content: editorial
log_content: reference
---

# Shipped.

**Issue #03: Patron**
*A magazine of what Anthropic ships.*
*Period: 2026-04-24 to 2026-04-30. Volume I.*

---

## The Open

Today, April 30, a beta header stops working. `context-1m-2025-08-07`, the flag that bought a million tokens of context on Sonnet 4.5 and Sonnet 4, is no longer honored. Anyone over 200k tokens on those models gets rejected at the gateway. The migration path is Sonnet 4.6 or Opus 4.6, where 1M is GA, no header, standard pricing.

Pre-announced March 30. Mundane on its face. A calendar event.

But it lands in a week where Anthropic took $40 billion from one patron and decided what to retire for everyone else, all inside seven days. The patron giveth and the patron taketh away. This issue is about who is holding the purse.

---

---

## The Lead Story

# The Patron Economy

The headline isn't $40 billion. It's that the money flows in both directions.

On April 24, Google committed up to $40 billion to Anthropic, $10 billion in cash now at a $350 billion valuation, the same mark as February's Series G, with the remaining $30 billion contingent on milestones. The deal carries five gigawatts of TPU compute over five years. Read it next to last week's AWS arrangement, $100 billion-plus over a decade with its own gigawatts of Trainium, and a shape comes into focus. Two hyperscalers, two compute substrates, both contractually bound to Anthropic's roadmap. By April 29, TechCrunch and Bloomberg reported Anthropic weighing a $50 billion round at $850 to $900 billion, a number that would roughly match OpenAI. Reported, not announced. Anthropic has confirmed none of it.

That is the patronage flowing in. Here is the part the field had not seen before.

On April 28, the same day it shipped nine creative connectors, Anthropic joined the Blender Development Fund as a Corporate Patron, the tier that holds Epic Games, NVIDIA, Microsoft, AMD. The Blender connector depends on the Python API the Blender Foundation maintains. So Anthropic now pays the foundation whose open-source primitive Claude needs to stay useful inside professional software. That is not philanthropy. It is the same move as Google paying Anthropic for compute, pointed downward. Anthropic is now the largest recipient of compute patronage in the history of the industry and a patron itself, underwriting the primitives it runs on.

Underneath the compute deal, the territory spreads. NEC named Anthropic its first Japan-based global partner on April 24, with Claude going to roughly 30,000 NEC Group employees and Opus 4.7 plus Claude Code folded into its BluStellar Scenario consulting. Three days later the Sydney office opened, with Theo Hourmouzis, who ran ANZ and ASEAN at Snowflake, named GM. Commonwealth Bank and Quantium cited as customers. Seoul named next. NEC is the Japan distribution patron the way Google is the compute patron: a partner who carries Anthropic into a market it cannot reach alone.

What does an AI company that lives entirely on patronage owe its patrons? In April, Anthropic became something the field had not yet had a name for, an entity underwritten by two hyperscalers and simultaneously underwriting the open-source primitives it depends on. The shape of that obligation is the load-bearing question of the next year.

---

## Investigation

# The Disclosure Tax

April was a press cycle Anthropic rode. Mythos launched, the Project Glasswing partner list was set, the BioMysteryBench numbers landed, Google wired $40 billion. This week the cycle turned. Nothing broke. Four disclosure gaps simply surfaced in the same window, and the bill for a month of favorable coverage came due.

The load-bearing piece is Bruce Schneier. On April 28 he published "What Anthropic's Mythos Means for the Future of Cybersecurity" and called the rollout "very much a PR play by Anthropic that worked, with lots of reporters breathlessly repeating Anthropic's talking points without engaging with them critically." His specific complaints are not rhetorical. No disclosure of false-positive rates. No independent reproduction. Comparable open-source models, he writes, citing independent research, hallucinate vulnerabilities in already-patched code. The National ran a parallel "experts worry" piece the next day on the same thread. The pointed part is who Schneier is. He belongs to the security establishment Anthropic courted three weeks earlier with Glasswing, the partner roster that runs AWS, Apple, Cisco, CrowdStrike, Google, JPMorgan Chase, the Linux Foundation, Microsoft, NVIDIA, Palo Alto Networks. The critic is the one the safety-forward brand cannot easily dismiss, because it recruited him.

The second thread is in Anthropic's own paper. On April 29 the company published BioMysteryBench, and the headline wrote itself: Claude Mythos Preview solved 30% of 23 bioinformatics problems an expert panel could not crack. The caveat sat in the methodology. On hard problems, the success rate is one or two of five attempts, which reads as lucky paths rather than reproducible strategy. The press led with the 30%. The caveat barely registered. It was self-disclosed and still got lost.

The third is procurement. FT, Bloomberg, and Reuters reported that Goldman Sachs removed Claude access for its Hong Kong staff "in recent weeks," citing a strict reading of its Anthropic contract following consultation with the company. ChatGPT and Gemini stayed available to the same desks. Hong Kong is not a market where Anthropic officially supports the API or Claude.ai, and the contract language was never disclosed. The mechanism, an enterprise agreement read strictly enough to enforce a geographic restriction, is itself a precedent.

The fourth is the $50 billion round. A number at $850 to $900 billion, reported by two of the most careful outlets in the business, with one investor said to be ready to commit $5 billion and unable to get a meeting with CFO Krishna Rao. A week later, still "reportedly." A figure that large staying unconfirmed that long is its own data point.

The disclosure tax is the price of operating in the safety-forward register. Each of the four pieces is a different reader demanding a different disclosure that frontier labs had not yet been made to pay. The question is not whether Anthropic is in trouble. It is whether the safety-forward brand can survive a week where the safety establishment publicly grades it down.

---

## By the Numbers

The shape of one week, in figures. Compute flowing in, primitives flowing out, the territory underneath, and the one caveat the press cycle skipped.

- **$40B** committed by Google on April 24, $10B in cash now at a $350B valuation, the rest contingent on milestones.
- **5 GW** of TPU compute over five years in the Google deal, a second gigawatt-scale substrate alongside last week's AWS Trainium.
- **$900B** reported valuation per April 29 reports, on a **$50B** round Anthropic has not confirmed.
- **$30B** ARR publicly disclosed, against a **~$40B** run rate cited by reporting sources.
- **30,000** NEC Group employees getting Claude internally, NEC named Anthropic's first Japan-based global partner.
- **9** creative connectors shipped April 28, spanning Adobe, Blender, Autodesk, Ableton, Splice, Affinity, SketchUp, Resolume.
- **20M** paid Microsoft 365 Copilot seats reported at Q3 earnings, with Microsoft's AI run rate cited at **$37B**.
- **30%** Mythos solve rate on 23 expert-unsolvable BioMysteryBench problems. Caveat: one or two of five attempts on the hard ones.
- **0** Anthropic public confirmations of the $50B round.
- **April 30** the 1M-token context beta header retires on Sonnet 4.5 and Sonnet 4.

---

## Also Shipped

### Claude for Creative Work: nine connectors

A model becomes a tool the moment it can act inside the software you already own. On April 28 Anthropic shipped nine connectors letting Claude operate inside professional creative apps: Adobe across Photoshop, Premiere, Illustrator, Express, Lightroom, InDesign, Stock, and Firefly, plus Blender, Autodesk, Ableton, Splice, Affinity, SketchUp, and Resolume. The Blender connector exposes Blender's Python API for scene analysis and scripted batch changes. One day earlier, Adobe brought its Firefly AI Assistant to public beta, and per Axios, positioned Claude as the orchestrator the next day. The connectors run both ways, which makes the creative surface contestable rather than owned. They also run on OAuth, the same trust surface Issue 02 watched crack.

### NEC and Sydney: the territory half-week

Two enterprise moves landed inside three days. On April 24, NEC named Anthropic its first Japan-based global partner, with Claude going internally to roughly 30,000 NEC Group employees, Opus 4.7 and Claude Code folded into its BluStellar Scenario consulting, and Claude pulled into NEC's SOC services for cyber defense, the first commercial deployment of Anthropic inside a third-party security operations product. On April 27, the Sydney office opened with Theo Hourmouzis, formerly of Snowflake's ANZ and ASEAN business, named GM, citing Commonwealth Bank and Quantium as customers. Tokyo, Bengaluru, Sydney, with Seoul named next. The Asia footprint is now materially ahead of the EU one.

### The 1M context cliff, on schedule

The cliff that opened this issue is also a release. As of April 30, the `context-1m-2025-08-07` beta header is no longer honored on Sonnet 4.5 and Sonnet 4, and requests over 200k tokens on those models are rejected. Pre-announced March 30, biting on schedule. The migration path is Sonnet 4.6 or Opus 4.6, where the million-token window is GA at standard pricing with no header to set. The operator note: the model that earned the longer context is the patron version, and the beta surcharge, if you were paying one, is gone from the cost model on 4.6.

---

## Quiet on the Wire

### Rate Limits API, and a telemetry primitive

Quiet on the Wire is where Shipped. reads the plumbing for the road it implies. Two items this week. On April 24, a single changelog line: a Rate Limits API, a programmatic query of rate limits for an organization and its workspaces. No launch post. Per-workspace governance is the surface managed-agents pricing will sit on, and NEC's 30,000-seat deployment is the first test of it at scale. On April 28, Claude Code 2.1.122 added a `claude_code.at_mention` OpenTelemetry event, making `@`-mention resolution observable at the same granularity as a tool call. Neither is a product. Both are the shape of the road.

---

## Term of the Issue

# Patron

**Patron** /ˈpeɪ.trən/ *noun*

The two-way relationship a frontier AI lab now sits inside: compute flowing in from hyperscalers, money flowing out to the open-source primitives the lab depends on. A patron underwrites what it needs to exist and binds the recipient to its roadmap in the process.

**First observable** the week of 2026-04-24, when Google committed $40 billion and five gigawatts of TPU to Anthropic, and Anthropic joined the Blender Development Fund as a Corporate Patron the same day it shipped the connectors that lean on Blender's Python API. NEC carried Claude into Japan; Schneier sent the bill for the press cycle. Patronage in, patronage out, scrutiny on top.

**Usage** *"We don't have customers and vendors anymore. We have patrons, and we are one."*

---

## The Close

# What the patronage was for

A founder signs a term sheet at a valuation that doubles in ten weeks and wires the proceeds to a render-engine foundation in the same news cycle. The compute is bought. The primitive is paid. Somewhere a security researcher asks for the false-positive rate and gets a headline number instead.

Shipped was last year's verb. Underwritten is this year's.

The patron asks what the patronage was for. The user asks where they actually were when the work got done. This year you find out that both questions have the same answer, and that the answer was never going to be at claude.ai.

---

## A. Models

*1 entry in window.*

#### 2026-04-30 - 1M context beta header retired on Sonnet 4.5 and Sonnet 4 ([release notes](https://platform.claude.com/docs/en/release-notes/overview))
`[DEPRECATION]`

The `context-1m-2025-08-07` beta header is no longer honored on Sonnet 4.5 and Sonnet 4. Requests over 200k tokens on those models are rejected. Pre-announced 2026-03-30. Migration path: Sonnet 4.6 or Opus 4.6, where the 1M window is GA at standard pricing without a header.

## B. API & Platform

*1 entry in window.*

#### 2026-04-24 - Rate Limits API ([release notes](https://platform.claude.com/docs/en/release-notes/overview))
`[API]`

New endpoint lets administrators programmatically query rate limits for an organization and its workspaces. Shipped as a single changelog line, no launch post. Per-workspace governance plumbing for enterprise deployments.

## C. Claude Code

*1 entry in window.*

#### 2026-04-28 - Claude Code 2.1.122 ([changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md))
`[CODE]`

Bedrock service-tier selection via `ANTHROPIC_BEDROCK_SERVICE_TIER` (default, flex, priority). `/resume` PR-URL search now finds the session that created a given GitHub, GitHub Enterprise, GitLab, or Bitbucket PR. `/mcp` deduplication. New `claude_code.at_mention` OpenTelemetry log event plus numeric attribute support. Image resize bug fixed (was clamping to 2576px instead of 2000px on newer models).

## D. Claude Apps

*1 entry in window.*

#### 2026-04-28 - Claude for Creative Work, nine connectors ([announcement](https://www.anthropic.com/news/claude-for-creative-work))
`[APPS]`

Anthropic shipped nine connectors letting Claude operate inside professional creative software via APIs and product documentation: Adobe (Photoshop, Premiere, Illustrator, Express, Lightroom, InDesign, Stock, Firefly), Blender, Autodesk, Ableton, Splice, Affinity (Canva), SketchUp, Resolume. The Blender connector exposes Blender's Python API for scene analysis and scripted batch changes. Same-day, Anthropic joined the Blender Development Fund as a Corporate Patron.

## F. Research & Publications

*2 entries in window.*

#### 2026-04-29 - BioMysteryBench bioinformatics benchmark ([research](https://www.anthropic.com/research/Evaluating-Claude-For-Bioinformatics-With-BioMysteryBench))
`[RESEARCH]`

Anthropic published a 99-question expert-authored bioinformatics benchmark on messy real-world data. Headline: Claude Mythos Preview solved 30% of the 23 questions a domain-expert panel could not crack, with Sonnet 4.6 onward on par with experts overall. Self-disclosed caveat in the paper: on hard problems, success rate is one or two of five attempts, suggesting lucky paths rather than reproducible strategies.

#### 2026-04-24 - Election safeguards update ([news](https://www.anthropic.com/news/election-safeguards-update))
`[RESEARCH]`

First public testing of whether models can plan and run multi-step influence operations end-to-end without human prompting; Anthropic reports the latest models refused nearly every task. Opus 4.7 and Sonnet 4.6 scored 95% and 96% on political-neutrality evaluations. On a 600-prompt set (300 harmful, 300 legitimate), Opus 4.7 responded appropriately 100% of the time, Sonnet 4.6 at 99.8%. Election banners on Claude.ai will direct US users to TurboVote ahead of the midterms.

## G. Partnerships and Policy

*4 entries in window.*

#### 2026-04-24 - Google to invest up to $40B in Anthropic ([TechCrunch](https://techcrunch.com/2026/04/24/google-to-invest-up-to-40b-in-anthropic-in-cash-and-compute/), [Bloomberg](https://www.bloomberg.com/news/articles/2026-04-24/google-plans-to-invest-up-to-40-billion-in-anthropic))
`[NEWS]`

Google committed up to $40B: $10B in cash now at a $350B valuation (flat to February's Series G mark), with a contingent additional $30B tied to performance milestones. The deal includes five gigawatts of TPU compute over five years, positioning Google as a co-anchor compute partner alongside AWS, where Anthropic committed $100B+ over a decade last week.

#### 2026-04-24 - NEC named Anthropic's first Japan-based global partner ([Anthropic](https://www.anthropic.com/news/anthropic-nec), [NEC](https://www.nec.com/en/press/202604/global_20260423_01.html))
`[NEWS]`

NEC becomes Anthropic's first Japan-based global partner. Joint development of industry-specific AI for finance, manufacturing, and local government using Claude Cowork. NEC will deploy Claude internally to roughly 30,000 NEC Group employees and fold Opus 4.7 and Claude Code into its BluStellar Scenario consulting program, plus integrate Claude into its SOC services for cyber defense.

#### 2026-04-29 - $50B round at ~$900B valuation reported ([TechCrunch](https://techcrunch.com/2026/04/29/sources-anthropic-could-raise-a-new-50b-round-at-a-valuation-of-900b/), [Bloomberg](https://www.bloomberg.com/news/articles/2026-04-29/anthropic-considering-funding-offers-at-over-900-billion-value))
`[NEWS]`

TechCrunch and Bloomberg report multiple preemptive offers in the $850B to $900B range, with one institutional investor prepared to commit $5B reportedly unable to secure a meeting with CFO Krishna Rao. Reports cite a run rate closer to $40B against the publicly disclosed $30B ARR. Reported, not confirmed by Anthropic. Would more than double February's mark and roughly match OpenAI.

#### 2026-04-27 - Anthropic opens Sydney office, names ANZ GM ([Anthropic](https://www.anthropic.com/news/theo-hourmouzis-general-manager-australia-new-zealand), [Marketing-Interactive](https://www.marketing-interactive.com/anthropic-appoints-theo-hourmouzis-to-lead-anz-as-sydney-office-officially-opens))
`[NEWS]`

Anthropic opened a Sydney office and named Theo Hourmouzis, formerly of Snowflake where he ran ANZ and ASEAN, as ANZ GM. Customer base cited: Commonwealth Bank, Quantium, with integrations into Canva and Xero. Sydney follows Tokyo and Bengaluru; Seoul named as next.
