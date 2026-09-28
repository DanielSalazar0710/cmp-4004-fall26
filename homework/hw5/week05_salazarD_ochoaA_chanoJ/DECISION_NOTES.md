# Notas de decisiones — Salazar, Ochoa y Chano

## Contrato del agente

El torneo exige `choose_move(board, time_budget_ms) -> int` y la consigna pide usar el `alphabeta` que se entrega en `connect4.py`. No modificamos ese archivo ni `test_alphabeta.py`; sus huellas están en `SOURCE_MANIFEST.json`. Todo lo nuestro está en `starter.py`.

`choose_move` delega en `search_profile`, que devuelve además la lista de profundidades completadas. De este modo el notebook mide exactamente el agente del torneo, no una copia con otra lógica.

## Orden de jugadas

`order_moves(board, first=None)` devuelve las columnas legales en orden centro-primero (`CENTER_FIRST`). Si se le pasa la mejor jugada de la iteración anterior, la coloca al inicio: es el orden dinámico que sugiere la consigna. El segundo argumento es opcional para no romper la interfaz que usan los tests (`order_moves(board)`).

El `alphabeta` dado aplica la misma lista de prioridad en todos los niveles del árbol. Por eso adelantar una columna también la adelanta en las respuestas de MIN. No escribimos otra búsqueda para evitarlo, porque la consigna pide usar el motor dado. La tabla de transposición también quedó fuera por ese motivo: habría requerido una búsqueda propia.

## Profundización iterativa y reloj

Seguimos las tres reglas del docstring:
1. Siempre tenemos una jugada legal: `best` empieza con la primera columna del orden.
2. No empezamos una profundidad que probablemente no termine. Una llamada a `alphabeta` no se puede interrumpir a la mitad, así que antes de cada profundidad estimamos su tiempo como `tiempo_anterior × crecimiento`. El crecimiento es el cociente entre las dos últimas profundidades, acotado entre 2 y 8. Solo empezamos si el total estimado cabe en `SAFETY × presupuesto`.
3. Nos quedamos con la jugada de la última profundidad completa.

Elegimos `SAFETY = 0.6` con una prueba exploratoria sobre 13 posiciones aleatorias que no forma parte de los resultados guardados. Con 0.6 el máximo fue 288 ms. Con 0.8 se alcanzaba a veces una profundidad más, pero una jugada tardó 590 ms, más que el límite de 500 ms.

**La estimación no bastó (versión 1 → versión 2).** Con solo la estimación, una corrida completa del mini torneo registró una jugada de nuestro agente de **586 ms**. Esa jugada, más otras sobre el límite, le costó **3 partidas perdidas por tiempo** (2 contra `αβ fijo d4` y 1 contra el aleatorio). La evidencia está en `resultados_v1_sin_corte_duro/`, junto con el `starter_v1.py` que se midió. En esa corrida todo el equipo iba más lento que en la anterior (minimax a profundidad 6 tardó 10,7 s frente a 9,5 s), y la estimación del crecimiento no previó una profundidad más cara.

Por eso añadimos un **corte duro** sin modificar el motor. El `alphabeta` dado ejecuta `counter[0] += 1` en cada nodo, así que le pasamos un contador propio (`_ClockCounter`) que revisa el reloj en cada nodo. Si se llegó al 80 % del presupuesto (`HARD_STOP = 0.8`), lanza una excepción que abandona la profundidad en curso. Esa profundidad incompleta no se usa, y nos quedamos con la jugada de la última completa (regla 3). Como la excepción interrumpe la búsqueda antes de los `pop`, buscamos sobre una copia del tablero. Hay una prueba de esto en `test_group.py`. La estimación sigue sirviendo para no empezar profundidades que casi seguro se desperdiciarían.

Las partidas del retador LLM (sección 15 del notebook) se jugaron contra la versión 1. Ambas versiones hacen la misma búsqueda y solo difieren en el corte duro. En esas partidas no medimos el tiempo de nuestro agente, porque la regla de tiempo solo se aplica en el mini torneo.

Dos cortes adicionales:
- **Victoria forzada (valor 10 000):** dejamos de profundizar. `evaluate()` no descuenta la distancia a la victoria, así que una profundidad mayor podría preferir una victoria más lejana con el mismo valor. La primera profundidad que ve la victoria encuentra la más corta.
- **Derrota forzada (valor −10 000):** todas las jugadas empatan en la peor nota y `alphabeta` devolvería simplemente la primera del orden. Por eso conservamos la jugada de la profundidad anterior, que al menos no pierde dentro de ese horizonte más corto, y dejamos de buscar.

## Banco táctico

`tactics.py` genera, con semilla fija, 80 posiciones sin ganador en las que MAX mueve: 10 de victoria inmediata y 10 de bloqueo por cada tamaño (6, 12, 18 y 24 fichas). En las de bloqueo, MAX no tiene victoria inmediata y MIN amenaza exactamente una columna, así que la jugada correcta es única. Las respuestas se calculan probando cada columna con `winner()`; no las escribimos a mano. `test_group.py` comprueba que el banco se regenera igual y que cada respuesta es correcta.

El número de fichas es una aproximación a la dificultad que pide el eje de escalamiento del scorecard. No es una medida formal: una posición con pocas fichas puede ser tácticamente difícil.

## Retador LLM

- Usamos el prompt exacto de la consigna. `{board}` es `str(board)` visto desde el LLM, que siempre es `X`: si le toca jugar con MIN, invertimos las fichas con `tournament.as_max`.
- Validamos cada respuesta contra `legal_moves()`. Si no es legal, reintentamos una vez con otra semilla (semilla + 1000), porque repetir la misma llamada con temperatura 0 solo devolvería el mismo texto desde la caché. Si el reintento también falla, jugamos la primera columna legal del orden centro-primero y lo registramos como fallback.
- Separamos la lectura estricta (la respuesta es solo un número, como pide el prompt) de la tolerante (primer entero dentro del texto).
- Modelo principal: `qwen2.5:3b`, el valor por defecto del harness y de `resources/setup.md`. Corremos también el banco táctico con `qwen2.5:1.5b`, el modelo de nuestras semanas 0 a 2.
- **Independencia de las repeticiones.** En la semana 2, las cinco "repeticiones" eran aciertos de caché de la misma llamada. Aquí la clave de caché incluye la semilla. Las repeticiones usan las semillas 1 a 5, distintas de la semilla 0 de la corrida principal, así que la primera vez cada una es una inferencia nueva. `llm_calls.jsonl` guarda `cached` por llamada y el notebook comprueba que ninguna repetición medida fue un acierto de caché.
- La caché `.llm_cache/` se versiona porque es la evidencia de las respuestas, como pide `setup.md`.

## Mini torneo

Replicamos localmente las reglas del plan: 500 ms por jugada, la jugada ilegal pierde y excederse del tiempo pierde. Compiten nuestro agente, α-β de profundidad fija 6 (el agente de referencia que menciona el starter), α-β de profundidad 4 y un agente aleatorio. Cada par juega 6 aperturas de dos jugadas con ambos colores, 72 partidas en total. Las aperturas fijas evitan que dos agentes deterministas repitan una única partida.

El resultado depende de la velocidad de la máquina. En otra laptop, la profundidad 6 puede entrar o no en 500 ms, y nuestro agente alcanzará otra profundidad. Por la misma razón, nuestro agente no es determinista: la profundidad alcanzada depende del reloj.
