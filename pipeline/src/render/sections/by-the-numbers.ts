/**
 * "By the Numbers" — per-issue stat grid.
 *
 * Driven by the canonical frontmatter's `by_the_numbers` block. Each cell is
 * { label, value, note, size?, accent? }. size is 3, 4, or 6 (grid columns).
 * If the frontmatter block is absent, renders empty (section skipped).
 */

export interface BtnCell {
  label: string;
  value: string;
  note?: string;
  size?: 3 | 4 | 6;
  accent?: boolean;
}

export interface BtnData {
  head?: string;         // optional display heading
  deck?: string;         // optional italic deck
  cells?: BtnCell[];
}

export function renderByTheNumbers(data?: BtnData): string {
  if (!data || !Array.isArray(data.cells) || data.cells.length === 0) return '';

  const head = data.head ?? 'By <em>the</em> numbers.';
  const deck = data.deck ?? '';

  const cells = data.cells.map((c) => {
    const size = c.size ?? 3;
    const accentClass = c.accent ? ' accent' : '';
    const note = c.note ? `<span class="btn-note">${escapeHtml(c.note)}</span>` : '';
    return `    <div class="btn-cell s${size}">
      <span class="btn-label">${escapeHtml(c.label)}</span>
      <span class="btn-num${accentClass}">${c.value}</span>
      ${note}
    </div>`;
  }).join('\n');

  return `<section class="btn-section" id="numbers">
  <div class="section" style="padding-top:64px;padding-bottom:0">
    <div class="section-folio">
      <div class="section-folio-left">
        <span class="folio"><span class="ruler"></span>By the numbers</span>
      </div>
      <span class="section-folio-sub">By the numbers</span>
    </div>
    <h2 class="btn-head">${head}</h2>
    ${deck ? `<p class="btn-deck">${escapeHtml(deck)}</p>` : ''}
  </div>

  <div class="btn-grid">
${cells}
  </div>
</section>`;
}

function escapeHtml(s: string): string {
  return String(s).replace(/[&<>"']/g, (c) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
  }[c]!));
}
