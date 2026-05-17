<div align="center">

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                    T  R  I  A  G  E                          ║
║                                                              ║
║      meta-agendador que observa a própria fila               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Uma fila de prioridades autoconsciente.** Os sinais introduzem
factos sobre o mundo; as regras convertem factos em deltas de
prioridade; a fila reordena-se a si mesma a cada tick. Tu defines
os objectivos — o Triage decide a ordem e explica-te exactamente
porquê.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg?logo=apache)](LICENSE)
[![Stdlib only](https://img.shields.io/badge/deps-stdlib_only-success?logo=python&logoColor=white)](pyproject.toml)
[![Codeberg](https://img.shields.io/badge/Codeberg-CryptoJones%2FTriage-2185D0?logo=codeberg&logoColor=white)](https://codeberg.org/CryptoJones/Triage)
[![GitHub](https://img.shields.io/badge/GitHub-CryptoJones%2FTriage-181717?logo=github&logoColor=white)](https://github.com/CryptoJones/Triage)

**Lê isto em:**
[English](README.md) ·
[Español](README.es.md) ·
[Français](README.fr.md) ·
[Deutsch](README.de.md) ·
[Italiano](README.it.md) ·
**Português** ·
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

> Espelhado no [GitHub](https://github.com/CryptoJones/Triage) e no
> [Codeberg](https://codeberg.org/CryptoJones/Triage). São bem-vindas
> as issues abertas em qualquer uma das forjas; os commits são
> publicados em ambas.

---

## O que vês

```
╔════════════════════════════════════════════════════════╗
║                  T R I A G E   v0.9.0                  ║
╚════════════════════════════════════════════════════════╝
  ID               PRI  BAR    ASSUNTO
  ════════════  ══════  ═════  ════════════════════════════════════════
  7cfa440bc639  [ 101]  █████  Corrigir o linter      ← bloqueador auto-elevado
  f35d7cea6b7d  [ 100]  █████  Adicionar funcionalidade X
  19c80b807ddd  [  35]  █▒░░░  Rotar certificado      ← pressão de prazo
  abc123456789  [   2]  ░░░░░  Limpeza de rotina
```

Num terminal real, o banner aparece em magenta brilhante, as
prioridades estão coloridas por faixas (alta = amarelo, média =
verde, baixa = ciano ténue) e as barras de prioridade preenchem-se
proporcionalmente. O tema predefinido `bbs` é descaradamente anos 90.

---

## Como funciona

```
                   ┌─────────────────────┐
   sinais   ─────► │  Fontes de sinal    │  (cron-window, github-ci, ...)
                   └──────────┬──────────┘
                              ▼
                   ┌─────────────────────┐
                   │  ~/.triage/state/   │  (JSONL append-only por fonte)
                   └──────────┬──────────┘
                              ▼
   tick     ─────► ┌─────────────────────┐ ─────► fila reordenada
                   │ Agendador Triage    │        + registo de auditoria
                   └──────────┬──────────┘
                              ▼
                   ┌─────────────────────┐
   tarefas  ─────► │      CLI triage     │
                   └─────────────────────┘
```

1. **As fontes de sinal** introduzem factos (`cron-window`,
   `github-ci`, futuros `runpod-cost`, `github-pr`...).
2. **As regras** convertem os factos em deltas de prioridade
   (`base_score`, `deadline_decay`, `cron_window_active`,
   `ci_failing`, `blocker_transitive`).
3. **A fila reordena-se** a cada `triage tick`.
4. **Cada reordenação é explicável** — `triage why <id>` mostra
   exactamente quais regras contribuíram com quais deltas, por isso
   a ordem nunca é uma caixa negra.

Consulta [`DESIGN.md`](DESIGN.md) para a arquitectura completa, o
catálogo de regras e o roteiro.

---

## Instalação

```bash
git clone https://github.com/CryptoJones/Triage      # ou codeberg.org/CryptoJones/Triage
cd Triage
pip install -e .
```

Python stdlib puro. Sem dependências em tempo de execução. Testado
em 3.10 / 3.11 / 3.12.

---

## Utilização

### Tarefas

```bash
triage add "Corrigir o bug de auth" --base-score 10
triage add "Rotar o certificado de staging" --deadline 2026-05-20T00:00:00Z
triage add "Tarefa só em dias de semana" --cron-window "* 9-17 * * 1-5"
triage add "Vigiar CI"             --tag "gh-ci:CryptoJones/Triage@main"
triage add "Esperar pelo linter"   --blocked-by <linter-task-id>

triage list                     # ordem de prioridade actual
triage show <id>                # registo bruto da tarefa (JSON)
triage why  <id>                # quais regras contribuíram com quais deltas
triage rm   <id>                # remover
```

### Reordenar + sondar

```bash
triage tick                     # recalcular prioridades; imprimir a nova ordem
triage poll github-ci           # invocar uma fonte de sinal de rede
```

`tick` é barato, local e idempotente — invoca-o a partir do cron, de
um ciclo de shell ou do `ScheduleWakeup` do Claude Code. `poll` é
para fontes de sinal que tocam na rede (esses custos pagas-os
explicitamente).

### Idioma

O Triage fala várias línguas. Define o idioma com a opção `--lang` ou
as variáveis de ambiente habituais:

```bash
triage --lang pt list           # pontual
TRIAGE_LANG=pt triage list      # por shell
triage lang                     # lista os idiomas disponíveis
```

Idiomas suportados: English, Español, Français, Deutsch, Italiano,
Português. Idiomas desconhecidos recorrem ao inglês.

### Registo de eventos (para agentes externos)

Cada invocação da CLI acrescenta uma única linha JSON a um ficheiro
de registo, para que um agente externo possa fazer `tail -f` e
analisar o comportamento do Triage:

```bash
tail -f /var/log/triage.log | jq .   # se o ficheiro pertencer ao teu utilizador
```

Entradas de exemplo:

```json
{"ts":"2026-05-16T06:16:18+00:00","event":"add","task_id":"9e8040d267d9","subject":"Investigar consulta lenta","base_score":10,"tags":[],"deadline":null,"blocked_by":[]}
{"ts":"2026-05-16T06:16:18+00:00","event":"tick","ranked_count":2,"emitted_cron_signals":0,"top":[{"id":"ad2006db3c12","priority":35,"subject":"Rotar certificado"}],"warnings":[]}
{"ts":"2026-05-16T06:16:19+00:00","event":"poll","source":"github-ci","emitted":1,"warnings":[]}
{"ts":"2026-05-16T06:16:20+00:00","event":"rm","task_id":"9e8040d267d9"}
```

Configuração:

| Mecanismo                  | O que faz                                                            |
|----------------------------|----------------------------------------------------------------------|
| opção `--log-file PATH`    | Caminho do registo por invocação.                                    |
| env `TRIAGE_LOG_FILE=PATH` | Caminho do registo por shell.                                        |
| Predefinido                | `/var/log/triage.log`. Recorre a `~/.triage/triage.log` se `/var/log` não for gravável (avisa uma vez no stderr). |
| opção `--no-log`           | Desactiva o registo para esta invocação.                             |
| env `TRIAGE_NO_LOG=1`      | Desactiva o registo globalmente para a shell.                        |

Para usar o caminho padrão `/var/log` sem sudo em cada chamada:

```bash
sudo touch /var/log/triage.log
sudo chown $(id -un):$(id -gn) /var/log/triage.log
```

O registo é um canal lateral unidireccional estrito — os erros de
escrita são engolidos para que o comportamento principal da CLI
nunca seja perturbado.

### Temas

```bash
triage theme                    # listar temas disponíveis
triage theme --name bbs         # renderizar linhas de exemplo
triage --theme modern list      # substituição de tema pontual
TRIAGE_THEME=mono triage list   # tema por shell
```

| Tema     | Estética                                                                |
|----------|-------------------------------------------------------------------------|
| `bbs`    | **Predefinido.** BBS dos anos 90: magenta brilhante, caixa de linha dupla (`╔═╗`), barras de blocos. |
| `modern` | Paleta subtil, caixas de linha simples (`┌─┐`), barras com pontos (`█▒·`). |
| `mono`   | Sem cor, apenas ASCII (`+-+`, `#=.`) — seguro para pipes / terminais simples. |

A cor segue as convenções:

- Desactivada automaticamente quando o stdout não é um TTY.
- `NO_COLOR=1` desactiva a cor (cfr. [no-color.org](https://no-color.org/)).
- `FORCE_COLOR=1` activa a cor em não-TTY.
- A opção `--no-color` = interruptor explícito por invocação.

---

## Projectos relacionados

O Triage é uma peça de um pequeno ecossistema. As peças compõem-se:

| Repositório | Papel |
|-------------|-------|
| [**claude_skill-Triage**](https://github.com/CryptoJones/claude_skill-Triage) | Repositório de skills do Claude Code. Fornece hoje `TaskPriorityReorder` (**substituição manual** — «subir X ao topo») e alojará a skill `triage` (**recomendador guiado por sinais** — «o que devo fazer a seguir?») numa versão futura. |
| [**TriageMCP**](https://github.com/CryptoJones/TriageMCP) | **Servidor MCP** que envolve a API do Triage para agentes de IA. Oito ferramentas (`list_tasks`, `add_task`, `tick`, `why_task`, `status`, `remove_task`, `inject_signal`, `get_task`) sobre stdio. Coloca-o em `~/.claude/mcp.json` e um agente pode ler e escrever directamente a tua fila de prioridades. |
| [**RunPodBoss**](https://github.com/CryptoJones/RunPodBoss) | Salvaguarda do saldo de crédito para o RunPod. Integra-se com o Triage através de `extra_notify_command` — quando um limiar de facturação é cruzado, o RunPodBoss injecta um sinal manual no Triage para que a tarefa «esvaziar pods inactivos» suba ao topo da tua fila. Receita de configuração em [`docs/runpodboss-integration.md`](docs/runpodboss-integration.md). |

Os quatro partilham a primitiva do Triage (identidade estável + prioridade
recalculável) e vivem em espelhos duplos (GitHub + Codeberg).

---

## Estado

| Versão | Funcionalidade                                                            | Estado     |
|--------|---------------------------------------------------------------------------|------------|
| v0.1   | esqueleto, três regras, sinal cron-window, CLI                            | publicada  |
| v0.2   | propagação `blocker_transitive` + detecção de ciclos                      | publicada  |
| v0.3   | fonte de sinal `github-ci` + regra `ci_failing` + `triage poll`           | publicada  |
| v0.4   | tema ANSI ao estilo BBS + subcomando `triage theme`                       | publicada  |
| v0.5   | fonte de sinal `runpod-cost` + regra `cost_pressure`                      | publicada  |
| v0.6   | escritor de registo de eventos JSONL para agentes externos                | publicada  |
| v0.7   | fonte de sinal `github-pr` para PRs obsoletos                             | planeada   |
| v0.8   | skill `triage` do Claude Code (no repo `claude_skill-Triage`)             | planeada   |
| v0.9   | modo `triage watch` de longa duração + unidade systemd                    | planeada   |

---

## Licença

Apache 2.0. Consulta [LICENSE](LICENSE).

Feito com orgulho no Nebraska. Go Big Red! 🌽 https://xkcd.com/2347/
