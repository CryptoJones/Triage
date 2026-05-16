# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Tests for the runpod-cost signal source + rule_cost_pressure."""

from __future__ import annotations

import urllib.error
from datetime import datetime, timezone

import pytest

from triage.model import Signal, Task
from triage.rules import rule_cost_pressure
from triage.sources import runpod
from triage.store import Store


def test_parse_tag_accepts_canonical_form():
    t = runpod.PodTarget.parse("runpod:abc123xyz")
    assert t == runpod.PodTarget(pod_id="abc123xyz")


def test_parse_tag_strips_whitespace():
    t = runpod.PodTarget.parse("runpod:  abc123  ")
    assert t.pod_id == "abc123"


def test_parse_tag_rejects_non_prefixed():
    assert runpod.PodTarget.parse("gh-ci:o/r@main") is None
    assert runpod.PodTarget.parse("nebraska") is None


def test_parse_tag_rejects_empty_pod_id():
    assert runpod.PodTarget.parse("runpod:") is None
    assert runpod.PodTarget.parse("runpod:   ") is None


def test_classify_stopped_when_not_running():
    assert runpod._classify({"desiredStatus": "EXITED"}) == "stopped"
    assert runpod._classify({"desiredStatus": "TERMINATED"}) == "stopped"
    assert runpod._classify({"desiredStatus": ""}) == "stopped"


def test_classify_idle_when_low_util_for_long_uptime():
    pod = {
        "desiredStatus": "RUNNING",
        "runtime": {
            "uptimeInSeconds": 3600,
            "gpus": [{"gpuUtilPercent": 2}, {"gpuUtilPercent": 4}],
        },
    }
    assert runpod._classify(pod) == "idle"


def test_classify_running_when_high_util():
    pod = {
        "desiredStatus": "RUNNING",
        "runtime": {
            "uptimeInSeconds": 3600,
            "gpus": [{"gpuUtilPercent": 80}],
        },
    }
    assert runpod._classify(pod) == "running"


def test_classify_running_when_uptime_below_threshold_even_if_idle():
    """Don't pull the alarm on a freshly-started pod."""
    pod = {
        "desiredStatus": "RUNNING",
        "runtime": {
            "uptimeInSeconds": 60,  # < 600
            "gpus": [{"gpuUtilPercent": 0}],
        },
    }
    assert runpod._classify(pod) == "running"


def test_classify_running_when_gpus_report_no_util():
    pod = {
        "desiredStatus": "RUNNING",
        "runtime": {"uptimeInSeconds": 3600, "gpus": []},
    }
    assert runpod._classify(pod) == "running"


def test_classify_unknown_when_no_runtime_info():
    pod = {"desiredStatus": "RUNNING"}
    assert runpod._classify(pod) == "unknown"


def test_poll_silent_no_op_when_no_tagged_tasks(tmp_path):
    s = Store(root=tmp_path)
    s.save_tasks([Task(subject="untagged"), Task(subject="other", tags=["gh-ci:o/r@main"])])
    emitted, warnings = runpod.poll(s, token="k", fetch=lambda t: {"data": {"myself": {"pods": []}}})
    assert emitted == 0
    assert warnings == []


def test_poll_returns_warning_when_no_token_and_tasks_tagged(tmp_path, monkeypatch):
    monkeypatch.delenv("RUNPOD_API_KEY", raising=False)
    s = Store(root=tmp_path)
    s.save_tasks([Task(subject="x", tags=["runpod:abc123"])])
    emitted, warnings = runpod.poll(s, fetch=lambda t: {"data": {"myself": {"pods": []}}})
    assert emitted == 0
    assert any("no RUNPOD_API_KEY" in w for w in warnings)


def test_poll_emits_idle_signal_for_idle_pod(tmp_path):
    s = Store(root=tmp_path)
    s.save_tasks([Task(id="A", subject="a", tags=["runpod:pod-1"])])

    def fake(tok):
        return {
            "data": {
                "myself": {
                    "pods": [
                        {
                            "id": "pod-1",
                            "name": "training",
                            "desiredStatus": "RUNNING",
                            "costPerHr": 1.59,
                            "runtime": {
                                "uptimeInSeconds": 3600,
                                "gpus": [{"gpuUtilPercent": 1}],
                            },
                        }
                    ]
                }
            }
        }

    emitted, warnings = runpod.poll(s, token="k", fetch=fake)
    assert emitted == 1
    assert warnings == []
    sigs = list(s.iter_signals(source="runpod-cost"))
    assert len(sigs) == 1
    assert sigs[0].payload["state"] == "idle"
    assert sigs[0].payload["pod_id"] == "pod-1"
    assert sigs[0].payload["cost_per_hr"] == 1.59
    assert sigs[0].affects == ["A"]


def test_poll_emits_unknown_when_pod_not_in_account(tmp_path):
    s = Store(root=tmp_path)
    s.save_tasks([Task(id="A", subject="a", tags=["runpod:ghost-pod"])])

    emitted, warnings = runpod.poll(
        s, token="k", fetch=lambda t: {"data": {"myself": {"pods": []}}}
    )
    assert emitted == 1
    assert any("not found" in w for w in warnings)
    sigs = list(s.iter_signals(source="runpod-cost"))
    assert sigs[0].payload["state"] == "unknown"


