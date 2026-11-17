"""Figuras del reporte (mínimo 3; la primera es obligatoria).  [JALIL]

    python code/figuras.py --carpeta results/falso --salida fig/falso   # con datos falsos
    python code/figuras.py                                              # con los datos reales

Leen SOLO los CSV (resultados.leer) para que funcionen igual con datos falsos y
reales. Sin pandas: csv + matplotlib.

Figuras que necesitamos (nombres fijos, porque el REPORT las enlaza):
  1. precision_vs_dificultad.png  OBLIGATORIA. Eje x: nivel (facil, medio, dificil)
     o n_vars; eje y: % correcto. Una línea por brazo (A, B, Bp, C), con barras de
     error entre repeticiones (mín y máx o desviación estándar de las 3 semillas).
  2. costo_por_correcta.png       tokens (o segundos) por respuesta CORRECTA, por brazo.
                                  Usar costos.costo_por_correcta().
  3. tiempo_llm_vs_solver.png     barras apiladas por brazo: tiempo LLM vs tiempo solver.
  4. iteraciones_bp.png           histograma de iteraciones hasta acertar en Bp,
                                  más una barra "nunca convergió".
  5. taxonomia_b.png              conteo por categoria_error del brazo B, coloreado
                                  según detectable si/no.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from resultados import RAIZ, leer  # noqa: E402,F401

COLORES = {"A": "#4C72B0", "B": "#DD8452", "Bp": "#55A868", "C": "#C44E52"}
NOMBRES = {"A": "A (a mano)", "B": "B (híbrido)", "Bp": "B' (con refinamiento)", "C": "C (directo)"}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--carpeta", default=None, help="carpeta con los brazo_*.csv (por defecto results/)")
    ap.add_argument("--salida", default=str(RAIZ / "fig"), help="carpeta de salida de los PNG")
    args = ap.parse_args()
    # TODO Jalil
    raise NotImplementedError


if __name__ == "__main__":
    main()
