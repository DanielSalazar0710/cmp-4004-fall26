"""Costo por respuesta CORRECTA, no por intento.  [JALIL]

El profe: "un brazo barato y equivocado no es barato". Como usamos un modelo local,
el costo en dólares es un EQUIVALENTE: lo que costarían esos mismos tokens en un
proveedor hospedado (Groq o Together AI) para un modelo de tamaño parecido.

    python code/costos.py --carpeta results/falso      # con datos falsos
    python code/costos.py                              # reales -> results/costos.csv

Lo que tiene que hacer:
  * PRECIOS: dólares por millón de tokens (entrada y salida) del proveedor que
    elijan, con el enlace a la página de precios y la FECHA en que la consultaron.
    Si no hay qwen2.5:3b, usen el modelo más pequeño parecido y escríbanlo.
  * costo_por_correcta(filas) -> dict por brazo con:
        intentos, correctas, tokens_totales, usd_total, usd_por_correcta,
        segundos_totales (llm + solver), segundos_por_correcta
    Ojo: el total suma TODOS los intentos (también los fallidos y las iteraciones
    de B'), y se divide entre las correctas. Si un brazo tiene 0 correctas,
    el costo por correcta es infinito (escríbanlo como "inf", no como 0).
  * main(): imprime una tabla Markdown lista para pegar en el REPORT y escribe
    results/costos.csv.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from resultados import leer  # noqa: E402,F401

PRECIOS = {
    # TODO Jalil: completar con precios reales y su fuente
    "proveedor": "",
    "modelo_equivalente": "",
    "usd_por_millon_entrada": None,
    "usd_por_millon_salida": None,
    "fuente": "",
    "fecha_consulta": "",
}


def costo_por_correcta(filas: list[dict]) -> dict:
    # TODO Jalil
    raise NotImplementedError


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--carpeta", default=None)
    args = ap.parse_args()
    # TODO Jalil
    raise NotImplementedError


if __name__ == "__main__":
    main()
