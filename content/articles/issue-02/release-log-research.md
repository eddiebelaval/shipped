---
title: "Release Log research: 2026-04-17 to 2026-04-22"
issue: 2
section: release-log
status: research
created: 2026-04-22
updated: 2026-04-22
grade_override: true
grade_override_reason: "Back-of-book Release Log research. Factual compilation, not editorial. Rubric v2 does not apply: no counter-frame, no operator takeaway, no stake. These are compiled ship-notes, not articles."
sources:
  - https://www.anthropic.com/news/claude-design-anthropic-labs
  - https://www.anthropic.com/news/claude-opus-4-7
  - https://docs.anthropic.com/en/release-notes/overview.md
  - https://docs.claude.com/en/release-notes/overview.md
  - https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
  - https://releasebot.io/updates/anthropic
  - https://releasebot.io/updates/anthropic/claude-code
  - https://simonwillison.net/2026/Apr/22/claude-code-confusion/
  - https://www.theregister.com/2026/04/22/anthropic_removes_claude_code_pro/
  - https://www.rappler.com/technology/amazon-investment-anthropic-april-20-2026/
  - https://meyka.com/blog/amazon-invests-25b-in-anthropic-ai-on-april-21-2026-2104/
---

# Release Log research: 2026-04-17 to 2026-04-22

> Back-of-book, issue 02. Window opens Friday 2026-04-17 (Issue 01 ship day), closes Thursday 2026-04-23 PM (final scrape). Populated now, topped off tomorrow night.

## Format note

STYLE.md specifies the canonical Release Log entry format with an em dash separator:
`#### YYYY-MM-DD — Title (source-link)`.

Per the 2026-04-22 no-em-dashes rule, these entries use a colon separator instead:
`#### YYYY-MM-DD: Title (source-link)`.

That is a conflict with STYLE.md. Three options, Eddie picks at Thursday lock:

1. Keep the colon separator going forward and amend STYLE.md to match. Cleanest.
2. Keep em dashes only in Release Log entries as a format exception. Narrowest carve-out.
3. Use a different separator entirely (period, pipe). Breaks existing published-issue consistency.

Default I applied here: option 1. Easy to re-swap.

## Entries

### 2026-04-23 (Thursday, top-off pass)

#### 2026-04-23: Claude Code quality post-mortem published ([Anthropic Engineering](https://www.anthropic.com/engineering/april-23-postmortem), [@ClaudeDevs on X](https://x.com/ClaudeDevs/status/2045206682830303358))

Anthropic published "An update on recent Claude Code quality reports" addressing perceived degradation that Fortune covered on 2026-04-14. Three bugs confirmed, all in Claude Code and Agent SDK (which also impacted Cowork since it runs on the SDK); the API and inference layer were unaffected. Issue 1: default reasoning effort changed from `high` to `medium` on March 4 (fixed April 7). Issue 2: caching bug using `clear_thinking_20251015` with `keep:1` cleared reasoning every turn mid-tool-use instead of after idle periods, draining usage limits (fixed April 10 in v2.1.101). Issue 3: system-prompt verbosity instruction ("≤25 words between tool calls, ≤100 final") dropped coding quality 3% (fixed April 20 in v2.1.116). Usage limits reset for all subscribers as of April 23. Process changes: broader per-model evals on every system prompt change, soak periods for intelligence-impacting changes, internal dogfooding at parity with public build, tighter prompt-change review tooling. Anthropic quote: *"We never intentionally degrade our models and we were able to immediately confirm that our API and inference layer were unaffected."* Category: `[POLICY]`.

#### 2026-04-23: Claude Code 2.1.118 ([changelog](https://code.claude.com/docs/en/changelog))

Vim visual mode (`v`) and visual-line mode (`V`) added with selection, operators, and visual feedback. Fixed message duplication when scrolling in fullscreen mode. Category: `[RELEASE]`.

#### 2026-04-23: Claude ships 15 consumer connectors ([Anthropic](https://claude.com/blog/connectors-for-everyday-life/))

Anthropic added AllTrails, Audible, Booking.com, Instacart, Credit Karma, TurboTax, Resy, Spotify, StubHub, Taskrabbit, Thumbtack, TripAdvisor, Uber, Uber Eats, and Viator as native connectors inside Claude. Available on all plans, mobile in beta. Claude surfaces relevant ones mid-conversation based on context. Over 200 total connectors now live. Anthropic on record: *"ad-free and will stay that way."* Category: `[PRODUCT]`.

#### 2026-04-23: Memory for Claude Managed Agents enters public beta ([Anthropic](https://platform.claude.com/docs/en/release-notes/overview), [docs](https://platform.claude.com/docs/en/managed-agents/memory))

