/**
 * Shipped. — Next-action resolver.
 *
 * Reads the current Dashboard state (day, readiness, grades, gaps,
 * frontmatter metadata) and emits a prioritized action queue —
 * concrete, actionable moves the editor (or Claude, when delegated)
 * can take right now.
 *
 * DOCTRINE — Auto-ops, human-voice (see VISION.md).
 *
 * This resolver produces SCAFFOLDING actions only:
 *   - "add a `## Operator-layer implications` section"
 *   - "capture a new source article skeleton"
 *   - "lock the running order"
 *   - "assign a slug"
 *
 * The resolver shall NOT produce prose-generation prompts. Every
 * `claudePrompt` field in this file is a structural instruction.
 * The writer — human — produces the words that ship.
 *
 * If you are reading this and considering adding a prompt like
 * "write 300 words about X," stop. That crosses the auto-ops line.
 * See VISION.md § Auto-ops, human-voice.
 */

import type { Dashboard, DashboardArticle, SectionSlot } from './generate.js';

// ────────────────────────────────────────────────────────────────────
// Types
// ────────────────────────────────────────────────────────────────────

export type Priority = 'critical' | 'high' | 'medium' | 'low';
export type Phase = 'signal' | 'wip' | 'lock' | 'draft' | 'verify' | 'ship' | 'post-ship';

const PRIORITY_ORDER: Record<Priority, number> = { critical: 0, high: 1, medium: 2, low: 3 };

export interface NextAction {
  id: string;
  priority: Priority;
  phase: Phase;
  title: string;
  detail: string;
  why: string;
  claudePrompt: string;
  target?: { file?: string; section?: string; dimension?: string };
  estimate: string;
  command?: string;
}

export interface NextActionPlan {
  currentPhase: Phase;
  phaseName: string;
  dayOfWeek: string;
  hoursToLock: number | null;
  hoursToShip: number | null;
  actions: NextAction[];
  doctrine: string;
  generatedAt: string;
}

// ────────────────────────────────────────────────────────────────────
// Phase detection
// ────────────────────────────────────────────────────────────────────

interface TimeContext {
  phase: Phase;
  phaseName: string;
  dayOfWeek: string;
  hoursToLock: number | null;
  hoursToShip: number | null;
}

function detectPhase(dashboard: Dashboard): TimeContext {
  const now = new Date();
  const dayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  const day = now.getDay(); // local time — we're editorial-ops, not calendar-precise

  const shipDate = dashboard.shipDate ? parseLocalDate(dashboard.shipDate) : null;
  const lockDate = dashboard.lockDate ? parseLocalDate(dashboard.lockDate) : null;
  const hoursToLock = lockDate ? (lockDate.getTime() - now.getTime()) / 3600000 : null;
  const hoursToShip = shipDate ? (shipDate.getTime() - now.getTime()) / 3600000 : null;

  let phase: Phase = 'wip';
  let phaseName = 'WIP (Tue-Wed)';

  if (hoursToShip !== null && hoursToShip < -6) {
    phase = 'post-ship';
    phaseName = 'Post-ship (weekend)';
  } else if (day === 1) {
    phase = 'signal';
    phaseName = 'Signal (Mon)';
  } else if (day === 2 || day === 3) {
    phase = 'wip';
    phaseName = 'WIP (Tue-Wed)';
  } else if (day === 4) {
    // Thursday — lock AM, draft PM
    const hour = now.getHours();
    if (hour < 14) { phase = 'lock'; phaseName = 'Lock (Thu AM)'; }
    else { phase = 'draft'; phaseName = 'Draft (Thu PM)'; }
  } else if (day === 5) {
    // Friday — verify before 9 AM, ship at 9, post-ship after
    const hour = now.getHours();
    if (hour < 9) { phase = 'verify'; phaseName = 'Verify (Fri AM)'; }
    else if (hour < 12) { phase = 'ship'; phaseName = 'Ship (Fri 9 AM)'; }
    else { phase = 'post-ship'; phaseName = 'Post-ship (Fri PM)'; }
  } else {
    phase = 'post-ship';
    phaseName = 'Post-ship (weekend)';
  }

  return {
    phase,
    phaseName,
    dayOfWeek: dayNames[day] ?? 'Unknown',
    hoursToLock,
    hoursToShip,
  };
}

