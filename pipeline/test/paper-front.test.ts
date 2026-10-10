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

test('classic issues keep the classic cover and leak no front markers', async () => {
  const html = await renderTo(ISSUE_09);
  assert.match(html, /<section class="cover" id="top">/);
  assert.doesNotMatch(html, /front:classic/);
  assert.doesNotMatch(html, /class="pf"/);
});

test('layout: paper swaps in the newspaper front with wordmark, signature and folded headline', async () => {
  const dir = mkdtempSync(join(tmpdir(), 'shipped-paper-md-'));
  const md = join(dir, 'issue-99-paper-test.md');  // issue 99 has no images folder: text-only front
  writeFileSync(md, readFileSync(ISSUE_09, 'utf-8').replace(/^status: (.*)$/m, 'status: $1\nlayout: paper'));
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
