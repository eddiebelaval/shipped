/**
 * "Investigation" — Glasswing. Feature opener + prose-well + named quotes
 * (3 voices) + Firefox ratio chart + closing prose. The markdown encodes
 * blockquote-style attributions (`> "quote..." \n> — Name · Org`); we
 * detect and render those as orange/ink-bordered quote cards.
 */

import type { Section } from '../types.js';
import { extractRatioChart } from '../parse.js';
import { renderRatio } from '../charts.js';
import { inlineMarkdown } from '../markdown.js';

export function renderInvestigation(section: Section): string {
  const headline = extractHeadline(section.content);
  const ratio = extractRatioChart(section.content);
  const ratioHtml = ratio && ratio.kind === 'ratio' ? renderRatio(ratio.data) : '';

  const prose = renderProseWithQuotes(stripSidebar(section.content));

  return `<div class="feature-opener" id="investigation">
  <span class="vert-label">Investigation</span>
  <div class="feature-heading">
    <div class="feature-kicker">Reporting by Eddie Belaval</div>
    <h2 class="feature-title">${formatTitle(headline)}</h2>
  </div>
</div>

<div class="prose-well">
  <div class="prose drop-cap">
${prose}
  </div>
</div>

${ratioHtml}

<span class="ornament">&sect; &nbsp; &sect; &nbsp; &sect;</span>`;
}

function extractHeadline(content: string): string {
  const lines = content.split('\n');
  for (const l of lines) {
    if (l.startsWith('# ')) return l.slice(2).trim();
  }
  return 'Investigation';
}

function formatTitle(headline: string): string {
  // For multi-word or multi-clause titles, leave as-is with trailing period.
  // For single-word titles (e.g. "Glasswing"), italicize.
  if (/^\w+$/.test(headline.trim())) {
    return `<em>${headline}.</em>`;
  }
  return headline.replace(/\.$/, '') + '.';
}

interface Quote {
  text: string;
  attribution: string;
}

// Renders prose paragraphs and named quote cards in document order.
// Named quote pattern: > *”text”* followed by > — attribution
// CHART blocks and other > blocks are skipped (CHART is rendered via ratioHtml).
function renderProseWithQuotes(content: string): string {
  let quoteIdx = 0;
  const blocks = content
    .replace(/\r\n/g, '\n')
    .split(/\n{2,}/)
    .map((b) => b.trim())
    .filter((b) => b.length > 0 && !/^-{3,}$/.test(b) && !b.startsWith('#') && !b.startsWith('|'));

  return blocks
    .map((b) => {
      if (!b.startsWith('>')) {
        return `    <p>${inlineMarkdown(b.replace(/\n/g, ' '))}</p>`;
      }
      const lines = b.split('\n');
      const m = lines[0]?.match(/^>\s*\*"(.+?)"\*\s*$/);
      if (m && m[1] && m[1].length > 20) {
        let attr = '';
        for (let i = 1; i < lines.length; i++) {
          const a = lines[i]?.match(/^>\s*[—-]\s*(.+)$/);
          if (a) { attr = a[1]!.trim(); break; }
        }
        const accent = quoteIdx++ === 0 ? 'orange' : 'ink';
        return renderQuote({ text: m[1], attribution: attr }, accent);
      }
      return '';
    })
    .filter((s) => s.length > 0)
    .join('\n');
}

function renderQuote(q: Quote, accent: 'orange' | 'ink'): string {
  const borderColor = accent === 'orange' ? 'var(--orange)' : 'var(--ink)';
  return `<blockquote style="margin:32px 0;padding:0;border-left:3px solid ${borderColor};padding-left:20px">
      <p style="font-style:italic;font-size:22px;line-height:1.35;color:var(--ink);margin-bottom:12px">&ldquo;${inlineMarkdown(q.text)}&rdquo;</p>
      <span style="font-family:var(--narrow);font-size:11px;font-weight:600;letter-spacing:.22em;text-transform:uppercase;color:var(--muted)">— ${inlineMarkdown(q.attribution)}</span>
    </blockquote>`;
}

function stripSidebar(content: string): string {
  const lines = content.split('\n');
  const start = lines.findIndex((l) => /^>\s*###\s+Sidebar/.test(l));
  if (start < 0) return content;
  let s = start;
  while (s > 0 && lines[s - 1]!.startsWith('>')) s--;
  let e = start;
  while (e < lines.length - 1 && lines[e + 1]!.startsWith('>')) e++;
  return [...lines.slice(0, s), ...lines.slice(e + 1)].join('\n');
}

