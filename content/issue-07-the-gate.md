---
issue: 07
slug: the-gate
title: "The Gate"
date: 2026-05-29
period: 2026-05-24 to 2026-05-29
masthead: Shipped.
deck: "The model Anthropic held back found 10,000 bugs, flickered into Claude Code, then got a release date — the same week a $65B raise valued the company at $965B."
byline: Edited by Eddie Belaval. Reported with the assistance of Claude.
term_of_issue: The Gate
status: draft
ship_date: 2026-05-29
running_order_locked: true
fob_content: editorial
log_content: reference
---

# Shipped.

**Issue #07: The Gate**
*A magazine of what Anthropic ships.*
*Period: 2026-05-24 to 2026-05-29. Volume I.*

---

## The Open

There is a model you cannot buy. It is called Mythos, and for two months Anthropic has kept it behind a gate, handing it only to about fifty vetted partners on the grounds that it can find and exploit vulnerabilities in every major operating system and browser when you point it at one.

This week the gate started to swing. On Monday, the model's track record posted: more than 10,000 high- and critical-severity bugs in a single month. The same day, "claude-mythos-1-preview" flickered into Claude Code's model picker, then vanished. On Thursday, a flagship you can buy. On Friday, a $65 billion check and a sentence that reframed the whole week: Mythos is coming to everyone in "coming weeks."

The week was never about the model that shipped. It was about the one that's about to.

---

---

## The Lead Story

# The model they couldn't keep behind the glass

The most consequential release of the week is one Anthropic hasn't shipped yet.

