# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Norsk bokmål — Norwegian (Bokmål) locale.

Norwegian bokmål — the more widely-written of Norway's two written
standards. Native-speaker contributions for nynorsk welcome via PR
under a separate locale code if desired.
"""

STRINGS: dict[str, str] = {
    "__native_name__": "Norsk",

    # ---- argparse: top-level ----
    "Meta-scheduler that watches signals and reorders its own queue.":
        "Meta-planlegger som overvåker signaler og ombestiller sin egen kø.",
    "Override TRIAGE_HOME (default: ~/.triage or $TRIAGE_HOME).":
        "Overstyr TRIAGE_HOME (standard: ~/.triage eller $TRIAGE_HOME).",
    "Output theme (default from $TRIAGE_THEME or {default}). Set NO_COLOR=1 to disable colors regardless of theme.":
        "Utskriftstema (standard fra $TRIAGE_THEME eller {default}). Sett NO_COLOR=1 for å deaktivere farger uansett tema.",
    "Force-disable ANSI color even on a TTY.":
        "Tving av ANSI-farge selv på en TTY.",
    "Append JSONL events to this path (default: $TRIAGE_LOG_FILE or {default}; falls back to {fallback} if unwritable).":
        "Legg JSONL-hendelser til denne stien (standard: $TRIAGE_LOG_FILE eller {default}; faller tilbake til {fallback} hvis ikke skrivbar).",
    "Disable JSONL event logging for this invocation.":
        "Deaktiver JSONL-hendelseslogging for denne kjøringen.",
    "Language for CLI output (default from $TRIAGE_LANG, $LANG, or 'en').":
        "Språk for CLI-utskrift (standard fra $TRIAGE_LANG, $LANG eller 'en').",

    # ---- argparse: subcommands ----
    "Add a task.":
        "Legg til en oppgave.",
    "Show the current priority order.":
        "Vis gjeldende prioritetsrekkefølge.",
    "Show one task's full record.":
        "Vis hele posten for én oppgave.",
    "Audit log of rule contributions for a task.":
        "Revisjonslogg over regelbidrag for en oppgave.",
    "Recompute priorities; print new order.":
        "Rekalkuler prioriteter; skriv ut ny rekkefølge.",
    "Invoke a network-bound signal source's poller.":
        "Kall pollern til en nettverksbundet signalkilde.",
    "Inject a manual signal (for external watchers like RunPodBoss).":
        "Injiser et manuelt signal (for eksterne overvåkere som RunPodBoss).",
    "Remove a task by id.":
        "Fjern en oppgave etter id.",
    "One-screen at-a-glance: top-3 tasks, tag counts, signal counts.":
        "Oversikt på én skjerm: topp-3 oppgaver, taggtellinger, signaltellinger.",
    "List themes, or preview one with --name.":
        "List temaer, eller forhåndsvis ett med --name.",
    "List available output languages.":
        "List tilgjengelige utskriftsspråk.",

    # ---- cmd_list / cmd_tick ----
    "(no tasks)":
        "(ingen oppgaver)",
    "emitted {emitted} cron signal(s); ranked {ranked} task(s)":
        "sendte ut {emitted} cron-signal(er); rangerte {ranked} oppgave(r)",

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
        "forhåndsvisning av tema: {name}",

    # ---- cmd_status sections ----
    "TOP 3":
        "TOPP 3",
    "TAGS ({n})":
        "TAGGER ({n})",
    "ACTIVE SIGNALS ({n})":
        "AKTIVE SIGNALER ({n})",
    "total tasks: {tasks}    ranked: {ranked}":
        "totalt antall oppgaver: {tasks}    rangert: {ranked}",
    "(no tags)":
        "(ingen tagger)",
    "(no active signals)":
        "(ingen aktive signaler)",

    # ---- cmd_why ----
    "task {id}: {subject}":
        "oppgave {id}: {subject}",
    "priority = {priority}":
        "prioritet = {priority}",

    # ---- errors + status messages ----
    "no task with id {id}":
        "ingen oppgave med id {id}",
    "warning: {message}":
        "advarsel: {message}",
    "unknown source: {source}. known: {known}":
        "ukjent kilde: {source}. kjente: {known}",
    "polled {source}: emitted {emitted} signal(s)":
        "pollet {source}: sendte ut {emitted} signal(er)",
    "removed {id}":
        "fjernet {id}",
    "signal emitted: source={source} bump={bump} ttl={ttl}s affects={affects}":
        "signal sendt: kilde={source} økning={bump} ttl={ttl}s påvirker={affects}",
    "(all tasks)":
        "(alle oppgaver)",

    # ---- mock rows used in `triage theme --name X` preview ----
    "Critical hotfix":
        "Kritisk hurtigfiks",
    "Deploy migration":
        "Distribuer migrering",
    "Catch up on email":
        "Ta igjen e-post",

    # ---- lang subcommand ----
    "available languages (default: {default}):":
        "tilgjengelige språk (standard: {default}):",
    "unknown language: {lang}. known: {known}":
        "ukjent språk: {lang}. kjente: {known}",
}
