#!/usr/bin/env -S npx tsx
/**
 * Shipped. Assembler.
 *
 * Reads content/articles/issue-NN/*.md and content/issue-NN-wip.md,
 * writes content/issue-NN-{slug}.md (canonical for the renderer).
 *
 * MECHANICAL body extraction. No prose generation. Per VISION.md
 * doctrine (Auto-ops, human-voice): this command produces draft-zero
 * content only. Voice is Eddie's, added Thursday via /shipped-draft.
 *
 * Usage:
 *   pnpm assemble                   # auto-detect latest issue under content/articles/
 *   pnpm assemble --issue 02        # target a specific issue
 *   pnpm assemble --dry-run         # print to stdout, do not write
 *   pnpm assemble --force           # overwrite existing canonical without backing up
 */

import { readFileSync, readdirSync, existsSync, writeFileSync } from 'node:fs';
import { resolve, join, basename } from 'node:path';
import matter from 'gray-matter';

// ────────────────────────────────────────────────────────────────────
// CLI
// ────────────────────────────────────────────────────────────────────

interface Args {
  issue: string | null;
  force: boolean;
  dryRun: boolean;
  contentRoot: string;
}

function parseArgs(argv: string[]): Args {
  let issue: string | null = null;
  let force = false;
  let dryRun = false;
  let contentRoot = resolve(process.cwd(), '..', 'content');
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i]!;
    if (a === '--issue' && argv[i + 1]) { issue = argv[i + 1]!.padStart(2, '0'); i++; }
    else if (a === '--force') force = true;
    else if (a === '--dry-run' || a === '--dry') dryRun = true;
    else if (a === '--content-root' && argv[i + 1]) { contentRoot = argv[i + 1]!; i++; }
  }
  return { issue, force, dryRun, contentRoot };
}

function detectLatestIssue(contentRoot: string): string {
  const articlesRoot = join(contentRoot, 'articles');
  if (!existsSync(articlesRoot)) {
    throw new Error(`articles/ directory not found at ${articlesRoot}`);
  }
  const dirs = readdirSync(articlesRoot).filter((f) => /^issue-\d+$/.test(f));
  if (dirs.length === 0) throw new Error('No issue-NN/ directories under articles/');
  return dirs.sort().reverse()[0]!.replace('issue-', '');
}

// ────────────────────────────────────────────────────────────────────
// Body extraction
// ────────────────────────────────────────────────────────────────────

// H2 headings that mark scaffolding. Everything BEFORE the first match
// is treated as shippable body. Everything after is stripped.
const SCAFFOLDING_HEADERS: RegExp[] = [
  /^##\s+attribution caveats?\s*$/im,
  /^##\s+how this fits the issue\s*$/im,
  /^##\s+for builders?\s*$/im,
  /^##\s+the stake\s*$/im,
  /^##\s+(the )?operator-?layer implications?\s*$/im,
  /^##\s+the operator takeaway\s*$/im,
  /^##\s+voice notes\b/im,
  /^##\s+voice budget\b/im,
  /^##\s+named evidence\b/im,
  /^##\s+open questions\b/im,
  /^##\s+cross-references within the issue\s*$/im,
  /^##\s+the close move it enables\s*$/im,
  /^##\s+format note\s*$/im,
  /^##\s+category groupings\b/im,
  /^##\s+still pending\b/im,
  /^##\s+scaffolding-only mode\b/im,
  /^##\s+how to use this file\s*$/im,
  /^##\s+draft scaffolding/im,
  /^##\s+pre-flight checklist/im,
];

function extractShippableBody(articleBody: string): string {
  const lines = articleBody.split('\n');
  let cutAt = lines.length;
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]!;
    if (!line.startsWith('## ')) continue;
    if (SCAFFOLDING_HEADERS.some((re) => re.test(line))) {
      cutAt = i;
      break;
    }
  }
  return lines.slice(0, cutAt).join('\n').trim();
}

