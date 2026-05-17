# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""End-to-end CLI tests for --lang + the lang subcommand."""

from __future__ import annotations

import pytest

from triage.cli import main


@pytest.fixture(autouse=True)
def _clean_env(tmp_path, monkeypatch):
    monkeypatch.setenv("TRIAGE_HOME", str(tmp_path))
    for var in ("TRIAGE_LANG", "LC_ALL", "LC_MESSAGES", "LANG", "TRIAGE_NO_LOG"):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setenv("TRIAGE_NO_LOG", "1")  # quiet logger for tests
    yield


def test_lang_subcommand_lists_codes(capsys):
    assert main(["lang"]) == 0
    out = capsys.readouterr().out
    assert "en" in out
    assert "es" in out
    assert "fr" in out
    assert "English" in out
    assert "Español" in out
    assert "Français" in out


def test_lang_json_emits_structured_languages(capsys):
    import json
    assert main(["lang", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["default"] == "en"
    codes = {entry["code"] for entry in payload["languages"]}
    assert {"en", "es", "fr", "de", "ca"} <= codes
    native = {entry["code"]: entry["native_name"] for entry in payload["languages"]}
    assert native["en"] == "English"
    assert native["es"] == "Español"
    assert native["ca"] == "Català"


def test_lang_check_json_clean_returns_zero_and_empty_dict(capsys):
    import json
    assert main(["lang", "--check", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload == {}


def test_lang_check_json_drift_returns_one_and_drift_report(capsys, monkeypatch):
    import json
    from triage.locales import LOCALES

    fake = {"__native_name__": "Test", "(no tasks)": "(none)"}
    monkeypatch.setitem(LOCALES, "zz", fake)
    try:
        assert main(["lang", "--check", "--json"]) == 1
        payload = json.loads(capsys.readouterr().out)
        assert "zz" in payload
        assert payload["zz"]["missing"], "expected missing keys to be reported"
    finally:
        LOCALES.pop("zz", None)


def test_no_tasks_in_english(capsys):
    assert main(["list"]) == 0
    out = capsys.readouterr().out
    assert "(no tasks)" in out


def test_no_tasks_in_spanish_via_flag(capsys):
    assert main(["--lang", "es", "list"]) == 0
    out = capsys.readouterr().out
    assert "(sin tareas)" in out


def test_no_tasks_in_french_via_env(capsys, monkeypatch):
    monkeypatch.setenv("TRIAGE_LANG", "fr")
    assert main(["list"]) == 0
    out = capsys.readouterr().out
    assert "(aucune tâche)" in out


def test_tick_output_spanish(capsys):
    main(["add", "x"])
    capsys.readouterr()
    assert main(["--lang", "es", "tick"]) == 0
    out = capsys.readouterr().out
    # Spanish translation contains 'señal' (Spanish for signal/cron)
    assert "señal" in out


def test_tick_output_french(capsys):
    main(["add", "x"])
    capsys.readouterr()
    assert main(["--lang", "fr", "tick"]) == 0
    out = capsys.readouterr().out
    assert "signal" in out.lower()  # FR uses "signal(aux)"


def test_unknown_lang_flag_falls_back_to_english(capsys):
    assert main(["--lang", "klingon", "list"]) == 0
    out = capsys.readouterr().out
    assert "(no tasks)" in out  # default-English


def test_LANG_env_picked_up(capsys, monkeypatch):
    monkeypatch.setenv("LANG", "fr_FR.UTF-8")
    assert main(["list"]) == 0
    out = capsys.readouterr().out
    assert "(aucune tâche)" in out


def test_TRIAGE_LANG_beats_LANG(capsys, monkeypatch):
    monkeypatch.setenv("LANG", "fr_FR.UTF-8")
    monkeypatch.setenv("TRIAGE_LANG", "es")
    assert main(["list"]) == 0
    out = capsys.readouterr().out
    assert "(sin tareas)" in out


def test_status_section_titles_spanish(capsys):
    main(["add", "x"])
    capsys.readouterr()
    assert main(["--lang", "es", "status"]) == 0
    out = capsys.readouterr().out
    assert "ETIQUETAS" in out or "TOP 3" in out  # at least one translated heading


def test_no_task_with_id_translated(capsys):
    rc = main(["--lang", "es", "show", "deadbeef0000"])
    assert rc == 1
    err = capsys.readouterr().err
    assert "ninguna tarea" in err
