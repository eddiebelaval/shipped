#!/usr/bin/env node
// Shipped. recipient sync — Supabase shipped list -> local recipients.json.
//
// Single source of truth is the Supabase `newsletter_subscribers` table:
// anyone active and on the `shipped` list (web form, CLI, Telegram) becomes a
// recipient. This refreshes ~/.shipped-distribution/recipients.json, which
// distribute-local.py reads at 22:45 (it prefers this local file, falling back
// to git origin/main for backward compatibility).
//
// Email-only today: every shipped subscriber gets all three cadences. Phone is
// stored on the row but not used here (the launcher drafts email via Mail.app).
//
// Preserves `send_mode` ("draft" | "off") and `from` from any existing
// recipients.json so operator settings survive a sync.
//
// Reads SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY from the id8labs app env.

import fs from 'fs'
import os from 'os'
import path from 'path'

const ENV_PATH = path.join(os.homedir(), 'Development/id8/id8labs/.env.local')
const OUT_PATH = path.join(os.homedir(), '.shipped-distribution/recipients.json')
const CADENCES = ['nightly', 'weekly', 'monthly']

function loadEnv(p) {
  const out = {}
  for (const line of fs.readFileSync(p, 'utf8').split('\n')) {
    const i = line.indexOf('=')
    if (i === -1 || line.trim().startsWith('#')) continue
    out[line.slice(0, i).trim()] =
      line.slice(i + 1).trim().replace(/^"|"$/g, '').replace(/\\n$/, '')
  }
  return out
}

function readExisting() {
  try { return JSON.parse(fs.readFileSync(OUT_PATH, 'utf8')) } catch { return {} }
}

async function main() {
  const env = loadEnv(ENV_PATH)
  const url = env.SUPABASE_URL || env.NEXT_PUBLIC_SUPABASE_URL
  const key = env.SUPABASE_SERVICE_ROLE_KEY
  if (!url || !key) throw new Error('Missing SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY')

  // active subscribers whose lists array contains 'shipped'
  const q = `${url}/rest/v1/newsletter_subscribers`
    + `?select=email&status=eq.active&lists=cs.%7Bshipped%7D&order=email`
  const res = await fetch(q, { headers: { apikey: key, Authorization: `Bearer ${key}` } })
  if (res.status >= 400) throw new Error(`${res.status}: ${await res.text()}`)
  const rows = await res.json()

  const seen = new Set()
  const recipients = []
  for (const r of rows) {
    const email = (r.email || '').toLowerCase().trim()
    if (!email || seen.has(email)) continue
    seen.add(email)
    recipients.push({ email, cadences: CADENCES })
  }

  const prev = readExisting()
  const out = {
    send_mode: prev.send_mode || 'draft',
    from: prev.from || 'eb@id8labs.tech',
    generated_at: new Date().toISOString(),
    source: 'supabase:newsletter_subscribers(lists@>shipped,active)',
    count: recipients.length,
    recipients,
  }
  fs.writeFileSync(OUT_PATH, JSON.stringify(out, null, 2) + '\n')
  console.log(`synced ${recipients.length} Shipped. recipient(s) -> ${OUT_PATH} (send_mode=${out.send_mode})`)
}

main().catch((e) => { console.error('sync-recipients failed:', e.message); process.exit(1) })
