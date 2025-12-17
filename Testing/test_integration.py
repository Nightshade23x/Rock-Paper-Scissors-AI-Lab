import unittest
import sys, os

ROOT = os.path.dirname(os.path.dirname(__file__))
AI_PATH = os.path.join(ROOT, "Main Game")
sys.path.insert(0, AI_PATH)


from ai_code import Multi_RPS_AI

"""
These following tests ensure that all components of the multi-model system work together
perfectly when simulated over multiple rounds of gameplay.
The goal is to ensure the AI system behaves consistently without throwing errors or 
providing invalid state transitions.
"""

class TestIntegration(unittest.TestCase):

    def test_multi_round_learning(self):
        """
        Steps:
        1.A temp JSON file was created to store transition data.
        2.A multi RPS instance is initialized with this file.
        3. A repeated move pattern is simulated for 40 cycles.Each cycle will update
        each model's recent result scores.
        4. After learning,the best performing model is retrieved.
        5. Its prediction is checked to see if it produces a valid move.

        These tests simply ensure the system produces valid output and does not fall into
        an invalid state.
        """
    
        test_file = "integration_test.json"
        if os.path.exists(test_file):
            os.remove(test_file)

        ai = Multi_RPS_AI(file_path=test_file)

        # simulate repeated pattern: player plays 'r' then 'p'
        for _ in range(40):
            ai.update_all('r')
            ai.update_model_scores('r')
            ai.update_all('p')
            ai.update_model_scores('p')

        # after enough learning, at least one model should predict properly
        best = ai.best_ai()
        best.prev_moves = ["r"]
        prediction = best.prediction()
        self.assertIn(prediction, ["p", "r", "s"])

if __name__ == "__main__":
    unittest.main()

