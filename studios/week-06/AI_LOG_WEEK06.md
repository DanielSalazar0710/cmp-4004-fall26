# Registro de asistencia — Week 06

Entrada para incorporar al AI_LOG.md del repositorio, conservando las entradas anteriores.

## Week 06 — CSP, Logic-LM y comparación A/B/C

**Herramienta:** ChatGPT, 29–30 de septiembre de 2026.

**Qué solicité:** guía paso a paso para completar el estudio de la semana 06, explicar las restricciones, conectar Python con Ollama, solucionar errores y comparar los tres brazos.

**Qué recibí:** código para scheduling_csp y solve_arm_b_with_refinement; un cliente de Ollama con caché; scripts para ejecutar B, C y A; ayuda de instalación y diagnóstico; mejoras del mensaje con p01; manejo de estructuras inválidas y caché incompleta; análisis de las salidas y borrador del reporte.

**Qué hice con la ayuda:** incorporé y ejecuté el código en mi equipo, compartí salidas y errores, apliqué las correcciones y ejecuté los 15 acertijos de evaluación en A/B/C. Las pruebas iniciales pasaron y el banco verificó 20 soluciones únicas. Conservé respuestas y CSV.

**Alcance de la asistencia:** ChatGPT redactó el código de modelado de A y consultó el banco del profesor, incluidas sus codificaciones y gold. A no fue construido de forma independiente ni a ciegas por mí. También redactó el reporte a partir de mis salidas. El experimento con qwen2.5:3b se documenta aparte como objeto de estudio.

**Cambios metodológicos:** el mensaje de B se ajustó después de observar fallos de estructura, usando p01 como ejemplo. El reporte distingue la ejecución original de la final y mantiene la evaluación estricta separada de la revisión posterior de equivalencias de formato.

**¿Lo entendí?:** Entendí la idea general del trabajo: representar un problema medianete variables, valores posibles y restricciones, y comparar ee enfoque con las respuestas del modelo de IA. También comprendí que el solucionador puede cumplir las restricciones recibidas aunque la IA haya traducido mal el problema. Necesité ayuda para implementar el código, configurar Ollama y resolver los errores. Todavía necesito repasar algunas partes del código y las técnicas FC, MRV y AC-3 para poder explicarlas por mi cuenta.
