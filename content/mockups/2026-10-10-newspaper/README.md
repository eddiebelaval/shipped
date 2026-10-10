# Shipped. newspaper mockups (2026-10-10)

- `index.html`: four layout directions (A Broadsheet, B Riso Tabloid, C The Wire, D Sunday Section) plus an image-treatment comparison. Keys 1-4 switch.
- `hybrid.html`: the pick under review. Broadsheet below, riso halftone cover splash above.
- `src/`: source photos + `credits.json` (licenses).
- `img/`: renders. Atkinson and halftone are from the image press with auto exposure; the Bayer and duo files are the first-pass renders kept for the comparison page only (retired treatments).

Re-render: `python pipeline/scripts/image-press.py render content/mockups/2026-10-10-newspaper/src content/mockups/2026-10-10-newspaper/img --halftone capitol,racks,keys,circuit` (needs numpy + Pillow).
Spec: `content/DESIGN.md`, Revision 6 (proposed).
