# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Command-line interface for Triage."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Sequence

from . import __version__, cron, i18n, log_writer, scheduler, theme
from .i18n import _
from .model import Task
from .sources import github_ci, github_pr, runpod
from .store import Store

POLLERS: dict[str, callable] = {
    "github-ci": lambda store: github_ci.poll(store),
    "github-pr": lambda store: github_pr.poll(store),
    "runpod-cost": lambda store: runpod.poll(store),
}


def _store_from_args(args: argparse.Namespace) -> Store:
    return Store(root=args.home) if args.home else Store()


def _theme(args: argparse.Namespace) -> tuple[theme.Theme, bool]:
    """Return (theme, color_enabled) honoring --no-color / NO_COLOR / TTY."""
    name = getattr(args, "theme", None)
    t = theme.get(name)
    color = theme.should_color(sys.stdout)
    if getattr(args, "no_color", False) or t.name == "mono":
        color = False
    return t, color


def _print_banner(t: theme.Theme, *, enabled: bool, title: str) -> None:
    for line in theme.banner(t, title, enabled=enabled):
        print(line)


def _print_warnings(t: theme.Theme, *, enabled: bool, warnings: list[str]) -> None:
    for w in warnings:
        msg = _("warning: {message}", message=w)
        print(theme.paint(msg, t.warning, enabled=enabled), file=sys.stderr)


def cmd_add(args: argparse.Namespace) -> int:
    store = _store_from_args(args)
    tasks = store.load_tasks()
    task = Task(
        subject=args.subject,
        description=args.description or "",
        base_score=args.base_score,
        tags=list(args.tag or []),
        deadline=args.deadline,
        blocked_by=list(args.blocked_by or []),
        cron_window=args.cron_window,
    )
    tasks.append(task)
    store.save_tasks(tasks)
    log_writer.log(
        "add",
        task_id=task.id,
        subject=task.subject,
        base_score=task.base_score,
        tags=task.tags,
        deadline=task.deadline,
        blocked_by=task.blocked_by,
    )
    print(task.id)
    return 0


def _format_row(t: theme.Theme, *, enabled: bool, s: scheduler.ScoredTask) -> str:
    pri_color = theme.priority_color(t, s.priority)
    bar = theme.priority_bar(t, s.priority)
    id_part = theme.paint(s.task.id, t.id_col, enabled=enabled)
    pri_part = theme.paint(f"[{s.priority:>4}]", pri_color, enabled=enabled)
    bar_part = theme.paint(bar, pri_color, enabled=enabled)
    subj = theme.paint(s.task.subject, t.subject, enabled=enabled)
    return f"  {id_part}  {pri_part}  {bar_part}  {subj}"


def _print_table(t: theme.Theme, *, enabled: bool, ranked: list[scheduler.ScoredTask]) -> None:
    # Translate each column heading then re-pad — fixed widths
    # (12/6/5) match the row layout in _format_row. If a locale
    # produces a heading wider than the column, it will overflow
    # by a couple of chars; tolerable for L1, refined later.
    id_h = _("ID")
    pri_h = _("PRI")
    bar_h = _("BAR")
    subj_h = _("SUBJECT")
    header_line = theme.paint(
        f"  {id_h:<12}  {pri_h:>6}  {bar_h:<5}  {subj_h}",
        t.header,
        enabled=enabled,
    )
    rule_line = theme.paint(
        "  " + t.rule * 12 + "  " + t.rule * 6 + "  " + t.rule * 5 + "  " + t.rule * 40,
        t.dim,
        enabled=enabled,
    )
    print(header_line)
    print(rule_line)
    for s in ranked:
        print(_format_row(t, enabled=enabled, s=s))


def cmd_list(args: argparse.Namespace) -> int:
    store = _store_from_args(args)
    cron.emit(store)
    tasks = store.load_tasks()
    signals = store.active_signals()
    ranked, warnings = scheduler.rank_with_warnings(tasks, signals)

    t, color = _theme(args)
    _print_warnings(t, enabled=color, warnings=warnings)

    if args.json:
        out = [
            {"id": s.task.id, "subject": s.task.subject, "priority": s.priority}
            for s in ranked
        ]
        print(json.dumps(out, indent=2))
        return 0
    log_writer.log(
        "list",
        count=len(ranked),
        top=[
            {"id": s.task.id, "subject": s.task.subject, "priority": s.priority}
            for s in ranked[:3]
        ],
        warnings=warnings,
    )

    if not ranked:
        print(theme.paint(_("(no tasks)"), t.dim, enabled=color))
        return 0

    _print_banner(t, enabled=color, title=_("T R I A G E   v{version}", version=__version__))
    _print_table(t, enabled=color, ranked=ranked)
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    store = _store_from_args(args)
    t, color = _theme(args)
    for task in store.load_tasks():
        if task.id == args.id:
            print(json.dumps(task.to_dict(), indent=2, sort_keys=True))
            return 0
    print(
        theme.paint(_("no task with id {id}", id=args.id), t.warning, enabled=color),
        file=sys.stderr,
    )
    return 1


