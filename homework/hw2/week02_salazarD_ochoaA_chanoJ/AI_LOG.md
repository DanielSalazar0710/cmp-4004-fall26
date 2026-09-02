# AI_LOG

## Week 2 - Vacuum World

**Tool:** ChatGPT / Codex

**What I asked:** Pedi ayuda para revisar la estructura de la semana 2, completar `goal_based` y `utility_based`, preparar el parser del agente LLM y escribir mis notas de decisiones en formato de entrega.

**What I got:** Una implementacion local en `starter.py`, resultados de tests/torneo, un wrapper local de `aicourse.llm.LLM` conectado a Ollama, y notas explicando por que el agente de utilidad deja suciedad bajo el costo inmediato.

**What I did with it:** Revise que los tests del profesor pasaran, compare el resultado con el README de la semana, y verifique el backend con `python -m aicourse.doctor`.

**Did I understand it?** Si. Puedo explicar que el agente goal-based necesita estado para saber cuando llego a la meta, y que el utility-based no esta "fallando": esta obedeciendo una funcion de utilidad miope sin planificacion.
