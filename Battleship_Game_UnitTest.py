import unittest
import tkinter as tk
from battleship_config import BOARD_SIZE, SHIP_TYPES
from board_display import BoardDisplay
from ship_manager import ShipManager
from board_validator import BoardValidator
from human_player import HumanPlayer
from computer_player import ComputerPlayer
from game_setup import GameSetup
from window_manager import WindowManager
from gui_display import GameDisplay
from gui_gameplay import BattleshipGUI

class TestBoardDisplay(unittest.TestCase):
    """Test cases for the BoardDisplay class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.display = BoardDisplay()

    def test_color_initialization(self):
        """Test if color codes are correctly initialized"""
        self.assertIn('X', self.display.COLORS)
        self.assertIn('-', self.display.COLORS)
        self.assertIn('RESET', self.display.COLORS)

class TestShipManager(unittest.TestCase):
    """Test cases for the ShipManager class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.ship_manager = ShipManager("Player")

    def test_initialization(self):
        """Test if ship manager is correctly initialized"""
        self.assertEqual(len(self.ship_manager.grid), BOARD_SIZE)
        self.assertEqual(len(self.ship_manager.grid[0]), BOARD_SIZE)
        self.assertEqual(self.ship_manager.ship_locations, {})
        self.assertEqual(self.ship_manager.opponent, "Player")

    def test_ship_deployment(self):
        """Test ship deployment functionality"""
        self.ship_manager.deploy_ship("Destroyer", 2, 0, 0, "H")
        
        # Check if ship is placed correctly
        self.assertEqual(self.ship_manager.grid[0][0], "X")
        self.assertEqual(self.ship_manager.grid[0][1], "X")
        self.assertEqual(len(self.ship_manager.ship_locations["Destroyer"]), 2)

    def test_check_sunk_ship(self):
        """Test ship sinking detection"""
        self.ship_manager.deploy_ship("Destroyer", 2, 0, 0, "H")
        
        # Hit first position
        self.ship_manager.check_sunk_ship(0, 0)
        self.assertIn("Destroyer", self.ship_manager.ship_locations)
        
        # Hit second position
        self.ship_manager.check_sunk_ship(0, 1)
        self.assertNotIn("Destroyer", self.ship_manager.ship_locations)

    def test_all_ships_sunk(self):
        """Test detection of all ships being sunk"""
        self.assertTrue(self.ship_manager.all_ships_sunk())
        
        self.ship_manager.deploy_ship("Destroyer", 2, 0, 0, "H")
        self.assertFalse(self.ship_manager.all_ships_sunk())
        
    def test_check_sunk_ship_gui(self):
        """Test the GUI version of ship sinking detection"""
        self.ship_manager.deploy_ship("Destroyer", 2, 0, 0, "H")
        
        # Hit first position
        result = self.ship_manager.check_sunk_ship_gui(0, 0)
        self.assertIsNone(result)
        self.assertIn("Destroyer", self.ship_manager.ship_locations)
        
        # Hit second position
        result = self.ship_manager.check_sunk_ship_gui(0, 1)
        self.assertEqual(result, "Destroyer")
        self.assertNotIn("Destroyer", self.ship_manager.ship_locations)

class TestBoardValidator(unittest.TestCase):
    """Test cases for the BoardValidator class"""

    def setUp(self):
        """Set up test fixtures before each test method"""
        self.validator = BoardValidator()
        self.test_grid = [[" "] * BOARD_SIZE for _ in range(BOARD_SIZE)]

    def test_validate_placement(self):
        """Test ship placement validation"""
        # Test valid placements
        self.assertTrue(self.validator.validate_placement(3, 0, 0, "H"))
        self.assertTrue(self.validator.validate_placement(3, 0, 0, "V"))
        
        # Test invalid placements (out of bounds)
        self.assertFalse(self.validator.validate_placement(3, 0, 6, "H"))
        self.assertFalse(self.validator.validate_placement(3, 6, 0, "V"))

    def test_check_overlap(self):
        """Test ship overlap detection"""
        # Place a ship
        self.test_grid[0][0] = "X"
        self.test_grid[0][1] = "X"
        
        # Test overlap detection
        self.assertTrue(self.validator.check_overlap(self.test_grid, 0, 0, "H", 2))
        self.assertFalse(self.validator.check_overlap(self.test_grid, 2, 2, "H", 2))

class TestHumanPlayer(unittest.TestCase):
    """Test cases for the HumanPlayer class"""

    def setUp(self):
        """Set up test fixtures before each test method"""
        self.player = HumanPlayer()

    def test_initialization(self):
        """Test player initialization"""
        self.assertEqual(self.player.name, "Player")
        self.assertEqual(self.player.opponent_name, "Computer")
        self.assertIsInstance(self.player.ship_manager, ShipManager)
        self.assertIsInstance(self.player.attack_board, ShipManager)
        self.assertIsInstance(self.player.display, BoardDisplay)
        self.assertIsInstance(self.player.validator, BoardValidator)
        
    def test_gui_mode(self):
        """Test GUI mode settings"""
        self.assertFalse(self.player.gui_mode)
        self.player.set_gui_mode(True)
        self.assertTrue(self.player.gui_mode)
        self.player.set_gui_mode(False)
        self.assertFalse(self.player.gui_mode)

