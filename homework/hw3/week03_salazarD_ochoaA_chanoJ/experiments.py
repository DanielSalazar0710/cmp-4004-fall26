"""Medición reproducible de las 160 combinaciones del studio."""
import csv
import hashlib
import json
import platform
import time
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, median
from starter import measure
from search import load_instances

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / 'resultados'

def fingerprints():
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in ['starter.py', 'search.py', 'instances.json']}

def run():
    RESULTS.mkdir(exist_ok=True)
    bank = load_instances()
    start = time.perf_counter()
    raw = measure(bank)
    elapsed = time.perf_counter() - start
    rows = []
    for i, (depth, algorithm, expansions, length) in enumerate(raw):
        index = (i // 4) % len(bank[depth])
        rows.append(dict(depth=depth, instance=index + 1, algorithm=algorithm,
                         expansions=expansions, solution_length=length))
    assert len(rows) == 160
    assert all(r['solution_length'] == r['depth'] for r in rows if r['algorithm'] != 'DFS')
    with (RESULTS / 'measurements.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    metadata = dict(utc=datetime.now(timezone.utc).isoformat(), python=platform.python_version(),
                    platform=platform.platform(), seconds_total=elapsed, runs=len(rows),
                    fingerprints=fingerprints(),
                    csv_sha256=hashlib.sha256((RESULTS / 'measurements.csv').read_bytes()).hexdigest())
    (RESULTS / 'metadata.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    return rows

def load():
    metadata = json.loads((RESULTS / 'metadata.json').read_text(encoding='utf-8'))
    if metadata['fingerprints'] != fingerprints():
        raise ValueError('El código o las instancias cambiaron: ejecutar python experiments.py')
    if hashlib.sha256((RESULTS / 'measurements.csv').read_bytes()).hexdigest() != metadata['csv_sha256']:
        raise ValueError('El CSV cambió: repetir la medición')
    with (RESULTS / 'measurements.csv').open(encoding='utf-8', newline='') as f:
        return [{k: v if k == 'algorithm' else int(v) for k, v in row.items()}
                for row in csv.DictReader(f)]

def summarize(rows):
    summary = []
    for depth in sorted({r['depth'] for r in rows}):
        for algorithm in ['BFS', 'DFS', 'UCS', 'IDS']:
            group = [r for r in rows if r['depth'] == depth and r['algorithm'] == algorithm]
            summary.append(dict(depth=depth, algorithm=algorithm, n=len(group),
                                expansions_mean=mean(r['expansions'] for r in group),
                                expansions_median=median(r['expansions'] for r in group),
                                expansions_min=min(r['expansions'] for r in group),
                                expansions_max=max(r['expansions'] for r in group),
                                length_mean=mean(r['solution_length'] for r in group),
                                length_min=min(r['solution_length'] for r in group),
                                length_max=max(r['solution_length'] for r in group)))
    return summary

def plot(rows):
    import matplotlib.pyplot as plt
    summary = summarize(rows)
    plt.rcParams.update({'font.size': 11, 'axes.spines.top': False, 'axes.spines.right': False})
    fig, ax = plt.subplots(figsize=(10, 5.5), layout='constrained')
    colors = {'BFS': '#126782', 'DFS': '#b54732', 'UCS': '#643c9c', 'IDS': '#228352'}
    for algorithm, marker, style in [('BFS', 'o', '-'), ('DFS', 's', '-'),
                                      ('UCS', 'x', '--'), ('IDS', '^', '-')]:
        group = [r for r in summary if r['algorithm'] == algorithm]
        ax.plot([r['depth'] for r in group], [r['expansions_mean'] for r in group],
                marker=marker, linestyle=style, color=colors[algorithm], label=algorithm,
                linewidth=2, markersize=8)
        for r in rows:
            if r['algorithm'] == algorithm:
                ax.scatter(r['depth'], r['expansions'], color=colors[algorithm], s=14, alpha=.20)
    ax.set(yscale='log', xticks=[4, 8, 12, 16], xlabel='Profundidad óptima de la instancia',
           ylabel='Nodos expandidos (escala logarítmica)',
           title='8-puzzle: trabajo de búsqueda frente a profundidad')
    ax.grid(axis='y', which='both', alpha=.18)
    ax.legend(title='Media de 10 instancias; puntos = corridas')
    fig.savefig(RESULTS / 'scaling.png', dpi=180)
    fig.savefig(RESULTS / 'scaling.svg')
    return fig

if __name__ == '__main__':
    rows = run()
    summary = summarize(rows)
    with (RESULTS / 'summary.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(summary[0]))
        writer.writeheader()
        writer.writerows(summary)
    plot(rows)
    print(json.dumps(summary, indent=2))
