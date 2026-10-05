# Duel 1 — Búsqueda clásica contra un LLM

**Equipo:** Daniel Salazar, Andretty Ochoa y Jalil Chano · CMP-4004 · USFQ

> Borrador. Cada sección indica quién la escribe. Límite: 2 000 palabras sin contar tablas ni leyendas. Las cifras salen de `results/`; ninguna se escribe a mano.

## 1. Qué medimos y cómo *(Daniel)*

Comparamos tres sistemas sobre las mismas 80 instancias: los algoritmos clásicos (BFS, DFS, UCS, IDS y A*), un LLM local (`qwen2.5:3b` en Ollama, temperatura 0, semilla 0) y ese mismo LLM con nuestro A* como herramienta.

- **8-puzzle:** banco del curso (week 3), 10 instancias por profundidad óptima 4, 8, 12 y 16.
- **Grilla con terrenos:** banco del curso (week 4), 10 grillas de 5×5, 8×8, 12×12 y 16×16. El costo se cobra al entrar a la celda: `.` = 1, `,` = 3 y `~` = 8. Los dos bancos usan la semilla 20260807.
- **Motor:** el `search()` del curso con frontera máxima, tiempo de reloj y un **timeout duro de 30 s por corrida**. Un timeout se reporta como timeout, nunca como "sin solución". `test_group.py` comprueba que expandimos exactamente igual que el original.
- **Validación del LLM:** un validador propio. El modelo nunca juzga sus propias respuestas.

Reportamos medianas y rango intercuartil (IQR). La Parte 1 se midió en la laptop de Andretty (Intel, Python 3.13) y los brazos LLM en la de Daniel (AMD con GPU RTX 5070 Ti, Python 3.12). Los tiempos de un sistema y otro no se comparan entre máquinas.

## 2. The Duel Scorecard *(Daniel, con datos de todos)*

| Eje | Clásico (A*) | LLM | Herramienta | Evidencia |
|---|---|---|---|---|
| 1 Corrección | | | | `results/…` |
| 2 Garantía | | | | — |
| 3 Costo | | | | |
| 4 Latencia (mediana / p95) | | | | |
| 5 Reproducibilidad | | | | `results/llm_reproducibilidad.csv` |
| 6 Escalado | | | | `fig/escalado_optimalidad.png` |
| 7 Interpretabilidad | | | | — |
| 8 Modo de falla | | | | |

## 3. Parte 1: comparación clásica

### 3.1 Optimalidad: UCS = A*, y BFS cuando los costos no son uniformes *(Daniel)*

UCS y A* con heurística admisible (misplaced y Manhattan) devolvieron **el mismo costo en las 80 instancias** (`results/optimalidad.csv`). BFS también fue óptimo en las 40 instancias del 8-puzzle, pero solo porque ahí todo paso cuesta 1. En la grilla, con costos no uniformes, BFS devolvió un camino más caro que el óptimo en **33 de 40 instancias**, y el sobrecosto mediano crece con el tamaño: 2 en 5×5 y 15 en 16×16.

Elegimos el ejemplo de forma automática: la grilla con mayor sobrecosto relativo. En `grid-12-09`, BFS y UCS usan 11 pasos cada uno, pero el camino de BFS cuesta **32** porque cruza agua (`~`), y el de UCS cuesta **11**. Los dos caminos están dibujados en `results/bfs_suboptimo.md`. BFS minimiza pasos, no costo: su optimalidad depende de que los costos sean uniformes.

### 3.2 Dominancia de Manhattan sobre misplaced *(Andretty)*

Comparamos A*-misplaced y A*-manhattan en las 40 instancias del 8-puzzle, usando como medida principal el número de expansiones. Manhattan dominó a misplaced en las 40 instancias: en ningún caso expandió más nodos. Esto coincide con lo esperado porque ambas heurísticas son admisibles, pero Manhattan utiliza más información sobre el estado. Misplaced solo cuenta cuántas fichas están fuera de su posición, mientras Manhattan estima cuántos movimientos mínimos necesita cada ficha para llegar a su objetivo.

La figura `fig/dominancia.png` muestra cada instancia con las expansiones de misplaced en el eje x y las de Manhattan en el eje y. La diagonal y=x representa igualdad. Todos los puntos quedan sobre o debajo de esa diagonal, por lo que nuestra evidencia respalda la dominancia de Manhattan en este banco. La diferencia se vuelve especialmente visible en las instancias más difíciles. Por ejemplo, en `8puzzle-16-00`, misplaced realizó 685 expansiones y Manhattan solo 169.

**Conclusión de la figura:** Manhattan nunca expandió más nodos que misplaced en las 40 instancias y su ventaja fue más evidente en los niveles difíciles.

### 3.3 Romper la admisibilidad: h × 3 *(Andretty)*

También multiplicamos Manhattan por 3 para estudiar qué ocurre al usar una heurística deliberadamente no admisible. Comparamos A*-manhattan_x3 contra A*-manhattan en 80 instancias. Medimos el speedup como expansiones de Manhattan divididas para expansiones de x3, y de forma equivalente para segundos. Para la calidad usamos `costo_x3 / costo_óptimo`: 1 significa que se conservó la solución óptima y valores mayores que 1 indican pérdida de calidad.