Start with the evidence. On Monday, Anthropic published its first formal update on Project Glasswing, the program that lets a gated model — Claude Mythos Preview — loose on real software ([Anthropic](https://www.anthropic.com/research/glasswing-initial-update)). The numbers are not subtle. Roughly fifty partners found more than 10,000 high- or critical-severity vulnerabilities in the program's first month. Cloudflare alone reported 2,000 bugs, 400 of them high or critical, at a false-positive rate its own team rated better than human testers. Mozilla fixed 271 vulnerabilities in Firefox 150 — ten times the rate it got from an earlier Claude model. Anthropic's own scan of more than 1,000 open-source projects turned up an estimated 6,202 high- and critical-severity findings out of 23,019 total.

Anthropic named the problem in its own words: "The relative ease of finding vulnerabilities compared with the difficulty of fixing them amounts to a major challenge for cybersecurity." Translation: the tool that finds the holes is now far ahead of the labor that patches them.

Then the slip. The same Monday, users spotted "claude-mythos-1-preview" in Claude Code's model picker and in Claude Security, alongside a string in the source: "Access to the Claude Mythos model in Claude Code and Claude Security" ([BleepingComputer](https://www.bleepingcomputer.com/news/artificial-intelligence/anthropics-restricted-claude-mythos-model-may-be-coming-to-claude-code/)). Both vanished fast. Anthropic said nothing. Not a release — a seam showing.

The seam closed into a date on Friday. In the same window it announced a $65 billion raise, Anthropic told customers it had made "swift progress" on safety safeguards and would release Mythos-level models to all customers in "coming weeks," first reported by Bloomberg ([Insurance Journal](https://www.insurancejournal.com/news/national/2026/05/29/871703.htm)). The first public timeline on a model the company previously said it was holding back because it could exploit every major OS and browser when directed.

Read the three beats together. The capability is proven at scale. The plumbing already has Mythos wired in. The timeline is now weeks, not "someday." The gate didn't open this week. It got a hinge.

---

---

## Also Shipped

### Opus 4.8, at the old price

On Thursday Anthropic shipped Claude Opus 4.8, and the honesty numbers carry it: it's the first Claude model to score 0% on uncritically accepting and reporting flawed results, with overconfidence more than tenfold lower than 4.7 ([Anthropic](https://www.anthropic.com/news/claude-opus-4-8)). USAMO 2026 jumped from 69.3% to 96.7%; SWE-bench Pro went from 64.3% to 69.2%; long-context F1 at 1M tokens nearly doubled to 68.1%. Pricing held at $5/$25 per MTok, and Fast mode got cheaper too: the same 2.5x speed now costs less of a premium than it did on 4.7. The flagship got better and didn't get more expensive — which, in a week measured in billions, is its own kind of statement.

### Dynamic workflows turn one task into hundreds of agents

Claude Code v2.1.154 shipped the same day as Opus 4.8 and carried the feature that names the direction: dynamic workflows, a research preview where you describe a large task and Claude spins up tens to hundreds of background subagents to run it in parallel ([GitHub](https://github.com/anthropics/claude-code/releases)). Opus 4.8 defaults to high effort in Claude Code; a lean system prompt is now standard for every model except the older ones; `! <command>` runs a shell command as a detachable background session. The CLI keeps eating the orchestration layer one release at a time.

### The system prompt can now change mid-conversation

Quieter than the model, with longer legs: the Claude API now accepts `role: "system"` messages after a user turn on Opus 4.8 ([Anthropic](https://www.anthropic.com/news/claude-opus-4-8)). System prompts were fixed at conversation start for the entire history of the API. Now an agent can rewrite its own operating instructions mid-session without tearing down the conversation. If you build long-horizon agents, this is the line in the release notes you re-read.

### The first partner broadcast

On Wednesday at 8:30 AM, Anthropic held The First Broadcast, its inaugural partner webinar, covering the month's product news and standing up the Anthropic Partner Academy with a new Claude Partner Certification going live alongside it ([Anthropic](https://www.anthropic.com/webinars/the-first-broadcast)). A global replay was set for May 28 at 11:00 AM SGT. No product in it, but the signal is real: a company building a certified channel is a company that expects partners to sell on its behalf at scale.

### Claude Code shipped six times in five days

While the headlines went to models and money, the CLI kept its weekday metronome. v2.1.152 made `/code-review --fix` apply findings to the working tree and dropped Auto mode's opt-in consent; v2.1.153 added terminal-aware status lines and surfaced macOS background agents in Privacy and Security; v2.1.156 was a same-day hotfix for Opus 4.8 thinking blocks throwing API errors; v2.1.157 let plugins in `.claude/skills` load without a marketplace ([GitHub](https://github.com/anthropics/claude-code/releases)). Six releases, May 25–29. The drumbeat doesn't stop for a $965B valuation.

---

## Quiet on the Wire

Sunday, May 24, held all the way to the sweep — no model news, no API change, just a v2.1.150 infrastructure release with nothing user-facing. It was the last quiet day before the week detonated. Worth noting what *didn't* run: through every sweep this week, Anthropic's own docs endpoints returned HTTP 403 on direct fetch, so the API and Claude Code release notes went unverified at the primary source. The release log is built from GitHub and announcements, not the docs that were dark all week.

---

## Term of the Issue

# The Gate

**The Gate** *noun*

The deliberate hold a frontier lab places between a capability it has proven and the customers it sells to — opened not when the model is ready, but when the safeguards (and the market) are. A model behind the gate is a fact about capability; a model with a release date is a fact about strategy. The distance between them is where the safety argument lives.

**First observable** 2026-05-29, the week Anthropic's withheld Mythos model posted a 10,000-bug month, flickered into Claude Code, and got a "coming weeks" timeline in the same window as a $65B raise.

**Usage** *"They didn't ship the model this week. They shipped the date."*

---

## The Close

A model you can't buy found ten thousand bugs.
Then it got a price tag and a calendar.
The gate was always going to open.

---

## A. Models

*1 entry in window.*

#### 2026-05-28 - Claude Opus 4.8 ([Anthropic](https://www.anthropic.com/news/claude-opus-4-8))
`[MODEL]`

Anthropic's new flagship. Available on Claude API, Amazon Bedrock, Google Cloud Vertex AI, and Microsoft Foundry. Context window one million tokens (200k on Foundry). Max output 128k tokens. Benchmarks vs 4.7: SWE-bench Pro 69.2% (from 64.3%), USAMO 2026 96.7% (from 69.3%), GraphWalks long-context F1 68.1% (from 40.3%). First Claude model to score 0% on uncritically reporting flawed results. Overconfidence more than tenfold lower than 4.7. Pricing unchanged: $5/$25 per MTok. Fast mode runs at 2.5x speed for a smaller premium than on 4.7. Also reported by [The Decoder](https://the-decoder.com/anthropic-ships-claude-opus-4-8-as-a-modest-but-tangible-improvement-that-tops-gpt-5-5-in-most-benchmarks/) and [TechCrunch](https://techcrunch.com/2026/05/28/anthropic-releases-opus-4-8-with-new-dynamic-workflow-tool/).

**How to use:**
```python
client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    messages=[{"role": "user", "content": "..."}]
)
```

## B. API & Platform

*1 entry in window.*

#### 2026-05-28 - Mid-conversation system messages ([Anthropic](https://www.anthropic.com/news/claude-opus-4-8))
`[API]`

The Claude API now accepts `role: "system"` messages after a user turn, on Opus 4.8. Previously, system prompts were fixed at conversation start. Enables dynamic system-prompt updates mid-session without restarting the conversation. The `stop_details` field is now documented publicly.

**How to use:** Pass a message with `role: "system"` at any position in your messages array after the first user turn. Requires `claude-opus-4-8`.

## C. Claude Code

*6 entries in window.*

#### 2026-05-29 - Claude Code v2.1.157 ([CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md))
`[CODE]`

Plugins in `.claude/skills` directories now load automatically without a marketplace requirement. `claude plugin init <name>` scaffolds new plugins. `EnterWorktree` can switch between Claude-managed worktrees mid-session. WSL improvements: image paste, screenshot paste, Windows Explorer drag-and-drop. `tool_decision` telemetry events include `tool_parameters` when `OTEL_LOG_TOOL_DETAILS=1`. Removed the "bash commands will be sandboxed" startup banner. Fixes: worktree isolation, background session reliability, terminal rendering, IDE stop button not stopping background subagents, `/model` picker showing incorrect "Newer version available" hints.

**How to use:** `claude update` or reinstall.

#### 2026-05-29 - Claude Code v2.1.156 ([CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md))
`[CODE]`

Hotfix: Opus 4.8 thinking blocks were being modified in Claude Code, causing API errors. Fixed.

**How to use:** `claude update`. Superseded same day by v2.1.157.

#### 2026-05-28 - Claude Code v2.1.154 ([releases](https://github.com/anthropics/claude-code/releases))
`[CODE]`

Opus 4.8 defaults to high effort in Claude Code. Dynamic workflows (research preview): describe a large task and Claude spins up tens to hundreds of background subagents to execute it in parallel. Fast mode for Opus 4.8 trades a pricing premium for higher speed. Lean system prompt is now the default for all models except Haiku, Sonnet, and Opus 4.7 and earlier. `/simplify` runs cleanup-only review and applies fixes automatically. Shell background sessions: `! <command>` runs a shell command as a background session with attach/detach. Streaming tool execution always enabled, including on Bedrock, Vertex, and Foundry. Worktree isolation guard prevents subagents from bypassing restrictions.

**How to use:** `claude update`. Dynamic workflows: start a large task description and Claude proposes splitting it across agents when applicable.

#### 2026-05-28 (00:52 UTC, in window) - Claude Code v2.1.153 ([releases](https://github.com/anthropics/claude-code/releases))
`[CODE]`

Adds `skipLfs` to `github`/`git` plugin marketplace sources to skip Git LFS downloads. Status line commands receive `COLUMNS` and `LINES` env vars for terminal-aware sizing. `claude agents` autocomplete now suggests native slash commands and bundled skills. PR column shows `PR #N` or `N PRs`. `claude doctor` shows the last update attempt; one-time notice when an npm global install cannot auto-update. MCP server and connector auth notifications combined into one message. macOS: background agents appear as "Claude Code" in Privacy and Security with persistent permissions. `/model` saves selection as default (press `s` for current session only). Fixes: stateful MCP reconnect-looping, custom API gateway OAuth, subagent MCP servers ignoring `--strict-mcp-config`/`--bare`, Windows PowerShell installer false success, resume memory usage, stream-json exit on closed stdin, malformed `file://` links.

#### 2026-05-27 - Claude Code v2.1.152 ([releases](https://github.com/anthropics/claude-code/releases))
`[CODE]`

`/code-review --fix` applies review findings to the working tree; `/simplify` aliases to it. Skills and commands can declare `disallowed-tools` in frontmatter. `/reload-skills` added. `SessionStart` hooks can return `reloadSkills: true` or set the session title. New `MessageDisplay` hook event for transforming assistant message text before render. `pluginSuggestionMarketplaces` managed setting for allowlisting plugin sources. Auto mode no longer requires opt-in consent. Vim mode: `/` in NORMAL opens reverse history search. `/usage` breakdown includes large session files. Thinking summaries render as markdown, capped at 10 lines (Ctrl+O for full).

#### 2026-05-23 - Claude Code v2.1.150 ([releases](https://github.com/anthropics/claude-code/releases))
`[CODE]`

Infrastructure-only release. No user-facing changes. Last version standing through the quiet Sunday, May 24.

## D. Claude Apps

*1 entry in window.*

#### 2026-05-28 - Effort control on claude.ai ([Anthropic](https://www.anthropic.com/news/claude-opus-4-8))
`[APPS]`

Claude.ai users can now select the effort level Claude applies to a response. Ships alongside Opus 4.8, for which high effort is the default. The control surfaces the quality-versus-speed tradeoff per conversation.

## E. Agent SDKs

*2 entries in window.*

#### 2026-05-28 - anthropic-sdk-python v0.105.0, v0.105.1, v0.105.2 ([GitHub](https://github.com/anthropics/anthropic-sdk-python/releases))
`[SDK-PY]`

v0.105.0 adds `claude-opus-4-8` model support, mid-conversation system blocks, and `usage.output_tokens_details`. v0.105.1 switches PyPI releases to Trusted Publishing for supply-chain security. v0.105.2 is a minor patch. Three releases inside 24 hours.

**How to use:** `pip install --upgrade anthropic`

#### 2026-05-28 - @anthropic-ai/sdk v0.100.0 and v0.100.1 ([GitHub](https://github.com/anthropics/anthropic-sdk-typescript/releases))
`[SDK-TS]`

v0.100.0 adds `claude-opus-4-8`, mid-conversation system blocks, and `usage.output_tokens_details`. v0.100.1 fixes streaming to carry `encrypted_content` on beta compaction blocks. Earlier in the window: v0.98.1 (May 26, preserves directory prefix in `skills.versions.create`, swaps to Trusted Publishing) and v0.99.0 (the day before Opus 4.8, custom file size caps, `stop_details` carried through `message_delta`).

**How to use:** `npm install @anthropic-ai/sdk@latest`

## F. Research & Publications

*1 entry in window.*

#### 2026-05-25 - Project Glasswing: An initial update ([Anthropic](https://www.anthropic.com/research/glasswing-initial-update))
`[RESEARCH]`

Anthropic and approximately 50 partners found more than ten thousand high- or critical-severity vulnerabilities using Claude Mythos Preview in the program's first month. Cloudflare reported 2,000 bugs (400 high/critical) at a false-positive rate its team rated better than human testers; Mozilla fixed 271 vulnerabilities in Firefox 150, ten times the rate of an earlier Claude model. Anthropic's independent scan of 1,000-plus open-source projects identified an estimated 6,202 high/critical findings out of 23,019 total. The program is expanding to additional partners, including U.S. and allied government critical infrastructure. Mythos Preview remains gated; Anthropic stated Mythos-class models will ship for general release pending stronger safeguards. Also reported by [BleepingComputer](https://www.bleepingcomputer.com/news/artificial-intelligence/anthropics-restricted-claude-mythos-model-may-be-coming-to-claude-code/).

## G. News & Partnerships

*4 entries in window.*

#### 2026-05-29 - Anthropic raises $65B Series H at $965B valuation ([Anthropic](https://www.anthropic.com/news/series-h))
`[NEWS]`

Round led by Altimeter Capital, Dragoneer, Greenoaks, and Sequoia. Post-money valuation: $965 billion, surpassing OpenAI as the most valuable private AI company. Run-rate revenue: $47 billion, with growth attributed to Claude Code. Prior milestones: $9B ARR at end of 2025, $14B at Series G close (February), $30B in April — a three-times revenue jump in three months. Reported by [Fortune](https://fortune.com/2026/05/29/anthropic-raises-65-billion-at-record-965-billion-valuation-promises-mythos-ai-model-in-wide-release-in-coming-weeks-releases-claude-opus-4-8/) and [Simon Willison](https://simonwillison.net/2026/May/29/anthropic/).

#### 2026-05-29 - Mythos-level capabilities coming to all customers in weeks ([Insurance Journal](https://www.insurancejournal.com/news/national/2026/05/29/871703.htm))
`[NEWS]`

Anthropic stated it has made "swift progress" developing safety safeguards sufficient to release Mythos-class models broadly. Mythos has been restricted to Glasswing partners since April, on the basis that it could identify and exploit vulnerabilities in every major OS and browser when directed. The timeline is now "coming weeks." No specific date given. First reported by Bloomberg; also reported by [Fortune](https://fortune.com/2026/05/29/anthropic-raises-65-billion-at-record-965-billion-valuation-promises-mythos-ai-model-in-wide-release-in-coming-weeks-releases-claude-opus-4-8/).

#### 2026-05-28 - Claude Opus 4.8 generally available for GitHub Copilot ([github.blog](https://github.blog/changelog/2026-05-28-claude-opus-4-8-is-generally-available-for-github-copilot/))
`[NEWS]`

Opus 4.8 is now selectable for all GitHub Copilot users in Copilot Chat, inline suggestions, and agent mode, up from limited preview. Reported by GitHub.

#### 2026-05-27 - The First Broadcast ([Anthropic](https://www.anthropic.com/webinars/the-first-broadcast))
`[NEWS]`

Anthropic's inaugural partner webinar, held at 8:30 AM, covered May product news and CCAF certification updates and introduced the Anthropic Partner Academy, a new partner training experience, with the Claude Partner Certification going live alongside it. Global replay scheduled May 28 at 11:00 AM SGT.
