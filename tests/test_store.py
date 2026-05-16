# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
from datetime import datetime, timezone

from triage.model import Signal, Task
from triage.store import Store


def test_store_creates_root_on_demand(tmp_path):
    s = Store(root=tmp_path / "home")
    s.ensure()
    assert (tmp_path / "home" / "tasks.json").exists()
    assert (tmp_path / "home" / "state").is_dir()


def test_store_roundtrips_tasks(tmp_path):
    s = Store(root=tmp_path)
    a = Task(subject="alpha")
    b = Task(subject="beta", base_score=5)
    s.save_tasks([a, b])
    loaded = s.load_tasks()
    assert [t.subject for t in loaded] == ["alpha", "beta"]
    assert loaded[1].base_score == 5


def test_store_save_is_atomic_on_overwrite(tmp_path):
    s = Store(root=tmp_path)
    s.save_tasks([Task(subject="one")])
    s.save_tasks([Task(subject="two")])
    assert [t.subject for t in s.load_tasks()] == ["two"]


def test_signals_append_and_iter(tmp_path):
    s = Store(root=tmp_path)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    s.append_signal(Signal(source="cron", captured_at=now, payload={"active": True}))
    s.append_signal(Signal(source="cron", captured_at=now, payload={"active": False}))
    s.append_signal(Signal(source="ci", captured_at=now, payload={"state": "failing"}))

    all_signals = list(s.iter_signals())
    assert len(all_signals) == 3

    cron_only = list(s.iter_signals(source="cron"))
    assert len(cron_only) == 2
    assert all(sig.source == "cron" for sig in cron_only)


def test_active_signals_filters_expired(tmp_path):
    s = Store(root=tmp_path)
    fresh = datetime.now(timezone.utc).isoformat(timespec="seconds")
    stale = "2000-01-01T00:00:00+00:00"
    s.append_signal(Signal(source="cron", captured_at=fresh, payload={}, ttl_seconds=600))
    s.append_signal(Signal(source="cron", captured_at=stale, payload={}, ttl_seconds=600))
    active = s.active_signals()
    assert len(active) == 1
    assert active[0].captured_at == fresh
