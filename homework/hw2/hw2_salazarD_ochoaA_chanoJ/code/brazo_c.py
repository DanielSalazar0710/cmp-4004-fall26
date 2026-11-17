"""Brazo C: el LLM responde directo desde el enunciado.  [JALIL]

    python code/brazo_c.py --solo ejemplos     # prueba rápida con los 3 ejemplos
    python code/brazo_c.py                     # todo el dataset x 3 semillas -> results/brazo_c.csv
    python code/brazo_c.py --falso             # sin Ollama (ClienteFalso), solo para probar

Qué tiene que hacer `correr_problema` (una fila del CSV por llamada):
  1. prompt = construir_prompt(p); r = llm.llamar(prompt, semilla)
  2. respuesta, cat = leer_respuesta(r.texto, p)
  3. resultado, detalles = calificar(p, respuesta)
  4. categoria_error: "" si es correcto; si no, cat si cat != "" y si no "incorrecta"
     detectable = ERRORES_C[categoria_error] (vacío si es correcto)
  5. medir tiempo_total_s con time.perf_counter() alrededor de todo;
     tiempo_llm_s, tokens_entrada, tokens_salida y cache salen de r;
     tiempo_solver_s = 0, iteraciones = 1, llamadas_llm = 1
  6. devolver fila_vacia(...) con TODAS las columnas de resultados.COLUMNAS
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import config  # noqa: E402,F401
from csp_motor import metricas  # noqa: E402,F401
from llm_cliente import ClienteFalso, ClienteLLM  # noqa: E402,F401
from problemas import calificar, cargar, ejemplos  # noqa: E402,F401
from respuesta_c import construir_prompt, leer_respuesta  # noqa: E402,F401
from resultados import ERRORES_C, a_json, escribir, fila_vacia  # noqa: E402,F401


def correr_problema(p: dict, llm, repeticion: int, semilla: int) -> dict:
    # TODO Jalil
    raise NotImplementedError


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--solo", choices=["ejemplos"], help="correr solo problems/ejemplos/")
    ap.add_argument("--falso", action="store_true", help="usar ClienteFalso (sin Ollama)")
    args = ap.parse_args()
    # TODO Jalil: cargar problemas (o ejemplos), crear el cliente, recorrer
    # problemas x config.SEMILLAS, escribir results/brazo_c.csv
    # (o results/brazo_c_ejemplos.csv con --solo ejemplos) e imprimir un resumen.
    raise NotImplementedError


if __name__ == "__main__":
    main()
