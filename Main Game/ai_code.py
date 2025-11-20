import random
from move_storage import load_data, update_data

class RPS_AI:
    """
    A single Markov chain model that predicts the player's next move
    based on the last `memory_length` moves.
    Note,this is the legacy model,scroll down to Multi_RPS_AI,that is in use right now.
    """

    def __init__(self, file_path="moves.json", memory_length=1):
        self.file_path = file_path
        self.memory_length = memory_length
        self.sequence = load_data(self.file_path)
        self.prev_moves = []  # last n moves (memory_length)

    def store_moves(self, cur_move):
        """Update transition counts for this model."""
        if len(self.prev_moves) == self.memory_length:
            key = ''.join(self.prev_moves)
            self.sequence = update_data(self.sequence, key, cur_move, self.file_path)

        self.prev_moves.append(cur_move)
        if len(self.prev_moves) > self.memory_length:
            self.prev_moves.pop(0)

    def prediction(self):
        """Predict the player's next move based on transition frequencies."""
        if len(self.prev_moves) < self.memory_length:
            return random.choice(['r', 'p', 's'])

        key = ''.join(self.prev_moves)
        next_count = self.sequence.get(key, {'r': 0, 'p': 0, 's': 0})

        if sum(next_count.values()) == 0:
            return random.choice(['r', 'p', 's'])

        return max(next_count, key=next_count.get)

    def choose_ai_move(self):
        """Return the AI move that beats the predicted player move."""
        counters = {'r': 'p', 'p': 's', 's': 'r'}
        return counters[self.prediction()]


class Multi_RPS_AI:
    """
    Uses multiple RPS_AI models (different memory lengths).
    Each model is judged INDIVIDUALLY based on how its own prediction would have performed each round.
    """

    def __init__(self, file_path="moves.json", max_m=5, focus_length=5):
        """
        max_m is the number of models to create,so 5 models
        focus_length is the number of recent rounds used to evaluate performance
        """
        self.models = [RPS_AI(file_path, m) for m in range(1, max_m + 1)]
        self.focus_length = focus_length
        self.scores = [[] for _ in range(max_m)]  # scores per model

    def score_model(self, ai_move, player_move):
        """
        Returns +1, 0, or -1 depending on AI model's move outcome.
        """
        if ai_move == player_move:
            return 0#model drew the game
        elif (ai_move == "r" and player_move == "s") or \
             (ai_move == "p" and player_move == "r") or \
             (ai_move == "s" and player_move == "p"):
            return 1  # model wins the game
        else:
            return -1  # model loses

    def update_scores(self, player_move):
        """Score each model individually based on THEIR predicted move.
        Each model predicts independently using its own markov chain,and so I score
        it based on how its prediction would have performed
        """
        for i, model in enumerate(self.models):
            ai_move = model.choose_ai_move()
            r = self.score_model(ai_move, player_move)

            self.scores[i].append(r)
            if len(self.scores[i]) > self.focus_length:
                self.scores[i].pop(0)

    def best_ai(self):
        """select the model with highest recent score sum.
        Note,if all models have a tie,a random model is picked
        """
        totals = [sum(s[-self.focus_length:]) for s in self.scores]

        if len(set(totals)) == 1:
            return random.choice(self.models)

        return self.models[totals.index(max(totals))]

    def get_move(self):
        """Get  a move from the best-performing model."""
        ai = self.best_ai()
        return ai.choose_ai_move()

    def update_all(self, player_move):
        """Update all models with the player's latest move
        This ensures the models keep learning,even if they are not selected for prediciton"""
        for ai in self.models:
            ai.store_moves(player_move)
