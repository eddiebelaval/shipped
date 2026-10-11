#!/usr/bin/env python3
"""Shipped. image QC: Claude holds the image review gate for editions.

Eddie, 2026-10-11: "i want out of the loop here. i need to trust you for QC."
His 10/10 bar was a human looking at every image "for legibility and aesthetic."
This is that look, made explicit and repeatable, so it can be trusted only after
it has proven it agrees with him (image-qc.py calibrate, below).

Per image the front will draw:
  1. HARD     the press flags (washed out / too heavy / flooded / halftone size)
              must be empty; a credit must exist; a generated image must say
              "AI-generated". Any failure rejects, no model involved.
  2. LOOK     Claude reads the printed PNG (what readers see) and the source
              photo, plus the caption and the story it sits beside, and scores
              five things 1-5 against DESIGN.md Rev 6. It also lists hard faults
              (text or logos, an identifiable real person, gore, a caption that
              says something the picture does not show, a picture implied to be
              the news event).
  3. CALL     approve only when no hard fault and legibility, relevance and caption
              truth each score 3+ (look and taste are advisory, rejecting only at 1);
              else reject with the reason. The bar is GATE below, set by calibration. For cover and lead, both treatments are graded and
              the stronger passing one is picked.

Writes approve / reject into the manifest as "Claude QC" with the scores in the
note, so every call is auditable later.

usage:
  image-qc.py review IMAGES_DIR --context EDITION_MD [--dry-run]
  image-qc.py calibrate             Eddie's approved images + known-bad decoys; must score 100%
"""
import argparse, importlib.util, json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
CONTENT = Path(os.environ.get("SHIPPED_CONTENT", SCRIPTS.parent.parent / "content"))
OUTPUT = SCRIPTS.parent / "output"
MODEL = os.environ.get("SHIPPED_QC_MODEL", "opus")
BY = "Claude QC"
AXES = ("legibility", "look", "relevance", "caption_truth", "taste")
# What gates and at what score. Eddie's own approvals (issue 10) taught this: the grader
# marked down heavy ink and one-ink detail loss that he called "excellent, exactly what I
# wanted", so look and taste only reject at rock bottom; readability and truth gate.
GATE = {"legibility": 3, "relevance": 3, "caption_truth": 3, "look": 2, "taste": 2}

RUBRIC = """You are the image editor of Shipped., a newspaper about the frontier AI labs. Every photo is
printed as a single-ink orange dither (Atkinson, or riso halftone for the big cover) on warm paper.
The editor-in-chief's bar: "legibility and aesthetic", and he loved images that were concrete,
tactile objects shot close (a knife switch, a wax seal, a split-flap clock mechanism, a calendar
with a circled date), readable at a glance in one ink.

Read the two image files with the Read tool:
  PRINTED: {printed}   (what readers see; judge legibility and look on THIS)
  SOURCE:  {source}    (the original photo, to check what is really in it)

Slot: {slot} ({size})
Caption printed under it: "{caption}"
Credit: "{credit}"
Source record (the file's own title on Wikimedia Commons, or the prompt it was generated from):
"{record}"
It runs beside this story:
---
{story}
---

Score each 1-5 (5 best):
- legibility: in the PRINTED file, can a reader tell what the subject is within a second?
  5 = instantly; 3 = recognisable once you read the caption; 1 = blank, noise, mush, or broken.
  A one-ink dither always loses fine detail and mid-tones; heavy ink or lost texture is normal
  and is NOT a legibility problem while the subject's shape still reads.
- look: does it work printed in one ink? 3 = acceptable. Advisory: reported, not gating.
- relevance: does the subject earn its place next to this story (literal, or a metaphor)?
  3 = loosely fits; 1 = has nothing to do with the story.
- caption_truth: does the PICTURE contradict the caption? Facts that come from the source record
  (who, when, where) are fine even though no picture can show a date. Every source is stored in
  grayscale, so a colour or material word (blue, red, copper, brass) cannot be checked: at worst
  that scores 3, never lower, and say in the note to drop the word. Score 1 or 2 ONLY when the
  caption names a different object, scene, count or action than the picture shows. 5 = matches.
- taste: right for a serious publication? Advisory: reported, not gating.

Hard faults (any one rejects): readable text, signage, logos or watermarks that dominate;
an identifiable real person's face; gore or distress; the picture implies it IS the news event;
a caption that is false; the printed file is blank, inverted, or broken.

If the caption is not exactly right (caption_truth under 5), write the corrected caption in
caption_fix: literal, no colour words, keeping any who/when/where facts from the source record.
If the caption names the wrong kind of object (a display called a clock, booths called a queue),
caption_truth is 2 at most.

Answer with ONLY this JSON, no prose:
{{"legibility": n, "look": n, "relevance": n, "caption_truth": n, "taste": n,
  "hard_faults": ["..."], "caption_fix": "", "note": "one sentence an editor would write"}}"""


