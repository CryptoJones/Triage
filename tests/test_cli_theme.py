# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""CLI-surface tests for the theme system end-to-end."""

from __future__ import annotations

import pytest

from triage.cli import main


@pytest.fixture
def home(tmp_path, monkeypatch):
    monkeypatch.setenv("TRIAGE_HOME", str(tmp_path))
    monkeypatch.delenv("TRIAGE_THEME", raising=False)
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.delenv("FORCE_COLOR", raising=False)
    return tmp_path


def test_theme_subcommand_lists_themes(home, capsys):
    assert main(["theme"]) == 0
    out = capsys.readouterr().out
    assert "bbs" in out
    assert "modern" in out
    assert "mono" in out
    assert "default" in out.lower()


def test_theme_preview_renders_sample_rows(home, capsys):
    assert main(["theme", "--name", "bbs"]) == 0
    out = capsys.readouterr().out
    # Banner + 3 mock rows
    assert "theme preview: bbs" in out
    assert "Critical hotfix" in out
    assert "Deploy migration" in out
    assert "Catch up on email" in out


def test_no_color_flag_strips_ansi_from_output(home, capsys, monkeypatch):
    monkeypatch.setenv("FORCE_COLOR", "1")  # would normally enable color
    main(["add", "x", "--base-score", "10"])
    capsys.readouterr()
    assert main(["--no-color", "list"]) == 0
    out = capsys.readouterr().out
    assert "\x1b[" not in out


def test_mono_theme_strips_ansi_even_with_FORCE_COLOR(home, capsys, monkeypatch):
    monkeypatch.setenv("FORCE_COLOR", "1")
    main(["add", "x", "--base-score", "10"])
    capsys.readouterr()
    assert main(["--theme", "mono", "list"]) == 0
    out = capsys.readouterr().out
    assert "\x1b[" not in out


def test_NO_COLOR_env_disables_color(home, capsys, monkeypatch):
    monkeypatch.setenv("FORCE_COLOR", "1")
    monkeypatch.setenv("NO_COLOR", "1")
    main(["add", "x", "--base-score", "10"])
    capsys.readouterr()
    main(["--theme", "bbs", "list"])
    out = capsys.readouterr().out
    assert "\x1b[" not in out


def test_bbs_theme_emits_ansi_when_forced(home, capsys, monkeypatch):
    monkeypatch.setenv("FORCE_COLOR", "1")
    main(["add", "x", "--base-score", "10"])
    capsys.readouterr()
    main(["--theme", "bbs", "list"])
    out = capsys.readouterr().out
    assert "\x1b[" in out  # at least one escape sequence
    assert "T R I A G E" in out  # banner present
    assert "╔" in out  # double-line box from bbs theme


def test_modern_theme_uses_light_box_drawing(home, capsys, monkeypatch):
    monkeypatch.setenv("FORCE_COLOR", "1")
    main(["add", "x", "--base-score", "10"])
    capsys.readouterr()
    main(["--theme", "modern", "list"])
    out = capsys.readouterr().out
    assert "┌" in out  # light corner
    assert "╔" not in out  # no heavy corner


def test_tick_uses_theme(home, capsys, monkeypatch):
    monkeypatch.setenv("FORCE_COLOR", "1")
    main(["add", "x", "--base-score", "10"])
    capsys.readouterr()
    main(["--theme", "bbs", "tick"])
    out = capsys.readouterr().out
    assert "T R I A G E   T I C K" in out
    assert "ranked 1 task" in out


def test_unknown_theme_rejected_by_argparse(home, capsys):
    with pytest.raises(SystemExit):
        main(["--theme", "neon-2049", "list"])
