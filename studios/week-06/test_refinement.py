"""Regression checks for refinement, without calling a language model."""
import contextlib
import io
import json
import unittest

from logic_lm import worked_examples
from starter import solve_arm_b_with_refinement


class ScriptedModel:
    def __init__(self, replies):
        self.replies = iter(replies)
        self.prompts = []

    def complete(self, prompt):
        self.prompts.append(prompt)
        return next(self.replies)


class RefinementTests(unittest.TestCase):
    def run_case(self, replies, retries=3):
        example = worked_examples()[0]
        model = ScriptedModel(replies)
        with contextlib.redirect_stdout(io.StringIO()):
            result = solve_arm_b_with_refinement(
                model, example['puzzle'], gold=example['gold'], max_retries=retries
            )
        return result, model

    def test_recovers_from_invalid_structure_and_returns_feedback(self):
        good = json.dumps(worked_examples()[0]['spec'])
        bad = json.dumps({'variables': {'X': [1]}, 'constraints': [None]})
        result, model = self.run_case([bad, good])
        self.assertEqual((result[0], result[2]), ('correct', 2))
        self.assertIn('AttributeError', model.prompts[1])
        self.assertIn(bad, model.prompts[1])

    def test_retries_unsatisfiable_translation(self):
        bad = json.dumps({'variables': {'X': [1]}, 'constraints': [
            {'type': 'eq', 'a': 'X', 'b': 2}]})
        result, model = self.run_case([bad, json.dumps(worked_examples()[0]['spec'])])
        self.assertEqual((result[0], result[2]), ('correct', 2))
        self.assertIn('no solution', model.prompts[1])

    def test_stops_at_attempt_budget(self):
        result, model = self.run_case(['not JSON'] * 3)
        self.assertEqual((result[0], result[2]), ('malformed_json', 3))
        self.assertEqual(len(model.prompts), 3)

    def test_gold_mismatch_does_not_trigger_retry(self):
        reply = json.dumps({'variables': {'X': [1]}, 'constraints': []})
        result, model = self.run_case([reply])
        self.assertEqual((result[0], result[2]), ('valid_json_wrong_model', 1))
        self.assertEqual(len(model.prompts), 1)


if __name__ == '__main__':
    unittest.main()
