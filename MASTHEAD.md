# MASTHEAD.md — Shipped.

> The publication modeled as a chain of primitives. Who sits at each desk, what each pass takes in and hands off, and the eval that decides whether the pass is done or runs again. The **Editor-in-Chief** owns the chain and runs the loop so the humans don't have to sit in it.
>
> This is the org chart and the assembly line in one file. STYLE governs voice, FORMULA governs the weekly's shape, DAILY governs the daily's depth, RUBRIC governs readiness — **MASTHEAD governs who does what, in what order, and what gate each pass has to clear.**

**Read order:** [VISION.md](./VISION.md) → [EDITORIAL.md](./EDITORIAL.md) → **MASTHEAD.md** (this file) → [DAILY.md](./content/DAILY.md) / [FORMULA.md](./content/FORMULA.md) → [STYLE.md](./content/STYLE.md) → [RUBRIC.md](./content/RUBRIC.md).

Authored 2026-06-10 by Eddie Belaval (with Claude). Built to take Eddie out of the per-pass loop after the June 10 daily put Fable 5's general release — a landmark — out as two paragraphs.

---

## The principle: a magazine is a chain of passes, not one act of writing

Amateur publishing is one person writing a thing and posting it. Professional publishing is a **relay** — a story moves desk to desk, and each desk does exactly one job and hands off. The reporter doesn't design. The designer doesn't fact-check. The fact-checker doesn't rewrite for voice. Each pass is narrow, which is what makes each pass good.

Shipped. is built as that relay. Each desk is a **primitive**: a single transformation with a typed input, a typed output, and an eval gate that says "done" or "again." The chain is the primitives in sequence. The **Editor-in-Chief** is the agent that walks a story down the chain, reads each eval, and decides whether to advance, loop back, or escalate. That loop — pass, grade, loop-back-until-it-clears — is the whole game. It is why the output is good without a human re-reading every sentence.

```
   SWEEP → BUDGET → DIG → LINE → CHECK → ART → CRIT → PRESS
  reporter  editor  writer copy  fact   design  EIC   publisher
            └─────────── the loop the EIC runs ──────────┘      └ human gate ┘
```

---

## The desks (the primitives)

Each desk is one primitive. **In** is what it must receive. **Out** is what it must produce. **Eval** is the gate the EIC checks before advancing. **Loop-back** is where it goes if the eval fails.

### 1 · SWEEP — the News Desk (Reporter)

- **Job:** Find everything Anthropic shipped in the window. Every claim gets a primary source URL.
- **In:** a date or date-range window.
- **Out:** `signal facts` — a structured list of releases (product area, version, date, what changed, source URLs, one independent-coverage link where it exists).
- **Eval:** every fact has ≥1 primary source; relative dates converted to absolute; no claim without a URL. (RUBRIC dim 1: Sourcing.)
- **Loop-back:** missing source → re-sweep that item. No source after two tries → the item is dropped to a release-log line, never invented.
- **Tooling:** GitHub releases (claude-code, SDKs), anthropic.com/news, docs release-notes, web search for independent coverage.

### 2 · BUDGET — the Editor (Assignment)

> In print, "the budget" is the meeting where the editor decides which stories run and how big. Not money. The issue's running order.

- **Job:** Decide the lead, the running order, and — critically — **what gets dug**. Size each story to *reader value*, not release volume (DAILY law). A landmark in two lines fails here.
- **In:** `signal facts`.
- **Out:** `issue plan` — lead pick + rationale, running order, per-item dig depth (full Dig / partial / release-log line), word targets, any Term-of-Issue candidate.
- **Eval:** the biggest-value story is the lead and is marked full-Dig; nothing landmark is sized as a stub; word targets meet the DAILY/FORMULA floors.
- **Loop-back:** if the plan under-sizes the lead, the EIC rejects the budget and reassigns depth before any prose is written. **This is the pass that would have caught the Fable 5 failure.**

### 3 · DIG — the Staff Writer (Draft)

