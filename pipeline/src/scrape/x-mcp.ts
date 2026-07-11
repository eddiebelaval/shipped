/**
 * X (Twitter) MCP source for the Shipped. beat scraper.
 *
 * X ships an official MCP server. This is the client that speaks to it — the
 * preferred source ahead of the raw X API v2 timeline pull (x-api.ts) and the
 * Nitter HTML fallback (nitter.ts). It does two things the bare timeline pull
 * cannot:
 *
 *   1. fetchTimeline()  — a lab's own posts, same shape as the other sources.
 *   2. searchPosts()    — the *enrichment* sweep. Search across X for posts
 *                         about a lab's products from anyone, not just the lab.
 *                         This is the well the front-of-book digs against the
 *                         recurring "issue collapsed to two paragraphs" failure
 *                         (content/DAILY.md): cross-lab and third-party signal
 *                         the single-feed pull never sees.
 *
 * Transport: MCP Streamable HTTP. JSON-RPC 2.0 over POST, built-in `fetch`,
 * no SDK — same dependency-free posture as x-api.ts. The server may answer
 * either `application/json` or an SSE-framed `text/event-stream`; we parse
 * both. The `initialize` handshake runs once per client and the session id it
 * returns (if any) rides on every subsequent request.
 *
 * Read-only. Never posts. Configured by X_MCP_URL + X_MCP_BEARER_TOKEN; on a
 * missing URL it throws MissingMcpConfigError and the caller falls back to the
 * X API exactly as it falls back from the API to Nitter.
 */

import { normalizeUrl } from './cross-reference.js';
import type {
  ScrapedTweet,
  ScrapeOptions,
  TweetEngagement,
} from './types.js';

/** MCP spec version we negotiate. Servers downgrade to what they support. */
const MCP_PROTOCOL_VERSION = '2025-06-18';
const REQUEST_DELAY_MS = 1000; // 1 req/sec ceiling, matching x-api.ts
const REQUEST_TIMEOUT_MS = 15_000;

/** Default tool names on X's MCP server. Override per-deployment if they drift. */
const DEFAULT_TIMELINE_TOOL = 'get_user_posts';
const DEFAULT_SEARCH_TOOL = 'search_posts';

/** Thrown when X_MCP_URL is not configured. Caller should fall back to x-api. */
export class MissingMcpConfigError extends Error {
  constructor() {
    super('X_MCP_URL not set in environment');
    this.name = 'MissingMcpConfigError';
  }
}

/** Thrown for transport failures and JSON-RPC / tool errors from the server. */
export class XMcpError extends Error {
  constructor(
    message: string,
    public readonly status?: number,
    public readonly body?: string,
  ) {
    super(message);
    this.name = 'XMcpError';
  }
}

/* -------------------------------------------------------------------------- */
/* JSON-RPC + MCP wire shapes (only the fields we read)                       */
/* -------------------------------------------------------------------------- */

interface JsonRpcError {
  code: number;
  message: string;
  data?: unknown;
}

interface JsonRpcResponse<T> {
  jsonrpc: '2.0';
  id: number | string | null;
  result?: T;
  error?: JsonRpcError;
}

interface McpTextContent {
  type: 'text';
  text: string;
}

interface McpToolResult {
  /** Content blocks. We read the first `text` block as a JSON payload. */
  content?: Array<McpTextContent | { type: string; [k: string]: unknown }>;
  /** Some servers also return a parsed object directly. Preferred if present. */
  structuredContent?: unknown;
  /** MCP marks tool-level failures here rather than as a JSON-RPC error. */
  isError?: boolean;
}

/**
 * One post as the X MCP server returns it. The schema is external and still
 * settling, so every field is optional and `normalizeMcpPost` is defensive
 * about the spellings we've seen (`text`/`content`, `created_at`/`createdAt`,
 * `public_metrics`/`engagement`, …).
 */
