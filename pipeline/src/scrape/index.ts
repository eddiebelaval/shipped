/**
 * Main orchestrator for the beat scraper.
 *
 * Strategy (preferred → fallback):
 *   1. X MCP — X's official MCP server (if X_MCP_URL is configured).
 *   2. X API — X API v2 timeline pull (if X_API_BEARER_TOKEN is present).
 *   3. Nitter — best-effort HTML fallback.
 *   4. If all fail, return an empty result with `failureReason` set -- the
 *      caller (/shipped) decides whether that's tolerable.
 *
 * Enrichment (the lever against thin issues): when `enrich` is on AND the X
 * MCP source is configured, a search sweep runs on top of whichever timeline
 * source won, merging in novel cross-lab / third-party posts. See
 * content/DAILY.md for why more signal is the cure for the collapsed issue.
 *
 * Always writes output via `output.ts`. Logs progress to stdout.
 */

import { NitterClient } from './nitter.js';
import { writeScrapeResult, outputDirForUser } from './output.js';
import { searchTermsForHandle } from './sources.js';
import {
  DEFAULT_SCRAPE_OPTIONS,
  type ScrapedTweet,
  type ScrapeOptions,
  type ScrapeResult,
} from './types.js';
import { MissingTokenError, XApiClient, XApiError } from './x-api.js';
import { MissingMcpConfigError, XMcpClient, XMcpError, mergeNovel } from './x-mcp.js';

export interface ScrapeRunOptions extends Partial<ScrapeOptions> {
  /** If true, do not write output files. Useful for `--dry`. */
  dry?: boolean;
  /** Override fetch (used for tests). */
  fetchImpl?: typeof fetch;
  /** Override the X API token (defaults to env). */
  xApiToken?: string;
  /** Override the X MCP endpoint (defaults to env X_MCP_URL). */
  xMcpUrl?: string;
  /** Override the X MCP token (defaults to env X_MCP_BEARER_TOKEN). */
  xMcpToken?: string;
  /** If true, disable the X MCP source even when configured. */
  noMcp?: boolean;
  /** Inter-request delay overrides for tests. */
  delayMs?: number;
}

export type ScrapeRunResult = ScrapeResult & {
  /** Absolute path of the output file written, or null if `dry`. */
  outputPath: string | null;
};

