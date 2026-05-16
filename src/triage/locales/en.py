# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""English — the baseline locale + canonical key set.

Every other locale's STRINGS dict must use these same keys. Tests
verify that and that placeholder names line up.
"""

STRINGS: dict[str, str] = {
    "__native_name__": "English",

    # ---- argparse: top-level ----
    "Meta-scheduler that watches signals and reorders its own queue.":
        "Meta-scheduler that watches signals and reorders its own queue.",
    "Override TRIAGE_HOME (default: ~/.triage or $TRIAGE_HOME).":
        "Override TRIAGE_HOME (default: ~/.triage or $TRIAGE_HOME).",
    "Output theme (default from $TRIAGE_THEME or {default}). Set NO_COLOR=1 to disable colors regardless of theme.":
        "Output theme (default from $TRIAGE_THEME or {default}). Set NO_COLOR=1 to disable colors regardless of theme.",
    "Force-disable ANSI color even on a TTY.":
        "Force-disable ANSI color even on a TTY.",
    "Append JSONL events to this path (default: $TRIAGE_LOG_FILE or {default}; falls back to {fallback} if unwritable).":
        "Append JSONL events to this path (default: $TRIAGE_LOG_FILE or {default}; falls back to {fallback} if unwritable).",
    "Disable JSONL event logging for this invocation.":
        "Disable JSONL event logging for this invocation.",
    "Language for CLI output (default from $TRIAGE_LANG, $LANG, or 'en').":
        "Language for CLI output (default from $TRIAGE_LANG, $LANG, or 'en').",

    # ---- argparse: subcommands ----
    "Add a task.":
        "Add a task.",
    "Show the current priority order.":
        "Show the current priority order.",
    "Show one task's full record.":
        "Show one task's full record.",
    "Audit log of rule contributions for a task.":
        "Audit log of rule contributions for a task.",
    "Recompute priorities; print new order.":
        "Recompute priorities; print new order.",
    "Invoke a network-bound signal source's poller.":
        "Invoke a network-bound signal source's poller.",
    "Inject a manual signal (for external watchers like RunPodBoss).":
        "Inject a manual signal (for external watchers like RunPodBoss).",
    "Remove a task by id.":
        "Remove a task by id.",
    "One-screen at-a-glance: top-3 tasks, tag counts, signal counts.":
        "One-screen at-a-glance: top-3 tasks, tag counts, signal counts.",
    "List themes, or preview one with --name.":
        "List themes, or preview one with --name.",
    "List available output languages.":
        "List available output languages.",

    # ---- cmd_list / cmd_tick ----
    "(no tasks)":
        "(no tasks)",
    "emitted {emitted} cron signal(s); ranked {ranked} task(s)":
        "emitted {emitted} cron signal(s); ranked {ranked} task(s)",

    # ---- table headers ----
    "ID":
        "ID",
    "PRI":
        "PRI",
    "BAR":
        "BAR",
    "SUBJECT":
        "SUBJECT",

    # ---- banner titles ----
    "T R I A G E   v{version}":
        "T R I A G E   v{version}",
    "T R I A G E   T I C K   v{version}":
        "T R I A G E   T I C K   v{version}",
    "T R I A G E   S T A T U S":
        "T R I A G E   S T A T U S",
    "theme preview: {name}":
        "theme preview: {name}",

    # ---- cmd_status sections ----
    "TOP 3":
        "TOP 3",
    "TAGS ({n})":
        "TAGS ({n})",
    "ACTIVE SIGNALS ({n})":
        "ACTIVE SIGNALS ({n})",
    "total tasks: {tasks}    ranked: {ranked}":
        "total tasks: {tasks}    ranked: {ranked}",
    "(no tags)":
        "(no tags)",
    "(no active signals)":
        "(no active signals)",

    # ---- cmd_why ----
    "task {id}: {subject}":
        "task {id}: {subject}",
    "priority = {priority}":
        "priority = {priority}",

    # ---- errors + status messages ----
    "no task with id {id}":
        "no task with id {id}",
    "warning: {message}":
        "warning: {message}",
    "unknown source: {source}. known: {known}":
        "unknown source: {source}. known: {known}",
    "polled {source}: emitted {emitted} signal(s)":
        "polled {source}: emitted {emitted} signal(s)",
    "removed {id}":
        "removed {id}",
    "signal emitted: source={source} bump={bump} ttl={ttl}s affects={affects}":
        "signal emitted: source={source} bump={bump} ttl={ttl}s affects={affects}",
    "(all tasks)":
        "(all tasks)",

    # ---- mock rows used in `triage theme --name X` preview ----
    "Critical hotfix":
        "Critical hotfix",
    "Deploy migration":
        "Deploy migration",
    "Catch up on email":
        "Catch up on email",

    # ---- lang subcommand ----
    "available languages (default: {default}):":
        "available languages (default: {default}):",
    "unknown language: {lang}. known: {known}":
        "unknown language: {lang}. known: {known}",
}
