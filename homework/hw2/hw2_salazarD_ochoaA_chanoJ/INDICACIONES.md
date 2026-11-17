# HW2 · The Formalizer · Indicaciones del equipo

**Equipo:** Daniel Salazar, Andretty Ochoa y Jalil Chano
**Consigna del profe:** [`referencias/hw2.md`](referencias/hw2.md) (manda sobre todo lo de aquí) · **Scorecard:** [`referencias/duel-scorecard.md`](referencias/duel-scorecard.md)
**Rama:** `hw1-salazarD` en https://github.com/DanielSalazar0710/cmp-4004-fall26/tree/hw1-salazarD/homework/hw2/hw2_salazarD_ochoaA_chanoJ
**Entrega del deber: mié 18 nov.** Sus partes me las mandan **mañana miércoles 18 hasta las 13:00** (sección 5).

Léanlo completo antes de empezar. Ya dejé hecha y probada la base: el motor CSP, el formato de los problemas con 3 ejemplos verificados, el cliente del LLM con caché, el formato de los CSV, el brazo A y el verificador del dataset. Cada uno completa **solo sus archivos**. Así nadie espera a nadie y nadie pisa el trabajo de otro.

---

## 0. Lo que todos deben saber

### Qué estamos haciendo
Probamos la arquitectura de Logic-LM, LINC y LLM-Modulo: **el LLM traduce el problema a un modelo formal y un solver lo resuelve**. Elegimos **CSP**, que es lo que vimos en el studio de la semana 6, y medimos cuatro brazos sobre los mismos problemas:

| Brazo | Qué hace | Quién |
|---|---|---|
| **A, a mano** | nuestro modelo CSP escrito a mano → solver. Es el techo y sirve de verdad base | Andretty (los modelos) |
| **B, híbrido** | el LLM escribe el modelo CSP → solver | Daniel |
| **B′, con refinamiento** | igual que B, pero si el solver da error se lo devolvemos al LLM, máximo 3 veces | Daniel |
| **C, directo** | el LLM responde directo desde el enunciado | Jalil |

- **Modelo:** `qwen2.5:3b` en Ollama, el del curso. Temperatura 0.7 y **3 semillas (0, 1, 2)** por problema para medir varianza. Todo está en [`code/config.py`](code/config.py); no lo cambien sin avisar.
- **Dataset:** 21 problemas propios, 7 fáciles, 7 medios y 7 difíciles (el profe pide al menos 20). La dificultad se mide por el **número de variables** del modelo CSP: fácil ≤ 8, medio de 9 a 15, difícil ≥ 16.
- **Lo más importante del deber:** la taxonomía de errores del brazo B y la columna "¿se detecta sin la respuesta correcta?". Un sistema cuyos errores se anuncian solos se puede usar en la vida real. Uno cuyos errores son silenciosos, no.

### Cómo es un modelo CSP en nuestro formato
Lo usan el brazo A (escrito a mano) y el brazo B (escrito por el LLM). Las claves van en inglés, como en el studio:

```json
{"variables": {"Ana": [1, 2, 3], "Bruno": [1, 2, 3], "Red": [1, 2, 3]},
 "constraints": [
   {"type": "alldiff", "vars": ["Ana", "Bruno", "Carla"]},
   {"type": "eq",  "a": "Ana", "b": "Red"},
   {"type": "eq",  "a": "Carla", "b": 1},
   {"type": "neq", "a": "Blue", "b": 3},
   {"type": "lt",  "a": "Ana", "b": "Bruno"},
   {"type": "gt",  "a": "Ana", "b": "Bruno"},
   {"type": "adj", "a": "Ana", "b": "Bruno"},
   {"type": "offset", "a": "Bruno", "b": "Green", "k": 1}
 ]}
```

