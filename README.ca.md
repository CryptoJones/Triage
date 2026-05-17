<div align="center">

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                    T  R  I  A  G  E                          ║
║                                                              ║
║      meta-planificador que vigila la seva pròpia cua         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Una cua de prioritats conscient de si mateixa.** Els senyals
aporten fets sobre el món; les regles converteixen els fets en deltes
de prioritat; la cua es reordena sola a cada tick. Tu fixes els
objectius — Triage decideix l'ordre i t'explica exactament per què.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg?logo=apache)](LICENSE)
[![Stdlib only](https://img.shields.io/badge/deps-stdlib_only-success?logo=python&logoColor=white)](pyproject.toml)
[![Codeberg](https://img.shields.io/badge/Codeberg-CryptoJones%2FTriage-2185D0?logo=codeberg&logoColor=white)](https://codeberg.org/CryptoJones/Triage)
[![GitHub](https://img.shields.io/badge/GitHub-CryptoJones%2FTriage-181717?logo=github&logoColor=white)](https://github.com/CryptoJones/Triage)

**Llegeix-ho en:**
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
[Dansk](README.da.md) ·
[Suomi](README.fi.md) ·
[Română](README.ro.md) ·
[Magyar](README.hu.md) ·
[Türkçe](README.tr.md) ·
**Català**

</div>

> Replicat tant a [GitHub](https://github.com/CryptoJones/Triage) com a
> [Codeberg](https://codeberg.org/CryptoJones/Triage). Els tiquets a
> qualsevol de les dues farges són benvinguts; els commits aterren a
> totes dues.

---

## El que veus

```
╔════════════════════════════════════════════════════════╗
║                  T R I A G E   v0.10.0                  ║
╚════════════════════════════════════════════════════════╝
  ID               PRI  BAR    ASSUMPTE
  ════════════  ══════  ═════  ════════════════════════════════════════
  7cfa440bc639  [ 101]  █████  Arreglar el linter      ← bloquejador auto-elevat
  f35d7cea6b7d  [ 100]  █████  Afegir funció X         ← bloquejada pel linter
  19c80b807ddd  [  35]  █▒░░░  Rotar certificat        ← pressió de termini
  abc123456789  [   2]  ░░░░░  Neteja rutinària
```

En un terminal real, la pancarta és magenta brillant, les prioritats
estan acolorides per bandes (alta = groc, mitjana = verd, baixa =
cian atenuat) i les barres de prioritat s'omplen proporcionalment.
El tema per defecte `bbs` és descaradament dels anys 90.

---

## Com funciona

```
                   ┌─────────────────────┐
   senyals  ─────► │  Fonts de senyal    │  (cron-window, github-ci, ...)
                   └──────────┬──────────┘
                              ▼
                   ┌─────────────────────┐
                   │  ~/.triage/state/   │  (append-only JSONL per font)
                   └──────────┬──────────┘
                              ▼
   tick     ─────► ┌─────────────────────┐ ─────► cua reordenada
                   │ Planificador Triage │        + registre d'auditoria per tasca
                   └──────────┬──────────┘
                              ▼
                   ┌─────────────────────┐
   tasques  ─────► │      CLI triage     │
                   └─────────────────────┘
```

1. **Les fonts de senyal** aporten fets (`cron-window`, `github-ci`,
   futurs `runpod-cost`, `github-pr`...).
2. **Les regles** converteixen els fets en deltes de prioritat
   (`base_score`, `deadline_decay`, `cron_window_active`,
   `ci_failing`, `blocker_transitive`).
3. **La cua es reordena** a cada `triage tick`.
4. **Cada reordenació és explicable** — `triage why <id>` mostra
   exactament quines regles han contribuït amb quines deltes, així
   que l'ordre mai no és una caixa negra.

Mira [`DESIGN.md`](DESIGN.md) per a l'arquitectura completa, el
catàleg de regles i el full de ruta.

---

## Instal·lació

```bash
git clone https://github.com/CryptoJones/Triage      # o codeberg.org/CryptoJones/Triage
cd Triage
pip install -e .
```

Biblioteca estàndard de Python pura. Sense dependències en temps
d'execució. Provat a 3.10 / 3.11 / 3.12.

---

## Ús

### Tasques

```bash
triage add "Arreglar bug d'autenticació" --base-score 10
triage add "Rotar el certificat de staging" --deadline 2026-05-20T00:00:00Z
triage add "Tasca només laborable"  --cron-window "* 9-17 * * 1-5"
triage add "Vigilar CI"             --tag "gh-ci:CryptoJones/Triage@main"
triage add "Esperar al linter"      --blocked-by <linter-task-id>

triage list                     # ordre de prioritat actual
triage show <id>                # registre brut de la tasca (JSON)
triage why  <id>                # quines regles han contribuït amb quines deltes
triage rm   <id>                # eliminar
```

### Reordenar + sondejar

```bash
triage tick                     # recalcular prioritats; imprimir nou ordre
triage poll github-ci           # invocar una font de senyal lligada a la xarxa
```

`tick` és barat, local i idempotent — crida'l des de cron, un bucle
de shell o `ScheduleWakeup` de Claude Code. `poll` és per a fonts de
senyal que toquen la xarxa (pagues per aquestes explícitament).

### Llengua

Triage parla diverses llengües. Estableix la llengua amb l'opció
`--lang` o les variables d'entorn habituals:

```bash
triage --lang ca list           # un sol cop
TRIAGE_LANG=ca triage list      # per shell
triage lang                     # llista les llengües disponibles
```

Llengües suportades: English, Español, Français, Deutsch, Italiano,
Português, Nederlands, Polski, Čeština, Svenska, Norsk, Dansk, Suomi,
Română, Magyar, Türkçe, Català. Si la llengua no es reconeix, s'usa
l'anglès com a reserva.

### Registre d'esdeveniments (per a agents externs)

Cada invocació del CLI afegeix una sola línia JSON a un fitxer de
registre, així un agent extern pot fer `tail -f` i analitzar el
comportament de Triage:

```bash
tail -f /var/log/triage.log | jq .   # si el fitxer pertany al teu usuari
```

Entrades d'exemple:

```json
{"ts":"2026-05-16T06:16:18+00:00","event":"add","task_id":"9e8040d267d9","subject":"Investigar consulta lenta","base_score":10,"tags":[],"deadline":null,"blocked_by":[]}
{"ts":"2026-05-16T06:16:18+00:00","event":"tick","ranked_count":2,"emitted_cron_signals":0,"top":[{"id":"ad2006db3c12","priority":35,"subject":"Rotar certificat"}],"warnings":[]}
{"ts":"2026-05-16T06:16:19+00:00","event":"poll","source":"github-ci","emitted":1,"warnings":[]}
{"ts":"2026-05-16T06:16:20+00:00","event":"rm","task_id":"9e8040d267d9"}
```

Configuració:

| Mecanisme                  | Què fa                                                            |
|----------------------------|-------------------------------------------------------------------|
| opció `--log-file PATH`    | Camí del registre per invocació.                                  |
| env `TRIAGE_LOG_FILE=PATH` | Camí del registre per shell.                                      |
| Per defecte                | `/var/log/triage.log`. Recau a `~/.triage/triage.log` si `/var/log` no és escrivible (avisa un cop a stderr). |
| opció `--no-log`           | Desactiva el registre per a aquesta invocació.                    |
| env `TRIAGE_NO_LOG=1`      | Desactiva el registre globalment per al shell.                    |

Per utilitzar el camí estàndard `/var/log` sense sudo a cada crida:

```bash
sudo touch /var/log/triage.log
sudo chown $(id -un):$(id -gn) /var/log/triage.log
```

El registre és un canal lateral estrictament unidireccional — els
errors durant l'escriptura s'empassen perquè el comportament principal
del CLI mai no es vegi interromput.

### Temes

```bash
triage theme                    # llista temes disponibles
triage theme --name bbs         # renderitza files d'exemple
triage --theme modern list      # sobreescriu el tema per una invocació
TRIAGE_THEME=mono triage list   # tema per shell
```

| Tema     | Estètica                                                              |
|----------|-----------------------------------------------------------------------|
| `bbs`    | **Per defecte.** BBS dels 90: magenta brillant, marc de doble línia (`╔═╗`), barres de blocs. |
| `modern` | Paleta subtil, marcs de línia simple (`┌─┐`), barres de punts (`█▒·`). |
| `mono`   | Sense color, només ASCII (`+-+`, `#=.`) — segur per a canonades i terminals senzills. |

El color segueix les convencions:

- Desactivat automàticament quan stdout no és un TTY.
- `NO_COLOR=1` desactiva el color (segons [no-color.org](https://no-color.org/)).
- `FORCE_COLOR=1` activa el color en no-TTY.
- L'opció `--no-color` = interruptor explícit per invocació.

---

## Projectes relacionats

Triage és una peça d'un petit ecosistema. Les peces es componen:

| Repositori | Rol |
|------------|-----|
| [**claude_skill-Triage**](https://github.com/CryptoJones/claude_skill-Triage) | Repositori de skills de Claude Code. Avui ofereix `TaskPriorityReorder` (**sobreescriptura manual** — «pujar X al capdamunt») i allotjarà la skill `triage` (**recomanador guiat per senyals** — «què hauria de fer ara?») en una versió futura. |
| [**TriageMCP**](https://github.com/CryptoJones/TriageMCP) | **Servidor MCP** que embolcalla l'API de Triage per a agents d'IA. Vuit eines (`list_tasks`, `add_task`, `tick`, `why_task`, `status`, `remove_task`, `inject_signal`, `get_task`) sobre stdio. Posa'l a `~/.claude/mcp.json` i un agent podrà llegir i escriure la teva cua de prioritats directament. |
| [**RunPodBoss**](https://github.com/CryptoJones/RunPodBoss) | Protector del saldo de crèdit de RunPod. S'integra amb Triage via `extra_notify_command` — quan se sobrepassa un llindar de facturació, RunPodBoss empeny un senyal manual a Triage perquè la tasca «buidar pods inactius» suri al capdamunt de la teva cua. Recepta de configuració a [`docs/runpodboss-integration.md`](docs/runpodboss-integration.md). |

Els quatre comparteixen la primitiva de Triage (identitat estable +
prioritat recalculable) i viuen en miralls dobles (GitHub + Codeberg).

---

## Estat

| Versió | Característica                                                       | Estat       |
|--------|----------------------------------------------------------------------|-------------|
| v0.1   | esquelet, tres regles, senyal cron-window, CLI                       | llançada    |
| v0.2   | propagació `blocker_transitive` + detecció de cicles                 | llançada    |
| v0.3   | font de senyal `github-ci` + regla `ci_failing` + `triage poll`      | llançada    |
| v0.4   | sistema de temes ANSI estil BBS + subcomanda `triage theme`          | llançada    |
| v0.5   | font de senyal `runpod-cost` + regla `cost_pressure`                 | llançada    |
| v0.6   | escriptor de registre d'esdeveniments JSONL per a agents externs     | llançada    |
| v0.7   | font de senyal `github-pr` + regla `rule_stale_pr`                   | llançada    |
| v0.8   | CLI `triage signal` + regla `manual_bump` + integració RunPodBoss    | llançada    |
| v0.8.1 | resum d'un cop d'ull `triage status`                                 | llançada    |
| v0.9   | base d'i18n — opció `--lang` + locales en/es/fr                      | llançada    |
| v0.10  | i18n completa — 17 locales + detector de regressions `triage lang --check` | llançada    |
| —      | skill `triage` de Claude Code (al repo `claude_skill-Triage`)        | planificada |
| —      | mode `triage watch` de llarga durada + unitat systemd                | planificada |

---

## Llicència

Apache 2.0. Vegeu [LICENSE](LICENSE).

Fet amb orgull a Nebraska. Go Big Red! 🌽 https://xkcd.com/2347/
