/**
 * "The Close" — three-beat closer on dark background.
 *
 * Each non-empty paragraph in the markdown becomes a `.close-line`.
 * The last paragraph gets `.close-final` (italic orange).
 */

import type { Section } from '../types.js';
import { inlineMarkdown } from '../markdown.js';

export function renderClose(section: Section): string {
  const rawBlocks = section.content
    .split(/\n{2,}/)
    .map((b) => b.trim())
    .filter((b) => b.length > 0);

  // A `---` divider in the close marks "everything below here is coda."
  // Coda paragraphs render as italic-orange voiceover (.close-final).
  // Without a divider, only the last paragraph becomes coda (legacy behavior).
  const blocks: Array<{ text: string; isCoda: boolean }> = [];
  let inCoda = false;
  for (const b of rawBlocks) {
    if (/^-{3,}$/.test(b)) {
      inCoda = true;
      continue;
    }
    blocks.push({ text: b, isCoda: inCoda });
  }

  const hasCodaDivider = blocks.some((b) => b.isCoda);

  const linesHtml = blocks
    .map((b, i) => {
      const isLast = i === blocks.length - 1;
      const isCoda = b.isCoda || (!hasCodaDivider && isLast);
      const isFirstCoda = isCoda && (b.isCoda ? !blocks[i - 1]?.isCoda : true);
      const cls = isCoda
        ? 'close-line close-final' + (isFirstCoda ? ' close-coda-start' : '')
        : 'close-line';
      return `    <p class="${cls}">${inlineMarkdown(b.text)}</p>`;
    })
    .join('\n');

  return `<section class="close-section">
  <div class="close-kicker">The Close</div>
  <div class="close-stack">
${linesHtml}
  </div>
  <div class="close-mark">&#10022;</div>
</section>`;
}
