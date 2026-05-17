<div align="center">

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                    T  R  I  A  G  E                          ║
║                                                              ║
║      meta-planista, który obserwuje własną kolejkę           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Samoświadoma kolejka priorytetowa.** Sygnały dostarczają faktów o
świecie; reguły przekształcają fakty w delty priorytetów; kolejka
przeszereguje się sama przy każdym tyknięciu. Ty wyznaczasz cele —
Triage decyduje o kolejności i mówi ci dokładnie dlaczego.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg?logo=apache)](LICENSE)
[![Stdlib only](https://img.shields.io/badge/deps-stdlib_only-success?logo=python&logoColor=white)](pyproject.toml)
[![Codeberg](https://img.shields.io/badge/Codeberg-CryptoJones%2FTriage-2185D0?logo=codeberg&logoColor=white)](https://codeberg.org/CryptoJones/Triage)
[![GitHub](https://img.shields.io/badge/GitHub-CryptoJones%2FTriage-181717?logo=github&logoColor=white)](https://github.com/CryptoJones/Triage)

**Przeczytaj to w:**
[English](README.md) ·
[Español](README.es.md) ·
[Français](README.fr.md) ·
[Deutsch](README.de.md) ·
[Italiano](README.it.md) ·
[Português](README.pt.md) ·
[Nederlands](README.nl.md) ·
**Polski** ·
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

> Lustrzane kopie na [GitHub](https://github.com/CryptoJones/Triage) i
> [Codeberg](https://codeberg.org/CryptoJones/Triage). Zgłoszenia
> przyjmowane na obu kuźniach; commity trafiają na obie.

---

## Co widzisz

```
╔════════════════════════════════════════════════════════╗
║                  T R I A G E   v0.10.0                  ║
╚════════════════════════════════════════════════════════╝
  ID               PRI  BAR    TEMAT
  ════════════  ══════  ═════  ════════════════════════════════════════
  7cfa440bc639  [ 101]  █████  Naprawić linter         ← blokada auto-podniesiona
  f35d7cea6b7d  [ 100]  █████  Dodać funkcję X         ← zablokowane przez linter
  19c80b807ddd  [  35]  █▒░░░  Wymienić certyfikat     ← presja terminu
  abc123456789  [   2]  ░░░░░  Rutynowe porządki
```

W prawdziwym terminalu baner jest jasnomagenta, priorytety są
kolorowane pasmami (wysoki = żółty, średni = zielony, niski =
przygaszony cyjan), a paski priorytetu wypełniają się proporcjonalnie.
Domyślny motyw `bbs` jest bez wstydu lat 90.

---

## Jak to działa

```
                   ┌─────────────────────┐
   sygnały  ─────► │  Źródła sygnałów    │  (cron-window, github-ci, ...)
                   └──────────┬──────────┘
                              ▼
                   ┌─────────────────────┐
                   │  ~/.triage/state/   │  (append-only JSONL na źródło)
                   └──────────┬──────────┘
                              ▼
   tick     ─────► ┌─────────────────────┐ ─────► przeszeregowana kolejka
                   │  Planista Triage    │        + dziennik audytu zadania
                   └──────────┬──────────┘
                              ▼
                   ┌─────────────────────┐
   zadania  ─────► │      CLI triage     │
                   └─────────────────────┘
```

1. **Źródła sygnałów** dostarczają fakty (`cron-window`, `github-ci`,
   przyszłe `runpod-cost`, `github-pr`...).
2. **Reguły** przekształcają fakty w delty priorytetów
   (`base_score`, `deadline_decay`, `cron_window_active`,
   `ci_failing`, `blocker_transitive`).
3. **Kolejka przeszereguje się** przy każdym `triage tick`.
4. **Każde przeszeregowanie jest wytłumaczalne** — `triage why <id>`
   pokazuje dokładnie, które reguły wniosły jakie delty, więc
   kolejność nigdy nie jest czarną skrzynką.

Zobacz [`DESIGN.md`](DESIGN.md), aby poznać pełną architekturę,
katalog reguł i mapę drogową.

---

## Instalacja

```bash
git clone https://github.com/CryptoJones/Triage      # albo codeberg.org/CryptoJones/Triage
cd Triage
pip install -e .
```

Czysta biblioteka standardowa Pythona. Brak zależności runtime.
Testowane na 3.10 / 3.11 / 3.12.

---

## Użycie

### Zadania

```bash
triage add "Napraw błąd uwierzytelniania" --base-score 10
triage add "Wymień certyfikat staging" --deadline 2026-05-20T00:00:00Z
triage add "Zadanie tylko w dni robocze" --cron-window "* 9-17 * * 1-5"
triage add "Pilnuj CI"             --tag "gh-ci:CryptoJones/Triage@main"
triage add "Czekaj na linter"      --blocked-by <linter-task-id>

triage list                     # bieżąca kolejność priorytetów
triage show <id>                # surowy rekord zadania (JSON)
triage why  <id>                # które reguły wniosły jakie delty
triage rm   <id>                # usuń
```

### Przeszeregowanie + odpytywanie

```bash
triage tick                     # przelicz priorytety; wypisz nową kolejność
triage poll github-ci           # wywołaj sieciowe źródło sygnału
```

`tick` jest tani, lokalny i idempotentny — wywołuj go z crona,
pętli powłoki lub `ScheduleWakeup` Claude Code. `poll` jest dla źródeł
sygnału, które sięgają do sieci (za to płacisz wprost).

### Język

Triage mówi w wielu językach. Ustaw język opcją `--lang` lub zwykłymi
zmiennymi środowiskowymi:

```bash
triage --lang pl list           # jednorazowo
TRIAGE_LANG=pl triage list      # na powłokę
triage lang                     # wypisz dostępne języki
```

Obsługiwane języki: English, Español, Français, Deutsch, Italiano,
Português, Nederlands, Polski, Čeština. Jeśli język nie jest
rozpoznany, jako zapasowy używany jest angielski.

### Dziennik zdarzeń (dla zewnętrznych agentów)

Każde wywołanie CLI dopisuje jedną linię JSON do pliku dziennika,
aby zewnętrzny agent mógł zrobić `tail -f` i parsować zachowanie
Triage:

```bash
tail -f /var/log/triage.log | jq .   # jeśli plik należy do twojego użytkownika
```

Przykładowe wpisy:

```json
{"ts":"2026-05-16T06:16:18+00:00","event":"add","task_id":"9e8040d267d9","subject":"Zbadaj wolne zapytanie","base_score":10,"tags":[],"deadline":null,"blocked_by":[]}
{"ts":"2026-05-16T06:16:18+00:00","event":"tick","ranked_count":2,"emitted_cron_signals":0,"top":[{"id":"ad2006db3c12","priority":35,"subject":"Wymień certyfikat"}],"warnings":[]}
{"ts":"2026-05-16T06:16:19+00:00","event":"poll","source":"github-ci","emitted":1,"warnings":[]}
{"ts":"2026-05-16T06:16:20+00:00","event":"rm","task_id":"9e8040d267d9"}
```

Konfiguracja:

| Mechanizm                   | Co robi                                                          |
|-----------------------------|------------------------------------------------------------------|
| opcja `--log-file PATH`     | Ścieżka dziennika dla wywołania.                                 |
| env `TRIAGE_LOG_FILE=PATH`  | Ścieżka dziennika na powłokę.                                    |
| Domyślnie                   | `/var/log/triage.log`. Spada na `~/.triage/triage.log`, jeśli `/var/log` nie jest zapisywalny (ostrzega raz na stderr). |
| opcja `--no-log`            | Wyłącz logowanie dla tego wywołania.                             |
| env `TRIAGE_NO_LOG=1`       | Wyłącz logowanie globalnie dla powłoki.                          |

Aby używać standardowej ścieżki `/var/log` bez sudo przy każdym wywołaniu:

```bash
sudo touch /var/log/triage.log
sudo chown $(id -un):$(id -gn) /var/log/triage.log
```

Logowanie to ściśle jednokierunkowy kanał boczny — błędy podczas zapisu
są pochłaniane, aby główne zachowanie CLI nigdy nie zostało zakłócone.

### Motywy

```bash
triage theme                    # wypisz dostępne motywy
triage theme --name bbs         # wyrenderuj przykładowe wiersze
triage --theme modern list      # jednorazowa zmiana motywu
TRIAGE_THEME=mono triage list   # motyw na powłokę
```

| Motyw    | Estetyka                                                              |
|----------|-----------------------------------------------------------------------|
| `bbs`    | **Domyślny.** BBS lat 90: jasnomagenta, ramka podwójna (`╔═╗`), paski blokowe. |
| `modern` | Subtelna paleta, ramki pojedyncze (`┌─┐`), paski kropkowe (`█▒·`).   |
| `mono`   | Bez koloru, tylko ASCII (`+-+`, `#=.`) — bezpieczne dla potoków i prostych terminali. |

Kolor podąża za konwencjami:

- Wyłączany automatycznie, gdy stdout nie jest TTY.
- `NO_COLOR=1` wyłącza kolor (zgodnie z [no-color.org](https://no-color.org/)).
- `FORCE_COLOR=1` włącza kolor na nie-TTY.
- Opcja `--no-color` = jawny wyłącznik na wywołanie.

---

## Powiązane projekty

Triage to jedna część małego ekosystemu. Części się składają:

| Repozytorium | Rola |
|--------------|------|
| [**claude_skill-Triage**](https://github.com/CryptoJones/claude_skill-Triage) | Repozytorium skille Claude Code. Dziś dostarcza `TaskPriorityReorder` (**ręczne nadpisanie** — „podbij X na górę") i będzie hostować skill `triage` (**rekomendator sterowany sygnałami** — „co powinienem zrobić dalej?") w przyszłym wydaniu. |
| [**TriageMCP**](https://github.com/CryptoJones/TriageMCP) | **Serwer MCP** opakowujący API Triage dla agentów AI. Osiem narzędzi (`list_tasks`, `add_task`, `tick`, `why_task`, `status`, `remove_task`, `inject_signal`, `get_task`) przez stdio. Wrzuć go do `~/.claude/mcp.json` i agent będzie mógł bezpośrednio czytać i zapisywać twoją kolejkę priorytetów. |
| [**RunPodBoss**](https://github.com/CryptoJones/RunPodBoss) | Bariera ochronna salda kredytowego RunPod. Integruje się z Triage przez `extra_notify_command` — gdy próg billingowy zostanie przekroczony, RunPodBoss wstrzykuje ręczny sygnał do Triage, aby zadanie „opróżnij bezczynne pody" wypłynęło na górę twojej kolejki. Przepis konfiguracji w [`docs/runpodboss-integration.md`](docs/runpodboss-integration.md). |

Wszystkie cztery dzielą prymityw Triage (stabilna tożsamość + przeliczalny
priorytet) i żyją na podwójnych lustrach (GitHub + Codeberg).

---

## Stan

| Wersja | Funkcjonalność                                                       | Stan       |
|--------|----------------------------------------------------------------------|------------|
| v0.1   | szkielet, trzy reguły, sygnał cron-window, CLI                       | wydane     |
| v0.2   | propagacja `blocker_transitive` + wykrywanie cykli                   | wydane     |
| v0.3   | źródło sygnału `github-ci` + reguła `ci_failing` + `triage poll`     | wydane     |
| v0.4   | system motywów ANSI w stylu BBS + podkomenda `triage theme`          | wydane     |
| v0.5   | źródło sygnału `runpod-cost` + reguła `cost_pressure`                | wydane     |
| v0.6   | zapisywacz dziennika zdarzeń JSONL dla zewnętrznych agentów          | wydane     |
| v0.7   | źródło sygnału `github-pr` + reguła `rule_stale_pr`                  | wydane     |
| v0.8   | CLI `triage signal` + reguła `manual_bump` + integracja RunPodBoss   | wydane     |
| v0.8.1 | podsumowanie jednego ekranu `triage status`                          | wydane     |
| v0.9   | podstawa i18n — opcja `--lang` + lokalizacje en/es/fr                | wydane     |
| v0.10  | i18n kompletne — 17 lokalizacji + detektor regresji `triage lang --check` | wydane     |
| —      | skill `triage` Claude Code (w repo `claude_skill-Triage`)            | planowane  |
| —      | tryb długo działający `triage watch` + jednostka systemd             | planowane  |

---

## Licencja

Apache 2.0. Zobacz [LICENSE](LICENSE).

Z dumą wyprodukowane w Nebrasce. Go Big Red! 🌽 https://xkcd.com/2347/
