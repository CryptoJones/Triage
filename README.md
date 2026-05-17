<div align="center">

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                    T  R  I  A  G  E                          ║
║                                                              ║
║          meta-scheduler that watches its own queue           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**A self-aware priority queue.** Signals push facts about the world;
rules turn facts into priority deltas; the queue reorders itself on
every tick. You set the goals — Triage decides the order, and tells
you exactly why.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg?logo=apache)](LICENSE)
[![Stdlib only](https://img.shields.io/badge/deps-stdlib_only-success?logo=python&logoColor=white)](pyproject.toml)
[![Codeberg](https://img.shields.io/badge/Codeberg-CryptoJones%2FTriage-2185D0?logo=codeberg&logoColor=white)](https://codeberg.org/CryptoJones/Triage)
[![GitHub](https://img.shields.io/badge/GitHub-CryptoJones%2FTriage-181717?logo=github&logoColor=white)](https://github.com/CryptoJones/Triage)

**Read this in:** **English** ·
[Español](README.es.md) ·
[Français](README.fr.md) ·
[Deutsch](README.de.md) ·
[Italiano](README.it.md) ·
[Português](README.pt.md) ·
[Nederlands](README.nl.md) ·
[Polski](README.pl.md) ·
[Čeština](README.cs.md) ·
[Svenska](README.sv.md) ·
[Norsk](README.no.md) ·
[Dansk](README.da.md) ·
[Suomi](README.fi.md) ·
[Română](README.ro.md) ·
[Magyar](README.hu.md) ·
[Türkçe](README.tr.md)

</div>

> Mirrored on both [GitHub](https://github.com/CryptoJones/Triage) and
> [Codeberg](https://codeberg.org/CryptoJones/Triage). Issues filed on
> either forge are welcome; commits land on both.

---

## What you see

```
╔════════════════════════════════════════════════════════╗
║                  T R I A G E   v0.4.0                  ║
╚════════════════════════════════════════════════════════╝
  ID               PRI  BAR    SUBJECT
  ════════════  ══════  ═════  ════════════════════════════════════════
  7cfa440bc639  [ 101]  █████  Fix the linter        ← blocker auto-bumped
  f35d7cea6b7d  [ 100]  █████  Add feature X         ← blocked-by linter
  19c80b807ddd  [  35]  █▒░░░  Rotate cert           ← deadline pressure
  abc123456789  [   2]  ░░░░░  Routine cleanup
```

In a real terminal the banner is bright magenta, the priorities are
color-banded (high = yellow, mid = green, low = dim cyan), and the
priority bars fill in proportionally. The default `bbs` theme is
unapologetically 1990s.

---

## How it works

```
                   ┌─────────────────────┐
   signals  ─────► │   Signal sources    │  (cron-window, github-ci, ...)
                   └──────────┬──────────┘
                              ▼
                   ┌─────────────────────┐
                   │  ~/.triage/state/   │  (append-only JSONL per source)
                   └──────────┬──────────┘
                              ▼
   tick     ─────► ┌─────────────────────┐ ─────► reordered queue
                   │  Triage scheduler   │        + per-task audit log
                   └──────────┬──────────┘
                              ▼
                   ┌─────────────────────┐
   tasks    ─────► │     triage CLI      │
                   └─────────────────────┘
```

1. **Signal sources** push facts (`cron-window`, `github-ci`, future
   `runpod-cost`, `github-pr`...).
2. **Rules** turn facts into priority deltas
   (`base_score`, `deadline_decay`, `cron_window_active`,
   `ci_failing`, `blocker_transitive`).
3. **The queue reorders** on every `triage tick`.
4. **Every reorder is explainable** — `triage why <id>` shows
   exactly which rules contributed which deltas, so the order is
   never a black box.

See [`DESIGN.md`](DESIGN.md) for the full architecture, the rule
catalog, and the roadmap.

---

## Install

```bash
git clone https://github.com/CryptoJones/Triage      # or codeberg.org/CryptoJones/Triage
cd Triage
pip install -e .
```

Pure Python stdlib. No runtime dependencies. Tested on 3.10 / 3.11 / 3.12.

---

## Usage

### Tasks

```bash
triage add "Fix the auth bug" --base-score 10
triage add "Rotate the staging cert" --deadline 2026-05-20T00:00:00Z
triage add "Weekday-only chore" --cron-window "* 9-17 * * 1-5"
triage add "Watch CI"          --tag "gh-ci:CryptoJones/Triage@main"
triage add "Wait on linter"    --blocked-by <linter-task-id>

triage list                     # current priority order
triage show <id>                # the raw task record (JSON)
triage why  <id>                # which rules contributed which deltas
triage rm   <id>                # remove
```

### Reorder + poll

```bash
triage tick                     # recompute priorities; print new order
triage poll github-ci           # invoke a network-bound signal source
```

`tick` is cheap, local, and idempotent — call it from cron, a shell
loop, or Claude Code's `ScheduleWakeup`. `poll` is for signal sources
that hit the network (you pay for those explicitly).

### Event log (for external agents)

Every CLI invocation appends a single JSON line to a log file so an
external agent can `tail -f` and parse Triage's behavior:

```bash
tail -f /var/log/triage.log | jq .   # if the file is owned by your user
```

Sample entries:

```json
{"ts":"2026-05-16T06:16:18+00:00","event":"add","task_id":"9e8040d267d9","subject":"Investigate slow query","base_score":10,"tags":[],"deadline":null,"blocked_by":[]}
{"ts":"2026-05-16T06:16:18+00:00","event":"tick","ranked_count":2,"emitted_cron_signals":0,"top":[{"id":"ad2006db3c12","priority":35,"subject":"Rotate cert"},...],"warnings":[]}
{"ts":"2026-05-16T06:16:19+00:00","event":"poll","source":"github-ci","emitted":1,"warnings":[]}
{"ts":"2026-05-16T06:16:20+00:00","event":"rm","task_id":"9e8040d267d9"}
```

Configuration:

| Mechanism                  | What it does                                                     |
|----------------------------|------------------------------------------------------------------|
| `--log-file PATH` flag     | Per-invocation log path.                                         |
| `TRIAGE_LOG_FILE=PATH` env | Per-shell log path.                                              |
| Default                    | `/var/log/triage.log`. Falls back to `~/.triage/triage.log` if `/var/log` isn't writable (warns once on stderr). |
| `--no-log` flag            | Disable logging for this invocation.                             |
| `TRIAGE_NO_LOG=1` env      | Disable logging globally for the shell.                          |

To use the standard `/var/log` path without sudo on every call:

```bash
sudo touch /var/log/triage.log
sudo chown $(id -un):$(id -gn) /var/log/triage.log
```

Logging is a strict one-way side channel — errors during write are
swallowed so the CLI's primary behavior is never disrupted.

### Themes

```bash
triage theme                    # list available themes
triage theme --name bbs         # render sample rows
triage --theme modern list      # one-shot theme override
TRIAGE_THEME=mono triage list   # per-shell theme
```

| Theme    | Aesthetic                                                              |
|----------|------------------------------------------------------------------------|
| `bbs`    | **Default.** 1990s BBS: bright magenta, double-line box (`╔═╗`), block bars. |
| `modern` | Subtle palette, single-line boxes (`┌─┐`), dot-fill bars (`█▒·`).    |
| `mono`   | No color, ASCII-only (`+-+`, `#=.`) — safe for pipes / dumb terminals. |

Color follows the standards:

- Auto-disabled when stdout isn't a TTY.
- `NO_COLOR=1` disables color (per [no-color.org](https://no-color.org/)).
- `FORCE_COLOR=1` enables color on non-TTY.
- `--no-color` flag = explicit per-invocation kill switch.

---

## Related projects

Triage is one piece of a small ecosystem. The pieces compose:

| Repo | Role |
|------|------|
| [**claude_skill-Triage**](https://github.com/CryptoJones/claude_skill-Triage) | Claude Code skills repo. Ships `TaskPriorityReorder` (**manual override** — "bump X to top") today; will host the `triage` skill (**signal-driven recommender** — "what should I do next?") in a future release. |
| [**TriageMCP**](https://github.com/CryptoJones/TriageMCP) | **MCP server** wrapping Triage's API for AI agents. Eight tools (`list_tasks`, `add_task`, `tick`, `why_task`, `status`, `remove_task`, `inject_signal`, `get_task`) over stdio. Drop it into `~/.claude/mcp.json` and an agent can read + write your priority queue directly. |
| [**RunPodBoss**](https://github.com/CryptoJones/RunPodBoss) | Credit-balance guardrail for RunPod. Integrates with Triage via `extra_notify_command` — when a billing threshold trips, RunPodBoss pushes a manual signal into Triage so the "drain idle pods" task floats to the top of your queue. Setup recipe in [`docs/runpodboss-integration.md`](docs/runpodboss-integration.md). |

All four share Triage's stable-id-plus-recomputable-priority primitive
and live on dual mirrors (GitHub + Codeberg).

---

## Status

| Version | Feature                                                       | Status   |
|---------|---------------------------------------------------------------|----------|
| v0.1    | scaffold, three rules, cron-window signal, CLI                | shipped  |
| v0.2    | `blocker_transitive` propagation + cycle detection            | shipped  |
| v0.3    | `github-ci` signal source + `ci_failing` rule + `triage poll` | shipped  |
| v0.4    | BBS-style ANSI theme system + `triage theme` subcommand       | shipped  |
| v0.5    | `runpod-cost` signal source + `cost_pressure` rule            | shipped  |
| v0.6    | JSONL event log writer for external agents                    | shipped  |
| v0.7    | `github-pr` stale-PR signal source                            | planned  |
| v0.8    | Claude Code `triage` skill (in `claude_skill-Triage` repo)    | planned  |
| v0.9    | `triage watch` long-running mode + systemd unit               | planned  |

---

## License

Apache 2.0. See [LICENSE](LICENSE).

Proudly Made in Nebraska. Go Big Red! 🌽 https://xkcd.com/2347/
