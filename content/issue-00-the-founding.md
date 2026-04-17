---
issue: 00
title: The Founding Issue — The Shadow Release
date: 2026-04-16
period: 2026-03-27 to 2026-04-16
status: dry-run
masthead: Shipped.
deck: "Three weeks of Anthropic, in one read. Plus: the model you can't have."
byline: Edited by Eddie Belaval. Reported with the assistance of Claude.
fob_content: editorial
log_content: reference
---

# Shipped.

**Issue #00 — The Founding Issue**
*A magazine of what Anthropic ships.*
*Period: 2026-03-27 → 2026-04-16. Volume I.*

---

## The Open

There's a thing Anthropic does now that doesn't have a name. They release a flagship model, and in the same breath, they tell you about a better one you can't have. Opus 4.6 in November. Opus 4.7 today. Mythos in between, gated, available only to a handful of security partners.

Call it the *shadow release*. The model that ships sets the floor. The model that doesn't reveals the ceiling. The space between them is where everyone who builds with this stuff now lives.

Three weeks of velocity below. Fifty-six releases — models, agents, infrastructure, a security pact with twelve names you'd recognize, twenty-six versions of Claude Code, a tokenizer change you'll feel in your bill. Plus the shadow.

---

## In This Issue

```
FRONT OF BOOK
  The Open                                       p.01
  By the Numbers — The shape of three weeks      p.02
  THE LEAD STORY  · The chart that wasn't
                    about Opus 4.7               p.04
  COMPANION       · Where each model wins        p.06
  FEATURE         · The agent stack got serious  p.08
  INVESTIGATION   · Glasswing                    p.10
  TIMELINE        · 21 days, 56 releases         p.13
  SURVEY          · Claude Code grew a body      p.15
  Cowork shipped, finally                        p.17
  Two papers worth your Friday                   p.18
  Term of the Issue · "shadow release"           p.19
  Quiet on the Wire                              p.20
  The Close                                      p.21

BACK OF BOOK — THE RELEASE LOG
  A · Models                                     p.21
  B · API & Platform                             p.22
  C · Claude Code (every version)                p.24
  D · Claude Apps                                p.27
  E · Agent SDKs (Python + TypeScript)           p.28
  F · Research & Publications                    p.30
  G · News & Partnerships                        p.31
  Sources & Bibliography                         p.32
  Colophon                                       p.34
```

---

## By the Numbers

> **THE SHAPE OF THREE WEEKS**
>
> **56** — releases shipped, March 27 through April 16
> **26** — versions of Claude Code, v2.1.85 through v2.1.111
> **20** — Agent SDK releases (10 Python, 10 TypeScript)
> **12** — founding organizations in Project Glasswing
> **1** — frontier model held back from public release (Mythos Preview)
>
> **— The Opus 4.7 Sweep —**
>
> **87.6%** — Opus 4.7 SWE-bench Verified (vs 80.8% on 4.6)
> **64.3%** — Opus 4.7 SWE-bench Pro · *leads the field*
> **98.5%** — Opus 4.7 XBOW Visual-Acuity (vs 54.5% on 4.6 · **+44 pts**)
> **70%** — Opus 4.7 CursorBench (vs 58% on 4.6 · +12 pts)
> **94.2%** — Opus 4.7 GPQA Diamond
> **77.3%** — Opus 4.7 MCP-Atlas (scaled tool use, leads the field)
> **90.9%** — Opus 4.7 BigLaw Bench (Harvey, high-effort)
> **3×** — Opus 4.7 production tasks resolved per attempt vs 4.6 (Rakuten-SWE-Bench)
>
> **— The Mythos Bar —**
>
> **93.9%** — Mythos Preview SWE-bench Verified · *top of the chart*
> **94.5%** — Mythos GPQA Diamond
> **97.6%** — Mythos USAMO
> **83.1%** — Mythos CyberGym vulnerability score (Opus 4.6: 66.6%)
> **6.3 pts** — gap between Opus 4.7 and Mythos on SWE-bench Verified
> **181** — working Firefox shell exploits Mythos produced in trial
> **2** — working Firefox shell exploits Opus 4.6 produced in the same trial
> **90×** — exploit ratio between the two models
> **10** — fully patched OSS-Fuzz targets Mythos achieved control-flow hijack on
> **27** — years, age of the oldest OpenBSD bug Mythos identified
> **16** — years, age of the FFmpeg flaw Mythos found across 5M prior fuzz hits
>
> **— The Glasswing Commitment —**
>
> **$100M** — model credits Anthropic committed to Glasswing partners
> **$4M** — donated to OpenSSF, Apache, Alpha-Omega for open-source security
> **40+** — additional organizations in early conversation beyond the 12 founders
>
> **— The Operator Numbers —**
>
> **$5 / $25** — Opus 4.7 pricing per million input/output tokens (unchanged from 4.6)
> **1.0–1.35×** — tokenizer change in Opus 4.7. Same input, more tokens
> **3** — free `/ultrareview` cloud reviews per Pro/Max user
> **2,576px** — long-edge image resolution in Opus 4.7 (3× prior versions)
>
> **— The Calendar —**
>
> **June 15, 2026** — Sonnet 4 and Opus 4 retire from the API
> **April 30, 2026** — Sonnet 4.5 / Sonnet 4 1M-context beta dies
> **90 days** — until Glasswing's first public progress report

---

## The Lead Story

# The chart that wasn't about Opus 4.7

Opus 4.7 went generally available this morning. Same pricing as 4.6 — five dollars per million input, twenty-five per million output. Better at coding, sharper on hard software engineering, with the kind of self-verification that previously required you to paper over with scaffolding. Vision tripled in resolution: 2,576 pixels on the long edge, more than three times what prior versions could see. The model can now read dense screenshots and pixel-perfect references without you down-sampling first.

A new effort level called `xhigh` slotted in between `high` and `max`. Claude Code now defaults to `xhigh` on every plan. If you're paying attention to your bills, that change matters as much as anything else in the launch — `xhigh` produces more thinking tokens than `high`, and Anthropic raised the default before most users will notice.

The migration notes mention a tokenizer change: the same input may consume 1.0 to 1.35× more tokens depending on what you feed it. Re-tune your prompts. The bill will tell you which way it broke.

The vision change deserves its own paragraph. At 2,576 pixels on the long edge — roughly 3.75 megapixels — Opus 4.7 can read a full-density desktop screenshot without you cropping or scaling. Diagrams that used to need OCR pre-processing can now go in raw. UI mockups can be referenced pixel-for-pixel for code generation. This isn't a knob; it's a workflow change for anyone who's been hand-feeding the model lower-resolution slices.

But the headline isn't the model.

The headline is the chart Anthropic published next to the model.

> *That's the news. Anthropic shipped a flagship and conceded, in the same breath, that it isn't the frontier.*

It shows Opus 4.7 beating Opus 4.6. Beating GPT-5.4. Beating Gemini 3.1 Pro across the relevant benchmarks. And then it shows Opus 4.7 losing to a fourth bar labeled *Mythos Preview*. The fourth bar is taller than every other bar. The fourth bar is the model you can't use.

