<div align="center">

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                    T  R  I  A  G  E                          ║
║                                                              ║
║      meta-planificator care își urmărește propria coadă      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**O coadă de priorități conștientă de sine.** Semnalele aduc fapte
despre lume; regulile transformă faptele în delte de prioritate;
coada se reordonează singură la fiecare tick. Tu stabilești
obiectivele — Triage decide ordinea și îți spune exact de ce.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg?logo=apache)](LICENSE)
[![Stdlib only](https://img.shields.io/badge/deps-stdlib_only-success?logo=python&logoColor=white)](pyproject.toml)
[![Codeberg](https://img.shields.io/badge/Codeberg-CryptoJones%2FTriage-2185D0?logo=codeberg&logoColor=white)](https://codeberg.org/CryptoJones/Triage)
[![GitHub](https://img.shields.io/badge/GitHub-CryptoJones%2FTriage-181717?logo=github&logoColor=white)](https://github.com/CryptoJones/Triage)

**Citește în:**
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
**Română** ·
[Magyar](README.hu.md) ·
[Türkçe](README.tr.md) ·
[Català](README.ca.md)

</div>

> Oglindit atât pe [GitHub](https://github.com/CryptoJones/Triage) cât și pe
> [Codeberg](https://codeberg.org/CryptoJones/Triage). Tichetele pe oricare
> dintre forge-uri sunt binevenite; commit-urile aterizează pe ambele.

---

## Ce vezi

```
╔════════════════════════════════════════════════════════╗
║                  T R I A G E   v0.9.0                  ║
╚════════════════════════════════════════════════════════╝
  ID               PRI  BAR    SUBIECT
  ════════════  ══════  ═════  ════════════════════════════════════════
  7cfa440bc639  [ 101]  █████  Repară linter-ul       ← blocator auto-ridicat
  f35d7cea6b7d  [ 100]  █████  Adaugă funcția X       ← blocat de linter
  19c80b807ddd  [  35]  █▒░░░  Rotește certificatul   ← presiune termen
  abc123456789  [   2]  ░░░░░  Curățenie de rutină
```

Într-un terminal real, banner-ul este magenta strălucitor, prioritățile
sunt colorate pe benzi (mare = galben, mediu = verde, mic = cyan
diluat) și barele de prioritate se umplu proporțional. Tema implicită
`bbs` este fără rușine anii '90.

---

## Cum funcționează

```
                   ┌─────────────────────┐
   semnale  ─────► │   Surse de semnal   │  (cron-window, github-ci, ...)
                   └──────────┬──────────┘
                              ▼
                   ┌─────────────────────┐
                   │  ~/.triage/state/   │  (append-only JSONL per sursă)
                   └──────────┬──────────┘
                              ▼
   tick     ─────► ┌─────────────────────┐ ─────► coadă reordonată
                   │ Planificator Triage │        + jurnal de audit pe sarcină
                   └──────────┬──────────┘
                              ▼
                   ┌─────────────────────┐
   sarcini  ─────► │      CLI triage     │
                   └─────────────────────┘
```

1. **Sursele de semnal** aduc fapte (`cron-window`, `github-ci`,
   viitoarele `runpod-cost`, `github-pr`...).
2. **Regulile** transformă faptele în delte de prioritate
   (`base_score`, `deadline_decay`, `cron_window_active`,
   `ci_failing`, `blocker_transitive`).
3. **Coada se reordonează** la fiecare `triage tick`.
4. **Fiecare reordonare este explicabilă** — `triage why <id>` arată
   exact care reguli au contribuit cu ce delte, deci ordinea nu este
   niciodată o cutie neagră.

Vezi [`DESIGN.md`](DESIGN.md) pentru arhitectura completă, catalogul
de reguli și foaia de parcurs.

---

## Instalare

```bash
git clone https://github.com/CryptoJones/Triage      # sau codeberg.org/CryptoJones/Triage
cd Triage
pip install -e .
```

Bibliotecă standard Python pură. Fără dependențe în timpul rulării.
Testat pe 3.10 / 3.11 / 3.12.

---

## Utilizare

### Sarcini

```bash
triage add "Repară bug-ul de autentificare" --base-score 10
triage add "Rotește certificatul staging" --deadline 2026-05-20T00:00:00Z
triage add "Treabă doar în zilele lucrătoare" --cron-window "* 9-17 * * 1-5"
triage add "Supraveghează CI"     --tag "gh-ci:CryptoJones/Triage@main"
triage add "Așteaptă linter-ul"   --blocked-by <linter-task-id>

triage list                     # ordinea curentă a priorităților
triage show <id>                # înregistrarea brută a sarcinii (JSON)
triage why  <id>                # care reguli au contribuit cu ce delte
triage rm   <id>                # elimină
```

### Reordonare + interogare

```bash
triage tick                     # recalculează prioritățile; afișează noua ordine
triage poll github-ci           # invocă o sursă de semnal legată de rețea
```

`tick` este ieftin, local și idempotent — apelează-l din cron, dintr-o
buclă shell sau din `ScheduleWakeup` al Claude Code. `poll` este pentru
surse de semnal care ating rețeaua (plătești explicit pentru acelea).

### Limbă

Triage vorbește mai multe limbi. Setează limba cu opțiunea `--lang`
sau cu variabilele de mediu obișnuite:

```bash
triage --lang ro list           # o singură dată
TRIAGE_LANG=ro triage list      # per shell
triage lang                     # listează limbile disponibile
```

Limbi acceptate: English, Español, Français, Deutsch, Italiano,
Português, Nederlands, Polski, Čeština, Svenska, Norsk, Dansk, Suomi,
Română, Magyar, Türkçe. Dacă limba nu este recunoscută, se folosește
engleza ca rezervă.

### Jurnal de evenimente (pentru agenți externi)

Fiecare invocare CLI adaugă o singură linie JSON la un fișier de jurnal,
astfel încât un agent extern să poată face `tail -f` și să parseze
comportamentul Triage:

```bash
tail -f /var/log/triage.log | jq .   # dacă fișierul este deținut de utilizatorul tău
```

Intrări exemplu:

```json
{"ts":"2026-05-16T06:16:18+00:00","event":"add","task_id":"9e8040d267d9","subject":"Investighează interogarea lentă","base_score":10,"tags":[],"deadline":null,"blocked_by":[]}
{"ts":"2026-05-16T06:16:18+00:00","event":"tick","ranked_count":2,"emitted_cron_signals":0,"top":[{"id":"ad2006db3c12","priority":35,"subject":"Rotește certificatul"}],"warnings":[]}
{"ts":"2026-05-16T06:16:19+00:00","event":"poll","source":"github-ci","emitted":1,"warnings":[]}
{"ts":"2026-05-16T06:16:20+00:00","event":"rm","task_id":"9e8040d267d9"}
```

Configurare:

| Mecanism                    | Ce face                                                          |
|-----------------------------|------------------------------------------------------------------|
| opțiunea `--log-file PATH`  | Calea jurnalului per invocare.                                   |
| env `TRIAGE_LOG_FILE=PATH`  | Calea jurnalului per shell.                                      |
| Implicit                    | `/var/log/triage.log`. Revine la `~/.triage/triage.log` dacă `/var/log` nu este scriibil (avertizează o singură dată pe stderr). |
| opțiunea `--no-log`         | Dezactivează jurnalizarea pentru această invocare.               |
| env `TRIAGE_NO_LOG=1`       | Dezactivează jurnalizarea global pentru shell.                   |

Pentru a folosi calea standard `/var/log` fără sudo la fiecare apel:

```bash
sudo touch /var/log/triage.log
sudo chown $(id -un):$(id -gn) /var/log/triage.log
```

Jurnalizarea este un canal lateral strict unidirecțional — erorile
în timpul scrierii sunt înghițite pentru ca comportamentul principal
al CLI-ului să nu fie niciodată întrerupt.

### Teme

```bash
triage theme                    # listează temele disponibile
triage theme --name bbs         # redă rândurile exemplu
triage --theme modern list      # suprascriere temă punctuală
TRIAGE_THEME=mono triage list   # temă per shell
```

| Temă     | Estetică                                                              |
|----------|-----------------------------------------------------------------------|
| `bbs`    | **Implicit.** BBS anii '90: magenta strălucitor, cadru cu linie dublă (`╔═╗`), bare-bloc. |
| `modern` | Paletă subtilă, cadre cu linie simplă (`┌─┐`), bare-punct (`█▒·`).   |
| `mono`   | Fără culoare, doar ASCII (`+-+`, `#=.`) — sigur pentru pipe-uri / terminale simple. |

Culoarea respectă standardele:

- Dezactivată automat când stdout nu este un TTY.
- `NO_COLOR=1` dezactivează culoarea (conform [no-color.org](https://no-color.org/)).
- `FORCE_COLOR=1` activează culoarea pe non-TTY.
- Opțiunea `--no-color` = comutator explicit per invocare.

---

## Proiecte conexe

Triage este o piesă a unui mic ecosistem. Piesele se compun:

| Depozit | Rol |
|---------|-----|
| [**claude_skill-Triage**](https://github.com/CryptoJones/claude_skill-Triage) | Depozitul de skill-uri Claude Code. Livrează astăzi `TaskPriorityReorder` (**suprascriere manuală** — „ridică X în vârf") și va găzdui skill-ul `triage` (**recomandator condus de semnale** — „ce ar trebui să fac în continuare?") într-o versiune viitoare. |
| [**TriageMCP**](https://github.com/CryptoJones/TriageMCP) | **Server MCP** care înfășoară API-ul Triage pentru agenți IA. Opt unelte (`list_tasks`, `add_task`, `tick`, `why_task`, `status`, `remove_task`, `inject_signal`, `get_task`) prin stdio. Pune-l în `~/.claude/mcp.json` și un agent îți poate citi și scrie direct coada de priorități. |
| [**RunPodBoss**](https://github.com/CryptoJones/RunPodBoss) | Apărător al soldului de credit RunPod. Se integrează cu Triage via `extra_notify_command` — când un prag de facturare este depășit, RunPodBoss împinge un semnal manual în Triage astfel încât sarcina „golește pod-urile inactive" plutește în vârful cozii tale. Rețeta de configurare în [`docs/runpodboss-integration.md`](docs/runpodboss-integration.md). |

Toate cele patru împart primitiva Triage (identitate stabilă + prioritate
recalculabilă) și trăiesc pe oglinzi duble (GitHub + Codeberg).

---

## Stare

| Versiune | Funcționalitate                                                    | Stare      |
|----------|--------------------------------------------------------------------|------------|
| v0.1     | schelet, trei reguli, semnal cron-window, CLI                      | lansată    |
| v0.2     | propagare `blocker_transitive` + detectare cicluri                 | lansată    |
| v0.3     | sursă de semnal `github-ci` + regulă `ci_failing` + `triage poll`  | lansată    |
| v0.4     | sistem de teme ANSI în stil BBS + subcomanda `triage theme`        | lansată    |
| v0.5     | sursă de semnal `runpod-cost` + regulă `cost_pressure`             | lansată    |
| v0.6     | scriitor de jurnal de evenimente JSONL pentru agenți externi       | lansată    |
| v0.7     | sursă de semnal `github-pr` pentru PR-uri învechite                | planificată |
| v0.8     | skill `triage` Claude Code (în repo-ul `claude_skill-Triage`)      | planificată |
| v0.9     | modul lung-durată `triage watch` + unitate systemd                 | planificată |

---

## Licență

Apache 2.0. Vezi [LICENSE](LICENSE).

Făcut cu mândrie în Nebraska. Go Big Red! 🌽 https://xkcd.com/2347/
