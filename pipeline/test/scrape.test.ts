/**
 * Tests for the @claudedevs scraper.
 *
 * All network calls are mocked. Real X API calls happen only via manual
 * `pnpm scrape` invocations -- never in the test suite.
 */

import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, readFile, rm, lstat, readlink } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

import {
  XApiClient,
  XApiError,
  MissingTokenError,
  normalizeTweet,
} from '../src/scrape/x-api.js';
import {
  NitterClient,
  parseNitterHtml,
  parseNitterDate,
} from '../src/scrape/nitter.js';
import {
  crossReferenceTweets,
  parseReleaseLog,
  normalizeUrl,
  extractUrlsFromMarkdown,
  type ReleaseEntry,
} from '../src/scrape/cross-reference.js';
import { writeScrapeResult, formatDateStamp } from '../src/scrape/output.js';
import type { ScrapedTweet, ScrapeResult } from '../src/scrape/types.js';
import { scrapeClaudedevs } from '../src/scrape/index.js';
import {
  XMcpClient,
  MissingMcpConfigError,
  parseRpcBody,
  decodeToolResult,
  extractPostArray,
  normalizeMcpPost,
  mergeNovel,
} from '../src/scrape/x-mcp.js';
import { searchTermsForHandle } from '../src/scrape/sources.js';

/* -------------------------------------------------------------------------- */
/* Helpers                                                                    */
/* -------------------------------------------------------------------------- */

function makeFetchStub(responses: Map<string | RegExp, unknown>): typeof fetch {
  return (async (input: RequestInfo | URL): Promise<Response> => {
    const url = typeof input === 'string' ? input : input.toString();
    for (const [pattern, body] of responses) {
      if (typeof pattern === 'string' ? url.includes(pattern) : pattern.test(url)) {
        if (body instanceof Response) return body;
        if (typeof body === 'string') {
          return new Response(body, {
            status: 200,
            headers: { 'content-type': 'text/html' },
          });
        }
        return new Response(JSON.stringify(body), {
          status: 200,
          headers: { 'content-type': 'application/json' },
        });
      }
    }
    return new Response('not found', { status: 404 });
  }) as unknown as typeof fetch;
}

function makeTweet(overrides: Partial<ScrapedTweet> = {}): ScrapedTweet {
  return {
    id: '1234',
    date: '2026-04-15T12:00:00.000Z',
    text: 'hello world',
    url: 'https://x.com/claudedevs/status/1234',
    links: [],
    hashtags: [],
    attachments: [],
    thread_root_id: null,
    is_thread_continuation: false,
    engagement: { likes: 0, reposts: 0, replies: 0 },
    ...overrides,
  };
}

/**
 * A fetch stub for the X MCP server. Routes JSON-RPC messages by method/tool
 * to the supplied tool payloads, wrapping each in an MCP text-content result.
 * Initialize returns an Mcp-Session-Id; notifications get a 202.
 */
function makeMcpFetch(opts: {
  tools: Record<string, (args: Record<string, unknown>) => unknown>;
  url?: string;
  failHttp?: number;
}): typeof fetch {
  const mcpUrl = opts.url ?? 'https://mcp.test/';
  return (async (input: RequestInfo | URL, init?: RequestInit): Promise<Response> => {
    const url = typeof input === 'string' ? input : input.toString();
    if (!url.startsWith(mcpUrl)) return new Response('not found', { status: 404 });
    if (opts.failHttp) {
      return new Response('mcp down', { status: opts.failHttp });
    }
    const msg = init?.body ? JSON.parse(String(init.body)) : {};
    if (msg.id === undefined) return new Response('', { status: 202 }); // notification
    let result: unknown = {};
    if (msg.method === 'initialize') {
      result = { protocolVersion: '2025-06-18', capabilities: {}, serverInfo: { name: 'x', version: '1' } };
    } else if (msg.method === 'tools/call') {
      const name = msg.params?.name as string;
      const args = (msg.params?.arguments ?? {}) as Record<string, unknown>;
      const tool = opts.tools[name];
      const payload = tool ? tool(args) : { posts: [] };
      result = { content: [{ type: 'text', text: JSON.stringify(payload) }] };
    }
    return new Response(JSON.stringify({ jsonrpc: '2.0', id: msg.id, result }), {
      status: 200,
      headers: { 'content-type': 'application/json', 'mcp-session-id': 'sess-test' },
    });
  }) as unknown as typeof fetch;
}

