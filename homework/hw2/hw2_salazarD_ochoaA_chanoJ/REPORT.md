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
- **Tipos estrictos.** Nuestro solver rechaza `"b": "3"` (texto) cuando el dominio es numérico y lo cuenta como error de alcance. Un parser que convirtiera números escritos como texto habría rescatado esos casos. Lo dejamos estricto porque así se comporta un solver real, pero reportamos cuántos fallos de B se salvarían con esa conversión _(pendiente: número)_.
- **El vocabulario lo diseñamos nosotros.** Los 7 tipos de restricción (`alldiff`, `eq`, `neq`, `lt`, `gt`, `adj`, `offset`) cubren exactamente los problemas que escribimos. Un acertijo con disyunciones ("vive en la casa 1 o en la 5") no cabe, así que el dataset favorece al brazo B: las pistas se traducen casi una a una.
- **Ejemplo few-shot de una sola familia.** El prompt de B lleva un ejemplo resuelto tipo Einstein; los problemas de horario y coloreo no tienen uno propio. El prompt de C no lleva ejemplo resuelto. _(pendiente: confirmar con el prompt final de C)_
- **Retroalimentación generosa.** B′ solo recibe el mensaje del solver, pero ese mensaje lo redactamos nosotros y es informativo (por ejemplo, "dos soluciones difieren en Bird, Dog"). Un solver de caja negra daría menos señal.
- **Ajustamos los prompts solo con los 3 ejemplos**, que no cuentan en la evaluación. Aun así, el ejemplo few-shot de B es uno de esos 3, así que los números de B sobre los ejemplos no son una medición limpia y no los reportamos como resultado.
- **Modelo pequeño y temperatura 0.7.** Un modelo de 3B a temperatura 0.7 se equivoca más en todos los brazos; elegimos 0.7 para medir varianza entre semillas. Con temperatura 0 los números de B y C probablemente suban, y la varianza sería cero por construcción.
- **El brazo A es 100 % por construcción:** la misma persona escribió el enunciado, el modelo a mano y el gold, y el verificador exige que coincidan. Sirve como techo y control, no como evidencia de que modelar a mano sea fácil.

## 7. Recomendación
_(pendiente: qué brazo desplegaríamos, defendido con nuestros números)_

**Monitoreo que adjuntaríamos (borrador):**
- Alarma por cada respuesta que el solver marca como sin solución, con varias soluciones, con error de construcción o con timeout: son fallos que se anuncian solos y no deben llegar al usuario.
- Muestreo y revisión humana de un porcentaje de los modelos de solución única, porque el "problema equivocado" es el único fallo silencioso de B.
- Seguimiento de la tasa de cada categoría por semana y de las iteraciones de B′, para detectar si cambió el modelo o el tipo de problemas.
