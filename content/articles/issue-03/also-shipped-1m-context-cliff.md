---
title: "The 1M context cliff (April 30)"
issue: 03
section: also-shipped
status: research
created: 2026-05-24
updated: 2026-05-24
placement_open: "Also-Shipped vs Open. The Open candidate in WIP uses this story (`The 1M context cliff` → cold open into the patronage week). If the Open absorbs it, this scaffold can collapse into a Release Log entry. Eddie's call at lock."
sources:
  - https://platform.claude.com/docs/en/release-notes/overview
---

# The 1M context cliff (April 30)

> Also Shipped item OR Open hook (placement_open above). The `context-1m-2025-08-07` beta header retires on Sonnet 4.5 and Sonnet 4. Pre-announced March 30, biting today.

## Research notes (raw, not prose)

- 2026-04-30: `context-1m-2025-08-07` beta header no longer honored on Sonnet 4.5 and Sonnet 4.
- Requests over 200k tokens on those models will be rejected.
- Migration path: Sonnet 4.6 or Opus 4.6, where 1M is GA at standard pricing without a header.
- Pre-announced 2026-03-30; biting on ship date of Issue 03's original window (04-30 cliff was the same day as the WIP lock).

## The editorial beat

The cliff itself is mundane (a beta header retiring on schedule). The editorial move (drafted in WIP 04-30) is using it as the cold open into a patron-economy week. *The patron giveth and the patron taketh away.* If that line earns its keep in The Open, this article collapses into a Release Log entry. If the Open lands differently in draft, this stays as Also Shipped with a 60–80 word distillation.

## Attribution caveats

- **"Pre-announced March 30"** — confirmed by platform release notes. Safe.
- **"Requests over 200k will be rejected"** — confirmed by the platform behavior. Safe. Do not characterize as a "breaking change" without context that the beta period was capped.
- The story is editorial framing, not the announcement itself. Do not over-attribute structural reads to Anthropic.

## Operator-layer implications

- Operators who pinned to Sonnet 4.5 or 4 for the 1M context window must migrate to 4.6 / Opus 4.6 by 04-30 or absorb 200k rejection at the gateway.
- Standard-pricing GA on 4.6 + Opus 4.6 means the 1M surcharge (if it existed for the beta) is no longer in the cost model. Procurement note worth surfacing in the operator layer.

## Open questions / TODOs before press

- Did Anthropic publish migration analytics or any 04-30+ telemetry on rejections?
- Are any platform.claude.com release notes between 04-30 and ship date (2026-05-29) worth pulling in?

## Voice notes for the distilled prose

- If this lands in The Open (80–150 words), the move is the cold open: name the mundane event, pivot to the structural week. *The patron giveth and the patron taketh away* is the candidate landing.
- If it lands in Also Shipped (60–100 words), it reads as a release-log-like operator note with a single structural beat: the cliff is on schedule, the model that earned the longer context is the patron version.
- Per STYLE.md: dry, confident. The 1M cliff is not a scandal; it is a calendar event that the editorial frame uses.
