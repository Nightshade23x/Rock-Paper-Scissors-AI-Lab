import unittest
import sys, os

ROOT = os.path.dirname(os.path.dirname(__file__))
AI_PATH = os.path.join(ROOT, "Main Game")
sys.path.insert(0, AI_PATH)

from ai_code import Multi_RPS_AI, RPS_AI


class TestMultiRPSAI(unittest.TestCase):
    """
    Tests for the multi rps ai system
    """

    def setUp(self):
        """
        Creates a fresh Multi_RPS_AI instance and a clean test JSON file before each test to ensure isolation and consistent state
        """
        self.test_file = "test_multi.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.multi = Multi_RPS_AI(file_path=self.test_file, max_m=5, focus_length=5)

    def test_models_created(self):
        """
        Ensure that exactly 5 models are created and all are RPS_AI.
        """
        self.assertEqual(len(self.multi.models), 5)
        self.assertTrue(all(isinstance(m, RPS_AI) for m in self.multi.models))

    def test_update_all_updates_models(self):
        """
        Update_all should store the player's move in each model's memory.
        """
        self.multi.update_all('p')
        for m in self.multi.models:
            self.assertEqual(m.prev_moves, ['p'])

    def test_update_model_scores(self):
        """
        Update_model_scores should add one score per model each round.
        """
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
        """
        best_ai should return the model with the largest score total.
        """
        self.multi.scores[3] = [+1, +1, +1, +1, +1]  # give model 3 the highest sum
        self.assertIs(self.multi.best_ai(), self.multi.models[3])

    def test_get_move_uses_best_model(self):
        """
        get_move should use the move predicted by the best-performing model.
        """
        # force model 0 to always predict 'r'
        self.multi.models[0].prediction = lambda: "r"
        # give model 0 highest score
        self.multi.scores[0] = [+1, +1, +1, +1, +1]

        move = self.multi.get_move()
        self.assertEqual(move, "p")  # p beats r
    
    def test_multi_handles_invalid_prev(self):
        """
        Ensures the multi model system remains stable even when one model contains corrupted history data.
        """
        # Simulate corrupted history in one model
        self.multi.models[2].prev_moves = ["x", "y"]
        move = self.multi.get_move()
        # Should not crash; must return a valid move
        self.assertIn(move, ["r", "p", "s"])
    
    def test_scores_trim_to_focus_length(self):
        """
        Verifies that the score lists for each model never exceed the defined focus length.After more than 'focus_length' updates, the score lists should be trimmed to maintain only the most recent scores.
        """
        # focus_length = 5 from setup
        for _ in range(10):  # add more scores than the window
            self.multi.update_model_scores("r")
        # all models must have exactly focus_length items
        for score_list in self.multi.scores:
            self.assertEqual(len(score_list), 5)
    
    def test_best_ai_handles_ties(self):
        """
        Confirms that best_ai behaves correctly when 2 or more models have the same total score.In the event of a tie,the method should still return a valid model without any errors.
        """
        # force model 0 and 1 to have equal sums
        self.multi.scores[0] = [1, 1, 1]
        self.multi.scores[1] = [1, 1, 1]
        best = self.multi.best_ai()
        self.assertIn(best, [self.multi.models[0], self.multi.models[1]])

if __name__ == "__main__":
    unittest.main()
