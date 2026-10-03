# Duel 1 — Asignaciones del equipo

**Equipo:** Daniel Salazar, Andretty Ochoa y Jalil Chano
**Consigna:** [`referencias/hw1/hw-1-search.md`](referencias/hw1/hw-1-search.md) · **Rúbrica en checklist:** [`RUBRICA.md`](RUBRICA.md)
**Entrega:** lunes de la semana 7 (15 % de la nota). Las fechas internas están al final.

Léanlo completo antes de empezar. La base ya está hecha y probada: el motor de búsqueda, los dos bancos de instancias, el benchmark y las pruebas. Cada uno completa **solo sus archivos**, porque así nadie pisa el trabajo de otro y los CSV encajan entre sí.

---

## 0. Lo que todos deben saber

### Qué estamos midiendo
Comparamos tres sistemas sobre **las mismas 80 instancias**:

| Sistema | Qué es | Quién |
|---|---|---|
| Clásico | BFS, DFS, UCS, IDS y A* (misplaced, manhattan, manhattan×3) | Daniel (motor), Andretty (heurísticas) |
| LLM | `qwen2.5:3b` en Ollama, recibe la instancia como texto | Jalil |
| Herramienta | el mismo LLM, que puede llamar a nuestro A* con un JSON | Daniel |

- **8-puzzle:** 10 instancias por profundidad óptima 4, 8, 12 y 16 (banco del profe, week 3).
- **Grilla con terrenos:** 10 instancias por tamaño 5×5, 8×8, 12×12 y 16×16 (banco del profe, week 4). Los costos se cobran al **entrar** a una celda: `.`=1, `,`=3, `~`=8, `S`/`G`=1.
- Cada instancia tiene un id que se usa en **todos** los CSV: `8puzzle-12-03`, `grid-16-07`.

### Preparar el entorno (una vez)
Desde la raíz del repo, en PowerShell, con Python 3.10 o posterior:

```powershell
git clone https://github.com/DanielSalazar0710/cmp-4004-fall26.git   # si aún no lo tienen
cd cmp-4004-fall26
git fetch origin
git checkout hw1-salazarD
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r homework\hw1\duel1_salazarD_ochoaA_chanoJ\requirements.txt
cd homework\hw1\duel1_salazarD_ochoaA_chanoJ
$env:PYTHONIOENCODING="utf-8"
python code\tests\test_group.py        # debe decir: 7 pruebas de la base pasan
python code\benchmark.py --rapido      # corre en segundos; NO es la medición oficial
```

Jalil necesita además Ollama con el modelo del curso (`resources/setup.md`):
```powershell
ollama pull qwen2.5:3b
ollama list                            # debe aparecer qwen2.5:3b
```

### Cómo trabajamos con git
1. Cada uno trabaja en **su rama**, creada desde `hw1-salazarD`:
   ```powershell
   git checkout hw1-salazarD
   git pull origin hw1-salazarD
   git checkout -b hw1-ochoaA          # Andretty
   git checkout -b hw1-chanoJ          # Jalil
   ```
2. Hagan commits pequeños y con mensaje claro, por ejemplo `Implementa h_misplaced y h_manhattan_puzzle`.
3. Suban su rama con `git push -u origin hw1-ochoaA` (o `hw1-chanoJ`) y abran un Pull Request **hacia `hw1-salazarD`** en el fork de Daniel. Daniel lo revisa y lo integra.
4. Si GitHub no les deja hacer push, avisen a Daniel por el chat del grupo y envíenle sus archivos. **No suban archivos a `main` por la web.**
5. Antes de cada commit:
   ```powershell
   python code\tests\test_group.py
   ```
   Corran también la prueba de su parte. Si una prueba de la base falla, no la "arreglen" debilitándola: avisen.

### Reglas que no se negocian (de la rúbrica y del profe)
- **No editen** nada de `code/curso/` ni de `code/aicourse/`. Son archivos del curso y sus huellas están en `SOURCE_MANIFEST.json`.
- **No usen pandas.** En la laptop de Daniel, Windows bloquea sus DLL y el notebook final no correría. Usen `code/estadistica.py` (`leer_csv`, `mediana_iqr`, `agrupar`) y `numpy`.
- **Medianas e IQR, nunca solo promedios.** Nada de "A* tardó 0,03 s" con una sola instancia.
- **Un timeout es un timeout.** No es "no resolvió" ni "falló": se cuenta y se reporta aparte.
- **Nunca le pregunten al LLM si su respuesta es correcta.** Lo decide nuestro validador.
- **No digan "BFS es óptimo"** sin la condición: solo con costos uniformes.
- Los CSV se generan **con código**. Nada se copia ni se edita a mano.
- Todas las figuras se guardan en `fig/` como PNG, con títulos y ejes en español, unidades y `n` por punto.
- Escriban en español, en primera persona del plural ("medimos", "encontramos").

