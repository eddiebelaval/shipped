/**
 * Renderer entry point.
 *
 * `renderIssue(markdownPath, options)` reads the markdown source, parses
 * it into a ParsedIssue, dispatches each section to the matching renderer,
 * splices the results into the template, writes the issue HTML, and
 * idempotently updates the archive page.
 */

import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

import { parseIssue, extractSweepTable } from './parse.js';
import { loadTemplate, render } from './template.js';
import { renderSweepTable } from './charts.js';
import { renderReleaseLog } from './release-log.js';
import { updateArchive } from './archive.js';
import {
  renderOpen,
  renderByTheNumbers,
  renderLeadStory,
  renderInvestigation,
  renderFeature,
  renderTimeline,
  renderSurvey,
  renderAlsoShipped,
  renderTermOfIssue,
  renderQuietOnWire,
  renderClose,
} from './sections/index.js';
import { fmtPrettyDate, pad2 } from './markdown.js';
import type { ParsedIssue, RenderOptions, RenderResult, Section } from './types.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Default deploy paths relative to the renderer module.
// The deployed id8labs.app site lives at id8/id8labs/ (inside the id8
// monorepo). The sibling id8labs/ at ~/Development/ is a legacy scaffold.
//   id8/shipped/pipeline/src/render/  →  ../../../id8labs/public/shipped
const DEFAULT_DEPLOY_ROOT = path.resolve(__dirname, '../../../../id8labs/public/shipped');

// ────────────────────────────────────────────────────────────────────
// Public entry point
// ────────────────────────────────────────────────────────────────────

export async function renderIssue(
  markdownPath: string,
  options: RenderOptions = {},
): Promise<RenderResult> {
  const absMarkdown = path.resolve(markdownPath);
  const markdown = await fs.readFile(absMarkdown, 'utf-8');
  const issue = parseIssue(markdown, absMarkdown);

  // Issue number maps 1:1 to the URL path. Historical +1 offset removed
  // 2026-04-22: it was leftover from Issue 00 being a dry-run, but it now
  // misleads (Issue 02 rendered at /shipped/03/). Source of truth is the
  // frontmatter `issue` field.
  const issueNum = pad2(issue.frontmatter.issue);
  const deployRoot =
    options.deployRoot ??
    process.env.SHIPPED_DEPLOY_PATH ??
    DEFAULT_DEPLOY_ROOT;

  const outputPath =
    options.outputPath ?? path.join(deployRoot, issueNum, 'index.html');
  const archivePath =
    options.archivePath ?? path.join(deployRoot, 'index.html');
  const scratchPath =
    options.scratchPath ?? '/tmp/shipped-render-output.html';

  // Build the template data dictionary.
  const data = await buildTemplateData(issue, issueNum);

  // Apply
  const template = await loadTemplate();
  const html = render(template, data);

  // Always write to scratch for diffing.
  await fs.writeFile(scratchPath, html, 'utf-8');

  if (!options.dryRun) {
    await fs.mkdir(path.dirname(outputPath), { recursive: true });
    await fs.writeFile(outputPath, html, 'utf-8');
    await updateArchive(archivePath, issue, issueNum);
  }

  return {
    outputPath,
    archivePath,
    wordCount: issue.wordCount,
    sectionCount: issue.sections.length,
    releaseLogEntryCount: issue.releaseLog.reduce((s, c) => s + c.entries.length, 0),
    scratchPath,
  };
}

// ────────────────────────────────────────────────────────────────────
// Template data builder
// ────────────────────────────────────────────────────────────────────

