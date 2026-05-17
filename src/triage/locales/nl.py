# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Nederlands — Dutch locale.

Northern-Dutch (Netherlands) register, broadly readable for Flemish
speakers as well. Native-speaker contributions welcome via PR.
"""

STRINGS: dict[str, str] = {
    "__native_name__": "Nederlands",

    # ---- argparse: top-level ----
    "Meta-scheduler that watches signals and reorders its own queue.":
        "Meta-scheduler die signalen volgt en zijn eigen wachtrij herordent.",
    "Override TRIAGE_HOME (default: ~/.triage or $TRIAGE_HOME).":
        "TRIAGE_HOME overschrijven (standaard: ~/.triage of $TRIAGE_HOME).",
    "Output theme (default from $TRIAGE_THEME or {default}). Set NO_COLOR=1 to disable colors regardless of theme.":
        "Uitvoerthema (standaard uit $TRIAGE_THEME of {default}). Zet NO_COLOR=1 om kleuren uit te schakelen ongeacht het thema.",
    "Force-disable ANSI color even on a TTY.":
        "ANSI-kleur expliciet uitschakelen, zelfs op een TTY.",
    "Append JSONL events to this path (default: $TRIAGE_LOG_FILE or {default}; falls back to {fallback} if unwritable).":
        "JSONL-gebeurtenissen aan dit pad toevoegen (standaard: $TRIAGE_LOG_FILE of {default}; valt terug op {fallback} als niet schrijfbaar).",
    "Disable JSONL event logging for this invocation.":
        "JSONL-gebeurtenislogboek uitschakelen voor deze aanroep.",
    "Language for CLI output (default from $TRIAGE_LANG, $LANG, or 'en').":
        "Taal voor CLI-uitvoer (standaard uit $TRIAGE_LANG, $LANG, of 'en').",

    # ---- argparse: subcommands ----
    "Add a task.":
        "Een taak toevoegen.",
    "Show the current priority order.":
        "De huidige prioriteitsvolgorde tonen.",
    "Show one task's full record.":
        "Het volledige record van één taak tonen.",
    "Audit log of rule contributions for a task.":
        "Auditlogboek van regelbijdragen voor een taak.",
    "Recompute priorities; print new order.":
        "Prioriteiten herberekenen; nieuwe volgorde afdrukken.",
    "Invoke a network-bound signal source's poller.":
        "De poller van een netwerkgebonden signaalbron aanroepen.",
    "Inject a manual signal (for external watchers like RunPodBoss).":
        "Een handmatig signaal injecteren (voor externe watchers zoals RunPodBoss).",
    "Remove a task by id.":
        "Een taak verwijderen op id.",
    "One-screen at-a-glance: top-3 tasks, tag counts, signal counts.":
        "Eén scherm in een oogopslag: top-3 taken, tagaantallen, signaalaantallen.",
    "List themes, or preview one with --name.":
        "Thema's opsommen, of een voorbeeld bekijken met --name.",
    "List available output languages.":
        "Beschikbare uitvoertalen opsommen.",

    # ---- cmd_list / cmd_tick ----
    "(no tasks)":
        "(geen taken)",
    "emitted {emitted} cron signal(s); ranked {ranked} task(s)":
        "{emitted} cron-signa(a)l(en) uitgezonden; {ranked} ta(a)k(en) gerangschikt",

    # ---- table headers ----
    "ID":
        "ID",
    "PRI":
        "PRI",
    "BAR":
        "BAR",
    "SUBJECT":
        "ONDERWERP",

    # ---- banner titles ----
    "T R I A G E   v{version}":
        "T R I A G E   v{version}",
    "T R I A G E   T I C K   v{version}":
        "T R I A G E   T I C K   v{version}",
    "T R I A G E   S T A T U S":
        "T R I A G E   S T A T U S",
    "theme preview: {name}":
        "themavoorbeeld: {name}",

    # ---- cmd_status sections ----
    "TOP 3":
        "TOP 3",
    "TAGS ({n})":
        "TAGS ({n})",
    "ACTIVE SIGNALS ({n})":
        "ACTIEVE SIGNALEN ({n})",
    "total tasks: {tasks}    ranked: {ranked}":
        "totaal taken: {tasks}    gerangschikt: {ranked}",
    "(no tags)":
        "(geen tags)",
    "(no active signals)":
        "(geen actieve signalen)",

    # ---- cmd_why ----
    "task {id}: {subject}":
        "taak {id}: {subject}",
    "priority = {priority}":
        "prioriteit = {priority}",

    # ---- errors + status messages ----
    "no task with id {id}":
        "geen taak met id {id}",
    "warning: {message}":
        "waarschuwing: {message}",
    "unknown source: {source}. known: {known}":
        "onbekende bron: {source}. bekend: {known}",
    "polled {source}: emitted {emitted} signal(s)":
        "{source} gepolld: {emitted} signa(a)l(en) uitgezonden",
    "removed {id}":
        "{id} verwijderd",
    "signal emitted: source={source} bump={bump} ttl={ttl}s affects={affects}":
        "signaal uitgezonden: bron={source} verhoging={bump} ttl={ttl}s raakt={affects}",
    "(all tasks)":
        "(alle taken)",

    # ---- mock rows used in `triage theme --name X` preview ----
    "Critical hotfix":
        "Kritieke hotfix",
    "Deploy migration":
        "Migratie uitrollen",
    "Catch up on email":
        "E-mail bijwerken",

    # ---- lang subcommand ----
    "available languages (default: {default}):":
        "beschikbare talen (standaard: {default}):",
    "unknown language: {lang}. known: {known}":
        "onbekende taal: {lang}. bekend: {known}",

    # ---- model-layer errors + warnings (L10) ----
    "cron expression must have 5 fields, got {got}: {expr}":
        "cron-expressie moet 5 velden hebben, kreeg {got}: {expr}",
    "cycle: removed edge {u} -> {v} (back-edge)":
        "cyclus: rand {u} -> {v} verwijderd (terugrand)",
    "self-block: {id} blocks itself; ignored":
        "zelfblokkering: {id} blokkeert zichzelf; genegeerd",
    "dangling blocker: {id} blocked_by {blocker} (unknown); ignored":
        "loshangende blokkeerder: {id} blocked_by {blocker} (onbekend); genegeerd",
    "triage: log path {path} is not writable; logging disabled (set TRIAGE_NO_LOG=1 to silence).":
        "triage: logpad {path} is niet schrijfbaar; loggen uitgeschakeld (zet TRIAGE_NO_LOG=1 om te dempen).",
    "triage: {default} not writable, logging to {fallback} instead (create + chown {default} to use the standard path).":
        "triage: {default} niet schrijfbaar, log nu naar {fallback} (maak + chown {default} aan om het standaardpad te gebruiken).",
    "triage: neither {default} nor {fallback} is writable; events will not be logged.":
        "triage: noch {default} noch {fallback} is schrijfbaar; gebeurtenissen worden niet gelogd.",
}
