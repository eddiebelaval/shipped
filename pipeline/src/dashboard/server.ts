/**
 * Shipped. — Dashboard dev server.
 *
 * Localhost HTTP server that serves the dashboard HTML (always
 * freshly regenerated from disk) and accepts POST /api/move
 * to persist drag-drop moves to article frontmatter.
 *
 * Usage:
 *   pnpm dashboard-dev               # defaults to latest issue, port 4321
 *   pnpm dashboard-dev --issue 02    # target a specific issue
 *   pnpm dashboard-dev --port 5000   # custom port
 *
 * Routes:
 *   GET  /                    → dashboard HTML (live-mode JS, POSTs on drop)
 *   POST /api/move            → { filename, section } → updates frontmatter
 *   GET  /api/health          → { ok: true, issue, articles, grade }
 *   GET  /api/article/:name   → raw article content (for future preview)
 */

import { createServer, type IncomingMessage, type ServerResponse } from 'node:http';
import { readdirSync, existsSync } from 'node:fs';
import { readFile, appendFile } from 'node:fs/promises';
import { resolve, join, basename } from 'node:path';
import { randomBytes } from 'node:crypto';
import matter from 'gray-matter';
import { buildDashboard } from './generate.js';
import { renderDashboard } from './template.js';
import { moveArticle, setArticleImage } from './writer.js';

// ────────────────────────────────────────────────────────────────────
// Config
// ────────────────────────────────────────────────────────────────────

interface ServerConfig {
  issue: string;
  port: number;
  contentRoot: string;
}

function parseArgs(argv: string[]): { issue: string | null; port: number } {
  let issue: string | null = null;
  let port = 4321;
  const issueIdx = argv.indexOf('--issue');
  if (issueIdx >= 0 && argv[issueIdx + 1]) issue = argv[issueIdx + 1]!.padStart(2, '0');
  const portIdx = argv.indexOf('--port');
  if (portIdx >= 0 && argv[portIdx + 1]) port = parseInt(argv[portIdx + 1]!, 10) || 4321;
  return { issue, port };
}

function resolveLatestIssue(contentRoot: string): string {
  const articlesRoot = resolve(contentRoot, 'articles');
  const issues = readdirSync(articlesRoot)
    .filter(f => f.startsWith('issue-'))
    .map(f => f.replace('issue-', ''))
    .sort()
    .reverse();
  return issues[0] ?? '02';
}

// ────────────────────────────────────────────────────────────────────
// Request helpers
// ────────────────────────────────────────────────────────────────────

async function readRequestBody(req: IncomingMessage): Promise<string> {
  return new Promise((resolve, reject) => {
    const chunks: Buffer[] = [];
    req.on('data', chunk => chunks.push(chunk));
    req.on('end', () => resolve(Buffer.concat(chunks).toString('utf8')));
    req.on('error', reject);
  });
}

function sendJson(res: ServerResponse, status: number, body: unknown): void {
  res.statusCode = status;
  res.setHeader('Content-Type', 'application/json');
  res.end(JSON.stringify(body));
}

function sendHtml(res: ServerResponse, status: number, html: string): void {
  res.statusCode = status;
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.setHeader('Cache-Control', 'no-cache');
  res.end(html);
}

// ────────────────────────────────────────────────────────────────────
// Route handlers
// ────────────────────────────────────────────────────────────────────

async function handleDashboard(cfg: ServerConfig, res: ServerResponse): Promise<void> {
  try {
    const dashboard = await buildDashboard(cfg.issue, cfg.contentRoot);
    const html = renderDashboard(dashboard, { live: true, port: cfg.port });
    sendHtml(res, 200, html);
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    sendHtml(res, 500, `<h1>Dashboard error</h1><pre>${escape(msg)}</pre>`);
  }
}

