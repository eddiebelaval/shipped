/**
 * Manifest sync.
 *
 * Regenerates the id8labs site's Shipped issue data file
 * (`id8labs/lib/shipped/issues.data.ts`) from the published hub archive
 * (`public/shipped/index.html`). The hub archive is the single source of truth
 * for what has shipped, so the unified /writing feed and homepage featured slot
 * derive from the same place the magazine's own archive page does and can never
 * drift from it.
 *
 * Called by renderIssue() after updateArchive() on every non-dry-run publish.
 */

import { promises as fs } from 'fs';
import path from 'path';

interface HubIssue {
  issueNumber: string;
  title: string;
  subtitle: string;
  date: string; // ISO YYYY-MM-DD
  readTime: string;
  tags: string[];
}

const MONTHS: Record<string, string> = {
  jan: '01', feb: '02', mar: '03', apr: '04', may: '05', jun: '06',
  jul: '07', aug: '08', sep: '09', oct: '10', nov: '11', dec: '12',
};

function stripTags(s: string): string {
  return s.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
}

function decode(s: string): string {
  return s
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&rsquo;/g, '’')
    .replace(/&nbsp;/g, ' ');
}

/** "May 8, 2026" → "2026-05-08". Returns '' if unparseable. */
function toIso(prettyDate: string): string {
  const m = prettyDate.match(/([A-Za-z]{3,})\.?\s+(\d{1,2}),\s*(\d{4})/);
  if (!m) return '';
  const mon = MONTHS[m[1]!.slice(0, 3).toLowerCase()];
  if (!mon) return '';
  return `${m[3]}-${mon}-${m[2]!.padStart(2, '0')}`;
}

/** Word count of a rendered issue HTML, for read-time estimation. */
async function readTimeFor(deployRoot: string, issueNumber: string): Promise<string> {
  try {
    const html = await fs.readFile(
      path.join(deployRoot, issueNumber, 'index.html'),
      'utf-8',
    );
    const text = html
      .replace(/<(script|style)[\s\S]*?<\/\1>/gi, ' ')
      .replace(/<[^>]+>/g, ' ');
    const words = text.split(/\s+/).filter(Boolean).length;
    const mins = Math.max(1, Math.round(words / 220));
    return `${mins} min read`;
  } catch {
    return '';
  }
}

/** Parse every issue card out of the hub archive HTML. */
function parseHubCards(hubHtml: string): Omit<HubIssue, 'readTime'>[] {
  const out: Omit<HubIssue, 'readTime'>[] = [];
  const cardRe = /href="\/shipped\/(\d{2})\/"([\s\S]*?)<\/a>/g;
  let m: RegExpExecArray | null;
  while ((m = cardRe.exec(hubHtml)) !== null) {
    const num = m[1]!;
    const body = m[2]!;
    if (!/issue-mid|issue-num/.test(body)) continue; // skip non-card anchors
    const h2 = body.match(/<h2[^>]*>([\s\S]*?)<\/h2>/);
    const p = body.match(/<p[^>]*>([\s\S]*?)<\/p>/);
    const date = body.match(/class="date"[^>]*>([\s\S]*?)</);
    const tags = [...body.matchAll(/<span[^>]*>([\s\S]*?)<\/span>/g)]
      .map((t) => decode(stripTags(t[1]!)))
      .filter((t) => t && t !== '.' && t.length > 1);
    out.push({
      issueNumber: num,
      title: h2 ? decode(stripTags(h2[1]!)) : `Issue ${num}`,
      subtitle: p ? decode(stripTags(p[1]!)) : '',
      date: date ? toIso(decode(stripTags(date[1]!))) : '',
      tags,
    });
  }
  return out;
}

function renderDataFile(issues: HubIssue[], generatedOn: string): string {
  // newest first
  const sorted = [...issues].sort((a, b) => (a.date < b.date ? 1 : -1));
  const numbers = sorted.map((i) => i.issueNumber).join(', ');
  const body = sorted
    .map((i, idx) => {
      const featured = idx === 0 ? '\n    featured: true,' : '';
      const tags = i.tags.map((t) => `'${t.replace(/'/g, "\\'")}'`).join(', ');
      const esc = (s: string) => s.replace(/\\/g, '\\\\').replace(/'/g, "\\'");
      return `  {
    issueNumber: '${i.issueNumber}',
    title: '${esc(i.title)}',
    subtitle: '${esc(i.subtitle)}',
    date: '${i.date}',
    excerpt: '${esc(i.subtitle)}',
    readTime: '${i.readTime}',
    tags: [${tags}],${featured}
  },`;
    })
    .join('\n');

  return `/**
 * Shipped. — Magazine Issue Data (AUTO-GENERATED)
 *
 * DO NOT EDIT BY HAND. Regenerated from the published hub archive
 * (public/shipped/index.html) by the Shipped pipeline on every publish:
 *
 *     pipeline/src/render/sync-manifest.ts  →  this file
 *
 * The hub archive is the single source of truth for what has shipped, so the
 * unified /writing feed and the homepage featured slot can never drift from the
 * magazine's own archive page.
 *
 * Last generated: ${generatedOn} (issues ${numbers})
 */

import type { ShippedIssuePreview } from './issues'

/** The canonical Shipped. issue list, newest first. Mirrors the hub archive. */
export const SHIPPED_ISSUES: ShippedIssuePreview[] = [
${body}
]
`;
}

export interface SyncManifestOptions {
  /** public/shipped root that holds index.html + NN/index.html. */
  deployRoot: string;
  /** Override the destination data file (defaults to the id8labs lib path). */
  manifestPath?: string;
  /** Date stamp for the generated header (YYYY-MM-DD). */
  generatedOn?: string;
}

/**
 * Regenerate issues.data.ts from the hub archive. Returns the path written and
 * the issue count, or null if the hub archive could not be read.
 */
export async function syncManifest(
  opts: SyncManifestOptions,
): Promise<{ manifestPath: string; count: number } | null> {
  const { deployRoot } = opts;
  const manifestPath =
    opts.manifestPath ??
    path.resolve(deployRoot, '../../lib/shipped/issues.data.ts');

  let hubHtml: string;
  try {
    // The hub archive moved from index.html -> archive.html when the dynamic
    // /shipped App Router page took over the index slot. Prefer archive.html;
    // fall back to index.html for older deploys.
    try {
      hubHtml = await fs.readFile(path.join(deployRoot, 'archive.html'), 'utf-8');
    } catch {
      hubHtml = await fs.readFile(path.join(deployRoot, 'index.html'), 'utf-8');
    }
  } catch {
    console.warn(`[sync-manifest] hub archive not found under ${deployRoot} (skipping)`);
    return null;
  }

  const cards = parseHubCards(hubHtml);
  if (cards.length === 0) {
    console.warn('[sync-manifest] no issue cards parsed from hub (skipping)');
    return null;
  }

  const issues: HubIssue[] = await Promise.all(
    cards.map(async (c) => ({
      ...c,
      readTime: await readTimeFor(deployRoot, c.issueNumber),
    })),
  );

  const generatedOn = opts.generatedOn ?? new Date().toISOString().slice(0, 10);
  const contents = renderDataFile(issues, generatedOn);
  await fs.mkdir(path.dirname(manifestPath), { recursive: true });
  await fs.writeFile(manifestPath, contents, 'utf-8');
  return { manifestPath, count: issues.length };
}