| Tipo | Significa | Ejemplo en inglés |
|---|---|---|
| `alldiff` | todas distintas | "each lives in a different house" |
| `eq` | iguales: misma casa, o la variable vale ese número | "Ana lives in the red house", "Carla lives in house 1" |
| `neq` | distintas | "the blue house is not house 3" |
| `lt` / `gt` | menor / mayor (solo números) | "Elena lives somewhere to the right of Diego" → `gt Elena Diego` |
| `adj` | contiguas: \|a − b\| = 1 | "Ana lives next to the blue house" |
| `offset` | a − b = k | "Bruno lives immediately to the right of the green house" → `offset Bruno Green k=1` |

Regla: si `b` es el nombre de una variable, la restricción las relaciona. Si `b` es un número, fija o excluye ese valor.

### Cómo es un problema
Cada problema es un archivo `problems/<id>.json`. Abran los 3 ejemplos de [`problems/ejemplos/`](problems/ejemplos/) antes de escribir uno. Las claves están explicadas en [`code/problemas.py`](code/problemas.py):
`id`, `nivel`, `familia`, `enunciado` (en inglés), `formato_respuesta`, `modelo_mano`, `gold`, `verificacion_manual` y `fuente`.

### Preparar el entorno (una vez)
En PowerShell, con Python 3.10 o posterior:

```powershell
git clone https://github.com/DanielSalazar0710/cmp-4004-fall26.git   # si no lo tienen
cd cmp-4004-fall26
git fetch origin
git checkout hw1-salazarD
git pull origin hw1-salazarD
python -m venv .venv                       # si no lo tienen del deber 1
.venv\Scripts\activate
python -m pip install -r homework\hw2\hw2_salazarD_ochoaA_chanoJ\requirements.txt
cd homework\hw2\hw2_salazarD_ochoaA_chanoJ
$env:PYTHONIOENCODING="utf-8"
python code\tests\test_base.py             # debe decir: 8 pruebas de la base pasan
python code\verificar_dataset.py --ejemplos   # debe decir: TODO EL DATASET ESTÁ BIEN
```

Jalil necesita además Ollama con el modelo del curso:
```powershell
ollama pull qwen2.5:3b
ollama list                                # debe aparecer qwen2.5:3b
```

### Cómo trabajamos con git (igual que en el deber 1)
1. Cada uno trabaja en **su rama**, creada desde `hw1-salazarD`:
   ```powershell
   git checkout hw1-salazarD
   git pull origin hw1-salazarD
   git checkout -b hw2-ochoaA          # Andretty
   git checkout -b hw2-chanoJ          # Jalil
   ```
2. Hagan commits pequeños y con mensaje claro, por ejemplo `Agrega problemas facil-01 a facil-04`.
3. Suban su rama con `git push -u origin hw2-ochoaA` (o `hw2-chanoJ`) y abran un Pull Request **hacia `hw1-salazarD`** en mi fork. Yo lo reviso y lo integro.
4. **Solo tocan sus archivos** (sección 2 o 3). Si creen que hay que cambiar un archivo de la base, me escriben primero.
5. Antes de cada push corran sus pruebas (están en su sección). Si fallan, no suban: escríbanme.
6. Si GitHub no los deja hacer push, me mandan sus archivos por el grupo. **No suban nada a `main` ni por la web.**

### Reglas del curso que aplican a todos
- **Sin pandas.** Usamos `csv`, `json`, `numpy` y `matplotlib`.
- **Nada de usar `solution.py` ni `solution.ipynb` del repo del profe.**
- **Todo en primera persona como equipo** ("medimos", "decidimos").
- **AI_LOG honesto:** si usan una IA, anoten en su sección de [`AI_LOG.md`](AI_LOG.md) para qué la usaron y qué revisaron ustedes.
- **El brazo B′ nunca puede ver el gold.** Solo se le devuelve el mensaje del solver. Si se filtra la respuesta, el brazo queda invalidado.
- En OneDrive, si aparece un aviso para borrar archivos, pulsen **"Keep"**.

