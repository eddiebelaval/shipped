# The Command Index

A living, self-updating reference of **every slash command available in this
Claude Code install** — rendered in Shipped.'s design language as a permanent
back-of-book reference. Built because Anthropic keeps shipping new commands and
the install surface (built-ins + plugins + custom) is too large to track by hand.

## What it indexes — three streams

| Stream | Source | Subtypes | Keeps up via |
|---|---|---|---|
| **Built-in** | `builtins.json` (seeded from [code.claude.com/docs/en/commands](https://code.claude.com/docs/en/commands)) | command, bundled skill | weekly `/schedule` routine (`refresh-builtins.md`) |
| **Plugin** | `~/.claude/plugins/cache/` (installed only) | plugin command, plugin skill, by marketplace | weekly `update.sh` scan |
| **Custom** | `~/.claude/commands/` + `~/.claude/skills/` | command, skill | weekly `update.sh` scan |

It indexes what is **installed/available**, not the browsable marketplace
catalog (which is mostly uninstalled community templates).

## Files

```
builtins.json          Anthropic built-in commands + bundled skills (the data
                       file the intelligence routine maintains).
generate.py            Deterministic generator: scans local install, merges
                       builtins.json, renders command-index.html + .json.
update.sh              Weekly cron entry: re-scan + re-render, mirror to deploy.
refresh-builtins.md    Prompt for the weekly /schedule routine that reconciles
                       builtins.json against Anthropic's live docs + changelog.
com.id8labs.shipped-command-index.plist   launchd job (Fri 08:40) for update.sh.
output/                command-index.html (the page) + command-index.json (data).
```

## Run it by hand

```bash
python3 generate.py --out ./output      # render
open output/command-index.html          # view
bash update.sh                          # full weekly refresh + deploy mirror
```

## The two-layer "keeps up forever" design

- **Deterministic layer** (`update.sh`, launchd, weekly): scans files. Catches
  every new plugin or custom command/skill the moment it lands on disk. Free,
  no network, no LLM.
- **Intelligence layer** (`refresh-builtins.md`, `/schedule`, weekly): the only
  part that needs judgment + web. Anthropic's built-ins aren't files — they live
  in the CLI binary and are only documented online. The routine reads the docs +
  changelog, diffs `builtins.json`, and adds/removes/edits as Anthropic ships.

Neither layer commits or pushes. Staging is human-gated (Shipped invariant #1).

## Ties to the Shipped ecosystem

- Lives in the Shipped repo, rendered in the Shipped design system (Fraunces /
  Archivo / JetBrains Mono, warm paper, orange period, grain).
- Linked from the archive index as a standing reference.
- Same cadence as the Friday ship window. Shipped is the magazine on what
  Anthropic ships; this is its command-line companion.
