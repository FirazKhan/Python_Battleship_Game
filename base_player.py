from battleship_config import BOARD_SIZE
from board_display import BoardDisplay
from ship_manager import ShipManager
from board_validator import BoardValidator

class BasePlayer:
    """Base class for player functionality"""
    def __init__(self, name):
        """
        Initializes the BasePlayer with player components and attributes.
        
        Args:
            name (str): The name of the player.
        """
        self.name = name
        self.opponent_name = "Computer" if name == "Player" else "Player"
        self.ship_manager = ShipManager(self.opponent_name)  # Manages player's ships
        self.attack_board = ShipManager(self.opponent_name)  # Tracks attacks made
        self.display = BoardDisplay()  # Handles board display
        self.validator = BoardValidator()  # Validates moves
        self.hit_directions = [(0,1), (0,-1), (1,0), (-1,0)]  # Possible attack directions

    def can_place_ship(self, opponent, row, col, length, orientation):
        """
        Checks if a ship can be placed at the specified location.
        
        Args:
            opponent (BasePlayer): The opponent player.
            row (int): The starting row for the ship.
            col (int): The starting column for the ship.
            length (int): The length of the ship.
            orientation (str): The orientation of the ship ('H' for horizontal, 'V' for vertical).
        
        Returns:
            bool: True if the ship can be placed, False otherwise.
        """
        if orientation == "H":
            if col + length > BOARD_SIZE:
                return False
            for i in range(length):
                if self.attack_board.grid[row][col + i] in ["-", "X"]:
                    return False
        else:
            if row + length > BOARD_SIZE:
                return False
            for i in range(length):
                if self.attack_board.grid[row + i][col] in ["-", "X"]:
                    return False
        return True 