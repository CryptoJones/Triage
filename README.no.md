<div align="center">

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                    T  R  I  A  G  E                          ║
║                                                              ║
║      meta-planlegger som overvåker sin egen kø               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**En selvbevisst prioritetskø.** Signaler leverer fakta om verden;
regler omformer fakta til prioritetsdeltaer; køen ombestiller seg
selv ved hvert tick. Du setter målene — Triage avgjør rekkefølgen
og forteller deg nøyaktig hvorfor.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg?logo=apache)](LICENSE)
[![Stdlib only](https://img.shields.io/badge/deps-stdlib_only-success?logo=python&logoColor=white)](pyproject.toml)
[![Codeberg](https://img.shields.io/badge/Codeberg-CryptoJones%2FTriage-2185D0?logo=codeberg&logoColor=white)](https://codeberg.org/CryptoJones/Triage)
[![GitHub](https://img.shields.io/badge/GitHub-CryptoJones%2FTriage-181717?logo=github&logoColor=white)](https://github.com/CryptoJones/Triage)

**Les dette på:**
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
**Norsk** ·
[Dansk](README.da.md) ·
[Suomi](README.fi.md)

</div>

> Speilet på både [GitHub](https://github.com/CryptoJones/Triage) og
> [Codeberg](https://codeberg.org/CryptoJones/Triage). Issues på begge
> smier er velkomne; commits lander på begge.

---

## Hva du ser

```
╔════════════════════════════════════════════════════════╗
║                  T R I A G E   v0.9.0                  ║
╚════════════════════════════════════════════════════════╝
  ID               PRI  BAR    EMNE
  ════════════  ══════  ═════  ════════════════════════════════════════
  7cfa440bc639  [ 101]  █████  Fiks linteren           ← blokkerer auto-løftet
  f35d7cea6b7d  [ 100]  █████  Legg til funksjon X     ← blokkert av linter
  19c80b807ddd  [  35]  █▒░░░  Roter sertifikat        ← deadlinepress
  abc123456789  [   2]  ░░░░░  Rutineopprydding
```

I en ekte terminal er banneret klart magenta, prioritetene er
fargebåndede (høy = gul, midt = grønn, lav = dempet cyan), og
prioritetsbjelkene fylles proporsjonalt. Standardtemaet `bbs` er
ubeskjemt 90-tall.

---

## Hvordan det fungerer

```
                   ┌─────────────────────┐
   signaler ─────► │    Signalkilder     │  (cron-window, github-ci, ...)
                   └──────────┬──────────┘
                              ▼
                   ┌─────────────────────┐
                   │  ~/.triage/state/   │  (append-only JSONL per kilde)
                   └──────────┬──────────┘
                              ▼
   tick     ─────► ┌─────────────────────┐ ─────► ombestilt kø
                   │ Triage-planlegger   │        + revisjonslogg per oppgave
                   └──────────┬──────────┘
                              ▼
                   ┌─────────────────────┐
   oppgaver ─────► │      triage CLI     │
                   └─────────────────────┘
```

1. **Signalkilder** leverer fakta (`cron-window`, `github-ci`,
   fremtidige `runpod-cost`, `github-pr`...).
2. **Regler** gjør fakta om til prioritetsdeltaer
   (`base_score`, `deadline_decay`, `cron_window_active`,
   `ci_failing`, `blocker_transitive`).
3. **Køen ombestilles** ved hvert `triage tick`.
4. **Hver ombestilling er forklarlig** — `triage why <id>` viser
   nøyaktig hvilke regler som bidro med hvilke deltaer, så
   rekkefølgen er aldri en svart boks.

Se [`DESIGN.md`](DESIGN.md) for full arkitektur, regelkatalog og
veikart.

---

## Installasjon

```bash
git clone https://github.com/CryptoJones/Triage      # eller codeberg.org/CryptoJones/Triage
cd Triage
pip install -e .
```

Rent Python-standardbibliotek. Ingen runtime-avhengigheter. Testet
på 3.10 / 3.11 / 3.12.

---

## Bruk

### Oppgaver

```bash
triage add "Fiks autentiseringsfeilen" --base-score 10
triage add "Roter staging-sertifikatet" --deadline 2026-05-20T00:00:00Z
triage add "Hverdagsoppgave"     --cron-window "* 9-17 * * 1-5"
triage add "Overvåk CI"          --tag "gh-ci:CryptoJones/Triage@main"
triage add "Vent på linter"      --blocked-by <linter-task-id>

triage list                     # gjeldende prioritetsrekkefølge
triage show <id>                # rå oppgavepost (JSON)
triage why  <id>                # hvilke regler bidro med hvilke deltaer
triage rm   <id>                # fjern
```

### Ombestilling + polling

```bash
triage tick                     # rekalkuler prioriteter; skriv ut ny rekkefølge
triage poll github-ci           # kall en nettverksbundet signalkilde
```

`tick` er billig, lokal og idempotent — kall den fra cron, en
shell-loop eller Claude Codes `ScheduleWakeup`. `poll` er for
signalkilder som rører ved nettverket (det betaler du eksplisitt for).

### Språk

Triage snakker flere språk. Sett språket med flagget `--lang` eller
de vanlige miljøvariablene:

```bash
triage --lang no list           # engangs
TRIAGE_LANG=no triage list      # per skall
triage lang                     # list tilgjengelige språk
```

Støttede språk: English, Español, Français, Deutsch, Italiano,
Português, Nederlands, Polski, Čeština, Svenska, Norsk, Dansk, Suomi.
Hvis språket ikke gjenkjennes, brukes engelsk som reserve.

### Hendelseslogg (for eksterne agenter)

Hvert CLI-anrop legger til én JSON-linje i en loggfil slik at en
ekstern agent kan kjøre `tail -f` og parse Triages oppførsel:

```bash
tail -f /var/log/triage.log | jq .   # hvis filen eies av brukeren din
```

Eksempeloppføringer:

```json
{"ts":"2026-05-16T06:16:18+00:00","event":"add","task_id":"9e8040d267d9","subject":"Undersøk treg spørring","base_score":10,"tags":[],"deadline":null,"blocked_by":[]}
{"ts":"2026-05-16T06:16:18+00:00","event":"tick","ranked_count":2,"emitted_cron_signals":0,"top":[{"id":"ad2006db3c12","priority":35,"subject":"Roter sertifikat"}],"warnings":[]}
{"ts":"2026-05-16T06:16:19+00:00","event":"poll","source":"github-ci","emitted":1,"warnings":[]}
{"ts":"2026-05-16T06:16:20+00:00","event":"rm","task_id":"9e8040d267d9"}
```

Konfigurasjon:

| Mekanisme                  | Hva den gjør                                                     |
|----------------------------|------------------------------------------------------------------|
| flagget `--log-file PATH`  | Loggsti per kjøring.                                             |
| env `TRIAGE_LOG_FILE=PATH` | Loggsti per skall.                                               |
| Standard                   | `/var/log/triage.log`. Faller tilbake til `~/.triage/triage.log` hvis `/var/log` ikke er skrivbar (advarer én gang på stderr). |
| flagget `--no-log`         | Deaktiver logging for denne kjøringen.                           |
| env `TRIAGE_NO_LOG=1`      | Deaktiver logging globalt for skallet.                           |

For å bruke standardstien `/var/log` uten sudo ved hvert anrop:

```bash
sudo touch /var/log/triage.log
sudo chown $(id -un):$(id -gn) /var/log/triage.log
```

Logging er en streng enveis-sidekanal — feil under skriving svelges
slik at CLI:ens primære oppførsel aldri forstyrres.

### Temaer

```bash
triage theme                    # list tilgjengelige temaer
triage theme --name bbs         # gjengi eksempelrader
triage --theme modern list      # engangs temaoverstyring
TRIAGE_THEME=mono triage list   # tema per skall
```

| Tema     | Estetikk                                                            |
|----------|---------------------------------------------------------------------|
| `bbs`    | **Standard.** 90-talls-BBS: klar magenta, dobbelt-linje-ramme (`╔═╗`), blokkbjelker. |
| `modern` | Subtil palett, enkelt-linje-rammer (`┌─┐`), prikkbjelker (`█▒·`).  |
| `mono`   | Ingen farge, kun ASCII (`+-+`, `#=.`) — trygt for piper / dumme terminaler. |

Farge følger standardene:

- Auto-deaktivert når stdout ikke er en TTY.
- `NO_COLOR=1` deaktiverer farge (jf. [no-color.org](https://no-color.org/)).
- `FORCE_COLOR=1` aktiverer farge på ikke-TTY.
- Flagget `--no-color` = eksplisitt nødbryter per kjøring.

---

## Relaterte prosjekter

Triage er én bit av et lite økosystem. Bitene komponerer:

| Forrådsmapper | Rolle |
|---------------|-------|
| [**claude_skill-Triage**](https://github.com/CryptoJones/claude_skill-Triage) | Claude Codes skill-forrådsmappe. Leverer i dag `TaskPriorityReorder` (**manuell overstyring** — "løft X til toppen") og vil huse skill:en `triage` (**signaldrevet anbefaler** — "hva bør jeg gjøre videre?") i en fremtidig versjon. |
| [**TriageMCP**](https://github.com/CryptoJones/TriageMCP) | **MCP-server** som omslutter Triages API for AI-agenter. Åtte verktøy (`list_tasks`, `add_task`, `tick`, `why_task`, `status`, `remove_task`, `inject_signal`, `get_task`) over stdio. Slipp den inn i `~/.claude/mcp.json`, og en agent kan lese og skrive prioritetskøen din direkte. |
| [**RunPodBoss**](https://github.com/CryptoJones/RunPodBoss) | Kredittsaldo-vakt for RunPod. Integrerer med Triage via `extra_notify_command` — når en faktureringsterskel utløses, dytter RunPodBoss et manuelt signal inn i Triage slik at oppgaven "tøm ledige pods" flyter til toppen av køen din. Oppsettsoppskrift i [`docs/runpodboss-integration.md`](docs/runpodboss-integration.md). |

Alle fire deler Triages primitiv (stabil identitet + reberegnelig
prioritet) og lever på doble speil (GitHub + Codeberg).

---

## Status

| Versjon | Funksjon                                                          | Status     |
|---------|-------------------------------------------------------------------|------------|
| v0.1    | grunnverk, tre regler, cron-window-signal, CLI                    | sluppet    |
| v0.2    | `blocker_transitive`-propagering + syklusdeteksjon                | sluppet    |
| v0.3    | `github-ci`-signalkilde + `ci_failing`-regel + `triage poll`      | sluppet    |
| v0.4    | ANSI-temasystem i BBS-stil + underkommando `triage theme`         | sluppet    |
| v0.5    | `runpod-cost`-signalkilde + `cost_pressure`-regel                 | sluppet    |
| v0.6    | JSONL-hendelsesloggskriver for eksterne agenter                   | sluppet    |
| v0.7    | `github-pr`-signalkilde for utdaterte PR-er                       | planlagt   |
| v0.8    | Claude Codes `triage`-skill (i `claude_skill-Triage`-repo)        | planlagt   |
| v0.9    | `triage watch`-langkjørende modus + systemd-enhet                 | planlagt   |

---

## Lisens

Apache 2.0. Se [LICENSE](LICENSE).

Stolt produsert i Nebraska. Go Big Red! 🌽 https://xkcd.com/2347/