### AI_LOG (obligatorio para cada uno)
Si usan ChatGPT, Claude, Copilot o cualquier otra IA, agreguen una entrada en `AI_LOG.md` con el formato de `referencias/resources/ai-policy.md`: herramienta, qué pidieron, qué recibieron, qué hicieron con eso y **¿lo entendí?** Escribir "no" está permitido. Escribir "sí" sin poder defenderlo en el checkpoint, no. Una entrada vacía o hueca cuenta como entrega parcial.

---

## 1. Daniel Salazar — base, análisis 1 y 4, brazo con herramienta, integración

Ya hecho (base, con Claude Code): `code/motor.py`, `code/dominios.py`, `code/benchmark.py`, `code/estadistica.py`, `code/rutas.py` y `code/tests/test_group.py`.

Pendiente:
- `code/analisis_optimalidad.py`
  - **Análisis 1:** UCS = A* admisible en costo en las 80 instancias. Mostrar el caso donde BFS es subóptimo en la grilla (ya aparece en `grid-8-00`: BFS 15 vs. óptimo 13).
  - **Análisis 4:** b* de A* con cada heurística, por nivel.
- `code/herramienta.py`: brazo con herramienta (JSON → nuestro A* → respuesta), validado con el validador de Jalil.
- Corrida oficial de `benchmark.py` (timeout 30 s) cuando las heurísticas de Andretty estén integradas.
- `REPORT.md`: scorecard de 3 columnas, integración de secciones y límite de 2 000 palabras.
- Al final, con Claude: el notebook de presentación y completar lo que haya quedado pendiente.

---

## 2. Andretty Ochoa — heurísticas, análisis 2 y 3, figuras de la Parte 1

**Peso en la rúbrica:** implementaciones correctas con pruebas (25 %) y análisis (25 %).

### Archivos tuyos
- `code/heuristicas.py`: completar los `TODO`.
- `code/analisis_heuristicas.py`: completar los `TODO`.
- `code/tests/test_heuristicas.py`: ya trae 6 pruebas de aceptación. Puedes agregar más; no borres ni debilites ninguna.
- Tu sección en `REPORT.md` (marcada con tu nombre) y tus entradas en `DECISION_NOTES.md` y `AI_LOG.md`.

### Paso 1 — Heurísticas
Firma obligatoria: `h(problema, estado) -> número`.

| Función | Qué calcula | Cuidado con |
|---|---|---|
| `h_misplaced` | fichas 1..8 fuera de lugar | **no** contar el blanco (0): rompería la admisibilidad |
| `h_manhattan_puzzle` | Σ \|fila−fila_meta\| + \|col−col_meta\| de las fichas 1..8 | ubicar la meta con `problema.goal`, sin suponer posiciones; no contar el blanco |
| `h_manhattan_grid` | Manhattan × `MIN_COST` hasta `problema.goal` | el estado es `(fila, col)`; es admisible porque cada paso cuesta ≥ `MIN_COST` |
| `inflar(h, 3)` | devuelve una función nueva = 3 × h | ponerle `__name__` terminado en `_x3` |

Referencias: el notebook `referencias/notebooks/week-04-astar-heuristics.ipynb` (secciones de `h_misplaced`, `h_manhattan` y `h_bad`) y `referencias/studios/week-04/README.md`.

Verifica con:
```powershell
python code\tests\test_heuristicas.py     # debe decir 6/6 pasan
python code\benchmark.py --rapido         # ya no deben salir avisos de "sin implementar"
```
**Haz commit y push apenas pase el paso 1.** Daniel lo necesita para la corrida oficial.

### Paso 2 — Análisis (solo lee `results/parte1_mediciones.csv`)
Mientras Daniel no haga la corrida oficial, genera tu propio CSV con `python code\benchmark.py`. Tarda unos minutos y escribe ese mismo archivo.