function parseLocalDate(s: string): Date {
  // Parse 'YYYY-MM-DD' as local midnight, not UTC
  const m = s.match(/^(\d{4})-(\d{2})-(\d{2})/);
  if (!m) return new Date(s);
  return new Date(Number(m[1]), Number(m[2]) - 1, Number(m[3]));
}

// ────────────────────────────────────────────────────────────────────
// Main resolver
// ────────────────────────────────────────────────────────────────────

export function resolveNextActions(dashboard: Dashboard): NextActionPlan {
  const ctx = detectPhase(dashboard);
  const actions: NextAction[] = [];

  // Phase-aware rules
  if (ctx.phase === 'signal') {
    pushMaybe(actions, ruleSignalKickoff(dashboard));
  }

  if (ctx.phase === 'wip' || ctx.phase === 'signal') {
    pushMaybe(actions, ruleInventoryBelowFormula(dashboard));
    pushMany(actions, ruleLowGradeRetrofit(dashboard));
    pushMany(actions, ruleUnfilledRequiredSections(dashboard));
  }

  if (ctx.phase === 'wip' || ctx.phase === 'lock') {
    pushMany(actions, rulePlacementOpen(dashboard));
    pushMaybe(actions, ruleTermOfIssueUnset(dashboard, ctx));
    pushMaybe(actions, ruleTitleOrSlugTbd(dashboard, ctx));
  }

  if (ctx.phase === 'lock') {
    pushMaybe(actions, ruleRunningOrderNotLocked(dashboard, ctx));
    pushMany(actions, ruleUnfilledRequiredSections(dashboard, 'critical'));
  }

  if (ctx.phase === 'draft') {
    pushMaybe(actions, ruleDraftProse(dashboard));
    pushMaybe(actions, ruleReleaseLogScrape(dashboard));
  }

  if (ctx.phase === 'verify') {
    pushMaybe(actions, ruleVerifierRun(dashboard));
  }

  if (ctx.phase === 'ship') {
    pushMaybe(actions, ruleShip(dashboard));
  }

  if (ctx.phase === 'post-ship') {
    pushMaybe(actions, rulePostShipNextIssue(dashboard));
  }

  // Always-on rules
  pushMany(actions, ruleLowGradePromoted(dashboard));

  // Sort: priority, then by id for stability
  actions.sort((a, b) => {
    const p = PRIORITY_ORDER[a.priority] - PRIORITY_ORDER[b.priority];
    if (p !== 0) return p;
    return a.id.localeCompare(b.id);
  });

  // Cap at 6 — keep the surface actionable, not overwhelming
  const capped = actions.slice(0, 6);

  return {
    currentPhase: ctx.phase,
    phaseName: ctx.phaseName,
    dayOfWeek: ctx.dayOfWeek,
    hoursToLock: ctx.hoursToLock,
    hoursToShip: ctx.hoursToShip,
    actions: capped,
    doctrine: 'Auto-ops only. Resolver proposes structural scaffolding, not prose. See VISION.md § Auto-ops, human-voice.',
    generatedAt: new Date().toISOString(),
  };
}

function pushMaybe(list: NextAction[], item: NextAction | null): void {
  if (item) list.push(item);
}
function pushMany(list: NextAction[], items: NextAction[]): void {
  for (const i of items) list.push(i);
}

// ────────────────────────────────────────────────────────────────────
// Rules
// ────────────────────────────────────────────────────────────────────

function ruleSignalKickoff(d: Dashboard): NextAction | null {
  const hasSignal = [...d.sections.flatMap(s => s.articles), ...d.scratchPad]
    .some(a => a.filename === 'signal-report.md');
  if (hasSignal) return null;
  return {
    id: 'signal-kickoff',
    priority: 'high',
    phase: 'signal',
    title: 'Run /shipped-signal to kick off the week',
    detail: 'Monday signal report is the first thing on the calendar. It seeds the WIP.',
    why: 'No signal-report.md on disk for this issue.',
    claudePrompt: `Invoke /shipped-signal --issue ${d.issue}. This runs the Monday research sweep and produces content/articles/issue-${d.issue}/signal-report.md. Report back with the headline findings.`,
    estimate: '15–30 min',
    command: '/shipped-signal',
  };
}

