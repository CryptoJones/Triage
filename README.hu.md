<div align="center">

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                    T  R  I  A  G  E                          ║
║                                                              ║
║      meta-ütemező, amely figyeli a saját sorát               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Öntudatos prioritási sor.** A jelzések tényeket szállítanak a
világról; a szabályok a tényeket prioritási delta-vá alakítják; a
sor minden ticknél átrendezi magát. Te tűzöd ki a célokat — a Triage
dönti el a sorrendet, és pontosan elmondja, miért.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg?logo=apache)](LICENSE)
[![Stdlib only](https://img.shields.io/badge/deps-stdlib_only-success?logo=python&logoColor=white)](pyproject.toml)
[![Codeberg](https://img.shields.io/badge/Codeberg-CryptoJones%2FTriage-2185D0?logo=codeberg&logoColor=white)](https://codeberg.org/CryptoJones/Triage)
[![GitHub](https://img.shields.io/badge/GitHub-CryptoJones%2FTriage-181717?logo=github&logoColor=white)](https://github.com/CryptoJones/Triage)

**Olvasd ezt:**
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
**Magyar** ·
[Türkçe](README.tr.md) ·
[Català](README.ca.md)

</div>

> Tükrözve mind a [GitHubon](https://github.com/CryptoJones/Triage), mind
> a [Codebergen](https://codeberg.org/CryptoJones/Triage). Bármelyik
> kovácsműhelyen nyitott hibajegyek üdvözlendők; a commitok mindkettőre
> kerülnek.

---

## Amit látsz

```
╔════════════════════════════════════════════════════════╗
║                  T R I A G E   v0.10.0                 ║
╚════════════════════════════════════════════════════════╝
  ID               PRI  BAR    TÁRGY
  ════════════  ══════  ═════  ════════════════════════════════════════
  7cfa440bc639  [ 101]  █████  Lintert javítani         ← blokkoló auto-emelve
  f35d7cea6b7d  [ 100]  █████  X funkció hozzáadása     ← linter blokkolja
  19c80b807ddd  [  35]  █▒░░░  Tanúsítvány rotálása     ← határidő-nyomás
  abc123456789  [   2]  ░░░░░  Rutintakarítás
```

Egy igazi terminálban a banner élénk magenta, a prioritások sávokra
színezve (magas = sárga, közepes = zöld, alacsony = halvány ciánkék),
és a prioritás-oszlopok arányosan töltődnek. Az alapértelmezett `bbs`
téma szégyentelenül 1990-es évek.

---

## Hogyan működik

```
                   ┌─────────────────────┐
   jelzések ─────► │  Jelzésforrások     │  (cron-window, github-ci, ...)
                   └──────────┬──────────┘
                              ▼
                   ┌─────────────────────┐
                   │  ~/.triage/state/   │  (csak-hozzáfűző JSONL forrásonként)
                   └──────────┬──────────┘
                              ▼
   tick     ─────► ┌─────────────────────┐ ─────► átrendezett sor
                   │   Triage-ütemező    │        + feladatonkénti audit-napló
                   └──────────┬──────────┘
                              ▼
                   ┌─────────────────────┐
   feladatok ────► │      triage CLI     │
                   └─────────────────────┘
```

1. **A jelzésforrások** tényeket szállítanak (`cron-window`, `github-ci`,
   jövőbeli `runpod-cost`, `github-pr`...).
2. **A szabályok** a tényeket prioritási delta-vá alakítják
   (`base_score`, `deadline_decay`, `cron_window_active`,
   `ci_failing`, `blocker_transitive`).
3. **A sor átrendeződik** minden `triage tick`-nél.
4. **Minden átrendezés magyarázható** — a `triage why <id>` pontosan
   megmutatja, melyik szabály mekkora deltával járult hozzá, így a
   sorrend soha nem fekete doboz.

Lásd a [`DESIGN.md`](DESIGN.md)-ben a teljes architektúrát, a
szabálykatalógust és az ütemtervet.

---

## Telepítés

```bash
git clone https://github.com/CryptoJones/Triage      # vagy codeberg.org/CryptoJones/Triage
cd Triage
pip install -e .
```

Tiszta Python sztenderd-könyvtár. Nincsenek futásidejű függőségek.
Tesztelve 3.10 / 3.11 / 3.12 verziókkal.

---

## Használat

### Feladatok

```bash
triage add "Auth-bug javítása" --base-score 10
triage add "Staging tanúsítvány rotálása" --deadline 2026-05-20T00:00:00Z
triage add "Hétköznapi feladat"  --cron-window "* 9-17 * * 1-5"
triage add "CI figyelése"        --tag "gh-ci:CryptoJones/Triage@main"
triage add "Várni a linterre"    --blocked-by <linter-task-id>

triage list                     # jelenlegi prioritási sorrend
triage show <id>                # nyers feladatrekord (JSON)
triage why  <id>                # melyik szabály mekkora deltával járult hozzá
triage rm   <id>                # eltávolítás
```

### Átrendezés + lekérdezés

```bash
triage tick                     # prioritások újraszámítása; új sorrend kiírása
triage poll github-ci           # hálózathoz kötött jelzésforrás meghívása
```

A `tick` olcsó, lokális és idempotens — hívd cronból, shell-ciklusból
vagy a Claude Code `ScheduleWakeup`-jából. A `poll` olyan
jelzésforrásokhoz való, amelyek a hálózatot érintik (azokért
kifejezetten fizetsz).

### Nyelv

A Triage több nyelvet beszél. Állítsd be a nyelvet a `--lang`
kapcsolóval vagy a szokásos környezeti változókkal:

```bash
triage --lang hu list           # egyszeri
TRIAGE_LANG=hu triage list      # shellenként
triage lang                     # elérhető nyelvek listázása
```

Támogatott nyelvek: English, Español, Français, Deutsch, Italiano,
Português, Nederlands, Polski, Čeština, Svenska, Norsk, Dansk, Suomi,
Română, Magyar, Türkçe, Català. Ha a nyelvet nem ismeri fel, az angol
a tartalék.

### Eseménynapló (külső ágenseknek)

Minden CLI-hívás egyetlen JSON-sort fűz a naplófájlhoz, így egy külső
ágens `tail -f`-fel követheti és elemezheti a Triage viselkedését:

```bash
tail -f /var/log/triage.log | jq .   # ha a fájl a saját felhasználódé
```

Példa bejegyzések:

```json
{"ts":"2026-05-16T06:16:18+00:00","event":"add","task_id":"9e8040d267d9","subject":"Lassú lekérdezés vizsgálata","base_score":10,"tags":[],"deadline":null,"blocked_by":[]}
{"ts":"2026-05-16T06:16:18+00:00","event":"tick","ranked_count":2,"emitted_cron_signals":0,"top":[{"id":"ad2006db3c12","priority":35,"subject":"Tanúsítvány rotálása"}],"warnings":[]}
{"ts":"2026-05-16T06:16:19+00:00","event":"poll","source":"github-ci","emitted":1,"warnings":[]}
{"ts":"2026-05-16T06:16:20+00:00","event":"rm","task_id":"9e8040d267d9"}
```

Konfiguráció:

| Mechanizmus                | Mit csinál                                                       |
|----------------------------|------------------------------------------------------------------|
| `--log-file PATH` kapcsoló | Naplóútvonal hívásonként.                                        |
| env `TRIAGE_LOG_FILE=PATH` | Naplóútvonal shellenként.                                        |
| Alapértelmezett            | `/var/log/triage.log`. Visszaesik `~/.triage/triage.log`-ra, ha a `/var/log` nem írható (egyszer figyelmeztet stderre). |
| `--no-log` kapcsoló        | Naplózás kikapcsolása ehhez a híváshoz.                          |
| env `TRIAGE_NO_LOG=1`      | Naplózás globális kikapcsolása a shellben.                       |

A `/var/log` szabványos útvonal használatához sudo nélkül minden híváskor:

```bash
sudo touch /var/log/triage.log
sudo chown $(id -un):$(id -gn) /var/log/triage.log
```

A naplózás szigorúan egyirányú oldalcsatorna — az írás közbeni hibákat
elnyeli, hogy a CLI elsődleges viselkedése soha ne sérüljön.

### Témák

```bash
triage theme                    # elérhető témák listázása
triage theme --name bbs         # mintasorok renderelése
triage --theme modern list      # egyszeri témafelülírás
TRIAGE_THEME=mono triage list   # téma shellenként
```

| Téma     | Esztétika                                                            |
|----------|----------------------------------------------------------------------|
| `bbs`    | **Alapértelmezett.** 1990-es BBS: élénk magenta, dupla-vonalú keret (`╔═╗`), blokk-sávok. |
| `modern` | Visszafogott paletta, egyvonalú keretek (`┌─┐`), pont-sávok (`█▒·`). |
| `mono`   | Nincs szín, csak ASCII (`+-+`, `#=.`) — biztonságos csövekhez / buta terminálokhoz. |

A szín a szabványokat követi:

- Automatikusan kikapcsol, ha a stdout nem TTY.
- `NO_COLOR=1` kikapcsolja a színt ([no-color.org](https://no-color.org/) szerint).
- `FORCE_COLOR=1` bekapcsolja a színt nem-TTY-n.
- A `--no-color` kapcsoló = kifejezett vészkapcsoló hívásonként.

---

## Kapcsolódó projektek

A Triage egy darabja egy kis ökoszisztémának. A darabok együttműködnek:

| Repozitórium | Szerep |
|--------------|--------|
| [**claude_skill-Triage**](https://github.com/CryptoJones/claude_skill-Triage) | A Claude Code skill-repozitóriuma. Ma a `TaskPriorityReorder`-t szállítja (**kézi felülírás** — „emeld X-et a tetejére"), és egy jövőbeli kiadásban fogja otthont adni a `triage` skillnek (**jelzés-vezérelt ajánló** — „mit csináljak most?"). |
| [**TriageMCP**](https://github.com/CryptoJones/TriageMCP) | **MCP-szerver**, amely a Triage API-ját csomagolja AI-ágenseknek. Nyolc eszköz (`list_tasks`, `add_task`, `tick`, `why_task`, `status`, `remove_task`, `inject_signal`, `get_task`) stdio-n keresztül. Dobd be a `~/.claude/mcp.json`-ba, és egy ágens közvetlenül olvashatja és írhatja a prioritási sorodat. |
| [**RunPodBoss**](https://github.com/CryptoJones/RunPodBoss) | A RunPod kreditegyenlegének védőkorlátja. Integrálódik a Triage-zsel az `extra_notify_command`-en keresztül — amikor egy számlázási küszöb átlépésre kerül, a RunPodBoss kézi jelzést tol a Triage-be, hogy a „tétlen pod-ok kiürítése" feladat a sor tetejére kerüljön. Konfigurációs recept itt: [`docs/runpodboss-integration.md`](docs/runpodboss-integration.md). |

Mind a négy osztozik a Triage primitívén (stabil identitás + újraszámolható
prioritás), és kettős tükörben él (GitHub + Codeberg).

---

## Állapot

| Verzió | Funkció                                                            | Állapot   |
|--------|--------------------------------------------------------------------|-----------|
| v0.1   | váz, három szabály, cron-window-jelzés, CLI                        | kiadva    |
| v0.2   | `blocker_transitive`-terjedés + ciklusészlelés                     | kiadva    |
| v0.3   | `github-ci`-jelzésforrás + `ci_failing`-szabály + `triage poll`    | kiadva    |
| v0.4   | BBS-stílusú ANSI-témarendszer + `triage theme` alparancs           | kiadva    |
| v0.5   | `runpod-cost`-jelzésforrás + `cost_pressure`-szabály               | kiadva    |
| v0.6   | JSONL eseménynaplóíró külső ágenseknek                             | kiadva    |
| v0.7   | `github-pr` jelzésforrás + szabály `rule_stale_pr`                 | kiadva    |
| v0.8   | `triage signal` CLI + szabály `manual_bump` + RunPodBoss-integráció | kiadva    |
| v0.8.1 | `triage status` egyképernyős áttekintés                            | kiadva    |
| v0.9   | i18n alap — `--lang` kapcsoló + en/es/fr nyelvek                   | kiadva    |
| v0.10  | i18n teljes — 17 nyelv + regresszió-detektor `triage lang --check` | kiadva    |
| —      | Claude Code `triage`-skill (a `claude_skill-Triage` repóban)       | tervezett |
| —      | hosszan futó `triage watch`-mód + systemd-egység                   | tervezett |

---

## Licenc

Apache 2.0. Lásd [LICENSE](LICENSE).

Büszkén Nebraskában készült. Go Big Red! 🌽 https://xkcd.com/2347/