1. `resumen_parte1()` → `results/resumen_parte1.csv`. Por dominio, nivel y config: n, resueltas, timeouts y mediana [q1, q3] de expansions, max_frontier, seconds y cost. Usa `estadistica.mediana_iqr`. Los timeouts **no** entran en las medianas de costo; se cuentan aparte.
2. `dominancia()` → `results/dominancia.csv`. En **cada una** de las 40 instancias del 8-puzzle, compara las expansiones de A*-manhattan con las de A*-misplaced. El enunciado dice que manhattan debe expandir **lo mismo o menos en todas**. Si encuentras una instancia donde no pasa, **no la escondas**. Puede ser un bug en una heurística o un empate de `f` que se resolvió en otro orden. Investígala y documenta qué era en `DECISION_NOTES.md`; esa investigación vale puntos.
3. `inflado_x3()` → `results/inflado_x3.csv`. Compara A*-manhattan_x3 con A*-manhattan en **ambos** dominios. Reporta **los dos números** por nivel, o el análisis queda incompleto:
   - speedup = expansiones(manhattan) / expansiones(x3), y también en segundos;
   - pérdida de calidad = costo(x3) / costo óptimo, y cuántas instancias quedaron subóptimas.

   Señala la peor instancia. En el 8-puzzle, x3 puede no perder calidad; en la grilla sí debería, porque el `h_bad` del profe ya lo mostraba.
4. `figuras()`:
   - `fig/expansiones_vs_nivel.png`: eje y **logarítmico**, una curva por config, barras de IQR y un panel por dominio.
   - `fig/dominancia.png`: dispersión de expansiones misplaced (x) contra manhattan (y), con la diagonal y = x. Ningún punto debería quedar sobre la diagonal.
   - `fig/inflado_x3.png`: speedup y pérdida de calidad por nivel.

   Cada figura necesita una **leyenda de conclusión** para el REPORT: una oración que diga qué debe concluir el lector, por ejemplo "Manhattan expande entre 3 y 40 veces menos que misplaced en las 40 instancias".

### Paso 3 — Texto
En `REPORT.md`, sección "Análisis 2 y 3" (alrededor de 400 palabras): qué medimos, la tabla corta, las figuras con su conclusión y **qué no podemos afirmar**. Por ejemplo, x3 en estas grillas no dice nada de grillas con paredes. Agrega en "Where we may have been unfair" al menos un punto propio. Por ejemplo: probamos heurísticas conocidas, ¿las ajustamos mirando los resultados?

### Para la exposición
Prepárate para explicar a mano por qué misplaced y Manhattan son admisibles, por qué Manhattan domina a misplaced y por qué inflar h acelera la búsqueda pero rompe la garantía de optimalidad. El checkpoint es individual y sin apuntes.

---

## 3. Jalil Chano — brazo LLM, validador, reproducibilidad y escalado

**Peso en la rúbrica:** es el 40 % de la Parte 2 y alimenta el scorecard.

### Archivos tuyos
- `code/validador.py`: completar los `TODO`.
- `code/duelo_llm.py`: completar los `TODO`.
- `code/tests/test_validador.py`: ya trae 7 pruebas de aceptación. Puedes agregar más; no borres ni debilites ninguna.
- `.llm_cache/`: se versiona **entero**, porque es la evidencia de las llamadas.
- Tu sección en `REPORT.md` y tus entradas en `DECISION_NOTES.md` y `AI_LOG.md`.

### Paso 1 — Validador (sin LLM todavía)
El enunciado exige "a validator you wrote". El `duel.py` del curso (`code/curso/week04/duel.py`) sirve de **referencia**, pero no basta: no revisa paredes ni el 8-puzzle. Escribe el tuyo:

- `recorrer_grid` y `recorrer_puzzle`: caminan el camino paso a paso. Revisan símbolos válidos (U/D/L/R), que no se salga del tablero, que no entre a una pared `#` y que termine en la meta. Suman el costo real: en la grilla, el de cada celda a la que se **entra**; en el puzzle, 1 por movimiento. Las letras del puzzle mueven el **blanco**.
- `costo_optimo`: el óptimo con **nuestro** A* (`motor.resolver(..., "astar", h=...)`, o `"ucs"` mientras no estén las heurísticas). Guarda los resultados en una caché por id, porque se piden muchas veces.
- `validar`: clasifica en `malformed → illegal → suboptimal → wrong_cost → correct`, en ese orden. Las tres fallas del enunciado son **illegal**, **suboptimal** y **wrong_cost**, y se cuentan **por separado**.
- `extraer_respuesta`: lee `PATH:` y `COST:`. Registra aparte si tuviste que ser tolerante (por ejemplo `PATH: U, R, D`), igual que la lectura estricta y la tolerante de week 5.