---

## 1. Base ya hecha (Daniel)

| Archivo | Qué hace |
|---|---|
| [`code/csp_motor.py`](code/csp_motor.py) | solver CSP: backtracking con forward checking y MRV (semana 6). Cuenta hasta 2 soluciones, así que distingue **única / múltiple / sin solución / timeout**, y clasifica los modelos rotos como `sintaxis` o `aridad_alcance` |
| [`code/problemas.py`](code/problemas.py) | carga los problemas, `calificar(problema, respuesta)` y `texto_formato(problema)` |
| [`code/llm_cliente.py`](code/llm_cliente.py) | `ClienteLLM().llamar(prompt, semilla)` → texto, tokens de entrada y salida, tiempo del LLM (el original aunque venga de caché). `ClienteFalso` sirve para probar sin Ollama |
| [`code/resultados.py`](code/resultados.py) | **el formato único de los CSV** (columnas, taxonomía, errores de C) |
| [`code/config.py`](code/config.py) | modelo, temperatura, semillas y límites |
| [`code/brazo_a.py`](code/brazo_a.py) | brazo A → `results/brazo_a.csv` |
| [`code/verificar_dataset.py`](code/verificar_dataset.py) | revisa cada problema: solución única, igual al gold, nivel correcto y sin fugas |
| [`code/datos_falsos.py`](code/datos_falsos.py) | CSV **falsos** con el formato real, para probar figuras y costos sin esperar las corridas |
| [`problems/ejemplos/`](problems/ejemplos/) | 3 problemas de ejemplo (uno por nivel), ya verificados. **No cuentan** en los 21 |

---

## 2. Andretty · Dataset de 21 problemas y brazo A

**Por qué es clave:** es el 15 % de "construcción del dataset" y además es la verdad base de todo. Si un gold está mal, todos los números del deber quedan mal.

### Qué entregar
1. **21 archivos** en `problems/`: `facil-01.json` … `facil-07.json`, `medio-01.json` … `medio-07.json` y `dificil-01.json` … `dificil-07.json`, con todas las claves del formato.
2. **`problems/README.md`** (media página): qué familias usaste, la métrica de dificultad (número de variables, con la tabla de los 21 que genera el verificador) y cómo verificaste cada gold a mano.
3. Tu sección en `AI_LOG.md`.

### Cómo hacerlo
1. Copia un ejemplo de `problems/ejemplos/` y cámbiale el id, el enunciado, el modelo y el gold.
2. **Mezcla al menos 3 familias**, porque así el dataset no es "21 veces el mismo acertijo":
   - **einstein:** personas, colores y mascotas en casas en fila (como los ejemplos). Usa `eq`, `adj`, `offset` y `gt`.
   - **horario:** tareas o personas en franjas 1..N, con "antes de", "justo después de", "no en la franja 2". Usa `lt`, `offset` y `neq`.
   - **coloreo:** regiones de un mapa con colores. Las variables son las regiones, los valores son colores (`"red"`, `"green"`…) y vecinos distintos se modelan con `neq`. Para que haya una sola solución, fija uno o dos colores en el enunciado.
   - Si se te ocurre otra familia que quepa en nuestros 7 tipos de restricción, también vale.
3. **Tamaños:**
   - fácil: 3 entidades × 2 atributos (6 variables) o 4 × 2 (8)
   - medio: 4 × 3 (12) o 5 × 3 (15)
   - difícil: 5 × 4 (20) o 5 × 5 (25)
