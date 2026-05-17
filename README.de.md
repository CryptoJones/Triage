<div align="center">

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                    T  R  I  A  G  E                          ║
║                                                              ║
║      Meta-Scheduler, der seine eigene Warteschlange beobachtet ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Eine selbstbewusste Prioritätswarteschlange.** Signale tragen
Fakten über die Welt ein; Regeln wandeln Fakten in Prioritätsdeltas
um; die Warteschlange ordnet sich bei jedem Tick selbst neu. Sie
setzen die Ziele — Triage entscheidet die Reihenfolge und erklärt
genau warum.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg?logo=apache)](LICENSE)
[![Stdlib only](https://img.shields.io/badge/deps-stdlib_only-success?logo=python&logoColor=white)](pyproject.toml)
[![Codeberg](https://img.shields.io/badge/Codeberg-CryptoJones%2FTriage-2185D0?logo=codeberg&logoColor=white)](https://codeberg.org/CryptoJones/Triage)
[![GitHub](https://img.shields.io/badge/GitHub-CryptoJones%2FTriage-181717?logo=github&logoColor=white)](https://github.com/CryptoJones/Triage)

**Lies das auf:**
[English](README.md) ·
[Español](README.es.md) ·
[Français](README.fr.md) ·
**Deutsch** ·
[Italiano](README.it.md) ·
[Português](README.pt.md) ·
[Nederlands](README.nl.md) ·
[Polski](README.pl.md) ·
[Čeština](README.cs.md) ·
[Svenska](README.sv.md) ·
[Norsk](README.no.md) ·
[Dansk](README.da.md) ·
[Suomi](README.fi.md)

</div>

> Gespiegelt auf [GitHub](https://github.com/CryptoJones/Triage) und
> [Codeberg](https://codeberg.org/CryptoJones/Triage). Issues auf
> beiden Forges sind willkommen; Commits landen auf beiden.

---

## Was Sie sehen

```
╔════════════════════════════════════════════════════════╗
║                  T R I A G E   v0.9.0                  ║
╚════════════════════════════════════════════════════════╝
  ID               PRI  BAL    BETREFF
  ════════════  ══════  ═════  ════════════════════════════════════════
  7cfa440bc639  [ 101]  █████  Linter reparieren     ← Blockierer auto-erhöht
  f35d7cea6b7d  [ 100]  █████  Feature X hinzufügen  ← blockiert vom Linter
  19c80b807ddd  [  35]  █▒░░░  Zertifikat rotieren   ← Termindruck
  abc123456789  [   2]  ░░░░░  Routinepflege
```

In einem echten Terminal ist das Banner hellmagenta, die Prioritäten
sind farblich gebändert (hoch = gelb, mittel = grün, niedrig = mattes
Cyan) und die Prioritätsbalken füllen sich proportional. Das
Standardthema `bbs` ist unverschämt 90er-Jahre.

---

## Funktionsweise

```
                   ┌─────────────────────┐
   Signale  ─────► │   Signalquellen     │  (cron-window, github-ci, ...)
                   └──────────┬──────────┘
                              ▼
                   ┌─────────────────────┐
                   │  ~/.triage/state/   │  (append-only JSONL pro Quelle)
                   └──────────┬──────────┘
                              ▼
   tick     ─────► ┌─────────────────────┐ ─────► neu geordnete Warteschlange
                   │  Triage-Scheduler   │        + Audit-Protokoll
                   └──────────┬──────────┘
                              ▼
                   ┌─────────────────────┐
   Aufgaben ─────► │     Triage-CLI      │
                   └─────────────────────┘
```

1. **Signalquellen** tragen Fakten ein (`cron-window`, `github-ci`,
   künftig `runpod-cost`, `github-pr`...).
2. **Regeln** wandeln Fakten in Prioritätsdeltas um (`base_score`,
   `deadline_decay`, `cron_window_active`, `ci_failing`,
   `blocker_transitive`).
3. **Die Warteschlange wird neu geordnet** bei jedem `triage tick`.
4. **Jede Neuordnung ist erklärbar** — `triage why <id>` zeigt genau,
   welche Regeln welche Deltas beigetragen haben, die Reihenfolge ist
   also nie eine Blackbox.

Siehe [`DESIGN.md`](DESIGN.md) für die vollständige Architektur, den
Regelkatalog und die Roadmap.

---

## Installation

```bash
git clone https://github.com/CryptoJones/Triage      # oder codeberg.org/CryptoJones/Triage
cd Triage
pip install -e .
```

Reines Python-Stdlib. Keine Laufzeitabhängigkeiten. Getestet auf
3.10 / 3.11 / 3.12.

---

## Verwendung

### Aufgaben

```bash
triage add "Auth-Bug beheben" --base-score 10
triage add "Staging-Zertifikat rotieren" --deadline 2026-05-20T00:00:00Z
triage add "Nur-Werktags-Aufgabe" --cron-window "* 9-17 * * 1-5"
triage add "CI beobachten"     --tag "gh-ci:CryptoJones/Triage@main"
triage add "Auf Linter warten" --blocked-by <linter-task-id>

triage list                     # aktuelle Prioritätsreihenfolge
triage show <id>                # vollständiger Aufgaben-Datensatz (JSON)
triage why  <id>                # welche Regeln welche Deltas beigetragen haben
triage rm   <id>                # entfernen
```

### Neuordnen + Abfragen

```bash
triage tick                     # Prioritäten neu berechnen; neue Reihenfolge ausgeben
triage poll github-ci           # eine netzwerkgebundene Signalquelle aufrufen
```

`tick` ist günstig, lokal und idempotent — rufen Sie es von cron,
einer Shell-Schleife oder Claude Codes `ScheduleWakeup` auf. `poll`
ist für Signalquellen, die das Netzwerk berühren (diese Kosten zahlen
Sie explizit).

### Sprache

Triage spricht mehrere Sprachen. Sprache mit der `--lang`-Option oder
den üblichen Umgebungsvariablen festlegen:

```bash
triage --lang de list           # einmalig
TRIAGE_LANG=de triage list      # pro Shell
triage lang                     # listet verfügbare Sprachen
```

Unterstützte Sprachen: English, Español, Français, Deutsch, Italiano,
Português. Unbekannte Sprachen fallen auf Englisch zurück.

### Ereignisprotokoll (für externe Agenten)

Jeder CLI-Aufruf hängt eine einzelne JSON-Zeile an eine Protokolldatei
an, sodass ein externer Agent das Verhalten von Triage per `tail -f`
beobachten und parsen kann:

```bash
tail -f /var/log/triage.log | jq .   # wenn die Datei Ihrem Benutzer gehört
```

Beispieleinträge:

```json
{"ts":"2026-05-16T06:16:18+00:00","event":"add","task_id":"9e8040d267d9","subject":"Langsame Abfrage untersuchen","base_score":10,"tags":[],"deadline":null,"blocked_by":[]}
{"ts":"2026-05-16T06:16:18+00:00","event":"tick","ranked_count":2,"emitted_cron_signals":0,"top":[{"id":"ad2006db3c12","priority":35,"subject":"Zertifikat rotieren"}],"warnings":[]}
{"ts":"2026-05-16T06:16:19+00:00","event":"poll","source":"github-ci","emitted":1,"warnings":[]}
{"ts":"2026-05-16T06:16:20+00:00","event":"rm","task_id":"9e8040d267d9"}
```

Konfiguration:

| Mechanismus                | Was es tut                                                          |
|----------------------------|---------------------------------------------------------------------|
| Option `--log-file PFAD`   | Protokollpfad pro Aufruf.                                           |
| env `TRIAGE_LOG_FILE=PFAD` | Protokollpfad pro Shell.                                            |
| Standard                   | `/var/log/triage.log`. Weicht auf `~/.triage/triage.log` aus, wenn `/var/log` nicht schreibbar ist (warnt einmalig auf stderr). |
| Option `--no-log`          | Protokollierung für diesen Aufruf deaktivieren.                     |
| env `TRIAGE_NO_LOG=1`      | Protokollierung global für die Shell deaktivieren.                  |

So nutzen Sie den Standardpfad `/var/log` ohne sudo bei jedem Aufruf:

```bash
sudo touch /var/log/triage.log
sudo chown $(id -un):$(id -gn) /var/log/triage.log
```

Die Protokollierung ist ein striktes Einweg-Seitenkanal — Schreibfehler
werden geschluckt, damit das Hauptverhalten der CLI nie gestört wird.

### Themen

```bash
triage theme                    # verfügbare Themen auflisten
triage theme --name bbs         # Beispielzeilen rendern
triage --theme modern list      # einmalige Themen-Übersteuerung
TRIAGE_THEME=mono triage list   # Thema pro Shell
```

| Thema    | Ästhetik                                                                  |
|----------|---------------------------------------------------------------------------|
| `bbs`    | **Standard.** 90er-Jahre BBS: hellmagenta, Doppellinien-Rahmen (`╔═╗`), Blockbalken. |
| `modern` | Dezente Palette, Einzellinien-Rahmen (`┌─┐`), Punkt-Balken (`█▒·`).      |
| `mono`   | Keine Farbe, nur ASCII (`+-+`, `#=.`) — sicher für Pipes / einfache Terminals. |

Farbverhalten:

- Automatisch deaktiviert, wenn stdout kein TTY ist.
- `NO_COLOR=1` deaktiviert Farbe (gemäß [no-color.org](https://no-color.org/)).
- `FORCE_COLOR=1` aktiviert Farbe auf nicht-TTYs.
- Option `--no-color` = expliziter Notausschalter pro Aufruf.

---

## Verwandte Projekte

Triage ist ein Baustein eines kleinen Ökosystems. Die Teile greifen ineinander:

| Repository | Rolle |
|------------|-------|
| [**claude_skill-Triage**](https://github.com/CryptoJones/claude_skill-Triage) | Claude-Code-Skills-Repository. Liefert heute `TaskPriorityReorder` (**manuelle Übersteuerung** — „X nach oben schieben") und wird die `triage`-Skill (**signalgetriebener Empfehlungsgeber** — „was soll ich als Nächstes tun?") in einem zukünftigen Release beherbergen. |
| [**TriageMCP**](https://github.com/CryptoJones/TriageMCP) | **MCP-Server**, der die Triage-API für KI-Agenten verfügbar macht. Acht Werkzeuge (`list_tasks`, `add_task`, `tick`, `why_task`, `status`, `remove_task`, `inject_signal`, `get_task`) über stdio. In `~/.claude/mcp.json` eintragen, und ein Agent kann deine Prioritätswarteschlange direkt lesen und schreiben. |
| [**RunPodBoss**](https://github.com/CryptoJones/RunPodBoss) | Guthaben-Schutzschwelle für RunPod. Integriert sich mit Triage über `extra_notify_command` — bei Überschreiten einer Abrechnungsschwelle injiziert RunPodBoss ein manuelles Signal in Triage, sodass die Aufgabe „leerlaufende Pods abbauen" an die Spitze deiner Warteschlange wandert. Konfigurationsrezept in [`docs/runpodboss-integration.md`](docs/runpodboss-integration.md). |

Alle vier teilen die Triage-Primitive (stabile Identität + neu berechenbare
Priorität) und leben auf Doppel-Mirrors (GitHub + Codeberg).

---

## Status

| Version | Funktion                                                                | Status        |
|---------|-------------------------------------------------------------------------|---------------|
| v0.1    | Gerüst, drei Regeln, cron-window-Signal, CLI                            | veröffentlicht |
| v0.2    | `blocker_transitive`-Propagation + Zykluserkennung                      | veröffentlicht |
| v0.3    | `github-ci`-Signalquelle + `ci_failing`-Regel + `triage poll`           | veröffentlicht |
| v0.4    | ANSI-Themensystem im BBS-Stil + Unterbefehl `triage theme`              | veröffentlicht |
| v0.5    | `runpod-cost`-Signalquelle + `cost_pressure`-Regel                      | veröffentlicht |
| v0.6    | JSONL-Ereignisprotokollschreiber für externe Agenten                    | veröffentlicht |
| v0.7    | `github-pr`-Signalquelle für veraltete PRs                              | geplant        |
| v0.8    | Claude-Code-`triage`-Skill (im Repo `claude_skill-Triage`)              | geplant        |
| v0.9    | Langläufer-Modus `triage watch` + systemd-Unit                          | geplant        |

---

## Lizenz

Apache 2.0. Siehe [LICENSE](LICENSE).

Stolz hergestellt in Nebraska. Go Big Red! 🌽 https://xkcd.com/2347/
