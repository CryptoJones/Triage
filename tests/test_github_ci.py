# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Tests for the github-ci signal source.

`_fetch_runs` is replaced with a fake at the call boundary — no real
network access happens in this suite.
"""

from __future__ import annotations

import urllib.error

import pytest

from triage.model import Task
from triage.sources import github_ci
from triage.store import Store


def test_parse_tag_accepts_canonical_form():
    t = github_ci.CITarget.parse("gh-ci:CryptoJones/Triage@main")
    assert t == github_ci.CITarget(owner="CryptoJones", repo="Triage", branch="main")


def test_parse_tag_strips_whitespace():
    t = github_ci.CITarget.parse("gh-ci: owner / repo @ branch ")
    assert t.owner == "owner"
    assert t.repo == "repo"
    assert t.branch == "branch"


def test_parse_tag_rejects_non_prefixed():
    assert github_ci.CITarget.parse("nebraska") is None
    assert github_ci.CITarget.parse("repo:owner/name") is None


def test_parse_tag_rejects_missing_at_or_slash():
    assert github_ci.CITarget.parse("gh-ci:owner") is None
    assert github_ci.CITarget.parse("gh-ci:owner@branch") is None
    assert github_ci.CITarget.parse("gh-ci:owner/repo") is None
    assert github_ci.CITarget.parse("gh-ci:owner/repo@") is None
    assert github_ci.CITarget.parse("gh-ci:/repo@branch") is None
    assert github_ci.CITarget.parse("gh-ci:owner/@branch") is None


def test_parse_tag_handles_branch_with_slash():
    """Feature branches like 'feat/cmd-test' should still parse — we rsplit on @."""
    t = github_ci.CITarget.parse("gh-ci:owner/repo@feat/cmd-test")
    assert t.branch == "feat/cmd-test"


def test_classify_in_progress_states():
    for status in ["queued", "in_progress", "requested", "waiting", "pending"]:
        assert github_ci._classify({"status": status, "conclusion": None}) == "in_progress"


def test_classify_success():
    assert github_ci._classify({"status": "completed", "conclusion": "success"}) == "success"


def test_classify_failure_states():
    for c in ["failure", "timed_out", "cancelled", "startup_failure"]:
        assert github_ci._classify({"status": "completed", "conclusion": c}) == "failure"


def test_classify_unknown_falls_through():
    assert github_ci._classify({"status": "completed", "conclusion": "skipped"}) == "unknown"
    assert github_ci._classify({}) == "unknown"


def test_poll_emits_one_signal_per_ci_tagged_task(tmp_path):
    s = Store(root=tmp_path)
    t1 = Task(subject="ci-tagged", tags=["gh-ci:o/r@main"])
    t2 = Task(subject="untagged")
    t3 = Task(subject="other-tag", tags=["release:stable"])
    s.save_tasks([t1, t2, t3])

    def fake_fetch(target, *, token=None):
        return {"workflow_runs": [{"id": 1, "status": "completed", "conclusion": "success", "html_url": "u"}]}

    emitted, warnings = github_ci.poll(s, fetch=fake_fetch)
    assert emitted == 1
    assert warnings == []

    sigs = list(s.iter_signals(source="github-ci"))
    assert len(sigs) == 1
    assert sigs[0].affects == [t1.id]
    assert sigs[0].payload["state"] == "success"
    assert sigs[0].payload["owner"] == "o"


def test_poll_emits_failure_state(tmp_path):
    s = Store(root=tmp_path)
    s.save_tasks([Task(id="X", subject="x", tags=["gh-ci:o/r@main"])])

    def fake_fetch(target, *, token=None):
        return {
            "workflow_runs": [
                {"id": 1, "status": "completed", "conclusion": "failure", "html_url": "u"}
            ]
        }

    github_ci.poll(s, fetch=fake_fetch)
    sigs = list(s.iter_signals(source="github-ci"))
    assert sigs[0].payload["state"] == "failure"
    assert sigs[0].payload["run_id"] == 1


def test_poll_empty_runs_emits_unknown(tmp_path):
    s = Store(root=tmp_path)
    s.save_tasks([Task(subject="x", tags=["gh-ci:o/r@main"])])

    def fake_fetch(target, *, token=None):
        return {"workflow_runs": []}

    github_ci.poll(s, fetch=fake_fetch)
    sigs = list(s.iter_signals(source="github-ci"))
    assert sigs[0].payload["state"] == "unknown"
    assert sigs[0].payload["run_id"] is None


def test_poll_http_error_records_warning_and_continues(tmp_path):
    s = Store(root=tmp_path)
    s.save_tasks([
        Task(id="A", subject="a", tags=["gh-ci:o/repo404@main"]),
        Task(id="B", subject="b", tags=["gh-ci:o/repo200@main"]),
    ])

    def fake_fetch(target, *, token=None):
        if "404" in target.repo:
            raise urllib.error.HTTPError(
                url="http://x", code=404, msg="Not Found", hdrs=None, fp=None
            )
        return {"workflow_runs": [{"id": 9, "status": "completed", "conclusion": "success"}]}

    emitted, warnings = github_ci.poll(s, fetch=fake_fetch)
    assert emitted == 1  # only B succeeded
    assert any("HTTP 404" in w for w in warnings)


def test_poll_url_error_records_warning(tmp_path):
    s = Store(root=tmp_path)
    s.save_tasks([Task(subject="x", tags=["gh-ci:o/r@main"])])

    def fake_fetch(target, *, token=None):
        raise urllib.error.URLError("connection refused")

    emitted, warnings = github_ci.poll(s, fetch=fake_fetch)
    assert emitted == 0
    assert any("fetch failed" in w for w in warnings)


def test_poll_passes_token_through(tmp_path, monkeypatch):
    s = Store(root=tmp_path)
    s.save_tasks([Task(subject="x", tags=["gh-ci:o/r@main"])])
    seen = {}

    def fake_fetch(target, *, token=None):
        seen["token"] = token
        return {"workflow_runs": []}

    monkeypatch.setenv("GITHUB_TOKEN", "ghs_xxx")
    github_ci.poll(s, fetch=fake_fetch)
    assert seen["token"] == "ghs_xxx"


def test_poll_explicit_token_overrides_env(tmp_path, monkeypatch):
    s = Store(root=tmp_path)
    s.save_tasks([Task(subject="x", tags=["gh-ci:o/r@main"])])
    seen = {}

    def fake_fetch(target, *, token=None):
        seen["token"] = token
        return {"workflow_runs": []}

    monkeypatch.setenv("GITHUB_TOKEN", "env-token")
    github_ci.poll(s, fetch=fake_fetch, token="explicit-token")
    assert seen["token"] == "explicit-token"
