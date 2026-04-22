/**
 * Shipped. — Frontmatter writeback for dashboard drag-drop moves.
 *
 * Safely updates the `section:` field of an article's YAML frontmatter
 * without mangling the rest of the document. Uses gray-matter to parse
 * and stringify, preserving formatting as much as possible.
 *
 * Safety:
 *  - Validates that the target file lives under the expected issue dir
 *  - Validates that the new section is a canonical FORMULA key
 *  - Preserves all other frontmatter keys
 */

import { readFile, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { resolve, normalize } from 'node:path';
import matter from 'gray-matter';

/**
 * gray-matter parses date-like strings (e.g. "2026-04-22") into JS Date
 * objects. Re-stringifying emits ISO datetime instead of the original
 * date string, which churns git diffs. Convert known date-typed fields
 * back to yyyy-mm-dd before write.
 */
function normalizeDates(fm: Record<string, unknown>): void {
  const dateFields = ['created', 'updated', 'ship_date', 'date', 'running_order_decision_at', 'grade_override_date'];
  for (const field of dateFields) {
    const value = fm[field];
    if (value instanceof Date) {
      fm[field] = value.toISOString().slice(0, 10);
    }
  }
}

// ────────────────────────────────────────────────────────────────────
// Canonical section keys (mirror of SECTION_RULES in generate.ts)
// ────────────────────────────────────────────────────────────────────

const CANONICAL_SECTIONS = new Set([
  'open',
  'lead-story',
  'companion',
  'feature',
  'investigation',
  'also-shipped',
  'quiet-wire',
  'term-of-issue',
  'close',
  'release-log',
  'background', // meta-documents (signal, WIP drafts)
]);

// ────────────────────────────────────────────────────────────────────
// Types
// ────────────────────────────────────────────────────────────────────

export interface MoveRequest {
  filename: string;  // e.g., "conway-leak-analysis.md"
  section: string;   // target canonical section
  issueNumber: string;
}

export interface MoveResult {
  ok: boolean;
  error?: string;
  file?: string;
  previousSection?: string;
  newSection?: string;
}

export interface ImageRequest {
  filename: string;  // article to attach the image to
  imageUrl: string;  // http(s) URL, data: URI, or relative path
  issueNumber: string;
}

export interface ImageResult {
  ok: boolean;
  error?: string;
  file?: string;
  previousImage?: string | null;
  newImage?: string;
}

// ────────────────────────────────────────────────────────────────────
// Main
// ────────────────────────────────────────────────────────────────────

export async function moveArticle(req: MoveRequest, contentRoot: string): Promise<MoveResult> {
  // Validate section
  if (!CANONICAL_SECTIONS.has(req.section)) {
    return { ok: false, error: `Section "${req.section}" is not a canonical FORMULA key.` };
  }

  // Validate filename (no path traversal)
  if (req.filename.includes('..') || req.filename.includes('/') || req.filename.includes('\\')) {
    return { ok: false, error: `Filename "${req.filename}" contains invalid characters.` };
  }
  if (!/^[a-z0-9][a-z0-9_-]*\.md$/i.test(req.filename)) {
    return { ok: false, error: `Filename "${req.filename}" must match [a-z0-9_-]+\\.md` };
  }

  // Resolve target path — must live under content/articles/issue-NN/
  const articlesDir = resolve(contentRoot, 'articles', `issue-${req.issueNumber}`);
  const targetPath = resolve(articlesDir, req.filename);

  // Defensive: target must be inside articlesDir
  if (!normalize(targetPath).startsWith(normalize(articlesDir))) {
    return { ok: false, error: `Path traversal rejected: ${targetPath}` };
  }

  if (!existsSync(targetPath)) {
    return { ok: false, error: `Article not found: ${targetPath}` };
  }

  // Read + parse
  const raw = await readFile(targetPath, 'utf8');
  const parsed = matter(raw);
  const fm = parsed.data as Record<string, unknown>;

  const previousSection = fm.section ? String(fm.section) : '(unset)';

  // Already at target? No-op.
  if (previousSection === req.section) {
    return {
      ok: true,
      file: targetPath,
      previousSection,
      newSection: req.section,
    };
  }

  // Update section, bump updated date (today, UTC)
  fm.section = req.section;
  fm.updated = new Date().toISOString().slice(0, 10);

  // Normalize date fields back to yyyy-mm-dd so git diffs stay tight
  normalizeDates(fm);

  // Re-stringify with gray-matter (preserves content)
  const updated = matter.stringify(parsed.content, fm, { lineWidth: -1 } as unknown as object);

  await writeFile(targetPath, updated, 'utf8');

  return {
    ok: true,
    file: targetPath,
    previousSection,
    newSection: req.section,
  };
}

// ────────────────────────────────────────────────────────────────────
// Image attachment
// ────────────────────────────────────────────────────────────────────

export async function setArticleImage(req: ImageRequest, contentRoot: string): Promise<ImageResult> {
  if (req.filename.includes('..') || req.filename.includes('/') || req.filename.includes('\\')) {
    return { ok: false, error: `Filename "${req.filename}" contains invalid characters.` };
  }
  if (!/^[a-z0-9][a-z0-9_-]*\.md$/i.test(req.filename)) {
    return { ok: false, error: `Filename "${req.filename}" must match [a-z0-9_-]+\\.md` };
  }

  // Permit http(s), relative assets paths, and data URIs. Reject file:// and other schemes.
  const url = req.imageUrl.trim();
  if (!url) {
    return { ok: false, error: 'imageUrl is empty' };
  }
  if (url.length > 4096) {
    return { ok: false, error: 'imageUrl too long (>4096 chars).' };
  }
  const isOk =
    /^https?:\/\//i.test(url) ||
    /^data:image\//i.test(url) ||
    /^assets\//i.test(url) ||
    /^\.\/assets\//i.test(url);
  if (!isOk) {
    return { ok: false, error: 'imageUrl must be http(s)://, data:image/..., or a relative assets/ path.' };
  }

  const articlesDir = resolve(contentRoot, 'articles', `issue-${req.issueNumber}`);
  const targetPath = resolve(articlesDir, req.filename);
  if (!normalize(targetPath).startsWith(normalize(articlesDir))) {
    return { ok: false, error: 'Path traversal rejected.' };
  }
  if (!existsSync(targetPath)) {
    return { ok: false, error: `Article not found: ${targetPath}` };
  }

  const raw = await readFile(targetPath, 'utf8');
  const parsed = matter(raw);
  const fm = parsed.data as Record<string, unknown>;
  const previousImage = fm.hero_image ? String(fm.hero_image) : null;

  fm.hero_image = url;
  fm.updated = new Date().toISOString().slice(0, 10);

  normalizeDates(fm);

  const updated = matter.stringify(parsed.content, fm, { lineWidth: -1 } as unknown as object);
  await writeFile(targetPath, updated, 'utf8');

  return { ok: true, file: targetPath, previousImage, newImage: url };
}
