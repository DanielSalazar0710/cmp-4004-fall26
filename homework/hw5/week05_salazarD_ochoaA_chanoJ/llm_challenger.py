"""El retador LLM del Studio 5, con el prompt exacto del plan.

    python llm_challenger.py                          # qwen2.5:3b, los tres experimentos
    python llm_challenger.py --model qwen2.5:1.5b --only tactics
    python llm_challenger.py --check                  # solo verifica el backend

Modelo principal: qwen2.5:3b, el valor por defecto del harness y de
resources/setup.md. qwen2.5:1.5b es el que usamos en semanas 0-2; lo corremos
sobre el banco táctico para comparar.

Tres experimentos (todas las llamadas quedan en resultados_llm/llm_calls.jsonl):

  1. tactics : las 80 posiciones del banco táctico, temperatura 0, semilla 0.
  2. repro   : 20 posiciones × 5 semillas (1..5) × temperaturas 0 y 0.7.
               Usamos semillas DISTINTAS de la del experimento 1 para que ninguna
               repetición sea un acierto de caché: cada una es una inferencia nueva.
               El registro guarda `cached` por llamada y el análisis lo comprueba.
  3. games   : partidas LLM vs nuestro agente α-β (ambos colores).

Nunca creemos la respuesta del modelo: la jugada se valida contra
`legal_moves()` y el resultado táctico se compara con el banco verificado.
"""
import argparse
import hashlib
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from aicourse.llm import LLM
from connect4 import Connect4, MAX, MIN, CENTER_FIRST
import starter
import tactics
import tournament

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'resultados_llm'
LOG = OUT / 'llm_calls.jsonl'
MODEL = 'qwen2.5:3b'
BACKEND = 'ollama'

# Prompt exacto de studios/week-05/README.md ("The LLM challenger").
PROMPT = """Connect-4. You are 'X'. Columns numbered 0-6, left to right.
Board (bottom row last):
{board}
Legal columns: {legal}
Reply with one column number and nothing else."""

RETRY_SEED_OFFSET = 1000       # el reintento usa otra semilla: es otra inferencia


def make_prompt(board):
    """`board` debe estar visto desde el LLM: sus fichas son MAX ('X')."""
    return PROMPT.format(board=str(board), legal=board.legal_moves())


def parse_move(text):
    """Devuelve (columna o None, estricto).

    estricto = la respuesta es exactamente un número (lo que pide el prompt).
    Si no, tomamos el primer entero aislado del texto (lectura tolerante).
    """
    t = text.strip()
    if re.fullmatch(r'\d+', t):
        return int(t), True
    m = re.search(r'(?<!\d)(\d+)(?!\d)', t)
    return (int(m.group(1)), False) if m else (None, False)


class Challenger:
    def __init__(self, backend=BACKEND, model=MODEL, cache_dir=None, log=LOG):
        self.llm = LLM(backend=backend, model=model,
                       cache_dir=str(cache_dir or ROOT / '.llm_cache'), timeout=300.0)
        self.log = Path(log)

    def ask(self, board, *, experiment, item, temperature=0.0, seed=0, retries=1):
        """Una jugada del LLM con validación y un reintento; registra cada llamada."""
        legal = board.legal_moves()
        prompt = make_prompt(board)
        attempts = []
        for k in range(retries + 1):
            sd = seed + k * RETRY_SEED_OFFSET
            r = self.llm.complete(prompt, temperature=temperature, seed=sd)
            col, strict = parse_move(r.text)
            ok = col in legal and r.error is None
            rec = dict(utc=datetime.now(timezone.utc).isoformat(), experiment=experiment,
                       item=item, attempt=k, model=r.model, backend=r.backend,
                       temperature=temperature, seed=sd,
                       prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(),
                       prompt=prompt, text=r.text, parsed=col, strict=strict, legal=ok,
                       cached=r.cached, elapsed=r.elapsed, error=r.error,
                       eval_count=r.meta.get('eval_count'),
                       prompt_eval_count=r.meta.get('prompt_eval_count'))
            attempts.append(rec)
            with self.log.open('a', encoding='utf-8') as f:
                f.write(json.dumps(rec, ensure_ascii=False) + '\n')
            if ok:
                return col, attempts, False
        fallback = next(c for c in CENTER_FIRST if c in legal)
        return fallback, attempts, True


def run_tactics(ch, positions):
    rows = []
    for i, pos in enumerate(positions, 1):
        b = tactics.board_from_moves(pos['moves'])
        col, attempts, fb = ch.ask(b, experiment='tactics', item=pos['id'])
        first = attempts[0]
        rows.append(dict(id=pos['id'], kind=pos['kind'], size=pos['size'],
                         answers=' '.join(map(str, pos['answers'])),
                         raw=first['text'], first_parsed=first['parsed'],
                         first_strict=int(first['strict']), first_legal=int(first['legal']),
                         final_move=col, fallback=int(fb),
                         correct_first=int(first['legal'] and first['parsed'] in pos['answers']),
                         correct_final=int(col in pos['answers']),
                         calls=len(attempts), cached_first=int(first['cached']),
                         seconds_first=round(first['elapsed'], 3),
                         eval_count=first['eval_count'],
                         prompt_eval_count=first['prompt_eval_count']))
        print(f"  [{i:>2}/{len(positions)}] {pos['id']}: {first['text']!r} -> "
              f"{'OK' if rows[-1]['correct_first'] else 'x'}", flush=True)
    return rows


