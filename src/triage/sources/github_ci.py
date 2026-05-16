# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""GitHub Actions CI signal source.

A task opts in by adding a tag of the form ``gh-ci:owner/repo@branch``
(e.g. ``gh-ci:CryptoJones/Triage@main``). When ``poll()`` runs, this
source queries the GitHub Actions API for the latest workflow run on
that ref and emits a ``github-ci`` signal targeted at the task with
``payload.state`` ∈ {``success``, ``failure``, ``in_progress``,
``unknown``}.

The associated rule ``rule_ci_failing`` (see ``triage.rules``) adds
+50 to the task's priority when a fresh failure signal is active.

Auth: an optional ``GITHUB_TOKEN`` environment variable is read once
at poll time. Unauthenticated polling works for public repos but is
heavily rate-limited (60 req/hr/IP); a token raises that to 5000.

Network access is funneled through the private ``_fetch_runs``
function so tests can monkeypatch it without touching urllib.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone

from ..model import Signal, Task
from ..store import Store

TAG_PREFIX = "gh-ci:"
SOURCE_NAME = "github-ci"
DEFAULT_TTL_SECONDS = 600
USER_AGENT = "triage-scheduler/0.3 (+https://github.com/CryptoJones/Triage)"


@dataclass
class CITarget:
    """Parsed ``gh-ci:owner/repo@branch`` tag."""

    owner: str
    repo: str
    branch: str

    @classmethod
    def parse(cls, tag: str) -> "CITarget | None":
        if not tag.startswith(TAG_PREFIX):
            return None
        rest = tag[len(TAG_PREFIX) :]
        if "@" not in rest or "/" not in rest:
            return None
        slug, branch = rest.rsplit("@", 1)
        if "/" not in slug or not branch:
            return None
        owner, repo = slug.split("/", 1)
        if not owner or not repo:
            return None
        return cls(owner=owner.strip(), repo=repo.strip(), branch=branch.strip())


def _fetch_runs(target: CITarget, *, token: str | None = None) -> dict:
    """Fetch the most recent workflow runs for a repo+branch.

    Returns the parsed JSON body from
    ``GET /repos/{owner}/{repo}/actions/runs?branch={branch}&per_page=5``.
    Raises ``urllib.error.HTTPError`` on non-2xx responses.

    Tests should monkeypatch this function to avoid real network I/O.
    """
    url = (
        f"https://api.github.com/repos/{target.owner}/{target.repo}"
        f"/actions/runs?branch={target.branch}&per_page=5"
    )
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": USER_AGENT,
        "X-GitHub-Api-Version": "2022-11-28",
    })
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _classify(run: dict) -> str:
    """Map a GitHub Actions run object to one of our four states."""
    status = (run.get("status") or "").lower()
    conclusion = (run.get("conclusion") or "").lower()
    if status in ("queued", "in_progress", "requested", "waiting", "pending"):
        return "in_progress"
    if conclusion == "success":
        return "success"
    if conclusion in ("failure", "timed_out", "cancelled", "startup_failure"):
        return "failure"
    return "unknown"


def poll(
    store: Store,
    *,
    now: datetime | None = None,
    token: str | None = None,
    fetch: callable = _fetch_runs,
) -> tuple[int, list[str]]:
    """Walk all tasks, polling github-ci for each gh-ci-tagged target.

    Emits one signal per matching task. Returns ``(emitted_count,
    warnings)``. Network errors per task are caught and recorded as
    warnings — one failed task does not stop the poll.
    """
    ref = now or datetime.now(timezone.utc)
    token = token if token is not None else os.environ.get("GITHUB_TOKEN")
    tasks = store.load_tasks()

    emitted = 0
    warnings: list[str] = []

    for task in tasks:
        for tag in task.tags:
            target = CITarget.parse(tag)
            if target is None:
                continue
            try:
                body = fetch(target, token=token)
            except urllib.error.HTTPError as exc:
                warnings.append(
                    f"{SOURCE_NAME}: HTTP {exc.code} for "
                    f"{target.owner}/{target.repo}@{target.branch}: {exc.reason}"
                )
                continue
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                warnings.append(
                    f"{SOURCE_NAME}: fetch failed for "
                    f"{target.owner}/{target.repo}@{target.branch}: {exc}"
                )
                continue

            runs = body.get("workflow_runs") or []
            if not runs:
                state = "unknown"
                run_id = None
                run_url = None
            else:
                latest = runs[0]
                state = _classify(latest)
                run_id = latest.get("id")
                run_url = latest.get("html_url")

            store.append_signal(
                Signal(
                    source=SOURCE_NAME,
                    captured_at=ref.isoformat(timespec="seconds"),
                    payload={
                        "state": state,
                        "owner": target.owner,
                        "repo": target.repo,
                        "branch": target.branch,
                        "run_id": run_id,
                        "run_url": run_url,
                    },
                    affects=[task.id],
                    ttl_seconds=DEFAULT_TTL_SECONDS,
                )
            )
            emitted += 1

    return emitted, warnings
