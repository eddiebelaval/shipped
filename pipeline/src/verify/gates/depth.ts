/**
 * Depth gate.
 *
 * Enforces the word floors that doctrine has only ever *asked* for. The
 * recurring failure mode is the issue that collapses to a paragraph on a quiet
 * news day — "bug day = two paragraphs" (content/DAILY.md) — and ships anyway
 * because nothing blocks it. This gate blocks it.
 *
 * Floors are mirrored here from the doctrine, the same way the voice gate
 * mirrors STYLE.md's forbidden list:
 *
 *   - Daily   (content/DAILY.md):  quiet-day minimum 1,000 words ex-Release Log.
 *   - Weekly/Issue (content/FORMULA.md): lean front-of-book 1,800 words; the
 *     old 600–1,500 band "shipped issues that read short", so <1,500 is a hard
 *     fail, the lean floor warns, and >4,500 (hard ceiling) warns to split.
 *
 * Severities: catastrophic shortfall FAILs (blocks publish, invariant #2);
 * a near-miss below the target WARNs (surfaces, does not block). A WARN ships;
 * a FAIL does not. Floors carry a small tolerance below the doctrine target so
 * an honestly-tuned issue is not blocked by word-counting drift, but a
 * collapsed one (Friday's 2026-06-26 daily was ~250 words) never survives.
 *
 * The measured region is the **front-of-book** — the Release Log, Sources
 * footer, and the trailing "Generated …" stamp are excluded, because the floor
 * is about editorial depth, not how many release lines the scraper compiled.
 */

import type { VerifyResult } from "../types.js";

const GATE_NAME = "depth";

interface Floor {
  /** Below this, FAIL (blocks publish). */
  failBelow: number;
  /** At or above failBelow but below this, WARN. */
  target: number;
  /** Above this, WARN to split. 0 = no ceiling. */
  ceiling: number;
  /** Human label for the shape, used in messages. */
  label: string;
  /** Doctrine file the floor comes from. */
  doctrine: string;
}

// Daily — content/DAILY.md. Quiet-day floor 1,000; fail with ~10% tolerance.
const DAILY_FLOOR: Floor = {
  failBelow: 900,
  target: 1000,
  ceiling: 2800, // heavy-day ceiling; doctrine says split above this
  label: "daily",
  doctrine: "DAILY.md",
};

// Weekly / numbered issue — content/FORMULA.md front-of-book targets.
const ISSUE_FLOOR: Floor = {
  failBelow: 1500,
  target: 1800,
  ceiling: 4500,
  label: "weekly/issue",
  doctrine: "FORMULA.md",
};

/**
 * Pick the floor by frontmatter. `type: anthropic-daily` -> daily floors;
 * everything else (weekly digest, numbered issue) -> the heavier issue floors.
 */
function floorFor(frontmatter: Record<string, unknown>): Floor {
  const type = String(frontmatter.type ?? "").toLowerCase();
  if (type === "anthropic-daily") return DAILY_FLOOR;
  return ISSUE_FLOOR;
}

export function runDepthGate(
  body: string,
  frontmatter: Record<string, unknown> = {},
): VerifyResult[] {
  const floor = floorFor(frontmatter);
  const prose = frontOfBook(body);
  const words = countWords(prose);

  const where = `front-of-book ${words}w (${floor.label}, floor ${floor.target} per ${floor.doctrine})`;

  if (words < floor.failBelow) {
    return [
      {
        passed: false,
        gate: GATE_NAME,
        severity: "fail",
        details: `Issue too short: ${where}. This is the "bug day = two paragraphs" collapse the depth doctrine exists to stop. Dig each item through the levers; do not demote by default.`,
        claim: {
          id: "depth-too-short",
          kind: "formula",
          text: `${words} words`,
          meta: { words, ...floor },
        },
      },
    ];
  }

  if (words < floor.target) {
    return [
      {
        passed: false,
        gate: GATE_NAME,
        severity: "warn",
        details: `Below target: ${where}. Under the floor but not collapsed — dig the thin items before shipping.`,
        claim: {
          id: "depth-below-target",
          kind: "formula",
          text: `${words} words`,
          meta: { words, ...floor },
        },
      },
    ];
  }

  if (floor.ceiling > 0 && words > floor.ceiling) {
    return [
      {
        passed: false,
        gate: GATE_NAME,
        severity: "warn",
        details: `Over ceiling: ${where}, ceiling ${floor.ceiling}. Consider splitting into a second edition (${floor.doctrine}).`,
        claim: {
          id: "depth-over-ceiling",
          kind: "formula",
          text: `${words} words`,
          meta: { words, ...floor },
        },
      },
    ];
  }

  return [
    {
      passed: true,
      gate: GATE_NAME,
      severity: "info",
      details: `Depth OK: ${where}.`,
    },
  ];
}

// ------------------------------------------------------------------ helpers

/**
 * The front-of-book: everything before the Release Log heading, with the
 * Sources footer and "Generated …" stamp removed. If there is no Release Log
 * heading (some numbered issues run prose-only), the whole prose body counts.
 */
export function frontOfBook(markdown: string): string {
  let body = stripFrontmatter(markdown);
  body = stripCodeFences(body);

  const lines = body.split(/\r?\n/);

  // Cut at the Release Log heading (any heading level, any leading "The").
  let end = lines.length;
  for (let i = 0; i < lines.length; i++) {
    if (/^#{1,6}\s+(the\s+)?release log\b/i.test(lines[i] ?? "")) {
      end = i;
      break;
    }
  }

  const kept: string[] = [];
  for (let i = 0; i < end; i++) {
    const line = lines[i] ?? "";
    // Drop the trailing "Sources:" list and the generation stamp.
    if (/^sources:\s*$/i.test(line.trim())) break;
    if (/^generated\b/i.test(line.trim())) continue;
    kept.push(line);
  }

  return kept.join("\n");
}

/** Count real words: whitespace-split tokens containing at least one letter/number. */
export function countWords(text: string): number {
  return stripMarkup(text)
    .split(/\s+/)
    .filter((t) => /[A-Za-z0-9]/.test(t)).length;
}

function stripFrontmatter(md: string): string {
  if (!md.startsWith("---")) return md;
  const end = md.indexOf("\n---", 3);
  if (end === -1) return md;
  return md.slice(end + 4);
}

function stripCodeFences(md: string): string {
  return md.replace(/```[\s\S]*?```/g, " ");
}

/** Reduce markdown to its prose: link text without URLs, no markup, no tag chips. */
function stripMarkup(md: string): string {
  return md
    .replace(/!\[[^\]]*\]\([^)]*\)/g, " ") // images
    .replace(/\[([^\]]*)\]\([^)]*\)/g, "$1") // links -> link text
    .replace(/`[^`]*`/g, " ") // inline code (incl. `[CODE]` chips)
    .replace(/https?:\/\/\S+/g, " ") // bare URLs
    .replace(/^[#>\s-]+/gm, " ") // heading/blockquote/list/hr markers
    .replace(/[*_~]/g, " ") // emphasis
    .replace(/[|]/g, " "); // table pipes
}
