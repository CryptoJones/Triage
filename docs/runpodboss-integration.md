# Connecting [RunPodBoss](https://github.com/CryptoJones/RunPodBoss) to Triage

**Status:** Evaluation. Recommended integration is implementable today
(once the `triage signal` CLI ships — see Prerequisite below). No
RunPodBoss code changes required for the recommended path; only a
config-file update.

---

## TL;DR

**Yes, they fit together cleanly.** RunPodBoss already exposes the
exact hook needed (`extra_notify_command` in `config.json`). Once
Triage's `triage signal` CLI ships, you can wire RunPodBoss to push
a `runpodboss-threshold` signal into Triage on every threshold cross,
and a new `rule_balance_pressure` rule can turn those signals into
priority bumps on `runpod:<pod-id>`-tagged tasks.

The result: when RunPod balance crosses below a configured threshold,
Triage's queue reorders so the "drain idle pods" task floats to the
top — without RunPodBoss needing to know anything about Triage's
priority model.

---

## What each side does today

### RunPodBoss

- Polls RunPod GraphQL every 60s for **client balance** + **pod list**.
- Maintains armed/fired state per named threshold
  (e.g. `warning $10`, `critical $2`, `emergency $0.50`) at
  `~/.runpodboss/state.json`.
- On threshold-cross-down (balance below threshold for the first
  time since the last "above"), fires:
    - `claude -p "<templated prompt>"` — spawns a Claude Code agent
      with the balance + pods context to make termination decisions.
    - Optionally, `extra_notify_command` — any extra shell command
      with the same `{balance}` / `{pods_json}` / `{name}` template
      substitution. **Empty by default.**

### Triage

- File-backed task queue + signal-driven scoring.
- Already polls RunPod's *pod* state via `triage poll runpod-cost`
  (v0.5). Bumps tasks tagged `runpod:<pod-id>` based on per-pod
  idle/running state.
- Does **not** poll balance. Has no concept of dollar amounts.

### The complementary gap

- RunPodBoss has **balance context** (Triage doesn't).
- Triage has **task-priority context** (RunPodBoss doesn't).
- Both poll RunPod independently — but at different cadences and
  for different reasons.

The integration isn't "merge them." It's "RunPodBoss already has the
information Triage lacks; let it push that information across."

---

## Recommended integration

Use RunPodBoss's existing `extra_notify_command` to push a signal
into Triage on every threshold cross. Concretely:

```json
{
  "thresholds": [
    {
      "name": "critical",
      "below_usd": 2.00,
      "prompt": "RunPod balance CRITICAL: ${balance:.2f}…",
      "extra_notify_command": [
        "triage", "signal", "manual",
        "--source", "runpodboss",
        "--bump", "150",
        "--ttl", "1800",
        "--note", "balance below {name} threshold: {balance:.2f}"
      ]
    }
  ]
}
```

Then in Triage, the existing `runpod:<pod-id>`-tagged tasks see a new
signal with `source: runpodboss`, payload includes the threshold name
and balance, and a small new rule bumps their priority. The drain-pods
task floats to the top.

### Why this design

1. **No RunPodBoss code changes.** The hook already exists; we just
   fill in the config.
2. **Triage stays passive.** RunPodBoss is the active poller; Triage
   receives events. Triage already has a "manual signal" pattern from
   the v0.8 plan (`triage signal manual --bump N`).
3. **No new shared state.** No coupling to `~/.runpodboss/state.json`
   format. Each tool stays the source of truth for its own data.
4. **Easy to disable / override.** Operators who don't run RunPodBoss
   just don't get the signals. Operators who want a different bump
   weight or TTL tune the config without touching either codebase.

---

## Alternatives considered

### A. Triage polls RunPodBoss's state.json directly

A new `triage poll runpodboss-state` source that reads
`~/.runpodboss/state.json`.

**Rejected because:**
- `state.json` only stores armed/fired flags, not balance/pods.
  Triage would still need to poll RunPod separately for balance.
- Couples Triage to RunPodBoss's on-disk format.
- Adds polling cost (each `tick` runs the read).

### B. RunPodBoss writes JSONL directly into `~/.triage/state/`

`extra_notify_command: ["sh", "-c", "echo {...} >> ~/.triage/state/runpodboss.jsonl"]`

**Rejected because:** bypasses Triage's signal model. Schema drift
becomes silent. Fragile.

### C. Merge the two projects

**Rejected because:** they serve different deadlines —
RunPodBoss must fire fast (sub-minute) on credit emergencies;
Triage runs on user invocations or longer cron intervals. Different
operational characteristics, different deploys, different failure
modes. Keep them separate.

### D. Both → Telegram via [InterruptingCow](https://github.com/CryptoJones/InterruptingCow)

Independent of the Triage integration: RunPodBoss's
`extra_notify_command` could call `moo "RunPod {name}: ${balance:.2f}"`
to ping the operator on Telegram immediately. This is a
human-notification side channel and is **complementary** to the
Triage signal — not an alternative. Worth wiring once the Telegram
chat_id is in place.

---

## Prerequisite: `triage signal` CLI verb

The recommended integration relies on a `triage signal manual` CLI
verb that doesn't exist yet. It's small and self-contained:

```
triage signal manual \
  --source <name> \
  --affects <task-id> [--affects ...]  \
  --bump <int> \
  --ttl <seconds> \
  [--note <string>]
```

Writes a `Signal` to `~/.triage/state/manual.jsonl` so the existing
signal/rule plumbing picks it up on next `triage tick` / `triage list`.

This PR ships that verb along with this document.

---

## Recommended next steps

1. **(this PR)** Ship `triage signal manual` CLI verb + this
   evaluation doc.
2. **Follow-up PR in RunPodBoss:** add an `extra_notify_command`
   example to `config.example.json` showing the Triage wiring (no
   runtime code changes needed).
3. **Follow-up small Triage feature:** new rule
   `rule_balance_pressure` that scales the bump by threshold severity
   (e.g. warning → +30, critical → +80, emergency → +150).
4. **(Once Telegram chat_id is available)** wire a parallel
   `moo "..."` invocation for human-level alerting.

---

## What this does NOT do

- Triage will still not know about RunPod balance autonomously.
  It only knows what RunPodBoss tells it via signals.
- Killing pods is still RunPodBoss / Claude Code's job. Triage
  reorders the **queue**; an external actor (human or agent)
  still does the work.
- No new auth surface. RunPodBoss already has the RunPod API key;
  Triage just receives derived signals from RunPodBoss.

---

Proudly Made in Nebraska. Go Big Red! 🌽 https://xkcd.com/2347/
