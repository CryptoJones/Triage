<div align="center">

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                    T  R  I  A  G  E                          ║
║                                                              ║
║      méta-planificateur qui surveille sa propre file         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Une file de priorités consciente d'elle-même.** Les signaux
apportent des faits sur le monde ; les règles convertissent les
faits en deltas de priorité ; la file se réordonne d'elle-même à
chaque tick. Vous fixez les objectifs — Triage décide de l'ordre
et vous explique précisément pourquoi.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg?logo=apache)](LICENSE)
[![Stdlib only](https://img.shields.io/badge/deps-stdlib_only-success?logo=python&logoColor=white)](pyproject.toml)
[![Codeberg](https://img.shields.io/badge/Codeberg-CryptoJones%2FTriage-2185D0?logo=codeberg&logoColor=white)](https://codeberg.org/CryptoJones/Triage)
[![GitHub](https://img.shields.io/badge/GitHub-CryptoJones%2FTriage-181717?logo=github&logoColor=white)](https://github.com/CryptoJones/Triage)

**Lisez-le en :**
[English](README.md) ·
[Español](README.es.md) ·
**Français** ·
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
[Català](README.ca.md)

</div>

> Miroir sur [GitHub](https://github.com/CryptoJones/Triage) et
> [Codeberg](https://codeberg.org/CryptoJones/Triage). Les tickets
> déposés sur l'une ou l'autre forge sont les bienvenus ; les
> commits atterrissent sur les deux.

---

## Ce que vous voyez

```
╔════════════════════════════════════════════════════════╗
║                  T R I A G E   v0.10.0                 ║
╚════════════════════════════════════════════════════════╝
  ID               PRI  BAR    SUJET
  ════════════  ══════  ═════  ════════════════════════════════════════
  7cfa440bc639  [ 101]  █████  Réparer le linter     ← bloqueur auto-promu
  f35d7cea6b7d  [ 100]  █████  Ajouter la fonctionnalité X
  19c80b807ddd  [  35]  █▒░░░  Renouveler le certif  ← pression d'échéance
  abc123456789  [   2]  ░░░░░  Nettoyage de routine
```

Dans un vrai terminal le bandeau est magenta vif, les priorités sont
bandées par couleur (élevée = jaune, moyenne = verte, basse = cyan
atténué) et les barres de priorité se remplissent proportionnellement.
Le thème par défaut `bbs` est résolument années 90.

---

## Fonctionnement

```
                   ┌─────────────────────┐
   signaux  ─────► │  Sources de signal  │  (cron-window, github-ci, ...)
                   └──────────┬──────────┘
                              ▼
                   ┌─────────────────────┐
                   │  ~/.triage/state/   │  (JSONL append-only par source)
                   └──────────┬──────────┘
                              ▼
   tick     ─────► ┌─────────────────────┐ ─────► file réordonnée
                   │ Planificateur Triage│        + journal d'audit
                   └──────────┬──────────┘
                              ▼
                   ┌─────────────────────┐
   tâches   ─────► │     CLI triage      │
                   └─────────────────────┘
```

1. **Les sources de signal** apportent des faits (`cron-window`,
   `github-ci`, futurs `runpod-cost`, `github-pr`...).
2. **Les règles** convertissent les faits en deltas de priorité
   (`base_score`, `deadline_decay`, `cron_window_active`,
   `ci_failing`, `blocker_transitive`).
3. **La file se réordonne** à chaque `triage tick`.
4. **Chaque réordonnancement est explicable** — `triage why <id>`
   montre exactement quelles règles ont contribué quels deltas,
   l'ordre n'est donc jamais une boîte noire.

Voir [`DESIGN.md`](DESIGN.md) pour l'architecture complète, le
catalogue de règles et la feuille de route.

---

## Installation

```bash
git clone https://github.com/CryptoJones/Triage      # ou codeberg.org/CryptoJones/Triage
cd Triage
pip install -e .
```

Python stdlib pur. Aucune dépendance d'exécution. Testé sur
3.10 / 3.11 / 3.12.

---

## Utilisation

### Tâches

```bash
triage add "Corriger le bug d'auth" --base-score 10
triage add "Renouveler le certif staging" --deadline 2026-05-20T00:00:00Z
triage add "Corvée en semaine seulement" --cron-window "* 9-17 * * 1-5"
triage add "Surveiller CI"          --tag "gh-ci:CryptoJones/Triage@main"
triage add "Attendre le linter"     --blocked-by <linter-task-id>

triage list                     # ordre de priorité actuel
triage show <id>                # enregistrement brut de la tâche (JSON)
triage why  <id>                # quelles règles ont contribué quels deltas
triage rm   <id>                # supprimer
```

### Réordonner + sonder

```bash
triage tick                     # recalculer les priorités ; afficher le nouvel ordre
triage poll github-ci           # invoquer une source de signal réseau
```

`tick` est bon marché, local et idempotent — appelez-le depuis cron,
une boucle shell ou le `ScheduleWakeup` de Claude Code. `poll` est
pour les sources de signal qui touchent au réseau (vous payez ces
coûts explicitement).

### Langue

Triage parle plusieurs langues. Définissez la langue avec l'option
`--lang` ou les variables d'environnement habituelles :

```bash
triage --lang fr list           # ponctuel
TRIAGE_LANG=fr triage list      # par shell
triage lang                     # liste les langues disponibles
```

Langues prises en charge : English, Español, Français, Deutsch,
Italiano, Português, Nederlands, Polski, Čeština, Svenska, Norsk,
Dansk, Suomi, Română, Magyar, Türkçe, Català. Toute langue non
reconnue retombe sur l'anglais.

### Journal d'événements (pour les agents externes)

Chaque invocation de la CLI ajoute une ligne JSON à un fichier
journal, de sorte qu'un agent externe puisse `tail -f` et analyser
le comportement de Triage :

```bash
tail -f /var/log/triage.log | jq .   # si le fichier appartient à votre utilisateur
```

Exemples d'entrées :

```json
{"ts":"2026-05-16T06:16:18+00:00","event":"add","task_id":"9e8040d267d9","subject":"Enquêter sur la requête lente","base_score":10,"tags":[],"deadline":null,"blocked_by":[]}
{"ts":"2026-05-16T06:16:18+00:00","event":"tick","ranked_count":2,"emitted_cron_signals":0,"top":[{"id":"ad2006db3c12","priority":35,"subject":"Renouveler le certif"}],"warnings":[]}
{"ts":"2026-05-16T06:16:19+00:00","event":"poll","source":"github-ci","emitted":1,"warnings":[]}
{"ts":"2026-05-16T06:16:20+00:00","event":"rm","task_id":"9e8040d267d9"}
```

Configuration :

| Mécanisme                  | Effet                                                              |
|----------------------------|--------------------------------------------------------------------|
| option `--log-file PATH`   | Chemin du journal par invocation.                                  |
| env `TRIAGE_LOG_FILE=PATH` | Chemin du journal par shell.                                       |
| Par défaut                 | `/var/log/triage.log`. Bascule sur `~/.triage/triage.log` si `/var/log` n'est pas inscriptible (avertit une fois sur stderr). |
| option `--no-log`          | Désactive la journalisation pour cette invocation.                 |
| env `TRIAGE_NO_LOG=1`      | Désactive la journalisation globalement pour le shell.             |

Pour utiliser le chemin standard `/var/log` sans sudo à chaque appel :

```bash
sudo touch /var/log/triage.log
sudo chown $(id -un):$(id -gn) /var/log/triage.log
```

La journalisation est un canal latéral unidirectionnel strict — les
erreurs d'écriture sont avalées pour que le comportement principal
de la CLI ne soit jamais perturbé.

### Thèmes

```bash
triage theme                    # lister les thèmes disponibles
triage theme --name bbs         # rendre des lignes d'exemple
triage --theme modern list      # changement de thème ponctuel
TRIAGE_THEME=mono triage list   # thème par shell
```

| Thème    | Esthétique                                                                |
|----------|---------------------------------------------------------------------------|
| `bbs`    | **Par défaut.** BBS années 90 : magenta vif, cadre à double trait (`╔═╗`), barres en blocs. |
| `modern` | Palette discrète, cadres à trait unique (`┌─┐`), barres en pointillés (`█▒·`). |
| `mono`   | Sans couleur, ASCII uniquement (`+-+`, `#=.`) — sûr pour les pipes et terminaux limités. |

La couleur suit les conventions :

- Désactivée automatiquement quand stdout n'est pas un TTY.
- `NO_COLOR=1` désactive la couleur (cf. [no-color.org](https://no-color.org/)).
- `FORCE_COLOR=1` active la couleur en non-TTY.
- L'option `--no-color` = interrupteur explicite par invocation.

---

## Projets connexes

Triage est une pièce d'un petit écosystème. Les pièces se combinent :

| Dépôt | Rôle |
|-------|------|
| [**claude_skill-Triage**](https://github.com/CryptoJones/claude_skill-Triage) | Dépôt de skills Claude Code. Livre aujourd'hui `TaskPriorityReorder` (**surcharge manuelle** — « remonter X en haut ») et hébergera la skill `triage` (**recommandeur piloté par signaux** — « que devrais-je faire ensuite ? ») dans une version future. |
| [**TriageMCP**](https://github.com/CryptoJones/TriageMCP) | **Serveur MCP** qui enveloppe l'API de Triage pour les agents IA. Huit outils (`list_tasks`, `add_task`, `tick`, `why_task`, `status`, `remove_task`, `inject_signal`, `get_task`) sur stdio. Place-le dans `~/.claude/mcp.json` et un agent pourra lire et écrire directement ta file de priorités. |
| [**RunPodBoss**](https://github.com/CryptoJones/RunPodBoss) | Garde-fou du solde RunPod. S'intègre à Triage via `extra_notify_command` — lorsqu'un seuil de facturation est franchi, RunPodBoss injecte un signal manuel dans Triage pour que la tâche « vider les pods inactifs » remonte en tête de file. Recette de configuration dans [`docs/runpodboss-integration.md`](docs/runpodboss-integration.md). |

Les quatre partagent la primitive de Triage (identité stable + priorité
recalculable) et vivent sur des miroirs doubles (GitHub + Codeberg).

---

## État

| Version | Fonctionnalité                                                            | État    |
|---------|---------------------------------------------------------------------------|---------|
| v0.1    | squelette, trois règles, signal cron-window, CLI                          | publié    |
| v0.2    | propagation `blocker_transitive` + détection de cycles                    | publié    |
| v0.3    | source de signal `github-ci` + règle `ci_failing` + `triage poll`         | publié    |
| v0.4    | thème ANSI style BBS + sous-commande `triage theme`                       | publié    |
| v0.5    | source de signal `runpod-cost` + règle `cost_pressure`                    | publié    |
| v0.6    | écrivain de journal d'événements JSONL pour agents externes               | publié    |
| v0.7    | source de signal `github-pr` + règle `rule_stale_pr`                      | publié    |
| v0.8    | CLI `triage signal` + règle `manual_bump` + intégration RunPodBoss        | publié    |
| v0.8.1  | résumé sur un écran `triage status`                                       | publié    |
| v0.9    | base d'i18n — option `--lang` + locales en/es/fr                          | publié    |
| v0.10   | i18n complète — 17 locales + détecteur de régressions `triage lang --check` | publié    |
| —       | skill `triage` Claude Code (dans le dépôt `claude_skill-Triage`)          | prévu     |
| —       | mode `triage watch` longue durée + unité systemd                          | prévu     |

---

## Licence

Apache 2.0. Voir [LICENSE](LICENSE).

Fièrement fabriqué au Nebraska. Go Big Red ! 🌽 https://xkcd.com/2347/
