"""Brazo C: prompt de respuesta directa y lector de la respuesta.  [JALIL]

El LLM lee el enunciado y responde él mismo, sin solver. Aquí van dos cosas:

1. `construir_prompt(problema)`: el texto que se le manda al modelo. Debe llevar
   el enunciado y `texto_formato(problema)` (la lista exacta de variables y
   valores), y pedir la respuesta como UN objeto JSON {"Ana": 3, ...}.
   NO puede llevar el gold ni el modelo_mano.

2. `leer_respuesta(texto, problema)`: convierte lo que contestó el modelo en
   (respuesta, categoria):
       respuesta  dict {variable: valor} o None si no se pudo leer nada
       categoria  ""             respuesta bien formada (puede estar bien o mal;
                                 eso lo decide calificar() con el gold)
                  "sin_formato"  no hay JSON legible
                  "incompleta"   faltan variables o hay valores fuera de los posibles
   Para leer el JSON usen `extraer_json` (ya está hecho, es el mismo criterio del
   studio de la semana 6: tolerante con el texto alrededor, estricto con el JSON).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from problemas import normalizar, texto_formato  # noqa: E402,F401


def extraer_json(texto: str):
    """Primer objeto {...} balanceado del texto. Lanza ValueError si no hay."""
    if not texto:
        raise ValueError("respuesta vacía")
    bloque = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", texto, re.DOTALL)
    candidato = bloque.group(1) if bloque else None
    if candidato is None:
        inicio = texto.find("{")
        if inicio == -1:
            raise ValueError("no hay '{' en la respuesta")
        nivel = 0
        for i in range(inicio, len(texto)):
            if texto[i] == "{":
                nivel += 1
            elif texto[i] == "}":
                nivel -= 1
                if nivel == 0:
                    candidato = texto[inicio:i + 1]
                    break
        if candidato is None:
            raise ValueError("llaves sin cerrar")
    return json.loads(candidato)


def construir_prompt(problema: dict) -> str:
    # TODO Jalil: escribir el prompt del brazo C (en inglés, como el enunciado).
    raise NotImplementedError


def leer_respuesta(texto: str, problema: dict) -> tuple[dict | None, str]:
    # TODO Jalil
    raise NotImplementedError
