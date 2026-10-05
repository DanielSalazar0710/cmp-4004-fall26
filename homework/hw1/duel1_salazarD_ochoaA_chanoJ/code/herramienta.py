"""Parte 2 — brazo con herramienta. RESPONSABLE: Daniel Salazar.

El modelo recibe la misma instancia y el mismo texto que el brazo LLM puro, más
la descripción de una herramienta ``astar``. Si emite una llamada JSON, corremos
NUESTRO A* (``motor.resolver``) sobre los argumentos QUE EL MODELO ESCRIBIÓ y le
devolvemos el camino y su costo. Después responde PATH/COST y lo valida
``validador.py``, igual que al brazo puro.

Usamos los argumentos del modelo y no la instancia original a propósito: si el
modelo copia mal la grilla, la herramienta resuelve otro problema y ese error es
parte de lo que medimos (columna ``tool_args_match``).

Salidas (mismas columnas que results/llm_respuestas.csv, con system="tool"):
    results/herramienta_respuestas.csv
        ... + tool_called, tool_json_ok, tool_args_match, tool_rounds, tool_h
    results/llm_calls.jsonl     cada llamada al modelo (se agrega, no se borra)

Modos de falla que contamos, sin corregirlos a mano: no llama a la herramienta,
JSON mal formado, argumentos equivocados, o copia mal el resultado.

Uso:
    python code/herramienta.py --dominio grid --por-nivel 2     # prueba corta
    python code/herramienta.py                                  # corrida completa
Al volver a correr, las respuestas salen de la caché y solo se vuelven a validar;
los errores del modelo (timeout, error 500) no se guardan y se reintentan.
"""
from __future__ import annotations

import argparse
import json
import sys
import time

from rutas import CACHE, RESULTS, preparar_rutas

preparar_rutas()
import dominios  # noqa: E402
import heuristicas  # noqa: E402
import motor  # noqa: E402
import validador  # noqa: E402
from aicourse import LLM  # noqa: E402
from estadistica import escribir_csv  # noqa: E402
from gridworld import TERRAIN  # noqa: E402
from duelo_llm import latencia, llamar, veredicto_error  # noqa: E402

MODELO = "qwen2.5:3b"
MAX_RONDAS = 2           # llamadas a la herramienta permitidas por instancia
TIMEOUT_LLM_S = 300      # el harness trae 120 s; una grilla de 16×16 a veces no alcanza

INSTRUCCIONES_HERRAMIENTA = """
You also have a tool that computes the minimum-cost path exactly (A* search).
To use it, reply with ONLY one line of JSON and nothing else:
{ejemplo}
The tool will reply with the path and its total cost. After that, give your
final answer in the required two-line format.
"""
EJEMPLOS = {
    "grid": '{"tool": "astar", "domain": "grid", "grid": ["<row 1>", "<row 2>", "..."]}'
            "   (rows exactly as in the grid above, without spaces)",
    "8puzzle": '{"tool": "astar", "domain": "8puzzle", "state": [9 numbers, row by row, 0 = blank]}',
}

COLUMNAS = ["instance", "domain", "level", "system", "model", "temperature", "seed",
            "cached", "seconds", "tokens_in", "tokens_out", "category", "reason", "path",
            "reported_cost", "checker_cost", "optimal_cost", "suboptimal",
            "wrong_cost", "tolerant", "tool_called",
            "tool_json_ok", "tool_args_match", "tool_rounds", "tool_h"]


def prompt_base(dominio, instancia):
    """El MISMO texto que recibe el brazo LLM puro (sin esto la comparación no es justa)."""
    if dominio == "grid":
        import duel                      # curso/week04, prompt exacto del plan
        return duel.prompt_for(instancia)
    import duelo_llm                     # prompt del 8-puzzle del brazo puro
    return duelo_llm.prompt_puzzle(instancia)


def prompt_herramienta(dominio, instancia):
    return prompt_base(dominio, instancia) + INSTRUCCIONES_HERRAMIENTA.format(
        ejemplo=EJEMPLOS[dominio])


def extraer_llamada(texto):
    """Primer objeto JSON con "tool" en el texto. (dict, ok) o (None, False).

    ok=False con dict=None y "{" presente significa JSON mal formado."""
    decodificador = json.JSONDecoder()
    for i, ch in enumerate(texto):
        if ch != "{":
            continue
        try:
            obj, _ = decodificador.raw_decode(texto, i)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and obj.get("tool") == "astar":
            return obj, True
    return None, False


def _heuristica(dominio):
    """La mejor admisible ya implementada; si aún no hay, h = 0 (UCS)."""
    nombre = "manhattan"
    try:
        h = heuristicas.registro()[dominio][nombre]
        prob = dominios.problema(dominio, next(dominios.instancias(dominio))[2])
        h(prob, prob.initial)
        return h, nombre
    except (NotImplementedError, KeyError):
        return heuristicas.h_cero, "cero"


def ejecutar_herramienta(llamada, dominio):
    """Corre nuestro A* con los argumentos del modelo. Devuelve (respuesta, instancia_del_modelo)."""
    try:
        if llamada.get("domain") != dominio:
            raise ValueError(f"domain debe ser {dominio!r}")
        if dominio == "grid":
            grid = llamada["grid"]
            if isinstance(grid, str):    # aceptamos también filas separadas por saltos de línea
                grid = grid.splitlines()
            filas = [str(f).replace(" ", "") for f in grid if str(f).strip()]
            if not filas or len({len(f) for f in filas}) != 1:
                raise ValueError("las filas deben tener el mismo largo")
            texto = "".join(filas)
            if any(ch not in TERRAIN for ch in texto) or texto.count("S") != 1 \
                    or texto.count("G") != 1:
                raise ValueError("símbolos inválidos o S/G no aparecen una sola vez")
            instancia = filas
        else:
            instancia = tuple(int(x) for x in llamada["state"])
            if sorted(instancia) != list(range(9)):
                raise ValueError("state debe ser una permutación de 0..8")
        h, _ = _heuristica(dominio)
        r = motor.resolver(dominios.problema(dominio, instancia), "astar", h=h)
        if r.status != "solved":
            return {"error": f"no solution ({r.status})"}, instancia
        return {"path": "".join(r.path), "cost": r.cost}, instancia
    except (KeyError, TypeError, ValueError) as e:
        return {"error": str(e)}, None


