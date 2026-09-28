"""Comprobaciones del grupo; no reemplazan los tests del profesor (test_alphabeta.py)."""
import time
import unittest

from connect4 import Connect4, MAX, MIN, CENTER_FIRST
import starter
import tactics
import tournament
from llm_challenger import parse_move, make_prompt, PROMPT


def snapshot(b):
    return [row[:] for row in b.grid], b.heights[:]


class AgentTests(unittest.TestCase):
    def test_dynamic_order_puts_previous_best_first(self):
        b = Connect4()
        self.assertEqual(starter.order_moves(b), CENTER_FIRST)
        self.assertEqual(starter.order_moves(b, first=6), [6, 3, 2, 4, 1, 5, 0])
        self.assertEqual(sorted(starter.order_moves(b, first=6)), b.legal_moves())

    def test_order_skips_full_columns(self):
        b = Connect4()
        for k in range(6):
            b.push(3, MAX if k % 2 else MIN)
        self.assertNotIn(3, starter.order_moves(b, first=3))
        self.assertEqual(sorted(starter.order_moves(b)), b.legal_moves())

    def test_choose_move_does_not_mutate_board(self):
        b = tactics.board_from_moves([3, 3, 2, 4])
        before = snapshot(b)
        starter.choose_move(b, 200)
        self.assertEqual(snapshot(b), before)

    def test_tiny_budget_still_legal(self):
        b = tactics.board_from_moves([3, 3, 2, 4])
        self.assertIn(starter.choose_move(b, 1), b.legal_moves())

    def test_hard_stop_bounds_time_and_keeps_board(self):
        # Forzamos a empezar siempre otra profundidad: solo el corte duro detiene la búsqueda.
        b = tactics.board_from_moves([3, 3, 2, 4])
        before = snapshot(b)
        old = starter.SAFETY
        starter.SAFETY = 100.0
        try:
            t0 = time.perf_counter()
            move, info = starter.search_profile(b, 100)
            ms = (time.perf_counter() - t0) * 1000
        finally:
            starter.SAFETY = old
        self.assertIn(move, b.legal_moves())
        self.assertLess(ms, 100 * starter.HARD_STOP + 50)
        self.assertEqual(snapshot(b), before)

    def test_last_empty_cell(self):
        # Tablero casi lleno sin ganador: una sola columna legal.
        b = Connect4()
        for r in range(6):
            for c in range(7):
                b.grid[r][c] = MAX if (c // 2 + r % 2) % 2 == 0 else MIN
        b.grid[5][6] = 0
        b.heights = [6] * 6 + [5]
        self.assertIsNone(b.winner())
        self.assertEqual(starter.choose_move(b, 100), 6)


class BankTests(unittest.TestCase):
    def test_bank_is_reproducible(self):
        self.assertEqual(tactics.generate(), tactics.load())

    def test_bank_answers_are_verified(self):
        bank = tactics.load()
        self.assertEqual(len(bank), 80)
        for pos in bank:
            b = tactics.board_from_moves(pos['moves'])
            self.assertIsNone(b.winner())
            self.assertEqual(sum(b.heights), pos['size'])
            if pos['kind'] == 'win':
                self.assertEqual(tactics.winning_moves(b, MAX), pos['answers'])
            else:
                self.assertEqual(tactics.winning_moves(b, MAX), [])
                self.assertEqual(tactics.winning_moves(b, MIN), pos['answers'])
                self.assertEqual(len(pos['answers']), 1)


class TournamentTests(unittest.TestCase):
    def test_as_max_swaps_colors_without_mutating(self):
        b = tactics.board_from_moves([3, 2])
        before = snapshot(b)
        v = tournament.as_max(b, MIN)
        self.assertEqual(snapshot(b), before)
        self.assertEqual(v.grid[0][3], -b.grid[0][3])
        self.assertIs(tournament.as_max(b, MAX).grid is b.grid, False)

    def test_illegal_move_loses(self):
        g = tournament.play_game(lambda b, t: 99, lambda b, t: 0)
        self.assertEqual((g['winner'], g['reason']), (MIN, 'ilegal'))

    def test_timeout_forfeits(self):
        import time

        def slow(b, t):
            time.sleep(0.05)
            return b.legal_moves()[0]
        g = tournament.play_game(slow, lambda b, t: 0, budget_ms=10)
        self.assertEqual((g['winner'], g['reason']), (MIN, 'tiempo'))


class LLMParsingTests(unittest.TestCase):
    """Casos sintéticos para el parser: NO son respuestas observadas del modelo."""
    def test_parse(self):
        self.assertEqual(parse_move('3'), (3, True))
        self.assertEqual(parse_move(' 4\n'), (4, True))
        self.assertEqual(parse_move('Column 5.'), (5, False))
        self.assertEqual(parse_move('I play column 12'), (12, False))
        self.assertEqual(parse_move('center'), (None, False))

    def test_prompt_is_the_plan_prompt(self):
        b = tactics.board_from_moves([3, 3])
        p = make_prompt(b)
        self.assertTrue(p.startswith("Connect-4. You are 'X'."))
        self.assertIn(str(b), p)
        self.assertIn('Legal columns: [0, 1, 2, 3, 4, 5, 6]', p)
        self.assertEqual(p, PROMPT.format(board=str(b), legal=b.legal_moves()))


if __name__ == '__main__':
    unittest.main(verbosity=2)
