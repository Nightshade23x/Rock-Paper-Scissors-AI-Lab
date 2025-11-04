import random
class RPS_AI:
    def __init__(self):
        self.sequence={choice:{'r':0,'p':0,'s':0} for choice in ['r','p','s']}
        self.prev_move=None

    def store_moves(self,cur_move):
        if self.prev_move:
            self.sequence[self.prev_move][cur_move]+=1
        self.prev_move=cur_move

    def prediction(self):
        next_count=self.sequence[self.prev_move]
        total=sum(next_count.values())
        if total==0:
            return random.choice(['r','p','s'])
        return max(next_count,key=next_count.get)
    
    def choose_ai_move(self):
        move_predicted=self.prediction()
        counters={'r':'p','p':'s','s':'r'}
        return counters[move_predicted]

    