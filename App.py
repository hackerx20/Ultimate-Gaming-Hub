import customtkinter as ctk
from tkinter import messagebox
import time
import os
import sys
from utils.game_manager import GameManager
from ui.main_menu import MainMenu

class App:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Ultimate Gaming Platform")
        self.root.geometry("1200x800")
        
        # Set appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Initialize game manager
        self.game_manager = GameManager(self)
        
        # Create main menu
        self.main_menu = MainMenu(self.root, self.game_manager)
        self.main_menu_frame = self.main_menu.main_frame  # Save the frame to re-pack later

        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    # Add the project root directory to Python path
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(project_root)
    
    app = App()
    app.run()