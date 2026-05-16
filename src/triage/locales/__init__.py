# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Locale catalogs.

To add a new language:
  1. Copy ``en.py`` to ``<iso639-1-code>.py``.
  2. Translate every value in STRINGS. Set ``__native_name__`` to the
     language's name in its own script (e.g. "Español", "Français").
  3. Add an import line + LOCALES entry below.
  4. Run ``pytest`` — the suite catches missing keys + mismatched
     placeholders.

Languages ship one at a time in successive loop iterations. The
roadmap is on the README's "Status" table.
"""

from . import en   # English (baseline)
from . import es   # Spanish
from . import fr   # French

LOCALES: dict[str, dict[str, str]] = {
    "en": en.STRINGS,
    "es": es.STRINGS,
    "fr": fr.STRINGS,
}
