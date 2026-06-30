/**
 * Type definitions for the @claudedevs X (Twitter) scraper.
 *
 * The scraper feeds the Shipped. magazine pipeline as a SUPPLEMENTAL source.
 * It only ever READS from X — never writes/posts. See README.md for full architecture.
 */

/**
 * Engagement metrics on a tweet at scrape time.
 * Snapshotted at scrape — these change over time but we don't track changes.
 */
export interface TweetEngagement {
  likes: number;
  reposts: number;
  replies: number;
}

/**
 * A normalized tweet from any source (X API, Nitter, cache).
 * This is the canonical shape consumed by /shipped's source-gathering step.
 */
export interface ScrapedTweet {
  /** Tweet ID (string to preserve precision; X IDs exceed Number.MAX_SAFE_INTEGER). */
  id: string;

  /** ISO 8601 timestamp of when the tweet was posted. */
  date: string;

  /** Full text of the tweet (with URLs unexpanded; expanded versions are in `links`). */
  text: string;

  /** Canonical URL to the tweet (e.g. https://x.com/claudedevs/status/{id}). */
  url: string;

  /**
   * Handle of the post's author, without the `@`. For a timeline pull this is
   * the feed being scraped; for enrichment search hits (X MCP) it is whoever
   * actually posted — which is how third-party / cross-lab signal carries its
   * provenance instead of masquerading as the anchor feed. Optional for
   * backward compatibility: consumers should fall back to the feed handle.
   */
  author?: string;

  /** Expanded URLs found in the tweet (excluding the tweet's own URL). */
  links: string[];

  /** Hashtags found in the tweet, lowercased, without the `#` prefix. */
  hashtags: string[];

  /** Attachment types: "image", "video", "gif", or "link". Empty if none. */
  attachments: string[];

  /** ID of the root tweet if this is part of a thread; null otherwise. */
  thread_root_id: string | null;

  /** True if this tweet is a continuation of a thread (i.e. not the root). */
  is_thread_continuation: boolean;

  /** Engagement at scrape time. */
  engagement: TweetEngagement;
}

/**
 * Options controlling a scrape run.
 */
export interface ScrapeOptions {
  /** Username to scrape (no `@`). Defaults to "claudedevs". */
  username: string;

  /** Number of days to look back from now. Defaults to 7. */
  sinceDays: number;

  /**
   * Whether to include replies. Default false.
   * If true, only replies that thread off the user's own tweets are included.
   */
  includeReplies: boolean;

  /** Whether to include retweets. Default false. */
  includeRetweets: boolean;

  /**
   * Whether to run the X MCP search-enrichment sweep after the timeline pull.
   * Off by default. Requires the X MCP source to be configured (X_MCP_URL);
   * a no-op otherwise. This is the lever against thin issues: the timeline
   * pull is one feed, the search sweep brings in the cross-lab/third-party
   * signal the front-of-book digs (see content/DAILY.md, lever 6).
   */
  enrich?: boolean;

  /**
   * Terms the enrichment sweep searches X for. Defaults to the lab/product
   * terms derived from the handle (see scrape/sources.ts). Ignored unless
   * `enrich` is true.
   */
  searchTerms?: string[];
}

/**
 * The result of a scrape run, regardless of which source succeeded.
 */
export interface ScrapeResult {
  /** Normalized tweets, deduplicated by id, sorted newest-first. */
  tweets: ScrapedTweet[];

  /** ISO 8601 timestamp of when the scrape ran. */
  scrapedAt: string;

  /**
   * Which source produced the timeline. "x-mcp" is the preferred source (X's
   * MCP server); "x-api" and "nitter" are fallbacks; "cached" means no live
   * source was reachable.
   */
  source: 'x-mcp' | 'x-api' | 'nitter' | 'cached';

  /**
   * Human-readable reason if every live source failed and cache was empty.
   * Set only when `tweets.length === 0` and source is "cached".
   */
  failureReason?: string;

  /**
   * Set when the X MCP search-enrichment sweep ran. `added` is how many novel
   * posts the sweep merged on top of the timeline; `terms` is what it searched.
   */
  enrichment?: {
    added: number;
    terms: string[];
  };
}

/**
 * A tweet matched against an existing Release Log entry.
 * The matched URL is the bridge — same URL implies same release.
 */
export interface TweetMatch {
  tweet: ScrapedTweet;

  /** The URL from the tweet that matched. */
  matchedUrl: string;

  /** Identifier of the existing release entry (e.g. heading slug, line number, or hash). */
  entryId: string;
}

/**
 * Cross-reference output: how scraped tweets relate to existing log entries.
 */
export interface CrossReferenceResult {
  /** Tweets that share a URL with an existing release entry — supporting context. */
  matched: TweetMatch[];

  /** Tweets with URLs that don't appear in any existing entry — candidates for new entries. */
  novel: ScrapedTweet[];

  /**
   * Tweets with no URLs but mention a feature/version (e.g. "Opus 4.7", "1.5.0").
   * Editorial flag — needs human review.
   */
  context_only: ScrapedTweet[];
}

/**
 * Default scrape options for the @claudedevs feed.
 */
export const DEFAULT_SCRAPE_OPTIONS: ScrapeOptions = {
  username: 'claudedevs',
  sinceDays: 7,
  includeReplies: false,
  includeRetweets: false,
};
