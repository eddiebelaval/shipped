---
title: "OpenClaw Re-Enables Anthropic Support"
issue: 02
section: also-shipped
status: research
created: 2026-04-21
updated: 2026-04-21
sources:
  - https://docs.openclaw.ai/providers/anthropic
---

# OpenClaw Re-Enables Anthropic Support

## What OpenClaw is

OpenClaw is a multi-provider LLM gateway and CLI. One configuration, many providers underneath — Anthropic, OpenAI, Qwen, MiniMax, Z.AI, Bedrock. Target user: developers and teams who want to route between providers or hedge against vendor lock-in without writing the glue themselves.

## What shipped

Full Anthropic integration, including:

- **Authentication:** Anthropic API key auth AND Claude CLI backend reuse (legacy token auth is supported again).
- **Models:** All Claude families — opus-4-6, sonnet-4-6, and newer releases as they land.
- **Prompt caching:** Both `cacheRetention: short` (5-min) and `long` (1-hour) options.
- **Extended thinking:** Adaptive thinking modes for Claude 4.6.
- **Fast mode:** Exposed via `service_tier` parameters.
- **1M context window:** Available in beta via `context1m: true`.
- **Bedrock Claude:** Integration supported for teams on AWS.

## The signal that matters

The feature matrix is table stakes. The editorial beat is a line in the docs:

> "Anthropic staff reportedly told us OpenClaw-style Claude CLI usage is allowed again... the team treats this usage pattern as sanctioned for this integration unless Anthropic publishes a new policy."

Translation: there was a period where CLI reuse through third-party gateways was in a grey zone. It is now sanctioned — at least by verbal confirmation OpenClaw is willing to publish. Anthropic has not, as far as this research can find, made a formal public statement.

That's the beat. **Policy, not product.** Anthropic expanding the set of sanctioned ways to consume Claude, right as the Trust Week stories (Lovable, Vercel) show what happens when platforms mishandle the flexibility builders already have.

## How this fits the issue

Also Shipped candidate. 60-100 words in the magazine.

The through-line for the section: Anthropic is expanding the *sanctioned surface area* for how Claude gets used (Claude Design for designers, Conway in the pipeline for always-on agents, OpenClaw for multi-provider gateways). Every one of those expansions is a new trust surface. Trust Week is the counterweight: here's what happens when a platform mishandles the trust it already has.

## Attribution caveats

- The "Anthropic sanctioned this" claim comes **from OpenClaw only** — an interested party. Attribute carefully in the magazine as "per OpenClaw's docs" rather than "Anthropic sanctioned."
- The docs do not state a date for when Anthropic support was re-enabled. Either dig for a version history or attribute it as "recently" / "as of late April 2026."

## Open questions / TODOs before press

- [ ] Is there a date-stamped changelog entry on OpenClaw's site or GitHub?
- [ ] Is there any public Anthropic statement (blog, X post, docs change) corroborating the CLI-reuse sanction? If yes, cite; if no, the attribution caveat holds.
- [ ] Worth a quick search — did another gateway (OpenRouter, LiteLLM) get the same policy update this week? If so, the beat is broader than OpenClaw specifically.

## Voice notes for the Also Shipped compress

- Lead with the policy signal, not the feature matrix. Feature lists are what press releases do.
- Keep the "trust surface" thread implicit — the Trust Week investigation will do the heavy lift.
- 80 words or under. This is a supporting beat, not a feature.
