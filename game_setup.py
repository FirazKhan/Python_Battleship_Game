import random
from human_player import HumanPlayer
from computer_player import ComputerPlayer
from battleship_config import BOARD_SIZE, SHIP_TYPES, LETTERS_TO_NUMS

class GameSetup:
    """Handles game initialization and ship placement"""
    def __init__(self):
        """Initializes the GameSetup with human and computer players"""
        self.players = [HumanPlayer(), ComputerPlayer()]

    def deploy_all_ships(self, player):
        """
        Manages the ship deployment phase for each player.
        
        Args:
            player (BasePlayer): The player for whom to deploy ships.
        """
        if player.name == "Player":
            print("\n\033[1m       Place Your Ships\033[0m")
            print("----------------------------------------\n")

        for ship, length in SHIP_TYPES.items():
            if player.name == "Player":
                print(f"Place the {ship} (length: {length})")
                print("----------------------------------------")
            
            while True:
                if player.name == "Computer":
                    orientation = random.choice(["H", "V"])
                    row = random.randint(0, BOARD_SIZE - 1)
                    column = random.randint(0, BOARD_SIZE - 1)
                else:
                    row, column, orientation = self.get_user_input(True, length, player)
                if player.validator.validate_placement(length, row, column, orientation):
                    if not player.validator.check_overlap(player.ship_manager.grid, row, column, orientation, length):
                        player.ship_manager.deploy_ship(ship, length, row, column, orientation)
                        if player.name != "Computer":
                            player.display.display_board(player.ship_manager.grid)
                            print("----------------------------------------\n")
                        break
        if player.name == "Computer":
            print('===============================================')

    def get_user_input(self, place_ship, ship_length=None, player=None):
        """
        Gets user input for ship placement or attack position.
        
        Args:
            place_ship (bool): Whether the input is for placing a ship.
            ship_length (int, optional): The length of the ship to place.
            player (BasePlayer, optional): The player placing the ship.
        
        Returns:
            tuple: The row, column, and orientation (if placing a ship).
        """
        if place_ship:
            while True:
                try:
                    orientation = input("Enter orientation Horizontal - H or Vertical - V: ").upper()
                    if orientation not in ["H", "V"]:
                        raise ValueError("Invalid orientation. Please enter 'H' for Horizontal or 'V' for Vertical.\n")
                    break
                except ValueError as e:
                    print(e)
            while True:
                try:
                    position = input("Enter the position (e.g., A2): ").upper()
                    if len(position) < 2 or position[0] not in 'ABCDEFGH' or not position[1:].isdigit():
                        raise ValueError("Invalid position. Please enter a valid position (e.g., A2).\n")
                    column = LETTERS_TO_NUMS[position[0]]
                    row = int(position[1:]) - 1
                    if row < 0 or row >= BOARD_SIZE or column < 0 or column >= BOARD_SIZE:
                        raise ValueError("Position out of bounds. Please enter a valid position within the grid.\n")
                    if ship_length and not player.validator.validate_placement(ship_length, row, column, orientation):
                        raise ValueError("The ship cannot be placed at this position due to size constraints.\n")
                    if player and player.validator.check_overlap(player.ship_manager.grid, row, column, orientation, ship_length):
                        raise ValueError("A ship is already placed at this position. Please enter another location.\n")
                    break
                except ValueError as e:
                    print(e)
            return row, column, orientation
        else:
            while True:
                try:
                    position = input("Enter the position (e.g., A2): ").upper()
                    if len(position) < 2 or position[0] not in 'ABCDEFGH' or not position[1:].isdigit():
                        raise ValueError("Invalid position. Please enter a valid position (e.g., A2).\n")
                    column = LETTERS_TO_NUMS[position[0]]
                    row = int(position[1:]) - 1
                    if row < 0 or row >= BOARD_SIZE or column < 0 or column >= BOARD_SIZE:
                        raise ValueError("Position out of bounds. Please enter a valid position within the grid.\n")
                    break
                except ValueError as e:
                    print(e)
            return row, column 