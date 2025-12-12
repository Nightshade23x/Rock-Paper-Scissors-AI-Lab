import unittest
import sys, os
BASE = os.path.dirname(os.path.dirname(__file__))
ai_path = os.path.join(BASE, "Main Game")
sys.path.append(ai_path)

from ai_code import RPS_AI

"""
These tests ensure that the AI behaves predictibly when it encounters unsual state conditions
such as inefficient move history or unexpected keys in the transition data.
The goal is not to verify predicitons but simply ensure stability and sustainability of the code 
regardless of what it faces.
"""

class TestEdgeCases(unittest.TestCase):
    
    def test_empty_prev_moves(self):
        """
        Tests the AI's prediction when there are fewer prev moves than required
        by the specified memory length
        Expected behaviour is that since the AI doesnt have enough data to form a key
        for the transition dict,it should default to a safe random move,either r,p or s
        """
        ai = RPS_AI(memory_length=3)
        pred = ai.prediction()
        self.assertIn(pred, ["r", "p", "s"])

    def test_missing_key_in_json(self):
        """
        Tests how the AI responds when its prev move history form a key that does not exist
        in the matrix,eg invalid moves.This hopes to simulate corrupted data.
    Expected behaviour is that the AI shouldnt crash,and fall back to random choice behaviour.
        """
        ai = RPS_AI()
        ai.prev_moves = ["x"]  # invalid key
        pred = ai.prediction()
        self.assertIn(pred, ["r", "p", "s"])

if __name__ == "__main__":
    unittest.main()

