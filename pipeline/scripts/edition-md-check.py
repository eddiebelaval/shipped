#!/usr/bin/env python3
"""Shipped. edition markdown: the one shape the paper front renders from.

The cloud routines write their markdown in this shape (content/anthropic-<cadence>/<stem>.md) and run this
check before publishing. The Edition Desk renders the paper front straight from a file that passes, so it
never has to guess an edition's structure back out of HTML (the cause of every hold 2026-10-12 to 10-15).

Shape (frontmatter, then sections in this order; optional ones may be left out):

    ---
    date: 2026-10-15                       # daily: the Eastern date; weekly: the Friday; monthly: the last day
    title: "Shipped. Daily, Thursday, October 15, 2026"
    deck: "One sentence, the shape of the day."
    period: "Oct 14 to Oct 15"
    weather: "Optional closing line for the front."
    ---

    ## The Open                           (optional)
    *An optional italic opening line.*
    Paragraphs.

    ## The Lead Story                     (required)
    # The Lead's Headline
    **An optional bold deck line.**
    Paragraphs; links as [text](url).

    ## Also Shipped                       (optional)
    ### A Story's Headline
    Paragraphs.
    *[github.com/org/repo/releases](https://github.com/org/repo/releases)*   (the story's source line, last;
                                          write it whenever the story cites one primary source)

    ## Quiet on the Wire                  (optional)
    ## The Close                          (optional)

    ## A. Category Name                   (the release log: lettered A, B, C... in order)
    *One italic deck line for the category.*   (optional; the only text allowed before the first entry)
    #### 2026-10-15 - Entry Title ([source](https://primary.source/url))   (a monthly may date YYYY-MM; source optional if linked in the body)
    `[MODEL]`

    One paragraph of body.

    **How to use:** optional.

    **Why it matters:** optional.

Same words (2026-10-19): this markdown is the edition. Every sentence, source line and deck line on the
published page is in it word for word, and nothing on the page is missing from it. On 10-19 the page
carried a source line, two category decks and a reworded sentence the markdown did not, and the desk's
shadow held it.

usage: python3 edition-md-check.py FILE.md      exit 0 = renders as is; exit 1 prints every problem
"""
import re
import sys

TAGS = {"MODEL", "API", "CODE", "APPS", "SDK", "SDK-PY", "SDK-TS", "NEWS", "RESEARCH", "DEPRECATION"}
FRONT = ("The Open", "The Lead Story", "Also Shipped", "Quiet on the Wire", "The Close")
DASH = re.compile("[" + chr(0x2014) + chr(0x2013) + "]")
ENTRY = re.compile(r"^#### (\d{4}-\d{2}(?:-\d{2})?) - (.+?)(?: \(\[source\]\((https?://[^)\s]+)\)\))?\s*$")


def check(text):
    p = []
    if not text.startswith("---\n") or text.count("\n---\n") < 1:
        return ["no frontmatter (--- block) at the top"]
    head, body = text[4:].split("\n---\n", 1)
    fm = dict(re.findall(r"^(\w+):\s*(.*)$", head, re.M))
    for k in ("date", "title", "deck"):
        if not fm.get(k, "").strip().strip('"'):
            p.append(f"frontmatter: '{k}' missing")
    if fm.get("date") and not re.match(r'^"?\d{4}-\d{2}-\d{2}"?$', fm["date"].strip()):
        p.append(f"frontmatter: date '{fm['date']}' is not YYYY-MM-DD")
    if DASH.search(text):
        p.append("an em or en dash is in the file (house rule: none)")

    secs = re.split(r"^## ", body, flags=re.M)[1:]
    names = [s.partition("\n")[0].strip() for s in secs]
    front = [n for n in names if n in FRONT]
    if "The Lead Story" not in names:
        p.append("no '## The Lead Story' section")
    if front != [n for n in FRONT if n in front]:
        p.append(f"front sections out of order: {front} (order is {list(FRONT)})")
    letter, entries, seen_log = "A", 0, False
    for s in secs:
        name, _, content = s.partition("\n")
        name = name.strip()
        if name in FRONT:
            if seen_log:
                p.append(f"'## {name}' comes after the release log")
            if name == "The Lead Story":
                titles = re.findall(r"^# (.+)$", content, re.M)
                if len(titles) != 1:
                    p.append(f"The Lead Story needs exactly one '# Headline' line (found {len(titles)})")
                paras = [b for b in re.split(r"\n\s*\n", content) if b.strip() and not b.lstrip().startswith("# ")]
                if not paras:
                    p.append("The Lead Story has no paragraphs")
            if name == "Also Shipped":
                stories = re.split(r"^### ", content, flags=re.M)
                if stories[0].strip():
                    p.append("Also Shipped has text before its first '### Headline'")
                for st in stories[1:]:
                    t, _, b = st.partition("\n")
                    if not b.strip():
                        p.append(f"Also Shipped story '{t.strip()[:40]}' has no paragraphs")
            continue
        m = re.match(r"^([A-Z])\. (.+)$", name)
        if not m:
            p.append(f"unknown section '## {name}' (front sections: {', '.join(FRONT)}; log: '## A. Category')")
            continue
        seen_log = True
        if m.group(1) != letter:
            p.append(f"log section '## {name}' should be lettered {letter}.")
        letter = chr(ord(m.group(1)) + 1)
        blocks = re.split(r"^(?=#### )", content, flags=re.M)
        if blocks[0].strip() and not re.fullmatch(r"\*[^*].*\*", blocks[0].strip()):
            p.append(f"'## {name}': text before its first entry (only one *italic deck line* is allowed)")
        for blk in blocks[1:]:
            head_line, _, rest = blk.partition("\n")
            em = ENTRY.match(head_line)
            if not em:
                p.append(f"log entry heading not '#### YYYY-MM-DD - Title ([source](url))': {head_line[:70]}")
                continue
            entries += 1
            tm = re.match(r"^`\[([A-Z-]+)\]`\s*$", rest.lstrip("\n").partition("\n")[0])
            if not tm:
                p.append(f"entry '{em.group(2)[:40]}': second line must be a tag like `[MODEL]`")
            elif tm.group(1) not in TAGS:
                p.append(f"entry '{em.group(2)[:40]}': tag {tm.group(1)} not one of {sorted(TAGS)}")
    return p  # a log with no entries is allowed: a genuinely empty day prints an empty log box


if __name__ == "__main__":
    probs = check(open(sys.argv[1], encoding="utf-8").read())
    for x in probs:
        print("FAIL", x)
    print("edition-md-check: OK" if not probs else f"edition-md-check: {len(probs)} problem(s)")
    sys.exit(1 if probs else 0)
