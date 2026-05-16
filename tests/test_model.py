# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
from datetime import datetime, timedelta, timezone

from triage.model import Signal, Task


def test_task_has_stable_id_via_factory():
    t = Task(subject="a")
    assert isinstance(t.id, str)
    assert len(t.id) == 12


def test_task_roundtrips_through_dict():
    t = Task(subject="s", description="d", base_score=5, tags=["x"])
    t2 = Task.from_dict(t.to_dict())
    assert t == t2


def test_task_from_dict_ignores_unknown_keys():
    t = Task.from_dict({"id": "abc", "subject": "s", "totally_made_up": True})
    assert t.id == "abc"
    assert t.subject == "s"


def test_signal_expiry_uses_captured_at_and_ttl():
    now = datetime.now(timezone.utc)
    fresh = Signal(
        source="cron",
        captured_at=now.isoformat(timespec="seconds"),
        payload={},
        ttl_seconds=60,
    )
    stale = Signal(
        source="cron",
        captured_at=(now - timedelta(minutes=10)).isoformat(timespec="seconds"),
        payload={},
        ttl_seconds=60,
    )
    assert not fresh.is_expired(now=now)
    assert stale.is_expired(now=now)


def test_signal_roundtrips_through_dict():
    s = Signal(
        source="cron",
        captured_at="2026-05-15T00:00:00+00:00",
        payload={"active": True},
        affects=["a", "b"],
    )
    assert Signal.from_dict(s.to_dict()) == s
