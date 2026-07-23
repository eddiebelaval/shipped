#!/usr/bin/env python3
"""
Shipped. — backfill the subscribe CTA into published daily/weekly/monthly pages.

The pages on the daily-pages branch had no subscribe form at all: not at the
top, not at the foot. They are also the most current surface Shipped. has (77
dailies through 2026-07-22, while the numbered issues stopped at Jun 16), so
every reader the dailies reached had no way to subscribe.

Applies the same two edits the templates now make, so a backfilled page and a
freshly rendered one are structurally identical:

  1. A "Subscribe" pill in the sticky publication bar, anchored to #subscribe.
     Folio/date meta collapse under 720px so the bar stays one line.
  2. The subscribe block from src/render/subscribe-block.html before </body>,
     with {{SOURCE}} bound to the page type for attribution.

Idempotent: a page that already carries the CTA is skipped, so a re-run after a
partial failure is safe.

Usage:
  backfill-subscribe.py <root>            patch in place
  backfill-subscribe.py <root> --dry-run  report what would change
"""

import argparse
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
SNIPPET = HERE.parent / "src" / "render" / "subscribe-block.html"

# Directory -> the source tag the form reports. The "shipped" prefix is load
# bearing: the subscribe API only merges a reader onto the Shipped. list when
# the source starts with it.
SOURCES = {
    "anthropic-daily": "shipped-daily",
    "anthropic-weekly": "shipped-weekly",
    "anthropic-monthly": "shipped-monthly",
}

CTA_LINK = '    <a href="#subscribe" class="pub-bar-cta">Subscribe</a>\n'

# The 88 published pages span four shapes, found by surveying rather than
# assuming: 50 modern (pub-bar + closed document), 36 older (no nav at all,
# predating the publication bar), and 2 truncated files that simply stop after
# </footer> with no </body> or </html>. The patcher handles all four, and the
# CTA is applied only where there is a spine to put it in.


def patch(html: str, source: str) -> tuple[str, str | None, str]:
    """Return (new_html, error, note). error is None on success."""
    if 'class="pub-bar-cta"' in html or 'id="subscribe"' in html:
        return html, "already-patched", ""

    notes = []

    # 1 — Spine CTA, only where a publication bar exists. The older chrome has
    # no nav, so those pages get the form without a top CTA rather than failing.
    m = re.search(r'<div class="pub-bar-right">(.*?)</div>', html, re.S)
    if m:
        inner = m.group(1)
        # Collapse existing meta on narrow screens so the CTA always has room.
        new_inner = inner.replace(
            '<span class="pub-bar-meta">', '<span class="pub-bar-meta pub-bar-hide-sm">'
        ).replace(
            '<span class="pub-bar-sep">', '<span class="pub-bar-sep pub-bar-hide-sm">'
        )
        html = (
            html[: m.start()]
            + f'<div class="pub-bar-right">{new_inner}{CTA_LINK}  </div>'
            + html[m.end() :]
        )
    else:
        notes.append("no-spine")

    # 2 — The subscribe block. Every page gets it. All the CSS it needs travels
    # with it (with token fallbacks), so it renders correctly on the 37 pages
    # that predate the shared design tokens.
    block = SNIPPET.read_text(encoding="utf-8").replace("{{SOURCE}}", source)

    n_body = html.count("</body>")
    if n_body == 1:
        html = html.replace("</body>", block + "\n</body>", 1)
    elif n_body == 0:
        # Truncated document: append the block and close it properly.
        html = html.rstrip() + "\n" + block + "\n</body>\n</html>\n"
        notes.append("closed-truncated-doc")
    else:
        return html, f"expected 0 or 1 </body>, found {n_body}", ""

    return html, None, ",".join(notes)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", help="checkout root holding anthropic-*/ dirs")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    root = pathlib.Path(args.root)
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 1
    if not SNIPPET.exists():
        print(f"snippet not found: {SNIPPET}", file=sys.stderr)
        return 1

    patched, skipped, failed, noted = [], [], [], []

    for subdir, source in sorted(SOURCES.items()):
        d = root / subdir
        if not d.is_dir():
            continue
        for page in sorted(d.glob("*.html")):
            rel = str(page.relative_to(root))
            original = page.read_text(encoding="utf-8")
            new, err, note = patch(original, source)
            if err == "already-patched":
                skipped.append(rel)
                continue
            if err:
                failed.append(f"{rel}: {err}")
                continue
            if not args.dry_run:
                page.write_text(new, encoding="utf-8")
            patched.append(rel)
            if note:
                noted.append(f"{rel}: {note}")

    verb = "would patch" if args.dry_run else "patched"
    print(f"{verb}: {len(patched)}   already had it: {len(skipped)}   failed: {len(failed)}")
    if noted:
        no_spine = [n for n in noted if "no-spine" in n]
        truncated = [n for n in noted if "closed-truncated-doc" in n]
        print(f"  form-only (older chrome, no publication bar): {len(no_spine)}")
        for t in truncated:
            print(f"  CLOSED TRUNCATED DOC {t}")
    for f in failed:
        print(f"  FAIL {f}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