async function buildTemplateData(
  issue: ParsedIssue,
  issueNum: string,
): Promise<Record<string, string>> {
  const fm = issue.frontmatter;
  const find = (kindOrName: string): Section | undefined =>
    issue.sections.find((s) => s.kind === kindOrName || s.name === kindOrName);

  const datePretty = fmtPrettyDate(fm.date);
  const dateShort = datePretty.replace(/(\w+) (\d+), (\d+)/, '$1\u00a0$2, $3');
  const dateIsoSpaced = fm.date.replace(/-/g, ' — ');

  // Companion to the Lead — sweep table
  const companion = find('companion_lead');
  const sweep = companion ? extractSweepTable(companion.content) : null;
  const sweepHtml = sweep && sweep.kind === 'sweep_table' ? renderSweepTable(sweep.data) : '';

  // Editorial sections
  const open = find('open');
  const lead = find('lead_story');
  const investigation = find('investigation');
  const feature = find('feature');
  const timeline = find('timeline');
  const survey = find('survey');
  const cowork = find('cowork');
  const papers = find('papers');
  const alsoShipped = find('also_shipped');
  const term = find('term_of_issue');
  const quiet = find('quiet_on_wire');
  const close = find('close');

  // Compute "next issue" date (current + 7 days)
  const nextIssueDate = computeNextIssueDate(fm.date);

  // Build cover bottom row from frontmatter (term_of_issue + optional cover_bottom array).
  const coverBottomRow = renderCoverBottomRow(fm as unknown as { term_of_issue?: string; cover_bottom?: Array<{ label: string; val: string }> });

  const releaseLogHtml = renderReleaseLog(issue.releaseLog);
  const releaseLogCount = issue.releaseLog.reduce((s, c) => s + c.entries.length, 0);

  return {
    // Meta
    meta_title: `Shipped. — Issue ${issueNum} — ${stripTitlePrefix(fm.title)}`,
    meta_description: `A weekly magazine on what Anthropic ships. Issue ${issueNum} — ${fm.deck ?? stripTitlePrefix(fm.title)}.`,
    meta_description_short: 'A weekly magazine on what Anthropic ships.',
    canonical_url: `https://id8labs.app/shipped/${issueNum}/`,
    og_image_url: `https://id8labs.app/shipped/${issueNum}/og.png?v=2`,
    author: 'Eddie Belaval',

    // Pub bar
    issue_num: issueNum,
    date_short: dateShort,

    // Cover
    volume: 'I',
    cover_label: stripTitlePrefix(fm.title) || `Issue ${issueNum}`,
    cover_sub: fm.deck ?? `Week of ${fm.date}.`,
    date_iso_spaced: dateIsoSpaced,
    period: fmtPeriod(fm.period),
    cover_top_meta: `${releaseLogCount} Releases · ${computePeriodLabel(fm.period)}`,
    cover_huge_num: issueNum,
    cover_deck: stripTitlePrefix(fm.title),
    cover_deckline: fm.deck ?? '',
    cover_bottom_row: coverBottomRow,
    toc_html: renderToc(issue.sections, issueNum),
    sources_html: renderSources(fm as unknown as { sources?: string[] }),

    // Editorial
    'section:open': open ? renderOpen(open, fm.period) : '',
    'section:by_the_numbers': renderByTheNumbers(fm.by_the_numbers as { head?: string; deck?: string; cells?: Array<{ label: string; value: string; note?: string; size?: 3 | 4 | 6; accent?: boolean }> } | undefined),
    'section:lead_story': lead ? renderLeadStory(lead) : '',
    'chart:sweep_table': sweepHtml,
    'section:investigation': investigation ? renderInvestigation(investigation) : '',
    'section:feature': feature ? renderFeature(feature) : '',
    'section:timeline': timeline ? renderTimeline(timeline) : '',
    'section:survey': survey ? renderSurvey(survey) : '',
    'section:also_shipped': renderAlsoShipped(alsoShipped, cowork, papers),
    'section:term_of_issue': term ? renderTermOfIssue(term) : '',
    'section:quiet_on_wire': quiet ? renderQuietOnWire(quiet) : '',
    'section:close': close ? renderClose(close) : '',

    // Release log
    release_log_sections: releaseLogHtml,

    // Colophon
    word_count: String(issue.wordCount),
    release_log_count: String(releaseLogCount),
    release_log_sections_count: String(issue.releaseLog.length),
    status_display: fm.status === 'dry-run' ? 'Published' : capitalize(fm.status),
    next_issue_date: nextIssueDate,
    next_issue_label: `Issue ${pad2(fm.issue + 2)}`,
    next_issue_date_long: nextIssueDate.replace(',', '') + ' at 9 AM ET',
  };
}

function stripTitlePrefix(title: string): string {
  // "The Founding Issue — The Shadow Release" → "The Shadow Release"
  const parts = title.split(' — ');
  return parts[parts.length - 1] ?? title;
}

function fmtPeriod(period: string): string {
  // Pass-through with space normalization
  return period.replace(/\s+/g, ' ').trim().replace(/ to /, ' → ');
}

