# Week 03 — Salazar, Ochoa y Chano

## Presentación principal

Abrimos el [notebook de presentación](week03_salazarD_ochoaA_chanoJ.ipynb) junto a [starter.py](starter.py).
El notebook contiene las explicaciones en español y resultados guardados de una ejecución completa.
También incluimos la versión HTML para presentar sin iniciar un kernel.

## Ejecución

Desde esta carpeta, con Python 3.10 o posterior:

```powershell
python -m pip install -r requirements.txt
python test_search.py
python test_group.py
python starter.py
jupyter notebook week03_salazarD_ochoaA_chanoJ.ipynb
```

En VS Code también podemos abrir el notebook y seleccionar un kernel de Python con estas dependencias.
Para regenerar las 160 mediciones y comprobar sus rutas:

```powershell
python experiments.py
python verify_results.py
```

En el notebook usamos `REPETIR_MEDICION=False` para leer una corrida ya guardada, comprobando las huellas del código y del banco. Con `True` recalculamos. Si modificamos el código, debemos regenerar los resultados y ejecutar nuevamente el notebook.

## Qué contiene

- `starter.py`: implementación sobre la plantilla del profesor.
- `week03_salazarD_ochoaA_chanoJ.ipynb`: presentación ejecutable del grupo.
- `week03_salazarD_ochoaA_chanoJ.html`: versión de lectura con resultados.
- `search.py`, `test_search.py`, `instances.json`, `_generate_instances.py`: originales intactos.
- `experiments.py`: guardado de datos, resumen y gráfica logarítmica.
- `test_group.py`: seis comprobaciones adicionales.
- `verify_results.py`: revisión independiente de profundidades y de las 160 rutas completas.
- `resultados/measurements.csv`: expansiones y longitud por instancia y algoritmo.
- `resultados/summary.csv`: medias, medianas y rangos.
- `resultados/scaling.png` y `.svg`: gráfica de escalamiento.
- `resultados/metadata.json`: fecha, entorno, duración total y huellas de integridad.
- `resultados/verification.json`: verificación de profundidades y rutas.
- `DECISION_NOTES.md`: razones de implementación y límites de interpretación.
- `GUIA_EXPOSICION.md`: orden para presentar y preguntas de ensayo.
- `failure_atlas.md`: fallo de calidad de DFS con evidencia reproducible.
- `AI_LOG.md`: asistencia utilizada y revisión personal pendiente.
- `SOURCE_MANIFEST.json`: revisión del repositorio y huellas de los originales.
- `referencias/`: materiales del profesor conservados en inglés.

## Resultados principales

Los cinco tests originales y los seis adicionales pasan. BFS, UCS e IDS obtienen longitudes óptimas en las 40 instancias. A profundidad 16, BFS y UCS promedian 9 401,4 expansiones; IDS, 24 432,6; DFS, 33 434,4 y soluciones de longitud media 30 136,8.

No interpretamos esos valores como garantía universal. El DFS usado conserva `explored`; no atribuimos a esa implementación el ahorro de memoria de un DFS de árbol sin historial global. La extrapolación a profundidad 24 es un ejercicio, no un benchmark ejecutado.

Las rutas `weeks/` y `projects/` citadas por el profesor no están en la revisión descargada; seguimos el studio y los materiales disponibles. Esta entrega se comparte en la rama week03-salazarD del fork de Daniel Salazar.