def cmd_why(args: argparse.Namespace) -> int:
    store = _store_from_args(args)
    cron.emit(store)
    tasks = store.load_tasks()
    signals = store.active_signals()
    ranked, warnings = scheduler.rank_with_warnings(tasks, signals)

    t, color = _theme(args)
    _print_warnings(t, enabled=color, warnings=warnings)

    for s in ranked:
        if s.task.id == args.id:
            heading = " " + _("task {id}: {subject}", id=s.task.id, subject=s.task.subject) + " "
            rule = t.rule * 3
            print(theme.paint(f"{rule}{heading}{rule}", t.header, enabled=color))
            pri_color = theme.priority_color(t, s.priority)
            # Render `priority = <colored value>  <colored bar>`.
            # Split so the bar/value stay color-banded but the
            # label/equals get localized.
            label = _("priority = {priority}", priority="").rstrip(" =") + " = "
            print(
                "  " + label
                + theme.paint(str(s.priority), pri_color, enabled=color)
                + "  "
                + theme.paint(
                    theme.priority_bar(t, s.priority), pri_color, enabled=color
                )
            )
            for c in s.contributions:
                if c.delta == 0:
                    marker = theme.paint(" ·", t.rule_contrib_zero, enabled=color)
                    body = theme.paint(
                        f"{c.name}: {c.delta:+d}", t.rule_contrib_zero, enabled=color
                    )
                else:
                    marker = theme.paint(" +", t.rule_contrib_plus, enabled=color)
                    body = theme.paint(
                        f"{c.name}: {c.delta:+d}", t.rule_contrib_plus, enabled=color
                    )
                print(f" {marker} {body}")
            return 0

    print(
        theme.paint(_("no task with id {id}", id=args.id), t.warning, enabled=color),
        file=sys.stderr,
    )
    return 1


def cmd_tick(args: argparse.Namespace) -> int:
    store = _store_from_args(args)
    emitted = cron.emit(store)
    tasks = store.load_tasks()
    signals = store.active_signals()
    ranked, warnings = scheduler.rank_with_warnings(tasks, signals)

    t, color = _theme(args)
    _print_warnings(t, enabled=color, warnings=warnings)

    log_writer.log(
        "tick",
        emitted_cron_signals=emitted,
        ranked_count=len(ranked),
        top=[
            {"id": s.task.id, "subject": s.task.subject, "priority": s.priority}
            for s in ranked[:3]
        ],
        warnings=warnings,
    )

    _print_banner(t, enabled=color, title=_("T R I A G E   T I C K   v{version}", version=__version__))
    summary = _("emitted {emitted} cron signal(s); ranked {ranked} task(s)",
                emitted=emitted, ranked=len(ranked))
    print(theme.paint(summary, t.header, enabled=color))
    _print_table(t, enabled=color, ranked=ranked)
    return 0


def cmd_poll(args: argparse.Namespace) -> int:
    store = _store_from_args(args)
    t, color = _theme(args)
    poller = POLLERS.get(args.source)
    if poller is None:
        msg = _(
            "unknown source: {source}. known: {known}",
            source=args.source,
            known=", ".join(sorted(POLLERS)),
        )
        print(theme.paint(msg, t.warning, enabled=color), file=sys.stderr)
        return 1
    emitted, warnings = poller(store)
    log_writer.log("poll", source=args.source, emitted=emitted, warnings=warnings)
    _print_warnings(t, enabled=color, warnings=warnings)
    print(
        theme.paint(
            _("polled {source}: emitted {emitted} signal(s)",
              source=args.source, emitted=emitted),
            t.success,
            enabled=color,
        )
    )
    return 0


