# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Español — Spanish locale.

Translations done by Claude with hands-on review for tone matching
Triage's CLI register (terse, technical, lower-case command output,
sentence-case banners). Native-speaker contributions welcome via PR.
"""

STRINGS: dict[str, str] = {
    "__native_name__": "Español",

    # ---- argparse: top-level ----
    "Meta-scheduler that watches signals and reorders its own queue.":
        "Meta-planificador que observa señales y reordena su propia cola.",
    "Override TRIAGE_HOME (default: ~/.triage or $TRIAGE_HOME).":
        "Reemplaza TRIAGE_HOME (predeterminado: ~/.triage o $TRIAGE_HOME).",
    "Output theme (default from $TRIAGE_THEME or {default}). Set NO_COLOR=1 to disable colors regardless of theme.":
        "Tema de salida (predeterminado de $TRIAGE_THEME o {default}). Define NO_COLOR=1 para desactivar colores independientemente del tema.",
    "Force-disable ANSI color even on a TTY.":
        "Forzar la desactivación del color ANSI incluso en una TTY.",
    "Append JSONL events to this path (default: $TRIAGE_LOG_FILE or {default}; falls back to {fallback} if unwritable).":
        "Añadir eventos JSONL a esta ruta (predeterminado: $TRIAGE_LOG_FILE o {default}; recurre a {fallback} si no se puede escribir).",
    "Disable JSONL event logging for this invocation.":
        "Desactivar el registro de eventos JSONL para esta invocación.",
    "Language for CLI output (default from $TRIAGE_LANG, $LANG, or 'en').":
        "Idioma de la salida CLI (predeterminado de $TRIAGE_LANG, $LANG o 'en').",

    # ---- argparse: subcommands ----
    "Add a task.":
        "Añadir una tarea.",
    "Show the current priority order.":
        "Mostrar el orden de prioridad actual.",
    "Show one task's full record.":
        "Mostrar el registro completo de una tarea.",
    "Audit log of rule contributions for a task.":
        "Registro de auditoría de las contribuciones de reglas para una tarea.",
    "Recompute priorities; print new order.":
        "Recalcular prioridades; imprimir el nuevo orden.",
    "Invoke a network-bound signal source's poller.":
        "Invocar el sondeador de una fuente de señales basada en red.",
    "Inject a manual signal (for external watchers like RunPodBoss).":
        "Inyectar una señal manual (para observadores externos como RunPodBoss).",
    "Remove a task by id.":
        "Eliminar una tarea por id.",
    "One-screen at-a-glance: top-3 tasks, tag counts, signal counts.":
        "Vista de una pantalla: las 3 tareas principales, recuentos de etiquetas, recuentos de señales.",
    "List themes, or preview one with --name.":
        "Listar temas, o previsualizar uno con --name.",
    "List available output languages.":
        "Listar los idiomas de salida disponibles.",

    # ---- cmd_list / cmd_tick ----
    "(no tasks)":
        "(sin tareas)",
    "emitted {emitted} cron signal(s); ranked {ranked} task(s)":
        "se emitieron {emitted} señal(es) cron; se ordenaron {ranked} tarea(s)",

    # ---- table headers ----
    "ID":
        "ID",
    "PRI":
        "PRI",
    "BAR":
        "BAR",
    "SUBJECT":
        "ASUNTO",

    # ---- banner titles ----
    "T R I A G E   v{version}":
        "T R I A G E   v{version}",
    "T R I A G E   T I C K   v{version}":
        "T R I A G E   T I C K   v{version}",
    "T R I A G E   S T A T U S":
        "T R I A G E   E S T A D O",
    "theme preview: {name}":
        "previsualización del tema: {name}",

    # ---- cmd_status sections ----
    "TOP 3":
        "TOP 3",
    "TAGS ({n})":
        "ETIQUETAS ({n})",
    "ACTIVE SIGNALS ({n})":
        "SEÑALES ACTIVAS ({n})",
    "total tasks: {tasks}    ranked: {ranked}":
        "tareas totales: {tasks}    ordenadas: {ranked}",
    "(no tags)":
        "(sin etiquetas)",
    "(no active signals)":
        "(sin señales activas)",

    # ---- cmd_why ----
    "task {id}: {subject}":
        "tarea {id}: {subject}",
    "priority = {priority}":
        "prioridad = {priority}",

    # ---- errors + status messages ----
    "no task with id {id}":
        "ninguna tarea con id {id}",
    "warning: {message}":
        "advertencia: {message}",
    "unknown source: {source}. known: {known}":
        "fuente desconocida: {source}. conocidas: {known}",
    "polled {source}: emitted {emitted} signal(s)":
        "sondeado {source}: se emitieron {emitted} señal(es)",
    "removed {id}":
        "eliminado {id}",
    "signal emitted: source={source} bump={bump} ttl={ttl}s affects={affects}":
        "señal emitida: fuente={source} incremento={bump} ttl={ttl}s afecta={affects}",
    "(all tasks)":
        "(todas las tareas)",

    # ---- mock rows used in `triage theme --name X` preview ----
    "Critical hotfix":
        "Corrección urgente crítica",
    "Deploy migration":
        "Desplegar migración",
    "Catch up on email":
        "Ponerse al día con el correo",

    # ---- lang subcommand ----
    "available languages (default: {default}):":
        "idiomas disponibles (predeterminado: {default}):",
    "unknown language: {lang}. known: {known}":
        "idioma desconocido: {lang}. conocidos: {known}",
}
