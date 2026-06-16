# DAILY.md — Shipped. Daily

> The depth doctrine for the daily digest. FORMULA.md governs the weekly's volume and shape; this file governs the daily's **depth**. It exists because the daily kept collapsing on quiet days: two items shipped, two paragraphs went out.
>
> **The core law: size the copy to the reader's value, never to the release count.** A bug-fix day is not a thin read. It is a day that demands you dig.

**Read order:** [VISION.md](../VISION.md) → [STYLE.md](./STYLE.md) → [FORMULA.md](./FORMULA.md) → **DAILY.md** (this file).

Authored 2026-06-10 by Eddie Belaval (with Claude). Derived from the June 8 daily (298 words, two items, thin) and the recurring "bug day = two paragraphs" failure.

---

## The failure this fixes

The daily routine summarizes what Anthropic shipped in a 24-hour window. When a lot ships, the digest is full. When little ships — a hotfix, one SDK patch, a docs change — the digest shrivels to a lead paragraph and a release-log stub. 298 words. The reader opens it, sees nothing happened, and learns nothing.

That is the wrong instinct. **A quiet day is the day the daily earns its slot.** Anyone can rewrite a release-heavy day into a list. The value of a curated daily is that it tells you what a one-line bug fix actually *means* for the code you're running tonight. On a loud day the facts carry the read. On a quiet day, *we* carry it.

The rule: **the depth floor does not move with the news.** Few items is not few words. Few items is more work per item.

---

## The Dig — five levers, run on every item

When the surface is thin, go down. Every item — even a one-line changelog entry, even a bug fix — gets run through these five levers. Most release-log lines won't survive all five, and that's fine; the ones that do become the day's read.

1. **The mechanism.** What actually changed, one level below the changelog sentence. Not "fixed an auth bug" — *what* was broken, in the actual code path. "The Foundry client wasn't attaching the `x-api-key` header on API-key auth" is a mechanism. "Auth bug fixed" is a press release.

2. **The blast radius.** Who hit this, how they'd have noticed, what it cost them. Name the builder. "Anyone authenticating to Claude through Azure AI Foundry with an API key was getting silent 401s with a key they *knew* was valid — the kind of failure you burn an afternoon blaming on your own config." A bug nobody could hit is a release-log line. A bug that cost someone a Tuesday is a lead.

3. **The pattern.** Where this sits in the week and the month. Is it the third SDK auth fix in a fortnight? A drift in one product's stability? A theme (security week, agent-infra week)? Link to the recent dailies. One data point is a fact; three is a story, and the daily is the only place positioned to connect them day-over-day.

4. **The read.** What it tells you about the platform — stated as opinion, with teeth, per STYLE.md. Maturity, surface area, where Anthropic is spending its attention, what they're quietly conceding. This is the sentence the reader screenshots. Earn one per daily.

5. **The builder's move.** What the reader should actually *do* tonight. Pin the version. Update. Check if last week's phantom errors were this. Ignore it unless you're on the affected path. End every item that survives the dig on a verb the reader can act on.

If an item runs the five levers and still has nothing — no mechanism worth explaining, no one in the blast radius, no pattern, no read, no move — it stays a one-line Release Log entry. Not everything earns prose. But the *default* is to dig before demoting, not demote by default.

---

## Word discipline

Depth comes from the five levers, never from adjectives. "Write more" means *tell more* — more mechanism, more stakes, more pattern. It never means more padding.

| Day shape | Word floor (front matter, ex-Release Log) | Notes |
|---|---|---|
| One real item (bug fix, single patch) | **500** | The hardest day. One item, fully dug, beats five items listed. |
| Quiet day (2–3 items) | **600–900** | The June-8 case. This is where the doctrine bites. |
| Normal day (4–6 items) | 700–1,100 | Lead + 2–3 dug items + the rest in the log. |
| Heavy day | up to 1,400 | Same ceiling logic as the weekly. Split if it overflows. |

There is no upper-bound *exemption* on a quiet day and no lower-bound *excuse*. If the day genuinely produced nothing — no releases, no news, repo silent — say that in one honest sentence and pivot to ecosystem context (a community build on the SDK, a research citation, a competitor move that reframes the week). The daily never skips and never lies that something happened. But "nothing shipped" is rare; "nothing *looked* like it shipped" is the usual case, and that's a dig, not a skip.

---

## The shape of a dug daily

```
Lead            The one item that carries the day, fully dug through all five levers.
                Even if it's a bug fix. 150–300 words.

The Dig         1–3 secondary items, each run through the levers that apply.
                Not every lever on every item — the ones that have something.
                80–150 words each.

The Read        One opinion sentence the day earned. Can live inside the Lead
                or stand alone. The screenshot line. (STYLE.md sass budget.)

Quiet on the    What landed just outside the window, what's rumored, what to
Wire            watch tomorrow. 50–80 words.

Release Log     Everything in the window, grouped A–G per STYLE.md. The items
                that didn't survive the dig live here as one-liners. Unbounded.
```

This is not the weekly's seven-section skeleton. The daily is lighter and faster. But it has a spine, and the spine holds even when two items shipped.

---

## Voice — same house, same teeth

The daily is governed by STYLE.md exactly like the weekly. Dry, confident, opinions stated never hedged, sass load-bearing. The forbidden-phrase list applies. The "X isn't Y, it's Z" budget is **one per daily** (tighter than the weekly, because the daily is short and the tic shows faster). No "thrilled to," no "ushers in," no "EPIC."

Digging deeper is not license to inflate. The teeth come from precision — naming the blast radius, stating the read — not from volume. A 700-word daily that respects the reader's time is the target. A 700-word daily that padded its way there is the failure mode this doc was written to kill.

---

## The line that doesn't fabricate

Depth is interpretation, not invention. The five levers add *analysis* grounded in the facts that shipped — they never add facts that didn't. The blast radius is reasoned from the mechanism, not reported as if a source said it. The pattern links real prior dailies, not imagined ones. The read is opinion, flagged as opinion. Every number, quote, and date still passes the verifier. You can dig as deep as you want; you cannot dig up something that isn't there.

---

## Changelog

| Date | Change | Reason |
|---|---|---|
| 2026-06-10 | Initial draft. The Dig (five levers), word floors, dug-daily shape. | The daily had no depth doctrine; quiet days collapsed to two paragraphs. FORMULA governs the weekly's shape, nothing governed the daily's depth. |
