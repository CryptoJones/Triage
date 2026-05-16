# Triage Examples

Real-world recipes you can copy + tweak. Each one demonstrates a
different combination of Triage's primitives.

| Example                             | Demonstrates                                       |
|-------------------------------------|----------------------------------------------------|
| [`rotate-credentials.sh`](rotate-credentials.sh) | `--deadline`, `--cron-window`, per-task TTLs    |
| [`release-train.sh`](release-train.sh)           | `--blocked-by` chains, transitive propagation   |
| [`cron-tick`](cron-tick)            | Cron-scheduled `triage tick`; goes into `/etc/cron.d/`  |
| [`runpodboss-bridge.sh`](runpodboss-bridge.sh)   | `triage signal manual` driven by an external watcher |

Run any of the shell examples directly — they're idempotent
(re-running adds duplicate tasks, which `triage rm` can clean up).

```bash
chmod +x examples/*.sh
./examples/rotate-credentials.sh
triage list
```

The cron-tick file is plain text installable into `/etc/cron.d/`
(or `crontab -e`). See its header comment for the install steps.
