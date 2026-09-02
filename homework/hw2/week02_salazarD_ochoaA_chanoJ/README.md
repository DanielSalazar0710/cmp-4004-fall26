# Week 02 Studio - Vacuum World

## Que contiene esta entrega

Complete la semana 2 trabajando sobre una copia local de los archivos necesarios del estudio `week-02`.
La parte principal fue cerrar la taxonomia de agentes:

- `goal_based`: agente con meta explicita, limpia las dos habitaciones y luego se queda en `NoOp`.
- `utility_based`: agente que decide por utilidad inmediata bajo el costo del torneo.
- `llm_agent`: deje implementado el socket para conectar un LLM al mismo contrato `percept -> action`, incluyendo parser, retry y fallback.

Todo lo necesario para revisar esta semana esta en esta misma carpeta. No inclui `slides`, `resources` ni archivos de otras semanas porque los use solo como referencia.

## Como correrlo

Desde esta carpeta:

```bash
python test_agents.py
python starter.py
```

El notebook principal de presentacion es:

```bash
jupyter notebook week02_salazarD_ochoaA_chanoJ.ipynb
```

Para verificar el backend LLM en PowerShell:

```powershell
$env:PYTHONIOENCODING="utf-8"
$env:AICOURSE_MODEL="qwen2.5:1.5b"
python -m aicourse.doctor
```

## Resultado de tests

```text
ok  reflex failed on 2/4 broken-sensor configs; model_based cleaned all
ok  goal_based reaches (both rooms clean) on all 8 configs
ok  goal_based returns NoOp once the goal is reached
ok  utility_based always cleans the (dirty) room it starts in
ok  utility_based rationally left a room dirty on 4/8 configs

all 5 tests pass
```

## Torneo

```text
start                         reflex         model          goal       utility
------------------------------------------------------------------------------
dirt=(True, True) loc=0            92           109           109            58
dirt=(True, True) loc=1            92            57           109            58
dirt=(True, False) loc=0            99           117           117           118
dirt=(True, False) loc=1            96            59           114            60
dirt=(False, True) loc=0            96           114           114            60
dirt=(False, True) loc=1            99           117           117           118
dirt=(False, False) loc=0          100           119           119           120
dirt=(False, False) loc=1          100           119           119           120
------------------------------------------------------------------------------
TOTAL                              774           811           918           712
```

El resultado mas importante del torneo es que el agente de utilidad no obtiene el mayor puntaje. Su decision esta limitada al percepto actual y no usa horizonte de planificacion. Por eso, moverse hacia una habitacion que todavia no puede evaluar tiene costo inmediato negativo, aunque a largo plazo podria convenir.

## Scorecard: `utility_based` vs `llm_agent`

| Eje | Utility-based | LLM agent | Evidencia |
|---|---|---|---|
| Correctness | Limpia su habitacion inicial si esta sucia; deja alguna habitacion sucia en 4/8 configs. | Resolvio 3/3 configuraciones en la corrida capada. | `test_agents.py`, `llm_results.md` |
| Guarantee | Si el percepto dice `dirty=True`, ejecuta `Suck`; si no, solo cruza si el beneficio inmediato supera el costo. | Ninguna garantia formal: depende de texto generado y del parser. | Codigo en `starter.py` |
| Cost | CPU local, sin tokens, costo constante por paso. | Requiere una llamada a modelo por paso; la corrida uso cache para replay. | `.llm_cache/`, `llm_results.md` |
| Latency | Practicamente instantaneo en 8 configs. | Mediana original cacheada: 3.152s por llamada; p95: 3.673s. | `.llm_cache/`, `llm_results.md` |
| Reproducibility | 1 secuencia por entrada, porque es deterministico. | 1 secuencia distinta en 5 repeticiones. | `llm_results.md` |
| Scaling | Para 2 habitaciones funciona; para n habitaciones habria que reescribir la representacion de estado. | Escala peor en costo por paso, pero podria ayudar cuando describir reglas sea lo dificil. | Analisis de arquitectura |
| Interpretability | Alta: se puede explicar cada accion con costo inmediato. | Media/baja: el texto puede explicar algo, pero no es certificado. | Comparacion conceptual |
| Failure mode | MIOPE: deja valor sobre la mesa porque no planea. | Texto mal formado, accion ambigua, timeout o respuesta fuera del conjunto permitido. | `failure_atlas.md` |

## Donde puede haber sido injusto

El agente clasico esta completamente controlado por reglas, mientras que el agente LLM depende de texto generado. Esa diferencia obliga a agregar parser, registro de fallas, retry y fallback. Ese codigo defensivo no mejora la arquitectura del ambiente; solo hace posible conectar una salida textual a acciones formales.

El experimento LLM usa un modelo local pequeno (`qwen2.5:1.5b`). Un modelo mas grande podria comportarse distinto, pero eso tendria que medirse con el mismo torneo y no asumirse.

## Archivos en esta carpeta

- `starter.py`: codigo final de los agentes.
- `vacuum.py`: ambiente y agentes base entregados por el curso.
- `tournament.py`: evaluador de utilidad neta.
- `configs.json`: las 8 configuraciones iniciales.
- `test_agents.py`: tests usados para verificar la solucion.
- `llm_experiment.py`: corrida del agente LLM usando `aicourse.llm.LLM`.
- `llm_results.md`: resultados de la corrida LLM capada y replay desde cache.
- `aicourse/`: harness base de Week 0 usado para `LLM`, cache y `doctor`.
- `requirements.txt`: dependencias indicadas en el paquete base de Week 0.
- `week02_salazarD_ochoaA_chanoJ.ipynb`: reporte/presentacion del trabajo del grupo.
- `README.md`: resumen de ejecucion, tests, torneo y scorecard.
- `DECISION_NOTES.md`: notas de decisiones de implementacion.
- `failure_atlas.md`: entrada de Failure Atlas.
- `AI_LOG.md`: registro de uso de IA segun la politica del curso.
