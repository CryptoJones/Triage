# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""CLI surface tests for `triage poll <source>`."""

from __future__ import annotations

import pytest

from triage.cli import main


@pytest.fixture
def home(tmp_path, monkeypatch):
    monkeypatch.setenv("TRIAGE_HOME", str(tmp_path))
    return tmp_path


def test_poll_unknown_source_exits_nonzero(home, capsys):
    assert main(["poll", "no-such-source"]) == 1
    assert "unknown source" in capsys.readouterr().err


def test_poll_github_ci_invokes_poller(home, capsys, monkeypatch):
    main(["add", "ci-tagged", "--tag", "gh-ci:o/r@main"])
    capsys.readouterr()

    from triage.sources import github_ci

    def fake_fetch(target, *, token=None):
        return {
            "workflow_runs": [
                {"id": 42, "status": "completed", "conclusion": "failure", "html_url": "u"}
            ]
        }

    monkeypatch.setattr(github_ci, "_fetch_runs", fake_fetch)
    # Re-wire the POLLERS entry to use the patched module
    from triage import cli

    monkeypatch.setitem(
        cli.POLLERS, "github-ci", lambda store: github_ci.poll(store, fetch=fake_fetch)
    )

    assert main(["poll", "github-ci"]) == 0
    out = capsys.readouterr().out
    assert "emitted 1 signal(s)" in out


def test_poll_failure_signal_bumps_via_tick(home, capsys, monkeypatch):
    main(["add", "ci-tagged", "--tag", "gh-ci:o/r@main", "--base-score", "1"])
    ci_id = capsys.readouterr().out.strip()
    main(["add", "calm", "--base-score", "10"])
    capsys.readouterr()

    from triage.sources import github_ci
    from triage import cli

    def fake_fetch(target, *, token=None):
        return {
            "workflow_runs": [
                {"id": 1, "status": "completed", "conclusion": "failure", "html_url": "u"}
            ]
        }

    monkeypatch.setitem(
        cli.POLLERS, "github-ci", lambda store: github_ci.poll(store, fetch=fake_fetch)
    )

    main(["poll", "github-ci"])
    capsys.readouterr()
    main(["list"])
    out = capsys.readouterr().out
    # ci_id should now outrank "calm" because base 1 + ci_failing 50 = 51 > 10
    assert out.index(ci_id) < out.index("calm")  # ci first
