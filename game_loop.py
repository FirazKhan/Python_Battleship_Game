class GameLoop:
    """Manages the main game loop and turn sequence"""
    def __init__(self, players):
        """
        Initializes the GameLoop with the given players.
        
        Args:
            players (list): List of player objects.
        """
        self.players = players
        self.current_player = 0

    def run(self):
        """Executes the main game loop until a winner is determined"""
        while True:
            current_player = self.players[self.current_player]
            opponent = self.players[1 - self.current_player]

            print(f'\033[1m               {current_player.name}\'s turn:\033[0m')
            
            if current_player.name == "Player":
                print('\033[1m       Player`s Guess Board\033[0m')
                current_player.display.display_board(current_player.attack_board.grid)
                current_player.take_turn(opponent)
            else:
                current_player.take_turn(opponent)

            if opponent.ship_manager.all_ships_sunk():
                print("\n*******************************************")
                print(f"\033[1m       {current_player.name} has won the game!\033[0m")
                print("*******************************************\n")
                break

            self.current_player = 1 - self.current_player
            print('----------------------------------------------') 