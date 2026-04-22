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
import { readdirSync } from 'node:fs';
import { resolve } from 'node:path';
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
    sendJson(res, 200, {
      issue: dashboard.issue,
      ...dashboard.nextActions,
    });
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    sendJson(res, 500, { error: msg });
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
    console.log(`└─ Ctrl+C to stop`);
  });
}

main().catch(err => {
  console.error('Server failed to start:', err);
  process.exit(1);
});
