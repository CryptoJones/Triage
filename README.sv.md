<div align="center">

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                    T  R  I  A  G  E                          ║
║                                                              ║
║      metaschemaläggare som bevakar sin egen kö               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**En självmedveten prioritetskö.** Signaler levererar fakta om världen;
regler omvandlar fakta till prioritetsdeltan; kön ordnar om sig själv
vid varje tick. Du sätter målen — Triage avgör ordningen och berättar
exakt varför.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg?logo=apache)](LICENSE)
[![Stdlib only](https://img.shields.io/badge/deps-stdlib_only-success?logo=python&logoColor=white)](pyproject.toml)
[![Codeberg](https://img.shields.io/badge/Codeberg-CryptoJones%2FTriage-2185D0?logo=codeberg&logoColor=white)](https://codeberg.org/CryptoJones/Triage)
[![GitHub](https://img.shields.io/badge/GitHub-CryptoJones%2FTriage-181717?logo=github&logoColor=white)](https://github.com/CryptoJones/Triage)

**Läs detta på:**
[English](README.md) ·
[Español](README.es.md) ·
[Français](README.fr.md) ·
[Deutsch](README.de.md) ·
[Italiano](README.it.md) ·
[Português](README.pt.md) ·
[Nederlands](README.nl.md) ·
[Polski](README.pl.md) ·
[Čeština](README.cs.md) ·
**Svenska** ·
[Norsk](README.no.md) ·
[Dansk](README.da.md) ·
[Suomi](README.fi.md) ·
[Română](README.ro.md) ·
[Magyar](README.hu.md) ·
[Türkçe](README.tr.md) ·
[Català](README.ca.md)

</div>

> Speglat både på [GitHub](https://github.com/CryptoJones/Triage) och
> [Codeberg](https://codeberg.org/CryptoJones/Triage). Issues på endera
> smedjan välkomnas; commits landar på båda.

---

## Vad du ser

```
╔════════════════════════════════════════════════════════╗
║                  T R I A G E   v0.10.0                  ║
╚════════════════════════════════════════════════════════╝
  ID               PRI  BAR    ÄMNE
  ════════════  ══════  ═════  ════════════════════════════════════════
  7cfa440bc639  [ 101]  █████  Fixa lintern           ← blockerare auto-höjd
  f35d7cea6b7d  [ 100]  █████  Lägg till funktion X   ← blockerad av lintern
  19c80b807ddd  [  35]  █▒░░░  Rotera certifikat      ← deadline-tryck
  abc123456789  [   2]  ░░░░░  Rutinstädning
```

I en riktig terminal är bannern klart magentafärgad, prioriteterna är
färgbandade (hög = gul, mitt = grön, låg = dämpad cyan), och
prioritetstaplarna fylls i proportionellt. Standardtemat `bbs` är
oblygt 90-tal.

---

## Hur det fungerar

```
                   ┌─────────────────────┐
   signaler ─────► │    Signalkällor     │  (cron-window, github-ci, ...)
                   └──────────┬──────────┘
                              ▼
                   ┌─────────────────────┐
                   │  ~/.triage/state/   │  (append-only JSONL per källa)
                   └──────────┬──────────┘
                              ▼
   tick     ─────► ┌─────────────────────┐ ─────► omordnad kö
                   │ Triage-schemaläggare│        + granskningslogg per uppgift
                   └──────────┬──────────┘
                              ▼
                   ┌─────────────────────┐
   uppgift  ─────► │      triage CLI     │
                   └─────────────────────┘
```

1. **Signalkällor** levererar fakta (`cron-window`, `github-ci`,
   framtida `runpod-cost`, `github-pr`...).
2. **Regler** omvandlar fakta till prioritetsdeltan
   (`base_score`, `deadline_decay`, `cron_window_active`,
   `ci_failing`, `blocker_transitive`).
3. **Kön ordnas om** vid varje `triage tick`.
4. **Varje omordning är förklarlig** — `triage why <id>` visar exakt
   vilka regler som bidrog med vilka deltan, så ordningen är aldrig
   en svart låda.

Se [`DESIGN.md`](DESIGN.md) för fullständig arkitektur, regelkatalog
och roadmap.

---

## Installation

```bash
git clone https://github.com/CryptoJones/Triage      # eller codeberg.org/CryptoJones/Triage
cd Triage
pip install -e .
```

Ren Python-standardbibliotek. Inga runtime-beroenden. Testat på
3.10 / 3.11 / 3.12.

---

## Användning

### Uppgifter

```bash
triage add "Fixa autentiseringsbuggen" --base-score 10
triage add "Rotera staging-certifikatet" --deadline 2026-05-20T00:00:00Z
triage add "Vardags-syssla"      --cron-window "* 9-17 * * 1-5"
triage add "Bevaka CI"           --tag "gh-ci:CryptoJones/Triage@main"
triage add "Vänta på linter"     --blocked-by <linter-task-id>

triage list                     # nuvarande prioritetsordning
triage show <id>                # rå uppgiftspost (JSON)
triage why  <id>                # vilka regler bidrog med vilka deltan
triage rm   <id>                # ta bort
```

### Omordning + pollning

```bash
triage tick                     # räkna om prioriteter; skriv ut ny ordning
triage poll github-ci           # kalla en nätverksbunden signalkälla
```

`tick` är billig, lokal och idempotent — anropa den från cron, en
shell-loop eller Claude Codes `ScheduleWakeup`. `poll` är för
signalkällor som tar emot nätverkstrafik (det betalar du explicit för).

### Språk

Triage talar flera språk. Sätt språket med flaggan `--lang` eller
vanliga miljövariabler:

```bash
triage --lang sv list           # engångs
TRIAGE_LANG=sv triage list      # per skal
triage lang                     # lista tillgängliga språk
```

Språk som stöds: English, Español, Français, Deutsch, Italiano,
Português, Nederlands, Polski, Čeština, Svenska, Norsk, Dansk, Suomi.
Om språket inte känns igen används engelska som reserv.

### Händelselogg (för externa agenter)

Varje CLI-anrop lägger till en enda JSON-rad i en loggfil så att en
extern agent kan göra `tail -f` och parsa Triages beteende:

```bash
tail -f /var/log/triage.log | jq .   # om filen ägs av din användare
```

Exempelposter:

```json
{"ts":"2026-05-16T06:16:18+00:00","event":"add","task_id":"9e8040d267d9","subject":"Undersök långsam fråga","base_score":10,"tags":[],"deadline":null,"blocked_by":[]}
{"ts":"2026-05-16T06:16:18+00:00","event":"tick","ranked_count":2,"emitted_cron_signals":0,"top":[{"id":"ad2006db3c12","priority":35,"subject":"Rotera certifikat"}],"warnings":[]}
{"ts":"2026-05-16T06:16:19+00:00","event":"poll","source":"github-ci","emitted":1,"warnings":[]}
{"ts":"2026-05-16T06:16:20+00:00","event":"rm","task_id":"9e8040d267d9"}
```

Konfiguration:

| Mekanism                   | Vad den gör                                                      |
|----------------------------|------------------------------------------------------------------|
| flaggan `--log-file PATH`  | Loggsökväg per anrop.                                            |
| env `TRIAGE_LOG_FILE=PATH` | Loggsökväg per skal.                                             |
| Standard                   | `/var/log/triage.log`. Faller tillbaka till `~/.triage/triage.log` om `/var/log` inte är skrivbar (varnar en gång på stderr). |
| flaggan `--no-log`         | Inaktivera loggning för detta anrop.                             |
| env `TRIAGE_NO_LOG=1`      | Inaktivera loggning globalt för skalet.                          |

För att använda standardsökvägen `/var/log` utan sudo vid varje anrop:

```bash
sudo touch /var/log/triage.log
sudo chown $(id -un):$(id -gn) /var/log/triage.log
```

Loggning är en strikt envägs-sidokanal — fel under skrivning sväljs
så att CLI:s primära beteende aldrig störs.

### Teman

```bash
triage theme                    # lista tillgängliga teman
triage theme --name bbs         # rendera exempelrader
triage --theme modern list      # tematilsidesättning per anrop
TRIAGE_THEME=mono triage list   # tema per skal
```

| Tema     | Estetik                                                              |
|----------|----------------------------------------------------------------------|
| `bbs`    | **Standard.** 90-tals-BBS: klar magenta, dubbellinjig ram (`╔═╗`), blockstaplar. |
| `modern` | Subtil palett, enkellinjiga ramar (`┌─┐`), prickstaplar (`█▒·`).    |
| `mono`   | Ingen färg, enbart ASCII (`+-+`, `#=.`) — säker för pipes / dumma terminaler. |

Färg följer standarder:

- Inaktiveras automatiskt när stdout inte är en TTY.
- `NO_COLOR=1` inaktiverar färg (enligt [no-color.org](https://no-color.org/)).
- `FORCE_COLOR=1` aktiverar färg på icke-TTY.
- Flaggan `--no-color` = explicit avstängningsknapp per anrop.

---

## Relaterade projekt

Triage är en bit av ett litet ekosystem. Bitarna komponerar:

| Förråd | Roll |
|--------|------|
| [**claude_skill-Triage**](https://github.com/CryptoJones/claude_skill-Triage) | Claude Codes skill-förråd. Levererar idag `TaskPriorityReorder` (**manuell tilsidesättning** — "höj X till toppen") och kommer att hysa skill:en `triage` (**signalstyrd rekommenderare** — "vad ska jag göra härnäst?") i en framtida release. |
| [**TriageMCP**](https://github.com/CryptoJones/TriageMCP) | **MCP-server** som omsluter Triages API för AI-agenter. Åtta verktyg (`list_tasks`, `add_task`, `tick`, `why_task`, `status`, `remove_task`, `inject_signal`, `get_task`) via stdio. Lägg in den i `~/.claude/mcp.json` och en agent kan läsa och skriva din prioritetskö direkt. |
| [**RunPodBoss**](https://github.com/CryptoJones/RunPodBoss) | Kreditbalans-skydd för RunPod. Integrerar med Triage via `extra_notify_command` — när ett faktureringströskel passeras skickar RunPodBoss en manuell signal till Triage så att uppgiften "töm inaktiva pods" flyter upp till toppen av din kö. Konfigurationsrecept i [`docs/runpodboss-integration.md`](docs/runpodboss-integration.md). |

Alla fyra delar Triages primitiv (stabil identitet + omräkningsbar
prioritet) och lever på dubbla speglar (GitHub + Codeberg).

---

## Status

| Version | Funktion                                                            | Status     |
|---------|---------------------------------------------------------------------|------------|
| v0.1    | grundskelett, tre regler, cron-window-signal, CLI                   | släppt     |
| v0.2    | `blocker_transitive`-propagering + cykeldetektering                 | släppt     |
| v0.3    | `github-ci`-signalkälla + `ci_failing`-regel + `triage poll`        | släppt     |
| v0.4    | ANSI-temasystem i BBS-stil + underkommando `triage theme`           | släppt     |
| v0.5    | `runpod-cost`-signalkälla + `cost_pressure`-regel                   | släppt     |
| v0.6    | JSONL-händelseloggskrivare för externa agenter                      | släppt     |
| v0.7    | `github-pr`-signalkälla + regel `rule_stale_pr`                     | släppt     |
| v0.8    | `triage signal`-CLI + regel `manual_bump` + RunPodBoss-integration  | släppt     |
| v0.8.1  | `triage status` översikt på en skärm                                | släppt     |
| v0.9    | i18n-grund — `--lang`-flagga + en/es/fr-lokaler                     | släppt     |
| v0.10   | i18n komplett — 17 lokaler + regressionsdetektor `triage lang --check` | släppt     |
| —       | Claude Codes `triage`-skill (i `claude_skill-Triage`-repo)          | planerad   |
| —       | `triage watch`-långkörande läge + systemd-enhet                     | planerad   |

---

## Licens

Apache 2.0. Se [LICENSE](LICENSE).

Stolt tillverkad i Nebraska. Go Big Red! 🌽 https://xkcd.com/2347/
