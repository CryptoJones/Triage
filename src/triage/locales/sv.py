# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Svenska — Swedish locale.

Standard Swedish (Sweden). Native-speaker contributions welcome via PR.
"""

STRINGS: dict[str, str] = {
    "__native_name__": "Svenska",

    # ---- argparse: top-level ----
    "Meta-scheduler that watches signals and reorders its own queue.":
        "Metaschemaläggare som bevakar signaler och ordnar om sin egen kö.",
    "Override TRIAGE_HOME (default: ~/.triage or $TRIAGE_HOME).":
        "Åsidosätt TRIAGE_HOME (standard: ~/.triage eller $TRIAGE_HOME).",
    "Output theme (default from $TRIAGE_THEME or {default}). Set NO_COLOR=1 to disable colors regardless of theme.":
        "Utskriftstema (standard från $TRIAGE_THEME eller {default}). Sätt NO_COLOR=1 för att inaktivera färger oavsett tema.",
    "Force-disable ANSI color even on a TTY.":
        "Tvinga av ANSI-färg även på en TTY.",
    "Append JSONL events to this path (default: $TRIAGE_LOG_FILE or {default}; falls back to {fallback} if unwritable).":
        "Lägg till JSONL-händelser i denna sökväg (standard: $TRIAGE_LOG_FILE eller {default}; faller tillbaka till {fallback} om ej skrivbar).",
    "Disable JSONL event logging for this invocation.":
        "Inaktivera JSONL-händelseloggning för detta anrop.",
    "Language for CLI output (default from $TRIAGE_LANG, $LANG, or 'en').":
        "Språk för CLI-utskrift (standard från $TRIAGE_LANG, $LANG eller 'en').",

    # ---- argparse: subcommands ----
    "Add a task.":
        "Lägg till en uppgift.",
    "Show the current priority order.":
        "Visa aktuell prioritetsordning.",
    "Show one task's full record.":
        "Visa hela posten för en uppgift.",
    "Audit log of rule contributions for a task.":
        "Granskningslogg över regelbidrag för en uppgift.",
    "Recompute priorities; print new order.":
        "Räkna om prioriteter; skriv ut ny ordning.",
    "Invoke a network-bound signal source's poller.":
        "Anropa en nätverksbunden signalkällas pollare.",
    "Inject a manual signal (for external watchers like RunPodBoss).":
        "Injicera en manuell signal (för externa observatörer som RunPodBoss).",
    "Remove a task by id.":
        "Ta bort en uppgift via id.",
    "One-screen at-a-glance: top-3 tasks, tag counts, signal counts.":
        "Översikt på en skärm: topp-3 uppgifter, taggräkningar, signalräkningar.",
    "List themes, or preview one with --name.":
        "Lista teman, eller förhandsgranska ett med --name.",
    "List available output languages.":
        "Lista tillgängliga utskriftsspråk.",

    # ---- cmd_list / cmd_tick ----
    "(no tasks)":
        "(inga uppgifter)",
    "emitted {emitted} cron signal(s); ranked {ranked} task(s)":
        "skickade {emitted} cron-signal(er); rangordnade {ranked} uppgift(er)",

    # ---- table headers ----
    "ID":
        "ID",
    "PRI":
        "PRI",
    "BAR":
        "BAR",
    "SUBJECT":
        "ÄMNE",

    # ---- banner titles ----
    "T R I A G E   v{version}":
        "T R I A G E   v{version}",
    "T R I A G E   T I C K   v{version}":
        "T R I A G E   T I C K   v{version}",
    "T R I A G E   S T A T U S":
        "T R I A G E   S T A T U S",
    "theme preview: {name}":
        "förhandsvisning av tema: {name}",

    # ---- cmd_status sections ----
    "TOP 3":
        "TOPP 3",
    "TAGS ({n})":
        "TAGGAR ({n})",
    "ACTIVE SIGNALS ({n})":
        "AKTIVA SIGNALER ({n})",
    "total tasks: {tasks}    ranked: {ranked}":
        "totalt antal uppgifter: {tasks}    rangordnade: {ranked}",
    "(no tags)":
        "(inga taggar)",
    "(no active signals)":
        "(inga aktiva signaler)",

    # ---- cmd_why ----
    "task {id}: {subject}":
        "uppgift {id}: {subject}",
    "priority = {priority}":
        "prioritet = {priority}",

    # ---- errors + status messages ----
    "no task with id {id}":
        "ingen uppgift med id {id}",
    "warning: {message}":
        "varning: {message}",
    "unknown source: {source}. known: {known}":
        "okänd källa: {source}. kända: {known}",
    "polled {source}: emitted {emitted} signal(s)":
        "pollade {source}: skickade {emitted} signal(er)",
    "removed {id}":
        "tog bort {id}",
    "signal emitted: source={source} bump={bump} ttl={ttl}s affects={affects}":
        "signal skickad: källa={source} höjning={bump} ttl={ttl}s påverkar={affects}",
    "(all tasks)":
        "(alla uppgifter)",

    # ---- mock rows used in `triage theme --name X` preview ----
    "Critical hotfix":
        "Kritisk akutfix",
    "Deploy migration":
        "Distribuera migrering",
    "Catch up on email":
        "Hinna ifatt e-posten",

    # ---- lang subcommand ----
    "available languages (default: {default}):":
        "tillgängliga språk (standard: {default}):",
    "unknown language: {lang}. known: {known}":
        "okänt språk: {lang}. kända: {known}",
}
