# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Command-line interface for Triage."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Sequence

from . import __version__, cron, log_writer, scheduler, theme
from .model import Task
from .sources import github_ci, runpod
from .store import Store

POLLERS: dict[str, callable] = {
    "github-ci": lambda store: github_ci.poll(store),
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
        print(theme.paint(f"warning: {w}", t.warning, enabled=enabled), file=sys.stderr)


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
    header_line = theme.paint(
        f"  {'ID':<12}  {'PRI':>6}  {'BAR':<5}  SUBJECT",
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
        print(theme.paint("(no tasks)", t.dim, enabled=color))
        return 0

    _print_banner(t, enabled=color, title=f"T R I A G E   v{__version__}")
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
        theme.paint(f"no task with id {args.id}", t.warning, enabled=color),
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
            heading = f" task {s.task.id}: {s.task.subject} "
            rule = t.rule * 3
            print(theme.paint(f"{rule}{heading}{rule}", t.header, enabled=color))
            pri_color = theme.priority_color(t, s.priority)
            print(
                "  priority = "
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
        theme.paint(f"no task with id {args.id}", t.warning, enabled=color),
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

    _print_banner(t, enabled=color, title=f"T R I A G E   T I C K   v{__version__}")
    summary = (
        f"emitted {emitted} cron signal(s); ranked {len(ranked)} task(s)"
    )
    print(theme.paint(summary, t.header, enabled=color))
    _print_table(t, enabled=color, ranked=ranked)
    return 0


def cmd_poll(args: argparse.Namespace) -> int:
    store = _store_from_args(args)
    t, color = _theme(args)
    poller = POLLERS.get(args.source)
    if poller is None:
        msg = (
            f"unknown source: {args.source}. known: {', '.join(sorted(POLLERS))}"
        )
        print(theme.paint(msg, t.warning, enabled=color), file=sys.stderr)
        return 1
    emitted, warnings = poller(store)
    log_writer.log("poll", source=args.source, emitted=emitted, warnings=warnings)
    _print_warnings(t, enabled=color, warnings=warnings)
    print(
        theme.paint(
            f"polled {args.source}: emitted {emitted} signal(s)",
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
            theme.paint(f"no task with id {args.id}", t.warning, enabled=color),
            file=sys.stderr,
        )
        return 1
    store.save_tasks(tasks)
    log_writer.log("rm", task_id=args.id)
    print(theme.paint(f"removed {args.id}", t.success, enabled=color))
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
        _print_banner(t, enabled=color, title=f"theme preview: {t.name}")
        # Mock a few rows
        from .model import Task
        mock = [
            scheduler.ScoredTask(
                task=Task(id="aaaa11112222", subject="Critical hotfix"),
                priority=120,
                contributions=[],
            ),
            scheduler.ScoredTask(
                task=Task(id="bbbb33334444", subject="Deploy migration"),
                priority=45,
                contributions=[],
            ),
            scheduler.ScoredTask(
                task=Task(id="cccc55556666", subject="Catch up on email"),
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


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="triage",
        description="Meta-scheduler that watches signals and reorders its own queue.",
    )
    p.add_argument("--version", action="version", version=f"triage {__version__}")
    p.add_argument(
        "--home",
        help="Override TRIAGE_HOME (default: ~/.triage or $TRIAGE_HOME).",
    )
    p.add_argument(
        "--theme",
        choices=sorted(theme.THEMES),
        default=None,
        help=(
            f"Output theme (default from $TRIAGE_THEME or {theme.DEFAULT_THEME}). "
            "Set NO_COLOR=1 to disable colors regardless of theme."
        ),
    )
    p.add_argument(
        "--no-color",
        action="store_true",
        help="Force-disable ANSI color even on a TTY.",
    )
    p.add_argument(
        "--log-file",
        default=None,
        help=(
            "Append JSONL events to this path "
            f"(default: $TRIAGE_LOG_FILE or {log_writer.DEFAULT_LOG_PATH}; "
            f"falls back to {log_writer.FALLBACK_LOG_PATH} if unwritable)."
        ),
    )
    p.add_argument(
        "--no-log",
        action="store_true",
        help="Disable JSONL event logging for this invocation.",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", help="Add a task.")
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

    lst = sub.add_parser("list", help="Show the current priority order.")
    lst.add_argument("--json", action="store_true")
    lst.set_defaults(func=cmd_list)

    sh = sub.add_parser("show", help="Show one task's full record.")
    sh.add_argument("id")
    sh.set_defaults(func=cmd_show)

    why = sub.add_parser("why", help="Audit log of rule contributions for a task.")
    why.add_argument("id")
    why.set_defaults(func=cmd_why)

    tk = sub.add_parser("tick", help="Recompute priorities; print new order.")
    tk.set_defaults(func=cmd_tick)

    pl = sub.add_parser(
        "poll",
        help="Invoke a network-bound signal source's poller.",
    )
    pl.add_argument(
        "source",
        help=f"Signal source to poll. Known: {', '.join(sorted(POLLERS))}.",
    )
    pl.set_defaults(func=cmd_poll)

    rm = sub.add_parser("rm", help="Remove a task by id.")
    rm.add_argument("id")
    rm.set_defaults(func=cmd_rm)

    th = sub.add_parser("theme", help="List themes, or preview one with --name.")
    th.add_argument(
        "--name",
        choices=sorted(theme.THEMES),
        help="Preview the named theme by rendering sample rows.",
    )
    th.set_defaults(func=cmd_theme)

    return p


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    log_writer.configure(path=getattr(args, "log_file", None), disabled=getattr(args, "no_log", False))
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
