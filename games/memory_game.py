import customtkinter as ctk
import random
import time
from tkinter import messagebox
import threading
import tkinter

class MemoryGame:
    def __init__(self, parent, game_manager=None):
        self.parent = parent
        self.game_manager = game_manager
        self.game_frame = None
        self.cards = []
        self.card_buttons = []
        self.flipped_cards = []
        self.matched_pairs = 0
        self.moves = 0
        self.start_time = None
        self.game_active = False
        self.grid_size = 4  # 4x4 grid (16 cards, 8 pairs)
        self.timer_job = None  # Track timer job for proper cleanup
        self.checking_match = False  # Prevent multiple simultaneous checks
        
        # Card themes
        self.themes = {
            "Numbers": list(range(1, 19)),  # Extended for 6x6 support (18 pairs max)
            "Letters": ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R'],
            "Symbols": ['★', '♠', '♥', '♦', '♣', '♪', '☀', '☽', '⚡', '❄', '🔥', '💧', '🌟', '⭐', '✨', '💫', '🌙', '☄'],
            "Emojis": ['🎮', '🎯', '🎨', '🎪', '🎭', '🎲', '🎸', '🎹', '🎵', '🎬', '🎤', '🎧', '🎺', '🎻', '🥁', '🎪', '🎠', '🎡']
        }
        self.current_theme = "Numbers"
        
        # Initialize the game window
        self.create_game_window()
        
    def create_game_window(self):
        # Clear parent and cancel any existing timers
        self.cleanup()
        for widget in self.parent.winfo_children():
            widget.destroy()
            
        # Main container
        main_container = ctk.CTkFrame(self.parent, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ctk.CTkFrame(main_container, height=80, fg_color="#1a1a2e")
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame, 
            text="🧠 Memory Game", 
            font=ctk.CTkFont(family="Arial", size=28, weight="bold"),
            text_color="#ffd700"
        )
        title_label.pack(side="left", padx=20, pady=20)
        
        # Controls frame
        controls_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        controls_frame.pack(side="right", padx=20, pady=20)
        
        # Theme selector
        theme_label = ctk.CTkLabel(controls_frame, text="Theme:", font=ctk.CTkFont(size=14))
        theme_label.pack(side="left", padx=(0, 10))
        
        self.theme_var = ctk.StringVar(value=self.current_theme)
        theme_menu = ctk.CTkOptionMenu(
            controls_frame,
            variable=self.theme_var,
            values=list(self.themes.keys()),
            command=self.change_theme,
            width=100
        )
        theme_menu.pack(side="left", padx=(0, 20))
        
        # Difficulty selector
        difficulty_label = ctk.CTkLabel(controls_frame, text="Size:", font=ctk.CTkFont(size=14))
        difficulty_label.pack(side="left", padx=(0, 10))
        
        self.difficulty_var = ctk.StringVar(value="4x4")
        difficulty_menu = ctk.CTkOptionMenu(
            controls_frame,
            variable=self.difficulty_var,
            values=["4x4", "6x6"],
            command=self.change_difficulty,
            width=80
        )
        difficulty_menu.pack(side="left", padx=(0, 20))
        
        # New Game button
        new_game_btn = ctk.CTkButton(
            controls_frame,
            text="New Game",
            command=self.start_new_game,
            width=100,
            height=35,
            fg_color="#00ff88",
            hover_color="#00cc6a"
        )
        new_game_btn.pack(side="left")
        
        # Stats frame
        stats_frame = ctk.CTkFrame(main_container, height=60, fg_color="#16213e")
        stats_frame.pack(fill="x", pady=(0, 20))
        stats_frame.pack_propagate(False)
        
        # Stats labels with proper font handling
        self.moves_label = ctk.CTkLabel(
            stats_frame, 
            text="Moves: 0", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.moves_label.pack(side="left", padx=20, pady=15)
        
        self.time_label = ctk.CTkLabel(
            stats_frame, 
            text="Time: 00:00", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.time_label.pack(side="left", padx=20, pady=15)
        
        self.pairs_label = ctk.CTkLabel(
            stats_frame, 
            text="Pairs: 0/8", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.pairs_label.pack(side="left", padx=20, pady=15)
        
        # Game area
        self.game_frame = ctk.CTkFrame(main_container, fg_color="#0f0f23")
        self.game_frame.pack(fill="both", expand=True)
        
        # Back button
        back_btn = ctk.CTkButton(
            main_container,
            text="← Back to Menu",
            command=self.back_to_menu,
            width=150,
            height=40,
            fg_color="#ff6b6b",
            hover_color="#ff5252"
        )
        back_btn.pack(pady=20)
        
        # Start first game
        self.start_new_game()
        
    def change_theme(self, theme):
        self.current_theme = theme
        if self.game_active:
            self.start_new_game()
            
    def change_difficulty(self, difficulty):
        if difficulty == "4x4":
            self.grid_size = 4
        elif difficulty == "6x6":
            self.grid_size = 6
        
        if self.game_active:
            self.start_new_game()
    
    def start_new_game(self):
        # Cleanup previous game
        self.cleanup()
        
        # Clear existing game
        if self.game_frame and self.game_frame.winfo_exists():
            for widget in self.game_frame.winfo_children():
                widget.destroy()
            
        # Reset game state
        self.cards = []
        self.card_buttons = []
        self.flipped_cards = []
        self.matched_pairs = 0
        self.moves = 0
        self.start_time = time.time()
        self.game_active = True
        self.checking_match = False
        
        # Create cards
        self.create_cards()
        self.create_card_grid()
        self.update_stats()
        
        # Start timer
        self.update_timer()
        
    def create_cards(self):
        total_pairs = (self.grid_size * self.grid_size) // 2
        theme_values = self.themes[self.current_theme][:total_pairs]
        
        # Ensure we have enough values for the selected grid size
        if len(theme_values) < total_pairs:
            # Fallback to numbers if theme doesn't have enough values
            theme_values = list(range(1, total_pairs + 1))
        
        # Create pairs
        self.cards = theme_values * 2
        random.shuffle(self.cards)
        
        # Update pairs label safely
        try:
            if hasattr(self, 'pairs_label') and self.pairs_label.winfo_exists():
                self.pairs_label.configure(text=f"Pairs: 0/{total_pairs}")
        except tkinter.TclError:
            pass
        
    def create_card_grid(self):
        if not self.game_frame or not self.game_frame.winfo_exists():
            return
            
        # Configure grid
        for i in range(self.grid_size):
            self.game_frame.grid_rowconfigure(i, weight=1)
            self.game_frame.grid_columnconfigure(i, weight=1)
            
        # Create card buttons
        self.card_buttons = []
        card_size = max(60, min(100, 400 // self.grid_size))
        
        for i in range(self.grid_size):
            row_buttons = []
            for j in range(self.grid_size):
                idx = i * self.grid_size + j
                
                btn = ctk.CTkButton(
                    self.game_frame,
                    text="?",
                    width=card_size,
                    height=card_size,
                    font=ctk.CTkFont(size=24, weight="bold"),
                    fg_color="#2b2b52",
                    hover_color="#3d3d73",
                    command=lambda index=idx: self.flip_card(index)
                )
                btn.grid(row=i, column=j, padx=2, pady=2, sticky="nsew")
                row_buttons.append(btn)
                
            self.card_buttons.append(row_buttons)
            
    def flip_card(self, index):
        if not self.game_active or len(self.flipped_cards) >= 2 or self.checking_match:
            return
        
        # Validate index
        if index < 0 or index >= len(self.cards):
            return
            
        row, col = index // self.grid_size, index % self.grid_size
        
        # Validate button exists
        try:
            if (row >= len(self.card_buttons) or col >= len(self.card_buttons[row])):
                return
            btn = self.card_buttons[row][col]
            if not btn.winfo_exists():
                return
        except (IndexError, tkinter.TclError):
            return
            
        # Don't flip already flipped or matched cards
        if (row, col) in self.flipped_cards or btn.cget("fg_color") == "#00ff88":
            return
            
        # Flip card
        try:
            btn.configure(text=str(self.cards[index]), fg_color="#ffd700", text_color="#000000")
            self.flipped_cards.append((row, col))
        except tkinter.TclError:
            return
        
        # Check for match
        if len(self.flipped_cards) == 2:
            self.moves += 1
            self.update_stats()
            self.checking_match = True
            # Use after() instead of threading for GUI operations
            self.parent.after(1000, self.check_match)
            
    def check_match(self):
        if len(self.flipped_cards) != 2 or not self.game_active:
            self.checking_match = False
            return
            
        try:
            pos1, pos2 = self.flipped_cards
            idx1 = pos1[0] * self.grid_size + pos1[1]
            idx2 = pos2[0] * self.grid_size + pos2[1]
            
            # Validate indices and buttons
            if (idx1 >= len(self.cards) or idx2 >= len(self.cards) or
                pos1[0] >= len(self.card_buttons) or pos1[1] >= len(self.card_buttons[pos1[0]]) or
                pos2[0] >= len(self.card_buttons) or pos2[1] >= len(self.card_buttons[pos2[0]])):
                self.flipped_cards = []
                self.checking_match = False
                return
            
            btn1 = self.card_buttons[pos1[0]][pos1[1]]
            btn2 = self.card_buttons[pos2[0]][pos2[1]]
            
            # Check if buttons still exist
            if not btn1.winfo_exists() or not btn2.winfo_exists():
                self.flipped_cards = []
                self.checking_match = False
                return
            
            if self.cards[idx1] == self.cards[idx2]:
                # Match found
                btn1.configure(fg_color="#00ff88", hover_color="#00ff88")
                btn2.configure(fg_color="#00ff88", hover_color="#00ff88")
                self.matched_pairs += 1
                
                # Check for game completion
                total_pairs = (self.grid_size * self.grid_size) // 2
                if self.matched_pairs == total_pairs:
                    self.game_complete()
            else:
                # No match, flip back
                btn1.configure(text="?", fg_color="#2b2b52", text_color="#ffffff")
                btn2.configure(text="?", fg_color="#2b2b52", text_color="#ffffff")
                
        except (IndexError, AttributeError, tkinter.TclError):
            # Handle any errors gracefully
            pass
        finally:
            self.flipped_cards = []
            self.checking_match = False
            self.update_stats()
        
    def game_complete(self):
        self.game_active = False
        self.cleanup()
        
        if self.start_time:
            end_time = time.time()
            game_time = int(end_time - self.start_time)
            
            minutes = game_time // 60
            seconds = game_time % 60
            
            try:
                messagebox.showinfo(
                    "Congratulations!",
                    f"🎉 You completed the memory game!\n\n"
                    f"Time: {minutes:02d}:{seconds:02d}\n"
                    f"Moves: {self.moves}\n"
                    f"Grid Size: {self.grid_size}x{self.grid_size}\n"
                    f"Theme: {self.current_theme}"
                )
            except Exception:
                # Fallback if messagebox fails
                print(f"Game completed! Time: {minutes:02d}:{seconds:02d}, Moves: {self.moves}")
        
    def update_stats(self):
        try:
            if not self.game_active:
                return
                
            total_pairs = (self.grid_size * self.grid_size) // 2
            
            if hasattr(self, 'moves_label') and self.moves_label.winfo_exists():
                self.moves_label.configure(text=f"Moves: {self.moves}")
            if hasattr(self, 'pairs_label') and self.pairs_label.winfo_exists():
                self.pairs_label.configure(text=f"Pairs: {self.matched_pairs}/{total_pairs}")
        except (AttributeError, tkinter.TclError):
            pass
        
    def update_timer(self):
        try:
            if self.game_active and self.start_time and hasattr(self, 'time_label') and self.time_label.winfo_exists():
                elapsed = int(time.time() - self.start_time)
                minutes = elapsed // 60
                seconds = elapsed % 60
                self.time_label.configure(text=f"Time: {minutes:02d}:{seconds:02d}")
                # Store the timer job reference for cleanup
                self.timer_job = self.parent.after(1000, self.update_timer)
        except (AttributeError, tkinter.TclError):
            # Widget no longer exists, stop timer
            self.game_active = False
            
    def cleanup(self):
        """Clean up timers and resources"""
        self.game_active = False
        if self.timer_job:
            try:
                self.parent.after_cancel(self.timer_job)
            except:
                pass
            self.timer_job = None
            
    def back_to_menu(self):
        self.cleanup()
        if self.game_manager:
            self.game_manager.return_to_menu()
        else:
            # Fallback: clear the parent frame
            for widget in self.parent.winfo_children():
                widget.destroy()
            print("Returning to main menu...")

# Test function
def test_memory_game():
    """Test function to run the memory game standalone"""
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()
    root.title("Memory Game Test")
    root.geometry("800x700")
    
    game = MemoryGame(root)
    
    root.mainloop()

if __name__ == "__main__":
    test_memory_game()