/** A recent ISO timestamp guaranteed inside any reasonable lookback window. */
function recentIso(): string {
  return new Date(Date.now() - 60 * 60 * 1000).toISOString();
}

/* -------------------------------------------------------------------------- */
/* X API                                                                      */
/* -------------------------------------------------------------------------- */

test('XApiClient throws MissingTokenError when no token is provided', () => {
  const previous = process.env['X_API_BEARER_TOKEN'];
  delete process.env['X_API_BEARER_TOKEN'];
  try {
    assert.throws(() => new XApiClient(), MissingTokenError);
  } finally {
    if (previous !== undefined) process.env['X_API_BEARER_TOKEN'] = previous;
  }
});

test('XApiClient resolves user id from username lookup', async () => {
  const fetchStub = makeFetchStub(
    new Map([
      [
        '/users/by/username/claudedevs',
        { data: { id: '999000111', username: 'claudedevs', name: 'Claude Devs' } },
      ],
    ]),
  );
  const client = new XApiClient({
    token: 'fake-token',
    fetchImpl: fetchStub,
    delayMs: 0,
  });
  const id = await client.resolveUserId('claudedevs');
  assert.equal(id, '999000111');
});

test('XApiClient surfaces 401 as XApiError with status', async () => {
  const fetchStub = (async () =>
    new Response('{"title":"Unauthorized"}', {
      status: 401,
    })) as unknown as typeof fetch;
  const client = new XApiClient({
    token: 'fake-token',
    fetchImpl: fetchStub,
    delayMs: 0,
  });
  await assert.rejects(
    () => client.resolveUserId('claudedevs'),
    (err: unknown) => {
      assert.ok(err instanceof XApiError);
      assert.equal((err as XApiError).status, 401);
      return true;
    },
  );
});

test('XApiClient surfaces 429 (rate limit) as XApiError', async () => {
  const fetchStub = (async () =>
    new Response('rate limited', { status: 429 })) as unknown as typeof fetch;
  const client = new XApiClient({
    token: 'fake-token',
    fetchImpl: fetchStub,
    delayMs: 0,
  });
  await assert.rejects(
    () => client.resolveUserId('x'),
    (err: unknown) => err instanceof XApiError && (err as XApiError).status === 429,
  );
});

test('XApiClient.fetchTimeline normalizes a paginated response', async () => {
  let call = 0;
  const fetchStub = (async (input: RequestInfo | URL): Promise<Response> => {
    const url = typeof input === 'string' ? input : input.toString();
    if (url.includes('/users/by/username/')) {
      return new Response(
        JSON.stringify({ data: { id: '1', username: 'claudedevs', name: 'C' } }),
        { status: 200 },
      );
    }
    call += 1;
    if (call === 1) {
      return new Response(
        JSON.stringify({
          data: [
            {
              id: '100',
              text: 'first tweet https://anthropic.com/news/x',
              created_at: '2026-04-15T10:00:00.000Z',
              public_metrics: { like_count: 5, retweet_count: 2, reply_count: 1 },
              entities: {
                urls: [
                  {
                    url: 'https://t.co/abc',
                    expanded_url: 'https://anthropic.com/news/x',
                  },
                ],
                hashtags: [{ tag: 'Claude' }],
              },
            },
          ],
          meta: { next_token: 'page2', result_count: 1 },
        }),
        { status: 200 },
      );
    }
    return new Response(
      JSON.stringify({
        data: [
          {
            id: '101',
            text: 'second',
            created_at: '2026-04-14T10:00:00.000Z',
            public_metrics: { like_count: 0, retweet_count: 0, reply_count: 0 },
          },
        ],
        meta: { result_count: 1 },
      }),
      { status: 200 },
    );
  }) as unknown as typeof fetch;

  const client = new XApiClient({
    token: 't',
    fetchImpl: fetchStub,
    delayMs: 0,
  });
  const userId = await client.resolveUserId('claudedevs');
  const tweets = await client.fetchTimeline(userId, {
    username: 'claudedevs',
    sinceDays: 7,
    includeReplies: false,
    includeRetweets: false,
  });
  assert.equal(tweets.length, 2);
  assert.equal(tweets[0]?.id, '100', 'newest first');
  assert.deepEqual(tweets[0]?.links, ['https://anthropic.com/news/x']);
  assert.deepEqual(tweets[0]?.hashtags, ['claude']);
  assert.equal(tweets[0]?.engagement.likes, 5);
});