def press():
    spec = importlib.util.spec_from_file_location("image_press", SCRIPTS / "image-press.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def story_context(md_path, slot):
    """The text an image sits beside: the open for the cover, the lead story, or story N."""
    if not md_path or not os.path.exists(md_path):
        return ""
    body = open(md_path, encoding="utf-8").read().split("---", 2)[-1]
    secs = {m.group(1).strip(): m.group(2) for m in re.finditer(r"^## (.+?)\n(.*?)(?=^## |\Z)", body, re.M | re.S)}
    if slot == "cover":
        return (secs.get("The Open", "") + "\n" + secs.get("The Lead Story", ""))[:1800]
    if slot == "lead":
        return secs.get("The Lead Story", "")[:1800]
    n = int(slot.split("-")[1]) if slot.startswith("story-") else 0
    stories = re.split(r"^### ", secs.get("Also Shipped", ""), flags=re.M)[1:]
    return stories[n - 1][:1500] if 0 < n <= len(stories) else ""


FLOOD_QC = 0.25  # the press flags 18%; Eddie approved a 20% flood on 10/10, so QC rejects only past 25%


def hard_checks(entry):
    bad = []
    for f in entry.get("flags") or []:
        m = re.match(r"flooded: (\d+)%", f)
        if m and int(m.group(1)) / 100 <= FLOOD_QC:
            continue
        bad.append(f)
    if not entry.get("credit"):
        bad.append("no credit")
    if entry.get("license") == "generated" and "AI-generated" not in (entry.get("credit") or ""):
        bad.append("generated image not labeled AI-generated")
    return bad


def grade(printed, source, slot, caption, credit, story, model=MODEL, record=""):
    size = "full-width cover, about 1100px" if slot == "cover" else ("lead, column or full band" if slot == "lead" else "story column, about 330px")
    prompt = RUBRIC.format(printed=printed, source=source or printed, slot=slot, size=size,
                           caption=caption.replace('"', "'"), credit=credit, record=record.replace('"', "'") or "(none)", story=story.strip() or "(no story text)")
    r = subprocess.run(["claude", "-p", "--model", model, "--output-format", "json",
                        "--allowedTools", "Read", "--max-turns", "6"],
                       input=prompt, capture_output=True, text=True, timeout=600)
    if r.returncode:
        raise RuntimeError(f"claude -p failed: {(r.stderr or r.stdout)[:300]}")
    text = json.loads(r.stdout).get("result", "")
    m = re.search(r"\{[\s\S]*\}", text)
    if not m:
        raise RuntimeError(f"no JSON in grade: {text[:200]}")
    g = json.loads(m.group(0))
    for k in AXES:
        g[k] = int(g.get(k, 0))
    g["hard_faults"] = [f for f in g.get("hard_faults") or [] if f and f.strip()]
    g["caption_fix"] = (g.get("caption_fix") or "").strip()
    if g["caption_truth"] < 5 and not g["caption_fix"]:
        g["caption_truth"] = min(g["caption_truth"], 2)  # flagged but unfixed: never approve a caption QC doubts
    return g


def verdict(g, hard):
    faults = hard + g.get("hard_faults", [])
    low = [k for k in AXES if g.get(k, 0) < GATE[k]]
    ok = not faults and not low
    scores = " ".join(f"{k[:4]}={g.get(k, '-')}" for k in AXES)
    why = "; ".join(faults + [f"{k} {g[k]}/5" for k in low])
    return ok, f"{BY} [{scores}] {g.get('note', '')}" + ("" if ok else f" REJECT: {why}")


def record_for(images_dir, slot):
    p = Path(images_dir) / "src" / "credits.json"
    c = json.loads(p.read_text()).get(slot, {}) if p.exists() else {}
    return " ".join(x for x in (c.get("title"), c.get("url")) if x)


def source_for(images_dir, slot):
    src = Path(images_dir) / "src"
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        if (src / f"{slot}{ext}").exists():
            return str(src / f"{slot}{ext}")
    return None


def review(images_dir, context_md, dry=False, log=print):
    """Grade every pending image the front can draw; write the calls. Returns {file: (ok, note)}."""
    ip = press()
    out = str(images_dir)
    m = ip.load_manifest(out)
    slots = ip.load_slots(out) or {}
    results = {}
    for slot, meta in slots.items():
        options = [t for t in ("atkinson", "halftone") if f"{slot}-{t}.png" in m["images"]]
        graded, fixes = {}, {}
        for t in options:
            f = f"{slot}-{t}.png"
            e = m["images"][f]
            if e["review"]["status"] != "pending":
                continue
            hard = hard_checks(e)
            g = {k: 0 for k in AXES} if hard else grade(os.path.join(out, f), source_for(out, slot), slot,
                                                         meta.get("caption", ""), e.get("credit", ""),
                                                         story_context(context_md, slot), record=record_for(out, slot))
            graded[t] = verdict(g, hard) + (sum(g.get(k, 0) for k in AXES),)
            if g.get("caption_fix") and graded[t][0]:
                fixes[slot] = g["caption_fix"]
        if not graded:
            continue
        # The atkinson print is always drawn (small screens), so it must pass for the slot to run.
        passing = [t for t, (ok, _, _) in graded.items() if ok]
        if "halftone" in passing and slot in ip.HALFTONE_SLOTS and "atkinson" in passing:
            pick = "halftone" if graded["halftone"][2] >= graded["atkinson"][2] else "atkinson"
        else:
            pick = "atkinson"
        for t, (ok, note, _) in graded.items():
            f = f"{slot}-{t}.png"
            results[f] = (ok, note)
            log(f"  {'APPROVE' if ok else 'REJECT '} {f}: {note}")
            if not dry:
                ip.set_status(argparse.Namespace(out=out, file=f, by=BY, note=note), "approved" if ok else "rejected")
        if not dry and slot in ip.HALFTONE_SLOTS and "halftone" in graded:
            ip.set_pick(out, slot, pick)
        if not dry and slot in fixes:  # the editor corrects the caption rather than run a wrong one
            cur = ip.load_slots(out)
            cur[slot]["caption_was"] = cur[slot].get("caption", "")
            cur[slot]["caption"] = fixes[slot]
            json.dump(cur, open(os.path.join(out, "slots.json"), "w"), indent=2)
            log(f"  caption fixed for {slot}: {fixes[slot]}")
    return results


# ---------------------------------------------------------------- calibration

def decoys(tmp):
    """Images an editor must refuse: built from real renders so the grader cannot spot the trick by format."""
    from PIL import Image, ImageDraw, ImageFilter, ImageOps
    base = CONTENT / "articles" / "issue-10" / "images"
    good = Image.open(base / "story-1-atkinson.png").convert("RGB")
    w, h = good.size
    out = {}
    blank = Image.new("RGB", (w, h), (250, 248, 244))
    cap = "A row of empty voting booths with blue privacy curtains stands on the wooden floor of a school gymnasium."
    blank.save(tmp / "blank.png"); out["blank.png"] = ("blank page", cap)
    mush = good.filter(ImageFilter.GaussianBlur(18))
    mush.save(tmp / "mush.png"); out["mush.png"] = ("unreadable blur", cap)
    inv = ImageOps.invert(good)
    inv.save(tmp / "inverted.png"); out["inverted.png"] = ("inverted print", cap)
    sign = good.copy()
    d = ImageDraw.Draw(sign)
    d.rectangle([w * 0.1, h * 0.3, w * 0.9, h * 0.7], fill=(238, 92, 40))
    d.text((w * 0.15, h * 0.42), "BUY NOW  WWW.EXAMPLE.COM  BUY NOW", fill=(250, 248, 244))
    sign.save(tmp / "logo.png"); out["logo.png"] = ("dominant text banner", cap)
    good.save(tmp / "liar.png"); out["liar.png"] = ("false caption", "A crowd of voters queues outside the Philadelphia police headquarters at night.")
    import random
    rnd = random.Random(7)
    noise = Image.new("RGB", (w, h), (250, 248, 244))
    px = noise.load()
    for y in range(h):
        for x in range(w):
            if rnd.random() < 0.42:
                px[x, y] = (238, 92, 40)
    noise.save(tmp / "noise.png"); out["noise.png"] = ("pure dither noise", cap)
    return out


# Grader rejections of an Eddie approval that are the grader being RIGHT, verified by hand.
# Each names the evidence. Never add an entry to make a run pass on taste.
EXCUSED: dict[str, str] = {}


def cmd_calibrate(a):
    base = CONTENT / "articles" / "issue-10" / "images"
    ip = press()
    m = ip.load_manifest(str(base))
    slots = ip.load_slots(str(base)) or {}
    md = next(iter(sorted((CONTENT).glob("issue-10-*.md"))), None)
    rows, agree, total = [], 0, 0
    for f, e in sorted(m["images"].items()):
        if e["review"]["status"] != "approved" or e["review"].get("by") != "Eddie":
            continue
        slot = f.rsplit("-", 1)[0]
        g = grade(str(base / f), source_for(base, slot), slot, slots.get(slot, {}).get("caption", ""),
                  e.get("credit", ""), story_context(str(md) if md else None, slot), a.model, record_for(base, slot))
        ok, note = verdict(g, hard_checks(e))
        excused = EXCUSED.get(f) if not ok else None
        total += 1; agree += ok or bool(excused)
        rows.append(("EDDIE APPROVED", f, "agree" if ok else ("EXCUSED" if excused else "DISAGREE"),
                     note + (f" || excused: {excused}" if excused else "")))
    tmp = Path(tempfile.mkdtemp(prefix="qc-decoys-"))
    try:
        for f, (why, caption) in decoys(tmp).items():
            g = grade(str(tmp / f), str(base / "src" / "story-1.jpg"), "story-1", caption,
                      "Illustration, AI-generated (OpenAI gpt-image-2)", story_context(str(md) if md else None, "story-1"),
                      a.model, record_for(base, "story-1"))
            ok, note = verdict(g, [])
            total += 1; agree += (not ok)
            rows.append((f"DECOY ({why})", f, "agree" if not ok else "DISAGREE", note))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    for r in rows:
        print(f"{r[2]:9} {r[0]:28} {r[1]:24} {r[3][:150]}")
    print(f"\ncalibration ({a.model}): {agree}/{total} agree with Eddie's bar")
    report = {"model": a.model, "agree": agree, "total": total, "rows": rows}
    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / "image-qc-calibration.json").write_text(json.dumps(report, indent=1))
    sys.exit(0 if agree == total else 1)


def cmd_review(a):
    res = review(a.images, a.context, a.dry_run)
    print(f"{sum(ok for ok, _ in res.values())} approved, {sum(not ok for ok, _ in res.values())} rejected")


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    r = sp.add_parser("review")
    r.add_argument("images"); r.add_argument("--context"); r.add_argument("--dry-run", action="store_true")
    c = sp.add_parser("calibrate")
    c.add_argument("--model", default=MODEL)
    a = ap.parse_args()
    {"review": cmd_review, "calibrate": cmd_calibrate}[a.cmd](a)


if __name__ == "__main__":
    main()
