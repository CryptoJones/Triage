# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Cron-window signal source.

Tasks may carry a `cron_window` field — a five-field cron expression
describing the window during which the task is "active". When a task's
window matches the current minute, this source emits a signal with
`payload.active = True` targeting that task's id.

This is the v0.1 signal adapter; see DESIGN.md for the v0.2+ roadmap
(CI status, RunPod cost, GitHub PR freshness).
"""

from __future__ import annotations

from .i18n import _

from datetime import datetime, timezone

from .model import Signal, Task
from .store import Store


def _expand_field(spec: str, lo: int, hi: int) -> set[int]:
    if spec == "*":
        return set(range(lo, hi + 1))
    out: set[int] = set()
    for piece in spec.split(","):
        step = 1
        if "/" in piece:
            piece, step_s = piece.split("/", 1)
            step = int(step_s)
        if piece == "*":
            start, end = lo, hi
        elif "-" in piece:
            a, b = piece.split("-", 1)
            start, end = int(a), int(b)
        else:
            start = end = int(piece)
        for v in range(start, end + 1, step):
            if lo <= v <= hi:
                out.add(v)
    return out


def matches(expr: str, when: datetime) -> bool:
    """Return True if the five-field cron expression matches `when`."""
    parts = expr.split()
    if len(parts) != 5:
        raise ValueError(_(
            "cron expression must have 5 fields, got {got}: {expr}",
            got=len(parts), expr=repr(expr),
        ))
    minute_s, hour_s, dom_s, month_s, dow_s = parts
    minutes = _expand_field(minute_s, 0, 59)
    hours = _expand_field(hour_s, 0, 23)
    doms = _expand_field(dom_s, 1, 31)
    months = _expand_field(month_s, 1, 12)
    dows = _expand_field(dow_s, 0, 6)
    return (
        when.minute in minutes
        and when.hour in hours
        and when.day in doms
        and when.month in months
        and (when.weekday() + 1) % 7 in dows
    )


def emit(store: Store, *, now: datetime | None = None) -> int:
    """Walk all tasks with a cron_window; write a signal for each match."""
    ref = now or datetime.now(timezone.utc)
    tasks = store.load_tasks()
    count = 0
    for task in tasks:
        if not task.cron_window:
            continue
        try:
            active = matches(task.cron_window, ref)
        except ValueError:
            continue
        store.append_signal(
            Signal(
                source="cron",
                captured_at=ref.isoformat(timespec="seconds"),
                payload={"active": active, "window": task.cron_window},
                affects=[task.id],
                ttl_seconds=120,
            )
        )
        count += 1
    return count
