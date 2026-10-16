import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, writeFileSync, readFileSync, rmSync, mkdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { renderIssue } from '../src/render/index.js';
import { loadSlotImages } from '../src/render/paper-front.js';

const CONTENT = resolve(dirname(fileURLToPath(import.meta.url)), '..', '..', 'content');
const ISSUE_09 = join(CONTENT, 'issue-09-the-public-frontier.md');

async function renderTo(md: string): Promise<string> {
  const dir = mkdtempSync(join(tmpdir(), 'shipped-paper-'));
  const scratchPath = join(dir, 'out.html');
  await renderIssue(md, { dryRun: true, scratchPath });
  const html = readFileSync(scratchPath, 'utf-8');
  rmSync(dir, { recursive: true, force: true });
  return html;
}

// The issue files carry their own layout (every issue moved to the paper, 2026-10-15); the tests pin it.
const ISSUE_09_SRC = () => readFileSync(ISSUE_09, 'utf-8').replace(/^layout: .*\n/m, '');

test('classic issues keep the classic cover and leak no front markers', async () => {
  const dir = mkdtempSync(join(tmpdir(), 'shipped-classic-md-'));
  const md = join(dir, 'issue-09-the-public-frontier.md');
  writeFileSync(md, ISSUE_09_SRC());
  const html = await renderTo(md);
  rmSync(dir, { recursive: true, force: true });
  assert.match(html, /<section class="cover" id="top">/);
  assert.doesNotMatch(html, /front:classic/);
  assert.doesNotMatch(html, /class="pf"/);
});

test('layout: paper swaps in the newspaper front with wordmark, signature and folded headline', async () => {
  const dir = mkdtempSync(join(tmpdir(), 'shipped-paper-md-'));
  const md = join(dir, 'issue-99-paper-test.md');  // issue 99 has no images folder: text-only front
  writeFileSync(md, ISSUE_09_SRC().replace(/^status: (.*)$/m, 'status: $1\nlayout: paper'));
  try {
    const html = await renderTo(md);
    assert.match(html, /<section class="pf" id="top">/);
    assert.doesNotMatch(html, /<section class="cover" id="top">/);
    assert.doesNotMatch(html, /front:classic/);
    assert.match(html, /class="pf-mark"/);           // locked wordmark, not live text
    assert.match(html, /class="pf-sig"/);            // "from id8" rebrand signature
    assert.match(html, /<header class="pf-head">/);  // one folded headline under the cover
    assert.equal((html.match(/id="also"/g) ?? []).length, 1);        // full Also Shipped once, below the front
    assert.match(html, /id="front-also"/);                            // front carries the excerpts
    assert.match(html, /class="pf-jump/);                             // and jumps to the full stories
  } finally { rmSync(dir, { recursive: true, force: true }); }
});

test('loadSlotImages marks an image approved only when every file for the slot is approved', () => {
  const dir = mkdtempSync(join(tmpdir(), 'shipped-slots-'));
  try {
    mkdirSync(dir, { recursive: true });
    for (const f of ['cover-atkinson.png', 'cover-halftone.png', 'lead-atkinson.png']) writeFileSync(join(dir, f), '');
    writeFileSync(join(dir, 'slots.json'), JSON.stringify({ cover: { caption: 'c', alt: 'a' }, lead: { caption: 'l', alt: 'a' } }));
    writeFileSync(join(dir, 'manifest.json'), JSON.stringify({ images: {
      'cover-atkinson.png': { credit: 'Public domain', review: { status: 'approved' } },
      'cover-halftone.png': { credit: 'Public domain', review: { status: 'pending' } },
      'lead-atkinson.png': { credit: 'Illustration, AI-generated', review: { status: 'approved' } },
    } }));
    const imgs = loadSlotImages(dir);
    assert.equal(imgs.cover?.approved, false);
    assert.equal(imgs.cover?.halftone, 'cover-halftone.png');
    assert.equal(imgs.lead?.approved, true);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});

test('excerpt keeps whole paragraphs under budget and cuts a long first paragraph at a sentence', async () => {
  const { excerpt } = await import('../src/render/paper-front.js');
  const a = excerpt('one two three.\n\nfour five six.\n\nseven eight nine ten.', 6);
  assert.equal(a.text, 'one two three.\n\nfour five six.'); assert.equal(a.cut, true);
  const b = excerpt('First sentence here. Second sentence is longer than budget allows.', 4);
  assert.equal(b.text, 'First sentence here.'); assert.equal(b.cut, true);
  assert.equal(excerpt('short.', 10).cut, false);
});

test('the Brief states only computed facts (no hard-coded April figures)', async () => {
  const html = await renderTo(ISSUE_09);
  assert.doesNotMatch(html, /Consortium|12 orgs|Apr 2026<\/span>|<b>Days<\/b> 21<|<b>Releases<\/b> 56</);
  assert.match(html, /<b>Releases<\/b> \d+/);
  const { periodDays } = await import('../src/render/sections/open.js');
  assert.equal(periodDays('2026-06-13 to 2026-06-16'), 4);
  assert.equal(periodDays('nonsense'), null);
});

test('insideFigures repeats each story photo above its full story and keeps the drop cap on the text', async () => {
  const { insideFigures } = await import('../src/render/paper-front.js');
  const img = (file: string, caption: string) => ({ file, caption, credit: 'Public domain', alt: caption, approved: true, treatment: 'atkinson' as const });
  const html = [
    '<div class="feature-opener">Lead</div><div class="prose-well"><div class="prose drop-cap drop-cap-orange"><p>First lead paragraph.</p></div></div>',
    '<span class="section-folio-sub">Also shipped</span><div class="prose">',
    '<h3 style="font-family:var(--disp);x">One.</h3><p>a</p><h3 style="font-family:var(--disp);x">Two.</h3><p>b</p>',
    '<h3 style="font-family:var(--disp);x">Three.</h3><p>c</p></div>',
  ].join('');
  const out = insideFigures(html, { lead: img('lead-atkinson.png', 'Lead pic'), 'story-1': img('story-1-atkinson.png', 'One pic'), 'story-2': img('story-2-atkinson.png', 'Two pic') });
  assert.match(out, /<div class="prose"><figure class="pf-fig pf-jumpfig"><img src="img\/lead-atkinson.png"/);
  assert.match(out, /<p class="drop-cap drop-cap-orange">First lead paragraph/);
  assert.ok(out.indexOf('story-1-atkinson') < out.indexOf('>One.</h3>'));
  assert.ok(out.indexOf('>One.</h3>') < out.indexOf('story-2-atkinson') && out.indexOf('story-2-atkinson') < out.indexOf('>Two.</h3>'));
  assert.equal((out.match(/pf-jumpfig/g) ?? []).length, 3, 'no photo for a story without one');
  assert.equal(insideFigures(html, {}), html, 'no images, no change');
  const gap = insideFigures(html, { 'story-3': img('story-3-atkinson.png', 'Three pic') });
  assert.ok(gap.indexOf('story-3-atkinson') > gap.indexOf('>Two.</h3>') && gap.indexOf('story-3-atkinson') < gap.indexOf('>Three.</h3>'), 'a missing story-1 photo does not stop story-3');
});
