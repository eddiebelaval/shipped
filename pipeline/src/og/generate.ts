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

function archiveHtml(): string {
  return renderOgHtml({
    kicker: 'Weekly · Every Friday, 9 AM ET',
    number: '',
    title: 'A weekly magazine on what Anthropic ships.',
    date: 'id8labs.app/shipped',
    isArchive: true,
  });
}

function issueHtml(fm: Record<string, unknown>, issueNum: string): string {
  const title = String(fm.title || '').replace(/^"|"$/g, '');
  const date = String(fm.date || '');
  const prettyDate = date ? formatPrettyDate(date) : '';
  return renderOgHtml({
    kicker: `Issue ${issueNum}${prettyDate ? ` · ${prettyDate}` : ''}`,
    number: issueNum,
    title,
    date: String(fm.deck || '').replace(/^"|"$/g, ''),
    isArchive: false,
  });
}

function formatPrettyDate(iso: string): string {
  const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  const m = iso.match(/^(\d{4})-(\d{2})-(\d{2})/);
  if (!m) return iso;
  return `${months[parseInt(m[2]!, 10) - 1]} ${parseInt(m[3]!, 10)}, ${m[1]}`;
}

function renderOgHtml(args: { kicker: string; number: string; title: string; date: string; isArchive: boolean }): string {
  const { kicker, number, title, date, isArchive } = args;
  return `<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,700;1,9..144,400;1,9..144,500&family=Archivo+Narrow:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
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
    padding:52px 64px;
    position:relative;
    display:flex;flex-direction:column;justify-content:space-between;
    border:2px solid var(--ink);
    box-shadow: inset 0 0 0 14px var(--paper), inset 0 0 0 15px var(--ink);
  }
  .kicker{
    font-family:var(--narrow);
    font-size:18px;font-weight:600;
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
    font-size:180px;line-height:.9;letter-spacing:-.04em;
    color:var(--ink);
    margin:12px 0 20px -6px;
  }
  .masthead .dot{color:var(--orange);font-style:normal}
  .number{
    font-family:var(--serif);
    font-weight:400;font-variation-settings:"opsz" 144;
    font-size:96px;line-height:1;letter-spacing:-.03em;
    color:var(--ink);
    margin-bottom:6px;
  }
  .title{
    font-family:var(--serif);font-weight:400;
    font-variation-settings:"opsz" 72;
    font-size:52px;line-height:1.1;letter-spacing:-.018em;
    color:var(--ink);
    max-width:1000px;
  }
  .title em{font-style:italic;color:var(--orange)}
  .sub{
    font-family:var(--serif);font-style:italic;
    font-size:24px;line-height:1.4;
    color:var(--muted);
    max-width:960px;
    margin-top:12px;
  }
  .footer{
    display:flex;justify-content:space-between;align-items:flex-end;
    border-top:1px solid var(--hair);
    padding-top:18px;
    font-family:var(--mono);font-size:14px;color:var(--muted);
  }
  .footer b{color:var(--ink);font-weight:500}
  .big-mark{
    position:absolute;
    right:64px;bottom:64px;
    font-family:var(--serif);font-style:italic;font-weight:500;
    font-size:56px;letter-spacing:-.02em;color:var(--ink);
    opacity:1;
    font-variation-settings:"opsz" 144;
  }
  .big-mark .dot{color:var(--orange);font-style:normal}
  .archive-hero{
    display:flex;flex-direction:column;justify-content:center;align-items:center;
    height:100%;text-align:center;gap:0;
  }
  .archive-hero .masthead{font-size:240px;margin:0}
  .archive-hero .sub{margin-top:24px;text-align:center;font-size:32px}
  .archive-hero .kicker{justify-content:center;margin-bottom:32px}
</style>
</head>
<body>
  ${isArchive ? `
  <div class="card">
    <div class="archive-hero">
      <div class="kicker">${kicker}</div>
      <div class="masthead">Shipped<span class="dot">.</span></div>
      <div class="sub">${escape(title)}</div>
    </div>
    <div class="footer" style="position:absolute;bottom:40px;left:64px;right:64px;">
      <span><b>id8labs.app/shipped</b></span>
      <span>Published by id8Labs</span>
    </div>
  </div>` : `
  <div class="card">
    <div>
      <div class="kicker">${kicker}</div>
      <div class="masthead">Shipped<span class="dot">.</span></div>
    </div>
    <div>
      ${number ? `<div class="number">Issue ${number}.</div>` : ''}
      <div class="title">${formatTitle(title)}</div>
      ${date ? `<div class="sub">${escape(date)}</div>` : ''}
    </div>
    <div class="footer">
      <span>id8labs.app/shipped/${number}</span>
      <span>Edited by <b>Eddie Belaval</b> · Published by id8Labs</span>
    </div>
  </div>`}
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