interface XMcpPost {
  id?: string | number;
  rest_id?: string | number;
  post_id?: string | number;
  text?: string;
  content?: string;
  full_text?: string;
  created_at?: string;
  createdAt?: string;
  date?: string;
  url?: string;
  author?: string | { username?: string; handle?: string; screen_name?: string };
  username?: string;
  handle?: string;
  links?: string[];
  urls?: Array<string | { url?: string; expanded_url?: string }>;
  hashtags?: Array<string | { tag?: string }>;
  media?: Array<string | { type?: string }>;
  in_reply_to_status_id?: string | number;
  reply_to_id?: string | number;
  public_metrics?: {
    like_count?: number;
    retweet_count?: number;
    repost_count?: number;
    reply_count?: number;
  };
  engagement?: { likes?: number; reposts?: number; replies?: number };
}

/* -------------------------------------------------------------------------- */
/* Client                                                                     */
/* -------------------------------------------------------------------------- */

export interface XMcpClientOptions {
  /** MCP server endpoint. Defaults to env X_MCP_URL. */
  url?: string;
  /** Optional bearer token. Defaults to env X_MCP_BEARER_TOKEN. */
  token?: string;
  /** Override fetch (used for tests). */
  fetchImpl?: typeof fetch;
  /** Override the inter-request delay in ms (used for tests). */
  delayMs?: number;
  /** Per-request timeout in ms. */
  timeoutMs?: number;
  /** Timeline tool name. Defaults to env X_MCP_TIMELINE_TOOL or get_user_posts. */
  timelineTool?: string;
  /** Search tool name. Defaults to env X_MCP_SEARCH_TOOL or search_posts. */
  searchTool?: string;
}

export class XMcpClient {
  private readonly url: string;
  private readonly token: string | undefined;
  private readonly fetchImpl: typeof fetch;
  private readonly delayMs: number;
  private readonly timeoutMs: number;
  private readonly timelineTool: string;
  private readonly searchTool: string;

  private sessionId: string | undefined;
  private initialized = false;
  private rpcId = 0;
  private lastRequestAt = 0;

  constructor(options: XMcpClientOptions = {}) {
    const url = options.url ?? process.env['X_MCP_URL'];
    if (!url) {
      throw new MissingMcpConfigError();
    }
    this.url = url;
    this.token = options.token ?? process.env['X_MCP_BEARER_TOKEN'];
    this.fetchImpl = options.fetchImpl ?? fetch;
    this.delayMs = options.delayMs ?? REQUEST_DELAY_MS;
    this.timeoutMs = options.timeoutMs ?? REQUEST_TIMEOUT_MS;
    this.timelineTool =
      options.timelineTool ??
      process.env['X_MCP_TIMELINE_TOOL'] ??
      DEFAULT_TIMELINE_TOOL;
    this.searchTool =
      options.searchTool ??
      process.env['X_MCP_SEARCH_TOOL'] ??
      DEFAULT_SEARCH_TOOL;
  }

  /**
   * Fetch a lab's own recent posts via the MCP timeline tool. Mapped to the
   * canonical ScrapedTweet shape, filtered to the lookback window, newest-first.
   */
  async fetchTimeline(options: ScrapeOptions): Promise<ScrapedTweet[]> {
    const startTime = sinceIso(options.sinceDays);
    const raw = await this.callTool(this.timelineTool, {
      username: options.username,
      handle: options.username,
      max_results: 100,
      start_time: startTime,
      since_days: options.sinceDays,
      exclude_replies: !options.includeReplies,
      exclude_retweets: !options.includeRetweets,
    });
    return this.shape(raw, options.username, options.sinceDays);
  }

  /**
   * The enrichment sweep: search X for posts matching `query` (a lab/product
   * term), regardless of author. Hits carry their real author so third-party
   * and cross-lab signal is attributed honestly.
   */
  async searchPosts(query: string, options: ScrapeOptions): Promise<ScrapedTweet[]> {
    const startTime = sinceIso(options.sinceDays);
    const raw = await this.callTool(this.searchTool, {
      query,
      max_results: 50,
      start_time: startTime,
      since_days: options.sinceDays,
    });
    return this.shape(raw, options.username, options.sinceDays);
  }

  /* ---------------------------------------------------------------------- */
  /* MCP plumbing                                                           */
  /* ---------------------------------------------------------------------- */

