# Locale data format — Python module vs JSON vs YAML

**Status:** decision doc, not an implementation plan. Captured at
L14 of the post-i18n loop (after `lang --check` + DESIGN.md
i18n section landed).

**TL;DR:** stay on Python modules for now. Revisit if/when external
translators (not Aaron) start contributing locales, or if the
smart-quote bug pattern bites again. The migration is non-trivial
and the current pain is bounded.

---

## Background — the smart-quote bug history

Three times during the i18n iteration arc, a translation broke
import because a typographic quote inside a Python `"..."` literal
terminated the string early:

- **L3 (Polish, pl.py).** First write used `„en")` — the `"` is
  U+201D, an ASCII double quote. Inside a `"..."` Python literal
  that's `"text...{closer}` — the string closed at the curly quote,
  the `)` became an unmatched parenthesis, every test errored on
  collection. Caught by pytest's `SyntaxError`, fixed by replacing
  the literal with ASCII `'en'`.
- **L5 / Czech (cs.py).** Similar pattern in `„en\"` — the escape
  worked, but I'd already learned to default to ASCII. Switched the
  one literal back to `'en'`.
- **L10 (model-layer translations).** Avoided proactively in 16
  catalogs by sticking to ASCII apostrophes throughout. None broke
  on import. The DESIGN.md i18n section (L13) explicitly documents
  this gotcha so future translators don't have to learn it the way
  I did.

The bug is real but **fully containable by convention** — `triage
lang --check` doesn't even need to know about it because syntax
errors fail at import time, long before catalog audits.

---

## Tradeoff matrix

|                                | Python module | JSON          | YAML          |
|--------------------------------|---------------|---------------|---------------|
| Editor support                 | ✅ everywhere | ✅ everywhere | ⚠️ less than JSON |
| Parser robustness              | ⚠️ smart-quote trap | ✅ closed-set lexer | ⚠️ tab/anchor pitfalls |
| Build pipeline cost            | ✅ none       | ✅ none (stdlib `json`) | ❌ extra dep (`PyYAML`) |
| IDE syntax check               | ✅ best (full Python LSP) | ✅ great | ✅ good |
| Hot-reload during dev          | ⚠️ stale `_strings` cache | ✅ trivial re-load | ✅ trivial re-load |
| Translator workflow            | ⚠️ contributors need Python literacy | ✅ format-agnostic | ✅ format-agnostic |
| Runtime cost                   | ✅ zero (already imported) | ⚠️ one-time parse + dict allocation | ⚠️ slower parse than JSON |
| Stdlib-only purity             | ✅            | ✅            | ❌            |
| Plays nicely with `.po` round-trip if someone wants `babel` later | ⚠️ awkward | ⚠️ awkward | ⚠️ awkward |
| Diff readability               | ✅ Python syntax familiar | ✅ flat key/value | ✅ block scalars |
| Catalog-completeness test cost | ✅ ~free (Python objects) | ⚠️ load + diff at test time | ⚠️ same |

---

## Recommendation — stay on Python, defer the migration

**Why now isn't the right time:**

1. **The pain is bounded.** Three instances of the smart-quote bug
   in 17 locales is ~18% friction. After L8 documented the ASCII-
   apostrophe convention and L13 wrote it into DESIGN.md, the next
   contributor (Aaron or anyone) has the documentation to dodge it.
2. **YAML loses outright** because it requires an external
   dependency, breaking the project's stdlib-only invariant.
3. **JSON is plausible but expensive to migrate.** Every locale
   file in `src/triage/locales/*.py`, the loader in `__init__.py`,
   the `check_locales()` helper, and the test suite would all need
   updates. The translator-onboarding benefit isn't yet worth the
   migration cost because **all 17 locales were authored in-repo
   by the maintainer.**

**The trigger condition for revisiting:** if the project starts
accepting locale contributions from people who aren't Python
developers — e.g. a native-Hungarian speaker submitting a polish
pass against `hu.py` — JSON probably wins. At that point:

- Editor-on-`triage/locales/hu.json` is much friendlier than asking
  the contributor to learn Python literal syntax + the
  smart-quote gotcha.
- `json.load(path)` is one stdlib call; the loader change is
  ~5 lines.
- The catalog-completeness + placeholder-matching tests port
  trivially (same dict shape, different deserializer).

Until that happens, the status quo is fine.

---

## Out of scope (but worth noting for whoever picks this up)

A migration touches:

- `src/triage/locales/<code>.py` × 17 → `src/triage/locales/<code>.json` × 17.
- `src/triage/locales/__init__.py` — replace per-module imports with
  a directory scan + `json.load` loop populating `LOCALES`.
- `src/triage/i18n.py:check_locales()` — unchanged (works on dicts,
  doesn't care where they came from).
- `tests/test_i18n.py` — unchanged for the same reason.
- `triage lang --check` — unchanged.

The smallest plausible migration PR would be ~17 file renames + ~30
LOC in the loader. The risk is mostly UX (translators rebase work
mid-migration) and tooling (any IDE plugin that highlights
`__native_name__` would need an update).

---

Proudly Made in Nebraska. Go Big Red! 🌽 https://xkcd.com/2347/
