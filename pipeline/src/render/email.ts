/**
 * Email renderer — issue markdown → email-safe HTML.
 *
 * The web template (template.html) cannot survive email clients: Gmail clips
 * messages over ~102KB, Outlook renders with Word's engine, web fonts and
 * JavaScript are stripped. This renderer produces a second artifact from the
 * same markdown — email.html next to index.html in the deploy tree — built
 * for that environment:
 *
 *   - single centered 640px table, every style inline
 *   - font stacks that degrade: Fraunces → Georgia, Archivo → Helvetica/Arial
 *   - front-of-book prose in full; Release Log compacted to date · tag ·
 *     linked title + first sentence (full log lives on the web page)
 *   - charts and figures skipped ("view on the web" covers them)
 *   - "View in browser" up top, reply-to-unsubscribe in the footer
 *
 * Markdown stays the source of truth: this is a function of (md), never
 * hand-edited HTML.
 */

import * as fs from 'node:fs/promises';
import * as path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseIssue } from './parse.js';
import { esc, inlineMarkdown, fmtPrettyDate, pad2 } from './markdown.js';
import type { ParsedIssue, ReleaseLogCategory, Section } from './types.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Design tokens — mirror template.html; email cannot use CSS variables.
const PAPER = '#FAF8F4';
const PAPER_SHADOW = '#f2f0e8';
const INK = '#0b0b0b';
const ORANGE = '#FF6B35';
const FAINT = '#6b6b6b';
const SERIF = "Fraunces, Georgia, 'Times New Roman', serif";
const SANS = "Archivo, 'Helvetica Neue', Helvetica, Arial, sans-serif";

const SITE_ROOT = 'https://id8labs.app/shipped';

/** Gmail clips above ~102KB; warn well before that. */
const SIZE_WARN_BYTES = 95 * 1024;

export interface EmailRenderOptions {
  outputPath?: string;
  deployRoot?: string;
  dryRun?: boolean;
  scratchPath?: string;
}

export interface EmailRenderResult {
  outputPath: string;
  bytes: number;
  subject: string;
  clippingRisk: boolean;
  /** When dryRun is true, this is where the scratch copy went. */
  scratchPath?: string;
}

// ── inline-styled building blocks ────────────────────────────────────────────

/** Give every anchor an inline style — email clients ignore <style> rules. */
function styleLinks(html: string): string {
  return html.replace(/<a href=/g, `<a style="color:${ORANGE};text-decoration:underline;" href=`);
}

function p(html: string, extra = ''): string {
  return `<p style="margin:0 0 16px;font-family:${SANS};font-size:16px;line-height:1.65;color:${INK};${extra}">${html}</p>`;
}

/**
 * Frontmatter strings (deck, by-the-numbers head) may carry literal <em>
 * markup meaning "orange accent". Escape everything else, honor that.
 */
function accented(raw: string): string {
  const escaped = esc(raw)
    .replace(/&lt;em&gt;/g, `<em style="font-style:normal;color:${ORANGE};">`)
    .replace(/&lt;\/em&gt;/g, '</em>');
  return escaped;
}

/**
 * Prose blocks → email HTML. Handles the grammar the front-of-book uses:
 * paragraphs, ### subheads, - bullets, > quotes. Chart/figure blockquotes
 * (`> ###` data blocks) are dropped — the web page carries them.
 */
