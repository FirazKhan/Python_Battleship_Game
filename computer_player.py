import numpy as np
import random
from base_player import BasePlayer
from battleship_config import BOARD_SIZE, SHIP_TYPES

class ComputerPlayer(BasePlayer):
    """AI player with intelligent targeting system"""
    def __init__(self):
        super().__init__("Computer")
        # Initialize AI targeting attributes
        self.last_hit = None  # Stores last successful hit
        self.hit_stack = []  # Queue of potential target positions
        self.direction = None  # Current targeting direction (H or V)
        self.probability_map = np.zeros((BOARD_SIZE, BOARD_SIZE))  # Heat map for targeting
        self.last_move_sunk = None  # Stores the name of the ship sunk in the last move (for GUI)
        self.last_move_hit = False  # Tracks if the last move was a hit (for GUI)
        self.gui_mode = False  # Flag to determine whether to print to console

    def set_gui_mode(self, is_gui=True):
        """
        Sets the GUI mode flag to determine whether to print to console.
        
        Args:
            is_gui (bool): If True, computer will not print to console.
        """
        self.gui_mode = is_gui

    def take_turn(self, opponent):
        """
        Handles the computer player's turn.
        
        Args:
            opponent (BasePlayer): The opponent player.
        """
        if not hasattr(self, 'probability_map'):
            self.probability_map = np.zeros((BOARD_SIZE, BOARD_SIZE))

        # Reset tracking variables for this turn
        self.last_move_sunk = None
        self.last_move_hit = False

        row = None
        column = None

        # First Priority - Check hit stack for potential targets
        if self.hit_stack:
            row, column = self.hit_stack.pop(0)
        # Second Priority - Use last hit information
        elif self.last_hit:
            row, column = self.last_hit
            if self.direction:
                # If we know the ship's direction, try moves along that line
                if self.direction == "H":
                    possible_moves = [(row, column-1), (row, column+1)]
                else:
                    possible_moves = [(row-1, column), (row+1, column)]
                
                # Filter out invalid or already tried moves
                possible_moves = [(r, c) for r, c in possible_moves 
                                if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE 
                                and self.attack_board.grid[r][c] not in ["-", "X"]]
                
                if possible_moves:
                    row, column = random.choice(possible_moves)
                else:
                    # Reset targeting if no valid moves in current direction
                    self.last_hit = None
                    self.direction = None
                    self.hit_stack = []
                    self.update_probability_map(opponent)
                    row, column = np.unravel_index(np.argmax(self.probability_map), self.probability_map.shape)
            else:
                # Try all adjacent positions if direction unknown
                possible_moves = [(row-1, column), (row+1, column), (row, column-1), (row, column+1)]
                possible_moves = [(r, c) for r, c in possible_moves 
                                if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE 
                                and self.attack_board.grid[r][c] not in ["-", "X"]]
                if possible_moves:
                    row, column = random.choice(possible_moves)
                else:
                    # Reset targeting if no valid adjacent moves
                    self.last_hit = None
                    self.direction = None
                    self.hit_stack = []
                    self.update_probability_map(opponent)
                    row, column = np.unravel_index(np.argmax(self.probability_map), self.probability_map.shape)
        # Third Priority - Use probability map for targeting
        else:
            self.update_probability_map(opponent)
            row, column = np.unravel_index(np.argmax(self.probability_map), self.probability_map.shape)

        # Process the attack result
        if opponent.ship_manager.grid[row][column] == "X":
            # Handle successful hit
            self.attack_board.grid[row][column] = "X"
            self.last_move_hit = True
            
            # Only print to console if not in GUI mode
            if not self.gui_mode:
                print("\nComputer hit!\n")
                print('\033[1m       Computer`s Guess Board\033[0m')
                self.display.display_board(self.attack_board.grid)
            
            if self.last_hit:
                # Determine ship orientation based on multiple hits
                if row == self.last_hit[0]:
                    self.direction = "H"
                elif column == self.last_hit[1]:
                    self.direction = "V"
                
                # Add next potential moves based on ship direction
                if self.direction == "H":
                    next_moves = [(row, min(column, self.last_hit[1])-1), 
                                (row, max(column, self.last_hit[1])+1)]
                else:  # Vertical
                    next_moves = [(min(row, self.last_hit[0])-1, column), 
                                (max(row, self.last_hit[0])+1, column)]
                
                # Filter valid moves and add to hit stack
                valid_moves = [(r, c) for r, c in next_moves 
                              if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE 
                              and self.attack_board.grid[r][c] not in ["-", "X"]]
                self.hit_stack.extend(valid_moves)
            
            self.last_hit = (row, column)
            
            # Check if a ship was sunk and store the name for GUI display
            sunk_ship = opponent.ship_manager.check_sunk_ship_gui(row, column)
            if sunk_ship:
                self.last_move_sunk = sunk_ship
                # Only print to console if not in GUI mode
                if not self.gui_mode:
                    print("\n*******************************************")
                    print(f"\033[1m        Computer has sunk the {sunk_ship}!\033[0m")
                    print("*******************************************\n")
        else:
            # Handle miss
            self.attack_board.grid[row][column] = "-"
            # Only print to console if not in GUI mode
            if not self.gui_mode:
                print("\nComputer miss!\n")
                print('\033[1m       Computer`s Guess Board\033[0m')
                self.display.display_board(self.attack_board.grid)

    def update_probability_map(self, opponent):
        """
        Updates probability map for intelligent targeting.
        
        Args:
            opponent (BasePlayer): The opponent player.
        """
        # Reset the probability map
        self.probability_map = np.zeros((BOARD_SIZE, BOARD_SIZE))
        
        # First mark all attacked positions with zero probability
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                # Explicitly set already attacked positions to 0
                if self.attack_board.grid[row][col] in ["-", "X"]:
                    self.probability_map[row][col] = 0
                    continue
        
        # Calculate additional probabilities for possible ship placements
        for ship, length in SHIP_TYPES.items():
            for row in range(BOARD_SIZE):
                for col in range(BOARD_SIZE):
                    # Check horizontal placement possibility
                    if self.can_place_ship(opponent, row, col, length, "H"):
                        for i in range(length):
                            # Only increment if position hasn't been attacked
                            if self.attack_board.grid[row][col + i] not in ["-", "X"]:
                                self.probability_map[row][col + i] += 1
                    # Check vertical placement possibility
                    if self.can_place_ship(opponent, row, col, length, "V"):
                        for i in range(length):
                            # Only increment if position hasn't been attacked
                            if self.attack_board.grid[row + i][col] not in ["-", "X"]:
                                self.probability_map[row + i][col] += 1
        
        # Ensure no negative probabilities and zero out already hit positions
        self.probability_map = np.maximum(self.probability_map, 0)
        
        # If all positions are zero, reset to uniform distribution
        if np.all(self.probability_map == 0):
            self.probability_map = np.ones((BOARD_SIZE, BOARD_SIZE))
            for row in range(BOARD_SIZE):
                for col in range(BOARD_SIZE):
                    if self.attack_board.grid[row][col] in ["-", "X"]:
                        self.probability_map[row][col] = 0

    def get_move(self, opponent):
        """
        Determines the next move for the computer player.
        
        Args:
            opponent (BasePlayer): The opponent player.
        
        Returns:
            tuple: The row and column of the next move.
        """
        if self.last_hit:
            row, col = self.last_hit
            random.shuffle(self.hit_directions)
            
            for dr, dc in self.hit_directions:
                new_row = row + dr
                new_col = col + dc
                
                if (0 <= new_row < BOARD_SIZE and 
                    0 <= new_col < BOARD_SIZE and 
                    opponent.ship_manager.grid[new_row][new_col] not in ["-", "H"]):
                    return new_row, new_col
            
            self.last_hit = None

        while True:
            row = random.randint(0, BOARD_SIZE - 1)
            col = random.randint(0, BOARD_SIZE - 1)
            
            if opponent.ship_manager.grid[row][col] not in ["-", "H"]:
                if opponent.ship_manager.grid[row][col] == "X":
                    self.last_hit = (row, col)
                return row, col 