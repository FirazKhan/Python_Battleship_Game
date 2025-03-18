from battleship_config import BOARD_SIZE

class BoardValidator:
    """Validates ship placements and board positions"""
    def __init__(self):
        """Initializes the BoardValidator with the board size"""
        self.size = BOARD_SIZE

    def validate_placement(self, length, row, column, orientation):
        """
        Checks if a ship placement is within board boundaries.
        
        Args:
            length (int): The length of the ship.
            row (int): The starting row for the ship.
            column (int): The starting column for the ship.
            orientation (str): The orientation of the ship ('H' for horizontal, 'V' for vertical).
        
        Returns:
            bool: True if the placement is valid, False otherwise.
        """
        if orientation == "H":
            return column + length <= self.size
        else:
            return row + length <= self.size

    def check_overlap(self, grid, row, column, orientation, length):
        """
        Checks if a ship placement overlaps with existing ships.
        
        Args:
            grid (list): The game board grid.
            row (int): The starting row for the ship.
            column (int): The starting column for the ship.
            orientation (str): The orientation of the ship ('H' for horizontal, 'V' for vertical).
            length (int): The length of the ship.
        
        Returns:
            bool: True if there is an overlap, False otherwise.
        """
        try:
            if orientation == "H":
                return any(grid[row][i] == "X" for i in range(column, column + length))
            else:
                return any(grid[i][column] == "X" for i in range(row, row + length))
        except IndexError:
            return True
        return False 