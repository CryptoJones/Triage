# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Tests for the BBS theme system + color gating."""

from __future__ import annotations

import io

import pytest

from triage import theme


def test_themes_registry_has_three_named():
    assert set(theme.THEMES) == {"bbs", "modern", "mono"}


def test_default_theme_is_bbs():
    assert theme.DEFAULT_THEME == "bbs"
    assert theme.get().name == "bbs"


def test_resolve_arg_wins_over_env(monkeypatch):
    monkeypatch.setenv("TRIAGE_THEME", "modern")
    assert theme.resolve_theme_name("mono") == "mono"


def test_resolve_env_used_when_no_arg(monkeypatch):
    monkeypatch.setenv("TRIAGE_THEME", "modern")
    assert theme.resolve_theme_name(None) == "modern"


def test_resolve_unknown_name_falls_back_to_default(monkeypatch):
    monkeypatch.delenv("TRIAGE_THEME", raising=False)
    assert theme.resolve_theme_name("nonsense") == "bbs"


def test_mono_theme_has_no_color_escapes():
    t = theme.get("mono")
    # Every color slot should be empty
    assert t.banner == ""
    assert t.header == ""
    assert t.priority_high == ""
    assert t.subject == ""
    assert t.warning == ""


def test_bbs_theme_uses_double_line_box_drawing():
    t = theme.get("bbs")
    assert t.box_tl == "╔"
    assert t.box_h == "═"
    assert t.box_br == "╝"


def test_modern_theme_uses_light_box_drawing():
    t = theme.get("modern")
    assert t.box_tl == "┌"
    assert t.box_h == "─"


def test_paint_no_op_when_disabled():
    t = theme.get("bbs")
    assert theme.paint("hi", t.header, enabled=False) == "hi"


def test_paint_no_op_when_code_empty():
    assert theme.paint("hi", "", enabled=True) == "hi"


def test_paint_wraps_with_reset_when_enabled():
    t = theme.get("bbs")
    out = theme.paint("hi", t.header, enabled=True)
    assert out.startswith("\x1b[")
    assert out.endswith(theme.RESET)
    assert "hi" in out


def test_should_color_false_when_NO_COLOR_set(monkeypatch):
    monkeypatch.setenv("NO_COLOR", "1")
    fake_tty = io.StringIO()
    fake_tty.isatty = lambda: True  # would normally enable color
    assert theme.should_color(fake_tty) is False


def test_should_color_false_when_not_a_tty(monkeypatch):
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.delenv("FORCE_COLOR", raising=False)
    fake_pipe = io.StringIO()  # isatty -> AttributeError caught
    assert theme.should_color(fake_pipe) is False


def test_should_color_force_color_overrides_non_tty(monkeypatch):
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.setenv("FORCE_COLOR", "1")
    fake_pipe = io.StringIO()
    assert theme.should_color(fake_pipe) is True


def test_should_color_true_on_real_tty_no_overrides(monkeypatch):
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.delenv("FORCE_COLOR", raising=False)
    fake_tty = io.StringIO()
    fake_tty.isatty = lambda: True
    assert theme.should_color(fake_tty) is True


def test_priority_color_bands():
    t = theme.get("bbs")
    assert theme.priority_color(t, 100) == t.priority_high
    assert theme.priority_color(t, 50) == t.priority_high
    assert theme.priority_color(t, 49) == t.priority_mid
    assert theme.priority_color(t, 10) == t.priority_mid
    assert theme.priority_color(t, 9) == t.priority_low
    assert theme.priority_color(t, 0) == t.priority_low


def test_priority_bar_renders_blocks_proportional():
    t = theme.get("bbs")
    assert theme.priority_bar(t, 100, width=5) == "█████"
    assert theme.priority_bar(t, 0, width=5) == "░░░░░"
    bar50 = theme.priority_bar(t, 50, width=5)
    assert len(bar50) == 5
    # 50 // 20 = 2 full; 50 % 20 = 10 -> half; rest empty
    assert bar50 == "██▒░░"


def test_priority_bar_caps_at_width():
    t = theme.get("bbs")
    bar = theme.priority_bar(t, 100000, width=5)
    assert bar == "█████"
    assert len(bar) == 5


def test_banner_returns_three_lines():
    t = theme.get("bbs")
    lines = theme.banner(t, "TEST", enabled=False, inner_width=10)
    assert len(lines) == 3
    assert lines[0].startswith(t.box_tl)
    assert lines[0].endswith(t.box_tr)
    assert t.box_v in lines[1]
    assert "TEST" in lines[1]
    assert lines[2].startswith(t.box_bl)
    assert lines[2].endswith(t.box_br)


def test_banner_with_color_emits_escapes():
    t = theme.get("bbs")
    lines = theme.banner(t, "TEST", enabled=True, inner_width=10)
    joined = "\n".join(lines)
    assert "\x1b[" in joined
    assert theme.RESET in joined


def test_banner_in_mono_has_no_escapes():
    t = theme.get("mono")
    lines = theme.banner(t, "TEST", enabled=True, inner_width=10)
    for line in lines:
        assert "\x1b[" not in line


def test_mono_box_drawing_is_ascii_only():
    t = theme.get("mono")
    lines = theme.banner(t, "TEST", enabled=False, inner_width=10)
    for line in lines:
        assert all(ord(c) < 128 for c in line)