function extractH2Section(body: string, headingPattern: RegExp): string | null {
  const lines = body.split('\n');
  let start = -1;
  for (let i = 0; i < lines.length; i++) {
    if (headingPattern.test(lines[i]!)) {
      start = i + 1;
      break;
    }
  }
  if (start < 0) return null;
  let end = lines.length;
  for (let i = start; i < lines.length; i++) {
    if (/^##\s/.test(lines[i]!)) {
      end = i;
      break;
    }
  }
  const out = lines.slice(start, end).join('\n').trim();
  return out.length > 0 ? out : null;
}

function stripH1(body: string): string {
  return body
    .split('\n')
    .filter((l) => !l.startsWith('# '))
    .join('\n')
    .trim();
}

// Demote all H2 to H3 inside extracted article body so they become sub-headings
// of the canonical's H2 section (e.g., "## The split" -> "### The split" under
// "## The Lead Story"). Preserves document structure while fitting the
// renderer's "## = top-level section" convention.
function demoteH2(body: string): string {
  return body
    .split('\n')
    .map((l) => (l.startsWith('## ') ? '### ' + l.slice(3) : l))
    .join('\n');
}

function stripBlockquoteScaffoldNote(body: string): string {
  // Remove leading blockquote paragraph(s) that begin with scaffolding
  // markers like "> Scaffolding for..." or "> Companion / ...".
  const lines = body.split('\n');
  let i = 0;
  while (i < lines.length && lines[i]!.trim() === '') i++;
  // If the first non-empty block is a blockquote, drop it.
  if (i < lines.length && lines[i]!.startsWith('>')) {
    while (i < lines.length && (lines[i]!.startsWith('>') || lines[i]!.trim() === '')) i++;
  }
  return lines.slice(i).join('\n').trim();
}

// ────────────────────────────────────────────────────────────────────
// Reading
// ────────────────────────────────────────────────────────────────────

interface Article {
  path: string;
  filename: string;
  fm: Record<string, unknown>;
  body: string;
  section: string;
  status: string;
  title: string;
}

function readArticles(contentRoot: string, issueNumber: string): Article[] {
  const dir = join(contentRoot, 'articles', `issue-${issueNumber}`);
  if (!existsSync(dir)) throw new Error(`Articles dir not found: ${dir}`);
  const out: Article[] = [];
  for (const f of readdirSync(dir)) {
    if (!f.endsWith('.md')) continue;
    const path = join(dir, f);
    const raw = readFileSync(path, 'utf8');
    const parsed = matter(raw);
    const fm = parsed.data as Record<string, unknown>;
    out.push({
      path,
      filename: f,
      fm,
      body: parsed.content,
      section: String(fm.section ?? 'background'),
      status: String(fm.status ?? 'research'),
      title: String(fm.title ?? f.replace(/\.md$/, '')),
    });
  }
  return out;
}

interface WipMeta {
  issue: string;
  slug: string;
  title: string;
  date: string;
  period: string;
  termOfIssue: string;
  masthead: string;
  deck: string;
  byline: string;
  investigationUmbrella: string;
  byTheNumbers: boolean;
}

function readWipMetadata(contentRoot: string, issueNumber: string): WipMeta {
  const wipPath = join(contentRoot, `issue-${issueNumber}-wip.md`);
  if (!existsSync(wipPath)) throw new Error(`WIP not found: ${wipPath}`);
  const wipFm = matter(readFileSync(wipPath, 'utf8')).data as Record<string, unknown>;

  // Inherit masthead / deck / byline from any existing canonical (preserves Eddie's edits).
  const slug = String(wipFm.slug ?? 'wip');
  let canonicalFm: Record<string, unknown> = {};
  if (slug && slug !== 'wip') {
    const canonicalPath = join(contentRoot, `issue-${issueNumber}-${slug}.md`);
    if (existsSync(canonicalPath)) {
      canonicalFm = matter(readFileSync(canonicalPath, 'utf8')).data as Record<string, unknown>;
    }
  }

  const date = normalizeDate(wipFm.ship_date ?? canonicalFm.date ?? wipFm.date);
  const period = String(wipFm.period ?? canonicalFm.period ?? inferPeriod(date));

  return {
    issue: issueNumber,
    slug,
    title: String(wipFm.title ?? canonicalFm.title ?? 'TBD'),
    date,
    period,
    termOfIssue: String(wipFm.term_of_issue ?? canonicalFm.term_of_issue ?? ''),
    masthead: String(canonicalFm.masthead ?? 'Shipped.'),
    deck: String(canonicalFm.deck ?? ''),
    byline: String(canonicalFm.byline ?? 'Edited by Eddie Belaval. Reported with the assistance of Claude.'),
    investigationUmbrella: String(wipFm.investigation_umbrella ?? canonicalFm.investigation_umbrella ?? ''),
    byTheNumbers: wipFm.by_the_numbers_placeholder !== false,
  };
}

