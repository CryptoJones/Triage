<div align="center">

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                    T  R  I  A  G  E                          ║
║                                                              ║
║      kendi kuyruğunu izleyen meta-zamanlayıcı                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Öz farkındalığa sahip bir öncelik kuyruğu.** Sinyaller dünyaya dair
gerçekleri taşır; kurallar gerçekleri öncelik delta'larına dönüştürür;
kuyruk her tick'te kendisini yeniden sıralar. Hedefleri sen koyarsın
— Triage sırayı belirler ve sana tam olarak nedenini söyler.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg?logo=apache)](LICENSE)
[![Stdlib only](https://img.shields.io/badge/deps-stdlib_only-success?logo=python&logoColor=white)](pyproject.toml)
[![Codeberg](https://img.shields.io/badge/Codeberg-CryptoJones%2FTriage-2185D0?logo=codeberg&logoColor=white)](https://codeberg.org/CryptoJones/Triage)
[![GitHub](https://img.shields.io/badge/GitHub-CryptoJones%2FTriage-181717?logo=github&logoColor=white)](https://github.com/CryptoJones/Triage)

**Bunu şu dilde oku:**
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
**Türkçe**

</div>

> Hem [GitHub](https://github.com/CryptoJones/Triage) hem de
> [Codeberg](https://codeberg.org/CryptoJones/Triage) üzerinde aynalandı.
> Her iki demirhanedeki issue'lar memnuniyetle karşılanır; commit'ler
> her ikisine de iner.

---

## Ne görürsün

```
╔════════════════════════════════════════════════════════╗
║                  T R I A G E   v0.9.0                  ║
╚════════════════════════════════════════════════════════╝
  ID               PRI  BAR    KONU
  ════════════  ══════  ═════  ════════════════════════════════════════
  7cfa440bc639  [ 101]  █████  Linter'ı düzelt        ← engelleyici otomatik yükseltildi
  f35d7cea6b7d  [ 100]  █████  X özelliği ekle        ← linter tarafından engellendi
  19c80b807ddd  [  35]  █▒░░░  Sertifikayı döndür     ← son tarih baskısı
  abc123456789  [   2]  ░░░░░  Rutin temizlik
```

Gerçek bir terminalde banner parlak magentadır, öncelikler bantlarla
renklendirilmiştir (yüksek = sarı, orta = yeşil, düşük = solgun camgöbeği)
ve öncelik çubukları orantılı olarak doldurulur. Varsayılan `bbs`
teması utanmazca 1990'lardandır.

---

## Nasıl çalışır

```
                   ┌─────────────────────┐
   sinyaller ────► │   Sinyal kaynakları │  (cron-window, github-ci, ...)
                   └──────────┬──────────┘
                              ▼
                   ┌─────────────────────┐
                   │  ~/.triage/state/   │  (kaynak başına append-only JSONL)
                   └──────────┬──────────┘
                              ▼
   tick     ─────► ┌─────────────────────┐ ─────► yeniden sıralanmış kuyruk
                   │  Triage zamanlayıcı │        + görev başına denetim günlüğü
                   └──────────┬──────────┘
                              ▼
                   ┌─────────────────────┐
   görevler  ───► │      triage CLI     │
                   └─────────────────────┘
```

1. **Sinyal kaynakları** gerçekleri yayar (`cron-window`, `github-ci`,
   gelecekteki `runpod-cost`, `github-pr`...).
2. **Kurallar** gerçekleri öncelik delta'larına dönüştürür
   (`base_score`, `deadline_decay`, `cron_window_active`,
   `ci_failing`, `blocker_transitive`).
3. **Kuyruk yeniden sıralanır** her `triage tick`'te.
4. **Her yeniden sıralama açıklanabilirdir** — `triage why <id>`,
   hangi kuralın hangi delta ile katkıda bulunduğunu tam olarak
   gösterir, böylece sıra asla bir kara kutu değildir.

Tam mimari, kural kataloğu ve yol haritası için
[`DESIGN.md`](DESIGN.md)'a bakın.

---

## Kurulum

```bash
git clone https://github.com/CryptoJones/Triage      # veya codeberg.org/CryptoJones/Triage
cd Triage
pip install -e .
```

Saf Python standart kitaplığı. Çalışma zamanı bağımlılığı yok.
3.10 / 3.11 / 3.12 üzerinde test edildi.

---

## Kullanım

### Görevler

```bash
triage add "Kimlik doğrulama hatasını düzelt" --base-score 10
triage add "Staging sertifikasını döndür" --deadline 2026-05-20T00:00:00Z
triage add "Sadece hafta içi görev"    --cron-window "* 9-17 * * 1-5"
triage add "CI'ı izle"             --tag "gh-ci:CryptoJones/Triage@main"
triage add "Linter'ı bekle"        --blocked-by <linter-task-id>

triage list                     # mevcut öncelik sırası
triage show <id>                # ham görev kaydı (JSON)
triage why  <id>                # hangi kuralın hangi delta ile katkı sağladığı
triage rm   <id>                # kaldır
```

### Yeniden sıralama + yoklama

```bash
triage tick                     # öncelikleri yeniden hesapla; yeni sırayı yazdır
triage poll github-ci           # ağa bağlı bir sinyal kaynağını çağır
```

`tick` ucuz, yerel ve idempotenttir — cron'dan, bir shell döngüsünden
veya Claude Code'un `ScheduleWakeup`'ından çağırın. `poll` ağa
dokunan sinyal kaynakları içindir (bunların bedelini açıkça ödersiniz).

### Dil

Triage birden çok dil konuşur. Dili `--lang` seçeneği veya olağan
ortam değişkenleri ile ayarlayın:

```bash
triage --lang tr list           # tek seferlik
TRIAGE_LANG=tr triage list      # shell başına
triage lang                     # mevcut dilleri listele
```

Desteklenen diller: English, Español, Français, Deutsch, Italiano,
Português, Nederlands, Polski, Čeština, Svenska, Norsk, Dansk, Suomi,
Română, Magyar, Türkçe. Dil tanınmazsa İngilizce yedek olarak kullanılır.

### Olay günlüğü (harici ajanlar için)

Her CLI çağrısı bir günlük dosyasına tek bir JSON satırı ekler, böylece
harici bir ajan `tail -f` ile Triage'ın davranışını ayrıştırabilir:

```bash
tail -f /var/log/triage.log | jq .   # dosya kullanıcına aitse
```

Örnek girdiler:

```json
{"ts":"2026-05-16T06:16:18+00:00","event":"add","task_id":"9e8040d267d9","subject":"Yavaş sorguyu araştır","base_score":10,"tags":[],"deadline":null,"blocked_by":[]}
{"ts":"2026-05-16T06:16:18+00:00","event":"tick","ranked_count":2,"emitted_cron_signals":0,"top":[{"id":"ad2006db3c12","priority":35,"subject":"Sertifikayı döndür"}],"warnings":[]}
{"ts":"2026-05-16T06:16:19+00:00","event":"poll","source":"github-ci","emitted":1,"warnings":[]}
{"ts":"2026-05-16T06:16:20+00:00","event":"rm","task_id":"9e8040d267d9"}
```

Yapılandırma:

| Mekanizma                  | Ne yapar                                                         |
|----------------------------|------------------------------------------------------------------|
| `--log-file PATH` seçeneği | Çağrı başına günlük yolu.                                        |
| env `TRIAGE_LOG_FILE=PATH` | Shell başına günlük yolu.                                        |
| Varsayılan                 | `/var/log/triage.log`. `/var/log` yazılamazsa `~/.triage/triage.log`'a düşer (stderr'de bir kez uyarır). |
| `--no-log` seçeneği        | Bu çağrı için günlüğü devre dışı bırak.                          |
| env `TRIAGE_NO_LOG=1`      | Shell için günlüğü genel olarak devre dışı bırak.                |

Her çağrıda sudo olmadan standart `/var/log` yolunu kullanmak için:

```bash
sudo touch /var/log/triage.log
sudo chown $(id -un):$(id -gn) /var/log/triage.log
```

Günlük kaydı sıkı tek yönlü bir yan kanaldır — yazma sırasındaki
hatalar yutulur, böylece CLI'nin birincil davranışı asla bozulmaz.

### Temalar

```bash
triage theme                    # mevcut temaları listele
triage theme --name bbs         # örnek satırları işle
triage --theme modern list      # çağrı başına tema geçersiz kılma
TRIAGE_THEME=mono triage list   # shell başına tema
```

| Tema     | Estetik                                                              |
|----------|----------------------------------------------------------------------|
| `bbs`    | **Varsayılan.** 1990'ların BBS'i: parlak magenta, çift çizgili kutu (`╔═╗`), blok çubuklar. |
| `modern` | İnce palet, tek çizgili kutular (`┌─┐`), noktalı çubuklar (`█▒·`).   |
| `mono`   | Renk yok, sadece ASCII (`+-+`, `#=.`) — borular / aptal terminaller için güvenli. |

Renk standartlara uyar:

- stdout TTY olmadığında otomatik olarak devre dışı bırakılır.
- `NO_COLOR=1` rengi devre dışı bırakır ([no-color.org](https://no-color.org/) uyarınca).
- `FORCE_COLOR=1` TTY olmayanda rengi etkinleştirir.
- `--no-color` seçeneği = çağrı başına açık kapatma anahtarı.

---

## İlgili projeler

Triage küçük bir ekosistemin bir parçasıdır. Parçalar birlikte çalışır:

| Depo | Rol |
|------|-----|
| [**claude_skill-Triage**](https://github.com/CryptoJones/claude_skill-Triage) | Claude Code'un skill deposu. Bugün `TaskPriorityReorder`'ı sağlar (**manuel geçersiz kılma** — "X'i en üste taşı") ve gelecekteki bir sürümde `triage` skill'ini (**sinyal güdümlü öneri sahibi** — "sırada ne yapmalıyım?") barındıracaktır. |
| [**TriageMCP**](https://github.com/CryptoJones/TriageMCP) | AI ajanları için Triage API'sini saran **MCP sunucusu**. stdio üzerinden sekiz araç (`list_tasks`, `add_task`, `tick`, `why_task`, `status`, `remove_task`, `inject_signal`, `get_task`). Bunu `~/.claude/mcp.json`'a bırakın, bir ajan öncelik kuyruğunuzu doğrudan okuyup yazabilir. |
| [**RunPodBoss**](https://github.com/CryptoJones/RunPodBoss) | RunPod için kredi bakiyesi koruyucusu. Triage ile `extra_notify_command` üzerinden entegre olur — bir faturalandırma eşiği aşıldığında, RunPodBoss Triage'a manuel bir sinyal iter, böylece "boş pod'ları boşalt" görevi kuyruğunuzun üstüne çıkar. Yapılandırma tarifi: [`docs/runpodboss-integration.md`](docs/runpodboss-integration.md). |

Dördü de Triage'ın ilkelini paylaşır (kararlı kimlik + yeniden
hesaplanabilir öncelik) ve çift aynalarda yaşar (GitHub + Codeberg).

---

## Durum

| Sürüm | Özellik                                                              | Durum     |
|-------|----------------------------------------------------------------------|-----------|
| v0.1  | iskelet, üç kural, cron-window sinyali, CLI                          | yayınlandı |
| v0.2  | `blocker_transitive` yayılımı + döngü algılama                       | yayınlandı |
| v0.3  | `github-ci` sinyal kaynağı + `ci_failing` kuralı + `triage poll`     | yayınlandı |
| v0.4  | BBS tarzı ANSI tema sistemi + `triage theme` alt komutu              | yayınlandı |
| v0.5  | `runpod-cost` sinyal kaynağı + `cost_pressure` kuralı                | yayınlandı |
| v0.6  | harici ajanlar için JSONL olay günlük yazıcısı                       | yayınlandı |
| v0.7  | bayatlamış PR'lar için `github-pr` sinyal kaynağı                    | planlandı |
| v0.8  | Claude Code `triage` skill'i (`claude_skill-Triage` repo'sunda)      | planlandı |
| v0.9  | uzun süreli `triage watch` modu + systemd birimi                     | planlandı |

---

## Lisans

Apache 2.0. Bkz. [LICENSE](LICENSE).

Nebraska'da gururla üretilmiştir. Go Big Red! 🌽 https://xkcd.com/2347/
