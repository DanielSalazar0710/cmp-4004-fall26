"""Parte 2 — brazo LLM puro. RESPONSABLE: Jalil Chano (ASIGNACIONES.md §3).

Le damos al modelo LAS MISMAS 80 instancias de la Parte 1 como texto y validamos
cada respuesta con ``validador.py``. Modelo: qwen2.5:3b vía Ollama
(``aicourse.LLM(backend="ollama")``), temperatura 0 y semilla 0 en la corrida
principal. Todas las respuestas quedan en ``.llm_cache/`` (se versiona).

Salidas (contrato del grupo):
    results/llm_respuestas.csv     una fila por instancia
        instance, domain, level, system, model, temperature, seed, cached,
        seconds, tokens_in, tokens_out, category, reason, path,
        reported_cost, checker_cost, optimal_cost
        (system = "llm"; el brazo con herramienta escribe las mismas columnas
         con system = "tool")
    results/llm_reproducibilidad.csv  5 llamadas idénticas a UNA instancia
    results/llm_calls.jsonl        registro de cada llamada, con la marca cached
    fig/escalado_optimalidad.png   tasa de óptimos vs tamaño, clásico vs LLM
                                   (y herramienta cuando exista su CSV)

Uso:
    python code/duelo_llm.py --solo grid --por-nivel 2     # prueba corta
    python code/duelo_llm.py                               # corrida completa
    python code/duelo_llm.py --repro grid-8-00
    python code/duelo_llm.py --figura
"""
from rutas import preparar_rutas

preparar_rutas()


def prompt_grid(grid) -> str:
    """Usa EXACTAMENTE ``duel.prompt_for`` del curso (curso/week04/duel.py)."""
    raise NotImplementedError  # TODO Jalil


def prompt_puzzle(estado) -> str:
    """Prompt nuestro para el 8-puzzle, con el mismo formato de salida PATH/COST.

    Debe explicar: el tablero 3x3 (0 o _ = blanco), la meta 1 2 3 / 4 5 6 / 7 8 _,
    que las letras U/D/L/R mueven el BLANCO, que cada movimiento cuesta 1 y que se
    pide el camino más corto. Escríbelo UNA vez y no lo ajustes mirando
    resultados: si lo cambias, guarda la versión anterior y dilo en el REPORT
    (sección "Where we may have been unfair").
    """
    raise NotImplementedError  # TODO Jalil


def correr_brazo_llm(dominios=("8puzzle", "grid"), por_nivel=None):
    """Una llamada por instancia, validada. Escribe results/llm_respuestas.csv."""
    raise NotImplementedError  # TODO Jalil


def reproducibilidad(id_instancia="grid-8-00", n=5):
    """Cinco llamadas IDÉNTICAS (mismo prompt, temperatura y semilla).

    Ojo: con la caché encendida las llamadas 2..5 serían copias de la 1 y el
    resultado sería falso. Usa ``llm.complete(prompt, use_cache=False)`` y guarda
    cada transcripción tú mismo (ver ASIGNACIONES.md). Cuenta respuestas distintas.
    """
    raise NotImplementedError  # TODO Jalil


def figura_escalado():
    """fig/escalado_optimalidad.png: % correct (óptimo y bien reportado) vs nivel,
    una curva por sistema, un panel por dominio, n por punto en la leyenda."""
    raise NotImplementedError  # TODO Jalil


if __name__ == "__main__":
    raise SystemExit("duelo_llm.py todavía no está implementado (Jalil)")
