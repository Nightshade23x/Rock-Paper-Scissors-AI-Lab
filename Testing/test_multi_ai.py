import unittest
import os
from ai_code import Multi_RPS_AI, RPS_AI


class TestMultiRPSAI(unittest.TestCase):
    """Tests for the multi rps ai system"""

    def setUp(self):
        self.test_file = "test_multi.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.multi = Multi_RPS_AI(file_path=self.test_file, max_m=5, focus_length=5)

    def test_models_created(self):
        self.assertEqual(len(self.multi.models), 5)
        self.assertTrue(all(isinstance(m, RPS_AI) for m in self.multi.models))

    def test_update_all_updates_models(self):
        self.multi.update_all('p')
        for m in self.multi.models:
            self.assertEqual(m.prev_moves, ['p'])

    def test_update_scores(self):
        self.multi.update_scores(+1)
        self.multi.update_scores(-1)
        for score_list in self.multi.scores:
            self.assertEqual(score_list, [+1, -1])

    def test_best_ai_selects_highest_score(self):
        # give model index 3 the highest score
        self.multi.scores[3] = [+1, +1, +1, +1, +1]
        self.assertIs(self.multi.best_ai(), self.multi.models[3])

    def test_get_move_uses_best_model(self):
        # force model[0] to be best
        self.multi.models[0].prediction = lambda: "r"
        self.multi.scores[0] = [+1, +1, +1, +1, +1]
        move = self.multi.get_move(player_history=[])
        self.assertEqual(move, "p")   # p beats r


if __name__=="__main__":
    unittest.main()