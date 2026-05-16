# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Tests for `triage signal manual` CLI verb + rule_manual_bump."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from triage.cli import main
from triage.model import Signal, Task
from triage.rules import rule_manual_bump
from triage.store import Store


@pytest.fixture
def home(tmp_path, monkeypatch):
    monkeypatch.setenv("TRIAGE_HOME", str(tmp_path))
    monkeypatch.delenv("TRIAGE_NO_LOG", raising=False)
    monkeypatch.delenv("TRIAGE_LOG_FILE", raising=False)
    return tmp_path


def test_signal_manual_emits_signal(home, capsys):
    main(["add", "x"])
    task_id = capsys.readouterr().out.strip()

    rc = main([
        "signal", "manual",
        "--source", "runpodboss",
        "--affects", task_id,
        "--bump", "100",
        "--ttl", "600",
        "--note", "balance below warning threshold",
    ])
    assert rc == 0
    out = capsys.readouterr().out
    assert "signal emitted" in out
    assert "source=runpodboss" in out
    assert "bump=100" in out


def test_signal_persisted_to_store(home, capsys):
    main(["add", "x"])
    task_id = capsys.readouterr().out.strip()

    main([
        "signal", "manual",
        "--source", "runpodboss",
        "--affects", task_id,
        "--bump", "50",
        "--ttl", "300",
    ])
    capsys.readouterr()

    store = Store(root=home)
    sigs = list(store.iter_signals(source="runpodboss"))
    assert len(sigs) == 1
    assert sigs[0].payload["bump"] == 50
    assert sigs[0].affects == [task_id]
    assert sigs[0].ttl_seconds == 300


def test_signal_without_affects_targets_all(home, capsys):
    main(["add", "x"])
    main(["add", "y"])
    capsys.readouterr()

    main(["signal", "manual", "--source", "operator", "--bump", "5"])
    store = Store(root=home)
    sigs = list(store.iter_signals(source="operator"))
    assert sigs[0].affects == []  # empty = applies to all per existing Signal semantics


def test_signal_bump_lifts_target_above_unbumped(home, capsys):
    main(["add", "calm",   "--base-score", "10"])
    calm_id = capsys.readouterr().out.strip()
    main(["add", "bumped", "--base-score", "1"])
    bumped_id = capsys.readouterr().out.strip()
    main([
        "signal", "manual",
        "--source", "operator",
        "--affects", bumped_id,
        "--bump", "100",
        "--ttl", "600",
    ])
    capsys.readouterr()

    main(["list"])
    out = capsys.readouterr().out
    # bumped (base 1 + manual 100 = 101) should outrank calm (10)
    assert out.index(bumped_id) < out.index(calm_id)


def test_signal_optional_state_flag(home, capsys):
    main(["add", "x"])
    task_id = capsys.readouterr().out.strip()
    main([
        "signal", "manual",
        "--source", "runpodboss",
        "--affects", task_id,
        "--bump", "150",
        "--ttl", "1800",
        "--state", "critical",
    ])
    store = Store(root=home)
    sigs = list(store.iter_signals(source="runpodboss"))
    assert sigs[0].payload["state"] == "critical"


def test_signal_event_logged(home, capsys):
    log_path = home / "events.log"
    main(["add", "x"])
    task_id = capsys.readouterr().out.strip()
    main([
        "--log-file", str(log_path),
        "signal", "manual",
        "--source", "runpodboss",
        "--affects", task_id,
        "--bump", "50",
        "--ttl", "300",
    ])
    import json
    rows = [json.loads(l) for l in log_path.read_text().splitlines() if l]
    signal_row = [r for r in rows if r["event"] == "signal"][0]
    assert signal_row["source"] == "runpodboss"
    assert signal_row["bump"] == 50


# ---------- rule_manual_bump ----------

def test_manual_bump_zero_without_signal():
    assert rule_manual_bump(Task(id="A", subject="a"), []) == 0


def test_manual_bump_sums_bumps_from_any_source():
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    sigs = [
        Signal(source="runpodboss", captured_at=ts, payload={"bump": 50}, affects=["A"]),
        Signal(source="operator",   captured_at=ts, payload={"bump": 30}, affects=["A"]),
    ]
    assert rule_manual_bump(Task(id="A", subject="a"), sigs) == 80


def test_manual_bump_ignores_first_class_sources():
    """First-class sources have dedicated rules — don't double-count."""
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    sigs = [
        Signal(source="cron",        captured_at=ts, payload={"bump": 99, "active": True}, affects=["A"]),
        Signal(source="github-ci",   captured_at=ts, payload={"bump": 99, "state": "failure"}, affects=["A"]),
        Signal(source="github-pr",   captured_at=ts, payload={"bump": 99, "state": "stale"}, affects=["A"]),
        Signal(source="runpod-cost", captured_at=ts, payload={"bump": 99, "state": "idle"}, affects=["A"]),
    ]
    assert rule_manual_bump(Task(id="A", subject="a"), sigs) == 0


def test_manual_bump_ignores_non_int_bump():
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    sigs = [
        Signal(source="x", captured_at=ts, payload={"bump": "not an int"}, affects=["A"]),
        Signal(source="x", captured_at=ts, payload={}, affects=["A"]),
        Signal(source="x", captured_at=ts, payload={"bump": 7}, affects=["A"]),
    ]
    assert rule_manual_bump(Task(id="A", subject="a"), sigs) == 7


def test_manual_bump_unscoped_signal_applies_to_all():
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    sig = Signal(source="x", captured_at=ts, payload={"bump": 42}, affects=[])
    assert rule_manual_bump(Task(id="A", subject="a"), [sig]) == 42


def test_manual_bump_ignores_other_tasks():
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    sig = Signal(source="x", captured_at=ts, payload={"bump": 50}, affects=["OTHER"])
    assert rule_manual_bump(Task(id="A", subject="a"), [sig]) == 0
