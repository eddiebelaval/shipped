---
title: Vercel flips env-var default to sensitive:on
issue: 2
section: also-shipped
status: research
created: 2026-04-22
updated: 2026-04-22
sources:
  - https://vercel.com/kb/bulletin/vercel-april-2026-security-incident
  - https://blog.gitguardian.com/vercel-april-2026-incident-non-sensitive-environment-variables-need-investigation-too/
  - https://www.theregister.com/2026/04/21/vercel_ceo_points_to_aidriven/
  - https://www.itnews.com.au/news/cloud-deployment-firm-vercel-breached-advises-secrets-rotation-625197
  - https://www.coindesk.com/tech/2026/04/20/hack-at-vercel-sends-crypto-developers-scrambling-to-lock-down-api-keys
---

# Vercel flips env-var default to sensitive:on

Vercel's April bulletin confirms the default for new environment variables flips to `sensitive: on` going forward. Previously, non-sensitive was the default; users had to opt in. Per GitGuardian's reading of the bulletin, pre-existing env vars stay in their original state until manually rotated. The fix is a default change, not a migration. Legacy non-sensitive vars need manual rotation and re-flagging. Watch Netlify, Railway, Render for parallel moves. The default was the problem.

## Attribution caveats

- **"Default is changing to sensitive:on."** Vercel's own bulletin. Safe to attribute.
- **"Pre-existing env vars remain in their original state."** Per GitGuardian reading of the bulletin. Not a direct Vercel quote, attribute as "per GitGuardian's analysis."
- **"Other platforms are following."** Speculation unless a second platform announces before Thursday. Hedge: "industry-watchers expect similar moves."

## How this fits the issue

**Slot:** Also Shipped, position TBD in running order (Thursday lock).

**Frame:** Policy-signal beat. Companion/echo to the Trust Week Investigation. The Investigation is the breach; this is the response. Keeps the Investigation focused on narrative and offloads the operational update here.

**Word budget:** 60 to 100 words (FORMULA.md Also Shipped item spec).

**Pairing:** Runs adjacent to OpenClaw Anthropic-return (also Also Shipped, also a policy signal). Two policy shifts in one slot cluster, that's a texture beat, not an accident.

## Open questions / TODOs before press

- [ ] **Confirm bulletin language.** Pull the exact wording Vercel used for the default change. If the bulletin updates between Wed and Fri, re-pull.
- [ ] **Cross-platform scan.** Netlify, Railway, Render, Fly, did any of them ship a parallel policy change in the same week? If yes, the beat broadens from Vercel-specific to industry.
- [ ] **Does Conway's webhook surface get the same treatment?** Irrelevant if Conway isn't in the issue; relevant if it's Lead third-act.
- [ ] **Verify no-prose invariant held.** Source article is research-status only. Prose happens in `issue-02-{slug}.md`.

## For builders

Vetted moves, imperative, action-layer:

- Audit every env var on your Vercel projects today; flag each one's sensitive state explicitly.
- Rotate any non-sensitive env var that predates the default flip; the flip is forward-looking only.
- Re-flag credentials that should have been sensitive from the start; do not rely on the UI label.
- Check your OAuth grants on every AI-native tool connected to Vercel; revoke what's unused.
- Verify your secrets-rotation cadence; monthly minimum for anything touching production.
- Stop treating "non-sensitive" as a security property; treat it as a label.
- Watch Netlify, Railway, Render, and Fly for parallel policy announcements this quarter.
- Monitor your `package.json` for supply-chain drift; daily `npm audit` until the investigation settles.
- Read this next to the Trust Week Investigation; the policy change is a response, not a resolution.
- Treat every OAuth-connected tool as a pivot surface until proven otherwise.

**Named evidence**, data points for the 60 to 100w compress:

- **$2M**. BreachForums Vercel listing price, still live per The Register.
- **0**. Anthropic public statements on Claude Code auth model between the Vercel disclosure and Issue 02 ship.
- **2026-04-19**, weekend incident disclosure date.
- **100%** of pre-flip non-sensitive env vars remain in their original state until manually rotated.
- **5+** vendors engaged per the bulletin: Mandiant, GitHub, Microsoft, npm, Socket.

## The stake

The call is: "non-sensitive" was a UI label, not a security property. What this means: every pre-flip env var on Vercel needs manual rotation; the default change does not migrate legacy configuration. The tell is: Vercel shipped the default change *before* the incident investigation closed. The posture is: flip the default first, explain later. The precedent is: platform defaults are trust contracts whether the platform calls them that or not. The decision was: treat non-sensitive as the exception going forward, not the rule. The bet is: developers rotate fast enough that the legacy exposure window stays small. That bet is generous.

## Voice notes for the distilled prose

House moves for the 60 to 100w Also Shipped compress:

- **Pattern 2 (the turn):** structure is what changed → what the default used to be → what this means for legacy vars. Three beats. Third one bites.
- **Move B (punchline isolation):** "The default was the problem." Own line. Own paragraph.
- **"X isn't Y, it's Z" formula:** NOT allowed. Issue budget spent in the Lead. Hard kill.
- **Specificity in nouns.** Name the flag (`sensitive`). Name the default state (`on`). Name the affected surface (env vars). Don't abstract.
- **Raoul Duke anchor:** single-detail characterization. The `sensitive: on` syntax IS the detail. Preserve the literal.
- **Sass budget:** zero. This is a straight policy-signal item; sass would undercut the operator value.
- **Tie-back:** one oblique line to the Investigation without re-stating it. Reader is already there.
- **Hedge language where warranted.** "Vercel confirmed" = safe. "Other platforms are expected to follow" = speculation, either cite a second platform by name or drop the line.

**Kill on sight**, forbidden phrases for this item:

- *"security-first"*
- *"best practice"*
- *"raises the bar"*
- *"unveiled"*
- *"strengthens posture"*
- *"takes a stand on"*
- *"in the wake of"*
- *"proactive measures"*
- *"hardens the platform"*
- *"industry-leading"*
- *"security-minded"*
- *"robust defense"*
