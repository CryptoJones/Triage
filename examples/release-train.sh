#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
#
# release-train.sh — a four-task release pipeline where the
# upstream tasks must finish before the downstream ones.
#
# Demonstrates:
# - --blocked-by chains and the blocker_transitive rule. Setting
#   --base-score on the *final* task naturally lifts its blockers
#   above it, so the queue reflects the actual work order even
#   though the human-readable priority is "ship the release."
# - The visible output of `triage list` matches the order you'd
#   actually have to execute the tasks in.
#
# Usage:
#   ./examples/release-train.sh
#   triage list
#   triage why <release-task-id>
#
# Cleanup: `triage rm <id>` per task, or wipe with
#   rm ~/.triage/tasks.json

set -euo pipefail

# We need each task's id to set up the blocked_by chain. Capture them.
ID_PR=$(triage add "Open release PR + run full test matrix" \
  --base-score 1 \
  --tag "release:v1.0")

ID_RC=$(triage add "Cut release candidate tag" \
  --base-score 1 \
  --tag "release:v1.0" \
  --blocked-by "$ID_PR")

ID_QA=$(triage add "QA smoke pass on the RC" \
  --base-score 1 \
  --tag "release:v1.0" \
  --blocked-by "$ID_RC")

ID_SHIP=$(triage add "Ship the release announcement" \
  --base-score 100 \
  --tag "release:v1.0" \
  --blocked-by "$ID_QA")

echo "release train queued:"
echo "  $ID_PR    open PR (blocks the rest)"
echo "  $ID_RC    cut RC  (blocked by PR)"
echo "  $ID_QA    QA pass (blocked by RC)"
echo "  $ID_SHIP  ship    (blocked by QA, base-score 100)"
echo ""
echo "blocker_transitive propagates the 100 backwards: open-PR ends up"
echo "at priority 103, cut-RC at 102, QA at 101, ship-release at 100."
echo "run: triage list"
