<div align="center">

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                    T  R  I  A  G  E                          ║
║                                                              ║
║      meta-plánovač, který sleduje vlastní frontu             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Sebevědomá prioritní fronta.** Signály přinášejí fakta o světě;
pravidla převádějí fakta na priority delty; fronta se přeskupuje
sama při každém tiknutí. Ty stanovuješ cíle — Triage rozhodne o
pořadí a řekne ti přesně proč.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg?logo=apache)](LICENSE)
[![Stdlib only](https://img.shields.io/badge/deps-stdlib_only-success?logo=python&logoColor=white)](pyproject.toml)
[![Codeberg](https://img.shields.io/badge/Codeberg-CryptoJones%2FTriage-2185D0?logo=codeberg&logoColor=white)](https://codeberg.org/CryptoJones/Triage)
[![GitHub](https://img.shields.io/badge/GitHub-CryptoJones%2FTriage-181717?logo=github&logoColor=white)](https://github.com/CryptoJones/Triage)

**Přečti si to v:**
[English](README.md) ·
[Español](README.es.md) ·
[Français](README.fr.md) ·
[Deutsch](README.de.md) ·
[Italiano](README.it.md) ·
[Português](README.pt.md) ·
[Nederlands](README.nl.md) ·
[Polski](README.pl.md) ·
**Čeština**

</div>

> Zrcadleno na [GitHub](https://github.com/CryptoJones/Triage) i
> [Codeberg](https://codeberg.org/CryptoJones/Triage). Issues na obou
> kovárnách jsou vítány; commity přistávají na obou.

---

## Co vidíš

```
╔════════════════════════════════════════════════════════╗
║                  T R I A G E   v0.9.0                  ║
╚════════════════════════════════════════════════════════╝
  ID               PRI  BAR    PŘEDMĚT
  ════════════  ══════  ═════  ════════════════════════════════════════
  7cfa440bc639  [ 101]  █████  Opravit linter         ← blokátor automaticky povýšen
  f35d7cea6b7d  [ 100]  █████  Přidat funkci X        ← blokováno linterem
  19c80b807ddd  [  35]  █▒░░░  Obnovit certifikát     ← tlak termínu
  abc123456789  [   2]  ░░░░░  Rutinní úklid
```

V reálném terminálu je banner jasně purpurový, priority jsou barevně
rozdělené do pásem (vysoká = žlutá, střední = zelená, nízká = tlumená
azurová) a sloupce priority se vyplňují proporcionálně. Výchozí téma
`bbs` je beze studu z 90. let.

---

## Jak to funguje

```
                   ┌─────────────────────┐
   signály  ─────► │   Zdroje signálů    │  (cron-window, github-ci, ...)
                   └──────────┬──────────┘
                              ▼
                   ┌─────────────────────┐
                   │  ~/.triage/state/   │  (append-only JSONL na zdroj)
                   └──────────┬──────────┘
                              ▼
   tick     ─────► ┌─────────────────────┐ ─────► přeskupená fronta
                   │   Plánovač Triage   │        + auditní záznam úkolů
                   └──────────┬──────────┘
                              ▼
                   ┌─────────────────────┐
   úkoly    ─────► │      CLI triage     │
                   └─────────────────────┘
```

1. **Zdroje signálů** přinášejí fakta (`cron-window`, `github-ci`,
   budoucí `runpod-cost`, `github-pr`...).
2. **Pravidla** převádějí fakta na priority delty
   (`base_score`, `deadline_decay`, `cron_window_active`,
   `ci_failing`, `blocker_transitive`).
3. **Fronta se přeskupuje** při každém `triage tick`.
4. **Každé přeskupení je vysvětlitelné** — `triage why <id>` ukazuje
   přesně, která pravidla přispěla jakými deltami, takže pořadí
   nikdy není černá skříňka.

Viz [`DESIGN.md`](DESIGN.md) pro úplnou architekturu, katalog pravidel
a plán cesty.

---

## Instalace

```bash
git clone https://github.com/CryptoJones/Triage      # nebo codeberg.org/CryptoJones/Triage
cd Triage
pip install -e .
```

Čistá standardní knihovna Pythonu. Žádné runtime závislosti.
Testováno na 3.10 / 3.11 / 3.12.

---

## Použití

### Úkoly

```bash
triage add "Opravit chybu autentizace" --base-score 10
triage add "Obnovit staging certifikát" --deadline 2026-05-20T00:00:00Z
triage add "Úkol jen ve všední dny" --cron-window "* 9-17 * * 1-5"
triage add "Hlídat CI"          --tag "gh-ci:CryptoJones/Triage@main"
triage add "Čekat na linter"    --blocked-by <linter-task-id>

triage list                     # aktuální pořadí priorit
triage show <id>                # surový záznam úkolu (JSON)
triage why  <id>                # která pravidla přispěla jakými deltami
triage rm   <id>                # odstranit
```

### Přeskupení + dotazování

```bash
triage tick                     # přepočítat priority; vypsat nové pořadí
triage poll github-ci           # vyvolat síťově vázaný zdroj signálu
```

`tick` je levný, lokální a idempotentní — volej ho z cronu, smyčky
shellu nebo `ScheduleWakeup` Claude Code. `poll` je pro zdroje signálu,
které sahají na síť (za ty platíš výslovně).

### Jazyk

Triage mluví více jazyky. Nastav jazyk pomocí volby `--lang` nebo
obvyklých proměnných prostředí:

```bash
triage --lang cs list           # jednorázově
TRIAGE_LANG=cs triage list      # na shell
triage lang                     # vypíše dostupné jazyky
```

Podporované jazyky: English, Español, Français, Deutsch, Italiano,
Português, Nederlands, Polski, Čeština. Pokud jazyk není rozpoznán,
použije se jako záloha angličtina.

### Záznam událostí (pro externí agenty)

Každé vyvolání CLI připíše jeden řádek JSON do souboru se záznamem,
aby externí agent mohl `tail -f` a parsovat chování Triage:

```bash
tail -f /var/log/triage.log | jq .   # pokud soubor patří tvému uživateli
```

Ukázkové záznamy:

```json
{"ts":"2026-05-16T06:16:18+00:00","event":"add","task_id":"9e8040d267d9","subject":"Prošetřit pomalý dotaz","base_score":10,"tags":[],"deadline":null,"blocked_by":[]}
{"ts":"2026-05-16T06:16:18+00:00","event":"tick","ranked_count":2,"emitted_cron_signals":0,"top":[{"id":"ad2006db3c12","priority":35,"subject":"Obnovit certifikát"}],"warnings":[]}
{"ts":"2026-05-16T06:16:19+00:00","event":"poll","source":"github-ci","emitted":1,"warnings":[]}
{"ts":"2026-05-16T06:16:20+00:00","event":"rm","task_id":"9e8040d267d9"}
```

Konfigurace:

| Mechanismus                | Co dělá                                                          |
|----------------------------|------------------------------------------------------------------|
| volba `--log-file PATH`    | Cesta záznamu pro vyvolání.                                      |
| env `TRIAGE_LOG_FILE=PATH` | Cesta záznamu na shell.                                          |
| Výchozí                    | `/var/log/triage.log`. Spadne zpět na `~/.triage/triage.log`, pokud není `/var/log` zapisovatelný (jednou varuje na stderr). |
| volba `--no-log`           | Vypne záznam pro toto vyvolání.                                  |
| env `TRIAGE_NO_LOG=1`      | Vypne záznam globálně pro shell.                                 |

Pro použití standardní cesty `/var/log` bez sudo při každém volání:

```bash
sudo touch /var/log/triage.log
sudo chown $(id -un):$(id -gn) /var/log/triage.log
```

Záznam je striktně jednosměrný postranní kanál — chyby během zápisu
jsou spolknuty, aby hlavní chování CLI nikdy nebylo narušeno.

### Témata

```bash
triage theme                    # vypíše dostupná témata
triage theme --name bbs         # vykreslí ukázkové řádky
triage --theme modern list      # jednorázová změna tématu
TRIAGE_THEME=mono triage list   # téma na shell
```

| Téma     | Estetika                                                              |
|----------|-----------------------------------------------------------------------|
| `bbs`    | **Výchozí.** BBS 90. let: jasně purpurová, dvojitý rámeček (`╔═╗`), blokové sloupce. |
| `modern` | Decentní paleta, jednoduché rámečky (`┌─┐`), tečkované sloupce (`█▒·`). |
| `mono`   | Bez barvy, jen ASCII (`+-+`, `#=.`) — bezpečné pro roury / hloupé terminály. |

Barva se řídí konvencemi:

- Automaticky vypnuta, když stdout není TTY.
- `NO_COLOR=1` vypíná barvu (podle [no-color.org](https://no-color.org/)).
- `FORCE_COLOR=1` zapíná barvu na ne-TTY.
- Volba `--no-color` = výslovný vypínač na vyvolání.

---

## Související projekty

Triage je jeden kus malého ekosystému. Kusy do sebe zapadají:

| Repozitář | Role |
|-----------|------|
| [**claude_skill-Triage**](https://github.com/CryptoJones/claude_skill-Triage) | Repozitář skille Claude Code. Dnes dodává `TaskPriorityReorder` (**ruční přepsání** — „posuň X nahoru") a v budoucím vydání bude hostit skill `triage` (**doporučovač řízený signály** — „co bych měl dělat dál?"). |
| [**TriageMCP**](https://github.com/CryptoJones/TriageMCP) | **MCP server** obalující API Triage pro AI agenty. Osm nástrojů (`list_tasks`, `add_task`, `tick`, `why_task`, `status`, `remove_task`, `inject_signal`, `get_task`) přes stdio. Vlož ho do `~/.claude/mcp.json` a agent bude moci přímo číst a zapisovat tvou prioritní frontu. |
| [**RunPodBoss**](https://github.com/CryptoJones/RunPodBoss) | Ochranná bariéra zůstatku kreditu RunPod. Integruje se s Triage přes `extra_notify_command` — když je překročena fakturační hranice, RunPodBoss vstříkne ruční signál do Triage, takže úkol „vyprázdnit nečinné pody" vypluje na vrchol tvé fronty. Recept konfigurace v [`docs/runpodboss-integration.md`](docs/runpodboss-integration.md). |

Všechny čtyři sdílejí primitivu Triage (stabilní identita + přepočitatelná
priorita) a žijí na dvojitých zrcadlech (GitHub + Codeberg).

---

## Stav

| Verze | Funkce                                                              | Stav    |
|-------|---------------------------------------------------------------------|---------|
| v0.1  | kostra, tři pravidla, signál cron-window, CLI                       | vydáno  |
| v0.2  | propagace `blocker_transitive` + detekce cyklů                      | vydáno  |
| v0.3  | zdroj signálu `github-ci` + pravidlo `ci_failing` + `triage poll`   | vydáno  |
| v0.4  | systém ANSI témat ve stylu BBS + podpříkaz `triage theme`           | vydáno  |
| v0.5  | zdroj signálu `runpod-cost` + pravidlo `cost_pressure`              | vydáno  |
| v0.6  | zapisovač záznamu událostí JSONL pro externí agenty                 | vydáno  |
| v0.7  | zdroj signálu `github-pr` pro zastaralé PR                          | plánováno |
| v0.8  | skill `triage` Claude Code (v repu `claude_skill-Triage`)           | plánováno |
| v0.9  | dlouho běžící režim `triage watch` + jednotka systemd               | plánováno |

---

## Licence

Apache 2.0. Viz [LICENSE](LICENSE).

Hrdě vyrobeno v Nebrasce. Go Big Red! 🌽 https://xkcd.com/2347/
