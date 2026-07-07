---
title: "264 Checks"
section: also-shipped
status: skeleton
created: 2026-07-06
window_start: 2026-06-16
window_end: 2026-07-02
sources:
  - /Users/eddiebelaval/Development/id8/FIELD_NOTES.md (2026-06-16 release-cut hardening entry)
  - ~/.claude/skills/fd-cut-release/ (the skill this hardened into)
  - ~/Development/donato-brill-build/docs/RELEASE-PROTOCOL.md
  - memory: feedback_pre_delivery_test_security_gate, feedback_full_engine_docker_e2e_gate, feedback_release_deploy_doctrine
skeleton_note: >
  Fable set the spine + voice beats on the last sub day; a cheaper tier or the pipeline
  fleshes each beat to prose against STYLE.md. Every number below is load-bearing and must
  survive to an attribution caveat before publish — verify counts against FIELD_NOTES, do
  not round. This is an Also Shipped companion to the lead feature (the loop piece); it is
  the origin story of the /fd-cut-release gate that feature references.
---

# 264 Checks

## The spine (one sentence)

The night before a client release, an automated cut-gate ran 264 offline checks and caught a
crash bug and two security holes that every compile-check had waved through, which is the whole
argument for verification you cannot talk your way past.

## Beats to draft (in order)

1. **Open, in medias res.** The moment: a release bundle looked clean (compiled, tests green)
   the night before a D&B install. State the stakes in one line: a bad bundle in front of a law
   firm is the forward-deployment cardinal sin. Do not set up; drop the reader on the eve of the cut.

2. **What "looked ready" meant, and why that is a trap.** Compile-green and test-green is the
   floor, not the ceiling. Name the gap: a bundle can compile, pass unit tests, and still carry a
   runtime crash and a security hole because those live in the seams the compiler never reads
   (config, routing, secrets in the delivered `.env.example`, the actual Docker full-engine E2E).

3. **The gate, concretely.** The cut ran the full sequence: release-train sweep, pre-delivery test
   + CVE + security scan, Docker full-engine E2E, version-on-delivery, both transfer paths, Warden.
   264 offline checks total (VERIFY exact count vs FIELD_NOTES). Enumerate what it caught: one
   HIGH-severity crash bug, two Medium security holes, one silent routing bug. Name each in one
   clause; the specificity is the credibility.

4. **The counterfactual.** Without the gate, that bundle ships. The crash surfaces live, on the
   install call, in front of the client and their IT vendor. Tie back to the cardinal rule (never
   debug in front of the client) — the gate is how you keep the rule when you are one person and
   tired.

5. **The promotion.** This did not stay a one-off. It hardened into `/fd-cut-release`, a skill that
   runs the whole sequence on every client delivery and halts on the first red. Name the doctrine:
   the verifier is the product. Connect explicitly to the lead feature's ladder (a proven, recurring
   failure mode became an executable gate).

6. **Close.** One rhythm-closer beat. Candidate: the bundle that passed the compiler failed the gate,
   and the gate was right. Do not over-explain; land it and stop.

## Voice notes (enforce at draft time)

- No em/en dashes. First person. "Shipped." with the period if the magazine names itself.
- Kill list: "robust" (infra prose tempts it), "game-changing," "leverage," "best-in-class."
- Numbers are the voice here. Do not soften "264" or the severity counts into "several." Exactness
  is the register.
- Budget: do NOT use the "X isn't Y, it's Z" construction — it is spent in the lead feature for the issue.
- This piece must stay honest that the gate is boring by design. The drama is that boring caught what
  clever missed. Do not dramatize the tooling; dramatize the near-miss.

## Open question for Eddie (editorial)

Confirm this belongs in Issue 04 (window 6/16-7/02) vs held — the hardening pass is dated June 16,
in-window, but it also anchors a skill referenced in the lead feature, so running both in one issue
risks redundancy. Recommend running it as a short Also Shipped, not a second feature, so it complements
rather than repeats the lead. Your call on placement.
