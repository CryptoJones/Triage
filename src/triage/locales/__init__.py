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
from . import cs   # Czech
from . import da   # Danish
from . import de   # German
from . import es   # Spanish
from . import fi   # Finnish
from . import fr   # French
from . import hu   # Hungarian
from . import it   # Italian
from . import nl   # Dutch
from . import no   # Norwegian
from . import pl   # Polish
from . import pt   # Portuguese
from . import ro   # Romanian
from . import sv   # Swedish
from . import tr   # Turkish

LOCALES: dict[str, dict[str, str]] = {
    "cs": cs.STRINGS,
    "da": da.STRINGS,
    "de": de.STRINGS,
    "en": en.STRINGS,
    "es": es.STRINGS,
    "fi": fi.STRINGS,
    "fr": fr.STRINGS,
    "hu": hu.STRINGS,
    "it": it.STRINGS,
    "nl": nl.STRINGS,
    "no": no.STRINGS,
    "pl": pl.STRINGS,
    "pt": pt.STRINGS,
    "ro": ro.STRINGS,
    "sv": sv.STRINGS,
    "tr": tr.STRINGS,
}
