from battleship_config import BOARD_SIZE

class ShipManager:
    """Manages the game board state and ship placements"""
    def __init__(self, opponent):
        """
        Initializes the ShipManager with an empty grid and ship tracking.
        
        Args:
            opponent (str): The name of the opponent.
        """
        self.grid = [[" "] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.ship_locations = {}  # Dictionary to track ship positions
        self.opponent = opponent

    def deploy_ship(self, ship, length, row, column, orientation):
        """
        Places a ship on the board and records its location.
        
        Args:
            ship (str): The name of the ship.
            length (int): The length of the ship.
            row (int): The starting row for the ship.
            column (int): The starting column for the ship.
            orientation (str): The orientation of the ship ('H' for horizontal, 'V' for vertical).
        """
        if orientation == "H":  # Horizontal placement
            for i in range(column, column + length):
                self.grid[row][i] = "X"
                self.ship_locations.setdefault(ship, []).append((row, i))
        else:  # Vertical placement
            for i in range(row, row + length):
                self.grid[i][column] = "X"
                self.ship_locations.setdefault(ship, []).append((i, column))

    def check_sunk_ship(self, row, column):
        """
        Checks if a ship has been sunk and updates the ship locations.
        
        Args:
            row (int): The row of the attack.
            column (int): The column of the attack.
        """
        for ship, positions in self.ship_locations.items():
            if (row, column) in positions:
                positions.remove((row, column))
                if not positions:
                    print("\n*******************************************")
                    print(f"\033[1m        {self.opponent} has sunk the {ship}!\033[0m")
                    print("*******************************************\n")
                    del self.ship_locations[ship]
                    break
    
    def check_sunk_ship_gui(self, row, column):
        """
        Checks if a ship has been sunk and updates the ship locations.
        Returns the name of the ship if it was sunk.
        In GUI mode, doesn't print to console.
        
        Args:
            row (int): The row of the attack.
            column (int): The column of the attack.
            
        Returns:
            str: The name of the ship that was sunk, or None if no ship was sunk.
        """
        for ship, positions in self.ship_locations.items():
            if (row, column) in positions:
                positions.remove((row, column))
                if not positions:
                    sunk_ship = ship
                    # Don't print to console in GUI mode
                    del self.ship_locations[ship]
                    return sunk_ship
        return None

    def all_ships_sunk(self):
        """
        Checks if all ships have been sunk.
        
        Returns:
            bool: True if all ships are sunk, False otherwise.
        """
        return all(not positions for positions in self.ship_locations.values()) 