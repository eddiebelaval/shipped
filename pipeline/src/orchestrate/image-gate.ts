/**
 * Shipped. image review gate.
 *
 * Every image an issue runs is rendered by pipeline/scripts/image-press.py, which
 * logs it to content/articles/issue-NN/images/manifest.json as pending. Eddie's
 * rule (2026-10-10): every image is reviewed by a human for legibility and look
 * before it publishes. The orchestrator runs `image-press.py check` on that
 * manifest before staging; a pending, rejected, or uncredited image blocks.
 *
 * An issue with no images folder has nothing to gate.
 */

import { existsSync } from 'node:fs';
import { basename, join } from 'node:path';

/** The issue's images folder if it has a manifest, else null. */
export function issueImageDir(markdownPath: string, contentRoot: string): string | null {
  const m = basename(markdownPath).match(/^issue-(\d+)/);
  const num = m?.[1];
  if (!num) return null;
  const dir = join(contentRoot, 'articles', `issue-${num.padStart(2, '0')}`, 'images');
  return existsSync(join(dir, 'manifest.json')) ? dir : null;
}