def cmd_signal(args: argparse.Namespace) -> int:
    """Inject a manual signal into the store. Used by RunPodBoss-style
    external watchers (and humans) to bump priority programmatically.
    """
    from datetime import datetime, timezone
    from .model import Signal

    store = _store_from_args(args)
    t, color = _theme(args)

    payload: dict[str, object] = {"bump": args.bump}
    if args.note:
        payload["note"] = args.note
    if args.state:
        payload["state"] = args.state

    sig = Signal(
        source=args.source,
        captured_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        payload=payload,
        affects=list(args.affects or []),
        ttl_seconds=args.ttl,
    )
    store.append_signal(sig)
    log_writer.log(
        "signal",
        source=args.source,
        bump=args.bump,
        ttl_seconds=args.ttl,
        affects=list(args.affects or []),
        state=args.state,
        note=args.note,
    )
    affected_str = ",".join(args.affects) if args.affects else _("(all tasks)")
    print(
        theme.paint(
            _("signal emitted: source={source} bump={bump} ttl={ttl}s affects={affects}",
              source=args.source, bump=args.bump, ttl=args.ttl, affects=affected_str),
            t.success,
            enabled=color,
        )
    )
    return 0


def cmd_rm(args: argparse.Namespace) -> int:
    store = _store_from_args(args)
    t, color = _theme(args)
    tasks = store.load_tasks()
    before = len(tasks)
    tasks = [task for task in tasks if task.id != args.id]
    if len(tasks) == before:
        print(
            theme.paint(_("no task with id {id}", id=args.id), t.warning, enabled=color),
            file=sys.stderr,
        )
        return 1
    store.save_tasks(tasks)
    log_writer.log("rm", task_id=args.id)
    print(theme.paint(_("removed {id}", id=args.id), t.success, enabled=color))
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    """One-screen at-a-glance: top-3 tasks, tag counts, signal counts."""
    from collections import Counter

    store = _store_from_args(args)
    cron.emit(store)
    tasks = store.load_tasks()
    signals = store.active_signals()
    ranked, warnings = scheduler.rank_with_warnings(tasks, signals)

    t, color = _theme(args)
    _print_warnings(t, enabled=color, warnings=warnings)

    tag_counts = Counter()
    for task in tasks:
        for tag in task.tags:
            tag_counts[tag] += 1

    signal_counts = Counter()
    for sig in signals:
        signal_counts[sig.source] += 1

    log_writer.log(
        "status",
        task_count=len(tasks),
        ranked_count=len(ranked),
        tag_counts=dict(tag_counts),
        signal_counts=dict(signal_counts),
        top=[
            {"id": s.task.id, "subject": s.task.subject, "priority": s.priority}
            for s in ranked[:3]
        ],
        warnings=warnings,
    )

    if args.json:
        print(json.dumps({
            "task_count": len(tasks),
            "tag_counts": dict(tag_counts),
            "signal_counts": dict(signal_counts),
            "top": [
                {"id": s.task.id, "subject": s.task.subject, "priority": s.priority}
                for s in ranked[:3]
            ],
            "warnings": warnings,
        }, indent=2, sort_keys=True))
        return 0

    _print_banner(
        t,
        enabled=color,
        title=_("T R I A G E   S T A T U S") + f"   v{__version__}",
    )

    print(theme.paint("  " + _("TOP 3"), t.header, enabled=color))
    print(theme.paint("  " + t.rule * 56, t.dim, enabled=color))
    if not ranked:
        print(theme.paint("    " + _("(no tasks)"), t.dim, enabled=color))
    else:
        for s in ranked[:3]:
            print(_format_row(t, enabled=color, s=s))

    print()
    print(theme.paint("  " + _("TAGS ({n})", n=len(tag_counts)), t.header, enabled=color))
    print(theme.paint("  " + t.rule * 56, t.dim, enabled=color))
    if not tag_counts:
        print(theme.paint("    " + _("(no tags)"), t.dim, enabled=color))
    else:
        for tag, n in sorted(tag_counts.items(), key=lambda kv: (-kv[1], kv[0])):
            count_part = theme.paint(f"{n:>3}", t.priority_mid, enabled=color)
            tag_part = theme.paint(tag, t.subject, enabled=color)
            print(f"    {count_part}  {tag_part}")

    print()
    print(theme.paint(
        "  " + _("ACTIVE SIGNALS ({n})", n=sum(signal_counts.values())),
        t.header, enabled=color,
    ))
    print(theme.paint("  " + t.rule * 56, t.dim, enabled=color))
    if not signal_counts:
        print(theme.paint("    " + _("(no active signals)"), t.dim, enabled=color))
    else:
        for source, n in sorted(signal_counts.items(), key=lambda kv: (-kv[1], kv[0])):
            count_part = theme.paint(f"{n:>3}", t.priority_mid, enabled=color)
            source_part = theme.paint(source, t.subject, enabled=color)
            print(f"    {count_part}  {source_part}")

    print()
    print(theme.paint(
        "  " + _("total tasks: {tasks}    ranked: {ranked}",
                 tasks=len(tasks), ranked=len(ranked)),
        t.dim,
        enabled=color,
    ))
    return 0


