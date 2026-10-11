/**
 * Edition render CLI: an edition's paper markdown -> a self-contained page for daily-pages.
 *
 *   tsx src/render/edition-cli.ts <edition.md> <out.html> [--approved-only]
 *
 * Always a dry run: it never touches the id8labs deploy folder, the archive, or the
 * manifest (renderIssue writes only the scratch path, and copies images beside it).
 * The magazine template is built for id8labs.app/shipped/NN, so the edition's
 * own URL and subscribe source are written over the magazine ones here.
 */

import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import matter from 'gray-matter';
import { renderIssue } from './index.js';

const ASSETS = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../assets');
const PAGES = 'https://eddiebelaval.github.io/shipped';
const SOURCE: Record<string, string> = {
  'anthropic-daily': 'shipped-daily',
  'anthropic-weekly': 'shipped-weekly',
  'anthropic-monthly': 'shipped-monthly',
};

/** Night Desk and the Edition Desk recognise an edition's paper front by this tag. */
export const PAPER_MARKER = '<meta name="shipped-layout" content="paper">';

const CADENCE: Record<string, { label: string; when: string }> = {
  'anthropic-daily': { label: 'Daily', when: 'every night at 9 PM ET' },
  'anthropic-weekly': { label: 'Weekly', when: 'every Friday' },
  'anthropic-monthly': { label: 'Monthly', when: 'on the first of the month' },
};

export interface EditionMeta { section: string; stem: string; issueNum: string; title: string; deck: string; period: string }

const attr = (s: string) => s.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;');

/**
 * Swap the magazine's identity for the edition's: URL, title and description
 * meta, OG card, subscribe source, pub-bar and colophon copy, next-issue lines.
 * The edition gate forbids em/en dashes, so the template's are rewritten too.
 */
export function editionize(html: string, m: EditionMeta): string {
  const source = SOURCE[m.section];
  const cad = CADENCE[m.section];
  if (!source || !cad) throw new Error(`unknown edition section: ${m.section}`);
  const url = `${PAGES}/${m.section}/${m.stem}.html`;
  const title = attr(m.title);
  const deck = attr(m.deck);
  return html
    .replaceAll(`https://id8labs.app/shipped/${m.issueNum}/`, url)
    .replace(/<meta (property="og:image"|name="twitter:image") content="[^"]*">\n?/g, '')
    .replaceAll(`shipped-magazine-issue-${m.issueNum}`, source)
    .replace(/<title>[^<]*<\/title>/, `<title>${title}</title>\n${PAPER_MARKER}`)
    .replace(/(<meta (?:property="og:title"|name="twitter:title") content=")[^"]*"/g, `$1${title}"`)
    .replace(/(<meta (?:property="og:description"|name="twitter:description"|name="description") content=")[^"]*"/g, `$1${deck}"`)
    .replace('A weekly magazine by <a', `${cad.label} edition by <a`)
    .replace(`Issue <b>${m.issueNum}</b>`, attr(m.period))
    .replaceAll(/Next issue, [A-Z][a-z]{2} \d{1,2}, \d{4}/g, `New ${cad.when}`)
    .replace(/A weekly magazine on what Anthropic is releasing\. Published every Friday at 9 AM ET, by/,
      `The ${cad.label.toLowerCase()} edition of Shipped., a frontier-labs publication. Published ${cad.when}, by`)
    .replaceAll(`<span class="dot">·</span> ${m.issueNum} <span class="dot">·</span>`, `<span class="dot">·</span> ${cad.label} <span class="dot">·</span>`)
    .replace(`<b>Issue</b> ${m.issueNum} (`, `<b>Edition</b> ${cad.label} (`)
    .replace(/src="\/brand\/([\w-]+\.svg)"/g, (whole, file: string) => {
      // github.io has no /brand/; the page must carry its own wordmarks.
      const f = path.join(ASSETS, file);
      if (!existsSync(f)) throw new Error(`edition page references /brand/${file}, missing from pipeline/assets`);
      return `src="data:image/svg+xml;base64,${readFileSync(f).toString('base64')}"`;
    })
    .replace(/ ?[\u2014\u2013] ?/g, ', ');
}

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  const flags = args.filter((a) => a.startsWith('--'));
  const [md, out] = args.filter((a) => !a.startsWith('--'));
  const unknown = flags.filter((f) => f !== '--approved-only');
  if (!md || !out || unknown.length) {
    console.error('Usage: tsx src/render/edition-cli.ts <edition.md> <out.html> [--approved-only]');
    process.exit(1);
  }
  const fm = matter(readFileSync(md, 'utf-8')).data as {
    issue: number; title: string; deck?: string; period?: string; edition_section?: string; edition_stem?: string;
  };
  if (!fm.edition_section || !fm.edition_stem) {
    console.error(`${md}: not an edition (edition_section / edition_stem missing)`);
    process.exit(1);
  }
  const r = await renderIssue(md, { dryRun: true, scratchPath: out, approvedImagesOnly: flags.includes('--approved-only') });
  writeFileSync(out, editionize(readFileSync(out, 'utf-8'), {
    section: fm.edition_section, stem: fm.edition_stem, issueNum: String(fm.issue).padStart(2, '0'),
    title: fm.title, deck: fm.deck ?? '', period: String(fm.period ?? fm.edition_stem),
  }));
  console.log(JSON.stringify({ out, words: r.wordCount, logEntries: r.releaseLogEntryCount }));
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch((e) => { console.error(e); process.exit(1); });
}
