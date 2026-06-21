#!/usr/bin/env node
/**
 * check-floors — the mechanical guard against the "short issue" failure.
 *
 * The depth doctrine (content/DAILY.md, content/FORMULA.md) sets word floors so a
 * landmark never ships as two paragraphs again. Those floors were doctrine only;
 * nothing enforced them, so the nightly daily kept shipping under floor. This is
 * the enforcement: it counts the front-of-book (everything above the Release Log)
 * and fails when an issue is under floor.
 *
 *   node scripts/check-floors.mjs <file-or-dir> [...more]
 *   node scripts/check-floors.mjs ../content/anthropic-weekly/2026-25.md
 *   node scripts/check-floors.mjs ../content/anthropic-daily   # checks every file
 *
 * Exit code 0 = all at/above floor. Exit code 1 = at least one under floor.
 * Use --warn to report without failing (advisory mode).
 */

import { readFileSync, readdirSync, statSync } from "node:fs";
import { join, basename } from "node:path";

// Front-of-book floors (words), keyed by issue type. The hard floor is the line
// below which an issue is presumed thin and must be dug, not shipped. Targets are
// the healthy band from DAILY.md / FORMULA.md and are advisory.
const FLOORS = {
  "anthropic-daily": { hard: 700, target: 1000 },
  "anthropic-weekly": { hard: 1800, target: 2400 },
  "anthropic-monthly": { hard: 1500, target: 2500 },
};

// The heading that opens the back-of-book. Everything above it is front-of-book.
const RELEASE_LOG_RE = /^#{1,6}\s+(the\s+)?release\s+log\b/i;

function frontOfBookWordCount(markdown) {
  const body = markdown.replace(/^---\n[\s\S]*?\n---\n/, ""); // strip frontmatter
  const lines = body.split("\n");
  const front = [];
  for (const line of lines) {
    if (RELEASE_LOG_RE.test(line.trim())) break;
    front.push(line);
  }
  return front
    .join(" ")
    .replace(/[#>*_`|()\[\]]/g, " ")
    .split(/\s+/)
    .filter((w) => /[A-Za-z0-9]/.test(w)).length;
}

function issueType(markdown) {
  const m = markdown.match(/^type:\s*([a-z-]+)/im);
  return m ? m[1] : null;
}

function expand(paths) {
  const files = [];
  for (const p of paths) {
    const s = statSync(p);
    if (s.isDirectory()) {
      for (const f of readdirSync(p)) {
        if (f.endsWith(".md") && !f.startsWith("_") && f.toLowerCase() !== "readme.md") {
          files.push(join(p, f));
        }
      }
    } else {
      files.push(p);
    }
  }
  return files;
}

const args = process.argv.slice(2);
const warnOnly = args.includes("--warn");
const targets = args.filter((a) => !a.startsWith("--"));

if (targets.length === 0) {
  console.error("usage: node scripts/check-floors.mjs <file-or-dir> [...] [--warn]");
  process.exit(2);
}

let failures = 0;
let checked = 0;
for (const file of expand(targets)) {
  let md;
  try {
    md = readFileSync(file, "utf8");
  } catch {
    continue;
  }
  const type = issueType(md);
  const floor = FLOORS[type];
  if (!floor) continue; // not an issue file we gate
  checked++;
  const words = frontOfBookWordCount(md);
  const name = basename(file);
  if (words < floor.hard) {
    failures++;
    console.log(`UNDER FLOOR  ${name}  ${words}w  (${type} hard floor ${floor.hard})  -> dig, don't pad`);
  } else if (words < floor.target) {
    console.log(`thin        ${name}  ${words}w  (${type} target ${floor.target})`);
  } else {
    console.log(`ok          ${name}  ${words}w  (${type})`);
  }
}

if (checked === 0) {
  console.error("no issue files found to check");
  process.exit(2);
}

if (failures > 0 && !warnOnly) {
  console.log(`\n${failures} issue(s) under hard floor. The depth doctrine is not optional (content/DAILY.md).`);
  process.exit(1);
}
console.log(`\n${checked} checked, ${failures} under floor.`);