test('normalizeTweet skips self-link and detects thread continuation', () => {
  const tweet = normalizeTweet(
    {
      id: '500',
      text: 'reply to root',
      created_at: '2026-04-15T00:00:00.000Z',
      public_metrics: { like_count: 1, retweet_count: 0, reply_count: 0 },
      referenced_tweets: [{ type: 'replied_to', id: '499' }],
      entities: {
        urls: [
          {
            url: 'https://t.co/self',
            expanded_url: 'https://twitter.com/i/web/status/500',
          },
          {
            url: 'https://t.co/real',
            expanded_url: 'https://docs.anthropic.com/x',
          },
        ],
      },
    },
    'claudedevs',
    new Map(),
  );
  assert.equal(tweet.is_thread_continuation, true);
  assert.equal(tweet.thread_root_id, '499');
  assert.deepEqual(tweet.links, ['https://docs.anthropic.com/x']);
});

/* -------------------------------------------------------------------------- */
/* Nitter                                                                     */
/* -------------------------------------------------------------------------- */

test('parseNitterHtml extracts a single tweet', () => {
  const html = `
    <div class="timeline-item ">
      <a class="tweet-link" href="/claudedevs/status/777#m"></a>
      <span class="tweet-date"><a title="Apr 15, 2026 2:23 PM UTC">2h</a></span>
      <div class="tweet-content media-body">Opus 4.7 ships tomorrow <a href="https://anthropic.com/news/opus-47" rel="nofollow">link</a></div>
      <a href="/search?q=%23opus47">#opus47</a>
      <span class="tweet-stat"><div>5</div></span>
      <span class="tweet-stat"><div>10</div></span>
      <span class="tweet-stat"><div>2</div></span>
      <span class="tweet-stat"><div>100</div></span>
      </div></div></div>
  `;
  const tweets = parseNitterHtml(html, 'claudedevs');
  assert.equal(tweets.length, 1);
  const t = tweets[0]!;
  assert.equal(t.id, '777');
  assert.match(t.text, /Opus 4\.7 ships tomorrow/);
  assert.deepEqual(t.links, ['https://anthropic.com/news/opus-47']);
  assert.deepEqual(t.hashtags, ['opus47']);
  assert.equal(t.engagement.replies, 5);
  assert.equal(t.engagement.reposts, 10);
  assert.equal(t.engagement.likes, 100);
});

test('parseNitterDate handles Nitter title strings', () => {
  const iso = parseNitterDate('Apr 15, 2026 2:23 PM UTC');
  assert.match(iso, /^2026-04-15T/);
  assert.equal(parseNitterDate(''), new Date(0).toISOString());
});

test('NitterClient walks mirror list and returns empty on all-failure', async () => {
  let attempts = 0;
  const fetchStub = (async (): Promise<Response> => {
    attempts += 1;
    return new Response('', { status: 503 });
  }) as unknown as typeof fetch;
  const client = new NitterClient({
    fetchImpl: fetchStub,
    delayMs: 0,
    timeoutMs: 1000,
    mirrors: ['https://a.example', 'https://b.example'],
  });
  const tweets = await client.fetchTimeline({
    username: 'claudedevs',
    sinceDays: 7,
    includeReplies: false,
    includeRetweets: false,
  });
  assert.equal(tweets.length, 0);
  assert.equal(attempts, 2);
});

test('NitterClient parses HTML when first mirror succeeds', async () => {
  const html = `
    <div class="timeline-item">
      <a class="tweet-link" href="/claudedevs/status/888#m"></a>
      <span class="tweet-date"><a title="${new Date().toUTCString()}">now</a></span>
      <div class="tweet-content media-body">hi</div>
      </div></div></div>
  `;
  const fetchStub = (async (): Promise<Response> =>
    new Response(html, { status: 200 })) as unknown as typeof fetch;
  const client = new NitterClient({
    fetchImpl: fetchStub,
    delayMs: 0,
    mirrors: ['https://a.example'],
  });
  const tweets = await client.fetchTimeline({
    username: 'claudedevs',
    sinceDays: 7,
    includeReplies: false,
    includeRetweets: false,
  });
  assert.equal(tweets.length, 1);
  assert.equal(tweets[0]?.id, '888');
});

