# Week 05 — Salazar, Ochoa y Chano

## Presentación principal

Abrimos el [notebook de presentación](week05_salazarD_ochoaA_chanoJ.ipynb) junto a [starter.py](starter.py). El notebook contiene las explicaciones en español y las salidas guardadas de una ejecución completa desde un kernel limpio. También incluimos la versión HTML para presentar sin iniciar un kernel.

## Ejecución

Desde la raíz del repositorio, en PowerShell y con Python 3.10 o posterior:

```powershell
python -m venv .venv
.venv\Scripts\activate
cd homework\hw5\week05_salazarD_ochoaA_chanoJ
python -m pip install -r requirements.txt
$env:PYTHONIOENCODING="utf-8"      # la consola de Windows no imprime α-β sin esto
python test_alphabeta.py
python test_group.py
python starter.py
jupyter notebook week05_salazarD_ochoaA_chanoJ.ipynb
```

El notebook lee las mediciones guardadas y verifica sus huellas (`REPETIR_MEDICION=False`). Para regenerarlas:

```powershell
python experiments.py                                   # clásico, unos 4 minutos
ollama pull qwen2.5:3b; ollama pull qwen2.5:1.5b
python llm_challenger.py                                # qwen2.5:3b: banco, repeticiones y partidas
python llm_challenger.py --model qwen2.5:1.5b --only tactics
```

Si se vuelve a ejecutar `llm_challenger.py`, las respuestas salen de `.llm_cache/` y `llm_calls.jsonl` las registra con `cached=true`. Para medir de nuevo la variabilidad hay que usar semillas nuevas o borrar la caché. Si cambia `starter.py`, hay que regenerar `resultados/` antes de ejecutar el notebook: las huellas lo exigen.

## Qué contiene

- `starter.py`: nuestro agente (`order_moves`, `search_profile`, `choose_move`) con profundización iterativa y corte duro de tiempo.
- `connect4.py`, `test_alphabeta.py`: originales del curso, intactos (huellas en `SOURCE_MANIFEST.json`).
- `test_group.py`: 13 comprobaciones adicionales.
- `tactics.py`, `tactical_bank.json`: banco táctico de 80 posiciones verificadas.
- `tournament.py`: mini torneo con la regla de 500 ms.
- `experiments.py`, `resultados/`: mediciones clásicas con metadatos y huellas.
- `resultados_v1_sin_corte_duro/`: evidencia de la versión 1 del agente, que perdió partidas por tiempo.
- `llm_challenger.py`, `resultados_llm/`, `.llm_cache/`: retador LLM, registro de las 401 llamadas y caché.
- `aicourse/`: harness del curso, copiado sin cambios de nuestra entrega de Week 02.
- `doctor.txt`: salida de `python -m aicourse.doctor` en la laptop donde se hicieron las mediciones.
- `DECISION_NOTES.md`, `GUIA_EXPOSICION.md`, `failure_atlas.md`, `AI_LOG.md`.
- `referencias/`: consigna, notebook, slides y recursos del curso en su idioma original.

## Resultados principales

- Pasan los 7 tests de la consigna y nuestras 13 comprobaciones.
- α-β devuelve el mismo valor que minimax con 57/45, 2 801/1 002, 19 607/4 103 y 132 179/17 030 nodos (minimax/α-β sin orden), igual que la consigna. Con orden centro-primero son 3 700 nodos a profundidad 6.
- Nuestro agente resolvió 80/80 posiciones tácticas. En el mini torneo su jugada más lenta fue de 400,1 ms, sin derrotas por tiempo. `αβ fijo d6` perdió casi todo por tiempo. Contra `αβ fijo d4` nuestro agente perdió 7 a 5, un resultado que discutimos en el notebook.
- El LLM `qwen2.5:3b`, con el prompt del plan, jugó siempre columnas legales, pero acertó 18/80 posiciones tácticas (22,5 %), menos que jugar siempre al centro (28/80). En partidas perdió 8 de 8 y no bloqueó ninguna de las 7 amenazas únicas. `qwen2.5:1.5b` acertó 8/80.
- Las 200 repeticiones para medir reproducibilidad fueron inferencias nuevas, sin aciertos de caché.

Compartimos la entrega en la rama `week05-salazarD` del fork de Daniel Salazar.
