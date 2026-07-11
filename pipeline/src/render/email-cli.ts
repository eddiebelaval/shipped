/**
 * Email render CLI.
 *
 *   pnpm render:email path/to/issue-NN.md [--dry-run]
 *
 * Writes email.html next to the issue's index.html in the deploy tree
 * (id8labs/public/shipped/NN/email.html). The send side fetches it from
 * the public URL, so staging it is enough — nothing sends from here.
 */

import { renderEmailIssue } from './email.js';

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  const positional = args.filter((a) => !a.startsWith('--'));
  const flags = new Set(args.filter((a) => a.startsWith('--')));

  const markdownPath = positional[0];
  if (!markdownPath) {
    console.error('Usage: pnpm render:email <issue.md> [--dry-run]');
    process.exit(1);
  }

  const dryRun = flags.has('--dry-run');

  try {
    const result = await renderEmailIssue(markdownPath, { dryRun });
    console.log('');
    console.log('  Shipped. — email render complete');
    console.log('  ─────────────────────────────────');
    console.log(`  Source   : ${markdownPath}`);
    console.log(`  Output   : ${result.outputPath}${dryRun ? '  (dry-run, not written)' : ''}`);
    console.log(`  Scratch  : ${result.scratchPath}`);
    console.log(`  Subject  : ${result.subject}`);
    console.log(`  Size     : ${(result.bytes / 1024).toFixed(1)} KB${result.clippingRisk ? '  ⚠ over 95KB — Gmail clips near 102KB' : ''}`);
    console.log('');
    if (result.clippingRisk) process.exitCode = 0; // warn, don't fail — the verifier owns gates
  } catch (err) {
    console.error('Email render failed:', err instanceof Error ? err.message : err);
    if (err instanceof Error && err.stack) console.error(err.stack);
    process.exit(1);
  }
}

void main();
