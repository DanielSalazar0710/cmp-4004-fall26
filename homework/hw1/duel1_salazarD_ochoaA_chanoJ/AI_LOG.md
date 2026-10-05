# Registro de asistencia de IA — Duel 1

Formato de `referencias/resources/ai-policy.md`. Cada integrante agrega sus propias entradas. El LLM que es objeto del experimento (`qwen2.5:3b`) no va aquí; va en el reporte.

## Base del Duel 1 — estructura, motor instrumentado y asignaciones

**Quién:** Daniel Salazar.
**Herramienta:** Claude Code (Anthropic), trabajando en la carpeta local del repositorio de Daniel, 2 de octubre de 2026.

**Qué le pedí:** revisar a fondo el repositorio del profe y las ramas del equipo, proponer una base para el Duel 1, armarla y escribir asignaciones detalladas para Andretty y Jalil.

**Qué recibí:**
- La estructura de carpetas que exige la consigna, con nuestras convenciones de hw3 y hw5 (archivos del curso intactos, `SOURCE_MANIFEST.json`, `referencias/` y `DECISION_NOTES.md`).
- `code/motor.py`: el bucle de `search()` del curso con frontera máxima, tiempo, timeout y A*, más el IDS de nuestra hw3.
- `code/dominios.py`, `code/benchmark.py`, `code/estadistica.py` y `code/rutas.py`.
- `code/tests/test_group.py` (7 pruebas), los esqueletos con `TODO` y las pruebas de aceptación de cada parte (`test_heuristicas.py` y `test_validador.py`). Con Claude Code comprobé, usando una implementación de referencia que no guardé en el repo, que esas pruebas se pueden pasar.
- `ASIGNACIONES.md`, `RUBRICA.md`, el borrador de `REPORT.md` y este registro.

**Qué hice con eso:** revisé la estructura y las asignaciones, pedí que todo quedara escrito con la voz del equipo y subí la base a la rama `hw1-salazarD` para Andretty y Jalil. También pedí los issues de GitHub y una guía en PDF para el equipo.

**¿Lo entendí?** Pendiente. Debo poder explicar por qué el test de meta va al expandir, cómo se mide la frontera máxima en IDS y por qué un timeout no es "no hay solución".

## Análisis 1 y 4 y brazo con herramienta

**Quién:** Daniel Salazar.
**Herramienta:** Claude Code (Anthropic), 2 de octubre de 2026.

**Qué le pedí:** desarrollar conmigo mi parte: el análisis de optimalidad (UCS = A* y BFS con costos no uniformes), el factor de ramificación efectivo b* y el brazo con herramienta.

**Qué recibí:** `code/analisis_optimalidad.py` (tablas, el informe de BFS dibujado, b* por bisección y su figura), una prueba de b* en `test_group.py` y `code/herramienta.py` (la llamada JSON, la ejecución de nuestro A* con los argumentos del modelo y el registro de cada llamada). Probamos el análisis con una corrida de benchmark hecha con heurísticas de prueba que no guardamos en el repo, porque las heurísticas oficiales son de Andretty. El brazo con herramienta lo probamos en 4 grillas con una caché aparte, para no mezclar esas pruebas con la evidencia.

**Qué hice con eso:** pendiente. Hay que correr ambos con los datos oficiales cuando estén las heurísticas y el validador.

**¿Lo entendí?** Pendiente. Debo poder explicar por qué BFS falla con costos no uniformes, cómo se calcula b* y por qué nuestro b* de UCS es menor que el de la tabla de las slides.


## Heurísticas, análisis 2 y 3 y figuras

**Quién:** Andretty Ochoa.  
**Herramienta:** ChatGPT (OpenAI), 4 de octubre de 2026.

**Qué le pedí:** acompañarme paso a paso en mi parte del Duel 1, incluyendo la implementación y revisión de las heurísticas para 8-puzzle y grid, la comparación entre misplaced y Manhattan, el experimento con Manhattan ×3, el procesamiento de las mediciones y la generación de las figuras requeridas. También lo usé para interpretar los resultados y preparar mis aportes al reporte y a las notas de decisiones.

**Qué recibí:**
- Apoyo para implementar y revisar `h_misplaced`, `h_manhattan_puzzle`, `h_manhattan_grid` e `inflar` en `code/heuristicas.py`.
- Apoyo para completar `code/analisis_heuristicas.py`, generando `resumen_parte1.csv`, `dominancia.csv`, `inflado_x3.csv` y las tres figuras de la Parte 1.
- Explicaciones sobre admisibilidad, dominancia, heurísticas infladas, speedup y pérdida de optimalidad.
- Ayuda para interpretar las mediciones oficiales y redactar mis secciones de `REPORT.md` y `DECISION_NOTES.md`.

**Qué hice con eso:** revisé el código antes de incorporarlo, ejecuté personalmente las pruebas de heurísticas y del grupo, corrí primero el benchmark rápido y después el benchmark completo de 520 mediciones. Verifiqué los resultados de dominancia y del experimento ×3 y regeneré los CSV y las figuras con los datos oficiales antes de usarlos en el reporte.

**¿Lo entendí?** Sí. Puedo explicar por qué misplaced y Manhattan excluyen el espacio vacío, por qué Manhattan es admisible, por qué Manhattan domina informativamente a misplaced, por qué multiplicar la heurística por 3 rompe la garantía de admisibilidad y cómo interpretar los speedups y la pérdida de calidad observada.