async function handleMove(cfg: ServerConfig, req: IncomingMessage, res: ServerResponse): Promise<void> {
  try {
    const body = await readRequestBody(req);
    const data = JSON.parse(body) as { filename?: string; section?: string };
    if (!data.filename || !data.section) {
      sendJson(res, 400, { ok: false, error: 'filename and section required' });
      return;
    }
    const result = await moveArticle(
      { filename: data.filename, section: data.section, issueNumber: cfg.issue },
      cfg.contentRoot,
    );
    if (!result.ok) {
      sendJson(res, 400, result);
      return;
    }
    // Rebuild dashboard to get fresh grade for the moved article
    const dashboard = await buildDashboard(cfg.issue, cfg.contentRoot);
    const allArticles = [
      ...dashboard.sections.flatMap(s => s.articles),
      ...dashboard.scratchPad,
    ];
    const moved = allArticles.find(a => a.filename === data.filename);
    sendJson(res, 200, {
      ...result,
      readinessPercent: dashboard.readinessPercent,
      articleCountTotal: dashboard.articleCountTotal,
      grade: moved?.grade ?? null,
    });
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    sendJson(res, 500, { ok: false, error: msg });
  }
}

async function handleImage(cfg: ServerConfig, req: IncomingMessage, res: ServerResponse): Promise<void> {
  try {
    const body = await readRequestBody(req);
    const data = JSON.parse(body) as { filename?: string; imageUrl?: string };
    if (!data.filename || !data.imageUrl) {
      sendJson(res, 400, { ok: false, error: 'filename and imageUrl required' });
      return;
    }
    const result = await setArticleImage(
      { filename: data.filename, imageUrl: data.imageUrl, issueNumber: cfg.issue },
      cfg.contentRoot,
    );
    sendJson(res, result.ok ? 200 : 400, result);
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    sendJson(res, 500, { ok: false, error: msg });
  }
}

async function handleNext(cfg: ServerConfig, res: ServerResponse): Promise<void> {
  try {
    const dashboard = await buildDashboard(cfg.issue, cfg.contentRoot);
    const highlights = await readHighlights(cfg);
    const recent = highlights.slice().reverse().slice(0, 10); // newest first, cap at 10
    const plan = { ...dashboard.nextActions, actions: [...dashboard.nextActions.actions] };

    // Promote any unreviewed highlights to the top of the action queue.
    if (recent.length > 0) {
      const top = recent[0]!;
      const snippet = top.text.length > 80 ? top.text.slice(0, 80) + '…' : top.text;
      const highlightAction = {
        id: 'review-highlights',
        priority: 'high' as const,
        phase: plan.currentPhase,
        title: `Review ${recent.length} highlight${recent.length === 1 ? '' : 's'} from Eddie`,
        detail: `Most recent: "${snippet}" (${top.filename})`,
        why: 'A highlight is a manual signal. Eddie flagged that phrase as structurally important — it may need a pull-quote slot, counter-frame header, or operator-takeaway hook the article doesn\'t yet have.',
        claudePrompt: `Eddie left ${recent.length} highlight${recent.length === 1 ? '' : 's'} in the reader. Read content/articles/issue-${cfg.issue}/_highlights.jsonl OR curl http://127.0.0.1:${cfg.port}/api/highlights for the full list. For each highlight: quote the phrase, name its article, and surface Eddie's note (if any). Then propose ONE structural scaffolding move per highlight (new section header, bullet slot, voice note anchor) that would let that phrase land cleanly in the final prose. Present as a short table. DO NOT write prose. Wait for Eddie to pick which scaffolds to apply.`,
        estimate: '5-15 min',
      };
      plan.actions = [highlightAction, ...plan.actions];
    }

    sendJson(res, 200, {
      issue: dashboard.issue,
      ...plan,
      recentHighlights: recent,
      highlightsTotal: highlights.length,
    });
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    sendJson(res, 500, { error: msg });
  }
}

