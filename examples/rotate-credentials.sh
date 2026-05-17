#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
#
# rotate-credentials.sh — quarterly credential-rotation queue.
#
# Requires: triage v0.1+ (uses --deadline, --cron-window, --tag).
#
# Demonstrates:
# - Per-task --deadline so deadline_decay bumps priority as the
#   rotation date approaches.
# - --cron-window tied to "office hours" so the bump is loudest
#   when you might actually act on it.
# - --tag to group rotations by environment so `triage list` is
#   easy to filter (e.g. `triage list --json | jq '.[] | select(.tags[]?=="env:prod")'`).
#
# Usage:
#   ./examples/rotate-credentials.sh
#   triage list
#   triage why <id>   # to see which rules pushed something to the top
#
# Re-running this script creates duplicates. Clean up with `triage rm`.

set -euo pipefail

QUARTER_END=$(date -d "$(date +%Y-%m-15) +90 days" -Iseconds 2>/dev/null || \
              date -j -v+90d -f "%Y-%m-%d" "$(date +%Y-%m-15)" "+%Y-%m-%dT%H:%M:%S+00:00")

triage add "Rotate AWS root account access keys" \
  --deadline "$QUARTER_END" \
  --base-score 8 \
  --tag "env:prod" \
  --tag "vendor:aws" \
  --cron-window "* 9-17 * * 1-5"

triage add "Rotate GitHub fine-grained PATs" \
  --deadline "$QUARTER_END" \
  --base-score 7 \
  --tag "env:prod" \
  --tag "vendor:github" \
  --cron-window "* 9-17 * * 1-5"

triage add "Rotate Codeberg API tokens" \
  --deadline "$QUARTER_END" \
  --base-score 7 \
  --tag "env:prod" \
  --tag "vendor:codeberg" \
  --cron-window "* 9-17 * * 1-5"

triage add "Rotate Hugging Face write tokens" \
  --deadline "$QUARTER_END" \
  --base-score 5 \
  --tag "env:prod" \
  --tag "vendor:huggingface" \
  --cron-window "* 9-17 * * 1-5"

triage add "Rotate RunPod API key" \
  --deadline "$QUARTER_END" \
  --base-score 6 \
  --tag "env:prod" \
  --tag "vendor:runpod" \
  --cron-window "* 9-17 * * 1-5"

echo "queued 5 credential rotations with deadline $QUARTER_END"
echo "run: triage list"