def cmd_theme(args: argparse.Namespace) -> int:
    """List available themes (or preview one if --name given)."""
    if args.name:
        if args.name not in theme.THEMES:
            print(
                f"unknown theme: {args.name}. known: {', '.join(sorted(theme.THEMES))}",
                file=sys.stderr,
            )
            return 1
        t = theme.get(args.name)
        color = theme.should_color(sys.stdout) and t.name != "mono"
        if args.no_color:
            color = False
        _print_banner(t, enabled=color, title=_("theme preview: {name}", name=t.name))
        # Mock a few rows. Subjects are translated so a preview in
        # the active locale shows realistic content.
        from .model import Task
        mock = [
            scheduler.ScoredTask(
                task=Task(id="aaaa11112222", subject=_("Critical hotfix")),
                priority=120,
                contributions=[],
            ),
            scheduler.ScoredTask(
                task=Task(id="bbbb33334444", subject=_("Deploy migration")),
                priority=45,
                contributions=[],
            ),
            scheduler.ScoredTask(
                task=Task(id="cccc55556666", subject=_("Catch up on email")),
                priority=3,
                contributions=[],
            ),
        ]
        _print_table(t, enabled=color, ranked=mock)
        return 0

    print(f"available themes (default: {theme.DEFAULT_THEME}):")
    for name in sorted(theme.THEMES):
        marker = " *" if name == theme.DEFAULT_THEME else "  "
        print(f"{marker} {name}")
    return 0