class TestComputerPlayer(unittest.TestCase):
    """Test cases for the ComputerPlayer class"""

    def setUp(self):
        """Set up test fixtures before each test method"""
        self.computer = ComputerPlayer()

    def test_initialization(self):
        """Test computer player initialization"""
        self.assertEqual(self.computer.name, "Computer")
        self.assertEqual(self.computer.opponent_name, "Player")
        self.assertIsNone(self.computer.last_hit)
        self.assertEqual(self.computer.hit_stack, [])
        self.assertIsNone(self.computer.direction)

    def test_probability_map_initialization(self):
        """Test probability map initialization"""
        self.computer.update_probability_map(HumanPlayer())
        self.assertEqual(self.computer.probability_map.shape, (BOARD_SIZE, BOARD_SIZE))
        
    def test_gui_mode(self):
        """Test GUI mode settings"""
        self.assertFalse(self.computer.gui_mode)
        self.computer.set_gui_mode(True)
        self.assertTrue(self.computer.gui_mode)
        self.computer.set_gui_mode(False)
        self.assertFalse(self.computer.gui_mode)

class TestGameSetup(unittest.TestCase):
    """Test cases for the GameSetup class"""

    def setUp(self):
        """Set up test fixtures before each test method"""
        self.setup = GameSetup()

    def test_initialization(self):
        """Test game setup initialization"""
        self.assertEqual(len(self.setup.players), 2)
        self.assertIsInstance(self.setup.players[0], HumanPlayer)
        self.assertIsInstance(self.setup.players[1], ComputerPlayer)

class TestWindowManager(unittest.TestCase):
    """Test cases for the WindowManager class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the window
    
    def tearDown(self):
        """Clean up after each test method"""
        self.root.destroy()
    
    def test_center_window(self):
        """Test window centering"""
        # This is more of a functional test, but let's ensure it doesn't error
        try:
            WindowManager.center_window(self.root)
            success = True
        except Exception:
            success = False
        self.assertTrue(success)
    
    def test_create_styles(self):
        """Test style creation"""
        try:
            WindowManager.create_styles()
            style = self.root.tk.call("ttk::style", "configure", "Ship.TButton", "-background")
            self.assertIsNotNone(style)
            success = True
        except Exception:
            success = False
        self.assertTrue(success)

class TestGameDisplay(unittest.TestCase):
    """Test cases for the GameDisplay class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the window
        try:
            self.display = GameDisplay(self.root)
            self.setup_success = True
        except Exception:
            self.setup_success = False
    
    def tearDown(self):
        """Clean up after each test method"""
        self.root.destroy()
    
    def test_initialization(self):
        """Test GameDisplay initialization"""
        self.assertTrue(self.setup_success)
        self.assertTrue(hasattr(self.display, 'setup_frame'))
        self.assertTrue(hasattr(self.display, 'game_frame'))
        self.assertTrue(hasattr(self.display, 'placement_buttons'))
        self.assertTrue(hasattr(self.display, 'player_buttons'))
        self.assertTrue(hasattr(self.display, 'computer_buttons'))
        self.assertTrue(hasattr(self.display, 'game_message'))
        
    def test_button_grid_size(self):
        """Test button grid dimensions"""
        self.assertEqual(len(self.display.placement_buttons), BOARD_SIZE)
        self.assertEqual(len(self.display.placement_buttons[0]), BOARD_SIZE)
        self.assertEqual(len(self.display.player_buttons), BOARD_SIZE)
        self.assertEqual(len(self.display.player_buttons[0]), BOARD_SIZE)
        self.assertEqual(len(self.display.computer_buttons), BOARD_SIZE)
        self.assertEqual(len(self.display.computer_buttons[0]), BOARD_SIZE)

class TestBattleshipGUI(unittest.TestCase):
    """Test cases for the BattleshipGUI class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the window
        try:
            WindowManager.create_styles()
            self.gui = BattleshipGUI(self.root)
            self.setup_success = True
        except Exception as e:
            print(f"Setup error: {e}")
            self.setup_success = False
    
    def tearDown(self):
        """Clean up after each test method"""
        self.root.destroy()
    
    def test_initialization(self):
        """Test BattleshipGUI initialization"""
        self.assertTrue(self.setup_success)
        self.assertTrue(hasattr(self.gui, 'setup'))
        self.assertTrue(hasattr(self.gui, 'players'))
        self.assertTrue(hasattr(self.gui, 'display'))
        self.assertEqual(len(self.gui.players), 2)
        self.assertIsInstance(self.gui.players[0], HumanPlayer)
        self.assertIsInstance(self.gui.players[1], ComputerPlayer)
        
    def test_gui_mode_setting(self):
        """Test that GUI mode is set correctly"""
        # Both players should have GUI mode set to True
        self.assertTrue(hasattr(self.gui.players[0], 'gui_mode'))
        self.assertTrue(hasattr(self.gui.players[1], 'gui_mode'))
        self.assertTrue(self.gui.players[0].gui_mode)
        self.assertTrue(self.gui.players[1].gui_mode)

def run_tests():
    """Run all test cases"""
    unittest.main()

if __name__ == '__main__':
    run_tests() 