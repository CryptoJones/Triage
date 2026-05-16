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
