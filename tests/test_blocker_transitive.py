# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Tests for the blocker_transitive propagation logic."""

from __future__ import annotations

from triage.model import Task
from triage.scheduler import propagate_blockers, rank, rank_with_warnings, ScoredTask


def _bare(task: Task, priority: int) -> ScoredTask:
    return ScoredTask(task=task, priority=priority, contributions=[])


def test_blocker_gets_bumped_above_blocked():
    blocker = Task(id="B", subject="b")
    blocked = Task(id="A", subject="a", blocked_by=["B"])
    scored = [_bare(blocker, 1), _bare(blocked, 100)]

    adjusted, warnings = propagate_blockers(scored)
    by_id = {s.task.id: s for s in adjusted}

    assert warnings == []
    assert by_id["A"].priority == 100
    assert by_id["B"].priority == 101
    # blocked_transitive contribution recorded on both
    assert any(c.name == "blocker_transitive" for c in by_id["A"].contributions)
    assert any(c.name == "blocker_transitive" for c in by_id["B"].contributions)


def test_no_change_when_blocker_already_higher():
    blocker = Task(id="B", subject="b")
    blocked = Task(id="A", subject="a", blocked_by=["B"])
    scored = [_bare(blocker, 200), _bare(blocked, 5)]

    adjusted, warnings = propagate_blockers(scored)
    by_id = {s.task.id: s for s in adjusted}

    assert warnings == []
    assert by_id["A"].priority == 5
    assert by_id["B"].priority == 200


def test_chain_propagation_three_deep():
    # C is blocked by B, B is blocked by A. So A and B must both rank above C.
    a = Task(id="A", subject="a")
    b = Task(id="B", subject="b", blocked_by=["A"])
    c = Task(id="C", subject="c", blocked_by=["B"])
    scored = [_bare(a, 1), _bare(b, 1), _bare(c, 50)]

    adjusted, _ = propagate_blockers(scored)
    by_id = {s.task.id: s for s in adjusted}

    assert by_id["C"].priority == 50
    assert by_id["B"].priority == 51
    assert by_id["A"].priority == 52


def test_multiple_blockers_all_bumped():
    a = Task(id="A", subject="a", blocked_by=["B", "C"])
    b = Task(id="B", subject="b")
    c = Task(id="C", subject="c")
    scored = [_bare(a, 30), _bare(b, 1), _bare(c, 2)]

    adjusted, _ = propagate_blockers(scored)
    by_id = {s.task.id: s for s in adjusted}

    assert by_id["A"].priority == 30
    assert by_id["B"].priority == 31
    assert by_id["C"].priority == 31


def test_self_loop_produces_warning_and_no_bump():
    a = Task(id="A", subject="a", blocked_by=["A"])
    scored = [_bare(a, 10)]

    adjusted, warnings = propagate_blockers(scored)
    assert adjusted[0].priority == 10
    assert any("self-block" in w for w in warnings)


def test_dangling_blocker_id_warns_and_is_ignored():
    a = Task(id="A", subject="a", blocked_by=["GHOST"])
    scored = [_bare(a, 5)]

    adjusted, warnings = propagate_blockers(scored)
    assert adjusted[0].priority == 5
    assert any("dangling blocker" in w for w in warnings)


def test_two_node_cycle_is_broken():
    # A is blocked by B, B is blocked by A. Pick one back-edge to remove.
    a = Task(id="A", subject="a", blocked_by=["B"])
    b = Task(id="B", subject="b", blocked_by=["A"])
    scored = [_bare(a, 10), _bare(b, 10)]

    adjusted, warnings = propagate_blockers(scored)
    by_id = {s.task.id: s for s in adjusted}

    assert any("cycle" in w for w in warnings)
    # Whichever edge survives, the graph is now a DAG and the surviving
    # blocker is bumped exactly one above its blocked.
    pri_a, pri_b = by_id["A"].priority, by_id["B"].priority
    assert {pri_a, pri_b} == {10, 11}


def test_three_node_cycle_is_broken():
    a = Task(id="A", subject="a", blocked_by=["B"])
    b = Task(id="B", subject="b", blocked_by=["C"])
    c = Task(id="C", subject="c", blocked_by=["A"])
    scored = [_bare(a, 5), _bare(b, 5), _bare(c, 5)]

    adjusted, warnings = propagate_blockers(scored)
    by_id = {s.task.id: s for s in adjusted}

    assert any("cycle" in w for w in warnings)
    # All three priorities should remain bounded — no infinite escalation.
    for s in adjusted:
        assert by_id[s.task.id].priority < 100


def test_propagation_is_deterministic_across_runs():
    a = Task(id="A", subject="a", blocked_by=["B"])
    b = Task(id="B", subject="b", blocked_by=["A"])
    scored = [_bare(a, 10), _bare(b, 10)]
    run1, _ = propagate_blockers(scored)
    run2, _ = propagate_blockers(scored)
    assert [s.priority for s in run1] == [s.priority for s in run2]


def test_rank_uses_blocker_propagation_in_final_order():
    # A is blocked by B; even though A has higher base_score,
    # B should now outrank A in the final ranking.
    a = Task(id="A", subject="a", base_score=100, blocked_by=["B"])
    b = Task(id="B", subject="b", base_score=1)

    ranked = rank([a, b], [])
    assert [s.task.id for s in ranked] == ["B", "A"]
    assert ranked[0].priority == ranked[1].priority + 1


def test_rank_with_warnings_returns_both():
    a = Task(id="A", subject="a", blocked_by=["A"])
    ranked, warnings = rank_with_warnings([a], [])
    assert len(ranked) == 1
    assert any("self-block" in w for w in warnings)


def test_no_blockers_leaves_priorities_alone():
    a = Task(id="A", subject="a", base_score=10)
    b = Task(id="B", subject="b", base_score=20)

    adjusted, warnings = propagate_blockers([_bare(a, 10), _bare(b, 20)])
    assert warnings == []
    assert adjusted[0].priority == 10
    assert adjusted[1].priority == 20
    # contribution still recorded (delta=0) for auditability
    for s in adjusted:
        bt = [c for c in s.contributions if c.name == "blocker_transitive"]
        assert len(bt) == 1
        assert bt[0].delta == 0
