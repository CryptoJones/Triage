# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Tests for the github-pr signal source + rule_stale_pr."""

from __future__ import annotations

import urllib.error
from datetime import datetime, timedelta, timezone

from triage.model import Signal, Task
from triage.rules import rule_stale_pr
from triage.sources import github_pr
from triage.store import Store


# ---------- Tag parsing ----------

def test_parse_tag_repo_level():
    t = github_pr.PRTarget.parse("gh-pr:owner/repo")
    assert t == github_pr.PRTarget(owner="owner", repo="repo", number=None)


def test_parse_tag_specific_pr():
    t = github_pr.PRTarget.parse("gh-pr:owner/repo#42")
    assert t == github_pr.PRTarget(owner="owner", repo="repo", number=42)


def test_parse_tag_strips_whitespace():
    t = github_pr.PRTarget.parse("gh-pr: owner / repo # 7 ")
    assert t == github_pr.PRTarget(owner="owner", repo="repo", number=7)


def test_parse_tag_rejects_non_prefix():
    assert github_pr.PRTarget.parse("gh-ci:owner/repo@main") is None
    assert github_pr.PRTarget.parse("runpod:abc") is None


def test_parse_tag_rejects_malformed():
    assert github_pr.PRTarget.parse("gh-pr:") is None
    assert github_pr.PRTarget.parse("gh-pr:owner") is None
    assert github_pr.PRTarget.parse("gh-pr:/repo") is None
    assert github_pr.PRTarget.parse("gh-pr:owner/") is None
    assert github_pr.PRTarget.parse("gh-pr:owner/repo#abc") is None  # not int
    assert github_pr.PRTarget.parse("gh-pr:owner/repo#0") is None
    assert github_pr.PRTarget.parse("gh-pr:owner/repo#-1") is None


# ---------- Classification ----------

def _now() -> datetime:
    return datetime(2026, 5, 16, 12, 0, tzinfo=timezone.utc)


def test_classify_fresh_when_recently_updated():
    pr = {"updated_at": (_now() - timedelta(hours=1)).isoformat()}
    assert github_pr._classify(pr, now=_now()) == "fresh"


def test_classify_stale_when_older_than_threshold():
    pr = {"updated_at": (_now() - timedelta(hours=48)).isoformat()}
    assert github_pr._classify(pr, now=_now()) == "stale"


def test_classify_boundary_at_24h():
    pr = {"updated_at": (_now() - timedelta(hours=24)).isoformat()}
    assert github_pr._classify(pr, now=_now()) == "stale"


def test_classify_just_under_threshold_is_fresh():
    pr = {"updated_at": (_now() - timedelta(hours=23, minutes=59)).isoformat()}
    assert github_pr._classify(pr, now=_now()) == "fresh"


def test_classify_unknown_when_missing_updated_at():
    assert github_pr._classify({}, now=_now()) == "unknown"


def test_classify_unknown_when_updated_at_malformed():
    assert github_pr._classify({"updated_at": "not-a-date"}, now=_now()) == "unknown"


def test_classify_handles_z_suffix():
    """GitHub uses 'Z' suffix instead of '+00:00'."""
    pr = {"updated_at": "2026-05-15T12:00:00Z"}
    assert github_pr._classify(pr, now=_now()) == "stale"  # 24h ago


# ---------- Polling ----------

def test_poll_silent_no_op_when_no_tagged_tasks(tmp_path):
    s = Store(root=tmp_path)
    s.save_tasks([Task(subject="untagged"), Task(subject="other", tags=["gh-ci:o/r@main"])])
    emitted, warnings = github_pr.poll(s, fetch=lambda t, *, token=None: [])
    assert emitted == 0
    assert warnings == []


def test_poll_emits_one_signal_per_pr_for_repo_level_target(tmp_path):
    s = Store(root=tmp_path)
    s.save_tasks([Task(id="A", subject="a", tags=["gh-pr:o/r"])])

    def fake(target, *, token=None):
        return [
            {"number": 1, "title": "Pr1", "updated_at": (_now() - timedelta(hours=2)).isoformat(), "html_url": "u1"},
            {"number": 2, "title": "Pr2", "updated_at": (_now() - timedelta(hours=48)).isoformat(), "html_url": "u2"},
        ]

    emitted, warnings = github_pr.poll(s, now=_now(), token="k", fetch=fake)
    assert emitted == 2
    assert warnings == []

    sigs = list(s.iter_signals(source="github-pr"))
    states = sorted(sig.payload["state"] for sig in sigs)
    assert states == ["fresh", "stale"]
    for sig in sigs:
        assert sig.affects == ["A"]


def test_poll_single_pr_target_emits_one_signal(tmp_path):
    s = Store(root=tmp_path)
    s.save_tasks([Task(id="A", subject="a", tags=["gh-pr:o/r#7"])])

    def fake(target, *, token=None):
        return [{"number": 7, "title": "X", "updated_at": (_now() - timedelta(hours=30)).isoformat(), "html_url": "u"}]

    emitted, _ = github_pr.poll(s, now=_now(), token="k", fetch=fake)
    assert emitted == 1
    sigs = list(s.iter_signals(source="github-pr"))
    assert sigs[0].payload["state"] == "stale"
    assert sigs[0].payload["number"] == 7


