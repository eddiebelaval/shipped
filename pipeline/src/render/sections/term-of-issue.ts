/**
 * "Term of the Issue" — dictionary-style entry.
 */

import type { Section, TermOfIssue } from '../types.js';
import { inlineMarkdown } from '../markdown.js';

export function renderTermOfIssue(section: Section): string {
  const data = (section.data as TermOfIssue | undefined) ?? {
    word: 'shadow release',
    pronunciation: 'SHA-doh ree-LEES',
    partOfSpeech: 'noun',
    definition: [],
  };

  const wordHtml = formatWord(data.word);
  const part = data.partOfSpeech ?? 'noun';
  const pron = data.pronunciation ?? '';
  const defHtml = (data.definition ?? [])
    .map((p) => `    <p>${inlineMarkdown(p)}</p>`)
    .join('\n');
  const firstObs = data.firstObservable
    ? `    <p><strong>First observable instance:</strong> ${inlineMarkdown(data.firstObservable)}</p>`
    : '';
  const usage = data.usage
    ? `    <div class="term-usage">
      <b>Usage</b>
      &ldquo;${stripQuotes(inlineMarkdown(data.usage))}&rdquo;
    </div>`
    : '';

  // Build the kicker line — pull dynamic bits from data; fall back to legacy
  // fixed copy only when nothing was provided (preserves Issue 01 behavior).
  const page = (data as TermOfIssue & { page?: string }).page ?? 'p.19';
  const firstObsKicker = data.firstObservable
    ? `First observable ${data.firstObservable}`
    : 'First observable 2026-04-16';
  const kicker = `Term of the Issue &nbsp;·&nbsp; ${page} &nbsp;·&nbsp; ${firstObsKicker}`;

  return `<section class="term-section" id="term">
  <div class="term-kicker">${kicker}</div>
  <div class="term-word">
    ${wordHtml}<span class="part">/<em>${formatPron(pron)}</em>/&nbsp;&nbsp;·&nbsp;&nbsp;${part}</span>
  </div>
  <div class="term-def">
${defHtml}
${firstObs}
${usage}
  </div>
</section>`;
}

function formatWord(word: string): string {
  // Two-word terms break across lines: "shadow<br>release"
  return word.split(' ').join('<br>');
}

function formatPron(pron: string): string {
  // Convert "SHA-doh ree-LEES" → "SHA</em>-doh&nbsp;&nbsp;ree-<em>LEES"
  // Keep it simple: replace double space with double nbsp
  return pron.replace(/\s+/g, '&nbsp;&nbsp;');
}

function stripQuotes(s: string): string {
  return s.replace(/^[“"]/, '').replace(/[”"]$/, '').trim();
}
