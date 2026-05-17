# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Dansk — Danish locale.

Standard Danish (Denmark). Native-speaker contributions welcome via PR.
"""

STRINGS: dict[str, str] = {
    "__native_name__": "Dansk",

    # ---- argparse: top-level ----
    "Meta-scheduler that watches signals and reorders its own queue.":
        "Meta-planlægger der overvåger signaler og omordner sin egen kø.",
    "Override TRIAGE_HOME (default: ~/.triage or $TRIAGE_HOME).":
        "Tilsidesæt TRIAGE_HOME (standard: ~/.triage eller $TRIAGE_HOME).",
    "Output theme (default from $TRIAGE_THEME or {default}). Set NO_COLOR=1 to disable colors regardless of theme.":
        "Outputtema (standard fra $TRIAGE_THEME eller {default}). Sæt NO_COLOR=1 for at deaktivere farver uanset tema.",
    "Force-disable ANSI color even on a TTY.":
        "Tving ANSI-farve fra selv på en TTY.",
    "Append JSONL events to this path (default: $TRIAGE_LOG_FILE or {default}; falls back to {fallback} if unwritable).":
        "Tilføj JSONL-hændelser til denne sti (standard: $TRIAGE_LOG_FILE eller {default}; falder tilbage til {fallback}, hvis ikke skrivbar).",
    "Disable JSONL event logging for this invocation.":
        "Deaktivér JSONL-hændelseslogning for denne kørsel.",
    "Language for CLI output (default from $TRIAGE_LANG, $LANG, or 'en').":
        "Sprog til CLI-output (standard fra $TRIAGE_LANG, $LANG eller 'en').",

    # ---- argparse: subcommands ----
    "Add a task.":
        "Tilføj en opgave.",
    "Show the current priority order.":
        "Vis den aktuelle prioritetsrækkefølge.",
    "Show one task's full record.":
        "Vis hele posten for én opgave.",
    "Audit log of rule contributions for a task.":
        "Revisionslog over regelbidrag for en opgave.",
    "Recompute priorities; print new order.":
        "Genberegn prioriteter; udskriv ny rækkefølge.",
    "Invoke a network-bound signal source's poller.":
        "Kald polleren for en netværksbunden signalkilde.",
    "Inject a manual signal (for external watchers like RunPodBoss).":
        "Injicér et manuelt signal (til eksterne overvågere som RunPodBoss).",
    "Remove a task by id.":
        "Fjern en opgave efter id.",
    "One-screen at-a-glance: top-3 tasks, tag counts, signal counts.":
        "Overblik på én skærm: top-3 opgaver, tag-antal, signal-antal.",
    "List themes, or preview one with --name.":
        "List temaer, eller forhåndsvis ét med --name.",
    "List available output languages.":
        "List tilgængelige outputsprog.",

    # ---- cmd_list / cmd_tick ----
    "(no tasks)":
        "(ingen opgaver)",
    "emitted {emitted} cron signal(s); ranked {ranked} task(s)":
        "udsendte {emitted} cron-signal(er); rangerede {ranked} opgave(r)",

    # ---- table headers ----
    "ID":
        "ID",
    "PRI":
        "PRI",
    "BAR":
        "BAR",
    "SUBJECT":
        "EMNE",

    # ---- banner titles ----
    "T R I A G E   v{version}":
        "T R I A G E   v{version}",
    "T R I A G E   T I C K   v{version}":
        "T R I A G E   T I C K   v{version}",
    "T R I A G E   S T A T U S":
        "T R I A G E   S T A T U S",
    "theme preview: {name}":
        "tema-forhåndsvisning: {name}",

    # ---- cmd_status sections ----
    "TOP 3":
        "TOP 3",
    "TAGS ({n})":
        "TAGS ({n})",
    "ACTIVE SIGNALS ({n})":
        "AKTIVE SIGNALER ({n})",
    "total tasks: {tasks}    ranked: {ranked}":
        "opgaver i alt: {tasks}    rangerede: {ranked}",
    "(no tags)":
        "(ingen tags)",
    "(no active signals)":
        "(ingen aktive signaler)",

    # ---- cmd_why ----
    "task {id}: {subject}":
        "opgave {id}: {subject}",
    "priority = {priority}":
        "prioritet = {priority}",

    # ---- errors + status messages ----
    "no task with id {id}":
        "ingen opgave med id {id}",
    "warning: {message}":
        "advarsel: {message}",
    "unknown source: {source}. known: {known}":
        "ukendt kilde: {source}. kendte: {known}",
    "polled {source}: emitted {emitted} signal(s)":
        "pollede {source}: udsendte {emitted} signal(er)",
    "removed {id}":
        "fjernede {id}",
    "signal emitted: source={source} bump={bump} ttl={ttl}s affects={affects}":
        "signal udsendt: kilde={source} forhøjelse={bump} ttl={ttl}s påvirker={affects}",
    "(all tasks)":
        "(alle opgaver)",

    # ---- mock rows used in `triage theme --name X` preview ----
    "Critical hotfix":
        "Kritisk hotfix",
    "Deploy migration":
        "Udrul migrering",
    "Catch up on email":
        "Indhent e-mail",

    # ---- lang subcommand ----
    "available languages (default: {default}):":
        "tilgængelige sprog (standard: {default}):",
    "unknown language: {lang}. known: {known}":
        "ukendt sprog: {lang}. kendte: {known}",

    # ---- model-layer errors + warnings (L10) ----
    "cron expression must have 5 fields, got {got}: {expr}":
        "cron-udtryk skal have 5 felter, fik {got}: {expr}",
    "cycle: removed edge {u} -> {v} (back-edge)":
        "cyklus: fjernede kant {u} -> {v} (bagkant)",
    "self-block: {id} blocks itself; ignored":
        "selvblokering: {id} blokerer sig selv; ignoreret",
    "dangling blocker: {id} blocked_by {blocker} (unknown); ignored":
        "los blokering: {id} blocked_by {blocker} (ukendt); ignoreret",
    "triage: log path {path} is not writable; logging disabled (set TRIAGE_NO_LOG=1 to silence).":
        "triage: logsti {path} kan ikke skrives; logning deaktiveret (sat TRIAGE_NO_LOG=1 for at dampe).",
    "triage: {default} not writable, logging to {fallback} instead (create + chown {default} to use the standard path).":
        "triage: {default} kan ikke skrives, logger til {fallback} i stedet (opret + chown {default} for at bruge standardstien).",
    "triage: neither {default} nor {fallback} is writable; events will not be logged.":
        "triage: hverken {default} eller {fallback} kan skrives; handelser logges ikke.",
}
