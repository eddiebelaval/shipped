/**
 * Shipped. — Dashboard generator
 *
 * Reads:
 *   content/articles/issue-NN/*.md  (via gray-matter frontmatter)
 *   content/issue-NN-wip.md          (for theme-of-week + ship date)
 *
 * Writes:
 *   pipeline/output/dashboard-issue-NN.html
 *
 * Purpose:
 *   A visual production table for assembling an issue. Read-only v0.1.
 *   Drag-drop UI is present but doesn't persist — v0.2 adds write-back.
 *
 * Usage:
 *   pnpm dashboard                  # defaults to latest issue
 *   pnpm dashboard --issue 02       # target a specific issue
 */

import { readdir, readFile, writeFile } from 'node:fs/promises';
import { existsSync, readdirSync } from 'node:fs';
import { join, resolve } from 'node:path';
import matter from 'gray-matter';
import { renderDashboard } from './template.js';
import { gradeArticle, type Grade } from './grader.js';

// ────────────────────────────────────────────────────────────────────
// Types
// ────────────────────────────────────────────────────────────────────

export interface DashboardArticle {
  file: string;
  filename: string;
  title: string;
  issue: string;
  section: string;
  status: 'research' | 'draft' | 'used' | string;
  wordCount: number;
  sourceCount: number;
  created: string;
  updated: string;
  placementOpen: string | null;
  heroImage: string | null;
  grade: Grade;
}

export interface SectionSlot {
  key: string;
  label: string;
  required: boolean;
  slotKind: 'mandatory' | 'shelf';
  description: string;
  wordBudgetMin: number;
  wordBudgetMax: number;
  articleCountMin: number;
  articleCountMax: number;
  articles: DashboardArticle[];
  filled: boolean;
  gap: string | null;
}

export interface Dashboard {
  issue: string;
  shipDate: string;
  theme: string;
  slug: string;
  title: string;
  status: string;
  lockDate: string;
  readinessPercent: number;
  readinessLabel: string;
  articleCountTotal: number;
  articleCountHealthy: { min: number; max: number };
  sections: SectionSlot[];
  scratchPad: DashboardArticle[];
  gaps: string[];
  generatedAt: string;
}

// ────────────────────────────────────────────────────────────────────
// Section formula — mirrors content/FORMULA.md
// ────────────────────────────────────────────────────────────────────

interface SlotRule {
  key: string;
  label: string;
  slotKind: 'mandatory' | 'shelf';
  description: string;
  wordBudgetMin: number;
  wordBudgetMax: number;
  articleCountMin: number;
  articleCountMax: number;
  required: boolean;
}

const SECTION_RULES: SlotRule[] = [
  {
    key: 'open',
    label: 'The Open',
    slotKind: 'mandatory',
    description: 'Editorial hook. Opening-line pattern + a turn.',
    wordBudgetMin: 80,
    wordBudgetMax: 150,
    articleCountMin: 0,
    articleCountMax: 1,
    required: true,
  },
  {
    key: 'lead-story',
    label: 'The Lead Story',
    slotKind: 'mandatory',
    description: 'The week’s biggest release. 200–300 distilled; source ~800–1,200w.',
    wordBudgetMin: 800,
    wordBudgetMax: 1200,
    articleCountMin: 1,
    articleCountMax: 2,
    required: true,
  },
  {
    key: 'companion',
    label: 'Companion to the Lead',
    slotKind: 'shelf',
    description: 'Cross-competitor / cross-product data. Only when lead is data-heavy.',
    wordBudgetMin: 150,
    wordBudgetMax: 250,
    articleCountMin: 0,
    articleCountMax: 1,
    required: false,
  },
  {
    key: 'feature',
    label: 'Feature',
    slotKind: 'shelf',
    description: 'A product-family arc. Editorial-explanatory. One slot per issue.',
    wordBudgetMin: 800,
    wordBudgetMax: 1500,
    articleCountMin: 0,
    articleCountMax: 1,
    required: false,
  },
  {
    key: 'investigation',
    label: 'Investigation',
    slotKind: 'shelf',
    description: 'Multi-source story beyond "what shipped." Reporting + attribution.',
    wordBudgetMin: 1000,
    wordBudgetMax: 1500,
    articleCountMin: 0,
    articleCountMax: 3,
    required: false,
  },
  {
    key: 'also-shipped',
    label: 'Also Shipped',
    slotKind: 'mandatory',
    description: '3–5 items × 60–100 words each. Source articles 300–500w per item.',
    wordBudgetMin: 300,
    wordBudgetMax: 500,
    articleCountMin: 3,
    articleCountMax: 5,
    required: true,
  },
  {
    key: 'quiet-wire',
    label: 'Quiet on the Wire',
    slotKind: 'mandatory',
    description: 'What’s rumored, hinted, expected. Compiled from signal report.',
    wordBudgetMin: 50,
    wordBudgetMax: 80,
    articleCountMin: 0,
    articleCountMax: 1,
    required: true,
  },
  {
    key: 'term-of-issue',
    label: 'Term of the Issue',
    slotKind: 'shelf',
    description: 'A concept worth naming. Only when earned.',
    wordBudgetMin: 100,
    wordBudgetMax: 150,
    articleCountMin: 0,
    articleCountMax: 1,
    required: false,
  },
  {
    key: 'close',
    label: 'The Close',
    slotKind: 'mandatory',
    description: 'Rhythm closer. Three beats. Last one lands.',
    wordBudgetMin: 30,
    wordBudgetMax: 80,
    articleCountMin: 0,
    articleCountMax: 1,
    required: true,
  },
  {
    key: 'release-log',
    label: 'Release Log',
    slotKind: 'mandatory',
    description: 'Full week catalog, grouped A–G. Scraper output.',
    wordBudgetMin: 0,
    wordBudgetMax: 0,
    articleCountMin: 0,
    articleCountMax: 0,
    required: true,
  },
];

