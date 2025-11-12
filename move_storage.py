import json

def load_data(file_path):
    """Load move data from the JSON file."""
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def update_data(data, prev_move, curr_move):
    """Update the transition count safely, creating keys if they don’t exist."""
    # If the previous move sequence doesn't exist, create it
    if prev_move not in data:
        data[prev_move] = {'r': 0, 'p': 0, 's': 0}
    # If the current move key doesn't exist (shouldn’t happen, but safe)
    if curr_move not in data[prev_move]:
        data[prev_move][curr_move] = 0
    # Update the transition count
    data[prev_move][curr_move] += 1

    # Save back to the file
    with open("moves.json", "w") as file:
        json.dump(data, file, indent=4)
