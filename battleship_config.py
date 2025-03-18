import json
import os

# Load configuration from JSON file
def load_config():
    # Get the directory where the current script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, 'config.json')
    
    with open(config_path, 'r') as f:
        return json.load(f)

# Initialize configuration
config = load_config()

# Export configuration values
SHIP_TYPES = config['ships']
LETTERS_TO_NUMS = config['grid_letters']
BOARD_SIZE = config['board_size'] 