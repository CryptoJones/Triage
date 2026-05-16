# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Deutsch — German locale.

Translations done by Claude with hands-on review for tone matching
Triage's CLI register (terse, technical, lower-case command output,
sentence-case banners). Native-speaker contributions welcome via PR.
"""

STRINGS: dict[str, str] = {
    "__native_name__": "Deutsch",

    # ---- argparse: top-level ----
    "Meta-scheduler that watches signals and reorders its own queue.":
        "Meta-Scheduler, der Signale beobachtet und seine eigene Warteschlange neu ordnet.",
    "Override TRIAGE_HOME (default: ~/.triage or $TRIAGE_HOME).":
        "TRIAGE_HOME überschreiben (Standard: ~/.triage oder $TRIAGE_HOME).",
    "Output theme (default from $TRIAGE_THEME or {default}). Set NO_COLOR=1 to disable colors regardless of theme.":
        "Ausgabethema (Standard aus $TRIAGE_THEME oder {default}). Setze NO_COLOR=1, um Farben unabhängig vom Thema zu deaktivieren.",
    "Force-disable ANSI color even on a TTY.":
        "ANSI-Farben auch auf einem TTY zwangsweise deaktivieren.",
    "Append JSONL events to this path (default: $TRIAGE_LOG_FILE or {default}; falls back to {fallback} if unwritable).":
        "JSONL-Ereignisse an diesen Pfad anhängen (Standard: $TRIAGE_LOG_FILE oder {default}; weicht auf {fallback} aus, falls nicht schreibbar).",
    "Disable JSONL event logging for this invocation.":
        "JSONL-Ereignisprotokollierung für diesen Aufruf deaktivieren.",
    "Language for CLI output (default from $TRIAGE_LANG, $LANG, or 'en').":
        "Sprache für die CLI-Ausgabe (Standard aus $TRIAGE_LANG, $LANG oder 'en').",

    # ---- argparse: subcommands ----
    "Add a task.":
        "Eine Aufgabe hinzufügen.",
    "Show the current priority order.":
        "Aktuelle Prioritätsreihenfolge anzeigen.",
    "Show one task's full record.":
        "Vollständigen Eintrag einer Aufgabe anzeigen.",
    "Audit log of rule contributions for a task.":
        "Audit-Protokoll der Regelbeiträge für eine Aufgabe.",
    "Recompute priorities; print new order.":
        "Prioritäten neu berechnen; neue Reihenfolge ausgeben.",
    "Invoke a network-bound signal source's poller.":
        "Den Abrufer einer netzwerkgebundenen Signalquelle aufrufen.",
    "Inject a manual signal (for external watchers like RunPodBoss).":
        "Ein manuelles Signal einfügen (für externe Beobachter wie RunPodBoss).",
    "Remove a task by id.":
        "Eine Aufgabe nach ID entfernen.",
    "One-screen at-a-glance: top-3 tasks, tag counts, signal counts.":
        "Ein-Bildschirm-Übersicht: Top-3 Aufgaben, Tag-Zählungen, Signal-Zählungen.",
    "List themes, or preview one with --name.":
        "Themen auflisten oder eines mit --name vorschauen.",
    "List available output languages.":
        "Verfügbare Ausgabesprachen auflisten.",

    # ---- cmd_list / cmd_tick ----
    "(no tasks)":
        "(keine Aufgaben)",
    "emitted {emitted} cron signal(s); ranked {ranked} task(s)":
        "{emitted} Cron-Signal(e) ausgegeben; {ranked} Aufgabe(n) eingeordnet",

    # ---- table headers ----
    "ID":
        "ID",
    "PRI":
        "PRI",
    "BAR":
        "BAL",
    "SUBJECT":
        "BETREFF",

    # ---- banner titles ----
    "T R I A G E   v{version}":
        "T R I A G E   v{version}",
    "T R I A G E   T I C K   v{version}":
        "T R I A G E   T I C K   v{version}",
    "T R I A G E   S T A T U S":
        "T R I A G E   S T A T U S",
    "theme preview: {name}":
        "Themen-Vorschau: {name}",

    # ---- cmd_status sections ----
    "TOP 3":
        "TOP 3",
    "TAGS ({n})":
        "TAGS ({n})",
    "ACTIVE SIGNALS ({n})":
        "AKTIVE SIGNALE ({n})",
    "total tasks: {tasks}    ranked: {ranked}":
        "Aufgaben gesamt: {tasks}    eingeordnet: {ranked}",
    "(no tags)":
        "(keine Tags)",
    "(no active signals)":
        "(keine aktiven Signale)",

    # ---- cmd_why ----
    "task {id}: {subject}":
        "Aufgabe {id}: {subject}",
    "priority = {priority}":
        "Priorität = {priority}",

    # ---- errors + status messages ----
    "no task with id {id}":
        "keine Aufgabe mit ID {id}",
    "warning: {message}":
        "Warnung: {message}",
    "unknown source: {source}. known: {known}":
        "unbekannte Quelle: {source}. bekannt: {known}",
    "polled {source}: emitted {emitted} signal(s)":
        "{source} abgefragt: {emitted} Signal(e) ausgegeben",
    "removed {id}":
        "{id} entfernt",
    "signal emitted: source={source} bump={bump} ttl={ttl}s affects={affects}":
        "Signal ausgegeben: Quelle={source} Erhöhung={bump} TTL={ttl}s betrifft={affects}",
    "(all tasks)":
        "(alle Aufgaben)",

    # ---- mock rows used in `triage theme --name X` preview ----
    "Critical hotfix":
        "Kritischer Hotfix",
    "Deploy migration":
        "Migration bereitstellen",
    "Catch up on email":
        "E-Mails aufholen",

    # ---- lang subcommand ----
    "available languages (default: {default}):":
        "verfügbare Sprachen (Standard: {default}):",
    "unknown language: {lang}. known: {known}":
        "unbekannte Sprache: {lang}. bekannt: {known}",
}
