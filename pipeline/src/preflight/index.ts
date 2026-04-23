/**
 * Shipped. pre-flight check.
 *
 * Single entry point for "are we green to launch?" Runs a suite of checks
 * across continuity, arc, content, voice, tech, attribution, and render.
 *
 * Output: GREEN (ship it), AMBER (warnings only, ship with note), or
 * RED (blockers present, fix before ship) + an ordered punch list of
 * files to edit.
 *
 * Usage:
 *   pnpm preflight --issue 02
 *   pnpm preflight           # auto-detects latest
 */

import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';

type Severity = 'pass' | 'warn' | 'fail';

interface CheckResult {
  id: string;
  name: string;
  status: Severity;
  summary: string;
  details: string[];
  fix?: string;
}

function parseArgs(argv: string[]): { issue?: string; contentRoot: string; skipLinks: boolean } {
  const out = { issue: undefined as string | undefined, contentRoot: '', skipLinks: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i]!;
    if (a === '--issue') out.issue = argv[++i];
    else if (a === '--content') out.contentRoot = argv[++i]!;
    else if (a === '--skip-links') out.skipLinks = true;
  }
  if (!out.contentRoot) {
    out.contentRoot = join(process.cwd().replace(/\/pipeline$/, ''), 'content');
  }
  return out;
}

function detectLatestIssue(articlesRoot: string): string {
  const dirs = readdirSync(articlesRoot).filter((f) => /^issue-\d+$/.test(f));
  if (dirs.length === 0) throw new Error(`No issue-* dirs in ${articlesRoot}`);
  return dirs.sort().reverse()[0]!.replace('issue-', '');
}

function runCurl(url: string): string {
  const r = spawnSync('curl', ['-sIL', '-A', 'Mozilla/5.0', '--max-time', '8', '-o', '/dev/null', '-w', '%{http_code}', url], { encoding: 'utf8' });
  return (r.stdout || '').trim();
}

function checkCanonical(contentRoot: string, issueNum: string): CheckResult {
  const dir = readdirSync(contentRoot);
  const canonical = dir.find((f) => new RegExp(`^issue-${issueNum}-.+\\.md$`).test(f) && !f.endsWith('.prev.md') && !f.endsWith('-wip.md'));
  if (!canonical) {
    return { id: 'canonical', name: 'Canonical assembled', status: 'fail', summary: 'No canonical file found.', details: [`Expected: content/issue-${issueNum}-{slug}.md`], fix: `pnpm assemble --issue ${issueNum}` };
  }
  const body = readFileSync(join(contentRoot, canonical), 'utf8');
  const fm = body.match(/^---\n([\s\S]*?)\n---/);
  if (!fm) return { id: 'canonical', name: 'Canonical assembled', status: 'fail', summary: 'Canonical has no frontmatter', details: [] };
  const missing: string[] = [];
  for (const key of ['title', 'date', 'term_of_issue', 'deck']) {
    const re = new RegExp(`^${key}:\\s*(.+)$`, 'm');
    const m = fm[1]!.match(re);
    if (!m || !m[1] || m[1].trim() === 'TBD' || m[1].trim() === '""' || m[1].trim() === '"TBD"') missing.push(key);
  }
  if (missing.length) {
    return { id: 'canonical', name: 'Canonical assembled', status: 'fail', summary: `Missing or TBD: ${missing.join(', ')}`, details: missing.map((k) => `  • ${k}`), fix: `Set in issue-${issueNum}-wip.md + re-assemble` };
  }
  return { id: 'canonical', name: 'Canonical assembled', status: 'pass', summary: canonical, details: [] };
}

