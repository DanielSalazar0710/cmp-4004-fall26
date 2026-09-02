# Notas de decisiones - Week 02

Estas notas explican las decisiones que tome para la solucion, no solo los cambios de codigo.

## 1. Goal-based

Lo hice con memoria interna porque el punto de la clase era que un agente no siempre puede decidir bien mirando solo el percepto actual. Guarde dos cosas:

- `clean`: lo que el agente cree que ya esta limpio.
- `loc`: la ubicacion que reporta el sensor.

Cuando la habitacion actual esta sucia, el agente hace `Suck` y marca esa habitacion como limpia. Cuando ya cree que ambas habitaciones estan limpias, devuelve `NoOp`. Esa parte era importante porque el agente reflexivo sigue moviendose para siempre, aunque el mundo ya este limpio.

No use una tabla grande de perceptos porque la clase muestra que esa tabla crece como `4^T`. Para este mundo de dos habitaciones era mas claro guardar solo el estado minimo.

## 2. Utility-based

Aqui no intente hacer que el agente "se vea mejor". Segui la consigna: maximizar utilidad neta un paso a la vez.

Por eso, si la habitacion actual esta sucia, `Suck` tiene sentido porque convierte una habitacion sucia en una limpia y luego esa habitacion empieza a pagar recompensa. Pero si la habitacion actual ya esta limpia, cruzar a la otra habitacion cuesta `1` ahora mismo y el agente no puede ver si alla hay suciedad. Como no hay lookahead, el beneficio inmediato de cruzar no supera el costo, entonces hace `NoOp`.

Esto produce el resultado raro pero esperado: deja suciedad en 4 de 8 configuraciones. Lo anote como resultado, no como bug, porque es racional bajo la medida que le dimos.

## 3. LLM agent

No cambie la arquitectura para el LLM. Lo deje como otra politica conectada al mismo socket:

```text
percept -> action
```

La diferencia es que el LLM devuelve texto, no acciones limpias. Por eso agregue:

- parser para extraer `Left`, `Right`, `Suck` o `NoOp`.
- log de fallas cuando no aparece ninguna accion valida.
- retry por si la primera respuesta viene mal.
- fallback para no romper la corrida.

Ese codigo defensivo es parte del resultado. Los agentes clasicos no necesitan parser ni fallback porque sus acciones ya son simbolos del dominio.

## 4. Corrida LLM

Para mantener la interfaz del curso, use `aicourse.llm.LLM` como punto de entrada del modelo. La carpeta `aicourse/` fue tomada de la base de Week 0, que es donde estaba el harness usado para `LLM`, cache y `doctor`.

La verificacion del backend es:

```bash
python -m aicourse.doctor
```

Ese comando confirma que Python puede importar `aicourse`, que el cache esta disponible y que el backend local de Ollama responde. En Windows use `PYTHONIOENCODING=utf-8` porque el `doctor` original imprime simbolos como `✔`.

## 5. Conclusiones

Los tests verifican dos comportamientos principales:

1. `goal` gana porque limpia y se detiene.
2. `utility` pierde contra `goal` porque decide sin horizonte.

La comparacion mantiene la idea central de la semana: todos los agentes usan el mismo socket `percept -> action`, pero cada arquitectura toma decisiones con distinta informacion interna.
