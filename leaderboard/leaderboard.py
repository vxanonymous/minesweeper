import json
import os
from tkinter import simpledialog

LEADERBOARD_FILE = os.path.join(os.path.dirname(__file__), "leaderboard_data.json")

# This is the absolute minimal structure if the file is missing or totally corrupt.
# The game will populate it as scores are added.
MINIMAL_EMPTY_LEADERBOARD_STRUCTURE = {
  "classic": {
    "Beginner": [],
    "Intermediate": [],
    "Expert": [],
    "Random": []
  },
  "hexagon": {
    "Beginner": [],
    "Intermediate": [],
    "Expert": [],
    "Random": []
  },
  "custom_mode": {
    "records": []
  }
}

def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, "r") as f:
                # Handle empty file case
                content = f.read()
                if not content.strip():
                    print(f"Warning: Leaderboard file '{LEADERBOARD_FILE}' is empty. Initializing with empty structure.")
                    return json.loads(json.dumps(MINIMAL_EMPTY_LEADERBOARD_STRUCTURE)) # Return a deep copy
                
                data = json.loads(content) # Use loads on content read

                # Basic validation: ensure top-level keys and their expected types (dict/list) exist.
                # If not, it's safer to start fresh or with a minimal structure.
                valid_structure = True
                for mode_key, mode_template in MINIMAL_EMPTY_LEADERBOARD_STRUCTURE.items():
                    if mode_key not in data or not isinstance(data[mode_key], type(mode_template)):
                        valid_structure = False
                        break
                    if isinstance(mode_template, dict): # For classic/hexagon
                        for diff_key, diff_template in mode_template.items():
                            if diff_key not in data[mode_key] or not isinstance(data[mode_key][diff_key], type(diff_template)):
                                valid_structure = False
                                break
                    if not valid_structure:
                        break
                
                if not valid_structure:
                    print(f"Warning: Leaderboard file '{LEADERBOARD_FILE}' has an unexpected structure. Initializing with empty structure.")
                    return json.loads(json.dumps(MINIMAL_EMPTY_LEADERBOARD_STRUCTURE))
                
                return data
        except (json.JSONDecodeError, TypeError) as e: # Catch TypeError for unexpected data types
            print(f"Warning: Leaderboard file '{LEADERBOARD_FILE}' is corrupted or malformed ({e}). Initializing with empty structure.")
            # Fall through to return a copy of the minimal empty data
            
    # If file doesn't exist or any error above, return a deep copy of the minimal empty structure
    return json.loads(json.dumps(MINIMAL_EMPTY_LEADERBOARD_STRUCTURE))


def save_leaderboard(data):
    try:
        # Ensure the 'leaderboard' directory exists
        leaderboard_dir = os.path.dirname(LEADERBOARD_FILE)
        if not os.path.exists(leaderboard_dir) and leaderboard_dir: # Check if leaderboard_dir is not empty string
            os.makedirs(leaderboard_dir)
            
        with open(LEADERBOARD_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error saving leaderboard: {e}")

def _get_player_name(title="New High Score!"):
    name = simpledialog.askstring(title, "You made the leaderboard! Enter your name:")
    if name is None:
        return None 
    name = name.strip()
    return name if name else "Player"

def update_leaderboard(mode, difficulty, time_value, width=None, height=None, mines=None):
    data = load_leaderboard()
    
    # Ensure the path to the records list exists, creating if necessary
    # This uses the minimal structure as a reference for keys if they are missing entirely
    current_mode_data = data.setdefault(mode, MINIMAL_EMPTY_LEADERBOARD_STRUCTURE[mode])
    records = current_mode_data.setdefault(difficulty, MINIMAL_EMPTY_LEADERBOARD_STRUCTURE[mode][difficulty])


    new_entry_data = {"time": time_value}
    is_random_proportional = difficulty == "Random" and all(v is not None for v in [width, height, mines])

    current_config = "N/A"
    if is_random_proportional:
        total_tiles = width * height
        new_entry_data["proportion"] = mines / total_tiles if total_tiles > 0 else 0
        current_config = f"{width}x{height}, {mines}m"
        sort_key = lambda e: (-e.get("proportion", 0), e.get("time", float('inf')))
        if len(records) >= 10:
            temp_records = sorted(list(records), key=sort_key) # Sort a copy
            last_prop = temp_records[-1].get("proportion", 0)
            last_time = temp_records[-1].get("time", float('inf'))
            if new_entry_data["proportion"] < last_prop or \
               (new_entry_data["proportion"] == last_prop and new_entry_data["time"] >= last_time):
                return 
    else:
        sort_key = lambda e: e.get("time", float('inf'))
        if len(records) >= 10:
            temp_records = sorted(list(records), key=sort_key) # Sort a copy
            if time_value >= temp_records[-1].get("time", float('inf')):
                return

    name = _get_player_name()
    if name is None:
        return 

    new_entry = {"name": name, **new_entry_data}
    if is_random_proportional or difficulty == "Random": 
        new_entry["config"] = current_config

    records.append(new_entry)
    records.sort(key=sort_key)
    data[mode][difficulty] = records[:10] # Assign back to the original data structure
    save_leaderboard(data)

def update_custom_leaderboard(width, height, mines, time_value):
    data = load_leaderboard()
    
    # Ensure the path to custom_mode records exists
    custom_mode_data = data.setdefault("custom_mode", MINIMAL_EMPTY_LEADERBOARD_STRUCTURE["custom_mode"])
    records = custom_mode_data.setdefault("records", MINIMAL_EMPTY_LEADERBOARD_STRUCTURE["custom_mode"]["records"])


    total_tiles = width * height
    mine_percentage = mines / total_tiles if total_tiles > 0 else 0
    
    current_config = f"{width}x{height}, {mines}m ({mine_percentage*100:.1f}%)"
    sort_key = lambda e: (-e.get("mine_percentage",0), e.get("time", float('inf')))

    if len(records) >= 10:
        temp_records = sorted(list(records), key=sort_key) # Sort a copy
        last_perc = temp_records[-1].get("mine_percentage",0)
        last_time = temp_records[-1].get("time", float('inf'))
        if mine_percentage < last_perc or \
           (mine_percentage == last_perc and time_value >= last_time):
            return

    name = _get_player_name("Custom Mode Leaderboard")
    if name is None:
        return

    new_entry = {
        "name": name, "mine_percentage": mine_percentage, "time": time_value,
        "config": current_config
    }
    records.append(new_entry)
    records.sort(key=sort_key)
    data["custom_mode"]["records"] = records[:10] # Assign back
    save_leaderboard(data)