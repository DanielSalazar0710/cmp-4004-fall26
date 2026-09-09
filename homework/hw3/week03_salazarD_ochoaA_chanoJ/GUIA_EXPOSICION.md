# Guía de exposición — Salazar, Ochoa y Chano

## Preparación

Abrimos `starter.py` y el notebook uno junto al otro. Ejecutamos el notebook en orden antes de la clase y comprobamos que sus salidas estén guardadas. La versión HTML sirve para mostrar las mismas salidas sin depender del kernel. La medición ya está guardada; explicamos cuándo fue ejecutada y cómo repetirla.

## Propuesta de distribución de la exposición

| Integrante | Bloque | Demostración |
|---|---|---|
| Salazar | Formulación, secciones 1–4 | Cargas legales y tabla de los 11 cruces |
| Ochoa | Algoritmos, secciones 5–8 | Fronteras, TinyGraph, IDS y tests |
| Chano | Experimentos, secciones 9–14 | Tablero, tabla, gráfica, límites y conclusión |

Proponemos 4–5 minutos por bloque. Cerramos con la discusión de la sección 15, que relaciona los tres bloques del trabajo.

## Qué decimos y qué mostramos

1. **Inicio:** «En la semana anterior elegíamos acciones; ahora formulamos un problema y buscamos un plan completo». Mostramos los cinco componentes.
2. **En `MissionariesAndCannibals`:** «Guardamos solo la izquierda y el bote; la derecha se deduce». Mostramos `is_valid` y por qué se evalúan ambas orillas.
3. **Cruces:** «Un misionero solo no puede salir al inicio: dejaría dos misioneros con tres caníbales». Ejecutamos la tabla de cargas, después la ruta de 11 cruces.
4. **En `bfs`, `dfs`, `ucs`:** «Presentamos las funciones de una línea ya que comparten el mismo ciclo; cada frontera cambia qué nodo exploramos primero». Mostramos las tres cadenas y la tabla de TinyGraph.
5. **En `depth_limited` e `ids`:** «El límite crece y reiniciamos; sumamos también los intentos fallidos». Mostramos la tabla de límites 0–8 y explicamos `on_path`.
6. **Pruebas:** ejecutamos la celda de tests. «BFS con costo 10 es precisamente el resultado esperado en ese test».
7. **Medición:** «Cada algoritmo enfrenta las mismas 40 instancias, 160 corridas en total». Mostramos primero calidad de solución y luego expansiones.
8. **Gráfica:** señalamos el eje logarítmico, la superposición BFS/UCS, la dispersión DFS y la diferencia de IDS. A profundidad 16, IDS usa cerca de 2,60 veces las expansiones de BFS.
9. **Fallo:** «DFS sí llega, pero puede recorrer 94 144 movimientos cuando bastan 4. Encontrar una meta no garantiza una solución útil».
10. **Cierre:** «La representación decide qué es legal; la frontera decide qué encontramos primero; la medición muestra el costo».

## Preguntas con respuesta breve

- **¿Qué significa una acción del puzzle?** El índice destino del hueco, no el número de la ficha.
- **¿Por qué no basta excluir al padre en IDS?** Evita ciclos de dos pasos, pero no los de tres o más; el camino actual cubre ambos.
- **¿Por qué no usar `visited` global en IDS?** Puede podar una llegada más corta que todavía tiene profundidad para llegar a la meta.
- **¿Es UCS siempre completo?** En estos grafos finitos sí; para espacios infinitos necesitamos condiciones como ramificación finita y costo mínimo positivo.
- **¿Cómo sabemos las profundidades?** Contrastamos las profundidades del banco con una BFS exhaustiva desde la meta en `verify_results.py`.
- **¿La solución DFS enorme es legal?** Se reprodujeron todas las acciones de las 160 rutas y se verificó que llegan a la meta.
- **¿Por qué IDS es menor que BFS en profundidad 4?** El orden de hallazgo y los cortes importan; reiniciar no obliga a hacer más expansiones en cada instancia.
- **¿Qué significa la escala logarítmica?** Distancias verticales iguales representan factores multiplicativos iguales.
- **¿Podemos decir que profundidad 24 no cabe en la laptop?** No con estos datos: el grafo del 8-puzzle es finito. La proyección es orientativa y la memoria no fue medida.
- **¿Cómo se relacionan los bloques?** La formulación define estados y acciones; los algoritmos recorren ese espacio; el experimento compara el trabajo realizado y la calidad de las soluciones.
