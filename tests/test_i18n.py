# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Localization tests."""

from __future__ import annotations

import re

import pytest

from triage import i18n
from triage.locales import LOCALES, en


@pytest.fixture(autouse=True)
def _reset(monkeypatch):
    i18n.reset_for_test()
    for var in ("TRIAGE_LANG", "LC_ALL", "LC_MESSAGES", "LANG", "TRIAGE_I18N_DEBUG"):
        monkeypatch.delenv(var, raising=False)
    yield
    i18n.reset_for_test()


# ---------- resolve_lang ----------

def test_resolve_arg_wins_over_env(monkeypatch):
    monkeypatch.setenv("TRIAGE_LANG", "fr")
    assert i18n.resolve_lang("es") == "es"


def test_resolve_env_used_when_no_arg(monkeypatch):
    monkeypatch.setenv("TRIAGE_LANG", "fr")
    assert i18n.resolve_lang(None) == "fr"


def test_resolve_lang_strips_locale_suffix(monkeypatch):
    monkeypatch.setenv("LANG", "es_ES.UTF-8")
    assert i18n.resolve_lang(None) == "es"


def test_resolve_lang_strips_at_modifier(monkeypatch):
    monkeypatch.setenv("LANG", "es@valencia")
    assert i18n.resolve_lang(None) == "es"


def test_resolve_lang_ignores_C_locale(monkeypatch):
    monkeypatch.setenv("LANG", "C")
    assert i18n.resolve_lang(None) == "en"


def test_resolve_lang_unknown_falls_through_to_default(monkeypatch):
    monkeypatch.setenv("TRIAGE_LANG", "xx")
    assert i18n.resolve_lang(None) == "en"


def test_resolve_arg_unknown_ignored(monkeypatch):
    assert i18n.resolve_lang("nope") == "en"


def test_resolve_lc_all_priority_over_lang(monkeypatch):
    monkeypatch.setenv("LANG", "es")
    monkeypatch.setenv("LC_ALL", "fr_FR")
    assert i18n.resolve_lang(None) == "fr"


# ---------- _() lookup ----------

def test_lookup_english_returns_baseline():
    i18n.configure("en")
    assert i18n._("(no tasks)") == "(no tasks)"


def test_lookup_spanish():
    i18n.configure("es")
    assert i18n._("(no tasks)") == "(sin tareas)"


def test_lookup_french():
    i18n.configure("fr")
    assert i18n._("(no tasks)") == "(aucune tâche)"


def test_missing_key_returns_msgid():
    i18n.configure("es")
    assert i18n._("definitely not a real key 12345") == "definitely not a real key 12345"


def test_format_args_applied():
    i18n.configure("en")
    assert i18n._("removed {id}", id="abc") == "removed abc"


def test_format_args_applied_in_translation():
    i18n.configure("es")
    assert i18n._("removed {id}", id="abc") == "eliminado abc"


def test_bad_placeholder_in_translation_falls_back_to_english():
    # Force a placeholder mismatch by injecting a broken catalog
    i18n.configure("en")
    i18n._strings = {"hello {name}": "hola {nombre}"}  # wrong placeholder name
    result = i18n._("hello {name}", name="aaron")
    assert result == "hello aaron"


# ---------- catalog completeness ----------

def test_every_locale_has_native_name():
    for code, catalog in LOCALES.items():
        assert "__native_name__" in catalog, f"{code} missing __native_name__"
        assert catalog["__native_name__"], f"{code} native name is empty"


def test_every_locale_has_every_english_key():
    en_keys = set(en.STRINGS.keys())
    for code, catalog in LOCALES.items():
        if code == "en":
            continue
        missing = en_keys - set(catalog.keys())
        assert not missing, (
            f"locale {code!r} is missing keys: {sorted(missing)}"
        )


_PLACEHOLDER_RE = re.compile(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}")


def _placeholders(s: str) -> set[str]:
    return set(_PLACEHOLDER_RE.findall(s))


def test_every_locale_has_matching_placeholders():
    """{name} placeholders in English must appear identically in every translation."""
    for code, catalog in LOCALES.items():
        if code == "en":
            continue
        for key, en_text in en.STRINGS.items():
            en_ph = _placeholders(en_text)
            tr_text = catalog.get(key, "")
            tr_ph = _placeholders(tr_text)
            assert en_ph == tr_ph, (
                f"locale {code!r} key {key!r}: placeholder mismatch "
                f"(en: {sorted(en_ph)} vs {code}: {sorted(tr_ph)})"
            )


# ---------- list_available ----------

def test_list_available_returns_pairs():
    pairs = i18n.list_available()
    codes = [c for c, _native in pairs]
    assert "en" in codes
    assert "es" in codes
    assert "fr" in codes


def test_list_available_native_names():
    pairs = dict(i18n.list_available())
    assert pairs["en"] == "English"
    assert pairs["es"] == "Español"
    assert pairs["fr"] == "Français"


# ---------- end-to-end ----------

def test_current_lang_lazy_initializes(monkeypatch):
    monkeypatch.setenv("TRIAGE_LANG", "fr")
    i18n.reset_for_test()
    assert i18n.current_lang() == "fr"


def test_configure_returns_resolved():
    assert i18n.configure("es") == "es"
    assert i18n.configure("xx") == "en"


# ---------- check_locales ----------

def test_check_locales_clean_on_shipping_catalogs():
    """Real shipped catalogs should pass the audit clean — the tests already
    cover missing keys and placeholder mismatches, so check_locales() must
    agree with that."""
    assert i18n.check_locales() == {}


def test_check_locales_detects_missing_key(monkeypatch):
    """Inject a broken catalog and confirm check_locales surfaces it."""
    fake = {"__native_name__": "Test", "(no tasks)": "(none)"}  # missing nearly everything
    monkeypatch.setitem(LOCALES, "zz", fake)
    try:
        report = i18n.check_locales()
        assert "zz" in report
        assert report["zz"]["missing"], "expected missing keys to be reported"
        assert "(no tasks)" not in report["zz"]["missing"], (
            "key that IS present should not be in missing"
        )
    finally:
        LOCALES.pop("zz", None)


def test_check_locales_detects_placeholder_mismatch(monkeypatch):
    """A locale that uses {tasks_total} where en uses {tasks} must fail."""
    fake = dict(en.STRINGS)
    fake["__native_name__"] = "Test"
    fake["total tasks: {tasks}    ranked: {ranked}"] = (
        "total tareas: {tareas}    clasificadas: {clasificadas}"
    )
    monkeypatch.setitem(LOCALES, "zz", fake)
    try:
        report = i18n.check_locales()
        assert "zz" in report
        mismatches = report["zz"]["placeholder_mismatches"]
        keys_with_issues = [k for k, _en_ph, _tr_ph in mismatches]
        assert "total tasks: {tasks}    ranked: {ranked}" in keys_with_issues
    finally:
        LOCALES.pop("zz", None)


def test_check_locales_detects_extra_key(monkeypatch):
    fake = dict(en.STRINGS)
    fake["__native_name__"] = "Test"
    fake["fictional-extra-key"] = "shouldn't be here"
    monkeypatch.setitem(LOCALES, "zz", fake)
    try:
        report = i18n.check_locales()
        assert "zz" in report
        assert "fictional-extra-key" in report["zz"]["extra"]
    finally:
        LOCALES.pop("zz", None)
