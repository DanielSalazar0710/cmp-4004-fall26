"""Genera CSV FALSOS con el formato real, para probar figuras y costos sin
esperar las corridas con Ollama. Se guardan en results/falso/ (no se suben y
NO se reportan).

    python code/datos_falsos.py
    python code/figuras.py --carpeta results/falso --salida fig/falso
"""
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from resultados import CARPETA, ERRORES_C, TAXONOMIA, escribir, fila_vacia  # noqa: E402

NIVELES = {"facil": 6, "medio": 12, "dificil": 20}
PROB_OK = {"A": (1, 1, 1), "B": (.8, .55, .3), "Bp": (.9, .7, .45), "C": (.7, .35, .1)}


def main() -> None:
    rnd = random.Random(7)
    por_brazo: dict[str, list] = {b: [] for b in PROB_OK}
    for i_n, (nivel, n_vars) in enumerate(NIVELES.items()):
        for k in range(8):
            pid = f"{nivel}-{k + 1:02d}"
            for rep in range(3):
                for brazo, probs in PROB_OK.items():
                    ok = rnd.random() < probs[i_n]
                    llm = brazo != "A"
                    iters = 0 if not llm else (1 if brazo in ("B", "C") else rnd.choice([1, 1, 2, 3, 4]))
                    t_llm = round(rnd.uniform(5, 40) * iters, 3) if llm else 0
                    t_sol = round(rnd.uniform(0.001, 0.05), 4) if brazo != "C" else 0
                    if ok:
                        cat, det, res = "", "", "correcto"
                    elif brazo in ("B", "Bp"):
                        cat = rnd.choice(list(TAXONOMIA))
                        det, res = TAXONOMIA[cat], ("sin_respuesta" if TAXONOMIA[cat] == "si" else "incorrecto")
                    else:
                        cat = rnd.choice(list(ERRORES_C))
                        det, res = ERRORES_C[cat], ("incorrecto" if cat == "incorrecta" else "sin_respuesta")
                    por_brazo[brazo].append(fila_vacia(
                        problema_id=pid, nivel=nivel, n_vars=n_vars, n_restricciones=n_vars - 2,
                        brazo=brazo, repeticion=rep, semilla=rep if llm else "", resultado=res,
                        categoria_error=cat, detectable=det, iteraciones=iters,
                        tiempo_total_s=round(t_llm + t_sol + 0.01, 3), tiempo_llm_s=t_llm,
                        tiempo_solver_s=t_sol, tokens_entrada=rnd.randint(300, 900) * iters,
                        tokens_salida=rnd.randint(80, 400) * iters, llamadas_llm=iters,
                        cache="no", modelo="falso", estado_solver="", respuesta=json.dumps({}),
                        detalle="DATO FALSO"))
    destino = CARPETA / "falso"
    escribir(por_brazo["A"], "brazo_a.csv", destino)
    escribir(por_brazo["B"] + por_brazo["Bp"], "brazo_b.csv", destino)
    escribir(por_brazo["C"], "brazo_c.csv", destino)
    print(f"CSV falsos en {destino}")


if __name__ == "__main__":
    main()
