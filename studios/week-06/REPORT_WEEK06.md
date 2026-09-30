# Week 06 — CSP y comparación A/B/C

**Estudiante:** Andretty Ochoa  
**Curso:** CMP-4004  
**Fecha:** 30 de septiembre de 2026

## 1. Horario escolar

Se modelaron seis actividades como variables y los períodos 1–6 como dominios. Sports se restringió a los períodos 1–3. Todas las actividades son vecinas entre sí para exigir períodos distintos.

Horario obtenido: Math 2, English 3, Science 4, Sports 1, Art 5 y Music 6. Cumple ambas restricciones.

| Configuración | Llamadas | Tiempo observado | Resuelto |
|---|---:|---:|---|
| Backtracking básico | 8 | 0.0001 s | Sí |
| + Forward checking | 7 | 0.0001 s | Sí |
| + MRV | 7 | 0.0001 s | Sí |
| + LCV | 7 | 0.0003 s | Sí |
| + AC-3 preprocessing | 7 | 0.0002 s | Sí |

Las configuraciones son las del helper: LCV y AC-3 se añaden por separado a FC+MRV. Forward checking redujo una llamada. Las demás técnicas no redujeron más las llamadas en este horario. Los tiempos proceden de una ejecución y son demasiado pequeños para establecer diferencias fiables de rendimiento.

El estudiante reportó que todas las pruebas de test_csp.py pasaron. La verificación del banco produjo ALL 20 PUZZLES SOUND. No se registraron aquí contadores propios para las pruebas de Sudoku.

## 2. Método

Se evaluaron los 15 acertijos p06–p20. Los cinco primeros se reservaron para ejemplos y desarrollo. Entorno: Windows, Python 3.13.2, Ollama 0.34.4, qwen2.5:3b sobre CPU. Configuración de las llamadas: temperature=0, seed=42, num_ctx=4096, num_predict=2048.

- A: modelos explícitos de dominios y restricciones, construidos con asistencia de ChatGPT, revisables en run_arm_a.py; solver del curso con FC+MRV. El código no carga el campo spec para construirlos. Durante la asistencia se consultó el banco completo, que incluye las codificaciones y respuestas de referencia. Por ello A es un control asistido y revisado contra material de referencia, no una medición independiente de modelado humano a ciegas.
- B: traducción del acertijo a CSP por el modelo local, seguida del solver. El mensaje final contiene reglas de formato y el ejemplo p01. Se comparó un intento con hasta tres intentos totales. Solo se reintenta ante malformed_json o valid_no_solution, devolviendo información del error. gold se usa para evaluar y no se envía al modelo.
- C: respuesta directa del mismo modelo, solicitada como diccionario JSON, sin solver ni reintentos. Se compara con gold después de generar la respuesta.

Las respuestas se guardaron en .llm_cache. B sin/con refinamiento reutiliza exactamente la primera respuesta. Los mensajes de B y C no son idénticos: corresponden a tareas distintas y B incluye un ejemplo completo de traducción. Los resultados caracterizan estas configuraciones concretas, no aíslan el efecto del solver ni permiten generalizar a todos los LLM.

## 3. Scorecard principal: comparación estricta

| Métrica | A | B sin refinamiento | B con refinamiento | C |
|---|---:|---:|---:|---:|
| Acertijos | 15 | 15 | 15 | 15 |
| Aciertos | 15 | 7 | 7 | 7 |
| Tasa de acierto | 100 % | 46.7 % | 46.7 % | 46.7 % |

El criterio automático comprueba nombres, valores y tipos frente a gold. En B y C compara las claves esperadas; no rechaza por sí solo claves adicionales. El efecto del refinamiento en la evaluación final fue de **0 puntos porcentuales**. p17 fue el único caso de B que llegó a tres intentos; siguió sin solución. No se midieron tiempos globales de A/B/C.

### Taxonomía de B

