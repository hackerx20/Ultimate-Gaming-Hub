import customtkinter as ctk
import random
import time
from tkinter import messagebox
from tkinter import Canvas
import tkinter


class TetrisGame:
    def __init__(self, parent):
        self.parent = parent
        self.canvas = None
        self.game_active = False
        self.paused = False
        self.game_loop_job = None  # Track the game loop job for cleanup

        # Game settings
        self.BOARD_WIDTH = 10
        self.BOARD_HEIGHT = 20
        self.CELL_SIZE = 30
        self.fall_time = 500  # milliseconds

        # Game state
        self.board = [
            [0 for _ in range(self.BOARD_WIDTH)] for _ in range(self.BOARD_HEIGHT)
        ]
        self.current_piece = None
        self.current_x = 0
        self.current_y = 0
        self.next_piece = None

        # Score tracking
        self.score = 0
        self.lines_cleared = 0
        self.level = 1

        # Tetris pieces (tetrominoes)
        self.pieces = {
            "I": [
                [".....", "..#..", "..#..", "..#..", "..#.."],
                [".....", ".....", "####.", ".....", "....."],
            ],
            "O": [[".....", ".....", ".##..", ".##..", "....."]],
            "T": [
                [".....", ".....", ".#...", "###..", "....."],
                [".....", ".....", ".#...", ".##..", ".#..."],
                [".....", ".....", ".....", "###..", ".#..."],
                [".....", ".....", ".#...", "##...", ".#..."],
            ],
            "S": [
                [".....", ".....", ".##..", "##...", "....."],
                [".....", ".#...", ".##..", "..#..", "....."],
            ],
            "Z": [
                [".....", ".....", "##...", ".##..", "....."],
                [".....", "..#..", ".##..", ".#...", "....."],
            ],
            "J": [
                [".....", ".#...", ".#...", "##...", "....."],
                [".....", ".....", "#....", "###..", "....."],
                [".....", ".##..", ".#...", ".#...", "....."],
                [".....", ".....", "###..", "..#..", "....."],
            ],
            "L": [
                [".....", "..#..", "..#..", ".##..", "....."],
                [".....", ".....", "###..", "#....", "....."],
                [".....", "##...", ".#...", ".#...", "....."],
                [".....", ".....", "..#..", "###..", "....."],
            ],
        }

        # Colors for pieces
        self.colors = {
            "I": "#00f5ff",
            "O": "#ffd700",
            "T": "#9400d3",
            "S": "#00ff00",
            "Z": "#ff0000",
            "J": "#0000ff",
            "L": "#ff8c00",
        }

        self.current_rotation = 0

    def create_game_window(self):
        # Clear parent and cleanup any existing timers
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
            text="🧩 Tetris",
            font=("Arial", 28, "bold"),
            text_color="#ffd700",
        )
        title_label.pack(side="left", padx=20, pady=20)

        # Controls
        controls_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        controls_frame.pack(side="right", padx=20, pady=20)

        self.pause_btn = ctk.CTkButton(
            controls_frame,
            text="Pause",
            command=self.toggle_pause,
            width=80,
            height=35,
            fg_color="#ffd700",
            hover_color="#ffcc00",
            text_color="#000000",
        )
        self.pause_btn.pack(side="left", padx=(0, 10))

        new_game_btn = ctk.CTkButton(
            controls_frame,
            text="New Game",
            command=self.start_new_game,
            width=100,
            height=35,
            fg_color="#00ff88",
            hover_color="#00cc6a",
        )
        new_game_btn.pack(side="left")

        # Game container
        game_container = ctk.CTkFrame(main_container, fg_color="transparent")
        game_container.pack(fill="both", expand=True)

        # Left panel - Game board
        game_panel = ctk.CTkFrame(game_container, fg_color="#0f0f23")
        game_panel.pack(side="left", fill="both", expand=True, padx=(0, 20))

        # Canvas for game
        canvas_width = self.BOARD_WIDTH * self.CELL_SIZE
        canvas_height = self.BOARD_HEIGHT * self.CELL_SIZE

        self.canvas = Canvas(
            game_panel,
            width=canvas_width,
            height=canvas_height,
            bg="#000000",
            highlightthickness=2,
            highlightbackground="#ffd700",
        )
        self.canvas.pack(padx=20, pady=20)

        # Right panel - Stats and next piece
        stats_panel = ctk.CTkFrame(game_container, width=200, fg_color="#16213e")
        stats_panel.pack(side="right", fill="y")
        stats_panel.pack_propagate(False)

        # Stats labels
        stats_title = ctk.CTkLabel(
            stats_panel,
            text="STATISTICS",
            font=("Arial", 18, "bold"),
            text_color="#ffd700",
        )
        stats_title.pack(pady=(20, 10))

        self.score_label = ctk.CTkLabel(
            stats_panel, text="Score: 0", font=("Arial", 16, "bold")
        )
        self.score_label.pack(pady=5)

        self.lines_label = ctk.CTkLabel(
            stats_panel, text="Lines: 0", font=("Arial", 16, "bold")
        )
        self.lines_label.pack(pady=5)

        self.level_label = ctk.CTkLabel(
            stats_panel, text="Level: 1", font=("Arial", 16, "bold")
        )
        self.level_label.pack(pady=5)

        # Next piece preview
        next_title = ctk.CTkLabel(
            stats_panel,
            text="NEXT PIECE",
            font=("Arial", 18, "bold"),
            text_color="#ffd700",
        )
        next_title.pack(pady=(30, 10))

        self.next_canvas = Canvas(
            stats_panel,
            width=120,
            height=120,
            bg="#000000",
            highlightthickness=1,
            highlightbackground="#ffd700",
        )
        self.next_canvas.pack(pady=10)

        # Controls info
        controls_title = ctk.CTkLabel(
            stats_panel,
            text="CONTROLS",
            font=("Arial", 18, "bold"),
            text_color="#ffd700",
        )
        controls_title.pack(pady=(30, 10))

        controls_text = """← → : Move
↓ : Soft Drop
↑ : Rotate
Space : Hard Drop
P : Pause"""

        controls_info = ctk.CTkLabel(
            stats_panel, text=controls_text, font=("Arial", 12), justify="left"
        )
        controls_info.pack(pady=10)

        # Back button
        back_btn = ctk.CTkButton(
            main_container,
            text="← Back to Menu",
            command=self.back_to_menu,
            width=150,
            height=40,
            fg_color="#ff6b6b",
            hover_color="#ff5252",
        )
        back_btn.pack(pady=20)

        # Bind keys
        self.parent.bind("<Key>", self.handle_keypress)
        self.parent.focus_set()

        # Start game
        self.start_new_game()

    def start_new_game(self):
        # Cleanup any existing game loop
        self.cleanup()
        
        self.game_active = True
        self.paused = False
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.fall_time = 500

        # Clear board
        self.board = [
            [0 for _ in range(self.BOARD_WIDTH)] for _ in range(self.BOARD_HEIGHT)
        ]

        # Generate first pieces
        self.next_piece = random.choice(list(self.pieces.keys()))
        self.spawn_piece()

        self.update_display()
        self.game_loop()

    def spawn_piece(self):
        self.current_piece = self.next_piece
        self.next_piece = random.choice(list(self.pieces.keys()))
        self.current_rotation = 0
        self.current_x = self.BOARD_WIDTH // 2 - 2
        self.current_y = 0

        # Check for game over
        if self.check_collision():
            self.game_over()
            return

        self.draw_next_piece()

    def check_collision(self, dx=0, dy=0, rotation=None):
        if rotation is None:
            rotation = self.current_rotation

        if not self.current_piece:
            return True

        piece_shape = self.pieces[self.current_piece][
            rotation % len(self.pieces[self.current_piece])
        ]

        for y, row in enumerate(piece_shape):
            for x, cell in enumerate(row):
                if cell == "#":
                    new_x = self.current_x + x + dx
                    new_y = self.current_y + y + dy

                    # Check boundaries
                    if (
                        new_x < 0
                        or new_x >= self.BOARD_WIDTH
                        or new_y >= self.BOARD_HEIGHT
                    ):
                        return True

                    # Check collision with placed pieces
                    if new_y >= 0 and self.board[new_y][new_x]:
                        return True

        return False

    def place_piece(self):
        if not self.current_piece:
            return
            
        piece_shape = self.pieces[self.current_piece][
            self.current_rotation % len(self.pieces[self.current_piece])
        ]

        for y, row in enumerate(piece_shape):
            for x, cell in enumerate(row):
                if cell == "#":
                    board_x = self.current_x + x
                    board_y = self.current_y + y
                    if board_y >= 0:
                        self.board[board_y][board_x] = self.current_piece

        self.clear_lines()
        self.spawn_piece()

    def clear_lines(self):
        lines_to_clear = []

        for y in range(self.BOARD_HEIGHT):
            if all(self.board[y]):
                lines_to_clear.append(y)

        for y in lines_to_clear:
            del self.board[y]
            self.board.insert(0, [0 for _ in range(self.BOARD_WIDTH)])

        if lines_to_clear:
            lines_count = len(lines_to_clear)
            self.lines_cleared += lines_count

            # Scoring
            line_scores = {1: 100, 2: 300, 3: 500, 4: 800}
            self.score += line_scores.get(lines_count, 0) * self.level

            # Level progression
            self.level = self.lines_cleared // 10 + 1
            self.fall_time = max(50, 500 - (self.level - 1) * 50)

    def handle_keypress(self, event):
        if not self.game_active or self.paused:
            if event.keysym in ("p", "P"):
                self.toggle_pause()
            return

        key = event.keysym

        if key == "Left":
            if not self.check_collision(dx=-1):
                self.current_x -= 1
        elif key == "Right":
            if not self.check_collision(dx=1):
                self.current_x += 1
        elif key == "Down":
            if not self.check_collision(dy=1):
                self.current_y += 1
        elif key == "Up":
            new_rotation = (self.current_rotation + 1) % len(
                self.pieces[self.current_piece]
            )
            if not self.check_collision(rotation=new_rotation):
                self.current_rotation = new_rotation
        elif key == "space":
            while not self.check_collision(dy=1):
                self.current_y += 1
            self.place_piece()
        elif key == "p" or key == "P":
            self.toggle_pause()

        self.update_display()

    def toggle_pause(self):
        self.paused = not self.paused
        if hasattr(self, 'pause_btn') and self.pause_btn.winfo_exists():
            self.pause_btn.configure(text="Resume" if self.paused else "Pause")
        if not self.paused and self.game_active:
            self.game_loop()

    def game_loop(self):
        if not self.game_active or self.paused:
            return

        # Cancel any existing game loop job
        if self.game_loop_job:
            try:
                self.parent.after_cancel(self.game_loop_job)
            except:
                pass

        if not self.check_collision(dy=1):
            self.current_y += 1
        else:
            self.place_piece()

        self.update_display()
        
        if self.game_active:
            self.game_loop_job = self.parent.after(self.fall_time, self.game_loop)

    def update_display(self):
        if not self.canvas or not self.canvas.winfo_exists():
            return
            
        self.canvas.delete("all")

        # Draw placed pieces
        for y in range(self.BOARD_HEIGHT):
            for x in range(self.BOARD_WIDTH):
                if self.board[y][x]:
                    color = self.colors.get(self.board[y][x], "#ffffff")
                    self.draw_cell(x, y, color)

        # Draw current piece
        if self.current_piece:
            piece_shape = self.pieces[self.current_piece][
                self.current_rotation % len(self.pieces[self.current_piece])
            ]
            color = self.colors[self.current_piece]

            for y, row in enumerate(piece_shape):
                for x, cell in enumerate(row):
                    if cell == "#":
                        screen_x = self.current_x + x
                        screen_y = self.current_y + y
                        if screen_y >= 0:
                            self.draw_cell(screen_x, screen_y, color)

        # Update stats
        try:
            if hasattr(self, 'score_label') and self.score_label.winfo_exists():
                self.score_label.configure(text=f"Score: {self.score}")
            if hasattr(self, 'lines_label') and self.lines_label.winfo_exists():
                self.lines_label.configure(text=f"Lines: {self.lines_cleared}")
            if hasattr(self, 'level_label') and self.level_label.winfo_exists():
                self.level_label.configure(text=f"Level: {self.level}")
        except tkinter.TclError:
            pass

    def draw_cell(self, x, y, color):
        if not self.canvas or not self.canvas.winfo_exists():
            return
            
        x1 = x * self.CELL_SIZE
        y1 = y * self.CELL_SIZE
        x2 = x1 + self.CELL_SIZE
        y2 = y1 + self.CELL_SIZE

        self.canvas.create_rectangle(
            x1, y1, x2, y2, fill=color, outline="#ffffff", width=1
        )

    def draw_next_piece(self):
        if not hasattr(self, 'next_canvas') or not self.next_canvas.winfo_exists():
            return
            
        self.next_canvas.delete("all")

        if self.next_piece:
            piece_shape = self.pieces[self.next_piece][0]
            color = self.colors[self.next_piece]
            cell_size = 20

            for y, row in enumerate(piece_shape):
                for x, cell in enumerate(row):
                    if cell == "#":
                        x1 = x * cell_size + 10
                        y1 = y * cell_size + 10
                        x2 = x1 + cell_size
                        y2 = y1 + cell_size

                        self.next_canvas.create_rectangle(
                            x1, y1, x2, y2, fill=color, outline="#ffffff", width=1
                        )

    def game_over(self):
        self.game_active = False
        try:
            messagebox.showinfo(
                "Game Over",
                f"🎮 Game Over!\n\n"
                f"Final Score: {self.score}\n"
                f"Lines Cleared: {self.lines_cleared}\n"
                f"Level Reached: {self.level}",
            )
        except Exception:
            print(f"Game Over! Score: {self.score}, Lines: {self.lines_cleared}, Level: {self.level}")

    def cleanup(self):
        """Clean up timers and resources"""
        self.game_active = False
        if self.game_loop_job:
            try:
                self.parent.after_cancel(self.game_loop_job)
            except:
                pass
            self.game_loop_job = None

    def back_to_menu(self):
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
def test_tetris_game():
    """Test function to run the tetris game standalone"""
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()
    root.title("Tetris Game Test")
    root.geometry("800x700")
    
    game = TetrisGame(root)
    game.create_game_window()
    
    root.mainloop()

if __name__ == "__main__":
    test_tetris_game()