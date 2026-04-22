/**
 * Shipped. — Dashboard HTML template.
 *
 * Self-contained HTML + CSS + JS in one file. No external dependencies
 * beyond Google Fonts. Matches the Shipped. magazine aesthetic
 * (Fraunces display serif, Archivo sans, orange #FF6B35 accent).
 *
 * Drag-drop is visual-only in v0.1 — reorder in browser, does not persist.
 * v0.2 will add a local HTTP server that accepts POST /move and writes
 * back to article frontmatter.
 */

import type { Dashboard, DashboardArticle, SectionSlot } from './generate.js';

// ────────────────────────────────────────────────────────────────────
// Public entry point
// ────────────────────────────────────────────────────────────────────

export interface RenderOptions {
  live?: boolean;   // true when served by dashboard-dev; enables writeback POSTs
  port?: number;   // server port when live
}

export function renderDashboard(d: Dashboard, opts: RenderOptions = {}): string {
  const live = opts.live === true;
  const port = opts.port ?? 4321;
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Shipped. Dashboard — Issue ${escapeHtml(d.issue)}${live ? ' · LIVE' : ''}</title>
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ccircle cx='75' cy='62' r='14' fill='%23FF6B35'/%3E%3Ctext x='10' y='75' font-family='Georgia,serif' font-weight='700' font-size='62' fill='%231a1a1a'%3ES%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,700;1,9..144,400;1,9..144,500&family=Archivo:wght@400;500;600;700&family=Archivo+Narrow:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>${CSS}</style>
</head>
<body${live ? ' data-live="1"' : ''} data-view="table">
  ${renderPubBar(d, live)}
  ${renderHeader(d)}
  ${renderGapStrip(d)}
  <main class="stage" data-view-pane="table">
    ${renderSidebar(d)}
    ${renderCanvas(d)}
  </main>
  ${renderMagazineMockup(d)}
  ${renderFooter(d, live)}
  <div class="toast" id="dashboard-toast" role="status" aria-live="polite" hidden></div>
  <script>window.__SHIPPED_LIVE__ = ${live ? 'true' : 'false'}; window.__SHIPPED_PORT__ = ${port};</script>
  <script>${JS}</script>
</body>
</html>`;
}

// ────────────────────────────────────────────────────────────────────
// Rendering
// ────────────────────────────────────────────────────────────────────

function renderPubBar(d: Dashboard, live: boolean): string {
  const genTime = new Date(d.generatedAt);
  const timeStr = genTime.toLocaleString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true });
  const liveBadge = live
    ? '<span class="live-dot" title="Dev server running · drag-drop persists"></span><span class="pub-bar-meta live-label">LIVE</span><span class="pub-bar-sep"></span>'
    : '';
  return `
<header class="pub-bar">
  <div class="pub-bar-left">
    <span class="pub-bar-mark">Shipped<span class="dot">.</span></span>
    <span class="pub-bar-sep"></span>
    <span class="pub-bar-meta">Production Table</span>
    <span class="pub-bar-sep"></span>
    ${liveBadge}
  </div>
  <div class="pub-bar-right">
    <div class="view-toggle" role="tablist" aria-label="View">
      <button class="view-toggle-btn active" type="button" data-view="table" role="tab" aria-selected="true">Table</button>
      <button class="view-toggle-btn" type="button" data-view="mockup" role="tab" aria-selected="false">Mockup</button>
    </div>
    <span class="pub-bar-sep"></span>
    <span class="pub-bar-meta">Issue <b>${escapeHtml(d.issue)}</b></span>
    <span class="pub-bar-sep"></span>
    <span class="pub-bar-meta">ship · <b>${escapeHtml(d.shipDate || 'TBD')}</b></span>
    <span class="pub-bar-sep"></span>
    <span class="pub-bar-meta">lock · <b>${escapeHtml(d.lockDate || 'TBD')}</b></span>
    <span class="pub-bar-sep"></span>
    <span class="pub-bar-folio">rendered · ${escapeHtml(timeStr)}</span>
  </div>
</header>`;
}

function renderHeader(d: Dashboard): string {
  const readinessTier =
    d.readinessPercent >= 90 ? 'tier-ship'
    : d.readinessPercent >= 70 ? 'tier-track'
    : d.readinessPercent >= 50 ? 'tier-mid'
    : 'tier-early';

  return `
<section class="issue-header">
  <div class="issue-header-inner">
    <div class="issue-head-left">
      <div class="kicker">Issue <b>${escapeHtml(d.issue)}</b> · ${escapeHtml(d.status || 'drafting')}</div>
      <h1 class="issue-title">
        ${d.title && d.title !== 'TBD' ? escapeHtml(d.title) : '<span class="unset">Title TBD</span>'}
      </h1>
      <div class="issue-slug">
        slug:
        ${d.slug && d.slug !== 'TBD' ? `<code>${escapeHtml(d.slug)}</code>` : '<span class="unset">TBD</span>'}
        ${d.theme ? `<span class="sep">·</span> term · <em>${escapeHtml(d.theme)}</em>` : ''}
      </div>
    </div>
    <div class="issue-head-right">
      <div class="readiness ${readinessTier}">
        <div class="readiness-label">${escapeHtml(d.readinessLabel)}</div>
        <div class="readiness-number">${d.readinessPercent}<span>%</span></div>
        <div class="readiness-bar"><div class="readiness-fill" style="width:${d.readinessPercent}%"></div></div>
        <div class="readiness-meta">
          ${d.articleCountTotal} source article${d.articleCountTotal === 1 ? '' : 's'} ·
          formula ${d.articleCountHealthy.min}–${d.articleCountHealthy.max}
        </div>
      </div>
    </div>
  </div>
</section>`;
}

function renderGapStrip(d: Dashboard): string {
  if (d.gaps.length === 0) {
    return `<div class="gap-strip gap-strip-clear"><span class="gap-dot"></span> No gaps — all required sections have source material.</div>`;
  }
  const items = d.gaps.map(g => `<li>${escapeHtml(g)}</li>`).join('');
  return `
<div class="gap-strip">
  <div class="gap-strip-label">Gaps · ${d.gaps.length}</div>
  <ul class="gap-list">${items}</ul>
</div>`;
}

function renderSidebar(d: Dashboard): string {
  const allArticles = [
    ...d.sections.flatMap(s => s.articles),
    ...d.scratchPad,
  ];
  const cards = allArticles.map(renderArticleCard).join('');

  return `
<aside class="sidebar">
  <div class="sidebar-head">
    <div class="folio"><b>01</b><span class="ruler"></span><span>The Dock</span></div>
    <div class="sidebar-sub">All articles · drag to place</div>
  </div>
  <div class="sidebar-body">
    ${cards || '<div class="empty-state">No articles yet. Run /shipped-wip --capture to add one.</div>'}
  </div>
  ${d.scratchPad.length > 0 ? renderScratchPad(d.scratchPad) : ''}
</aside>`;
}

function renderScratchPad(articles: DashboardArticle[]): string {
  const cards = articles.map(renderArticleCard).join('');
  return `
<div class="scratch-pad">
  <div class="scratch-head">
    <div class="folio"><b>02</b><span class="ruler"></span><span>Scratch pad</span></div>
    <div class="scratch-sub">${articles.length} unhomed · no section assigned</div>
  </div>
  <div class="scratch-body">${cards}</div>
</div>`;
}

function renderArticleCard(a: DashboardArticle): string {
  const statusClass = `status-${a.status}`;
  const placement = a.section && a.section !== 'background'
    ? `<span class="card-section">${escapeHtml(a.section)}</span>`
    : '<span class="card-section card-section-unset">unhomed</span>';

  const placementOpen = a.placementOpen
    ? `<div class="card-flag">◇ placement open</div>`
    : '';

  const cardId = `card-${a.filename.replace(/[^a-z0-9]/gi, '-')}`;

  return `
<article class="article-card" draggable="true"
  data-filename="${escapeHtml(a.filename)}"
  data-section="${escapeHtml(a.section)}"
  data-status="${escapeHtml(a.status)}"
  data-wordcount="${a.wordCount}"
  id="${cardId}">
  <header class="card-head">
    <span class="card-status ${statusClass}">${escapeHtml(a.status)}</span>
    ${renderGradeBadge(a)}
  </header>
  <h3 class="card-title">${escapeHtml(a.title)}</h3>
  <div class="card-meta">
    <span>${a.wordCount} w</span>
    <span class="card-dot">·</span>
    <span>${a.sourceCount} source${a.sourceCount === 1 ? '' : 's'}</span>
    <span class="card-dot">·</span>
    ${placement}
  </div>
  ${placementOpen}
  ${renderGradePanel(a)}
  <footer class="card-foot">
    <span class="card-file">${escapeHtml(a.filename)}</span>
    <button class="card-grade-toggle" type="button" data-target="${cardId}-notes" aria-label="Toggle grade notes">notes ▾</button>
  </footer>
</article>`;
}

function renderGradeBadge(a: DashboardArticle): string {
  const g = a.grade;
  const letterClass = `grade-${g.letter.toLowerCase()}`;
  if (g.overridden) {
    return `<span class="grade-badge grade-override" title="Grade override: ${escapeHtml(g.overrideReason ?? '')}">OVR</span>`;
  }
  return `<span class="grade-badge ${letterClass}" title="${g.total}/28 · ${escapeHtml(g.status)}">${g.letter}<span class="grade-num">${g.total}</span></span>`;
}

function renderGradePanel(a: DashboardArticle): string {
  const g = a.grade;
  const cardId = `card-${a.filename.replace(/[^a-z0-9]/gi, '-')}`;

  if (g.overridden) {
    return `
<div class="grade-panel" id="${cardId}-notes" hidden>
  <div class="grade-panel-head">
    <span class="grade-panel-total">Override</span>
    <span class="grade-panel-status">${escapeHtml(g.status)}</span>
  </div>
  <div class="grade-override-reason">${escapeHtml(g.overrideReason ?? 'No reason given')}</div>
</div>`;
  }

  const dimensions = g.dimensions.map(d => `
<li class="grade-dim">
  <div class="grade-dim-head">
    <span class="grade-dim-letter grade-${d.letter.toLowerCase()}">${d.letter}</span>
    <span class="grade-dim-label">${escapeHtml(d.label)}</span>
    <span class="grade-dim-score">${d.score}/4</span>
  </div>
  <div class="grade-dim-note">${escapeHtml(d.note)}</div>
</li>`).join('');

  return `
<div class="grade-panel" id="${cardId}-notes" hidden>
  <div class="grade-panel-head">
    <span class="grade-panel-total">${g.total}<small>/28</small></span>
    <span class="grade-panel-status">${escapeHtml(g.status)}</span>
  </div>
  <ul class="grade-dims">${dimensions}</ul>
  <div class="grade-panel-foot">
    <span>Rubric: <code>content/RUBRIC.md</code></span>
  </div>
</div>`;
}

function renderCanvas(d: Dashboard): string {
  const mandatory = d.sections.filter(s => s.slotKind === 'mandatory');
  const shelf = d.sections.filter(s => s.slotKind === 'shelf');

  return `
<section class="canvas">
  <div class="canvas-head">
    <div class="folio"><b>03</b><span class="ruler"></span><span>The Issue</span></div>
    <div class="canvas-sub">Front-of-book skeleton · mandatory core + optional shelf</div>
  </div>
  <div class="canvas-stack">
    <div class="canvas-group">
      <div class="group-label">Mandatory core</div>
      ${mandatory.map(renderSlot).join('')}
    </div>
    <div class="canvas-group">
      <div class="group-label">Optional shelf · include when the week earns it</div>
      ${shelf.map(renderSlot).join('')}
    </div>
  </div>
</section>`;
}

function renderSlot(s: SectionSlot): string {
  const filledClass = s.filled ? 'slot-filled' : (s.required ? 'slot-gap' : 'slot-empty');
  const bar = renderBudgetBar(s);
  const articles = s.articles.length > 0
    ? s.articles.map(renderSlotArticle).join('')
    : '<div class="slot-dropzone">Drop an article here, or /shipped-wip --capture to add one.</div>';

  const countBadge = s.articleCountMin > 0
    ? `<span class="slot-badge">${s.articles.length} / ${s.articleCountMin}${s.articleCountMax > s.articleCountMin ? `–${s.articleCountMax}` : ''}</span>`
    : '';

  return `
<section class="slot ${filledClass}" data-section="${escapeHtml(s.key)}">
  <header class="slot-head">
    <div class="slot-head-left">
      <span class="slot-status-dot"></span>
      <h2 class="slot-title">${escapeHtml(s.label)}</h2>
      ${s.required ? '<span class="slot-required">required</span>' : '<span class="slot-optional">optional</span>'}
      ${countBadge}
    </div>
    ${bar}
  </header>
  <p class="slot-desc">${escapeHtml(s.description)}</p>
  <div class="slot-body">${articles}</div>
  ${s.gap ? `<div class="slot-gap-note">⚠ ${escapeHtml(s.gap)}</div>` : ''}
</section>`;
}

function renderBudgetBar(s: SectionSlot): string {
  if (s.wordBudgetMin === 0 && s.wordBudgetMax === 0) {
    return '<div class="slot-budget slot-budget-none">unbounded</div>';
  }
  const currentWords = s.articles.reduce((sum, a) => sum + a.wordCount, 0);
  const target = s.wordBudgetMax;
  const pct = Math.min(100, Math.round((currentWords / target) * 100));
  const state = currentWords >= s.wordBudgetMin && currentWords <= s.wordBudgetMax ? 'in-range'
              : currentWords > s.wordBudgetMax ? 'over'
              : 'under';
  return `
<div class="slot-budget">
  <div class="budget-meta">
    <span class="budget-current">${currentWords}w</span>
    <span class="budget-target">${s.wordBudgetMin}–${s.wordBudgetMax}</span>
  </div>
  <div class="budget-bar">
    <div class="budget-fill budget-${state}" style="width:${pct}%"></div>
    <div class="budget-zone" style="left:${(s.wordBudgetMin / target) * 100}%;width:${((s.wordBudgetMax - s.wordBudgetMin) / target) * 100}%"></div>
  </div>
</div>`;
}

function renderSlotArticle(a: DashboardArticle): string {
  return `
<div class="slot-article" data-filename="${escapeHtml(a.filename)}">
  <div class="slot-article-left">
    <span class="card-status status-${escapeHtml(a.status)}">${escapeHtml(a.status)}</span>
    <h4 class="slot-article-title">${escapeHtml(a.title)}</h4>
    <div class="slot-article-file">${escapeHtml(a.filename)} · ${a.wordCount}w · ${a.sourceCount} src</div>
  </div>
  ${a.placementOpen ? '<div class="card-flag">◇ placement open</div>' : ''}
</div>`;
}

function renderMagazineMockup(d: Dashboard): string {
  // Compose the filled sections + Term of Issue + Close as a magazine storyboard
  const allArticles = [
    ...d.sections.flatMap(s => s.articles.map(a => ({ slot: s, article: a }))),
  ];

  const spreads = d.sections.filter(s => s.required || s.articles.length > 0).map(slot => {
    const articles = slot.articles;
    const isLead = slot.key === 'lead-story';
    const isInvestigation = slot.key === 'investigation';
    const isMulti = articles.length > 1;

    let headlineArticle = articles[0];
    if (!headlineArticle && slot.required) {
      return `
<section class="mockup-spread mockup-spread-empty">
  <div class="mockup-kicker">${escapeHtml(slot.label)}</div>
  <h2 class="mockup-headline mockup-headline-empty">— pending —</h2>
  <div class="mockup-dek">No source article placed yet.</div>
</section>`;
    }
    if (!headlineArticle) return '';

    const supportingArticles = articles.slice(1);
    const supportLine = supportingArticles.length > 0
      ? `<div class="mockup-support">with: ${supportingArticles.map(a => escapeHtml(a.title)).join(' · ')}</div>`
      : '';

    const statusPill = `<span class="mockup-status mockup-status-${escapeHtml(headlineArticle.status)}">${escapeHtml(headlineArticle.status)}</span>`;
    const gradeChip = headlineArticle.grade.overridden
      ? '<span class="mockup-grade grade-override">OVR</span>'
      : `<span class="mockup-grade grade-${headlineArticle.grade.letter.toLowerCase()}">${headlineArticle.grade.letter}</span>`;

    const classes = ['mockup-spread'];
    if (isLead) classes.push('mockup-spread-lead');
    if (isInvestigation) classes.push('mockup-spread-investigation');

    const heroImage = headlineArticle.heroImage;
    const imageBlock = heroImage
      ? `<div class="mockup-hero"><img src="${escapeHtml(heroImage)}" alt="" loading="lazy"/><button class="mockup-image-btn mockup-image-btn-change" type="button" data-filename="${escapeHtml(headlineArticle.filename)}" data-current="${escapeHtml(heroImage)}">change image</button></div>`
      : `<button class="mockup-image-btn mockup-image-btn-add" type="button" data-filename="${escapeHtml(headlineArticle.filename)}">+ add hero image</button>`;

    return `
<section class="${classes.join(' ')}">
  <div class="mockup-meta">
    <span class="mockup-kicker">${escapeHtml(slot.label)}</span>
    ${statusPill}
    ${gradeChip}
  </div>
  ${imageBlock}
  <h2 class="mockup-headline">${escapeHtml(headlineArticle.title)}</h2>
  <div class="mockup-dek">${escapeHtml(slot.description)}</div>
  ${supportLine}
  <div class="mockup-footer">
    <span class="mockup-file">${escapeHtml(headlineArticle.filename)}</span>
    <span class="mockup-budget">${headlineArticle.wordCount}w · budget ${slot.wordBudgetMin}–${slot.wordBudgetMax}</span>
  </div>
</section>`;
  }).filter(Boolean).join('');

  return `
<main class="magazine-mockup" data-view-pane="mockup" hidden>
  <div class="mockup-cover">
    <div class="mockup-cover-top">
      <span class="mockup-cover-kicker">Volume I · Issue <b>${escapeHtml(d.issue)}</b></span>
      <span class="mockup-cover-date">${escapeHtml(d.shipDate || 'ship TBD')}</span>
    </div>
    <h1 class="mockup-cover-title">${d.title && d.title !== 'TBD' ? escapeHtml(d.title) : '<em>Title TBD</em>'}</h1>
    ${d.theme ? `<p class="mockup-cover-deck">Term of the Issue · <em>${escapeHtml(d.theme)}</em></p>` : ''}
    <div class="mockup-cover-rule"></div>
    <div class="mockup-cover-foot">
      Shipped<span class="dot">.</span> — a weekly magazine on what Anthropic ships
    </div>
  </div>
  <div class="mockup-storyboard">
    <div class="mockup-toc-label">Front of book</div>
    ${spreads}
  </div>
  <div class="mockup-notice">
    Mockup preview — storyboard only. Prose renders at ship time via the pipeline.
  </div>
</main>`;
}

function renderFooter(d: Dashboard, live: boolean): string {
  const writebackLabel = live
    ? '<span class="foot-writeback-on">drag-drop · persists to frontmatter</span>'
    : '<span>drag-drop · visual-only (run <code>pnpm dashboard-dev</code> to persist)</span>';
  return `
<footer class="page-foot">
  <div class="foot-left">
    <span class="pub-bar-mark">Shipped<span class="dot">.</span></span>
    Production Table · ${live ? 'v0.2 live' : 'v0.1 static'}
  </div>
  <div class="foot-right">
    ${writebackLabel}
    <span class="pub-bar-sep"></span>
    <span>rubric · <code>content/RUBRIC.md</code></span>
    <span class="pub-bar-sep"></span>
    <span>formula · <code>content/FORMULA.md</code></span>
  </div>
</footer>`;
}

// ────────────────────────────────────────────────────────────────────
// Escaping
// ────────────────────────────────────────────────────────────────────

function escapeHtml(s: string): string {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

// ────────────────────────────────────────────────────────────────────
// CSS — editorial brutalism + print craft
// ────────────────────────────────────────────────────────────────────

const CSS = `
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{font-size:16px;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;text-rendering:optimizeLegibility}
body{background:#fafaf7;color:#0b0b0b;font-family:'Archivo',sans-serif;min-height:100vh}
::selection{background:#FF6B35;color:#fff}

:root{
  --orange:#FF6B35;
  --ink:#0b0b0b;
  --paper:#fafaf7;
  --paper-shadow:#f2f0e8;
  --paper-alt:#f6f4ed;
  --body:#2a2a2a;
  --muted:#5a5a5a;
  --gray:#8a8a8a;
  --hair:rgba(11,11,11,0.12);
  --hair-soft:rgba(11,11,11,0.06);
  --hair-hard:rgba(11,11,11,0.22);
  --green:#2b7d4f;
  --red:#b8361e;
  --amber:#b87517;
  --disp:'Fraunces','Times New Roman',serif;
  --sans:'Archivo',system-ui,sans-serif;
  --narrow:'Archivo Narrow','Archivo',sans-serif;
  --mono:'JetBrains Mono',ui-monospace,monospace;
}

body::before{
  content:"";position:fixed;inset:0;pointer-events:none;z-index:1000;opacity:.04;mix-blend-mode:multiply;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='180' height='180'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' seed='3'/><feColorMatrix values='0 0 0 0 0.02  0 0 0 0 0.02  0 0 0 0 0.02  0 0 0 0.22 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");
}

/* ── Publication bar ─────────────────────────────────────── */
.pub-bar{
  position:sticky;top:0;z-index:100;
  background:var(--paper);
  border-bottom:1px solid var(--hair);
  padding:0 28px;height:42px;
  display:flex;align-items:center;justify-content:space-between;
  font-family:var(--narrow);
  font-size:11px;font-weight:600;letter-spacing:.22em;
  text-transform:uppercase;color:var(--ink);
}
.pub-bar-left,.pub-bar-right{display:flex;align-items:center;gap:16px}
.pub-bar-mark{font-family:var(--disp);font-weight:500;font-size:16px;letter-spacing:-.01em;text-transform:none;font-style:italic}
.pub-bar-mark .dot{color:var(--orange)}
.pub-bar-sep{width:1px;height:12px;background:var(--hair-hard)}
.pub-bar-meta{color:var(--muted)}
.pub-bar-folio{color:var(--ink)}
.pub-bar-folio b{font-weight:600;color:var(--orange)}
.live-dot{
  display:inline-block;width:8px;height:8px;border-radius:50%;
  background:var(--green);margin-right:6px;
  box-shadow:0 0 0 3px rgba(43,125,79,.18);
  animation:pulse 1.8s infinite;
}
.live-label{color:var(--green);font-weight:700;letter-spacing:.28em}
@keyframes pulse{
  0%,100%{box-shadow:0 0 0 3px rgba(43,125,79,.18)}
  50%{box-shadow:0 0 0 6px rgba(43,125,79,.06)}
}
.foot-writeback-on{color:var(--green);font-weight:700}

/* ── Folio ─────────────────────────────────────── */
.folio{
  font-family:var(--narrow);
  font-size:10px;font-weight:500;letter-spacing:.28em;
  text-transform:uppercase;color:var(--gray);
  display:flex;align-items:center;gap:10px;
}
.folio b{color:var(--ink);font-weight:700}
.folio .ruler{width:28px;height:1px;background:var(--hair-hard)}

/* ── Issue header ─────────────────────────────────────── */
.issue-header{
  border-bottom:1px solid var(--ink);
  background:var(--paper);
  padding:48px 28px 40px;
}
.issue-header-inner{
  max-width:1600px;margin:0 auto;
  display:grid;grid-template-columns:1fr auto;gap:40px;align-items:end;
}
.kicker{
  font-family:var(--narrow);
  font-size:10px;font-weight:600;letter-spacing:.32em;
  text-transform:uppercase;color:var(--muted);
  margin-bottom:10px;
}
.kicker b{color:var(--orange);font-weight:700}
.issue-title{
  font-family:var(--disp);
  font-weight:500;
  font-size:clamp(36px,5vw,64px);
  line-height:.98;
  letter-spacing:-.04em;
  color:var(--ink);
  margin-bottom:16px;
}
.issue-title .unset{color:var(--gray);font-style:italic;font-weight:400}
.issue-slug{
  font-family:var(--narrow);
  font-size:12px;font-weight:500;letter-spacing:.2em;
  text-transform:uppercase;color:var(--muted);
}
.issue-slug code{
  font-family:var(--mono);
  font-size:11px;padding:2px 8px;
  background:var(--paper-shadow);border:1px solid var(--hair);
  color:var(--ink);letter-spacing:0;
}
.issue-slug .unset{color:var(--gray);font-style:italic;text-transform:none;letter-spacing:0}
.issue-slug em{font-family:var(--disp);font-style:italic;color:var(--orange);font-weight:500;letter-spacing:0;font-size:14px;text-transform:none}
.issue-slug .sep{margin:0 10px;color:var(--hair-hard)}

.readiness{min-width:260px}
.readiness-label{
  font-family:var(--narrow);
  font-size:10px;font-weight:700;letter-spacing:.28em;
  text-transform:uppercase;color:var(--muted);
  margin-bottom:4px;
}
.readiness-number{
  font-family:var(--disp);
  font-weight:500;font-size:56px;line-height:1;letter-spacing:-.03em;
  color:var(--ink);
}
.readiness-number span{font-size:22px;color:var(--gray);margin-left:4px;font-weight:400}
.readiness-bar{
  height:3px;background:var(--paper-shadow);margin:12px 0 8px;position:relative;border:1px solid var(--hair);
}
.readiness-fill{height:100%;background:var(--ink);transition:width .4s}
.readiness.tier-ship .readiness-fill{background:var(--green)}
.readiness.tier-ship .readiness-number{color:var(--green)}
.readiness.tier-track .readiness-fill{background:var(--ink)}
.readiness.tier-mid .readiness-fill{background:var(--amber)}
.readiness.tier-mid .readiness-number{color:var(--amber)}
.readiness.tier-early .readiness-fill{background:var(--red)}
.readiness.tier-early .readiness-number{color:var(--red)}
.readiness-meta{
  font-family:var(--narrow);
  font-size:10px;font-weight:500;letter-spacing:.18em;
  text-transform:uppercase;color:var(--muted);
}

/* ── Gap strip ─────────────────────────────────────── */
.gap-strip{
  background:var(--paper-alt);
  border-bottom:1px solid var(--hair);
  padding:16px 28px;
  display:flex;align-items:flex-start;gap:24px;
}
.gap-strip-label{
  font-family:var(--narrow);
  font-size:10px;font-weight:700;letter-spacing:.28em;
  text-transform:uppercase;color:var(--red);
  flex:0 0 auto;padding-top:3px;
}
.gap-list{
  list-style:none;display:flex;flex-wrap:wrap;gap:8px 24px;
  font-family:var(--sans);font-size:13px;color:var(--body);
}
.gap-list li{position:relative;padding-left:14px}
.gap-list li::before{content:"●";position:absolute;left:0;top:-1px;color:var(--amber);font-size:8px}
.gap-strip-clear{
  font-family:var(--narrow);
  font-size:11px;font-weight:500;letter-spacing:.22em;
  text-transform:uppercase;color:var(--green);
}
.gap-strip-clear .gap-dot{
  display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--green);margin-right:10px;vertical-align:middle;
}

/* ── Stage (sidebar + canvas) ─────────────────────────────────────── */
.stage{
  display:grid;grid-template-columns:320px 1fr;gap:0;
  min-height:calc(100vh - 320px);
  max-width:1600px;margin:0 auto;
}
@media (max-width:900px){
  .stage{grid-template-columns:1fr}
}

/* ── Sidebar ─────────────────────────────────────── */
.sidebar{
  background:var(--paper-alt);
  border-right:1px solid var(--hair);
  padding:28px 20px;
  max-height:calc(100vh - 42px);
  overflow-y:auto;
  position:sticky;top:42px;
}
.sidebar-head{margin-bottom:20px;padding-bottom:16px;border-bottom:1px solid var(--hair)}
.sidebar-sub{
  font-family:var(--narrow);font-size:11px;font-weight:500;letter-spacing:.18em;
  text-transform:uppercase;color:var(--muted);margin-top:6px;
}
.sidebar-body{display:flex;flex-direction:column;gap:10px}
.empty-state{
  font-family:var(--disp);font-style:italic;color:var(--gray);font-size:14px;
  padding:24px 12px;text-align:center;
}
.scratch-pad{margin-top:32px;padding-top:20px;border-top:1px dashed var(--hair-hard)}
.scratch-head{margin-bottom:14px}
.scratch-sub{
  font-family:var(--narrow);font-size:10px;font-weight:500;letter-spacing:.18em;
  text-transform:uppercase;color:var(--muted);margin-top:4px;
}
.scratch-body{display:flex;flex-direction:column;gap:10px}

/* ── Article card ─────────────────────────────────────── */
.article-card{
  background:var(--paper);
  border:1px solid var(--hair-hard);
  padding:12px 14px;
  cursor:grab;
  position:relative;
  transition:transform .12s,box-shadow .12s,border-color .12s;
}
.article-card:hover{border-color:var(--ink);transform:translateY(-1px);box-shadow:0 4px 0 var(--paper-shadow)}
.article-card:active{cursor:grabbing;transform:scale(.98)}
.article-card.dragging{opacity:.4}
.card-head{
  display:flex;align-items:center;justify-content:space-between;
  margin-bottom:8px;gap:8px;
}
.card-status{
  font-family:var(--narrow);
  font-size:9px;font-weight:700;letter-spacing:.18em;
  text-transform:uppercase;padding:2px 6px;
  border:1px solid;
}
.status-research{color:var(--amber);border-color:var(--amber);background:rgba(184,117,23,.06)}
.status-draft{color:var(--ink);border-color:var(--ink);background:rgba(11,11,11,.04)}
.status-used{color:var(--green);border-color:var(--green);background:rgba(43,125,79,.06)}
.card-section{
  font-family:var(--mono);font-size:9px;
  color:var(--orange);letter-spacing:.04em;
}
.card-section-unset{color:var(--gray);font-style:italic}
.card-title{
  font-family:var(--disp);font-weight:500;font-size:16px;line-height:1.2;
  color:var(--ink);margin-bottom:8px;letter-spacing:-.015em;
}
.card-meta{
  font-family:var(--narrow);font-size:10px;font-weight:500;letter-spacing:.12em;
  text-transform:uppercase;color:var(--muted);display:flex;gap:6px;align-items:center;
}
.card-dot{color:var(--hair-hard)}
.card-flag{
  margin-top:6px;font-family:var(--narrow);font-size:10px;font-weight:600;letter-spacing:.18em;
  text-transform:uppercase;color:var(--amber);
}
.card-foot{
  margin-top:8px;padding-top:8px;border-top:1px solid var(--hair-soft);
  display:flex;align-items:center;justify-content:space-between;gap:8px;
}
.card-file{font-family:var(--mono);font-size:10px;color:var(--gray)}
.card-grade-toggle{
  font-family:var(--narrow);font-size:9px;font-weight:600;letter-spacing:.18em;
  text-transform:uppercase;color:var(--muted);
  background:transparent;border:1px solid var(--hair);
  padding:3px 8px;cursor:pointer;
  transition:border-color .12s,color .12s;
}
.card-grade-toggle:hover{border-color:var(--ink);color:var(--ink)}
.card-grade-toggle[aria-expanded="true"]{color:var(--ink);border-color:var(--ink);background:var(--paper-shadow)}

/* ── Grade badge ─────────────────────────────────────── */
.grade-badge{
  font-family:var(--disp);
  font-weight:700;font-size:14px;line-height:1;letter-spacing:-.02em;
  padding:4px 8px;border:1px solid;display:inline-flex;align-items:baseline;gap:5px;
  min-width:38px;justify-content:center;
  cursor:help;
}
.grade-badge .grade-num{font-family:var(--mono);font-size:9px;font-weight:500;letter-spacing:0;color:inherit;opacity:.7}
.grade-a{color:var(--green);border-color:var(--green);background:rgba(43,125,79,.08)}
.grade-b{color:var(--ink);border-color:var(--ink);background:rgba(11,11,11,.04)}
.grade-c{color:var(--amber);border-color:var(--amber);background:rgba(184,117,23,.08)}
.grade-d{color:var(--red);border-color:var(--red);background:rgba(184,54,30,.08)}
.grade-f{color:#fff;border-color:var(--red);background:var(--red)}
.grade-override{color:var(--orange);border-color:var(--orange);background:rgba(255,107,53,.08);font-family:var(--narrow);font-size:10px;font-weight:700;letter-spacing:.2em}

/* ── Grade panel ─────────────────────────────────────── */
.grade-panel{
  margin-top:10px;padding:12px;
  background:var(--paper-alt);
  border:1px solid var(--hair);
  border-left:3px solid var(--ink);
}
.grade-panel[hidden]{display:none}
.grade-panel-head{
  display:flex;align-items:baseline;gap:10px;
  padding-bottom:8px;margin-bottom:10px;border-bottom:1px solid var(--hair);
}
.grade-panel-total{
  font-family:var(--disp);font-weight:700;font-size:22px;line-height:1;letter-spacing:-.02em;color:var(--ink);
}
.grade-panel-total small{font-family:var(--mono);font-size:11px;font-weight:500;color:var(--gray);margin-left:2px;letter-spacing:0}
.grade-panel-status{
  font-family:var(--narrow);font-size:10px;font-weight:700;letter-spacing:.22em;
  text-transform:uppercase;color:var(--muted);
}
.grade-dims{list-style:none;display:flex;flex-direction:column;gap:8px}
.grade-dim{padding:8px 10px;background:var(--paper);border:1px solid var(--hair-soft)}
.grade-dim-head{
  display:flex;align-items:center;gap:10px;margin-bottom:4px;
}
.grade-dim-letter{
  font-family:var(--disp);font-weight:700;font-size:12px;line-height:1;
  width:22px;height:22px;display:flex;align-items:center;justify-content:center;
  border:1px solid;flex:0 0 auto;
}
.grade-dim-label{
  font-family:var(--narrow);font-size:10px;font-weight:700;letter-spacing:.2em;
  text-transform:uppercase;color:var(--ink);flex:1;
}
.grade-dim-score{
  font-family:var(--mono);font-size:10px;font-weight:500;color:var(--muted);
}
.grade-dim-note{
  font-family:var(--sans);font-size:12px;line-height:1.45;color:var(--body);
  padding-left:32px;
}
.grade-panel-foot{
  margin-top:10px;padding-top:8px;border-top:1px solid var(--hair);
  font-family:var(--narrow);font-size:9px;font-weight:500;letter-spacing:.18em;
  text-transform:uppercase;color:var(--gray);
}
.grade-panel-foot code{font-family:var(--mono);font-size:10px;letter-spacing:0;color:var(--ink);background:var(--paper-shadow);padding:1px 5px;border:1px solid var(--hair)}
.grade-override-reason{
  font-family:var(--disp);font-style:italic;font-size:13px;line-height:1.4;color:var(--muted);
}

/* ── Canvas ─────────────────────────────────────── */
.canvas{padding:28px 32px 64px}
.canvas-head{margin-bottom:8px;padding-bottom:16px;border-bottom:1px solid var(--hair)}
.canvas-sub{
  font-family:var(--narrow);font-size:11px;font-weight:500;letter-spacing:.18em;
  text-transform:uppercase;color:var(--muted);margin-top:6px;
}
.canvas-stack{display:flex;flex-direction:column;gap:40px;margin-top:24px}
.canvas-group{display:flex;flex-direction:column;gap:16px}
.group-label{
  font-family:var(--narrow);
  font-size:10px;font-weight:700;letter-spacing:.28em;
  text-transform:uppercase;color:var(--muted);
  padding-bottom:8px;border-bottom:1px dashed var(--hair-hard);
}

/* ── Slot ─────────────────────────────────────── */
.slot{
  background:var(--paper);
  border:1px solid var(--hair-hard);
  padding:20px 22px;
  transition:border-color .12s,background .12s;
  position:relative;
}
.slot.slot-filled{border-left:4px solid var(--green);padding-left:18px}
.slot.slot-gap{border-left:4px solid var(--red);padding-left:18px}
.slot.slot-empty{border-left:4px solid var(--hair-hard);padding-left:18px;opacity:.75}
.slot.drop-target{border-color:var(--orange);background:rgba(255,107,53,.04)}
.slot-head{
  display:flex;align-items:flex-start;justify-content:space-between;gap:20px;
  margin-bottom:14px;flex-wrap:wrap;
}
.slot-head-left{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.slot-status-dot{width:8px;height:8px;border-radius:50%;background:var(--hair-hard)}
.slot-filled .slot-status-dot{background:var(--green)}
.slot-gap .slot-status-dot{background:var(--red)}
.slot-title{
  font-family:var(--disp);font-weight:500;font-size:26px;line-height:1;letter-spacing:-.02em;
  color:var(--ink);
}
.slot-required,.slot-optional{
  font-family:var(--narrow);font-size:9px;font-weight:700;letter-spacing:.22em;
  text-transform:uppercase;padding:3px 8px;border:1px solid;
}
.slot-required{color:var(--ink);border-color:var(--ink)}
.slot-optional{color:var(--gray);border-color:var(--gray)}
.slot-badge{
  font-family:var(--mono);font-size:11px;font-weight:500;
  padding:2px 8px;background:var(--paper-shadow);border:1px solid var(--hair);
  color:var(--ink);
}
.slot-desc{
  font-family:var(--disp);font-style:italic;font-size:13px;
  color:var(--muted);margin-bottom:14px;
}
.slot-body{display:flex;flex-direction:column;gap:8px;min-height:40px}
.slot-dropzone{
  font-family:var(--narrow);font-size:10px;font-weight:500;letter-spacing:.2em;
  text-transform:uppercase;color:var(--gray);
  padding:18px;text-align:center;border:1px dashed var(--hair-hard);
  background:var(--paper-alt);
}
.slot-gap-note{
  margin-top:10px;font-family:var(--narrow);font-size:11px;font-weight:500;letter-spacing:.1em;
  text-transform:uppercase;color:var(--red);
  padding:8px 12px;background:rgba(184,54,30,.05);border:1px solid rgba(184,54,30,.18);
}

/* ── Slot budget bar ─────────────────────────────────────── */
.slot-budget{min-width:200px;max-width:260px;flex:0 0 auto}
.slot-budget-none{
  font-family:var(--narrow);font-size:10px;font-weight:500;letter-spacing:.2em;
  text-transform:uppercase;color:var(--gray);font-style:italic;
}
.budget-meta{
  display:flex;justify-content:space-between;align-items:baseline;
  font-family:var(--narrow);font-size:10px;font-weight:500;letter-spacing:.14em;
  text-transform:uppercase;margin-bottom:4px;
}
.budget-current{color:var(--ink);font-weight:700}
.budget-target{color:var(--muted)}
.budget-bar{
  height:4px;background:var(--paper-shadow);border:1px solid var(--hair);position:relative;
}
.budget-fill{height:100%;transition:width .3s}
.budget-in-range{background:var(--green)}
.budget-under{background:var(--amber)}
.budget-over{background:var(--red)}
.budget-zone{
  position:absolute;top:-2px;bottom:-2px;
  border-left:1px solid var(--hair-hard);border-right:1px solid var(--hair-hard);
  pointer-events:none;
}

/* ── Slot article (placed) ─────────────────────────────────────── */
.slot-article{
  background:var(--paper-alt);
  border:1px solid var(--hair);
  padding:10px 14px;
  display:flex;align-items:center;justify-content:space-between;gap:16px;
}
.slot-article-left{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.slot-article-title{
  font-family:var(--disp);font-weight:500;font-size:14px;line-height:1.3;
  color:var(--ink);
}
.slot-article-file{
  font-family:var(--mono);font-size:10px;color:var(--muted);
}

/* ── Footer ─────────────────────────────────────── */
.page-foot{
  border-top:1px solid var(--hair);
  padding:16px 28px;
  display:flex;align-items:center;justify-content:space-between;gap:16px;
  font-family:var(--narrow);font-size:10px;font-weight:500;letter-spacing:.2em;
  text-transform:uppercase;color:var(--muted);
  background:var(--paper);
  flex-wrap:wrap;
}
.foot-left,.foot-right{display:flex;align-items:center;gap:12px}
.page-foot code{font-family:var(--mono);font-size:10px;letter-spacing:0;color:var(--ink);background:var(--paper-shadow);padding:1px 6px;border:1px solid var(--hair)}

/* ── View toggle ─────────────────────────────────────── */
.view-toggle{
  display:inline-flex;border:1px solid var(--hair-hard);background:var(--paper);
}
.view-toggle-btn{
  font-family:var(--narrow);font-size:10px;font-weight:700;letter-spacing:.22em;
  text-transform:uppercase;color:var(--muted);
  background:transparent;border:none;padding:6px 12px;cursor:pointer;
  transition:background .12s,color .12s;
}
.view-toggle-btn:hover{color:var(--ink)}
.view-toggle-btn.active{background:var(--ink);color:var(--paper)}

/* ── Magazine mockup ─────────────────────────────────────── */
.magazine-mockup{
  max-width:1200px;margin:0 auto;padding:48px 32px 96px;
  background:var(--paper);
  min-height:calc(100vh - 200px);
}
body[data-view="mockup"] .stage{display:none}
body[data-view="mockup"] .magazine-mockup{display:block}
body[data-view="table"] .magazine-mockup{display:none}

.mockup-cover{
  border-top:2px solid var(--ink);
  border-bottom:1px solid var(--ink);
  padding:48px 0 64px;margin-bottom:48px;
  position:relative;
}
.mockup-cover-top{
  display:flex;justify-content:space-between;align-items:baseline;
  font-family:var(--narrow);font-size:10px;font-weight:600;letter-spacing:.32em;
  text-transform:uppercase;color:var(--muted);margin-bottom:32px;
}
.mockup-cover-kicker b{color:var(--orange);font-weight:700}
.mockup-cover-title{
  font-family:var(--disp);
  font-weight:500;
  font-size:clamp(48px,7vw,96px);
  line-height:.96;letter-spacing:-.045em;
  color:var(--ink);margin-bottom:24px;
}
.mockup-cover-title em{font-style:italic;color:var(--gray);font-weight:400}
.mockup-cover-deck{
  font-family:var(--disp);font-style:italic;font-size:20px;
  color:var(--body);margin-bottom:24px;letter-spacing:-.015em;
}
.mockup-cover-deck em{font-style:normal;color:var(--orange);font-weight:500}
.mockup-cover-rule{height:2px;background:var(--ink);margin:32px 0 24px;max-width:120px}
.mockup-cover-foot{
  font-family:var(--disp);font-style:italic;font-size:14px;color:var(--muted);
}
.mockup-cover-foot .dot{color:var(--orange)}

.mockup-storyboard{
  display:grid;grid-template-columns:1fr 1fr;gap:48px;
}
@media (max-width:900px){ .mockup-storyboard{grid-template-columns:1fr} }
.mockup-toc-label{
  grid-column:1/-1;
  font-family:var(--narrow);font-size:10px;font-weight:700;letter-spacing:.32em;
  text-transform:uppercase;color:var(--muted);
  padding-bottom:12px;border-bottom:1px dashed var(--hair-hard);margin-bottom:8px;
}

.mockup-spread{
  padding:20px 24px;
  border:1px solid var(--hair-hard);
  background:var(--paper);
  position:relative;
}
.mockup-spread-lead{
  grid-column:1/-1;
  border:2px solid var(--ink);padding:32px 36px;
}
.mockup-spread-investigation{grid-column:1/-1}
.mockup-spread-empty{opacity:.55;border-style:dashed}

.mockup-meta{
  display:flex;align-items:center;gap:12px;margin-bottom:14px;flex-wrap:wrap;
}
.mockup-kicker{
  font-family:var(--narrow);font-size:10px;font-weight:700;letter-spacing:.32em;
  text-transform:uppercase;color:var(--orange);
}
.mockup-status{
  font-family:var(--narrow);font-size:9px;font-weight:700;letter-spacing:.2em;
  text-transform:uppercase;padding:2px 6px;border:1px solid;
}
.mockup-status-research{color:var(--amber);border-color:var(--amber);background:rgba(184,117,23,.06)}
.mockup-status-draft{color:var(--ink);border-color:var(--ink)}
.mockup-status-used{color:var(--green);border-color:var(--green);background:rgba(43,125,79,.06)}
.mockup-grade{
  font-family:var(--disp);font-weight:700;font-size:11px;line-height:1;
  padding:3px 7px;border:1px solid;min-width:20px;text-align:center;
}
.mockup-headline{
  font-family:var(--disp);font-weight:500;line-height:1.02;letter-spacing:-.025em;
  color:var(--ink);margin-bottom:12px;
  font-size:clamp(22px,3vw,34px);
}
.mockup-spread-lead .mockup-headline{font-size:clamp(34px,4.5vw,56px)}
.mockup-headline-empty{color:var(--gray);font-style:italic;font-weight:400}
.mockup-dek{
  font-family:var(--disp);font-style:italic;font-size:14px;line-height:1.4;
  color:var(--muted);margin-bottom:12px;
}
.mockup-spread-lead .mockup-dek{font-size:17px}
.mockup-support{
  font-family:var(--narrow);font-size:11px;font-weight:500;letter-spacing:.16em;
  text-transform:uppercase;color:var(--muted);margin-bottom:12px;
  padding:8px 10px;background:var(--paper-alt);border-left:2px solid var(--orange);
}
.mockup-footer{
  display:flex;align-items:center;justify-content:space-between;gap:16px;
  padding-top:10px;border-top:1px solid var(--hair);
  font-family:var(--narrow);font-size:9px;font-weight:500;letter-spacing:.16em;
  text-transform:uppercase;color:var(--gray);flex-wrap:wrap;
}
.mockup-file{font-family:var(--mono);font-size:10px;letter-spacing:0;color:var(--muted)}
.mockup-budget{font-weight:600}

.mockup-hero{
  position:relative;margin:0 -24px 20px;
  aspect-ratio:16/9;
  background:var(--paper-shadow);
  border-top:1px solid var(--hair);border-bottom:1px solid var(--hair);
  overflow:hidden;
}
.mockup-spread-lead .mockup-hero{margin:0 -36px 28px;aspect-ratio:21/9}
.mockup-hero img{width:100%;height:100%;object-fit:cover;display:block}

.mockup-image-btn{
  font-family:var(--narrow);font-size:10px;font-weight:700;letter-spacing:.22em;
  text-transform:uppercase;color:var(--muted);
  background:var(--paper-alt);border:1px dashed var(--hair-hard);
  padding:14px 18px;cursor:pointer;display:block;width:100%;
  transition:border-color .12s,color .12s,background .12s;
  margin-bottom:14px;
}
.mockup-image-btn:hover{color:var(--ink);border-color:var(--ink);background:var(--paper)}
.mockup-image-btn-change{
  position:absolute;bottom:8px;right:8px;
  width:auto;margin:0;background:rgba(11,11,11,.88);color:var(--paper);
  padding:6px 10px;border:1px solid var(--ink);font-size:9px;
  opacity:0;transition:opacity .12s;
}
.mockup-hero:hover .mockup-image-btn-change{opacity:1}

.mockup-notice{
  margin-top:48px;padding:16px 20px;
  background:var(--paper-alt);border:1px dashed var(--hair-hard);
  font-family:var(--disp);font-style:italic;font-size:13px;color:var(--muted);
  text-align:center;
}

/* ── Toast ─────────────────────────────────────── */
.toast{
  position:fixed;bottom:24px;right:24px;z-index:200;
  background:var(--ink);color:var(--paper);
  padding:12px 18px;min-width:260px;max-width:360px;
  font-family:var(--narrow);font-size:11px;font-weight:500;letter-spacing:.14em;
  text-transform:uppercase;
  border-left:3px solid var(--orange);
  transform:translateY(10px);opacity:0;
  transition:transform .2s,opacity .2s;
}
.toast.show{transform:translateY(0);opacity:1}
.toast.toast-error{border-left-color:var(--red)}
.toast.toast-success{border-left-color:var(--green)}
.toast b{color:var(--orange);font-weight:700;letter-spacing:0}
`;

// ────────────────────────────────────────────────────────────────────
// JS — visual-only drag-drop for v0.1 (safe DOM methods, no innerHTML)
// ────────────────────────────────────────────────────────────────────

const JS = `
(function(){
  const cards = document.querySelectorAll('.article-card');
  const slots = document.querySelectorAll('.slot');
  let draggedCard = null;

  // View toggle (Table ↔ Mockup)
  const viewButtons = document.querySelectorAll('.view-toggle-btn');
  viewButtons.forEach(function(btn){
    btn.addEventListener('click', function(){
      const nextView = btn.dataset.view;
      if (!nextView) return;
      document.body.dataset.view = nextView;
      viewButtons.forEach(function(b){
        const isActive = b.dataset.view === nextView;
        b.classList.toggle('active', isActive);
        b.setAttribute('aria-selected', isActive ? 'true' : 'false');
      });
      // Persist preference per-session
      try { sessionStorage.setItem('shipped.view', nextView); } catch(e){}
    });
  });
  // Restore persisted view
  try {
    const saved = sessionStorage.getItem('shipped.view');
    if (saved === 'mockup') {
      const btn = document.querySelector('.view-toggle-btn[data-view="mockup"]');
      if (btn) btn.click();
    }
  } catch(e){}

  // Grade-panel toggle
  document.querySelectorAll('.card-grade-toggle').forEach(function(btn){
    btn.setAttribute('aria-expanded', 'false');
    btn.addEventListener('click', function(e){
      e.stopPropagation();
      const targetId = btn.dataset.target;
      const panel = document.getElementById(targetId);
      if (!panel) return;
      const isOpen = !panel.hasAttribute('hidden');
      if (isOpen) {
        panel.setAttribute('hidden', '');
        btn.setAttribute('aria-expanded', 'false');
        btn.textContent = 'notes ▾';
      } else {
        panel.removeAttribute('hidden');
        btn.setAttribute('aria-expanded', 'true');
        btn.textContent = 'notes ▴';
      }
    });
  });

  function createEl(tag, className, text){
    const el = document.createElement(tag);
    if (className) el.className = className;
    if (text !== undefined) el.textContent = text;
    return el;
  }

  cards.forEach(function(card){
    card.addEventListener('dragstart', function(e){
      draggedCard = card;
      card.classList.add('dragging');
      e.dataTransfer.effectAllowed = 'move';
      e.dataTransfer.setData('text/plain', card.dataset.filename);
    });
    card.addEventListener('dragend', function(){
      card.classList.remove('dragging');
      draggedCard = null;
      document.querySelectorAll('.drop-target').forEach(function(s){ s.classList.remove('drop-target'); });
    });
  });

  slots.forEach(function(slot){
    slot.addEventListener('dragover', function(e){
      e.preventDefault();
      e.dataTransfer.dropEffect = 'move';
      slot.classList.add('drop-target');
    });
    slot.addEventListener('dragleave', function(e){
      if (!slot.contains(e.relatedTarget)) slot.classList.remove('drop-target');
    });
    slot.addEventListener('drop', function(e){
      e.preventDefault();
      slot.classList.remove('drop-target');
      if (!draggedCard) return;
      const targetSection = slot.dataset.section;
      const filename = draggedCard.dataset.filename;
      const currentSection = draggedCard.dataset.section;
      const status = draggedCard.dataset.status;
      const wordCount = draggedCard.dataset.wordcount;
      const titleText = draggedCard.querySelector('.card-title').textContent;

      // Optimistic UI update
      const body = slot.querySelector('.slot-body');
      if (body) {
        const dropzone = body.querySelector('.slot-dropzone');
        if (dropzone) dropzone.remove();

        const wrap = createEl('div', 'slot-article');
        wrap.dataset.filename = filename;

        const left = createEl('div', 'slot-article-left');
        const statusSpan = createEl('span', 'card-status status-' + status, status);
        const titleH4 = createEl('h4', 'slot-article-title', titleText);
        const liveSuffix = window.__SHIPPED_LIVE__ ? ' · saving…' : ' · moved (visual only — not persisted)';
        const fileDiv = createEl('div', 'slot-article-file', filename + ' · ' + wordCount + 'w' + liveSuffix);
        left.appendChild(statusSpan);
        left.appendChild(titleH4);
        left.appendChild(fileDiv);

        wrap.appendChild(left);
        body.appendChild(wrap);
      }

      draggedCard.dataset.section = targetSection;
      const secEl = draggedCard.querySelector('.card-section');
      if (secEl) {
        secEl.textContent = targetSection;
        secEl.classList.remove('card-section-unset');
      }

      if (window.__SHIPPED_LIVE__) {
        fetch('/api/move', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ filename: filename, section: targetSection }),
        })
        .then(function(r){ return r.json(); })
        .then(function(data){
          if (data.ok) {
            showToast('success', filename + ' → ' + targetSection, 'saved');
            // Update the slot's file line to reflect saved state
            const fileLine = body ? body.querySelector('.slot-article[data-filename="' + filename + '"] .slot-article-file') : null;
            if (fileLine) fileLine.textContent = filename + ' · ' + wordCount + 'w · saved';
            // Reload after short delay to pick up fresh grade
            setTimeout(function(){ window.location.reload(); }, 900);
          } else {
            showToast('error', 'move failed', data.error || 'unknown error');
          }
        })
        .catch(function(err){
          showToast('error', 'move failed', String(err));
        });
      } else {
        console.log('[dashboard] moved', filename, 'from', currentSection, '→', targetSection, '(visual only — run pnpm dashboard-dev to persist)');
      }
    });
  });

  // Hero-image add/change handlers (mockup view)
  document.querySelectorAll('.mockup-image-btn').forEach(function(btn){
    btn.addEventListener('click', function(){
      if (!window.__SHIPPED_LIVE__) {
        showToast('error', 'image placement', 'run pnpm dashboard-dev to persist');
        return;
      }
      const filename = btn.dataset.filename;
      const current = btn.dataset.current || '';
      const url = window.prompt('Hero image URL (http(s)://, data:image/..., or assets/...):', current);
      if (url === null) return;
      const trimmed = url.trim();
      if (!trimmed) return;
      fetch('/api/image', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filename: filename, imageUrl: trimmed }),
      })
      .then(function(r){ return r.json(); })
      .then(function(data){
        if (data.ok) {
          showToast('success', filename, 'image set');
          setTimeout(function(){ window.location.reload(); }, 700);
        } else {
          showToast('error', 'image failed', data.error || 'unknown error');
        }
      })
      .catch(function(err){ showToast('error', 'image failed', String(err)); });
    });
  });

  function showToast(kind, title, detail){
    const t = document.getElementById('dashboard-toast');
    if (!t) return;
    t.className = 'toast toast-' + kind;
    t.removeAttribute('hidden');
    while (t.firstChild) t.removeChild(t.firstChild);
    const b = createEl('b', null, title);
    const sp = createEl('span', null, ' · ' + (detail || ''));
    t.appendChild(b);
    t.appendChild(sp);
    requestAnimationFrame(function(){ t.classList.add('show'); });
    setTimeout(function(){
      t.classList.remove('show');
      setTimeout(function(){ t.setAttribute('hidden',''); }, 300);
    }, 2400);
  }
})();
`;
