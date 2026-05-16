# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""RunPod cost-pressure signal source.

A task opts in by adding a tag of the form ``runpod:<pod-id>``. When
``poll()`` runs, this source queries the RunPod GraphQL API for the
current state of every referenced pod and emits a ``runpod-cost``
signal targeted at the task(s) that tagged it.

The classification logic is intentionally cautious:

- ``idle`` — pod is ``RUNNING`` AND has been up for >10 minutes AND
  the average reported GPU utilization across its GPUs is < 10%.
  This is the "you are paying for nothing — drain it" signal.
- ``running`` — pod is ``RUNNING`` but utilization is missing or
  above the idle threshold. A weaker "you are paying" reminder.
- ``stopped`` / ``unknown`` — no priority bump.

The companion rule ``rule_cost_pressure`` (see ``triage.rules``)
adds +100 for ``idle`` and +25 for ``running`` — so idle pods float
to the top hard, running pods just nudge up.

Auth is required: ``RUNPOD_API_KEY`` env var, or an explicit
``token=`` argument to ``poll()``. If neither is provided, ``poll()``
returns 0 emitted signals + a single warning explaining why.

Network access is funneled through ``_fetch_pods`` so tests can
monkeypatch the call boundary.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone

from ..model import Signal
from ..store import Store

TAG_PREFIX = "runpod:"
SOURCE_NAME = "runpod-cost"
DEFAULT_TTL_SECONDS = 600
IDLE_UTIL_THRESHOLD = 10.0   # GPU util % below this is "idle" if uptime > IDLE_UPTIME_SECONDS
IDLE_UPTIME_SECONDS = 600    # 10 minutes
USER_AGENT = "triage-scheduler/0.5 (+https://github.com/CryptoJones/Triage)"

GRAPHQL_ENDPOINT = "https://api.runpod.io/graphql"
GRAPHQL_QUERY = (
    "query Pods {"
    "  myself {"
    "    pods {"
    "      id"
    "      name"
    "      desiredStatus"
    "      costPerHr"
    "      runtime {"
    "        uptimeInSeconds"
    "        gpus { gpuUtilPercent }"
    "      }"
    "    }"
    "  }"
    "}"
)


@dataclass
class PodTarget:
    """Parsed ``runpod:<pod-id>`` tag."""

    pod_id: str

    @classmethod
    def parse(cls, tag: str) -> "PodTarget | None":
        if not tag.startswith(TAG_PREFIX):
            return None
        pod_id = tag[len(TAG_PREFIX):].strip()
        if not pod_id:
            return None
        return cls(pod_id=pod_id)


def _fetch_pods(token: str) -> dict:
    """POST the GraphQL query to RunPod. Returns parsed JSON.

    Tests monkeypatch this. Raises urllib HTTPError on non-2xx.
    """
    payload = json.dumps({"query": GRAPHQL_QUERY}).encode("utf-8")
    req = urllib.request.Request(
        GRAPHQL_ENDPOINT,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _classify(pod: dict) -> str:
    """Map a RunPod pod object to one of our four states."""
    status = (pod.get("desiredStatus") or "").upper()
    if status != "RUNNING":
        return "stopped"

    runtime = pod.get("runtime") or {}
    uptime = runtime.get("uptimeInSeconds") or 0
    gpus = runtime.get("gpus") or []

    if gpus:
        utils = [
            g.get("gpuUtilPercent") for g in gpus if g.get("gpuUtilPercent") is not None
        ]
        if utils:
            avg = sum(utils) / len(utils)
            if avg < IDLE_UTIL_THRESHOLD and uptime > IDLE_UPTIME_SECONDS:
                return "idle"
            return "running"

    if uptime > 0:
        return "running"
    return "unknown"


def poll(
    store: Store,
    *,
    now: datetime | None = None,
    token: str | None = None,
    fetch: callable = _fetch_pods,
) -> tuple[int, list[str]]:
    """Walk tasks tagged ``runpod:<pod-id>``, emit one signal per matching pod.

    Returns ``(emitted_count, warnings)``. If no API key is available,
    returns ``(0, ["..."])`` so the loop can carry on. If no tasks
    carry a runpod tag, returns ``(0, [])`` silently — that's not an
    error condition, just a no-op.
    """
    ref = now or datetime.now(timezone.utc)
    token = token if token is not None else os.environ.get("RUNPOD_API_KEY")

    tasks = store.load_tasks()
    pod_to_task_ids: dict[str, list[str]] = defaultdict(list)
    for task in tasks:
        for tag in task.tags:
            target = PodTarget.parse(tag)
            if target is None:
                continue
            pod_to_task_ids[target.pod_id].append(task.id)

    if not pod_to_task_ids:
        return 0, []

    if not token:
        return 0, [
            f"{SOURCE_NAME}: no RUNPOD_API_KEY in env and no explicit token; "
            f"skipping {len(pod_to_task_ids)} tagged pod(s)"
        ]

    try:
        body = fetch(token)
    except urllib.error.HTTPError as exc:
        return 0, [f"{SOURCE_NAME}: HTTP {exc.code}: {exc.reason}"]
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return 0, [f"{SOURCE_NAME}: fetch failed: {exc}"]

    pods = (((body.get("data") or {}).get("myself") or {}).get("pods") or [])
    pods_by_id = {p["id"]: p for p in pods if "id" in p}

    emitted = 0
    warnings: list[str] = []
    captured_at = ref.isoformat(timespec="seconds")

    for pod_id, task_ids in pod_to_task_ids.items():
        pod = pods_by_id.get(pod_id)
        if pod is None:
            warnings.append(
                f"{SOURCE_NAME}: pod {pod_id} not found in account; "
                f"emitting state=unknown for {len(task_ids)} task(s)"
            )
            state = "unknown"
            name = None
            cost = None
            uptime = None
        else:
            state = _classify(pod)
            name = pod.get("name")
            cost = pod.get("costPerHr")
            runtime = pod.get("runtime") or {}
            uptime = runtime.get("uptimeInSeconds")

        store.append_signal(
            Signal(
                source=SOURCE_NAME,
                captured_at=captured_at,
                payload={
                    "state": state,
                    "pod_id": pod_id,
                    "name": name,
                    "cost_per_hr": cost,
                    "uptime_seconds": uptime,
                },
                affects=list(task_ids),
                ttl_seconds=DEFAULT_TTL_SECONDS,
            )
        )
        emitted += 1

    return emitted, warnings
