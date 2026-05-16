# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
from datetime import datetime, timezone

import pytest

from triage.cron import emit, matches
from triage.model import Task
from triage.store import Store


def _at(year, month, day, hour, minute) -> datetime:
    return datetime(year, month, day, hour, minute, tzinfo=timezone.utc)


def test_matches_wildcard_always_true():
    assert matches("* * * * *", _at(2026, 5, 15, 12, 30)) is True


def test_matches_specific_minute_and_hour():
    assert matches("30 12 * * *", _at(2026, 5, 15, 12, 30)) is True
    assert matches("30 12 * * *", _at(2026, 5, 15, 12, 31)) is False
    assert matches("30 12 * * *", _at(2026, 5, 15, 13, 30)) is False


def test_matches_range():
    expr = "* 9-17 * * *"
    assert matches(expr, _at(2026, 5, 15, 9, 0)) is True
    assert matches(expr, _at(2026, 5, 15, 17, 0)) is True
    assert matches(expr, _at(2026, 5, 15, 18, 0)) is False
    assert matches(expr, _at(2026, 5, 15, 8, 59)) is False


def test_matches_step():
    expr = "*/15 * * * *"
    assert matches(expr, _at(2026, 5, 15, 12, 0)) is True
    assert matches(expr, _at(2026, 5, 15, 12, 15)) is True
    assert matches(expr, _at(2026, 5, 15, 12, 14)) is False


def test_matches_list():
    expr = "0,30 * * * *"
    assert matches(expr, _at(2026, 5, 15, 12, 0)) is True
    assert matches(expr, _at(2026, 5, 15, 12, 30)) is True
    assert matches(expr, _at(2026, 5, 15, 12, 15)) is False


def test_matches_dow_weekdays_only():
    expr = "* * * * 1-5"
    # 2026-05-15 is a Friday (weekday=4 → cron-dow=5)
    assert matches(expr, _at(2026, 5, 15, 12, 0)) is True
    # 2026-05-16 is a Saturday (weekday=5 → cron-dow=6)
    assert matches(expr, _at(2026, 5, 16, 12, 0)) is False
    # 2026-05-17 is a Sunday (weekday=6 → cron-dow=0)
    assert matches(expr, _at(2026, 5, 17, 12, 0)) is False


def test_matches_rejects_malformed_expression():
    with pytest.raises(ValueError):
        matches("* * *", _at(2026, 5, 15, 12, 0))


def test_emit_writes_one_signal_per_cron_task(tmp_path):
    s = Store(root=tmp_path)
    t1 = Task(subject="weekday-only", cron_window="* 9-17 * * 1-5")
    t2 = Task(subject="no-window")
    t3 = Task(subject="malformed", cron_window="not a cron expr")
    s.save_tasks([t1, t2, t3])

    count = emit(s, now=_at(2026, 5, 15, 12, 0))  # Friday noon
    assert count == 1

    signals = list(s.iter_signals(source="cron"))
    assert len(signals) == 1
    assert signals[0].payload["active"] is True
    assert signals[0].affects == [t1.id]


def test_emit_inactive_when_outside_window(tmp_path):
    s = Store(root=tmp_path)
    t = Task(subject="weekday-only", cron_window="* 9-17 * * 1-5")
    s.save_tasks([t])

    emit(s, now=_at(2026, 5, 16, 12, 0))  # Saturday noon
    signals = list(s.iter_signals(source="cron"))
    assert len(signals) == 1
    assert signals[0].payload["active"] is False
