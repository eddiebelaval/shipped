/**
 * Lab-coverage gate.
 *
 * The beat is six frontier labs — Anthropic the anchor, plus OpenAI, Google
 * DeepMind, Meta, Mistral, xAI (pipeline/src/scrape/sources.ts). The beat was
 * widened for exactly the reason a single-lab issue keeps recurring: "quiet
 * days on one lab are not thin days for the reader." When an issue mentions
 * only Anthropic, the cross-lab read (DAILY.md lever 6) never happened.
 *
 * This is a WARN, not a FAIL. You cannot force OpenAI to ship on a given day,
 * and a genuinely Anthropic-anchored heavy day is legitimate for the anchor.
 * Failing single-lab issues would produce false negatives. So the gate
 * surfaces the single-lab case loudly without blocking publish; the depth gate
 * is what blocks the collapse. Coverage is scanned across the whole prose body
 * (front-of-book + Release Log), since a lab can earn a mention in either.
 */

import type { VerifyResult } from "../types.js";

const GATE_NAME = "lab-coverage";

interface Lab {
  name: string;
  /** Distinctive tokens. Generic words (Google, Meta alone) are avoided to cut false hits. */
  patterns: RegExp[];
}

// Mirrors the LABS list in pipeline/src/scrape/sources.ts.
const LABS: Lab[] = [
  { name: "Anthropic", patterns: [/\bAnthropic\b/i, /\bClaude\b/i] },
  { name: "OpenAI", patterns: [/\bOpenAI\b/i, /\bChatGPT\b/i, /\bGPT-?\d/i] },
  {
    name: "Google DeepMind",
    patterns: [/\bDeepMind\b/i, /\bGemini\b/i],
  },
  { name: "Meta", patterns: [/\bMeta AI\b/i, /\bLlama\b/i] },
  { name: "Mistral", patterns: [/\bMistral\b/i] },
  { name: "xAI", patterns: [/\bxAI\b/i, /\bGrok\b/i] },
];

const MIN_LABS = 2;

export function runLabCoverageGate(
  body: string,
  _frontmatter: Record<string, unknown> = {},
): VerifyResult[] {
  const prose = stripForScan(body);
  const found = LABS.filter((lab) => lab.patterns.some((p) => p.test(prose))).map(
    (l) => l.name,
  );

  if (found.length < MIN_LABS) {
    const only = found.length ? found.join(", ") : "no labs detected";
    return [
      {
        passed: false,
        gate: GATE_NAME,
        severity: "warn",
        details: `Single-lab issue (${only}). The beat is six frontier labs; read this move against the other lanes (DAILY.md lever 6 — the contrast) or say plainly why the rest were silent.`,
        claim: {
          id: "lab-coverage-single",
          kind: "formula",
          text: only,
          meta: { found, min: MIN_LABS },
        },
      },
    ];
  }

  return [
    {
      passed: true,
      gate: GATE_NAME,
      severity: "info",
      details: `Lab coverage OK: ${found.length} labs (${found.join(", ")}).`,
    },
  ];
}

// ------------------------------------------------------------------ helpers

/** Strip frontmatter, code fences, and the Sources footer so URLs/handles don't inflate coverage. */
function stripForScan(md: string): string {
  let body = md.startsWith("---")
    ? md.slice((md.indexOf("\n---", 3) + 4) || 0)
    : md;
  body = body.replace(/```[\s\S]*?```/g, " ");
  // Drop the trailing Sources: block (source URLs name labs in their domains).
  const srcIdx = body.search(/^sources:\s*$/im);
  if (srcIdx !== -1) body = body.slice(0, srcIdx);
  body = body.replace(/https?:\/\/\S+/g, " ");
  return body;
}
