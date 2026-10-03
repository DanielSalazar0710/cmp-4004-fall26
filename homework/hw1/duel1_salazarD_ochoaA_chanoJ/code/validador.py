"""Validador propio de respuestas. RESPONSABLE: Jalil Chano (ASIGNACIONES.md §3).

Regla del enunciado: NUNCA se le pregunta al modelo si su respuesta es correcta.
Este archivo decide, con código nuestro, si un camino es legal, si su costo
reportado está bien calculado y si es óptimo contra A*.

El ``duel.py`` del curso (``curso/week04``) ya clasifica grillas, pero el
enunciado exige "a validator you wrote" y además no revisa paredes ni el
8-puzzle. Úsalo como referencia, no lo importes aquí.

Categorías (columna ``category`` de los CSV; no cambies los nombres):
    malformed   — no se pudo extraer PATH/COST de la respuesta
    illegal     — fuera de la grilla, atraviesa una pared, símbolo inválido o
                  no termina en la meta                  (falla tipo 1)
    suboptimal  — legal pero con costo real mayor que el óptimo  (falla tipo 2)
    wrong_cost  — legal y óptimo, pero el costo REPORTADO no es el real (falla tipo 3)
    correct     — legal, óptimo y con el costo bien reportado

``malformed`` va aparte de las tres fallas del enunciado y se reporta como modo
de falla (eje 8 del scorecard); explicarlo en el REPORT.
"""
from __future__ import annotations

from dataclasses import dataclass

from rutas import preparar_rutas

preparar_rutas()

CATEGORIAS = ("malformed", "illegal", "suboptimal", "wrong_cost", "correct")
PARED = "#"           # las grillas del curso no tienen paredes, pero se valida igual


@dataclass
class Veredicto:
    category: str               # una de CATEGORIAS
    reason: str                 # detalle legible: "sale de la grilla en el paso 7", etc.
    path: str | None            # camino tal como lo entendimos (U/D/L/R)
    reported_cost: int | None   # lo que dijo el modelo
    checker_cost: int | None    # lo que cuesta de verdad (None si es ilegal)
    optimal_cost: int           # óptimo según A* con heurística admisible


def costo_optimo(dominio, instancia) -> int:
    """Óptimo de referencia con NUESTRO A* (motor.resolver + heurística admisible).

    Mientras heuristicas.py no esté listo, usa UCS (A* con h=0): da el mismo
    costo. Cachea el resultado por id de instancia si se vuelve lento.
    """
    raise NotImplementedError  # TODO Jalil


def recorrer_grid(grid, camino: str):
    """Camina el camino desde S. Devuelve (estado_final, costo_real, motivo_error).

    Costo = suma del costo de cada celda en la que se ENTRA (TERRAIN del curso).
    motivo_error es None si todo fue legal; si no, di en qué paso y por qué.
    """
    raise NotImplementedError  # TODO Jalil


def recorrer_puzzle(estado, camino: str):
    """Aplica movimientos del BLANCO (U/D/L/R) al 8-puzzle.

    Devuelve (estado_final, costo_real, motivo_error). Cada movimiento cuesta 1.
    Un movimiento que saca al blanco del tablero es ilegal.
    """
    raise NotImplementedError  # TODO Jalil


def validar(dominio, instancia, camino: str | None, costo_reportado: int | None) -> Veredicto:
    """Clasifica una respuesta en una de CATEGORIAS, en este orden:
    malformed -> illegal -> suboptimal -> wrong_cost -> correct.

    Ojo con las paredes: ``GridProblem`` del curso no conoce '#' (TERRAIN no lo
    tiene). Revisa la legalidad con tu propio recorrido ANTES de pedir el óptimo,
    o haz que ``costo_optimo`` trate '#' como celda bloqueada."""
    raise NotImplementedError  # TODO Jalil


def extraer_respuesta(texto: str):
    """(camino, costo) desde el texto del modelo; (None, None) si no se puede.

    Formato pedido en el prompt: dos líneas 'PATH: <letras>' y 'COST: <entero>'.
    Guarda aparte si tuviste que ser tolerante (p. ej. 'PATH: U, D, R'): esa
    diferencia entre lectura estricta y tolerante la reportamos como en week 5.
    """
    raise NotImplementedError  # TODO Jalil
