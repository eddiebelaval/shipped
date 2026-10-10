/**
 * "The Open" — opening editorial essay.
 *
 * Layout: pull quote (first paragraph, italic, with em→orange), then
 * remaining paragraphs in serif body, with an aside listing the brief.
 */

import type { Section } from '../types.js';
import { inlineMarkdown } from '../markdown.js';

/** Facts the Brief can state truthfully, all derived from the issue itself. */
export interface OpenFacts {
  issueNum: string;
  date: string;          // YYYY-MM-DD
  releaseCount: number;
}

export function renderOpen(section: Section, period: string, facts?: OpenFacts): string {
  const paras = section.content
    .split(/\n{2,}/)
    .map((p) => p.trim())
    .filter((p) => p.length > 0 && !/^-{3,}$/.test(p));

  if (paras.length === 0) return '';

  const quoteText = inlineMarkdown(paras[0]!.replace(/\n/g, ' '));
  const restHtml = paras
    .slice(1)
    .map((p) => `<p>${inlineMarkdown(p.replace(/\n/g, ' '))}</p>`)
    .join('\n        ');

  const periodLabel = formatPeriod(period);
  // Every number here is computed from the issue. The Brief used to print one
  // April issue's figures (21 days, 56 releases, 12 orgs) on every issue.
  const days = periodDays(period);
  const folio = facts ? `${facts.issueNum} <span class="dot">·</span> ${monthYear(facts.date)}` : '';

  return `<section class="section open-section" id="open">
  <div class="section-folio">
    <div class="section-folio-left">
      <span class="folio"><b>p.03</b> <span class="ruler"></span> Shipped.${folio ? ` <span class="dot">·</span> ${folio}` : ''}</span>
    </div>
    <span class="section-folio-sub">The Open</span>
  </div>

  <div class="open-grid">
    <div class="open-lead">
      <p class="open-quote">${quoteText}</p>
      <div class="open-prose">
        ${restHtml}
      </div>
    </div>
    <aside class="open-aside">
      <div>The brief</div>
      <div><b>Period</b> ${periodLabel}</div>
      ${days ? `<div><b>Days</b> ${days}</div>` : ''}
      ${facts ? `<div><b>Releases</b> ${facts.releaseCount}</div>` : ''}
    </aside>
  </div>
</section>`;
}

/** Inclusive day count of "YYYY-MM-DD to YYYY-MM-DD"; null when unparseable. */
export function periodDays(period: string): number | null {
  const m = /(\d{4}-\d{2}-\d{2})\s+to\s+(\d{4}-\d{2}-\d{2})/.exec(period);
  if (!m) return null;
  const ms = Date.parse(`${m[2]}T00:00:00Z`) - Date.parse(`${m[1]}T00:00:00Z`);
  return Number.isFinite(ms) ? Math.round(ms / 86400000) + 1 : null;
}

function monthYear(date: string): string {
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const m = /^(\d{4})-(\d{2})/.exec(date);
  return m ? `${months[Number(m[2]) - 1]} ${m[1]}` : date;
}

function formatPeriod(period: string): string {
  // "2026-03-27 to 2026-04-16" -> "Mar 27 -> Apr 16"
  const re = /(\d{4})-(\d{2})-(\d{2})\s+to\s+(\d{4})-(\d{2})-(\d{2})/;
  const m = re.exec(period);
  if (!m) return period;
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const m1 = months[Number(m[2]) - 1];
  const m2 = months[Number(m[5]) - 1];
  return `${m1} ${Number(m[3])} → ${m2} ${Number(m[6])}`;
}
