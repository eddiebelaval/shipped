---
title: "Vercel. The OAuth Pivot, The Non-Sensitive Vars, and the Attribution That Cracked"
issue: 02
section: investigation
status: research
created: 2026-04-22
updated: 2026-04-22
sources:
  - https://vercel.com/kb/bulletin/vercel-april-2026-security-incident
  - https://www.theregister.com/2026/04/21/vercel_ceo_points_to_aidriven/
  - https://blog.gitguardian.com/vercel-april-2026-incident-non-sensitive-environment-variables-need-investigation-too/
  - https://hackread.com/vercel-breach-context-ai-shinyhunters-not-involved/
  - https://www.bleepingcomputer.com/news/security/shinyhunters-denies-vercel-breach/
---

# Vercel. The OAuth Pivot, The Non-Sensitive Vars, and the Attribution That Cracked

OAuth is a promise with a half-life. Six months ago someone at Vercel clicked through a scope. Sunday, April 19, the bill came due. Stolen employee credentials, used through an AI tool called Context.ai that had been granted read access to Vercel's environment at install. One session, six months old, became the pivot.

Environment variables marked non-sensitive were exposed. Variables marked sensitive were encrypted at rest and are believed safe. Vercel's fix, per its bulletin, flips the default: new env vars default to `sensitive: on` going forward. Legacy non-sensitive vars stay in their original state until manually rotated.

Non-sensitive was a UI label, not a security property.

Per GitGuardian's analysis, non-sensitive env vars routinely contain API keys to analytics and logging, staging database strings, auth tokens for internal services, feature-flag provider secrets. All of it reachable by whoever held Context.ai's OAuth grant. The default was the problem. The flip is forward-looking only.

Then the attribution cracked. A BreachForums listing offered Vercel data for two million dollars, initially credited to ShinyHunters. On Monday and Tuesday of this week, the group told BleepingComputer and Hackread they are not involved. The listing remains live. The identity behind it is now unclear.

The AI twist sharpens it. The pivot mechanism was an AI-native OAuth grant. The modern builder stack is OAuth-all-the-way-down. Vercel is the first large-scale public demonstration of AI-tool-as-OAuth-pivot in the wild.

## Attribution caveats

- **ShinyHunters.** Not the attacker. Use "initially credited to ShinyHunters; the group has since denied involvement."
- **"AI-pwned."** The Register's phrasing. Fun, but editorial. Paraphrase as "pivoted via an AI-native OAuth grant."
- **Context.ai.** Named in The Register and Hackread. Attribute to those outlets; do not accuse Context.ai of wrongdoing, the pivot was via an OAuth grant, not a Context.ai vulnerability.
- **"No compromised npm packages published by Vercel."** Vercel's own statement. Attribute to the Vercel bulletin.
- **Mandiant et al.** Named in Vercel's bulletin. Attribution is safe.

## How this fits the issue

**Primary slot: Investigation section** (400 to 700 words prose, paired with Lovable).

**Pairing structure:** two substories, one frame. Lead with Lovable's four-position retreat (the shape of the collapse), then pivot to Vercel (the mechanism. OAuth pivot + non-sensitive definition). The Investigation closes on the shared thesis: **trust margins in AI-native platforms are collapsing under pressure, and the platforms' own public explanations are the evidence.**

Tie back to the Lead: Conway (from the Lead third-act) has the OAuth/webhook/GitHub-subs profile that is precisely what Vercel just demonstrated fails. That's the third-act beat of the Investigation, the unspoken comparison, earned only if the Lead already set it up.

## Open questions / TODOs before press

- [ ] **Vercel post-incident update.** Check the Vercel bulletin for updates between 2026-04-21 and 2026-04-23. Anything new?
- [ ] **Context.ai statement.** Has Context.ai made any public statement about the OAuth scope? If yes, attribute; if silence, that's itself part of the beat.
- [ ] **BreachForums listing status.** Still live? Still $2M? Still no attribution? Check before press.
- [ ] **Secondary attribution.** If ShinyHunters isn't behind it, is anyone else now credited? Avoid naming unless confirmed by ≥2 outlets.
- [ ] **Pro quote candidate.** Target: an infosec engineer at a platform-company (not Vercel, not Lovable). Someone who has shipped OAuth scopes and can speak to the "scope drift at install time" problem. Scan X, LinkedIn, Risky Business podcast guests.
- [ ] **Link back to Conway.** Draft the sentence that ties Vercel's OAuth pivot to Conway's OAuth/webhook surface. Precise, not preachy. One line, late in the Investigation.

## Voice notes for the distilled prose

- **Lead with the mechanism, not the attacker.** The OAuth pivot is the beat. The attribution confusion is a secondary beat that *rhymes* with Lovable's explanation-shifting.
- **Name the primitive.** OAuth grants with read access to environment variables is the primitive. Say it plainly.
- **The "non-sensitive" definition is the punchline.** Isolate it per STYLE.md Move B (punchline isolation). One sentence, on its own, late in the section.
- **Rhythm discipline.** The Investigation is the longest front-of-book section. Vary sentence length aggressively. Mix short beats with longer analytical sentences.
- **Avoid "wake-up call" framing.** That's cyber-PR. The Trust Week isn't a wake-up call. It's a weather pattern.
- **Forbidden phrases:** "sophisticated attack," "threat actor" (unless naming one that's actually confirmed, which here we can't), "raises questions about."
