# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Scoring rules. Each rule is a pure function (Task, [Signal]) -> int_delta.

Rules compose additively. Each carries a stable name so its contribution
is auditable via `triage why <id>`.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable

from .model import Signal, Task

RuleFn = Callable[[Task, list[Signal]], int]


@dataclass
class RuleContribution:
    name: str
    delta: int


def rule_base_score(task: Task, signals: list[Signal]) -> int:
    return int(task.base_score)


def rule_deadline_decay(
    task: Task, signals: list[Signal], *, now: datetime | None = None
) -> int:
    if not task.deadline:
        return 0
    ref = now or datetime.now(timezone.utc)
    try:
        deadline = datetime.fromisoformat(task.deadline)
    except ValueError:
        return 0
    if deadline.tzinfo is None:
        deadline = deadline.replace(tzinfo=timezone.utc)

    remaining = (deadline - ref).total_seconds()
    if remaining <= 0:
        return 100
    if remaining < 3600:
        return 90
    if remaining < 24 * 3600:
        return 60
    if remaining < 7 * 24 * 3600:
        return 30
    return 10


def rule_cron_window_active(task: Task, signals: list[Signal]) -> int:
    for sig in signals:
        if sig.source != "cron":
            continue
        if sig.affects and task.id not in sig.affects:
            continue
        if sig.payload.get("active"):
            return 25
    return 0


def rule_ci_failing(task: Task, signals: list[Signal]) -> int:
    """+50 if a fresh github-ci signal targeting this task reports failure."""
    for sig in signals:
        if sig.source != "github-ci":
            continue
        if sig.affects and task.id not in sig.affects:
            continue
        if sig.payload.get("state") == "failure":
            return 50
    return 0


DEFAULT_RULES: list[tuple[str, RuleFn]] = [
    ("base_score", rule_base_score),
    ("deadline_decay", rule_deadline_decay),
    ("cron_window_active", rule_cron_window_active),
    ("ci_failing", rule_ci_failing),
]


def score(
    task: Task,
    signals: list[Signal],
    rules: list[tuple[str, RuleFn]] | None = None,
) -> tuple[int, list[RuleContribution]]:
    rules = rules if rules is not None else DEFAULT_RULES
    contribs = [RuleContribution(name=name, delta=fn(task, signals)) for name, fn in rules]
    return sum(c.delta for c in contribs), contribs
