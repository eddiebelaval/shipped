/**
 * Shipped. — the frontier-labs beat.
 *
 * The publication's source list. Shipped. tracks what the AI labs ship; this
 * is the set of X feeds the scraper sweeps each run. Anthropic stays the
 * anchor (tier: 'anchor'); the other frontier labs are tracked so quiet days
 * on one lab are not thin days for the reader.
 *
 * Each feed scrapes into its own output dir: output/x-{handle}/. The
 * Editor-in-Chief reads across all of them at SWEEP and decides what earns a
 * Dig (see content/DAILY.md). Adding a lab is one line here.
 *
 * Handles are the public dev/release feeds where each is most active. Tune
 * freely — the pipeline reads this list, nothing is hardcoded downstream.
 */

export type LabTier = 'anchor' | 'frontier'

export interface BeatSource {
  /** Lab / org name as it appears in copy. */
  lab: string
  /** X handle without the leading @. Output lands in output/x-{handle}/. */
  handle: string
  /** anchor = Anthropic (the spine); frontier = a tracked peer lab. */
  tier: LabTier
}

/**
 * The beat, newest-priority first. The anchor is swept first so it always
 * sets the lead; frontier labs add tension and volume.
 */
export const BEAT_SOURCES: BeatSource[] = [
  { lab: 'Anthropic', handle: 'claudedevs', tier: 'anchor' },
  { lab: 'Anthropic', handle: 'AnthropicAI', tier: 'anchor' },
  { lab: 'OpenAI', handle: 'OpenAIDevs', tier: 'frontier' },
  { lab: 'OpenAI', handle: 'OpenAI', tier: 'frontier' },
  { lab: 'Google DeepMind', handle: 'GoogleDeepMind', tier: 'frontier' },
  { lab: 'Meta AI', handle: 'AIatMeta', tier: 'frontier' },
  { lab: 'Mistral', handle: 'MistralAI', tier: 'frontier' },
  { lab: 'xAI', handle: 'xai', tier: 'frontier' },
]

/** Just the handles, in sweep order. */
export function beatHandles(): string[] {
  return BEAT_SOURCES.map((s) => s.handle)
}

/**
 * Lab → the terms the X MCP enrichment sweep searches for. A timeline pull
 * only sees a lab's own posts; the search sweep widens the net to everyone
 * talking about the lab's products, which is the cross-lab / third-party
 * signal the front-of-book digs against thin issues (content/DAILY.md).
 */
const LAB_SEARCH_TERMS: Record<string, string[]> = {
  Anthropic: ['Anthropic', 'Claude'],
  OpenAI: ['OpenAI', 'ChatGPT'],
  'Google DeepMind': ['Google DeepMind', 'Gemini'],
  'Meta AI': ['Meta AI', 'Llama'],
  Mistral: ['Mistral'],
  xAI: ['xAI', 'Grok'],
}

/**
 * Search terms for a feed handle, derived from its lab on the beat. Falls back
 * to the bare handle for anything not on the beat. Used by the scraper's
 * `--enrich` sweep when no explicit `--search` terms are given.
 */
export function searchTermsForHandle(handle: string): string[] {
  const src = BEAT_SOURCES.find(
    (s) => s.handle.toLowerCase() === handle.replace(/^@/, '').toLowerCase(),
  )
  if (!src) return [handle.replace(/^@/, '')]
  return LAB_SEARCH_TERMS[src.lab] ?? [src.lab]
}
