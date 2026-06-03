# Refresh the Anthropic built-ins — weekly intelligence routine

This is the prompt for the scheduled Claude routine that keeps the **Built-in**
stream of The Command Index current. Anthropic ships new Claude Code slash
commands with most CLI releases ("they keep coming") — this routine is the only
part of the system that needs judgment + network, so it runs as a `/schedule`
routine, not a dumb cron. The deterministic local scan (`update.sh`) handles
plugins and custom commands without any of this.

## How to install it (one time)

In an interactive Claude Code session, run `/schedule` and create a weekly
routine (Friday ~08:20 ET, just before `update.sh`'s 08:40 render) with the
prompt body below. Or paste the body into a new routine via the schedule skill.

## Cadence

Weekly. If nothing changed upstream, it's a ~30-second no-op that costs almost
nothing. The value is catching the week Anthropic adds `/whatever-is-next`.

## Routine prompt (copy verbatim into the routine)

> You maintain the Anthropic built-in slash-command list for id8Labs' "Command
> Index" reference. The data file is:
> `~/Development/id8/shipped/pipeline/scripts/command-index/builtins.json`
>
> Do this:
> 1. WebFetch `https://code.claude.com/docs/en/commands` and extract every
>    built-in slash command and bundled skill: the `/name` and a one-sentence
>    purpose. (Follow the redirect from docs.anthropic.com if needed.)
> 2. WebFetch the Claude Code changelog
>    `https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md`
>    and note any commands ADDED or REMOVED since the `fetched` date in the
>    file's `_meta`.
> 3. Read the current `builtins.json`. Diff the live set against it:
>    - NEW commands on the docs page that aren't in the file → add them, with an
>      accurate one-line `desc`, a sensible `category` (reuse an existing one
>      from the file; only invent a new category if nothing fits), and
>      `subtype` ("skill" if the docs label it a Skill/Workflow, else "command").
>    - Commands marked Removed/deprecated in the docs or changelog → delete them.
>    - Descriptions that changed materially upstream → update them.
> 4. Update `_meta.fetched` to today's date and `_meta.claude_version_at_fetch`
>    to the output of `claude --version`.
> 5. Keep the JSON valid and the existing formatting/ordering style. Do NOT
>    touch the plugin or custom streams — those are scanned live by update.sh.
> 6. Re-render by running:
>    `python3 ~/Development/id8/shipped/pipeline/scripts/command-index/generate.py --out ~/Development/id8/shipped/pipeline/output`
> 7. If anything changed, write a one-line summary to
>    `~/Development/id8/FIELD_NOTES.md` (past tense, dated): which commands were
>    added/removed. If nothing changed, do nothing and report "no upstream
>    change".
> 8. Do NOT git commit or push. Staging/shipping is human-gated (Shipped
>    invariant #1). Leave the working tree for Eddie to review and push.
>
> Verification before you finish: `python3 -c "import json;
> json.load(open('~/Development/id8/shipped/pipeline/scripts/command-index/builtins.json'.replace('~','$HOME')))"`
> must succeed, and the generate.py run must exit 0. Report the new totals line.

## Why a routine and not a cron

The cron (`update.sh`) is deterministic: scan files, render. It cannot discover
a brand-new Anthropic command, because the built-ins aren't files on disk — they
live inside the Claude Code binary and are only documented on the web. Reading a
web page, judging what's genuinely new vs. a reworded description, and writing a
correct category/subtype is model work. So the two layers split cleanly:

| Layer        | Tool                    | Tracks                                   |
|--------------|-------------------------|------------------------------------------|
| Deterministic| `update.sh` (launchd)   | plugin commands+skills, custom commands+skills |
| Intelligence | this routine (`/schedule`)| Anthropic built-ins as they ship        |