Persistent memory for Claude Managed Agents shipped in public beta under the `managed-agents-2026-04-01` header. Agents now maintain a durable context object that lives outside Claude's context window, stored in the session log. Lets agents carry knowledge and context across distinct sessions — the builder-side counterpart to the consumer connectors ship. Managed Agents itself launched public beta April 8; memory is the first research-preview capability to graduate. Category: `[PRODUCT]`.

#### 2026-04-23: UK and US regulators briefed banks on Mythos cyber risk ([FT](https://www.ft.com/content/56d65763-69fe-4756-baf4-c8192b7aadaf), [PYMNTS](https://www.pymnts.com/news/2026/financial-officials-sound-alarm-about-anthropics-banking-risk), [Bloomberg](https://www.bloomberg.com/news/videos/2026-04-17/financial-watchdog-to-share-insight-on-anthropic-ai-video))

At the IMF and World Bank spring meetings in Washington, regulators and central bankers focused on Anthropic's Claude Mythos Preview and the possibility that advanced LLMs could expose weak spots in banks' cyber defenses. Bank of England Governor Andrew Bailey (chair of the Financial Stability Board) called the issue "a very serious challenge for all of us." US Treasury secretary Scott Bessent summoned leaders of the largest US banks earlier in the week. Anthropic has said Mythos found thousands of high-severity vulnerabilities in major operating systems and browsers, with access limited to ~40 Project Glasswing partners (Amazon, Apple, JPMorgan Chase, etc.). Category: `[POLICY]`.

### 2026-04-22 (Wednesday)

#### 2026-04-22: Anthropic expands TPU deal with Google and Broadcom, 3.5 GW from 2027 ([Anthropic](https://www.anthropic.com/news/google-broadcom-partnership-compute), [Motley Fool](https://www.fool.com/investing/2026/04/22/anthropic-just-announced-huge-news-for-alphabet-an/), [Seeking Alpha](https://seekingalpha.com/news/4572848-anthropic-targets-30b-revenue-signs-tpu-deal-with-google-and-broadcom))

Anthropic announced expanded access to next-generation TPUs via the Broadcom + Alphabet joint venture. Up to 3.5 GW of capacity from 2027. Accelerating demand has pushed run-rate revenue over $30B (up from $9B at end of 2025). Second major compute commitment this week after the Amazon $25B / $100B AWS deal. Category: `[DEAL]`. Cross-references Amazon entry below.

#### 2026-04-22: Claude Code 2.1.117 ([changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md))

Faster startup, stronger plugin management, better session resume and model persistence, improved OpenTelemetry. Experimental Advisor tool updates, safer auth handling, more reliable context and subagent behavior. macOS, Linux, Windows, and API fixes. Category: `[RELEASE]`.

#### 2026-04-22: Claude Code $20 Pro plan test reverted ([Avasare on X](https://x.com/amolavasare/status/2046724659039932830), [Simon Willison](https://simonwillison.net/2026/Apr/22/claude-code-confusion/))

Late afternoon 2026-04-21, Anthropic removed Claude Code from the $20 Pro plan on `claude.com/pricing` and in docs. By early 2026-04-22 Anthropic reversed: Pro checkmark and docs restored. Amol Avasare, head of growth, said on X: "running a small test on ~2% of new prosumer signups. Existing Pro and Max subscribers aren't affected." Category: `[POLICY]`. Cross-linked to Quiet on the Wire.

### 2026-04-21 (Tuesday)

#### 2026-04-21: Claude Code 2.1.116 ([changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md))

Faster `/resume` on large sessions. Quicker MCP startup. Smarter slash-command search. Terminal behavior improvements. Category: `[RELEASE]`.

#### 2026-04-21: Amazon invests $25B in Anthropic, Anthropic commits $100B on AWS ([Rappler](https://www.rappler.com/technology/amazon-investment-anthropic-april-20-2026/), [Meyka](https://meyka.com/blog/amazon-invests-25b-in-anthropic-ai-on-april-21-2026-2104/))

Amazon invests up to $25B in Anthropic: $5B immediate, $20B committed on commercial milestones. Anthropic commits $100B+ on AWS over 10 years. Target: 1 GW via Trainium2 and Trainium3 by end of 2026, 5 GW total goal. Ties back to Project Glasswing and Mythos context. Category: `[NEWS]`. Per Eddie's Tuesday AM call: release-log-only, not lead material.

#### 2026-04-21: Trump signals openness to Anthropic + Pentagon deal ([Detroit News](https://www.detroitnews.com/story/business/2026/04/21/trump-says-anthropic-is-shaping-up-open-to-deal-with-pentagon/89716263007/))

