import json
import os

def load_data(file_path="moves.json"):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return {
        "r": {"r": 0, "p": 0, "s": 0},
        "p": {"r": 0, "p": 0, "s": 0},
        "s": {"r": 0, "p": 0, "s": 0}
    }

def save_data(data,file_path="moves.json"):
    with open(file_path, "w") as f:
        json.dump(data, f)

def update_data(data, prev_move, curr_move,file_path="moves.json"):
    if prev_move:
        data[prev_move][curr_move] += 1
        save_data(data)
