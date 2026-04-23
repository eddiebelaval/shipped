/**
 * "The Lead Story" — feature opener + prose-well + Mythos chart + pull quote
 * + lead-story continuation + sidebar box (the Mythos detail).
 */

import type { Section } from '../types.js';
import { extractFiveBarChart } from '../parse.js';
import { renderFiveBar } from '../charts.js';
import { inlineMarkdown } from '../markdown.js';

export function renderLeadStory(section: Section): string {
  const headline = extractHeadline(section.content);
  const prose = paragraphs(stripChartBlock(stripSidebar(stripPullQuote(section.content))));

  const chart = extractFiveBarChart(section.content);
  const chartHtml = chart && chart.kind === 'five_bar' ? renderFiveBar(chart.bars) : '';

  const pullQuote = extractPullQuote(section.content);
  const pullQuoteHtml = pullQuote ? renderPullQuote(pullQuote) : '';

  return `<div class="feature-opener" id="lead">
  <span class="vert-label">The Lead Story <span class="vert-num">01</span></span>
  <div class="feature-heading">
    <div class="feature-kicker">Report by Eddie Belaval</div>
    <h2 class="feature-title">${formatTitle(headline)}</h2>
  </div>
</div>

<div class="prose-well">
  <div class="prose drop-cap drop-cap-orange">
${prose}
  </div>
</div>

${chartHtml}

${pullQuoteHtml}

<span class="ornament bold">&#10022; &nbsp; &#10022; &nbsp; &#10022;</span>`;
}

// ────────────────────────────────────────────────────────────────────
// Helpers
// ────────────────────────────────────────────────────────────────────

function extractHeadline(content: string): string {
  const lines = content.split('\n');
  for (const l of lines) {
    if (l.startsWith('# ')) return l.slice(2).trim();
  }
  return 'The Lead Story';
}

function formatTitle(headline: string): string {
  // Italicize words like "wasn't", "won't" if positioned mid-sentence.
  const words = headline.split(' ');
  if (words.length >= 3 && /^(wasn't|won't|isn't|wouldn't)$/i.test(words[2]!)) {
    words[2] = `<em>${words[2]}</em>`;
  }
  return words.join(' ').replace(/\s*$/, '.');
}

function splitOnChart(content: string): { before: string; after: string } {
  const idx = content.indexOf('> ### CHART');
  if (idx < 0) return { before: content, after: '' };
  const beforeEnd = content.lastIndexOf('\n', idx);
  const before = content.slice(0, beforeEnd > 0 ? beforeEnd : idx);
  const lines = content.split('\n');
  let i = 0;
  let charPos = 0;
  for (; i < lines.length; i++) {
    if (charPos >= idx) break;
    charPos += lines[i]!.length + 1;
  }
  while (i < lines.length && lines[i]!.startsWith('>')) i++;
  const after = lines.slice(i + 1).join('\n');
  return { before, after };
}

function stripChartBlock(content: string): string {
  const lines = content.split('\n');
  const start = lines.findIndex((l) => l.startsWith('>') && /CHART/.test(l));
  if (start < 0) return content;
  let s = start;
  while (s > 0 && lines[s - 1]!.startsWith('>')) s--;
  let e = start;
  while (e < lines.length - 1 && lines[e + 1]!.startsWith('>')) e++;
  return [...lines.slice(0, s), ...lines.slice(e + 1)].join('\n');
}

function extractPullQuote(content: string): string | null {
  const lines = content.split('\n');
  for (const l of lines) {
    const m = l.match(/^>\s*\*([^*].*[^*])\*\s*$/);
    if (m && m[1] && m[1].length > 30) return m[1];
  }
  return null;
}

function stripPullQuote(content: string): string {
  return content
    .split('\n')
    .filter((l) => !/^>\s*\*[^*].*[^*]\*\s*$/.test(l))
    .join('\n');
}

function renderPullQuote(text: string): string {
  return `<aside class="pq-full">
  <div class="pq-full-inner">
    <div class="pq-quote-mark">&ldquo;</div>
    <div class="pq-body">
      <p class="pq-text">${inlineMarkdown(text)}</p>
      <div class="pq-att">
        <span>Shipped. &nbsp;·&nbsp; Issue <b>01</b> &nbsp;·&nbsp; The Lead Story</span>
        <span>Eddie Belaval &nbsp;·&nbsp; <b>Apr 16, 2026</b></span>
      </div>
    </div>
  </div>
</aside>`;
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

function renderMythosSidebar(): string {
  return `<div class="sidebar-box accent" style="max-width:900px">
  <span class="sidebar-box-kicker">Sidebar &nbsp;·&nbsp; A profile of the model you can&apos;t use</span>
  <h4 class="sidebar-box-title">The Mythos Bar, in detail.</h4>
  <div class="sidebar-box-body">
    <p>Where Opus 4.6 hits 66.6% on the CyberGym vulnerability-reproduction benchmark, Mythos Preview hits 83.1%. Where Opus 4.6 produced two working Firefox shell exploits in several hundred attempts, Mythos produced <strong>181</strong>. On the OSS-Fuzz corpus, Mythos achieved full control-flow hijack on ten separate, fully patched targets.</p>
    <p>The vulnerabilities Mythos has surfaced are subtle, old, or both:</p>
    <ul class="sidebar-box-list">
      <li><span class="yr">27 <em>yr</em></span><span>Memory-corruption bug in OpenBSD. Survived decades of human review.</span><span></span></li>
      <li><span class="yr">16 <em>yr</em></span><span>FFmpeg flaw. Automated fuzzing missed it across 5M prior test hits.</span><span></span></li>
      <li><span class="yr">10 <em>tgt</em></span><span>Linux-kernel privilege escalation chains. Race conditions + KASLR bypass.</span><span></span></li>
      <li><span class="yr">4 <em>chn</em></span><span>Firefox JIT heap-spray. Escaped both renderer and OS sandboxes.</span><span></span></li>
    </ul>
    <p style="margin-top:16px">You can&apos;t have it. Mythos is gated to twelve security partners under Project Glasswing. Anthropic&apos;s stated reason is risk: a model that finds zero-days in OpenBSD that survived twenty-seven years of human review is a model you don&apos;t put on the open API. Whether that calculus holds — for how long, and under what pressure — is the open question of the year.</p>
  </div>
</div>`;
}

function paragraphs(body: string): string {
  const blocks = body
    .replace(/\r\n/g, '\n')
    .split(/\n{2,}/)
    .map((b) => b.trim())
    .filter(
      (b) =>
        b.length > 0 &&
        !/^-{3,}$/.test(b) &&
        !b.startsWith('#') &&
        !b.startsWith('>') &&
        !b.startsWith('|'),
    );
  return blocks
    .map((b) => `    <p>${inlineMarkdown(b.replace(/\n/g, ' '))}</p>`)
    .join('\n');
}