function ruleInventoryBelowFormula(d: Dashboard): NextAction | null {
  if (d.articleCountTotal >= d.articleCountHealthy.min) return null;
  const missing = d.articleCountHealthy.min - d.articleCountTotal;
  return {
    id: 'inventory-below-formula',
    priority: 'high',
    phase: 'wip',
    title: `Capture ${missing} more source article${missing === 1 ? '' : 's'}`,
    detail: `Issue has ${d.articleCountTotal} topic articles; FORMULA.md minimum is ${d.articleCountHealthy.min}.`,
    why: 'Thin inventories produce thin issues. The formula minimum exists for a reason.',
    claudePrompt: `Create a new source article skeleton in content/articles/issue-${d.issue}/. Pick a topic from signal-report.md that isn't already captured. Use conway-leak-analysis.md as the structural template — same frontmatter fields (title, issue, section, status: research, created, updated, sources, placement_open if ambiguous). Include all rubric-relevant section headers: ## Attribution caveats, ## The editorial beat (or ## How this fits the issue), ## Operator-layer implications, ## Open questions / TODOs before press, ## Voice notes for the distilled prose. Populate each with research notes and structural prompts — DO NOT write prose that would ship. The writer produces the words.`,
    estimate: '30–45 min',
  };
}

function ruleLowGradeRetrofit(d: Dashboard): NextAction[] {
  const all = [...d.sections.flatMap(s => s.articles), ...d.scratchPad];
  const lowGrade = all
    .filter(a => !a.grade.overridden)
    .filter(a => a.section !== 'background')
    .filter(a => a.grade.letter === 'D' || a.grade.letter === 'F');

  const out: NextAction[] = [];
  for (const a of lowGrade) {
    const weakest = a.grade.dimensions.slice().sort((x, y) => x.score - y.score)[0];
    if (!weakest) continue;
    out.push({
      id: `retrofit-${a.filename}`,
      priority: a.grade.letter === 'F' ? 'high' : 'medium',
      phase: 'wip',
      title: `Retrofit ${a.filename.replace(/\.md$/, '')}`,
      detail: `Graded ${a.grade.letter} (${a.grade.total}/28). Weakest: ${weakest.label} at ${weakest.score}/4.`,
      why: weakest.note,
      claudePrompt: `Open content/articles/issue-${d.issue}/${a.filename}. The article grades ${a.grade.letter} (${a.grade.total}/28). Weakest dimension is "${weakest.label}" (${weakest.score}/4). Rubric note: "${weakest.note}". Add the structural scaffolding that dimension rewards — section headers, bullet slots, reference anchors to STYLE.md moves, attribution caveats. DO NOT write prose. The writer produces the words that ship. After adding the scaffolding, regenerate the dashboard (pnpm dashboard) and report the new grade.`,
      target: { file: a.filename, dimension: weakest.key },
      estimate: '15–25 min',
    });
  }
  return out;
}

function ruleLowGradePromoted(d: Dashboard): NextAction[] {
  // C-graded articles in required sections, when not already flagged as D/F retrofit
  const all = [...d.sections.flatMap(s => s.articles), ...d.scratchPad];
  const cGrade = all
    .filter(a => !a.grade.overridden)
    .filter(a => a.section !== 'background')
    .filter(a => a.grade.letter === 'C');

  const out: NextAction[] = [];
  for (const a of cGrade) {
    const weakest = a.grade.dimensions.slice().sort((x, y) => x.score - y.score)[0];
    if (!weakest) continue;
    out.push({
      id: `polish-${a.filename}`,
      priority: 'medium',
      phase: 'wip',
      title: `Polish ${a.filename.replace(/\.md$/, '')} (C → B)`,
      detail: `Graded ${a.grade.letter} (${a.grade.total}/28). Closest-to-B dimension: ${weakest.label} at ${weakest.score}/4.`,
      why: weakest.note,
      claudePrompt: `Open content/articles/issue-${d.issue}/${a.filename}. Graded ${a.grade.letter}. Weakest dimension is "${weakest.label}" at ${weakest.score}/4. Rubric note: "${weakest.note}". Add the structural scaffolding that dimension rewards (section headers, bullet slots, structural references). DO NOT write prose. Report the grade after the change.`,
      target: { file: a.filename, dimension: weakest.key },
      estimate: '10–15 min',
    });
  }
  return out;
}

