# Battleship Game

A Python implementation of the classic Battleship game with both **GUI** and **Command-Line** interfaces where you play against an AI opponent.

## Overview

This project brings the timeless Battleship game to life with two distinct gameplay modes:
- **GUI Version**: Interactive graphical interface using Tkinter
- **CLI Version**: Traditional command-line gameplay

Battle against an intelligent computer opponent in an 8x8 grid-based naval strategy game.

## Features

✨ **Two Game Modes**
- Graphical User Interface (Tkinter-based)
- Command-Line Interface

🎮 **Gameplay Features**
- 8x8 game board with letter/number coordinate system
- Five types of ships (Carrier, Battleship, Cruiser, Submarine, Destroyer)
- Intelligent AI opponent
- Turn-based gameplay
- Hit/Miss tracking and visual feedback
- Ship placement validation
- Game state management

🔧 **Technical Features**
- Object-oriented architecture
- Configuration-based game settings (JSON)
- Unit tests included
- Color-coded terminal output for CLI version

## Game Modes

### 5 Ship Types
- **Carrier**: 5 squares
- **Battleship**: 4 squares
- **Cruiser**: 3 squares
- **Submarine**: 3 squares
- **Destroyer**: 2 squares

## Requirements

To run this game, you need:
- Python 3.x
- Required packages listed in requirements.txt

## Installation

1. **Clone the repository** (or download the files)
   ```bash
   git clone <repository-url>
   cd Battleship-Game
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

### Start the Game
```bash
python main.py
```

You'll be presented with a menu to choose between:
- **Option 1**: GUI Version (Graphical Interface)
- **Option 2**: Command-Line Version (Terminal-based)

### GUI Version
- Select ships placement on your board
- Click coordinates on the opponent's board to attack
- Intuitive visual feedback with clicks showing hits and misses

### CLI Version
- Place your ships by entering coordinates
- Enter attack coordinates when prompted
- View live updated boards with clear hit/miss markers

## Gameplay Instructions

### Objective
Sink all of your opponent's ships before they sink all of yours.

### Setup Phase
1. Each player receives an 8x8 grid (labeled A-H rows, 1-8 columns)
2. Players secretly place their five ships either horizontally or vertically
3. Ships cannot overlap or be placed diagonally

### During Gameplay
1. Players alternate turns calling out coordinates (e.g., B6)
2. Opponent responds with "Hit" or "Miss"
3. Board updates show hits (X) and misses (-)
4. When all squares of a ship are hit, the ship sinks (announced)

### Victory Condition
First player to sink all opponent's ships wins!

## Video Tutorials

### Original Gameplay Tutorial
[Watch the original gameplay tutorial](https://youtu.be/4gHJlYLomrs?si=DQgB6NL0lvH1ZWOU)

### How the Game Works
[View detailed game walkthrough](https://drive.google.com/file/d/1mRpq5Y_B3iUPA-9u3zXW7lwmjBkN_Ipt/view?usp=drive_link)

## Project Structure

```
├── main.py                      # Main entry point
├── cli_gameplay.py              # Command-line interface implementation
├── gui_gameplay.py              # GUI implementation with Tkinter
├── game_loop.py                 # Main game loop logic
├── game_setup.py                # Game initialization and setup
├── base_player.py               # Base player class
├── human_player.py              # Human player implementation
├── computer_player.py           # AI opponent logic
├── ship_manager.py              # Ship management and tracking
├── board_display.py             # Board display logic
├── board_validator.py           # Board and move validation
├── battleship_config.py         # Configuration loader
├── config.json                  # Game configuration (board size, ships, etc.)
├── requirements.txt             # Python dependencies
├── Battleship_Game_UnitTest.py  # Unit tests
└── README.md                    # This file
```

## Dependencies

```plaintext
numpy==1.24.3
tk==0.1.0
```

## Testing

Run the included unit tests to verify functionality:
```bash
python Battleship_Game_UnitTest.py
```

## Key Classes and Modules

### Core Classes
- **BasePlayer**: Abstract base class for game players
- **HumanPlayer**: Represents the human player
- **ComputerPlayer**: AI opponent with strategic gameplay
- **GameLoop**: Manages turn sequence and game state
- **ShipManager**: Handles ship placement and tracking
- **BoardValidator**: Validates moves and placements

### Display Modules
- **BoardDisplay**: CLI-based board rendering
- **GUIDisplay**: Tkinter-based graphical interface

## Game Configuration

All game settings are defined in `config.json`:
- Board size: 8x8
- Ship types and sizes
- Grid coordinate mappings
- Game rules and objectives

## Author Notes

This implementation provides a fully functional Battleship game with strategic AI opponent that adapts to gameplay. Both interface options offer engaging gameplay experiences suited to different preferences.

---

**Enjoy the game! May your naval tactics reign supreme!** ⚓🎮
