# Registro de asistencia de IA — Duel 1

Formato de `referencias/resources/ai-policy.md`. Cada integrante agrega sus propias entradas. El LLM que es objeto del experimento (`qwen2.5:3b`) no va aquí; va en el reporte.

## Base del Duel 1 — estructura, motor instrumentado y asignaciones

**Quién:** Daniel Salazar.
**Herramienta:** Claude Code (Anthropic), trabajando en la carpeta local del repositorio de Daniel, 2 de octubre de 2026.

**Qué pedí:** revisar a fondo el repositorio del profe y las ramas del equipo, proponer una base para el Duel 1, armarla y escribir asignaciones detalladas para Andretty y Jalil.

**Qué recibí:**
- La estructura de carpetas que exige la consigna, con nuestras convenciones de hw3 y hw5 (archivos del curso intactos, `SOURCE_MANIFEST.json`, `referencias/` y `DECISION_NOTES.md`).
- `code/motor.py`: el bucle de `search()` del curso con frontera máxima, tiempo, timeout y A*, más el IDS de nuestra hw3.
- `code/dominios.py`, `code/benchmark.py`, `code/estadistica.py` y `code/rutas.py`.
- `code/tests/test_group.py` (7 pruebas), los esqueletos con `TODO` y las pruebas de aceptación de cada parte (`test_heuristicas.py` y `test_validador.py`). Claude comprobó, con una implementación de referencia que no se guardó en el repo, que esas pruebas se pueden pasar.
- `ASIGNACIONES.md`, `RUBRICA.md`, el borrador de `REPORT.md` y este registro.

**Qué hice con eso:** pendiente de mi revisión antes del primer commit compartido.

**¿Lo entendí?** Pendiente. Debo poder explicar por qué el test de meta va al expandir, cómo se mide la frontera máxima en IDS y por qué un timeout no es "no hay solución".
