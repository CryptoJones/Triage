# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Română — Romanian locale.

Standard Romanian (Romania). Native-speaker contributions for
Moldovan welcome via PR under a separate locale code if desired.
"""

STRINGS: dict[str, str] = {
    "__native_name__": "Română",

    # ---- argparse: top-level ----
    "Meta-scheduler that watches signals and reorders its own queue.":
        "Meta-planificator care urmărește semnale și își reordonează propria coadă.",
    "Override TRIAGE_HOME (default: ~/.triage or $TRIAGE_HOME).":
        "Suprascrie TRIAGE_HOME (implicit: ~/.triage sau $TRIAGE_HOME).",
    "Output theme (default from $TRIAGE_THEME or {default}). Set NO_COLOR=1 to disable colors regardless of theme.":
        "Tema de ieșire (implicit din $TRIAGE_THEME sau {default}). Setează NO_COLOR=1 pentru a dezactiva culorile indiferent de temă.",
    "Force-disable ANSI color even on a TTY.":
        "Forțează dezactivarea culorii ANSI chiar și pe un TTY.",
    "Append JSONL events to this path (default: $TRIAGE_LOG_FILE or {default}; falls back to {fallback} if unwritable).":
        "Adaugă evenimente JSONL la această cale (implicit: $TRIAGE_LOG_FILE sau {default}; revine la {fallback} dacă nu este scriibilă).",
    "Disable JSONL event logging for this invocation.":
        "Dezactivează jurnalizarea evenimentelor JSONL pentru această invocare.",
    "Language for CLI output (default from $TRIAGE_LANG, $LANG, or 'en').":
        "Limba pentru ieșirea CLI (implicit din $TRIAGE_LANG, $LANG sau 'en').",

    # ---- argparse: subcommands ----
    "Add a task.":
        "Adaugă o sarcină.",
    "Show the current priority order.":
        "Afișează ordinea curentă a priorităților.",
    "Show one task's full record.":
        "Afișează înregistrarea completă a unei sarcini.",
    "Audit log of rule contributions for a task.":
        "Jurnal de audit al contribuțiilor regulilor pentru o sarcină.",
    "Recompute priorities; print new order.":
        "Recalculează prioritățile; afișează noua ordine.",
    "Invoke a network-bound signal source's poller.":
        "Invocă interogatorul unei surse de semnal legate de rețea.",
    "Inject a manual signal (for external watchers like RunPodBoss).":
        "Injectează un semnal manual (pentru observatori externi precum RunPodBoss).",
    "Remove a task by id.":
        "Elimină o sarcină după id.",
    "One-screen at-a-glance: top-3 tasks, tag counts, signal counts.":
        "Privire pe un singur ecran: top-3 sarcini, numărători de etichete, numărători de semnale.",
    "List themes, or preview one with --name.":
        "Listează teme sau previzualizează una cu --name.",
    "List available output languages.":
        "Listează limbile de ieșire disponibile.",

    # ---- cmd_list / cmd_tick ----
    "(no tasks)":
        "(fără sarcini)",
    "emitted {emitted} cron signal(s); ranked {ranked} task(s)":
        "emise {emitted} semnal(e) cron; clasate {ranked} sarcină(i)",

    # ---- table headers ----
    "ID":
        "ID",
    "PRI":
        "PRI",
    "BAR":
        "BAR",
    "SUBJECT":
        "SUBIECT",

    # ---- banner titles ----
    "T R I A G E   v{version}":
        "T R I A G E   v{version}",
    "T R I A G E   T I C K   v{version}":
        "T R I A G E   T I C K   v{version}",
    "T R I A G E   S T A T U S":
        "T R I A G E   S T A R E",
    "theme preview: {name}":
        "previzualizare temă: {name}",

    # ---- cmd_status sections ----
    "TOP 3":
        "TOP 3",
    "TAGS ({n})":
        "ETICHETE ({n})",
    "ACTIVE SIGNALS ({n})":
        "SEMNALE ACTIVE ({n})",
    "total tasks: {tasks}    ranked: {ranked}":
        "total sarcini: {tasks}    clasate: {ranked}",
    "(no tags)":
        "(fără etichete)",
    "(no active signals)":
        "(fără semnale active)",

    # ---- cmd_why ----
    "task {id}: {subject}":
        "sarcina {id}: {subject}",
    "priority = {priority}":
        "prioritate = {priority}",

    # ---- errors + status messages ----
    "no task with id {id}":
        "nicio sarcină cu id {id}",
    "warning: {message}":
        "avertisment: {message}",
    "unknown source: {source}. known: {known}":
        "sursă necunoscută: {source}. cunoscute: {known}",
    "polled {source}: emitted {emitted} signal(s)":
        "interogat {source}: emise {emitted} semnal(e)",
    "removed {id}":
        "eliminat {id}",
    "signal emitted: source={source} bump={bump} ttl={ttl}s affects={affects}":
        "semnal emis: sursă={source} creștere={bump} ttl={ttl}s afectează={affects}",
    "(all tasks)":
        "(toate sarcinile)",

    # ---- mock rows used in `triage theme --name X` preview ----
    "Critical hotfix":
        "Remediere critică",
    "Deploy migration":
        "Implementează migrarea",
    "Catch up on email":
        "Recuperează e-mailul",

    # ---- lang subcommand ----
    "available languages (default: {default}):":
        "limbi disponibile (implicit: {default}):",
    "unknown language: {lang}. known: {known}":
        "limbă necunoscută: {lang}. cunoscute: {known}",
}
