# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Claude Code `triage` skill in `claude_skill-Triage/triage/`
  (wraps `triage tick` + `triage list --json` + `triage why <id>`,
  surfaces top-N tasks with rule contributions; operator confirms
  before any reorder).
- `triage watch` long-running mode + `examples/triage.service`
  systemd unit.

---

## [0.11.1] — 2026-05-17

Patch release. Adds the `triage doctor` env-diagnostics subcommand
that started life as a "small bug-report helper" and turned out to
be genuinely useful enough to flush into a tagged version.

### Added
- **`triage doctor`** — one-screen, read-only environment-diagnostics
  subcommand. Reports version, Python version, resolved locale +
  the signal that won locale resolution (TRIAGE_LANG / LC_ALL /
  LC_MESSAGES / LANG / locale.getlocale() / default), store path,
  log path, and locale-catalog drift count. Plain text or `--json`.
  Designed for paste-into-bug-reports use.

### Docs
- Surfaced `triage doctor` in `README.md` (new `### Diagnostics`
  block under Usage) and `examples/i18n-recipes.md` (new recipe #6
  showing how to use `source` field for locale debugging).
- README banner ticked v0.11.0 → v0.11.1; English README only.
  Translated READMEs intentionally lag — v0.11.x is invisible-to-
  reader CLI polish, not new user-facing surface.

---

## [0.11.0] — 2026-05-16

The post-i18n polish release. Locks down everything that grew out
of v0.10 once the 17 locales actually landed and contributors
started using them.

### Added
- **`locale.getlocale()` fallback** in `i18n.resolve_lang`. Windows
  + bare POSIX shells (no `$LANG`) now get system-locale-driven
  auto-detection instead of always falling back to English.
- **`triage lang --json`** output mode. Without `--check`, emits the
  available-languages list as a JSON object; with `--check`, emits
  the drift report from `check_locales()` directly. CI tools can
  now `jq` the result instead of regex-parsing the human text.
- **`triage lang --check` runs as a CI gate** on both forges
  (`.github/workflows/test.yml` + `.woodpecker.yml`) — locale drift
  surfaces with its own red mark separately from pytest.
- **Version stamp in `triage status` banner.** A one-screen status
  snapshot now reports which version produced it.

### Changed
- **Model-layer error messages now route through `_()`.** Seven
  previously hardcoded strings (cron.py × 1, scheduler.py × 3,
  log_writer.py × 3) localize across all 17 catalogs.
- README banner-width padding repaired across all 17 translations
  after the v0.10 sed bump knocked the right `║` one column off.
