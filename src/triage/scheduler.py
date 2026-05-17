# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""The reorder loop: read tasks, read active signals, compute, sort.

Two phases:

1. **Score** each task independently via the configured rule set
   (see `triage.rules`). Each rule contributes a named delta.
2. **Propagate blockers** transitively: for any task A that is
   `blocked_by` task B, B's effective priority must be at least
   one higher than A's, so B is worked first. Cycles in the
   `blocked_by` graph are broken deterministically before
   propagation.

The blocker_transitive contribution is recorded on every task (often
as 0) so `triage why` can show exactly how propagation affected the
final score.
"""

from __future__ import annotations

from dataclasses import dataclass

from .i18n import _
from .model import Signal, Task
from .rules import DEFAULT_RULES, RuleContribution, RuleFn, score
from .store import Store


@dataclass
class ScoredTask:
    task: Task
    priority: int
    contributions: list[RuleContribution]


def _break_cycles(blocks: dict[str, list[str]]) -> list[str]:
    """DFS back-edge removal. Mutates `blocks` in place to produce a DAG.

    Source nodes are visited in lexicographic order so the resulting
    DAG is deterministic for any given input graph.

    Returns a list of human-readable warning strings describing each
    removed edge (one per back-edge found).
    """
    white, gray, black = 0, 1, 2
    color: dict[str, int] = {tid: white for tid in blocks}
    warnings: list[str] = []

    def dfs(u: str) -> None:
        color[u] = gray
        for v in list(blocks.get(u, [])):
            cv = color.get(v, white)
            if cv == gray:
                blocks[u] = [x for x in blocks[u] if x != v]
                warnings.append(_("cycle: removed edge {u} -> {v} (back-edge)", u=u, v=v))
            elif cv == white:
                dfs(v)
        color[u] = black

    for u in sorted(blocks.keys()):
        if color[u] == white:
            dfs(u)
    return warnings


def propagate_blockers(scored: list[ScoredTask]) -> tuple[list[ScoredTask], list[str]]:
    """Adjust scored tasks so each blocker out-ranks what it blocks by ≥ 1.

    Semantic: if task A is `blocked_by` [B, C, ...], then B and C
    must come before A in the queue, so each of B and C is bumped
    such that `priority(blocker) >= priority(blocked) + 1`. The
    blocked task A keeps its own score; the blockers absorb the bump.

    Cycles are detected via DFS back-edge removal (deterministic
    by sorted source-id traversal). Dangling blocker ids and
    self-loops are reported as warnings and ignored.

    Returns the adjusted scored list (same order) and a list of
    warning strings.
    """
    by_id: dict[str, ScoredTask] = {s.task.id: s for s in scored}

    # Build "blocks" graph: blocker_id -> [task ids it blocks]
    blocks: dict[str, list[str]] = {tid: [] for tid in by_id}
    warnings: list[str] = []
    for s in scored:
        for blocker_id in s.task.blocked_by:
            if blocker_id == s.task.id:
                warnings.append(_("self-block: {id} blocks itself; ignored", id=s.task.id))
                continue
            if blocker_id not in by_id:
                warnings.append(_(
                    "dangling blocker: {id} blocked_by {blocker} (unknown); ignored",
                    id=s.task.id, blocker=blocker_id,
                ))
                continue
            blocks[blocker_id].append(s.task.id)

    warnings.extend(_break_cycles(blocks))

    # Reverse-topo propagation via DFS memoization.
    # For each task t: final[t] = max(own, max(final[d] for d in blocks[t]) + 1).
    final: dict[str, int] = {}

    def resolve(tid: str) -> int:
        if tid in final:
            return final[tid]
        own = by_id[tid].priority
        max_downstream = 0
        downstream = blocks.get(tid, [])
        for d in downstream:
            max_downstream = max(max_downstream, resolve(d))
        result = max(own, max_downstream + 1) if downstream else own
        final[tid] = result
        return result

    for tid in by_id:
        resolve(tid)

    adjusted: list[ScoredTask] = []
    for s in scored:
        delta = final[s.task.id] - s.priority
        new_contribs = list(s.contributions) + [
            RuleContribution(name="blocker_transitive", delta=delta)
        ]
        adjusted.append(
            ScoredTask(
                task=s.task,
                priority=final[s.task.id],
                contributions=new_contribs,
            )
        )
    return adjusted, warnings


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
    scored, _warnings = propagate_blockers(scored)
    scored.sort(key=lambda s: (-s.priority, s.task.created_at, s.task.id))
    return scored


def rank_with_warnings(
    tasks: list[Task],
    signals: list[Signal],
    rules: list[tuple[str, RuleFn]] | None = None,
) -> tuple[list[ScoredTask], list[str]]:
    """Same as rank() but also returns the propagation warning list."""
    rules = rules if rules is not None else DEFAULT_RULES
    scored = [
        ScoredTask(task=t, priority=p, contributions=c)
        for t, (p, c) in ((t, score(t, signals, rules=rules)) for t in tasks)
    ]
    scored, warnings = propagate_blockers(scored)
    scored.sort(key=lambda s: (-s.priority, s.task.created_at, s.task.id))
    return scored, warnings


def tick(store: Store) -> list[ScoredTask]:
    tasks = store.load_tasks()
    signals = store.active_signals()
    return rank(tasks, signals)