function emailProse(body: string): string {
  const blocks = body
    .replace(/\r\n/g, '\n')
    .split(/\n{2,}/)
    .map((b) => b.trim())
    .filter((b) => b.length > 0 && !/^-{3,}$/.test(b));

  const out: string[] = [];
  for (const block of blocks) {
    if (block.startsWith('>')) {
      // Chart/figure data blocks are `> ###`-headed; skip them.
      if (/^>\s*###/.test(block)) continue;
      const quote = block
        .split('\n')
        .map((l) => l.replace(/^>\s?/, '').trim())
        .filter(Boolean)
        .join(' ');
      out.push(
        `<blockquote style="margin:0 0 16px;padding:12px 20px;border-left:3px solid ${ORANGE};background:${PAPER_SHADOW};font-family:${SERIF};font-size:16px;line-height:1.6;color:${INK};">${inlineMarkdown(quote)}</blockquote>`
      );
      continue;
    }
    if (block.startsWith('### ')) {
      const lines = block.split('\n');
      out.push(
        `<h3 style="margin:28px 0 12px;font-family:${SERIF};font-size:20px;line-height:1.3;color:${INK};">${inlineMarkdown(lines[0]!.slice(4))}</h3>`
      );
      const rest = lines.slice(1).join('\n').trim();
      if (rest) out.push(emailProse(rest));
      continue;
    }
    if (/^[-*] /m.test(block) && block.split('\n').every((l) => /^[-*] /.test(l.trim()))) {
      const items = block
        .split('\n')
        .map((l) => l.trim().replace(/^[-*] /, ''))
        .map((l) => `<li style="margin:0 0 8px;">${inlineMarkdown(l)}</li>`)
        .join('');
      out.push(
        `<ul style="margin:0 0 16px;padding-left:24px;font-family:${SANS};font-size:16px;line-height:1.65;color:${INK};">${items}</ul>`
      );
      continue;
    }
    out.push(p(inlineMarkdown(block.replace(/\n/g, ' '))));
  }
  return out.join('\n');
}

/** Section H2 header. */
function sectionHead(name: string): string {
  return `<h2 style="margin:40px 0 16px;font-family:${SERIF};font-size:26px;line-height:1.2;color:${INK};border-top:2px solid ${INK};padding-top:24px;">${inlineMarkdown(name)}</h2>`;
}

/** First sentence of a markdown summary, for the compact Release Log. */
function firstSentence(text: string): string {
  const flat = text.replace(/\s+/g, ' ').trim();
  const m = flat.match(/^.*?[.!?](?=\s|$)/);
  return m ? m[0] : flat;
}

function renderByTheNumbers(issue: ParsedIssue): string {
  const btn = issue.frontmatter.by_the_numbers;
  if (!btn?.cells?.length) return '';
  const cells = btn.cells
    .map(
      (c) =>
        `<tr>
          <td style="padding:10px 16px;border-bottom:1px solid ${PAPER_SHADOW};font-family:${SERIF};font-size:22px;color:${c.accent ? ORANGE : INK};white-space:nowrap;">${esc(String(c.value))}</td>
          <td style="padding:10px 16px;border-bottom:1px solid ${PAPER_SHADOW};font-family:${SANS};font-size:13px;line-height:1.4;color:${FAINT};">${esc(String(c.label))}${c.note ? `<br><span style="font-size:12px;">${esc(String(c.note))}</span>` : ''}</td>
        </tr>`
    )
    .join('');
  return (
    sectionHead(btn.head ? accented(btn.head) : 'By the numbers.') +
    (btn.deck ? p(accented(btn.deck), `color:${FAINT};font-style:italic;`) : '') +
    `<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:0 0 16px;">${cells}</table>`
  );
}

function renderReleaseLogCompact(categories: ReleaseLogCategory[], issueNum: string): string {
  if (!categories.length) return '';
  const parts: string[] = [
    sectionHead('Release Log'),
    p(
      `The complete log, with usage notes and code, is in the <a href="${SITE_ROOT}/${issueNum}/">web edition</a>.`,
      `color:${FAINT};font-size:14px;`
    ),
  ];
  for (const cat of categories) {
    parts.push(
      `<h3 style="margin:24px 0 10px;font-family:${SANS};font-size:13px;letter-spacing:0.12em;text-transform:uppercase;color:${INK};">${esc(cat.letter)}. ${esc(cat.name)}${cat.subLabel ? ` <span style="color:${FAINT};text-transform:none;letter-spacing:0;">${esc(cat.subLabel)}</span>` : ''}</h3>`
    );
    for (const entry of cat.entries) {
      const title = entry.url
        ? `<a href="${entry.url.replace(/"/g, '%22')}">${esc(entry.title)}</a>`
        : `<strong>${esc(entry.title)}</strong>`;
      parts.push(
        `<p style="margin:0 0 12px;font-family:${SANS};font-size:14px;line-height:1.55;color:${INK};">` +
          `<span style="color:${FAINT};">${esc(entry.date)}</span> · ` +
          `<span style="color:${ORANGE};font-weight:600;">${esc(entry.category)}</span> · ` +
          `${title}<br>${inlineMarkdown(firstSentence(entry.summary))}</p>`
      );
    }
  }
  return parts.join('\n');
}

// Front-of-book section kinds rendered as prose, in document order.
const PROSE_KINDS = new Set([
  'open',
  'lead_story',
  'companion_lead',
  'feature',
  'investigation',
  'also_shipped',
  'timeline',
  'survey',
  'cowork',
  'papers',
  'term_of_issue',
  'quiet_on_wire',
  'close',
]);

function renderFrontOfBook(issue: ParsedIssue): string {
  const parts: string[] = [];
  for (const section of issue.sections) {
    if (section.kind === 'by_the_numbers') {
      parts.push(renderByTheNumbers(issue));
      continue;
    }
    if (!PROSE_KINDS.has(section.kind)) continue;
    parts.push(sectionHead(section.name));
    parts.push(emailProse(section.content));
  }
  return parts.join('\n');
}

// ── document assembly ────────────────────────────────────────────────────────

export function buildEmailHtml(issue: ParsedIssue): { html: string; subject: string } {
  const fm = issue.frontmatter;
  const issueNum = pad2(fm.issue);
  const webUrl = `${SITE_ROOT}/${issueNum}/`;
  const prettyDate = fmtPrettyDate(fm.date);
  const subject = `Shipped. ${issueNum} — ${fm.title}`;
  const deck = fm.deck ?? '';

  const html = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<title>${esc(subject)}</title>
</head>
<body style="margin:0;padding:0;background:${PAPER};">
<!-- preheader: first line shown next to the subject in inboxes -->
<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;">${esc(deck)}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:${PAPER};">
<tr><td align="center" style="padding:24px 12px;">
<table role="presentation" width="640" cellpadding="0" cellspacing="0" style="max-width:640px;width:100%;">
<tr><td style="padding:0 12px;">

<p style="margin:0 0 20px;text-align:right;font-family:${SANS};font-size:12px;color:${FAINT};">
  <a style="color:${FAINT};text-decoration:underline;" href="${webUrl}">View in browser</a>
</p>

<h1 style="margin:0;font-family:${SERIF};font-size:52px;line-height:1;color:${INK};">Shipped<span style="color:${ORANGE};">.</span></h1>
<p style="margin:10px 0 0;font-family:${SANS};font-size:12px;letter-spacing:0.14em;text-transform:uppercase;color:${FAINT};">
  Issue ${esc(issueNum)} · ${esc(prettyDate)} · ${esc(fm.period)}
</p>
<h2 style="margin:24px 0 6px;font-family:${SERIF};font-size:32px;line-height:1.15;color:${INK};">${esc(fm.title)}</h2>
${deck ? `<p style="margin:0 0 8px;font-family:${SERIF};font-style:italic;font-size:18px;line-height:1.5;color:${FAINT};">${esc(deck)}</p>` : ''}
${fm.byline ? `<p style="margin:0 0 8px;font-family:${SANS};font-size:12px;color:${FAINT};">${esc(fm.byline)}</p>` : ''}

${styleLinks(renderFrontOfBook(issue))}

${styleLinks(renderReleaseLogCompact(issue.releaseLog, issueNum))}

<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:48px 0 0;">
<tr><td style="border-top:2px solid ${INK};padding:20px 0 40px;">
<p style="margin:0 0 8px;font-family:${SANS};font-size:12px;line-height:1.6;color:${FAINT};">
  Shipped. is published by id8Labs. Read every issue at
  <a style="color:${ORANGE};text-decoration:underline;" href="${SITE_ROOT}/">id8labs.app/shipped</a>.
</p>
<p style="margin:0;font-family:${SANS};font-size:12px;line-height:1.6;color:${FAINT};">
  You are on the Shipped. reading list. Reply to this email to be removed.
</p>
</td></tr>
</table>

</td></tr>
</table>
</td></tr>
</table>
</body>
</html>
`;

  return { html, subject };
}

export async function renderEmailIssue(
  markdownPath: string,
  options: EmailRenderOptions = {}
): Promise<EmailRenderResult> {
  const absPath = path.resolve(markdownPath);
  const markdown = await fs.readFile(absPath, 'utf-8');
  const issue = parseIssue(markdown, absPath);
  const issueNum = pad2(issue.frontmatter.issue);

  const { html, subject } = buildEmailHtml(issue);
  const bytes = Buffer.byteLength(html, 'utf-8');
  const clippingRisk = bytes > SIZE_WARN_BYTES;

  const deployRoot =
    options.deployRoot ??
    process.env.SHIPPED_DEPLOY_PATH ??
    path.resolve(__dirname, '..', '..', '..', '..', 'id8labs', 'public', 'shipped');
  const outputPath = options.outputPath ?? path.join(deployRoot, issueNum, 'email.html');

  const scratchPath =
    options.scratchPath ?? path.join('/tmp', `shipped-email-${issueNum}.html`);
  await fs.writeFile(scratchPath, html, 'utf-8');

  if (!options.dryRun) {
    await fs.mkdir(path.dirname(outputPath), { recursive: true });
    await fs.writeFile(outputPath, html, 'utf-8');
  }

  return { outputPath, bytes, subject, clippingRisk, scratchPath };
}
