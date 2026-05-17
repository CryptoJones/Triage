# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
import json
import os
import sys

import pytest

from triage.cli import main


@pytest.fixture
def home(tmp_path, monkeypatch):
    monkeypatch.setenv("TRIAGE_HOME", str(tmp_path))
    return tmp_path


def test_add_and_list(home, capsys):
    assert main(["add", "first task"]) == 0
    out = capsys.readouterr().out.strip()
    task_id = out
    assert len(task_id) == 12

    assert main(["list"]) == 0
    out = capsys.readouterr().out
    assert task_id in out
    assert "first task" in out


def test_list_empty(home, capsys):
    assert main(["list"]) == 0
    assert "(no tasks)" in capsys.readouterr().out


def test_list_json(home, capsys):
    main(["add", "x"])
    capsys.readouterr()
    assert main(["list", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert len(payload) == 1
    assert payload[0]["subject"] == "x"
    assert "priority" in payload[0]


def test_show_missing_id_exits_nonzero(home, capsys):
    assert main(["show", "deadbeef0000"]) == 1


def test_why_lists_named_contributions(home, capsys):
    main(["add", "weighted", "--base-score", "12"])
    task_id = capsys.readouterr().out.strip()
    assert main(["why", task_id]) == 0
    out = capsys.readouterr().out
    assert "priority = 12" in out
    assert "base_score" in out
    assert "deadline_decay" in out
    assert "cron_window_active" in out


def test_rm_removes(home, capsys):
    main(["add", "to-die"])
    task_id = capsys.readouterr().out.strip()

    assert main(["rm", task_id]) == 0
    capsys.readouterr()

    main(["list"])
    out = capsys.readouterr().out
    assert task_id not in out


def test_higher_base_score_sorts_first(home, capsys):
    main(["add", "low"])
    low = capsys.readouterr().out.strip()
    main(["add", "high", "--base-score", "100"])
    high = capsys.readouterr().out.strip()

    main(["list"])
    out = capsys.readouterr().out
    # high should appear before low
    assert out.index(high) < out.index(low)


def test_tick_prints_count(home, capsys):
    main(["add", "x"])
    capsys.readouterr()
    assert main(["tick"]) == 0
    out = capsys.readouterr().out
    assert "ranked 1 task" in out


def test_blocker_bumps_blocker_above_blocked(home, capsys):
    main(["add", "blocker", "--base-score", "1"])
    blocker_id = capsys.readouterr().out.strip()

    main(["add", "blocked", "--base-score", "100", "--blocked-by", blocker_id])
    blocked_id = capsys.readouterr().out.strip()

    main(["list"])
    out = capsys.readouterr().out
    # blocker should appear FIRST (higher priority) even though base_score=1
    assert out.index(blocker_id) < out.index(blocked_id)


def test_why_surfaces_blocker_transitive_contribution(home, capsys):
    main(["add", "blocker", "--base-score", "1"])
    blocker_id = capsys.readouterr().out.strip()
    main(["add", "blocked", "--base-score", "50", "--blocked-by", blocker_id])
    capsys.readouterr()

    main(["why", blocker_id])
    out = capsys.readouterr().out
    assert "blocker_transitive" in out
    assert "+50" in out  # bumped from 1 -> 51


def test_self_loop_warning_appears_on_stderr(home, capsys, monkeypatch):
    main(["add", "self"])
    task_id = capsys.readouterr().out.strip()

    import json
    p = home / "tasks.json"
    data = json.loads(p.read_text())
    for t in data:
        if t["id"] == task_id:
            t["blocked_by"] = [task_id]
    p.write_text(json.dumps(data, indent=2, sort_keys=True))

    main(["list"])
    captured = capsys.readouterr()
    assert "self-block" in captured.err


def test_doctor_text_output_contains_core_fields(home, capsys, monkeypatch):
    monkeypatch.setenv("TRIAGE_NO_LOG", "1")
    assert main(["doctor"]) == 0
    out = capsys.readouterr().out
    assert "triage v" in out
    assert "locale:" in out
    assert "store:" in out
    assert "log:" in out
    assert str(home) in out


def test_doctor_json_output_has_expected_shape(home, capsys, monkeypatch):
    monkeypatch.setenv("TRIAGE_NO_LOG", "1")
    assert main(["doctor", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert "version" in payload
    assert "python" in payload
    assert payload["store"]["path"] == str(home)
    assert payload["log"]["enabled"] is False  # TRIAGE_NO_LOG=1
    assert payload["locale"]["resolved"] in {"en", "es", "fr"}  # whatever resolved
    assert payload["locale"]["drift"] == 0
    assert payload["locale"]["available"] >= 17


def test_doctor_reports_explicit_env_locale_source(home, capsys, monkeypatch):
    monkeypatch.setenv("TRIAGE_NO_LOG", "1")
    monkeypatch.setenv("TRIAGE_LANG", "es")
    assert main(["doctor", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["locale"]["resolved"] == "es"
    assert payload["locale"]["source"] == "TRIAGE_LANG"
