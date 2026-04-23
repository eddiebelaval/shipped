---
title: "Issue 02 launch copy"
issue: 2
section: launch
status: research
created: 2026-04-22
updated: 2026-04-22
ship_target: "2026-04-24 09:00 ET"
grade_override: true
grade_override_reason: "Ship-day launch copy scaffold. Operational file, not an editorial article. Rubric v2 does not apply. Per doctrine (auto-ops, human-voice), prose is Eddie's; this file provides structural templates and voice notes only."
sources:
  - content/articles/issue-02/claude-design-reception.md
  - content/articles/issue-02/conway-leak-analysis.md
  - content/articles/issue-02/trust-week-vercel.md
  - content/articles/issue-02/trust-week-lovable.md
  - content/articles/issue-02/counter-signal-field-moved.md
  - content/articles/issue-02/quiet-claude-code-pro-test.md
  - content/STYLE.md
---

# Issue 02 launch copy

> Scaffolding for the social and email launch copy. Per auto-ops doctrine, prose is Eddie's. This file provides structural templates with slots, voice guardrails, and timing guidance.

## Ship moment

- **Publish:** Friday 2026-04-24, 09:00 ET.
- **Slug:** `presence`.
- **Term of the Issue:** Presence.
- **Issue title:** TBD (locked Thursday AM).

## Platform templates

### X / Twitter thread

Shape: 4 to 6 tweets. Opener, lead hook, second beat, third beat, CTA.

```
[1/n] HOOK
{ONE-LINE HOOK tied to the Term or the Lead's distribution tell. Examples:
  - The product that arrived before you called for it.
  - Anthropic is not building an API company.
  - The platforms under your app will fail in ways you didn't model.}
Shipped. Issue 02 is live.
{link}

[2/n] LEAD
{ONE-LINE SUMMARY of the Claude Design thesis. Do not paraphrase the headline.
Use one of the house moves from STYLE.md (punchline isolation or name-the-invisible).}

[3/n] B-STORY
{ONE-LINE on Conway. Frame as reported-only. "A codename in the leak."}

[4/n] INVESTIGATION
{ONE-LINE on the Trust Week. Name Lovable + Vercel. Name the shape: trust margins collapsing.}

[5/n] THE TURN
{ONE-LINE on the field context from Counter-signal. OpenAI shipped. Google shipped. Anthropic is not alone in the product turn.}

[6/n] CTA
Read Issue 02 at id8labs.app/shipped
Subscribe: {subscribe-link}
```

**Voice rules for the X thread:**
- No em dashes or en dashes.
- No emojis.
- No "🚀" or "thread" callouts.
- Period-heavy. Sentence length varies aggressively.
- First person reserved for the CTA tweet, if at all.
- Each tweet is one self-contained thought. No cliffhangers.

**Kill on sight** in X copy:
- *"Just dropped"*
- *"Thread incoming"*
- *"Here's why it matters"*
- *"Who wins?"*
- *"Hot take"*
- *"Unpopular opinion"*
- *"Buckle up"*

### LinkedIn post

Shape: 150 to 300 word standalone post. One hook, two to three body paragraphs, CTA.

```
HOOK (1 line):
{Line that could be the magazine title or a distilled Lead quote.}

BODY (two to three short paragraphs):
{Paragraph 1: What's in the issue. Name the four arc threads in order: Claude Design, Conway, Trust Week, the field moved.}
{Paragraph 2: Why it matters to builders specifically. Land one operator-layer takeaway.}
{Paragraph 3 (optional): Tie to Issue 01 or the Term of Issue. Rhyme with the Close.}

CTA (1 line + link):
Read Issue 02: {link}
```

**Voice rules for LinkedIn:**
- Do not use the word "proud" or "excited" or "thrilled."
- Do not tag Anthropic, OpenAI, or Google employees unless pre-cleared.
- Do not use #AI or #Innovation or any hashtag that signals LinkedIn-performative register.
- One hashtag maximum, and only if it is functional (e.g., `#Shipped`).