def _log(ruta, registro):
    with ruta.open("a", encoding="utf-8") as f:
        f.write(json.dumps(registro, ensure_ascii=False) + "\n")


def resolver_instancia(llm, id_inst, dominio, nivel, instancia, log):
    prompt = prompt_herramienta(dominio, instancia)
    tok_in = tok_out = 0
    seg = 0.0
    todas_cacheadas = True
    llamo = json_ok = False
    args_ok = None
    rondas = 0
    texto = ""
    while True:
        r = llamar(llm, prompt)
        _log(log, {"system": "tool", "instance": id_inst, "round": rondas,
                   "model": r.model, "temperature": r.temperature, "seed": r.seed,
                   "cached": r.cached, "elapsed": r.elapsed, "error": r.error,
                   "meta": r.meta, "prompt": prompt, "text": r.text})
        seg += latencia(llm, prompt, r)     # tiempo real, aunque venga de la caché
        tok_in += r.meta.get("prompt_eval_count", 0) or 0
        tok_out += r.meta.get("eval_count", 0) or 0
        todas_cacheadas = todas_cacheadas and r.cached
        texto = r.text
        if r.error:
            break
        llamada, ok = extraer_llamada(texto)
        if llamada is None:
            if "{" in texto and '"tool"' in texto:
                llamo = True            # intentó llamar, pero el JSON no sirve
            break
        llamo, json_ok = True, json_ok or ok
        if rondas >= MAX_RONDAS:
            break
        t0 = time.perf_counter()
        salida, inst_modelo = ejecutar_herramienta(llamada, dominio)
        seg += time.perf_counter() - t0
        if inst_modelo is not None:
            original = list(instancia) if dominio == "grid" else tuple(instancia)
            args_ok = (inst_modelo == original) if args_ok is None else (args_ok and inst_modelo == original)
        rondas += 1
        prompt = (f"{prompt}\n\nYour reply:\n{texto.strip()}\n\n"
                  f"Tool result: {json.dumps(salida)}\n\n"
                  "Now give your final answer as two lines:\nPATH: <letters, no separators>\n"
                  "COST: <integer>\n")

    if r.error:                          # el modelo no respondió: no hay nada que validar
        v = veredicto_error(r.error)
    else:
        v = validador.validar_texto(dominio, instancia, texto)
    return {"instance": id_inst, "domain": dominio, "level": nivel, "system": "tool",
            "model": llm.model, "temperature": llm.temperature, "seed": llm.seed,
            "cached": todas_cacheadas, "seconds": round(seg, 3), "tokens_in": tok_in,
            "tokens_out": tok_out, "category": v.category, "reason": v.reason, "path": v.path,
            "reported_cost": v.reported_cost, "checker_cost": v.checker_cost,
            "optimal_cost": v.optimal_cost, "suboptimal": v.suboptimal,
            "wrong_cost": v.wrong_cost, "tolerant": v.tolerant,
            "tool_called": llamo, "tool_json_ok": json_ok, "tool_args_match": args_ok,
            "tool_rounds": rondas, "tool_h": _heuristica(dominio)[1]}


def correr_brazo_herramienta(doms=("8puzzle", "grid"), por_nivel=None, salida=None):
    llm = LLM(backend="ollama", model=MODELO, cache_dir=str(CACHE), timeout=TIMEOUT_LLM_S)
    log = RESULTS / "llm_calls.jsonl"
    RESULTS.mkdir(exist_ok=True)
    filas = []
    for dominio in doms:
        try:
            prompt_herramienta(dominio, next(dominios.instancias(dominio))[2])
        except NotImplementedError:
            print(f"  [aviso] {dominio}: falta el prompt del brazo puro "
                  f"(duelo_llm.prompt_puzzle); se omite", file=sys.stderr)
            continue
        for id_inst, nivel, inst in dominios.instancias(dominio, por_nivel=por_nivel):
            fila = resolver_instancia(llm, id_inst, dominio, nivel, inst, log)
            filas.append(fila)
            tiempo = "cache" if fila["cached"] else f"{fila['seconds']:.1f}s"
            print(f"  {id_inst:<14} {fila['category']:<11} tool={fila['tool_called']!s:<5} "
                  f"json={fila['tool_json_ok']!s:<5} args={fila['tool_args_match']!s:<5} "
                  f"{tiempo}", file=sys.stderr)
    escribir_csv(salida or RESULTS / "herramienta_respuestas.csv", filas, COLUMNAS)
    return filas


def main(argv=None):
    ap = argparse.ArgumentParser(description="Brazo con herramienta (LLM + nuestro A*)")
    ap.add_argument("--dominio", choices=dominios.DOMINIOS, action="append")
    ap.add_argument("--por-nivel", type=int, default=None)
    ap.add_argument("--salida", default=None)
    a = ap.parse_args(argv)
    correr_brazo_herramienta(a.dominio or dominios.DOMINIOS, a.por_nivel, a.salida)


if __name__ == "__main__":
    main()
