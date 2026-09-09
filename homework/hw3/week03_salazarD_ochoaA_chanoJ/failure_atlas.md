# Failure Atlas — DFS: encontrar meta no garantiza calidad

**Equipo:** Salazar, Ochoa y Chano · **Semana:** 03

**Tipo:** solución válida pero muy subóptima. No es un fallo de formato ni de ejecución.

**Entrada reproducible:** `load_instances()[4][8]`, instancia 9 del grupo de profundidad 4.

**Criterio deseado:** minimizar movimientos; cada acción del 8-puzzle cuesta uno.

**Esperado con un algoritmo óptimo:** 4 movimientos.

**Observado con DFS:** 94,144 movimientos y 122,569 expansiones. Fuente: `resultados/measurements.csv`.

**Causa:** la frontera LIFO sigue una rama profunda de acuerdo con el orden fijo de acciones. El conjunto de explorados evita ciclos, pero no selecciona la ruta de menor longitud. El grafo finito todavía admite rutas muy largas.

**Reproducción:**

```python
from search import EightPuzzle, load_instances
from starter import bfs, dfs
p = EightPuzzle(load_instances()[4][8])
for name, algorithm in [('BFS', bfs), ('DFS', dfs)]:
    node, expanded = algorithm(p)
    print(name, len(node.path()), expanded)
```

**Verificación:** `verify_results.py` reproduce cada acción de las 160 soluciones, comprueba su legalidad y su llegada a la meta. Una ruta extensa puede ser válida y seguir siendo inadecuada.

**Mitigación:** escoger BFS o IDS cuando los costos son uniformes y necesitamos longitud óptima; UCS cuando varían los costos no negativos. No cambiamos DFS para ocultar la limitación: se perdería la comparación.

**Alcance:** esta instancia demuestra que DFS no garantiza optimalidad. No demuestra que DFS siempre sea lento o que siempre encuentre rutas malas; su comportamiento depende del grafo y del orden de acciones.
