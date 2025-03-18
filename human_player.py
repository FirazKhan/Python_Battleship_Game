from base_player import BasePlayer
from battleship_config import LETTERS_TO_NUMS, BOARD_SIZE

class HumanPlayer(BasePlayer):
    """Represents a human player"""
    def __init__(self):
        """Initializes the HumanPlayer with the name 'Player'"""
        super().__init__("Player")
        self.gui_mode = False  # Flag to determine whether to print to console

    def set_gui_mode(self, is_gui=True):
        """
        Sets the GUI mode flag to determine whether to print to console.
        
        Args:
            is_gui (bool): If True, player will not print to console.
        """
        self.gui_mode = is_gui

    def take_turn(self, opponent):
        """
        Handles the human player's turn.
        
        Args:
            opponent (BasePlayer): The opponent player.
        """
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
            
        if self.attack_board.grid[row][column] in ["-", "X"]:
            print("\nYou already attacked this position. Try again.\n")
            return self.take_turn(opponent)
        elif opponent.ship_manager.grid[row][column] == "X":
            self.attack_board.grid[row][column] = "X"
            
            # Only print to console if not in GUI mode
            if not self.gui_mode:
                print("\nHit!\n")
                print('\033[1m       Player`s Guess Board\033[0m')
                self.display.display_board(self.attack_board.grid)
                
            opponent.ship_manager.check_sunk_ship(row, column)
        else:
            self.attack_board.grid[row][column] = "-"
            
            # Only print to console if not in GUI mode
            if not self.gui_mode:
                print("\nMiss!\n")
                print('\033[1m       Player`s Guess Board\033[0m')
                self.display.display_board(self.attack_board.grid) 