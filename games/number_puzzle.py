import customtkinter as ctk
import random
import math
import tkinter
from tkinter import messagebox
import json
import os

class NumberPuzzle:
    def __init__(self, parent, return_callback=None):
        self.parent = parent
        self.grid_size = 4
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.score = 0
        self.best_score = self.load_best_score()
        self.moves = 0
        self.game_active = False
        self.tile_buttons = []
        self.previous_state = None
        self.game_won_shown = False  # Track if win message was shown
        self.return_callback = return_callback
        # Colors for different tile values
        self.tile_colors = {
            0: "#cdc1b4",
            2: "#eee4da",
            4: "#ede0c8",
            8: "#f2b179",
            16: "#f59563",
            32: "#f67c5f",
            64: "#f65e3b",
            128: "#edcf72",
            256: "#edcc61",
            512: "#edc850",
            1024: "#edc53f",
            2048: "#edc22e",
            4096: "#3c3a32",
            8192: "#3c3a32",
            16384: "#3c3a32"
        }
        
        self.text_colors = {
            0: "#776e65",
            2: "#776e65",
            4: "#776e65",
            8: "#f9f6f2",
            16: "#f9f6f2",
            32: "#f9f6f2",
            64: "#f9f6f2",
            128: "#f9f6f2",
            256: "#f9f6f2",
            512: "#f9f6f2",
            1024: "#f9f6f2",
            2048: "#f9f6f2",
            4096: "#f9f6f2",
            8192: "#f9f6f2",
            16384: "#f9f6f2"
        }
        
    def load_best_score(self):
        """Load best score from file"""
        try:
            score_file = "2048_best_score.json"
            if os.path.exists(score_file):
                with open(score_file, 'r') as f:
                    data = json.load(f)
                    return data.get('best_score', 0)
        except (json.JSONDecodeError, IOError, KeyError):
            pass
        return 0
    
    def save_best_score(self):
        """Save best score to file"""
        try:
            score_file = "2048_best_score.json"
            with open(score_file, 'w') as f:
                json.dump({'best_score': self.best_score}, f)
        except IOError:
            pass  # Fail silently if can't save
        
    def create_game_window(self):
        # Clear parent and unbind any existing key handlers
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
            text="🔢 2048 Puzzle", 
            font=("Arial", 28, "bold"),
            text_color="#ffd700"
        )
        title_label.pack(side="left", padx=20, pady=20)
        
        # Controls
        controls_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        controls_frame.pack(side="right", padx=20, pady=20)
        
        new_game_btn = ctk.CTkButton(
            controls_frame,
            text="New Game",
            command=self.start_new_game,
            width=100,
            height=35,
            fg_color="#00ff88",
            hover_color="#00cc6a"
        )
        new_game_btn.pack(side="left", padx=(0, 10))
        
        self.undo_btn = ctk.CTkButton(
            controls_frame,
            text="Undo",
            command=self.undo_move,
            width=80,
            height=35,
            fg_color="#ffd700",
            hover_color="#ffcc00",
            text_color="#000000",
            state="disabled"  # Initially disabled
        )
        self.undo_btn.pack(side="left")
        
        # Score panel
        score_frame = ctk.CTkFrame(main_container, height=60, fg_color="#16213e")
        score_frame.pack(fill="x", pady=(0, 20))
        score_frame.pack_propagate(False)
        
        self.score_label = ctk.CTkLabel(
            score_frame,
            text="Score: 0",
            font=("Arial", 18, "bold"),
            text_color="#ffd700"
        )
        self.score_label.pack(side="left", padx=20, pady=15)
        
        self.best_label = ctk.CTkLabel(
            score_frame,
            text=f"Best: {self.best_score}",
            font=("Arial", 18, "bold"),
            text_color="#00ff88"
        )
        self.best_label.pack(side="left", padx=20, pady=15)
        
        self.moves_label = ctk.CTkLabel(
            score_frame,
            text="Moves: 0",
            font=("Arial", 18, "bold")
        )
        self.moves_label.pack(side="left", padx=20, pady=15)
        
        # Goal info
        goal_label = ctk.CTkLabel(
            score_frame,
            text="Goal: Reach 2048!",
            font=("Arial", 16, "bold"),
            text_color="#ff6b6b"
        )
        goal_label.pack(side="right", padx=20, pady=15)
        
        # Game grid container
        grid_container = ctk.CTkFrame(main_container, fg_color="#bbada0")
        grid_container.pack(pady=20)
        
        # Create game grid
        self.create_grid(grid_container)
        
        # Instructions
        instructions_frame = ctk.CTkFrame(main_container, fg_color="#0f0f23")
        instructions_frame.pack(fill="x", pady=20)
        
        instructions_text = """🎯 HOW TO PLAY: Use arrow keys to move tiles. When two tiles with the same number touch, they merge into one!
⌨️ CONTROLS: ← → ↑ ↓ Arrow Keys to move tiles | Try to reach the 2048 tile to win!"""
        
        instructions_label = ctk.CTkLabel(
            instructions_frame,
            text=instructions_text,
            font=("Arial", 14),
            justify="center"
        )
        instructions_label.pack(pady=15)
        
        # Back button
        back_btn = ctk.CTkButton(
            main_container,
            text="← Back to Menu",
            command=self.return_to_menu,
            width=150,
            height=40,
            fg_color="#ff6b6b",
            hover_color="#ff5252"
        )
        back_btn.pack(pady=20)
        
        # Bind keys - Fixed key binding
        self.parent.bind('<KeyPress>', self.handle_keypress)
        self.parent.focus_set()
        
        # Start game
        self.start_new_game()
        
    def create_grid(self, parent):
        self.tile_buttons = []
        
        for i in range(self.grid_size):
            row_buttons = []
            for j in range(self.grid_size):
                btn = ctk.CTkButton(
                    parent,
                    text="",
                    width=80,
                    height=80,
                    font=("Arial", 24, "bold"),
                    fg_color=self.tile_colors[0],
                    text_color=self.text_colors[0],
                    hover_color=self.tile_colors[0],
                    state="disabled"
                )
                btn.grid(row=i, column=j, padx=5, pady=5)
                row_buttons.append(btn)
            self.tile_buttons.append(row_buttons)
            
    def start_new_game(self):
        # Reset game state
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.score = 0
        self.moves = 0
        self.game_active = True
        self.previous_state = None
        self.game_won_shown = False
        
        # Update undo button state
        if hasattr(self, 'undo_btn') and self.undo_btn.winfo_exists():
            self.undo_btn.configure(state="disabled")
        
        # Add two initial tiles
        self.add_random_tile()
        self.add_random_tile()
        
        self.update_display()
    def add_random_tile(self):
        empty_cells = []
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] == 0:
                    empty_cells.append((i, j))
                    
        if empty_cells:
            i, j = random.choice(empty_cells)
            # 90% chance of 2, 10% chance of 4
            self.grid[i][j] = 2 if random.random() < 0.9 else 4


    def handle_keypress(self, event):
        if not self.game_active:
            return
            
        key = event.keysym
        moved = False
        
        # Save current state for undo
        self.previous_state = {
            'grid': [row[:] for row in self.grid],
            'score': self.score,
            'moves': self.moves
        }
        
        if key == 'Left':
            moved = self.move_left()
        elif key == 'Right':
            moved = self.move_right()
        elif key == 'Up':
            moved = self.move_up()
        elif key == 'Down':
            moved = self.move_down()
            
        if moved:
            self.add_random_tile()
            self.moves += 1
            self.update_display()
            self.check_game_state()
            
            # Enable undo button
            if hasattr(self, 'undo_btn') and self.undo_btn.winfo_exists():
                self.undo_btn.configure(state="normal")
        else:
            # No move made, restore previous state
            self.previous_state = None
            
    def move_left(self):
        moved = False
        for i in range(self.grid_size):
            # Compress row
            row = [cell for cell in self.grid[i] if cell != 0]
            
            # Merge adjacent equal values
            j = 0
            while j < len(row) - 1:
                if row[j] == row[j + 1]:
                    row[j] *= 2
                    self.score += row[j]
                    del row[j + 1]
                j += 1
                
            # Pad with zeros
            row.extend([0] * (self.grid_size - len(row)))
            
            # Check if row changed
            if row != self.grid[i]:
                moved = True
                self.grid[i] = row
                
        return moved
        
    def move_right(self):
        moved = False
        for i in range(self.grid_size):
            # Compress row (from right)
            row = [cell for cell in self.grid[i] if cell != 0]
            
            # Merge adjacent equal values (from right)
            j = len(row) - 1
            while j > 0:
                if row[j] == row[j - 1]:
                    row[j] *= 2
                    self.score += row[j]
                    del row[j - 1]
                    j -= 1
                else:
                    j -= 1
                    
            # Pad with zeros at beginning
            row = [0] * (self.grid_size - len(row)) + row
            
            # Check if row changed
            if row != self.grid[i]:
                moved = True
                self.grid[i] = row
                
        return moved
        
    def move_up(self):
        moved = False
        for j in range(self.grid_size):
            # Extract column
            column = [self.grid[i][j] for i in range(self.grid_size)]
            
            # Compress column
            column = [cell for cell in column if cell != 0]
            
            # Merge adjacent equal values
            i = 0
            while i < len(column) - 1:
                if column[i] == column[i + 1]:
                    column[i] *= 2
                    self.score += column[i]
                    del column[i + 1]
                i += 1
                
            # Pad with zeros
            column.extend([0] * (self.grid_size - len(column)))
            
            # Check if column changed
            original_column = [self.grid[i][j] for i in range(self.grid_size)]
            if column != original_column:
                moved = True
                for i in range(self.grid_size):
                    self.grid[i][j] = column[i]
                    
        return moved
        
    def move_down(self):
        moved = False
        for j in range(self.grid_size):
            # Extract column
            column = [self.grid[i][j] for i in range(self.grid_size)]
            
            # Compress column (from bottom)
            column = [cell for cell in column if cell != 0]
            
            # Merge adjacent equal values (from bottom)
            i = len(column) - 1
            while i > 0:
                if column[i] == column[i - 1]:
                    column[i] *= 2
                    self.score += column[i]
                    del column[i - 1]
                    i -= 1
                else:
                    i -= 1
                    
            # Pad with zeros at beginning
            column = [0] * (self.grid_size - len(column)) + column
            
            # Check if column changed
            original_column = [self.grid[i][j] for i in range(self.grid_size)]
            if column != original_column:
                moved = True
                for i in range(self.grid_size):
                    self.grid[i][j] = column[i]
                    
        return moved
        
    def undo_move(self):
        if self.previous_state and self.game_active:
            self.grid = self.previous_state['grid']
            self.score = self.previous_state['score']
            self.moves = self.previous_state['moves']
            self.previous_state = None
            self.update_display()
            
            # Disable undo button after use
            if hasattr(self, 'undo_btn') and self.undo_btn.winfo_exists():
                self.undo_btn.configure(state="disabled")
            
    def update_display(self):
        try:
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    if (i < len(self.tile_buttons) and j < len(self.tile_buttons[i]) and
                        self.tile_buttons[i][j].winfo_exists()):
                        
                        value = self.grid[i][j]
                        btn = self.tile_buttons[i][j]
                        
                        if value == 0:
                            btn.configure(text="", fg_color=self.tile_colors[0])
                        else:
                            # Calculate font size based on number length
                            font_size = 24 if value < 1000 else (20 if value < 10000 else 16)
                            
                            btn.configure(
                                text=str(value),
                                fg_color=self.tile_colors.get(value, "#3c3a32"),
                                text_color=self.text_colors.get(value, "#f9f6f2"),
                                font=("Arial", font_size, "bold")
                            )
                            
            # Update scores
            if hasattr(self, 'score_label') and self.score_label.winfo_exists():
                self.score_label.configure(text=f"Score: {self.score}")
            
            if self.score > self.best_score:
                self.best_score = self.score
                self.save_best_score()
                
            if hasattr(self, 'best_label') and self.best_label.winfo_exists():
                self.best_label.configure(text=f"Best: {self.best_score}")
                
            if hasattr(self, 'moves_label') and self.moves_label.winfo_exists():
                self.moves_label.configure(text=f"Moves: {self.moves}")
                
        except (AttributeError, tkinter.TclError):
            # Handle widget destruction gracefully
            pass
        
    def check_game_state(self):
        # Check for 2048 (win condition) - only show once
        if not self.game_won_shown:
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    if self.grid[i][j] == 2048:
                        self.game_won()
                        return
                    
        # Check for game over
        if self.is_game_over():
            self.game_over()
            
    def is_game_over(self):
        # Check for empty cells
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] == 0:
                    return False
                    
        # Check for possible moves
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                current = self.grid[i][j]
                
                # Check right neighbor
                if j < self.grid_size - 1 and self.grid[i][j + 1] == current:
                    return False
                    
                # Check bottom neighbor
                if i < self.grid_size - 1 and self.grid[i + 1][j] == current:
                    return False
                    
        return True
        
    def game_won(self):
        self.game_won_shown = True
        try:
            result = messagebox.askyesno(
                "Congratulations!",
                f"🎉 You reached 2048!\n\n"
                f"Final Score: {self.score}\n"
                f"Moves: {self.moves}\n\n"
                f"Continue playing to reach higher scores?\n"
                f"(Click No to start a new game)"
            )
            
            if not result:
                self.start_new_game()
        except Exception:
            # Fallback if messagebox fails
            print(f"You won! Score: {self.score}, Moves: {self.moves}")
        
    def game_over(self):
        self.game_active = False
        try:
            result = messagebox.askyesno(
                "Game Over",
                f"🎮 No more moves possible!\n\n"
                f"Final Score: {self.score}\n"
                f"Moves: {self.moves}\n"
                f"Best Score: {self.best_score}\n\n"
                f"Start a new game?"
            )
            
            if result:
                self.start_new_game()
        except Exception:
            # Fallback if messagebox fails
            print(f"Game Over! Score: {self.score}, Best: {self.best_score}")
            
    def cleanup(self):
        """Clean up event handlers and resources"""
        self.game_active = False
        try:
            self.parent.unbind('<Key>')
        except:
            pass
        
    def return_to_menu(self):
        self.cleanup()
        try:
            # Import here to avoid circular imports
            from ui.main_menu import MainMenu
            main_menu = MainMenu(self.parent)
            main_menu.create_main_menu()
        except ImportError:
            # Fallback if main menu import fails
            print("Returning to main menu...")
            for widget in self.parent.winfo_children():
                widget.destroy()

# Additional utility function for standalone testing
def test_number_puzzle():
    """Test function to run the 2048 game standalone"""
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()
    root.title("2048 Puzzle Test")
    root.geometry("600x800")
    
    game = NumberPuzzleGame(root)
    game.create_game_window()
    
    root.mainloop()

if __name__ == "__main__":
    test_number_puzzle()