/* -------------------------------------------------------------------------- */
/* Cross-reference                                                            */
/* -------------------------------------------------------------------------- */

test('normalizeUrl strips tracking params and trailing slash', () => {
  assert.equal(
    normalizeUrl('https://www.Anthropic.com/News/Opus/?utm_source=tw&id=1'),
    'https://anthropic.com/News/Opus?id=1',
  );
});

test('extractUrlsFromMarkdown picks up md, angle, and bare URLs', () => {
  const md = `
    See [the post](https://anthropic.com/news/x).
    Also <https://docs.anthropic.com/y>.
    And bare: https://github.com/anthropics/z
  `;
  const urls = extractUrlsFromMarkdown(md);
  assert.deepEqual(urls.sort(), [
    'https://anthropic.com/news/x',
    'https://docs.anthropic.com/y',
    'https://github.com/anthropics/z',
  ]);
});

test('parseReleaseLog buckets entries by ## headings', () => {
  const md = `
## Models
Opus 4.7 [post](https://anthropic.com/news/opus-47).

## SDKs
TypeScript SDK [v1.5](https://github.com/anthropics/sdk-ts).
`;
  const entries = parseReleaseLog(md);
  assert.equal(entries.length, 2);
  assert.equal(entries[0]?.id, 'models');
  assert.deepEqual(entries[0]?.urls, ['https://anthropic.com/news/opus-47']);
  assert.deepEqual(entries[1]?.urls, ['https://github.com/anthropics/sdk-ts']);
});

test('crossReferenceTweets buckets matched / novel / context_only', () => {
  const entries: ReleaseEntry[] = [
    { id: 'opus-47', urls: ['https://anthropic.com/news/opus-47'] },
  ];
  const tweets: ScrapedTweet[] = [
    makeTweet({
      id: '1',
      links: ['https://anthropic.com/news/opus-47'],
      text: 'opus 4.7 is live',
    }),
    makeTweet({
      id: '2',
      links: ['https://anthropic.com/news/something-new'],
      text: 'new feature',
    }),
    makeTweet({
      id: '3',
      links: [],
      text: 'Opus 4.7 is rolling out today',
    }),
    makeTweet({
      id: '4',
      links: [],
      text: 'just chatting about coffee',
    }),
  ];

  const result = crossReferenceTweets(tweets, entries);
  assert.equal(result.matched.length, 1);
  assert.equal(result.matched[0]?.entryId, 'opus-47');
  assert.equal(result.novel.length, 1);
  assert.equal(result.novel[0]?.id, '2');
  assert.equal(result.context_only.length, 1);
  assert.equal(result.context_only[0]?.id, '3');
});

test('crossReferenceTweets prefix-matches when not strict', () => {
  const entries: ReleaseEntry[] = [
    { id: 'docs', urls: ['https://docs.anthropic.com/api'] },
  ];
  const tweets: ScrapedTweet[] = [
    makeTweet({
      id: 'a',
      links: ['https://docs.anthropic.com/api/messages'],
    }),
  ];
  const result = crossReferenceTweets(tweets, entries, { strictMatch: false });
  assert.equal(result.matched.length, 1);
  assert.equal(result.matched[0]?.entryId, 'docs');

  const strict = crossReferenceTweets(tweets, entries, { strictMatch: true });
  assert.equal(strict.matched.length, 0);
  assert.equal(strict.novel.length, 1);
});

/* -------------------------------------------------------------------------- */
/* Output                                                                     */
/* -------------------------------------------------------------------------- */

