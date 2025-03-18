import tkinter as tk
from tkinter import ttk
from game_setup import GameSetup
from battleship_config import SHIP_TYPES, BOARD_SIZE
from window_manager import WindowManager
from gui_display import GameDisplay

class BattleshipGUI:
    """Main game coordinator for GUI version"""
    def __init__(self, root):
        """
        Initializes the Battleship GUI.

        Args:
            root (tk.Tk): The root window.
        """
        self.root = root
        self.root.title("Battleship")
        
        WindowManager.center_window(self.root)
        WindowManager.create_styles()
        
        self.setup_new_game()

    def setup_new_game(self):
        """Sets up a new game."""
        self.setup = GameSetup()
        self.players = self.setup.players
        
        # Set GUI mode for both players
        for player in self.players:
            if hasattr(player, 'set_gui_mode'):
                player.set_gui_mode(True)
            
        self.display = GameDisplay(self.root)
        
        # Set up placement phase
        self.current_ship_index = 0
        self.ships_to_place = list(SHIP_TYPES.items())
        
        # Bind events
        self.bind_placement_buttons()
        self.bind_game_buttons()
        self.display.start_button.configure(command=self.start_game)

    def bind_placement_buttons(self):
        """Binds the placement buttons to their respective commands."""
        
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                self.display.placement_buttons[i][j].configure(
                    command=lambda x=i, y=j: self.try_place_ship(x, y))

    def bind_game_buttons(self):
        """Binds the game buttons to their respective commands"""
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                self.display.player_buttons[i][j].configure(
                    command=lambda x=i, y=j: self.make_move(x, y))

    def try_place_ship(self, row, col):
        """
        Attempts to place a ship on the board.

        Args:
            row (int): The row index where the ship should be placed.
            col (int): The column index where the ship should be placed.
        """
        if self.current_ship_index >= len(self.ships_to_place):
            return
            
        ship, length = self.ships_to_place[self.current_ship_index]
        orientation = self.display.orientation.get()
        
        # Use player's validation methods
        player = self.players[0]
        if player.validator.validate_placement(length, row, col, orientation):
            if not player.validator.check_overlap(player.ship_manager.grid, row, col, orientation, length):
                player.ship_manager.deploy_ship(ship, length, row, col, orientation)
                self.update_placement_board()
                self.advance_ship_placement()

    def advance_ship_placement(self):
        """Advances to the next ship placement"""
        self.current_ship_index += 1
        if self.current_ship_index >= len(self.ships_to_place):
            self.display.message_label.config(text="All ships placed! Click Start Game")
            self.display.start_button.config(state='normal')
        else:
            ship, length = self.ships_to_place[self.current_ship_index]
            self.display.message_label.config(text=f"Place your {ship} (length: {length})")

    def update_placement_board(self):
        """Updates the placement board to reflect the current state"""
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.players[0].ship_manager.grid[i][j] == "X":
                    self.display.placement_buttons[i][j].config(style='Ship.TButton')

    def make_move(self, row, col):
        """
        Makes a move in the game.

        Args:
            row (int): The row index of the move.
            col (int): The column index of the move.
        """
        human = self.players[0]
        computer = self.players[1]

        # Player's turn
        if human.attack_board.grid[row][col] in ["-", "X"]:
            self.display.game_message.config(text="Already attacked this position!")
            return

        hit = computer.ship_manager.grid[row][col] == "X"
        human.attack_board.grid[row][col] = "X" if hit else "-"
        self.display.player_buttons[row][col].config(
            style='Hit.TButton' if hit else 'Miss.TButton')

        # Handle player's move result
        if hit:
            # Check if ship was sunk
            sunk_ship = computer.ship_manager.check_sunk_ship_gui(row, col)
            if sunk_ship:
                # Display sunk ship message with emphasis
                message = f"Player has sunk the {sunk_ship}!"
                self.display.game_message.config(
                    text=message, 
                    style='Sunk.TLabel'
                )
                
                # Check for win condition
                if computer.ship_manager.all_ships_sunk():
                    self.show_game_over("Player")
                    return
                
                # Add a delay when a ship is sunk (3 seconds)
                self.root.after(3000, lambda: self.process_computer_turn(human, computer))
            else:
                # Regular hit message
                self.display.game_message.config(
                    text="Hit!", 
                    font=('Arial', 10),
                    foreground='black'
                )
                # Normal delay for hit (500ms)
                self.root.after(500, lambda: self.process_computer_turn(human, computer))
        else:
            # Miss message
            self.display.game_message.config(
                text="Miss!", 
                font=('Arial', 10),
                foreground='black'
            )
            # Normal delay for miss (500ms)
            self.root.after(500, lambda: self.process_computer_turn(human, computer))
    
    def process_computer_turn(self, human, computer):
        """
        Process the computer's turn after the player has moved.
        
        Args:
            human (HumanPlayer): The human player.
            computer (ComputerPlayer): The computer player.
        """
        # Computer makes its move
        computer.take_turn(human)
        self.update_computer_board()
        
        # Get and display appropriate message for computer's move
        computer_message = self.get_computer_message()
        if computer_message:
            if "sunk" in computer_message:
                # Computer sunk a ship - display with emphasis
                self.display.game_message.config(
                    text=computer_message, 
                    style='ComputerSunk.TLabel'
                )
                # Pause for a moment when computer sinks a ship too
                if not human.ship_manager.all_ships_sunk():
                    # Only pause if game isn't over
                    self.root.update()  # Force update the UI
                    self.root.after(3000, lambda: None)  # Wait for 3 seconds
            else:
                # Regular hit/miss message
                self.display.game_message.config(
                    text=computer_message, 
                    font=('Arial', 10),
                    foreground='black'
                )
        
        # Check if computer won
        if human.ship_manager.all_ships_sunk():
            self.show_game_over("Computer")

    def get_computer_message(self):
        """
        Gets any messages from the computer's last move.
        
        Returns:
            str: A message about the computer's last move, or None if no message.
        """
        computer = self.players[1]
        if hasattr(computer, 'last_move_sunk'):
            if computer.last_move_sunk:
                ship_name = computer.last_move_sunk
                computer.last_move_sunk = None  # Reset for next turn
                return f"Computer has sunk the {ship_name}!"
            elif hasattr(computer, 'last_move_hit') and computer.last_move_hit:
                computer.last_move_hit = False  # Reset for next turn
                return "Computer hit!"
            else:
                return "Computer miss!"
        return None

    def update_computer_board(self):
        """Updates the computer's board to reflect the current state"""
        computer = self.players[1]
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if computer.attack_board.grid[i][j] in ["-", "X"]:
                    self.display.computer_buttons[i][j].config(
                        style='Hit.TButton' if computer.attack_board.grid[i][j] == "X" else 'Miss.TButton')

    def start_game(self):
        """Starts the game"""
        self.setup.deploy_all_ships(self.players[1])
        self.display.setup_frame.grid_remove()
        self.display.game_frame.grid()
        self.display.game_message.config(
            text="Game started! Make your move",
            font=('Arial', 10),
            foreground='black'
        )

    def show_game_over(self, winner):
        """
        Displays the game over message.

        Args:
            winner (str): The winner of the game.
        """
        popup = tk.Toplevel(self.root)
        popup.title("Game Over")
        popup.transient(self.root)
        
        message = ttk.Label(popup, text=f"Game Over! {winner} wins!", 
                          font=('Arial', 14, 'bold'), padding=20)
        message.pack()
        
        # Create a frame for the buttons
        button_frame = ttk.Frame(popup, padding=10)
        button_frame.pack(fill=tk.X)
        
        play_again_btn = ttk.Button(button_frame, text="Play Again", 
                                  command=lambda: self.restart_game(popup))
        play_again_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        quit_btn = ttk.Button(button_frame, text="Quit", 
                           command=self.root.destroy)
        quit_btn.pack(side=tk.RIGHT, padx=10, pady=10)
        
        WindowManager.center_window(popup)

    def restart_game(self, popup):
        """
        Restarts the game.

        Args:
            popup (tk.Toplevel): The game over popup window.
        """

        # Destroy the popup
        popup.destroy()
        
        # Remove old game frames
        if hasattr(self, 'display'):
            self.display.setup_frame.destroy()
            self.display.game_frame.destroy()
        
        # Setup new game
        self.setup_new_game()

def main():
    root = tk.Tk()
    app = BattleshipGUI(root)
    root.minsize(600, 400)
    WindowManager.center_window(root)
    root.mainloop()

if __name__ == "__main__":
    main() 