function ruleUnfilledRequiredSections(d: Dashboard, overridePriority?: Priority): NextAction[] {
  return d.sections
    .filter(s => s.required && s.gap !== null)
    .filter(s => s.articleCountMin > 0)
    .map(s => ({
      id: `fill-${s.key}`,
      priority: overridePriority ?? ('high' as Priority),
      phase: 'wip' as Phase,
      title: `Fill "${s.label}" — ${s.gap}`,
      detail: `${s.articles.length}/${s.articleCountMin} articles. ${s.description}`,
      why: `Required section below minimum article count.`,
      claudePrompt: `The "${s.label}" section needs ${s.articleCountMin - s.articles.length} more source article(s). Create a skeleton in content/articles/issue-${d.issue}/ with section: ${s.key} in the frontmatter. Match conway-leak-analysis.md's structure. Include all required RUBRIC.md sections as scaffolding — no prose in the body beyond research notes.`,
      estimate: '30–45 min',
    }));
}

function rulePlacementOpen(d: Dashboard): NextAction[] {
  const all = [...d.sections.flatMap(s => s.articles), ...d.scratchPad];
  return all
    .filter(a => a.placementOpen !== null)
    .map(a => ({
      id: `placement-${a.filename}`,
      priority: 'medium' as Priority,
      phase: 'lock' as Phase,
      title: `Resolve placement: ${a.filename.replace(/\.md$/, '')}`,
      detail: a.placementOpen ?? 'Placement flagged open in frontmatter.',
      why: 'Thursday running-order lock requires placement decisions resolved.',
      claudePrompt: `The article content/articles/issue-${d.issue}/${a.filename} has placement_open: "${a.placementOpen}". Eddie needs to make the call before Thursday lock. Present the tradeoffs (from the article's own "How this fits the issue" section) and ask Eddie to decide. Once decided: update the frontmatter section: field via the dashboard API (POST /api/move) and remove placement_open. Do not decide on Eddie's behalf.`,
      target: { file: a.filename },
      estimate: "5 min (Eddie's call)",
    }));
}

function ruleTermOfIssueUnset(d: Dashboard, ctx: TimeContext): NextAction | null {
  if (d.theme && d.theme !== 'TBD' && d.theme !== '') return null;
  if (ctx.hoursToLock !== null && ctx.hoursToLock > 36) return null; // not urgent until <36h
  const priority = ctx.hoursToLock !== null && ctx.hoursToLock < 12 ? 'high' : 'medium';
  return {
    id: 'term-of-issue',
    priority,
    phase: 'lock',
    title: 'Name the Term of the Issue',
    detail: 'Term of the Issue is the concept this issue names. Locked by Thursday.',
    why: 'Without a named term, the Close has nothing to land on and the issue reads as unthreaded.',
    claudePrompt: `Open content/issue-${d.issue}-wip.md. The frontmatter term_of_issue field is TBD or empty. Read the signal report + source articles and surface 2-3 candidate terms (each with a short definition). Present them to Eddie for a pick. Do not pick on his behalf — naming the term is editorial judgment. Once picked, update the WIP frontmatter.`,
    estimate: "10 min (Eddie's call)",
  };
}

function ruleTitleOrSlugTbd(d: Dashboard, ctx: TimeContext): NextAction | null {
  const needsTitle = !d.title || d.title === 'TBD' || d.title === '';
  const needsSlug = !d.slug || d.slug === 'TBD' || d.slug === '';
  if (!needsTitle && !needsSlug) return null;
  if (ctx.hoursToLock !== null && ctx.hoursToLock > 36) return null;
  const priority = ctx.hoursToLock !== null && ctx.hoursToLock < 12 ? 'high' : 'medium';
  const fields = [needsTitle && 'title', needsSlug && 'slug'].filter(Boolean).join(' + ');
  return {
    id: 'title-slug-tbd',
    priority,
    phase: 'lock',
    title: `Assign ${fields}`,
    detail: `Issue ${d.issue} ${fields} still TBD.`,
    why: 'Title and slug lock editorial identity before prose begins. Thursday is the gate.',
    claudePrompt: `Open content/issue-${d.issue}-wip.md. The frontmatter ${fields} field(s) are TBD. Surface 3 candidates each, drawn from the issue's thesis and Term of the Issue. Present to Eddie. Do not pick on his behalf. Once picked, update the WIP frontmatter.`,
    estimate: "10 min (Eddie's call)",
  };
}

