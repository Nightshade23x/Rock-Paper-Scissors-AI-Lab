
from ai_code import RPS_AI
import unittest
import sys, os

ROOT = os.path.dirname(os.path.dirname(__file__))
AI_PATH = os.path.join(ROOT, "Main Game")
sys.path.insert(0, AI_PATH)

class Testing(unittest.TestCase):
    """Tests for single model RPS_AI"""
    def setUp(self):
        self.ai=RPS_AI()
        self.test_file="tests_single.json"#making a new json file to store tests,i dont want to pollute my storage file
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.ai=RPS_AI(file_path=self.test_file)

    def test_store_moves(self):
        #simulated p and then s
        self.ai.prev_moves=['p']
        self.ai.store_moves('s')
        #check if the matrix is working and storing values
        self.assertEqual(self.ai.sequence['p']['s'],1)

    def test_prediction_beginning(self):
        #no prev move yet,so prediciton should be random
        predicted=self.ai.prediction()
        self.assertIn(predicted,['r','p','s'])

    def test_prediciton_after(self):
        # simulate p followed by s 100 times
        for x in range(100):
            self.ai.prev_moves=['p']
            self.ai.store_moves('s')
        self.ai.prev_moves='p'
        #since prev move is p,prediction should be s
        predicted=self.ai.prediction()
        self.assertEqual(predicted,'s')

    def test_if_ai_wins(self):
        #if ai predicts r,then it should choose p,because p beats r
        self.ai.prediction=lambda:'r'#this is for a mock prediction result
        ai_move=self.ai.choose_ai_move()
        self.assertEqual(ai_move,'p')