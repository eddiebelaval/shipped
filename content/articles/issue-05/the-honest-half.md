---
title: "The Honest Half"
section: also-shipped
status: draft
created: 2026-08-09
window_start: 2026-08-07
window_end: 2026-08-09
sources:
  - ~/Development/resonance/HANDOFF.md (constraints, the two corrections to the original spec, "things that bit")
  - ~/Development/resonance/src/data/primer.ts (the authored orientation pieces, incl. the neutrino paragraph)
  - ~/Development/resonance/src/core/design.ts:16-52 (SOLAR_ARC, the [95, 83] search bracket, the straddle assertion)
  - ~/Development/resonance/src/core/numerology.ts:108-128 (Personal Year turns on the birthday; the corpus-caught-the-engine comment)
  - ~/Development/resonance/src/data/corpus/numerology.ts:25-33 (the corpus entry that flagged the discrepancy)
  - ~/Development/resonance/src/core/nonaContext.ts + api/nona.ts (the interpret-only seam)
  - live: resonance88.id8labs.app
  - memory: project-resonance-shipped, feedback-a-guard-you-never-saw-fail-is-not-a-guard
note: >
  Own-work register, same week as the build, per the also-shipped precedent set by
  "The Flower and the Clock" (issue 05) and "264 Checks" (issue 04). No em dashes per the
  VOICE gene. The "isn't Y, it's Z" move is spent once, on purpose, in the section break
  before The Line.

  Editorial pipeline run 2026-08-09, six passes. Fact-check corrected four claims against
  source: 184 tests belongs to the whole suite (15 files), not to the astronomy half;
  "static host" was wrong (api/nona.ts is a serverless function, so the claim is now scoped
  to the reading never touching a server); the Personal Year rollover is eleven weeks, not
  ten (1 January to 21 March is 79 days); 177 is the Academy shelf count, generated from
  the reference corpus, not the corpus itself. Structural cut the orphaned "it is free, it
  is live" line before the closer (it was a second three-beat competing with the real one)
  and moved free/live up to the second paragraph as information. "What I would take to the
  next one" retitled "What generalizes" and its second beat rewritten to stop restating the
  thesis. Nona's rising-sign refusal broken out to land as an isolated punchline.
  Adversarial softened one unevidenced market claim ("makes its money" to "is built on")
  and REJECTED any hedge on the neutrino paragraph or the 1987 provenance.

  OPEN FOR EDDIE, not an article problem: the comment in design.ts:23 says births near the
  FAST end of the orbit put the root outside 92 days. The physics in the same comment says
  the opposite (fast end is 86.3 days, slow end is 92.3). The code is correct; the comment
  contradicts itself. The article now says "slow end," which matches the numbers.
---

# The Honest Half

This week I wrote a sentence into an app that undercuts the app.

The app is Resonance. It is free, it is live, and it draws your Human Design chart and your Pythagorean numerology in a browser. The sentence sits in its orientation section, and it reads: *nothing in physics says they carry information that shapes a person, and no study has shown a Human Design chart predicts anything.*

"They" is neutrinos. Human Design dates to January 1987, when a man named Alan Krakower took the name Ra Uru Hu and said he received the system over eight days on Ibiza. His mechanism: neutrinos streaming off the Sun carry information into you at birth. Neutrinos are real. They pass through you in astonishing numbers. They were confirmed to have mass in 1998. The rest is a story.

I put the sentence in anyway. Leaving it out would have made everything else in the app less true.

## The half you can check

Half of Resonance is astronomy, and astronomy is checkable.

A star-position engine is built into the page. No API call, no lookup table, no stored chart. Every reading is a pure function of two instants: the one you were born in, and the one you are reading in. That constraint bought more than purity. It is why scrubbing the sky six months forward cost exactly one state variable, and why a reading never touches a server.

The project carries 184 tests across 15 files and a set of golden fixtures the engine is not allowed to argue with. Two of those caught things I would never have found by reading the code.

The first was a search bracket. Human Design casts your chart twice: once at birth, and once at the moment the Sun sat 88 degrees of arc earlier. Eighty-eight degrees is roughly 88 days, so the original spec searched a window of 92 to 84 days back and bisected for the root. That window is wrong, and it is wrong in the worst available way. The Earth's orbit is an ellipse, so the Sun's apparent motion runs about 0.9533 degrees per day at aphelion and about 1.0197 at perihelion. Eighty-eight degrees of arc takes anywhere from 86.3 to 92.3 days depending on where in the year you were born. A birth near the slow end of the orbit puts the root just outside 92.

A bisection that does not straddle its root does not fail. It converges cheerfully to the endpoint and hands back a plausible, wrong date. Nothing on screen looks broken. Half your chart is simply somebody else's. The window is [95, 83] now, and the function throws unless the bracket actually straddles.

The second is my favorite thing all week, and it went the other way. The app ships a 177-entry reference shelf, generated from a corpus that is cross-checked against the engine, explaining what each gate and number means. One of those entries says the Personal Year turns on your birthday, not on 1 January. The engine used the calendar year. So the prose promised one thing and the arithmetic did another, and a 21 March subject rolled over on 1 January, silently, eleven weeks before the app said it would.

The corpus caught the engine. The words were right and the math was wrong, which is not the direction that failure usually runs.

## The half you cannot

The other half is a tradition somebody invented in living memory, and it borrows openly. The 64 gates are the 64 hexagrams of the I Ching. The positions are read off Western astrology. The nine centers are an expansion of the seven Hindu chakras. The shape wiring them together is the Kabbalistic Tree of Life.

None of that is a knock. It is a synthesis, it is coherent, and people find it useful. But it is not tested, and no amount of correct astronomy underneath makes it tested.

This is the move most software in the category is built on. You compute something real, you print something unfalsifiable next to it, and you let the precision of the first launder the authority of the second. The decimal places do the arguing. Nobody has to claim anything.

That isn't a design decision you make once. It's a line you either draw or spend the whole build quietly erasing.

## The line, in code

So the app says which half is which, out loud, in its own orientation section, before it tells you anything flattering about yourself.

And the line is not only copy. It is enforced at the one place it could plausibly leak. Resonance has an agent named Nona, who answers questions about your chart. She is handed every fact pre-computed and cannot derive new ones. That boundary is asserted in tests. Then it was verified in production the only way that counts. Somebody asked her for a rising sign, which the engine does not compute. She declined to invent one.

An app that builds a reference corpus for accuracy and then blurs the line about what the corpus is has not been accurate about the thing that matters.

## What generalizes

Two things carry past an app about hexagrams.

The first is that a wrong answer that looks right is a different category of bug from a crash, and it deserves a different category of defense. The bracket did not need a try/catch. It needed an assertion that the assumption it was built on was still true at runtime. Most of what I got wrong this week was shaped like that.

The second is cheaper than it sounds. Naming the seam between the hard layer and the soft one cost four paragraphs of copy nobody asked for, and it is the only reason the rest of the page is worth reading.

The engine computes.
The tradition interprets.
The page says which is which.
