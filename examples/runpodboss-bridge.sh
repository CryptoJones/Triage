#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
#
# runpodboss-bridge.sh — example wiring for an external watcher
# (like https://github.com/CryptoJones/RunPodBoss) to push
# threshold-cross events into Triage as manual signals.
#
# Demonstrates:
# - `triage signal manual` with --source and --bump for
#   external-watcher integration.
# - How `rule_manual_bump` turns a one-off signal into a priority
#   delta visible in `triage list` and `triage why`.
#
# Real RunPodBoss users should not call this script — they should
# add the same command to their `config.json` under
# `extra_notify_command` so RunPodBoss invokes it directly. See
# docs/runpodboss-integration.md for the design rationale.
#
# This script exists as a smoke test you can run manually to verify
# the bridge works end-to-end before flipping the switch in
# RunPodBoss's config.
#
# Usage:
#   ./examples/runpodboss-bridge.sh <pod-id> [<bump>] [<threshold-name>]
# Example:
#   ./examples/runpodboss-bridge.sh abc123pod 100 critical

set -euo pipefail

POD_ID="${1:?missing pod id (e.g. abc123pod)}"
BUMP="${2:-100}"
STATE="${3:-critical}"

# Find tasks tagged for this pod (if any).
AFFECTED=$(triage list --json 2>/dev/null | \
  python3 -c "import sys, json
tasks = json.load(sys.stdin)
# We can't see tags from list --json; fall back to running the source's
# own tag logic via 'triage show' on each task. For demo purposes,
# we'll just print all task ids and let triage signal target all.
print()
")

# For demonstration, emit a broadcast bump (no --affects = all tasks).
# In production, the RunPodBoss extra_notify_command should target
# specific task ids if the operator wants pod-specific bumps.
triage signal manual \
  --source runpodboss \
  --bump "$BUMP" \
  --ttl 1800 \
  --state "$STATE" \
  --note "POD $POD_ID — balance below $STATE threshold (bridge demo)"

echo ""
echo "Signal emitted. Verify with:"
echo "  triage list      # see the new priority order"
echo "  cat /var/log/triage.log | tail -1 | jq .    # see the JSONL event"
