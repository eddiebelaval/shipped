/**
 * Shipped. newspaper front page (DESIGN.md Revision 6, ratified 2026-10-10).
 *
 * Issues opt in with `layout: paper` in frontmatter; every earlier issue keeps
 * the classic cover, so published issues never change. The front is a
 * broadsheet: nameplate (the locked wordmark), a full-width riso halftone
 * cover photo, the lead headline folded directly beneath it, then three ruled
 * columns (lead story, Also Shipped, a rail with the log, the numbers and the
 * term of the issue).
 *
 * Images come from the image desk (pipeline/scripts/image-desk.py):
 * content/articles/issue-NN/images/{slots.json, manifest.json, *.png}.
 * Slots: cover, lead, story-1..N. A missing image leaves its slot text-only.
 * An image not yet approved renders with a PENDING REVIEW stamp; the publish
 * gate (image-gate.ts) blocks staging until every image is approved.
 */

import { existsSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { esc, inlineMarkdown, paragraphs, fmtPrettyDate } from './markdown.js';
import type { ParsedIssue, Section, TermOfIssue } from './types.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const WORDMARK = path.resolve(__dirname, '../../assets/shipped-wordmark.svg');
// Rebrand Phase 3 signature: "from" + the id8 instrument-family wordmark, dot inked (one orange per masthead).
const SIGNATURE = path.resolve(__dirname, '../../assets/id8-wordmark-short-ink.svg');

export interface SlotImage {
  file: string;            // e.g. "lead-atkinson.png"
  halftone?: string;       // cover only
  caption: string;
  credit: string;
  alt: string;
  approved: boolean;
  treatment: 'atkinson' | 'halftone';
}

export type SlotImages = Record<string, SlotImage>;

interface ManifestEntry { credit?: string | null; review?: { status?: string } }

/** Read the desk's slots + the press manifest into renderable slot images. */
export function loadSlotImages(imagesDir: string | null): SlotImages {
  if (!imagesDir) return {};
  const slotsPath = path.join(imagesDir, 'slots.json');
  const manPath = path.join(imagesDir, 'manifest.json');
  if (!existsSync(slotsPath) || !existsSync(manPath)) return {};
  const slots = JSON.parse(readFileSync(slotsPath, 'utf-8')) as Record<string, { caption?: string; alt?: string; treatment?: string }>;
  const man = (JSON.parse(readFileSync(manPath, 'utf-8')) as { images: Record<string, ManifestEntry> }).images;
  const out: SlotImages = {};
  for (const [slot, meta] of Object.entries(slots)) {
    const file = `${slot}-atkinson.png`;
    const entry = man[file];
    if (!entry || !existsSync(path.join(imagesDir, file))) continue;
    // Eddie picks the treatment per slot at the image desk; cover defaults to halftone.
    const treatment = (meta.treatment ?? (slot === 'cover' ? 'halftone' : 'atkinson')) === 'halftone' ? 'halftone' : 'atkinson';
    const halftone = treatment === 'halftone' && man[`${slot}-halftone.png`] ? `${slot}-halftone.png` : undefined;
    const files = [file, halftone].filter(Boolean) as string[];
    out[slot] = {
      file,
      halftone,
      caption: meta.caption ?? '',
      credit: entry.credit ?? '',
      alt: meta.alt ?? '',
      approved: files.every((f) => man[f]?.review?.status === 'approved'),
      treatment: halftone ? 'halftone' : 'atkinson',
    };
  }
  return out;
}

/** The locked wordmark as inline SVG (same extraction as backfill-wordmark.py). */
function wordmark(): string {
  const src = readFileSync(WORDMARK, 'utf-8');
  const vb = src.match(/viewBox="([^"]+)"/)?.[1] ?? '0 0 776 259';
  const g = src.match(/<g transform="([^"]+)">/)?.[1] ?? '';
  const ink = src.match(/<path class="ink" d="([^"]+)"/)?.[1] ?? '';
  const dot = src.match(/<path class="accent" d="([^"]+)"/)?.[1] ?? '';
  return `<svg class="pf-mark" viewBox="${vb}" role="img" aria-label="Shipped."><g transform="${g}"><path fill="currentColor" d="${ink}"/><path fill="#ff6b35" d="${dot}"/></g></svg>`;
}

