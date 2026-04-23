---
title: "Pro-interview DM: Trust Week source"
issue: 2
section: ops
status: research
created: 2026-04-22
updated: 2026-04-22
grade_override: true
grade_override_reason: "Operational outreach template. Not editorial. OVR."
---

# Pro-interview DM: Trust Week source

> Draft outreach for a named infosec engineer quote in the Trust Week Investigation (Issue 02). One quote on "OAuth scope drift at install time" specifically around the Context.ai / Vercel pivot. Transforms the Investigation from synthesis into reporting.

## Candidate hunt (do this first, Wednesday night)

Scan these surfaces for 5 candidates. Criteria: platform-company infosec or builder-company infosec; has shipped OAuth scope design; public-facing (either on X or a substack or a podcast guest appearance). Not from Vercel, Lovable, Anthropic, or Context.ai (conflict of interest).

- **X search terms:** "OAuth scope" infosec, "Context.ai" breach, "non-sensitive env vars", GitGuardian (see if their author is quotable, or who they quote).
- **LinkedIn:** search "infosec engineer YC", "application security" + "AI", "DevSecOps" + recent activity this week on the Vercel story.
- **Risky Business podcast:** recent guests, the technical ones.
- **Hacker News comment thread:** news.ycombinator.com on the Vercel article. Top comments often include the engineer you want.
- **GitGuardian's research team:** their piece on non-sensitive env vars is the best-sourced single outside take on the incident. Author contact via their blog.

List 5 on a notecard with handle, one-line bio, why they fit. Pick 2 to DM. Send both, 15 min apart.

## The DM (paste-ready)

**Subject or opener (X / LinkedIn):**

> Quick ask from a magazine I edit.

**Body, short version (3 sentences, ≤ 90 words, no em dashes):**

> Hey {name}, I edit Shipped. ({URL}), a weekly on what Anthropic is releasing. For Issue 02 (Friday) we're running a Trust Week investigation on the Lovable BOLA and the Vercel Context.ai pivot, and the beat that matters is OAuth scope drift at install time. Would you give us 10 minutes on Wednesday evening or Thursday morning for a single quote we can cite by name and title? Happy to share the draft before ship and run the quote past you for wording. Not for publication without your approval.

**If they want a longer preview before the call:**

> Short context: we framed the Vercel incident as "a platform-level OAuth grant that was scoped beyond what most admins remember approving." We'd love your version of that sentence (or the sentence that comes before it, in your experience shipping scopes). The frame we're resisting is "sophisticated attack"; the frame we're leaning into is "scope decay is normal, and normal is the risk." Your take on whether we've got that right is exactly what we need.

## Ship-ready quote container

If they agree, write the rendered quote in this shape (for easy paste into the canonical's Investigation):

```
> *"{quote text, roughly 30 to 80 words}"*
> — {First Last}, {Role}, {Company}
```

Example target shape (hypothetical):

```
> *"OAuth scopes at install time are a commitment most admins don't revisit. When the tool you authorized three months ago gets compromised, the scope you granted is the one an attacker runs."*
> — Name Here, Staff Security Engineer, Company Here
```

## If both declines

Fallback voices (no DM required, quotable by attribution):

- **GitGuardian blog (2026-04-20):** their non-sensitive-env-vars piece is itself a quotable source. Attribute by publication + date.
- **The Register (2026-04-21):** Vercel CEO commentary. Already in the canonical.
- **Mandiant post-incident writeup (pending):** if they publish before Friday, that becomes the primary.

## Post-call discipline

- Send them the draft Investigation paragraph that includes their quote, 24h before ship.
- If they ask for a tweak, take the tweak.
- If they pull the quote after seeing it in context, reply with gratitude and pull it immediately. Use a GitGuardian cite instead. Do not argue.
- After ship: send the live URL plus one line of thanks. Add to a source roster for future issues.

## Kill on sight

Phrases that poison the DM:

- *"synergies"*, *"thought leader"*, *"would love to pick your brain"*
- *"quick chat"* (give a specific time)
- *"sophisticated attacker"* (the frame we're resisting)
- *"wake-up call"*
- *"our audience"* (pretentious for a weekly)

## Open TODOs

- [ ] Pick 5 candidates Wednesday night.
- [ ] DM two of them before Thursday 10 AM.
- [ ] If neither replies by Thursday 3 PM, fall back to GitGuardian cite.
- [ ] If one agrees, schedule Thursday evening or Friday 7 AM.
