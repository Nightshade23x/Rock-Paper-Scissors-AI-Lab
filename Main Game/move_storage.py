"""
These are functions for loading and safely updating the transition data for moves which is used by the AI models.
"""
import json

def load_data(file_path):
    """
    Load move data from the JSON file.
    If the file does not exist,an empty dictionary is returned to ensure safe execution regardless.
    file_path is the path to the JSON file storing the transition data.
    
    Returns:
        dict: The transition data loaded from the JSON file or an empty dict if the file
              does not exist or is invalid
    """
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def update_data(data, prev_move, curr_move, file_path):
    """
    Update the transition count safely
    data is the existing transition data.
    prev_move is the previous move sequence used as a key.
    curr_move is the current player move to record.
    file_path is the path to the JSON file storing transitions.
    
    Returns:
        dict: The updated transition data after incrementing the transition count
    """
    # If the previous move sequence doesn't exist, create it
    if prev_move not in data:
        data[prev_move] = {'r': 0, 'p': 0, 's': 0}
    # If the current move key doesn't exist,very unlikely but kept as a safety measure
    if curr_move not in data[prev_move]:
        data[prev_move][curr_move] = 0
    # Update the transition count
    data[prev_move][curr_move] += 1
    # Save back to the file
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
    return data
