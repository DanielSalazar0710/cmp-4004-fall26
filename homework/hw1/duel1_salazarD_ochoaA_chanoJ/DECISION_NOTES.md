# Notas de decisiones — Salazar, Ochoa y Chano

Cada integrante agrega aquí las decisiones de su parte, con el porqué. Las de la base son estas.

## Instancias

Usamos los bancos del curso sin cambios: el 8-puzzle de week 3 (profundidades óptimas 4, 8, 12 y 16, verificadas por el profe con BFS exhaustivo) y las grillas de week 4 (5, 8, 12 y 16). Ambos tienen 10 instancias por nivel y semilla 20260807. No generamos instancias propias, para que nadie pueda pensar que elegimos un banco favorable a un lado. Es una limitación: los niveles los fijó el profe, no nosotros.

Las grillas del curso no tienen paredes. El validador igual las revisa, porque el enunciado lo pide, pero ningún camino puede fallar por una pared en este banco. Lo declaramos en la sección de honestidad.

## Motor instrumentado

El `search()` del curso no mide la frontera máxima ni el tiempo, y no tiene timeout. Por eso `code/motor.py` repite su bucle con esas métricas, sin modificar el original: el test de meta va al expandir, `expansions` cuenta lo mismo y el desempate es estable. `test_group.py` comprueba que nuestras expansiones y costos son idénticos a los del `search()` del curso en BFS, DFS y UCS.

A* es la misma búsqueda de grafo con prioridad `g + h` y conjunto de explorados. Con una heurística admisible pero no consistente, esa versión podría perder optimalidad. Misplaced y Manhattan son consistentes en el 8-puzzle, y Manhattan × MIN_COST lo es en la grilla, así que no afecta a las heurísticas admisibles. Con h × 3 la pérdida es justamente lo que medimos.

IDS es el de nuestra hw3: usa el conjunto del camino actual contra ciclos y `max_depth` de 60. Su "frontera máxima" es la profundidad máxima de la pila de recursión, porque IDS no tiene cola. Lo decimos así en el reporte para no comparar peras con manzanas.

## Timeout

Usamos 30 s por corrida (algoritmo × instancia). El reloj se revisa cada 256 expansiones, así que una corrida puede pasarse unos milisegundos. Un timeout se guarda como `status=timeout` con las expansiones hasta el corte, y no entra en las medianas de costo. En la prueba rápida, IDS se queda sin tiempo en la grilla de 16×16: busca la menor profundidad y, con costos no uniformes, el número de caminos simples crece demasiado.

## LLM

Usamos `qwen2.5:3b`, el modelo por defecto de `resources/setup.md`, con temperatura 0 y semilla 0 en la corrida principal. La caché del harness incluye la semilla en la clave. Las 5 llamadas de reproducibilidad se hacen sin caché, porque si no serían copias de la primera (como pasó en week 2).

## Análisis 1 y 4 (Daniel)

Para el análisis 1 comparamos el costo de UCS con el de cada A* admisible (misplaced y Manhattan), instancia por instancia. A*-manhattan_x3 queda fuera porque no es admisible a propósito. Para mostrar a BFS elegimos, de forma automática, la grilla donde su sobrecosto relativo es mayor, y dibujamos los dos caminos. Así no escogemos a mano un ejemplo favorable.

Para b* usamos la definición de las slides de week 4: N son los nodos que A* **expandió** y d es la longitud de la solución. Lo resolvemos por bisección, igual que `effective_bf` del notebook. Incluimos a UCS como referencia sin heurística. En nuestra corrida de prueba, b* de UCS a profundidad 12 sale cerca de 1,7, menor que el ~2,8 típico de la tabla de las slides. La razón es que nuestro motor es búsqueda de grafo con conjunto de explorados, no búsqueda de árbol: no vuelve a expandir estados repetidos. Lo decimos en el reporte en vez de forzar el número de la tabla.

## Brazo con herramienta (Daniel)

El modelo recibe exactamente el mismo texto que el brazo puro, más la descripción de una herramienta `astar` que se llama con una línea de JSON. Ejecutamos nuestro A* sobre la grilla **que el modelo escribió** en la llamada, no sobre la instancia original. Si el modelo la copia mal, la herramienta resuelve otro problema; eso lo medimos con `tool_args_match`. Aceptamos la grilla como lista de filas o como texto con saltos de línea, porque es la misma información. Una grilla aplanada en una sola línea es ambigua y se devuelve como error a la herramienta. El modelo puede llamar a la herramienta hasta 2 veces.

En las pruebas con 4 grillas ya aparecieron los modos de falla que esperábamos. El modelo aplanó la grilla, la herramienta respondió con error y el modelo inventó un camino. También copió mal una grilla de 12×12. Y en una de 16×16 el modelo no terminó de responder en 300 s. Estos casos se cuentan; no se corrigen.

Subimos el timeout del cliente de 120 s a 300 s y registramos los errores del modelo como `llm_error`. El harness no limita la longitud de la respuesta y lo dejamos sin cambios, por eso no fijamos `num_predict`.

## Librerías

No usamos pandas. En la laptop de Daniel, el Control inteligente de aplicaciones de Windows bloquea sus DLL. Todo se hace con `csv` y `numpy`.
