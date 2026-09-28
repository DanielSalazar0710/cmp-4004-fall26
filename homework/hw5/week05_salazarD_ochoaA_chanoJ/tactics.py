"""Banco táctico reproducible: posiciones con victoria inmediata o amenaza que bloquear.

Lo usamos para medir, con la misma vara, a nuestro agente α-β y al retador LLM.
Todas las posiciones tienen a MAX ('X') por mover, como supone el prompt del plan.

El "tamaño" de cada instancia es el número de fichas ya colocadas (6, 12, 18, 24):
cuanto más lleno el tablero, más texto tiene que leer el LLM y más líneas pueden
esconder la jugada correcta. Es una aproximación de dificultad, no una medida
formal; lo discutimos en el notebook.
"""
import json
import random
from pathlib import Path

from connect4 import Connect4, MAX, MIN, ROWS, COLS

SEED = 20260928
SIZES = (6, 12, 18, 24)
PER_SIZE = 10
BANK_FILE = Path(__file__).resolve().parent / 'tactical_bank.json'


def winning_moves(board, player):
    """Columnas con las que `player` gana en esta misma jugada."""
    wins = []
    for col in board.legal_moves():
        board.push(col, player)
        if board.winner() == player:
            wins.append(col)
        board.pop(col)
    return wins


def board_from_moves(moves):
    """Reconstruye un tablero desde la secuencia de columnas; empieza MIN.

    Empezar con MIN y usar un número par de fichas deja a MAX por mover.
    """
    b = Connect4()
    player = MIN
    for col in moves:
        b.push(col, player)
        player = -player
    return b


def to_grid(board):
    """Copia serializable del tablero (filas de abajo hacia arriba)."""
    return [row[:] for row in board.grid]


def board_from_grid(grid):
    b = Connect4()
    b.grid = [row[:] for row in grid]
    b.heights = [sum(1 for r in range(ROWS) if b.grid[r][c] != 0) for c in range(COLS)]
    return b


def _random_position(rng, n_discs):
    """Partida aleatoria sin ganador de `n_discs` fichas (MIN empieza)."""
    while True:
        moves, b, player = [], Connect4(), MIN
        ok = True
        for _ in range(n_discs):
            col = rng.choice(b.legal_moves())
            b.push(col, player)
            moves.append(col)
            if b.winner() is not None:
                ok = False
                break
            player = -player
        if ok:
            return moves, b


def generate(seed=SEED):
    """Genera 10 posiciones 'win' y 10 'block' por tamaño.

    win   : MAX tiene al menos una victoria inmediata.
    block : MAX no tiene victoria inmediata y MIN amenaza exactamente UNA columna,
            así que existe una única jugada que evita perder en la siguiente jugada.
    """
    rng = random.Random(seed)
    bank = []
    for size in SIZES:
        found = {'win': 0, 'block': 0}
        seen = set()
        while min(found.values()) < PER_SIZE:
            moves, b = _random_position(rng, size)
            key = tuple(moves)
            if key in seen:
                continue
            seen.add(key)
            max_wins = winning_moves(b, MAX)
            min_wins = winning_moves(b, MIN)
            if max_wins:
                kind, answers = 'win', max_wins
            elif len(min_wins) == 1:
                kind, answers = 'block', min_wins
            else:
                continue
            if found[kind] >= PER_SIZE:
                continue
            found[kind] += 1
            bank.append(dict(id=f'{kind}-{size:02d}-{found[kind]:02d}', kind=kind,
                             size=size, moves=moves, answers=answers))
    return bank


def save(bank, path=BANK_FILE):
    path.write_text(json.dumps(dict(seed=SEED, sizes=SIZES, per_size=PER_SIZE,
                                    positions=bank), indent=1), encoding='utf-8')


def load(path=BANK_FILE):
    data = json.loads(path.read_text(encoding='utf-8'))
    return data['positions']


if __name__ == '__main__':
    bank = generate()
    save(bank)
    print(f'{len(bank)} posiciones guardadas en {BANK_FILE.name}')
