# Notas de decisiones — Salazar, Ochoa y Chano

## Representación y contrato

Elegimos `(m_left, c_left, boat_side)`, la representación utilizada en el studio. Derivamos la derecha por resta; guardar siete entidades por separado introduciría identidades que no cambian las reglas. El estado es una tupla para usar conjuntos y comparar estados completos.

Filtramos en `actions()`: primero verificamos que haya pasajeros en la orilla de salida y luego la seguridad de ambas orillas. `result()` solo aplica la transición, con la precondición de una acción legal. Validar únicamente la llegada dejaría pasar `(3,3,0) -> (2,3,1)`, donde la izquierda es insegura. Admitimos cero misioneros en una orilla; allí no hay nadie que proteger de una mayoría de caníbales.

Heredamos `step_cost=1`. Por eso BFS minimiza tanto cruces como costo. No modificamos `search.py` para adaptar el problema: formulamos el problema para cumplir su interfaz.

## BFS, DFS y UCS

Reutilizamos el ciclo de búsqueda compartido con `fifo`, `lifo` y `priority`. Conservamos el test de meta al extraer un nodo y el control de estados explorados. Los tres wrappers cortos son intencionales: duplicar el ciclo ocultaría que la diferencia está en la frontera.

El motor usa un contador para desempatar prioridades de forma estable. Con costo unitario, BFS y UCS recorren en el mismo orden. Con los costos de TinyGraph, BFS retorna 10 y UCS 2. No alteramos el test que comprueba el costo 10 de BFS.

## IDS y ciclos

Implementamos búsqueda limitada recursiva sin llamar a `search()`. Usamos el conjunto del camino actual para eliminar ciclos de cualquier longitud. Excluir solo al padre inmediato evitaría los ciclos de dos pasos, pero dejaría pasar ciclos más largos. Al volver de una rama retiramos el estado del conjunto; una llegada por otro camino puede tener más profundidad disponible.

La meta se comprueba antes de cortar por profundidad. En el límite inspeccionamos si hay sucesores no presentes en el camino; una hoja no debe producir un corte falso. Esta inspección cuesta CPU pero no se registra como expansión porque no descendemos ni construimos hijos. El contador mide trabajo de expansión, no operaciones elementales.

IDS suma las expansiones de cada límite. Mantuvimos `max_depth=40`; devolver `None` al alcanzar esa cota no prueba insolubilidad. En los experimentos comprobamos que sí se obtiene solución para todas las instancias.

## Medición y presentación

Conservamos las cuatro columnas de `measure()`. Cambiamos la selección del banco a `bank is None` para que un banco vacío no sea reemplazado accidentalmente. Si no hay solución, lanzamos un error explícito en vez de intentar `node.path()` sobre `None`.

El guardado y la gráfica están en `experiments.py`; el notebook importa la implementación de `starter.py`. Así no pueden aparecer dos algoritmos distintos con el mismo nombre en la exposición. Las explicaciones nuevas son en español; las fuentes originales están intactas en `referencias/`.

Mostramos las 160 corridas mediante datos detallados y agregamos diez instancias por profundidad con media, mediana y rango. Los puntos de la gráfica evitan que una media de DFS esconda su variabilidad. Guardamos huellas del código y del CSV para detectar resultados desactualizados.

## Garantías y límites

La memoria `O(bm)` se refiere a la formulación habitual de DFS de árbol; el motor de búsqueda de grafo que usamos también conserva estados explorados, potencialmente `O(|V|)`. Analizamos la memoria a partir de las estructuras almacenadas; la medición experimental se centró en expansiones y longitud de solución.

El ejemplo del 11 % de sobrecosto de IDS asume un árbol regular con ramificación cercana a 10. Nuestro 8-puzzle es un grafo con estados repetidos: la relación observada IDS/BFS a profundidad 16 es aproximadamente 2,60. No ajustamos el código o las cifras para forzar el ejemplo teórico.

La proyección exponencial a profundidad 24 tiene límites. BFS no puede expandir más de 181 440 estados distintos en este 8-puzzle; no concluimos que una laptop es insuficiente sin medir. La verificación independiente recorre ese espacio y confirma las profundidades del banco.

## Relación entre nuestras decisiones

El filtro de acciones define qué cruces son legales; el test de meta y la frontera determinan cuándo aceptamos una solución; el conjunto del camino de IDS permite controlar ciclos conservando poca memoria. Evaluamos estas decisiones mediante ejemplos, pruebas y las mediciones del banco de instancias.
