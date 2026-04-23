/**
 * "Also shipped" — combines the "Cowork shipped, finally" and
 * "Two papers worth your Friday" sections into one editorial block.
 *
 * Each section's H1 is rendered as an italic display heading inside the
 * prose-well; paragraphs follow.
 */

import type { Section } from '../types.js';
import { inlineMarkdown } from '../markdown.js';

export function renderAlsoShipped(
  alsoShipped: Section | undefined,
  cowork: Section | undefined,
  papers: Section | undefined,
): string {
  // Modern path: a single "Also Shipped" section from the markdown (Issue 02+).
  // H3 subsections become italic display headings; each subsection's body
  // becomes paragraphs underneath.
  if (alsoShipped) {
    return `<section class="section" id="also">
  <div class="section-folio">
    <div class="section-folio-left">
      <span class="folio">Shipped. <span class="dot">·</span> Also shipped</span>
    </div>
    <span class="section-folio-sub">Also shipped</span>
  </div>

  <div class="prose-well" style="padding:0">
    <div class="prose">
${renderBodyWithSubheadings(alsoShipped.content)}
    </div>
  </div>
</section>`;
  }

  // Legacy Issue 00 path (cowork + papers split into two sections).
  const coworkHtml = cowork ? renderInner(cowork) : '';
  const papersHtml = papers ? renderInner(papers, /*isFirst*/ false) : '';
  if (!coworkHtml && !papersHtml) return '';

  return `<section class="section" id="also">
  <div class="section-folio">
    <div class="section-folio-left">
      <span class="folio">Shipped. <span class="dot">·</span> Also shipped</span>
    </div>
    <span class="section-folio-sub">Also shipped</span>
  </div>

  <div class="prose-well" style="padding:0">
    <div class="prose">
${coworkHtml}
${papersHtml}
    </div>
  </div>
</section>`;
}

function renderBodyWithSubheadings(content: string): string {
  const lines = content.split('\n');
  const out: string[] = [];
  let buffer: string[] = [];
  const flushBuffer = () => {
    if (buffer.length > 0) {
      out.push(paragraphs(buffer.join('\n')));
      buffer = [];
    }
  };
  for (const line of lines) {
    if (line.startsWith('# ')) continue; // skip H1
    const h3 = line.match(/^###\s+(.+)$/);
    if (h3) {
      flushBuffer();
      out.push(
        `      <h3 style="font-family:var(--disp);font-weight:500;font-style:italic;font-size:30px;letter-spacing:-.02em;line-height:1.15;color:var(--ink);margin:32px 0 14px">${h3[1]}.</h3>`,
      );
      continue;
    }
    buffer.push(line);
  }
  flushBuffer();
  return out.join('\n');
}

function renderInner(section: Section, isFirst = true): string {
  const heading = section.name;
  const margin = isFirst ? '0 0 20px' : '48px 0 20px';
  const headingHtml = `      <h3 style="font-family:var(--disp);font-weight:500;font-style:italic;font-size:36px;letter-spacing:-.02em;line-height:1;color:var(--ink);margin:${margin}">${heading}.</h3>`;

  return [headingHtml, paragraphs(section.content)].join('\n');
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
        !b.startsWith('>'),
    );
  return blocks
    .map((b) => `      <p>${inlineMarkdown(b.replace(/\n/g, ' '))}</p>`)
    .join('\n');
}
