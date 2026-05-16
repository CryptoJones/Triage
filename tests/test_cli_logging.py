# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""End-to-end CLI tests for the JSONL log writer."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from triage import log_writer
from triage.cli import main


@pytest.fixture
def home(tmp_path, monkeypatch):
    monkeypatch.setenv("TRIAGE_HOME", str(tmp_path / "triage-home"))
    monkeypatch.delenv("TRIAGE_NO_LOG", raising=False)
    monkeypatch.delenv("TRIAGE_LOG_FILE", raising=False)
    log_writer.reset_for_test()
    yield tmp_path
    log_writer.reset_for_test()


def _lines(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def test_add_emits_log_entry(home):
    log_path = home / "triage.log"
    assert main(["--log-file", str(log_path), "add", "first task", "--base-score", "5"]) == 0
    rows = _lines(log_path)
    assert len(rows) == 1
    assert rows[0]["event"] == "add"
    assert rows[0]["subject"] == "first task"
    assert rows[0]["base_score"] == 5


def test_list_emits_log_entry_with_top(home):
    log_path = home / "triage.log"
    main(["--log-file", str(log_path), "add", "one"])
    main(["--log-file", str(log_path), "add", "two"])
    main(["--log-file", str(log_path), "list"])
    rows = _lines(log_path)
    # add, add, list
    assert [r["event"] for r in rows] == ["add", "add", "list"]
    assert rows[2]["count"] == 2
    assert len(rows[2]["top"]) == 2


def test_tick_logs_emitted_and_ranked_counts(home):
    log_path = home / "triage.log"
    main(["--log-file", str(log_path), "add", "x"])
    main(["--log-file", str(log_path), "tick"])
    rows = _lines(log_path)
    tick = [r for r in rows if r["event"] == "tick"][0]
    assert tick["ranked_count"] == 1
    assert "emitted_cron_signals" in tick


def test_rm_logs_event(home):
    log_path = home / "triage.log"
    main(["--log-file", str(log_path), "add", "soon-deleted"])
    rows = _lines(log_path)
    task_id = rows[0]["task_id"]
    main(["--log-file", str(log_path), "rm", task_id])
    rows = _lines(log_path)
    assert rows[-1]["event"] == "rm"
    assert rows[-1]["task_id"] == task_id


def test_no_log_flag_suppresses_writes(home):
    log_path = home / "triage.log"
    assert main(["--log-file", str(log_path), "--no-log", "add", "silent"]) == 0
    assert not log_path.exists()


def test_TRIAGE_NO_LOG_env_suppresses_writes(home, monkeypatch):
    monkeypatch.setenv("TRIAGE_NO_LOG", "1")
    log_path = home / "triage.log"
    main(["--log-file", str(log_path), "add", "silent"])
    assert not log_path.exists()


def test_env_log_file_used_when_no_flag(home, monkeypatch):
    log_path = home / "env.log"
    monkeypatch.setenv("TRIAGE_LOG_FILE", str(log_path))
    main(["add", "from-env"])
    rows = _lines(log_path)
    assert rows[0]["subject"] == "from-env"


def test_poll_logs_source_and_emitted(home, monkeypatch):
    log_path = home / "events.log"
    main(["--log-file", str(log_path), "add", "ci-task", "--tag", "gh-ci:o/r@main"])

    from triage.sources import github_ci
    from triage import cli as cli_mod

    def fake(target, *, token=None):
        return {
            "workflow_runs": [
                {"id": 1, "status": "completed", "conclusion": "success", "html_url": "u"}
            ]
        }

    monkeypatch.setitem(
        cli_mod.POLLERS,
        "github-ci",
        lambda store: github_ci.poll(store, fetch=fake),
    )
    main(["--log-file", str(log_path), "poll", "github-ci"])
    rows = _lines(log_path)
    poll_row = [r for r in rows if r["event"] == "poll"][0]
    assert poll_row["source"] == "github-ci"
    assert poll_row["emitted"] == 1