export async function scrapeClaudedevs(
  options: ScrapeRunOptions = {},
): Promise<ScrapeRunResult> {
  const username = options.username ?? DEFAULT_SCRAPE_OPTIONS.username;
  const opts: ScrapeOptions = {
    username,
    sinceDays: options.sinceDays ?? DEFAULT_SCRAPE_OPTIONS.sinceDays,
    includeReplies:
      options.includeReplies ?? DEFAULT_SCRAPE_OPTIONS.includeReplies,
    includeRetweets:
      options.includeRetweets ?? DEFAULT_SCRAPE_OPTIONS.includeRetweets,
    enrich: options.enrich ?? false,
    searchTerms:
      options.searchTerms && options.searchTerms.length > 0
        ? options.searchTerms
        : searchTermsForHandle(username),
  };

  const scrapedAt = new Date().toISOString();
  const result: ScrapeResult = {
    tweets: [],
    scrapedAt,
    source: 'cached',
  };
  const failures: string[] = [];

  // ----- 0. Build the X MCP client (preferred source + enrichment) -----
  const mcpConfigured =
    !options.noMcp && Boolean(options.xMcpUrl ?? process.env['X_MCP_URL']);
  let mcpClient: XMcpClient | null = null;
  if (mcpConfigured) {
    try {
      const mcpOpts: ConstructorParameters<typeof XMcpClient>[0] = {};
      if (options.xMcpUrl !== undefined) mcpOpts.url = options.xMcpUrl;
      if (options.xMcpToken !== undefined) mcpOpts.token = options.xMcpToken;
      if (options.fetchImpl !== undefined) mcpOpts.fetchImpl = options.fetchImpl;
      if (options.delayMs !== undefined) mcpOpts.delayMs = options.delayMs;
      mcpClient = new XMcpClient(mcpOpts);
    } catch (err) {
      if (!(err instanceof MissingMcpConfigError)) {
        log(`[scrape] X MCP client init failed: ${describeError(err)}`);
        failures.push(`x-mcp: ${describeError(err)}`);
      }
      mcpClient = null;
    }
  }

  // ----- 1. Try X MCP timeline -----
  if (mcpClient) {
    try {
      log(`[scrape] Attempting X MCP for @${opts.username} (last ${opts.sinceDays}d)`);
      const tweets = await mcpClient.fetchTimeline(opts);
      result.tweets = tweets;
      result.source = 'x-mcp';
      log(`[scrape] X MCP success: ${tweets.length} posts`);
    } catch (err) {
      const reason = describeError(err);
      log(`[scrape] X MCP failed: ${reason}`);
      failures.push(`x-mcp: ${reason}`);
    }
  } else if (!options.noMcp) {
    log('[scrape] X_MCP_URL not set; skipping X MCP');
  }

  // ----- 2. Try X API (only if X MCP didn't already win) -----
  if (result.source !== 'x-mcp') {
    const tokenAvailable = Boolean(
      options.xApiToken ?? process.env['X_API_BEARER_TOKEN'],
    );
    if (tokenAvailable) {
      try {
        log(`[scrape] Attempting X API for @${opts.username} (last ${opts.sinceDays}d)`);
        const xClientOpts: ConstructorParameters<typeof XApiClient>[0] = {};
        if (options.xApiToken !== undefined) xClientOpts.token = options.xApiToken;
        if (options.fetchImpl !== undefined) xClientOpts.fetchImpl = options.fetchImpl;
        if (options.delayMs !== undefined) xClientOpts.delayMs = options.delayMs;
        const xClient = new XApiClient(xClientOpts);
        const userId = await xClient.resolveUserId(opts.username);
        const tweets = await xClient.fetchTimeline(userId, opts);
        result.tweets = tweets;
        result.source = 'x-api';
        log(`[scrape] X API success: ${tweets.length} tweets`);
      } catch (err) {
        const reason = describeError(err);
        log(`[scrape] X API failed: ${reason}`);
        failures.push(`x-api: ${reason}`);
      }
    } else {
      log('[scrape] X_API_BEARER_TOKEN not set; skipping X API');
      failures.push('x-api: token missing');
    }
  }

  // ----- 3. Fall back to Nitter (only if no live timeline yet) -----
  if (result.source === 'cached') {
    try {
      log(`[scrape] Attempting Nitter fallback for @${opts.username}`);
      const nitterOpts: ConstructorParameters<typeof NitterClient>[0] = {};
      if (options.fetchImpl !== undefined) nitterOpts.fetchImpl = options.fetchImpl;
      if (options.delayMs !== undefined) nitterOpts.delayMs = options.delayMs;
      const nitter = new NitterClient(nitterOpts);
      const tweets = await nitter.fetchTimeline(opts);
      if (tweets.length > 0) {
        result.tweets = tweets;
        result.source = 'nitter';
        log(`[scrape] Nitter success: ${tweets.length} tweets`);
      } else {
        log('[scrape] Nitter returned 0 tweets');
        failures.push('nitter: empty result');
      }
    } catch (err) {
      const reason = describeError(err);
      log(`[scrape] Nitter failed: ${reason}`);
      failures.push(`nitter: ${reason}`);
    }
  }

  // ----- 4. Enrichment sweep (X MCP search) -----
  // Runs on top of whichever timeline source won. This is the lever against
  // thin issues: search brings in cross-lab / third-party posts the single
  // feed never sees. MCP-only; a no-op when X MCP isn't configured.
  if (opts.enrich && mcpClient) {
    const terms = opts.searchTerms ?? [];
    log(`[scrape] Enriching @${opts.username} via X MCP search: ${terms.join(', ')}`);
    const found: ScrapedTweet[] = [];
    for (const term of terms) {
      try {
        const hits = await mcpClient.searchPosts(term, opts);
        found.push(...hits);
      } catch (err) {
        log(`[scrape] X MCP search "${term}" failed: ${describeError(err)}`);
        failures.push(`x-mcp-search(${term}): ${describeError(err)}`);
      }
    }
    if (found.length > 0) {
      const { merged, added } = mergeNovel(result.tweets, found);
      result.tweets = merged;
      result.enrichment = { added, terms };
      // A pure-enrichment result (no live timeline) still came from X MCP.
      if (result.source === 'cached' && merged.length > 0) result.source = 'x-mcp';
      log(`[scrape] Enrichment merged ${added} novel post(s)`);
    } else {
      result.enrichment = { added: 0, terms };
    }
  }

  // ----- 5. Failure path -----
  if (result.tweets.length === 0 && result.source === 'cached') {
    result.failureReason =
      failures.length > 0
        ? `All sources failed: ${failures.join('; ')}`
        : 'All sources returned no tweets';
  }

  // ----- 4. Write output -----
  let outputPath: string | null = null;
  if (!options.dry) {
    try {
      outputPath = await writeScrapeResult(result, {
        outputDir: outputDirForUser(opts.username),
      });
      log(`[scrape] Wrote ${outputPath}`);
    } catch (err) {
      log(`[scrape] Failed to write output: ${describeError(err)}`);
    }
  } else {
    log('[scrape] --dry: skipping output write');
  }

  return { ...result, outputPath };
}

function log(msg: string): void {
  // eslint-disable-next-line no-console
  console.log(msg);
}

function describeError(err: unknown): string {
  if (err instanceof MissingTokenError) return 'token missing';
  if (err instanceof MissingMcpConfigError) return 'X_MCP_URL missing';
  if (err instanceof XApiError) {
    return `X API error ${err.status}: ${err.message}`;
  }
  if (err instanceof XMcpError) {
    return err.status ? `X MCP error ${err.status}: ${err.message}` : err.message;
  }
  if (err instanceof Error) return err.message;
  return String(err);
}

// Re-exports for convenience.
export type {
  CrossReferenceResult,
  ScrapedTweet,
  ScrapeOptions,
  ScrapeResult,
  TweetEngagement,
  TweetMatch,
} from './types.js';
export {
  crossReferenceTweets,
  parseReleaseLog,
  normalizeUrl,
  extractUrlsFromMarkdown,
  type ReleaseEntry,
  type CrossReferenceOptions,
} from './cross-reference.js';
export {
  XMcpClient,
  XMcpError,
  MissingMcpConfigError,
  mergeNovel,
  normalizeMcpPost,
  extractPostArray,
  decodeToolResult,
  parseRpcBody,
} from './x-mcp.js';
export { searchTermsForHandle } from './sources.js';
