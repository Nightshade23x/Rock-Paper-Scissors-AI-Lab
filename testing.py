import unittest
from ai_code import RPS_AI

class Testing(unittest.TestCase):
    def setUp(self):
        self.ai=RPS_AI()
    
    def test_store_moves(self):
        #simulated p and then s
        self.ai.prev_move='p'
        self.ai.store_moves('s')
        #check if the matrix is working and storing values
        self.assertEqual(self.ai.sequence['p']['s'],1)

    def test_prediction_beginning(self):
        #no prev move yet,so prediciton should be random
        predicted=self.ai.prediction()
        self.assertIn(predicted,['r','p','s'])
    
    def test_prediciton_after(self):
        # simulate p followed by s 5 times
        for x in range(5):
            self.ai.prev_move='p'
            self.ai.store_moves('s')
        self.ai.prev_move='p'
        #since prev move is p,prediction should be s
        predicted=self.ai.prediction()
        self.assertEqual(predicted,'s')
    
    def test_if_ai_wins(self):
        #if ai predicts r,then it should choose p,because p beats r
        self.ai.prediction=lambda:'r'#this is for a mock prediction result
        ai_move=self.ai.choose_ai_move()
        self.assertEqual(ai_move,'p')
if __name__=="__main__":
    unittest.main()