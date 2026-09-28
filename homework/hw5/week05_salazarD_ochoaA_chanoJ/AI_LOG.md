# Registro de asistencia de IA

## Week 05 — Agente α-β para el torneo de Connect-4, retador LLM y presentación

**Equipo:** Salazar, Ochoa y Chano.

**Herramienta:** Claude Code (Anthropic), trabajando en la carpeta local del repositorio de Daniel Salazar.

**Qué pedimos:** revisar el repositorio del curso y nuestras entregas anteriores, identificar la consigna del Studio 5 y desarrollarlo completo con nuestro formato: `starter.py` completado, pruebas, mediciones, retador LLM con el prompt del plan, notebook explicado en español y registros. También pedimos instalar el entorno de las semanas 0 y 1 (Ollama, modelos `qwen2.5` y librerías de `resources/setup.md`).

**Qué recibimos:**
- `order_moves` (centro primero, con la mejor jugada de la iteración anterior adelante) y `choose_move` con profundización iterativa sobre el `alphabeta` que se entrega.
- `tactics.py` (banco táctico de 80 posiciones verificadas), `tournament.py` (mini torneo con la regla de 500 ms), `experiments.py` (mediciones clásicas), `llm_challenger.py` (retador LLM con registro de cada llamada) y `test_group.py` (13 pruebas adicionales).
- Las ejecuciones de los tests, las mediciones y las 401 inferencias con Ollama.
- Una corrección del agente: la primera versión perdió 3 partidas del mini torneo por tiempo. Claude Code añadió el corte duro `_ClockCounter`, y la evidencia de la versión 1 se conserva en `resultados_v1_sin_corte_duro/`.
- El notebook, este registro y los borradores de README, notas de decisiones, guía de exposición y Failure Atlas.

**Cómo lo incorporamos:** usamos el código y los borradores generados con Claude Code como base de esta entrega. `connect4.py` y `test_alphabeta.py` se conservan sin cambios, y sus huellas SHA-256 están en `SOURCE_MANIFEST.json`. Los resultados del notebook se leen de los archivos que produjeron las ejecuciones; no se escribieron a mano.

**Decisiones que requieren comprensión:**
- Por qué α-β devuelve exactamente el valor de minimax.
- Por qué el orden de jugadas cambia los nodos y no el valor.
- Por qué la profundización iterativa conserva la jugada de la última profundidad completa.
- Qué hacen `SAFETY = 0.6` y `HARD_STOP = 0.8`, y cómo el contador de nodos interrumpe la búsqueda sin modificar `connect4.py`.
- Por qué un agente de profundidad fija pierde por tiempo.
- Qué es el efecto horizonte y por qué `play(5, 5)` es un artefacto de `evaluate()`.
- Por qué las repeticiones del LLM usan semillas distintas de la corrida principal.

**¿Lo comprendimos?** Pendiente. Todavía no registramos la revisión individual de Salazar, Ochoa y Chano. Preguntas para esa revisión:
1. ¿Por qué el corte `alpha >= beta` no puede cambiar el valor de la raíz?
2. En `search_profile`, ¿por qué dejamos de profundizar al ver una victoria forzada, y por qué ante una derrota forzada conservamos la jugada anterior?
3. ¿Qué pasaría en el torneo sin `HARD_STOP`, y por qué la búsqueda interrumpida trabaja sobre una copia del tablero?
4. ¿Por qué `αβ fijo d6` pierde partidas por tiempo aunque juega "mejor" por jugada?
5. ¿Qué demuestra y qué no demuestra el banco táctico sobre el LLM?
6. ¿Cómo explicamos que nuestro agente perdiera 7 a 5 contra `αβ fijo d4`?