Trump told reporters Anthropic is "shaping up" and indicated willingness to explore a Pentagon deal. Read alongside the White House chief-of-staff + Dario Amodei meeting (Apr 17). National-security surface for Mythos continues to widen. Category: `[POLICY]`.

### 2026-04-20 (Monday)

#### 2026-04-20: Claude Cowork live artifacts — dashboards and trackers that auto-refresh ([@claudeai on X](https://x.com/claudeai/status/2046328619249684989))

Cowork can now build live artifacts: dashboards and trackers connected to apps and files. Open any of them later and they refresh with current data. Shifts artifacts from one-shot snapshots to persistent surfaces with data bindings — closer to a Notion or Retool block than the previous Claude artifact format. Category: `[LAUNCH]`. Pairs with the Cowork GA + Enterprise feature push the same day.

#### 2026-04-20: Claude Cowork goes GA on macOS and Windows desktop, expanded analytics, OpenTelemetry support, RBAC for Enterprise ([Medium / Data Mind](https://medium.com/ai-analytics-diaries/claude-cowork-just-went-ga-how-agentic-ai-agents-are-automating-data-science-workflows-in-2026-433ed86b0727), [Phemex](https://phemex.com/news/article/claude-launches-live-artifacts-for-autorefreshing-dashboards-in-cowork-74713))

Cowork moves from public beta to GA on Claude Desktop (macOS + Windows). Bundled with: expanded usage analytics, OpenTelemetry export support, role-based access controls for Enterprise plans, custom charts, and inline visualizations in responses. Category: `[LAUNCH]`. Cowork was previously preview-status as recently as Issue 01's coverage; this is the formal exit.

#### 2026-04-20: Claude Haiku 3 retired on Claude Developer Platform ([release notes](https://docs.claude.com/en/release-notes/overview))

Claude Haiku 3 retired. Users urged to upgrade to Claude Haiku 4.5. Category: `[MODEL]`. Deprecation cadence continues from the Apr 14 Opus 4 and Sonnet 4 deprecations.

### 2026-04-19 (Sunday)

#### 2026-04-19: Claude Code 2.1.114 ([changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md))

Fixed crash in permission dialog when agent teammates request tool access. Category: `[FIX]`.

#### 2026-04-17: White House chief-of-staff meets Dario Amodei over Mythos ([CNN](https://www.cnn.com/2026/04/17/business/anthropic-white-house-meeting-dario-amodei))

Susie Wiles (White House Chief of Staff) met with Anthropic CEO Dario Amodei to discuss Mythos, framed as "productive and constructive" and exploring collaboration plus "balancing innovation and safety." Category: `[POLICY]`.

### 2026-04-17 (Friday, Issue 01 ship day)

#### 2026-04-17: Claude Design launch ([announcement](https://www.anthropic.com/news/claude-design-anthropic-labs))

Anthropic Labs shipped Claude Design, powered by Claude Opus 4.7. Research preview for Pro, Max, Team, Enterprise. Turns prompts, codebases, PRDs into designs, prototypes, slides, one-pagers, full design systems. Exports to PDF, URL, PPTX, Canva. Category: `[LAUNCH]`. Already the Lead Story for Issue 02. Release Log reference only.

#### 2026-04-17: Claude Code 2.1.112 ([changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md))

Hotfix: resolved "claude-opus-4-7 is temporarily unavailable" in auto mode. Category: `[FIX]`. **Note for Issue 02:** v2.1.111 itself was dated 2026-04-16 and was already carried in Issue 01's Release Log; 2.1.112 is the first post-ship-window version.

#### 2026-04-17: Claude Code `/usage` command (@ClaudeDevs first post) ([ClaudeDevs on X](https://x.com/ClaudeDevs/status/2045206682830303358))

@ClaudeDevs (the newly launched official Anthropic dev channel) announced the `/usage` command in Claude Code: breakdown of parallel sessions, subagents, cache misses, long context, plus tips to optimize each. Meta: @ClaudeDevs itself was announced Apr 10-11 by Thariq (@trq212) and @claudeai as the new front door for Claude Code + platform updates. Category: `[RELEASE]`.

## Category groupings (per STYLE.md)

STYLE.md specifies seven groupings for Release Log entries. Tagged above with the category at the end of each entry:

- `[LAUNCH]`: new products, new brand-level announcements.
- `[MODEL]`: new models, model updates, deprecations.
- `[RELEASE]`: versioned software releases (Claude Code, CLI, SDK).
- `[FIX]`: hotfix releases, bug fixes, stability patches.
- `[POLICY]`: pricing, access, plan changes, terms updates.
- `[NEWS]`: company news, funding, partnerships, leadership.
- `[ECOSYSTEM]`: third-party integrations, partner tools, gateways.