function checkDashes(canonicalPath: string): CheckResult {
  const body = readFileSync(canonicalPath, 'utf8');
  const fobStart = body.search(/^##\s+The Open/m);
  const fobEnd = body.search(/^##\s+[A-G]\.\s/m);
  if (fobStart < 0) return { id: 'dashes', name: 'No em/en dashes in FOB', status: 'warn', summary: 'Could not locate FOB boundaries', details: [] };
  const fob = body.slice(fobStart, fobEnd > 0 ? fobEnd : body.length);
  const lines = fob.split('\n');
  const hits: string[] = [];
  lines.forEach((line, i) => {
    if (/[—–]/.test(line)) hits.push(`  line ${i}: ${line.trim().slice(0, 100)}`);
  });
  if (hits.length === 0) return { id: 'dashes', name: 'No em/en dashes in FOB', status: 'pass', summary: '0 dashes', details: [] };
  return { id: 'dashes', name: 'No em/en dashes in FOB', status: 'fail', summary: `${hits.length} dash(es) in FOB`, details: hits, fix: 'Swap for commas/colons/periods in source articles; re-assemble.' };
}

const FORBIDDEN = ['thrilled', 'ushers in', 'game-changing', 'industry-leading', 'synergies', 'best-in-class', 'empowers users', 'robust solution', 'unveiled', 'leverag', 'paradigm shift', 'revolutionary', 'groundbreaking', 'wake-up call', 'mounting pressure', 'raises concerns', 'comes on the heels', 'amid growing', 'seamless integration', 'next-gen', 'AI arms race'];

function checkForbiddenPhrases(canonicalPath: string): CheckResult {
  // Only scan FOB (editorial prose). Release Log entries are factual summaries
  // that may legitimately contain words like "next-generation" — skipped to
  // avoid false positives on legit compounds vs. the banned "next-gen" shorthand.
  const full = readFileSync(canonicalPath, 'utf8');
  const fobStart = full.search(/^##\s+The Open/m);
  const fobEnd = full.search(/^##\s+[A-G]\.\s/m);
  const fob = full.slice(Math.max(0, fobStart), fobEnd > 0 ? fobEnd : full.length).toLowerCase();
  const hits: string[] = [];
  for (const p of FORBIDDEN) {
    // Word-boundary match so "next-gen" doesn't match "next-generation".
    const re = new RegExp(`(^|[^\\w-])${p.toLowerCase().replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}(?![\\w-])`, 'i');
    if (re.test(fob)) hits.push(`  • "${p}"`);
  }
  if (hits.length === 0) return { id: 'forbidden', name: 'No kill-list phrases', status: 'pass', summary: '0 forbidden phrases in FOB', details: [] };
  return { id: 'forbidden', name: 'No kill-list phrases', status: 'fail', summary: `${hits.length} forbidden phrase(s) in FOB`, details: hits, fix: 'Rewrite to house voice in source articles; re-assemble.' };
}

function checkXYZFormula(canonicalPath: string): CheckResult {
  const body = readFileSync(canonicalPath, 'utf8');
  const fobStart = body.search(/^##\s+The Open/m);
  const fobEnd = body.search(/^##\s+[A-G]\.\s/m);
  const fob = body.slice(Math.max(0, fobStart), fobEnd > 0 ? fobEnd : body.length);
  const matches = fob.match(/(is not|isn't)\s[^.]+\.\s+It is |(is not|isn't)\s[^;]+;\s+it'?s /gi) || [];
  if (matches.length <= 1) return { id: 'xyz-formula', name: '"X isn\'t Y, it\'s Z" budget', status: 'pass', summary: `${matches.length} use (budget: 1)`, details: [] };
  return { id: 'xyz-formula', name: '"X isn\'t Y, it\'s Z" budget', status: 'fail', summary: `${matches.length} uses in FOB (budget: 1)`, details: matches.map((m) => `  • ${m.slice(0, 80)}...`), fix: 'Keep the flagship use. Rewrite others.' };
}

function checkRepaint(contentRoot: string, canonicalPath: string, issueNum: string): CheckResult {
  const prior = join(contentRoot, 'issue-00-the-founding.md');
  if (!existsSync(prior)) return { id: 'repaint', name: 'No repaint vs prior', status: 'pass', summary: 'No prior issue baseline', details: [] };
  const current = readFileSync(canonicalPath, 'utf8');
  const priorBody = readFileSync(prior, 'utf8');
  const normalize = (s: string) => s.replace(/\(\[[^\]]+\]\([^)]+\)\)/g, '').trim().slice(0, 100);
  const priorEntries = new Set((priorBody.match(/^####\s+\d{4}-\d{2}-\d{2}[\s\S-]+?$/gm) || []).map(normalize));
  const currentEntries = (current.match(/^####\s+\d{4}-\d{2}-\d{2}[\s\S-]+?$/gm) || []).map(normalize);
  const repaints = currentEntries.filter((e) => priorEntries.has(e));
  if (repaints.length === 0) return { id: 'repaint', name: 'No repaint vs prior', status: 'pass', summary: `Issue ${issueNum} carries no Issue 01 entries`, details: [] };
  return { id: 'repaint', name: 'No repaint vs prior', status: 'fail', summary: `${repaints.length} duplicate(s)`, details: repaints.map((e) => `  • ${e}`), fix: 'Drop duplicates from release-log-research.md; re-assemble.' };
}

function checkFobWordCount(canonicalPath: string): CheckResult {
  const body = readFileSync(canonicalPath, 'utf8');
  const fobStart = body.search(/^##\s+The Open/m);
  const fobEnd = body.search(/^##\s+[A-G]\.\s/m);
  if (fobStart < 0) return { id: 'fob-words', name: 'FOB word budget', status: 'warn', summary: 'Could not locate FOB', details: [] };
  const fob = body.slice(fobStart, fobEnd > 0 ? fobEnd : body.length);
  const words = fob.replace(/```[\s\S]*?```/g, ' ').replace(/[#>*`_|\-]/g, ' ').split(/\s+/).filter((w) => w.length > 0).length;
  const soft = 1500;
  const hard = 3000;
  if (words <= soft) return { id: 'fob-words', name: 'FOB word budget', status: 'pass', summary: `${words} / ${soft}w soft ceiling`, details: [] };
  if (words <= hard) return { id: 'fob-words', name: 'FOB word budget', status: 'warn', summary: `${words}w (${soft}w soft / ${hard}w hard)`, details: [`  ${Math.round((words / soft - 1) * 100)}% over soft`] };
  return { id: 'fob-words', name: 'FOB word budget', status: 'fail', summary: `${words}w exceeds ${hard}w hard`, details: [`  Trim ${words - hard}+ words`], fix: 'Trim section bodies (Investigation + Feature are biggest levers).' };
}

function checkLinks(canonicalPath: string, skip: boolean): CheckResult {
  if (skip) return { id: 'links', name: 'Links resolve', status: 'pass', summary: 'Skipped (--skip-links)', details: [] };
  const issueMatch = canonicalPath.match(/issue-(\d+)/);
  const issueNum = issueMatch ? issueMatch[1]! : '00';
  const renderedPath = `/Users/eddiebelaval/Development/id8labs/public/shipped/${issueNum}/index.html`;
  const source = existsSync(renderedPath) ? readFileSync(renderedPath, 'utf8') : readFileSync(canonicalPath, 'utf8');
  const urls = new Set<string>();
  const hrefRe = /https?:\/\/[^\s")'<>]+/g;
  let m: RegExpExecArray | null;
  while ((m = hrefRe.exec(source))) {
    const u = m[0].replace(/[.,);]$/, '');
    if (u.startsWith('https://fonts.')) continue;
    if (u.includes('id8labs.app/shipped')) continue;
    urls.add(u);
  }
  const broken: string[] = [];
  const botBlocked: string[] = [];
  const botHosts = ['x.com', 'twitter.com', 'medium.com', 'seekingalpha.com', 'bloomberg.com', 'ft.com', 'linkedin.com'];
  for (const u of urls) {
    const code = runCurl(u);
    if (code.startsWith('2') || code.startsWith('3')) continue;
    let host = '';
    try { host = new URL(u).host.replace(/^www\./, ''); } catch { host = ''; }
    if (botHosts.some((h) => host.endsWith(h)) && code === '403') {
      botBlocked.push(`  • ${code} ${u}`);
    } else {
      broken.push(`  • ${code} ${u}`);
    }
  }
  if (broken.length === 0 && botBlocked.length === 0) return { id: 'links', name: 'Links resolve', status: 'pass', summary: `${urls.size}/${urls.size} live`, details: [] };
  if (broken.length === 0) return { id: 'links', name: 'Links resolve', status: 'warn', summary: `${urls.size - botBlocked.length}/${urls.size} live; ${botBlocked.length} bot-guarded (likely OK)`, details: botBlocked };
  return { id: 'links', name: 'Links resolve', status: 'fail', summary: `${broken.length} broken, ${botBlocked.length} bot-guarded`, details: [...broken, ...botBlocked], fix: 'Swap or drop broken cites in source articles.' };
}

function checkRender(canonicalPath: string): CheckResult {
  const r = spawnSync('pnpm', ['render', canonicalPath], { encoding: 'utf8', cwd: '/Users/eddiebelaval/Development/id8/shipped/pipeline' });
  const out = (r.stdout || '') + (r.stderr || '');
  if (r.status !== 0 || /\berror\b/i.test(out)) {
    return { id: 'render', name: 'Canonical renders', status: 'fail', summary: 'pnpm render failed', details: out.split('\n').filter((l) => /error|fail/i.test(l)).slice(0, 8).map((l) => `  ${l}`), fix: 'Inspect render output; fix markdown or frontmatter.' };
  }
  const m = out.match(/Sections\s*:\s*(\d+)[\s\S]*?FOB words\s*:\s*(\d+)[\s\S]*?Log entries\s*:\s*(\d+)/);
  return { id: 'render', name: 'Canonical renders', status: 'pass', summary: m ? `${m[1]} sections, ${m[2]}w FOB, ${m[3]} log entries` : 'render complete', details: [] };
}

function checkArc(canonicalPath: string): CheckResult {
  const body = readFileSync(canonicalPath, 'utf8');
  const req = ['## The Open', '## The Lead Story', '## Feature', '## Investigation', '## Also Shipped', '## Quiet on the Wire', '## Term of the Issue', '## The Close'];
  const missing = req.filter((s) => !body.includes(s));
  if (missing.length) return { id: 'arc', name: 'Editorial arc complete', status: 'fail', summary: `Missing ${missing.length} section(s)`, details: missing.map((s) => `  • ${s}`), fix: 'Populate missing source articles or verify section names.' };
  const idx = req.map((s) => body.indexOf(s));
  for (let i = 1; i < idx.length; i++) {
    if (idx[i]! < idx[i - 1]!) return { id: 'arc', name: 'Editorial arc complete', status: 'fail', summary: 'Section order wrong', details: [`  ${req[i - 1]} after ${req[i]}`], fix: 'Re-assemble (order is assembler-owned).' };
  }
  return { id: 'arc', name: 'Editorial arc complete', status: 'pass', summary: 'All FOB sections present, order correct', details: [] };
}

function run(): void {
  const args = parseArgs(process.argv.slice(2));
  const articlesRoot = join(args.contentRoot, 'articles');
  const issueNum = args.issue ?? detectLatestIssue(articlesRoot);

  console.log('');
  console.log('  Shipped. pre-flight');
  console.log('  ─────────────────────────────');
  console.log(`  issue        : ${issueNum}`);
  console.log(`  content      : ${args.contentRoot}`);
  console.log('');

  const dir = readdirSync(args.contentRoot);
  const canonicalFile = dir.find((f) => new RegExp(`^issue-${issueNum}-.+\\.md$`).test(f) && !f.endsWith('.prev.md') && !f.endsWith('-wip.md'));
  const canonicalPath = canonicalFile ? join(args.contentRoot, canonicalFile) : '';

  const checks: CheckResult[] = [];
  checks.push(checkCanonical(args.contentRoot, issueNum));
  if (canonicalPath && existsSync(canonicalPath)) {
    checks.push(checkArc(canonicalPath));
    checks.push(checkDashes(canonicalPath));
    checks.push(checkForbiddenPhrases(canonicalPath));
    checks.push(checkXYZFormula(canonicalPath));
    checks.push(checkFobWordCount(canonicalPath));
    checks.push(checkRepaint(args.contentRoot, canonicalPath, issueNum));
    checks.push(checkRender(canonicalPath));
    checks.push(checkLinks(canonicalPath, args.skipLinks));
  }

  const failures = checks.filter((c) => c.status === 'fail');
  const warnings = checks.filter((c) => c.status === 'warn');
  const verdict = failures.length > 0 ? 'RED' : warnings.length > 0 ? 'AMBER' : 'GREEN';

  const pad = (s: string, n: number) => (s + ' '.repeat(n)).slice(0, n);
  const icon = (s: Severity) => s === 'pass' ? '\x1b[32m✓\x1b[0m' : s === 'warn' ? '\x1b[33m!\x1b[0m' : '\x1b[31m✗\x1b[0m';

  for (const c of checks) {
    console.log(`  ${icon(c.status)}  ${pad(c.name, 34)} ${c.summary}`);
    if (c.status !== 'pass' && c.details.length > 0) {
      for (const d of c.details.slice(0, 6)) console.log(`     ${d}`);
      if (c.details.length > 6) console.log(`     ...and ${c.details.length - 6} more`);
    }
  }
  console.log('');

  const banner = verdict === 'GREEN'
    ? '\x1b[42m\x1b[30m GREEN \x1b[0m  all checks pass, ready to ship'
    : verdict === 'AMBER'
      ? `\x1b[43m\x1b[30m AMBER \x1b[0m  ${warnings.length} warning${warnings.length === 1 ? '' : 's'}, no blockers`
      : `\x1b[41m\x1b[37m  RED  \x1b[0m  ${failures.length} blocker${failures.length === 1 ? '' : 's'}, DO NOT SHIP`;
  console.log(`  ${banner}`);
  console.log('');

  if (verdict !== 'GREEN') {
    console.log('  Punch list (in order):');
    const ordered = [...failures, ...warnings];
    ordered.forEach((c, i) => {
      console.log(`    ${String(i + 1).padStart(2, '0')}  ${c.name}`);
      if (c.fix) console.log(`        → ${c.fix}`);
    });
    console.log('');
  }

  if (verdict === 'RED') process.exit(2);
}

run();