async function handleArticle(
  cfg: ServerConfig,
  filenameRaw: string,
  res: ServerResponse,
): Promise<void> {
  try {
    // Path-traversal guard: strip directories, reject suspicious names
    const filename = basename(filenameRaw);
    if (!filename.endsWith('.md') || filename.startsWith('.') || filename !== filenameRaw) {
      sendJson(res, 400, { ok: false, error: 'Invalid filename' });
      return;
    }

    // Try per-issue articles dir first; fall back to content root for WIP/signal etc.
    const articleDir = resolve(cfg.contentRoot, 'articles', `issue-${cfg.issue}`);
    const articlePath = join(articleDir, filename);
    const wipPath = join(cfg.contentRoot, filename);
    const path = existsSync(articlePath)
      ? articlePath
      : existsSync(wipPath) ? wipPath : null;

    if (!path) {
      sendJson(res, 404, { ok: false, error: `Article not found: ${filename}` });
      return;
    }

    const raw = await readFile(path, 'utf8');
    const parsed = matter(raw);
    const fm = parsed.data as Record<string, unknown>;

    // Lookup grade from a fresh dashboard build
    const dashboard = await buildDashboard(cfg.issue, cfg.contentRoot);
    const allArticles = [
      ...dashboard.sections.flatMap(s => s.articles),
      ...dashboard.scratchPad,
    ];
    const meta = allArticles.find(a => a.filename === filename);

    sendJson(res, 200, {
      ok: true,
      filename,
      title: String(fm.title ?? filename.replace(/\.md$/, '')),
      section: String(fm.section ?? 'background'),
      status: String(fm.status ?? 'research'),
      created: String(fm.created ?? ''),
      updated: String(fm.updated ?? ''),
      wordCount: meta?.wordCount ?? parsed.content.trim().split(/\s+/).length,
      sourceCount: meta?.sourceCount ?? (Array.isArray(fm.sources) ? fm.sources.length : 0),
      sources: Array.isArray(fm.sources) ? fm.sources : [],
      grade: meta?.grade ?? null,
      content: parsed.content,
      frontmatterRaw: parsed.matter,
    });
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    sendJson(res, 500, { ok: false, error: msg });
  }
}

interface HighlightRecord {
  id: string;
  issue: string;
  filename: string;
  text: string;
  context: string | null;
  note: string | null;
  createdAt: string;
}

function highlightsFilePath(cfg: ServerConfig): string {
  return resolve(cfg.contentRoot, 'articles', `issue-${cfg.issue}`, '_highlights.jsonl');
}

async function readHighlights(cfg: ServerConfig): Promise<HighlightRecord[]> {
  const path = highlightsFilePath(cfg);
  if (!existsSync(path)) return [];
  const raw = await readFile(path, 'utf8');
  const records: HighlightRecord[] = [];
  for (const line of raw.split('\n')) {
    const trimmed = line.trim();
    if (!trimmed) continue;
    try {
      records.push(JSON.parse(trimmed) as HighlightRecord);
    } catch {
      // skip malformed lines
    }
  }
  return records;
}

async function handleHighlightCreate(
  cfg: ServerConfig,
  req: IncomingMessage,
  res: ServerResponse,
): Promise<void> {
  try {
    const body = await readRequestBody(req);
    const data = JSON.parse(body) as {
      filename?: string;
      text?: string;
      context?: string;
      note?: string;
    };
    if (!data.filename || !data.text) {
      sendJson(res, 400, { ok: false, error: 'filename and text required' });
      return;
    }
    const filename = basename(data.filename);
    if (!filename.endsWith('.md') || filename !== data.filename) {
      sendJson(res, 400, { ok: false, error: 'Invalid filename' });
      return;
    }
    const text = String(data.text).trim();
    if (!text || text.length > 4000) {
      sendJson(res, 400, { ok: false, error: 'text must be 1-4000 chars' });
      return;
    }

    const record: HighlightRecord = {
      id: 'h-' + randomBytes(4).toString('hex'),
      issue: cfg.issue,
      filename,
      text,
      context: typeof data.context === 'string' ? data.context.slice(0, 400) : null,
      note: typeof data.note === 'string' ? data.note.slice(0, 1000) : null,
      createdAt: new Date().toISOString(),
    };
    await appendFile(highlightsFilePath(cfg), JSON.stringify(record) + '\n', 'utf8');
    sendJson(res, 200, { ok: true, highlight: record });
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    sendJson(res, 500, { ok: false, error: msg });
  }
}