- All 17 README "Supported languages" in-prose lists now enumerate
  the full Latin-script set (some were stuck at their iteration
  batch's last entry).
- Status tables across all 17 READMEs refreshed for v0.10/v0.11
  reality.

### Docs
- `DESIGN.md` gained a top-level "Internationalization (i18n)"
  section: catalog story, `_()` lookup, resolution precedence,
  "add a locale" recipe, the release gate, and the smart-quote
  gotcha.
- `docs/i18n-data-format-comparison.md` — decision doc comparing
  Python-module vs JSON vs YAML for locale data. Recommendation:
  stay on Python until external translators start contributing.
- `examples/i18n-recipes.md` — five copy-pasteable patterns
  (forced lang, per-shell preference, system-locale auto, CI gate,
  `TRIAGE_I18N_DEBUG`) plus the "what's NOT translated" list.
- `examples/*.sh` audited end-to-end against the v0.10/v0.11 CLI:
  no functional drift; minimum-version headers added to each.
- `CHANGELOG.md` (this file) consolidated — i18n journey table
  under v0.10, footer release-link backfill.

---

## [0.10.0] — 2026-05-16

### Added
- **i18n complete.** Triage now ships with 17 Latin-script locale
  catalogs: `en` (baseline), `es`, `fr`, `de`, `it`, `pt`, `nl`, `pl`,
  `cs`, `sv`, `no`, `da`, `fi`, `ro`, `hu`, `tr`, `ca`. Every locale
  passes the catalog-completeness and placeholder-matching tests.
- **`triage lang --check`** subcommand. Audits every locale against
  the English baseline and reports missing keys, extra keys, and
  placeholder mismatches. Exits non-zero if any drift is found —
  suitable for release-gate use in CI alongside `pytest`.
- **17 README translations.** Every locale has a `README.<code>.md`
  full translation; the "Read this in:" switcher is consistent across
  all 17 docs.

### Changed
- Status tables in every README refreshed to reflect what has
  actually shipped through v0.10 (previously stale — claimed v0.7
  was planned despite shipping at `f4d6686`).
- ASCII-art banner bumped to `v0.10.0` in every README; banner-box
  width re-tightened to match the 56-column rule above/below
  (post-bump polish that L8 closed).

### Notes — i18n journey

i18n shipped iteratively across nine loop iterations before being
locked in as a milestone. For readers digging through git history:

| Iteration | Scope                                                         | Landed at |
|-----------|---------------------------------------------------------------|-----------|
| L1        | Foundation: `_()` lookup, `--lang` flag, en/es/fr catalogs    | `a77eed1` |
| L2        | de/it/pt + first wave of README translations                  | `f1e4c52` |
| L3        | nl/pl/cs (Germanic + Slavic batch)                            | `7f34137` |
| L4        | sv/no/da/fi (Nordic batch)                                    | `6d948ac` |
| L5        | ro/hu/tr (Eastern-European batch)                             | `80ce829` |
| L6        | ca — last Romance                                             | `0e93420` |
| L7        | `lang --check` + v0.10.0 bump + Status-table refresh          | `168268e` |
| L8        | Banner-width polish + 17-lang in-prose support-list audit     | `ff12490` |

Catalogs live in `src/triage/locales/<code>.py`. The release gate
is `triage lang --check`, which mirrors the `tests/test_i18n.py`
catalog-completeness and placeholder-matching assertions in a form
that's runnable outside the test harness.

---

## [0.9.0] — 2026-05-16

### Added
- **i18n foundation.** Hand-rolled dict-based locale catalogs
  (`src/triage/locales/<code>.py`), `_()` lookup with English
  fallback, `--lang` CLI flag and `$TRIAGE_LANG` env var.
- Locales shipped iteratively across loop iterations L1-L6 (en, es,
  fr, de, it, pt, nl, pl, cs, sv, no, da, fi, ro, hu, tr, ca).
- `triage lang` subcommand listing available languages with native
  names + active marker.
- Catalog-completeness and placeholder-matching tests gate every
  locale on import.

---

## [0.8.1] — 2026-05-16

### Added
- `triage status` one-screen at-a-glance summary: top-3 tasks, tag
  counts, signal counts.

---

## [0.8.0] — 2026-05-16

### Added
- `triage signal manual` CLI verb for injecting one-off signals from
  external watchers (RunPodBoss, calendar daemons, anything). Flags:
  `--source NAME`, `--affects ID` (repeatable), `--bump N`, `--ttl SECS`,
  `--note STR`, `--state STR`. Emitted signal lives in
  `~/.triage/state/<source>.jsonl`.
- `rule_manual_bump` rule that sums `bump` integers from any non-
  first-class signal source. Multiple bumps stack within their TTL
  window. Added to `DEFAULT_RULES` (now 7 rules).
- `docs/runpodboss-integration.md` — evaluation answering "can
  RunPodBoss connect to Triage?" The recommended integration is a
  config-only change in RunPodBoss using its existing
  `extra_notify_command` hook; no RunPodBoss code required.

### Changed
- `rule_manual_bump` explicitly excludes signals from `cron`,
  `github-ci`, `github-pr`, `runpod-cost` (those have dedicated
  rules) so it never double-counts.

[0.8.0]: https://github.com/CryptoJones/Triage/releases/tag/v0.8.0

---

## [0.7.0] — 2026-05-16

### Added
- `src/triage/sources/github_pr.py` — third network-bound signal
  source. Tasks tagged `gh-pr:owner/repo` (all open PRs) or
  `gh-pr:owner/repo#N` (specific PR). Polls GitHub Pulls API.
- `rule_stale_pr` rule: +20 when a `github-pr` signal targeting the
  task has `state == "stale"` (updated_at > 24h old). Added to
  `DEFAULT_RULES`.
- States classified per PR: `fresh` (< 24h), `stale` (≥ 24h),
  `missing` (specific-PR 404), `unknown` (unparseable response).
- 27 new tests in `tests/test_github_pr.py`.

[0.7.0]: https://github.com/CryptoJones/Triage/releases/tag/v0.7.0

---

## [0.6.0] — 2026-05-16

### Added
- `src/triage/log_writer.py` — JSONL event log writer for external
  agents. Strictly one-way side channel: Triage writes, agents read.
- Global `--log-file PATH` and `--no-log` CLI flags; `TRIAGE_LOG_FILE`
  and `TRIAGE_NO_LOG` environment variables.
- Events logged: `add`, `list`, `tick`, `poll`, `rm`, `signal`. Each
  entry is one append-flushed JSON line so a tailing agent never
  sees a partial record.

### Defaults
- Log path defaults to `/var/log/triage.log`; falls back to
  `~/.triage/triage.log` with a one-time stderr breadcrumb if the
  system path isn't writable. Explicit `--log-file` / `TRIAGE_LOG_FILE`
  values that aren't writable warn + disable rather than silently
  re-routing.

### Safety
- Logging never breaks the CLI. All write errors are swallowed.
- `ts` and `event` fields are reserved — user kwargs cannot overwrite.

### Tests
- 24 new tests across `tests/test_log_writer.py` and
  `tests/test_cli_logging.py` (158 total passing).

[0.6.0]: https://github.com/CryptoJones/Triage/releases/tag/v0.6.0

---

## [0.5.0] — 2026-05-16

### Added
- `src/triage/sources/runpod.py` — second network-bound signal
  source. Tasks tagged `runpod:<pod-id>`. Polls RunPod GraphQL API
  for the current state of every referenced pod.
- `rule_cost_pressure` rule (two-tier scoring):
  - **+100** when state == `idle` (RUNNING + uptime > 10 min + avg
    GPU util < 10% — drain it now).
  - **+25** when state == `running` (paying but util unknown or
    above the idle threshold — softer reminder).
- Per-pod grouping: when multiple tasks share a `runpod:<pod-id>`
  tag, one signal is emitted with `affects = [list of task ids]`.

[0.5.0]: https://github.com/CryptoJones/Triage/releases/tag/v0.5.0

---

## [0.4.0] — 2026-05-16

### Added
- `src/triage/theme.py` — BBS-style ANSI theme system. Three themes
  ship:
  - **`bbs`** (default) — 1990s BBS: bright magenta double-line
    banners (`╔═╗║╚╝`), color-banded priorities, block-character
    priority bars (`█▒░`).
  - **`modern`** — subtle palette, single-line boxes (`┌─┐`),
    dot-fill bars (`█▒·`).
  - **`mono`** — no color, ASCII-only (`+-+`, `#=.`).
- Global `--theme NAME` flag and `TRIAGE_THEME` environment variable.
- `--no-color` flag and `NO_COLOR=1` environment variable
  (per [no-color.org](https://no-color.org/)).
- `FORCE_COLOR=1` to enable color on non-TTY surfaces.
- New `triage theme` subcommand: lists themes or `--name <theme>`
  renders sample rows for visual selection.

### Changed
- `list`, `tick`, `why`, `poll`, `rm`, `show` all themed by default.
- Banner appears on `triage list` and `triage tick` output.

[0.4.0]: https://github.com/CryptoJones/Triage/releases/tag/v0.4.0

---

## [0.3.0] — 2026-05-15

### Added
- `src/triage/sources/github_ci.py` — first network-bound signal
  source. Tasks tagged `gh-ci:owner/repo@branch` (branch names with
  slashes supported). Polls GitHub Actions API for the most recent
  workflow run.
- `rule_ci_failing` rule: +50 when a `github-ci` signal targeting the
  task reports `state == "failure"`.
- `triage poll <source>` CLI verb for explicit network-bound polls.
  Cron remains auto-emitted on `triage tick`; `github-ci` is opt-in.
- Auth via optional `GITHUB_TOKEN` environment variable.

### Tests
- 24 new tests; `_fetch_runs` is monkeypatched in every test (no
  real network calls).

[0.3.0]: https://github.com/CryptoJones/Triage/releases/tag/v0.3.0

---

## [0.2.0] — 2026-05-15

### Added
- `blocker_transitive` propagation: enforces the invariant
  `priority(blocker) ≥ priority(blocked) + 1` across the entire
  task graph. Implemented as a post-scoring reverse-topo pass in the
  scheduler.
- DFS-based cycle detection: cycles in the `blocked_by` graph are
  broken via back-edge removal (deterministic by lex-sorted source-id
  traversal). Each removed edge is recorded as a warning.
- Self-loop and dangling-blocker-id detection (warns + ignores).

### Fixed
- v0.1 `DESIGN.md` had the propagation semantic backward — it
  described raising the *blocked* task above its blocker, when the
  correct semantic is the opposite (the *blocker* must outrank what
  it blocks). Doc rewritten; behavior was always correct (it just
  hadn't been implemented yet).

### Tests
- 12 new tests in `tests/test_blocker_transitive.py`.

[0.2.0]: https://github.com/CryptoJones/Triage/releases/tag/v0.2.0

---

## [0.1.0] — 2026-05-15

### Added
- Initial release. Stdlib-only Python package.
- Task model with stable IDs, base_score, deadline, tags, blocked_by,
  cron_window fields.
- Signal model with TTL-based expiry.
- Atomic file-backed `Store` (`~/.triage/`, overridable via
  `TRIAGE_HOME`).
- Three built-in scoring rules: `base_score`, `deadline_decay`,
  `cron_window_active`. Each contribution is named and auditable via
  `triage why <id>`.
- `Scheduler`: `rank(tasks, signals) -> sorted ScoredTask list`.
- First signal source: `cron-window`. Tasks opt in via
  `--cron-window` with a five-field cron expression; the source
  emits per-task signals with `payload.active` reflecting whether
  the window is currently open.
- CLI verbs: `triage add | list | show | why | tick | rm`, with
  `--json` on `list`.
- 39 tests across model, store, rules, scheduler, cron, cli.
- GitHub Actions + Codeberg Woodpecker pipelines.

[0.11.1]: https://github.com/CryptoJones/Triage/releases/tag/v0.11.1
[0.11.0]: https://github.com/CryptoJones/Triage/releases/tag/v0.11.0
[0.10.0]: https://github.com/CryptoJones/Triage/releases/tag/v0.10.0
[0.9.0]: https://github.com/CryptoJones/Triage/releases/tag/v0.9.0
[0.8.1]: https://github.com/CryptoJones/Triage/releases/tag/v0.8.1
[0.1.0]: https://github.com/CryptoJones/Triage/releases/tag/v0.1.0

---

Proudly Made in Nebraska. Go Big Red! 🌽 https://xkcd.com/2347/