> ### CHART — SWE-bench Verified
>
> *The launch chart, recreated. The orange bar is the model you cannot call.*
>
> | Model | Score | |
> |---|---:|---|
> | Gemini 3.1 Pro | **80.6%** | ▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰ |
> | Opus 4.6 | **80.8%** | ▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰ |
> | GPT-5.4 | **84.5%** | ▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰ |
> | **Opus 4.7** | **87.6%** | ▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰ |
> | **Mythos Preview** *(gated)* | **93.9%** | ▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰ |
>
> *Source: Anthropic Opus 4.7 announcement, April 16, 2026.*

That's the news. Anthropic shipped a flagship and conceded, in the same breath, that it isn't the frontier. The frontier is in a vault, working on the OSS-Fuzz corpus, finding 27-year-old vulnerabilities in OpenBSD. Opus 4.7 is the floor of what you can buy this week. Mythos is the ceiling of what exists. The distance between them is the new normal — and Anthropic has decided that the distance, for now, is a feature, not a bug.

The implication is institutional, not technical. For the first time, the lab has an internal precedent for "we found something too dangerous to ship in the standard channel." That precedent will be invoked again. Probably soon. The next time it happens, the chart will look familiar.

> ### Sidebar — The Mythos Bar
>
> **A profile of the model you can't use.**
>
> Where Opus 4.6 hits 66.6% on the CyberGym vulnerability-reproduction benchmark, Mythos Preview hits 83.1%. Where Opus 4.6 produced two working Firefox shell exploits in several hundred attempts, Mythos produced 181. On the OSS-Fuzz corpus, Mythos achieved full control-flow hijack on ten separate, fully patched targets.
>
> The vulnerabilities Mythos has surfaced are subtle, old, or both:
>
> — **A 27-year-old vulnerability in OpenBSD.** Survived decades of human review.
> — **A 16-year-old flaw in FFmpeg.** Automated fuzzing missed it across 5 million test hits.
> — **Multiple Linux kernel privilege escalation chains.** Subtle race conditions and KASLR bypasses, autonomously discovered.
> — **A Firefox JIT heap-spray.** Chained four vulnerabilities to escape both renderer and OS sandboxes.
>
> You can't have it. Mythos is gated to twelve security partners under Project Glasswing. Anthropic's stated reason is risk: a model that finds zero-days in OpenBSD that survived twenty-seven years of human review is a model you don't put on the open API.
>
> Whether that calculus holds — for how long, and under what pressure — is the open question of the year.

---

## Companion to the Lead

# Where each model wins — the cross-benchmark sweep

Eight benchmarks Anthropic published in the Opus 4.7 launch, with comparable scores from competitor models where reported. **Bold** = winner. **Orange bold** = Mythos Preview leads.

| Benchmark | Opus 4.6 | Opus 4.7 | GPT-5.4 | Gemini 3.1 Pro | Mythos |
|---|---:|---:|---:|---:|---:|
| **SWE-bench Verified** *(general SWE)* | 80.8% | 87.6% | 84.5% | 80.6% | **🟧 93.9%** |
| **SWE-bench Pro** *(agentic SWE)* | — | **64.3%** | 57.7% | 54.2% | — |
| **GPQA Diamond** *(graduate reasoning)* | 91.3% | 94.2% | 94.4% | 94.3% | **🟧 94.5%** |
| **MCP-Atlas** *(scaled tool use)* | 75.8% | **77.3%** | 68.1% | 73.9% | — |
| **CursorBench** *(IDE agentic)* | 58.0% | **70.0%** *(+12)* | — | — | — |
| **XBOW Visual-Acuity** *(vision)* | 54.5% | **98.5%** *(+44)* | — | — | — |
| **BigLaw Bench** *(Harvey, legal)* | — | **90.9%** | — | — | — |
| **CyberGym** *(vulnerability repro)* | 73.8% | — | — | — | **🟧 83.1%** |

The pattern is the news. Opus 4.7 leads or ties on every benchmark Anthropic published — except the two Mythos sits on. **Anthropic now ships the second-best model and tells you who's first.**

The +44-point XBOW jump deserves its own paragraph. Vision tripled in resolution to 2,576px on the long edge, and the model's ability to read dense screenshots, extract from complex diagrams, and reference pixel-perfect detail moved from "useful with pre-processing" to "send the raw screenshot." If you've been hand-feeding cropped slices into 4.6, stop. 4.7 sees what 4.6 couldn't.

The +12 CursorBench gain is the IDE-agentic story. Opus 4.7 inside Cursor is materially better at the multi-file edit + test loop than 4.6 was. Expect Cursor adoption to spike.

*Source: Anthropic Opus 4.7 announcement, anthropic.com/news/claude-opus-4-7. Mythos figures cross-referenced with red.anthropic.com Mythos Preview disclosure. Em-dash = no published score for that model on that benchmark.*

---

## Feature

# The agent stack got serious

For the past year, every team building agents on Claude has been writing the same code. A sandbox, a tool harness, a context manager, a streaming loop. The interfaces varied. The components didn't. Anyone who's built an agent in production has shipped some version of all four.

April 8 and 9 was the week Anthropic shipped all four primitives. The era of writing your own loop is closing. Anthropic is taking that work in-house.

**Managed Agents** went into public beta on April 8 (header `managed-agents-2026-04-01`). Fully managed harness with secure sandboxing, built-in tools, and server-sent event streaming. You create agents and configure containers through the API — what used to be a Kubernetes problem, an IAM problem, and a tool-routing problem becomes one HTTP call. The pricing model is unannounced; the implication is that Anthropic intends to compete with whatever your in-house agent platform looks like, on its own infrastructure.

**The advisor tool** shipped April 9 (`advisor-tool-2026-03-01`). The pattern is simple and overdue: pair a faster executor model with a higher-intelligence advisor that provides strategic guidance mid-generation. Long-horizon agentic workloads get close to advisor-solo quality at executor-model cost. If you've been running Sonnet 4.6 for the bulk work and bouncing to Opus 4.6 for the hard turns, the advisor tool just made that pattern a primitive instead of an architecture.

**The `ant` CLI** dropped the same day. A command-line client for the Claude API with native Claude Code integration and YAML-based versioning of API resources — skills, agents, deployments. The implication is bigger than the tool: agents are becoming versionable, declarative configurations rather than code. Treat your agent definitions like Terraform.

> ### Sidebar — Composition example
>
> ```python
> # Old: write your own executor + advisor loop
> while not done:
>     plan = opus.messages.create(model="claude-opus-4-7", ...)
>     for step in plan:
>         result = sonnet.messages.create(
>             model="claude-sonnet-4-6",
>             messages=[..., step],
>         )
>
> # New: one call, advisor inline
> response = client.messages.create(
>     model="claude-sonnet-4-6",
>     advisor={"model": "claude-opus-4-7", "trigger": "auto"},
>     messages=[...],
>     extra_headers={"anthropic-beta": "advisor-tool-2026-03-01"},
> )
> ```

