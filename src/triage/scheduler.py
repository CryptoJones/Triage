# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""The reorder loop: read tasks, read active signals, compute, sort."""

from __future__ import annotations

from dataclasses import dataclass

from .model import Signal, Task
from .rules import DEFAULT_RULES, RuleContribution, RuleFn, score
from .store import Store


@dataclass
class ScoredTask:
    task: Task
    priority: int
    contributions: list[RuleContribution]


def rank(
    tasks: list[Task],
    signals: list[Signal],
    rules: list[tuple[str, RuleFn]] | None = None,
) -> list[ScoredTask]:
    rules = rules if rules is not None else DEFAULT_RULES
    scored = [
        ScoredTask(task=t, priority=p, contributions=c)
        for t, (p, c) in ((t, score(t, signals, rules=rules)) for t in tasks)
    ]
    scored.sort(key=lambda s: (-s.priority, s.task.created_at, s.task.id))
    return scored


def tick(store: Store) -> list[ScoredTask]:
    tasks = store.load_tasks()
    signals = store.active_signals()
    return rank(tasks, signals)
