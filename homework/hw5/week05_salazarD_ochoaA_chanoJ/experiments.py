"""Mediciones clásicas del Studio 5, guardadas en resultados/.

    python experiments.py          # repite todas las mediciones clásicas

Cuatro experimentos:
  A. minimax vs α-β: mismo valor, nodos y tiempo (garantía de exactitud).
  B. orden de jugadas: izquierda-derecha, centro-primero y peor orden.
  C. nuestro agente sobre el banco táctico: jugada correcta, profundidad y tiempo.
  D. mini torneo round-robin con la regla de 500 ms por jugada.
  E. efecto horizonte: play() con profundidades distintas.
  F. profundidad sin reloj: α-β fijo d6 vs d4 con las mismas aperturas, sin
     derrota por tiempo, para separar el efecto de la profundidad del reloj.
"""
import csv
import hashlib
import json
import platform
import time
from datetime import datetime, timezone
from math import inf
from pathlib import Path

from connect4 import (Connect4, minimax, alphabeta, play, MAX, MIN,
                      CENTER_FIRST, LEFT_TO_RIGHT, WORST)
import starter
import tactics
import tournament

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / 'resultados'
CODE_FILES = ['connect4.py', 'starter.py', 'tactics.py', 'tournament.py',
              'experiments.py', 'tactical_bank.json']
CSV_FILES = ['guarantee.csv', 'ordering.csv', 'agent_tactics.csv',
             'tournament.csv', 'horizon.csv', 'depth_no_clock.csv']


def fingerprints():
    return {n: hashlib.sha256((ROOT / n).read_bytes()).hexdigest() for n in CODE_FILES}


def _fresh():
    b = Connect4()
    b.push(3, MAX); b.push(3, MIN)
    return b


def exp_guarantee():
    rows = []
    for depth in (2, 4, 5, 6):
        for name, fn in [('minimax', lambda b, c: minimax(b, depth, MAX, c)),
                         ('alfa-beta sin orden', lambda b, c: alphabeta(b, depth, MAX, -inf, inf, c)),
                         ('alfa-beta centro', lambda b, c: alphabeta(b, depth, MAX, -inf, inf, c, CENTER_FIRST))]:
            b, c = _fresh(), [0]
            t0 = time.perf_counter()
            value, move = fn(b, c)
            rows.append(dict(depth=depth, algorithm=name, value=value, move=move,
                             nodes=c[0], seconds=round(time.perf_counter() - t0, 4)))
    return rows


def exp_ordering():
    rows = []
    for depth in (4, 5, 6, 7):
        for name, order in [('izquierda-derecha', LEFT_TO_RIGHT),
                            ('centro-primero', CENTER_FIRST), ('peor orden', WORST)]:
            b, c = _fresh(), [0]
            t0 = time.perf_counter()
            value, move = alphabeta(b, depth, MAX, -inf, inf, c, order)
            rows.append(dict(depth=depth, order=name, value=value, move=move,
                             nodes=c[0], seconds=round(time.perf_counter() - t0, 4)))
    return rows


def exp_agent_tactics(budget_ms=tournament.BUDGET_MS):
    rows = []
    for pos in tactics.load():
        b = tactics.board_from_moves(pos['moves'])
        t0 = time.perf_counter()
        move, info = starter.search_profile(b, budget_ms)
        ms = (time.perf_counter() - t0) * 1000
        rows.append(dict(id=pos['id'], kind=pos['kind'], size=pos['size'], move=move,
                         answers=' '.join(map(str, pos['answers'])),
                         correct=int(move in pos['answers']), depth=info[-1][0],
                         nodes=sum(r[3] for r in info), ms=round(ms, 1)))
    return rows


def exp_horizon():
    rows = []
    for dmax, dmin in [(2, 5), (4, 5), (5, 5), (6, 4)]:
        w, board = play(dmax, dmin)
        plies = sum(board.heights)
        rows.append(dict(depth_max=dmax, depth_min=dmin,
                         winner={MAX: 'MAX', MIN: 'MIN', None: 'empate'}[w], plies=plies))
    return rows


def exp_depth_no_clock(n_openings=6):
    rows = []
    agents = {'αβ fijo d6': 6, 'αβ fijo d4': 4}
    for op in tournament.openings(n_openings):
        for x, o in (('αβ fijo d6', 'αβ fijo d4'), ('αβ fijo d4', 'αβ fijo d6')):
            g = tournament.play_game(tournament.fixed_depth_agent(agents[x]),
                                     tournament.fixed_depth_agent(agents[o]), op, forfeit=False)
            rows.append(dict(x=x, o=o, opening=f'{op[0]}{op[1]}',
                             winner={MAX: x, MIN: o, None: 'empate'}[g['winner']],
                             plies=len(g['moves']), moves=' '.join(map(str, g['moves']))))
    return rows


def _write(name, rows):
    with (RESULTS / name).open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def run(n_openings=6):
    RESULTS.mkdir(exist_ok=True)
    timings = {}
    data = {}
    for name, fn in [('guarantee.csv', exp_guarantee), ('ordering.csv', exp_ordering),
                     ('agent_tactics.csv', exp_agent_tactics),
                     ('tournament.csv', lambda: tournament.round_robin(n_openings=n_openings)),
                     ('horizon.csv', exp_horizon),
                     ('depth_no_clock.csv', lambda: exp_depth_no_clock(n_openings))]:
        print(f'== {name}', flush=True)
        t0 = time.perf_counter()
        data[name] = fn()
        timings[name] = round(time.perf_counter() - t0, 2)
        _write(name, data[name])
    meta = dict(utc=datetime.now(timezone.utc).isoformat(), python=platform.python_version(),
                platform=platform.platform(), processor=platform.processor(),
                budget_ms=tournament.BUDGET_MS, safety=starter.SAFETY,
                n_openings=n_openings, seconds=timings, fingerprints=fingerprints(),
                csv_sha256={n: hashlib.sha256((RESULTS / n).read_bytes()).hexdigest()
                            for n in CSV_FILES})
    (RESULTS / 'metadata.json').write_text(json.dumps(meta, indent=2, ensure_ascii=False),
                                          encoding='utf-8')
    return load()


def _num(v):
    try:
        return int(v)
    except ValueError:
        try:
            return float(v)
        except ValueError:
            return v


def load(check=True):
    """Lee la corrida guardada; con check=True falla si el código o los CSV cambiaron."""
    meta = json.loads((RESULTS / 'metadata.json').read_text(encoding='utf-8'))
    if check:
        if meta['fingerprints'] != fingerprints():
            raise ValueError('El código cambió después de medir: ejecutar python experiments.py')
        for n in CSV_FILES:
            if hashlib.sha256((RESULTS / n).read_bytes()).hexdigest() != meta['csv_sha256'][n]:
                raise ValueError(f'{n} cambió: repetir la medición')
    out = {'metadata': meta}
    for n in CSV_FILES:
        with (RESULTS / n).open(encoding='utf-8', newline='') as f:
            out[n[:-4]] = [{k: (v if k in ('moves', 'answers', 'opening') else _num(v))
                            for k, v in r.items()} for r in csv.DictReader(f)]
    return out


if __name__ == '__main__':
    res = run()
    print('guardado en', RESULTS)
