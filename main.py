import sys
import tkinter as tk

def run_gui_version():
    """Run the GUI version of the Battleship game."""
    from gui_gameplay import main as gui_main
    gui_main()

def run_command_line_version():
    """Run the command-line version of the Battleship game."""
    from cli_gameplay import CLIGamePlay
    game = CLIGamePlay()
    game.run_game()

def main():
    """Main entry point for the Battleship game."""
    print("Welcome to Battleship!")
    print("Choose your game mode:")
    print("1. GUI Version")
    print("2. Command-Line Version")
    
    while True:
        try:
            choice = input("Enter your choice (1 or 2): ").strip()
            
            if choice == '1':
                # GUI Version
                root = tk.Tk()
                from gui_gameplay import BattleshipGUI
                app = BattleshipGUI(root)
                root.minsize(600, 400)
                root.mainloop()
                break
            
            elif choice == '2':
                # Command-Line Version
                run_command_line_version()
                break
            
            else:
                print("Invalid choice. Please enter 1 or 2.")
        
        except KeyboardInterrupt:
            print("\nGame terminated.")
            sys.exit(0)
        except Exception as e:
            print(f"An error occurred: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main() 