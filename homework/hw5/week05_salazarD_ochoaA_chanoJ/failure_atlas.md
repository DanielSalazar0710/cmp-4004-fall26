# Failure Atlas — Week 05

Cada entrada salió de una corrida registrada en `resultados_llm/llm_calls.jsonl` o `resultados/`. Los textos inventados para probar el parser (`test_group.py`) **no** están aquí porque no son fallos observados.

## [Wk5] El LLM no toma una victoria inmediata (banco táctico, `win-06-01`)

**Setup:** prompt exacto del plan, Ollama `qwen2.5:3b`, temperatura 0, semilla 0. Es una posición sintética del banco táctico: `tactics.board_from_moves([2, 6, 1, 5, 0, 4])`.

```text
|. . . . . . .|
|. . . . . . .|
|. . . . . . .|
|. . . . . . .|
|. . . . . . .|
|O O O . X X X|
 0 1 2 3 4 5 6
Legal columns: [0, 1, 2, 3, 4, 5, 6]
```

**Clásico:** la columna 3 completa cuatro en línea para X. Lo verificamos con `winner()`, y nuestro agente la juega con profundidad 1.
**LLM:** `'4'`, una respuesta legal y con el formato pedido, pero no gana. Además deja a O la victoria en la columna 3.
**Categoría:** wrong-but-confident.
**Frecuencia en el banco:** `qwen2.5:3b` tomó la victoria en 11 de 40 posiciones de victoria.

## [Wk5] El LLM no bloquea una amenaza vertical en partida (`g0X`, jugada 10)

**Setup:** partida LLM (X) contra nuestro agente (O) con la apertura 3-3, `qwen2.5:3b` a temperatura 0. El tablero que recibió el LLM:

```text
|. . . . . . .|
|. . . . X . .|
|. . . O X . .|
|. . . O O . .|
|. . . O X . .|
|. . . X X O .|
 0 1 2 3 4 5 6
```

**Clásico:** O tiene tres fichas seguidas en la columna 3, y la única jugada que evita perder es la columna 3.
**LLM:** `'4'`. En la jugada siguiente nuestro agente completó la columna 3 y ganó.
**Categoría:** wrong-but-confident.
**Frecuencia:** en las 8 partidas hubo 7 turnos con una única amenaza que bloquear, y el LLM no bloqueó ninguna. Datos en `resultados_llm/llm_game_moves_3b.csv`, con el tablero exacto de cada turno.

## [Wk5] Jugada ilegal: columna llena (`qwen2.5:1.5b`, `win-24-01`)

**Setup:** el mismo prompt con `qwen2.5:1.5b`. La columna 4 estaba llena y `Legal columns: [0, 1, 2, 3, 6]` aparecía en el prompt.
**LLM:** `'4'`. El reintento con otra semilla (1000) también devolvió `'4'`, así que se jugó el *fallback* (columna 3). La victoria estaba en la columna 6.
**Categoría:** invalid (respuesta bien formada pero ilegal).

## [Wk5] Agente clásico: derrota por tiempo con la versión 1

**Setup:** mini torneo con 500 ms por jugada y la versión 1 de `starter.py` (solo estimación del tiempo, `resultados_v1_sin_corte_duro/starter_v1.py`).
**Observado:** una jugada de 586 ms y 3 partidas perdidas por tiempo (`resultados_v1_sin_corte_duro/tournament.csv`).
**Causa:** el `alphabeta` dado no se puede interrumpir, y la estimación del costo de la siguiente profundidad falló bajo carga de la máquina.
**Corrección:** corte duro con `_ClockCounter` (ver `DECISION_NOTES.md`). En la corrida final, la jugada más lenta fue de 400,1 ms y no hubo derrotas por tiempo.
**Categoría:** times out.