The week's three releases compose. You can run a Managed Agent that uses the advisor tool internally, with the agent definition versioned as YAML through `ant`. None of this is theoretical — the docs ship with examples that combine all three.

What this means for the people who built their own agent loops: most of that code is now a glue layer. Some of it remains differentiated — your prompt library, your domain-specific tools, your retrieval pipeline. The harness, the sandbox, the streaming, the context window management — those are commodity now. If your competitive moat was the loop, your moat just shrank.

---

## Investigation

# Glasswing

On April 7, twelve organizations agreed to use a model none of their customers can touch.

Project Glasswing is the consortium Anthropic announced alongside Mythos Preview's gated release. The founders: Amazon Web Services, Apple, Broadcom, Cisco, CrowdStrike, Google, JPMorgan Chase, the Linux Foundation, Microsoft, NVIDIA, Palo Alto Networks, and Anthropic itself. Forty-plus additional organizations are in early conversation. The goal, stated plainly: harden the world's most critical software infrastructure against a class of vulnerabilities that AI can now find faster than humans can patch them.

The financial structure is unusual for a security consortium. $100M in model credits committed by Anthropic to Glasswing participants — meaning the partners pay nothing for the inference. $2.5M donated to Alpha-Omega and OpenSSF. $1.5M to the Apache Software Foundation. The donations matter because they answer the obvious objection: this isn't a private security tool for big vendors. The funding is meant to flow to open-source maintainers who don't have security teams.

