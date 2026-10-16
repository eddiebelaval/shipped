/**
 * Inline markdown: code inside a link, and code escaped exactly once (archive editions 2026-08-21, 2026-05-29).
 */

import { test } from 'node:test';
import assert from 'node:assert/strict';
import { inlineMarkdown } from '../src/render/markdown.js';

test('code inside a link renders as code, not a placeholder', () => {
  const html = inlineMarkdown('[Update with `claude update`](https://code.claude.com/docs/en/changelog). Then restart.');
  assert.equal(html, '<a href="https://code.claude.com/docs/en/changelog">Update with <code>claude update</code></a>. Then restart.');
  assert.doesNotMatch(html, /\u0000/);
});

test('angle brackets in code are escaped once', () => {
  assert.equal(inlineMarkdown('`claude plugin init <name>`'), '<code>claude plugin init &lt;name&gt;</code>');
  assert.equal(inlineMarkdown('`a && b`'), '<code>a &amp;&amp; b</code>');
});