| Dominio | Nivel | Speedup expansiones (mediana) | Speedup segundos (mediana) | Razón de costo (mediana) | Subóptimas |
|---|---:|---:|---:|---:|---:|
| 8-puzzle | 4 | 1.000 | 1.079 | 1.000 | 0/10 |
| 8-puzzle | 8 | 1.036 | 1.242 | 1.000 | 0/10 |
| 8-puzzle | 12 | 1.252 | 0.856 | 1.000 | 1/10 |
| 8-puzzle | 16 | 0.695 | 0.489 | 1.125 | 6/10 |
| grid | 5 | 1.650 | 1.208 | 1.000 | 2/10 |
| grid | 8 | 2.458 | 2.209 | 1.059 | 5/10 |
| grid | 12 | 2.500 | 1.390 | 1.000 | 2/10 |
| grid | 16 | 3.670 | 3.301 | 1.000 | 4/10 |

El efecto depende claramente del dominio. En grid, x3 redujo considerablemente las expansiones, llegando a un speedup mediano de 3.67× en nivel 16. En el 8-puzzle difícil ocurrió lo contrario: en nivel 16 el speedup mediano fue 0.695×, por lo que x3 expandió más nodos, y además perdió optimalidad con frecuencia. En total, 20 de las 80 instancias fueron subóptimas. El peor caso fue `8puzzle-16-07`: Manhattan encontró costo 16 con 99 expansiones, mientras x3 produjo costo 24 con 261 expansiones, una pérdida de costo del 50 %.

**Conclusión de la figura:** inflar Manhattan puede acelerar considerablemente la búsqueda, especialmente en grid, pero no garantiza menos trabajo ni optimalidad; el intercambio entre velocidad y calidad depende del dominio y de la instancia.

### 3.4 Factor de ramificación efectivo b* *(Daniel)*

Resolvimos N + 1 = 1 + b* + … + (b*)^d por bisección, con N = nodos expandidos y d = longitud de la solución (`results/branching_resumen.csv`, `fig/branching.png`).

| 8-puzzle, profundidad | UCS | A*-misplaced | A*-manhattan |
|---|---:|---:|---:|
| 8 | 1,78 | 1,17 | 1,08 |
| 12 | 1,70 | 1,31 | 1,17 |
| 16 | 1,67 | 1,37 | 1,22 |

Manhattan tiene el b* más cercano a 1 en todos los niveles, de forma consistente con la dominancia de la sección 3.2. En la grilla, A*-manhattan queda entre 1,15 y 1,20 y UCS entre 1,25 y 1,36. Nuestros valores son menores que la tabla típica de las slides (~2,8 para UCS a d = 12) porque nuestro motor es búsqueda de grafo: no vuelve a expandir estados repetidos. No forzamos el número de la tabla.

**Conclusión de la figura:** con mejor heurística, b* se acerca a 1, y la diferencia entre heurísticas se mantiene en todos los niveles.

## 4. Parte 2: el duelo

### 4.1 Brazo LLM: fallas por categoría y escalado *(Jalil)*

### 4.2 Reproducibilidad *(Jalil)*

### 4.3 Brazo con herramienta *(Daniel)*

## 5. Where we may have been unfair *(todos; cada uno aporta al menos un punto propio)*

- **Heurísticas ajustadas contra prompt sin ajustar.** Usamos heurísticas conocidas y probadas (Manhattan), mientras que el modelo recibió un solo prompt por dominio, escrito una vez y nunca ajustado. Un prompt con ejemplos resueltos o con "piensa paso a paso" podría rendir distinto. No lo medimos.
- **Un modelo pequeño.** `qwen2.5:3b` es el modelo que recomienda el curso, pero un modelo grande podría comportarse muy distinto. Nuestra evidencia no dice nada sobre él.
- **Distribución de instancias.** Los bancos del curso son pequeños (grillas de hasta 16×16, profundidad 16 como máximo) y no tienen paredes. Favorecen a los algoritmos clásicos, que resuelven todo en milisegundos. Además, el validador revisa paredes que este banco nunca pone a prueba.
- **Tiempo de desarrollo.** No contamos las horas que nos tomó escribir el motor, las heurísticas y el validador, ni las del prompt. Si se contaran, el costo del sistema clásico sería mucho mayor que sus milisegundos de ejecución.
- **Máquinas distintas.** La Parte 1 se midió en una laptop Intel y los brazos LLM en una laptop con GPU. Las latencias de un sistema y otro no son comparables entre sí en términos absolutos.
- **Las respuestas que no terminan cuentan como falla.** Sin un tope de tokens, un bucle del modelo cuesta 300 s y se clasifica como `no_termina`. Con un tope, esas instancias seguirían fallando, pero mucho más rápido: la latencia del LLM que reportamos depende de esa decisión.

**Andretty:** La comparación de Manhattan con Manhattan ×3 no representa dos algoritmos con las mismas garantías. Multiplicar la heurística por 3 rompe intencionalmente la admisibilidad y favorece una búsqueda más agresiva, por lo que sería injusto comparar solo expansiones o tiempo ignorando el costo de las soluciones. Por eso reportamos ambas dimensiones: eficiencia y pérdida de calidad.

## 6. Lo que nuestra evidencia no permite afirmar *(todos)*

**Andretty:** Nuestros resultados no permiten afirmar que Manhattan vaya a dominar a misplaced en cualquier implementación o conjunto de problemas, sino que observamos esa dominancia en las 40 instancias del 8-puzzle evaluadas. Tampoco podemos afirmar que inflar una heurística por 3 siempre mejore el rendimiento. En nuestros experimentos el efecto dependió del dominio y del nivel: x3 redujo considerablemente las expansiones en varias grillas, pero en el 8-puzzle de nivel 16 llegó a expandir más nodos y a producir soluciones subóptimas. Por tanto, estos resultados muestran el comportamiento en nuestros bancos y condiciones experimentales, no una garantía general sobre cualquier problema de búsqueda.
