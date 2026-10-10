import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, writeFileSync, rmSync, readFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve, dirname } from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { issueImageDir } from '../src/orchestrate/image-gate.js';

const PRESS = resolve(dirname(fileURLToPath(import.meta.url)), '..', 'scripts', 'image-press.py');

function scratch() {
  const root = mkdtempSync(join(tmpdir(), 'shipped-imggate-'));
  const dir = join(root, 'articles', 'issue-07', 'images');
  mkdirSync(dir, { recursive: true });
  return { root, dir };
}

function manifest(dir: string, review: string, credit: string | null, treatment = 'atkinson', width = 1200) {
  writeFileSync(join(dir, 'manifest.json'), JSON.stringify({
    images: { 'a.png': { treatment, width, credit, review: { status: review } } },
  }));
}

function gate(dir: string): number {
  try { execFileSync('python3', [PRESS, 'check', dir], { stdio: 'pipe' }); return 0; }
  catch (e) { return (e as { status: number }).status; }
}

test('issueImageDir finds the manifest for an issue file, null otherwise', () => {
  const { root, dir } = scratch();
  try {
    assert.equal(issueImageDir('/x/issue-07-the-gate.md', root), null);
    manifest(dir, 'pending', 'PD');
    assert.equal(issueImageDir('/x/issue-07-the-gate.md', root), dir);
    assert.equal(issueImageDir('/x/issue-7-the-gate.md', root), dir);
    assert.equal(issueImageDir('/x/daily-2026-10-10.md', root), null);
  } finally { rmSync(root, { recursive: true, force: true }); }
});

test('image gate blocks pending, rejected, uncredited and small halftone; clears approved', () => {
  const { root, dir } = scratch();
  try {
    manifest(dir, 'pending', 'PD'); assert.equal(gate(dir), 1);
    manifest(dir, 'rejected', 'PD'); assert.equal(gate(dir), 1);
    manifest(dir, 'approved', null); assert.equal(gate(dir), 1);
    manifest(dir, 'approved', 'PD', 'halftone', 600); assert.equal(gate(dir), 1);
    manifest(dir, 'approved', 'Carl Lender, CC BY 2.0'); assert.equal(gate(dir), 0);
  } finally { rmSync(root, { recursive: true, force: true }); }
});

test('review desk page script parses (a stray newline once broke it silently)', () => {
  const src = readFileSync(PRESS, 'utf-8');
  const html = src.slice(src.indexOf('DESK_HTML = r"""') + 16, src.indexOf('</html>"""') + 7);
  const js = html.slice(html.indexOf('<script>') + 8, html.indexOf('</script>'));
  const dir = mkdtempSync(join(tmpdir(), 'shipped-deskjs-'));
  try {
    writeFileSync(join(dir, 'desk.js'), js);
    execFileSync(process.execPath, ['--check', join(dir, 'desk.js')], { stdio: 'pipe' });
  } finally { rmSync(dir, { recursive: true, force: true }); }
});