  /** Run the MCP handshake once: initialize + initialized notification. */
  private async ensureInitialized(): Promise<void> {
    if (this.initialized) return;
    await this.rpc('initialize', {
      protocolVersion: MCP_PROTOCOL_VERSION,
      capabilities: {},
      clientInfo: { name: 'shipped-pipeline', version: '0.1' },
    });
    // Per spec the client confirms with a notification (no response expected).
    await this.notify('notifications/initialized', {});
    this.initialized = true;
  }

  /** Invoke a tool and return its decoded payload (array of post objects, etc). */
  private async callTool(
    name: string,
    args: Record<string, unknown>,
  ): Promise<unknown> {
    await this.ensureInitialized();
    const result = await this.rpc<McpToolResult>('tools/call', {
      name,
      arguments: args,
    });
    if (result?.isError) {
      throw new XMcpError(`X MCP tool "${name}" reported an error`);
    }
    return decodeToolResult(result);
  }

  /** A JSON-RPC request that expects a response. */
  private async rpc<T = unknown>(
    method: string,
    params: Record<string, unknown>,
  ): Promise<T> {
    const id = (this.rpcId += 1);
    const text = await this.post({ jsonrpc: '2.0', id, method, params });
    const parsed = parseRpcBody<T>(text);
    if (parsed?.error) {
      throw new XMcpError(
        `X MCP error ${parsed.error.code}: ${parsed.error.message}`,
      );
    }
    if (parsed?.result === undefined) {
      throw new XMcpError(`X MCP returned no result for ${method}`);
    }
    return parsed.result;
  }

  /** A JSON-RPC notification — fire and forget, body ignored. */
  private async notify(
    method: string,
    params: Record<string, unknown>,
  ): Promise<void> {
    await this.post({ jsonrpc: '2.0', method, params }, { tolerateEmpty: true });
  }

  /** POST one JSON-RPC message; capture the session id; return the raw body. */
  private async post(
    message: Record<string, unknown>,
    opts: { tolerateEmpty?: boolean } = {},
  ): Promise<string> {
    await this.throttle();

    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      Accept: 'application/json, text/event-stream',
      'MCP-Protocol-Version': MCP_PROTOCOL_VERSION,
      'User-Agent': 'shipped-pipeline/0.1 (+https://id8labs.app/shipped)',
    };
    if (this.token) headers['Authorization'] = `Bearer ${this.token}`;
    if (this.sessionId) headers['Mcp-Session-Id'] = this.sessionId;

    // The abort timer must stay armed through the *body* read, not just the
    // header round-trip. On a Streamable HTTP / SSE response `fetch` resolves
    // as soon as headers arrive, so clearing the timer right after would leave
    // a stalled or never-closing stream to hang `safeReadText` forever — and,
    // because the MCP call would then never reject, suppress fallback to the X
    // API / Nitter. Keep one timer over the whole exchange; on timeout the
    // abort collapses the body read to '' and surfaces as an error the caller
    // can fall back from.
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), this.timeoutMs);
    try {
      let res: Response;
      try {
        res = await this.fetchImpl(this.url, {
          method: 'POST',
          headers,
          body: JSON.stringify(message),
          signal: controller.signal,
        });
      } catch (err) {
        throw new XMcpError(`X MCP request failed: ${(err as Error).message}`);
      }

      const sid = res.headers.get('mcp-session-id');
      if (sid) this.sessionId = sid;

      if (!res.ok) {
        const body = await safeReadText(res);
        throw new XMcpError(
          `X MCP HTTP ${res.status}: ${res.statusText}`,
          res.status,
          body,
        );
      }

      const body = await safeReadText(res);
      if (!body && !opts.tolerateEmpty) {
        throw new XMcpError('X MCP returned an empty body', res.status);
      }
      return body;
    } finally {
      clearTimeout(timer);
    }
  }

  private async throttle(): Promise<void> {
    const elapsed = Date.now() - this.lastRequestAt;
    if (elapsed < this.delayMs) {
      await sleep(this.delayMs - elapsed);
    }
    this.lastRequestAt = Date.now();
  }

  /** Decode → normalize → window-filter → newest-first. */
  private shape(
    raw: unknown,
    fallbackHandle: string,
    sinceDays: number,
  ): ScrapedTweet[] {
    const cutoff = Date.now() - sinceDays * 24 * 60 * 60 * 1000;
    const posts = extractPostArray(raw);
    const out: ScrapedTweet[] = [];
    for (const p of posts) {
      const tweet = normalizeMcpPost(p, fallbackHandle);
      if (!tweet) continue;
      const ts = Date.parse(tweet.date);
      // Drop only posts with a *real* date older than the window. Undated posts
      // (schema drift / a renamed date field) are stamped at the epoch by
      // normalizeMcpPost; keep those rather than treat drift as an empty week,
      // which would also mask the fallback to X API / Nitter. `ts > 0` excludes
      // that epoch sentinel from the cutoff.
      if (Number.isFinite(ts) && ts > 0 && ts < cutoff) continue;
      out.push(tweet);
    }
    const seen = new Set<string>();
    return out
      .filter((t) => {
        if (seen.has(t.id)) return false;
        seen.add(t.id);
        return true;
      })
      .sort((a, b) => (a.date < b.date ? 1 : a.date > b.date ? -1 : 0));
  }
}

