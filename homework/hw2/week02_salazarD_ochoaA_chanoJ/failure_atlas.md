# Failure Atlas - Week 02

## [Wk2] LLM devuelve texto sin accion valida

**Contexto:** agente LLM conectado al socket `percept -> action` del Vacuum World.

**Respuesta problematica usada para probar el parser:**

```text
banana
```

**Falla:** el texto no contiene ninguna de las acciones permitidas: `Left`, `Right`, `Suck`, `NoOp`.

**Por que importa:** el mundo no puede ejecutar "banana". Un agente clasico no tiene esta clase de falla porque retorna directamente un simbolo valido. El LLM necesita una capa extra para convertir texto libre en una accion formal.

**Mitigacion que deje en el codigo:**

- `parse_action` busca acciones validas aunque vengan con puntuacion o dentro de una frase.
- Si no encuentra accion, guarda la respuesta en `failures`.
- `llm_agent` puede reintentar.
- Si sigue fallando, usa `fallback="NoOp"`.

**Ejemplos que si parsea:**

```text
Suck. -> Suck
I would suck because the room is dirty. -> Suck
After thinking, Right is best. -> Right
```

**Leccion:** el LLM no es una arquitectura nueva aqui. Es una politica textual dentro de la misma interfaz, y el costo escondido esta en hacer que ese texto sea seguro para el simulador.