test('writeScrapeResult writes JSON and updates latest symlink', async () => {
  const dir = await mkdtemp(join(tmpdir(), 'shipped-scrape-'));
  try {
    const result: ScrapeResult = {
      tweets: [makeTweet({ id: 'aaa' })],
      scrapedAt: '2026-04-15T12:00:00.000Z',
      source: 'x-api',
    };
    const today = new Date('2026-04-15T00:00:00.000Z');
    const path = await writeScrapeResult(result, { outputDir: dir, today });
    const expected = join(dir, '2026-04-15.json');
    assert.equal(path, expected);

    const written = JSON.parse(await readFile(expected, 'utf8'));
    assert.equal(written.source, 'x-api');
    assert.equal(written.tweets.length, 1);
    assert.equal(written.tweets[0].id, 'aaa');
    assert.equal(written.scrapedAt, '2026-04-15T12:00:00.000Z');

    // Verify latest is either a symlink or copy.
    const latestPath = join(dir, 'latest.json');
    const stat = await lstat(latestPath);
    if (stat.isSymbolicLink()) {
      const target = await readlink(latestPath);
      assert.equal(target, '2026-04-15.json');
    } else {
      const data = JSON.parse(await readFile(latestPath, 'utf8'));
      assert.equal(data.tweets[0].id, 'aaa');
    }
  } finally {
    await rm(dir, { recursive: true, force: true });
  }
});

test('formatDateStamp returns YYYY-MM-DD UTC', () => {
  const d = new Date('2026-01-05T23:59:59.999Z');
  assert.equal(formatDateStamp(d), '2026-01-05');
});

test('writeScrapeResult includes failureReason when set', async () => {
  const dir = await mkdtemp(join(tmpdir(), 'shipped-scrape-fr-'));
  try {
    const result: ScrapeResult = {
      tweets: [],
      scrapedAt: '2026-04-15T12:00:00.000Z',
      source: 'cached',
      failureReason: 'all sources offline',
    };
    const path = await writeScrapeResult(result, {
      outputDir: dir,
      today: new Date('2026-04-15T00:00:00.000Z'),
      skipLatestSymlink: true,
    });
    const written = JSON.parse(await readFile(path, 'utf8'));
    assert.equal(written.failureReason, 'all sources offline');
    assert.equal(written.tweets.length, 0);
  } finally {
    await rm(dir, { recursive: true, force: true });
  }
});

/* -------------------------------------------------------------------------- */
/* Orchestrator (graceful empty)                                              */
/* -------------------------------------------------------------------------- */

test('scrapeClaudedevs returns empty with failureReason when no token + nitter fails', async () => {
  const previous = process.env['X_API_BEARER_TOKEN'];
  delete process.env['X_API_BEARER_TOKEN'];
  try {
    const fetchStub = (async (): Promise<Response> =>
      new Response('', { status: 503 })) as unknown as typeof fetch;
    const result = await scrapeClaudedevs({
      fetchImpl: fetchStub,
      dry: true,
      delayMs: 0,
    });
    assert.equal(result.tweets.length, 0);
    assert.equal(result.source, 'cached');
    assert.ok(result.failureReason, 'failureReason should be set');
    assert.equal(result.outputPath, null);
  } finally {
    if (previous !== undefined) process.env['X_API_BEARER_TOKEN'] = previous;
  }
});

test('scrapeClaudedevs uses X API when token is set and fetch succeeds', async () => {
  const fetchStub = (async (input: RequestInfo | URL): Promise<Response> => {
    const url = typeof input === 'string' ? input : input.toString();
    if (url.includes('/users/by/username/')) {
      return new Response(
        JSON.stringify({ data: { id: '1', username: 'claudedevs', name: 'C' } }),
        { status: 200 },
      );
    }
    return new Response(
      JSON.stringify({
        data: [
          {
            id: '900',
            text: 'live',
            created_at: '2026-04-15T08:00:00.000Z',
            public_metrics: { like_count: 0, retweet_count: 0, reply_count: 0 },
          },
        ],
        meta: { result_count: 1 },
      }),
      { status: 200 },
    );
  }) as unknown as typeof fetch;

  const result = await scrapeClaudedevs({
    xApiToken: 'fake',
    fetchImpl: fetchStub,
    dry: true,
    delayMs: 0,
  });
  assert.equal(result.source, 'x-api');
  assert.equal(result.tweets.length, 1);
  assert.equal(result.tweets[0]?.id, '900');
  assert.equal(result.outputPath, null);
});

/* -------------------------------------------------------------------------- */
/* X MCP                                                                      */
/* -------------------------------------------------------------------------- */

test('XMcpClient throws MissingMcpConfigError when no url is configured', () => {
  const previous = process.env['X_MCP_URL'];
  delete process.env['X_MCP_URL'];
  try {
    assert.throws(() => new XMcpClient(), MissingMcpConfigError);
  } finally {
    if (previous !== undefined) process.env['X_MCP_URL'] = previous;
  }
});

