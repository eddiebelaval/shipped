/**
 * "Feature" — the Agent Stack story. Feature opener + 2 prose-wells +
 * embedded code block. The fenced code block in the markdown becomes a
 * `<div class="code-block">` with the magazine's terminal styling.
 */

import type { Section } from '../types.js';
import { inlineMarkdown, esc } from '../markdown.js';

export function renderFeature(section: Section): string {
  const headline = extractHeadline(section.content);

  // Split prose around the fenced code block.
  const { before, after, code } = splitOnCodeBlock(section.content);

  const beforeProse = paragraphs(before);
  const afterProse = paragraphs(after);
  const codeHtml = code ? renderCodeBlock(code) : '';

  const fullProse = paragraphs(stripCodeBlock(section.content));

  return `<div class="feature-opener" id="feature">
  <span class="vert-label">Feature</span>
  <div class="feature-heading">
    <div class="feature-kicker">Reporting by Eddie Belaval</div>
    <h2 class="feature-title">${formatTitle(headline)}</h2>
  </div>
</div>

<div class="prose-well">
  <div class="prose drop-cap">
${fullProse}
${codeHtml}
  </div>
</div>`;
}

function stripCodeBlock(content: string): string {
  const { before, after } = splitOnCodeBlock(content);
  return before + '\n\n' + after;
}

function extractHeadline(content: string): string {
  const lines = content.split('\n');
  for (const l of lines) {
    if (l.startsWith('# ')) return l.slice(2).trim();
  }
  return 'Feature';
}

function formatTitle(headline: string): string {
  // Italicize the last 2 words (e.g. "got serious")
  const words = headline.split(' ');
  if (words.length >= 3) {
    const i = words.length - 2;
    const last2 = words.slice(i).join(' ');
    return [...words.slice(0, i), `<em>${last2}.</em>`].join(' ');
  }
  return headline + '.';
}

function splitOnCodeBlock(content: string): {
  before: string;
  after: string;
  code: string | null;
} {
  const lines = content.split('\n');
  const fenceRe = /^```/;
  let openIdx = -1;
  let closeIdx = -1;
  for (let i = 0; i < lines.length; i++) {
    if (fenceRe.test(lines[i]!)) {
      if (openIdx < 0) openIdx = i;
      else {
        closeIdx = i;
        break;
      }
    }
  }
  if (openIdx < 0 || closeIdx < 0) {
    return { before: content, after: '', code: null };
  }
  const before = lines.slice(0, openIdx).join('\n');
  const code = lines.slice(openIdx + 1, closeIdx).join('\n');
  const after = lines.slice(closeIdx + 1).join('\n');
  return { before, after, code };
}

function renderCodeBlock(code: string): string {
  // Light Python-ish syntax coloring: strings, comments, keywords.
  const escaped = esc(code);
  const colored = escaped
    .replace(/(#.*?)(?=$|\n)/gm, '<span class="c">$1</span>')
    .replace(/(&quot;[^&]*?&quot;)/g, '<span class="s">$1</span>')
    .replace(/\b(while|not|for|in|if|else|return|def|class|with|as|import|from)\b/g, '<span class="k">$1</span>');

  return `<div class="code-block">
      <div class="code-block-head">
        <span>python &nbsp;·&nbsp; messages.create</span>
        <span>advisor-tool-2026-03-01</span>
      </div>
<pre>${colored}</pre>
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
        !b.startsWith('>'),
    );
  return blocks
    .map((b) => `    <p>${inlineMarkdown(b.replace(/\n/g, ' '))}</p>`)
    .join('\n');
}
