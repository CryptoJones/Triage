# Triage

A meta-scheduler that watches signals about the world and reorders its
own priority queue accordingly. The human sets the goals; Triage decides
the order.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg?logo=apache)](LICENSE)
[![Codeberg](https://img.shields.io/badge/Codeberg-CryptoJones%2FTriage-2185D0?logo=codeberg&logoColor=white)](https://codeberg.org/CryptoJones/Triage)
[![GitHub](https://img.shields.io/badge/GitHub-CryptoJones%2FTriage-181717?logo=github&logoColor=white)](https://github.com/CryptoJones/Triage)

> Mirrored on both [GitHub](https://github.com/CryptoJones/Triage) and
> [Codeberg](https://codeberg.org/CryptoJones/Triage). Issues filed on
> either are welcome; commits are pushed to both.

---

## What it does

Human-curated priority queues drift. The #3 task yesterday might be #1
today because staging is on fire, a token is about to expire, or a
$40/hr GPU pod is idle. Manually keeping a queue accurate is its own
job.

Triage closes the loop:

1. **Signal sources** push facts (cron windows, CI status, cost
   pressure, deadlines).
2. **Rules** turn facts into priority deltas.
3. **The queue reorders** on every `triage tick`.

Every reorder is explainable — `triage why <id>` shows exactly which
rules contributed which deltas.

See [`DESIGN.md`](DESIGN.md) for the architecture, signal model, and
rule catalog.

## Install

```bash
git clone https://github.com/CryptoJones/Triage
cd Triage
pip install -e .
```

Or via Codeberg:

```bash
git clone https://codeberg.org/CryptoJones/Triage
cd Triage
pip install -e .
```

Pure Python stdlib — no runtime dependencies.

## Usage

```bash
# Add tasks
triage add "Fix the auth bug" --base-score 10
triage add "Rotate the staging cert" --deadline 2026-05-20T00:00:00Z

# Inspect
triage list                    # current order
triage show <id>               # one task + active rule contributions
triage why <id>                # audit log: which rules pushed it where

# Recompute (call this from cron / a shell loop / ScheduleWakeup)
triage tick

# Cleanup
triage rm <id>
```

## Companion: TaskPriorityReorder

[claude-skill-TaskPriorityReorder](https://github.com/CryptoJones/claude-skill-TaskPriorityReorder)
is the manual override — a Claude Code skill that re-orders the queue
when a human says "bump X to top". Triage is the automatic version.
They share the same primitive: stable identity per task plus a
recomputable priority.

## License

Apache 2.0. See [LICENSE](LICENSE).

Proudly Made in Nebraska. Go Big Red! 🌽 https://xkcd.com/2347/