function renderToc(sections: Array<{ name: string; kind: string }>, issueNum: string): string {
  // Skip non-editorial sections in the ToC.
  const editorialKinds = new Set([
    'open', 'in_this_issue', 'by_the_numbers', 'lead_story',
    'companion_lead', 'feature', 'investigation', 'also_shipped',
    'timeline', 'survey', 'cowork', 'papers', 'term_of_issue',
    'quiet_on_wire', 'close',
  ]);
  const entries = sections
    .filter(s => editorialKinds.has(s.kind))
    .map((s, i) => {
      const anchor = '#' + s.name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
      const num = String(i + 1).padStart(2, '0');
      return `<a href="${anchor}" class="toc-entry">
      <span class="toc-entry-n">${num}</span>
      <div class="toc-entry-body">
        <span class="toc-entry-kicker">${s.name}</span>
      </div>
    </a>`;
    })
    .join('\n    ');

  if (!entries) return '';
  return `<section class="section toc-section" id="contents">
  <div class="section-folio">
    <div class="section-folio-left">
      <span class="folio"><b>p.02</b> <span class="ruler"></span> Shipped. <span class="dot">·</span> ${issueNum} <span class="dot">·</span> Front of book</span>
    </div>
    <span class="section-folio-sub">Front of book</span>
  </div>

  <div class="toc-head">
    <div class="toc-head-num">${issueNum}</div>
    <div class="toc-head-title">In this issue,</div>
  </div>

  <div class="toc-grid">
    ${entries}
  </div>
</section>`;
}

function renderSources(fm: { sources?: string[] }): string {
  const sources = Array.isArray(fm.sources) ? fm.sources : [];
  if (sources.length === 0) return '';

  const items = sources
    .filter((s) => typeof s === 'string' && /^https?:\/\//.test(s))
    .map((url) => {
      const host = url.match(/^https?:\/\/([^/]+)/)?.[1] ?? url;
      return `<li><a href="${url}" style="color:var(--ink);text-decoration:none;border-bottom:1px solid rgba(0,0,0,0.2)" target="_blank" rel="noopener">${host}</a></li>`;
    })
    .join('\n          ');

  if (!items) return '';

  return `<section style="max-width:1240px;margin:96px auto 64px;padding:0 32px">
  <div style="display:flex;align-items:baseline;justify-content:space-between;border-bottom:2px solid var(--ink);padding-bottom:14px;margin-bottom:32px">
    <span style="font-family:var(--narrow);font-weight:700;font-size:12px;letter-spacing:.25em;text-transform:uppercase;color:var(--orange)">Sources</span>
    <span style="font-family:var(--sans);font-size:13px;color:var(--muted)">Every claim traceable</span>
  </div>

  <div style="background:#ffffff;border:1px solid rgba(0,0,0,0.08);padding:48px 56px">
    <ul style="list-style:none;padding:0;margin:0;font-family:var(--sans);font-size:13px;line-height:1.9;color:var(--ink);columns:2;column-gap:48px">
          ${items}
    </ul>
  </div>
</section>`;
}

function computePeriodLabel(period: string | undefined): string {
  if (!period) return '7 Days';
  const m = period.match(/(\d{4}-\d{2}-\d{2}).*?(\d{4}-\d{2}-\d{2})/);
  if (!m) return '7 Days';
  const start = new Date(m[1]!);
  const end = new Date(m[2]!);
  const days = Math.round((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24));
  return `${days} Days`;
}

function computeNextIssueDate(date: string): string {
  const d = new Date(date);
  d.setUTCDate(d.getUTCDate() + 7);
  return fmtPrettyDate(d.toISOString().slice(0, 10));
}

function capitalize(s: string): string {
  return s.length === 0 ? s : s[0]!.toUpperCase() + s.slice(1);
}

function renderCoverBottomRow(fm?: { term_of_issue?: string; cover_bottom?: Array<{ label: string; val: string }> }): string {
  // Per-issue override via frontmatter `cover_bottom` array. Fallback to a
  // generic four-cell layout with Term of the Issue if provided.
  if (fm?.cover_bottom && Array.isArray(fm.cover_bottom)) {
    const cells = fm.cover_bottom
      .map(
        (c) => `<div class="cover-bottom-cell">
      <span class="cover-bottom-label">${c.label}</span>
      <span class="cover-bottom-val">${c.val}</span>
    </div>`,
      )
      .join('\n    ');
    return `<div class="cover-bottom">\n    ${cells}\n  </div>`;
  }
  const termCell = fm?.term_of_issue
    ? `<div class="cover-bottom-cell">
      <span class="cover-bottom-label">The Term</span>
      <span class="cover-bottom-val"><em>${fm.term_of_issue.toLowerCase()}</em></span>
    </div>`
    : '';
  return `<div class="cover-bottom">\n    ${termCell}\n  </div>`;
}