/* -------------------------------------------------------------------------- */
/* Decoding helpers (exported for tests)                                      */
/* -------------------------------------------------------------------------- */

/**
 * Parse a JSON-RPC response body. The Streamable HTTP transport may return a
 * plain JSON object or an SSE stream (`event: message\ndata: {...}`); handle both.
 */
export function parseRpcBody<T>(body: string): JsonRpcResponse<T> | null {
  const trimmed = body.trim();
  if (!trimmed) return null;
  if (trimmed.startsWith('{') || trimmed.startsWith('[')) {
    return safeJson<JsonRpcResponse<T>>(trimmed);
  }
  // SSE framing: take the last non-empty `data:` line.
  const dataLines = trimmed
    .split(/\r?\n/)
    .filter((l) => l.startsWith('data:'))
    .map((l) => l.slice(5).trim())
    .filter((l) => l && l !== '[DONE]');
  const last = dataLines[dataLines.length - 1];
  return last ? safeJson<JsonRpcResponse<T>>(last) : null;
}

/** Pull the tool's JSON payload out of an MCP tools/call result. */
export function decodeToolResult(result: McpToolResult | undefined): unknown {
  if (!result) return null;
  if (result.structuredContent !== undefined) return result.structuredContent;
  for (const block of result.content ?? []) {
    if (block.type === 'text' && typeof (block as McpTextContent).text === 'string') {
      const parsed = safeJson<unknown>((block as McpTextContent).text);
      if (parsed !== null) return parsed;
      return (block as McpTextContent).text;
    }
  }
  return null;
}

/** Find the array of posts inside whatever envelope the tool returned. */
export function extractPostArray(payload: unknown): XMcpPost[] {
  if (Array.isArray(payload)) return payload as XMcpPost[];
  if (payload && typeof payload === 'object') {
    const obj = payload as Record<string, unknown>;
    for (const key of ['posts', 'tweets', 'data', 'results', 'items']) {
      if (Array.isArray(obj[key])) return obj[key] as XMcpPost[];
    }
  }
  return [];
}

/**
 * Map one X MCP post → ScrapedTweet. Returns null when there isn't even an id
 * to anchor on. Defensive about the field spellings the server might use.
 */
