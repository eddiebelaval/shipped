/**
 * Tests for the verification engine.
 *
 * Uses node:test (built-in). Run with `pnpm test:verify`.
 *
 * Covers:
 *   1. Claim extraction on the real Issue #00 markdown.
 *   2. URL liveness with one known-good URL and one known-bad URL.
 *   3. Voice gate finds a forbidden phrase in a small synthetic markdown.
 *   4. Report aggregation produces sensible counts and verdict.
 */

import { test } from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { resolve } from "node:path";

import { extractClaims } from "../src/verify/extract.js";
import { runUrlLiveness } from "../src/verify/gates/url-liveness.js";
import { runVoiceGate } from "../src/verify/gates/voice.js";
import { runDepthGate } from "../src/verify/gates/depth.js";
import { runLabCoverageGate } from "../src/verify/gates/lab-coverage.js";
import { runVerification, formatReport } from "../src/verify/index.js";
import type { Claim } from "../src/verify/types.js";
import { numberVariants } from "../src/verify/gates/number-attestation.js";
import { dateVariants } from "../src/verify/gates/date-attestation.js";
import { wordOverlap } from "../src/verify/gates/quote-attestation.js";

// Resolve relative to this test file: scrapers/shipped/test -> repo root needs ../../../..
const ISSUE_MD = resolve(
  new URL(".", import.meta.url).pathname,
  "../../content/issue-00-the-founding.md",
);

// ---------------------------------------------------------------------------
// 1. Extraction on the real Issue #00 markdown.
// ---------------------------------------------------------------------------

test("extractClaims pulls URL/number/quote/date claims from Issue #00", async () => {
  const md = await readFile(ISSUE_MD, "utf8");
  const { claims } = extractClaims(md);

  const byKind = (k: Claim["kind"]) => claims.filter((c) => c.kind === k);

  // URLs: bibliography alone has 30+ links.
  assert.ok(byKind("url").length >= 20, `expected >=20 url claims, got ${byKind("url").length}`);

  // Number claims: tons of percentages and dollar values.
  assert.ok(
    byKind("number").length >= 10,
    `expected >=10 number claims, got ${byKind("number").length}`,
  );

  // Quote claims: at least the three Glasswing quotes (Tsyganskiy, Grieco, Zemlin).
  const quotes = byKind("quote");
  assert.ok(quotes.length >= 3, `expected >=3 quote claims, got ${quotes.length}`);
  const quotePeople = quotes.map((q) => (q.meta as { person?: string })?.person).filter(Boolean);
  assert.ok(
    quotePeople.some((p) => p?.includes("Tsyganskiy")),
    `expected quote attributed to Tsyganskiy, got ${JSON.stringify(quotePeople)}`,
  );
});

// ---------------------------------------------------------------------------
// 2. URL liveness with known-good and known-bad URLs.
// ---------------------------------------------------------------------------

test("runUrlLiveness passes a known-good URL and fails a known-bad URL", async () => {
  const claims: Claim[] = [
    {
      id: "good",
      kind: "url",
      text: "https://anthropic.com/",
      sourceUrl: "https://anthropic.com/",
    },
    {
      id: "bad",
      kind: "url",
      text: "https://httpstat.us/404",
      sourceUrl: "https://httpstat.us/404",
    },
  ];

  const results = await runUrlLiveness(claims, { concurrency: 2, timeoutMs: 15_000 });
  assert.equal(results.length, 2, "expected 2 results");

  const good = results.find((r) => r.claim?.id === "good");
  const bad = results.find((r) => r.claim?.id === "bad");
  assert.ok(good, "good result missing");
  assert.ok(bad, "bad result missing");

  // anthropic.com should be reachable. Skip on transport failure or firewall (403 from sandboxed envs).
  if (good!.details.startsWith("Transport failure") || good!.details.includes("(403)")) {
    console.warn(`Skipping URL liveness assertions: network unavailable or firewalled (${good!.details}).`);
    return;
  }

  assert.equal(good!.passed, true, `expected pass for anthropic.com, got: ${good!.details}`);
  assert.equal(bad!.passed, false, `expected fail for httpstat.us/404, got: ${bad!.details}`);
});

// ---------------------------------------------------------------------------
// 3. Voice gate finds forbidden phrases.
// ---------------------------------------------------------------------------

test("runVoiceGate flags 'EPIC launch' and 'thrilled to announce'", () => {
  const md = [
    "# Test issue",
    "",
    "We're thrilled to announce our EPIC launch of the new platform.",
    "Best-in-class performance, industry-leading speed.",
    "",
    "We can leverage these synergies for game-changing results.",
  ].join("\n");

  const results = runVoiceGate(md);
  const fails = results.filter((r) => !r.passed);
  assert.ok(fails.length >= 5, `expected >=5 voice failures, got ${fails.length}: ${JSON.stringify(fails.map((f) => f.details))}`);

  const labels = fails.map((f) => (f.claim?.meta as { rule?: string } | undefined)?.rule);
  assert.ok(labels.includes("EPIC"));
  assert.ok(labels.includes("thrilled to announce/share"));
});

