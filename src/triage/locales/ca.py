# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Català — Catalan locale.

Standard Catalan (Catalonia). Native-speaker contributions for
Valencian welcome via PR.
"""

STRINGS: dict[str, str] = {
    "__native_name__": "Català",

    # ---- argparse: top-level ----
    "Meta-scheduler that watches signals and reorders its own queue.":
        "Meta-planificador que vigila els senyals i reordena la seva pròpia cua.",
    "Override TRIAGE_HOME (default: ~/.triage or $TRIAGE_HOME).":
        "Sobreescriu TRIAGE_HOME (per defecte: ~/.triage o $TRIAGE_HOME).",
    "Output theme (default from $TRIAGE_THEME or {default}). Set NO_COLOR=1 to disable colors regardless of theme.":
        "Tema de sortida (per defecte des de $TRIAGE_THEME o {default}). Estableix NO_COLOR=1 per desactivar els colors independentment del tema.",
    "Force-disable ANSI color even on a TTY.":
        "Força la desactivació del color ANSI fins i tot en un TTY.",
    "Append JSONL events to this path (default: $TRIAGE_LOG_FILE or {default}; falls back to {fallback} if unwritable).":
        "Afegeix esdeveniments JSONL a aquest camí (per defecte: $TRIAGE_LOG_FILE o {default}; recau a {fallback} si no és escrivible).",
    "Disable JSONL event logging for this invocation.":
        "Desactiva el registre d'esdeveniments JSONL per a aquesta invocació.",
    "Language for CLI output (default from $TRIAGE_LANG, $LANG, or 'en').":
        "Llengua per a la sortida CLI (per defecte des de $TRIAGE_LANG, $LANG o 'en').",

    # ---- argparse: subcommands ----
    "Add a task.":
        "Afegeix una tasca.",
    "Show the current priority order.":
        "Mostra l'ordre actual de prioritat.",
    "Show one task's full record.":
        "Mostra el registre complet d'una tasca.",
    "Audit log of rule contributions for a task.":
        "Registre d'auditoria de les contribucions de regles per a una tasca.",
    "Recompute priorities; print new order.":
        "Recalcula prioritats; imprimeix el nou ordre.",
    "Invoke a network-bound signal source's poller.":
        "Invoca l'enquestador d'una font de senyal lligada a la xarxa.",
    "Inject a manual signal (for external watchers like RunPodBoss).":
        "Injecta un senyal manual (per a observadors externs com RunPodBoss).",
    "Remove a task by id.":
        "Elimina una tasca per id.",
    "One-screen at-a-glance: top-3 tasks, tag counts, signal counts.":
        "Cop d'ull d'una pantalla: top-3 tasques, recomptes d'etiquetes, recomptes de senyals.",
    "List themes, or preview one with --name.":
        "Llista temes, o previsualitza'n un amb --name.",
    "List available output languages.":
        "Llista les llengües de sortida disponibles.",

    # ---- cmd_list / cmd_tick ----
    "(no tasks)":
        "(sense tasques)",
    "emitted {emitted} cron signal(s); ranked {ranked} task(s)":
        "emesos {emitted} senyal(s) cron; classificades {ranked} tasca/-ques",

    # ---- table headers ----
    "ID":
        "ID",
    "PRI":
        "PRI",
    "BAR":
        "BAR",
    "SUBJECT":
        "ASSUMPTE",

    # ---- banner titles ----
    "T R I A G E   v{version}":
        "T R I A G E   v{version}",
    "T R I A G E   T I C K   v{version}":
        "T R I A G E   T I C K   v{version}",
    "T R I A G E   S T A T U S":
        "T R I A G E   E S T A T",
    "theme preview: {name}":
        "previsualització del tema: {name}",

    # ---- cmd_status sections ----
    "TOP 3":
        "TOP 3",
    "TAGS ({n})":
        "ETIQUETES ({n})",
    "ACTIVE SIGNALS ({n})":
        "SENYALS ACTIUS ({n})",
    "total tasks: {tasks}    ranked: {ranked}":
        "tasques totals: {tasks}    classificades: {ranked}",
    "(no tags)":
        "(sense etiquetes)",
    "(no active signals)":
        "(sense senyals actius)",

    # ---- cmd_why ----
    "task {id}: {subject}":
        "tasca {id}: {subject}",
    "priority = {priority}":
        "prioritat = {priority}",

    # ---- errors + status messages ----
    "no task with id {id}":
        "cap tasca amb id {id}",
    "warning: {message}":
        "advertiment: {message}",
    "unknown source: {source}. known: {known}":
        "font desconeguda: {source}. conegudes: {known}",
    "polled {source}: emitted {emitted} signal(s)":
        "enquestat {source}: emesos {emitted} senyal(s)",
    "removed {id}":
        "eliminat {id}",
    "signal emitted: source={source} bump={bump} ttl={ttl}s affects={affects}":
        "senyal emès: font={source} augment={bump} ttl={ttl}s afecta={affects}",
    "(all tasks)":
        "(totes les tasques)",

    # ---- mock rows used in `triage theme --name X` preview ----
    "Critical hotfix":
        "Correcció crítica urgent",
    "Deploy migration":
        "Desplegar migració",
    "Catch up on email":
        "Posar-se al dia amb el correu",

    # ---- lang subcommand ----
    "available languages (default: {default}):":
        "llengües disponibles (per defecte: {default}):",
    "unknown language: {lang}. known: {known}":
        "llengua desconeguda: {lang}. conegudes: {known}",
}
