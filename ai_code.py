import random
from move_storage import load_data,update_data

class RPS_AI:
    """
    Markov chain will predict the player's next move based on their historical playing style and counter it
    """
    def __init__(self):
        """
        sequence is essentially a transition matrix which will track how many times each move choice is followed by another
        """
        self.sequence=load_data()
        #for sequnce,each prev move maps to how many times the player played either one of the choices afterwards
        self.prev_move=None#in the beginning,we have no prev move

    def store_moves(self,cur_move):
        """
        Record the player's current move and update the matrix
        """
        if self.prev_move:
            update_data(self.sequence,self.prev_move,cur_move)
        self.prev_move=cur_move

    def prediction(self):
        """"
        This is where the magic happens,the player's move is predicted based on transition probabilities
        """
        if self.prev_move is None:
            return random.choice(['r','p','s'])
        #retrieve how many times each move followed the prev one
        next_count=self.sequence[self.prev_move]
        total=sum(next_count.values())
        #if we just started and have no data,choose a random move to kick off the matrix
        if total==0:
            return random.choice(['r','p','s'])
        #otherwise if all is well,return the move that has happened most often after the move the player just played
        return max(next_count,key=next_count.get)
    
    def choose_ai_move(self):
        """
        Choose the AI's move that will beat the player's move(well predicted one)
        """
        move_predicted=self.prediction()
        #define which move beats which(logic behind normal RPS)
        counters={'r':'p','p':'s','s':'r'}
        return counters[move_predicted]

    