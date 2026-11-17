# HW2 · The Formalizer (CSP)

**Equipo:** Daniel Salazar, Andretty Ochoa, Jalil Chano · **Formalismo:** CSP (solver propio: backtracking + forward checking + MRV) · **Modelo:** `qwen2.5:3b` (3 mil millones de parámetros, Ollama en CPU), temperatura 0.7, semillas 0, 1 y 2.

> Borrador: las secciones marcadas _(pendiente)_ se llenan con los datos reales.

## 0. Diseño del experimento
- **Dataset:** 21 problemas propios en 3 niveles por número de variables (fácil ≤ 8, medio 9–15, difícil ≥ 16), con verdad base verificada a mano y por el solver (solución única). Ver `problems/README.md`.
- **Brazos:** A (modelo a mano → solver), B (LLM → modelo → solver), B′ (B + hasta 3 rondas con el mensaje del solver, sin ver el gold), C (LLM responde directo).
- **Instrumentación por instancia:** correcto / incorrecto / sin respuesta, reloj de pared, tokens de entrada y salida, tiempo del LLM y del solver por separado (`results/*.csv`).
- **Detección sin ground truth:** nuestro solver cuenta hasta 2 soluciones, así que un modelo sub-restringido se detecta sin conocer la respuesta.

## 1. Duel Scorecard
_(pendiente: tabla A / B / B′ / C con los 8 ejes de `referencias/duel-scorecard.md`)_

## 2. Precisión vs. dificultad
![precisión vs dificultad](fig/precision_vs_dificultad.png)
_(pendiente)_

## 3. Taxonomía de errores
_(pendiente: tabla de `taxonomy.md` + 5 ejemplos verbatim anotados)_

## 4. Análisis del refinamiento
_(pendiente: iteraciones hasta acertar, fracción que nunca converge, diferencia entre fallos arreglados en 1 ronda y los que sobreviven 3)_

## 5. Costo por respuesta correcta
_(pendiente: tabla de `costos.py`)_

## 6. Dónde pudimos haber sido injustos
_(pendiente)_

## 7. Recomendación
_(pendiente)_
