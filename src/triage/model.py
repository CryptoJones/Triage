# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Core data model: Task and Signal dataclasses + JSON (de)serialization."""

from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _new_task_id() -> str:
    return uuid.uuid4().hex[:12]


@dataclass
class Task:
    id: str = field(default_factory=_new_task_id)
    subject: str = ""
    description: str = ""
    created_at: str = field(default_factory=_utcnow_iso)
    base_score: int = 0
    tags: list[str] = field(default_factory=list)
    deadline: str | None = None
    blocked_by: list[str] = field(default_factory=list)
    cron_window: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Task:
        known = {f for f in cls.__dataclass_fields__}
        return cls(**{k: v for k, v in d.items() if k in known})


@dataclass
class Signal:
    source: str
    captured_at: str
    payload: dict[str, Any]
    affects: list[str] = field(default_factory=list)
    ttl_seconds: int = 3600

    def is_expired(self, *, now: datetime | None = None) -> bool:
        ref = now or datetime.now(timezone.utc)
        captured = datetime.fromisoformat(self.captured_at)
        if captured.tzinfo is None:
            captured = captured.replace(tzinfo=timezone.utc)
        return (ref - captured).total_seconds() > self.ttl_seconds

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Signal:
        known = {f for f in cls.__dataclass_fields__}
        return cls(**{k: v for k, v in d.items() if k in known})


def dumps(obj: Any) -> str:
    return json.dumps(obj, indent=2, sort_keys=True)
