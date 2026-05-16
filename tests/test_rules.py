# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
from datetime import datetime, timedelta, timezone

from triage.model import Signal, Task
from triage.rules import (
    rule_base_score,
    rule_ci_failing,
    rule_cron_window_active,
    rule_deadline_decay,
    score,
)


def test_base_score_returns_field_value():
    assert rule_base_score(Task(subject="s", base_score=7), []) == 7
    assert rule_base_score(Task(subject="s"), []) == 0


def test_deadline_decay_zero_when_no_deadline():
    assert rule_deadline_decay(Task(subject="s"), []) == 0


def test_deadline_decay_past_deadline_yields_max():
    past = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
    assert rule_deadline_decay(Task(subject="s", deadline=past), []) == 100


def test_deadline_decay_progressive_buckets():
    now = datetime.now(timezone.utc)
    in_30min = (now + timedelta(minutes=30)).isoformat()
    in_6h = (now + timedelta(hours=6)).isoformat()
    in_3d = (now + timedelta(days=3)).isoformat()
    in_3w = (now + timedelta(weeks=3)).isoformat()

    assert rule_deadline_decay(Task(subject="s", deadline=in_30min), [], now=now) == 90
    assert rule_deadline_decay(Task(subject="s", deadline=in_6h), [], now=now) == 60
    assert rule_deadline_decay(Task(subject="s", deadline=in_3d), [], now=now) == 30
    assert rule_deadline_decay(Task(subject="s", deadline=in_3w), [], now=now) == 10


def test_deadline_decay_handles_malformed_dates():
    assert rule_deadline_decay(Task(subject="s", deadline="not-a-date"), []) == 0


def test_cron_window_active_requires_matching_source_and_payload():
    t = Task(id="abc", subject="s")
    fresh = datetime.now(timezone.utc).isoformat(timespec="seconds")

    inactive = Signal(source="cron", captured_at=fresh, payload={"active": False}, affects=["abc"])
    active_for_other = Signal(
        source="cron", captured_at=fresh, payload={"active": True}, affects=["other"]
    )
    active_for_this = Signal(
        source="cron", captured_at=fresh, payload={"active": True}, affects=["abc"]
    )
    wrong_source = Signal(source="ci", captured_at=fresh, payload={"active": True}, affects=["abc"])

    assert rule_cron_window_active(t, [inactive]) == 0
    assert rule_cron_window_active(t, [active_for_other]) == 0
    assert rule_cron_window_active(t, [wrong_source]) == 0
    assert rule_cron_window_active(t, [active_for_this]) == 25


def test_cron_window_active_unscoped_signal_applies_to_all():
    t = Task(id="abc", subject="s")
    fresh = datetime.now(timezone.utc).isoformat(timespec="seconds")
    sig = Signal(source="cron", captured_at=fresh, payload={"active": True}, affects=[])
    assert rule_cron_window_active(t, [sig]) == 25


def test_score_composes_rules_additively_with_named_contributions():
    t = Task(subject="s", base_score=10)
    total, contribs = score(t, [])
    assert total == 10
    names = [c.name for c in contribs]
    assert names == [
        "base_score",
        "deadline_decay",
        "cron_window_active",
        "ci_failing",
        "cost_pressure",
    ]
    assert sum(c.delta for c in contribs) == total


def test_ci_failing_zero_when_no_signal():
    assert rule_ci_failing(Task(id="A", subject="a"), []) == 0


def test_ci_failing_bumps_on_matching_failure_signal():
    from datetime import datetime, timezone

    from triage.model import Signal

    fresh = datetime.now(timezone.utc).isoformat(timespec="seconds")
    t = Task(id="A", subject="a")
    sig = Signal(
        source="github-ci",
        captured_at=fresh,
        payload={"state": "failure"},
        affects=["A"],
    )
    assert rule_ci_failing(t, [sig]) == 50


def test_ci_failing_zero_on_success_or_in_progress():
    from datetime import datetime, timezone

    from triage.model import Signal

    fresh = datetime.now(timezone.utc).isoformat(timespec="seconds")
    t = Task(id="A", subject="a")
    for state in ["success", "in_progress", "unknown"]:
        sig = Signal(
            source="github-ci",
            captured_at=fresh,
            payload={"state": state},
            affects=["A"],
        )
        assert rule_ci_failing(t, [sig]) == 0


def test_ci_failing_ignores_other_task_signals():
    from datetime import datetime, timezone

    from triage.model import Signal

    fresh = datetime.now(timezone.utc).isoformat(timespec="seconds")
    t = Task(id="A", subject="a")
    sig = Signal(
        source="github-ci",
        captured_at=fresh,
        payload={"state": "failure"},
        affects=["OTHER"],
    )
    assert rule_ci_failing(t, [sig]) == 0


def test_ci_failing_ignores_wrong_source():
    from datetime import datetime, timezone

    from triage.model import Signal

    fresh = datetime.now(timezone.utc).isoformat(timespec="seconds")
    t = Task(id="A", subject="a")
    sig = Signal(
        source="cron",
        captured_at=fresh,
        payload={"state": "failure"},
        affects=["A"],
    )
    assert rule_ci_failing(t, [sig]) == 0
