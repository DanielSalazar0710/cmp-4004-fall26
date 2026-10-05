# Checklist de calificación — Duel 1

Construida desde la tabla de calificación de la consigna, `resources/duel-scorecard.md` y la lista "Common ways to lose points". Marcamos `[x]` solo cuando el archivo que lo prueba existe.

## Tabla del profe

| Criterio | Peso | Qué lo prueba en nuestra entrega | Responsable |
|---|---|---|---|
| Implementaciones correctas y pruebas que pasan | 25 % | `code/tests/test_group.py`, `test_heuristicas.py` y `test_validador.py` en verde | Daniel, Andretty, Jalil |
| Protocolo experimental (tamaños, instancias, varianza) | 25 % | 4 niveles × 10 instancias × 2 dominios; timeout de 30 s declarado; medianas e IQR | Daniel (benchmark), Andretty (resumen) |
| Calidad del análisis: ¿las conclusiones se siguen? | 25 % | análisis 1–4, fallas del LLM, leyendas de figura que dicen qué concluir | todos |
| Scorecard completo y preciso en el eje 2 (garantías) | 15 % | tabla de 3 columnas con garantías **condicionales** | Daniel |
| Sección de honestidad | 10 % | "Where we may have been unfair" con fallas reales de nuestro experimento | todos |

## Parte 1 — clásico (40 %)
- [x] Por algoritmo y dominio: costo, longitud, expansiones, frontera máxima y tiempo (`results/parte1_mediciones.csv`)
- [x] 4 niveles por dominio, 10 instancias por nivel, medianas e IQR (`results/resumen_parte1.csv`)
- [x] Timeout duro declarado (30 s) y timeouts reportados como timeouts
- [x] Análisis 1: UCS = A* admisible en costo, y la instancia donde BFS es subóptimo (`results/optimalidad.csv`, `results/bfs_suboptimo.md`)
- [x] Análisis 2: dominancia de Manhattan sobre misplaced en **cada** instancia (`results/dominancia.csv`, `fig/dominancia.png`)
- [x] Análisis 3: h×3 con speedup **y** pérdida de calidad (`results/inflado_x3.csv`, `fig/inflado_x3.png`)
- [x] Análisis 4: b* de A* por heurística (`results/branching.csv`, `fig/branching.png`)

## Parte 2 — duelo (40 %)
- [x] Validador propio: legalidad (contiguo, dentro, sin paredes), costo aritmético y optimalidad contra A*
- [x] Tres fallas contadas por separado: illegal, suboptimal y wrong_cost (además, malformed como modo de falla)
- [x] Reproducibilidad: 1 instancia, 5 llamadas idénticas **sin caché**, conteo de respuestas distintas
- [x] Gráfico de escalado: tasa de óptimos contra tamaño, 4 tamaños y los 3 sistemas (`fig/escalado_optimalidad.png`)
- [x] Brazo con herramienta medido como tercer sistema (`results/herramienta_respuestas.csv`)
- [x] `.llm_cache/` versionado

## Parte 3 — REPORT.md (20 %)
- [x] 2 000 palabras como máximo (contarlas antes de entregar)
- [x] Scorecard con 8 ejes × 3 columnas y una columna de evidencia que apunte a archivos
- [x] Al menos 3 figuras, cada una con una leyenda que diga qué concluir
- [x] "Where we may have been unfair": ¿heurística ajustada contra prompt sin ajustar? ¿distribución de instancias favorable a un lado? ¿contamos nuestro tiempo de desarrollo? ¿modelo de 3B en CPU? ¿grillas sin paredes? ¿latencia medida en laptops distintas?
- [x] Lo que la evidencia **no** permite afirmar (por ejemplo, nada sobre tamaños mayores a 16)
- [ ] `AI_LOG.md` completo y reflexivo, con entradas de los tres (falta la de Jalil y el "¿lo entendí?" de Daniel)

## Formas de perder puntos (de la consigna)
- [x] Ninguna medición de una sola instancia
- [x] Nunca solo promedios: siempre con varianza
- [x] Más de un tamaño, para poder hablar de escalado
- [x] El LLM nunca valida al LLM
- [x] BFS "óptimo" solo con la condición de costos uniformes
- [x] La honestidad no dice "fuimos justos"

## Scorecard: cómo se puntúa cada eje (0–4)
Para llegar a 4 en un eje necesitamos medir en varias instancias **y** varios tamaños, con varianza y una limitación declarada. Llevamos todos los ejes a ese nivel cuando se pueda:

| Eje | Cómo llegamos a 4 |
|---|---|
| 1 Corrección | % correct por nivel en las 80 instancias, por sistema |
| 2 Garantía | prosa condicional: "A* devuelve costo mínimo **si** h es admisible; nada sobre tiempo"; "LLM: ninguna"; "herramienta: óptimo **si** el modelo llama bien y copia bien" |
| 3 Costo | expansiones (mediana [IQR]) y tokens de entrada y salida (mediana [IQR]) por nivel |
| 4 Latencia | mediana y p95 de segundos por instancia, por nivel |
| 5 Reproducibilidad | respuestas distintas en 5 llamadas idénticas (clásico: 1, por construcción, pero medido) |
| 6 Escalado | la curva de 4 tamaños, no un punto |
| 7 Interpretabilidad | certificado verificable: camino + costo recalculado por el validador |
| 8 Modo de falla | timeouts (clásico), wrong-but-confident, malformed y JSON inválido (herramienta), con conteos |
