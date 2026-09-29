#!/usr/bin/env python3
"""
Shipped. -- give every routine-published page a share image.

The daily, weekly and monthly pages on the daily-pages branch declare
twitter:card summary_large_image but never name an image, so every shared link
to a daily or a sweep showed no picture (found 2026-09-29, 142 dailies and 25
sweeps). The routines render HTML from their own prompts, so the fix lives
here, at the branch, like the subscribe block: deterministic, covers every
routine, and heals any page a prompt later writes without it.

The image is the brand card, per Eddie's standing rule (the thumbnail is the
brand, not the edition), in the sibling for the page's kind:

  anthropic-daily/*, index.html     -> og-daily-v1.png  (Every night, 9 PM ET)
  anthropic-weekly/*, -monthly/*    -> og-sweep-v1.png  (The week, swept)

Both are served from id8labs.app (pipeline/src/og/file.ts names them) and draw
the locked Shipped. wordmark. Other folders on the branch are left alone.

Idempotent: a page that already names an og:image is skipped. Guarded: a card
is only linked once it is actually served (HTTP 200, image/png) from
id8labs.app, so the sweep never points a page at an image that is not live.

Usage:
  backfill-og.py <root>            patch in place
  backfill-og.py <root> --dry-run  report what would change
"""

import argparse
import pathlib
import sys
import urllib.request

BASE = "https://id8labs.app/shipped/"
# The ?v= query is the cache key, like the site's own ?v=3 icons. Cloudflare
# fronts id8labs.app and every .png path is served "immutable, 1 year", 404s
# included: a pre-deploy existence check (2026-09-29) pinned a 404 on the bare
# URLs. Bump v when a card changes; never probe a URL before it is deployed.
CARDS = {
    "anthropic-daily": "og-daily-v1.png?v=1",
    "anthropic-weekly": "og-sweep-v1.png?v=1",
    "anthropic-monthly": "og-sweep-v1.png?v=1",
}
ALT = "Shipped. from id8"


def card_for(root: pathlib.Path, page: pathlib.Path):
    rel = page.relative_to(root)
    if rel.as_posix() == "index.html":
        return CARDS["anthropic-daily"]
    return CARDS.get(rel.parts[0]) if len(rel.parts) > 1 else None


def tags(url: str) -> str:
    return (
        f'<meta property="og:image" content="{url}">\n'
        f'<meta property="og:image:width" content="1200">\n'
        f'<meta property="og:image:height" content="630">\n'
        f'<meta property="og:image:alt" content="{ALT}">\n'
        f'<meta name="twitter:image" content="{url}">\n'
    )


def patch(html: str, url: str):
    if 'property="og:image"' in html:
        return None
    # After the last og:/twitter: meta if there is one, else before </head>.
    anchor = max(html.rfind('<meta property="og:'), html.rfind('<meta name="twitter:'))
    if anchor != -1:
        end = html.find(">", anchor) + 1
        nl = "\n" if html[end:end + 1] != "\n" else ""
        return html[:end] + "\n" + tags(url).rstrip("\n") + nl + html[end:]
    head = html.find("</head>")
    if head == -1:
        return None
    return html[:head] + tags(url) + html[head:]


def live(url: str) -> bool:
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "shipped-sweep"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status == 200 and r.headers.get("Content-Type", "").startswith("image/")
    except Exception:
        return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    root = pathlib.Path(a.root)
    serving = {c: live(BASE + c) for c in set(CARDS.values())}
    missing = sorted(c for c, ok in serving.items() if not ok)
    if missing:
        print(f"backfill-og: skipped, card(s) not live yet on {BASE}: {', '.join(missing)}")
        return 0
    changed, skipped = [], 0
    for page in sorted(root.rglob("*.html")):
        card = card_for(root, page)
        if not card:
            continue
        html = page.read_text(encoding="utf-8")
        out = patch(html, BASE + card)
        if out is None:
            skipped += 1
            continue
        changed.append(page.relative_to(root).as_posix())
        if not a.dry_run:
            page.write_text(out, encoding="utf-8")
    verb = "would add" if a.dry_run else "added"
    print(f"backfill-og: {verb} a share image to {len(changed)} page(s), {skipped} already had one")
    return 0


if __name__ == "__main__":
    sys.exit(main())
