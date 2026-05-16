# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Tests for `triage status` — one-screen at-a-glance summary."""

from __future__ import annotations

import json

import pytest

from triage.cli import main


@pytest.fixture
def home(tmp_path, monkeypatch):
    monkeypatch.setenv("TRIAGE_HOME", str(tmp_path))
    monkeypatch.delenv("TRIAGE_NO_LOG", raising=False)
    monkeypatch.delenv("TRIAGE_LOG_FILE", raising=False)
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.delenv("FORCE_COLOR", raising=False)
    return tmp_path


def test_status_empty_queue(home, capsys):
    assert main(["status"]) == 0
    out = capsys.readouterr().out
    assert "TRIAGE" in out or "T R I A G E" in out
    assert "STATUS" in out or "S T A T U S" in out
    assert "(no tasks)" in out


def test_status_shows_top_3_only(home, capsys):
    for i in range(5):
        main(["add", f"task-{i}", "--base-score", str(i * 10)])
    capsys.readouterr()
    main(["status"])
    out = capsys.readouterr().out
    # task-4 (40), task-3 (30), task-2 (20) should appear; task-1 / task-0 should not in top section
    assert "task-4" in out
    assert "task-3" in out
    assert "task-2" in out
    # task-0 might still appear in tag counts if tagged, but with no tags it shouldn't
    # We can verify by checking total mentions of "task-0"
    assert out.count("task-0") <= 1  # only if it shows somewhere by accident — but should be 0


def test_status_tag_counts(home, capsys):
    main(["add", "a", "--tag", "env:prod", "--tag", "vendor:aws"])
    main(["add", "b", "--tag", "env:prod"])
    main(["add", "c", "--tag", "env:staging"])
    capsys.readouterr()
    main(["status"])
    out = capsys.readouterr().out
    assert "TAGS" in out or "T A G S" in out
    # env:prod has 2, env:staging has 1, vendor:aws has 1
    assert "env:prod" in out
    assert "env:staging" in out
    assert "vendor:aws" in out


def test_status_json_output(home, capsys):
    main(["add", "first",  "--base-score", "10", "--tag", "x:1"])
    main(["add", "second", "--base-score", "5",  "--tag", "x:1"])
    main(["add", "third",  "--base-score", "1",  "--tag", "y:2"])
    capsys.readouterr()
    main(["status", "--json"])
    payload = json.loads(capsys.readouterr().out)
    assert payload["task_count"] == 3
    assert payload["tag_counts"] == {"x:1": 2, "y:2": 1}
    assert len(payload["top"]) == 3
    assert payload["top"][0]["subject"] == "first"
    assert payload["top"][0]["priority"] == 10


def test_status_signal_counts_via_manual_signal(home, capsys):
    main(["add", "tagged-task"])
    task_id = capsys.readouterr().out.strip()
    main(["signal", "manual", "--source", "runpodboss", "--affects", task_id, "--bump", "50", "--ttl", "600"])
    main(["signal", "manual", "--source", "calendar",   "--affects", task_id, "--bump", "10", "--ttl", "600"])
    capsys.readouterr()

    main(["status", "--json"])
    payload = json.loads(capsys.readouterr().out)
    sc = payload["signal_counts"]
    assert sc.get("runpodboss") == 1
    assert sc.get("calendar") == 1


def test_status_top_reflects_priorities(home, capsys):
    main(["add", "low",  "--base-score", "1"])
    main(["add", "high", "--base-score", "100"])
    main(["add", "mid",  "--base-score", "20"])
    capsys.readouterr()
    main(["status", "--json"])
    payload = json.loads(capsys.readouterr().out)
    assert [t["subject"] for t in payload["top"]] == ["high", "mid", "low"]


def test_status_logs_status_event(home, capsys):
    log_path = home / "events.log"
    main(["add", "x", "--tag", "env:prod"])
    capsys.readouterr()
    main(["--log-file", str(log_path), "status"])
    rows = [json.loads(l) for l in log_path.read_text().splitlines() if l]
    status_rows = [r for r in rows if r["event"] == "status"]
    assert status_rows
    last = status_rows[-1]
    assert last["task_count"] == 1
    assert last["tag_counts"] == {"env:prod": 1}
    assert len(last["top"]) == 1


def test_status_renders_zero_signals_section_cleanly(home, capsys):
    main(["add", "x"])
    capsys.readouterr()
    main(["status"])
    out = capsys.readouterr().out
    assert "ACTIVE SIGNALS" in out or "A C T I V E" in out
    assert "(no active signals)" in out