def cmd_lang(args: argparse.Namespace) -> int:
    """List available output languages (or switch via --lang on any command)."""
    if getattr(args, "check", False):
        report = i18n.check_locales()
        if not report:
            print(f"OK: all {len(i18n.list_available()) - 1} non-English locales match the English baseline.")
            return 0
        for code in sorted(report):
            issues = report[code]
            print(f"locale {code!r}:")
            if issues["missing"]:
                print(f"  missing keys ({len(issues['missing'])}):")
                for key in issues["missing"]:
                    print(f"    - {key!r}")
            if issues["extra"]:
                print(f"  extra keys ({len(issues['extra'])}):")
                for key in issues["extra"]:
                    print(f"    + {key!r}")
            if issues["placeholder_mismatches"]:
                print(f"  placeholder mismatches ({len(issues['placeholder_mismatches'])}):")
                for key, en_ph, tr_ph in issues["placeholder_mismatches"]:
                    print(f"    {key!r}: en={en_ph} vs {code}={tr_ph}")
        return 1
    print(_("available languages (default: {default}):", default=i18n.DEFAULT_LANG))
    for code, native in i18n.list_available():
        marker = " *" if code == i18n.DEFAULT_LANG else "  "
        active = " (active)" if code == i18n.current_lang() else ""
        print(f"{marker} {code}  {native}{active}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="triage",
        description=_("Meta-scheduler that watches signals and reorders its own queue."),
    )
    p.add_argument("--version", action="version", version=f"triage {__version__}")
    p.add_argument(
        "--home",
        help=_("Override TRIAGE_HOME (default: ~/.triage or $TRIAGE_HOME)."),
    )
    p.add_argument(
        "--theme",
        choices=sorted(theme.THEMES),
        default=None,
        help=_(
            "Output theme (default from $TRIAGE_THEME or {default}). "
            "Set NO_COLOR=1 to disable colors regardless of theme.",
            default=theme.DEFAULT_THEME,
        ),
    )
    p.add_argument(
        "--no-color",
        action="store_true",
        help=_("Force-disable ANSI color even on a TTY."),
    )
    p.add_argument(
        "--lang",
        default=None,
        help=_("Language for CLI output (default from $TRIAGE_LANG, $LANG, or 'en')."),
    )
    p.add_argument(
        "--log-file",
        default=None,
        help=_(
            "Append JSONL events to this path "
            "(default: $TRIAGE_LOG_FILE or {default}; "
            "falls back to {fallback} if unwritable).",
            default=log_writer.DEFAULT_LOG_PATH,
            fallback=log_writer.FALLBACK_LOG_PATH,
        ),
    )
    p.add_argument(
        "--no-log",
        action="store_true",
        help=_("Disable JSONL event logging for this invocation."),
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", help=_("Add a task."))
    a.add_argument("subject")
    a.add_argument("--description", default="")
    a.add_argument("--base-score", type=int, default=0)
    a.add_argument("--tag", action="append")
    a.add_argument("--deadline", help="ISO 8601 deadline (e.g. 2026-05-20T00:00:00Z).")
    a.add_argument("--blocked-by", action="append")
    a.add_argument(
        "--cron-window",
        help='Five-field cron expression for active window (e.g. "* 9-17 * * 1-5").',
    )
    a.set_defaults(func=cmd_add)

    lst = sub.add_parser("list", help=_("Show the current priority order."))
    lst.add_argument("--json", action="store_true")
    lst.set_defaults(func=cmd_list)

    sh = sub.add_parser("show", help=_("Show one task's full record."))
    sh.add_argument("id")
    sh.set_defaults(func=cmd_show)

    why = sub.add_parser("why", help=_("Audit log of rule contributions for a task."))
    why.add_argument("id")
    why.set_defaults(func=cmd_why)

    tk = sub.add_parser("tick", help=_("Recompute priorities; print new order."))
    tk.set_defaults(func=cmd_tick)

    pl = sub.add_parser(
        "poll",
        help=_("Invoke a network-bound signal source's poller."),
    )
    pl.add_argument(
        "source",
        help=f"Signal source to poll. Known: {', '.join(sorted(POLLERS))}.",
    )
    pl.set_defaults(func=cmd_poll)

    sg = sub.add_parser(
        "signal",
        help=_("Inject a manual signal (for external watchers like RunPodBoss)."),
    )
    sg_sub = sg.add_subparsers(dest="signal_cmd", required=True)
    manual = sg_sub.add_parser(
        "manual",
        help="Write a one-off signal with a numeric priority bump.",
    )
    manual.add_argument(
        "--source",
        required=True,
        help='Signal source name (e.g. "runpodboss", "manual", "operator").',
    )
    manual.add_argument(
        "--affects",
        action="append",
        help="Task id this signal targets. Pass multiple times for multiple tasks. "
        "Omit to target all tasks.",
    )
    manual.add_argument(
        "--bump",
        type=int,
        required=True,
        help="Priority delta applied by rule_manual_bump while the signal is fresh.",
    )
    manual.add_argument(
        "--ttl",
        type=int,
        default=1800,
        help="Signal TTL in seconds (default: 1800).",
    )
    manual.add_argument(
        "--note",
        default=None,
        help="Free-text annotation written into the signal payload.",
    )
    manual.add_argument(
        "--state",
        default=None,
        help="Optional state label (e.g. 'warning', 'critical'); shows up in audit log.",
    )
    manual.set_defaults(func=cmd_signal)

    rm = sub.add_parser("rm", help=_("Remove a task by id."))
    rm.add_argument("id")
    rm.set_defaults(func=cmd_rm)

    st = sub.add_parser(
        "status",
        help=_("One-screen at-a-glance: top-3 tasks, tag counts, signal counts."),
    )
    st.add_argument("--json", action="store_true", help="Emit JSON instead of human-readable.")
    st.set_defaults(func=cmd_status)

    th = sub.add_parser("theme", help=_("List themes, or preview one with --name."))
    th.add_argument(
        "--name",
        choices=sorted(theme.THEMES),
        help="Preview the named theme by rendering sample rows.",
    )
    th.set_defaults(func=cmd_theme)

    lng = sub.add_parser("lang", help=_("List available output languages."))
    lng.add_argument(
        "--check",
        action="store_true",
        help=(
            "Audit every locale against the English baseline. "
            "Exits non-zero if any locale has missing/extra keys or placeholder mismatches."
        ),
    )
    lng.set_defaults(func=cmd_lang)

    return p


def _peek_lang(argv: Sequence[str] | None) -> str | None:
    """Pre-scan argv for `--lang LANG` so help-strings come back localized.

    argparse builds the help text from whatever `_()` returns at
    parser-construction time, so we need to resolve the locale
    BEFORE build_parser() runs. We do that here without touching
    argparse so an invalid value falls through to argparse's normal
    error path on the second pass.
    """
    if argv is None:
        argv = sys.argv[1:]
    it = iter(argv)
    for tok in it:
        if tok == "--lang":
            return next(it, None)
        if tok.startswith("--lang="):
            return tok.split("=", 1)[1]
    return None


def main(argv: Sequence[str] | None = None) -> int:
    i18n.configure(_peek_lang(argv))
    parser = build_parser()
    args = parser.parse_args(argv)
    # If `--lang` actually parsed to a different value (e.g. via
    # ambiguous prefix), reconfigure so the command body uses it too.
    i18n.configure(getattr(args, "lang", None))
    log_writer.configure(path=getattr(args, "log_file", None), disabled=getattr(args, "no_log", False))
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
