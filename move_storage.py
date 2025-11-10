import json
import os

FILE_PATH = "moves.json"

def load_data():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as f:
            return json.load(f)
    return {
        "r": {"r": 0, "p": 0, "s": 0},
        "p": {"r": 0, "p": 0, "s": 0},
        "s": {"r": 0, "p": 0, "s": 0}
    }

def save_data(data):
    with open(FILE_PATH, "w") as f:
        json.dump(data, f)

def update_data(data, prev_move, curr_move):
    if prev_move:
        data[prev_move][curr_move] += 1
        save_data(data)
