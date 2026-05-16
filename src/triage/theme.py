# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""ANSI theme system for Triage CLI output.

Three themes ship: ``bbs`` (default — 1990s BBS aesthetic with bright
colors, double-line box drawing, and block-character priority bars),
``modern`` (subtle, single-line borders, fewer colors), and ``mono``
(no color, no decoration — safe for pipes, captured output, dumb
terminals).

Color is **disabled automatically** when:

- stdout is not a TTY (e.g. piped to a file or another command);
- the ``NO_COLOR`` environment variable is set to anything non-empty
  (per https://no-color.org/);
- the active theme is ``mono``.

Color can be **forced on** with ``FORCE_COLOR=1`` even when stdout
isn't a TTY — useful for piping into a pager that handles ANSI.

The theme is selectable via:

1. the ``--theme NAME`` CLI flag, or
2. the ``TRIAGE_THEME`` environment variable, or
3. the default (``bbs``).
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass


# ANSI escape building blocks — kept inline rather than a dep for portability.
RESET = "\x1b[0m"


def _esc(*codes: int) -> str:
    return "\x1b[" + ";".join(str(c) for c in codes) + "m"


@dataclass(frozen=True)
class Theme:
    """A theme is a set of ANSI escape strings + a few decoration chars.

    Empty strings mean "render nothing for this slot" — that's how the
    ``mono`` theme degrades cleanly.
    """

    name: str

    # Box drawing
    box_tl: str  # top-left corner
    box_tr: str
    box_bl: str
    box_br: str
    box_h: str   # horizontal
    box_v: str   # vertical
    rule: str    # full-width horizontal rule character

    # Priority bar glyph (used as a fill character for priority "weight")
    bar_full: str
    bar_half: str
    bar_empty: str

    # Color / style escapes
    banner: str       # for the title banner
    header: str       # for column headers and section headings
    id_col: str       # task id rendering
    priority_high: str
    priority_mid: str
    priority_low: str
    subject: str
    rule_contrib_plus: str   # for "+ name: +delta" lines
    rule_contrib_zero: str   # for "· name: +0" lines
    warning: str
    success: str
    dim: str
    accent: str       # for the lead character / bullet


def _bbs() -> Theme:
    return Theme(
        name="bbs",
        box_tl="╔", box_tr="╗", box_bl="╚", box_br="╝",
        box_h="═", box_v="║",
        rule="═",
        bar_full="█", bar_half="▒", bar_empty="░",
        banner=_esc(1, 95),               # bold magenta
        header=_esc(1, 96),               # bold cyan
        id_col=_esc(90),                  # bright black / gray
        priority_high=_esc(1, 93),        # bold yellow
        priority_mid=_esc(1, 92),         # bold green
        priority_low=_esc(36),            # dim cyan
        subject=_esc(1, 97),              # bold white
        rule_contrib_plus=_esc(1, 92),    # bold green
        rule_contrib_zero=_esc(90),       # gray
        warning=_esc(1, 91),              # bold red
        success=_esc(1, 92),              # bold green
        dim=_esc(2),                      # dim
        accent=_esc(1, 95),               # bold magenta
    )


def _modern() -> Theme:
    return Theme(
        name="modern",
        box_tl="┌", box_tr="┐", box_bl="└", box_br="┘",
        box_h="─", box_v="│",
        rule="─",
        bar_full="█", bar_half="▒", bar_empty="·",
        banner=_esc(1, 37),               # bold white
        header=_esc(1, 36),               # bold cyan
        id_col=_esc(90),
        priority_high=_esc(33),           # yellow
        priority_mid=_esc(32),            # green
        priority_low=_esc(36),            # cyan
        subject=_esc(37),                 # white
        rule_contrib_plus=_esc(32),
        rule_contrib_zero=_esc(90),
        warning=_esc(31),                 # red
        success=_esc(32),
        dim=_esc(2),
        accent=_esc(36),
    )


def _mono() -> Theme:
    """No color, no fancy box drawing — minimal ASCII only."""
    return Theme(
        name="mono",
        box_tl="+", box_tr="+", box_bl="+", box_br="+",
        box_h="-", box_v="|",
        rule="-",
        bar_full="#", bar_half="=", bar_empty=".",
        banner="", header="", id_col="",
        priority_high="", priority_mid="", priority_low="",
        subject="", rule_contrib_plus="", rule_contrib_zero="",
        warning="", success="", dim="", accent="",
    )


THEMES: dict[str, callable] = {
    "bbs": _bbs,
    "modern": _modern,
    "mono": _mono,
}

DEFAULT_THEME = "bbs"


def resolve_theme_name(arg: str | None = None) -> str:
    """Pick the theme name from arg / env / default. Unknown names fall to default."""
    name = arg or os.environ.get("TRIAGE_THEME") or DEFAULT_THEME
    if name not in THEMES:
        return DEFAULT_THEME
    return name


def get(name: str | None = None) -> Theme:
    return THEMES[resolve_theme_name(name)]()


def should_color(stream=None) -> bool:
    """Return True iff color should be emitted on the given stream.

    Respects the standard ``NO_COLOR`` (disable) and ``FORCE_COLOR``
    (enable even on non-TTY) environment variables.
    """
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("FORCE_COLOR"):
        return True
    s = stream if stream is not None else sys.stdout
    return bool(getattr(s, "isatty", lambda: False)())


def paint(text: str, code: str, *, enabled: bool = True) -> str:
    """Wrap ``text`` in ``code`` ... RESET. No-op if disabled or code empty."""
    if not enabled or not code:
        return text
    return f"{code}{text}{RESET}"


def priority_color(theme: Theme, priority: int) -> str:
    """Pick the right priority color band for a given numeric priority."""
    if priority >= 50:
        return theme.priority_high
    if priority >= 10:
        return theme.priority_mid
    return theme.priority_low


def priority_bar(theme: Theme, priority: int, *, width: int = 5) -> str:
    """Render a small bar reflecting priority magnitude. Caps at width."""
    if priority <= 0:
        return theme.bar_empty * width
    full = min(width, max(0, priority // 20))
    half = 1 if (priority % 20) >= 10 and full < width else 0
    empty = width - full - half
    return theme.bar_full * full + theme.bar_half * half + theme.bar_empty * empty


def banner(theme: Theme, title: str, *, enabled: bool, inner_width: int = 56) -> list[str]:
    """Render a centered title banner with double-line box drawing."""
    title_padded = title.center(inner_width)
    top = theme.box_tl + theme.box_h * inner_width + theme.box_tr
    middle = theme.box_v + title_padded + theme.box_v
    bottom = theme.box_bl + theme.box_h * inner_width + theme.box_br
    if not enabled or not theme.banner:
        return [top, middle, bottom]
    return [
        paint(top, theme.accent, enabled=enabled),
        paint(theme.box_v, theme.accent, enabled=enabled)
        + paint(title_padded, theme.banner, enabled=enabled)
        + paint(theme.box_v, theme.accent, enabled=enabled),
        paint(bottom, theme.accent, enabled=enabled),
    ]
