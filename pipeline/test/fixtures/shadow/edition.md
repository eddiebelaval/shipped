---
issue: 90
title: "Shipped., Thursday, October 15, 2026"
date: 2026-10-15
period: "Oct 14 to Oct 15"
status: published
masthead: Shipped.
layout: paper
edition: Daily Edition
issue_label: "Daily · Oct 14 to Oct 15"
deck: "Meta releases 816 billion parameters for free, and the rest of the frontier recalibrates."
weather: "The race is not only about who ships the best model anymore."
edition_section: "anthropic-daily"
edition_stem: "2026-10-15"
---

## The Open

*The number is 816 billion.*

That is the parameter count of Muse Spark Open, the model Meta released this morning. You can download it from Hugging Face right now. All 816 billion parameters, a sparse mixture-of-experts, roughly 42 billion active per token, a million-token context window, multimodal. Free to download and run under a custom license with revenue thresholds.

The rest of the frontier kept its schedule. Anthropic published two policy pieces and opened a Singapore office. xAI shipped Grok Voice 3.0 at the same price as 2.0. Claude Code got a minor quality-of-life update. OpenAI and Google DeepMind were quiet.

The quiet is the story. When Meta drops the biggest open-weight model in history, no one rushes to match it. They absorb the news and hope the ecosystem does not notice how much ground just shifted.

## The Lead Story

# 816 Billion Free

**Muse Spark Open ships its weights to Hugging Face. One download and the largest open-weight model in history is yours.**

*Source: Hugging Face, SiliconANGLE, Bloomberg · Date: October 15, 2026 · Tag: Model, Open Weights*

**By the numbers:** 816B total parameters; 42B active per token; 1M token context; BF16 and NVFP4 formats; ~1.65 TB (BF16) / ~537 GB (NVFP4); $20M revenue threshold; 89.2 on MCP-Atlas (Meta-reported).

The mechanism is a sparse mixture-of-experts architecture. 816 billion total parameters, with roughly 42 billion active per forward pass. The MoE design means most of the model stays dormant while a small routing layer picks the relevant expert weights and runs them. Context window is one million tokens. Input modalities are text, image, audio, and video. Weights ship in BF16, approximately 1.65 terabytes, and NVFP4, approximately 537 gigabytes. Meta says it runs on two Apple M5 Ultra Mac Studios for local inference. API access is already live via OpenRouter, Together AI, and Groq for builders who want frontier-class performance without the hardware investment.

The blast radius is anyone who builds with frontier models. A research-grade coding agent no longer requires a commercial API call at flagship pricing. A startup that was priced out of the leading models now has a 1M-context, multimodal, MoE architecture available for the cost of a Groq API key. Meta's own benchmark figure is 89.2 on MCP-Atlas. Independent scores at scale would be more convincing, but the architecture alone justifies testing. The lab that has been quietly building out its APAC partnerships and independent-evaluator access now competes in a market where the price floor for a capable open model just moved to zero.

The pattern is strategic, not ideological. Llama 1 through 3 were open. Muse Spark 1.0, when it launched in April, was closed, a deliberate break from Meta's prior cadence. Muse Glimmer, the 30-billion-parameter distillation Meta released in August under Apache 2.0, was a partial correction. Muse Spark Open is the full recalibration. Meta takes the second-generation frontier model, the one it trained through the summer and has been selling commercially since August as Muse Spark 1.2, and hands it to the ecosystem. The current frontier version, Muse Spark 1.3, stays closed. Meta keeps the newest generation proprietary and releases the prior generation as a community asset. It is a moat strategy dressed as generosity, and it works either way.

The read: the labs that justify their API pricing on model quality alone now have a harder conversation. Anthropic's answer has always been alignment, safety, and verified attestation. OpenAI's answer has been speed and Intelligent UI integration. Google's answer has been Gemini's native tooling and multimodal reach. Meta just made the third-party answer a 1.65-terabyte download. Labs that cannot articulate the API premium beyond raw capability are in a more exposed position. The ones with a clear safety-and-trust story, Anthropic chief among them, are not. But the conversation got more expensive for everyone in the next six months.

The builder's move: pull NVFP4 from Hugging Face or call the Together AI API today. Check the MCP-Atlas claim against your own workload before committing infrastructure to it. The revenue license threshold is $20 million gross annual, so most individual developers and small teams will never hit it. The "Built with Muse Spark Open" labeling requirement applies to shipped products. Military and critical-infrastructure uses are barred.

## Also Shipped

### METR Gets a Key to the Office

Six employees from METR, the nonprofit AI evaluator, now have office space, hardware, and internal tool access at Anthropic roughly equivalent to its own risk assessment teams. METR can publish its findings without Anthropic approval. Anthropic can require redactions in predefined narrow categories, but METR can note publicly whether it considers those redactions justified, without revealing what was redacted.

