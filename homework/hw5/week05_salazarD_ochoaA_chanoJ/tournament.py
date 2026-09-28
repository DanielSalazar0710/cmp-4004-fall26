"""Mini torneo round-robin local, con las reglas del plan (500 ms por jugada).

No es el torneo de la clase: es nuestra réplica para comprobar, antes de
enviar el agente, que respeta el reloj y cómo se comporta frente a agentes de
profundidad fija. Todos los agentes reciben el tablero "visto como MAX": si les
toca jugar con MIN, invertimos las fichas antes de llamarlos (`as_max`).
"""
import random
import time
from math import inf

from connect4 import Connect4, alphabeta, MAX, MIN, CENTER_FIRST
import starter

BUDGET_MS = 500


def as_max(board, player):
    """Copia del tablero en la que `player` aparece como MAX."""
    b = Connect4()
    b.grid = [[v * player for v in row] for row in board.grid]
    b.heights = board.heights[:]
    return b


def fixed_depth_agent(depth):
    def agent(board, time_budget_ms):
        _, move = alphabeta(board, depth, MAX, -inf, inf, [0], CENTER_FIRST)
        return move if move is not None else board.legal_moves()[0]
    agent.__name__ = f'ab_d{depth}'
    return agent


def random_agent(seed):
    rng = random.Random(seed)

    def agent(board, time_budget_ms):
        return rng.choice(board.legal_moves())
    return agent


AGENTS = {
    'ID-αβ (nuestro)': lambda: starter.choose_move,
    'αβ fijo d6': lambda: fixed_depth_agent(6),
    'αβ fijo d4': lambda: fixed_depth_agent(4),
    'aleatorio': lambda: random_agent(0),
}


def play_game(agent_x, agent_o, opening=(), budget_ms=BUDGET_MS, forfeit=True):
    """Juega una partida. agent_x mueve primero (MAX), agent_o segundo (MIN).

    `opening` son jugadas iniciales impuestas (alternando desde MAX) para que
    los agentes deterministas no repitan siempre la misma partida.
    Devuelve dict con ganador, motivo, jugadas y tiempos por jugada.
    """
    board = Connect4()
    player = MAX
    moves, times = [], []
    for col in opening:
        board.push(col, player)
        moves.append(col)
        player = -player
    reason = None
    while board.winner() is None and not board.full():
        agent = agent_x if player == MAX else agent_o
        view = as_max(board, player)
        t0 = time.perf_counter()
        col = agent(view, budget_ms)
        ms = (time.perf_counter() - t0) * 1000
        times.append((player, ms))
        if col not in board.legal_moves():
            return dict(winner=-player, reason='ilegal', moves=moves, times=times, board=board)
        if forfeit and ms > budget_ms:
            return dict(winner=-player, reason='tiempo', moves=moves + [col], times=times, board=board)
        board.push(col, player)
        moves.append(col)
        player = -player
    w = board.winner()
    return dict(winner=w, reason='cuatro en línea' if w else 'empate', moves=moves,
                times=times, board=board)


def openings(n, seed=5):
    """`n` aperturas distintas de dos jugadas; siempre incluimos centro-centro."""
    rng = random.Random(seed)
    pairs = [(3, 3)] + [(a, b) for a in range(7) for b in range(7) if (a, b) != (3, 3)]
    rest = pairs[1:]
    rng.shuffle(rest)
    return [pairs[0]] + rest[:n - 1]


def round_robin(names=None, n_openings=6, budget_ms=BUDGET_MS, progress=True):
    """Cada par de agentes juega cada apertura con ambos colores."""
    names = list(names or AGENTS)
    rows = []
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            for k, op in enumerate(openings(n_openings)):
                for x, o in ((a, b), (b, a)):
                    g = play_game(AGENTS[x](), AGENTS[o](), op, budget_ms)
                    winner = {MAX: x, MIN: o, None: 'empate'}[g['winner']]
                    tx = [ms for p, ms in g['times'] if p == MAX]
                    to = [ms for p, ms in g['times'] if p == MIN]
                    rows.append(dict(x=x, o=o, opening=f'{op[0]}{op[1]}', winner=winner,
                                     reason=g['reason'], plies=len(g['moves']),
                                     x_max_ms=round(max(tx), 1) if tx else 0.0,
                                     o_max_ms=round(max(to), 1) if to else 0.0,
                                     moves=' '.join(map(str, g['moves']))))
                    if progress:
                        print(f"  {x:>16} vs {o:<16} ap {op}: {winner} ({g['reason']})", flush=True)
    return rows
