// ──────────────────────────────────────────────────────────────────────────────
// Shipped. subscriber endpoint
// Deploy to:  id8labs/api/newsletter/subscribe.ts
// Runtime:    Vercel Edge (V8 isolate — Web APIs: fetch, atob, btoa, Request, Response)
// Env var:    GITHUB_TOKEN
//   A GitHub fine-grained PAT scoped to eddiebelaval/shipped, Contents: Read+Write.
//   Add it in Vercel → Settings → Environment Variables.
// ──────────────────────────────────────────────────────────────────────────────

export const config = { runtime: 'edge' };

const REPO    = 'eddiebelaval/shipped';
const FILE    = 'pipeline/recipients.json';
const GH_API  = 'https://api.github.com';
const ORIGINS = ['https://id8labs.app', 'https://eddiebelaval.github.io'];
const CADENCES = new Set(['nightly', 'weekly', 'monthly']);

// ── helpers ──────────────────────────────────────────────────────────────────

function corsHeaders(origin: string): Record<string, string> {
  const allowed = ORIGINS.some(o => origin === o || origin.startsWith(o + '/'));
  if (!allowed) return {};
  return {
    'Access-Control-Allow-Origin': origin,
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };
}

function json(body: unknown, status = 200, extra: Record<string, string> = {}): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json', ...extra },
  });
}

// ── handler ──────────────────────────────────────────────────────────────────

export default async function handler(req: Request): Promise<Response> {
  const origin = req.headers.get('origin') ?? '';
  const cors = corsHeaders(origin);

  if (req.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors });
  if (req.method !== 'POST') return json({ error: 'Method not allowed' }, 405, cors);

  // Parse body
  let body: Record<string, unknown>;
  try { body = await req.json(); }
  catch { return json({ error: 'Invalid JSON' }, 400, cors); }

  // Validate + sanitize email
  const email = String(body.email ?? '').toLowerCase().trim();
  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return json({ error: 'Valid email required.' }, 400, cors);
  }

  // Sanitize name (optional — fall back to local-part of email)
  const name = String(body.name ?? '').trim().slice(0, 120) || email.split('@')[0];

  // Sanitize cadences — must be subset of the allowed set
  const rawCadences = Array.isArray(body.cadences) ? body.cadences : ['nightly', 'weekly'];
  const cadences = (rawCadences as unknown[])
    .filter((c): c is string => typeof c === 'string' && CADENCES.has(c));
  if (!cadences.length) cadences.push('nightly', 'weekly');

  const token = process.env.GITHUB_TOKEN;
  if (!token) return json({ error: 'Server configuration error.' }, 500, cors);

  const ghHeaders = {
    Authorization: `token ${token}`,
    Accept: 'application/vnd.github.v3+json',
    'User-Agent': 'shipped-subscribe/1.0',
  };

  // Read current recipients.json from GitHub
  const fileRes = await fetch(`${GH_API}/repos/${REPO}/contents/${FILE}`, { headers: ghHeaders });
  if (!fileRes.ok) return json({ error: 'Could not read distribution list.' }, 502, cors);

  const fileData = await fileRes.json() as { content: string; sha: string };
  const list = JSON.parse(atob(fileData.content.replace(/\n/g, '')));

  // Deduplicate — return 200 so the UI can show a friendly "already subscribed" message
  if ((list.recipients as Array<{ email: string }>).some(r => r.email.toLowerCase() === email)) {
    return json({ ok: true, alreadySubscribed: true }, 200, cors);
  }

  // Append new subscriber
  list.recipients.push({
    name,
    email,
    cadences,
    subscribed: new Date().toISOString().slice(0, 10),
  });
  list.updated = new Date().toISOString().slice(0, 10);

  // Write back via GitHub Contents API
  // If two requests race on the same SHA, GitHub returns 409 and the second caller
  // gets a 502 with "Try again" — rare enough not to warrant a retry loop here.
  const newContent = btoa(JSON.stringify(list, null, 2) + '\n');
  const writeRes = await fetch(`${GH_API}/repos/${REPO}/contents/${FILE}`, {
    method: 'PUT',
    headers: { ...ghHeaders, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message: `chore(subscribers): add ${email}`,
      content: newContent,
      sha: fileData.sha,
    }),
  });

  if (!writeRes.ok) {
    const errData = await writeRes.json().catch(() => ({})) as { message?: string };
    return json({ error: errData.message ?? 'Could not save subscription.' }, 502, cors);
  }

  return json({ ok: true }, 200, cors);
}
