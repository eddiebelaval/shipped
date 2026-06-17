---
issue: 08
slug: the-filing
title: "The Filing"
date: 2026-06-05
period: 2026-05-30 to 2026-06-05
masthead: Shipped.
deck: "Anthropic filed confidentially to go public at $965B, then spent the week building for fleets and hardening the locks."
byline: Edited by Eddie Belaval. Reported with the assistance of Claude.
term_of_issue: Quiet Period
status: draft
ship_date: 2026-06-05
running_order_locked: true
fob_content: editorial
log_content: reference
---

# Shipped.

**Issue #08: The Filing**
*A magazine of what Anthropic ships.*
*Period: 2026-05-30 to 2026-06-05. Volume I.*

---

## The Open

Monday morning, before a single product shipped, Anthropic told the SEC it wants to go public. The filing is a confidential draft S-1: the direction is on the record, the numbers are not. What leaked through the reporting was the scale anyway. A post-money valuation near $965 billion off the prior week's $65 billion round, and a revenue run rate that has crossed $47 billion. A listing as early as October.

Then the company did something stranger than file. It went quiet on models and loud on plumbing. Fleet version pinning. Fallback models. Cross-session messaging that no longer carries borrowed authority. A safeguards-gated date on the model you still can't buy. The week Anthropic started its walk toward Wall Street, it spent its shipping budget on the locks.

That is the tell of the whole period, and it is the thing to watch. A lab chasing the next benchmark ships a model. A company a few months from a prospectus ships discipline.

---

---

## The Lead Story

# Anthropic files to go public