def test_poll_single_pr_404_emits_missing_signal(tmp_path):
    s = Store(root=tmp_path)
    s.save_tasks([Task(id="A", subject="a", tags=["gh-pr:o/r#999"])])

    def fake(target, *, token=None):
        return []  # mimics fetch's 404 → empty list

    emitted, _ = github_pr.poll(s, now=_now(), token="k", fetch=fake)
    assert emitted == 1
    sigs = list(s.iter_signals(source="github-pr"))
    assert sigs[0].payload["state"] == "missing"
    assert sigs[0].payload["number"] == 999


def test_poll_repo_level_with_no_open_prs_is_silent(tmp_path):
    s = Store(root=tmp_path)
    s.save_tasks([Task(id="A", subject="a", tags=["gh-pr:o/r"])])

    def fake(target, *, token=None):
        return []

    emitted, warnings = github_pr.poll(s, now=_now(), token="k", fetch=fake)
    assert emitted == 0
    assert warnings == []


def test_poll_groups_multiple_tasks_for_same_target(tmp_path):
    s = Store(root=tmp_path)
    s.save_tasks([
        Task(id="A", subject="a", tags=["gh-pr:o/r"]),
        Task(id="B", subject="b", tags=["gh-pr:o/r"]),
    ])

    def fake(target, *, token=None):
        return [{"number": 1, "updated_at": (_now() - timedelta(hours=1)).isoformat()}]

    emitted, _ = github_pr.poll(s, now=_now(), token="k", fetch=fake)
    assert emitted == 1  # one PR, one signal
    sigs = list(s.iter_signals(source="github-pr"))
    assert set(sigs[0].affects) == {"A", "B"}


def test_poll_http_error_returns_warning(tmp_path):
    s = Store(root=tmp_path)
    s.save_tasks([Task(subject="x", tags=["gh-pr:o/r"])])

    def boom(target, *, token=None):
        raise urllib.error.HTTPError(url="x", code=403, msg="Rate Limited", hdrs=None, fp=None)

    emitted, warnings = github_pr.poll(s, token="k", fetch=boom)
    assert emitted == 0
    assert any("HTTP 403" in w for w in warnings)


def test_poll_url_error_returns_warning(tmp_path):
    s = Store(root=tmp_path)
    s.save_tasks([Task(subject="x", tags=["gh-pr:o/r"])])

    def boom(target, *, token=None):
        raise urllib.error.URLError("dns")

    emitted, warnings = github_pr.poll(s, token="k", fetch=boom)
    assert emitted == 0
    assert any("fetch failed" in w for w in warnings)


def test_poll_continues_after_one_target_fails(tmp_path):
    s = Store(root=tmp_path)
    s.save_tasks([
        Task(id="A", subject="a", tags=["gh-pr:bad/repo"]),
        Task(id="B", subject="b", tags=["gh-pr:good/repo"]),
    ])

    def fake(target, *, token=None):
        if target.repo == "repo" and target.owner == "bad":
            raise urllib.error.HTTPError(url="x", code=404, msg="Not Found", hdrs=None, fp=None)
        return [{"number": 1, "updated_at": (_now() - timedelta(hours=1)).isoformat()}]

    emitted, warnings = github_pr.poll(s, now=_now(), token="k", fetch=fake)
    assert emitted == 1  # only good/repo succeeded
    assert any("HTTP 404" in w for w in warnings)


def test_poll_uses_env_token(tmp_path, monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "ghs_env")
    s = Store(root=tmp_path)
    s.save_tasks([Task(subject="x", tags=["gh-pr:o/r"])])
    seen = {}

    def fake(target, *, token=None):
        seen["token"] = token
        return []

    github_pr.poll(s, fetch=fake)
    assert seen["token"] == "ghs_env"


# ---------- Rule ----------

def test_rule_stale_pr_zero_without_signal():
    assert rule_stale_pr(Task(id="A", subject="a"), []) == 0


def test_rule_stale_pr_20_on_stale():
    fresh_ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    sig = Signal(
        source="github-pr",
        captured_at=fresh_ts,
        payload={"state": "stale"},
        affects=["A"],
    )
    assert rule_stale_pr(Task(id="A", subject="a"), [sig]) == 20


def test_rule_stale_pr_zero_on_fresh_or_missing_or_unknown():
    fresh_ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    for state in ["fresh", "missing", "unknown"]:
        sig = Signal(
            source="github-pr",
            captured_at=fresh_ts,
            payload={"state": state},
            affects=["A"],
        )
        assert rule_stale_pr(Task(id="A", subject="a"), [sig]) == 0


def test_rule_stale_pr_ignores_other_tasks():
    fresh_ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    sig = Signal(
        source="github-pr",
        captured_at=fresh_ts,
        payload={"state": "stale"},
        affects=["OTHER"],
    )
    assert rule_stale_pr(Task(id="A", subject="a"), [sig]) == 0


def test_rule_stale_pr_ignores_wrong_source():
    fresh_ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    sig = Signal(
        source="github-ci",
        captured_at=fresh_ts,
        payload={"state": "stale"},
        affects=["A"],
    )
    assert rule_stale_pr(Task(id="A", subject="a"), [sig]) == 0