function ruleRunningOrderNotLocked(d: Dashboard, ctx: TimeContext): NextAction | null {
  if (d.status && d.status.toLowerCase().includes('lock')) return null;
  const priority = ctx.hoursToLock !== null && ctx.hoursToLock < 4 ? 'critical' : 'high';
  return {
    id: 'running-order-lock',
    priority,
    phase: 'lock',
    title: 'Lock the running order',
    detail: 'Thursday gate. After this, no new sections, no moved sections until post-ship corrections.',
    why: 'The lock is what separates research from draft. Missing it means prose begins against moving targets.',
    claudePrompt: `All running-order decisions should be resolved by now: lead story, B-story placement, investigation slot(s), Also Shipped line-up, Term of Issue, title, slug. Read the dashboard and report unresolved items. Once Eddie confirms all resolved, update content/issue-${d.issue}-wip.md frontmatter: running_order_locked: true + status: locked. Do not lock on Eddie's behalf — this is the editorial gate.`,
    estimate: '5 min once gates clear',
  };
}

function ruleDraftProse(d: Dashboard): NextAction | null {
  return {
    id: 'draft-prose',
    priority: 'high',
    phase: 'draft',
    title: 'Write front-of-book prose',
    detail: 'Thursday PM — draft the Open, distilled Lead, Also Shipped, Quiet on the Wire, Close.',
    why: 'Source articles are research. The magazine ships prose. The writer produces prose.',
    claudePrompt: `REMINDER — auto-ops doctrine: this action is scaffolding, not prose generation. Open content/issue-${d.issue}-wip.md. For each front-of-book section in the locked running order, verify the skeleton is in place (section heading, word-budget target noted, source article linked). Do NOT write the prose — that is Eddie's work. Report any sections without a skeleton.`,
    estimate: '2–4 hours (Eddie writing)',
  };
}

function ruleReleaseLogScrape(d: Dashboard): NextAction | null {
  return {
    id: 'release-log-scrape',
    priority: 'high',
    phase: 'draft',
    title: 'Run Thursday PM scraper for Release Log',
    detail: 'Thursday PM scraper pass seeds the Back-of-Book.',
    why: 'Release Log compiles from scraper output. Without a fresh scrape, the Back-of-Book is stale.',
    claudePrompt: `Invoke pnpm scrape in shipped/pipeline. Report the number of new releases detected and any scrape failures. The Release Log renderer will consume this on Friday morning.`,
    estimate: '10 min',
    command: 'pnpm scrape',
  };
}

function ruleVerifierRun(d: Dashboard): NextAction | null {
  return {
    id: 'verifier-run',
    priority: 'critical',
    phase: 'verify',
    title: 'Run /verify-shipped attestation gates',
    detail: 'Friday morning. Every URL, number, quote, date, voice check must pass.',
    why: 'VISION.md non-negotiable: the verifier runs, or the issue does not ship.',
    claudePrompt: `Invoke /verify-shipped --issue ${d.issue}. Report the pass/fail of each gate (URL, number, quote, date, voice). If any gate fails, Eddie fixes the copy — do not modify copy to pass the gate. See VISION.md: voice gate is immutable mid-issue.`,
    estimate: '10–20 min (plus fix time)',
    command: '/verify-shipped',
  };
}

function ruleShip(d: Dashboard): NextAction | null {
  return {
    id: 'ship',
    priority: 'critical',
    phase: 'ship',
    title: 'Ship Issue ' + d.issue,
    detail: 'Friday 9 AM — stage + human git push.',
    why: 'VISION.md non-negotiable: the human pushes git.',
    claudePrompt: `Invoke /publish-shipped to stage the rendered HTML to id8labs/public/shipped/${d.issue}/. After staging completes, report the stage path. Eddie runs git commit && git push from the id8labs repo. Do NOT automate the push.`,
    estimate: '5 min stage + Eddie pushing',
    command: '/publish-shipped',
  };
}

function rulePostShipNextIssue(d: Dashboard): NextAction | null {
  return {
    id: 'post-ship-next',
    priority: 'low',
    phase: 'post-ship',
    title: 'Capture post-ship lessons + open next issue',
    detail: 'Note what worked / what broke / what to carry forward. Create issue-NN+1-wip.md scaffolding.',
    why: 'Lessons decay fast. Capture before Monday.',
    claudePrompt: `Two tasks: (1) Create content/articles/issue-${d.issue}/post-ship.md documenting what worked, what broke, what to carry forward. Use the standard article frontmatter with section: post-ship. (2) Create content/issue-${padIssue(d.issue, +1)}-wip.md scaffolding — copy the structure of the current WIP with empty fields, status: drafting, ship_date set to next Friday. Do not populate content — the signal report (Monday) does that.`,
    estimate: '15 min',
  };
}

function padIssue(current: string, delta: number): string {
  const n = parseInt(current, 10);
  if (isNaN(n)) return current;
  return String(n + delta).padStart(2, '0');
}