| Categoría | Sin refinamiento | Con refinamiento |
|---|---:|---:|
| correct | 7 | 7 |
| malformed_json | 0 | 0 |
| valid_json_wrong_model | 7 | 7 |
| valid_no_solution | 1 | 1 |
| timeout del solver | 0 | 0 |

Correctos: p09, p10, p11, p12, p13, p14, p19. Wrong_model: p06, p07, p08, p15, p16, p18, p20. Sin solución: p17. La etiqueta wrong_model significa desacuerdo con la representación gold; no demuestra por sí sola que la asignación sea semánticamente incorrecta. C tuvo siete correctos, ocho incorrectos estrictos y cero errores de formato JSON.

## 4. Auditoría de representación

La revisión posterior distingue errores de contenido de diferencias de representación, sin sobrescribir los CSV originales ni cambiar la métrica principal.

| Brazo | Casos adicionales equivalentes en significado | Total tras revisión de asignaciones |
|---|---|---:|
| B | p06: nombres y valores como black_car/spot1; p08: HouseA frente a A; p16: mapeo escritorio→persona en lugar de persona→escritorio | 10/15 (66.7 %) |
| C | p06, p07, p09, p12: números como cadenas; p10: nombres completos de días | 12/15 (80 %) |

Esta es una auditoría posterior de las respuestas, no una segunda evaluación automática predefinida. En B, una asignación equivalente no prueba que todas las restricciones del CSP generado sean fieles al enunciado. C presenta errores de contenido en p13, p16 y p18. Su tasa estricta de 46.7 % subestima las asignaciones correctas en significado debido a las diferencias de formato.

## 5. Desarrollo e incidencias

El mensaje original indujo al modelo a copiar marcadores como name/domain/values. En los cinco ejemplos, el primer intento obtuvo 0/5 y el refinamiento 1/5. Una ejecución parcial sobre los acertijos de evaluación también mostró fallos de estructura; se interrumpió y se aclaró el mensaje usando p01. Después se ejecutaron los 15 con esa configuración fija. Esta adaptación se hizo tras observar fallos de evaluación: los 15 no constituyen un conjunto completamente intacto respecto al desarrollo del mensaje.

Se capturaron errores de estructura no manejados por el clasificador proporcionado dentro de starter.py, sin modificar logic_lm.py. Un archivo de caché no válido se conservó con extensión .invalid y se regeneró esa respuesta. Se implementó escritura mediante archivo temporal. También se reinició Ollama tras un error de conexión. Estos incidentes de infraestructura no se contaron como timeout del solver.

## 6. Conclusión

Los modelos explícitos de A resolvieron los 15 casos. B y C empataron bajo el criterio automático estricto; la auditoría posterior encontró más asignaciones semánticamente correctas en C. En esta evaluación, los reintentos de B no mejoraron el resultado final: los desacuerdos con gold no activan correcciones y el caso sin solución persistió.

El solver garantiza el cumplimiento del modelo formal recibido, bajo sus condiciones y límites; no garantiza que la traducción represente fielmente el enunciado. Algunos errores de B son observables por estructura inválida o ausencia de solución, pero otros generan soluciones y requieren comprobación externa. Por ello no se puede afirmar que todos los fallos de B sean visibles automáticamente.

## Evidencia y fuentes

- Código local: starter.py, run_experiment.py, run_arm_a.py y run_arm_c.py.
- Datos medidos por el estudiante: results_arm_a.csv, results_arm_b.csv, results_arm_c.csv y .llm_cache.
- Material del curso: https://github.com/aproano2/cmp-4004-fall26/tree/main/studios/week-06
- Política de IA: https://github.com/aproano2/cmp-4004-fall26/blob/main/resources/ai-policy.md
- Documentación de la API: https://docs.ollama.com/api/generate

Este reporte se preparó con las salidas compartidas por el estudiante; no representa una ejecución independiente adicional.
