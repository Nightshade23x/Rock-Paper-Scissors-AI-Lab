import unittest
import os
from ai_code import RPS_AI,Multi_RPS_AI

class Testing(unittest.TestCase):
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
            self.ai.prev_move=['p']
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

class TestMultiRPSAI(unittest.TestCase):

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