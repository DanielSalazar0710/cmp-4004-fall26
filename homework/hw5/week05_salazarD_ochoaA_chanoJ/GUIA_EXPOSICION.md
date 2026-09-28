# Guía de exposición — Salazar, Ochoa y Chano

## Preparación

Abrimos `starter.py` y el notebook uno junto al otro. Antes de la clase ejecutamos el notebook en orden y comprobamos que sus salidas estén guardadas. La versión HTML muestra las mismas salidas sin depender del kernel. Las mediciones ya están guardadas; explicamos cuándo se ejecutaron y cómo repetirlas. Si queremos mostrar el LLM en vivo, Ollama debe estar abierto, y la primera llamada tarda más mientras carga el modelo.

## Propuesta de distribución de la exposición

Es una propuesta. El grupo todavía no la ha confirmado.

| Integrante | Bloque | Demostración |
|---|---|---|
| Salazar | Consigna y agente, secciones 1–6 | `search_profile` sobre una posición, el corte duro y los tests |
| Ochoa | Garantías y torneo, secciones 7–11 | Tabla minimax/α-β, orden de jugadas, horizonte y torneo |
| Chano | Retador LLM y cierre, secciones 12–19 | Prompt, banco táctico, reproducibilidad, partidas, scorecard y conclusiones |

Proponemos 4–5 minutos por bloque.

## Qué decimos y qué mostramos

1. **Inicio:** «En la semana 4 buscábamos solos; ahora hay un rival y un reloj». Mostramos la tabla de requisitos de la sección 2.
2. **Agente:** «Buscamos a profundidad 1, 2, 3… y nos quedamos con la última completa». Mostramos la tabla de la sección 4, con cada profundidad varias veces más cara que la anterior.
3. **Corte duro:** «La primera versión perdió partidas por tiempo; ahora el contador de nodos revisa el reloj». Mostramos `_ClockCounter`.
4. **Tests:** ejecutamos la celda de la sección 6.
5. **Garantía:** «Mismo valor, 36 veces menos nodos». Mostramos la tabla de la sección 7, que coincide con la de la consigna.
6. **Horizonte:** mostramos `play(2, 5)` y explicamos por qué `play(5, 5)` es un artefacto.
7. **Torneo:** «`d6` juega mejor cada jugada, pero pierde por tiempo». Después contamos el resultado inesperado contra `d4` y el control sin reloj.
8. **LLM:** mostramos el prompt, luego la tabla y la gráfica del banco táctico. «Siempre legal, pero acierta menos que jugar siempre al centro».
9. **Reproducibilidad:** «Esta vez las cinco repeticiones fueron inferencias nuevas; lo comprobamos en el registro».
10. **Cierre:** Failure Atlas, scorecard, «Where we may have been unfair» y conclusiones.

## Preguntas con respuesta breve

- **¿Por qué α-β no cambia el valor?** Solo poda ramas que no pueden cambiar la decisión de la raíz.
- **¿Qué hace `SAFETY` y qué hace `HARD_STOP`?** El primero decide si empezamos otra profundidad; el segundo interrumpe la que está corriendo.
- **¿Por qué buscamos sobre una copia?** La excepción corta la búsqueda antes de los `pop`, y el tablero quedaría con fichas de más.
- **¿Por qué perdimos contra `d4`?** No lo sabemos con certeza. Sin reloj, `d6` tampoco le gana claramente a `d4`, así que sospechamos de `evaluate()`. Es una hipótesis.
- **¿Por qué el LLM a temperatura 0 dio dos respuestas distintas en 2 posiciones?** No lo comprobamos. Una hipótesis es el no determinismo numérico de la ejecución.
- **¿El banco táctico prueba que los LLM no juegan Connect-4?** No. Mide a estos dos modelos pequeños con este prompt.
