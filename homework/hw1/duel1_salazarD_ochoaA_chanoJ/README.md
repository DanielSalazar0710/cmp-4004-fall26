# Duel 1 — Salazar, Ochoa y Chano

Comparación de BFS, DFS, UCS, IDS y A* entre sí, contra un LLM (`qwen2.5:3b` en Ollama) y contra ese mismo LLM con nuestro A* como herramienta. Usamos las mismas 80 instancias en todos los casos: 8-puzzle y grilla con terrenos, 4 niveles × 10 instancias.

- Consigna: [`referencias/hw1/hw-1-search.md`](referencias/hw1/hw-1-search.md)
- Quién hace qué: [`ASIGNACIONES.md`](ASIGNACIONES.md)
- Checklist de calificación: [`RUBRICA.md`](RUBRICA.md)
- Reporte: [`REPORT.md`](REPORT.md) · Decisiones: [`DECISION_NOTES.md`](DECISION_NOTES.md) · IA: [`AI_LOG.md`](AI_LOG.md)

## Estado y resultados principales

Las tres partes están completas y todas las pruebas pasan: 9 de la base, 6 de heurísticas y 9 del validador.

| Sistema | Correctas (de 80) | Evidencia |
|---|---|---|
| A*-Manhattan (clásico) | 80 | `results/parte1_mediciones.csv` |
| LLM `qwen2.5:3b` | 0 | `results/llm_respuestas.csv` |
| LLM + nuestro A* como herramienta | 17 | `results/herramienta_respuestas.csv` |

Quién hizo qué: Andretty Ochoa las heurísticas y los análisis 2 y 3 (PR #4); Jalil Chano el borrador del validador y del brazo LLM, que integramos; Daniel Salazar la base, los análisis 1 y 4, el brazo con herramienta, la integración y el reporte. El uso de IA está en `AI_LOG.md`.

Las corridas que descartamos están en `evidencia_descartada/`, cada una con un README que explica por qué: dos procesos a la vez contra Ollama, y un error de nuestra herramienta en el 8-puzzle que ya corregimos.

## Ejecución

Desde la raíz del repositorio, en PowerShell y con Python 3.10 o posterior:

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r homework\hw1\duel1_salazarD_ochoaA_chanoJ\requirements.txt
cd homework\hw1\duel1_salazarD_ochoaA_chanoJ
$env:PYTHONIOENCODING="utf-8"
python code\tests\test_group.py          # base
python code\tests\test_heuristicas.py    # Andretty
python code\tests\test_validador.py      # Jalil
python code\benchmark.py                 # Parte 1 completa (timeout 30 s por corrida)
python code\analisis_heuristicas.py      # análisis 2 y 3 + figuras
python code\analisis_optimalidad.py      # análisis 1 y 4
ollama pull qwen2.5:3b
python code\duelo_llm.py                 # brazo LLM, reproducibilidad, escalado
python code\herramienta.py               # brazo con herramienta
python code\duelo_llm.py --repro grid-8-00   # reproducibilidad (también grid-5-00)
python code\duelo_llm.py --figuras       # figuras y conteo de fallas
python code\auditoria_ollama.py --por-hora   # auditoría de llamadas sin texto
python code\scorecard.py                 # números del scorecard
```

## Estructura

```
REPORT.md  AI_LOG.md  ASIGNACIONES.md  RUBRICA.md  DECISION_NOTES.md  SOURCE_MANIFEST.json
code/
  motor.py              BFS/DFS/UCS/IDS/A* con expansiones, frontera máxima, tiempo y timeout
  dominios.py           bancos del curso e ids de instancia
  benchmark.py          Parte 1 → results/parte1_mediciones.csv
  estadistica.py        CSV, mediana e IQR, huellas (sin pandas)
  heuristicas.py        (Andretty)  analisis_heuristicas.py (Andretty)
  validador.py          (Jalil)     duelo_llm.py          (Jalil)
  analisis_optimalidad.py (Daniel)  herramienta.py        (Daniel)
  tests/                pruebas de la base y de aceptación de cada parte
  curso/week03, week04  archivos del profe, intactos
  aicourse/             harness del curso, copiado sin cambios de nuestra Week 05
results/  fig/  .llm_cache/
referencias/            consigna, resources, studios 3 y 4, notebooks y slides del curso
```
