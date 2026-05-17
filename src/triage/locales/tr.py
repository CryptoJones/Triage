# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Türkçe — Turkish locale.

Standard Turkish (Turkey). Native-speaker contributions welcome via PR.
"""

STRINGS: dict[str, str] = {
    "__native_name__": "Türkçe",

    # ---- argparse: top-level ----
    "Meta-scheduler that watches signals and reorders its own queue.":
        "Sinyalleri izleyen ve kendi kuyruğunu yeniden sıralayan meta-zamanlayıcı.",
    "Override TRIAGE_HOME (default: ~/.triage or $TRIAGE_HOME).":
        "TRIAGE_HOME değerini geçersiz kıl (varsayılan: ~/.triage veya $TRIAGE_HOME).",
    "Output theme (default from $TRIAGE_THEME or {default}). Set NO_COLOR=1 to disable colors regardless of theme.":
        "Çıktı teması (varsayılan $TRIAGE_THEME veya {default} kaynaklı). Temadan bağımsız olarak renkleri devre dışı bırakmak için NO_COLOR=1 ayarlayın.",
    "Force-disable ANSI color even on a TTY.":
        "TTY üzerinde bile ANSI rengini zorla devre dışı bırak.",
    "Append JSONL events to this path (default: $TRIAGE_LOG_FILE or {default}; falls back to {fallback} if unwritable).":
        "JSONL olaylarını bu yola ekle (varsayılan: $TRIAGE_LOG_FILE veya {default}; yazılamıyorsa {fallback}'a düşer).",
    "Disable JSONL event logging for this invocation.":
        "Bu çağrı için JSONL olay günlüğünü devre dışı bırak.",
    "Language for CLI output (default from $TRIAGE_LANG, $LANG, or 'en').":
        "CLI çıktısı için dil (varsayılan $TRIAGE_LANG, $LANG veya 'en' kaynaklı).",

    # ---- argparse: subcommands ----
    "Add a task.":
        "Bir görev ekle.",
    "Show the current priority order.":
        "Mevcut öncelik sırasını göster.",
    "Show one task's full record.":
        "Bir görevin tam kaydını göster.",
    "Audit log of rule contributions for a task.":
        "Bir görev için kural katkılarının denetim günlüğü.",
    "Recompute priorities; print new order.":
        "Öncelikleri yeniden hesapla; yeni sırayı yazdır.",
    "Invoke a network-bound signal source's poller.":
        "Ağa bağlı bir sinyal kaynağının yoklayıcısını çağır.",
    "Inject a manual signal (for external watchers like RunPodBoss).":
        "Manuel sinyal enjekte et (RunPodBoss gibi harici izleyiciler için).",
    "Remove a task by id.":
        "Bir görevi id'ye göre kaldır.",
    "One-screen at-a-glance: top-3 tasks, tag counts, signal counts.":
        "Tek ekran bakışta: ilk 3 görev, etiket sayıları, sinyal sayıları.",
    "List themes, or preview one with --name.":
        "Temaları listele veya --name ile birini önizle.",
    "List available output languages.":
        "Mevcut çıktı dillerini listele.",

    # ---- cmd_list / cmd_tick ----
    "(no tasks)":
        "(görev yok)",
    "emitted {emitted} cron signal(s); ranked {ranked} task(s)":
        "{emitted} cron sinyali yayıldı; {ranked} görev sıralandı",

    # ---- table headers ----
    "ID":
        "ID",
    "PRI":
        "PRI",
    "BAR":
        "BAR",
    "SUBJECT":
        "KONU",

    # ---- banner titles ----
    "T R I A G E   v{version}":
        "T R I A G E   v{version}",
    "T R I A G E   T I C K   v{version}":
        "T R I A G E   T I C K   v{version}",
    "T R I A G E   S T A T U S":
        "T R I A G E   D U R U M",
    "theme preview: {name}":
        "tema önizlemesi: {name}",

    # ---- cmd_status sections ----
    "TOP 3":
        "İLK 3",
    "TAGS ({n})":
        "ETİKETLER ({n})",
    "ACTIVE SIGNALS ({n})":
        "AKTİF SİNYALLER ({n})",
    "total tasks: {tasks}    ranked: {ranked}":
        "toplam görev: {tasks}    sıralanan: {ranked}",
    "(no tags)":
        "(etiket yok)",
    "(no active signals)":
        "(aktif sinyal yok)",

    # ---- cmd_why ----
    "task {id}: {subject}":
        "görev {id}: {subject}",
    "priority = {priority}":
        "öncelik = {priority}",

    # ---- errors + status messages ----
    "no task with id {id}":
        "{id} id'li görev yok",
    "warning: {message}":
        "uyarı: {message}",
    "unknown source: {source}. known: {known}":
        "bilinmeyen kaynak: {source}. bilinenler: {known}",
    "polled {source}: emitted {emitted} signal(s)":
        "{source} yoklandı: {emitted} sinyal yayıldı",
    "removed {id}":
        "{id} kaldırıldı",
    "signal emitted: source={source} bump={bump} ttl={ttl}s affects={affects}":
        "sinyal yayıldı: kaynak={source} artış={bump} ttl={ttl}s etkiler={affects}",
    "(all tasks)":
        "(tüm görevler)",

    # ---- mock rows used in `triage theme --name X` preview ----
    "Critical hotfix":
        "Kritik hotfix",
    "Deploy migration":
        "Migrasyonu dağıt",
    "Catch up on email":
        "E-postaları yakala",

    # ---- lang subcommand ----
    "available languages (default: {default}):":
        "mevcut diller (varsayılan: {default}):",
    "unknown language: {lang}. known: {known}":
        "bilinmeyen dil: {lang}. bilinenler: {known}",
}
