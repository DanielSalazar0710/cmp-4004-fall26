# Duel 1 — Búsqueda clásica contra un LLM

**Equipo:** Daniel Salazar, Andretty Ochoa y Jalil Chano · CMP-4004 · USFQ

> Borrador. Cada sección indica quién la escribe. Límite: 2 000 palabras sin contar tablas ni leyendas. Las cifras salen de `results/`; ninguna se escribe a mano.

## 1. Qué medimos y cómo *(Daniel)*

Dominios, bancos (semilla 20260807), 4 niveles × 10 instancias, timeout de 30 s, máquina y modelo (`qwen2.5:3b`, temperatura 0, semilla 0).

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

## 4. Parte 2: el duelo

### 4.1 Brazo LLM: fallas por categoría y escalado *(Jalil)*

### 4.2 Reproducibilidad *(Jalil)*

### 4.3 Brazo con herramienta *(Daniel)*

## 5. Where we may have been unfair *(todos; cada uno aporta al menos un punto propio)*

**Andretty:** La comparación de Manhattan con Manhattan ×3 no representa dos algoritmos con las mismas garantías. Multiplicar la heurística por 3 rompe intencionalmente la admisibilidad y favorece una búsqueda más agresiva, por lo que sería injusto comparar solo expansiones o tiempo ignorando el costo de las soluciones. Por eso reportamos ambas dimensiones: eficiencia y pérdida de calidad.

## 6. Lo que nuestra evidencia no permite afirmar *(todos)*

**Andretty:** Nuestros resultados no permiten afirmar que Manhattan vaya a dominar a misplaced en cualquier implementación o conjunto de problemas, sino que observamos esa dominancia en las 40 instancias del 8-puzzle evaluadas. Tampoco podemos afirmar que inflar una heurística por 3 siempre mejore el rendimiento. En nuestros experimentos el efecto dependió del dominio y del nivel: x3 redujo considerablemente las expansiones en varias grillas, pero en el 8-puzzle de nivel 16 llegó a expandir más nodos y a producir soluciones subóptimas. Por tanto, estos resultados muestran el comportamiento en nuestros bancos y condiciones experimentales, no una garantía general sobre cualquier problema de búsqueda.
