/**
 * OG card generator for Shipped.
 *
 * Renders a branded 1200×630 PNG per target (archive index + each issue).
 * Uses Playwright headless Chromium to screenshot an HTML template built
 * in the Shipped. house style — paper background, Fraunces masthead,
 * orange dot accent, ink border.
 *
 * Usage:
 *   pnpm og               # generates all (archive + each issue)
 *   pnpm og --issue 02    # generates just the one
 *
 * Output: /Users/eddiebelaval/Development/id8/id8labs/public/shipped/{index|NN}/og.png
 */

import { readFileSync, readdirSync, existsSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';
import matter from 'gray-matter';

const CONTENT_ROOT = '/Users/eddiebelaval/Development/id8/shipped/content';
const DEPLOY_ROOT = '/Users/eddiebelaval/Development/id8/id8labs/public/shipped';

interface OgTarget {
  kind: 'archive' | 'issue';
  outPath: string;
  html: string;
}

// Same card on every thumbnail — signature Shipped. brand mark.
// The URL tells readers which issue; the thumbnail tells them what Shipped. is.
const CONSTANT_KICKER = 'Every Friday · 9 AM ET';
const CONSTANT_SUBHEAD = 'A weekly magazine on what Anthropic ships.';

function archiveHtml(): string {
  return renderOgHtml({
    number: '00',
    kicker: CONSTANT_KICKER,
    title: CONSTANT_SUBHEAD,
    isArchive: true,
  });
}

function issueHtml(_fm: Record<string, unknown>, _issueNum: string): string {
  // Issue cards are visually identical to the archive card. Per Eddie:
  // the thumbnail is the brand, not the issue. "00" and the tagline stay
  // constant across every shipped issue; the URL distinguishes them.
  return renderOgHtml({
    number: '00',
    kicker: CONSTANT_KICKER,
    title: CONSTANT_SUBHEAD,
    isArchive: false,
  });
}

function formatPrettyDate(iso: string): string {
  const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  const m = iso.match(/^(\d{4})-(\d{2})-(\d{2})/);
  if (!m) return iso;
  return `${months[parseInt(m[2]!, 10) - 1]} ${parseInt(m[3]!, 10)}, ${m[1]}`;
}

function renderOgHtml(args: { kicker: string; number: string; title: string; isArchive: boolean }): string {
  const { kicker, number, title } = args;
  return `<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,700;0,9..144,900;1,9..144,400;1,9..144,500&family=Archivo+Narrow:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root{
    --paper:#fafaf7;
    --paper-shadow:#f2f0e8;
    --ink:#0b0b0b;
    --body:#2a2a2a;
    --muted:#5a5a5a;
    --hair:#c8c4b8;
    --orange:#FF6B35;
    --serif:'Fraunces',Georgia,serif;
    --narrow:'Archivo Narrow',sans-serif;
    --mono:'JetBrains Mono',monospace;
  }
  *{margin:0;padding:0;box-sizing:border-box}
  html,body{
    width:1200px;height:630px;
    background:var(--paper);
    font-family:var(--serif);
    color:var(--ink);
    -webkit-font-smoothing:antialiased;
    text-rendering:optimizeLegibility;
  }
  .card{
    width:1200px;height:630px;
    padding:48px 64px;
    position:relative;
    overflow:hidden;
    border:2px solid var(--ink);
    box-shadow: inset 0 0 0 14px var(--paper), inset 0 0 0 15px var(--ink);
  }

  /* The big numeral sits CENTERED BEHIND the masthead — exact mirror of
     the magazine front cover's .cover-huge-num. Color is paper-shadow
     (faded tan) with a faint 8% ink outline for definition. The masthead
     overlays it at z-index 2. */
  .number-bg{
    position:absolute;
    top:50%;left:50%;transform:translate(-50%,-54%);
    font-family:var(--serif);
    font-weight:900;font-style:normal;
    font-variation-settings:"opsz" 144;
    font-size:640px;line-height:.78;letter-spacing:-.06em;
    color:var(--paper-shadow);
    -webkit-text-stroke:1px rgba(11,11,11,.08);
    user-select:none;
    pointer-events:none;
    z-index:1;
  }

  .fg{
    position:relative;z-index:2;
    height:100%;
    display:flex;flex-direction:column;justify-content:flex-start;align-items:center;
    text-align:center;
    padding-top:90px;
  }
  .top{display:flex;flex-direction:column;align-items:center;gap:18px}

  .kicker{
    font-family:var(--narrow);
    font-size:17px;font-weight:600;
    text-transform:uppercase;letter-spacing:.28em;
    color:var(--orange);
    display:flex;align-items:center;gap:14px;
  }
  .kicker::before{
    content:'';display:inline-block;
    width:10px;height:10px;border-radius:50%;
    background:var(--orange);
  }

  .masthead{
    font-family:var(--serif);font-style:italic;
    font-weight:500;font-variation-settings:"opsz" 144;
    font-size:260px;line-height:.86;letter-spacing:-.045em;
    color:var(--ink);
    margin:0;
  }
  .masthead .dot{color:var(--orange);font-style:normal}

  .sub{
    position:absolute;
    left:64px;right:64px;bottom:52px;
    text-align:center;
    font-family:var(--serif);font-style:italic;
    font-weight:400;font-variation-settings:"opsz" 72;
    font-size:30px;line-height:1.35;letter-spacing:-.005em;
    color:var(--body);
  }
  .sub em{font-style:italic;color:var(--orange);font-weight:500}
</style>
</head>
<body>
  <div class="card">
    <div class="number-bg">${number}</div>
    <div class="fg">
      <div class="top">
        <div class="kicker">${escape(kicker)}</div>
        <div class="masthead">Shipped<span class="dot">.</span></div>
      </div>
      <div class="sub">${formatTitle(title)}</div>
    </div>
  </div>
</body>
</html>`;
}

function escape(s: string): string {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function formatTitle(title: string): string {
  // Auto-italicize any emphasized words written as *word* (markdown style).
  return escape(title).replace(/\*([^*]+)\*/g, '<em>$1</em>');
}

function collectTargets(argIssue?: string): OgTarget[] {
  const targets: OgTarget[] = [];

  if (!argIssue) {
    targets.push({
      kind: 'archive',
      outPath: join(DEPLOY_ROOT, 'og.png'),
      html: archiveHtml(),
    });
  }

  const issueFiles = readdirSync(CONTENT_ROOT).filter(
    (f) => /^issue-\d+-.+\.md$/.test(f) && !f.endsWith('.prev.md') && !f.endsWith('-wip.md'),
  );
  for (const f of issueFiles) {
    const issueNum = f.match(/^issue-(\d+)-/)?.[1];
    if (!issueNum) continue;
    if (argIssue && issueNum !== argIssue) continue;
    const body = readFileSync(join(CONTENT_ROOT, f), 'utf8');
    const fm = matter(body).data;
    targets.push({
      kind: 'issue',
      outPath: join(DEPLOY_ROOT, issueNum, 'og.png'),
      html: issueHtml(fm, issueNum),
    });
  }

  return targets;
}

function renderTargetViaPlaywright(html: string, outPath: string): boolean {
  const tmpHtmlPath = `/tmp/shipped-og-${Date.now()}-${Math.random().toString(36).slice(2, 8)}.html`;
  writeFileSync(tmpHtmlPath, html, 'utf8');

  const pyScript = `
import sys
from playwright.sync_api import sync_playwright

html_path = sys.argv[1]
out_path = sys.argv[2]

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(
        viewport={"width": 1200, "height": 630},
        device_scale_factor=2,
    )
    page = context.new_page()
    page.goto(f"file://{html_path}", wait_until="networkidle")
    # Wait for custom fonts (Fraunces, Archivo, JetBrains Mono) to be loaded
    # and applied. Google Fonts serves with font-display: swap, so fallback
    # can appear first; we block until the real fonts are ready before the
    # screenshot, otherwise the OG renders in Times New Roman / Georgia.
    page.evaluate("() => document.fonts.ready")
    page.wait_for_timeout(400)
    page.screenshot(path=out_path, type="png", omit_background=False, clip={"x": 0, "y": 0, "width": 1200, "height": 630})
    browser.close()
`;

  const result = spawnSync(
    '/Library/Developer/CommandLineTools/usr/bin/python3',
    ['-c', pyScript, tmpHtmlPath, outPath],
    { encoding: 'utf8' },
  );

  if (result.status !== 0) {
    console.error(`  [og] ✗ ${outPath} — ${(result.stderr || '').slice(0, 400)}`);
    return false;
  }
  return true;
}

function main(): void {
  const argIdx = process.argv.indexOf('--issue');
  const argIssue = argIdx > 0 ? process.argv[argIdx + 1] : undefined;

  const targets = collectTargets(argIssue);

  console.log('');
  console.log('  Shipped. OG generator');
  console.log('  ─────────────────────────────');
  console.log(`  targets      : ${targets.length}`);
  console.log('');

  let ok = 0;
  let fail = 0;
  for (const t of targets) {
    if (!existsSync(join(t.outPath, '..'))) {
      console.log(`  [og] skip — ${t.outPath} (parent dir missing)`);
      continue;
    }
    const success = renderTargetViaPlaywright(t.html, t.outPath);
    if (success) {
      console.log(`  [og] ✓ ${t.outPath.replace('/Users/eddiebelaval/Development/id8/id8labs/public', '')}`);
      ok++;
    } else {
      fail++;
    }
  }

  console.log('');
  console.log(`  done         : ${ok} written, ${fail} failed`);
  console.log('');
}

main();
