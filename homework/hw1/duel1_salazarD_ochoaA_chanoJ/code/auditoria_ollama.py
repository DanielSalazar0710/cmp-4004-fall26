"""Auditoría de las llamadas que terminaron en error (Daniel).

Una llamada sin texto puede ser dos cosas muy distintas:
  * el MODELO entró en un bucle: generó miles de tokens sin terminar
    (Ollama lo corta con HTTP 500, o pasamos los 300 s)  -> falla del modelo;
  * una falla de INFRAESTRUCTURA: Ollama todavía estaba cancelando la generación
    anterior, o la GPU bajó de velocidad y la llamada se cortó con pocos tokens.

No adivinamos: cruzamos cada error con el log del servidor de Ollama, que
registra cuántos tokens llevaba generados (n_gen) cuando se cortó. Regla:

    bucle confirmado  si n_gen >= UMBRAL_TOKENS y el corte no es instantáneo
    infraestructura   en otro caso  -> se vuelve a correr esa instancia

UMBRAL_TOKENS = 2000 es más de 10 veces la respuesta normal más larga que
observamos (188 tokens). Las llamadas de una corrida son secuenciales (un solo
proceso), así que el k-ésimo error del registro corresponde al k-ésimo corte
del log dentro de la ventana de tiempo de esa corrida.

Uso:
    python code/auditoria_ollama.py --system llm --desde "2026/10/04 - 21:35:20" \
        --hasta "2026/10/04 - 23:42:28"
Salidas: results/auditoria_<system>.csv y results/ollama_cortes_<system>.txt
(extracto del log, como evidencia).
"""
from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

from rutas import RESULTS, preparar_rutas

preparar_rutas()
from estadistica import escribir_csv  # noqa: E402

UMBRAL_TOKENS = 2000
CORTE_INSTANTANEO_S = 5.0
LOG = Path(os.environ.get("LOCALAPPDATA", "")) / "Ollama" / "server.log"
_GIN = re.compile(r"^\[GIN\] (\d{4}/\d\d/\d\d - \d\d:\d\d:\d\d) \| 500 \|\s+(\S+)")
_NGEN = re.compile(r"n_gen =\s+(\d+), tg =\s+([\d.]+) t/s")


def _segundos(texto):
    """'5m0s', '28.3s', '864.3ms' -> segundos."""
    total = 0.0
    for valor, unidad in re.findall(r"([\d.]+)(ms|µs|m|s)", texto):
        total += float(valor) * {"ms": 1e-3, "µs": 1e-6, "m": 60, "s": 1}[unidad]
    return total


def cortes(log, desde, hasta):
    """[(hora, duracion_s, n_gen, tokens_por_s, linea)] de cada HTTP 500 en la ventana."""
    out, ultimo = [], (0, 0.0)
    nueva_tarea = re.compile(r"processing task")
    for linea in Path(log).read_text(encoding="utf-8", errors="replace").splitlines():
        if nueva_tarea.search(linea):
            ultimo = (0, 0.0)
        m = _NGEN.search(linea)
        if m:
            ultimo = (int(m.group(1)), float(m.group(2)))
        g = _GIN.match(linea)
        if g and desde <= g.group(1) <= hasta:
            out.append((g.group(1), _segundos(g.group(2)), ultimo[0], ultimo[1], linea))
    return out


def auditar(system, desde, hasta, log=LOG):
    errores = [json.loads(l) for l in (RESULTS / "llm_calls.jsonl").read_text(
        encoding="utf-8").splitlines() if l.strip()]
    errores = [e for e in errores if e.get("system") == system and e.get("error")]
    cs = cortes(log, desde, hasta)
    if len(cs) != len(errores):
        raise SystemExit(f"{len(errores)} errores en el registro pero {len(cs)} cortes en el "
                         "log: la correspondencia por orden no es segura; revisar a mano.")
    filas = []
    for e, (hora, dur, ngen, tps, _) in zip(errores, cs):
        bucle = ngen >= UMBRAL_TOKENS and dur > CORTE_INSTANTANEO_S
        filas.append({"instance": e["instance"], "round": e.get("round", 0),
                      "error": e["error"], "hora_log": hora, "duracion_s": round(dur, 1),
                      "tokens_generados": ngen, "tokens_por_s": tps,
                      "veredicto": "bucle_del_modelo" if bucle else "infraestructura"})
    escribir_csv(RESULTS / f"auditoria_{system}.csv", filas)
    (RESULTS / f"ollama_cortes_{system}.txt").write_text(
        "\n".join(f"{c[4]}    # n_gen previo = {c[2]}, {c[3]} t/s" for c in cs) + "\n",
        encoding="utf-8")
    return filas


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--system", default="llm", choices=("llm", "tool"))
    ap.add_argument("--desde", required=True, help='"AAAA/MM/DD - HH:MM:SS" (hora del log)')
    ap.add_argument("--hasta", required=True)
    a = ap.parse_args(argv)
    filas = auditar(a.system, a.desde, a.hasta)
    infra = sorted({f["instance"] for f in filas if f["veredicto"] == "infraestructura"})
    print(f"{len(filas)} errores: {len(filas) - len(infra)} bucles del modelo, "
          f"{len(infra)} de infraestructura")
    print("volver a correr:", ",".join(infra))


if __name__ == "__main__":
    main()