This week had: 1 LAUNCH, 1 MODEL, 4 RELEASE, 2 FIX, 1 POLICY, 1 NEWS, 0 ECOSYSTEM. Total: 10 entries for the Apr 17 to 22 window.

The OpenClaw sanctioning story fits `[ECOSYSTEM]` if it surfaces a dated event. Currently covered as an Also Shipped item, not a Release Log entry.

## Still pending, top off Thursday 2026-04-23 PM

These are the items I will search for in the Thursday-night scrape to close the window:

- Any Claude Code release Thursday 2026-04-23 (new version bumps ship almost daily this month).
- Any docs.anthropic.com release notes update posted Wednesday 2026-04-22 PM or Thursday 2026-04-23.
- Any Anthropic status page incidents in the window.
- Any @claudedevs, @anthropicai, or @alexalbert__ announcements during Thursday.
- Confirmation of the Claude Code $20 Pro test status Thursday: continuing, expanded, or ended.
- Any primary quote or statement from Anthropic corp comms on the Amazon deal, the Claude Code test, or Conway.
- Any model deprecations or new SKUs on the Claude Developer Platform.
- Any `/agents` API or `/skills` API surfacing between Wed PM and Thu PM.

## Attribution caveats

- **Releasebot.io as source**. A third-party aggregator, not a primary source. Each entry above has been cross-referenced against either the Anthropic announcement URL, the Claude Code CHANGELOG, or `docs.anthropic.com/en/release-notes/overview.md`. Releasebot pulled version numbers and dates; primary URLs confirm the facts. Do not cite Releasebot in the magazine.
- **Claude Code 2.1.112 vs 2.1.111 sequence on 2026-04-17**. Releasebot lists both on the same date. Treat 2.1.112 as the hotfix for a regression introduced by 2.1.111. Confirm the exact sequence from the CHANGELOG before Thursday lock.
- **Amazon $25B numbers**. Two primary-adjacent outlets (Rappler, Meyka) cite the $5B-now, $20B-milestone structure. Not yet cross-checked against an Amazon press release or Anthropic blog post. Do so before Thursday lock.
- **Avasare "2%" quote**. Cited verbatim from X status `2046724659039932830`, also quoted by Simon Willison. Safe.
- **Claude Haiku 3 retirement date**. Releasebot dates it 2026-04-20. Double-check against `docs.claude.com/en/release-notes/overview` before press.
- **No verified Anthropic X announcement** for the Amazon investment. All coverage is third-party. If an `@anthropicai` or CEO quote surfaces before Thursday lock, replace the third-party cite with the primary.

## Open questions / TODOs before press

- [ ] Cross-check every `[RELEASE]` and `[FIX]` entry against the actual CHANGELOG.md in the `anthropics/claude-code` GitHub repo. Releasebot is a mirror, not authoritative.
- [ ] Pull the `docs.anthropic.com/en/release-notes/overview.md` file for canonical Developer Platform entries.
- [ ] Verify the Claude Haiku 3 retirement announcement URL.
- [ ] Find the primary Amazon press release or Anthropic blog post for the $25B deal. If neither exists, the Release Log entry attributes to "per Rappler and Meyka."
- [ ] Archive the Avasare X post: X URLs decay, pin via Internet Archive before Thursday.
- [ ] Run the scrape again Thursday night to catch 2026-04-22 PM and 2026-04-23 items.

## Voice notes for the distilled entries

Release Log items are short factual summaries, not editorial prose. But STYLE.md still governs language:

- **Use ship verbs**, not launch verbs. "Anthropic shipped Claude Design" not "Anthropic launched."
- **Version numbers are sufficient characterization**. No need to editorialize what each release means in the Release Log. That is the front-of-book's job.
- **Category tags stay in the source article**. Production Release Log strips them to keep entries clean.
- **Per-entry word cap: 150 words**. These drafts already respect it. Most are 25 to 50.
- **No em or en dashes in entry titles or body**. Colon separator for date-title pairing until Eddie picks a final house format.

**Kill on sight** in Release Log entries:

- *"unveils"* or *"unveiled"*
- *"launches"* (use "shipped")
- *"rolls out"*
- *"announces plans to"*
- *"game-changing"*
- *"industry-leading"*
- *"officially confirmed"* (unless Anthropic actually confirmed)
- *"highly anticipated"*
- *"much-awaited"*
- *"cutting-edge"*
