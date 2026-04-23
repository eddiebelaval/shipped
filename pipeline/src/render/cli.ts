/**
 * Render CLI.
 *
 *   pnpm render path/to/issue-NN.md [--dry-run]
 *   pnpm render --issue 02 [--dry-run]       # auto-assembles if canonical is missing
 *
 * Prints a render summary on stdout. Exits 0 on success, 1 on any error.
 */

import { existsSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { resolve, join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { renderIssue } from './index.js';

const __dirname = dirname(fileURLToPath(import.meta.url));

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  const positional = args.filter((a) => !a.startsWith('--'));
  const flags = new Set(args.filter((a) => a.startsWith('--')));

  // --issue NN mode: resolve to content/issue-NN-{slug}.md; auto-assemble if missing.
  let markdownPath = positional[0];
  const issueIdx = args.indexOf('--issue');
  if (issueIdx >= 0 && args[issueIdx + 1]) {
    const issueNum = args[issueIdx + 1]!.padStart(2, '0');
    const contentRoot = resolve(process.cwd(), '..', 'content');
    // Try to read the WIP slug to find the canonical path.
    const matter = (await import('gray-matter')).default;
    const wipPath = join(contentRoot, `issue-${issueNum}-wip.md`);
    if (!existsSync(wipPath)) {
      console.error(`WIP not found: ${wipPath}. Cannot resolve canonical path.`);
      process.exit(1);
    }
    const { readFileSync } = await import('node:fs');
    const wipFm = matter(readFileSync(wipPath, 'utf8')).data as Record<string, unknown>;
    const slug = String(wipFm.slug ?? 'wip');
    markdownPath = join(contentRoot, `issue-${issueNum}-${slug}.md`);
  }

  if (!markdownPath) {
    console.error('Usage: pnpm render <issue.md> [--dry-run]');
    console.error('       pnpm render --issue NN [--dry-run]');
    process.exit(1);
  }

  // Auto-assemble if the canonical is missing.
  if (!existsSync(markdownPath)) {
    const match = markdownPath.match(/issue-(\d+)-[^/]+\.md$/);
    if (match) {
      const issueNum = match[1]!;
      console.log(`  Canonical not found at ${markdownPath}.`);
      console.log(`  Running assemble first for Issue ${issueNum}...`);
      try {
        execFileSync('npx', ['tsx', resolve(__dirname, '..', 'assemble.ts'), '--issue', issueNum], {
          cwd: process.cwd(),
          stdio: 'inherit',
        });
      } catch (err) {
        console.error('Auto-assemble failed:', err instanceof Error ? err.message : err);
        process.exit(1);
      }
    } else {
      console.error(`Canonical not found and filename pattern not recognized: ${markdownPath}`);
      process.exit(1);
    }
  }

  const dryRun = flags.has('--dry-run');

  try {
    const result = await renderIssue(markdownPath, { dryRun });
    console.log('');
    console.log('  Shipped. — render complete');
    console.log('  ────────────────────────────');
    console.log(`  Source       : ${markdownPath}`);
    console.log(`  Output       : ${result.outputPath}${dryRun ? '  (dry-run, not written)' : ''}`);
    console.log(`  Archive      : ${result.archivePath}${dryRun ? '  (dry-run, not written)' : ''}`);
    console.log(`  Scratch copy : ${result.scratchPath}`);
    console.log(`  Sections     : ${result.sectionCount}`);
    console.log(`  FOB words    : ${result.wordCount}`);
    console.log(`  Log entries  : ${result.releaseLogEntryCount}`);
    console.log('');
  } catch (err) {
    console.error('Render failed:', err instanceof Error ? err.message : err);
    if (err instanceof Error && err.stack) console.error(err.stack);
    process.exit(1);
  }
}

void main();
