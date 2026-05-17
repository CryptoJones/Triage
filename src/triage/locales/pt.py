# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Português — Portuguese locale.

European-Portuguese register with vocabulary acceptable to
Brazilian readers (e.g. "tarefa", "predefinido"). Native-speaker
contributions for pt-BR or pt-PT split welcome via PR.
"""

STRINGS: dict[str, str] = {
    "__native_name__": "Português",

    # ---- argparse: top-level ----
    "Meta-scheduler that watches signals and reorders its own queue.":
        "Meta-agendador que observa sinais e reordena a sua própria fila.",
    "Override TRIAGE_HOME (default: ~/.triage or $TRIAGE_HOME).":
        "Substitui TRIAGE_HOME (predefinido: ~/.triage ou $TRIAGE_HOME).",
    "Output theme (default from $TRIAGE_THEME or {default}). Set NO_COLOR=1 to disable colors regardless of theme.":
        "Tema de saída (predefinido de $TRIAGE_THEME ou {default}). Define NO_COLOR=1 para desativar as cores independentemente do tema.",
    "Force-disable ANSI color even on a TTY.":
        "Forçar a desativação da cor ANSI mesmo num TTY.",
    "Append JSONL events to this path (default: $TRIAGE_LOG_FILE or {default}; falls back to {fallback} if unwritable).":
        "Acrescentar eventos JSONL a este caminho (predefinido: $TRIAGE_LOG_FILE ou {default}; recorre a {fallback} se não for gravável).",
    "Disable JSONL event logging for this invocation.":
        "Desativar o registo de eventos JSONL para esta invocação.",
    "Language for CLI output (default from $TRIAGE_LANG, $LANG, or 'en').":
        "Idioma para a saída CLI (predefinido de $TRIAGE_LANG, $LANG ou 'en').",

    # ---- argparse: subcommands ----
    "Add a task.":
        "Adicionar uma tarefa.",
    "Show the current priority order.":
        "Mostrar a ordem de prioridade atual.",
    "Show one task's full record.":
        "Mostrar o registo completo de uma tarefa.",
    "Audit log of rule contributions for a task.":
        "Registo de auditoria das contribuições de regras para uma tarefa.",
    "Recompute priorities; print new order.":
        "Recalcular prioridades; imprimir a nova ordem.",
    "Invoke a network-bound signal source's poller.":
        "Invocar o sondador de uma fonte de sinais baseada em rede.",
    "Inject a manual signal (for external watchers like RunPodBoss).":
        "Injetar um sinal manual (para observadores externos como o RunPodBoss).",
    "Remove a task by id.":
        "Remover uma tarefa por id.",
    "One-screen at-a-glance: top-3 tasks, tag counts, signal counts.":
        "Vista de um ecrã: as 3 tarefas principais, contagens de etiquetas, contagens de sinais.",
    "List themes, or preview one with --name.":
        "Listar temas, ou pré-visualizar um com --name.",
    "List available output languages.":
        "Listar idiomas de saída disponíveis.",

    # ---- cmd_list / cmd_tick ----
    "(no tasks)":
        "(sem tarefas)",
    "emitted {emitted} cron signal(s); ranked {ranked} task(s)":
        "emitidos {emitted} sinal(ais) cron; ordenadas {ranked} tarefa(s)",

    # ---- table headers ----
    "ID":
        "ID",
    "PRI":
        "PRI",
    "BAR":
        "BAR",
    "SUBJECT":
        "ASSUNTO",

    # ---- banner titles ----
    "T R I A G E   v{version}":
        "T R I A G E   v{version}",
    "T R I A G E   T I C K   v{version}":
        "T R I A G E   T I C K   v{version}",
    "T R I A G E   S T A T U S":
        "T R I A G E   E S T A D O",
    "theme preview: {name}":
        "pré-visualização do tema: {name}",

    # ---- cmd_status sections ----
    "TOP 3":
        "TOP 3",
    "TAGS ({n})":
        "ETIQUETAS ({n})",
    "ACTIVE SIGNALS ({n})":
        "SINAIS ATIVOS ({n})",
    "total tasks: {tasks}    ranked: {ranked}":
        "tarefas totais: {tasks}    ordenadas: {ranked}",
    "(no tags)":
        "(sem etiquetas)",
    "(no active signals)":
        "(sem sinais ativos)",

    # ---- cmd_why ----
    "task {id}: {subject}":
        "tarefa {id}: {subject}",
    "priority = {priority}":
        "prioridade = {priority}",

    # ---- errors + status messages ----
    "no task with id {id}":
        "nenhuma tarefa com id {id}",
    "warning: {message}":
        "aviso: {message}",
    "unknown source: {source}. known: {known}":
        "fonte desconhecida: {source}. conhecidas: {known}",
    "polled {source}: emitted {emitted} signal(s)":
        "{source} sondado: emitidos {emitted} sinal(ais)",
    "removed {id}":
        "{id} removido",
    "signal emitted: source={source} bump={bump} ttl={ttl}s affects={affects}":
        "sinal emitido: fonte={source} incremento={bump} ttl={ttl}s afeta={affects}",
    "(all tasks)":
        "(todas as tarefas)",

    # ---- mock rows used in `triage theme --name X` preview ----
    "Critical hotfix":
        "Correção crítica urgente",
    "Deploy migration":
        "Implementar migração",
    "Catch up on email":
        "Pôr o email em dia",

    # ---- lang subcommand ----
    "available languages (default: {default}):":
        "idiomas disponíveis (predefinido: {default}):",
    "unknown language: {lang}. known: {known}":
        "idioma desconhecido: {lang}. conhecidos: {known}",

    # ---- model-layer errors + warnings (L10) ----
    "cron expression must have 5 fields, got {got}: {expr}":
        "a expressao cron deve ter 5 campos, recebidos {got}: {expr}",
    "cycle: removed edge {u} -> {v} (back-edge)":
        "ciclo: aresta {u} -> {v} removida (aresta de retorno)",
    "self-block: {id} blocks itself; ignored":
        "auto-bloqueio: {id} bloqueia-se a si proprio; ignorado",
    "dangling blocker: {id} blocked_by {blocker} (unknown); ignored":
        "bloqueador pendente: {id} blocked_by {blocker} (desconhecido); ignorado",
    "triage: log path {path} is not writable; logging disabled (set TRIAGE_NO_LOG=1 to silence).":
        "triage: caminho do registo {path} nao e gravavel; registo desactivado (define TRIAGE_NO_LOG=1 para silenciar).",
    "triage: {default} not writable, logging to {fallback} instead (create + chown {default} to use the standard path).":
        "triage: {default} nao e gravavel, regista em {fallback} (cria + chown {default} para usar o caminho padrao).",
    "triage: neither {default} nor {fallback} is writable; events will not be logged.":
        "triage: nem {default} nem {fallback} sao gravaveis; os eventos nao serao registados.",
}
