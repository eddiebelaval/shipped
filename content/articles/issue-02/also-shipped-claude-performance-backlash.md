---
title: The Claude Code post-mortem — three bugs, named
issue: 2
section: also-shipped
status: research
created: 2026-04-22
updated: 2026-04-23
sources:
  - https://www.anthropic.com/engineering/april-23-postmortem
  - https://x.com/ClaudeDevs/status/2045206682830303358
  - https://fortune.com/2026/04/14/anthropic-claude-performance-decline-user-complaints-backlash-lack-of-transparency-accusations-compute-crunch/
  - https://code.claude.com/docs/en/ultrareview
  - https://platform.claude.com/usage/cache
  - https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
---

# The Claude Code post-mortem, three bugs named

Ninety minutes before this issue shipped, Anthropic published "An update on recent Claude Code quality reports" and broke the silence Fortune called out nine days earlier. Three bugs confirmed. All in Claude Code and the Agent SDK. None in the models. Usage limits reset for all subscribers. *"We never intentionally degrade our models and we were able to immediately confirm that our API and inference layer were unaffected."*

The bugs, in order. **March 4, default effort.** Claude Code's default reasoning effort moved from `high` to `medium` to reduce UI-latency complaints. The tradeoff cost measurable intelligence. Fixed April 7. **March 26, caching with thinking deletion.** A prompt-cache optimization using the `clear_thinking_20251015` header with `keep:1` was meant to clear reasoning after idle periods. Instead it cleared reasoning every turn mid-tool-use, forcing cache misses and draining usage limits faster. Fixed April 10 in v2.1.101. **April 16, system-prompt verbosity.** An instruction to hold responses to under 25 words between tool calls and under 100 in the final dropped coding quality by 3%. Caught after weeks of internal testing that showed no regression. Fixed April 20 in v2.1.116.

Cowork was swept in because it runs on the Agent SDK. The API was never touched.

The committed process changes read like the audit the community asked for: broader per-model evals on every system-prompt change, soak periods for intelligence-impacting changes, staff dogfooding the public build, @ClaudeDevs and GitHub threads for faster transparency. One quoted line matters. *"Opus 4.7 found the bug, while Opus 4.6 didn't."* The model that caught the regression is the one the company couldn't have used two weeks earlier.

The silence Fortune named is over. The r/ClaudeAI *meh* was early.

## Attribution caveats

- **"Claude performance is degrading."** Contested. User perception is documented; objective measurement requires access to Anthropic's internals or independent benchmarks. Attribute as "user complaints about perceived degradation," not "confirmed degradation."
- **"Compute crunch."** Fortune's framing, not Anthropic's explicit language. Hedge accordingly, "coverage has framed this as a compute crunch" rather than "Anthropic admits compute crunch."
- **"Contaminating variable."** Editorial interpretation, not reported fact. Own it as magazine-level analysis.

## How this fits the issue

**Slot:** Also Shipped, position TBD.

**Frame:** Meta-beat on how every Anthropic-ship in Issue 02 is being received. Runs before or after the Claude Design Lead distillation, it pre-frames (if before) or post-frames (if after) the r/ClaudeAI "meh" reception already quoted in the Lead.

**Placement tradeoff:** Could instead collapse into the Lead Story as one sentence of context (e.g., "the launch lands in a week where Claude's perceived quality is already contested"). Editorial call. If collapsed, drop this Also Shipped slot.

**Word budget:** 60 to 100 words (FORMULA.md Also Shipped item spec).

## Open questions / TODOs before press

- [ ] **Independent benchmark scan.** Any public benchmark (LMSYS, SEAL, Artificial Analysis, Helm) show a measurable Claude quality delta in April? If yes, that reframes this from "perception" to "documented."
- [ ] **Anthropic public statement.** Check the Anthropic blog, @claudedevs, and any transparency-report cadence pages between 2026-04-14 and 2026-04-24. Has Anthropic said anything official since the Fortune piece?
- [ ] **Collapse vs. standalone.** Final call Thursday: does this run as its own Also Shipped item, or fold into the Lead as a context sentence? Depends on front-of-book word budget.
- [ ] **r/ClaudeAI sentiment check.** Revisit the subreddit between Tue 2026-04-21 and Thu 2026-04-23 for any shift. If sentiment flipped, the framing of "contaminating context" is out of date.

