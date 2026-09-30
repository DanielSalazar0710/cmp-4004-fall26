# Registro de asistencia de IA

## Week 06 — CSP, Logic-LM y comparación A/B/C

**Herramienta:** ChatGPT, 29–30 de septiembre de 2026.

**Qué solicité:** guía paso a paso para completar el estudio de la semana 06, explicar las restricciones, conectar Python con Ollama, solucionar errores y comparar los tres brazos.

**Qué recibí:** código para scheduling_csp y solve_arm_b_with_refinement; un cliente de Ollama con caché; scripts para ejecutar B, C y A; ayuda de instalación y diagnóstico; mejoras del mensaje con p01; manejo de estructuras inválidas y caché incompleta; análisis de las salidas y borrador del reporte.

**Qué hice con la ayuda:** incorporé y ejecuté el código en mi equipo, compartí salidas y errores, apliqué las correcciones y ejecuté los 15 acertijos de evaluación en A/B/C. Las pruebas iniciales pasaron y el banco verificó 20 soluciones únicas. Conservé respuestas y CSV.

**Alcance de la asistencia:** ChatGPT redactó el código de modelado de A y consultó el banco del profesor, incluidas sus codificaciones y gold. A no fue construido de forma independiente ni a ciegas por mí. También redactó el reporte a partir de mis salidas. El experimento con qwen2.5:3b se documenta aparte como objeto de estudio.

**Cambios metodológicos:** el mensaje de B se ajustó después de observar fallos de estructura, usando p01 como ejemplo. El reporte distingue la ejecución original de la final y mantiene la evaluación estricta separada de la revisión posterior de equivalencias de formato.

**¿Lo entendí?:** Entendí la idea general del trabajo: representar un problema mediante variables, valores posibles y restricciones, y comparar ese enfoque con las respuestas del modelo de IA. También comprendí que el solucionador puede cumplir las restricciones recibidas aunque la IA haya traducido mal el problema. Necesité ayuda para implementar el código, configurar Ollama y resolver los errores. Todavía necesito repasar algunas partes del código y las técnicas FC, MRV y AC-3 para poder explicarlas por mi cuenta.

## Week 06 — Verificación y notebook de presentación

**Herramienta:** Codex, 30 de septiembre de 2026.

**Qué solicitamos:** revisar la entrega frente a las instrucciones del profesor, preparar un notebook ejecutado para la presentación y organizar los archivos del equipo.

**Qué recibimos:** revisión del código y de los resultados, notebook con exposición y preguntas técnicas, comprobación de equivalencias de representación, corrección del manejo de AttributeError en el refinamiento y cuatro pruebas con respuestas controladas.

**Qué se incorporó y verificó:** notebook ejecutado; cinco pruebas originales aprobadas; veinte acertijos verificados; brazo A reproducido con 15/15; conteos y auditoría posterior calculados desde los CSV. Conservamos los resultados originales de B y C. No repetimos sus llamadas al modelo ni recuperamos la caché ausente. Retiramos del control de versiones los archivos compilados de Python.

**Comprensión:** el notebook documenta las decisiones, limitaciones y conceptos que debemos explicar en la exposición. La ejecución automática verifica resultados técnicos; no certifica el dominio individual de los conceptos. Conservamos la reflexión original de Andretty sobre los temas que requieren repaso.
