---
title: "Lovable. The BOLA That Wasn't Intentional, Then Was, Then Got Half-Fixed"
issue: 02
section: investigation
status: research
created: 2026-04-22
updated: 2026-04-22
sources:
  - https://vercel.com/kb/bulletin/vercel-april-2026-security-incident
  - https://lovable.dev/
  - https://hackerone.com/
  - https://www.theregister.com/2026/04/20/lovable_denies_data_leak/
  - https://www.techloy.com/is-your-code-safe-lovable-ai-fixes-vulnerability-that-leaked-database-credentials/
  - https://www.computing.co.uk/news/2026/security/lovable-flaw-exposed-source-code-credentials-and-ai-chats
  - https://www.superblocks.com/blog/lovable-vulnerabilities
  - https://cybersecuritynews.com/lovable-ai-app-builder-customer-data/
  - https://sifted.eu/articles/lovable-denies-data-breach
---

# Lovable. The BOLA That Wasn't Intentional, Then Was, Then Got Half-Fixed

A vulnerability disclosed is a vulnerability. A vulnerability filed as intended behavior is a posture. Lovable, the AI-native app builder, chose the second for forty-eight days. Source code, database credentials, and AI chat histories from public projects leaked through a broken object-level authorization flaw. HackerOne report sat. Closed as intended behavior.

Over three weeks in April, Lovable's public story shifted four times.

First position. Intentional. Public projects are public. Report closed. Second position. HackerOne's fault, the triagers closed the reports as duplicates. Third position. Admission: a February 2026 permissions-unification accidentally re-enabled access to public-project chats that were supposed to be private. Fourth position. Partial fix shipped. New projects patched.

New projects only.

Every pre-existing Lovable project created before November 2025 remains exposed. Source code, database credentials, AI chat transcripts, still reachable. Techloy's headline says Lovable "fixes" it. The Register and Computing.co.uk say the fix is new-projects-only. That gap is the story.

Public project in Lovable is a looser concept than most readers assume. A project could be discoverable while its chats and embedded secrets were, per Lovable's own documentation, supposed to be private. A UI label doing load-bearing work without a contract behind it.

This is not a vulnerability post. It's a trust-margin collapse. The pattern across AI-native platforms repeats. The platform holds more trust than it deserves, something goes wrong, and the public story evolves faster than the fix. The four positions are the story.

## The stake

The call is: Lovable's fix is narrower than the announcement implies. What this means: every pre-2025-11-01 public project is still carrying exposed chat histories and credentials today. The tell is: the four-position retreat, intentional, HackerOne's fault, admitted bug, partial fix. That is what a trust margin looks like when it collapses in public. The posture is: Lovable is defending the platform, not defending the builders who trusted it. The precedent is: AI-native builder platforms that treat "public" as a UI label will lose customer trust before they lose customers. The decision was made in the scope of the fix, new projects only. What Lovable chose is revealing. The bet is: most legacy projects have already rotated, so the blast radius is smaller than it reads. That bet is generous to Lovable.

## Attribution caveats

- **"Lovable fixed it"**, true only for new projects created after the patch. Soften to "Lovable shipped a partial fix (new projects patched; pre-existing projects remain exposed per independent coverage)."
- **"Intentional behavior"**, that was Lovable's first public position, since retracted. Quote with the timeline attached; do not quote in isolation.
- **"February permissions-unification"**, per Lovable's own admission via The Register. Attribute to Lovable's statement, not to independent reporting.
- **The Register's phrasing**. The Register has house voice ("intentional behavior defense"). Paraphrase for tone; cite for facts.

## Named evidence

- **48 days** between HackerOne report and partial fix.
- **100%** of pre-November 2025 Lovable projects remain exposed after the patch.
- **4 distinct public positions** in three weeks: intentional, HackerOne's fault, admitted bug, partial fix.
- **Bailey-style framing quote for builders:** *"Public was a UI label, not a security property."* — House voice; source the observation to independent coverage (The Register / Computing.co.uk), never to Lovable.

## For builders

Vetted moves, imperative, action-layer:

- Audit every Lovable project created before 2026-11-01; assume source, credentials, and AI chat transcripts are reachable until Lovable publishes a scope-complete fix.
- Rotate any database credentials, API keys, or tokens that ever lived in a pre-November 2025 Lovable project, including staging and abandoned sandboxes.
- Re-issue OAuth tokens embedded in Lovable AI chat transcripts; the chat surface is a credential-leak surface, not just a prompt surface.
- Check whether your Lovable projects are labelled "public" in the UI; treat "public" as a weak claim until Lovable publishes an explicit contract for public versus private data within a project.
- Monitor Lovable's support channel for a scope-complete fix announcement; absence is itself the signal.
- Treat this as a Presence-era trust decay, the same pattern that underwrites this issue's Term of the Issue; ambient trust margins collapse before the first incident report lands.

## How this fits the issue

**Primary slot: Investigation section** (400 to 700 words prose).

**Pairing:** shares the Investigation section with Vercel. Two substories, same narrative shape, one unifying editorial frame: *"trust margins collapsing under pressure in AI-native platforms."*

The Investigation should close on Anthropic, specifically, the Conway context from the Lead Story third-act. The setup: *"Anthropic is about to ship a product (Conway) whose trust surface is 10× what Vercel and Lovable just failed to protect."* That's the tie-back the magazine earned.

## Open questions / TODOs before press

- [ ] **Pro quote.** A working infosec engineer at an AI-native company is the right voice here. Scan: X, LinkedIn, recent InfoQ/Register comment threads. Target: someone who has shipped to both Lovable and Vercel and can speak to the OAuth scope question.
- [ ] **Legacy project exposure, confirm scope.** "Pre-existing projects remain exposed" per Computing.co.uk and The Register. Confirm this is still true as of 2026-04-23 (Thursday lock). Lovable may have shipped more fixes in the interim.
- [ ] **HackerOne side of the story.** Has HackerOne issued a statement, or is Lovable's "HackerOne's fault" position the only account? If HackerOne has spoken, cite.
- [ ] **Any statement from Lovable between Apr 20 to 23.** Watch for updates; the public-facing story has shifted four times already.
- [ ] **Link back to Conway.** Draft the one-sentence bridge that ties this Investigation back to the Lead's third-act. Should be precise, not preachy.

## Voice notes for the distilled prose

House moves for the Investigation pair (shared with Vercel, 400 to 700w combined):

- **Pattern 1 (in medias res):** open on the fourth-position pivot, "the fix that only covers new projects." One sentence, then rewind.
- **Move B (punchline isolation):** "New projects only." Own line, own paragraph. Preserve.
- **Pattern 2 (the turn):** structure is BOLA → four-position retreat → partial fix → the comparand (Conway's trust surface). The turn is in beat 3→4.
- **"X isn't Y, it's Z" formula:** NOT allowed here. Issue budget spent in the Lead. Hard kill.
- **Raoul Duke anchor:** single-detail characterization. "Intended behavior" IS the detail. Lovable's own language doing the work. Quote once, don't paraphrase away.
- **Sass budget:** one dry beat on the four-position retreat is earned. Two would be overreach. One.
- **Timeline as rhythm device.** Four bulleted positions, each landing in order, builds narrative momentum. Don't collapse into a paragraph.
- **Avoid cyber-blog register.** No "BOLA exposed" as headline verb. The magazine is builder-facing editorial, not a security bulletin.
- **The Close of the Investigation earns a callback to the Lead.** Conway's trust surface is the unspoken comparand. Make the comparison once, late, and land it.

**Kill on sight**, forbidden phrases for this piece:

- *"comes on the heels of"*
- *"raises concerns about"*
- *"highlights the need for better security"*
- *"security posture concerns"*
- *"threat actors"* (no confirmed actor here)
- *"in a statement"* (Lovable made four)
- *"backpedaled"* (use "retreated")
- *"wake-up call"*
- *"sophisticated attack"* (it wasn't)
- *"cybersecurity community"*
- *"mounting pressure"*
- *"amid growing concerns"*