test("runVoiceGate flags overuse of 'X isn't Y, it's Z' formula", () => {
  const md = [
    "It isn't a bug, it's a feature.",
    "It isn't a deal problem, it's a process problem.",
    "It isn't slow, that's the point.",
  ].join("\n");

  const results = runVoiceGate(md);
  const formulaFail = results.find(
    (r) => !r.passed && r.claim?.kind === "formula",
  );
  assert.ok(formulaFail, "expected formula-overuse failure");
});

test("runVoiceGate ignores forbidden phrases inside fenced code blocks", () => {
  const md = ["# Issue", "", "```", "EPIC", "leverage", "```"].join("\n");
  const results = runVoiceGate(md);
  const fails = results.filter((r) => !r.passed);
  assert.equal(fails.length, 0, `expected 0 fails inside code fence, got ${JSON.stringify(fails)}`);
});

// ---------------------------------------------------------------------------
// 3b. Depth gate -- the "one paragraph shipped" failure.
// ---------------------------------------------------------------------------

test("runDepthGate FAILs a collapsed one-paragraph daily", () => {
  const md = [
    "---",
    "type: anthropic-daily",
    "---",
    "",
    "Shipped. Daily.",
    "",
    "## Lead",
    "A single short paragraph went out and nothing else did.",
    "",
    "## Release Log",
    "### Code",
    "Lots and lots of release log words ".repeat(80),
  ].join("\n");

  const results = runDepthGate(md, { type: "anthropic-daily" });
  const fail = results.find((r) => !r.passed && r.severity === "fail");
  assert.ok(fail, `expected a depth FAIL, got ${JSON.stringify(results)}`);
  // Release Log padding must NOT rescue a thin front-of-book.
  assert.ok(fail!.details.includes("front-of-book"), fail!.details);
});

test("runDepthGate passes a daily that clears the floor", () => {
  const para = "Word ".repeat(1100);
  const md = ["---", "type: anthropic-daily", "---", "", "## Lead", para].join("\n");
  const results = runDepthGate(md, { type: "anthropic-daily" });
  assert.ok(results.every((r) => r.passed), JSON.stringify(results));
});

test("runDepthGate applies the heavier issue floor to weekly/issue docs", () => {
  const para = "Word ".repeat(1200); // clears daily floor, under issue floor
  const md = ["## Lead", para].join("\n");
  const results = runDepthGate(md, { issue: 5 });
  const fail = results.find((r) => !r.passed && r.severity === "fail");
  assert.ok(fail, `expected issue-floor FAIL at 1200w, got ${JSON.stringify(results)}`);
});

// ---------------------------------------------------------------------------
// 3c. Lab-coverage gate -- the single-lab failure.
// ---------------------------------------------------------------------------

test("runLabCoverageGate WARNs on an Anthropic-only issue", () => {
  const md = "Claude shipped a point release. Anthropic also published a report.";
  const results = runLabCoverageGate(md);
  const warn = results.find((r) => !r.passed && r.severity === "warn");
  assert.ok(warn, `expected single-lab WARN, got ${JSON.stringify(results)}`);
});

test("runLabCoverageGate passes when multiple labs appear", () => {
  const md = "Claude shipped; meanwhile OpenAI cut GPT pricing and Gemini answered.";
  const results = runLabCoverageGate(md);
  assert.ok(results.every((r) => r.passed), JSON.stringify(results));
});

// ---------------------------------------------------------------------------
// 4. Report aggregation.
// ---------------------------------------------------------------------------

test("runVerification produces a sensible aggregated report (offline)", async () => {
  const report = await runVerification(ISSUE_MD, { offline: true });
  assert.equal(report.markdownPath, ISSUE_MD);
  assert.ok(report.results.length > 0, "expected at least one result");
  assert.ok(typeof report.exitCode === "number");
  assert.ok([0, 1].includes(report.exitCode));

  const formatted = formatReport(report, false);
  assert.ok(formatted.includes("Verdict:"), "report should contain a Verdict line");
  assert.ok(formatted.includes("Per-gate"), "report should contain per-gate summary");
});

// ---------------------------------------------------------------------------
// 5. Helpers: number/date/quote-overlap unit checks.
// ---------------------------------------------------------------------------

test("numberVariants generates expected text variants", () => {
  const pct = numberVariants("87.6%");
  assert.ok(pct.includes("87.6%"));
  assert.ok(pct.includes("87.6 percent"));

  const dollars = numberVariants("$100M");
  assert.ok(dollars.includes("$100M"));
  assert.ok(dollars.includes("$100 million"));
  assert.ok(dollars.includes("100 million"));
});

test("dateVariants expands ISO date into common formats", () => {
  const v = dateVariants("2026-04-16");
  assert.ok(v.includes("2026-04-16"));
  assert.ok(v.includes("April 16, 2026"));
  assert.ok(v.includes("Apr 16, 2026"));
  assert.ok(v.includes("16 April 2026"));
});

test("wordOverlap scores high for nearly identical strings", () => {
  const quote = "The window between vulnerability discovery and exploitation has collapsed";
  const source =
    "Plenty of preamble. The window between vulnerability discovery and exploitation has collapsed -- what took months now happens in minutes. Closing.";
  const score = wordOverlap(quote, source);
  assert.ok(score >= 0.8, `expected >=0.8 overlap, got ${score}`);
});
