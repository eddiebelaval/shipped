import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync, rmSync, mkdirSync, copyFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';
import { editionize, PAPER_MARKER } from '../src/render/edition-cli.js';

const PIPELINE = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const EM = String.fromCharCode(0x2014);
const DASH = new RegExp(`[${EM}${String.fromCharCode(0x2013)}]`);

const META = {
  section: 'anthropic-daily', stem: '2026-10-10', issueNum: '90',
  title: 'Shipped. Daily, Saturday, October 10, 2026', deck: 'A "quoted" deck', period: 'Oct 09 to Oct 10',
};

test('editionize swaps the magazine identity for the edition', () => {
  const page = [
    `<title>Shipped. ${EM} Issue 90 ${EM} x</title>`,
    '<meta property="og:url" content="https://id8labs.app/shipped/90/">',
    '<meta property="og:image" content="https://id8labs.app/shipped/90/og.png">',
    '<meta name="description" content="A weekly magazine on what Anthropic ships.">',
    '<span class="pub-bar-meta">A weekly magazine by <a href="https://id8labs.app">id8Labs</a></span>',
    '<span class="pub-bar-folio">Issue <b>90</b></span>',
    '<span class="folio">Shipped. <span class="dot">·</span> 90 <span class="dot">·</span> Oct 2026</span>',
    '<div>Next issue, Oct 17, 2026</div>',
    "body: JSON.stringify({ source: 'shipped-magazine-issue-90' })",
    '<img class="shipped-mark" src="/brand/shipped-wordmark.svg">',
  ].join('\n');
  const out = editionize(page, META);
  assert.match(out, /<title>Shipped\. Daily, Saturday, October 10, 2026<\/title>/);
  assert.ok(out.includes(PAPER_MARKER));
  assert.ok(out.includes('https://eddiebelaval.github.io/shipped/anthropic-daily/2026-10-10.html'));
  assert.ok(!out.includes('og:image'));
  assert.ok(out.includes('content="A &quot;quoted&quot; deck"'));
  assert.ok(out.includes('Daily edition by'));
  assert.ok(out.includes('Oct 09 to Oct 10'));
  assert.ok(out.includes('<span class="dot">·</span> Daily <span class="dot">·</span>'));
  assert.ok(out.includes('New every night at 9 PM ET'));
  assert.ok(out.includes("source: 'shipped-daily'"));
  assert.match(out, /src="data:image\/svg\+xml;base64,/);
  assert.doesNotMatch(out, /Issue|\b90\b|\/brand\/|weekly magazine/);
  assert.doesNotMatch(out, DASH);
});

test('editionize refuses an unknown section', () => {
  assert.throws(() => editionize('', { ...META, section: 'anthropic-hourly' }), /unknown edition section/);
});

test('a routine page converts and renders into a paper edition the desk gate passes', () => {
  const dir = mkdtempSync(join(tmpdir(), 'shipped-edition-'));
  try {
    const ed = join(dir, 'anthropic-daily', '2026-10-10');
    mkdirSync(ed, { recursive: true });
    copyFileSync(join(PIPELINE, 'test', 'fixtures', 'routine-daily.html'), join(ed, 'source.html'));
    execFileSync('python3', [join(PIPELINE, 'scripts', 'edition-to-paper.py'), join(ed, 'source.html'), join(ed, 'edition.md'),
      '--section', 'anthropic-daily', '--stem', '2026-10-10']);
    const out = join(dir, 'out.html');
    execFileSync('npx', ['tsx', 'src/render/edition-cli.ts', join(ed, 'edition.md'), out, '--approved-only'], { cwd: PIPELINE });
    const html = readFileSync(out, 'utf-8');
    assert.ok(html.includes(PAPER_MARKER));
    assert.match(html, /class="pf-/, 'paper front present');
    assert.ok(html.includes('The Paper Trail'));
    assert.ok(html.includes('The Small Model Argument'));
    assert.ok(html.includes('Claude Haiku 5.5'), 'release log entry carried over');
    assert.equal(html.split('id="subscribe"').length - 1, 1);
    assert.doesNotMatch(html, DASH);
    const gate = execFileSync('python3', ['-c', [
      'import importlib.util,json',
      `s=importlib.util.spec_from_file_location("d","${join(PIPELINE, 'scripts', 'edition-desk.py')}")`,
      'd=importlib.util.module_from_spec(s);s.loader.exec_module(d)',
      `print(json.dumps(d.parity_gate(open("${join(ed, 'edition.md')}").read(), open("${out}").read())))`,
    ].join(';')]).toString();
    assert.deepEqual(JSON.parse(gate), []);
    // ...and catches a page that dropped a paragraph.
    const cut = html.replace(/The mechanism\. The report describes four behavior types\./g, '');
    const gate2 = execFileSync('python3', ['-c', [
      'import importlib.util,json,sys',
      `s=importlib.util.spec_from_file_location("d","${join(PIPELINE, 'scripts', 'edition-desk.py')}")`,
      'd=importlib.util.module_from_spec(s);s.loader.exec_module(d)',
      `print(json.dumps(d.parity_gate(open("${join(ed, 'edition.md')}").read(), sys.stdin.read())))`,
    ].join(';')], { input: cut }).toString();
    assert.ok(JSON.parse(gate2).some((p: string) => p.startsWith('text missing')));
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});
