---
title: Presence as a product category
issue: 2
section: companion
status: research
created: 2026-04-22
updated: 2026-04-22
placement_decision: Companion to the Lead. Eddie 2026-04-22 PM.
sources:
  - https://www.anthropic.com/news/claude-design-anthropic-labs
  - https://vercel.com/kb/bulletin/vercel-april-2026-security-incident
  - https://www.testingcatalog.com/anthropics-works-on-its-always-on-agent-with-new-ui-extensions/
  - https://techcrunch.com/2026/04/17/anthropic-launches-claude-design-a-new-product-for-creating-quick-visuals/
  - https://thehackernews.com/2026/04/claude-code-tleaked-via-npm-packaging.html
  - https://www.theregister.com/2026/04/21/vercel_ceo_points_to_aidriven/
  - content/articles/issue-02/conway-leak-analysis.md
  - content/articles/issue-02/trust-week-vercel.md
  - content/articles/issue-02/trust-week-lovable.md
  - content/articles/issue-02/claude-design-reception.md
  - knowledge/shipped/style/voice-corpus/presence-not-tools.md
---

# Three labs, one direction

Three products shipped or staged in two weeks name the same primitive.

Claude Design reads your codebase, design files, and PRD before you prompt. The input is ambient context. The output arrives closer to a collaborator's draft than a tool's response. That's the absorb half.

Conway, in the leaked source, watches. Webhook triggers. GitHub subscriptions. Browser control. Persistent container. Push notifications on condition, not request. That's the act-on-conditions half.

The Trust Week is the failure mode. Always-on plus ambient-context plus OAuth-everywhere is the attack surface that just got demonstrated in the wild. Lovable. Vercel. Two platforms, one shape. Presence inherits whatever trust contract sits beneath it, and if that contract isn't sealed, the product on top is only as safe as the scope a tired admin clicked through six months ago.

The field named this week by shipping variants of the same thing. Anthropic with Claude Design and Conway. OpenAI with Codex workspace agents. Google with Gemini auto-browse in Chrome. Three labs, one direction.

The question stops being *what does the model do* and becomes *what does the product occupy*. That's a category. Call it by its name.

## Cross-references within the issue

| Section | What to carry forward | How it lands |
|---|---|---|
| Lead Story (Claude Design) | "context-absorption is the move, not prompt-compression" | Sets up the first half of the presence argument |
| Lead third-act or B-story (Conway) | "persistent + webhook-triggered + browser-driving" | Names the second half |
| Investigation (Trust Week) | "OAuth-everywhere is the trust surface presence inherits" | Supplies the failure mode |
| Close | Presence is the name for what connects these three | Lands the Term of Issue |

## Named evidence for the argument

Data points the prose can lean on to turn "concept" into "category":

- **−7.28%**. Figma's close on 2026-04-17, same-day Claude Design launch. Presence absorbed attention, not just market share.
- **$100B+**. Anthropic's AWS commitment over 10 years (Amazon-Anthropic deal, 2026-04-20). The compute layer for always-on.
- **44 hidden feature flags**. Claude Code source leak, 2026-03-31. The backstage of presence as product.
- **$2M**. BreachForums Vercel listing. The price on a breach is the price on the trust surface presence inherits.
- **48 days**. Lovable's BOLA unfixed before partial patch. The gap between "present platform" and "watched platform."
- **0 Anthropic statements** on Conway between the leak and ship date. Silence is part of the pattern.

## The stake

The call is: presence is the emerging product category of this quarter, and Anthropic is ahead on it. What this means: builder attention moves from "what does the model do" to "what does the product occupy." The tell is: distribution choices. Canva for Claude Design, GitHub subscriptions for Conway, OAuth-everywhere for the trust failures. The posture is: presence is a land grab, not a feature. The decision was made when Anthropic chose Opus 4.7 as the engine for Claude Design rather than holding it for an API release, the bet is product, not platform. The precedent is: every always-on product category (email, calendar, chat) consolidated into 2-3 winners within 36 months of framing. The question becomes: which surface is Anthropic claiming, and which does it leave to OpenAI / Google? The bet is: the surface is knowledge-worker ambient assistance, and OpenAI's Operator is playing catch-up.

## For builders

Vetted moves, imperative, action-layer for the presence category:

- Audit the ambient-agent surfaces your product exposes today: webhooks, long-polling endpoints, background workers, push notifications.
- Rotate your OAuth scope review quarterly, presence products inherit trust from everything they connect to.
- Check whether your app has a "present" mode (watching user state) vs. a "summoned" mode (responding to calls). Name them.
- Verify the agent-facing API of your product matches its user-facing UI; presence only works if the agent can do what the UI can.
- Watch Anthropic's product cadence for what presence means next, the leak is the roadmap.
- Read the Trust Week alongside this article; presence's failure mode is already documented.
- Test what happens to your product when the user is *present but inactive* for 24 hours. That's where presence products win or lose.
- Treat "always-on" as a contract with the user; document your pause / revoke / forget UX.
- Monitor your app's telemetry for ambient-use patterns that already exist; they're the edge of your presence surface.