test('XMcpClient.fetchTimeline handshakes then maps posts to ScrapedTweet', async () => {
  const fetchStub = makeMcpFetch({
    tools: {
      get_user_posts: () => ({
        posts: [
          {
            id: '100',
            text: 'Opus 4.8 is live',
            created_at: recentIso(),
            public_metrics: { like_count: 12, retweet_count: 4, reply_count: 2 },
            urls: [{ expanded_url: 'https://anthropic.com/news/opus-48' }],
            hashtags: [{ tag: 'Claude' }],
          },
        ],
      }),
    },
  });
  const client = new XMcpClient({
    url: 'https://mcp.test/',
    token: 'k',
    fetchImpl: fetchStub,
    delayMs: 0,
  });
  const tweets = await client.fetchTimeline({
    username: 'claudedevs',
    sinceDays: 7,
    includeReplies: false,
    includeRetweets: false,
  });
  assert.equal(tweets.length, 1);
  assert.equal(tweets[0]?.id, '100');
  assert.equal(tweets[0]?.author, 'claudedevs');
  assert.deepEqual(tweets[0]?.links, ['https://anthropic.com/news/opus-48']);
  assert.deepEqual(tweets[0]?.hashtags, ['claude']);
  assert.equal(tweets[0]?.engagement.likes, 12);
  assert.equal(tweets[0]?.engagement.reposts, 4);
  assert.deepEqual(tweets[0]?.attachments, ['link']);
});

test('XMcpClient.searchPosts attributes the real third-party author', async () => {
  const fetchStub = makeMcpFetch({
    tools: {
      search_posts: (args) => ({
        posts: [
          {
            id: '777',
            text: `take on ${String(args['query'])}`,
            created_at: recentIso(),
            author: { username: 'simonw' },
            urls: [{ expanded_url: 'https://simonwillison.net/opus48' }],
          },
        ],
      }),
    },
  });
  const client = new XMcpClient({
    url: 'https://mcp.test/',
    fetchImpl: fetchStub,
    delayMs: 0,
  });
  const hits = await client.searchPosts('Claude', {
    username: 'claudedevs',
    sinceDays: 7,
    includeReplies: false,
    includeRetweets: false,
  });
  assert.equal(hits.length, 1);
  assert.equal(hits[0]?.author, 'simonw');
  assert.equal(hits[0]?.url, 'https://x.com/simonw/status/777');
});

test('parseRpcBody parses both plain JSON and SSE framing', () => {
  const plain = parseRpcBody<{ ok: boolean }>(
    '{"jsonrpc":"2.0","id":1,"result":{"ok":true}}',
  );
  assert.equal(plain?.result?.ok, true);

  const sse = parseRpcBody<{ ok: boolean }>(
    'event: message\ndata: {"jsonrpc":"2.0","id":2,"result":{"ok":true}}\n\n',
  );
  assert.equal(sse?.result?.ok, true);

  assert.equal(parseRpcBody('   '), null);
});

test('decodeToolResult prefers structuredContent, else parses text block', () => {
  assert.deepEqual(
    decodeToolResult({ structuredContent: { posts: [{ id: '1' }] } }),
    { posts: [{ id: '1' }] },
  );
  assert.deepEqual(
    decodeToolResult({ content: [{ type: 'text', text: '{"posts":[{"id":"2"}]}' }] }),
    { posts: [{ id: '2' }] },
  );
  assert.equal(decodeToolResult(undefined), null);
});

test('extractPostArray finds the array under common envelope keys', () => {
  assert.equal(extractPostArray([{ id: '1' }]).length, 1);
  assert.equal(extractPostArray({ posts: [{ id: '1' }] }).length, 1);
  assert.equal(extractPostArray({ data: [{ id: '1' }, { id: '2' }] }).length, 2);
  assert.equal(extractPostArray({ nothing: true }).length, 0);
});

test('normalizeMcpPost is defensive: null without id, maps minimal post', () => {
  assert.equal(normalizeMcpPost({}, 'claudedevs'), null);

  const t = normalizeMcpPost(
    { id: 5 as unknown as string, content: 'hi', username: 'openaidevs', urls: ['https://x.example/a'] },
    'claudedevs',
  );
  assert.ok(t);
  assert.equal(t?.id, '5');
  assert.equal(t?.text, 'hi');
  assert.equal(t?.author, 'openaidevs');
  assert.deepEqual(t?.links, ['https://x.example/a']);
  assert.deepEqual(t?.attachments, ['link']);
});

