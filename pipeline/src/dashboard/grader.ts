/**
 * Shipped. — Article grader (v2, identity-aligned).
 *
 * Evaluates a source article against content/RUBRIC.md v2.
 * Seven dimensions × 4 points = 28 total. Letter grade A–F.
 *
 * The grader reads structural + vocabulary signals. It flags patterns
 * the rubric rewards or penalizes. It does not judge editorial quality.
 * That's the editor's job. This is a readiness proxy, not a quality score.
 */

// ────────────────────────────────────────────────────────────────────
// Types
// ────────────────────────────────────────────────────────────────────

export type DimensionKey =
  | 'sourcing'
  | 'attribution'
  | 'counter-frame'
  | 'operator-takeaway'
  | 'stake'
  | 'throughline'
  | 'voice';

export type LetterGrade = 'A' | 'B' | 'C' | 'D' | 'F';

export interface DimensionScore {
  key: DimensionKey;
  label: string;
  score: number;        // 0–4
  letter: LetterGrade;
  note: string;
}

export interface Grade {
  total: number;              // 0–28
  letter: LetterGrade;
  status: string;
  dimensions: DimensionScore[];
  overridden: boolean;
  overrideReason: string | null;
}

const DIM_LABELS: Record<DimensionKey, string> = {
  sourcing: 'Sourcing & primary link',
  attribution: 'Attribution discipline',
  'counter-frame': 'The counter-frame',
  'operator-takeaway': 'Operator takeaway',
  stake: 'Stake & stance',
  throughline: 'Throughline',
  voice: 'Voice setup',
};

export interface GraderInput {
  body: string;
  frontmatter: Record<string, unknown>;
  filename: string;
}

// Primary-source domains — the originating announcement of a fact.
const PRIMARY_DOMAINS = new Set([
  'anthropic.com',
  'red.anthropic.com',
  'platform.claude.com',
  'support.claude.com',
  'transformer-circuits.pub',
  'github.com', // when paired with /anthropics
  'vercel.com',
  'openai.com',
  'google.com',
  'microsoft.com',
  'aws.amazon.com',
  'cloud.google.com',
  'docs.anthropic.com',
  'assets.anthropic.com',
]);

// ────────────────────────────────────────────────────────────────────
// Main
// ────────────────────────────────────────────────────────────────────

export function gradeArticle(input: GraderInput): Grade {
  if (input.frontmatter.grade_override === true) {
    return {
      total: 28,
      letter: 'A',
      status: 'Overridden',
      dimensions: [],
      overridden: true,
      overrideReason: String(input.frontmatter.grade_override_reason ?? 'Override (no reason given)'),
    };
  }

  const dimensions: DimensionScore[] = [
    scoreSourcing(input),
    scoreAttribution(input),
    scoreCounterFrame(input),
    scoreOperatorTakeaway(input),
    scoreStake(input),
    scoreThroughline(input),
    scoreVoice(input),
  ];

  const total = dimensions.reduce((sum, d) => sum + d.score, 0);
  const letter = totalToLetter(total);
  const status = letterToStatus(letter);

  return { total, letter, status, dimensions, overridden: false, overrideReason: null };
}

// ────────────────────────────────────────────────────────────────────
// Dimension 1 — Sourcing & primary link
// ────────────────────────────────────────────────────────────────────