function signature(): string {
  const b64 = readFileSync(SIGNATURE).toString('base64');
  return `<span class="pf-sig"><span class="pf-from">from</span><img src="data:image/svg+xml;base64,${b64}" alt="id8" width="71" height="58"></span>`;
}

function figure(img: SlotImage | undefined, cls = ''): string {
  if (!img) return '';
  const stamp = img.approved ? '' : '<span class="pf-pending">Pending review</span>';
  const caption = `<figcaption class="pf-cap">${esc(img.caption)} <i>${esc(img.credit)}.</i></figcaption>`;
  const media = img.halftone
    ? `<picture><source media="(min-width: 760px)" srcset="img/${img.halftone}"><img src="img/${img.file}" alt="${esc(img.alt)}"></picture>`
    : `<img src="img/${img.file}" alt="${esc(img.alt)}" loading="lazy">`;
  return `<figure class="pf-fig ${cls}">${stamp}${media}${caption}</figure>`;
}

function headlineOf(section: Section | undefined, fallback: string): string {
  const h = section?.content.split('\n').find((l) => l.startsWith('# '));
  return h ? h.slice(2).trim() : fallback;
}

function bodyOf(section: Section): string {
  return section.content.split('\n').filter((l) => !l.startsWith('# ')).join('\n');
}

/**
 * Front-page excerpt: whole paragraphs up to a word budget; a single long
 * paragraph is cut at a sentence end. The full story runs below the front
 * (the jump), so columns end level instead of one running the page.
 */