## The Close move it enables

Structural prompts for the Close (do not write the prose here, the Close is editorial):

- Open the Close on a concrete scene. Pattern 1 (STYLE.md).
- Land the Term of Issue in one sentence, not a paragraph.
- End on the inversion: the products that are present are the ones that inherit the trust surface. This is a pivot beat, not a summary.
- Budget: 3 beats. Last one lands.

## Attribution caveats

- **"Presence is a product category."** Editorial argument. Own it as magazine analysis. Do not claim Anthropic uses this framing.
- **"Conway is presence."** Reported-only; Anthropic has not confirmed Conway as a product. Use "reported codename" language consistent with the Conway source article.
- **"Always-on" vs. "presence."** Always-on is the technical description; presence is the editorial frame. Don't collapse them, the magazine's contribution is the reframe.
- **Prior usage:** Eddie's `presence-not-tools.md` essay (in the STYLE.md voice corpus) pre-dates this issue. If the corpus is referenced, attribute internally but do not quote it in the front-of-book, it's operator-facing for the writer, not reader-facing.

## How this fits the issue

**Primary placement:** Companion to the Lead (shelf item, 150 to 250 words), paired with the Lead Story section.

**Alternative placement:** Absorbed entirely into the Close as structural scaffolding, this article becomes the writer's reference doc only, no standalone section.

**Decision factor:** Front-of-book word budget. If total front-of-book after Lead + Conway + Trust Week is ≥1,200 words, absorb into Close only. If ≤1,000 words, run as Companion to stretch.

**FORMULA alignment:** Companion to the Lead slot exists when "Lead story has comparable cross-model/cross-product data worth tabling." Presence-as-category doesn't table data, it tables concepts. That's a stretch of the Companion slot definition. If Eddie reads the stretch as too far, fallback is scaffolding-only.

**Word budget:** 150 to 250w if Companion. Zero if scaffolding-only.

## Open questions / TODOs before press

- [ ] **Companion vs. scaffolding-only decision.** Eddie calls Thursday based on total front-of-book word budget.
- [ ] **Is the Term of Issue slot the right container?** Term of Issue slot (100 to 150w definition block) is a smaller footprint than Companion (150 to 250w). Could collapse into Term of Issue instead of Companion, cleaner if Presence is a term-name, not a section-frame.
- [ ] **Tension with Conway placement.** If Conway is Lead third-act, the presence argument lives inside the Lead naturally; Companion becomes redundant. If Conway is standalone B, the Companion has more work to do, it's the connective tissue.
- [ ] **Cross-check presence-not-tools.md.** Pull one line-level phrase from the voice corpus that does NOT appear in the front-of-book. If there isn't one clean enough to carry, the tie-back is cosmetic, drop it.
- [ ] **Final name test.** Presence vs. Always-on vs. Ambient. Presence won Tuesday PM. Does it still hold by Thursday? If a better term surfaces, swap at the lock.

## Voice notes for the distilled prose

- **Move:** Pattern 3 (the definition-as-beat). The term arrives mid-paragraph, not in a header. Reader earns the name by the time they read it.
- **Structural prompt, not prose:** the writer builds the argument one concrete product at a time. No abstract philosophy openers. Claude Design first, Conway second, Trust Week third, Close lands the term.
- **Kill rule:** no "paradigm shift," no "new era," no "the future of AI." These are the three vultures circling this topic. Shoot on sight.
- **Sass budget:** one dry line on the industry's appetite for always-on framing. Not a full paragraph. Sass earned, not sprayed (STYLE.md).
- **Forbidden:** "ushers in," "heralds," "defines a new category" (the magazine is *proposing* the category, not crowning it), "agentic future."
- **Raoul Duke anchor:** single-detail-as-characterization. Pick one concrete moment, a push notification from Conway, a Claude Design export-to-Canva click, a rotation advisory email, and let it carry the weight.
- **Tie-back:** the Close mirrors the Open beat. Whatever the Open landed on, the Close should rhyme with.

---

## Scaffolding-only mode (use if Companion slot is skipped)

If this article is not run as a standalone section, the writer still uses it as a reference. In that mode:

- The Term of Issue slot (if run) pulls its definition from the "concept in one line" section above.
- The Close pulls its three beats from the "Close move it enables" section.
- The cross-reference table is the writer's check that the argument is structurally grounded in existing issue material, not parachuted in.
- No prose from this file ships. It is scaffolding. The writer produces the words.
