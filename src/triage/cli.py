# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Command-line interface for Triage."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Sequence

from . import __version__, cron, scheduler
from .model import Task
from .sources import github_ci
from .store import Store

POLLERS: dict[str, callable] = {
    "github-ci": lambda store: github_ci.poll(store),
}


def _store_from_args(args: argparse.Namespace) -> Store:
    return Store(root=args.home) if args.home else Store()


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
    print(task.id)
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    store = _store_from_args(args)
    cron.emit(store)
    tasks = store.load_tasks()
    signals = store.active_signals()
    ranked, warnings = scheduler.rank_with_warnings(tasks, signals)
    for w in warnings:
        print(f"warning: {w}", file=sys.stderr)
    if args.json:
        out = [
            {
                "id": s.task.id,
                "subject": s.task.subject,
                "priority": s.priority,
            }
            for s in ranked
        ]
        print(json.dumps(out, indent=2))
        return 0
    if not ranked:
        print("(no tasks)")
        return 0
    for s in ranked:
        print(f"{s.task.id}  [{s.priority:>4}]  {s.task.subject}")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    store = _store_from_args(args)
    for t in store.load_tasks():
        if t.id == args.id:
            print(json.dumps(t.to_dict(), indent=2, sort_keys=True))
            return 0
    print(f"no task with id {args.id}", file=sys.stderr)
    return 1


def cmd_why(args: argparse.Namespace) -> int:
    store = _store_from_args(args)
    cron.emit(store)
    tasks = store.load_tasks()
    signals = store.active_signals()
    ranked, warnings = scheduler.rank_with_warnings(tasks, signals)
    for w in warnings:
        print(f"warning: {w}", file=sys.stderr)
    for s in ranked:
        if s.task.id == args.id:
            print(f"task {s.task.id}: {s.task.subject}")
            print(f"priority = {s.priority}")
            for c in s.contributions:
                marker = "  ·" if c.delta == 0 else "  +"
                print(f"{marker} {c.name}: {c.delta:+d}")
            return 0
    print(f"no task with id {args.id}", file=sys.stderr)
    return 1


def cmd_tick(args: argparse.Namespace) -> int:
    store = _store_from_args(args)
    emitted = cron.emit(store)
    tasks = store.load_tasks()
    signals = store.active_signals()
    ranked, warnings = scheduler.rank_with_warnings(tasks, signals)
    for w in warnings:
        print(f"warning: {w}", file=sys.stderr)
    print(f"emitted {emitted} cron signal(s); ranked {len(ranked)} task(s)")
    for s in ranked:
        print(f"  {s.task.id}  [{s.priority:>4}]  {s.task.subject}")
    return 0


def cmd_poll(args: argparse.Namespace) -> int:
    store = _store_from_args(args)
    poller = POLLERS.get(args.source)
    if poller is None:
        print(
            f"unknown source: {args.source}. known: {', '.join(sorted(POLLERS))}",
            file=sys.stderr,
        )
        return 1
    emitted, warnings = poller(store)
    for w in warnings:
        print(f"warning: {w}", file=sys.stderr)
    print(f"polled {args.source}: emitted {emitted} signal(s)")
    return 0


def cmd_rm(args: argparse.Namespace) -> int:
    store = _store_from_args(args)
    tasks = store.load_tasks()
    before = len(tasks)
    tasks = [t for t in tasks if t.id != args.id]
    if len(tasks) == before:
        print(f"no task with id {args.id}", file=sys.stderr)
        return 1
    store.save_tasks(tasks)
    print(f"removed {args.id}")
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

    return p


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