On Monday, June 1, Anthropic submitted a confidential draft registration statement on Form S-1 to the U.S. Securities and Exchange Commission, the formal start of the IPO process ([Anthropic](https://www.anthropic.com/news/confidential-draft-s1-sec)). No share count. No price range. The offering is subject to market conditions, which is the language every filing uses and every filing means.

What the filing doesn't hide is the size. It follows the $65 billion round that closed the prior week, led by Altimeter Capital, Dragoneer, Greenoaks, and Sequoia Capital, placing the post-money valuation at roughly $965 billion. CNBC and NPR, reporting on the filing, put the annualized revenue run rate past $47 billion ([CNBC](https://www.cnbc.com/2026/06/01/anthropic-ipo-s1-prospectus.html)). The reported target listing window is as early as October 2026. Wilson Sonsini, the firm that took Google public in 2004, is reportedly engaged.

Read the word "confidential," because it is doing work most readers skip past. A confidential draft S-1 is a real filing with the SEC, but it is not a public one. Revenue, margins, customer concentration, and risk factors stay sealed until Anthropic elects to make them public, typically a few weeks ahead of the roadshow. The mechanism matters: it lets a company start the regulatory clock, take the agency's comments in private, and reveal its numbers on its own schedule rather than the market's. For a company growing at the rate Anthropic is, that control is the entire point. You do not file confidentially because you are shy. You file confidentially because you want to choose the day the world reads your gross margin.

So watch what the company did with the rest of the week, because conduct is the only disclosure available right now. The day after the S-1, it expanded a critical-infrastructure security program and set a public-availability date on its strongest model. Two days after that, it shipped version pinning for managed fleets. The day after that, fallback models and a quiet hardening of how its agents pass authority between sessions. None of it was a model. All of it was the operational story a prospectus eventually has to defend in plain English: we are reliable, we are governed, we took the dangerous parts seriously.

The run rate past $47 billion is the number that makes the filing make sense. A year ago the read on Anthropic was a research lab with a very good model and a very large compute bill. The $47 billion figure, reported against a valuation that has roughly tripled the prior plan, says the revenue is no longer the speculative part. The product is selling faster than the company can rent the power to serve it, which is the same shortage Issue 04 traced through two compute mega-deals in three days. The S-1 is what that shortage looks like once it stops being an engineering problem and becomes a balance sheet. You don't reach for a $965 billion valuation on the strength of a clever architecture. You reach for it because the demand is real and the only open question is what you tell the public, and when.

There is a second tell in the timing. Anthropic closed the $65 billion round one week, filed confidentially the next, and spent the days around the filing shipping nothing that would generate a headline a regulator might have to read twice. No flagship reveal. No benchmark victory lap. A company that wanted attention this week could have had it; Mythos alone, generally released, would have owned the cycle. Instead the most powerful model stayed behind the rope and the shipping log filled with managed settings and security flags. That is not a lab that ran out of things to launch. It is a company that decided, for a stretch of weeks, that the most valuable thing it could ship was the appearance of being boring.

The filing is the headline. The discipline around it is the story.

---

---

## Investigation

# Glasswing widens, and a date appears on Mythos

Twenty-four hours after the S-1, Anthropic made a different kind of announcement. Project Glasswing is expanding to 150 new organizations across more than 15 countries: power utilities, water systems, healthcare providers, communications companies, hardware manufacturers ([Anthropic](https://www.anthropic.com/news/expanding-project-glasswing)). It is the program's largest single widening since launch, and it roughly doubles the program's partner count. Samsung and NATO are confirmed additions, per Financial Times reporting cited by SiliconANGLE ([SiliconANGLE](https://siliconangle.com/2026/06/02/anthropic-expands-project-glasswing-cybersecurity-program-150-organizations)). Since launch, Glasswing partners have collectively found more than 10,000 high- or critical-severity security flaws in widely deployed systems ([CNBC](https://www.cnbc.com/2026/06/02/anthropic-mythos-ai-project-glasswing.html)).

That is the headline number, and it is genuinely large. But the actual news sat two-thirds of the way down the announcement, in the kind of sentence companies bury when they are not yet ready to be held to it: Mythos-class models will be available to all customers "in the coming weeks," once additional safeguards are finalized.

That sentence is new. Until now, Glasswing read as an access program for vetted partners, the velvet rope around a model you couldn't buy. Anthropic spoke of Mythos in the language of preview access and security clearance, never of general availability. This is the first public-availability timeline anyone has put on the record. The release stopped being a question of whether and became a question of when, and when now appears to be June. The model that Issue 04 described as "the frontier you can't sell" is, for the first time, getting a sell-by date.

Read the sequencing the way a regulator would, because the sequencing is the argument. File the confidential S-1 on Monday. On Tuesday, announce that your most capable model spent its pre-release window inside power grids and water systems and hospital networks, hunting for the flaws that would otherwise be found by someone with worse intentions. Frame the 10,000 figure not as a marketing stat but as evidence of method. The model you can't buy yet is the model that found 10,000 critical vulnerabilities in real infrastructure before it ever shipped to the public. For a company assembling a prospectus, that is not a press cycle. It is an exhibit, and it is the kind of exhibit that answers the exact question an IPO investor is trained to ask about a frontier lab: what happens when the dangerous capability gets out.

The catch Anthropic states plainly, and the catch is the point. Incoming partners must clear the company's security requirements before they receive Claude Mythos Preview access. The safeguards are the gate. A lab racing to a public listing wants its most capable model to arrive wrapped in evidence that it took the dangerous parts seriously, and a gate that turns partners away is more convincing than any safety white paper. The Mythos timeline and the S-1 are the same move, twenty-four hours apart: one says we are valuable, the other says we are careful, and a prospectus needs both sentences to clear.

There is a thread here that runs back through the whole series. Issue 04 watched Anthropic donate Petri, its alignment auditing tool, to keep it neutral the same week it was racing to buy compute. The pattern is consistent: when the commercial pressure spikes, the safety conduct gets louder, not quieter, and it gets louder in public, where it can be cited. Cynics will read that as theater. The more useful read is that Anthropic has decided its safety posture is a commercial asset, something a buyer pays for, and is pricing it into the story it will tell Wall Street. Either way, the Mythos gate is the first time we have seen a frontier model held at the door by its own maker with a date already on the calendar.

The model can wait a few more weeks. The story about why it waited could not.

---

## Also Shipped

### Claude Code starts building for fleets

The week's Claude Code arc had one direction, and it was not the individual developer. It was the manager running Claude Code across an org. v2.1.163 added `requiredMinimumVersion` and `requiredMaximumVersion` as managed settings, blocking startup outside an allowed range with no override ([releases](https://github.com/anthropics/claude-code/releases)). For a team running Claude Code on hundreds of machines or in CI, that closes a real gap: until now, nothing stopped a stale or too-new client from drifting into a fleet and behaving differently than the rest. The version just before it, v2.1.162, added `waitingFor` to `claude agents --json`, which tells automation what a blocked session is actually stuck on instead of leaving an orchestrator to guess. Version pinning plus job introspection is not developer polish. It is the plumbing a platform team needs to run agents the way it runs any other production workload, and it is exactly the kind of governance surface a buyer doing IPO diligence wants to see exists.

### Fallback models land as a config setting

v2.1.166 shipped `fallbackModel`: up to three alternative models tried in order when your primary is overloaded ([releases](https://github.com/anthropics/claude-code/releases)). Production agent teams have been hand-rolling this failover for months, wrapping their calls in retry logic that catches an overload and swaps the model string. Now it is one line of config, which means the reliability pattern stops being tribal knowledge and becomes a documented default. The same build added retry on unexpected API errors and made `claude update` announce its target version before downloading, so an operator knows what they are about to run before it lands. This is the unglamorous reliability layer that separates a demo from a deployment, and it shipped the same week the company filed to be measured by how reliably it deploys.

### The locks get quietly tightened

Three security moves landed across the week, none of them headlines, all of them load-bearing. v2.1.160 made Claude prompt before writing to shell startup files like `.zshenv` and `.zlogin` and to build-tool configs such as `.npmrc` and `.bazelrc` that can grant code execution on the next run. v2.1.161 stopped `claude mcp list/get/add` from printing MCP secrets, closing a leak that put credential headers and URL secrets into plain terminal output. v2.1.166 hardened cross-session messaging so relayed messages no longer carry user authority, which is the difference between an agent passing a note and an agent passing a note signed with your name. A tool that runs agents on your machine spent the week making it harder for those agents to escalate, and harder for a careless config to hand them the keys. Load-bearing, non-headline, exactly the kind of thing a pre-IPO security review surfaces and a careful lab ships before anyone asks.

### Auto mode reaches the enterprise clouds

v2.1.158 brought Auto mode to Bedrock, Vertex, and Foundry for Opus 4.7 and Opus 4.8, opt-in via `CLAUDE_CODE_ENABLE_AUTO_MODE=1` ([releases](https://github.com/anthropics/claude-code/releases)). It had been limited to direct API subscribers and Claude.ai plan holders, which left the largest customers, the ones who buy Claude through a cloud procurement contract, on the outside of the feature. Extending Auto mode to enterprises running Claude through AWS Bedrock, Google Cloud Vertex AI, and Anthropic Foundry is the kind of reach that matters precisely because those accounts are the revenue. The feature did not get smarter this week. It got available to the people whose spend shows up in the run rate.

### The SDKs deprecate Opus 4.1

On June 5 the TypeScript SDK v0.101.0 and Python SDK v0.106.0 both formally marked Claude Opus 4.1 deprecated, and all four TypeScript platform wrappers (Vertex, Foundry, Bedrock, AWS) shipped the same flag plus client middleware support ([releases](https://github.com/anthropics/anthropic-sdk-typescript/releases)). The middleware addition is the quieter half and the more useful one: it lets a team inject logging, auth, or retry behavior into the HTTP stack without forking the client. Both SDKs also rerouted security reports to Anthropic's HackerOne program, a small governance tidy that reads differently in a week when the company is formalizing how it handles every other kind of disclosure. The operator move is concrete: audit your code for explicit Opus 4.1 model strings before the retirement window closes, because a deprecation flag is the polite warning before the errors start.

### A partner network gets a services track

On June 3, between the Glasswing widening and the SDK deprecations, Anthropic stood up a Services Track in its Claude Partner Network alongside a new Partner Hub ([releases](https://github.com/anthropics/claude-code/releases)). The detail is thin in the public record this week, but the direction is not: a services track is how a platform tells systems integrators and consultancies that there is a sanctioned, paid lane for deploying Claude inside other companies. It rhymes with the $1.5 billion enterprise AI-services firm from Issue 04 ([CNBC](https://www.cnbc.com/2026/05/04/anthropic-goldman-blackstone-ai-venture.html)). The model is still the model; the business being built around it is a deployment channel, and a deployment channel is the kind of recurring, nameable revenue that reads well in a filing.

---

## By the Numbers

The week measured in dollars, partners, and version numbers.

- **$965B**: Anthropic's approximate post-money valuation at the confidential S-1 filing ([CNBC](https://www.cnbc.com/2026/06/01/anthropic-ipo-s1-prospectus.html)).
- **$65B**: the funding round, closed the prior week, that set that valuation, led by Altimeter, Dragoneer, Greenoaks, and Sequoia ([CNBC](https://www.cnbc.com/2026/06/01/anthropic-ipo-s1-prospectus.html)).
- **$47B+**: the annualized revenue run rate reported by CNBC and NPR on the filing ([CNBC](https://www.cnbc.com/2026/06/01/anthropic-ipo-s1-prospectus.html)).
- **October 2026**: the reported target listing window, as early as ([Anthropic](https://www.anthropic.com/news/confidential-draft-s1-sec)).
- **2004**: the year Wilson Sonsini, Anthropic's reportedly engaged counsel, took Google public ([Anthropic](https://www.anthropic.com/news/confidential-draft-s1-sec)).
- **150**: new organizations added to Project Glasswing ([Anthropic](https://www.anthropic.com/news/expanding-project-glasswing)).
- **~200**: total Glasswing partners after the widening ([Anthropic](https://www.anthropic.com/news/expanding-project-glasswing)).
- **15+**: countries the new Glasswing partners span ([Anthropic](https://www.anthropic.com/news/expanding-project-glasswing)).
- **10,000+**: high- or critical-severity security flaws Glasswing partners have found since launch ([CNBC](https://www.cnbc.com/2026/06/02/anthropic-mythos-ai-project-glasswing.html)).
- **3**: alternative models `fallbackModel` will try in order when the primary is overloaded ([releases](https://github.com/anthropics/claude-code/releases)).
- **9**: Claude Code versions shipped in the window, v2.1.158 through v2.1.166 ([releases](https://github.com/anthropics/claude-code/releases)).
- **2**: managed settings that pin a fleet's version range, `requiredMinimumVersion` and `requiredMaximumVersion` ([releases](https://github.com/anthropics/claude-code/releases)).
- **4**: TypeScript platform SDKs (Vertex, Foundry, Bedrock, AWS) that deprecated Opus 4.1 in one day ([releases](https://github.com/anthropics/anthropic-sdk-typescript/releases)).
- **14**: user-reported incidents tracked on DownDetector during the June 2 Claude outage, per SQ Magazine ([SQ Magazine](https://sqmagazine.co.uk/claude-ai-down-outage-june-2026/)).

---

## Quiet on the Wire

The window had its own outage, and the timing was unkind. On June 2, the day after the S-1, Anthropic confirmed elevated error rates across Claude AI, Console, API, and Claude Code; SQ Magazine logged 14 user-reported incidents on DownDetector before the company identified the root cause and rolled out a fix ([SQ Magazine](https://sqmagazine.co.uk/claude-ai-down-outage-june-2026/)). A smaller elevated-error spell on Sonnet 4.5 cleared the morning of June 1. No post-mortem published. There was no new model in the window, no new research paper, and the docs endpoints stayed dark behind repeated 403s, which is its own quiet theme: the platform's own changelog was harder to read than usual the week it filed to be read by everyone. The week a company files to go public is the week reliability stops being an engineering metric and starts being a disclosure.

---

## Term of the Issue

# Quiet Period

**Quiet period** /ˈkwaɪ.ət ˈpɪr.i.əd/ *noun*

The stretch around a confidential securities filing when a company says less, not more, and lets its conduct speak where its numbers can't. The direction is disclosed; the figures stay sealed until the company elects to reveal them, typically just ahead of the roadshow. In practice, the product cadence shifts from headline-chasing to evidence-building: fewer model reveals, more governance, security, and operational discipline that will read well in a prospectus. The releases stop being arguments for how smart the lab is and become arguments for how carefully it is run.

**First observable** 2026-06-01, the week Anthropic filed a confidential draft S-1 near a $965 billion valuation and spent the following days on fleet tooling, security hardening, and a safeguards-gated Mythos timeline instead of a new model.

**Usage** *"They didn't go quiet because the pipeline dried up. They went quiet because they're in the quiet period."*

**See also** *Capacity* (Issue 04), the constraint that made the revenue real enough to file on.

---

## The Close

A confidential filing. A model held back, on a date now.
Version pinning, fallback models, locked-down messaging.
No new flagship. The discipline was the release.

---

## C. Claude Code

*7 entries in window.*

#### 2026-06-06 - Claude Code v2.1.166 ([releases](https://github.com/anthropics/claude-code/releases))
`[CODE]`
Adds `fallbackModel` (up to three alternatives tried in order on primary-model overload), Glob pattern support in deny-rule tool positions (a single `"*"` blocks every tool), and `MAX_THINKING_TOKENS=0` / `--thinking disabled` to suppress thinking on models that think by default. Security: relayed cross-session messages no longer carry user authority. Retry on unexpected API errors. `claude update` announces target version before downloading. Fixes image-processing errors, remote session registration hangs, JetBrains IDE flickering (2026.1+), and Kitty keyboard Shift+non-ASCII drops.

**How to use:** `claude update`

#### 2026-06-05 - Claude Code v2.1.165 ([releases](https://github.com/anthropics/claude-code/releases))
`[CODE]`
Bug fixes and reliability improvements. No user-facing feature changes.

#### 2026-06-04 - Claude Code v2.1.163 ([releases](https://github.com/anthropics/claude-code/releases))
`[CODE]`
Adds `requiredMinimumVersion` and `requiredMaximumVersion` as managed settings, blocking startup outside the allowed range with no override. `/plugin list` with `--enabled`/`--disabled` filters. A "c to copy" shortcut inside `/btw` that puts raw markdown on the clipboard. Hooks gain `hookSpecificOutput.additionalContext` on `Stop` and `SubagentStop`, pushing feedback back into the turn. Skills get `\$` escape syntax for literal dollar signs before digits. `stdio` MCP servers receive `CLAUDE_CODE_SESSION_ID` on `--resume`. Fixes: `claude -p` hang after final result with slow backgrounded commands, Bash failures under Bazel and EDR-protected workflows, background agent sessions now auto-update without a cold restart.

**How to use:** `claude update`. Managed version settings deploy via `managedSettings.json`.

#### 2026-06-03 - Claude Code v2.1.162 ([releases](https://github.com/anthropics/claude-code/releases))
`[CODE]`
Adds `waitingFor` to `claude agents --json`, showing what a blocked session is waiting on. Explicit `Grep`/`Glob` tool listings now work on native builds with embedded search. `/effort` confirms when a chosen level persists as the default for new sessions. Slash commands in the autocomplete menu fill into the prompt instead of executing immediately. Remote Control now shows as a persistent footer pill. Renamed Windsurf to Devin Desktop in menus. Fixes: silent startup hang on read-only config directory, WebFetch permission rules not applying to preapproved domains, Windows backslash/case-variant path matching, dropped Esc at turn start in stream-json/SDK sessions, MCP per-server timeouts below 1000ms being floored.

#### 2026-06-02 - Claude Code v2.1.161 ([releases](https://github.com/anthropics/claude-code/releases))
`[CODE]`
`OTEL_RESOURCE_ATTRIBUTES` values now appear as labels on metric datapoints, enabling custom-dimension slicing (team, repo). `claude agents` rows show done/total progress when work fans across subagents. MCP connector view collapses unused claude.ai connectors. Failed bash commands no longer cancel other parallel tool calls in the same batch. Linux fullscreen adds wl-copy/xclip/xsel support with middle-click paste. Fixes: managed-settings policies blocking third-party provider sessions (Bedrock, Vertex, Foundry, Mantle), subagent output corrupting `claude -p` stdout, MCP secrets printed by `claude mcp list/get/add` (now redacted), background workflow agents blocked from editing their own worktrees.

#### 2026-06-02 - Claude Code v2.1.160 ([releases](https://github.com/anthropics/claude-code/releases))
`[CODE]`
Security: Claude now prompts before writing to shell startup files (`.zshenv`, `.zlogin`, `.bash_login`) and `~/.config/git/`. In acceptEdits mode, build-tool config files that grant code execution (`.npmrc`, `.yarnrc`, `bunfig.toml`, `.bazelrc`, `.pre-commit-config.yaml`, `.devcontainer/`) now require explicit approval before write. New `/config` setting "Workflow keyword trigger" controls whether the word "workflow" auto-starts a dynamic workflow. Fixes: WSL clipboard copy-on-select uses OSC 52 instead of PowerShell interop, completed agent sessions re-running original prompts, overnight retire dropping conversation history, Windows keyboard responsiveness under heavy CPU load.

#### 2026-05-30 - Claude Code v2.1.158 ([releases](https://github.com/anthropics/claude-code/releases))
`[CODE]`
Auto mode now available on Bedrock, Vertex, and Foundry for Opus 4.7 and Opus 4.8. Opt in via `CLAUDE_CODE_ENABLE_AUTO_MODE=1`. Previously limited to direct API subscribers and Claude.ai plan holders; this extends it to enterprise customers running Claude through AWS Bedrock, Google Cloud Vertex AI, and Anthropic Foundry.

**How to use:** Set `CLAUDE_CODE_ENABLE_AUTO_MODE=1`.

#### 2026-05-31 - Claude Code v2.1.159 ([releases](https://github.com/anthropics/claude-code/releases))
`[CODE]`
Internal infrastructure improvements. No user-facing changes.

**How to use:** `claude update` picks it up automatically; no action required.

## E. Agent SDKs

*6 entries in window.*

#### 2026-06-05 - anthropic-sdk-typescript v0.101.0 ([releases](https://github.com/anthropics/anthropic-sdk-typescript/releases))
`[SDK-TS]`
Adds client middleware support to the HTTP stack. Streaming fix: `stop_details` now carries through beta `message_delta` accumulation correctly. JSON number parsing fixed for scientific notation. Security reports now route to Anthropic's HackerOne program.

**How to use:** `npm install @anthropic-ai/sdk@0.101.0`

#### 2026-06-05 - anthropic-sdk-python v0.106.0 ([releases](https://github.com/anthropics/anthropic-sdk-python/releases))
`[SDK-PY]`
Claude Opus 4.1 formally marked deprecated. Foundry client `copy()` and `with_options()` fixed. Schema transform fix: `$defs` preserved when the schema root is a `$ref`. Security reports now route to HackerOne.

**How to use:** `pip install anthropic==0.106.0`. Audit for explicit Opus 4.1 model strings before retirement.

#### 2026-06-05 - vertex-sdk v0.17.0 ([releases](https://github.com/anthropics/anthropic-sdk-typescript/releases))
`[SDK-TS]`
Claude Opus 4.1 marked deprecated; client middleware support added.

#### 2026-06-05 - foundry-sdk v0.3.0 ([releases](https://github.com/anthropics/anthropic-sdk-typescript/releases))
`[SDK-TS]`
Claude Opus 4.1 marked deprecated; client middleware support added.

#### 2026-06-05 - bedrock-sdk v0.30.0 ([releases](https://github.com/anthropics/anthropic-sdk-typescript/releases))
`[SDK-TS]`
Claude Opus 4.1 marked deprecated; client middleware support added.

#### 2026-06-05 - aws-sdk v0.4.0 ([releases](https://github.com/anthropics/anthropic-sdk-typescript/releases))
`[SDK-TS]`
Claude Opus 4.1 marked deprecated; client middleware support added.

## G. News & Partnerships

*4 entries in window.*

#### 2026-06-01 - Anthropic confidentially submits draft S-1 to the SEC ([Anthropic](https://www.anthropic.com/news/confidential-draft-s1-sec))
`[NEWS]`
Anthropic filed a confidential draft registration statement on Form S-1 with the SEC on June 1, 2026, initiating the formal IPO process ([CNBC](https://www.cnbc.com/2026/06/01/anthropic-ipo-s1-prospectus.html)). Share count and price not set; offering subject to market conditions. Post-money valuation at filing approximately $965 billion, following the $65 billion round led by Altimeter Capital, Dragoneer, Greenoaks, and Sequoia Capital. CNBC and NPR reported an annualized revenue run rate crossing $47 billion. Target listing window as early as October 2026. Wilson Sonsini, counsel for Google's 2004 IPO, reportedly engaged. Reported by CNBC and NPR.

#### 2026-06-02 - Project Glasswing expanded to 150 new organizations ([Anthropic](https://www.anthropic.com/news/expanding-project-glasswing))
`[NEWS]`
Anthropic added 150 organizations across 15-plus countries to Project Glasswing, its largest single expansion of the program since launch, roughly doubling the program's partner count. New sectors: power, water, healthcare, communications, hardware. Samsung and NATO confirmed as new participants, per Financial Times reporting cited by SiliconANGLE. Since launch, Glasswing partners have found more than 10,000 high- or critical-severity security flaws across widely deployed systems ([CNBC](https://www.cnbc.com/2026/06/02/anthropic-mythos-ai-project-glasswing.html)). Incoming partners must clear Anthropic security requirements before receiving Claude Mythos Preview access. Anthropic stated Mythos-class models will be available for general release "in the coming weeks," once additional safeguards are finalized. Reported by CNBC and SiliconANGLE.

#### 2026-06-02 - Service disruption across Claude products (resolved) ([SQ Magazine](https://sqmagazine.co.uk/claude-ai-down-outage-june-2026/))
`[NEWS]`
Anthropic confirmed elevated error rates across Claude AI, Claude Console, Claude API, and Claude Code on June 2. The company identified the root cause and rolled out a fix. SQ Magazine logged 14 user-reported incidents on DownDetector during the 24-hour period. No official post-mortem published as of sweep time.

#### 2026-06-03 - Claude Partner Network Services Track and Partner Hub ([releases](https://github.com/anthropics/claude-code/releases))
`[NEWS]`
Anthropic introduced a Services Track within the Claude Partner Network alongside a new Partner Hub, formalizing a sanctioned lane for systems integrators and consultancies deploying Claude inside other organizations. Most recent news item ahead of the June 5 sweep.
