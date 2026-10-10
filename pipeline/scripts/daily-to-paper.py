"""Shipped. daily edition -> paper-layout issue markdown (preview / future routine adoption).

The cloud routines write dailies as their own markdown (The Open, The Dig with
### stories, Quiet on the Wire, The Close, a bullet Release Log). This maps one
into the issue shape the renderer's paper front reads: the first Dig story is
the lead, the rest are Also Shipped, the bold dek is the deck, the bullets
become release-log entries.

usage: python daily-to-paper.py DAILY_MD OUT_MD
OUT_MD should be named issue-NN-*.md (the number keys its images folder).
"""
import re, sys

CATS = {"models": "MODEL", "api": "API", "claude apps": "APPS", "claude code": "CODE", "news": "NEWS"}

def main(src, dst):
    text = open(src).read()
    fm = dict(re.findall(r"^(\w+):\s*\"?(.*?)\"?\s*$", text.split("---")[1], re.M))
    body = text.split("---", 2)[2]
    dek = re.search(r"^\*\*(.+?)\*\*\s*$", body, re.M)
    secs = {m.group(1).strip(): m.group(2).strip() for m in re.finditer(r"^## (.+?)\n(.*?)(?=^## |\Z)", body, re.M | re.S)}
    dig = [c for c in re.split(r"^### ", secs.get("The Dig", ""), flags=re.M)[1:]]
    stories = []
    for c in dig:
        title, _, rest = c.partition("\n")
        title = re.sub(r"\s*\((?:[A-Z][a-z]{2} \d+)\)\s*$", "", title.strip()).replace(" -- ", ": ")
        stories.append((title, rest.strip().strip("-").strip()))
    date = fm["date"]
    log, letter = [], "A"
    for m in re.finditer(r"^### (.+?)\n(.*?)(?=^### |\Z)", secs.get("Release Log", ""), re.M | re.S):
        cat = m.group(1).strip(); tag = CATS.get(cat.lower(), "NEWS")
        entries = []
        for b in re.findall(r"^- (.+)$", m.group(2), re.M):
            bm = re.match(r"\*\*(.+?)\*\*\s*--\s*(.+)", b)
            title, summ = (bm.group(1), bm.group(2)) if bm else (re.split(r"[;.]", b)[0], b)
            entries.append(f"#### {date} — {title.strip()}\n`[{tag}]`\n\n{summ.strip()}\n")
        log.append(f"## {letter}. {cat}\n\n" + "\n".join(entries)); letter = chr(ord(letter) + 1)
    close_last = [l for l in secs.get("The Close", "").splitlines() if l.strip() and not l.startswith("---")]
    out = f"""---
issue: 90
title: "Shipped. Daily, {fm.get('mast', date)}"
date: {date}
period: {date} to {date}
status: published
masthead: Shipped.
layout: paper
edition: Daily Edition
issue_label: "Daily · {fm.get('window', date)}"
deck: "{(dek.group(1) if dek else '').replace('"', "'")}"
weather: "{(close_last[-1] if close_last else '').replace('"', "'")}"
---

## The Open

{secs.get('The Open', '').strip('- ').strip()}

## The Lead Story

# {stories[0][0]}

{stories[0][1]}

## Also Shipped

""" + "\n\n".join(f"### {t}\n\n{b}" for t, b in stories[1:]) + f"""

## Quiet on the Wire

{secs.get('Quiet on the Wire', '').strip('- ').strip()}

## The Close

{secs.get('The Close', '').strip('- ').strip()}

""" + "\n\n".join(log) + "\n"
    open(dst, "w").write(out.replace(" -- ", ", "))
    print(f"wrote {dst}: lead '{stories[0][0]}', {len(stories)-1} also-shipped, {sum(l.count('####') for l in log)} log entries")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