function inferPeriod(shipDate: string): string {
  if (!shipDate) return '';
  const m = shipDate.match(/^(\d{4})-(\d{2})-(\d{2})/);
  if (!m) return '';
  const end = new Date(`${m[1]}-${m[2]}-${m[3]}T12:00:00Z`);
  const start = new Date(end.getTime() - 7 * 86400000);
  const pad = (n: number) => String(n).padStart(2, '0');
  return `${start.getUTCFullYear()}-${pad(start.getUTCMonth() + 1)}-${pad(start.getUTCDate())} to ${m[1]}-${m[2]}-${m[3]}`;
}

// gray-matter coerces YAML `date:` fields to JS Date objects. Normalize back
// to YYYY-MM-DD so the frontmatter we emit is canonical and stable.
function normalizeDate(v: unknown): string {
  if (!v) return '';
  if (v instanceof Date) {
    const y = v.getUTCFullYear();
    const m = String(v.getUTCMonth() + 1).padStart(2, '0');
    const d = String(v.getUTCDate()).padStart(2, '0');
    return `${y}-${m}-${d}`;
  }
  const s = String(v);
  const iso = s.match(/^(\d{4}-\d{2}-\d{2})/);
  if (iso) return iso[1]!;
  return s;
}

// ────────────────────────────────────────────────────────────────────
// Assembly
// ────────────────────────────────────────────────────────────────────

function groupBySection(articles: Article[]): Map<string, Article[]> {
  const out = new Map<string, Article[]>();
  for (const a of articles) {
    if (!out.has(a.section)) out.set(a.section, []);
    out.get(a.section)!.push(a);
  }
  return out;
}