def test_poll_groups_multiple_tasks_for_same_pod(tmp_path):
    s = Store(root=tmp_path)
    s.save_tasks([
        Task(id="A", subject="a", tags=["runpod:pod-1"]),
        Task(id="B", subject="b", tags=["runpod:pod-1"]),
    ])

    def fake(tok):
        return {
            "data": {
                "myself": {
                    "pods": [
                        {
                            "id": "pod-1",
                            "name": "shared",
                            "desiredStatus": "RUNNING",
                            "runtime": {
                                "uptimeInSeconds": 3600,
                                "gpus": [{"gpuUtilPercent": 1}],
                            },
                        }
                    ]
                }
            }
        }

    emitted, _ = runpod.poll(s, token="k", fetch=fake)
    assert emitted == 1  # one pod => one signal
    sigs = list(s.iter_signals(source="runpod-cost"))
    assert set(sigs[0].affects) == {"A", "B"}


def test_poll_http_error_returns_warning(tmp_path):
    s = Store(root=tmp_path)
    s.save_tasks([Task(subject="x", tags=["runpod:p"])])

    def boom(tok):
        raise urllib.error.HTTPError(url="x", code=401, msg="Unauthorized", hdrs=None, fp=None)

    emitted, warnings = runpod.poll(s, token="k", fetch=boom)
    assert emitted == 0
    assert any("HTTP 401" in w for w in warnings)


def test_poll_url_error_returns_warning(tmp_path):
    s = Store(root=tmp_path)
    s.save_tasks([Task(subject="x", tags=["runpod:p"])])

    def boom(tok):
        raise urllib.error.URLError("dns")

    emitted, warnings = runpod.poll(s, token="k", fetch=boom)
    assert emitted == 0
    assert any("fetch failed" in w for w in warnings)


def test_poll_picks_up_env_token(tmp_path, monkeypatch):
    monkeypatch.setenv("RUNPOD_API_KEY", "ENV-KEY")
    s = Store(root=tmp_path)
    s.save_tasks([Task(id="A", subject="a", tags=["runpod:p"])])
    seen = {}

    def fake(tok):
        seen["token"] = tok
        return {"data": {"myself": {"pods": []}}}

    runpod.poll(s, fetch=fake)
    assert seen["token"] == "ENV-KEY"


def test_poll_explicit_token_overrides_env(tmp_path, monkeypatch):
    monkeypatch.setenv("RUNPOD_API_KEY", "env-token")
    s = Store(root=tmp_path)
    s.save_tasks([Task(subject="x", tags=["runpod:p"])])
    seen = {}

    def fake(tok):
        seen["token"] = tok
        return {"data": {"myself": {"pods": []}}}

    runpod.poll(s, token="explicit", fetch=fake)
    assert seen["token"] == "explicit"


def test_rule_cost_pressure_zero_without_signal():
    assert rule_cost_pressure(Task(id="A", subject="a"), []) == 0


def test_rule_cost_pressure_100_on_idle():
    fresh = datetime.now(timezone.utc).isoformat(timespec="seconds")
    sig = Signal(
        source="runpod-cost",
        captured_at=fresh,
        payload={"state": "idle"},
        affects=["A"],
    )
    assert rule_cost_pressure(Task(id="A", subject="a"), [sig]) == 100


def test_rule_cost_pressure_25_on_running():
    fresh = datetime.now(timezone.utc).isoformat(timespec="seconds")
    sig = Signal(
        source="runpod-cost",
        captured_at=fresh,
        payload={"state": "running"},
        affects=["A"],
    )
    assert rule_cost_pressure(Task(id="A", subject="a"), [sig]) == 25


def test_rule_cost_pressure_zero_on_stopped_or_unknown():
    fresh = datetime.now(timezone.utc).isoformat(timespec="seconds")
    for state in ["stopped", "unknown"]:
        sig = Signal(
            source="runpod-cost",
            captured_at=fresh,
            payload={"state": state},
            affects=["A"],
        )
        assert rule_cost_pressure(Task(id="A", subject="a"), [sig]) == 0


def test_rule_cost_pressure_ignores_other_tasks():
    fresh = datetime.now(timezone.utc).isoformat(timespec="seconds")
    sig = Signal(
        source="runpod-cost",
        captured_at=fresh,
        payload={"state": "idle"},
        affects=["OTHER"],
    )
    assert rule_cost_pressure(Task(id="A", subject="a"), [sig]) == 0


def test_rule_cost_pressure_ignores_wrong_source():
    fresh = datetime.now(timezone.utc).isoformat(timespec="seconds")
    sig = Signal(
        source="cron",
        captured_at=fresh,
        payload={"state": "idle"},
        affects=["A"],
    )
    assert rule_cost_pressure(Task(id="A", subject="a"), [sig]) == 0