> *"The window between vulnerability discovery and exploitation has collapsed — what took months now happens in minutes."*
> — Igor Tsyganskiy, Microsoft · [Source](https://www.anthropic.com/glasswing)

Mythos has already produced results. The model has identified zero-day vulnerabilities in every major operating system and every major web browser tested against it. The depth is what gets attention from people who've spent careers in this work: the bugs aren't surface-level. Many are subtle, old, and survived prior automated tooling. A 27-year-old OpenBSD bug. A 16-year-old FFmpeg flaw. Linux kernel privilege escalation chains that no published fuzzer has caught. The Firefox exploit Mythos wrote chained four separate vulnerabilities into a sandbox escape — the kind of compound exploit that a senior offensive security researcher might produce in a multi-week engagement.

> *"The old ways of hardening systems are no longer sufficient."*
> — Anthony Grieco, Cisco · [Source](https://www.anthropic.com/glasswing)

The benchmark Mythos is being judged against is CyberGym, an academic vulnerability-reproduction suite. Mythos hits 83.1%. Opus 4.6 — the previous publicly available frontier model — hits 66.6%. The Firefox-specific test is more dramatic: Opus 4.6 produced two working JavaScript shell exploits across several hundred attempts. Mythos produced 181.

> ### CHART — The Firefox Trial
>
> *Same browser, same vulnerability surface, same number of attempts.*
>
> ```
>   Opus 4.6   ┃ 2
>   Mythos     ┃ ████████████████████████████████████  181
> ```
>
> A **90× ratio** in working browser exploits. The capability gap is not "better." It is categorical. This is why Mythos is gated.
>
> *Source: Project Glasswing announcement (April 7, 2026), cross-referenced with AISI evaluation.*

> *"This initiative offers a credible path to making AI-augmented security a trusted tool for every maintainer, not just those with expensive teams."*
> — Jim Zemlin, the Linux Foundation · [Source](https://www.anthropic.com/glasswing)

The hard question is institutional, not technical. Anthropic has now established an internal precedent: a model that passes evaluations can still be held back from public release on safety grounds. The Glasswing framing is "defensive use only." But the model exists. The capability exists. The concession in the Opus 4.7 launch chart was that the capability can't be reproduced by you, no matter how much you pay.

The next time Anthropic invokes this precedent, what will the criteria be? What does the second Glasswing look like? When does the cybersecurity rationale extend to other categories — biological, cognitive, financial — and what's the institutional process for making that call? Anthropic has 90 days to publish the first Glasswing progress report. Read it carefully. The methodology will be precedent.

> ### Sidebar — What Mythos has found
>
> Selected zero-days surfaced by Mythos Preview in pre-deployment testing, per Anthropic and the Project Glasswing announcement:
>
> | Vulnerability | System | Age | Method |
> |---|---|---|---|
> | Memory corruption | OpenBSD | 27 years | Direct identification |
> | Logic flaw | FFmpeg | 16 years | Exposed where 5M fuzz hits failed |
> | Privilege escalation chain | Linux kernel | n/a | Race conditions + KASLR bypass |
> | JIT heap-spray | Firefox | n/a | 4-vuln chain → renderer + OS sandbox escape |
> | Control-flow hijack | OSS-Fuzz corpus | n/a | 10 fully patched targets compromised |
>
> All vulnerabilities have been disclosed to maintainers under embargo. The model is not available outside Glasswing.

---

## Timeline

# 21 days, 56 releases

```
MAR 27 ●               v2.1.85 (Claude Code) · Python SDK v0.1.51
MAR 28 ●●              v2.1.86, v2.1.87
MAR 29 ●               Python SDK v0.1.52
MAR 30 ●●●             v2.1.90 · max_tokens 300k batch beta
                       1M-context retirement notice (Sonnet 4.5/4)
MAR 31 ●●              v2.1.91 · Python SDK v0.1.53
APR 02 ●●              v2.1.92 · Python SDK v0.1.54
APR 03 ●●              v2.1.94 · Python SDK v0.1.55
APR 04 ●●              v2.1.96 · Python SDK v0.1.56
APR 07 ●●●●●           PROJECT GLASSWING + MYTHOS PREVIEW
                       Bedrock Messages API research preview
APR 08 ●●●             Managed Agents · ant CLI · TS SDK v0.2.97
APR 09 ●●●●●●●         COWORK GA
                       Advisor tool · Claude Code v2.1.98 + v2.1.101
                       Python SDK v0.1.57 + v0.1.58 · TS SDK v0.2.98
APR 10 ●               TS SDK v0.2.101 (security release)
APR 13 ●●●●            v2.1.105 · Python SDK v0.1.59
                       TS SDK v0.2.104 + v0.2.105
APR 14 ●●●●●●●         v2.1.107 + v2.1.108 · TS SDK v0.2.107 + v0.2.108
                       Sonnet 4 / Opus 4 deprecation
                       Automated Alignment Researchers paper
                       Vas Narasimhan to Long-Term Benefit Trust
APR 15 ●●●             v2.1.110 · TS SDK v0.2.109 + v0.2.110
APR 16 ●●●●●●●         CLAUDE OPUS 4.7 LAUNCH
                       Claude Code v2.1.111 · Python SDK v0.1.60
                       TS SDK v0.2.111 · Apps update
```

Read the bumps. Three of the seven weekdays in the window saw single-digit releases. Two weekdays saw seven-plus. April 7 (Glasswing), April 9 (Cowork + advisor + multiple SDK releases), April 14 (paper drop + deprecations + board appointment), and April 16 (Opus 4.7 launch wave) form the spine of the period. Between those peaks: continuous, unspectacular shipping. That's the pattern of a lab that does not rest.

---

## Survey

# Claude Code grew a body

Twenty-six versions shipped between v2.1.85 (March 27) and v2.1.111 (today). Most were point releases: bug fixes, env var additions, plugin tweaks. But woven through them is a clear arc — the CLI is becoming an IDE, and the IDE is becoming a control plane.

**Routines** are the most consequential addition (v2.1.101 area). A routine is a saved Claude Code configuration — prompt, repos, connectors — packaged once and run automatically on Anthropic's cloud. If you've been wondering when "agent that ships code on a schedule" stops being a custom build, the answer is: now. The infrastructure is hosted. The scheduling is configurable. The cost model is "you pay for the inference" — same as your interactive sessions.

**The UI redesign** (v2.1.110-111) is the most visible shift. Multiple Claude sessions side by side in one window, with a sidebar. Integrated terminal. File editing. HTML and PDF preview. A faster diff viewer. Anthropic is not subtle about the trajectory. The CLI is becoming the work environment.

**`/ultrareview`** (v2.1.111) is comprehensive parallel-analysis code review using cloud compute. Pro and Max users get three free per month. The implication: code review is now a heavyweight LLM task that shouldn't run on your local terminal — it should run on Anthropic's compute and stream back. A pattern other heavy commands will follow.

**`/team-onboarding`** (v2.1.101) generates a teammate ramp-up guide from your local Claude Code usage. It's a small feature with a quietly large implication: your AI usage patterns are themselves documentation. Future hires read your transcript shape to learn how to use the tools.

**Other moves worth tracking:** Push notifications (v2.1.110) so Claude can alert you on mobile when a long task finishes. PowerShell rollout on Windows (v2.1.111). Auto mode for Max subscribers without flags (v2.1.111). The `Monitor` tool for streaming background script events (v2.1.98). Subprocess sandboxing with PID namespaces on Linux (v2.1.98). PreCompact hooks with blocking capability (v2.1.105). Plugins that ship executables under `bin/` (v2.1.91). The `if` field on hooks for conditional firing (v2.1.85).

The closing question, after twenty-six versions in twenty-one days: when does Claude Code stop being a CLI? The answer is not far. The diff viewer is faster than your IDE's. The terminal is integrated. The file editor is in the sidebar. The cloud routines are running while you sleep. At some point — probably this year — saying "Claude Code is a CLI" will be technically true and effectively obsolete.

---

## Cowork shipped, finally

Claude Cowork went generally available on macOS and Windows on April 9, ending what felt like a long beta. The headline is GA itself. Cowork is Anthropic's bet on AI-native team collaboration — not a shared document with AI features bolted on, but a shared agent that works alongside the team and persists across members.

Three additions made the GA more than a milestone. **Role-based access controls for Enterprise plans** mean admins can carve up which teams get which Cowork capabilities. The pattern is familiar from any enterprise SaaS, but the implication for AI access control is new — what does it mean to scope an autonomous agent to one department's data and not another's? Cowork is the first product that has to answer.

**Cowork analytics in the API** exposes engagement and adoption data programmatically. You can route it into your existing observability stack. **OpenTelemetry support** is the second half of the same move — Cowork activity becomes telemetry like any other production system.

The harder question is adoption. Whether teams use Cowork the way Anthropic hopes — as a persistent collaborator, not a chat sidebar — depends on whether teams reorganize their workflows to give the agent something to persist. Two quarters from now, we'll know whether Cowork is Slack's AI replacement or Microsoft Bob.

---

## Two papers worth your Friday

**Automated Alignment Researchers** (April 14). Anthropic on using LLMs to scale scalable oversight. The premise: alignment work is itself a research program with bottlenecks, and LLMs may be the right tool to speed up the human researchers' own labor. The paper benchmarks the technique. Read it next to the Mythos disclosure: the same week the lab publicly held a model back for safety, they're publishing on how to use models to do the safety work faster. The two are not unrelated. If you're scaling capability, you have to scale oversight at the same rate or the gap becomes the story. This paper is Anthropic's bet on closing the gap.

**Emotion Concepts in Large Language Models** (March, on `transformer-circuits.pub`). Researchers found internal representations of emotion concepts in Claude that generalize across contexts and behaviors. The finding: when Claude is asked to reason about a frustrated user, the same internal representation activates as when Claude is reasoning about a frustrated character in a story — and that representation measurably changes the model's behavior in both cases.

The wrong question is whether the models *have* emotions. The right question, which the paper is built around, is whether they have *coherent internal representations* of emotions that change what they output. The answer the paper supports is yes. For builders, the practical implication is that prompting strategies that lean on emotional context — "the user is frustrated and needs reassurance" — are operating on something more substantive than persona. They're activating a stable internal pattern.

Both papers point at the same underlying program: the lab is trying to do interpretability and oversight at the speed of capability. Whether they can keep pace is the question that matters most this decade.

---

## Term of the Issue

> **shadow release**  /SHA-doh ree-LEES/ *noun*
>
> A pattern in which a frontier AI lab announces a flagship model while simultaneously revealing — through a benchmark chart, a press mention, or an explicit acknowledgment — that a more capable internal model exists but will not be made available to the public.
>
> The shipped model sets the floor of capability buyers can access. The shadow model reveals the ceiling of capability that exists. The space between is where institutional decisions about AI deployment now live.
>
> **First observable instance:** Anthropic's Opus 4.7 launch (April 16, 2026), in which the announcement chart placed Mythos Preview as the top bar — taller than every released model from Anthropic or its competitors — and noted that Mythos remains gated to security partners under Project Glasswing.
>
> **Usage:** *"We're shipping the executor model and shadow-releasing the planner."*

---

## Quiet on the Wire

Mythos broad release — no date, no signal, no roadmap visible. Project Glasswing's first 90-day report will be the next read on whether the gating posture holds. The Bedrock Messages API research preview is `us-east-1` only; regional rollout unannounced. Sonnet 4 and Opus 4 retire from the API on **June 15, 2026** — if you haven't migrated, the clock started two days ago. Sonnet 4.5's 1M-context beta dies April 30. The Long-Term Benefit Trust appointed Vas Narasimhan to the Board of Directors on April 14; the pharma-and-policy axis of governance is worth watching over the next quarter for biotech and regulated-industry deal flow.

Notable absences: no fast-mode preview for Opus 4.7 yet, no Haiku 5 signal, no Opus 4.7 on Vertex AI's edge regions, no public roadmap for the `ant` CLI's Windows binary. All gaps. All worth watching.

---

## The Close

Three weeks. Fifty-six releases. One model you can buy, one you can't.

The shadow is the news.

Build accordingly.

---

# The Release Log

*A 1:1 mirror of every Anthropic release in the window. Use it as reference. Share it with your team.*

---

## A. Models

#### 2026-04-16 — Claude Opus 4.7 ([announcement](https://www.anthropic.com/news/claude-opus-4-7))
`[MODEL]`

Anthropic's most capable generally available model. Coding, vision, and self-verification gains over 4.6. New `xhigh` effort level slots between `high` and `max`. Vision processes images up to 2,576px on long edge (3× prior). Tokenizer change — same input may consume 1.0–1.35× more tokens.

**How to use:**
```python
client.messages.create(
    model="claude-opus-4-7",
    effort={"level": "xhigh"},
    messages=[...]
)
```
Pricing unchanged: $5 / $25 per MTok. Available on Claude API, Bedrock, Vertex, Foundry, GitHub Copilot. Re-tune prompts; stricter instruction-following may surprise legacy code.

**Why it matters:** First flagship where Anthropic explicitly conceded a stronger internal model (Mythos) exists.

#### 2026-04-07 — Claude Mythos Preview (gated) ([Glasswing](https://www.anthropic.com/glasswing))
`[MODEL]`

Unreleased frontier model with strikingly capable cybersecurity performance. 83.1% on CyberGym (vs. Opus 4.6's 66.6%). Found zero-days in every major OS and browser including a 27-year-old OpenBSD bug.

**How to use:** Invitation-only, defensive cybersecurity work only, via [Project Glasswing](https://www.anthropic.com/glasswing). Not available on the public API.

---

## B. API & Platform

#### 2026-04-16 — Opus 4.7 API release + tokenizer change ([release notes](https://platform.claude.com/docs/en/release-notes/api))
`[API]`

Includes API breaking changes vs. Opus 4.6. New tokenizer means token counts shift 1.0–1.35×. Migration guide published.

**How to use:** Read the [Opus 4.7 migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide#migrating-to-claude-opus-4-7) before upgrading. Audit your prompt tokenizer counts before swapping model IDs.

#### 2026-04-14 — Sonnet 4 / Opus 4 deprecation ([deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations))
`[DEPRECATION]`

`claude-sonnet-4-20250514` and `claude-opus-4-20250514` retire **June 15, 2026**.

**How to use:** Migrate Sonnet 4 → `claude-sonnet-4-6`, Opus 4 → `claude-opus-4-7`. After June 15 these model IDs return errors.

#### 2026-04-09 — Advisor tool (public beta)
`[API]`

Pair a faster executor with a higher-intelligence advisor that provides strategic guidance mid-generation. Long-horizon agent runs approach advisor-solo quality at executor cost.

**How to use:** Add beta header `advisor-tool-2026-03-01` to requests. See [advisor tool docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool).

#### 2026-04-08 — Claude Managed Agents (public beta)
`[API]`

Fully managed agent harness — secure sandboxing, built-in tools, SSE streaming, container configuration via API.

**How to use:** Add beta header `managed-agents-2026-04-01`. Create agents and run sessions via the new endpoints. See [Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview).

#### 2026-04-08 — `ant` CLI launch
`[API]`

Command-line client for the Claude API with native Claude Code integration and YAML-based versioning of API resources (skills, agents, deployments).

**How to use:** Install per [CLI reference](https://platform.claude.com/docs/en/api/sdks/cli). Use to script API resource lifecycle outside the console.

#### 2026-04-07 — Messages API on Amazon Bedrock (research preview)
`[API]`

First-party Claude API request shape now available on Bedrock at `/anthropic/v1/messages` endpoint. Runs on AWS-managed infrastructure with zero operator access.

**How to use:** Available in `us-east-1` only. Contact your Anthropic account executive for access. See [Claude in Amazon Bedrock research preview](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock-research-preview).

#### 2026-03-30 — Message Batches API max_tokens raised to 300k
`[API]`

For Opus 4.6 and Sonnet 4.6 only. Long-form content, structured data, large code generation now supported in single batch turns.

**How to use:** Add beta header `output-300k-2026-03-24` to batch requests.

#### 2026-03-30 — 1M context beta deadline (April 30) for Sonnet 4.5 / Sonnet 4
`[DEPRECATION]`

After April 30, 2026, the `context-1m-2025-08-07` beta header has no effect on Sonnet 4.5/4. Requests over 200k return errors.

**How to use:** Migrate to Sonnet 4.6 or Opus 4.6 (both support 1M context at standard pricing, no header).

---

## C. Claude Code

*Every version shipped in window, newest first. Source: [CHANGELOG.md](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md).*

#### 2026-04-16 — v2.1.111
`[CODE]`

Opus 4.7 `xhigh` available, Auto mode for Max subscribers, interactive `/effort` slider, "Auto (match terminal)" theme, `/less-permission-prompts` skill, `/ultrareview` cloud code review, PowerShell rollout on Windows, Plan files named after user prompts, `Ctrl+U`/`Ctrl+Y` clear/restore input buffer.

**How to use:** `claude update`. Run `/ultrareview` in any session for parallel-analysis cloud code review. `/effort` opens the slider for reasoning depth.

#### 2026-04-15 — v2.1.110
`[CODE]`

`/tui` flicker-free fullscreen rendering, push notification tool for mobile alerts, `Ctrl+O` toggles transcript verbosity, `/focus` toggles focus view, `/plugin` Installed tab with priority sorting, session recap for telemetry-disabled users.

**How to use:** Run `/tui` for fullscreen mode. Configure push notifications via `/config`. Use `/focus` to hide non-essential UI during deep work.

#### 2026-04-14 — v2.1.109 / v2.1.108 / v2.1.107
`[CODE]`

v2.1.109: Improved extended-thinking indicator with rotating progress hint.
v2.1.108: `ENABLE_PROMPT_CACHING_1H` env var for 1-hour cache TTL, recap feature for session context after returning, model can discover and invoke built-in slash commands via Skill tool, `/undo` as alias for `/rewind`.
v2.1.107: Thinking hints displayed sooner during long operations.

**How to use:** `export ENABLE_PROMPT_CACHING_1H=1` to enable 1-hour cache. Configure recap behavior in `/config`. Use `/undo` interchangeably with `/rewind`.

#### 2026-04-13 — v2.1.105
`[CODE]`

`path` parameter added to EnterWorktree tool, PreCompact hook with blocking capability, plugin background monitor support via manifest key, `/proactive` alias for `/loop`, 5-minute abort timeout for stalled API streams.

**How to use:** Configure PreCompact hook in `.claude/settings.json` to block compaction. Plugins can declare `monitors` in their manifest for background processes.

#### 2026-04-09 — v2.1.101
`[CODE]`

`/team-onboarding` generates teammate ramp-up guide from your local usage, OS CA certificate store trusted by default, `/ultraplan` auto-creates cloud environment, improved brief mode retry logic.

**How to use:** Run `/team-onboarding` to produce a markdown ramp-up doc tailored to your codebase usage patterns.

#### 2026-04-09 — v2.1.98
`[CODE]`

Interactive Vertex AI setup wizard, `CLAUDE_CODE_PERFORCE_MODE` env var for Perforce support, Monitor tool for streaming background script events, subprocess sandboxing with PID namespace on Linux.

**How to use:** Run `/setup-vertex` for the wizard. Set `CLAUDE_CODE_PERFORCE_MODE=1` if you use Perforce. Linux users get tighter subprocess isolation by default.

#### 2026-04-08 — v2.1.97
`[CODE]`

Focus view toggle in `NO_FLICKER` mode, `refreshInterval` status line setting for periodic command re-runs.

**How to use:** Set `refreshInterval` in your status line config to auto-refresh expensive checks.

#### 2026-04-04 — v2.1.96
`[CODE]`

Fixed Bedrock authorization failures with `AWS_BEARER_TOKEN_BEDROCK`.

**How to use:** Bedrock users hitting auth failures should update.

#### 2026-04-03 — v2.1.94
`[CODE]`

Amazon Bedrock powered by Mantle support via `CLAUDE_CODE_USE_MANTLE=1`, default effort level changed to `high` for most user tiers, compact Slack message headers with clickable links.

**How to use:** Set `CLAUDE_CODE_USE_MANTLE=1` for Mantle-routed Bedrock. Effort default upgrade is automatic on update.

#### 2026-04-02 — v2.1.92
`[CODE]`

`forceRemoteSettingsRefresh` policy setting for fail-closed remote config, interactive Bedrock setup wizard, per-model and cache-hit breakdown in `/cost`, `/release-notes` as interactive version picker.

**How to use:** Run `/cost` for the new breakdown view. `/release-notes` lets you scroll past versions interactively.

#### 2026-03-31 — v2.1.91
`[CODE]`

MCP tool result persistence override via `_meta` annotation, `disableSkillShellExecution` setting to disable inline shell, multi-line prompt support in deep links, plugins can ship executables under `bin/`.

**How to use:** Set `disableSkillShellExecution: true` in settings to lock down skill-driven shell. Plugin authors can now ship binaries.

#### 2026-03-30 — v2.1.90
`[CODE]`

`/powerup` interactive feature lessons, `CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE` for offline environments, fixed infinite loop on rate-limit dialog.

**How to use:** Run `/powerup` for short lessons on under-used features.

#### 2026-03-29 — v2.1.89
`[CODE]`

"defer" permission decision for `PreToolUse` hooks in headless sessions, `CLAUDE_CODE_NO_FLICKER=1` for flicker-free alt-screen rendering, `PermissionDenied` hook fires after auto mode denials, named subagents in `@` mention suggestions.

**How to use:** Hooks can now return `"defer"` to delay permission decisions in headless mode. Set `CLAUDE_CODE_NO_FLICKER=1` if your terminal flickers.

#### 2026-03-28 — v2.1.87 / v2.1.86
`[CODE]`

v2.1.87: Fixed message delivery in Cowork Dispatch.
v2.1.86: `X-Claude-Code-Session-Id` header for API request aggregation, `.jj` and `.sl` excluded from VCS directory scans.

**How to use:** Cowork users on Dispatch should update. The new session header is set automatically — useful for grouping API observability.

#### 2026-03-27 — v2.1.85
`[CODE]`

`CLAUDE_CODE_MCP_SERVER_NAME` and `CLAUDE_CODE_MCP_SERVER_URL` env vars, conditional `if` field for hooks using permission rule syntax, timestamp markers for scheduled task firing.

**How to use:** Hooks can now have conditional `if` fields (same syntax as permission rules). Useful for selective hook activation.

---

## D. Claude Apps

#### 2026-04-16 — Opus 4.7 in Claude apps ([release notes](https://support.claude.com/en/articles/12138966-release-notes))
`[APPS]`

Opus 4.7 available across web, mobile, and desktop with vision and SWE improvements.

**How to use:** Update mobile/desktop. Web auto-uses latest. Select Opus 4.7 in the model picker.

#### 2026-04-09 — Claude Cowork GA on macOS and Windows
`[APPS]`

Cowork out of beta. RBAC for Enterprise plans, OpenTelemetry support, Cowork analytics in the Analytics API, custom roles per group.

**How to use:** Enterprise admins: configure groups and assign roles in Console. Pipe Cowork telemetry to your existing observability stack via OTel.

#### 2026-03-25 — Interactive apps in Claude mobile (iOS/Android)
`[APPS]`

Live charts, sketches, and shareable assets render visually in conversations.

**How to use:** Update the iOS/Android app. Visualizations now render inline.

#### 2026-03-23 — Computer use research preview for Pro/Max
`[APPS]`

Claude can access screens and perform tasks independently. Plus Claude Code Dispatch improvements.

**How to use:** Pro/Max users opt in to the computer use preview from settings. Read the [computer use guide](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool) before granting screen access.

#### 2026-03-17 — Persistent agent thread for Cowork on mobile
`[APPS]`

Manage Cowork tasks from phones via Claude Desktop or mobile.

**How to use:** Cowork tasks now persist across mobile sessions — no need to start fresh.

#### 2026-03-12 — Inline charts, diagrams, visualizations
`[APPS]`

Claude creates custom charts and diagrams inline in responses on web.

**How to use:** Just ask: "make a chart of X" or "diagram this architecture." Renders in the response.

#### 2026-03-11 — Claude for Excel and PowerPoint enhancements
`[APPS]`

Add-ins now share conversation context across docs, support skills, and connect to Bedrock / Vertex AI / Foundry via LLM gateway.

**How to use:** Update the add-ins. Skills authored in Console show up inside Excel/PowerPoint.

---

## E. Agent SDKs

### Python — `claude-agent-sdk`

#### 2026-04-16 — v0.1.60 ([releases](https://github.com/anthropics/claude-agent-sdk-python/releases))
`[SDK-PY]`

`list_subagents()` and `get_subagent_messages()` session helpers, W3C trace context propagation to CLI subprocess (OpenTelemetry), cascading session deletion. Bug fix: `setting_sources=[]` no longer silently dropped. Bundled CLI to v2.1.111.

**How to use:** `pip install -U "claude-agent-sdk[otel]"` for distributed tracing support.

#### 2026-04-13 — v0.1.59
`[SDK-PY]`

Bundled CLI to v2.1.105.

**How to use:** `pip install -U claude-agent-sdk`.

#### 2026-04-09 — v0.1.58 / v0.1.57
`[SDK-PY]`

v0.1.58: Bundled CLI to v2.1.97.
v0.1.57: `exclude_dynamic_sections` option on `SystemPromptPreset` for cross-user cache hits, `"auto"` PermissionMode, fixed `thinking={"type": "adaptive"}` mapping.

**How to use:** Use `exclude_dynamic_sections=True` to maximize cache hits across users with different dynamic content.

#### 2026-04-04 — v0.1.56
`[SDK-PY]`

Bundled CLI to v2.1.92.

#### 2026-04-03 — v0.1.55
`[SDK-PY]`

Fixed silent truncation of MCP tool results >50K chars (`maxResultSizeChars` now forwarded). Bundled CLI to v2.1.91.

#### 2026-04-02 — v0.1.54
`[SDK-PY]`

Internal release.

#### 2026-03-31 — v0.1.53
`[SDK-PY]`

Fixed `--setting-sources` empty string when not provided, fixed `query()` deadlock with string prompt + hooks/MCP. Bundled CLI to v2.1.88.

#### 2026-03-29 — v0.1.52
`[SDK-PY]`

`get_context_usage()` on `ClaudeSDKClient`, `typing.Annotated` parameter descriptions in JSON schema, `ToolPermissionContext` exposes `tool_use_id` and `agent_id`, `session_id` option on `ClaudeAgentOptions`. Fix: `connect(prompt="...")` no longer drops string prompt.

**How to use:** `client.get_context_usage()` returns current session token usage. Annotate parameters with `Annotated[str, "description"]` for richer schemas.

#### 2026-03-27 — v0.1.51
`[SDK-PY]`

`fork_session()`, `delete_session()`, offset-based pagination, `task_budget` option, `SystemPromptFile` support, AgentDefinition gets `disallowedTools`/`maxTurns`/`initialPrompt`. Plus 10+ fixes to async generator cleanup, MCP tool handling, env filtering, process cleanup.

**How to use:** Use `fork_session(session_id)` to branch a session. Pass `task_budget={"input_tokens": N}` to cap a run.

### TypeScript — `@anthropic-ai/claude-agent-sdk`

#### 2026-04-16 — v0.2.111 ([releases](https://github.com/anthropics/claude-agent-sdk-typescript/releases))
`[SDK-TS]`

Opus 4.7 support, `mcp_set_servers` per-tool `permission_policy` for HTTP/SSE servers, `startup()` and `WarmQuery` now public API, `options.env` overlays `process.env` instead of replacing.

**How to use:** `npm install -D @anthropic-ai/claude-agent-sdk@latest`. Use `WarmQuery` for pre-warmed sessions.

#### 2026-04-15 — v0.2.110
`[SDK-TS]`

Fixed `unstable_v2_createSession` not respecting `cwd`/`settingSources`/`allowDangerouslySkipPermissions`. New `shouldQuery: false` field on `SDKUserMessage` to append a message without triggering an assistant turn.

**How to use:** Send `{ shouldQuery: false }` to inject context without burning a model turn.

#### 2026-04-15 — v0.2.109
`[SDK-TS]`

Parity with Claude Code v2.1.109.

#### 2026-04-14 — v0.2.108 / v0.2.107
`[SDK-TS]`

v0.2.108: `SDKStatus` includes `'requesting'`; with `includePartialMessages` enabled, emits a `system/status/requesting` message before each API request.
v0.2.107: Parity with Claude Code v2.1.107.

#### 2026-04-13 — v0.2.105 / v0.2.104
`[SDK-TS]`

v0.2.105: Added `system/memory_recall` event and `memory_paths` on `system/init`. Fixed `error_max_structured_output_retries` emitted when final retry succeeded.
v0.2.104: CHANGELOG updates.

**How to use:** Subscribe to `system/memory_recall` events to see when the agent reads from memory.

#### 2026-04-10 — v0.2.101
`[SDK-TS]`

Security: bumped `@anthropic-ai/sdk` to `^0.81.0` and `@modelcontextprotocol/sdk` to `^1.29.0` (GHSA-5474-4w2j-mq4c). Fixed Windows resume-session temp directory leak. Fixed `MaxListenersExceededWarning` with 11+ concurrent `query()` calls.

**How to use:** **Security update — upgrade.** `npm update @anthropic-ai/claude-agent-sdk`.

#### 2026-04-09 — v0.2.98
`[SDK-TS]`

Parity with Claude Code v2.1.98.

#### 2026-04-08 — v0.2.97
`[SDK-TS]`

Parity with Claude Code v2.1.97.

---

## F. Research & Publications

#### 2026-04-14 — Automated Alignment Researchers (paper)
`[RESEARCH]`

"Using large language models to scale scalable oversight." Anthropic on having LLMs perform alignment work, with benchmarks for whether the technique holds.

**How to use:** Read the paper if you work on agent guardrails. Citations are useful for justifying LLM-based eval pipelines.

**Why it matters:** Same week Anthropic held Mythos back for safety, they're publishing on automating the safety work itself. The two are connected.

#### 2026-03 — Emotion Concepts in Large Language Models ([transformer-circuits](https://transformer-circuits.pub/2026/emotions/index.html))
`[RESEARCH]`

Internal representations of emotions in Claude that generalize across contexts and shape behavior.

**Why it matters:** The wrong question is whether the models *have* emotions. The right one is whether they have coherent internal representations that change output.

---

## G. News & Partnerships

#### 2026-04-14 — Vas Narasimhan to Long-Term Benefit Trust Board
`[NEWS]`

The LTBT appointed Vas Narasimhan (former Novartis CEO) to the Board of Directors.

**Why it matters:** Adds pharma-and-policy weight to Anthropic governance. Worth watching for biotech and regulated-industry deal flow.

#### 2026-04-07 — Project Glasswing launched ([Glasswing](https://www.anthropic.com/glasswing))
`[NEWS]`

12-organization consortium using Claude Mythos Preview to harden critical software infrastructure. Founders: AWS, Apple, Google, Microsoft, NVIDIA, Cisco, CrowdStrike, JPMorganChase, Linux Foundation, Palo Alto Networks, Broadcom, Anthropic. $100M in model credits. $4M to OpenSSF, Apache, Alpha-Omega.

**How to use:** Open-source maintainers of critical infrastructure can apply for Mythos access via Glasswing partners. Participation by application.

**Why it matters:** First time Anthropic explicitly held a model back, post-evaluation, on safety grounds that survived peer review. Sets a precedent.

---

## Sources & Bibliography

*Every URL consulted in the reporting of Issue #00. Verify any claim against its source.*

### A. Anthropic — Primary announcements

- **[Introducing Claude Opus 4.7](https://www.anthropic.com/news/claude-opus-4-7)** — Anthropic, April 16, 2026. Flagship announcement, benchmark chart, capability claims.
- **[Project Glasswing](https://www.anthropic.com/glasswing)** — Anthropic, April 7, 2026. Consortium founders, financial commitments, member quotes.
- **[Claude Mythos Preview](https://red.anthropic.com/2026/mythos-preview/)** — Anthropic Red, April 7, 2026. Capability disclosure, vulnerability findings, Glasswing rationale.
- **[What 81,000 people want from AI](https://www.anthropic.com/81k-interviews)** — Anthropic, March 18, 2026. Background reference for usage patterns.
- **[Introducing Claude Sonnet 4.6](https://www.anthropic.com/news/claude-sonnet-4-6)** — Anthropic, February 17, 2026. Migration target reference.
- **[Anthropic News (index)](https://www.anthropic.com/news)** — Master index used to identify all in-window announcements.

### B. Anthropic — Release notes & documentation

- **[Claude API release notes](https://platform.claude.com/docs/en/release-notes/api)** — Authoritative source for API/Platform entries (March 27 – April 16).
- **[Claude Code CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)** — Source of all 26 Claude Code versions catalogued (v2.1.85 → v2.1.111).
- **[Claude Apps release notes](https://support.claude.com/en/articles/12138966-release-notes)** — Web, mobile, desktop, Cowork updates.
- **[Python Agent SDK releases](https://github.com/anthropics/claude-agent-sdk-python/releases)** — All 10 Python SDK releases in window (v0.1.51 → v0.1.60).
- **[TypeScript Agent SDK releases](https://github.com/anthropics/claude-agent-sdk-typescript/releases)** — All 10 TypeScript SDK releases in window (v0.2.97 → v0.2.111).
- **[Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview)** — Beta documentation.
- **[Advisor tool documentation](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool)** — Beta-header reference.
- **[Opus 4.7 migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide#migrating-to-claude-opus-4-7)** — Tokenizer change, breaking changes.
- **[Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations)** — Sonnet 4 / Opus 4 / Haiku 3 retirement schedule.
- **[Claude in Amazon Bedrock (research preview)](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock-research-preview)** — Bedrock Messages API endpoint.
- **[Computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)** — Referenced in Claude Apps section.
- **[`ant` CLI reference](https://platform.claude.com/docs/en/api/sdks/cli)** — Command-line client docs.

### C. Research & engineering publications

- **Automated Alignment Researchers** — Anthropic, paper, April 14, 2026. *"Using large language models to scale scalable oversight."*
- **[Emotion Concepts and their Function in a Large Language Model](https://transformer-circuits.pub/2026/emotions/index.html)** — Transformer Circuits, March 2026.
- **[Alignment Faking in Large Language Models](https://assets.anthropic.com/m/983c85a201a962f/original/Alignment-Faking-in-Large-Language-Models-full-paper.pdf)** — Anthropic, prior work referenced for context.
- **[Natural Emergent Misalignment from Reward Hacking in Production RL](https://assets.anthropic.com/m/74342f2c96095771/original/Natural-emergent-misalignment-from-reward-hacking-paper.pdf)** — Anthropic, prior work referenced for context.

### D. News coverage & independent analysis

- **[Anthropic rolls out Claude Opus 4.7, an AI model that is less risky than Mythos](https://www.cnbc.com/2026/04/16/anthropic-claude-opus-4-7-model-mythos.html)** — CNBC, April 16, 2026.
- **[Anthropic releases Claude Opus 4.7, concedes it trails unreleased Mythos](https://www.axios.com/2026/04/16/anthropic-claude-opus-model-mythos)** — Axios, April 16, 2026.
- **[Anthropic rolls out Claude Opus 4.7, an AI model that is less risky than Mythos](https://www.cnbc.com/2026/04/16/anthropic-claude-opus-4-7-model-mythos.html)** — CNBC, April 16, 2026.
- **[Anthropic reveals new Opus 4.7 model with focus on advanced software engineering](https://9to5mac.com/2026/04/16/anthropic-reveals-new-opus-4-7-model-with-focus-on-advanced-software-engineering/)** — 9to5Mac, April 16, 2026.
- **[Anthropic debuts preview of powerful new AI model Mythos in new cybersecurity initiative](https://techcrunch.com/2026/04/07/anthropic-mythos-ai-model-preview-security/)** — TechCrunch, April 7, 2026.
- **[Anthropic Releases Claude Mythos Preview with Cybersecurity Capabilities but Withholds Public Access](https://www.infoq.com/news/2026/04/anthropic-claude-mythos/)** — InfoQ, April 2026.
- **[Six Reasons Claude Mythos Is an Inflection Point for AI—and Global Security](https://www.cfr.org/articles/six-reasons-claude-mythos-is-an-inflection-point-for-ai-and-global-security)** — Council on Foreign Relations.
- **[Anthropic's Mythos Preview and the End of a Twenty-Year Cybersecurity Equilibrium](https://postquantum.com/security-pqc/anthropic-mythos-preview-ai-offensive-security/)** — PostQuantum.
- **[Anthropic's Project Glasswing — restricting Claude Mythos to security researchers — sounds necessary to me](https://simonwillison.net/2026/Apr/7/project-glasswing/)** — Simon Willison, April 7, 2026.
- **[Anthropic's Glasswing Project with Mythos — Weekly AI Newsletter](https://medium.com/nlplanet/anthropics-glasswing-project-with-mythos-weekly-ai-newsletter-april-13th-2026-c846ba5c16ec)** — Generative AI / Medium, April 13, 2026.
- **[Anthropic adds routines to redesigned Claude Code](https://9to5mac.com/2026/04/14/anthropic-adds-repeatable-routines-feature-to-claude-code-heres-how-it-works/)** — 9to5Mac, April 14, 2026.
- **[Anthropic's Claude Code gets automated 'routines' and a desktop makeover](https://siliconangle.com/2026/04/14/anthropics-claude-code-gets-automated-routines-desktop-makeover/)** — SiliconANGLE, April 14, 2026.
- **[Anthropic Paper Examines Behavioral Impact of Emotion-Like Mechanisms in LLMs](https://www.infoq.com/news/2026/04/anthropic-paper-llms/)** — InfoQ, April 2026.

### E. Independent evaluations & benchmark sources

- **[Our evaluation of Claude Mythos Preview's cyber capabilities](https://www.aisi.gov.uk/blog/our-evaluation-of-claude-mythos-previews-cyber-capabilities)** — UK AI Safety Institute. Independent third-party assessment.
- **CyberGym** — Academic vulnerability-reproduction benchmark. Source for the 83.1% / 66.6% comparison.
- **OSS-Fuzz** — Google open-source fuzzing project. Source for the "10 fully patched targets" claim.

### F. Quote attributions

- **Igor Tsyganskiy, Microsoft.** *"The window between vulnerability discovery and exploitation has collapsed — what took months now happens in minutes."* Source: Project Glasswing announcement.
- **Anthony Grieco, Cisco.** *"The old ways of hardening systems are no longer sufficient."* Source: Project Glasswing announcement.
- **Jim Zemlin, the Linux Foundation.** *"This initiative offers a credible path to making AI-augmented security a trusted tool for every maintainer, not just those with expensive teams."* Source: Project Glasswing announcement.

### G. Aggregator references (cross-checked, not cited)

- **[Releasebot — Anthropic updates index](https://releasebot.io/updates/anthropic)** — Used to verify nothing was missed.
- **[Releasebot — Claude Code updates](https://releasebot.io/updates/anthropic/claude-code)** — Cross-check for Claude Code coverage.
- **[Releasebot — Claude updates](https://releasebot.io/updates/anthropic/claude)** — Cross-check for app/model coverage.

---

*Total sources consulted: 40+. All claims in the editorial front-of-book and the Release Log are traceable to one or more of the above. If you find a missing citation, file it back via `/shipped --issue 00 --revise`.*

---

## Colophon

*Shipped. is set in Libre Baskerville (editorial) and Barlow Condensed (mechanical) on Inter (systematic). Issue #00 is a dry-run; the front-of-book covers three weeks instead of one to stress-test the format at maximum size. Future issues cover seven days at lower volume — same skeleton, fewer entries, same density discipline.*

*Edited by Eddie Belaval. Reported with the assistance of Claude. Voice anchored by [STYLE.md](STYLE.md). Designed per [DESIGN.md](DESIGN.md). Generated by `/shipped`.*

***Shipped.***