async function handleHighlightList(
  cfg: ServerConfig,
  url: URL,
  res: ServerResponse,
): Promise<void> {
  try {
    const records = await readHighlights(cfg);
    const filter = url.searchParams.get('filename');
    const filtered = filter ? records.filter(r => r.filename === filter) : records;
    sendJson(res, 200, {
      ok: true,
      issue: cfg.issue,
      count: filtered.length,
      highlights: filtered,
    });
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    sendJson(res, 500, { ok: false, error: msg });
  }
}

async function handleHealth(cfg: ServerConfig, res: ServerResponse): Promise<void> {
  try {
    const dashboard = await buildDashboard(cfg.issue, cfg.contentRoot);
    sendJson(res, 200, {
      ok: true,
      issue: cfg.issue,
      articles: dashboard.articleCountTotal,
      readinessPercent: dashboard.readinessPercent,
      gaps: dashboard.gaps.length,
    });
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    sendJson(res, 500, { ok: false, error: msg });
  }
}

function escape(s: string): string {
  return s.replace(/[<>&"']/g, c => ({ '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;', "'": '&#39;' }[c]!));
}

// ────────────────────────────────────────────────────────────────────
// Main
// ────────────────────────────────────────────────────────────────────

async function main(): Promise<void> {
  const args = parseArgs(process.argv.slice(2));
  const pipelineRoot = process.cwd();
  const contentRoot = resolve(pipelineRoot, '..', 'content');
  const issue = args.issue ?? resolveLatestIssue(contentRoot);

  const cfg: ServerConfig = { issue, port: args.port, contentRoot };

  const server = createServer(async (req, res) => {
    try {
      const url = new URL(req.url ?? '/', `http://${req.headers.host}`);

      // GET / → dashboard HTML
      if (req.method === 'GET' && (url.pathname === '/' || url.pathname === '/index.html')) {
        await handleDashboard(cfg, res);
        return;
      }
      // POST /api/move → writeback
      if (req.method === 'POST' && url.pathname === '/api/move') {
        await handleMove(cfg, req, res);
        return;
      }
      // POST /api/image → attach image to article
      if (req.method === 'POST' && url.pathname === '/api/image') {
        await handleImage(cfg, req, res);
        return;
      }
      // GET /api/next → stage-aware action queue (auto-ops only)
      if (req.method === 'GET' && url.pathname === '/api/next') {
        await handleNext(cfg, res);
        return;
      }
      // GET /api/article/:filename → raw markdown + metadata (drives reader drawer)
      if (req.method === 'GET' && url.pathname.startsWith('/api/article/')) {
        const filename = decodeURIComponent(url.pathname.slice('/api/article/'.length));
        await handleArticle(cfg, filename, res);
        return;
      }
      // POST /api/highlight → save a user highlight from the reader
      if (req.method === 'POST' && url.pathname === '/api/highlight') {
        await handleHighlightCreate(cfg, req, res);
        return;
      }
      // GET /api/highlights[?filename=X] → list saved highlights (Claude reads this too)
      if (req.method === 'GET' && url.pathname === '/api/highlights') {
        await handleHighlightList(cfg, url, res);
        return;
      }
      // GET /api/health
      if (req.method === 'GET' && url.pathname === '/api/health') {
        await handleHealth(cfg, res);
        return;
      }
      // 404
      sendJson(res, 404, { error: 'Not found' });
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err);
      sendJson(res, 500, { error: msg });
    }
  });

  server.listen(cfg.port, '127.0.0.1', () => {
    const url = `http://127.0.0.1:${cfg.port}/`;
    console.log(`┌─ Shipped. Dashboard (live)`);
    console.log(`│  issue       : ${cfg.issue}`);
    console.log(`│  content     : ${contentRoot}`);
    console.log(`│  url         : ${url}`);
    console.log(`│  writeback   : POST /api/move (drag-drop persists to frontmatter)`);
    console.log(`│  reader      : GET  /api/article/:filename (inline reader popup)`);
    console.log(`│  highlights  : POST /api/highlight · GET /api/highlights?filename=X`);
    console.log(`│                persisted to: content/articles/issue-${cfg.issue}/_highlights.jsonl`);
    console.log(`└─ Ctrl+C to stop`);
  });
}

main().catch(err => {
  console.error('Server failed to start:', err);
  process.exit(1);
});
