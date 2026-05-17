<div align="center">

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                    T  R  I  A  G  E                          ║
║                                                              ║
║      meta-planlægger der overvåger sin egen kø               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**En selvbevidst prioritetskø.** Signaler leverer fakta om verden;
regler omformer fakta til prioritetsdeltaer; køen omordner sig selv
ved hvert tick. Du sætter målene — Triage afgør rækkefølgen og
fortæller dig præcis hvorfor.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg?logo=apache)](LICENSE)
[![Stdlib only](https://img.shields.io/badge/deps-stdlib_only-success?logo=python&logoColor=white)](pyproject.toml)
[![Codeberg](https://img.shields.io/badge/Codeberg-CryptoJones%2FTriage-2185D0?logo=codeberg&logoColor=white)](https://codeberg.org/CryptoJones/Triage)
[![GitHub](https://img.shields.io/badge/GitHub-CryptoJones%2FTriage-181717?logo=github&logoColor=white)](https://github.com/CryptoJones/Triage)

**Læs dette på:**
[English](README.md) ·
[Español](README.es.md) ·
[Français](README.fr.md) ·
[Deutsch](README.de.md) ·
[Italiano](README.it.md) ·
[Português](README.pt.md) ·
[Nederlands](README.nl.md) ·
[Polski](README.pl.md) ·
[Čeština](README.cs.md) ·
[Svenska](README.sv.md) ·
[Norsk](README.no.md) ·
**Dansk** ·
[Suomi](README.fi.md) ·
[Română](README.ro.md) ·
[Magyar](README.hu.md) ·
[Türkçe](README.tr.md)

</div>

> Spejlet på både [GitHub](https://github.com/CryptoJones/Triage) og
> [Codeberg](https://codeberg.org/CryptoJones/Triage). Issues på begge
> smedjer er velkomne; commits lander på begge.

---

## Hvad du ser

```
╔════════════════════════════════════════════════════════╗
║                  T R I A G E   v0.9.0                  ║
╚════════════════════════════════════════════════════════╝
  ID               PRI  BAR    EMNE
  ════════════  ══════  ═════  ════════════════════════════════════════
  7cfa440bc639  [ 101]  █████  Reparér linteren        ← blokerer auto-løftet
  f35d7cea6b7d  [ 100]  █████  Tilføj funktion X       ← blokeret af linter
  19c80b807ddd  [  35]  █▒░░░  Rotér certifikat        ← deadlinepres
  abc123456789  [   2]  ░░░░░  Rutineoprydning
```

I en rigtig terminal er banneret klart magenta, prioriteterne er
farvebåndede (høj = gul, midt = grøn, lav = dæmpet cyan), og
prioritetsbjælkerne fyldes proportionalt. Standardtemaet `bbs` er
uden undskyldning 90'er.

---

## Sådan virker det

```
                   ┌─────────────────────┐
   signaler ─────► │    Signalkilder     │  (cron-window, github-ci, ...)
                   └──────────┬──────────┘
                              ▼
                   ┌─────────────────────┐
                   │  ~/.triage/state/   │  (append-only JSONL pr. kilde)
                   └──────────┬──────────┘
                              ▼
   tick     ─────► ┌─────────────────────┐ ─────► omordnet kø
                   │  Triage-planlægger  │        + revisionslog pr. opgave
                   └──────────┬──────────┘
                              ▼
                   ┌─────────────────────┐
   opgaver  ─────► │      triage CLI     │
                   └─────────────────────┘
```

1. **Signalkilder** leverer fakta (`cron-window`, `github-ci`,
   fremtidige `runpod-cost`, `github-pr`...).
2. **Regler** omformer fakta til prioritetsdeltaer
   (`base_score`, `deadline_decay`, `cron_window_active`,
   `ci_failing`, `blocker_transitive`).
3. **Køen omordnes** ved hvert `triage tick`.
4. **Hver omordning er forklarlig** — `triage why <id>` viser præcis
   hvilke regler der bidrog med hvilke deltaer, så rækkefølgen er
   aldrig en sort boks.

Se [`DESIGN.md`](DESIGN.md) for fuld arkitektur, regelkatalog og
roadmap.

---

## Installation

```bash
git clone https://github.com/CryptoJones/Triage      # eller codeberg.org/CryptoJones/Triage
cd Triage
pip install -e .
```

Rent Python-standardbibliotek. Ingen runtime-afhængigheder. Testet
på 3.10 / 3.11 / 3.12.

---

## Brug

### Opgaver

```bash
triage add "Reparér autentificeringsfejl" --base-score 10
triage add "Rotér staging-certifikatet" --deadline 2026-05-20T00:00:00Z
triage add "Hverdagsopgave"      --cron-window "* 9-17 * * 1-5"
triage add "Overvåg CI"          --tag "gh-ci:CryptoJones/Triage@main"
triage add "Vent på linter"      --blocked-by <linter-task-id>

triage list                     # nuværende prioritetsrækkefølge
triage show <id>                # rå opgavepost (JSON)
triage why  <id>                # hvilke regler bidrog med hvilke deltaer
triage rm   <id>                # fjern
```

### Omordning + polling

```bash
triage tick                     # genberegn prioriteter; udskriv ny rækkefølge
triage poll github-ci           # kald en netværksbunden signalkilde
```

`tick` er billig, lokal og idempotent — kald den fra cron, et
shell-loop eller Claude Codes `ScheduleWakeup`. `poll` er til
signalkilder, der rammer netværket (det betaler du eksplicit for).

### Sprog

Triage taler flere sprog. Indstil sproget med flaget `--lang` eller
de sædvanlige miljøvariabler:

```bash
triage --lang da list           # engangs
TRIAGE_LANG=da triage list      # pr. skal
triage lang                     # list tilgængelige sprog
```

Understøttede sprog: English, Español, Français, Deutsch, Italiano,
Português, Nederlands, Polski, Čeština, Svenska, Norsk, Dansk, Suomi.
Hvis sproget ikke genkendes, bruges engelsk som reserve.

### Hændelseslog (til eksterne agenter)

Hvert CLI-kald tilføjer én JSON-linje til en logfil, så en ekstern
agent kan køre `tail -f` og parse Triages adfærd:

```bash
tail -f /var/log/triage.log | jq .   # hvis filen ejes af din bruger
```

Eksempelposter:

```json
{"ts":"2026-05-16T06:16:18+00:00","event":"add","task_id":"9e8040d267d9","subject":"Undersøg langsom forespørgsel","base_score":10,"tags":[],"deadline":null,"blocked_by":[]}
{"ts":"2026-05-16T06:16:18+00:00","event":"tick","ranked_count":2,"emitted_cron_signals":0,"top":[{"id":"ad2006db3c12","priority":35,"subject":"Rotér certifikat"}],"warnings":[]}
{"ts":"2026-05-16T06:16:19+00:00","event":"poll","source":"github-ci","emitted":1,"warnings":[]}
{"ts":"2026-05-16T06:16:20+00:00","event":"rm","task_id":"9e8040d267d9"}
```

Konfiguration:

| Mekanisme                  | Hvad den gør                                                     |
|----------------------------|------------------------------------------------------------------|
| flaget `--log-file PATH`   | Logsti pr. kald.                                                 |
| env `TRIAGE_LOG_FILE=PATH` | Logsti pr. skal.                                                 |
| Standard                   | `/var/log/triage.log`. Falder tilbage til `~/.triage/triage.log`, hvis `/var/log` ikke er skrivbar (advarer én gang på stderr). |
| flaget `--no-log`          | Deaktivér logning for dette kald.                                |
| env `TRIAGE_NO_LOG=1`      | Deaktivér logning globalt for skallet.                           |

For at bruge standardstien `/var/log` uden sudo ved hvert kald:

```bash
sudo touch /var/log/triage.log
sudo chown $(id -un):$(id -gn) /var/log/triage.log
```

Logning er en streng envejs-sidekanal — fejl under skrivning sluges,
så CLI:ens primære adfærd aldrig forstyrres.

### Temaer

```bash
triage theme                    # list tilgængelige temaer
triage theme --name bbs         # gengiv eksempelrækker
triage --theme modern list      # engangs tematilsidesættelse
TRIAGE_THEME=mono triage list   # tema pr. skal
```

| Tema     | Æstetik                                                            |
|----------|--------------------------------------------------------------------|
| `bbs`    | **Standard.** 90'er-BBS: klar magenta, dobbeltlinje-ramme (`╔═╗`), blokbjælker. |
| `modern` | Subtil palet, enkeltlinje-rammer (`┌─┐`), prikbjælker (`█▒·`).    |
| `mono`   | Ingen farve, kun ASCII (`+-+`, `#=.`) — sikker for piper / dumme terminaler. |

Farve følger standarderne:

- Auto-deaktiveret når stdout ikke er en TTY.
- `NO_COLOR=1` deaktiverer farve (jf. [no-color.org](https://no-color.org/)).
- `FORCE_COLOR=1` aktiverer farve på ikke-TTY.
- Flaget `--no-color` = eksplicit nødbryter pr. kald.

---

## Relaterede projekter

Triage er ét stykke af et lille økosystem. Stykkerne komponerer:

| Repository | Rolle |
|------------|-------|
| [**claude_skill-Triage**](https://github.com/CryptoJones/claude_skill-Triage) | Claude Codes skill-repository. Leverer i dag `TaskPriorityReorder` (**manuel tilsidesættelse** — "løft X til toppen") og vil huse skill:en `triage` (**signalstyret anbefaler** — "hvad bør jeg gøre nu?") i en fremtidig udgivelse. |
| [**TriageMCP**](https://github.com/CryptoJones/TriageMCP) | **MCP-server** der ombryder Triages API for AI-agenter. Otte værktøjer (`list_tasks`, `add_task`, `tick`, `why_task`, `status`, `remove_task`, `inject_signal`, `get_task`) over stdio. Slip den ind i `~/.claude/mcp.json`, og en agent kan læse og skrive din prioritetskø direkte. |
| [**RunPodBoss**](https://github.com/CryptoJones/RunPodBoss) | Kreditbalance-værn for RunPod. Integrerer med Triage via `extra_notify_command` — når en faktureringstærskel udløses, skubber RunPodBoss et manuelt signal ind i Triage, så opgaven "tøm inaktive pods" flyder til toppen af din kø. Opsætningsopskrift i [`docs/runpodboss-integration.md`](docs/runpodboss-integration.md). |

Alle fire deler Triages primitiv (stabil identitet + genberegnelig
prioritet) og lever på dobbelte spejle (GitHub + Codeberg).

---

## Status

| Version | Funktion                                                          | Status     |
|---------|-------------------------------------------------------------------|------------|
| v0.1    | grundstillads, tre regler, cron-window-signal, CLI                | udgivet    |
| v0.2    | `blocker_transitive`-propagering + cyklusdetektion                | udgivet    |
| v0.3    | `github-ci`-signalkilde + `ci_failing`-regel + `triage poll`      | udgivet    |
| v0.4    | ANSI-temasystem i BBS-stil + underkommando `triage theme`         | udgivet    |
| v0.5    | `runpod-cost`-signalkilde + `cost_pressure`-regel                 | udgivet    |
| v0.6    | JSONL-hændelseslogskriver til eksterne agenter                    | udgivet    |
| v0.7    | `github-pr`-signalkilde for forældede PR'er                       | planlagt   |
| v0.8    | Claude Codes `triage`-skill (i `claude_skill-Triage`-repo)        | planlagt   |
| v0.9    | `triage watch`-langkørende tilstand + systemd-enhed               | planlagt   |

---

## Licens

Apache 2.0. Se [LICENSE](LICENSE).

Stolt fremstillet i Nebraska. Go Big Red! 🌽 https://xkcd.com/2347/
