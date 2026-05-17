<div align="center">

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                    T  R  I  A  G  E                          ║
║                                                              ║
║      meta-aikataulutin, joka tarkkailee omaa jonoaan         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Itsetietoinen prioriteettijono.** Signaalit tuovat faktoja maailmasta;
säännöt muuntavat faktat prioriteettidelttoiksi; jono järjestää itsensä
uudelleen jokaisella tikityksellä. Sinä asetat tavoitteet — Triage
päättää järjestyksen ja kertoo tarkasti miksi.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg?logo=apache)](LICENSE)
[![Stdlib only](https://img.shields.io/badge/deps-stdlib_only-success?logo=python&logoColor=white)](pyproject.toml)
[![Codeberg](https://img.shields.io/badge/Codeberg-CryptoJones%2FTriage-2185D0?logo=codeberg&logoColor=white)](https://codeberg.org/CryptoJones/Triage)
[![GitHub](https://img.shields.io/badge/GitHub-CryptoJones%2FTriage-181717?logo=github&logoColor=white)](https://github.com/CryptoJones/Triage)

**Lue tämä kielellä:**
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
**Suomi** ·
[Română](README.ro.md) ·
[Magyar](README.hu.md) ·
[Türkçe](README.tr.md) ·
[Català](README.ca.md)

</div>

> Peilattu sekä [GitHubissa](https://github.com/CryptoJones/Triage)
> että [Codebergissä](https://codeberg.org/CryptoJones/Triage).
> Issueja otetaan vastaan kummassakin; commitit laskeutuvat molempiin.

---

## Mitä näet

```
╔════════════════════════════════════════════════════════╗
║                  T R I A G E   v0.9.0                  ║
╚════════════════════════════════════════════════════════╝
  ID               PRI  BAR    AIHE
  ════════════  ══════  ═════  ════════════════════════════════════════
  7cfa440bc639  [ 101]  █████  Korjaa linter         ← estäjä auto-nostettu
  f35d7cea6b7d  [ 100]  █████  Lisää ominaisuus X    ← linter estää
  19c80b807ddd  [  35]  █▒░░░  Kierrätä varmenne     ← määräaikapaine
  abc123456789  [   2]  ░░░░░  Rutiininomainen siivous
```

Oikeassa päätteessä banneri on kirkas magenta, prioriteetit ovat
värialueittain (korkea = keltainen, keskimmäinen = vihreä, matala =
himmennetty syaani), ja prioriteettipalkit täyttyvät suhteellisesti.
Oletusteema `bbs` on häpeämättömästi 90-lukua.

---

## Miten se toimii

```
                   ┌─────────────────────┐
   signaalit ────► │  Signaalilähteet    │  (cron-window, github-ci, ...)
                   └──────────┬──────────┘
                              ▼
                   ┌─────────────────────┐
                   │  ~/.triage/state/   │  (append-only JSONL per lähde)
                   └──────────┬──────────┘
                              ▼
   tick     ─────► ┌─────────────────────┐ ─────► uudelleenjärjestetty jono
                   │ Triage-aikataulutin │        + tarkastusloki per tehtävä
                   └──────────┬──────────┘
                              ▼
                   ┌─────────────────────┐
   tehtävät ─────► │      triage CLI     │
                   └─────────────────────┘
```

1. **Signaalilähteet** tuovat faktoja (`cron-window`, `github-ci`,
   tulevat `runpod-cost`, `github-pr`...).
2. **Säännöt** muuntavat faktat prioriteettidelttoiksi
   (`base_score`, `deadline_decay`, `cron_window_active`,
   `ci_failing`, `blocker_transitive`).
3. **Jono järjestetään uudelleen** jokaisella `triage tick` -komennolla.
4. **Jokainen uudelleenjärjestely on selitettävissä** — `triage why <id>`
   näyttää tarkalleen, mitkä säännöt myötävaikuttivat ja millä delttoilla,
   joten järjestys ei koskaan ole musta laatikko.

Katso [`DESIGN.md`](DESIGN.md) saadaksesi täyden arkkitehtuurin,
sääntöluettelon ja tiekartan.

---

## Asennus

```bash
git clone https://github.com/CryptoJones/Triage      # tai codeberg.org/CryptoJones/Triage
cd Triage
pip install -e .
```

Puhdas Pythonin standardikirjasto. Ei ajonaikaisia riippuvuuksia.
Testattu versioilla 3.10 / 3.11 / 3.12.

---

## Käyttö

### Tehtävät

```bash
triage add "Korjaa autentikointivika" --base-score 10
triage add "Kierrätä staging-varmenne" --deadline 2026-05-20T00:00:00Z
triage add "Arkipäivä-puuha"     --cron-window "* 9-17 * * 1-5"
triage add "Vahdi CI:tä"         --tag "gh-ci:CryptoJones/Triage@main"
triage add "Odota linteriä"      --blocked-by <linter-task-id>

triage list                     # nykyinen prioriteettijärjestys
triage show <id>                # raaka tehtävätietue (JSON)
triage why  <id>                # mitkä säännöt myötävaikuttivat millä delttoilla
triage rm   <id>                # poista
```

### Uudelleenjärjestys + kysely

```bash
triage tick                     # laske prioriteetit uudelleen; tulosta uusi järjestys
triage poll github-ci           # kutsu verkkoon sitoutunut signaalilähde
```

`tick` on halpa, paikallinen ja idempotentti — kutsu sitä cronista,
shell-silmukasta tai Claude Coden `ScheduleWakeup`-toiminnosta. `poll`
on signaalilähteille, jotka koskettavat verkkoa (niistä maksat
nimenomaisesti).

### Kieli

Triage puhuu useita kieliä. Aseta kieli valitsimella `--lang` tai
tavallisilla ympäristömuuttujilla:

```bash
triage --lang fi list           # kertakäyttöinen
TRIAGE_LANG=fi triage list      # per shell
triage lang                     # listaa käytettävissä olevat kielet
```

Tuetut kielet: English, Español, Français, Deutsch, Italiano,
Português, Nederlands, Polski, Čeština, Svenska, Norsk, Dansk, Suomi.
Jos kieltä ei tunnisteta, käytetään englantia varavaihtoehtona.

### Tapahtumaloki (ulkoisille agenteille)

Jokainen CLI-kutsu lisää yhden JSON-rivin lokitiedostoon, jotta
ulkoinen agentti voi tehdä `tail -f`:n ja jäsentää Triagen käyttäytymistä:

```bash
tail -f /var/log/triage.log | jq .   # jos tiedosto on käyttäjäsi omistuksessa
```

Esimerkkimerkinnät:

```json
{"ts":"2026-05-16T06:16:18+00:00","event":"add","task_id":"9e8040d267d9","subject":"Tutki hidas kysely","base_score":10,"tags":[],"deadline":null,"blocked_by":[]}
{"ts":"2026-05-16T06:16:18+00:00","event":"tick","ranked_count":2,"emitted_cron_signals":0,"top":[{"id":"ad2006db3c12","priority":35,"subject":"Kierrätä varmenne"}],"warnings":[]}
{"ts":"2026-05-16T06:16:19+00:00","event":"poll","source":"github-ci","emitted":1,"warnings":[]}
{"ts":"2026-05-16T06:16:20+00:00","event":"rm","task_id":"9e8040d267d9"}
```

Konfiguraatio:

| Mekanismi                  | Mitä se tekee                                                    |
|----------------------------|------------------------------------------------------------------|
| valitsin `--log-file PATH` | Lokin polku per kutsu.                                           |
| env `TRIAGE_LOG_FILE=PATH` | Lokin polku per shell.                                           |
| Oletus                     | `/var/log/triage.log`. Palautuu polkuun `~/.triage/triage.log`, jos `/var/log` ei ole kirjoituskelpoinen (varoittaa kerran stderrissä). |
| valitsin `--no-log`        | Poistaa lokituksen tämän kutsun ajaksi.                          |
| env `TRIAGE_NO_LOG=1`      | Poistaa lokituksen globaalisti shellistä.                        |

Käyttääksesi standardipolkua `/var/log` ilman sudoa joka kutsulla:

```bash
sudo touch /var/log/triage.log
sudo chown $(id -un):$(id -gn) /var/log/triage.log
```

Lokitus on tiukasti yksisuuntainen sivukanava — kirjoituksen aikaiset
virheet niellään, jotta CLI:n ensisijainen käyttäytyminen ei koskaan
häiriinny.

### Teemat

```bash
triage theme                    # listaa käytettävissä olevat teemat
triage theme --name bbs         # näytä esimerkkirivit
triage --theme modern list      # kertakäyttöinen teeman ohitus
TRIAGE_THEME=mono triage list   # teema per shell
```

| Teema    | Estetiikka                                                          |
|----------|---------------------------------------------------------------------|
| `bbs`    | **Oletus.** 90-luvun BBS: kirkas magenta, kaksoisviivainen kehys (`╔═╗`), lohkopalkit. |
| `modern` | Hillitty paletti, yksiviivaiset kehykset (`┌─┐`), pistepalkit (`█▒·`). |
| `mono`   | Ei väriä, vain ASCII (`+-+`, `#=.`) — turvallinen putkille ja tyhmille päätteille. |

Väri noudattaa standardeja:

- Automaattisesti pois käytöstä, kun stdout ei ole TTY.
- `NO_COLOR=1` poistaa värin (vrt. [no-color.org](https://no-color.org/)).
- `FORCE_COLOR=1` ottaa värin käyttöön ei-TTY:llä.
- Valitsin `--no-color` = nimenomainen hätäkytkin per kutsu.

---

## Liittyvät projektit

Triage on yksi pala pientä ekosysteemiä. Palaset sointuvat:

| Repositorio | Rooli |
|-------------|-------|
| [**claude_skill-Triage**](https://github.com/CryptoJones/claude_skill-Triage) | Claude Coden skill-repositorio. Toimittaa tänään `TaskPriorityReorder`-skillin (**manuaalinen ohitus** — "nosta X huipulle") ja tulee isännöimään `triage`-skilliä (**signaaliohjattu suosittelija** — "mitä minun pitäisi tehdä seuraavaksi?") tulevassa julkaisussa. |
| [**TriageMCP**](https://github.com/CryptoJones/TriageMCP) | **MCP-palvelin**, joka kääräisee Triagen API:n AI-agentteja varten. Kahdeksan työkalua (`list_tasks`, `add_task`, `tick`, `why_task`, `status`, `remove_task`, `inject_signal`, `get_task`) stdion yli. Pudota se tiedostoon `~/.claude/mcp.json`, ja agentti voi lukea ja kirjoittaa prioriteettijonoasi suoraan. |
| [**RunPodBoss**](https://github.com/CryptoJones/RunPodBoss) | RunPodin saldon suojakaari. Integroituu Triageen `extra_notify_command`-kautta — kun laskutuskynnys ylittyy, RunPodBoss työntää manuaalisen signaalin Triageen, jotta tehtävä "tyhjennä joutilaat podit" nousee jonosi kärkeen. Konfigurointiresepti tiedostossa [`docs/runpodboss-integration.md`](docs/runpodboss-integration.md). |

Kaikki neljä jakavat Triagen primitiivin (vakaa identiteetti +
uudelleenlaskettava prioriteetti) ja elävät kaksoispeileissä
(GitHub + Codeberg).

---

## Tila

| Versio | Ominaisuus                                                        | Tila      |
|--------|-------------------------------------------------------------------|-----------|
| v0.1   | runko, kolme sääntöä, cron-window-signaali, CLI                   | julkaistu |
| v0.2   | `blocker_transitive`-propagaatio + syklin havaitseminen           | julkaistu |
| v0.3   | `github-ci`-signaalilähde + `ci_failing`-sääntö + `triage poll`   | julkaistu |
| v0.4   | BBS-tyylinen ANSI-teemajärjestelmä + alikomento `triage theme`    | julkaistu |
| v0.5   | `runpod-cost`-signaalilähde + `cost_pressure`-sääntö              | julkaistu |
| v0.6   | JSONL-tapahtumalokin kirjoittaja ulkoisille agenteille            | julkaistu |
| v0.7   | `github-pr`-signaalilähde vanhentuneille PR:ille                  | suunniteltu |
| v0.8   | Claude Coden `triage`-skill (`claude_skill-Triage`-repossa)       | suunniteltu |
| v0.9   | `triage watch`-pitkäkestoinen tila + systemd-yksikkö              | suunniteltu |

---

## Lisenssi

Apache 2.0. Katso [LICENSE](LICENSE).

Ylpeästi valmistettu Nebraskassa. Go Big Red! 🌽 https://xkcd.com/2347/
