"""
Snake Game - games/snake_game.py
Classic snake game with modern UI and power-ups
"""

import customtkinter as ctk
import random
from tkinter import Canvas
from typing import Callable, List, Tuple
import math


class SnakeGame:
    def __init__(self, parent_frame: ctk.CTkFrame, return_callback: Callable = None):
        self.parent_frame = parent_frame
        self.move_callback_id = None
        self.return_callback = return_callback

        # Game settings
        self.cell_size = 20
        self.grid_width = 25
        self.grid_height = 20
        self.canvas_width = self.grid_width * self.cell_size
        self.canvas_height = self.grid_height * self.cell_size

        # Game state
        self.snake = [(12, 10), (11, 10), (10, 10)]  # Start in middle
        self.direction = "Right"
        self.next_direction = "Right"
        self.food = self.generate_food()
        self.power_ups = []
        self.score = 0
        self.high_score = 0
        self.game_running = False
        self.game_paused = False
        self.speed = 150  # milliseconds between moves
        self.level = 1

        # Power-up types
        self.power_up_types = {
            "speed_boost": {"color": "#00ffff", "points": 20, "effect": "speed"},
            "score_multiplier": {
                "color": "#ff00ff",
                "points": 30,
                "effect": "double_score",
            },
            "extra_food": {"color": "#ffff00", "points": 15, "effect": "extra_food"},
        }

        # Active effects
        self.active_effects = {"speed_boost": 0, "double_score": 0}

        # Colors
        self.colors = {
            "bg_primary": "#0f0f23",
            "bg_secondary": "#1a1a2e",
            "snake_head": "#00ff88",
            "snake_body": "#00cc66",
            "food": "#ff6b6b",
            "wall": "#333333",
            "grid": "#2a2a2a",
            "text": "#ffffff",
            "accent": "#ffd700",
        }

        # UI elements
        self.current_widgets = []
        self.canvas = None
        self.info_frame = None

        self.setup_game()

    def setup_game(self):
        """Initialize the game UI"""
        self.create_game_ui()
        self.draw_game()
        self.bind_keys()

    def create_game_ui(self):
        """Create the game interface"""
        # Clear existing widgets
        self.clear_widgets()

        # Main container
        self.main_frame = ctk.CTkFrame(
            self.parent_frame, fg_color=self.colors["bg_primary"], corner_radius=20
        )
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title_label = ctk.CTkLabel(
            self.main_frame,
            text="🐍 SNAKE GAME 🐍",
            font=("Arial",32, "bold"),
            text_color=self.colors["accent"],
        )
        title_label.pack(pady=10)

        # Info frame
        self.info_frame = ctk.CTkFrame(
            self.main_frame, fg_color=self.colors["bg_secondary"], corner_radius=15
        )
        self.info_frame.pack(fill="x", padx=20, pady=10)

        # Game stats
        stats_container = ctk.CTkFrame(self.info_frame, fg_color="transparent")
        stats_container.pack(fill="x", pady=10)

        self.score_label = ctk.CTkLabel(
            stats_container,
            text=f"Score: {self.score}",
            font=("Arial",18, "bold"),
            text_color=self.colors["text"],
        )
        self.score_label.pack(side="left", padx=20)

        self.level_label = ctk.CTkLabel(
            stats_container,
            text=f"Level: {self.level}",
            font=("Arial",18, "bold"),
            text_color=self.colors["accent"],
        )
        self.level_label.pack(side="left", padx=20)

        self.high_score_label = ctk.CTkLabel(
            stats_container,
            text=f"High Score: {self.high_score}",
            font=("Arial",18, "bold"),
            text_color=self.colors["snake_head"],
        )
        self.high_score_label.pack(side="right", padx=20)

        # Game canvas
        self.canvas = Canvas(
            self.main_frame,
            width=self.canvas_width,
            height=self.canvas_height,
            bg=self.colors["bg_primary"],
            highlightthickness=2,
            highlightbackground=self.colors["accent"],
        )
        self.canvas.pack(pady=20)
        self.canvas.focus_set()  # Make sure canvas is ready for key input


        # Control buttons
        self.create_control_buttons()

        # Instructions
        self.create_instructions()

        self.current_widgets.extend([self.main_frame])
    def return_to_menu(self):
        if self.return_callback:
            self.return_callback()  # Call the function directly
    
    def create_control_buttons(self):
        """Create game control buttons"""
        controls_frame = ctk.CTkFrame(
            self.main_frame, fg_color=self.colors["bg_secondary"], corner_radius=15
        )
        controls_frame.pack(fill="x", padx=20, pady=10)

        button_container = ctk.CTkFrame(controls_frame, fg_color="transparent")
        button_container.pack(pady=15)

        # Start/Pause button
        self.start_pause_btn = ctk.CTkButton(
            button_container,
            text="🎮 START GAME",
            width=150,
            height=45,
            font=("Arial",16, "bold"),
            fg_color=self.colors["snake_head"],
            hover_color="#00aa55",
            command=self.toggle_game,
        )
        self.start_pause_btn.pack(side="left", padx=10)

        # Restart button
        self.restart_btn = ctk.CTkButton(
            button_container,
            text="🔄 RESTART",
            width=150,
            height=45,
            font=("Arial",16, "bold"),
            fg_color=self.colors["accent"],
            hover_color="#ccaa00",
            command=self.restart_game,
        )
        self.restart_btn.pack(side="left", padx=10)

        # Exit button
        exit_btn = ctk.CTkButton(
            button_container,
            text="🚪 EXIT",
            width=150,
            height=45,
            font=("Arial",16, "bold"),
            fg_color="#ff6b6b",
            hover_color="#cc5555",
            command=self.exit_game,
        )
        exit_btn.pack(side="left", padx=10)

    def create_instructions(self):
        """Create game instructions"""
        instructions_frame = ctk.CTkFrame(
            self.main_frame, fg_color=self.colors["bg_secondary"], corner_radius=15
        )
        instructions_frame.pack(fill="x", padx=20, pady=(0, 20))

        instructions_title = ctk.CTkLabel(
            instructions_frame,
            text="🎯 HOW TO PLAY",
            font=("Arial",16, "bold"),
            text_color=self.colors["accent"],
        )
        instructions_title.pack(pady=(10, 5))

        instructions_text = """
        🔸 Use ARROW KEYS or WASD to control the snake
        🔸 Eat red food to grow and increase score
        🔸 Collect power-ups for special effects:
           💙 Speed Boost  💜 Score Multiplier  💛 Extra Food
        🔸 Avoid hitting walls or yourself
        🔸 Press SPACE to pause/unpause
        """

        instructions_label = ctk.CTkLabel(
            instructions_frame,
            text=instructions_text,
            font=("Arial", 12),
            text_color=self.colors["text"],
            justify="left",
        )
        instructions_label.pack(pady=(0, 15))

    def bind_keys(self):
        """Bind keyboard controls"""
        self.canvas.focus_set()  # Ensure canvas gets keyboard focus
        self.canvas.bind("<Key>", self.on_key_press)  # Bind keys to canvas
        self.canvas.bind("<Button-1>", lambda e: self.canvas.focus_set())  # Refocus on click


    def on_key_press(self, event):
        """Handle keyboard input"""
        key = event.keysym.lower()

        # Movement keys
        if key in ["up", "w"] and self.direction != "Down":
            self.next_direction = "Up"
        elif key in ["down", "s"] and self.direction != "Up":
            self.next_direction = "Down"
        elif key in ["left", "a"] and self.direction != "Right":
            self.next_direction = "Left"
        elif key in ["right", "d"] and self.direction != "Left":
            self.next_direction = "Right"
        elif key == "space":
            self.toggle_pause()

    def generate_food(self) -> Tuple[int, int]:
        """Generate random food position"""
        while True:
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            if (x, y) not in self.snake:
                return (x, y)

    def generate_power_up(self):
        """Generate random power-up"""
        if random.random() < 0.15 and len(self.power_ups) < 2:  # 15% chance
            while True:
                x = random.randint(0, self.grid_width - 1)
                y = random.randint(0, self.grid_height - 1)
                if (x, y) not in self.snake and (x, y) != self.food:
                    power_type = random.choice(list(self.power_up_types.keys()))
                    self.power_ups.append(
                        {
                            "pos": (x, y),
                            "type": power_type,
                            "timer": 200,  # Disappears after 200 game ticks
                        }
                    )
                    break

    def update_power_ups(self):
        """Update power-up timers and effects"""
        # Update power-up timers
        self.power_ups = [pu for pu in self.power_ups if pu["timer"] > 0]
        for pu in self.power_ups:
            pu["timer"] -= 1

        # Update active effects
        for effect in self.active_effects:
            if self.active_effects[effect] > 0:
                self.active_effects[effect] -= 1

    def move_snake(self):
        """Move the snake and handle game logic"""
        if not self.game_running or self.game_paused:
            return

        # Update direction
        self.direction = self.next_direction

        # Calculate new head position
        head_x, head_y = self.snake[0]

        if self.direction == "Up":
            new_head = (head_x, head_y - 1)
        elif self.direction == "Down":
            new_head = (head_x, head_y + 1)
        elif self.direction == "Left":
            new_head = (head_x - 1, head_y)
        else:  # Right
            new_head = (head_x + 1, head_y)

        # Check wall collision
        if (
            new_head[0] < 0
            or new_head[0] >= self.grid_width
            or new_head[1] < 0
            or new_head[1] >= self.grid_height
        ):
            self.game_over()
            return

        # Check self collision
        if new_head in self.snake:
            self.game_over()
            return

        # Add new head
        self.snake.insert(0, new_head)

        # Check food collision
        ate_food = False
        if new_head == self.food:
            ate_food = True
            score_multiplier = 2 if self.active_effects["double_score"] > 0 else 1
            self.score += 10 * score_multiplier
            self.food = self.generate_food()

            # Level up every 100 points
            new_level = (self.score // 100) + 1
            if new_level > self.level:
                self.level = new_level
                self.speed = max(50, self.speed - 10)  # Increase speed

            self.update_score_display()

        # Check power-up collision
        for i, power_up in enumerate(self.power_ups):
            if new_head == power_up["pos"]:
                self.collect_power_up(power_up)
                self.power_ups.pop(i)
                break

        # Remove tail if no food eaten
        if not ate_food:
            self.snake.pop()

        # Update power-ups and generate new ones
        self.update_power_ups()
        self.generate_power_up()

        # Draw game
        self.draw_game()

        # Schedule next move
        current_speed = self.speed
        if self.active_effects["speed_boost"] > 0:
            current_speed = max(50, current_speed // 2)

        self.parent_frame.after(current_speed, self.move_snake)

    def collect_power_up(self, power_up):
        """Handle power-up collection"""
        power_type = power_up["type"]
        power_data = self.power_up_types[power_type]

        # Add points
        score_multiplier = 2 if self.active_effects["double_score"] > 0 else 1
        self.score += power_data["points"] * score_multiplier

        # Apply effect
        effect = power_data["effect"]
        if effect == "speed":
            self.active_effects["speed_boost"] = 100  # 100 ticks
        elif effect == "double_score":
            self.active_effects["double_score"] = 150  # 150 ticks
        elif effect == "extra_food":
            # Add extra food point
            self.score += 20 * score_multiplier

        self.update_score_display()

    def draw_game(self):
        """Draw the game state"""
        self.canvas.delete("all")

        # Draw grid
        for i in range(self.grid_width + 1):
            x = i * self.cell_size
            self.canvas.create_line(
                x, 0, x, self.canvas_height, fill=self.colors["grid"], width=1
            )

        for i in range(self.grid_height + 1):
            y = i * self.cell_size
            self.canvas.create_line(
                0, y, self.canvas_width, y, fill=self.colors["grid"], width=1
            )

        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            x1, y1 = x * self.cell_size, y * self.cell_size
            x2, y2 = x1 + self.cell_size, y1 + self.cell_size

            if i == 0:  # Head
                self.canvas.create_oval(
                    x1 + 2,
                    y1 + 2,
                    x2 - 2,
                    y2 - 2,
                    fill=self.colors["snake_head"],
                    outline=self.colors["text"],
                    width=2,
                )
                # Eyes
                eye_size = 3
                self.canvas.create_oval(
                    x1 + 5, y1 + 5, x1 + 5 + eye_size, y1 + 5 + eye_size, fill="white"
                )
                self.canvas.create_oval(
                    x2 - 8, y1 + 5, x2 - 8 + eye_size, y1 + 5 + eye_size, fill="white"
                )
            else:  # Body
                self.canvas.create_rectangle(
                    x1 + 1,
                    y1 + 1,
                    x2 - 1,
                    y2 - 1,
                    fill=self.colors["snake_body"],
                    outline=self.colors["snake_head"],
                    width=1,
                )

        # Draw food
        fx, fy = self.food
        fx1, fy1 = fx * self.cell_size, fy * self.cell_size
        fx2, fy2 = fx1 + self.cell_size, fy1 + self.cell_size
        self.canvas.create_oval(
            fx1 + 2,
            fy1 + 2,
            fx2 - 2,
            fy2 - 2,
            fill=self.colors["food"],
            outline="darkred",
            width=2,
        )

        # Draw power-ups
        for power_up in self.power_ups:
            px, py = power_up["pos"]
            px1, py1 = px * self.cell_size, py * self.cell_size
            px2, py2 = px1 + self.cell_size, py1 + self.cell_size

            color = self.power_up_types[power_up["type"]]["color"]
            self.canvas.create_rectangle(
                px1 + 3, py1 + 3, px2 - 3, py2 - 3, fill=color, outline="white", width=2
            )

            # Add symbol
            symbol = (
                "⚡"
                if power_up["type"] == "speed_boost"
                else "💎" if power_up["type"] == "score_multiplier" else "🍎"
            )
            self.canvas.create_text(
                px1 + self.cell_size // 2,
                py1 + self.cell_size // 2,
                text=symbol,
                fill="white",
                font=("Arial", 8),
            )

        # Draw active effects indicator
        if any(self.active_effects.values()):
            effects_text = []
            if self.active_effects["speed_boost"] > 0:
                effects_text.append("⚡ Speed Boost")
            if self.active_effects["double_score"] > 0:
                effects_text.append("💎 Double Score")

            if effects_text:
                self.canvas.create_text(
                    10,
                    10,
                    text=" | ".join(effects_text),
                    fill=self.colors["accent"],
                    font=("Arial", 10),
                    anchor="nw",
                )

    def update_score_display(self):
        """Update score display"""
        self.score_label.configure(text=f"Score: {self.score}")
        self.level_label.configure(text=f"Level: {self.level}")
        if self.score > self.high_score:
            self.high_score = self.score
            self.high_score_label.configure(text=f"High Score: {self.high_score}")

    def toggle_game(self):
        """Start or pause the game"""
        if not self.game_running:
            self.start_game()
        else:
            self.toggle_pause()

    def start_game(self):
        """Start the game"""
        self.game_running = True
        self.game_paused = False
        self.start_pause_btn.configure(text="⏸️ PAUSE")
        self.move_snake()

    def toggle_pause(self):
        """Toggle pause state"""
        if self.game_running:
            self.game_paused = not self.game_paused
            if self.game_paused:
                self.start_pause_btn.configure(text="▶️ RESUME")
                # Draw pause message
                self.canvas.create_text(
                    self.canvas_width // 2,
                    self.canvas_height // 2,
                    text="PAUSED\nPress SPACE to resume",
                    fill=self.colors["accent"],
                    font=("Arial", 20, "bold"),
                    justify="center",
                    tags="pause",
                )
            else:
                self.start_pause_btn.configure(text="⏸️ PAUSE")
                self.canvas.delete("pause")
                self.move_snake()

    def game_over(self):
        """Handle game over"""
        self.game_running = False
        self.game_paused = False
        self.start_pause_btn.configure(text="🎮 START GAME")

        # Draw game over message
        self.canvas.create_text(
            self.canvas_width // 2,
            self.canvas_height // 2,
            text=f"GAME OVER!\nScore: {self.score}\nPress RESTART to play again",
            fill=self.colors["food"],
            font=("Arial", 16, "bold"),
            justify="center",
            tags="game_over",
        )

    def restart_game(self):
        """Restart the game"""
        self.snake = [(12, 10), (11, 10), (10, 10)]
        self.direction = "Right"
        self.next_direction = "Right"
        self.food = self.generate_food()
        self.power_ups = []
        self.score = 0
        self.level = 1
        self.speed = 150
        self.game_running = False
        self.game_paused = False
        self.active_effects = {"speed_boost": 0, "double_score": 0}

        self.start_pause_btn.configure(text="🎮 START GAME")
        self.update_score_display()
        self.draw_game()

    def exit_game(self):
        """Exit to main menu"""
        self.game_running = False

        # Cancel scheduled movement if any
        if self.move_callback_id:
            self.parent_frame.after_cancel(self.move_callback_id)
            self.move_callback_id = None

        self.clear_widgets()
        if self.return_callback:
            self.return_callback()


    def clear_widgets(self):
        """Clear all widgets"""
        for widget in self.current_widgets:
            widget.destroy()
        self.current_widgets.clear()


def start_snake_game(parent_frame: ctk.CTkFrame, return_callback: Callable = None):
    """
    Entry point function to start the snake game
    """
    return SnakeGame(parent_frame, return_callback)
