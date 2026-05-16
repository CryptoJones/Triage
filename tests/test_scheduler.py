# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
from datetime import datetime, timezone

from triage.model import Signal, Task
from triage.scheduler import rank


def test_rank_sorts_by_priority_descending():
    a = Task(subject="a", base_score=5)
    b = Task(subject="b", base_score=20)
    c = Task(subject="c", base_score=10)
    result = rank([a, b, c], [])
    assert [s.task.subject for s in result] == ["b", "c", "a"]


def test_rank_tiebreaks_on_created_at_then_id():
    a = Task(id="aaa", subject="a", created_at="2026-01-01T00:00:00+00:00", base_score=5)
    b = Task(id="bbb", subject="b", created_at="2026-01-01T00:00:00+00:00", base_score=5)
    result = rank([b, a], [])
    assert [s.task.id for s in result] == ["aaa", "bbb"]


def test_rank_combines_base_and_cron_signal():
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    quiet = Task(id="quiet", subject="q", base_score=10)
    loud = Task(id="loud", subject="l", base_score=5)
    sig = Signal(source="cron", captured_at=now, payload={"active": True}, affects=["loud"])
    result = rank([quiet, loud], [sig])
    assert [s.task.id for s in result] == ["loud", "quiet"]
    assert result[0].priority == 30
    assert result[1].priority == 10


def test_rank_empty_inputs():
    assert rank([], []) == []
