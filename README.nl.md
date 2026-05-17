<div align="center">

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                    T  R  I  A  G  E                          ║
║                                                              ║
║         meta-scheduler die zijn eigen wachtrij volgt         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Een zelfbewuste prioriteitswachtrij.** Signalen pushen feiten over de
wereld; regels zetten feiten om in prioriteitsdelta's; de wachtrij
herordent zichzelf bij elke tick. Jij stelt de doelen — Triage bepaalt
de volgorde, en vertelt je precies waarom.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg?logo=apache)](LICENSE)
[![Stdlib only](https://img.shields.io/badge/deps-stdlib_only-success?logo=python&logoColor=white)](pyproject.toml)
[![Codeberg](https://img.shields.io/badge/Codeberg-CryptoJones%2FTriage-2185D0?logo=codeberg&logoColor=white)](https://codeberg.org/CryptoJones/Triage)
[![GitHub](https://img.shields.io/badge/GitHub-CryptoJones%2FTriage-181717?logo=github&logoColor=white)](https://github.com/CryptoJones/Triage)

**Lees dit in:**
[English](README.md) ·
[Español](README.es.md) ·
[Français](README.fr.md) ·
[Deutsch](README.de.md) ·
[Italiano](README.it.md) ·
[Português](README.pt.md) ·
**Nederlands** ·
[Polski](README.pl.md) ·
[Čeština](README.cs.md) ·
[Svenska](README.sv.md) ·
[Norsk](README.no.md) ·
[Dansk](README.da.md) ·
[Suomi](README.fi.md) ·
[Română](README.ro.md) ·
[Magyar](README.hu.md) ·
[Türkçe](README.tr.md) ·
[Català](README.ca.md)

</div>

> Gespiegeld op zowel [GitHub](https://github.com/CryptoJones/Triage) als
> [Codeberg](https://codeberg.org/CryptoJones/Triage). Issues op beide
> forges zijn welkom; commits landen op beide.

---

## Wat je ziet

```
╔════════════════════════════════════════════════════════╗
║                  T R I A G E   v0.10.0                 ║
╚════════════════════════════════════════════════════════╝
  ID               PRI  BAR    ONDERWERP
  ════════════  ══════  ═════  ════════════════════════════════════════
  7cfa440bc639  [ 101]  █████  Linter repareren        ← blokkeerder auto-verhoogd
  f35d7cea6b7d  [ 100]  █████  Functie X toevoegen     ← geblokkeerd door linter
  19c80b807ddd  [  35]  █▒░░░  Certificaat roteren     ← deadlinedruk
  abc123456789  [   2]  ░░░░░  Routineschoonmaak
```

In een echte terminal is de banner helder magenta, zijn de prioriteiten
gekleurd in banden (hoog = geel, midden = groen, laag = gedimd cyaan)
en vullen de prioriteitsbalken zich evenredig. Het standaardthema `bbs`
is onbeschaamd jaren-90.

---

## Hoe het werkt

```
                   ┌─────────────────────┐
   signalen ─────► │   Signaalbronnen    │  (cron-window, github-ci, ...)
                   └──────────┬──────────┘
                              ▼
                   ┌─────────────────────┐
                   │  ~/.triage/state/   │  (alleen-toevoegen JSONL per bron)
                   └──────────┬──────────┘
                              ▼
   tick     ─────► ┌─────────────────────┐ ─────► herordende wachtrij
                   │  Triage-scheduler   │        + auditlogboek per taak
                   └──────────┬──────────┘
                              ▼
                   ┌─────────────────────┐
   taken    ─────► │     triage CLI      │
                   └─────────────────────┘
```

1. **Signaalbronnen** pushen feiten (`cron-window`, `github-ci`,
   toekomstige `runpod-cost`, `github-pr`...).
2. **Regels** zetten feiten om in prioriteitsdelta's
   (`base_score`, `deadline_decay`, `cron_window_active`,
   `ci_failing`, `blocker_transitive`).
3. **De wachtrij herordent** bij elke `triage tick`.
4. **Elke herordening is uitlegbaar** — `triage why <id>` toont
   precies welke regels welke delta's bijdroegen, zodat de volgorde
   nooit een zwarte doos is.

Zie [`DESIGN.md`](DESIGN.md) voor de volledige architectuur, de
regelcatalogus en de roadmap.

---

## Installatie

```bash
git clone https://github.com/CryptoJones/Triage      # of codeberg.org/CryptoJones/Triage
cd Triage
pip install -e .
```

Pure Python stdlib. Geen runtime-afhankelijkheden. Getest op
3.10 / 3.11 / 3.12.

---

## Gebruik

### Taken

```bash
triage add "Auth-bug repareren" --base-score 10
triage add "Staging-certificaat roteren" --deadline 2026-05-20T00:00:00Z
triage add "Doordeweekse klus" --cron-window "* 9-17 * * 1-5"
triage add "CI in de gaten houden"  --tag "gh-ci:CryptoJones/Triage@main"
triage add "Wachten op linter"      --blocked-by <linter-task-id>

triage list                     # huidige prioriteitsvolgorde
triage show <id>                # ruw taakrecord (JSON)
triage why  <id>                # welke regels welke delta's bijdroegen
triage rm   <id>                # verwijderen
```

### Herordenen + pollen

```bash
triage tick                     # prioriteiten herberekenen; nieuwe volgorde afdrukken
triage poll github-ci           # een netwerkgebonden signaalbron aanroepen
```

`tick` is goedkoop, lokaal en idempotent — roep het aan vanuit cron,
een shell-lus of Claude Code's `ScheduleWakeup`. `poll` is voor
signaalbronnen die het netwerk raken (daar betaal je expliciet voor).

### Taal

Triage spreekt meerdere talen. Stel de taal in met de optie `--lang`
of de gebruikelijke omgevingsvariabelen:

```bash
triage --lang nl list           # eenmalig
TRIAGE_LANG=nl triage list      # per shell
triage lang                     # beschikbare talen opsommen
```

Ondersteunde talen: English, Español, Français, Deutsch, Italiano,
Português, Nederlands, Polski, Čeština, Svenska, Norsk, Dansk, Suomi,
Română, Magyar, Türkçe, Català. Als de taal niet wordt herkend, wordt
Engels als terugval gebruikt.

### Gebeurtenislogboek (voor externe agents)

Elke CLI-aanroep voegt één JSON-regel toe aan een logbestand, zodat
een externe agent `tail -f` kan doen en het gedrag van Triage kan
parsen:

```bash
tail -f /var/log/triage.log | jq .   # als het bestand van je gebruiker is
```

Voorbeeldinvoer:

```json
{"ts":"2026-05-16T06:16:18+00:00","event":"add","task_id":"9e8040d267d9","subject":"Trage query onderzoeken","base_score":10,"tags":[],"deadline":null,"blocked_by":[]}
{"ts":"2026-05-16T06:16:18+00:00","event":"tick","ranked_count":2,"emitted_cron_signals":0,"top":[{"id":"ad2006db3c12","priority":35,"subject":"Certificaat roteren"}],"warnings":[]}
{"ts":"2026-05-16T06:16:19+00:00","event":"poll","source":"github-ci","emitted":1,"warnings":[]}
{"ts":"2026-05-16T06:16:20+00:00","event":"rm","task_id":"9e8040d267d9"}
```

Configuratie:

| Mechanisme                 | Wat het doet                                                       |
|----------------------------|--------------------------------------------------------------------|
| optie `--log-file PATH`    | Logpad per aanroep.                                                |
| env `TRIAGE_LOG_FILE=PATH` | Logpad per shell.                                                  |
| Standaard                  | `/var/log/triage.log`. Valt terug op `~/.triage/triage.log` als `/var/log` niet schrijfbaar is (waarschuwt eenmaal op stderr). |
| optie `--no-log`           | Logboek uitschakelen voor deze aanroep.                            |
| env `TRIAGE_NO_LOG=1`      | Logboek globaal uitschakelen voor de shell.                        |

Om het standaardpad `/var/log` te gebruiken zonder bij elke aanroep sudo:

```bash
sudo touch /var/log/triage.log
sudo chown $(id -un):$(id -gn) /var/log/triage.log
```

Het logboek is een strikt eenrichtings-zijkanaal — fouten tijdens
het schrijven worden ingeslikt zodat het primaire gedrag van de CLI
nooit wordt verstoord.

### Thema's

```bash
triage theme                    # beschikbare thema's opsommen
triage theme --name bbs         # voorbeeldrijen weergeven
triage --theme modern list      # eenmalige themaoverschrijving
TRIAGE_THEME=mono triage list   # thema per shell
```

| Thema    | Esthetiek                                                              |
|----------|------------------------------------------------------------------------|
| `bbs`    | **Standaard.** Jaren 90 BBS: helder magenta, dubbel-lijn kader (`╔═╗`), blokbalken. |
| `modern` | Subtiel palet, enkel-lijn kaders (`┌─┐`), puntbalken (`█▒·`).         |
| `mono`   | Geen kleur, alleen ASCII (`+-+`, `#=.`) — veilig voor pipes / domme terminals. |

Kleur volgt de standaarden:

- Automatisch uitgeschakeld wanneer stdout geen TTY is.
- `NO_COLOR=1` schakelt kleur uit (volgens [no-color.org](https://no-color.org/)).
- `FORCE_COLOR=1` schakelt kleur in op niet-TTY.
- De optie `--no-color` = expliciete noodknop per aanroep.

---

## Verwante projecten

Triage is één stukje van een klein ecosysteem. De stukken passen op elkaar:

| Repository | Rol |
|------------|-----|
| [**claude_skill-Triage**](https://github.com/CryptoJones/claude_skill-Triage) | Claude Code-skills-repository. Levert vandaag `TaskPriorityReorder` (**handmatige overschrijving** — "X naar de top schuiven") en zal de skill `triage` (**signaalgedreven aanbeveler** — "wat moet ik nu doen?") huisvesten in een toekomstige versie. |
| [**TriageMCP**](https://github.com/CryptoJones/TriageMCP) | **MCP-server** die Triage's API verpakt voor AI-agents. Acht tools (`list_tasks`, `add_task`, `tick`, `why_task`, `status`, `remove_task`, `inject_signal`, `get_task`) over stdio. Zet hem in `~/.claude/mcp.json` en een agent kan je prioriteitswachtrij rechtstreeks lezen en schrijven. |
| [**RunPodBoss**](https://github.com/CryptoJones/RunPodBoss) | Vangrails voor RunPod-kredietsaldo. Integreert met Triage via `extra_notify_command` — wanneer een factureringsdrempel wordt overschreden, pusht RunPodBoss een handmatig signaal naar Triage zodat de taak "leegloop pods opruimen" naar de top van je wachtrij drijft. Configuratierecept in [`docs/runpodboss-integration.md`](docs/runpodboss-integration.md). |

Alle vier delen de Triage-primitive (stabiele identiteit + herberekenbare
prioriteit) en leven op dubbele mirrors (GitHub + Codeberg).

---

## Status

| Versie | Functionaliteit                                                       | Status      |
|--------|-----------------------------------------------------------------------|-------------|
| v0.1   | scaffold, drie regels, cron-window-signaal, CLI                       | gepubliceerd |
| v0.2   | `blocker_transitive`-propagatie + cyclusdetectie                      | gepubliceerd |
| v0.3   | `github-ci`-signaalbron + `ci_failing`-regel + `triage poll`          | gepubliceerd |
| v0.4   | BBS-stijl ANSI-themasysteem + subcommando `triage theme`              | gepubliceerd |
| v0.5   | `runpod-cost`-signaalbron + `cost_pressure`-regel                     | gepubliceerd |
| v0.6   | JSONL-gebeurtenislogboekschrijver voor externe agents                 | gepubliceerd |
| v0.7   | `github-pr`-signaalbron + regel `rule_stale_pr`                       | gepubliceerd |
| v0.8   | `triage signal`-CLI + regel `manual_bump` + RunPodBoss-integratie     | gepubliceerd |
| v0.8.1 | `triage status` één-scherm-overzicht                                  | gepubliceerd |
| v0.9   | i18n-fundament — `--lang`-optie + en/es/fr locales                    | gepubliceerd |
| v0.10  | i18n compleet — 17 locales + regressiedetector `triage lang --check`  | gepubliceerd |
| —      | Claude Code `triage`-skill (in `claude_skill-Triage`-repo)            | gepland     |
| —      | `triage watch`-langlopende modus + systemd-unit                       | gepland     |

---

## Licentie

Apache 2.0. Zie [LICENSE](LICENSE).

Met trots gemaakt in Nebraska. Go Big Red! 🌽 https://xkcd.com/2347/