- **Job:** Write the front-of-book. Run every assigned item through The Dig's six levers — mechanism, blast radius, pattern, the read, the contrast, the move (see DAILY.md).
- **In:** `issue plan` + `signal facts`.
- **Out:** `draft prose` — lead, dug items, the read, quiet-on-the-wire, in the issue's markdown.
- **Eval:** each dug item shows mechanism + stakes + a builder move; word floors met; depth came from the levers, not padding.
- **Loop-back:** thin item → back to DIG with the specific lever that's missing. Padded item → back to DIG to cut.

### 4 · LINE — the Copy Desk (Line Editor)

- **Job:** Voice and sentence-craft. Enforce STYLE.md: kill forbidden phrases, hold the "X isn't Y, it's Z" budget (1/daily, 1/weekly), vary sentence length, keep the teeth, cut the fat. Does **not** add facts.
- **In:** `draft prose`.
- **Out:** `edited prose`.
- **Eval:** zero forbidden phrases; cliché budget respected; reads in Eddie's register, not press-release register.
- **Loop-back:** voice miss → back to LINE. If LINE can't fix it without changing meaning → back to DIG.

### 5 · CHECK — the Fact Desk (Fact-Checker)

- **Job:** Prove the issue doesn't lie. Run the five verifier gates: URL liveness, number attestation, quote attestation, date attestation, voice gate. **No override, no skip.**
- **In:** `edited prose`.
- **Out:** `verified prose` + a pass/fail report.
- **Eval:** all five gates green.
- **Loop-back:** any gate red → back to the desk that introduced the error (a wrong number → DIG; a dead link → SWEEP; a voice flag → LINE). Re-run CHECK after the fix. The verifier is the moat; it is the one pass that cannot be waved through.

### 6 · ART — the Art Desk (Designer)

- **Job:** Render to the house template (warm paper, Fraunces display, Archivo body, the orange). Typographic QA: no widows in heads, code blocks intact, OG image present, mobile clean.
- **In:** `verified prose`.
- **Out:** `staged HTML` in the deploy target.
- **Eval:** renders without error; loads and hydrates (not just HTTP 200 — see the Production Outage rule); design matches the template.
- **Loop-back:** render break or layout flaw → back to ART.

### 7 · CRIT — the Editor-in-Chief (Review)

- **Job:** The judgment pass. Score the staged issue against RUBRIC.md and the golden-sample set. Ask the only question that matters: *is this a read worth the reader's time?* Ship, loop, or kill.
- **In:** `staged HTML` + the full pass history.
- **Out:** `verdict` — a rubric score (x/28), a one-line call, and either GO or a specific loop-back assignment.
- **Eval (the bar):** **≥ B+ (22/28)** to advance for a daily; **≥ A− (24/28)** for a weekly. Below bar → loop back to the weakest desk with a named fix.
- **Loop-back:** CRIT is allowed to send a story all the way back to BUDGET if the problem is structural (wrong lead, wrong sizing), not cosmetic.

### 8 · PRESS — the Publisher (Ship)

- **Job:** Publish. `git commit && git push` from the deploy repo; verify the live URL hydrates.
- **In:** a CRIT verdict of GO.
- **Out:** the live issue + archive/tracker updates + launch copy.
- **The gate:** **human, by default.** See "Removing the humans from the loop" below for the only thing that crosses this line and the conditions under which it can move.

---

## The Editor-in-Chief: who runs the loop

The EIC is one agent (`.claude/agents/editor-in-chief.md`) that fuses the managing editor (runs the schedule, moves work between desks) and the editor-in-chief (owns the bar, makes the final call). It does not write, line-edit, or design itself — it **dispatches** each pass to the right desk, reads the eval, and decides advance / loop-back / escalate. It carries the whole issue in its head so no desk has to.

The EIC's contract:

1. **Run the chain in order.** SWEEP → BUDGET → DIG → LINE → CHECK → ART → CRIT.
2. **Gate every pass.** Do not advance a pass whose eval is red. Loop back to the responsible desk with a *specific* note, not "do better."
3. **Bound the loop.** Max **2** loop-backs per desk per issue. On the third failure, stop and escalate to the human with the exact blocker — never spin.
4. **Own the bar.** CRIT is the EIC's own pass. It does not lower the bar to ship on time; it ships late or escalates. (EDITORIAL: "Better to ship at 9:15 with clean copy than 9:00 with a lie.")
5. **Hand up, not around.** The human gate at PRESS is the only thing the EIC cannot self-clear by default.

