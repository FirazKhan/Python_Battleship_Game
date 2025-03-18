from game_setup import GameSetup
from game_loop import GameLoop
from battleship_config import config
import sys

class CLIGamePlay:
    """Main game coordinator for CLI version"""
    def __init__(self):
        """Initializes the GamePlay with game setup and players."""
        self.setup_new_game()

    def setup_new_game(self):
        """Sets up a new game instance"""
        self.setup = GameSetup()
        self.players = self.setup.players
        self.game_loop = GameLoop(self.players)

    def display_welcome_message(self):
        """Displays game introduction and instructions"""
        print('----------------------------------------- Welcome to the game \033[1m"BATTLESHIP"\033[0m -----------------------------------------')
        print('\n\033[1m                                        OBJECTIVE\033[0m')
        print(config['instructions']['objective'])
        
        print('\n\033[1m                                         SETUP\033[0m')
        for setup_instruction in config['instructions']['setup']:
            print(setup_instruction)
        
        print("\n2. The fleet includes:\n")
        for ship, length in config['ships'].items():
            print(f" • 1 {ship} ({length} squares)")
        
        print('\n\033[1m                                        GAMEPLAY\033[0m')
        for gameplay_instruction in config['instructions']['gameplay']:
            print(gameplay_instruction)
        
        print('\n\033[1m                                        WINNING\033[0m')
        print(config['instructions']['winning'])
        print('\n')
        print('---------------------------------------------------------------------------------------------------------------')

    def ask_play_again(self):
        """
        Asks the user if they want to play again or quit.
        
        Returns:
            bool: True if the user wants to play again, False otherwise.
        """
        while True:
            choice = input("\nDo you want to play again? (y/n): ").strip().lower()
            if choice == 'y' or choice == 'yes':
                return True
            elif choice == 'n' or choice == 'no':
                print("\nThanks for playing! Goodbye!")
                return False
            else:
                print("Invalid choice. Please enter 'y' for yes or 'n' for no.")

    def run_game(self):
        """Coordinates the complete game flow"""
        self.display_welcome_message()  # Show introduction
        
        while True:
            # Reset the game state for a new game
            self.setup_new_game()
            
            # Deploy ships for both players
            for player in self.players:
                self.setup.deploy_all_ships(player)  # Setup phase
            
            # Run the main game loop
            self.game_loop.run()  # Main game loop
            
            # Ask if the player wants to play again
            if not self.ask_play_again():
                break
            
            print("\n\n===============================================")
            print("           Starting a new game!")
            print("===============================================\n\n") 