# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Atomic file-backed persistence for tasks and signals."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Iterator

from .model import Signal, Task


def default_root() -> Path:
    env = os.environ.get("TRIAGE_HOME")
    if env:
        return Path(env)
    return Path.home() / ".triage"


class Store:
    def __init__(self, root: Path | None = None) -> None:
        self.root = Path(root) if root is not None else default_root()
        self.tasks_path = self.root / "tasks.json"
        self.state_dir = self.root / "state"

    def ensure(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        self.state_dir.mkdir(parents=True, exist_ok=True)
        if not self.tasks_path.exists():
            self._write_atomic(self.tasks_path, "[]\n")

    def _write_atomic(self, path: Path, content: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(prefix=".tmp-", dir=str(path.parent))
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                fh.write(content)
            os.replace(tmp, path)
        except Exception:
            try:
                os.unlink(tmp)
            except FileNotFoundError:
                pass
            raise

    def load_tasks(self) -> list[Task]:
        self.ensure()
        raw = json.loads(self.tasks_path.read_text(encoding="utf-8") or "[]")
        return [Task.from_dict(d) for d in raw]

    def save_tasks(self, tasks: list[Task]) -> None:
        self.ensure()
        payload = json.dumps([t.to_dict() for t in tasks], indent=2, sort_keys=True)
        self._write_atomic(self.tasks_path, payload + "\n")

    def append_signal(self, signal: Signal) -> None:
        self.ensure()
        path = self.state_dir / f"{signal.source}.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(signal.to_dict(), sort_keys=True))
            fh.write("\n")

    def iter_signals(self, source: str | None = None) -> Iterator[Signal]:
        self.ensure()
        files = (
            [self.state_dir / f"{source}.jsonl"]
            if source
            else sorted(self.state_dir.glob("*.jsonl"))
        )
        for path in files:
            if not path.exists():
                continue
            with path.open("r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    yield Signal.from_dict(json.loads(line))

    def active_signals(self) -> list[Signal]:
        return [s for s in self.iter_signals() if not s.is_expired()]