## For builders

Vetted moves, imperative, action-layer:

- Audit your April Claude benchmark runs; flag them as contaminated-context before drawing conclusions.
- Verify your eval harness captures model version + system prompt + timestamp, so a perception shift is distinguishable from a real regression.
- Check Anthropic's status page weekly until the transparency cadence improves.
- Rotate to A/B testing between Claude versions if you ship user-facing features on model output.
- Test prompts that worked in March against April to build your own drift signal.
- Watch the r/ClaudeAI weekly sentiment thread as a leading indicator.
- Treat "perceived degradation" as a product signal for Anthropic, log your failure cases and share them.
- Read this next to the Lead Story on Claude Design; reception reads are contaminated by the same context.

## The stake

The call is: the community isn't asking for capability. What matters is methodology disclosure, performance-report cadence, deprecation notices, version-to-version evals. The tell is: Anthropic's silence on the Fortune framing. What this means: reception of every April ship is filtered through the prior weeks of frustration, and Anthropic hasn't given builders the instrument to separate the two. The posture is: ship the product, don't show the math. The precedent is: the builder community will tell you about drift whether you measure it or not. The decision was: stay quiet and let the product defend itself. The bet is: Claude Design lands hard enough that the backlash fades.

## How this fits the issue

This is the contaminating context running underneath every Anthropic ship in Issue 02. Read alongside the Lead Story (Claude Design reception), the r/ClaudeAI "resounding meh" is partly downstream of this week's frustration, not the product itself. Pairs with the Trust Week Investigation as the other half of a trust-margin beat: Vercel and Lovable lose trust through OAuth pivots and shifting public stories; Anthropic is burning trust through the absence of methodology disclosure. Mirrors the Trust Week shape, a platform handling builder confidence, an evolving (or non-existent) public explanation, and a gap between what users experience and what the platform documents. Third-act connection to Conway: if Conway ships with the shape the leak describes, every performance complaint against it inherits this baseline. The editorial beat: reception is contaminated, and the contamination is the story. Ties into the Term of the Issue, **Presence**, inversely: when a product stays present but silent on its own behavior, the trust margin collapses. The signal that matters: the community isn't asking for more capability, it's asking for transparency.

**Named evidence**, data points the prose can lean on:

- **2026-04-14**. Fortune's backlash piece. Three days before Claude Design shipped on 2026-04-17.
- **−7.28%**. Figma's same-day close on 2026-04-17. Cross-reference from the Lead Story; the backlash context contaminated *that* reception too.
- **0 Anthropic public statements** between 2026-04-14 and 2026-04-22. The silence is the data point.

## Voice notes for the distilled prose

House moves for the 60 to 100w Also Shipped compress:

- **Pattern 2 (the turn):** structure is community complaint → Anthropic silence → what this means for reading this week's launches. The third beat carries the operator value.
- **Move B (punchline isolation):** the "0 Anthropic statements" beat lands on its own line if word budget allows.
- **"X isn't Y, it's Z" formula:** NOT allowed. Issue budget spent in the Lead. Hard kill.
- **Attribution posture:** mark as contested throughout. "Perceived degradation," not "degradation." "Fortune's framing," not "confirmed."
- **Sass budget:** one dry beat on the "compute crunch" framing is allowed. The Fortune phrase is itself a press-cycle beat, name it, don't inherit it.
- **Tie-back:** one line to the Lead Story's reception read without re-quoting. Reader is reading linearly.

**Kill on sight**, forbidden phrases for this item:

- *"users are frustrated"*
- *"community outcry"*
- *"Anthropic faces criticism"*
- *"amid growing concerns"*
- *"raises questions about"*
- *"in a statement"*
- *"comes as"*
- *"watershed moment"*
- *"compute crunch"* (paraphrase Fortune, don't inherit)
- *"transparency debate"*
- *"users are frustrated with"* (rename: be specific)
- *"mounting criticism"*