The tiered access structure Anthropic published is worth reading in full. Tier 1: narrow, company-approved investigations with Anthropic veto on publication. Tier 2: publication rights with minimal veto, broader information access. Tier 3, the METR arrangement: employee-like access, full publication rights, and a redaction dispute process. SecureBio sits at Tier 1 right now, reviewing the CBRN chapter of the August Risk Report. Hugging Face is in early talks. Accenture and Faculty are in a broader partnership covering red-teaming and alignment assessments.

This is the most concrete external accountability structure any frontier lab has published. Anthropic says every frontier company should do the same. That is either leadership or a PR dare. When the METR reports publish, they will be primary sources for anyone making model-selection decisions on safety grounds.

*[anthropic.com, October 15, 2026](https://www.anthropic.com/news/an-update-on-independent-evaluators)*

### Grok Voice 3.0 Ships at $0.08 Per Minute, Same as 2.0

xAI released Grok Voice 3.0 on October 14 in its Voice Agent API. Speech-to-speech, $0.08 per minute, unchanged from the prior version. Apps using the `grok-voice-latest` alias were automatically migrated. Grok Voice 2.0 is deprecated. Artificial Analysis scores it 86.9 on its Speech-to-Speech Index, which xAI cites as first place, though OpenAI holds a narrow lead on the separate tau-voice evaluation. xAI says the model handles millions of conversations per day in Tesla vehicles.

Shipping at competitive benchmark quality with no price increase, in a market that usually extracts one with each model generation, is a deliberate pricing strategy. If the benchmark holds in production, the voice API market just got more competitive without getting more expensive. The builder's move: `grok-voice-latest` already points to 3.0. If you have a hardcoded `grok-voice-2.0` string in production, it is deprecated and you should move it now.

*[SiliconANGLE, October 14, 2026](https://siliconangle.com/2026/10/14/grok-voice-3-0-from-spacexsi-outscores-openai-and-google-on-speech-to-speech-index/)*

### 99% Even-Handed, One Asterisk

Anthropic published its midterm election preparation update on October 14. Usage data from a late-September sample of approximately 250,000 US Claude conversations: 0.51% touched elections or voting, 0.01% asked Claude whom to vote for, 0.002% violated election integrity policies. Claude Opus 5.5, Sonnet 5.5, and Haiku 5.5 scored 99% on Anthropic's political evenhandedness evaluation.

One outside reviewer found an asymmetry worth flagging. The Foundation for American Innovation found that Claude Sonnet 4.5 was more likely to soften arguments for right-leaning positions than left-leaning ones. Anthropic says it is working on it, and it includes that finding in its own report. Publishing a 99% self-reported score alongside an external finding of directional bias is two measurements of two different things, both reported in the same document. Anthropic gets credit for including both. The contrast with a lab that would not publish the outside critique is the relevant comparison.

If you are building political content tools, Anthropic's new Usage Policy guidance for campaigns is the clearest current document on what is permitted versus prohibited: press statements and debate prep are in; fake personas and mass-produced engagement are out.

*[anthropic.com, October 14, 2026](https://www.anthropic.com/news/2026-us-midterms)*

### Singapore Office Opens, MOU Signed

Anthropic opened its Singapore office on October 14 and signed a Memorandum of Understanding with Singapore's Ministry of Digital Development and Information. Singapore ranks second of 121 countries in per-capita Claude.ai usage, nearly six times what its population alone would predict. GovTech Singapore has over 1,500 engineers using Claude Code. Grab's BriX sales assistant, built on Claude, reports approximately 40,000 hours per quarter in saved work. DBS and GIC are deploying Claude across developer and investment functions. No product news here, expansion and relationship formalization that has been in progress since 2023.

*[anthropic.com, October 14, 2026](https://www.anthropic.com/news/singapore-office-opening)*

## Quiet on the Wire

*What's next*

**Gemini 4 Argon** moved into broader developer and paid-subscriber availability on October 13, one day before this window. Google's first post-Gemini 4 release. API pricing is reported to match the Ultra tier. Worth tracking as third-party benchmarks accumulate.

**Meta Muse Spark 1.3** is the current closed frontier from Meta, rolling out in Muse Code and the API. Nothing in this window suggests 1.4 is imminent. Muse Spark Open is the 1.2 architecture, one generation behind the current production frontier.

**Anthropic** has signaled a more comprehensive election usage report later this month. A METR independent evaluation will follow once the review is sufficiently advanced. Claude Code got two infrastructure updates on October 14: idle compaction for long terminal sessions, and a new environment variable (`CLAUDE_CODE_DISABLE_FILE_MENTIONS`) to disable at-mention file expansion.

## The Close

Meta handed out 816 billion parameters for free.

Anthropic let outsiders into the office.

The race is not only about who ships the best model anymore.

## A. Meta AI

*Open-weight flagship. The largest open model available.*

#### 2026-10-15 - Muse Spark Open ([source](https://huggingface.co/blog/meta-muse-spark-open))
`[MODEL]`

816B-parameter sparse MoE, roughly 42B active per token, 1M-token context, multimodal (text, image, audio, video). Weights in BF16 (~1.65 TB) and NVFP4 (~537 GB). Available on Hugging Face, Amazon SageMaker AI, Google Cloud Model Garden, and Microsoft Foundry Models. API access via OpenRouter, Together AI, and Groq. Custom Muse Model License: free to use, commercial hosting revenue-share trigger at $20M gross annual, "Built with Muse Spark Open" labeling required, military and critical infrastructure prohibited. Meta reports 89.2 on MCP-Atlas (Meta-reported, independent verification pending).

**How to use:** Download NVFP4 weights from Hugging Face or call via Together AI or Groq for immediate API access. Local inference requires approximately two Apple M5 Ultra Mac Studios or equivalent memory. Check the license for revenue-threshold terms before commercial hosting at scale.

**Why it matters:** The largest open-weight frontier model available publicly. Changes the cost structure for research-grade coding and agent workloads, and raises the floor for what proprietary API pricing must justify.

## B. xAI

*Voice API upgrade at unchanged pricing.*

#### 2026-10-14 - Grok Voice 3.0 ([source](https://siliconangle.com/2026/10/14/grok-voice-3-0-from-spacexsi-outscores-openai-and-google-on-speech-to-speech-index/))
`[MODEL]`

Speech-to-speech model in the Voice Agent API. Artificial Analysis Speech-to-Speech Index: 86.9 (xAI-cited, first place per company). $0.08/min, same as Grok Voice 2.0. Apps using `grok-voice-latest` were auto-migrated to 3.0. Grok Voice 2.0 deprecated. xAI reports millions of daily conversations handled in Tesla vehicles.

**How to use:** `grok-voice-latest` now resolves to `grok-voice-3.0`. Migrate any hardcoded `grok-voice-2.0` strings in production code.

## C. Anthropic

*Policy, safety accountability, expansion, and a Claude Code quality-of-life update.*

#### 2026-10-15 - Update on Independent Evaluators ([source](https://www.anthropic.com/news/an-update-on-independent-evaluators))
`[NEWS]`

METR (6 employees) receives employee-like access: office space, hardware, and internal tools comparable to Anthropic's own risk assessment teams. Tiered evaluator framework published. Tier 1: narrow, company-approved investigations. Tier 2: broader information access, publication rights, minimal Anthropic veto. Tier 3 (METR): employee-like access, full publication rights, redaction dispute process. SecureBio at Tier 1, reviewing CBRN chapter of the August 2026 Risk Report. Hugging Face in early-stage talks. Accenture and Faculty covering red-teaming and alignment assessments.

#### 2026-10-14 - Preparing for the 2026 US Midterms ([source](https://www.anthropic.com/news/2026-us-midterms))
`[NEWS]`

Election safeguards update. Sept 21-27 sample (~250,000 US conversations): 0.51% touched elections or voting, 0.01% asked whom to vote for, 0.002% violated election integrity policies. Claude Opus 5.5, Sonnet 5.5, and Haiku 5.5 scored 99% on Anthropic's political evenhandedness evaluation. Foundation for American Innovation found Sonnet 4.5 more likely to soften right-leaning arguments than left-leaning ones. New classifiers for multi-step misuse and foreign state actor detection. Democracy Works integration for official state-specific voting information coming later in October.

**How to use:** Updated Usage Policy guidance for election campaigns is published. Permitted: press statements, debate prep, turnout data analysis. Prohibited: fake personas, mass-produced engagement, content posing as independent news.

#### 2026-10-14 - Singapore Office Opens, MOU with MDDI Signed ([source](https://www.anthropic.com/news/singapore-office-opening))
`[NEWS]`

Fifth APAC office. MOU signed with Singapore Ministry of Digital Development and Information (MDDI) covering AI safety, security, and responsible adoption. Singapore ranks second of 121 countries in per-capita Claude.ai usage. GovTech Singapore: 1,500+ engineers on Claude Code. Grab BriX: approximately 40,000 hours per quarter saved. DBS, GIC, Sea, and Supabase deploying Claude for developer and business functions.

#### 2026-10-14 - Claude Code: Idle Compaction and File-Mention Control ([source](https://code.claude.com/docs/en/changelog))
`[CODE]`

Two Claude Code updates shipped on October 14. Idle compaction: terminal sessions now compact long idle conversations before the prompt cache expires, avoiding full-context reprocessing on the next message. File-mention control: new environment variable `CLAUDE_CODE_DISABLE_FILE_MENTIONS` disables at-mention file expansion, so Claude receives file paths and reads files using its own tools rather than expanding them inline.

**How to use:** Idle compaction is automatic. To disable at-mention expansion: `export CLAUDE_CODE_DISABLE_FILE_MENTIONS=1` before starting a session.
