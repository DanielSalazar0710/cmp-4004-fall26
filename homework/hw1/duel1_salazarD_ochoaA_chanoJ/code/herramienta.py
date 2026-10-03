"""Parte 2 — brazo con herramienta. RESPONSABLE: Daniel Salazar (con Claude).

El modelo recibe la misma instancia que el brazo LLM puro y la descripción de
una herramienta ``astar``. Si emite una llamada JSON válida, corremos NUESTRO
A* (motor.resolver) y le devolvemos el resultado; luego responde PATH/COST y lo
valida ``validador.py`` de Jalil, igual que al brazo puro.

Se mide como tercer sistema (system="tool") con las mismas columnas que
``results/llm_respuestas.csv`` más: tool_called, tool_json_ok, tool_rounds.
Salidas: results/herramienta_respuestas.csv, results/llm_calls.jsonl.

Modos de falla esperables: JSON mal formado, argumentos equivocados, o copiar mal
el resultado de la herramienta. Se cuentan, no se corrigen a mano.
"""
from rutas import preparar_rutas

preparar_rutas()


def correr_brazo_herramienta(dominios=("8puzzle", "grid"), por_nivel=None):
    raise NotImplementedError  # TODO Daniel


if __name__ == "__main__":
    correr_brazo_herramienta()
