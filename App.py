# In your app.py, make sure you have this structure:

import customtkinter as ctk
from ui.main_menu import MainMenu
from utils.game_manager import GameManager

class GameApp:
    def __init__(self):
        # Initialize CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("Ultimate Gaming Platform")
        self.root.geometry("1200x800")
        self.root.configure(fg_color=("#1a1a2e", "#0f0f23"))
        
        # Initialize GameManager with self as main_app
        self.game_manager = GameManager(self)
        
        # Initialize MainMenu
        self.main_menu = MainMenu(self.root, self.game_manager)
        self.main_menu_frame = self.main_menu.main_frame
    
    def show_main_menu(self):
        """Method to return to main menu - CRITICAL for callbacks"""
        print("App: Showing main menu...")
        try:
            # Clear all widgets from root
            for widget in self.root.winfo_children():
                widget.destroy()
            
            # Re-create the main menu
            self.main_menu = MainMenu(self.root, self.game_manager)
            self.main_menu_frame = self.main_menu.main_frame
            
            print("App: Main menu recreated successfully")
        except Exception as e:
            print(f"App: Error showing main menu: {e}")
    
    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"Error running application: {e}")
        finally:
            # Cleanup
            if hasattr(self, 'game_manager'):
                self.game_manager.force_cleanup()

if __name__ == "__main__":
    app = GameApp()
    app.run()