function scoreSourcing(input: GraderInput): DimensionScore {
  const sources = Array.isArray(input.frontmatter.sources) ? input.frontmatter.sources : [];
  const count = sources.length;

  let primaryCount = 0;
  const hostnames = new Set<string>();
  for (const s of sources) {
    const url = String(s);
    const m = url.match(/^https?:\/\/([^/]+)(.*)/);
    if (!m) continue;
    const host = m[1]!.replace(/^www\./, '');
    const path = m[2] ?? '';
    hostnames.add(host);
    if (PRIMARY_DOMAINS.has(host)) {
      // github.com only counts as primary if path includes /anthropics or /openai
      if (host === 'github.com') {
        if (/^\/(anthropics|openai|vercel|microsoft|google)/i.test(path)) primaryCount++;
      } else {
        primaryCount++;
      }
    }
  }

  const outlets = hostnames.size;

  let score = 0;
  let note = '';
  if (primaryCount >= 1 && count >= 3 && outlets >= 2) {
    score = 4;
    note = `${count} sources · ${primaryCount} primary · ${outlets} unique outlets. Full attestation trail.`;
  } else if (primaryCount >= 1 && count >= 2) {
    score = 3;
    note = `${count} sources including ${primaryCount} primary. Add one more independent outlet for full credit.`;
  } else if (count >= 2 && primaryCount === 0) {
    score = 2;
    note = `${count} sources, ${outlets} outlets — but no primary source (no originating company/research URL). Add the official announcement/bulletin.`;
  } else if (count === 1) {
    score = 1;
    note = 'Single-source dependency. Add independent verification before press.';
  } else {
    score = 0;
    note = 'No sources listed in frontmatter. Article cannot move past research.';
  }

  return { key: 'sourcing', label: DIM_LABELS.sourcing, score, letter: scoreToLetter(score), note };
}

// ────────────────────────────────────────────────────────────────────
// Dimension 2 — Attribution discipline
// ────────────────────────────────────────────────────────────────────