test('mergeNovel dedupes by id and by shared normalized link', () => {
  const base = [makeTweet({ id: '1', links: ['https://a.com/x'] })];
  const extra = [
    makeTweet({ id: '1' }), // dup id
    makeTweet({ id: '2', links: ['https://www.a.com/x/'] }), // dup url (normalized)
    makeTweet({ id: '3', links: ['https://b.com/y'] }), // novel
  ];
  const { merged, added } = mergeNovel(base, extra);
  assert.equal(added, 1);
  assert.equal(merged.length, 2);
  assert.ok(merged.some((t) => t.id === '3'));
});

test('searchTermsForHandle derives lab terms, falls back to bare handle', () => {
  assert.deepEqual(searchTermsForHandle('claudedevs'), ['Anthropic', 'Claude']);
  assert.deepEqual(searchTermsForHandle('@OpenAIDevs'), ['OpenAI', 'ChatGPT']);
  assert.deepEqual(searchTermsForHandle('somebody_else'), ['somebody_else']);
});

/* -------------------------------------------------------------------------- */
/* Orchestrator with X MCP                                                    */
/* -------------------------------------------------------------------------- */

test('scrapeClaudedevs prefers x-mcp when X_MCP_URL is configured', async () => {
  const fetchStub = makeMcpFetch({
    tools: {
      get_user_posts: () => ({
        posts: [{ id: '900', text: 'live', created_at: recentIso() }],
      }),
    },
  });
  const result = await scrapeClaudedevs({
    xMcpUrl: 'https://mcp.test/',
    xMcpToken: 'k',
    fetchImpl: fetchStub,
    dry: true,
    delayMs: 0,
  });
  assert.equal(result.source, 'x-mcp');
  assert.equal(result.tweets.length, 1);
  assert.equal(result.tweets[0]?.id, '900');
});

test('scrapeClaudedevs enrichment merges novel search posts', async () => {
  const fetchStub = makeMcpFetch({
    tools: {
      get_user_posts: () => ({
        posts: [{ id: '900', text: 'anchor post', created_at: recentIso() }],
      }),
      search_posts: () => ({
        posts: [
          {
            id: '901',
            text: 'third-party benchmark',
            created_at: recentIso(),
            author: { username: 'analyst' },
            urls: [{ expanded_url: 'https://bench.example/claude' }],
          },
        ],
      }),
    },
  });
  const result = await scrapeClaudedevs({
    xMcpUrl: 'https://mcp.test/',
    fetchImpl: fetchStub,
    enrich: true,
    searchTerms: ['Claude'],
    dry: true,
    delayMs: 0,
  });
  assert.equal(result.source, 'x-mcp');
  assert.equal(result.tweets.length, 2);
  assert.equal(result.enrichment?.added, 1);
  assert.deepEqual(result.enrichment?.terms, ['Claude']);
  assert.ok(result.tweets.some((t) => t.author === 'analyst'));
});

test('scrapeClaudedevs falls back to x-api when X MCP is down', async () => {
  const mcpUrl = 'https://mcp.test/';
  const combined = (async (input: RequestInfo | URL, init?: RequestInit): Promise<Response> => {
    const url = typeof input === 'string' ? input : input.toString();
    if (url.startsWith(mcpUrl)) return new Response('mcp down', { status: 503 });
    if (url.includes('/users/by/username/')) {
      return new Response(
        JSON.stringify({ data: { id: '1', username: 'claudedevs', name: 'C' } }),
        { status: 200 },
      );
    }
    return new Response(
      JSON.stringify({
        data: [
          {
            id: '950',
            text: 'from api',
            created_at: recentIso(),
            public_metrics: { like_count: 0, retweet_count: 0, reply_count: 0 },
          },
        ],
        meta: { result_count: 1 },
      }),
      { status: 200 },
    );
  }) as unknown as typeof fetch;

  const result = await scrapeClaudedevs({
    xMcpUrl: mcpUrl,
    xApiToken: 'fake',
    fetchImpl: combined,
    dry: true,
    delayMs: 0,
  });
  assert.equal(result.source, 'x-api');
  assert.equal(result.tweets[0]?.id, '950');
});