Verifica con:
```powershell
python code\tests\test_validador.py       # debe decir 7/7 pasan
```
**Haz commit y push apenas pase.** Daniel lo usa para el brazo con herramienta.

### Paso 2 — Brazo LLM
- **Grilla:** usa **exactamente** `duel.prompt_for(grid)` del curso. No lo cambies.
- **8-puzzle:** escribe un prompt con el mismo formato de salida (`PATH:` / `COST:`). Debe explicar el tablero, la meta, que las letras mueven el blanco y que cada movimiento cuesta 1. Escríbelo **una vez**, antes de ver resultados. Si lo cambias, guarda la versión anterior y lo contamos en la sección de honestidad.
- Cliente:
  ```python
  from aicourse import LLM
  llm = LLM(backend="ollama", model="qwen2.5:3b", cache_dir=str(rutas.CACHE))
  r = llm.complete(prompt)                     # temperatura 0, semilla 0
  r.text, r.cached, r.elapsed, r.meta          # meta trae eval_count = tokens de salida
  ```
- Corre las 80 instancias (40 + 40) con temperatura 0 y semilla 0. Escribe `results/llm_respuestas.csv` con las columnas del docstring de `duelo_llm.py`, y agrega cada llamada a `results/llm_calls.jsonl` con la marca `cached`.
- Empieza con `--por-nivel 2` para probar. La corrida completa con el modelo 3b en CPU puede tardar bastante; déjala corriendo.
- **No reintentes ni corrijas a mano** una respuesta mala: se clasifica tal como salió.

### Paso 3 — Reproducibilidad
Una instancia (sugerencia: `grid-8-00`) y **cinco llamadas idénticas**: mismo prompt, temperatura y semilla.
- **Trampa:** con la caché encendida, las llamadas 2 a 5 salen de la caché y el resultado es falso. Ya nos pasó en week 2. Usa `llm.complete(prompt, use_cache=False)` y guarda cada transcripción tú mismo en `.llm_cache/repro/grid-8-00_llamada_1.json`, ..., `_5.json`.
- Cuenta cuántas respuestas distintas salen y guárdalo en `results/llm_reproducibilidad.csv`. Si las 5 son iguales, ese también es un resultado. En ese caso, como complemento, repite con temperatura 0.7 y semillas 1 a 5, igual que en week 5, y reporta ambos.

### Paso 4 — Figura de escalado
`fig/escalado_optimalidad.png`: porcentaje de respuestas `correct` contra el nivel (4 tamaños), una curva por sistema (clásico A*, LLM y herramienta cuando exista `results/herramienta_respuestas.csv`) y un panel por dominio. Muestra `n` por punto. Agrega un gráfico de barras apiladas con las 5 categorías por nivel (`fig/fallas_llm.png`).

### Paso 5 — Texto
En `REPORT.md`, sección "Parte 2: brazo LLM" (alrededor de 400 palabras): conteo de las tres fallas por nivel, reproducibilidad, la figura con su conclusión y la frase obligatoria sobre **lo que no dice la evidencia**. Por ejemplo: "resolvió X/10 en 8×8; eso no dice nada sobre 20×20". Agrega en "Where we may have been unfair" al menos dos puntos propios: un prompt sin ajustar contra heurísticas ajustadas, un modelo de 3B en CPU que no representa a modelos grandes, y las grillas sin paredes.

### Para la exposición
Prepárate para explicar por qué nunca usamos al LLM para validarse a sí mismo, qué diferencia hay entre `suboptimal` y `wrong_cost`, y por qué cinco llamadas idénticas con caché no miden reproducibilidad.

---

## 4. Fechas internas (Daniel puede ajustarlas)

| Hito | Qué | Cuándo |
|---|---|---|
| 1 | Heurísticas (Andretty) y validador (Jalil) con sus pruebas en verde, en su rama con PR | sábado, 22:00 |
| 2 | CSV, figuras y texto de cada sección en el PR | domingo, 18:00 |
| 3 | Integración, scorecard, REPORT final y notebook de presentación (Daniel y Claude) | domingo en la noche |

Si algo no alcanza, **avisen apenas lo sepan**. Daniel y Claude lo completan, y en `AI_LOG.md` y el README queda registrado quién hizo qué.