function scoreAttribution(input: GraderInput): DimensionScore {
  const section = extractSection(input.body, /^##\s+Attribution\s+caveats?$/im);
  const softeningVocab = /\b(reported by|per |according to|confirmed by|attributed to|softened|denial|denied|initially credited|claimed to|claimed by)\b/i;

  let score = 0;
  let note = '';

  if (!section) {
    if (softeningVocab.test(input.body)) {
      score = 1;
      note = 'No dedicated attribution section, but softening vocabulary found inline. Capture caveats explicitly before draft.';
    } else {
      score = 0;
      note = 'No attribution discipline visible. Add ## Attribution caveats before moving to draft.';
    }
    return { key: 'attribution', label: DIM_LABELS.attribution, score, letter: scoreToLetter(score), note };
  }

  const bullets = (section.match(/^[-*]\s/gm) ?? []).length;
  // Count capitalized named entities (crude heuristic — excludes sentence-starts)
  const namedEntities = new Set<string>();
  const nameMatches = section.match(/(?:^|[^.!?]\s+)([A-Z][a-z]+(?:[A-Z][a-z]+)?(?:\.[a-z]+)?)/g) ?? [];
  for (const m of nameMatches) {
    const clean = m.trim().replace(/^\s*[,.;:]/, '');
    if (clean.length > 2 && !/^(The|This|That|These|Those|When|Where|What|Who|Why|How|For|After|Before|During|Also|Still|Only|Not|But|And|Or)$/.test(clean)) {
      namedEntities.add(clean);
    }
  }

  if (bullets >= 3 && namedEntities.size >= 2) {
    score = 4;
    note = `Caveats section with ${bullets} bullets, ≥${namedEntities.size} named entities. Full attribution discipline.`;
  } else if (bullets >= 2) {
    score = 3;
    note = `Caveats section with ${bullets} items — add one more with a named entity for full credit.`;
  } else if (bullets >= 1 || softeningVocab.test(section)) {
    score = 2;
    note = 'Caveats section exists but thin. Add specific, named caveats.';
  } else {
    score = 1;
    note = 'Caveats section is generic. Name specific entities, outlets, or claims.';
  }

  return { key: 'attribution', label: DIM_LABELS.attribution, score, letter: scoreToLetter(score), note };
}

// ────────────────────────────────────────────────────────────────────
// Dimension 3 — The counter-frame
// ────────────────────────────────────────────────────────────────────

function scoreCounterFrame(input: GraderInput): DimensionScore {
  // Signal words/phrases that indicate the article is finding a second read
  const counterFramePatterns = [
    /\bthe headline isn['’]t\b/i,
    /\bbut the (story|news|beat) is\b/i,
    /\bthe implication is\b/i,
    /\bthe real news\b/i,
    /\bthe beat is\b/i,
    /\bwhat matters isn['’]t\b/i,
    /\bthe frame that matters\b/i,
    /\bthe twist\b/i,
    /\bthe counter-?read\b/i,
    /\bnot the announcement\b/i,
    /\bthe tell\b/i,
    /\bwhat['’]s actually\b/i,
    /\bthe second news\b/i,
    /\bthat['’]s the news\b/i,
    /\bthe editorial beat\b/i,
    /\bthe signal that matters\b/i,
    /\bthird[- ]act\b/i,
    /\bthe pattern is\b/i,
    /\bthe shape (is|of)\b/i,
    /\bthe deeper (story|news|beat)\b/i,
  ];

  let signalHits = 0;
  for (const pat of counterFramePatterns) {
    if (pat.test(input.body)) signalHits++;
  }

  // Check for a dedicated analytical section
  const hasEditorialSection =
    !!extractSection(input.body, /^##\s+The\s+editorial\s+beat$/im) ||
    !!extractSection(input.body, /^##\s+The\s+signal\s+that\s+matters$/im) ||
    !!extractSection(input.body, /^##\s+How\s+this\s+fits\s+the\s+issue$/im) ||
    !!extractSection(input.body, /^##\s+What['’]s\s+actually\s+(?:going on|happening)$/im);

  // Check for named evidence (charts, prices, quotes, benchmarks)
  const hasNamedEvidence =
    /\b\d+(\.\d+)?%\b/.test(input.body) ||   // percentages
    /-?\d+(\.\d+)?%/.test(input.body) ||     // stock moves
    />\s*\*?"[^"]{20,}\*?\s*—/.test(input.body) ||  // attributed quotes
    /\$[\d.]+[MBK]?\b/.test(input.body);     // dollar figures

  let score = 0;
  let note = '';

  if (signalHits >= 2 && hasEditorialSection && hasNamedEvidence) {
    score = 4;
    note = `Counter-frame explicitly articulated (${signalHits} signal phrases) + dedicated analytical section + named evidence. House move executed.`;
  } else if (signalHits >= 1 && hasEditorialSection) {
    score = 3;
    note = `Counter-frame present (${signalHits} signal phrase${signalHits === 1 ? '' : 's'}) + analytical section — add specific evidence (chart, quote, price) for full credit.`;
  } else if (hasEditorialSection && signalHits === 0) {
    score = 2;
    note = 'Analytical section exists but no explicit counter-frame language. Is there a "second read" here, or is this announcement coverage?';
  } else if (signalHits >= 1) {
    score = 2;
    note = `Counter-frame signals present (${signalHits}) but no dedicated section. Crystallize the angle.`;
  } else if (/\b(matters|implication|signal|posture|read)\b/i.test(input.body)) {
    score = 1;
    note = 'Analytical framing implied but no explicit counter-frame. Ask: what\'s the story that isn\'t the announcement?';
  } else {
    score = 0;
    note = 'Straight announcement coverage. Shipped.\'s house move is finding the story that isn\'t the headline. Find it.';
  }

  return { key: 'counter-frame', label: DIM_LABELS['counter-frame'], score, letter: scoreToLetter(score), note };
}

// ────────────────────────────────────────────────────────────────────
// Dimension 4 — Operator takeaway
// ────────────────────────────────────────────────────────────────────

function scoreOperatorTakeaway(input: GraderInput): DimensionScore {
  const sectionPatterns = [
    /^##\s+Operator-?layer\s+implications?$/im,
    /^##\s+For\s+builders?$/im,
    /^##\s+SOPs?$/im,
    /^##\s+What\s+to\s+do$/im,
    /^##\s+If\s+you\s+use\b/im,
    /^##\s+Builder\s+SOPs?$/im,
    /^##\s+The\s+operator-?layer\s+implications?$/im,
    /^##\s+How\s+to\s+use$/im,
  ];

  let section: string | null = null;
  for (const pat of sectionPatterns) {
    const extracted = extractSection(input.body, pat);
    if (extracted) { section = extracted; break; }
  }

  // Count imperative verbs at the start of bullets anywhere
  const imperativeVerbs = /^[-*]\s+(Audit|Rotate|Check|Verify|Migrate|Update|Stop|Assume|Re-?issue|Revoke|Watch|Read|Use|Install|Configure|Treat|Set|Flag|Monitor|Disable|Enable|Test|Rebuild|Re-tune|Re-read|Patch|Deploy)\b/gm;
  const imperativeMatches = input.body.match(imperativeVerbs) ?? [];

  let score = 0;
  let note = '';

  if (section) {
    const sectionImperatives = (section.match(imperativeVerbs) ?? []).length;
    if (sectionImperatives >= 3) {
      score = 4;
      note = `Dedicated operator section + ${sectionImperatives} imperative-verb items. Clear builder actions.`;
    } else if (sectionImperatives >= 1) {
      score = 3;
      note = `Dedicated section + ${sectionImperatives} actionable item${sectionImperatives === 1 ? '' : 's'}. Add more imperative-led items for full credit.`;
    } else {
      score = 2;
      note = 'Operator section exists but no imperative-verb items. Convert implications to actions the reader can take.';
    }
  } else if (imperativeMatches.length >= 3) {
    score = 3;
    note = `${imperativeMatches.length} imperative-verb items scattered in prose. Consolidate into a dedicated operator section.`;
  } else if (imperativeMatches.length >= 1) {
    score = 2;
    note = `${imperativeMatches.length} action item${imperativeMatches.length === 1 ? '' : 's'} implied. Elevate to a dedicated section.`;
  } else if (/\b(builders?|developers?|engineers?|operators?)\b/i.test(input.body)) {
    score = 1;
    note = 'Builder-relevant content but no explicit action layer. What should the reader actually do?';
  } else {
    score = 0;
    note = 'Purely informational. Shipped. serves builders — land an action-layer implication.';
  }

  return { key: 'operator-takeaway', label: DIM_LABELS['operator-takeaway'], score, letter: scoreToLetter(score), note };
}

// ────────────────────────────────────────────────────────────────────
// Dimension 5 — Stake & stance
// ────────────────────────────────────────────────────────────────────

function scoreStake(input: GraderInput): DimensionScore {
  const declarativePatterns = [
    /\bthis matters because\b/i,
    /\bthe posture is\b/i,
    /\bthe call is\b/i,
    /\bwhat\s+(Anthropic|Vercel|Lovable|the lab|they)\s+chose\b/i,
    /\bthe answer is\b/i,
    /\bthat['’]s the news\b/i,
    /\bthe precedent is\b/i,
    /\bthe question (is|isn['’]t|becomes)\b/i,
    /\bthe decision was\b/i,
    /\bwhat this means\b/i,
    /\bthe bet is\b/i,
    /\bthe tell is\b/i,
    /\bthe shape of (this|it) is\b/i,
  ];

  const strongVerbs = /\b(conceded|signals|reveals|refused|doubled down|broke|cracked|capitulated|hedged|retreated|announced|committed|overrode|exposed|failed|collapsed|pivoted|staged)\b/i;

  const hedgingPhrases = [
    /\barguably\b/i,
    /\bsome might say\b/i,
    /\bit could be argued\b/i,
    /\bperhaps\b/i,
    /\bmay be seen as\b/i,
    /\bone could\b/i,
    /\bin some sense\b/i,
    /\barguably\b/i,
    /\bon the one hand.*on the other\b/i,
  ];

  let declarativeHits = 0;
  for (const pat of declarativePatterns) {
    if (pat.test(input.body)) declarativeHits++;
  }
  const strongVerbHits = (input.body.match(new RegExp(strongVerbs, 'gi')) ?? []).length;

  let hedgingHits = 0;
  for (const pat of hedgingPhrases) {
    if (pat.test(input.body)) hedgingHits++;
  }

  const claimScore = declarativeHits + Math.min(2, Math.floor(strongVerbHits / 2));

  let score = 0;
  let note = '';
  if (claimScore >= 3 && hedgingHits === 0) {
    score = 4;
    note = `${declarativeHits} declarative claim${declarativeHits === 1 ? '' : 's'} + ${strongVerbHits} strong verb${strongVerbHits === 1 ? '' : 's'}, zero hedging. Stance stated plainly.`;
  } else if (claimScore >= 2 && hedgingHits <= 1) {
    score = 3;
    note = `${claimScore} stance signals, ${hedgingHits} hedging phrase${hedgingHits === 1 ? '' : 's'}. Tighten — kill the hedges.`;
  } else if (claimScore >= 1) {
    score = 2;
    note = `${claimScore} stance signal${claimScore === 1 ? '' : 's'}. Stance is present but muted. Sharpen.`;
  } else if (strongVerbHits >= 1) {
    score = 1;
    note = 'Reporting with reserved posture — some strong verbs, no stated position. State what you think.';
  } else {
    score = 0;
    note = 'No stance. Shipped.\'s voice is "opinions stated, never hedged." State yours.';
  }

  if (hedgingHits >= 2 && score > 1) {
    score = Math.max(1, score - 1);
    note += ` Penalized for ${hedgingHits} hedging phrases.`;
  }

  return { key: 'stake', label: DIM_LABELS.stake, score, letter: scoreToLetter(score), note };
}

// ────────────────────────────────────────────────────────────────────
// Dimension 6 — Throughline
// ────────────────────────────────────────────────────────────────────

function scoreThroughline(input: GraderInput): DimensionScore {
  const crossRefPatterns = [
    /\bties back to\b/i,
    /\becho(es|ing)\b/i,
    /\bsame pattern as\b/i,
    /\bsame shape as\b/i,
    /\bthe counterweight\b/i,
    /\bthe comparand\b/i,
    /\bfrom the [Ll]ead\b/i,
    /\balongside\b/i,
    /\bin the same issue\b/i,
    /\bread this next to\b/i,
    /\bpair(s|ed)? with\b/i,
    /\bthe\s+[A-Z][a-z]+\s+Week\b/,  // "Trust Week"
    /\brhym(es|ing)\b/i,
    /\bmirrors?\b/i,
  ];

  // Named thread topics — articles in current issue
  const topicNames = ['Conway', 'Claude Design', 'Trust Week', 'OpenClaw', 'Lovable', 'Vercel', 'Amazon-Anthropic', 'Mythos', 'Glasswing', 'Opus 4.7'];
  let crossRefHits = 0;
  for (const pat of crossRefPatterns) {
    if (pat.test(input.body)) crossRefHits++;
  }
  let topicHits = 0;
  for (const topic of topicNames) {
    // Don't count the article's own topic — use title as a weak proxy
    const title = String(input.frontmatter.title ?? '');
    if (title.toLowerCase().includes(topic.toLowerCase())) continue;
    const regex = new RegExp(`\\b${topic.replace(/[-/\\^$*+?.()|[\]{}]/g, '\\$&')}\\b`);
    if (regex.test(input.body)) topicHits++;
  }

  // Check for Term-of-the-Issue connection
  const termOfIssueCandidates = ['Presence', 'Trust', 'Shadow release', 'Context', 'Scope'];
  let termHits = 0;
  for (const term of termOfIssueCandidates) {
    const regex = new RegExp(`\\b${term}\\b`);
    if (regex.test(input.body)) termHits++;
  }

  const crossCount = crossRefHits + topicHits;

  let score = 0;
  let note = '';
  if (crossCount >= 3 && termHits >= 1) {
    score = 4;
    note = `${topicHits} topic cross-references + ${crossRefHits} connection phrases + Term-of-Issue connection. Tied to the issue's spine.`;
  } else if (crossCount >= 2) {
    score = 3;
    note = `${crossCount} cross-references to other issue content. Add a Term-of-Issue tie for full credit.`;
  } else if (crossCount >= 1) {
    score = 2;
    note = `${crossCount} cross-reference. More connections would deepen the tie.`;
  } else if (termHits >= 1) {
    score = 2;
    note = 'Term-of-Issue mentioned but no cross-references to other articles. Tie to siblings in the issue.';
  } else if (/\b(Anthropic|Claude)\b/.test(input.body)) {
    score = 1;
    note = 'Issue-adjacent topic but no explicit throughline to other articles or Term of Issue. Build the tie.';
  } else {
    score = 0;
    note = 'Isolated piece. "Nobody ties the week together. Shipped. is the tie." Tie this one.';
  }

  return { key: 'throughline', label: DIM_LABELS.throughline, score, letter: scoreToLetter(score), note };
}

// ────────────────────────────────────────────────────────────────────
// Dimension 7 — Voice setup
// ────────────────────────────────────────────────────────────────────

function scoreVoice(input: GraderInput): DimensionScore {
  const section = extractSection(input.body, /^##\s+Voice\s+notes(?:\s+for.*)?$/im)
    ?? extractSection(input.body, /^##\s+Voice$/im);

  let score = 0;
  let note = '';

  if (!section) {
    score = 0;
    note = 'No voice notes section. Add ## Voice notes for the distilled prose — name a STYLE.md move, list phrases to kill.';
    return { key: 'voice', label: DIM_LABELS.voice, score, letter: scoreToLetter(score), note };
  }

  const hasNamedMove = /\b(Move [ABC]|memoir.?→.?philosophy|punchline isolation|rhythm closer|memoir to philosophy)\b/i.test(section);
  const hasPattern = /\b(Pattern [123]|in medias res|stat-?first|name[- ]the[- ]invisible)\b/i.test(section);
  const hasKillMarker = /\b(forbidden|kill on sight|kill rule|do not use)\b/i.test(section);
  const killListBullets = (section.match(/^[-*]\s+["'].+["']/gm) ?? []).length;  // quoted kill items
  const totalBullets = (section.match(/^[-*]\s/gm) ?? []).length;

  if (section && (hasNamedMove || hasPattern) && hasKillMarker && (killListBullets >= 3 || totalBullets >= 4)) {
    score = 4;
    note = `Voice notes section with named move/pattern + kill list (${totalBullets} items). Draft writer has what they need.`;
  } else if (section && (hasNamedMove || hasPattern || hasKillMarker)) {
    score = 3;
    note = `Voice notes section with ${hasNamedMove ? 'a named move' : hasPattern ? 'pattern reference' : 'kill markers'}. Add the other for full credit.`;
  } else if (totalBullets >= 2) {
    score = 2;
    note = `Voice notes section with ${totalBullets} generic items. Name a specific STYLE.md move and a phrase-kill list.`;
  } else {
    score = 1;
    note = 'Voice notes section exists but nearly empty. Name the STYLE.md move, list phrases to kill.';
  }

  return { key: 'voice', label: DIM_LABELS.voice, score, letter: scoreToLetter(score), note };
}

// ────────────────────────────────────────────────────────────────────
// Helpers
// ────────────────────────────────────────────────────────────────────

function extractSection(body: string, headingPattern: RegExp): string | null {
  const lines = body.split('\n');
  let startIdx = -1;
  for (let i = 0; i < lines.length; i++) {
    if (headingPattern.test(lines[i]!)) { startIdx = i + 1; break; }
  }
  if (startIdx === -1) return null;

  let endIdx = lines.length;
  for (let i = startIdx; i < lines.length; i++) {
    if (/^##\s+/.test(lines[i]!)) { endIdx = i; break; }
  }
  return lines.slice(startIdx, endIdx).join('\n').trim();
}

function scoreToLetter(score: number): LetterGrade {
  if (score >= 4) return 'A';
  if (score >= 3) return 'B';
  if (score >= 2) return 'C';
  if (score >= 1) return 'D';
  return 'F';
}

function totalToLetter(total: number): LetterGrade {
  if (total >= 25) return 'A';
  if (total >= 21) return 'B';
  if (total >= 15) return 'C';
  if (total >= 9) return 'D';
  return 'F';
}

function letterToStatus(letter: LetterGrade): string {
  switch (letter) {
    case 'A': return 'Ship-ready';
    case 'B': return 'Solid';
    case 'C': return 'Needs work';
    case 'D': return 'Significant gaps';
    case 'F': return 'Not ready';
  }
}
