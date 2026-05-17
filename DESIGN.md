# Triage — Design

A meta-scheduler that watches signals about the world and reorders its
own priority queue accordingly. Tasks are not just first-come-first-served
or human-tagged; they get continuously reweighted as the environment
around them changes.

---

## Why this exists

Human-curated priority queues drift. The thing you ranked as #3 yesterday
might be #1 today because the staging cluster is on fire, a token is
about to expire, or a $40/hr GPU pod is sitting idle. Manually keeping
the queue accurate is itself work, and the tax compounds with the queue's
size.

Triage closes the loop: signal sources push facts, scoring rules turn
those facts into priority deltas, and the queue is reordered on every
tick. The human sets the **goals**; Triage decides the **order**.

The companion skill [TaskPriorityReorder](https://github.com/CryptoJones/claude-skill-TaskPriorityReorder)
is the manual override. Triage is the automatic version. They share the
same primitive: a stable identity per task plus a recomputable priority.

---

## Concepts

### Task

A unit of work with stable identity. Minimum fields:

| Field         | Type            | Purpose                                              |
|---------------|-----------------|------------------------------------------------------|
| `id`          | string (uuid)   | Stable identity across reorders                      |
| `subject`     | string          | One-line summary                                     |
| `description` | string          | Full body (markdown OK)                              |
| `created_at`  | ISO 8601        | When it entered the queue                            |
| `base_score`  | int             | Human-set baseline weight (default 0)                |
| `tags`        | list[string]    | Signal-source filters can scope to tags              |
| `deadline`    | ISO 8601 \| null | If set, time-decay signals will apply               |
| `blocked_by`  | list[task-id]   | Dependency edges (transitive priority bumps)         |

### Signal

A fact about the world that affects scoring. Each signal carries:

```python
@dataclass
class Signal:
    source: str            # "cron", "github-ci", "runpod-cost", ...
    captured_at: datetime
    payload: dict          # source-specific
    affects: list[str]     # task ids this signal applies to ([] = all)
```

Signals are append-only into a per-source ring buffer with a TTL. Old
signals expire and stop counting.

### Rule

A pure function: `(task, list[active_signals]) -> int_delta`. Rules
compose additively. Each rule has a stable name so its contribution is
auditable.

Built-in rules for v0.1:

- `base_score`: identity (returns `task.base_score`)
- `deadline_decay`: if `task.deadline` is set, returns
  `clamp(deadline_pressure(remaining_time), 0, 100)`. As deadline
  approaches, the bump grows.
- `blocker_transitive`: enforces the invariant `priority(blocker) >=
  priority(blocked) + 1`. If A is `blocked_by` B, B's priority is
  raised (not A's) to at least one above A's — because in queue order
  B must be worked first. Implemented as a post-scoring reverse-topo
  pass in the scheduler, not a per-task rule. Cycles in the
  `blocked_by` graph are detected and broken via DFS back-edge removal
  (deterministic by lex-sorted source-id traversal); each removed edge
  emits a warning. Self-loops and dangling blocker ids also produce
  warnings and are ignored.

Future rules:

- `stale_pr`: if a `github-pr` signal reports a PR sitting unreviewed
  for >24h, +20.

### Shipped in v0.3

- `ci_failing`: +50 when a fresh `github-ci` signal targeting the task
  reports `state == "failure"`. The companion signal source
  `triage.sources.github_ci` polls GitHub Actions for tasks tagged
  `gh-ci:owner/repo@branch` and emits one signal per matching task.
  Invoked manually via `triage poll github-ci` (not auto-emitted on
  `triage tick` because it's network-bound).

### Shipped in v0.5

- `cost_pressure`: bump tasks tagged for a paid pod that's currently
  running. +100 when state == 'idle' (uptime > 10 min AND avg GPU
  util < 10% — drain it now); +25 when state == 'running' (utilization
  unknown or above threshold — softer reminder). The companion source
  `triage.sources.runpod` polls the RunPod GraphQL API for tasks
  tagged `runpod:<pod-id>` and emits one signal per pod. Invoked
  manually via `triage poll runpod-cost`. Requires `RUNPOD_API_KEY`
  in env (or explicit token).

### Priority

`priority(task) = sum(rule(task, signals) for rule in rules)`. Higher =
top of queue. Reordering happens on every tick.

---

## Architecture

```
                 +--------------------+
   signals  ---> |  Signal Sources    |  (one process per source)
                 +--------------------+
                          |
                          v
                 +--------------------+
                 |  ~/.triage/state/  |  (append-only JSONL per source)
                 +--------------------+
                          ^
                          |
   tick     ----> +--------------------+  ----> reordered queue
                  |  Triage Scheduler  |        (printed / served)
                  +--------------------+
                          ^
                          |
   tasks    ----> +--------------------+
                  |   triage CLI       |
                  +--------------------+
```

All state on disk. No daemon required for v0.1 — `triage tick` is
idempotent and can be run from cron / a shell loop / Claude Code's
ScheduleWakeup. Signal sources are independent processes (or simple
shell scripts that append JSON lines) so anyone can write an adapter.

### File layout

```
~/.triage/
    tasks.json              # the queue itself (rewritten atomically on every change)
    state/
        cron.jsonl          # signals from time-based source
        github-ci.jsonl     # signals from CI poller (v0.2)
        runpod-cost.jsonl   # signals from RunPod poller (v0.3)
        ...
    config.toml             # source TTLs, rule weights, optional
```

### CLI surface

```
triage add "subject" [--description ...] [--base-score N] [--deadline ISO] [--tag T] [--blocked-by ID]
triage list                                 # current queue, ordered
triage show ID                              # one task + its current rule contributions
triage tick                                 # recompute priorities; print new order
triage signal SOURCE [--affects ID] PAYLOAD # write a signal (mostly for adapters)
triage rm ID
triage why ID                               # audit log: which rules contributed what
```

`triage why` is the killer accountability feature — every reorder is
explainable.

---

## v0.1 scope (this repo, today)

- File-backed state (atomic write via temp + rename).
- Tasks model + serialization.
- One signal source: **cron-window**. Tasks can opt in to a recurring
  active window (e.g. "this task is high-priority weekdays 9-5"). The
  cron source emits a signal when the window is currently active.
- Three built-in rules: `base_score`, `deadline_decay`,
  `cron_window_active`.
- `triage add | list | show | tick | rm | why` CLI verbs.
- Pure Python stdlib (no deps).
- 100% deterministic given inputs → property-based tests possible.

## Internationalization (i18n)

Shipped in v0.9 (foundation) and v0.10 (complete, 17 locales).

### Why dict-based catalogs instead of gettext

- **No build step.** Each locale is a plain Python module
  (`src/triage/locales/<code>.py`) that contributors edit directly.
  No `msgfmt`, no `.mo` compilation, no `babel`/`pybabel` runtime.
- **English fallback on miss.** `_(msgid)` returns the locale's
  translation if present, or the English msgid itself if absent —
  so a partial translation never breaks the CLI.
- **Stdlib only.** Matches the project's stdlib-only invariant.

### The `_()` lookup

```python
from triage.i18n import _
_("rank {n}", n=5)  # -> "rank 5" / "rango 5" / "rang 5" / ...
```

`_(msgid, **fmt)` is the runtime translation primitive. `msgid` is
the canonical English source string. `**fmt` are named-placeholder
kwargs applied via `str.format`. A missing key falls back to msgid
silently (visible only when `TRIAGE_I18N_DEBUG=1`).

### Resolution precedence

`triage.i18n.resolve_lang` picks the active locale via, in order:

1. `--lang LANG` CLI flag.
2. `$TRIAGE_LANG`.
3. `$LC_ALL` / `$LC_MESSAGES` / `$LANG` (first hit, stripped to the
   two-letter ISO 639-1 code; `C`/`POSIX` ignored).
4. `locale.getlocale()` — picked up since v0.10. Wrapped in
   try/except because some installs raise `ValueError`, and freshly-
   initialized processes can return `(None, None)`.
5. `DEFAULT_LANG` (= `en`).

Unknown codes at any level fall through to the next; the chain is
intentionally fail-safe so a misspelled env var becomes "use the next
source," never a crash.

### Adding a new locale

The 4-step recipe (also in `src/triage/locales/__init__.py`):

1. Copy `en.py` to `<iso639-1>.py`.
2. Translate every value in `STRINGS`. Set `__native_name__` to the
   language's name in its own script (e.g. `"Español"`, `"Türkçe"`).
3. Add an `import` line + `LOCALES` entry in `__init__.py`.
4. Run `pytest` and `triage lang --check` — both will catch missing
   keys or placeholder mismatches.

### The release gate

`triage lang --check` audits every non-English locale against the
English baseline and reports:

- **missing keys** — present in `en.STRINGS`, absent in `<lang>.STRINGS`.
- **extra keys** — present in `<lang>.STRINGS`, absent from `en`.
- **placeholder mismatches** — e.g. `{tasks}` in en but `{tareas}`
  in es. Names must line up exactly because they're passed as kwargs.

Exit code is 1 if any drift is found, 0 otherwise — runnable as a
release gate in both the GitHub Actions and Codeberg Woodpecker
pipelines.

### Known constraint: smart quotes in Python literals

A typographic right-quote `"` (U+201D) inside a Python `"..."`
string literal terminates the string early. Several translations
use typographic quotation marks around English-as-foreign-word
literals like `'en'`. **Use ASCII apostrophes (`'`) for those
literals** to avoid the parser bug — and a translator running
`triage lang --check` won't even notice the substitution because
the rendered output stays readable.

---

## Roadmap

| Version | Feature                                                       | Status   |
|---------|---------------------------------------------------------------|----------|
| v0.1    | scaffold, three rules, cron-window signal, CLI                | shipped  |
| v0.2    | `blocker_transitive` propagation + cycle detection            | shipped  |
| v0.3    | `github-ci` signal source + `ci_failing` rule + `triage poll` | shipped  |
| v0.4    | BBS-style ANSI theme system + `triage theme` subcommand       | shipped  |
| v0.5    | `runpod-cost` signal source + `cost_pressure` rule            | shipped  |
| v0.6    | JSONL event log writer for external agents                    | shipped  |
| v0.7    | `github-pr` stale-PR signal source + `stale_pr` rule          | shipped  |
| v0.8    | `triage signal` CLI + `manual_bump` rule + RunPodBoss eval    | shipped  |
| v0.8.1  | `triage status` one-screen at-a-glance summary                | shipped  |
| v0.9    | i18n foundation — `--lang` flag + en/es/fr baseline           | shipped  |
| v0.10   | i18n complete — 17 locales + `triage lang --check` regression detector | shipped  |
| v0.11   | Post-i18n polish — `locale.getlocale()` fallback, `lang --json`, CI gate, model-layer `_()`, status version stamp | shipped  |
| —       | Claude Code `triage` skill (in `claude_skill-Triage` repo)    | planned  |
| —       | Long-running mode (`triage watch`) + systemd unit             | planned  |

---

## Design tenets

1. **Reorders are explainable.** Every priority change must trace back
   to one or more named rule contributions. No black boxes.
2. **Signals expire.** A failing CI run from 3 days ago shouldn't still
   be pinning a task at #1. Every source declares a TTL.
3. **The human's tag beats the machine's signal.** Base score is
   additive on top of computed delta; a human-pinned task can always be
   forced to the top with a large base score.
4. **Stateless invocations.** `triage tick` reads state, computes,
   writes. No in-memory caches that diverge from disk. Crash-safe by
   construction.
5. **Stdlib only.** Same constraint as
   [correcthorsebatterystaple](https://github.com/CryptoJones/correcthorsebatterystaple) —
   easier to vendor into other projects, easier to audit.
6. **The skill stays manual.** TaskPriorityReorder remains the
   human-driven path. Triage doesn't replace it; it informs it.

---

Proudly Made in Nebraska. Go Big Red! 🌽 https://xkcd.com/2347/
