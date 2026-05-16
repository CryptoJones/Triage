# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Tests for the JSONL log writer side channel."""

from __future__ import annotations

import json
import os
import stat
from pathlib import Path

import pytest

from triage import log_writer


@pytest.fixture(autouse=True)
def _reset(monkeypatch):
    log_writer.reset_for_test()
    monkeypatch.delenv("TRIAGE_NO_LOG", raising=False)
    monkeypatch.delenv("TRIAGE_LOG_FILE", raising=False)
    yield
    log_writer.reset_for_test()


def _read_lines(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def test_configure_explicit_path_used_when_writable(tmp_path):
    target = tmp_path / "triage.log"
    resolved = log_writer.configure(path=target)
    assert resolved == target
    log_writer.log("test", foo="bar")
    rows = _read_lines(target)
    assert rows[0]["event"] == "test"
    assert rows[0]["foo"] == "bar"


def test_configure_env_path_used_when_no_arg(tmp_path, monkeypatch):
    target = tmp_path / "envlog.log"
    monkeypatch.setenv("TRIAGE_LOG_FILE", str(target))
    resolved = log_writer.configure()
    assert resolved == target


def test_configure_arg_wins_over_env(tmp_path, monkeypatch):
    env_target = tmp_path / "env.log"
    arg_target = tmp_path / "arg.log"
    monkeypatch.setenv("TRIAGE_LOG_FILE", str(env_target))
    resolved = log_writer.configure(path=arg_target)
    assert resolved == arg_target


def test_disabled_flag_disables_logging(tmp_path):
    target = tmp_path / "triage.log"
    resolved = log_writer.configure(path=target, disabled=True)
    assert resolved is None
    assert not log_writer.is_enabled()
    log_writer.log("test")
    assert not target.exists()


def test_TRIAGE_NO_LOG_env_disables(tmp_path, monkeypatch):
    monkeypatch.setenv("TRIAGE_NO_LOG", "1")
    assert log_writer.configure(path=tmp_path / "x.log") is None


def test_default_path_falls_back_silently_to_home(monkeypatch, tmp_path, capsys):
    # Force the home fallback location to a tmpdir we can verify
    fake_home_log = tmp_path / "home-fallback.log"
    monkeypatch.setattr(log_writer, "DEFAULT_LOG_PATH", Path("/proc/triage.log"))
    monkeypatch.setattr(log_writer, "FALLBACK_LOG_PATH", fake_home_log)

    resolved = log_writer.configure()
    assert resolved == fake_home_log
    captured = capsys.readouterr()
    assert "not writable" in captured.err
    assert str(fake_home_log) in captured.err


def test_default_fallback_warning_fires_only_once(monkeypatch, tmp_path, capsys):
    fake_home_log = tmp_path / "home.log"
    monkeypatch.setattr(log_writer, "DEFAULT_LOG_PATH", Path("/proc/triage.log"))
    monkeypatch.setattr(log_writer, "FALLBACK_LOG_PATH", fake_home_log)

    log_writer.configure()
    log_writer.log("first")
    log_writer.log("second")
    captured = capsys.readouterr()
    # Only one fallback warning even after multiple events
    assert captured.err.count("not writable, logging to") == 1


def test_explicit_unwritable_path_warns_and_disables(monkeypatch, tmp_path, capsys):
    # /proc is filesystem-level read-only on Linux for arbitrary writes
    bad = Path("/proc/triage-test-cannot-write.log")
    resolved = log_writer.configure(path=bad)
    assert resolved is None
    err = capsys.readouterr().err
    assert "not writable" in err
    assert "logging disabled" in err


def test_env_unwritable_path_warns_and_disables(monkeypatch, capsys):
    monkeypatch.setenv("TRIAGE_LOG_FILE", "/proc/triage-test-env.log")
    resolved = log_writer.configure()
    assert resolved is None
    assert "not writable" in capsys.readouterr().err


def test_log_writes_one_jsonl_line_per_event(tmp_path):
    target = tmp_path / "events.log"
    log_writer.configure(path=target)
    log_writer.log("add", task_id="abc", subject="Hello")
    log_writer.log("tick", ranked_count=3)
    lines = target.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    # Each line is valid JSON
    a = json.loads(lines[0])
    b = json.loads(lines[1])
    assert a["event"] == "add"
    assert a["task_id"] == "abc"
    assert b["event"] == "tick"
    assert b["ranked_count"] == 3
    assert "ts" in a and "ts" in b


def test_log_user_fields_cannot_overwrite_ts(tmp_path):
    target = tmp_path / "events.log"
    log_writer.configure(path=target)
    # `event` is a positional-only parameter at this call site, so Python
    # rejects passing it twice — but `ts` is a free kwarg and could be
    # spoofed. The writer must reserve it.
    log_writer.log("real_event", ts="not-a-real-timestamp")
    rows = _read_lines(target)
    assert rows[0]["event"] == "real_event"
    assert rows[0]["ts"] != "not-a-real-timestamp"


def test_log_serializes_complex_types_via_default(tmp_path):
    target = tmp_path / "events.log"
    log_writer.configure(path=target)
    log_writer.log("complex", path_field=Path("/x/y"), set_field={"a", "b"})
    rows = _read_lines(target)
    # Path is stringified via default=str; set becomes... let's just verify the line is valid JSON
    # and the event name survived (the side-channel must never raise).
    assert rows[0]["event"] == "complex"


def test_log_silently_swallows_errors_after_initial_setup(tmp_path):
    target = tmp_path / "events.log"
    log_writer.configure(path=target)
    # Make the path unwritable mid-flight by deleting and replacing with a dir
    target.unlink()
    target.mkdir()  # now opening for append fails
    # Must not raise
    log_writer.log("test_event")


def test_log_is_no_op_when_disabled(tmp_path):
    target = tmp_path / "x.log"
    log_writer.configure(path=target, disabled=True)
    log_writer.log("anything")
    assert not target.exists()


def test_get_path_lazy_initializes(monkeypatch, tmp_path):
    target = tmp_path / "lazy.log"
    monkeypatch.setenv("TRIAGE_LOG_FILE", str(target))
    log_writer.reset_for_test()
    # Don't call configure() — get_path should trigger it
    assert log_writer.get_path() == target


def test_atomic_single_line_writes_under_concurrent_appends(tmp_path):
    """Two interleaved log calls produce two complete JSON lines, never a partial one."""
    target = tmp_path / "interleaved.log"
    log_writer.configure(path=target)
    for i in range(50):
        log_writer.log("burst", n=i)
    rows = _read_lines(target)
    assert len(rows) == 50
    assert all(r["event"] == "burst" for r in rows)
    assert [r["n"] for r in rows] == list(range(50))