4. **El enunciado:** en inglés, que el modelo lo entienda mejor, con pistas numeradas y la última línea diciendo qué responder ("For each person and color, give the house number."). **Nunca** pongas la respuesta en el enunciado.
5. **`formato_respuesta.variables`:** exactamente los mismos nombres que usas en `modelo_mano` y en `gold`, escritos igual que en el enunciado ("Red", no "red house").
6. **El truco para que la solución sea única:** primero inventa la solución (la tabla completa), después escribe pistas que sean verdad para esa tabla y corre el verificador. Si dice `multiple`, te muestra en qué variables difieren dos soluciones: agrega una pista que las distinga. Si dice `sin_solucion`, alguna pista contradice tu tabla.
7. **`verificacion_manual`:** 2 a 5 frases con el razonamiento a mano (mira los ejemplos). El profe pide verdad base **verificada a mano**, no solo por el solver.
8. **Prueba de que está bien** (debe pasar antes de cada push):
   ```powershell
   python code\verificar_dataset.py      # debe terminar en: TODO EL DATASET ESTÁ BIEN
   python code\brazo_a.py                 # debe decir: Brazo A: 63/63 correctos
   ```

### Criterios de aceptación
- [ ] 21 problemas, 7 por nivel, y `verificar_dataset.py` sin errores.
- [ ] Al menos 3 familias, y cada nivel con al menos 2 familias.
- [ ] Cada `verificacion_manual` explica el razonamiento, no dice solo "lo revisé".
- [ ] Los enunciados no son copia de internet. Si adaptas uno clásico, ponlo en `fuente`.
- [ ] `problems/README.md` listo.

### Archivos que tocas
`problems/*.json` (no `problems/ejemplos/`), `problems/README.md` y tu sección de `AI_LOG.md`.

---

## 3. Jalil · Brazo C, figuras y costos

**Por qué es clave:** el brazo C es la línea base contra la que el profe quiere comparar ("¿cuántos errores de C se detectan sin la respuesta correcta? casi ninguno"). Las figuras y el costo por respuesta correcta valen el 10 % y entran en el REPORT.

### Qué entregar
1. [`code/respuesta_c.py`](code/respuesta_c.py): `construir_prompt(problema)` y `leer_respuesta(texto, problema)`.
2. [`code/brazo_c.py`](code/brazo_c.py): `correr_problema(...)` y `main()`. Escribe `results/brazo_c.csv`.
3. [`code/costos.py`](code/costos.py): `PRECIOS` con su fuente y fecha, `costo_por_correcta(filas)` y `main()`.
4. [`code/figuras.py`](code/figuras.py): las 5 figuras de la lista del archivo.
5. Tu sección en `AI_LOG.md`.

Cada archivo trae arriba, en su descripción, el detalle de qué hacer.

### Cómo hacerlo (en este orden, y sin esperar a nadie)
1. **Respuesta C.**
   - El prompt lleva el enunciado + `texto_formato(problema)` + la instrucción de responder **solo un objeto JSON** `{"Ana": 3, ...}`.
   - Prueba 2 o 3 redacciones con los 3 ejemplos y quédate con la que mejor responda en formato. Anota en `AI_LOG.md` cuáles probaste. No vale ajustar el prompt mirando los 21 problemas finales: para eso están los ejemplos.
   - El lector usa `extraer_json` (ya hecho) y devuelve `"sin_formato"` o `"incompleta"` según el caso.
2. **Brazo C.** Sigue los pasos de la descripción de `brazo_c.py`. Pruébalo con `--falso` y después con Ollama sobre los ejemplos:
   ```powershell
   python code\brazo_c.py --falso --solo ejemplos
   python code\brazo_c.py --solo ejemplos           # con Ollama: unos minutos
   ```
   La corrida grande (21 × 3) la hacemos Daniel y yo al integrar, con tu script, apenas esté el dataset. Tú no esperas al dataset.
3. **Figuras y costos con datos falsos**, mientras esperas el dataset:
   ```powershell
   python code\datos_falsos.py
   python code\figuras.py --carpeta results\falso --salida fig\falso
   python code\costos.py --carpeta results\falso
   ```
   - La figura `precision_vs_dificultad.png` es **obligatoria**: % correcto por nivel, una línea por brazo, con barras de variación entre las 3 semillas.
   - Usa los colores y nombres de `figuras.py`, para que todas las figuras del deber se vean iguales.
   - Para los precios, busca uno de **Groq o Together AI** (lo que pide el profe), anota el enlace y la fecha y escribe qué modelo tomaste como equivalente de qwen2.5:3b.
