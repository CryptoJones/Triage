# Triage i18n recipes

Copy-pasteable shell snippets for Triage's localization features.
The full architectural story is in [`DESIGN.md`](../DESIGN.md#internationalization-i18n);
this file is the cookbook.

Triage ships with 17 Latin-script locales: `en` (baseline), `es`,
`fr`, `de`, `it`, `pt`, `nl`, `pl`, `cs`, `sv`, `no`, `da`, `fi`,
`ro`, `hu`, `tr`, `ca`. Unknown languages silently fall back to
English.

---

## 1. Force a specific language for a single command

Use the `--lang` flag when you want one-shot output in a particular
language — useful when sharing screenshots, recording demos, or
debugging a translation:

```bash
triage --lang fr list
triage --lang de status
triage --lang es why <task-id>
```

The flag applies only to that invocation; the next call goes back
to the resolved system default.

---

## 2. Set a per-shell language preference

Set `TRIAGE_LANG` in your shell's startup file:

```bash
# ~/.bashrc / ~/.zshrc
export TRIAGE_LANG=de
```

```fish
# ~/.config/fish/config.fish
set -gx TRIAGE_LANG de
```

Now every Triage invocation in this shell speaks German. The
`--lang` flag still overrides per-call when you need it.

`TRIAGE_LANG` wins over `$LANG`/`$LC_ALL`/`$LC_MESSAGES`, so this
won't fight your other locale settings.

---

## 3. Let Triage detect the system locale automatically

This is the default. Without `--lang` and without `$TRIAGE_LANG`,
Triage resolves the language in this order:

```
$LC_ALL  →  $LC_MESSAGES  →  $LANG  →  locale.getlocale()  →  en
```

So on a typical Linux box with `LANG=es_ES.UTF-8` you get Spanish
automatically. On Windows (where those env vars are usually unset)
Triage falls back to `locale.getlocale()`, which reflects the OS
display language.

Verify what got picked:

```bash
triage lang
# *  en  English
#    cs  Čeština
#    da  Dansk
#    ...
#    es  Español (active)   ← marker on the resolved locale
```

---

## 4. Wire `triage lang --check` into release CI

`triage lang --check` audits every non-English locale against
`en.STRINGS` and reports drift: missing keys, extra keys, and
placeholder-name mismatches. Exit code is 1 on any drift, 0 if
clean — drop it into a CI workflow next to your test step.

Sample green run:

```bash
$ triage lang --check
OK: all 16 non-English locales match the English baseline.
$ echo $?
0
```

Sample drift report (one missing key):

```bash
$ triage lang --check
locale 'es':
  missing keys (1):
    - '(no tasks)'
$ echo $?
1
```

The live wiring lives in
[`.github/workflows/test.yml`](../.github/workflows/test.yml) and
[`.woodpecker.yml`](../.woodpecker.yml) — each runs `triage lang
--check` as its own CI step so locale drift shows up with its own
red mark rather than burying inside test output.

---

## 5. Debug a partial translation

When drafting a new locale or polishing an existing one, set
`TRIAGE_I18N_DEBUG=1` to surface missing-key warnings on stderr:

```bash
TRIAGE_I18N_DEBUG=1 triage --lang xx list
# triage-i18n: no translation for 'TOP 3' in 'xx'
# triage-i18n: no translation for 'TAGS ({n})' in 'xx'
# ...
```

Each missing key fires once per process so the noise doesn't drown
out useful output. Pair this with `triage lang --check` to find
everything that still needs translating before opening a PR.

---

## 6. First step when something's wrong: `triage doctor`

When a locale doesn't behave the way you expect — wrong language
appearing, fallback to English when you set `TRIAGE_LANG`, etc. —
run `triage doctor` first:

```bash
$ triage doctor
triage v0.11.0    (python 3.14.4)
  locale:  fr   source=TRIAGE_LANG   available=17   drift=0
  store:   /home/you/.triage   exists=True
  log:     /var/log/triage.log
```

The `source` line tells you which signal Triage picked up. Common
diagnoses:

- `source=default` despite a set `$LANG`? Your `$LANG` may be a
  locale code Triage doesn't ship (e.g. `ja_JP`). Run
  `triage lang` to see the supported list.
- `source=LANG` when you wanted `$TRIAGE_LANG` to win? Make sure
  the env var is exported, not just set in the parent shell.
- `drift > 0`? A fork or vendored copy got out of sync.
  `triage lang --check` will list the exact drift.

Paste the whole output into bug reports. Or use `--json` if a
tool needs to parse it.

---

## What's NOT translated

Triage deliberately leaves these in English / ASCII / numeric form
because translating them would either confuse readers or break
parsers:

- **Version strings** — `v0.10.0` is universal.
- **Task IDs** — opaque hex hashes (`9e8040d267d9`).
- **Tag names** — `gh-ci:CryptoJones/Triage@main` is machine-readable.
- **CLI flag names** — `--lang`, `--cron-window`, etc. translating
  them would break scripts.
- **Code blocks in docs** — same reasoning as flag names.

If you find user-facing English text that *should* be translated
but isn't (e.g. a new exception message), `_(\"<text>\", ...)` is
the routing primitive — add the key to
[`src/triage/locales/en.py`](../src/triage/locales/en.py), then
add a translation in each other locale catalog, then `triage lang
--check` to verify.

---

Proudly Made in Nebraska. Go Big Red! 🌽 https://xkcd.com/2347/
