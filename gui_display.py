import tkinter as tk
from tkinter import ttk
from battleship_config import BOARD_SIZE

class GameDisplay:
    """Handles all game UI elements"""
    def __init__(self, parent):
        """
        Initializes the game display.

        Args:
            parent (tk.Tk or tk.Toplevel): The parent window.
        """
        # Setup phase frame
        self.setup_frame = ttk.Frame(parent, padding="10")
        self.setup_frame.grid(row=0, column=0)
        
        # Create placement board
        self.create_placement_board()
        self.create_setup_controls()
        
        # Game phase frame
        self.game_frame = ttk.Frame(parent, padding="10")
        self.game_frame.grid(row=0, column=0)
        self.create_game_boards()
        self.game_frame.grid_remove()

    def create_placement_board(self):
        """Creates the ship placement board"""
        placement_frame = ttk.LabelFrame(self.setup_frame, text="Place Your Ships")
        placement_frame.grid(row=0, column=0, padx=5, pady=5)
        
        # Add column headers (A-H)
        for j in range(BOARD_SIZE):
            col_label = ttk.Label(placement_frame, text=chr(65 + j), width=3)
            col_label.grid(row=0, column=j+1, padx=1, pady=1)
        
        # Add row headers (1-8)
        for i in range(BOARD_SIZE):
            row_label = ttk.Label(placement_frame, text=str(i+1))
            row_label.grid(row=i+1, column=0, padx=1, pady=1)
        
        # Create placement buttons
        self.placement_buttons = [[
            ttk.Button(placement_frame, width=3)
            for _ in range(BOARD_SIZE)
        ] for _ in range(BOARD_SIZE)]
        
        # Position all buttons in the grid
        for i, row in enumerate(self.placement_buttons):
            for j, btn in enumerate(row):
                btn.grid(row=i+1, column=j+1, padx=1, pady=1)

    def create_setup_controls(self):
        """Creates the controls for the setup phase"""
        self.orientation = tk.StringVar(value="H")
        controls = ttk.Frame(self.setup_frame, padding="10")
        controls.grid(row=1, column=0)
        
        ttk.Radiobutton(controls, text="Horizontal", variable=self.orientation, 
                       value="H").grid(row=0, column=0, sticky='w')
        ttk.Radiobutton(controls, text="Vertical", variable=self.orientation, 
                       value="V").grid(row=1, column=0, sticky='w')
        
        self.message_label = ttk.Label(controls, text="Place your ships")
        self.message_label.grid(row=2, column=0)
        
        self.start_button = ttk.Button(controls, text="Start Game", state='disabled')
        self.start_button.grid(row=3, column=0)

    def create_game_boards(self):
        """Creates the game boards for both the player and the computer."""

        # Player's board
        player_frame = ttk.LabelFrame(self.game_frame, text="Your Guesses")
        player_frame.grid(row=0, column=0, padx=5)
        
        # Add column headers (A-H)
        for j in range(BOARD_SIZE):
            col_label = ttk.Label(player_frame, text=chr(65 + j), width=3)
            col_label.grid(row=0, column=j+1, padx=1, pady=1)
        
        # Add row headers (1-8)
        for i in range(BOARD_SIZE):
            row_label = ttk.Label(player_frame, text=str(i+1))
            row_label.grid(row=i+1, column=0, padx=1, pady=1)
        
        # Create the player buttons
        self.player_buttons = [[
            ttk.Button(player_frame, width=3)
            for _ in range(BOARD_SIZE)
        ] for _ in range(BOARD_SIZE)]
        
        # Computer's board
        computer_frame = ttk.LabelFrame(self.game_frame, text="Computer's Guesses")
        computer_frame.grid(row=0, column=1, padx=5)
        
        # Add column headers (A-H)
        for j in range(BOARD_SIZE):
            col_label = ttk.Label(computer_frame, text=chr(65 + j), width=3)
            col_label.grid(row=0, column=j+1, padx=1, pady=1)
        
        # Add row headers (1-8)
        for i in range(BOARD_SIZE):
            row_label = ttk.Label(computer_frame, text=str(i+1))
            row_label.grid(row=i+1, column=0, padx=1, pady=1)
        
        # Create the computer buttons
        self.computer_buttons = [[
            ttk.Button(computer_frame, width=3)
            for _ in range(BOARD_SIZE)
        ] for _ in range(BOARD_SIZE)]
        
        # Position all buttons in the grid
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                self.player_buttons[i][j].grid(row=i+1, column=j+1, padx=1, pady=1)
                self.computer_buttons[i][j].grid(row=i+1, column=j+1, padx=1, pady=1)
        
        # Create a message frame with border
        message_frame = ttk.Frame(self.game_frame, padding=10, relief="groove", borderwidth=2)
        message_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")
        
        # Make the message frame a specific height
        message_frame.grid_propagate(False)
        message_frame.config(height=50)  # Fixed height for message area
        
        # Create the message label with larger initial font
        self.game_message = ttk.Label(
            message_frame, 
            text="", 
            anchor="center", 
            justify="center",
            font=('Arial', 11)
        )
        self.game_message.pack(fill="both", expand=True) 