// Any section key not in SECTION_RULES goes to the scratch pad.
const KNOWN_SECTION_KEYS = new Set([
  ...SECTION_RULES.map(r => r.key),
  // Aliases and secondary placements that map to the scratch pad
  // if no canonical key found.
]);

// ────────────────────────────────────────────────────────────────────
// Helpers
// ────────────────────────────────────────────────────────────────────

function countWords(text: string): number {
  return text
    .replace(/```[\s\S]*?```/g, '')
    .replace(/[#*>_`\-|]/g, ' ')
    .split(/\s+/)
    .filter(Boolean).length;
}

function normalizeSection(raw: unknown): string {
  if (!raw) return 'background';
  const s = String(raw).trim().toLowerCase();
  // First token of a comma-separated section list is canonical placement
  const first = s.split(',')[0]!.trim();
  // Common aliases
  const aliases: Record<string, string> = {
    'lead': 'lead-story',
    'leadstory': 'lead-story',
    'also shipped': 'also-shipped',
    'alsoshipped': 'also-shipped',
    'quiet on the wire': 'quiet-wire',
    'quiet': 'quiet-wire',
    'term': 'term-of-issue',
    'term of issue': 'term-of-issue',
    'termofissue': 'term-of-issue',
    'release log': 'release-log',
    'releaselog': 'release-log',
  };
  return aliases[first] ?? first;
}

async function loadArticle(filePath: string): Promise<DashboardArticle | null> {
  const raw = await readFile(filePath, 'utf8');
  const parsed = matter(raw);
  const fm = parsed.data as Record<string, unknown>;
  const filename = filePath.split('/').pop() ?? filePath;

  const grade = gradeArticle({
    body: parsed.content,
    frontmatter: fm,
    filename,
  });

  return {
    file: filePath,
    filename,
    title: String(fm.title ?? filename.replace(/\.md$/, '')),
    issue: String(fm.issue ?? ''),
    section: normalizeSection(fm.section),
    status: String(fm.status ?? 'research'),
    wordCount: countWords(parsed.content),
    sourceCount: Array.isArray(fm.sources) ? fm.sources.length : 0,
    created: String(fm.created ?? ''),
    updated: String(fm.updated ?? ''),
    placementOpen: fm.placement_open ? String(fm.placement_open) : null,
    heroImage: fm.hero_image ? String(fm.hero_image) : null,
    grade,
  };
}

async function loadWipMetadata(issueDir: string): Promise<Partial<Dashboard>> {
  // Look for content/issue-NN-wip.md — one level up from articles/issue-NN
  const contentRoot = resolve(issueDir, '..', '..');
  const issueNumber = issueDir.match(/issue-(\d+)/)?.[1] ?? '00';
  const wipPath = join(contentRoot, `issue-${issueNumber}-wip.md`);
  if (!existsSync(wipPath)) return {};
  const raw = await readFile(wipPath, 'utf8');
  const fm = matter(raw).data as Record<string, unknown>;
  return {
    shipDate: String(fm.ship_date ?? ''),
    slug: String(fm.slug ?? ''),
    title: String(fm.title ?? ''),
    status: String(fm.status ?? ''),
    theme: String(fm.term_of_issue ?? ''),
  };
}

function computeSlot(rule: SlotRule, articles: DashboardArticle[]): SectionSlot {
  const placed = articles.filter(a => a.section === rule.key);
  let filled = false;
  let gap: string | null = null;

  if (rule.required) {
    if (rule.articleCountMin === 0) {
      filled = true; // editorial section, no source article needed
    } else if (placed.length >= rule.articleCountMin) {
      filled = true;
    } else {
      gap = `Need ${rule.articleCountMin - placed.length} more article${rule.articleCountMin - placed.length === 1 ? '' : 's'} (min ${rule.articleCountMin})`;
    }
  } else {
    filled = placed.length > 0;
  }

  return {
    key: rule.key,
    label: rule.label,
    required: rule.required,
    slotKind: rule.slotKind,
    description: rule.description,
    wordBudgetMin: rule.wordBudgetMin,
    wordBudgetMax: rule.wordBudgetMax,
    articleCountMin: rule.articleCountMin,
    articleCountMax: rule.articleCountMax,
    articles: placed,
    filled,
    gap,
  };
}

// ────────────────────────────────────────────────────────────────────
// Main
// ────────────────────────────────────────────────────────────────────

export async function buildDashboard(issueNumber: string, contentRoot: string): Promise<Dashboard> {
  const articlesDir = join(contentRoot, 'articles', `issue-${issueNumber}`);
  if (!existsSync(articlesDir)) {
    throw new Error(`No articles directory found: ${articlesDir}`);
  }

  const files = (await readdir(articlesDir))
    .filter(f => f.endsWith('.md'))
    .filter(f => !f.startsWith('.'));

  const articles: DashboardArticle[] = [];
  for (const f of files) {
    const article = await loadArticle(join(articlesDir, f));
    if (article) articles.push(article);
  }

  const sections = SECTION_RULES.map(rule => computeSlot(rule, articles));

  const scratchPad = articles.filter(a => !KNOWN_SECTION_KEYS.has(a.section));

  const requiredSections = sections.filter(s => s.required);
  const readySections = requiredSections.filter(s => s.filled).length;
  const readinessPercent = Math.round((readySections / requiredSections.length) * 100);

  const readinessLabel =
    readinessPercent >= 90 ? 'Ship-ready'
    : readinessPercent >= 70 ? 'On track'
    : readinessPercent >= 50 ? 'Mid-stream'
    : 'Early stage';

  const gaps: string[] = [];
  for (const s of sections) {
    if (s.gap) gaps.push(`${s.label}: ${s.gap}`);
  }
  // Article inventory gap per FORMULA.md (6–8 healthy)
  const totalSourceArticles = articles.filter(a => a.section !== 'background').length;
  if (totalSourceArticles < 6) {
    gaps.push(`Article inventory below formula (${totalSourceArticles}/6 min)`);
  }

  const wipMeta = await loadWipMetadata(articlesDir);

  // Compute Thursday lock date = ship date - 1 day
  let lockDate = '';
  if (wipMeta.shipDate) {
    const d = new Date(wipMeta.shipDate);
    d.setUTCDate(d.getUTCDate() - 1);
    lockDate = d.toISOString().slice(0, 10);
  }

  return {
    issue: issueNumber,
    shipDate: wipMeta.shipDate ?? '',
    theme: wipMeta.theme ?? '',
    slug: wipMeta.slug ?? '',
    title: wipMeta.title ?? '',
    status: wipMeta.status ?? 'drafting',
    lockDate,
    readinessPercent,
    readinessLabel,
    articleCountTotal: totalSourceArticles,
    articleCountHealthy: { min: 6, max: 8 },
    sections,
    scratchPad,
    gaps,
    generatedAt: new Date().toISOString(),
  };
}

// ────────────────────────────────────────────────────────────────────
// CLI
// ────────────────────────────────────────────────────────────────────

function parseArgs(argv: string[]): { issue: string } {
  const idx = argv.indexOf('--issue');
  if (idx >= 0 && argv[idx + 1]) return { issue: argv[idx + 1]!.padStart(2, '0') };

  // Default: latest issue by scanning content/articles/
  const contentRoot = resolve(process.cwd(), '..', 'content');
  const articlesRoot = join(contentRoot, 'articles');
  if (!existsSync(articlesRoot)) return { issue: '02' };
  const issues = readdirSync(articlesRoot)
    .filter(f => f.startsWith('issue-'))
    .map(f => f.replace('issue-', ''))
    .sort()
    .reverse();
  return { issue: issues[0] ?? '02' };
}

async function main(): Promise<void> {
  const { issue } = parseArgs(process.argv.slice(2));
  const pipelineRoot = process.cwd();
  const contentRoot = resolve(pipelineRoot, '..', 'content');
  const outputPath = resolve(pipelineRoot, 'output', `dashboard-issue-${issue}.html`);

  console.log(`→ Building dashboard for Issue ${issue}`);
  const dashboard = await buildDashboard(issue, contentRoot);
  const html = renderDashboard(dashboard);

  await writeFile(outputPath, html, 'utf8');
  console.log(`✓ Dashboard written: ${outputPath}`);
  console.log(`  Issue ${dashboard.issue} — ship ${dashboard.shipDate} — ${dashboard.readinessPercent}% ready`);
  console.log(`  Articles: ${dashboard.articleCountTotal} (healthy ${dashboard.articleCountHealthy.min}–${dashboard.articleCountHealthy.max})`);
  console.log(`  Gaps: ${dashboard.gaps.length}`);

  // Per-article grade summary
  const allArticles = [
    ...dashboard.sections.flatMap(s => s.articles),
    ...dashboard.scratchPad,
  ];
  if (allArticles.length > 0) {
    console.log(`\n  Grades (RUBRIC.md):`);
    for (const a of allArticles) {
      const g = a.grade;
      const badge = g.overridden ? 'OVR' : `${g.letter} ${g.total}/28`;
      console.log(`    ${badge.padEnd(8)}  ${a.filename}`);
    }
  }

  console.log(`\n  Open in browser:\n    open "${outputPath}"`);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(err => {
    console.error('Dashboard build failed:', err);
    process.exit(1);
  });
}