function collectAllSources(articles: Article[]): string[] {
  const set = new Set<string>();
  for (const a of articles) {
    const srcs = Array.isArray(a.fm.sources) ? (a.fm.sources as unknown[]) : [];
    for (const s of srcs) {
      if (typeof s === 'string' && /^https?:\/\//.test(s)) set.add(s);
    }
  }
  return Array.from(set).sort();
}

function writeSection(parts: string[], heading: string, body: string): void {
  if (!body.trim()) return;
  parts.push(`## ${heading}`);
  parts.push('');
  parts.push(body.trim());
  parts.push('');
  parts.push('---');
  parts.push('');
}

function bodyFromArticle(a: Article): string {
  // Keep the article H1 so it surfaces as the section's editorial title
  // in the renderer (each section's extractHeadline() looks for `# `).
  // Section local paragraph filters skip `#`-prefixed lines so the title
  // does not double-render in prose.
  return demoteH2(stripBlockquoteScaffoldNote(extractShippableBody(a.body)));
}

// For multi-article sections (Investigation, Also Shipped, QotW) the title
// is already emitted as `### {title}` per item, so the article H1 must be
// stripped to avoid a duplicate in the body.
function bodyFromArticleForSubstory(a: Article): string {
  return demoteH2(stripBlockquoteScaffoldNote(stripH1(extractShippableBody(a.body))));
}

function extractReleaseLogBlock(canonical: string): string | null {
  const lines = canonical.split('\n');
  let start = -1;
  for (let i = 0; i < lines.length; i++) {
    if (/^##\s+[A-G]\.\s+/.test(lines[i]!)) { start = i; break; }
  }
  if (start < 0) {
    for (let i = 0; i < lines.length; i++) {
      if (/^##\s+(the )?release log\b/i.test(lines[i]!)) { start = i; break; }
    }
  }
  if (start < 0) return null;
  return lines.slice(start).join('\n').trim();
}

// Category tag -> letter + name (per FORMULA.md's A-G Release Log schema)
const CATEGORY_MAP: Record<string, { letter: string; name: string }> = {
  MODEL: { letter: 'A', name: 'Models' },
  API: { letter: 'B', name: 'API and Platform' },
  PLATFORM: { letter: 'B', name: 'API and Platform' },
  CODE: { letter: 'C', name: 'Claude Code' },
  APP: { letter: 'D', name: 'Claude Apps' },
  LAUNCH: { letter: 'D', name: 'Claude Apps' },
  SDK: { letter: 'E', name: 'Agent SDKs' },
  RESEARCH: { letter: 'F', name: 'Research and Publications' },
  PAPER: { letter: 'F', name: 'Research and Publications' },
  POLICY: { letter: 'G', name: 'Partnerships and Policy' },
  DEAL: { letter: 'G', name: 'Partnerships and Policy' },
  NEWS: { letter: 'G', name: 'Partnerships and Policy' },
  ECOSYSTEM: { letter: 'G', name: 'Partnerships and Policy' },
  FIX: { letter: 'C', name: 'Claude Code' }, // fixes usually ride on Claude Code versions
  RELEASE: { letter: 'C', name: 'Claude Code' },
};

// Parse release-log-research.md entries into structured records.
// Each entry starts with `#### YYYY-MM-DD[: -] Title (source-link)`
// followed by prose until the next `####` or `### ` or `## `.
interface ReleaseEntry {
  date: string;
  title: string;
  body: string;
  categoryTag: string | null; // e.g. CODE, MODEL, POLICY
  sourceUrl: string | null;
  sourceLabel: string | null;
}

function parseReleaseLogResearch(body: string): ReleaseEntry[] {
  const lines = body.split('\n');
  const entries: ReleaseEntry[] = [];
  let i = 0;
  while (i < lines.length) {
    const line = lines[i]!;
    const m = line.match(/^####\s+(\d{4}-\d{2}-\d{2})\s*[:\-]\s*(.+?)\s*$/);
    if (!m) { i++; continue; }
    const date = m[1]!;
    let titleRaw = m[2]!.trim();
    // Extract trailing ([Label](URL)) if present
    let sourceLabel: string | null = null;
    let sourceUrl: string | null = null;
    const srcMatch = titleRaw.match(/\(\[([^\]]+)\]\(([^)]+)\)\)\s*$/);
    if (srcMatch) {
      sourceLabel = srcMatch[1]!;
      sourceUrl = srcMatch[2]!;
      titleRaw = titleRaw.slice(0, srcMatch.index).trim();
    }
    // Collect body + category tag until next heading.
    // Category tag may be on its own line (`[TAG]`) or inline in body
    // ("Category: `[TAG]`." in research format).
    let j = i + 1;
    const bodyLines: string[] = [];
    let categoryTag: string | null = null;
    while (j < lines.length) {
      const bl = lines[j]!;
      if (/^#{2,4}\s/.test(bl)) break;
      const tagOnOwnLine = bl.match(/^`\[([A-Z]+)\]`\s*$/);
      if (tagOnOwnLine) {
        categoryTag = tagOnOwnLine[1]!;
      } else {
        bodyLines.push(bl);
        const tagInline = bl.match(/Category:\s*`\[([A-Z]+)\]`/);
        if (tagInline && !categoryTag) categoryTag = tagInline[1]!;
      }
      j++;
    }
    entries.push({
      date,
      title: titleRaw,
      body: bodyLines.join('\n').trim(),
      categoryTag,
      sourceUrl,
      sourceLabel,
    });
    i = j;
  }
  return entries;
}

function categorizeReleaseLog(researchBody: string): string {
  const rawEntries = parseReleaseLogResearch(researchBody);
  // Dedupe by date+title so merged delta files don't double-enter entries.
  const seen = new Set<string>();
  const entries = rawEntries.filter((e) => {
    const key = `${e.date}::${e.title.trim().toLowerCase()}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
  if (entries.length === 0) return '';

  // Group by category letter
  const byCategory = new Map<string, { name: string; entries: ReleaseEntry[] }>();
  for (const e of entries) {
    const cat = e.categoryTag ? CATEGORY_MAP[e.categoryTag] : null;
    const letter = cat?.letter ?? 'G';
    const name = cat?.name ?? 'Partnerships and Policy';
    if (!byCategory.has(letter)) byCategory.set(letter, { name, entries: [] });
    byCategory.get(letter)!.entries.push(e);
  }

  // Sort each category's entries newest-first
  for (const g of byCategory.values()) {
    g.entries.sort((a, b) => b.date.localeCompare(a.date));
  }

  // Emit in letter order A through G
  const order = ['A', 'B', 'C', 'D', 'E', 'F', 'G'];
  const out: string[] = [];
  for (const letter of order) {
    const g = byCategory.get(letter);
    if (!g) continue;
    out.push(`## ${letter}. ${g.name}`);
    out.push('');
    out.push(`*${g.entries.length} entr${g.entries.length === 1 ? 'y' : 'ies'} in window.*`);
    out.push('');
    for (const e of g.entries) {
      const src = e.sourceUrl ? ` ([${e.sourceLabel ?? 'source'}](${e.sourceUrl}))` : '';
      out.push(`#### ${e.date} - ${e.title}${src}`);
      if (e.categoryTag) out.push(`\`[${e.categoryTag}]\``);
      out.push('');
      if (e.body) { out.push(e.body); out.push(''); }
    }
  }
  return out.join('\n').trim();
}

// Count front-of-book words (everything under ## The Open through ## The Close).
// Excludes Release Log sections (## A. through ## G.) and scaffolding H2s.
function countFobWords(markdown: string): number {
  const lines = markdown.split('\n');
  let inFob = false;
  let wordCount = 0;
  for (const line of lines) {
    if (/^##\s+The\s+Open\s*$/i.test(line)) { inFob = true; continue; }
    if (/^##\s+[A-G]\.\s+/.test(line)) { inFob = false; continue; }
    if (inFob) {
      // Skip headings, code fences, HTML comments
      if (/^##\s/.test(line)) continue;
      if (/^<!--/.test(line.trim())) continue;
      // Strip markdown formatting, count tokens
      const plain = line.replace(/[`*_#>\-\[\]()]/g, ' ').trim();
      if (plain) wordCount += plain.split(/\s+/).length;
    }
  }
  return wordCount;
}

function assembleCanonical(
  wip: WipMeta,
  articles: Article[],
  existingCanonical: string | null,
): string {
  const bySection = groupBySection(articles);
  const parts: string[] = [];

  // ── Frontmatter ────────────────────────────────────────────────
  parts.push('---');
  parts.push(`issue: ${wip.issue}`);
  parts.push(`slug: ${wip.slug}`);
  parts.push(`title: ${JSON.stringify(wip.title)}`);
  if (wip.date) parts.push(`date: ${wip.date}`);
  if (wip.period) parts.push(`period: ${wip.period}`);
  parts.push(`masthead: ${wip.masthead}`);
  if (wip.deck) parts.push(`deck: ${JSON.stringify(wip.deck)}`);
  parts.push(`byline: ${wip.byline}`);
  if (wip.termOfIssue) parts.push(`term_of_issue: ${wip.termOfIssue}`);
  parts.push(`status: draft`);
  if (wip.date) parts.push(`ship_date: ${wip.date}`);
  parts.push(`running_order_locked: false`);
  parts.push(`fob_content: editorial`);
  parts.push(`log_content: reference`);
  parts.push(`generated_at: ${new Date().toISOString().slice(0, 10)}`);
  parts.push(`generated_by: shipped-assemble`);

  const sources = collectAllSources(articles);
  if (sources.length > 0) {
    parts.push('sources:');
    for (const s of sources) parts.push(`  - ${s}`);
  }
  parts.push('---');
  parts.push('');

  // ── Masthead ───────────────────────────────────────────────────
  parts.push(`# ${wip.masthead}`);
  parts.push('');
  parts.push(`**Issue #${wip.issue}: ${wip.title}**`);
  parts.push(`*A magazine of what Anthropic ships.*`);
  if (wip.period) parts.push(`*Period: ${wip.period}. Volume I.*`);
  parts.push('');
  parts.push('---');
  parts.push('');

  // ── The Open (from front-of-book-draft.md) ────────────────────
  const fobDraft = articles.find((a) => a.filename === 'front-of-book-draft.md');
  if (fobDraft) {
    const openBody = extractH2Section(fobDraft.body, /^##\s+open\s*$/i);
    if (openBody) writeSection(parts, 'The Open', openBody);
  }

  // ── The Lead Story ─────────────────────────────────────────────
  const leadArticles = bySection.get('lead-story') ?? [];
  if (leadArticles.length > 0) {
    writeSection(parts, 'The Lead Story', bodyFromArticle(leadArticles[0]!));
  }

  // ── Companion to the Lead ──────────────────────────────────────
  const companionArticles = bySection.get('companion') ?? [];
  if (companionArticles.length > 0) {
    const primary = companionArticles[0]!;
    let companionBody = bodyFromArticle(primary);
    if (companionArticles.length > 1) {
      const alt = companionArticles.slice(1).map((a) => a.filename).join(', ');
      companionBody += `\n\n<!-- Additional Companion candidates (pick Thursday): ${alt}. -->`;
    }
    writeSection(parts, 'Companion to the Lead', companionBody);
  }

  // ── Feature (B-story) ──────────────────────────────────────────
  const featureArticles = bySection.get('feature') ?? [];
  if (featureArticles.length > 0) {
    writeSection(parts, 'Feature', bodyFromArticle(featureArticles[0]!));
  }

  // ── Investigation (may be paired) ──────────────────────────────
  const investigationArticles = bySection.get('investigation') ?? [];
  if (investigationArticles.length > 0) {
    const body: string[] = [];
    // Editorial umbrella title for the Investigation section — rendered as
    // the feature-title. Pulled from wip.investigationUmbrella if set, else
    // the section name fallback.
    const umbrella = wip.investigationUmbrella ?? '';
    if (umbrella) {
      body.push(`# ${umbrella}`);
      body.push('');
    }
    for (const a of investigationArticles) {
      const articleBody = bodyFromArticleForSubstory(a);
      const titleMatch = a.body.match(/^#\s+(.+)$/m);
      const title = titleMatch ? titleMatch[1]!.trim() : a.title;
      body.push(`### ${title}`);
      body.push('');
      body.push(articleBody);
      body.push('');
    }
    writeSection(parts, 'Investigation', body.join('\n').trim());
  }

  // ── By the Numbers (placeholder; cells render from frontmatter) ─
  // Positioned AFTER Investigation as a stat break before the short-form
  // items (Also Shipped / Quiet on the Wire / Term / Close).
  if (wip.byTheNumbers !== false) {
    writeSection(
      parts,
      'By the Numbers',
      '*The cells render from frontmatter; this section header is the placement marker for the renderer.*',
    );
  }

  // ── Also Shipped (multiple items as H3) ────────────────────────
  const alsoShipped = bySection.get('also-shipped') ?? [];
  if (alsoShipped.length > 0) {
    const body: string[] = [];
    for (const a of alsoShipped) {
      const articleBody = bodyFromArticleForSubstory(a);
      const titleMatch = a.body.match(/^#\s+(.+)$/m);
      const title = titleMatch ? titleMatch[1]!.trim() : a.title;
      body.push(`### ${title}`);
      body.push('');
      body.push(articleBody);
      body.push('');
    }
    writeSection(parts, 'Also Shipped', body.join('\n').trim());
  }

  // ── Quiet on the Wire (accepts 'quiet-wire' or 'quiet-on-the-wire') ─
  const quietArticles = [
    ...(bySection.get('quiet-wire') ?? []),
    ...(bySection.get('quiet-on-the-wire') ?? []),
  ];
  if (quietArticles.length > 0) {
    const body: string[] = [];
    for (const a of quietArticles) {
      const articleBody = bodyFromArticleForSubstory(a);
      const titleMatch = a.body.match(/^#\s+(.+)$/m);
      const title = titleMatch ? titleMatch[1]!.trim() : a.title;
      body.push(`### ${title}`);
      body.push('');
      body.push(articleBody);
      body.push('');
    }
    writeSection(parts, 'Quiet on the Wire', body.join('\n').trim());
  }

  // ── Term of the Issue ──────────────────────────────────────────
  const termArticles = bySection.get('term-of-issue') ?? [];
  if (termArticles.length > 0) {
    writeSection(parts, 'Term of the Issue', bodyFromArticle(termArticles[0]!));
  }

  // ── The Close ──────────────────────────────────────────────────
  const closeArticles = bySection.get('close') ?? [];
  if (closeArticles.length > 0) {
    writeSection(parts, 'The Close', bodyFromArticle(closeArticles[0]!));
  }

  // ── Release Log (auto-categorize from research; fall back to existing; else empty) ─
  // Aggregate ALL release-log section articles so delta files can contribute.
  const releaseArticles = articles.filter((a) => a.section === 'release-log');
  const combinedReleaseBody = releaseArticles.map((a) => a.body).join('\n\n');
  const autoCategorized = combinedReleaseBody ? categorizeReleaseLog(combinedReleaseBody) : '';
  const existingReleaseLog = existingCanonical ? extractReleaseLogBlock(existingCanonical) : null;

  if (autoCategorized) {
    parts.push(autoCategorized);
    parts.push('');
  } else if (existingReleaseLog) {
    parts.push(existingReleaseLog);
    parts.push('');
  } else {
    parts.push('## Release Log');
    parts.push('');
    parts.push('<!-- Empty. Run `pnpm scrape` to populate release-log-research.md, then re-assemble. -->');
    parts.push('');
  }

  return parts.join('\n');
}

// ────────────────────────────────────────────────────────────────────
// Main
// ────────────────────────────────────────────────────────────────────

function main(): void {
  const args = parseArgs(process.argv.slice(2));
  const { contentRoot, dryRun, force } = args;

  if (!existsSync(contentRoot)) {
    throw new Error(`Content root not found: ${contentRoot}`);
  }

  const issueNumber = args.issue ?? detectLatestIssue(contentRoot);

  console.log('');
  console.log('  Shipped. assembler');
  console.log('  ─────────────────────────────');
  console.log(`  issue       : ${issueNumber}`);
  console.log(`  content     : ${contentRoot}`);

  const wip = readWipMetadata(contentRoot, issueNumber);
  const articles = readArticles(contentRoot, issueNumber);

  console.log(`  slug        : ${wip.slug}`);
  console.log(`  title       : ${wip.title}`);
  console.log(`  date        : ${wip.date || '(none)'}`);
  console.log(`  period      : ${wip.period || '(none)'}`);
  console.log(`  term        : ${wip.termOfIssue || '(none)'}`);
  console.log(`  articles    : ${articles.length}`);

  const canonicalPath = join(contentRoot, `issue-${issueNumber}-${wip.slug}.md`);
  const existingCanonical = existsSync(canonicalPath)
    ? readFileSync(canonicalPath, 'utf8')
    : null;

  const markdown = assembleCanonical(wip, articles, existingCanonical);

  if (dryRun) {
    process.stdout.write(markdown);
    console.error('\n  (dry-run; not written)');
    return;
  }

  if (existingCanonical && !force) {
    const backupPath = canonicalPath.replace(/\.md$/, '.prev.md');
    writeFileSync(backupPath, existingCanonical, 'utf8');
    console.log(`  backup      : ${basename(backupPath)}`);
  }

  writeFileSync(canonicalPath, markdown, 'utf8');
  console.log(`  written     : ${basename(canonicalPath)}`);

  // FOB word-count warning (FORMULA.md ceiling is 1500)
  const fobWords = countFobWords(markdown);
  const ceiling = 1500;
  if (fobWords > ceiling) {
    const over = Math.round(((fobWords - ceiling) / ceiling) * 100);
    console.log(`  \x1b[33mFOB words   : ${fobWords} / ${ceiling} ceiling (${over}% over, trim in /shipped-draft)\x1b[0m`);
  } else {
    console.log(`  FOB words   : ${fobWords} / ${ceiling} ceiling (ok)`);
  }

  console.log('');
  console.log(`  next        : pnpm render ${canonicalPath}`);
  console.log('');
}

try {
  main();
} catch (err) {
  const msg = err instanceof Error ? err.message : String(err);
  console.error(`\n  ERR: ${msg}\n`);
  process.exit(1);
}