export function normalizeMcpPost(
  p: XMcpPost,
  fallbackHandle: string,
): ScrapedTweet | null {
  const id = firstString(p.id, p.rest_id, p.post_id);
  if (!id) return null;

  const text = firstString(p.text, p.content, p.full_text) ?? '';
  const date = toIso(firstString(p.created_at, p.createdAt, p.date));
  const author = resolveAuthor(p, fallbackHandle);

  const links = extractLinks(p, id);
  const hashtags = (p.hashtags ?? [])
    .map((h) => (typeof h === 'string' ? h : h.tag ?? ''))
    .map((t) => t.replace(/^#/, '').toLowerCase())
    .filter(Boolean);

  const attachments = extractAttachments(p);
  if (attachments.length === 0 && links.length > 0) attachments.push('link');

  const replyTo = firstString(p.in_reply_to_status_id, p.reply_to_id);
  const engagement: TweetEngagement = {
    likes: p.public_metrics?.like_count ?? p.engagement?.likes ?? 0,
    reposts:
      p.public_metrics?.retweet_count ??
      p.public_metrics?.repost_count ??
      p.engagement?.reposts ??
      0,
    replies: p.public_metrics?.reply_count ?? p.engagement?.replies ?? 0,
  };

  return {
    id,
    date,
    text,
    url: p.url ?? `https://x.com/${author}/status/${id}`,
    author,
    links,
    hashtags,
    attachments,
    thread_root_id: replyTo ?? null,
    is_thread_continuation: Boolean(replyTo),
    engagement,
  };
}

function resolveAuthor(p: XMcpPost, fallbackHandle: string): string {
  let raw: string | undefined;
  if (typeof p.author === 'string') raw = p.author;
  else if (p.author && typeof p.author === 'object') {
    raw = p.author.username ?? p.author.handle ?? p.author.screen_name;
  }
  raw = raw ?? p.username ?? p.handle ?? fallbackHandle;
  return raw.replace(/^@/, '');
}

function extractLinks(p: XMcpPost, id: string): string[] {
  const out: string[] = [];
  for (const l of p.links ?? []) {
    if (typeof l === 'string') out.push(l);
  }
  for (const u of p.urls ?? []) {
    const url = typeof u === 'string' ? u : u.expanded_url ?? u.url;
    if (url) out.push(url);
  }
  // Drop self-links to the post itself.
  return out.filter((u) => !u.includes(`/status/${id}`));
}

function extractAttachments(p: XMcpPost): string[] {
  const out: string[] = [];
  for (const m of p.media ?? []) {
    const type = typeof m === 'string' ? m : m.type ?? '';
    if (/photo|image/i.test(type)) out.push('image');
    else if (/video/i.test(type)) out.push('video');
    else if (/gif/i.test(type)) out.push('gif');
  }
  return out;
}

/* -------------------------------------------------------------------------- */
/* Merge helper — used by the orchestrator's enrichment step                  */
/* -------------------------------------------------------------------------- */

/**
 * Merge `extra` posts into `base`, dropping anything already present by id or
 * by a shared normalized link. Returns a fresh newest-first array and the
 * count of genuinely novel posts added.
 */
export function mergeNovel(
  base: ScrapedTweet[],
  extra: ScrapedTweet[],
): { merged: ScrapedTweet[]; added: number } {
  const seenIds = new Set(base.map((t) => t.id));
  const seenUrls = new Set<string>();
  for (const t of base) {
    for (const l of t.links) seenUrls.add(normalizeUrl(l));
  }

  const merged = [...base];
  let added = 0;
  for (const t of extra) {
    if (seenIds.has(t.id)) continue;
    const overlaps = t.links.some((l) => seenUrls.has(normalizeUrl(l)));
    if (overlaps) continue;
    seenIds.add(t.id);
    for (const l of t.links) seenUrls.add(normalizeUrl(l));
    merged.push(t);
    added += 1;
  }

  merged.sort((a, b) => (a.date < b.date ? 1 : a.date > b.date ? -1 : 0));
  return { merged, added };
}

/* -------------------------------------------------------------------------- */
/* Small utilities                                                            */
/* -------------------------------------------------------------------------- */

function sinceIso(sinceDays: number): string {
  return new Date(Date.now() - sinceDays * 24 * 60 * 60 * 1000).toISOString();
}

function firstString(...vals: Array<string | number | undefined>): string | undefined {
  for (const v of vals) {
    if (typeof v === 'string' && v.length > 0) return v;
    if (typeof v === 'number' && Number.isFinite(v)) return String(v);
  }
  return undefined;
}

function toIso(raw: string | undefined): string {
  if (!raw) return new Date(0).toISOString();
  const ts = Date.parse(raw);
  return Number.isFinite(ts) ? new Date(ts).toISOString() : new Date(0).toISOString();
}

function safeJson<T>(text: string): T | null {
  try {
    return JSON.parse(text) as T;
  } catch {
    return null;
  }
}

async function safeReadText(res: Response): Promise<string> {
  try {
    return await res.text();
  } catch {
    return '';
  }
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
