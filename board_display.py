class BoardDisplay:
    """Handles the visual representation of the game board with colored output"""
    def __init__(self):
        # Define color codes for different board elements
        self.COLORS = {
            'X': '\033[91m',  # Red for ships/hits
            '-': '\033[94m',  # Blue for misses
            'RESET': '\033[0m'  # Reset color formatting
        }

    def display_board(self, grid):
        """
        Displays the game board with colored output.
        
        Args:
            grid (list): The game board grid to display.
        """
        print("  A B C D E F G H")
        print("  +-+-+-+-+-+-+-+")
        row_num = 1
        for row in grid:
            formatted_row = []
            for cell in row:
                if cell in self.COLORS:
                    formatted_row.append(f"{self.COLORS[cell]}{cell}{self.COLORS['RESET']}")
                else:
                    formatted_row.append(cell)
            print("%d|%s|" % (row_num, "|".join(formatted_row)))
            row_num += 1 