export function excerpt(body: string, budget: number): { text: string; cut: boolean } {
  const paras = body.replace(/\r\n/g, '\n').split(/\n{2,}/).map((p) => p.trim())
    .filter((p) => p && !/^-{3,}$/.test(p) && !p.startsWith('>') && !p.startsWith('|'));
  const out: string[] = []; let words = 0;
  for (const p of paras) {
    const n = p.split(/\s+/).length;
    if (words + n <= budget) { out.push(p); words += n; continue; }
    if (out.length === 0) {
      const sentences = p.match(/[^.!?]+[.!?]+["')\]]*\s*/g) ?? [p];
      let acc = '';
      for (const sn of sentences) {
        if (acc && (acc + sn).split(/\s+/).length > budget) break;
        acc += sn;
      }
      out.push(acc.trim());
    }
    return { text: out.join('\n\n'), cut: true };
  }
  return { text: out.join('\n\n'), cut: false };
}

const LEAD_WORDS = 230;
const STORY_WORDS = 60;
const FRONT_STORIES = 3;
const FULL_ANCHOR: Record<string, string> = { investigation: '#investigation', lead_story: '#lead', feature: '#feature' };

function stories(section: Section | undefined): Array<{ title: string; body: string }> {
  if (!section) return [];
  return section.content.split(/^### /m).slice(1).map((chunk) => {
    const nl = chunk.indexOf('\n');
    return { title: chunk.slice(0, nl).trim(), body: chunk.slice(nl + 1).trim() };
  });
}

function termRail(term: Section | undefined): string {
  if (!term) return '';
  const d = term.data as TermOfIssue | undefined;
  const word = d?.word ?? headlineOf(term, 'Term of the Issue');
  const def = d?.definition?.[0] ?? '';
  const firstSentences = def.split(/(?<=\.)\s+/).slice(0, 2).join(' ');
  return `<div class="pf-term"><div class="pf-sect">Term of the Issue</div>
    <div class="pf-hw">${esc(word)}</div>
    ${d?.pronunciation ? `<div class="pf-ipa">${esc(d.pronunciation)} ${esc(d.partOfSpeech ?? '')}</div>` : ''}
    <p class="pf-sm">${inlineMarkdown(firstSentences)}</p>
    <a class="pf-more" href="#term">Full entry</a></div>`;
}

export function renderPaperFront(issue: ParsedIssue, issueNum: string, images: SlotImages): string {
  const fm = issue.frontmatter;
  const find = (k: string) => issue.sections.find((s) => s.kind === k);
  const lead = find('investigation') ?? find('lead_story') ?? find('feature');
  const also = find('also_shipped');
  const term = find('term_of_issue');
  const close = find('close');
  const quiet = find('quiet_on_wire');

  const log = issue.releaseLog.flatMap((c) => c.entries)
    .sort((a, b) => b.date.localeCompare(a.date)).slice(0, 6);
  const logCount = issue.releaseLog.reduce((s, c) => s + c.entries.length, 0);
  const weather = fm.weather
    ?? close?.content.split('\n').map((l) => l.trim()).find((l) => l && !/^-{3,}$/.test(l)) ?? '';
  const cells = (fm.by_the_numbers?.cells ?? []).slice(0, 4);
  // A lead picked as halftone runs as a full-width band (halftone needs 700px+).
  const leadBand = images.lead?.treatment === 'halftone';

  const all = stories(also);
  const storyHtml = all.slice(0, FRONT_STORIES).map((st, i) => {
    const ex = excerpt(st.body, STORY_WORDS);
    return `
      <div class="pf-story">
        ${figure(images[`story-${i + 1}`])}
        <h3>${inlineMarkdown(st.title)}</h3>
        <div class="pf-sm">${paragraphs(ex.text)}</div>
        ${ex.cut ? '<a class="pf-jump" href="#also">Continued inside</a>' : ''}
      </div>`;
  }).join('') + (all.length > FRONT_STORIES ? `
      <div class="pf-inside"><span class="pf-kick">Also inside</span>
        ${all.slice(FRONT_STORIES).map((st) => `<a href="#also">${inlineMarkdown(st.title)}</a>`).join('')}
      </div>` : '');
  const leadEx = lead ? excerpt(bodyOf(lead), LEAD_WORDS) : { text: '', cut: false };
  const leadAnchor = lead ? FULL_ANCHOR[lead.kind] ?? '#top' : '#top';

  return `<style>
.pf{max-width:1320px;margin:0 auto;padding:22px 28px 40px;font-family:var(--disp);color:var(--ink)}
.pf img{display:block;width:100%;height:auto;image-rendering:pixelated}
.pf-ears{display:flex;justify-content:space-between;gap:20px;font-family:var(--narrow);font-size:13px;letter-spacing:.06em;padding-bottom:10px;border-bottom:1px solid var(--ink)}
.pf-motto{text-align:center;font-family:var(--narrow);font-size:12px;letter-spacing:.42em;text-transform:uppercase;margin:16px 0 0;color:var(--muted)}
.pf-flag{display:flex;justify-content:center;align-items:flex-end;gap:18px;margin:14px 0 0}
.pf-sig{display:flex;align-items:flex-end;gap:10px;padding-bottom:.6%}
.pf-from{font-family:var(--narrow);font-weight:600;font-size:11px;letter-spacing:.24em;text-transform:uppercase;color:var(--muted);padding-bottom:8px}
.pf .pf-sig img{height:clamp(32px,4vw,56px);width:auto;image-rendering:auto}
.pf-mark{height:clamp(64px,11vw,150px);width:auto;overflow:visible}
.pf-weather{margin:18px 0 12px;text-align:center;font-style:italic;font-size:17px;color:var(--body)}
.pf-nav{border-top:4px double var(--ink);border-bottom:1px solid var(--ink);display:flex;justify-content:center;flex-wrap:wrap;gap:6px 32px;padding:10px 0;font-family:var(--narrow);font-weight:700;font-size:13px;letter-spacing:.2em;text-transform:uppercase}
.pf-nav a{color:inherit;text-decoration:none}.pf-nav a:first-child{color:var(--orange)}
.pf-fig{position:relative;margin:0}
.pf-fig img{border:1px solid var(--ink)}
.pf-cover{margin-top:22px}.pf-band{margin:22px 0 4px}.pf-cover img{border:3px solid var(--ink);max-height:560px;object-fit:cover}
.pf-cap{font-family:var(--narrow);font-size:12px;color:var(--muted);margin-top:6px;letter-spacing:.02em}
.pf-cap i{font-family:var(--disp)}
.pf-pending{position:absolute;top:10px;left:10px;z-index:2;background:var(--ink);color:var(--paper);font-family:var(--narrow);font-weight:700;font-size:11px;letter-spacing:.2em;text-transform:uppercase;padding:5px 9px}
.pf-head{padding:14px 0 18px;border-bottom:4px double var(--ink)}
.pf-kick{font-family:var(--narrow);font-weight:700;font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--orange)}
.pf-head h2{font-weight:800;font-size:clamp(38px,5vw,68px);line-height:.98;letter-spacing:-.025em;margin:8px 0 10px;max-width:1100px}
.pf-deck{font-style:italic;font-size:clamp(19px,1.8vw,23px);line-height:1.38;color:var(--body);max-width:900px}
.pf-byl{font-family:var(--narrow);font-size:13px;color:var(--muted);margin-top:10px}
.pf-grid{display:grid;grid-template-columns:1.55fr 1fr .9fr;margin-top:26px}
.pf-grid>*{padding:0 24px;min-width:0}.pf-grid>*:first-child{padding-left:0}.pf-grid>*:last-child{padding-right:0}
.pf-grid>*+*{border-left:1px solid rgba(11,11,11,.55)}
.pf-body{font-size:18px;line-height:1.58;color:var(--body);margin-top:16px}
.pf-body p+p{margin-top:12px}
.pf-body p:first-child::first-letter{float:left;font-weight:900;font-size:5.1em;line-height:.8;padding:6px 10px 0 0;color:var(--orange)}
.pf-sect{display:flex;justify-content:space-between;align-items:baseline;border-top:3px double var(--ink);border-bottom:1px solid var(--ink);padding:8px 0;margin-bottom:14px;font-family:var(--narrow);font-weight:700;font-size:13px;letter-spacing:.24em;text-transform:uppercase}
.pf-story h3{font-weight:700;font-size:23px;line-height:1.1;margin:12px 0 8px}
.pf-story+.pf-story{border-top:1px solid rgba(11,11,11,.14);margin-top:20px;padding-top:18px}
.pf-grid .pf-fig img{aspect-ratio:3/2;object-fit:cover}
/* Level columns: the lead column sets the row height; the middle and rail fill
   exactly that height (height:0 + min-height:100% takes the row's height without
   adding to it) and fade out behind a jump link. No column runs the page. */
.pf-fill{height:0;min-height:100%;overflow:hidden;position:relative}
.pf-fill::after{content:"";position:absolute;left:0;right:0;bottom:0;height:110px;background:linear-gradient(rgba(250,248,244,0),var(--paper) 70%);pointer-events:none}
.pf-pin{position:absolute;bottom:0;z-index:2;font-family:var(--narrow);font-weight:700;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--orange);text-decoration:none;border-bottom:1px solid currentColor}
.pf-fill.pf-fits::after,.pf-fill.pf-fits .pf-pin{display:none}
.pf-quiet{margin-top:22px}
.pf-jump{display:inline-block;margin-top:8px;font-family:var(--narrow);font-weight:700;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--orange);text-decoration:none;border-bottom:1px solid currentColor}
.pf-jump-lead{margin-top:14px}
.pf-inside{border-top:3px double var(--ink);margin-top:20px;padding-top:12px;display:flex;flex-direction:column;gap:8px}
.pf-inside a{font-weight:700;font-size:17px;line-height:1.2;color:var(--ink);text-decoration:none}
.pf-sm{font-size:16px;line-height:1.5;color:var(--body)}.pf-sm p+p{margin-top:10px}
.pf-box{border:2px solid var(--ink);background:#fffdf8;padding:16px 18px}
.pf-row{font-size:15px;line-height:1.4;padding:9px 0;border-bottom:1px dotted rgba(11,11,11,.55)}.pf-row:last-of-type{border-bottom:0}
.pf-tag{font-family:var(--mono);font-size:11px;color:var(--orange)}
.pf-more{font-family:var(--narrow);font-weight:700;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--ink);display:inline-block;margin-top:10px}
.pf-nums{margin-top:22px}.pf-num{display:grid;grid-template-columns:84px 1fr;align-items:baseline;border-top:1px solid rgba(11,11,11,.14);padding:8px 0}
.pf-num b{font-family:var(--narrow);font-size:28px;color:var(--orange);line-height:1}.pf-num span{font-family:var(--narrow);font-size:13px;line-height:1.35}
.pf-term{margin-top:22px}.pf-hw{font-style:italic;font-weight:700;font-size:30px}.pf-ipa{font-family:var(--mono);font-size:12px;color:var(--muted);margin-bottom:8px}
@media (max-width:980px){.pf-grid{grid-template-columns:1fr}.pf-grid>*{padding:0;border-left:0 !important;margin-bottom:28px}
  .pf-fill{height:auto;min-height:0;overflow:visible}.pf-fill::after,.pf-pin{display:none}.pf-quiet{display:none}}
@media (max-width:560px){.pf{padding-left:16px;padding-right:16px}.pf-ears{flex-direction:column;align-items:center;gap:4px}}
</style>
<section class="pf" id="top">
  <div class="pf-ears"><span>${esc(fm.issue_label ?? `Vol. I · No. ${issueNum}`)}</span><span>${fmtPrettyDate(fm.date)} · ${esc(fm.edition ?? 'Weekly Edition')}</span><span>${logCount} releases in the log · Anthropic first</span></div>
  <p class="pf-motto">All the frontier that ships</p>
  <div class="pf-flag">${wordmark()}${signature()}</div>
  ${weather ? `<p class="pf-weather">${inlineMarkdown(weather)}</p>` : ''}
  <nav class="pf-nav"><a href="#top">Front Page</a><a href="${leadAnchor}">Lead</a><a href="#also">Also Shipped</a>${term ? '<a href="#term">Term</a>' : ''}<a href="#log">The Log</a></nav>

  ${figure(images.cover, 'pf-cover')}

  <header class="pf-head">
    <span class="pf-kick">${lead && !/lead story/i.test(lead.name) ? `${esc(lead.name)} · ` : ''}Lead Story</span>
    <h2>${inlineMarkdown(headlineOf(lead, fm.title))}</h2>
    ${fm.deck ? `<p class="pf-deck">${inlineMarkdown(fm.deck)}</p>` : ''}
    ${fm.byline ? `<p class="pf-byl">${esc(fm.byline)}</p>` : ''}
  </header>

  ${leadBand ? figure(images.lead, 'pf-cover pf-band') : ''}
  <div class="pf-grid">
    <article id="front-lead">
      ${leadBand ? '' : figure(images.lead)}
      <div class="pf-body">${paragraphs(leadEx.text)}</div>
      ${leadEx.cut ? `<a class="pf-jump pf-jump-lead" href="${leadAnchor}">Continued inside</a>` : ''}
    </article>
    <div id="front-also" class="pf-fill">
      <div class="pf-sect">Also Shipped</div>
      ${storyHtml}
      <a class="pf-pin" href="#also">Continued inside</a>
    </div>
    <aside class="pf-fill">
      <div class="pf-box">
        <span class="pf-kick">The Log · In Window</span>
        ${log.map((e) => `<div class="pf-row"><b>${esc(e.date.slice(5))}</b> ${inlineMarkdown(e.title)} <span class="pf-tag">${esc(e.category)}</span></div>`).join('')}
        <a class="pf-more" href="#log">All ${logCount} entries</a>
      </div>
      ${cells.length ? `<div class="pf-nums"><div class="pf-sect">By the Numbers</div>${cells.map((c) => `<div class="pf-num"><b>${esc(c.value)}</b><span>${esc(c.label)}</span></div>`).join('')}</div>` : ''}
      ${termRail(term)}
      ${quiet ? `<div class="pf-quiet"><div class="pf-sect">Quiet on the Wire</div><div class="pf-sm">${paragraphs(quiet.content)}</div></div>` : ''}
      ${close ? `<div class="pf-quiet"><div class="pf-sect">The Close</div><div class="pf-sm"><em>${paragraphs(close.content)}</em></div></div>` : ''}
      <a class="pf-pin" href="#log">More inside</a>
    </aside>
  </div>
</section>
<script>(function(){function f(){document.querySelectorAll('.pf-fill').forEach(function(c){c.classList.toggle('pf-fits',c.scrollHeight<=c.clientHeight+2)})}window.addEventListener('load',f);window.addEventListener('resize',f)})();</script>`;
}