### Email newsletter (to existing subscribers)

Shape: subject, preheader, open, body, CTA.

```
Subject: {Option A: the Term} | {Option B: the Lead's tell} | {Option C: a quote from the issue}
Preheader: {One sentence that extends the subject without re-stating it.}

OPEN (2 to 3 sentences):
{Pulls from the magazine's Open. Do NOT copy-paste the Open verbatim; the email opener
is shorter and CTAs to the full issue.}

BODY (4 to 6 sentences):
{Summarizes the arc: product turn, trust margin, presence.}
{Names what the reader gets: hands-on SOPs, named sources, the Avasare quote, the field context.}

CTA:
Read Issue 02: {link}
Tell a builder: {share link}
```

**Voice rules for email:**
- Subject line under 60 characters.
- No leading emoji.
- No "Don't miss this" urgency framing.
- No unsubscribe bait.
- Plain-text-safe; no formatting tricks.

### WhatsApp group (internal circle)

Shape: one message, conversational register.

```
{Informal opener that rhymes with how you talk in the group. Reference the group's Issue 01 feedback if it shaped Issue 02.}

Issue 02 is live.
{One-line summary that is NOT the X hook.}

{Link}

Would love signal on: {one specific thing you want their read on, e.g., the Conway B-story placement, the Trust Week SOPs, the Presence term.}
```

**Voice rules for WhatsApp:**
- Informal is allowed.
- First person is allowed.
- One question mark maximum.
- Do not paste the same copy as LinkedIn or X.

### id8labs.app site pull-quote

One line, 6 to 12 words, from the issue. Appears on the home page under "Latest from Shipped."

Candidates to pick from, Thursday:
- "Anthropic is not building an API company."
- "The leak is the roadmap."
- "The platform under your app will fail in ways you didn't model."
- "Presence is what the field chose this month."

Pick one. Rotate on next issue.

## Timing

| When | What | Who |
|---|---|---|
| Thu 2026-04-23 PM | Title locked. Draft X, LinkedIn, email in `launch-copy.md`. | Eddie |
| Fri 2026-04-24 07:30 ET | Final prose pass on launch copy. Match the issue's final wording. | Eddie |
| Fri 2026-04-24 08:55 ET | `pnpm publish` renders the issue to staging. | Pipeline |
| Fri 2026-04-24 09:00 ET | Eddie commits and pushes. Issue is live. | Eddie |
| Fri 2026-04-24 09:05 ET | Post X thread. | Eddie |
| Fri 2026-04-24 09:10 ET | Post LinkedIn. | Eddie |
| Fri 2026-04-24 09:15 ET | Send email. | Eddie |
| Fri 2026-04-24 09:20 ET | Post WhatsApp group. | Eddie |
| Sat 2026-04-25 AM | Capture early reader signals. File into `post-ship.md`. | Eddie |

## Voice notes for all platforms

- **Every platform's copy is downstream of the magazine's voice**, not a translation of it. Do not dumb it down for LinkedIn or punch it up for X. The voice is one.
- **The Raoul Duke anchor carries.** One concrete detail per post. Same detail across platforms is acceptable; padding the detail out is not.
- **Sass budget:** one per post, not per sentence. Over-sassed launch copy reads cheap.
- **Forbidden across all platforms:** EPIC, thrilled, game-changing, ushers, unveils, the future of, next-gen, robust, best-in-class, industry-leading, synergies.
- **Attribution discipline:** any quote from the issue used in launch copy must still cite its source.

## Open questions / TODOs before ship

- [ ] Pick the pull-quote (Thursday AM).
- [ ] Draft and save the X thread (Thursday PM).
- [ ] Draft and save the LinkedIn post (Thursday PM).
- [ ] Draft and save the email (Thursday PM).
- [ ] Draft the WhatsApp message (Friday 8:30 AM).
- [ ] Confirm subscribe and share links are current.
- [ ] Verify OG card is live on the issue URL.
