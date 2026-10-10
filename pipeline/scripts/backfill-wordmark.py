#!/usr/bin/env python3
"""
Shipped. -- enforce the locked wordmark on every routine-published page.

Eddie 2026-09-29: "the Shipped font keeps changing ... this is how it should
always be" (the OG card). The site and templates draw the locked file; the
cloud routines render their own HTML and had improvised ~35 markups for the
wordmark as live text (402 instances on 169 pages, 109 light-on-dark).

This swaps each live-text wordmark, `Shipped<span class="...">.</span>` at the
start of an element's content, for the locked wordmark as INLINE SVG:
letters fill="currentColor" (so they take the element's own colour, which is
already correct for light and dark grounds), the period fixed orange. 1em tall
and baseline-aligned, so it sits where the text sat. No classes and no <style>
inside the SVG, so nothing leaks into or out of the page's CSS.

Source: pipeline/assets/shipped-wordmark.svg, a copy of the locked file
(id8 repo identity/id8labs-mark/family/shipped-wordmark.svg, src/shipped.py).

Idempotent: the swapped markup no longer matches, so a re-run changes nothing.

Usage:
  backfill-wordmark.py <root>            patch in place
  backfill-wordmark.py <root> --dry-run  report what would change
"""

import argparse
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ASSET = HERE.parent / "assets" / "shipped-wordmark.svg"
FOLDERS = ("anthropic-daily", "anthropic-weekly", "anthropic-monthly")

# The live-text wordmark at the START of an element's content, either alone or
# leading a short lockup ("Shipped. Daily", "Shipped. by id8Labs").
LIVE = re.compile(r'>Shipped<span class="[^"]*">\.</span>(?=\s|</)')


def inline_svg() -> str:
    src = ASSET.read_text(encoding="utf-8")
    vb = re.search(r'viewBox="([^"]+)"', src).group(1)
    w, h = (float(v) for v in vb.split()[2:])
    g = re.search(r'<g transform="([^"]+)">', src).group(1)
    ink = re.search(r'<path class="ink" d="([^"]+)"', src).group(1)
    dot = re.search(r'<path class="accent" d="([^"]+)"', src).group(1)
    # baseline sits at (h - descender); descender below baseline as a share of the height
    ty = float(g.split()[1].rstrip(")"))
    drop = (h - ty) / h
    return (
        f'<svg class="shipped-mark" viewBox="{vb}" role="img" aria-label="Shipped." '
        f'style="display:inline-block;height:1em;width:auto;vertical-align:-{drop:.3f}em;overflow:visible">'
        f'<g transform="{g}"><path fill="currentColor" d="{ink}"/><path fill="#ff6b35" d="{dot}"/></g></svg>'
    )


def pages(root: pathlib.Path):
    yield root / "index.html"
    for d in FOLDERS:
        yield from sorted((root / d).glob("*.html"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    root = pathlib.Path(a.root)
    mark = inline_svg()
    n_pages = n_marks = 0
    for page in pages(root):
        if not page.exists():
            continue
        html = page.read_text(encoding="utf-8")
        hits = len(LIVE.findall(html))
        if not hits:
            continue
        n_pages += 1
        n_marks += hits
        if not a.dry_run:
            page.write_text(LIVE.sub(">" + mark, html), encoding="utf-8")
    verb = "would swap" if a.dry_run else "swapped"
    print(f"backfill-wordmark: {verb} {n_marks} live-text wordmark(s) on {n_pages} page(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
