# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Suomi — Finnish locale.

Standard Finnish (Finland). Native-speaker contributions welcome via PR.
"""

STRINGS: dict[str, str] = {
    "__native_name__": "Suomi",

    # ---- argparse: top-level ----
    "Meta-scheduler that watches signals and reorders its own queue.":
        "Meta-aikataulutin, joka tarkkailee signaaleja ja järjestää oman jononsa uudelleen.",
    "Override TRIAGE_HOME (default: ~/.triage or $TRIAGE_HOME).":
        "Ohita TRIAGE_HOME (oletus: ~/.triage tai $TRIAGE_HOME).",
    "Output theme (default from $TRIAGE_THEME or {default}). Set NO_COLOR=1 to disable colors regardless of theme.":
        "Tulosteen teema (oletus $TRIAGE_THEME tai {default}). Aseta NO_COLOR=1 poistaaksesi värit teemasta riippumatta.",
    "Force-disable ANSI color even on a TTY.":
        "Pakota ANSI-väri pois käytöstä myös TTY:llä.",
    "Append JSONL events to this path (default: $TRIAGE_LOG_FILE or {default}; falls back to {fallback} if unwritable).":
        "Lisää JSONL-tapahtumat tähän polkuun (oletus: $TRIAGE_LOG_FILE tai {default}; palautuu polkuun {fallback}, jos ei kirjoituskelpoinen).",
    "Disable JSONL event logging for this invocation.":
        "Poista JSONL-tapahtumaloki tämän kutsun ajaksi.",
    "Language for CLI output (default from $TRIAGE_LANG, $LANG, or 'en').":
        "CLI-tulosteen kieli (oletus $TRIAGE_LANG, $LANG tai 'en').",

    # ---- argparse: subcommands ----
    "Add a task.":
        "Lisää tehtävä.",
    "Show the current priority order.":
        "Näytä nykyinen prioriteettijärjestys.",
    "Show one task's full record.":
        "Näytä yhden tehtävän koko tietue.",
    "Audit log of rule contributions for a task.":
        "Tarkastusloki tehtävän sääntöjen vaikutuksista.",
    "Recompute priorities; print new order.":
        "Laske prioriteetit uudelleen; tulosta uusi järjestys.",
    "Invoke a network-bound signal source's poller.":
        "Kutsu verkkoon sitoutuneen signaalilähteen kyselijää.",
    "Inject a manual signal (for external watchers like RunPodBoss).":
        "Lisää manuaalinen signaali (ulkoisia tarkkailijoita kuten RunPodBoss varten).",
    "Remove a task by id.":
        "Poista tehtävä id:n perusteella.",
    "One-screen at-a-glance: top-3 tasks, tag counts, signal counts.":
        "Yhden ruudun pikakatsaus: top-3 tehtävää, tunnistemäärät, signaalimäärät.",
    "List themes, or preview one with --name.":
        "Listaa teemat tai esikatsele yhtä --name-valitsimella.",
    "List available output languages.":
        "Listaa käytettävissä olevat tulostuskielet.",

    # ---- cmd_list / cmd_tick ----
    "(no tasks)":
        "(ei tehtäviä)",
    "emitted {emitted} cron signal(s); ranked {ranked} task(s)":
        "lähetettiin {emitted} cron-signaali(a); luokiteltiin {ranked} tehtävä(ä)",

    # ---- table headers ----
    "ID":
        "ID",
    "PRI":
        "PRI",
    "BAR":
        "BAR",
    "SUBJECT":
        "AIHE",

    # ---- banner titles ----
    "T R I A G E   v{version}":
        "T R I A G E   v{version}",
    "T R I A G E   T I C K   v{version}":
        "T R I A G E   T I C K   v{version}",
    "T R I A G E   S T A T U S":
        "T R I A G E   T I L A",
    "theme preview: {name}":
        "teeman esikatselu: {name}",

    # ---- cmd_status sections ----
    "TOP 3":
        "TOP 3",
    "TAGS ({n})":
        "TUNNISTEET ({n})",
    "ACTIVE SIGNALS ({n})":
        "AKTIIVISET SIGNAALIT ({n})",
    "total tasks: {tasks}    ranked: {ranked}":
        "tehtäviä yhteensä: {tasks}    luokiteltu: {ranked}",
    "(no tags)":
        "(ei tunnisteita)",
    "(no active signals)":
        "(ei aktiivisia signaaleja)",

    # ---- cmd_why ----
    "task {id}: {subject}":
        "tehtävä {id}: {subject}",
    "priority = {priority}":
        "prioriteetti = {priority}",

    # ---- errors + status messages ----
    "no task with id {id}":
        "ei tehtävää id:llä {id}",
    "warning: {message}":
        "varoitus: {message}",
    "unknown source: {source}. known: {known}":
        "tuntematon lähde: {source}. tunnetut: {known}",
    "polled {source}: emitted {emitted} signal(s)":
        "kysely {source}: lähetettiin {emitted} signaali(a)",
    "removed {id}":
        "poistettiin {id}",
    "signal emitted: source={source} bump={bump} ttl={ttl}s affects={affects}":
        "signaali lähetettiin: lähde={source} korotus={bump} ttl={ttl}s vaikuttaa={affects}",
    "(all tasks)":
        "(kaikki tehtävät)",

    # ---- mock rows used in `triage theme --name X` preview ----
    "Critical hotfix":
        "Kriittinen pikakorjaus",
    "Deploy migration":
        "Toteuta migraatio",
    "Catch up on email":
        "Käy sähköpostit läpi",

    # ---- lang subcommand ----
    "available languages (default: {default}):":
        "käytettävissä olevat kielet (oletus: {default}):",
    "unknown language: {lang}. known: {known}":
        "tuntematon kieli: {lang}. tunnetut: {known}",

    # ---- model-layer errors + warnings (L10) ----
    "cron expression must have 5 fields, got {got}: {expr}":
        "cron-lausekkeessa pitaa olla 5 kenttaa, saatiin {got}: {expr}",
    "cycle: removed edge {u} -> {v} (back-edge)":
        "sykli: poistettiin reuna {u} -> {v} (taaksepainreuna)",
    "self-block: {id} blocks itself; ignored":
        "itse-esto: {id} estaa itsensa; ohitettu",
    "dangling blocker: {id} blocked_by {blocker} (unknown); ignored":
        "irrallinen estaja: {id} blocked_by {blocker} (tuntematon); ohitettu",
    "triage: log path {path} is not writable; logging disabled (set TRIAGE_NO_LOG=1 to silence).":
        "triage: lokipolku {path} ei ole kirjoituskelpoinen; loki pois kaytosta (aseta TRIAGE_NO_LOG=1 vaimentaaksesi).",
    "triage: {default} not writable, logging to {fallback} instead (create + chown {default} to use the standard path).":
        "triage: {default} ei kirjoituskelpoinen, kirjataan {fallback} sijaan (luo + chown {default} kayttaaksesi vakiopolkua).",
    "triage: neither {default} nor {fallback} is writable; events will not be logged.":
        "triage: kumpikaan {default} tai {fallback} ei ole kirjoituskelpoinen; tapahtumia ei kirjata.",
}
