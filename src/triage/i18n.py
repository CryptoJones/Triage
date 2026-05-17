# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Localization for Triage CLI output.

Why a hand-rolled dict-based catalog instead of gettext:
- No msgfmt / .mo compilation step. Each locale ships as a Python
  module with a STRINGS dict that contributors can edit directly.
- The string lookup falls back to English on any miss, so a partial
  translation never breaks the CLI.
- pure-stdlib (no `babel`, no `pybabel`); matches the project's
  stdlib-only invariant.

Resolution precedence (highest -> lowest):
  1. ``triage --lang LANG ...`` CLI flag.
  2. ``TRIAGE_LANG`` environment variable.
  3. ``LC_ALL`` / ``LC_MESSAGES`` / ``LANG`` system locale (first hit;
     stripped to the 2-letter ISO 639-1 code).
  4. ``en`` (English baseline).

Strings are looked up by an English source-language key — _("OK")
returns the locale's translation of "OK" if present, or "OK" if not.
This is the gettext convention; it means the English baseline IS
the catalog of keys, and other languages translate from there.

A missed key in a non-English locale is recorded once-per-process
on stderr (only when TRIAGE_I18N_DEBUG=1) so contributors can see
what still needs translating in their language.
"""

from __future__ import annotations

import os
import sys
from typing import Any

from .locales import LOCALES

DEFAULT_LANG = "en"

_resolved_lang: str | None = None
_strings: dict[str, str] | None = None
_misses_logged: set[str] = set()


def _strip_locale(s: str) -> str:
    """Convert 'es_ES.UTF-8' / 'fr@latin' / 'pt_BR' -> 'es', 'fr', 'pt'."""
    if not s:
        return ""
    s = s.split(".", 1)[0]
    s = s.split("@", 1)[0]
    s = s.split("_", 1)[0]
    return s.strip().lower()


def resolve_lang(arg: str | None = None) -> str:
    """Pick the active locale from arg / env / system."""
    if arg:
        code = _strip_locale(arg)
        if code in LOCALES:
            return code
    env_lang = os.environ.get("TRIAGE_LANG")
    if env_lang:
        code = _strip_locale(env_lang)
        if code in LOCALES:
            return code
    for var in ("LC_ALL", "LC_MESSAGES", "LANG"):
        v = os.environ.get(var)
        if v and v != "C" and v != "POSIX":
            code = _strip_locale(v)
            if code in LOCALES:
                return code
    # Windows + any POSIX setup that doesn't export $LANG: try the
    # process locale registered with the C library. Wrapped because
    # locale.getlocale() can raise on misconfigured systems.
    try:
        import locale as _locale
        sys_locale = _locale.getlocale()[0]
        if sys_locale:
            code = _strip_locale(sys_locale)
            if code in LOCALES:
                return code
    except Exception:
        pass
    return DEFAULT_LANG


def configure(lang: str | None = None) -> str:
    """Resolve the active locale + load its catalog. Returns the lang code."""
    global _resolved_lang, _strings, _misses_logged
    _resolved_lang = resolve_lang(lang)
    _strings = LOCALES.get(_resolved_lang, {})
    _misses_logged = set()
    return _resolved_lang


def current_lang() -> str:
    """Return the active locale, configuring with defaults if not yet set."""
    if _resolved_lang is None:
        configure()
    return _resolved_lang or DEFAULT_LANG


def _(msgid: str, /, **fmt: Any) -> str:
    """Translate `msgid` into the active locale + apply str.format kwargs.

    If the active locale has no entry for `msgid`, the English source
    string is returned unchanged. Translations may use named
    placeholders that the caller passes as kwargs (e.g. _("rank {n}",
    n=5) -> "rank 5" / "rango 5" / ...).
    """
    if _resolved_lang is None:
        configure()

    translated = (_strings or {}).get(msgid)
    if translated is None:
        if _resolved_lang and _resolved_lang != DEFAULT_LANG and os.environ.get("TRIAGE_I18N_DEBUG") == "1":
            if msgid not in _misses_logged:
                _misses_logged.add(msgid)
                print(
                    f"triage-i18n: no translation for {msgid!r} in {_resolved_lang!r}",
                    file=sys.stderr,
                )
        translated = msgid

    if fmt:
        try:
            return translated.format(**fmt)
        except (KeyError, IndexError, ValueError):
            # Bad placeholder in the translation — fall back to the
            # English source applied with the same fmt args. Better
            # to show English than to raise.
            try:
                return msgid.format(**fmt)
            except Exception:
                return msgid
    return translated


def list_available() -> list[tuple[str, str]]:
    """Return [(code, native_name), ...] for every shipped locale."""
    out = []
    for code, catalog in LOCALES.items():
        native = catalog.get("__native_name__", code)
        out.append((code, native))
    out.sort(key=lambda kv: kv[0])
    return out


_PLACEHOLDER_RE = __import__("re").compile(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}")


def _placeholders(s: str) -> set[str]:
    return set(_PLACEHOLDER_RE.findall(s))


def check_locales() -> dict[str, dict[str, list]]:
    """Compare every non-English locale against the English baseline.

    Returns a dict ``{lang_code: {missing: [...], extra: [...], placeholder_mismatches: [...]}}``
    for every locale that has at least one issue. Empty dict = clean.

    - ``missing``    keys in en.STRINGS not present in <lang>.STRINGS
    - ``extra``      keys in <lang>.STRINGS not present in en.STRINGS
                     (excludes ``__native_name__`` which is locale-only)
    - ``placeholder_mismatches`` list of ``(key, en_placeholders, lang_placeholders)``
      tuples where the ``{name}`` placeholder set diverges from English.
    """
    from .locales import en as _en  # local import keeps top of file clean

    en_keys = set(_en.STRINGS.keys())
    report: dict[str, dict[str, list]] = {}

    for code, catalog in LOCALES.items():
        if code == DEFAULT_LANG:
            continue
        lang_keys = set(catalog.keys())
        missing = sorted(en_keys - lang_keys)
        extra = sorted(lang_keys - en_keys - {"__native_name__"})

        placeholder_mismatches: list[tuple[str, list[str], list[str]]] = []
        for key, en_text in _en.STRINGS.items():
            if key not in catalog:
                continue
            en_ph = _placeholders(en_text)
            tr_ph = _placeholders(catalog[key])
            if en_ph != tr_ph:
                placeholder_mismatches.append(
                    (key, sorted(en_ph), sorted(tr_ph))
                )

        if missing or extra or placeholder_mismatches:
            report[code] = {
                "missing": missing,
                "extra": extra,
                "placeholder_mismatches": placeholder_mismatches,
            }

    return report


def reset_for_test() -> None:
    """Reset module-level state. Used by tests."""
    global _resolved_lang, _strings, _misses_logged
    _resolved_lang = None
    _strings = None
    _misses_logged = set()
