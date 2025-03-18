import tkinter as tk
from tkinter import ttk

class WindowManager:
    """Handles window positioning and styling"""
    @staticmethod
    def center_window(window):
        """
        Centers the given window on the screen.

        Args:
            window (tk.Tk or tk.Toplevel): The window to center.
        """
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() - width) // 2
        y = (window.winfo_screenheight() - height) // 2
        window.geometry(f'+{x}+{y}')

    @staticmethod
    def create_styles():
        """Creates custom styles for the game buttons."""
        style = ttk.Style()
        style.configure('Ship.TButton', background='green')
        style.configure('Hit.TButton', background='red')
        style.configure('Miss.TButton', background='blue')
        
        # Add a style for sunk ship messages
        style.configure('Sunk.TLabel', 
                      foreground='red',
                      background='#f0f0f0',
                      font=('Arial', 12, 'bold'),
                      padding=10)
        
        # Add a style for computer sunk ship messages
        style.configure('ComputerSunk.TLabel', 
                      foreground='blue',
                      background='#f0f0f0',
                      font=('Arial', 12, 'bold'),
                      padding=10) 