4. **Prueba de que está bien** (debe pasar antes de cada push):
   ```powershell
   python code\tests\test_jalil.py    # debe decir: 5/5 pruebas de Jalil pasan
   ```
   Al principio fallan todas, y es normal. Van pasando a medida que completas cada archivo.

### Criterios de aceptación
- [ ] `test_jalil.py` pasa 5/5 sin Ollama.
- [ ] `results/brazo_c_ejemplos.csv` con la corrida real de los ejemplos.
- [ ] Las 5 figuras con datos falsos; las reales las genero yo con tu script al final.
- [ ] `PRECIOS` con fuente y fecha, y el costo **por respuesta correcta** (no por intento).
- [ ] Commiteas la caché `.llm_cache/` de tus corridas: es la evidencia que pide el profe.

### Archivos que tocas
`code/respuesta_c.py`, `code/brazo_c.py`, `code/costos.py`, `code/figuras.py`, `results/brazo_c*.csv`, `.llm_cache/` y tu sección de `AI_LOG.md`.

---

## 4. Daniel · Brazos B y B′, taxonomía, integración y reporte

- `code/brazo_b.py`: el prompt de traducción (con 1 o 2 ejemplos de `problems/ejemplos/` como few-shot), B (1 intento) y B′ (hasta 3 reintentos con **solo** el mensaje del solver). Cada intento queda guardado en el CSV y en la caché.
- La clasificación de cada fallo de B en las 6 categorías del profe (`resultados.TAXONOMIA`), más la revisión a mano de los que el solver no detecta ("problema equivocado").
- `taxonomy.md` con cada fallo de B, su categoría y la salida del modelo; `REPORT.md` con scorecard, figuras, análisis del refinamiento, costos, honestidad y recomendación. También el `AI_LOG.md` y la integración de los PRs.
- **Revisión de lo que suben:**
  - corro `verificar_dataset.py` y `test_jalil.py` en cada PR;
  - leo a mano una muestra de enunciados contra su `modelo_mano`;
  - reviso que el prompt de C no filtre la respuesta.
  Si algo falla, se lo comento en el PR y lo corregimos juntos.

---

## 5. Fechas y puntos de control (el deber se entrega mañana)

| Punto de control | Quién | Qué | Hasta |
|---|---|---|---|
| **PC1** | Andretty | PR con 6 problemas (2 por nivel) que pasan el verificador, para revisar el formato pronto | **hoy mar 17, 22:00** |
| **PC1** | Jalil | PR con `respuesta_c.py` + `brazo_c.py`; pasan `test_prompt_sin_fugas`, `test_lector` y `test_fila_brazo_c` | **hoy mar 17, 22:00** |
| **PC2 · entrega de su parte** | Andretty | los 21 problemas + `problems/README.md` + su AI_LOG | **mié 18, 13:00** |
| **PC2 · entrega de su parte** | Jalil | figuras y costos funcionando (`test_jalil` 5/5), corrida de ejemplos + su AI_LOG | **mié 18, 13:00** |
| **Integración** | Daniel | B y B′, corridas de todos los brazos, figuras reales, taxonomía y REPORT | mié 18, tarde |
| **Entrega** | todos | cada uno abre su PR al repo del profe con su carpeta `homework/hw2/<apellido>` | mié 18 |

Suban **apenas tengan algo que pase las pruebas**, aunque no esté todo: no esperen a la hora límite, porque las corridas con el LLM tardan horas y necesito empezar con lo que haya. Reviso cada PR al llegar y les comento ahí mismo. Si a las 13:00 falta algo, me avisan y lo completamos entre todos.
