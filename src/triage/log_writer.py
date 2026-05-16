# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""JSONL event log writer.

Triage emits one JSON line per CLI invocation (and per signal-source
poll) to a log file that external agents can tail and parse. This is
strictly a one-way side channel — Triage writes, agents read.

Default path is ``/var/log/triage.log`` (Aaron's request, so log
output lives in the standard system log directory). If that path is
not writable (the common case for non-root invocations on a fresh
install), the writer silently falls back to
``~/.triage/triage.log`` and emits a single one-time warning on
stderr describing the fallback.

Configuration precedence (highest to lowest):

1. ``--log-file PATH`` CLI flag (or ``--no-log`` to disable).
2. ``TRIAGE_NO_LOG=1`` environment variable (disable).
3. ``TRIAGE_LOG_FILE=PATH`` environment variable.
4. ``/var/log/triage.log`` default.

Event format::

    {"ts": "2026-05-16T03:51:00+00:00", "event": "list", ...fields...}

Each entry is appended atomically (single ``write()`` of one
newline-terminated JSON object), so a tailing agent never sees a
partial line.
"""

from __future__ import annotations

import errno
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_LOG_PATH = Path("/var/log/triage.log")
FALLBACK_LOG_PATH = Path.home() / ".triage" / "triage.log"

# Module-level cache so the fallback warning fires only once per process,
# and so subsequent calls don't re-stat the path on every event.
_resolved_path: Path | None = None
_disabled: bool = False
_warned: bool = False


def _writable(path: Path) -> bool:
    """Can we open `path` for append without raising?

    Tries to create parent dir + open the file. Returns False on any
    PermissionError, OSError(EACCES/EPERM), or filesystem-readonly.
    """
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8"):
            pass
        return True
    except PermissionError:
        return False
    except OSError as exc:
        if exc.errno in (errno.EACCES, errno.EPERM, errno.EROFS):
            return False
        # Unexpected error — bubble up via the False return; caller can
        # fall back. We don't want one filesystem quirk to crash the CLI.
        return False


def configure(
    *,
    path: str | os.PathLike | None = None,
    disabled: bool = False,
) -> Path | None:
    """Resolve the effective log path or disable logging.

    Returns the resolved path (a ``Path``) if logging is enabled, or
    ``None`` if disabled (either by flag, env, or because both the
    default and the fallback are unwritable).
    """
    global _resolved_path, _disabled, _warned
    _resolved_path = None
    _disabled = False
    _warned = False

    if disabled or os.environ.get("TRIAGE_NO_LOG"):
        _disabled = True
        return None

    if path is None:
        env_path = os.environ.get("TRIAGE_LOG_FILE")
        candidate = Path(env_path) if env_path else DEFAULT_LOG_PATH
    else:
        candidate = Path(path)

    if _writable(candidate):
        _resolved_path = candidate
        return candidate

    # Fallback path. If the user explicitly set a custom path and we
    # can't write to it, that's a configuration error — warn loudly
    # and stop (don't silently re-route their explicit choice).
    if path is not None or os.environ.get("TRIAGE_LOG_FILE"):
        print(
            f"triage: log path {candidate} is not writable; "
            f"logging disabled (set TRIAGE_NO_LOG=1 to silence).",
            file=sys.stderr,
        )
        _disabled = True
        return None

    # Default path fallback: try ~/.triage/triage.log silently and
    # emit a one-time stderr breadcrumb if successful.
    if _writable(FALLBACK_LOG_PATH):
        _resolved_path = FALLBACK_LOG_PATH
        if not _warned:
            print(
                f"triage: {DEFAULT_LOG_PATH} not writable, "
                f"logging to {FALLBACK_LOG_PATH} instead "
                f"(create + chown {DEFAULT_LOG_PATH} to use the standard path).",
                file=sys.stderr,
            )
            _warned = True
        return FALLBACK_LOG_PATH

    # Neither writable — disable, with a warning, so the CLI still works.
    if not _warned:
        print(
            f"triage: neither {DEFAULT_LOG_PATH} nor {FALLBACK_LOG_PATH} "
            f"is writable; events will not be logged.",
            file=sys.stderr,
        )
        _warned = True
    _disabled = True
    return None


def get_path() -> Path | None:
    """Return the currently resolved log path, or None if disabled.

    Calls ``configure()`` with defaults if not already configured.
    """
    if _resolved_path is None and not _disabled:
        configure()
    return _resolved_path


def is_enabled() -> bool:
    return get_path() is not None


def log(event: str, **fields: Any) -> None:
    """Append a single JSONL event line to the configured log path.

    Errors during write are swallowed — logging is a side channel and
    must never break the CLI's primary behavior.
    """
    path = get_path()
    if path is None:
        return

    entry = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "event": event,
    }
    # Merge user-provided fields; user fields cannot overwrite ts/event.
    for k, v in fields.items():
        if k in ("ts", "event"):
            continue
        entry[k] = v

    try:
        line = json.dumps(entry, sort_keys=True, default=str) + "\n"
        with path.open("a", encoding="utf-8") as fh:
            fh.write(line)
    except (OSError, TypeError, ValueError):
        # Side-channel failures must not break the CLI.
        return


def reset_for_test() -> None:
    """Reset module-level state. Used by tests to get a clean slate."""
    global _resolved_path, _disabled, _warned
    _resolved_path = None
    _disabled = False
    _warned = False
