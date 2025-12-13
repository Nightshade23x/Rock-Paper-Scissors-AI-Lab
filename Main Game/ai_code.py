import random
from move_storage import load_data, update_data

class RPS_AI:
    """
    A single Markov chain model that predicts the player's next move
    based on the last `memory_length` moves.
    RPS_AI is the core prediction engine used by all models
    """

    def __init__(self, file_path="moves.json", memory_length=1):
        """
        Initialize a single RPS_AI model.
        file path is the path to the JSON file storing transition data.
        memory_length is the number of previous moves used to form the prefix.
        """
        self.file_path = file_path
        self.memory_length = memory_length
        self.sequence = load_data(self.file_path)
        self.prev_moves = []  # last n moves (memory_length)

    def store_moves(self, cur_move):
        """Update transition counts for this model.
        cur_move stores the player's most recent move.
        """
        if len(self.prev_moves) == self.memory_length:
            key = ''.join(self.prev_moves)
            self.sequence = update_data(self.sequence, key, cur_move, self.file_path)

        self.prev_moves.append(cur_move)
        if len(self.prev_moves) > self.memory_length:
            self.prev_moves.pop(0)

    def prediction(self):
        """Predict the player's next move using prefix matching
        If insufficient data exists,or no matching transitions are found,a random move will be played.
        """
    # If not enough history for this model,then choose a random move
        if len(self.prev_moves) < self.memory_length:
            return random.choice(['r', 'p', 's'])

        prefix = ''.join(self.prev_moves)

        # Collect all transitions whose key starts with the prefix
        matched = []
        for key, counts in self.sequence.items():
            if key.startswith(prefix):
                matched.append(counts)

        # If no matching transitions found,use a random move
        if not matched:
            return random.choice(['r', 'p', 's'])

        # Aggregate transition counts from all prefix matching keys
        total = {'r': 0, 'p': 0, 's': 0}
        for c in matched:
            total['r'] += c.get('r', 0)
            total['p'] += c.get('p', 0)
            total['s'] += c.get('s', 0)

        # If all zero,use a random move
        if total['r'] == total['p'] == total['s'] == 0:
            return random.choice(['r', 'p', 's'])

        # Return move with highest frequency
        return max(total, key=total.get)


    def choose_ai_move(self):
        """Return the AI move that beats the predicted player move.
        """
        counters = {'r': 'p', 'p': 's', 's': 'r'}
        return counters[self.prediction()]


class Multi_RPS_AI:
    """
    Uses multiple RPS_AI models (different memory lengths).
    It creates multiple RPS_AI predictors with different memory lenghts
    Each model is judged INDIVIDUALLY based on how its own prediction would have performed each round.
    """

    def __init__(self, file_path="moves.json", max_m=5, focus_length=5):
        """
        file_path is again the JSON file storing the transition data.
        max_m is the number of  RPS_Ai models to create,so 5 models,each with memory length from 1 to max_m
        focus_length is the number of recent rounds used to evaluate performance
        """
        self.models = [RPS_AI(file_path, m) for m in range(1, max_m + 1)]
        self.focus_length = focus_length
        self.scores = [[] for _ in range(max_m)]  # scores per model
    
    def get_move(self):
        """Get a move from the best-performing model.
        Returns the AI's chosen move
        """
        ai = self.best_ai()
        return ai.choose_ai_move()

    def process_round(self, player_move):
        """
        Process a single game round.
        First scores all models based on their predictions,then updates all models with the player's move.
        """
        self.update_model_scores(player_move)
        self.update_all(player_move)


    def score_model(self, ai_move, player_move):
        """
        Returns +1, 0, or -1 depending on AI model's move outcome.
        ai_move is the AI's chosen move.
        player_move is the player's actual move.
        +1 is given to the model if it wins,0 if its a draw and -1 for a loss.
        """
        if ai_move == player_move:
            return 0#model drew the game
        elif (ai_move == "r" and player_move == "s") or \
             (ai_move == "p" and player_move == "r") or \
             (ai_move == "s" and player_move == "p"):
            return 1  # model wins the game
        else:
            return -1  # model loses
   
    def update_model_scores(self,player_move):
        """
        Updates the performance scores for each AI model after each round.
        Each model is scored independently using its own predicted move.
        Only the most recent focus_length scores are kept.
        player_move is the player's actual move for the round.
        """
        for i,model in enumerate(self.models):
            ai_move=model.choose_ai_move()
            r=self.score_model(ai_move,player_move)
            self.scores[i].append(r)
            if len(self.scores[i])>self.focus_length:
                self.scores[i].pop(0)


    def best_ai(self):
        """
        Select the model with the highest recent score sum.
        If multiple models are tied for best performance,one of them is chosen at random.
        """
        totals = [sum(s[-self.focus_length:]) for s in self.scores]
        max_score = max(totals)

        best_indices = [i for i, t in enumerate(totals) if t == max_score]
        chosen_index = random.choice(best_indices)
        return self.models[chosen_index]

   

    def update_all(self, player_move):
        """Update all models with the player's latest move
        This ensures the models keep learning,even if they are not selected for prediciton
        player_move is the player's most recent move.
        """
        for ai in self.models:
            ai.store_moves(player_move)

    
