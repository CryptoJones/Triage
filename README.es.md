<div align="center">

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                    T  R  I  A  G  E                          ║
║                                                              ║
║      meta-planificador que observa su propia cola            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Una cola de prioridades autoconsciente.** Las señales aportan
hechos sobre el mundo; las reglas convierten los hechos en deltas
de prioridad; la cola se reordena a sí misma en cada tick. Tú fijas
los objetivos — Triage decide el orden y te explica exactamente por qué.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg?logo=apache)](LICENSE)
[![Stdlib only](https://img.shields.io/badge/deps-stdlib_only-success?logo=python&logoColor=white)](pyproject.toml)
[![Codeberg](https://img.shields.io/badge/Codeberg-CryptoJones%2FTriage-2185D0?logo=codeberg&logoColor=white)](https://codeberg.org/CryptoJones/Triage)
[![GitHub](https://img.shields.io/badge/GitHub-CryptoJones%2FTriage-181717?logo=github&logoColor=white)](https://github.com/CryptoJones/Triage)

**Léelo en:**
[English](README.md) ·
**Español** ·
[Français](README.fr.md) ·
[Deutsch](README.de.md) ·
[Italiano](README.it.md) ·
[Português](README.pt.md) ·
[Nederlands](README.nl.md) ·
[Polski](README.pl.md) ·
[Čeština](README.cs.md)

</div>

> Replicado tanto en [GitHub](https://github.com/CryptoJones/Triage) como en
> [Codeberg](https://codeberg.org/CryptoJones/Triage). Se aceptan
> incidencias en cualquiera de las dos forjas; los commits se publican
> en ambas.

---

## Lo que ves

```
╔════════════════════════════════════════════════════════╗
║                  T R I A G E   v0.9.0                  ║
╚════════════════════════════════════════════════════════╝
  ID               PRI  BAR    ASUNTO
  ════════════  ══════  ═════  ════════════════════════════════════════
  7cfa440bc639  [ 101]  █████  Corregir el linter     ← bloqueador auto-elevado
  f35d7cea6b7d  [ 100]  █████  Añadir función X       ← bloqueada por el linter
  19c80b807ddd  [  35]  █▒░░░  Rotar certificado      ← presión por plazo
  abc123456789  [   2]  ░░░░░  Limpieza rutinaria
```

En una terminal real el banner es magenta brillante, las prioridades
están coloreadas por bandas (alta = amarillo, media = verde, baja =
cian tenue) y las barras se rellenan proporcionalmente. El tema por
defecto `bbs` es descaradamente noventero.

---

## Cómo funciona

```
                   ┌─────────────────────┐
   señales  ─────► │  Fuentes de señal   │  (cron-window, github-ci, ...)
                   └──────────┬──────────┘
                              ▼
                   ┌─────────────────────┐
                   │  ~/.triage/state/   │  (JSONL append-only por fuente)
                   └──────────┬──────────┘
                              ▼
   tick     ─────► ┌─────────────────────┐ ─────► cola reordenada
                   │  Planificador Triage│        + registro de auditoría
                   └──────────┬──────────┘
                              ▼
                   ┌─────────────────────┐
   tareas   ─────► │      CLI triage     │
                   └─────────────────────┘
```

1. **Las fuentes de señal** aportan hechos (`cron-window`, `github-ci`,
   futuros `runpod-cost`, `github-pr`...).
2. **Las reglas** convierten los hechos en deltas de prioridad
   (`base_score`, `deadline_decay`, `cron_window_active`,
   `ci_failing`, `blocker_transitive`).
3. **La cola se reordena** en cada `triage tick`.
4. **Cada reordenación es explicable** — `triage why <id>` muestra
   exactamente qué reglas contribuyeron qué deltas, así el orden
   nunca es una caja negra.

Consulta [`DESIGN.md`](DESIGN.md) para la arquitectura completa, el
catálogo de reglas y la hoja de ruta.

---

## Instalación

```bash
git clone https://github.com/CryptoJones/Triage      # o codeberg.org/CryptoJones/Triage
cd Triage
pip install -e .
```

Python stdlib puro. Sin dependencias en tiempo de ejecución. Probado
en 3.10 / 3.11 / 3.12.

---

## Uso

### Tareas

```bash
triage add "Corregir el bug de auth" --base-score 10
triage add "Rotar el certificado de staging" --deadline 2026-05-20T00:00:00Z
triage add "Tarea solo entre semana" --cron-window "* 9-17 * * 1-5"
triage add "Vigilar CI"            --tag "gh-ci:CryptoJones/Triage@main"
triage add "Esperar al linter"     --blocked-by <linter-task-id>

triage list                     # orden de prioridad actual
triage show <id>                # registro bruto de la tarea (JSON)
triage why  <id>                # qué reglas contribuyeron qué deltas
triage rm   <id>                # eliminar
```

### Reordenar + sondear

```bash
triage tick                     # recalcular prioridades; imprimir el nuevo orden
triage poll github-ci           # invocar una fuente de señal de red
```

`tick` es barato, local e idempotente — llámalo desde cron, un bucle
de shell o el `ScheduleWakeup` de Claude Code. `poll` es para fuentes
de señal que tocan la red (esos costes se pagan explícitamente).

### Idioma

Triage habla varios idiomas. Define el idioma con la opción `--lang`
o las variables de entorno habituales:

```bash
triage --lang es list           # de una sola vez
TRIAGE_LANG=es triage list      # por shell
triage lang                     # lista los idiomas disponibles
```

Idiomas admitidos: English, Español, Français, Deutsch, Italiano,
Português. Si no se reconoce el idioma, se utiliza inglés como
respaldo.

### Registro de eventos (para agentes externos)

Cada invocación de la CLI añade una línea JSON a un fichero de
registro, de modo que un agente externo pueda hacer `tail -f` y
analizar el comportamiento de Triage:

```bash
tail -f /var/log/triage.log | jq .   # si el fichero pertenece a tu usuario
```

Entradas de muestra:

```json
{"ts":"2026-05-16T06:16:18+00:00","event":"add","task_id":"9e8040d267d9","subject":"Investigar consulta lenta","base_score":10,"tags":[],"deadline":null,"blocked_by":[]}
{"ts":"2026-05-16T06:16:18+00:00","event":"tick","ranked_count":2,"emitted_cron_signals":0,"top":[{"id":"ad2006db3c12","priority":35,"subject":"Rotar certificado"}],"warnings":[]}
{"ts":"2026-05-16T06:16:19+00:00","event":"poll","source":"github-ci","emitted":1,"warnings":[]}
{"ts":"2026-05-16T06:16:20+00:00","event":"rm","task_id":"9e8040d267d9"}
```

Configuración:

| Mecanismo                  | Qué hace                                                          |
|----------------------------|-------------------------------------------------------------------|
| opción `--log-file PATH`   | Ruta del registro por invocación.                                 |
| env `TRIAGE_LOG_FILE=PATH` | Ruta del registro por shell.                                      |
| Predeterminado             | `/var/log/triage.log`. Recurre a `~/.triage/triage.log` si `/var/log` no es escribible (avisa una vez en stderr). |
| opción `--no-log`          | Desactiva el registro para esta invocación.                       |
| env `TRIAGE_NO_LOG=1`      | Desactiva el registro globalmente para el shell.                  |

Para usar la ruta estándar `/var/log` sin sudo en cada llamada:

```bash
sudo touch /var/log/triage.log
sudo chown $(id -un):$(id -gn) /var/log/triage.log
```

El registro es un canal lateral estricto y unidireccional — los
errores al escribir se ignoran para que el comportamiento principal
de la CLI nunca se vea interrumpido.

### Temas

```bash
triage theme                    # listar temas disponibles
triage theme --name bbs         # renderizar filas de muestra
triage --theme modern list      # cambio de tema puntual
TRIAGE_THEME=mono triage list   # tema por shell
```

| Tema     | Estética                                                                |
|----------|-------------------------------------------------------------------------|
| `bbs`    | **Predeterminado.** BBS noventero: magenta brillante, caja de doble línea (`╔═╗`), barras de bloques. |
| `modern` | Paleta sutil, cajas de línea sencilla (`┌─┐`), barras con puntos (`█▒·`). |
| `mono`   | Sin color, solo ASCII (`+-+`, `#=.`) — seguro para pipes y terminales tontos. |

El color sigue las convenciones:

- Se desactiva automáticamente cuando stdout no es una TTY.
- `NO_COLOR=1` desactiva el color (según [no-color.org](https://no-color.org/)).
- `FORCE_COLOR=1` activa el color en no-TTY.
- La opción `--no-color` = interruptor explícito por invocación.

---

## Proyectos relacionados

Triage es una pieza de un pequeño ecosistema. Las piezas componen:

| Repositorio | Rol |
|-------------|-----|
| [**claude_skill-Triage**](https://github.com/CryptoJones/claude_skill-Triage) | Repositorio de skills de Claude Code. Ofrece hoy `TaskPriorityReorder` (**anulación manual** — «subir X al principio») y alojará la skill `triage` (**recomendador guiado por señales** — «¿qué debería hacer ahora?») en una versión futura. |
| [**TriageMCP**](https://github.com/CryptoJones/TriageMCP) | **Servidor MCP** que envuelve la API de Triage para agentes de IA. Ocho herramientas (`list_tasks`, `add_task`, `tick`, `why_task`, `status`, `remove_task`, `inject_signal`, `get_task`) sobre stdio. Colócalo en `~/.claude/mcp.json` y un agente podrá leer y escribir tu cola de prioridades directamente. |
| [**RunPodBoss**](https://github.com/CryptoJones/RunPodBoss) | Protección del saldo de crédito para RunPod. Se integra con Triage mediante `extra_notify_command` — cuando se cruza un umbral de facturación, RunPodBoss inyecta una señal manual en Triage para que la tarea «vaciar pods inactivos» suba al principio de tu cola. Receta de configuración en [`docs/runpodboss-integration.md`](docs/runpodboss-integration.md). |

Los cuatro comparten la primitiva de Triage (identidad estable + prioridad
recomputable) y se publican en doble espejo (GitHub + Codeberg).

---

## Estado

| Versión | Función                                                              | Estado    |
|---------|----------------------------------------------------------------------|-----------|
| v0.1    | esqueleto, tres reglas, señal cron-window, CLI                       | publicada |
| v0.2    | propagación `blocker_transitive` + detección de ciclos               | publicada |
| v0.3    | fuente de señal `github-ci` + regla `ci_failing` + `triage poll`     | publicada |
| v0.4    | tema ANSI estilo BBS + subcomando `triage theme`                     | publicada |
| v0.5    | fuente de señal `runpod-cost` + regla `cost_pressure`                | publicada |
| v0.6    | escritor de registro de eventos JSONL para agentes externos          | publicada |
| v0.7    | fuente de señal `github-pr` para PRs obsoletos                       | planeada  |
| v0.8    | skill `triage` de Claude Code (en el repo `claude_skill-Triage`)     | planeada  |
| v0.9    | modo `triage watch` de larga ejecución + unidad systemd              | planeada  |

---

## Licencia

Apache 2.0. Consulta [LICENSE](LICENSE).

Hecho con orgullo en Nebraska. ¡Go Big Red! 🌽 https://xkcd.com/2347/
