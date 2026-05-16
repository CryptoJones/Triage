# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Italiano — Italian locale.

Translations done by Claude with hands-on review for tone matching
Triage's CLI register. Native-speaker contributions welcome via PR.
"""

STRINGS: dict[str, str] = {
    "__native_name__": "Italiano",

    # ---- argparse: top-level ----
    "Meta-scheduler that watches signals and reorders its own queue.":
        "Meta-scheduler che osserva i segnali e riordina la propria coda.",
    "Override TRIAGE_HOME (default: ~/.triage or $TRIAGE_HOME).":
        "Sovrascrivi TRIAGE_HOME (predefinito: ~/.triage o $TRIAGE_HOME).",
    "Output theme (default from $TRIAGE_THEME or {default}). Set NO_COLOR=1 to disable colors regardless of theme.":
        "Tema di output (predefinito da $TRIAGE_THEME o {default}). Imposta NO_COLOR=1 per disabilitare i colori indipendentemente dal tema.",
    "Force-disable ANSI color even on a TTY.":
        "Disabilita forzatamente il colore ANSI anche su un TTY.",
    "Append JSONL events to this path (default: $TRIAGE_LOG_FILE or {default}; falls back to {fallback} if unwritable).":
        "Aggiungi eventi JSONL a questo percorso (predefinito: $TRIAGE_LOG_FILE o {default}; ripiega su {fallback} se non scrivibile).",
    "Disable JSONL event logging for this invocation.":
        "Disabilita la registrazione degli eventi JSONL per questa invocazione.",
    "Language for CLI output (default from $TRIAGE_LANG, $LANG, or 'en').":
        "Lingua per l'output CLI (predefinita da $TRIAGE_LANG, $LANG, o 'en').",

    # ---- argparse: subcommands ----
    "Add a task.":
        "Aggiungi un'attività.",
    "Show the current priority order.":
        "Mostra l'ordine di priorità attuale.",
    "Show one task's full record.":
        "Mostra il record completo di un'attività.",
    "Audit log of rule contributions for a task.":
        "Registro di audit dei contributi delle regole per un'attività.",
    "Recompute priorities; print new order.":
        "Ricalcola le priorità; stampa il nuovo ordine.",
    "Invoke a network-bound signal source's poller.":
        "Invoca il polling di una sorgente di segnali basata sulla rete.",
    "Inject a manual signal (for external watchers like RunPodBoss).":
        "Inietta un segnale manuale (per osservatori esterni come RunPodBoss).",
    "Remove a task by id.":
        "Rimuovi un'attività per id.",
    "One-screen at-a-glance: top-3 tasks, tag counts, signal counts.":
        "Visualizzazione a colpo d'occhio: le 3 attività principali, conteggi dei tag, conteggi dei segnali.",
    "List themes, or preview one with --name.":
        "Elenca i temi o visualizzane uno in anteprima con --name.",
    "List available output languages.":
        "Elenca le lingue di output disponibili.",

    # ---- cmd_list / cmd_tick ----
    "(no tasks)":
        "(nessuna attività)",
    "emitted {emitted} cron signal(s); ranked {ranked} task(s)":
        "emessi {emitted} segnale(i) cron; classificate {ranked} attività",

    # ---- table headers ----
    "ID":
        "ID",
    "PRI":
        "PRI",
    "BAR":
        "BAR",
    "SUBJECT":
        "OGGETTO",

    # ---- banner titles ----
    "T R I A G E   v{version}":
        "T R I A G E   v{version}",
    "T R I A G E   T I C K   v{version}":
        "T R I A G E   T I C K   v{version}",
    "T R I A G E   S T A T U S":
        "T R I A G E   S T A T O",
    "theme preview: {name}":
        "anteprima tema: {name}",

    # ---- cmd_status sections ----
    "TOP 3":
        "TOP 3",
    "TAGS ({n})":
        "TAG ({n})",
    "ACTIVE SIGNALS ({n})":
        "SEGNALI ATTIVI ({n})",
    "total tasks: {tasks}    ranked: {ranked}":
        "attività totali: {tasks}    classificate: {ranked}",
    "(no tags)":
        "(nessun tag)",
    "(no active signals)":
        "(nessun segnale attivo)",

    # ---- cmd_why ----
    "task {id}: {subject}":
        "attività {id}: {subject}",
    "priority = {priority}":
        "priorità = {priority}",

    # ---- errors + status messages ----
    "no task with id {id}":
        "nessuna attività con id {id}",
    "warning: {message}":
        "avviso: {message}",
    "unknown source: {source}. known: {known}":
        "sorgente sconosciuta: {source}. conosciute: {known}",
    "polled {source}: emitted {emitted} signal(s)":
        "{source} interrogata: emessi {emitted} segnale(i)",
    "removed {id}":
        "{id} rimossa",
    "signal emitted: source={source} bump={bump} ttl={ttl}s affects={affects}":
        "segnale emesso: sorgente={source} incremento={bump} ttl={ttl}s riguarda={affects}",
    "(all tasks)":
        "(tutte le attività)",

    # ---- mock rows used in `triage theme --name X` preview ----
    "Critical hotfix":
        "Correzione critica urgente",
    "Deploy migration":
        "Distribuire la migrazione",
    "Catch up on email":
        "Mettersi in pari con le email",

    # ---- lang subcommand ----
    "available languages (default: {default}):":
        "lingue disponibili (predefinita: {default}):",
    "unknown language: {lang}. known: {known}":
        "lingua sconosciuta: {lang}. conosciute: {known}",
}
