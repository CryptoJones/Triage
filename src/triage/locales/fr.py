# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Français — French locale.

Translations done by Claude with hands-on review for tone matching
Triage's CLI register. Native-speaker contributions welcome via PR.
"""

STRINGS: dict[str, str] = {
    "__native_name__": "Français",

    # ---- argparse: top-level ----
    "Meta-scheduler that watches signals and reorders its own queue.":
        "Méta-planificateur qui surveille des signaux et réordonne sa propre file.",
    "Override TRIAGE_HOME (default: ~/.triage or $TRIAGE_HOME).":
        "Remplace TRIAGE_HOME (par défaut : ~/.triage ou $TRIAGE_HOME).",
    "Output theme (default from $TRIAGE_THEME or {default}). Set NO_COLOR=1 to disable colors regardless of theme.":
        "Thème de sortie (par défaut depuis $TRIAGE_THEME ou {default}). Définir NO_COLOR=1 désactive les couleurs quel que soit le thème.",
    "Force-disable ANSI color even on a TTY.":
        "Désactiver de force la couleur ANSI même sur un TTY.",
    "Append JSONL events to this path (default: $TRIAGE_LOG_FILE or {default}; falls back to {fallback} if unwritable).":
        "Ajouter les événements JSONL à ce chemin (par défaut : $TRIAGE_LOG_FILE ou {default} ; bascule sur {fallback} si non inscriptible).",
    "Disable JSONL event logging for this invocation.":
        "Désactiver la journalisation JSONL pour cette invocation.",
    "Language for CLI output (default from $TRIAGE_LANG, $LANG, or 'en').":
        "Langue pour la sortie CLI (par défaut depuis $TRIAGE_LANG, $LANG ou 'en').",

    # ---- argparse: subcommands ----
    "Add a task.":
        "Ajouter une tâche.",
    "Show the current priority order.":
        "Afficher l'ordre de priorité actuel.",
    "Show one task's full record.":
        "Afficher l'enregistrement complet d'une tâche.",
    "Audit log of rule contributions for a task.":
        "Journal d'audit des contributions de règles pour une tâche.",
    "Recompute priorities; print new order.":
        "Recalculer les priorités ; afficher le nouvel ordre.",
    "Invoke a network-bound signal source's poller.":
        "Invoquer le scrutateur d'une source de signaux réseau.",
    "Inject a manual signal (for external watchers like RunPodBoss).":
        "Injecter un signal manuel (pour des observateurs externes comme RunPodBoss).",
    "Remove a task by id.":
        "Supprimer une tâche par id.",
    "One-screen at-a-glance: top-3 tasks, tag counts, signal counts.":
        "Aperçu sur un écran : les 3 tâches principales, comptages d'étiquettes, comptages de signaux.",
    "List themes, or preview one with --name.":
        "Lister les thèmes, ou en prévisualiser un avec --name.",
    "List available output languages.":
        "Lister les langues de sortie disponibles.",

    # ---- cmd_list / cmd_tick ----
    "(no tasks)":
        "(aucune tâche)",
    "emitted {emitted} cron signal(s); ranked {ranked} task(s)":
        "{emitted} signal(aux) cron émis ; {ranked} tâche(s) classée(s)",

    # ---- table headers ----
    "ID":
        "ID",
    "PRI":
        "PRI",
    "BAR":
        "BAR",
    "SUBJECT":
        "SUJET",

    # ---- banner titles ----
    "T R I A G E   v{version}":
        "T R I A G E   v{version}",
    "T R I A G E   T I C K   v{version}":
        "T R I A G E   T I C K   v{version}",
    "T R I A G E   S T A T U S":
        "T R I A G E   É T A T",
    "theme preview: {name}":
        "aperçu du thème : {name}",

    # ---- cmd_status sections ----
    "TOP 3":
        "TOP 3",
    "TAGS ({n})":
        "ÉTIQUETTES ({n})",
    "ACTIVE SIGNALS ({n})":
        "SIGNAUX ACTIFS ({n})",
    "total tasks: {tasks}    ranked: {ranked}":
        "tâches totales : {tasks}    classées : {ranked}",
    "(no tags)":
        "(aucune étiquette)",
    "(no active signals)":
        "(aucun signal actif)",

    # ---- cmd_why ----
    "task {id}: {subject}":
        "tâche {id} : {subject}",
    "priority = {priority}":
        "priorité = {priority}",

    # ---- errors + status messages ----
    "no task with id {id}":
        "aucune tâche avec id {id}",
    "warning: {message}":
        "avertissement : {message}",
    "unknown source: {source}. known: {known}":
        "source inconnue : {source}. connues : {known}",
    "polled {source}: emitted {emitted} signal(s)":
        "{source} sondée : {emitted} signal(aux) émis",
    "removed {id}":
        "supprimé {id}",
    "signal emitted: source={source} bump={bump} ttl={ttl}s affects={affects}":
        "signal émis : source={source} incrément={bump} ttl={ttl}s affecte={affects}",
    "(all tasks)":
        "(toutes les tâches)",

    # ---- mock rows used in `triage theme --name X` preview ----
    "Critical hotfix":
        "Correctif critique urgent",
    "Deploy migration":
        "Déployer la migration",
    "Catch up on email":
        "Rattraper les courriels",

    # ---- lang subcommand ----
    "available languages (default: {default}):":
        "langues disponibles (par défaut : {default}) :",
    "unknown language: {lang}. known: {known}":
        "langue inconnue : {lang}. connues : {known}",

    # ---- model-layer errors + warnings (L10) ----
    "cron expression must have 5 fields, got {got}: {expr}":
        "l'expression cron doit avoir 5 champs, recus {got} : {expr}",
    "cycle: removed edge {u} -> {v} (back-edge)":
        "cycle : arete {u} -> {v} supprimee (arete arriere)",
    "self-block: {id} blocks itself; ignored":
        "auto-blocage : {id} se bloque elle-meme ; ignore",
    "dangling blocker: {id} blocked_by {blocker} (unknown); ignored":
        "bloqueur orphelin : {id} blocked_by {blocker} (inconnu) ; ignore",
    "triage: log path {path} is not writable; logging disabled (set TRIAGE_NO_LOG=1 to silence).":
        "triage : le chemin du journal {path} n'est pas accessible en ecriture ; journalisation desactivee (definissez TRIAGE_NO_LOG=1 pour silencer).",
    "triage: {default} not writable, logging to {fallback} instead (create + chown {default} to use the standard path).":
        "triage : {default} non accessible en ecriture, journalisation dans {fallback} a la place (creez + chown {default} pour utiliser le chemin standard).",
    "triage: neither {default} nor {fallback} is writable; events will not be logged.":
        "triage : ni {default} ni {fallback} n'est accessible en ecriture ; les evenements ne seront pas journalises.",
}
