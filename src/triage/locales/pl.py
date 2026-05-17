# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Polski — Polish locale.

Standard Polish (Poland). Native-speaker contributions welcome via PR.
"""

STRINGS: dict[str, str] = {
    "__native_name__": "Polski",

    # ---- argparse: top-level ----
    "Meta-scheduler that watches signals and reorders its own queue.":
        "Meta-planista, który obserwuje sygnały i przeszereguje własną kolejkę.",
    "Override TRIAGE_HOME (default: ~/.triage or $TRIAGE_HOME).":
        "Nadpisuje TRIAGE_HOME (domyślnie: ~/.triage lub $TRIAGE_HOME).",
    "Output theme (default from $TRIAGE_THEME or {default}). Set NO_COLOR=1 to disable colors regardless of theme.":
        "Motyw wyjścia (domyślnie z $TRIAGE_THEME lub {default}). Ustaw NO_COLOR=1, aby wyłączyć kolory niezależnie od motywu.",
    "Force-disable ANSI color even on a TTY.":
        "Wymusza wyłączenie koloru ANSI nawet na TTY.",
    "Append JSONL events to this path (default: $TRIAGE_LOG_FILE or {default}; falls back to {fallback} if unwritable).":
        "Dopisuje zdarzenia JSONL do tej ścieżki (domyślnie: $TRIAGE_LOG_FILE lub {default}; przełącza się na {fallback}, jeśli niezapisywalna).",
    "Disable JSONL event logging for this invocation.":
        "Wyłącza dziennik zdarzeń JSONL dla tego wywołania.",
    "Language for CLI output (default from $TRIAGE_LANG, $LANG, or 'en').":
        "Język wyjścia CLI (domyślnie z $TRIAGE_LANG, $LANG lub 'en').",

    # ---- argparse: subcommands ----
    "Add a task.":
        "Dodaj zadanie.",
    "Show the current priority order.":
        "Pokaż bieżącą kolejność priorytetów.",
    "Show one task's full record.":
        "Pokaż pełny rekord jednego zadania.",
    "Audit log of rule contributions for a task.":
        "Dziennik audytu wkładów reguł dla zadania.",
    "Recompute priorities; print new order.":
        "Przelicz priorytety; wypisz nową kolejność.",
    "Invoke a network-bound signal source's poller.":
        "Wywołaj odpytywacz sieciowego źródła sygnału.",
    "Inject a manual signal (for external watchers like RunPodBoss).":
        "Wstrzyknij ręczny sygnał (dla zewnętrznych obserwatorów jak RunPodBoss).",
    "Remove a task by id.":
        "Usuń zadanie po id.",
    "One-screen at-a-glance: top-3 tasks, tag counts, signal counts.":
        "Widok jednego ekranu: top-3 zadania, liczniki tagów, liczniki sygnałów.",
    "List themes, or preview one with --name.":
        "Wypisz motywy lub podejrzyj jeden za pomocą --name.",
    "List available output languages.":
        "Wypisz dostępne języki wyjścia.",

    # ---- cmd_list / cmd_tick ----
    "(no tasks)":
        "(brak zadań)",
    "emitted {emitted} cron signal(s); ranked {ranked} task(s)":
        "wyemitowano {emitted} sygnał(ów) cron; uszeregowano {ranked} zadań",

    # ---- table headers ----
    "ID":
        "ID",
    "PRI":
        "PRI",
    "BAR":
        "BAR",
    "SUBJECT":
        "TEMAT",

    # ---- banner titles ----
    "T R I A G E   v{version}":
        "T R I A G E   v{version}",
    "T R I A G E   T I C K   v{version}":
        "T R I A G E   T I C K   v{version}",
    "T R I A G E   S T A T U S":
        "T R I A G E   S T A T U S",
    "theme preview: {name}":
        "podgląd motywu: {name}",

    # ---- cmd_status sections ----
    "TOP 3":
        "TOP 3",
    "TAGS ({n})":
        "TAGI ({n})",
    "ACTIVE SIGNALS ({n})":
        "AKTYWNE SYGNAŁY ({n})",
    "total tasks: {tasks}    ranked: {ranked}":
        "wszystkie zadania: {tasks}    uszeregowane: {ranked}",
    "(no tags)":
        "(brak tagów)",
    "(no active signals)":
        "(brak aktywnych sygnałów)",

    # ---- cmd_why ----
    "task {id}: {subject}":
        "zadanie {id}: {subject}",
    "priority = {priority}":
        "priorytet = {priority}",

    # ---- errors + status messages ----
    "no task with id {id}":
        "brak zadania o id {id}",
    "warning: {message}":
        "ostrzeżenie: {message}",
    "unknown source: {source}. known: {known}":
        "nieznane źródło: {source}. znane: {known}",
    "polled {source}: emitted {emitted} signal(s)":
        "odpytano {source}: wyemitowano {emitted} sygnał(ów)",
    "removed {id}":
        "usunięto {id}",
    "signal emitted: source={source} bump={bump} ttl={ttl}s affects={affects}":
        "wyemitowano sygnał: źródło={source} podbicie={bump} ttl={ttl}s wpływa na={affects}",
    "(all tasks)":
        "(wszystkie zadania)",

    # ---- mock rows used in `triage theme --name X` preview ----
    "Critical hotfix":
        "Krytyczna poprawka",
    "Deploy migration":
        "Wdrożyć migrację",
    "Catch up on email":
        "Nadrobić e-maile",

    # ---- lang subcommand ----
    "available languages (default: {default}):":
        "dostępne języki (domyślnie: {default}):",
    "unknown language: {lang}. known: {known}":
        "nieznany język: {lang}. znane: {known}",

    # ---- model-layer errors + warnings (L10) ----
    "cron expression must have 5 fields, got {got}: {expr}":
        "wyrazenie cron musi miec 5 pol, otrzymano {got}: {expr}",
    "cycle: removed edge {u} -> {v} (back-edge)":
        "cykl: usunieto krawedz {u} -> {v} (krawedz wsteczna)",
    "self-block: {id} blocks itself; ignored":
        "samoblokada: {id} blokuje sama siebie; zignorowano",
    "dangling blocker: {id} blocked_by {blocker} (unknown); ignored":
        "wiszacy blokujacy: {id} blocked_by {blocker} (nieznany); zignorowano",
    "triage: log path {path} is not writable; logging disabled (set TRIAGE_NO_LOG=1 to silence).":
        "triage: sciezka dziennika {path} nie jest zapisywalna; logowanie wylaczone (ustaw TRIAGE_NO_LOG=1, aby wyciszyc).",
    "triage: {default} not writable, logging to {fallback} instead (create + chown {default} to use the standard path).":
        "triage: {default} nie jest zapisywalny, loguje do {fallback} (utworz + chown {default}, aby uzyc sciezki standardowej).",
    "triage: neither {default} nor {fallback} is writable; events will not be logged.":
        "triage: ani {default}, ani {fallback} nie jest zapisywalny; zdarzenia nie beda rejestrowane.",
}
