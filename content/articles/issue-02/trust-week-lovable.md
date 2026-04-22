---
title: "Lovable — The BOLA That Wasn't Intentional, Then Was, Then Got Half-Fixed"
issue: 02
section: investigation
status: research
created: 2026-04-22
updated: 2026-04-22
sources:
  - https://www.theregister.com/2026/04/20/lovable_denies_data_leak/
  - https://www.techloy.com/is-your-code-safe-lovable-ai-fixes-vulnerability-that-leaked-database-credentials/
  - https://www.computing.co.uk/news/2026/security/lovable-flaw-exposed-source-code-credentials-and-ai-chats
---

# Lovable — The BOLA That Wasn't Intentional, Then Was, Then Got Half-Fixed

## What happened

Lovable — the AI-native app builder — ran a **broken object-level authorization (BOLA)** flaw that exposed source code, database credentials, and AI chat histories from public projects. The vulnerability, reported through HackerOne, was initially closed as "intended behavior." Over three weeks in April 2026, Lovable's public-facing story shifted four times.

The timeline (per The Register, 2026-04-20):

1. **First position.** Intentional behavior. Public projects are public; data exposure is by design. Report closed.
2. **Second position.** HackerOne's fault — the triagers closed the reports as duplicates because they thought it was intended.
3. **Third position.** Admission that a February 2026 permissions-unification accidentally re-enabled access to public-project chats that were supposed to be private.
4. **Fourth position.** Partial fix shipped. New projects patched. **Every pre-existing (pre-November 2025) project remains exposed.**

Techloy's headline says Lovable "fixes" the vulnerability. Independent coverage (Computing.co.uk, The Register) says the fix is **new-projects-only**. That gap — announced fix vs. legacy-project exposure — is itself worth stating cleanly.

## What was exposed

Per Computing.co.uk's reporting:

- **Source code** of public Lovable projects
- **Database credentials** embedded in project configurations
- **AI chat histories** associated with the projects — including user prompts and model responses

"Public project" in Lovable is a looser concept than most readers assume. A project can be public (discoverable by anyone) while its chats and embedded secrets were — per Lovable's own documentation — supposed to be private.

## The editorial beat

This is not a vulnerability story. It's a **trust-margin-collapse story**, and the shape is the news.

The pattern that repeats across modern AI-native platforms: the platform holds more trust than it deserves, something goes wrong, and the public-facing story evolves faster than the fix does. Lovable's four-position retreat — intentional → HackerOne's fault → February permissions bug → partial fix — is a trust-margin collapse under public pressure. The fix is not the story. The four positions are the story.

Read this next to the Vercel piece. Different companies. Different attack surfaces. **Same narrative shape.** Both stories have:

- A platform that handles builder trust (deploys, secrets, code, chats)
- An evolving public explanation over ~3 weeks
- A gap between what was claimed and what was true
- A fix that is narrower than the announcement implies

That gap, measured in builder trust, is what the Trust Week investigation is actually reporting on.

## The operator-layer implications

This is where the magazine's action-layer posture kicks in. Vetted SOPs readers can run today:

- **If you use Lovable:** audit every project created before November 2025. If it's flagged public, assume the chat histories and embedded credentials are exposed. Rotate any credential that appeared in a Lovable chat. Revoke and re-issue.
- **If you use any "public" mode on any AI-native platform:** the word "public" is doing load-bearing work without a contract behind it. Read the platform's own definition of what "public" covers. Re-read it today. If it's ambiguous, assume maximum exposure.
- **If you use HackerOne for disclosure:** this incident is a reminder that triage closes happen. A closed report is not a resolved vulnerability. Re-open on resistance; escalate if needed.
- **If you embed secrets in any AI-native builder:** stop. Use env-var indirection. Rotate quarterly.

## Attribution caveats

- **"Lovable fixed it"** — true only for new projects created after the patch. Soften to "Lovable shipped a partial fix (new projects patched; pre-existing projects remain exposed per independent coverage)."
- **"Intentional behavior"** — that was Lovable's first public position, since retracted. Quote with the timeline attached; do not quote in isolation.
- **"February permissions-unification"** — per Lovable's own admission via The Register. Attribute to Lovable's statement, not to independent reporting.
- **The Register's phrasing** — The Register has house voice ("intentional behavior defense"). Paraphrase for tone; cite for facts.

## How this fits the issue

**Primary slot: Investigation section** (400–700 words prose).

**Pairing:** shares the Investigation section with Vercel. Two substories, same narrative shape, one unifying editorial frame: *"trust margins collapsing under pressure in AI-native platforms."*

The Investigation should close on Anthropic — specifically, the Conway context from the Lead Story third-act. The setup: *"Anthropic is about to ship a product (Conway) whose trust surface is 10× what Vercel and Lovable just failed to protect."* That's the tie-back the magazine earned.

## Open questions / TODOs before press

- [ ] **Pro quote.** A working infosec engineer at an AI-native company is the right voice here. Scan: X, LinkedIn, recent InfoQ/Register comment threads. Target: someone who has shipped to both Lovable and Vercel and can speak to the OAuth scope question.
- [ ] **Legacy project exposure — confirm scope.** "Pre-existing projects remain exposed" per Computing.co.uk and The Register. Confirm this is still true as of 2026-04-23 (Thursday lock) — Lovable may have shipped more fixes in the interim.
- [ ] **HackerOne side of the story.** Has HackerOne issued a statement, or is Lovable's "HackerOne's fault" position the only account? If HackerOne has spoken, cite.
- [ ] **Any statement from Lovable between Apr 20–23.** Watch for updates; the public-facing story has shifted four times already.
- [ ] **Link back to Conway.** Draft the one-sentence bridge that ties this Investigation back to the Lead's third-act. Should be precise, not preachy.

## Voice notes for the distilled prose

- **Lead with the shape, not the details.** "A vulnerability is not news. A vulnerability with four public positions in three weeks is news."
- **The timeline is a rhythm device.** Four bulleted positions, each landing in order, builds the narrative momentum. Don't collapse into a paragraph.
- **Avoid the cyber-blog register.** No "BOLA exposed" as a headline verb. The magazine is a builder-facing editorial magazine, not a security bulletin.
- **The Close of the Investigation earns a callback to the Lead.** Conway's trust surface is the unspoken comparand. Make the comparison once, late, and land it.
- **Forbidden phrases:** "comes on the heels of," "raises concerns about," "highlights the need for better security." All three are cyber-PR filler. Kill on sight.
