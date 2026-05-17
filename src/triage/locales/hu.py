# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Magyar — Hungarian locale.

Standard Hungarian (Hungary). Native-speaker contributions welcome
via PR.
"""

STRINGS: dict[str, str] = {
    "__native_name__": "Magyar",

    # ---- argparse: top-level ----
    "Meta-scheduler that watches signals and reorders its own queue.":
        "Meta-ütemező, amely figyeli a jelzéseket és átrendezi a saját sorát.",
    "Override TRIAGE_HOME (default: ~/.triage or $TRIAGE_HOME).":
        "TRIAGE_HOME felülbírálása (alapértelmezés: ~/.triage vagy $TRIAGE_HOME).",
    "Output theme (default from $TRIAGE_THEME or {default}). Set NO_COLOR=1 to disable colors regardless of theme.":
        "Kimeneti téma (alapértelmezés a $TRIAGE_THEME vagy {default} alapján). Állítsd NO_COLOR=1-re a színek kikapcsolásához témától függetlenül.",
    "Force-disable ANSI color even on a TTY.":
        "ANSI szín kényszerített kikapcsolása még TTY-n is.",
    "Append JSONL events to this path (default: $TRIAGE_LOG_FILE or {default}; falls back to {fallback} if unwritable).":
        "JSONL események hozzáfűzése ehhez az útvonalhoz (alapértelmezés: $TRIAGE_LOG_FILE vagy {default}; visszaesik {fallback}-re, ha nem írható).",
    "Disable JSONL event logging for this invocation.":
        "JSONL eseménynaplózás kikapcsolása ehhez a hívásahoz.",
    "Language for CLI output (default from $TRIAGE_LANG, $LANG, or 'en').":
        "CLI kimenet nyelve (alapértelmezés a $TRIAGE_LANG, $LANG vagy 'en' alapján).",

    # ---- argparse: subcommands ----
    "Add a task.":
        "Feladat hozzáadása.",
    "Show the current priority order.":
        "Az aktuális prioritási sorrend megjelenítése.",
    "Show one task's full record.":
        "Egy feladat teljes rekordjának megjelenítése.",
    "Audit log of rule contributions for a task.":
        "Audit-napló egy feladat szabály-hozzájárulásairól.",
    "Recompute priorities; print new order.":
        "Prioritások újraszámítása; új sorrend kiírása.",
    "Invoke a network-bound signal source's poller.":
        "Hálózathoz kötött jelzésforrás lekérdezőjének meghívása.",
    "Inject a manual signal (for external watchers like RunPodBoss).":
        "Kézi jelzés befecskendezése (külső megfigyelőkhöz, mint a RunPodBoss).",
    "Remove a task by id.":
        "Feladat eltávolítása azonosító alapján.",
    "One-screen at-a-glance: top-3 tasks, tag counts, signal counts.":
        "Egyképernyős áttekintés: top-3 feladat, címkeszámlálók, jelzésszámlálók.",
    "List themes, or preview one with --name.":
        "Témák felsorolása, vagy egy előnézete --name segítségével.",
    "List available output languages.":
        "Elérhető kimeneti nyelvek felsorolása.",

    # ---- cmd_list / cmd_tick ----
    "(no tasks)":
        "(nincs feladat)",
    "emitted {emitted} cron signal(s); ranked {ranked} task(s)":
        "{emitted} cron-jelzés kibocsátva; {ranked} feladat rangsorolva",

    # ---- table headers ----
    "ID":
        "ID",
    "PRI":
        "PRI",
    "BAR":
        "BAR",
    "SUBJECT":
        "TÁRGY",

    # ---- banner titles ----
    "T R I A G E   v{version}":
        "T R I A G E   v{version}",
    "T R I A G E   T I C K   v{version}":
        "T R I A G E   T I C K   v{version}",
    "T R I A G E   S T A T U S":
        "T R I A G E   Á L L A P O T",
    "theme preview: {name}":
        "téma előnézete: {name}",

    # ---- cmd_status sections ----
    "TOP 3":
        "TOP 3",
    "TAGS ({n})":
        "CÍMKÉK ({n})",
    "ACTIVE SIGNALS ({n})":
        "AKTÍV JELZÉSEK ({n})",
    "total tasks: {tasks}    ranked: {ranked}":
        "összes feladat: {tasks}    rangsorolva: {ranked}",
    "(no tags)":
        "(nincs címke)",
    "(no active signals)":
        "(nincs aktív jelzés)",

    # ---- cmd_why ----
    "task {id}: {subject}":
        "feladat {id}: {subject}",
    "priority = {priority}":
        "prioritás = {priority}",

    # ---- errors + status messages ----
    "no task with id {id}":
        "nincs feladat {id} azonosítóval",
    "warning: {message}":
        "figyelmeztetés: {message}",
    "unknown source: {source}. known: {known}":
        "ismeretlen forrás: {source}. ismertek: {known}",
    "polled {source}: emitted {emitted} signal(s)":
        "lekérdezve {source}: {emitted} jelzés kibocsátva",
    "removed {id}":
        "eltávolítva {id}",
    "signal emitted: source={source} bump={bump} ttl={ttl}s affects={affects}":
        "jelzés kibocsátva: forrás={source} emelés={bump} ttl={ttl}s érinti={affects}",
    "(all tasks)":
        "(összes feladat)",

    # ---- mock rows used in `triage theme --name X` preview ----
    "Critical hotfix":
        "Kritikus gyorsjavítás",
    "Deploy migration":
        "Migráció telepítése",
    "Catch up on email":
        "E-mailek behozása",

    # ---- lang subcommand ----
    "available languages (default: {default}):":
        "elérhető nyelvek (alapértelmezés: {default}):",
    "unknown language: {lang}. known: {known}":
        "ismeretlen nyelv: {lang}. ismertek: {known}",
}
