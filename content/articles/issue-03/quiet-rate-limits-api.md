---
title: "Rate Limits API + claude_code.at_mention telemetry"
issue: 03
section: quiet-wire
status: research
created: 2026-05-24
updated: 2026-05-24
sources:
  - https://platform.claude.com/docs/en/release-notes/overview
  - https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
---

# Rate Limits API + claude_code.at_mention

> Quiet on the Wire candidate. 50–80 words distilled. Two plumbing items shipped this window that signal where managed-agents pricing/governance is headed.

## Research notes (raw, not prose)

**Rate Limits API (2026-04-24).**
- New endpoint: programmatic query of rate limits for an organization and its workspaces.
- Single line in the changelog, not a launch post.
- Plumbing for enterprise governance: per-workspace governance is the next pricing surface.

**`claude_code.at_mention` OpenTelemetry event (Claude Code 2.1.122, 2026-04-28).**
- New telemetry primitive for `@`-mention resolution.
- Signals Anthropic is starting to instrument context retrieval inside Claude Code at the same granularity as tool calls.

## The editorial beat

Quiet on the Wire is where Shipped. reads the plumbing for what it tells you about the road. Two items, same signal: Anthropic is building the instrumentation and governance surfaces that managed-agents pricing will sit on. Not a launch. The shape of the road.

## Attribution caveats

- Both items are confirmed in official sources (platform release notes + Claude Code CHANGELOG). Safe to state.
- "Where managed-agents pricing is headed" is editorial inference, not Anthropic framing. Attribute as Shipped's read, not as Anthropic positioning.

## Operator-layer implications

- Workspace-level rate-limit queries are the precursor to workspace-level pricing tiers. Operators with multi-workspace deployments (cf. NEC's 30,000-seat deployment in lead-patron-economy.md) should expect this to become a pricing surface within 1–2 quarters.
- `claude_code.at_mention` telemetry means `@`-mention resolution becomes observable at the same level as tool calls. Operators running Claude Code in CI/CD or agentic workflows can use this for context-retrieval debugging now.

## Open questions / TODOs before press

- Has the Rate Limits API moved beyond query-only by ship date (2026-05-29)?
- Any signs of workspace-level pricing tiers in subsequent release notes (check 05-06 → 05-22 daily sweeps)?
- `claude_code.at_mention` event spec stable, or evolving in 2.1.123+ changelog?

## Voice notes for the distilled prose

- 50–80 words. Quiet on the Wire is the most compressed slot. One sentence per beat, plus the structural read.
- Per FORMULA.md, Quiet earns its slot when it tells operators what's coming, not what shipped.
- Anchor tone: dry, observational. This is the slot Raoul Duke would write — what no one else is calling a story.
