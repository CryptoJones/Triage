# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""GitHub PR staleness signal source.

A task opts in by adding a tag of one of two forms:

- ``gh-pr:owner/repo`` — track ALL open PRs in that repo.
- ``gh-pr:owner/repo#N`` — track a specific PR by number.

When ``poll()`` runs, this source queries GitHub for the matching
open PRs and emits one ``github-pr`` signal per PR per affected task,
with ``payload.state`` ∈ {``stale``, ``fresh``, ``missing``,
``unknown``}.

- ``stale`` — PR is open and ``updated_at`` is older than 24 hours.
- ``fresh`` — PR is open and recently updated.
- ``missing`` — specific-PR query returned 404 (PR was deleted or
  the number never existed).
- ``unknown`` — fetch succeeded but the response shape was
  unexpected.

The companion rule ``rule_stale_pr`` (see ``triage.rules``) adds
+20 when a ``stale`` signal targets the task.

Auth is optional but recommended (raises rate limit 60→5000/hr):
``GITHUB_TOKEN`` env var, or an explicit ``token=`` argument.
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

TAG_PREFIX = "gh-pr:"
SOURCE_NAME = "github-pr"
DEFAULT_TTL_SECONDS = 1800
STALE_THRESHOLD_HOURS = 24
USER_AGENT = "triage-scheduler/0.7 (+https://github.com/CryptoJones/Triage)"


@dataclass(frozen=True)
class PRTarget:
    """Parsed ``gh-pr:owner/repo[#N]`` tag."""

    owner: str
    repo: str
    number: int | None  # None = all open PRs for the repo

    @classmethod
    def parse(cls, tag: str) -> "PRTarget | None":
        if not tag.startswith(TAG_PREFIX):
            return None
        rest = tag[len(TAG_PREFIX):].strip()
        if not rest:
            return None
        number: int | None = None
        if "#" in rest:
            slug, num_s = rest.rsplit("#", 1)
            try:
                number = int(num_s.strip())
            except ValueError:
                return None
            if number <= 0:
                return None
        else:
            slug = rest
        if "/" not in slug:
            return None
        owner, repo = slug.split("/", 1)
        owner = owner.strip()
        repo = repo.strip()
        if not owner or not repo:
            return None
        return cls(owner=owner, repo=repo, number=number)


def _fetch_open_prs(target: PRTarget, *, token: str | None = None) -> list[dict]:
    """Return a list of PR objects for the target.

    For a number-less target, queries the open-PR list endpoint
    (``per_page=30``, single page). For a specific number, queries
    the single-PR endpoint and returns a one-element list (or empty
    list on 404). Other HTTP errors propagate as HTTPError.
    """
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": USER_AGENT,
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    if target.number is None:
        url = (
            f"https://api.github.com/repos/{target.owner}/{target.repo}"
            f"/pulls?state=open&per_page=30"
        )
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data if isinstance(data, list) else []

    # Single-PR endpoint
    url = (
        f"https://api.github.com/repos/{target.owner}/{target.repo}"
        f"/pulls/{target.number}"
    )
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return [data]
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return []
        raise


def _classify(pr: dict, *, now: datetime) -> str:
    """Map a PR object to one of our four states."""
    updated = pr.get("updated_at")
    if not updated:
        return "unknown"
    try:
        # GitHub uses 'Z' suffix; Python <3.11 needs an explicit replace.
        when = datetime.fromisoformat(updated.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return "unknown"
    if when.tzinfo is None:
        when = when.replace(tzinfo=timezone.utc)
    age_hours = (now - when).total_seconds() / 3600
    if age_hours >= STALE_THRESHOLD_HOURS:
        return "stale"
    return "fresh"


def poll(
    store: Store,
    *,
    now: datetime | None = None,
    token: str | None = None,
    fetch: callable = _fetch_open_prs,
) -> tuple[int, list[str]]:
    """Walk gh-pr-tagged tasks, emit one signal per matching open PR.

    Per-target errors are caught and recorded as warnings — one failed
    repo does not stop the poll. Returns ``(emitted_count, warnings)``.
    """
    ref = now or datetime.now(timezone.utc)
    token = token if token is not None else os.environ.get("GITHUB_TOKEN")

    tasks = store.load_tasks()
    target_to_tasks: dict[PRTarget, list[str]] = defaultdict(list)
    for task in tasks:
        for tag in task.tags:
            target = PRTarget.parse(tag)
            if target is None:
                continue
            target_to_tasks[target].append(task.id)

    if not target_to_tasks:
        return 0, []

    emitted = 0
    warnings: list[str] = []
    captured_at = ref.isoformat(timespec="seconds")

    for target, task_ids in target_to_tasks.items():
        target_label = f"{target.owner}/{target.repo}"
        if target.number is not None:
            target_label += f"#{target.number}"

        try:
            prs = fetch(target, token=token)
        except urllib.error.HTTPError as exc:
            warnings.append(
                f"{SOURCE_NAME}: HTTP {exc.code} for {target_label}: {exc.reason}"
            )
            continue
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            warnings.append(f"{SOURCE_NAME}: fetch failed for {target_label}: {exc}")
            continue

        if target.number is not None and not prs:
            # Specific-PR target returned empty list → 404.
            store.append_signal(
                Signal(
                    source=SOURCE_NAME,
                    captured_at=captured_at,
                    payload={
                        "state": "missing",
                        "owner": target.owner,
                        "repo": target.repo,
                        "number": target.number,
                    },
                    affects=list(task_ids),
                    ttl_seconds=DEFAULT_TTL_SECONDS,
                )
            )
            emitted += 1
            continue

        if not prs:
            # Repo-level target with no open PRs — emit nothing rather than
            # spamming a noisy "no PRs" signal every poll.
            continue

        for pr in prs:
            state = _classify(pr, now=ref)
            store.append_signal(
                Signal(
                    source=SOURCE_NAME,
                    captured_at=captured_at,
                    payload={
                        "state": state,
                        "owner": target.owner,
                        "repo": target.repo,
                        "number": pr.get("number"),
                        "title": pr.get("title"),
                        "updated_at": pr.get("updated_at"),
                        "html_url": pr.get("html_url"),
                    },
                    affects=list(task_ids),
                    ttl_seconds=DEFAULT_TTL_SECONDS,
                )
            )
            emitted += 1

    return emitted, warnings
