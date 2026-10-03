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

## Librerías

No usamos pandas. En la laptop de Daniel, el Control inteligente de aplicaciones de Windows bloquea sus DLL. Todo se hace con `csv` y `numpy`.
