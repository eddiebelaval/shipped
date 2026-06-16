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

Monday morning, before a single product shipped, Anthropic told the SEC it wants to go public. The filing is a confidential draft S-1: the direction is on the record, the numbers are not. What leaked through the reporting was the scale anyway: a $965 billion post-money valuation off last week's $65 billion round, and a revenue run rate that has crossed $47 billion. A listing as early as October.

Then the company did something stranger than file. It went quiet on models and loud on plumbing. Fleet version pinning. Fallback models. Cross-session messaging that no longer carries borrowed authority. The week Anthropic started its walk toward Wall Street, it spent its shipping budget on the locks.

---

---

## The Lead Story

# Anthropic files to go public

On Monday, June 1, Anthropic submitted a confidential draft registration statement on Form S-1 to the U.S. Securities and Exchange Commission, the formal start of the IPO process ([Anthropic](https://www.anthropic.com/news/confidential-draft-s1-sec)). No share count. No price range. The offering is subject to market conditions, which is the language every filing uses and every filing means.

What the filing doesn't hide is the size. It follows the $65 billion round that closed last week, led by Altimeter Capital, Dragoneer, Greenoaks, and Sequoia Capital, placing the post-money valuation at roughly $965 billion. CNBC and NPR, reporting on the filing, put the annualized revenue run rate past $47 billion ([CNBC](https://www.cnbc.com/2026/06/01/anthropic-ipo-s1-prospectus.html)). The reported target listing window is as early as October 2026. Wilson Sonsini, the firm that took Google public in 2004, is reportedly engaged.

Here is the tell. "Confidential" is doing work most readers skip past. Revenue, margins, and risk factors stay private until Anthropic elects to disclose them. A company a few months from a public listing has every incentive to look boring, predictable, governed. So watch what it did with the rest of the week. The day after the S-1, it expanded a security program and set a public-availability date on its strongest model. Two days after that, it shipped version pinning for managed fleets. That is not a lab chasing the next benchmark. It is a company building the operational story it will eventually have to defend in a prospectus.

The run rate past $47 billion is the number that makes the filing make sense. You don't file confidentially at $965 billion because you found a clever model. You file because the revenue is real and the only remaining question is what you tell the public, and when.

The filing is the headline. The discipline around it is the story.

---

---

## Investigation

# Glasswing widens, and a date on Mythos

Twenty-four hours after the S-1, Anthropic made a different kind of announcement. Project Glasswing is expanding to 150 new organizations across more than 15 countries: power utilities, water systems, healthcare providers, communications companies, hardware manufacturers ([Anthropic](https://www.anthropic.com/news/expanding-project-glasswing)). It is the program's largest single widening since launch. Samsung and NATO are confirmed additions, per Financial Times reporting cited by SiliconANGLE ([SiliconANGLE](https://siliconangle.com/2026/06/02/anthropic-expands-project-glasswing-cybersecurity-program-150-organizations)). Since launch, Glasswing partners have collectively found more than 10,000 high- or critical-severity security flaws in widely deployed systems ([CNBC](https://www.cnbc.com/2026/06/02/anthropic-mythos-ai-project-glasswing.html)).

That is the headline number, and it is impressive. The actual news sat two-thirds of the way down the announcement: Mythos-class models will be available to all customers "in the coming weeks," once additional safeguards are finalized.

That sentence is new. Until now, Glasswing read as an access program for vetted partners, the velvet rope around a model you couldn't buy. This is the first public-availability timeline. The release stopped being a question of whether and became a question of when, and when now appears to be June.

Read the sequencing the way a regulator would. File the S-1 on Monday. On Tuesday, announce that your most powerful model spent its pre-release window inside power grids and water systems hunting for the flaws that would otherwise be found by someone with worse intentions. The model you can't buy yet is the model that found 10,000 critical vulnerabilities before it shipped to the public. For a company assembling a prospectus, that is not a press cycle. It is an exhibit.

The catch Anthropic states plainly: incoming partners must clear the company's security requirements before they receive Claude Mythos Preview access. The safeguards are the gate, and the gate is the point. A lab racing to a public listing wants its most capable model to arrive wrapped in evidence that it took the dangerous parts seriously. The Mythos timeline and the S-1 are the same move, twenty-four hours apart.

The model can wait a few more weeks. The story about why it waited could not.

---

## Also Shipped

### Claude Code starts building for fleets

The week's Claude Code arc had one direction: managers, not individual developers. v2.1.163 added `requiredMinimumVersion` and `requiredMaximumVersion` as managed settings, blocking startup outside an allowed range with no override ([releases](https://github.com/anthropics/claude-code/releases)). For an org running Claude Code across hundreds of machines or in CI, that closes a real gap. The version before it added `waitingFor` to `claude agents --json`, telling automation what a blocked session is actually stuck on. Version pinning plus job introspection is fleet infrastructure, not developer polish.

### Fallback models land as a config setting

v2.1.166 shipped `fallbackModel`: up to three alternative models tried in order when your primary is overloaded ([releases](https://github.com/anthropics/claude-code/releases)). Production agent teams have been hand-rolling this failover for months. Now it is one line of config. The same build added retry on unexpected API errors and made `claude update` announce its target version before downloading. The unglamorous reliability layer that separates a demo from a deployment.

### The locks get quietly tightened

Three security moves landed across the week, none of them headlines. v2.1.160 made Claude prompt before writing to shell startup files and build-tool configs that grant code execution. v2.1.161 stopped `claude mcp list/get/add` from printing MCP secrets. v2.1.166 hardened cross-session messaging so relayed messages no longer carry user authority ([releases](https://github.com/anthropics/claude-code/releases)). A tool that runs agents on your machine spent the week making it harder for those agents to escalate. Load-bearing, non-headline, exactly the kind of thing a pre-IPO security review surfaces.

### Auto mode reaches the enterprise clouds

v2.1.158 brought Auto mode to Bedrock, Vertex, and Foundry for Opus 4.7 and Opus 4.8, opt-in via `CLAUDE_CODE_ENABLE_AUTO_MODE=1` ([releases](https://github.com/anthropics/claude-code/releases)). It had been limited to direct API subscribers and Claude.ai plan holders. Extending it to enterprise customers running Claude through AWS, Google Cloud, and Foundry is the kind of reach that matters when your largest accounts live behind a cloud procurement contract.

### The SDKs deprecate Opus 4.1

On June 5 the TypeScript SDK v0.101.0 and Python SDK v0.106.0 both formally marked Claude Opus 4.1 deprecated, and all four TypeScript platform wrappers (Vertex, Foundry, Bedrock, AWS) shipped the same flag plus client middleware support ([releases](https://github.com/anthropics/anthropic-sdk-typescript/releases)). Both SDKs also rerouted security reports to Anthropic's HackerOne program. Audit your code for explicit Opus 4.1 model strings before the retirement window closes.

---

## Quiet on the Wire

The window had its own outage. On June 2, Anthropic confirmed elevated error rates across Claude AI, Console, API, and Claude Code, beginning around 2:19 AM ET; it identified the root cause and rolled out a fix, with reports tracked on DownDetector per SQ Magazine ([SQ Magazine](https://sqmagazine.co.uk/claude-ai-down-outage-june-2026/)). A smaller elevated-error spell on Sonnet 4.5 cleared the morning of June 1. No post-mortem published. The week a company files to go public is the week reliability stops being an engineering metric and starts being a disclosure.

---

## Term of the Issue

# Quiet Period

**Quiet period** /ˈkwaɪ.ət ˈpɪr.i.əd/ *noun*

The stretch around a confidential securities filing when a company says less, not more, and lets its conduct speak where its numbers can't. The direction is disclosed; the figures stay sealed until the company elects to reveal them. In practice, the product cadence shifts from headline-chasing to evidence-building: fewer model reveals, more governance, security, and operational discipline that will read well in a prospectus.

**First observable** 2026-06-01, the week Anthropic filed a confidential draft S-1 at a $965 billion valuation and spent the following days on fleet tooling, security hardening, and a safeguards-gated Mythos timeline instead of a new model.

**Usage** *"They didn't go quiet because the pipeline dried up. They went quiet because they're in the quiet period."*

---

## The Close

A confidential filing. A model held back for safety.
Version pinning, fallback models, locked-down messaging.
No new flagship. The discipline was the release.

---

## C. Claude Code

*7 entries in window.*

#### 2026-06-06 - Claude Code v2.1.166 ([releases](https://github.com/anthropics/claude-code/releases))
`[CODE]`
Adds `fallbackModel` (up to three alternatives tried in order on primary-model overload), Glob pattern support in deny-rule tool positions (a single `"*"` blocks every tool), and `MAX_THINKING_TOKENS=0` / `--thinking disabled` to suppress thinking on models that think by default. Security: relayed cross-session messages no longer carry user authority. Retry on unexpected API errors. `claude update` announces target version before downloading. Fixes image-processing errors, remote session registration hangs, JetBrains IDE flickering (2026.1+), and Kitty keyboard Shift+non-ASCII drops. Shipped June 6 at 00:55 UTC.

**How to use:** `claude update`

#### 2026-06-05 - Claude Code v2.1.165 ([releases](https://github.com/anthropics/claude-code/releases))
`[CODE]`
Bug fixes and reliability improvements. No user-facing feature changes. Shipped June 5 at 05:45 UTC.

#### 2026-06-04 - Claude Code v2.1.163 ([releases](https://github.com/anthropics/claude-code/releases))
`[CODE]`
Adds `requiredMinimumVersion` and `requiredMaximumVersion` as managed settings, blocking startup outside the allowed range with no override. `/plugin list` with `--enabled`/`--disabled` filters. A "c to copy" shortcut inside `/btw` that puts raw markdown on the clipboard. Hooks gain `hookSpecificOutput.additionalContext` on `Stop` and `SubagentStop`, pushing feedback back into the turn. Skills get `\$` escape syntax for literal dollar signs before digits. `stdio` MCP servers receive `CLAUDE_CODE_SESSION_ID` on `--resume`. Fixes: `claude -p` hang after final result with slow backgrounded commands, Bash failures under Bazel and EDR-protected workflows, background agent sessions now auto-update without a cold restart. Shipped June 4 at 21:52 UTC.

**How to use:** `claude update`. Managed version settings deploy via `managedSettings.json`.

#### 2026-06-03 - Claude Code v2.1.162 ([releases](https://github.com/anthropics/claude-code/releases))
`[CODE]`
Adds `waitingFor` to `claude agents --json`, showing what a blocked session is waiting on. Explicit `Grep`/`Glob` tool listings now work on native builds with embedded search. `/effort` confirms when a chosen level persists as the default for new sessions. Slash commands in the autocomplete menu fill into the prompt instead of executing immediately. Remote Control now shows as a persistent footer pill. Renamed Windsurf to Devin Desktop in menus. Fixes: silent startup hang on read-only config directory, WebFetch permission rules not applying to preapproved domains, Windows backslash/case-variant path matching, dropped Esc at turn start in stream-json/SDK sessions, MCP per-server timeouts below 1000ms being floored. Shipped June 3 at 21:31 UTC.

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
Internal infrastructure improvements. No user-facing changes. Cleared the GitHub pipeline at 19:42 UTC (15:42 ET).

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

*3 entries in window.*

#### 2026-06-01 - Anthropic confidentially submits draft S-1 to the SEC ([Anthropic](https://www.anthropic.com/news/confidential-draft-s1-sec))
`[NEWS]`
Anthropic filed a confidential draft registration statement on Form S-1 with the SEC on June 1, 2026, initiating the formal IPO process ([CNBC](https://www.cnbc.com/2026/06/01/anthropic-ipo-s1-prospectus.html)). Share count and price not set; offering subject to market conditions. Post-money valuation at filing approximately $965 billion, following the $65 billion round led by Altimeter Capital, Dragoneer, Greenoaks, and Sequoia Capital. CNBC and NPR reported an annualized revenue run rate crossing $47 billion. Target listing window as early as October 2026. Wilson Sonsini, counsel for Google's 2004 IPO, reportedly engaged. Reported by CNBC and NPR.

#### 2026-06-02 - Project Glasswing expanded to 150 new organizations ([Anthropic](https://www.anthropic.com/news/expanding-project-glasswing))
`[NEWS]`
Anthropic added 150 organizations across 15-plus countries to Project Glasswing, its largest single expansion of the program since launch. New sectors: power, water, healthcare, communications, hardware. Samsung and NATO confirmed as new participants, per Financial Times reporting cited by SiliconANGLE. Since launch, Glasswing partners have found more than 10,000 high- or critical-severity security flaws across widely deployed systems. Incoming partners must clear Anthropic security requirements before receiving Claude Mythos Preview access. Anthropic stated Mythos-class models will be available for general release "in the coming weeks," once additional safeguards are finalized. Reported by CNBC and SiliconANGLE.

#### 2026-06-02 - Service disruption across Claude products (resolved) ([SQ Magazine](https://sqmagazine.co.uk/claude-ai-down-outage-june-2026/))
`[NEWS]`
Anthropic confirmed elevated error rates across Claude AI, Claude Console, Claude API, and Claude Code, with reports rising at 2:19 AM ET on June 2. The company identified the root cause and rolled out a fix. User-reported incidents tracked on DownDetector in the 24-hour period per SQ Magazine. No official post-mortem published as of sweep time.
