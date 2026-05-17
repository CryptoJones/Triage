# Post-v0.11 roadmap — should there be a v0.12?

**Status:** decision doc, written 2026-05-17 after the v0.11.1
patch ships. Documents whether Triage should plan a v0.12 milestone
or sit at steady-state until a v1.0 push.

**TL;DR:** sit at steady-state. The two remaining "Planned" items
(Claude Code skill, `triage watch`) are deliberately cross-repo and
long-running. Neither benefits from being grouped under a v0.12
milestone right now. Cut v0.12 when one of them is actually nearly
done.

---

## What v0.11.1 leaves in CHANGELOG / Planned

After this release, the only forward-looking items are:

1. **Claude Code `triage` skill** in `claude_skill-Triage/triage/` —
   would surface Triage's top-N tasks as a skill the agent can call,
   with operator confirmation before any reorder.
2. **`triage watch` long-running mode** + `examples/triage.service`
   systemd unit — turns Triage from cron-driven into an always-on
   daemon.

Both are real work; neither is urgent.

## Why not version-grouping them as v0.12 now

- **The skill lives in a sibling repo.** Versioning that against
  Triage proper would force coupled releases — fine for a leaf
  consumer, awkward for a skill that other people might want to
  fork or vendor.
- **`triage watch` is a behavioral mode, not new surface.** It
  doesn't change any existing CLI verb's semantics; it changes
  how `tick`s get triggered. The natural release moment is when
  the `examples/triage.service` systemd unit + the watch loop +
  the daemon-friendly logging all land together. Cutting v0.12
  with just the skill and back-filling watch later splits the
  release notes awkwardly.
- **17 locales + 252 tests + `lang --check` in CI gate** is a
  genuinely stable steady-state. Triage hit "we trust this
  enough to translate it 17 times" levels of confidence. There's
  no quality debt that a quick v0.12 would pay off.

## What would prompt cutting v0.12

Any of these would justify a new minor:

- The Claude Code skill in `claude_skill-Triage` actually ships
  AND gets used in anger for a week without surfacing Triage-side
  changes needed.
- A new signal source lands (e.g. `slack-mentions`, `gcal-event`,
  `linear-issue`) — those tend to come with their own rule and
  warrant the bump.
- `triage watch` ships with its systemd unit + a few weeks of
  uptime under the maintainer's actual queue.
- An external contributor opens a feature-grade PR on either forge
  that materially changes the CLI surface.

## What v1.0 would look like

A separate question, but worth marking now:

- v1.0 implies API stability commitment. Today the `_()` keys in
  `en.STRINGS` are technically a public-ish API (forks override
  them); freezing that surface is the main v1.0 lift.
- v1.0 implies "the model has matured" — likely after at least
  one real user beyond the maintainer has filed a non-trivial
  issue against a tagged release.
- v1.0 probably wants a `pip install triage-scheduler` story
  (PyPI upload), which is currently un-done.

None of those are in the post-v0.11 polish queue. They're the
v1.0 push, separate iteration cycle.

---

Proudly Made in Nebraska. Go Big Red! 🌽 https://xkcd.com/2347/
