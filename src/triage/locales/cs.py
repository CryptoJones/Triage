# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Čeština — Czech locale.

Standard Czech (Czech Republic). Native-speaker contributions welcome
via PR.
"""

STRINGS: dict[str, str] = {
    "__native_name__": "Čeština",

    # ---- argparse: top-level ----
    "Meta-scheduler that watches signals and reorders its own queue.":
        "Meta-plánovač, který sleduje signály a přeskupuje vlastní frontu.",
    "Override TRIAGE_HOME (default: ~/.triage or $TRIAGE_HOME).":
        "Přepíše TRIAGE_HOME (výchozí: ~/.triage nebo $TRIAGE_HOME).",
    "Output theme (default from $TRIAGE_THEME or {default}). Set NO_COLOR=1 to disable colors regardless of theme.":
        "Téma výstupu (výchozí z $TRIAGE_THEME nebo {default}). Nastavte NO_COLOR=1 pro vypnutí barev bez ohledu na téma.",
    "Force-disable ANSI color even on a TTY.":
        "Vynutit vypnutí ANSI barev i na TTY.",
    "Append JSONL events to this path (default: $TRIAGE_LOG_FILE or {default}; falls back to {fallback} if unwritable).":
        "Připojit události JSONL do této cesty (výchozí: $TRIAGE_LOG_FILE nebo {default}; spadne zpět na {fallback}, není-li zapisovatelná).",
    "Disable JSONL event logging for this invocation.":
        "Vypnout zápis událostí JSONL pro toto volání.",
    "Language for CLI output (default from $TRIAGE_LANG, $LANG, or 'en').":
        "Jazyk výstupu CLI (výchozí z $TRIAGE_LANG, $LANG nebo 'en').",

    # ---- argparse: subcommands ----
    "Add a task.":
        "Přidat úkol.",
    "Show the current priority order.":
        "Zobrazit aktuální pořadí priorit.",
    "Show one task's full record.":
        "Zobrazit úplný záznam jednoho úkolu.",
    "Audit log of rule contributions for a task.":
        "Auditní záznam příspěvků pravidel pro úkol.",
    "Recompute priorities; print new order.":
        "Přepočítat priority; vypsat nové pořadí.",
    "Invoke a network-bound signal source's poller.":
        "Spustit dotazovač síťově vázaného zdroje signálu.",
    "Inject a manual signal (for external watchers like RunPodBoss).":
        "Vložit ruční signál (pro externí pozorovatele jako RunPodBoss).",
    "Remove a task by id.":
        "Odstranit úkol podle id.",
    "One-screen at-a-glance: top-3 tasks, tag counts, signal counts.":
        "Jednoobrazovkový přehled: top-3 úkoly, počty štítků, počty signálů.",
    "List themes, or preview one with --name.":
        "Vypsat témata, nebo zobrazit náhled jednoho pomocí --name.",
    "List available output languages.":
        "Vypsat dostupné výstupní jazyky.",

    # ---- cmd_list / cmd_tick ----
    "(no tasks)":
        "(žádné úkoly)",
    "emitted {emitted} cron signal(s); ranked {ranked} task(s)":
        "vysláno {emitted} cron signál(ů); seřazeno {ranked} úkol(ů)",

    # ---- table headers ----
    "ID":
        "ID",
    "PRI":
        "PRI",
    "BAR":
        "BAR",
    "SUBJECT":
        "PŘEDMĚT",

    # ---- banner titles ----
    "T R I A G E   v{version}":
        "T R I A G E   v{version}",
    "T R I A G E   T I C K   v{version}":
        "T R I A G E   T I C K   v{version}",
    "T R I A G E   S T A T U S":
        "T R I A G E   S T A V",
    "theme preview: {name}":
        "náhled tématu: {name}",

    # ---- cmd_status sections ----
    "TOP 3":
        "TOP 3",
    "TAGS ({n})":
        "ŠTÍTKY ({n})",
    "ACTIVE SIGNALS ({n})":
        "AKTIVNÍ SIGNÁLY ({n})",
    "total tasks: {tasks}    ranked: {ranked}":
        "celkem úkolů: {tasks}    seřazeno: {ranked}",
    "(no tags)":
        "(žádné štítky)",
    "(no active signals)":
        "(žádné aktivní signály)",

    # ---- cmd_why ----
    "task {id}: {subject}":
        "úkol {id}: {subject}",
    "priority = {priority}":
        "priorita = {priority}",

    # ---- errors + status messages ----
    "no task with id {id}":
        "žádný úkol s id {id}",
    "warning: {message}":
        "upozornění: {message}",
    "unknown source: {source}. known: {known}":
        "neznámý zdroj: {source}. známé: {known}",
    "polled {source}: emitted {emitted} signal(s)":
        "dotázán {source}: vysláno {emitted} signál(ů)",
    "removed {id}":
        "odstraněn {id}",
    "signal emitted: source={source} bump={bump} ttl={ttl}s affects={affects}":
        "vyslán signál: zdroj={source} navýšení={bump} ttl={ttl}s ovlivňuje={affects}",
    "(all tasks)":
        "(všechny úkoly)",

    # ---- mock rows used in `triage theme --name X` preview ----
    "Critical hotfix":
        "Kritická oprava",
    "Deploy migration":
        "Nasadit migraci",
    "Catch up on email":
        "Dohnat e-mail",

    # ---- lang subcommand ----
    "available languages (default: {default}):":
        "dostupné jazyky (výchozí: {default}):",
    "unknown language: {lang}. known: {known}":
        "neznámý jazyk: {lang}. známé: {known}",

    # ---- model-layer errors + warnings (L10) ----
    "cron expression must have 5 fields, got {got}: {expr}":
        "vyraz cron musi mit 5 poli, obdrzeno {got}: {expr}",
    "cycle: removed edge {u} -> {v} (back-edge)":
        "cyklus: odstranena hrana {u} -> {v} (zpetna hrana)",
    "self-block: {id} blocks itself; ignored":
        "vlastni blokovani: {id} blokuje sama sebe; ignorovano",
    "dangling blocker: {id} blocked_by {blocker} (unknown); ignored":
        "viseny blokator: {id} blocked_by {blocker} (neznamy); ignorovano",
    "triage: log path {path} is not writable; logging disabled (set TRIAGE_NO_LOG=1 to silence).":
        "triage: cesta zaznamu {path} neni zapisovatelna; protokolovani zakazano (nastav TRIAGE_NO_LOG=1 pro utiseni).",
    "triage: {default} not writable, logging to {fallback} instead (create + chown {default} to use the standard path).":
        "triage: {default} neni zapisovatelna, protokoluji do {fallback} (vytvor + chown {default} pro standardni cestu).",
    "triage: neither {default} nor {fallback} is writable; events will not be logged.":
        "triage: ani {default}, ani {fallback} neni zapisovatelna; udalosti nebudou protokolovany.",
}
