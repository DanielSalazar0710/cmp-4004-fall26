"""Reejecuta y valida cada ruta, y verifica las profundidades independientemente."""
from collections import deque
import json
from pathlib import Path
import starter as s
import experiments as ex
from search import EightPuzzle, GOAL, load_instances

def verify():
    p = EightPuzzle(GOAL)
    distances = {GOAL: 0}
    queue = deque([GOAL])
    while queue:
        state = queue.popleft()
        for action in p.actions(state):
            child = p.result(state, action)
            if child not in distances:
                distances[child] = distances[state] + 1
                queue.append(child)
    assert len(distances) == 181440
    bank = load_instances()
    assert all(distances[state] == depth for depth, states in bank.items() for state in states)
    algorithms = {'BFS': s.bfs, 'DFS': s.dfs, 'UCS': s.ucs, 'IDS': s.ids}
    steps = 0
    for row in ex.load():
        problem = EightPuzzle(bank[row['depth']][row['instance']-1])
        node, expansions = algorithms[row['algorithm']](problem)
        assert expansions == row['expansions']
        path = node.path()
        assert len(path) == row['solution_length']
        state = problem.initial
        for action in path:
            assert action in problem.actions(state)
            state = problem.result(state, action)
            steps += 1
        assert state == GOAL
        assert node.g == len(path)
    report = dict(reachable_states=len(distances), bank_depths_verified=40,
                  routes_verified=160, legal_moves_replayed=steps,
                  fingerprints=ex.fingerprints())
    (ex.RESULTS / 'verification.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    verify()
