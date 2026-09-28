"""Week 5 studio — your tournament agent.

The engine (board, ``minimax``, ``alphabeta``, the static orderings, ``play``)
is GIVEN in ``connect4.py`` and must not be modified. Your job is the one thing
the tournament actually enforces: a **time-bounded, anytime** agent.

    def choose_move(board, time_budget_ms) -> int

Hard tournament rules (from the plan): 500 ms per move, no external processes,
no network, no opening book larger than 20 positions. The reference bracket runs
a plain α-β agent at depth 6 — beat it with *depth*, not cleverness.

Fill in the two functions below. Then run ``python3 test_alphabeta.py``; the
starter-dependent tests must pass and the two *guarantee* tests (which use the
given engine) show you what α-β and the horizon effect actually buy you.

Why iterative deepening rather than a fixed depth? Because a fixed depth either
finishes early (wasting budget) or blows the 500 ms limit and forfeits. Iterative
deepening searches depth 1, then 2, then 3, ... keeping the best move from the
last COMPLETED depth, and stops when the clock runs out. It is what turns α-β
into a time-bounded anytime agent — the single most important thing in the
tournament, per the plan.
"""
import time
from math import inf

from connect4 import Connect4, alphabeta, MAX, CENTER_FIRST


# Fracción del presupuesto en la que todavía empezamos una profundidad nueva, si
# la estimación de su costo cabe.
SAFETY = 0.6
# Corte duro: si una profundidad sigue corriendo al llegar a esta fracción del
# presupuesto, la abandonamos (versión 2, ver DECISION_NOTES.md).
HARD_STOP = 0.8
# Factor de crecimiento supuesto cuando todavía no tenemos dos profundidades medidas.
DEFAULT_GROWTH = 4.0


class _OutOfTime(Exception):
    pass


class _ClockCounter(list):
    """Contador de nodos que además revisa el reloj.

    El `alphabeta` dado hace `counter[0] += 1` en cada nodo. Al pasarle este
    contador, cada nodo comprueba la hora límite y, si ya pasó, lanza una
    excepción que abandona la profundidad en curso. Así interrumpimos la búsqueda
    sin modificar connect4.py.
    """
    def __init__(self, deadline):
        super().__init__([0])
        self.deadline = deadline

    def __setitem__(self, i, v):
        if time.perf_counter() > self.deadline:
            raise _OutOfTime
        super().__setitem__(i, v)


def _copy(board):
    # Una excepción a mitad de la búsqueda deja fichas sin `pop`: buscamos sobre
    # una copia para que el tablero del torneo nunca quede alterado.
    b = Connect4()
    b.grid = [row[:] for row in board.grid]
    b.heights = board.heights[:]
    return b


def order_moves(board, first=None):
    """Return this board's legal columns in the order α-β should try them.

    α-β's best case (O(b^(m/2)) — double the reachable depth) requires examining
    strong moves first. A good *static* order for Connect-4 is center-first
    (``CENTER_FIRST`` in connect4.py). Fast-finishing pairs: try a *dynamic*
    order that puts last iteration's best move first (see ``choose_move``).
    """
    # Orden estático centro-primero; si conocemos la mejor jugada de la
    # iteración anterior (`first`), la adelantamos (orden dinámico).
    legal = board.legal_moves()
    order = [c for c in CENTER_FIRST if c in legal]
    if first in order:
        order.remove(first)
        order.insert(0, first)
    return order


def search_profile(board, time_budget_ms):
    """Profundización iterativa instrumentada.

    Devuelve (best_move, info), donde info registra cada profundidad COMPLETADA:
    lista de (depth, value, move, nodes, seconds). `choose_move` usa esta misma
    función, así el notebook mide exactamente el agente del torneo.
    """
    start = time.perf_counter()
    budget = time_budget_ms / 1000.0
    deadline = start + budget * HARD_STOP
    order = order_moves(board)
    work = _copy(board)
    best = order[0]                         # regla 1: siempre hay una jugada legal
    completed = []
    empty = sum(6 - h for h in board.heights)
    last_dt = prev_dt = None
    for depth in range(1, empty + 1):
        elapsed = time.perf_counter() - start
        if last_dt is not None:
            growth = DEFAULT_GROWTH if not prev_dt else max(2.0, min(8.0, last_dt / prev_dt))
            # regla 2: no empezamos una profundidad que probablemente no termine
            if elapsed + last_dt * growth > budget * SAFETY:
                break
        elif elapsed >= budget * SAFETY:
            break
        counter = _ClockCounter(deadline)
        t0 = time.perf_counter()
        try:
            value, move = alphabeta(work, depth, MAX, -inf, inf, counter,
                                    order_moves(board, first=best))
        except _OutOfTime:
            break                           # profundidad incompleta: no se usa
        dt = time.perf_counter() - t0
        completed.append((depth, value, move, counter[0], dt))
        prev_dt, last_dt = last_dt, dt
        if value <= -10_000 and len(completed) > 1:
            # Derrota forzada demostrada: todas las jugadas empatan en -10 000.
            # Conservamos la jugada de la profundidad anterior, que al menos no
            # pierde dentro del horizonte menor, y dejamos de profundizar.
            break
        if move is not None:
            best = move                     # regla 3: gana la última profundidad completa
        if value >= 10_000:
            break                           # victoria forzada: la primera profundidad que la ve es la más corta
    return best, completed


def choose_move(board, time_budget_ms) -> int:
    """Return the column MAX should play, using iterative deepening + α-β.

    Contract (the tournament relies on all three):
      1. ALWAYS return a legal column, even if the budget is tiny — seed `best`
         with a legal move before the loop so you never return None.
      2. Never exceed `time_budget_ms` by much — check the clock between depths
         and stop; do not start a depth you cannot afford to be interrupted in.
      3. Keep the best move from the last COMPLETED depth (a half-finished depth
         can return a worse move than the one below it).

    You call the GIVEN ``alphabeta(board, depth, MAX, -inf, inf, counter, order)``
    at increasing depths. Pass ``order=order_moves(board)`` so pruning bites.
    """
    move, _ = search_profile(board, time_budget_ms)
    return move
if __name__ == "__main__":
    # Quick smoke test: choose a move on the opening position under a 500 ms budget.
    b = Connect4()
    b.push(3, MAX)          # suppose MIN opened center; MAX replies
    try:
        t0 = time.perf_counter()
        move = choose_move(b, 500)
        dt = (time.perf_counter() - t0) * 1000
        print(f"choose_move -> col {move}  ({dt:.0f} ms, budget 500)")
        assert move in b.legal_moves(), "returned an illegal column!"
        print("legal:", b.legal_moves())
    except NotImplementedError:
        print("choose_move / order_moves not implemented yet — fill them in.")
