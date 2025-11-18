import random
from move_storage import load_data,update_data

class RPS_AI:
    """
    A single Markov chain will predict the player's next move based on their previous moves of a given memory length
    This forms the base for Multi RPS AI...each RPS AI uses a different memory length i.e (1,2,3,4,5 etc) to capture
    different levels of player behaviour patterns.
    """
    def __init__(self,file_path="moves.json",memory_length=1):
        """
        memory_length is how many past moves the AI remembers
        file path leads to the json file storing the move transitions
        """
        self.file_path=file_path
        self.memory_length=memory_length
        self.sequence=load_data(self.file_path)
        self.prev_moves=[]#store the player's last 'memory length' moves

    def store_moves(self,cur_move):
        """
        Update the matrix with the latest move played.
        """
        if len(self.prev_moves)==self.memory_length:#only start recording once we have enough previous moves.
            key=''.join(self.prev_moves)
            self.sequence=update_data(self.sequence,key,cur_move,self.file_path)
        #updates the move history so it will only keep the last memory length moves.
        self.prev_moves.append(cur_move)
        if len(self.prev_moves)>self.memory_length:
            self.prev_moves.pop(0)

    def prediction(self):
        """"
        This is where the magic happens,the player's move is predicted based on transition probabilities
        If enough data isnt available,a random move will be chosen.
        """
        if len(self.prev_moves)<self.memory_length:
            return random.choice(['r','p','s'])
        key=''.join(self.prev_moves)
        next_count=self.sequence.get(key,{'r':0,'p':0,'s':0})
        #if we just started and have no data,choose a random move to kick off the matrix
        if sum(next_count.values())==0:
            return random.choice(['r','p','s'])
        #otherwise if all is well,return the move that has happened most often after the move the player just played
        return max(next_count,key=next_count.get)

    def choose_ai_move(self):
        """
        Choose the AI's move that will beat the player's move(well predicted one)
        """
        #define which move beats which(logic behind normal RPS)
        counters={'r':'p','p':'s','s':'r'}
        return counters[self.prediction()]

#BELOW IS THE IMPROVED VERSION OF THE AI SYSTEM.
#INSTEAD OF RELYING ON ONE FIXED MARKOV MODEL,IT COMBINES MULTIPLE RPS_AI MODELS WITH DIFFERENT MEMORY LENGTHS
#HENCE IT CAN DYNAMICALLY CHOOSE THE ONE PEROFORMING BEST IN THE RECENT ROUNDS.

class Multi_RPS_AI:
    """
    As mentioned above,we will use multiple models.We will evaluate each model's recent performance in terms of wins and loses
    and choose the best performing model's prediction for the next move.
    """

    def __init__(self,file_path="moves.json",max_m=5,focus_length=5):
        """
        max_m is the number of single models
        focus length is how many of the last few rounds will be used to compare performance
        """
        self.models=[
            RPS_AI(file_path,m)
            for m in range(1,max_m+1)
        ]
        self.focus_length=focus_length
        self.scores=[[] for i in range(max_m)]#this will store the recent results for each AI

    def update_scores(self,result):
        """
        Update each model's score list based on the last game's results
        +1 for an AI win,0 for a draw and -1 for a loss
        """

        for i in range(len(self.scores)):#go thru each model and record the latest round result
            self.scores[i].append(result)
            if len(self.scores[i])>self.focus_length:#keep only the last focus length results to stay relevant
                self.scores[i].pop(0)

    def best_ai(self):
        """
        Here is where we choose which model performed the best in the recent games
        this will be determined by summing its last results.
        """
        totals=[sum(s[-self.focus_length:]) for s in self.scores]
        if len(set(totals))==1:
            return random.choice(self.models)#if all are tied,pick randomly
        #find which model has the highest total score
        return self.models[totals.index(max(totals))]#return the best performing model

    def get_move(self,player_history):
        """
        And here we will get the next move from the best -performing AI
        """
        ai=self.best_ai()#ask the ai for its predicted counter move
        return ai.choose_ai_move()

    def update_all(self,player_move):
        """
        After each round,update all of the models with the latest player moves so all models continue learning
        """
        for ai in self.models:
            ai.store_moves(player_move)


