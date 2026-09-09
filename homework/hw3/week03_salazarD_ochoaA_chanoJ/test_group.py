"""Comprobaciones del grupo; no reemplazan los tests del profesor."""
import unittest
from collections import deque
from search import Problem, EightPuzzle, GOAL, D8
from starter import MissionariesAndCannibals, bfs, ids, depth_limited, measure


class Graph(Problem):
    def __init__(self, edges, initial='S', goal='G'):
        super().__init__(initial, goal)
        self.edges = edges
    def actions(self, state):
        return self.edges.get(state, [])
    def result(self, state, action):
        return action


class GroupTests(unittest.TestCase):
    def test_all_legal_crossings(self):
        p = MissionariesAndCannibals()
        for m in range(4):
            for c in range(4):
                for boat in (0, 1):
                    state = (m, c, boat)
                    if not p.is_valid(state):
                        self.assertEqual(p.actions(state), [])
                        continue
                    expected = set()
                    for dm in range(3):
                        for dc in range(3):
                            if not 1 <= dm + dc <= 2:
                                continue
                            sign = -1 if boat == 0 else 1
                            ml, cl = m + sign * dm, c + sign * dc
                            if not (0 <= ml <= 3 and 0 <= cl <= 3):
                                continue
                            if (ml and cl > ml) or (3-ml and 3-cl > 3-ml):
                                continue
                            expected.add((dm, dc))
                    self.assertEqual(set(p.actions(state)), expected)

    def test_missionaries_solution(self):
        p = MissionariesAndCannibals()
        for algorithm in (bfs, ids):
            node, _ = algorithm(p)
            self.assertEqual(len(node.path()), 11)
            state = p.initial
            for action in node.path():
                self.assertIn(action, p.actions(state))
                state = p.result(state, action)
                self.assertTrue(p.is_valid(state))
            self.assertEqual(state, p.goal)

    def test_cutoff_and_exhaustion(self):
        p = Graph({'S': ['A'], 'A': ['S']})
        self.assertEqual(depth_limited(p, 0), (None, 0, True))
        self.assertFalse(depth_limited(p, 1)[2])
        self.assertIsNone(ids(p)[0])
        self.assertEqual(depth_limited(Graph({}), 0), (None, 0, False))

    def test_revisit_via_shorter_path(self):
        # A global visited set would incorrectly discard the second route to X.
        p = Graph({'S': ['A', 'X'], 'A': ['B'], 'B': ['X'], 'X': ['G']})
        node, _, _ = depth_limited(p, 2)
        self.assertEqual(node.path(), ['X', 'G'])

    def test_initial_goal_and_depth_boundary(self):
        node, exp = ids(EightPuzzle(GOAL), 0)
        self.assertEqual((node.path(), exp), ([], 0))
        self.assertIsNone(ids(EightPuzzle(D8), 7)[0])
        self.assertEqual(len(ids(EightPuzzle(D8), 8)[0].path()), 8)
        with self.assertRaises(ValueError):
            depth_limited(EightPuzzle(D8), -1)

    def test_empty_bank(self):
        self.assertEqual(measure({}), [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