def repro_subset(positions, per_size_kind=None):
    """20 posiciones: las primeras 3 'win' y 2 'block' de cada tamaño... de forma fija."""
    out = []
    for size in tactics.SIZES:
        out += [p for p in positions if p['size'] == size and p['kind'] == 'win'][:3]
        out += [p for p in positions if p['size'] == size and p['kind'] == 'block'][:2]
    return out


def run_repro(ch, positions, seeds=(1, 2, 3, 4, 5), temps=(0.0, 0.7)):
    rows = []
    for temp in temps:
        for pos in positions:
            b = tactics.board_from_moves(pos['moves'])
            for sd in seeds:
                col, attempts, fb = ch.ask(b, experiment='repro', item=pos['id'],
                                           temperature=temp, seed=sd, retries=0)
                a = attempts[0]
                rows.append(dict(id=pos['id'], kind=pos['kind'], size=pos['size'],
                                 temperature=temp, seed=sd, raw=a['text'],
                                 parsed=a['parsed'], legal=int(a['legal']),
                                 correct=int(a['legal'] and a['parsed'] in pos['answers']),
                                 cached=int(a['cached']), seconds=round(a['elapsed'], 3)))
            got = [r['parsed'] for r in rows[-len(seeds):]]
            print(f"  T={temp} {pos['id']}: {got}", flush=True)
    return rows


def play_vs_agent(ch, llm_color, opening, game_id, budget_ms=tournament.BUDGET_MS):
    """Partida LLM vs nuestro agente. El LLM siempre 've' sus fichas como X."""
    board = Connect4()
    player = MAX
    moves, events = [], []
    for col in opening:
        board.push(col, player)
        moves.append(col)
        player = -player
    while board.winner() is None and not board.full():
        view = tournament.as_max(board, player)
        if player == llm_color:
            wins = tactics.winning_moves(view, MAX)
            threats = tactics.winning_moves(view, MIN)
            col, attempts, fb = ch.ask(view, experiment='games',
                                       item=f'{game_id}-ply{len(moves)}')
            events.append(dict(game=game_id, ply=len(moves), llm_color='X' if llm_color == MAX else 'O',
                               raw=attempts[0]['text'], first_legal=int(attempts[0]['legal']),
                               move=col, fallback=int(fb), calls=len(attempts),
                               seconds=round(sum(a['elapsed'] for a in attempts), 3),
                               had_win=' '.join(map(str, wins)),
                               missed_win=int(bool(wins) and col not in wins),
                               threats=' '.join(map(str, threats)),
                               missed_block=int(not wins and len(threats) == 1 and col not in threats),
                               board_seen=str(view)))
        else:
            col = starter.choose_move(view, budget_ms)
        board.push(col, player)
        moves.append(col)
        player = -player
    w = board.winner()
    result = 'LLM' if w == llm_color else ('agente' if w == -llm_color else 'empate')
    return dict(game=game_id, llm_color='X' if llm_color == MAX else 'O',
                opening=''.join(map(str, opening)), winner=result, plies=len(moves),
                moves=' '.join(map(str, moves))), events


def run_games(ch, n_openings=4):
    games, events = [], []
    for k, op in enumerate(tournament.openings(n_openings)):
        for color in (MAX, MIN):
            gid = f'g{k}{"X" if color == MAX else "O"}'
            g, ev = play_vs_agent(ch, color, op, gid)
            games.append(g)
            events += ev
            print(f"  {gid} apertura {op}: gana {g['winner']} en {g['plies']} jugadas", flush=True)
    return games, events


def _write(path, rows):
    import csv
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--only', choices=['tactics', 'repro', 'games'])
    ap.add_argument('--model', default=MODEL)
    args = ap.parse_args(argv)
    ch = Challenger(model=args.model)
    tag = args.model.split(':')[-1]
    if ch.llm.backend != BACKEND:
        sys.exit(f'backend {ch.llm.backend!r} no es {BACKEND!r}: no medimos sin un modelo real')
    if args.check:
        r = ch.llm.complete('Reply with the number 3 and nothing else.', use_cache=False)
        print(repr(r.text), r.error, f'{r.elapsed:.2f}s')
        return
    OUT.mkdir(exist_ok=True)
    positions = tactics.load()
    timings = {}
    if args.only in (None, 'tactics'):
        t0 = time.perf_counter()
        _write(OUT / f'llm_tactics_{tag}.csv', run_tactics(ch, positions))
        timings['tactics'] = round(time.perf_counter() - t0, 1)
    if args.only in (None, 'repro'):
        t0 = time.perf_counter()
        _write(OUT / f'llm_repro_{tag}.csv', run_repro(ch, repro_subset(positions)))
        timings['repro'] = round(time.perf_counter() - t0, 1)
    if args.only in (None, 'games'):
        t0 = time.perf_counter()
        games, events = run_games(ch)
        _write(OUT / f'llm_games_{tag}.csv', games)
        _write(OUT / f'llm_game_moves_{tag}.csv', events)
        timings['games'] = round(time.perf_counter() - t0, 1)
    meta_path = OUT / 'metadata.json'
    meta = json.loads(meta_path.read_text(encoding='utf-8')) if meta_path.exists() else {}
    import platform
    meta.update(backend=BACKEND, prompt=PROMPT, python=platform.python_version(),
                platform=platform.platform(),
                ollama_options='temperature y seed; resto por defecto del harness')
    run = meta.setdefault('runs', {}).setdefault(args.model, {})
    run.setdefault('seconds', {}).update(timings)
    run['last_run_utc'] = datetime.now(timezone.utc).isoformat()
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding='utf-8')


if __name__ == '__main__':
    main()
