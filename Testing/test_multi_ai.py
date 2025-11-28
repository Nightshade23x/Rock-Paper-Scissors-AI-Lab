import unittest
import sys, os

ROOT = os.path.dirname(os.path.dirname(__file__))
AI_PATH = os.path.join(ROOT, "Main Game")
sys.path.insert(0, AI_PATH)

from ai_code import Multi_RPS_AI, RPS_AI


class TestMultiRPSAI(unittest.TestCase):
    """Tests for the multi rps ai system"""

    def setUp(self):
        self.test_file = "test_multi.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.multi = Multi_RPS_AI(file_path=self.test_file, max_m=5, focus_length=5)

    def test_models_created(self):
        """Ensure that exactly 5 models are created and all are RPS_AI."""
        self.assertEqual(len(self.multi.models), 5)
        self.assertTrue(all(isinstance(m, RPS_AI) for m in self.multi.models))

    def test_update_all_updates_models(self):
        """update_all should store the player's move in each model's memory."""
        self.multi.update_all('p')
        for m in self.multi.models:
            self.assertEqual(m.prev_moves, ['p'])

    def test_update_model_scores(self):
        """update_model_scores should add one score per model each round."""
        self.multi.update_model_scores("r")
        self.multi.update_model_scores("p")

        # each model should have exactly 2 scores
        for score_list in self.multi.scores:
            self.assertEqual(len(score_list), 2)

        # all scores must be in [-1, 0, +1]
        for score_list in self.multi.scores:
            for s in score_list:
                self.assertIn(s, [-1, 0, 1])

    def test_best_ai_selects_highest_score(self):
        """best_ai should return the model with the largest score total."""
        self.multi.scores[3] = [+1, +1, +1, +1, +1]  # give model 3 the highest sum
        self.assertIs(self.multi.best_ai(), self.multi.models[3])

    def test_get_move_uses_best_model(self):
        """get_move should use the move predicted by the best-performing model."""
        # force model 0 to always predict 'r'
        self.multi.models[0].prediction = lambda: "r"
        # give model 0 highest score
        self.multi.scores[0] = [+1, +1, +1, +1, +1]

        move = self.multi.get_move()
        self.assertEqual(move, "p")  # p beats r


if __name__ == "__main__":
    unittest.main()
