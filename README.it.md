<div align="center">

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                    T  R  I  A  G  E                          ║
║                                                              ║
║      meta-scheduler che osserva la propria coda              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Una coda di priorità autocosciente.** I segnali apportano fatti
sul mondo; le regole convertono i fatti in delta di priorità; la
coda si riordina da sola a ogni tick. Tu fissi gli obiettivi —
Triage decide l'ordine e ti spiega esattamente perché.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg?logo=apache)](LICENSE)
[![Stdlib only](https://img.shields.io/badge/deps-stdlib_only-success?logo=python&logoColor=white)](pyproject.toml)
[![Codeberg](https://img.shields.io/badge/Codeberg-CryptoJones%2FTriage-2185D0?logo=codeberg&logoColor=white)](https://codeberg.org/CryptoJones/Triage)
[![GitHub](https://img.shields.io/badge/GitHub-CryptoJones%2FTriage-181717?logo=github&logoColor=white)](https://github.com/CryptoJones/Triage)

**Leggilo in:**
[English](README.md) ·
[Español](README.es.md) ·
[Français](README.fr.md) ·
[Deutsch](README.de.md) ·
**Italiano** ·
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
[Türkçe](README.tr.md)

</div>

> Replicato sia su [GitHub](https://github.com/CryptoJones/Triage) sia
> su [Codeberg](https://codeberg.org/CryptoJones/Triage). Le issue
> aperte su una qualsiasi delle due forge sono benvenute; i commit
> approdano su entrambe.

---

## Cosa vedi

```
╔════════════════════════════════════════════════════════╗
║                  T R I A G E   v0.9.0                  ║
╚════════════════════════════════════════════════════════╝
  ID               PRI  BAR    OGGETTO
  ════════════  ══════  ═════  ════════════════════════════════════════
  7cfa440bc639  [ 101]  █████  Correggere il linter   ← bloccante auto-promosso
  f35d7cea6b7d  [ 100]  █████  Aggiungere funzionalità X
  19c80b807ddd  [  35]  █▒░░░  Rotare il certificato  ← pressione scadenza
  abc123456789  [   2]  ░░░░░  Pulizia di routine
```

In un terminale reale il banner è magenta brillante, le priorità
sono colorate a fasce (alta = giallo, media = verde, bassa = ciano
attenuato) e le barre di priorità si riempiono in proporzione. Il
tema predefinito `bbs` è sfacciatamente anni '90.

---

## Come funziona

```
                   ┌─────────────────────┐
   segnali  ─────► │  Sorgenti di segnale│  (cron-window, github-ci, ...)
                   └──────────┬──────────┘
                              ▼
                   ┌─────────────────────┐
                   │  ~/.triage/state/   │  (JSONL append-only per sorgente)
                   └──────────┬──────────┘
                              ▼
   tick     ─────► ┌─────────────────────┐ ─────► coda riordinata
                   │  Scheduler Triage   │        + registro di audit
                   └──────────┬──────────┘
                              ▼
                   ┌─────────────────────┐
   attività ─────► │      CLI triage     │
                   └─────────────────────┘
```

1. **Le sorgenti di segnale** apportano fatti (`cron-window`,
   `github-ci`, futuri `runpod-cost`, `github-pr`...).
2. **Le regole** convertono i fatti in delta di priorità
   (`base_score`, `deadline_decay`, `cron_window_active`,
   `ci_failing`, `blocker_transitive`).
3. **La coda si riordina** a ogni `triage tick`.
4. **Ogni riordino è spiegabile** — `triage why <id>` mostra
   esattamente quali regole hanno contribuito quali delta, quindi
   l'ordine non è mai una scatola nera.

Vedi [`DESIGN.md`](DESIGN.md) per l'architettura completa, il
catalogo delle regole e la roadmap.

---

## Installazione

```bash
git clone https://github.com/CryptoJones/Triage      # o codeberg.org/CryptoJones/Triage
cd Triage
pip install -e .
```

Python stdlib puro. Nessuna dipendenza a runtime. Testato su
3.10 / 3.11 / 3.12.

---

## Uso

### Attività

```bash
triage add "Correggere il bug di auth" --base-score 10
triage add "Rotare il certificato di staging" --deadline 2026-05-20T00:00:00Z
triage add "Compito solo nei giorni feriali" --cron-window "* 9-17 * * 1-5"
triage add "Monitorare CI"          --tag "gh-ci:CryptoJones/Triage@main"
triage add "Attendere il linter"    --blocked-by <linter-task-id>

triage list                     # ordine di priorità attuale
triage show <id>                # record grezzo dell'attività (JSON)
triage why  <id>                # quali regole hanno contribuito quali delta
triage rm   <id>                # rimuovi
```

### Riordinare + sondare

```bash
triage tick                     # ricalcola le priorità; stampa il nuovo ordine
triage poll github-ci           # invoca una sorgente di segnale di rete
```

`tick` è economico, locale e idempotente — chiamalo da cron, da un
loop di shell o dallo `ScheduleWakeup` di Claude Code. `poll` è per
le sorgenti di segnale che toccano la rete (questi costi si pagano
esplicitamente).

### Lingua

Triage parla diverse lingue. Imposta la lingua con l'opzione `--lang`
o le solite variabili d'ambiente:

```bash
triage --lang it list           # una tantum
TRIAGE_LANG=it triage list      # per shell
triage lang                     # elenca le lingue disponibili
```

Lingue supportate: English, Español, Français, Deutsch, Italiano,
Português. Le lingue sconosciute ripiegano sull'inglese.

### Registro eventi (per agenti esterni)

Ogni invocazione della CLI aggiunge una singola riga JSON a un file
di registro, così un agente esterno può `tail -f` e analizzare il
comportamento di Triage:

```bash
tail -f /var/log/triage.log | jq .   # se il file appartiene al tuo utente
```

Esempi di voci:

```json
{"ts":"2026-05-16T06:16:18+00:00","event":"add","task_id":"9e8040d267d9","subject":"Investigare query lenta","base_score":10,"tags":[],"deadline":null,"blocked_by":[]}
{"ts":"2026-05-16T06:16:18+00:00","event":"tick","ranked_count":2,"emitted_cron_signals":0,"top":[{"id":"ad2006db3c12","priority":35,"subject":"Rotare certificato"}],"warnings":[]}
{"ts":"2026-05-16T06:16:19+00:00","event":"poll","source":"github-ci","emitted":1,"warnings":[]}
{"ts":"2026-05-16T06:16:20+00:00","event":"rm","task_id":"9e8040d267d9"}
```

Configurazione:

| Meccanismo                 | Effetto                                                             |
|----------------------------|---------------------------------------------------------------------|
| opzione `--log-file PATH`  | Percorso del registro per invocazione.                              |
| env `TRIAGE_LOG_FILE=PATH` | Percorso del registro per shell.                                    |
| Predefinito                | `/var/log/triage.log`. Ripiega su `~/.triage/triage.log` se `/var/log` non è scrivibile (avvisa una volta su stderr). |
| opzione `--no-log`         | Disabilita la registrazione per questa invocazione.                 |
| env `TRIAGE_NO_LOG=1`      | Disabilita la registrazione globalmente per la shell.               |

Per usare il percorso standard `/var/log` senza sudo a ogni chiamata:

```bash
sudo touch /var/log/triage.log
sudo chown $(id -un):$(id -gn) /var/log/triage.log
```

Il registro è un canale laterale unidirezionale rigoroso — gli errori
in scrittura vengono ignorati così il comportamento principale della
CLI non viene mai interrotto.

### Temi

```bash
triage theme                    # elenca i temi disponibili
triage theme --name bbs         # renderizza righe di esempio
triage --theme modern list      # sostituzione del tema una tantum
TRIAGE_THEME=mono triage list   # tema per shell
```

| Tema     | Estetica                                                                |
|----------|-------------------------------------------------------------------------|
| `bbs`    | **Predefinito.** BBS anni '90: magenta brillante, riquadro a doppia linea (`╔═╗`), barre a blocchi. |
| `modern` | Palette discreta, riquadri a linea singola (`┌─┐`), barre a punti (`█▒·`). |
| `mono`   | Senza colore, solo ASCII (`+-+`, `#=.`) — sicuro per pipe / terminali semplici. |

Il colore segue gli standard:

- Disabilitato automaticamente quando stdout non è un TTY.
- `NO_COLOR=1` disabilita il colore (cfr. [no-color.org](https://no-color.org/)).
- `FORCE_COLOR=1` abilita il colore su non-TTY.
- L'opzione `--no-color` = interruttore esplicito per invocazione.

---

## Progetti correlati

Triage è un pezzo di un piccolo ecosistema. I pezzi si combinano:

| Repository | Ruolo |
|------------|-------|
| [**claude_skill-Triage**](https://github.com/CryptoJones/claude_skill-Triage) | Repository delle skill di Claude Code. Fornisce oggi `TaskPriorityReorder` (**sovrascrittura manuale** — «porta X in cima») e ospiterà la skill `triage` (**raccomandatore guidato dai segnali** — «cosa dovrei fare adesso?») in una versione futura. |
| [**TriageMCP**](https://github.com/CryptoJones/TriageMCP) | **Server MCP** che avvolge l'API di Triage per agenti IA. Otto strumenti (`list_tasks`, `add_task`, `tick`, `why_task`, `status`, `remove_task`, `inject_signal`, `get_task`) su stdio. Inseriscilo in `~/.claude/mcp.json` e un agente potrà leggere e scrivere direttamente la tua coda di priorità. |
| [**RunPodBoss**](https://github.com/CryptoJones/RunPodBoss) | Salvaguardia del saldo di credito per RunPod. Si integra con Triage tramite `extra_notify_command` — quando viene superata una soglia di fatturazione, RunPodBoss inietta un segnale manuale in Triage in modo che l'attività «svuota i pod inattivi» salga in cima alla tua coda. Ricetta di configurazione in [`docs/runpodboss-integration.md`](docs/runpodboss-integration.md). |

Tutti e quattro condividono la primitiva di Triage (identità stabile + priorità
ricalcolabile) e vivono su mirror doppi (GitHub + Codeberg).

---

## Stato

| Versione | Funzionalità                                                            | Stato      |
|----------|-------------------------------------------------------------------------|------------|
| v0.1     | scheletro, tre regole, segnale cron-window, CLI                         | pubblicata |
| v0.2     | propagazione `blocker_transitive` + rilevamento dei cicli               | pubblicata |
| v0.3     | sorgente di segnale `github-ci` + regola `ci_failing` + `triage poll`   | pubblicata |
| v0.4     | tema ANSI in stile BBS + sottocomando `triage theme`                    | pubblicata |
| v0.5     | sorgente di segnale `runpod-cost` + regola `cost_pressure`              | pubblicata |
| v0.6     | scrittore di registro eventi JSONL per agenti esterni                   | pubblicata |
| v0.7     | sorgente di segnale `github-pr` per PR obsolete                         | pianificata |
| v0.8     | skill `triage` di Claude Code (nel repo `claude_skill-Triage`)          | pianificata |
| v0.9     | modalità `triage watch` a lunga esecuzione + unità systemd              | pianificata |

---

## Licenza

Apache 2.0. Vedi [LICENSE](LICENSE).

Fatto con orgoglio in Nebraska. Go Big Red! 🌽 https://xkcd.com/2347/