What this removes from the human: the per-pass back-and-forth — rewriting a thin lead, catching a forbidden phrase, re-running the verifier, nudging the render. The EIC does all of that and presents **one ship-ready issue plus its rubric score.** The human reads the final and pushes (or notes a change, which the EIC routes back into the loop).

---

## The loop is the product

"Make sure the loop is giving good results" means: **every pass has an eval, and no pass advances on a red eval.** The quality isn't in any single desk; it's in the relay refusing to pass bad work forward. Three rules keep the loop honest:

- **Evals are concrete, not vibes.** "Each dug item names a builder move" is checkable. "Make it punchier" is not. Every loop-back cites the specific eval that failed.
- **Loop-backs are bounded.** Two tries per desk, then escalate. A loop that never terminates is a worse failure than a thin issue.
- **The bar never moves to meet the clock.** CRIT scores against RUBRIC regardless of the ship time. Late-and-true beats on-time-and-thin.

When the loop is working, the human sees an A-grade issue and a green scorecard, not a draft to fix.

---

## Removing the humans from the loop — the ramp

Eddie's standing rule across the portfolio (and Shipped's founding doc): **the human at `git push` is the final gate, always.** Public, irreversible, money-and-reputation-adjacent — Eddie's lane. So the default, today, is:

> **The EIC runs SWEEP → CRIT autonomously and stages a ship-ready issue. The human reads the final and ships.**

That already removes the human from the *loop* (the seven passes) while keeping the human on the *button* (PRESS).

The button can move — but it earns its way, on the Succession pattern used everywhere else in the portfolio:

| Stage | What the EIC may do at PRESS | Gate to advance |
|---|---|---|
| **0 — Today** | Stage + notify. Human ships. | — |
| **1 — Assisted** | Stage + notify + open the staged page for one-tap ship. | EIC CRIT ≥ B+ on the last 5 dailies, zero post-ship corrections. |
| **2 — Delayed-auto (daily only)** | Auto-ship the **daily** after a 30-min veto window; human can kill it. Weekly stays human. | Stage-1 clean for 4 weeks + zero reader-reported factual errors. |
| **3 — Autonomous daily** | Auto-ship the daily; weekly always human. | Stage-2 clean for 8 weeks. |

The weekly never leaves the human gate under this ramp — it's the flagship, higher-stakes, and the place the brand lives. The ramp only ever frees the daily, and only after the eval record proves the loop holds. **Default is Stage 0.** Moving a stage is Eddie's call, logged here with the date and the evidence.

---

## Mapping to the existing pipeline

This doesn't replace the code pipeline (`pipeline/src/`) or the phase doc (EDITORIAL.md) — it names the agents that operate them and adds the editing/design passes as first-class primitives.

| MASTHEAD desk | EDITORIAL phase | Code / command |
|---|---|---|
| SWEEP | Signal | `/shipped-signal`, scrapers |
| BUDGET | WIP / Thursday lock | `/shipped-wip` + EIC |
| DIG | Draft | `/shipped-draft` + DAILY.md |
| LINE | (was folded into Draft) | EIC line pass + STYLE.md |
| CHECK | Verify | `pnpm verify` / `/verify-shipped` |
| ART | Stage | `pnpm publish` render / `/publish-shipped` |
| CRIT | (was Eddie's read) | EIC + RUBRIC grader |
| PRESS | Ship | human `git push` |

---

## Changelog

| Date | Change | Reason |
|---|---|---|
| 2026-06-10 | Initial masthead. Eight desks as primitives, the EIC as loop-runner, the Succession ramp for PRESS. | Eddie: model Shipped as a real publication's pass-sequence and put an EIC in charge so the humans leave the loop. Triggered by the Fable 5 GA daily shipping as two paragraphs. |
