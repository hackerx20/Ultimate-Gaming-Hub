"""
Enhanced Quiz Game (KBC Style) - FIXED TIMER VERSION
The key fix: Use threading.Timer instead of tkinter.after() for proper cancellation
"""

import customtkinter as ctk
import random
import time
import threading
from typing import Callable, List, Dict, Any


class QuizGame:
    def __init__(
        self,
        parent_frame: ctk.CTkFrame,
        questions: List[str],
        options: List[List[str]],
        correct_answers: List[str],
        return_callback: Callable = None,
    ):
        self.parent_frame = parent_frame
        self.questions = questions
        self.options = options
        self.correct_answers = correct_answers
        self.return_callback = return_callback

        # Game state
        self.current_question_index = 0
        self.score = 0
        self.total_questions = 10
        self.time_remaining = 30
        self.timer_running = False
        self.game_over = False
        self.selected_questions = []
        
        # CRITICAL FIX: Use threading.Timer instead of tkinter.after()
        self.is_cleaned_up = False
        self.timer_object = None  # Will store the threading.Timer object
        self.timer_lock = threading.Lock()  # Thread safety

        # Lifelines
        self.lifelines = {"fifty_fifty": True, "skip": True, "extra_time": True}

        # UI elements
        self.current_widgets = []
        self.timer_label = None
        self.progress_bar = None

        # Colors and styling
        self.colors = {
            "bg_primary": "#0f0f23",
            "bg_secondary": "#1a1a2e",
            "accent_gold": "#ffd700",
            "accent_blue": "#00d4ff",
            "success": "#00ff88",
            "danger": "#ff6b6b",
            "text_primary": "#ffffff",
            "text_secondary": "#cccccc",
            "button_hover": "#ffcc00",
        }

        self.setup_game()

    def setup_game(self):
        """Initialize game setup"""
        # Select random questions
        available_indices = list(range(len(self.questions)))
        self.selected_questions = random.sample(
            available_indices, min(self.total_questions, len(available_indices))
        )

        self.create_game_ui()
        self.start_game()

    def create_game_ui(self):
        """Create the main game interface"""
        # Clear existing widgets
        self.clear_widgets()

        # Main container with gradient effect
        self.main_frame = ctk.CTkFrame(
            self.parent_frame, fg_color=self.colors["bg_primary"], corner_radius=20
        )
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header section
        self.create_header()

        # Question section
        self.create_question_section()

        # Options section
        self.create_options_section()

        # Lifelines section
        self.create_lifelines_section()

        # Progress section
        self.create_progress_section()

        self.current_widgets.append(self.main_frame)

    def create_header(self):
        """Create game header with title and stats"""
        header_frame = ctk.CTkFrame(
            self.main_frame, fg_color=self.colors["bg_secondary"], corner_radius=15
        )
        header_frame.pack(fill="x", padx=20, pady=(20, 10))

        # Game title
        title_label = ctk.CTkLabel(
            header_frame,
            text="🏆 KAUN BANEGA CROREPATI 🏆",
            font=("Arial", 32, "bold"),
            text_color=self.colors["accent_gold"],
        )
        title_label.pack(pady=15)

        # Stats row
        stats_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        stats_frame.pack(fill="x", padx=20, pady=(0, 15))

        # Score
        self.score_label = ctk.CTkLabel(
            stats_frame,
            text=f"💰 Score: {self.score}",
            font=("Arial", 20, "bold"),
            text_color=self.colors["success"],
        )
        self.score_label.pack(side="left")

        # Timer
        self.timer_label = ctk.CTkLabel(
            stats_frame,
            text=f"⏰ Time: {self.time_remaining}s",
            font=("Arial", 20, "bold"),
            text_color=self.colors["danger"],
        )
        self.timer_label.pack(side="right")

        # Question counter
        self.question_counter = ctk.CTkLabel(
            stats_frame,
            text=f"Question {self.current_question_index + 1}/{self.total_questions}",
            font=("Arial", 18),
            text_color=self.colors["text_secondary"],
        )
        self.question_counter.pack()

    def create_question_section(self):
        """Create question display section"""
        self.question_frame = ctk.CTkFrame(
            self.main_frame, fg_color=self.colors["bg_secondary"], corner_radius=15
        )
        self.question_frame.pack(fill="x", padx=20, pady=10)

        self.question_label = ctk.CTkLabel(
            self.question_frame,
            text="",
            font=("Arial", 24, "bold"),
            text_color=self.colors["text_primary"],
            wraplength=600,
            justify="center",
        )
        self.question_label.pack(pady=30)

    def create_options_section(self):
        """Create options buttons section"""
        options_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        options_container.pack(fill="x", padx=20, pady=10)

        # Create 2x2 grid for options
        self.option_buttons = []
        positions = [(0, 0), (0, 1), (1, 0), (1, 1)]
        prefixes = ["A)", "B)", "C)", "D)"]

        for i in range(4):
            row, col = positions[i]

            btn = ctk.CTkButton(
                options_container,
                text="",
                font=("Arial", 18, "bold"),
                fg_color=self.colors["bg_secondary"],
                hover_color=self.colors["button_hover"],
                border_width=3,
                border_color=self.colors["accent_blue"],
                corner_radius=15,
                height=80,
                command=lambda idx=i: self.select_answer(idx),
            )

            btn.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
            self.option_buttons.append(btn)

        # Configure grid weights
        options_container.grid_columnconfigure(0, weight=1)
        options_container.grid_columnconfigure(1, weight=1)

    def create_lifelines_section(self):
        """Create lifelines buttons"""
        lifelines_frame = ctk.CTkFrame(
            self.main_frame, fg_color=self.colors["bg_secondary"], corner_radius=15
        )
        lifelines_frame.pack(fill="x", padx=20, pady=10)

        lifelines_title = ctk.CTkLabel(
            lifelines_frame,
            text="🎯 LIFELINES",
            font=("Arial", 16, "bold"),
            text_color=self.colors["accent_gold"],
        )
        lifelines_title.pack(pady=(10, 5))

        lifelines_container = ctk.CTkFrame(lifelines_frame, fg_color="transparent")
        lifelines_container.pack(pady=(0, 10))

        # Fifty-Fifty
        self.fifty_fifty_btn = ctk.CTkButton(
            lifelines_container,
            text="50:50",
            width=100,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color=self.colors["accent_blue"],
            hover_color=self.colors["button_hover"],
            command=self.use_fifty_fifty,
        )
        self.fifty_fifty_btn.pack(side="left", padx=5)

        # Skip Question
        self.skip_btn = ctk.CTkButton(
            lifelines_container,
            text="SKIP",
            width=100,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color=self.colors["success"],
            hover_color=self.colors["button_hover"],
            command=self.skip_question,
        )
        self.skip_btn.pack(side="left", padx=5)

        # Extra Time
        self.extra_time_btn = ctk.CTkButton(
            lifelines_container,
            text="+TIME",
            width=100,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color=self.colors["danger"],
            hover_color=self.colors["button_hover"],
            command=self.add_extra_time,
        )
        self.extra_time_btn.pack(side="left", padx=5)

    def create_progress_section(self):
        """Create progress bar and navigation"""
        progress_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        progress_frame.pack(fill="x", padx=20, pady=10)

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            progress_frame, height=20, progress_color=self.colors["accent_gold"]
        )
        self.progress_bar.pack(fill="x", pady=(0, 10))
        self.progress_bar.set(0)

        # Navigation buttons
        nav_frame = ctk.CTkFrame(progress_frame, fg_color="transparent")
        nav_frame.pack(fill="x")

        # Exit button
        exit_btn = ctk.CTkButton(
            nav_frame,
            text="🚪 EXIT GAME",
            width=150,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color=self.colors["danger"],
            hover_color="#cc5555",
            command=self.exit_game,
        )
        exit_btn.pack(side="left")

        # Next button (initially hidden)
        self.next_btn = ctk.CTkButton(
            nav_frame,
            text="NEXT QUESTION ➡️",
            width=200,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color=self.colors["success"],
            hover_color="#00cc77",
            command=self.next_question,
            state="disabled",
        )
        self.next_btn.pack(side="right")

    def start_game(self):
        """Start the quiz game"""
        self.display_question()
        self.start_timer()

    def display_question(self):
        """Display current question and options"""
        if self.current_question_index >= len(self.selected_questions):
            self.end_game()
            return

        # Get current question data
        q_index = self.selected_questions[self.current_question_index]
        question = self.questions[q_index]
        options = self.options[q_index]

        # Update UI
        self.question_label.configure(text=question)
        self.question_counter.configure(
            text=f"Question {self.current_question_index + 1}/{self.total_questions}"
        )

        # Update options
        prefixes = ["A)", "B)", "C)", "D)"]
        for i, (btn, option) in enumerate(zip(self.option_buttons, options)):
            btn.configure(
                text=f"{prefixes[i]} {option}",
                fg_color=self.colors["bg_secondary"],
                state="normal",
            )

        # Reset timer
        self.time_remaining = 30
        self.next_btn.configure(state="disabled")

        # Update progress
        progress = (self.current_question_index) / self.total_questions
        self.progress_bar.set(progress)

    # CRITICAL FIX: New timer implementation using threading.Timer
    def start_timer(self):
        """Start the countdown timer using threading.Timer for proper cleanup"""
        if not self.game_over and not self.is_cleaned_up:
            self.timer_running = True
            self.schedule_timer_update()

    def schedule_timer_update(self):
        """Schedule the next timer update using threading.Timer"""
        with self.timer_lock:
            if not self.timer_running or self.game_over or self.is_cleaned_up:
                return
            
            # Cancel any existing timer
            if self.timer_object and self.timer_object.is_alive():
                self.timer_object.cancel()
            
            # Create new timer for 1 second from now
            self.timer_object = threading.Timer(1.0, self.timer_tick)
            self.timer_object.daemon = True  # Dies when main thread dies
            self.timer_object.start()

    def timer_tick(self):
        """Timer tick handler - runs in separate thread"""
        with self.timer_lock:
            if not self.timer_running or self.game_over or self.is_cleaned_up:
                return
        
        try:
            # Check if parent frame still exists
            if not self.parent_frame.winfo_exists():
                self.stop_timer()
                return
        except:
            self.stop_timer()
            return

        if self.time_remaining > 0:
            # Use after_idle to safely update UI from timer thread
            try:
                self.parent_frame.after_idle(self.update_timer_display)
                self.time_remaining -= 1
                
                # Schedule next tick
                self.schedule_timer_update()
            except:
                self.stop_timer()
        else:
            # Time's up - handle timeout on main thread
            try:
                self.parent_frame.after_idle(self.timeout)
            except:
                self.stop_timer()

    def update_timer_display(self):
        """Update timer display on main thread"""
        if self.is_cleaned_up or not self.timer_running:
            return
            
        try:
            if self.timer_label and self.timer_label.winfo_exists():
                self.timer_label.configure(text=f"⏰ Time: {self.time_remaining}s")

                # Change color based on remaining time
                if self.time_remaining <= 10:
                    self.timer_label.configure(text_color=self.colors["danger"])
                elif self.time_remaining <= 20:
                    self.timer_label.configure(text_color=self.colors["button_hover"])
                else:
                    self.timer_label.configure(text_color=self.colors["text_secondary"])
        except:
            self.stop_timer()

    def stop_timer(self):
        """Stop the timer completely"""
        with self.timer_lock:
            self.timer_running = False
            if self.timer_object and self.timer_object.is_alive():
                self.timer_object.cancel()
                self.timer_object = None

    def select_answer(self, option_index: int):
        """Handle answer selection"""
        if self.game_over or self.is_cleaned_up:
            return

        self.stop_timer()  # Use the proper stop method

        # Get correct answer
        q_index = self.selected_questions[self.current_question_index]
        correct_answer = str(self.correct_answers[q_index]).strip()
        selected_option = str(self.options[q_index][option_index]).strip()
        is_correct = selected_option == correct_answer

        # Update button colors
        for i, btn in enumerate(self.option_buttons):
            if btn.winfo_exists():
                btn.configure(state="disabled")
                option_text = str(self.options[q_index][i]).strip()
                if option_text == correct_answer:
                    btn.configure(fg_color=self.colors["success"])
                elif i == option_index and not is_correct:
                    btn.configure(fg_color=self.colors["danger"])

        # Update score
        if is_correct:
            self.score += 10
            if self.score_label and self.score_label.winfo_exists():
                self.score_label.configure(text=f"💰 Score: {self.score}")

        # Enable next button
        if self.next_btn and self.next_btn.winfo_exists():
            self.next_btn.configure(state="normal")

    def next_question(self):
        """Move to next question"""
        if self.game_over or self.is_cleaned_up:
            return
            
        self.current_question_index += 1
        if self.current_question_index < self.total_questions:
            self.display_question()
            self.start_timer()
        else:
            self.end_game()

    def timeout(self):
        """Handle timer timeout"""
        if self.game_over or self.is_cleaned_up:
            return
            
        self.stop_timer()  # Use the proper stop method

        # Disable all buttons and show correct answer
        q_index = self.selected_questions[self.current_question_index]
        correct_answer = self.correct_answers[q_index]

        for i, btn in enumerate(self.option_buttons):
            if btn.winfo_exists():
                btn.configure(state="disabled")
                if self.options[q_index][i] == correct_answer:
                    btn.configure(fg_color=self.colors["success"])

        if self.next_btn and self.next_btn.winfo_exists():
            self.next_btn.configure(state="normal")

    def use_fifty_fifty(self):
        """Use fifty-fifty lifeline"""
        if not self.lifelines["fifty_fifty"] or self.game_over or self.is_cleaned_up:
            return

        self.lifelines["fifty_fifty"] = False
        if self.fifty_fifty_btn.winfo_exists():
            self.fifty_fifty_btn.configure(state="disabled", fg_color="gray")

        # Get correct answer and hide two wrong options
        q_index = self.selected_questions[self.current_question_index]
        correct_answer = str(self.correct_answers[q_index]).strip()
        options = [str(opt).strip() for opt in self.options[q_index]]

        if correct_answer not in options:
            print(f"[ERROR] Correct answer '{correct_answer}' not found in options: {options}")
            return

        correct_index = options.index(correct_answer)
        wrong_indices = [i for i in range(len(options)) if i != correct_index]
        to_hide = random.sample(wrong_indices, 2)

        for i in to_hide:
            if self.option_buttons[i].winfo_exists():
                self.option_buttons[i].configure(state="disabled", fg_color="gray")

    def skip_question(self):
        """Skip current question"""
        if not self.lifelines["skip"] or self.game_over or self.is_cleaned_up:
            return

        self.lifelines["skip"] = False
        if self.skip_btn.winfo_exists():
            self.skip_btn.configure(state="disabled", fg_color="gray")
        self.stop_timer()  # Use the proper stop method
        self.next_question()

    def add_extra_time(self):
        """Add extra time"""
        if not self.lifelines["extra_time"] or self.game_over or self.is_cleaned_up:
            return

        self.lifelines["extra_time"] = False
        if self.extra_time_btn.winfo_exists():
            self.extra_time_btn.configure(state="disabled", fg_color="gray")
        self.time_remaining += 15

    def end_game(self):
        """End the game and show results"""
        self.game_over = True
        self.stop_timer()  # Use the proper stop method

        # Clear current widgets
        self.clear_widgets()

        # Create results screen only if not cleaned up
        if not self.is_cleaned_up:
            self.create_results_screen()

    def create_results_screen(self):
        """Create game over results screen"""
        if self.is_cleaned_up:
            return
            
        results_frame = ctk.CTkFrame(
            self.parent_frame, fg_color=self.colors["bg_primary"], corner_radius=20
        )
        results_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title = ctk.CTkLabel(
            results_frame,
            text="🎉 GAME OVER! 🎉",
            font=("Arial", 36, "bold"),
            text_color=self.colors["accent_gold"],
        )
        title.pack(pady=30)

        # Score
        score_label = ctk.CTkLabel(
            results_frame,
            text=f"Final Score: {self.score} / {self.total_questions * 10}",
            font=("Arial", 28, "bold"),
            text_color=self.colors["success"],
        )
        score_label.pack(pady=20)

        # Performance message
        percentage = (self.score / (self.total_questions * 10)) * 100
        if percentage >= 80:
            message = "🏆 EXCELLENT! You're a Quiz Champion!"
            color = self.colors["success"]
        elif percentage >= 60:
            message = "👏 GOOD JOB! Well played!"
            color = self.colors["accent_blue"]
        elif percentage >= 40:
            message = "👍 NOT BAD! Keep practicing!"
            color = self.colors["button_hover"]
        else:
            message = "💪 KEEP TRYING! Practice makes perfect!"
            color = self.colors["danger"]

        message_label = ctk.CTkLabel(
            results_frame, text=message, font=("Arial", 20, "bold"), text_color=color
        )
        message_label.pack(pady=20)

        # Buttons
        buttons_frame = ctk.CTkFrame(results_frame, fg_color="transparent")
        buttons_frame.pack(pady=30)

        # Play Again
        play_again_btn = ctk.CTkButton(
            buttons_frame,
            text="🔄 PLAY AGAIN",
            width=200,
            height=50,
            font=("Arial", 16, "bold"),
            fg_color=self.colors["success"],
            hover_color="#00cc77",
            command=self.restart_game,
        )
        play_again_btn.pack(side="left", padx=10)

        # Main Menu
        menu_btn = ctk.CTkButton(
            buttons_frame,
            text="🏠 MAIN MENU",
            width=200,
            height=50,
            font=("Arial", 16, "bold"),
            fg_color=self.colors["accent_blue"],
            hover_color="#0099cc",
            command=self.exit_game,
        )
        menu_btn.pack(side="left", padx=10)

        self.current_widgets.append(results_frame)

    def restart_game(self):
        """Restart the game"""
        if self.is_cleaned_up:
            return
            
        self.stop_timer()  # Stop any running timer
        self.current_question_index = 0
        self.score = 0
        self.game_over = False
        self.timer_running = False
        self.lifelines = {"fifty_fifty": True, "skip": True, "extra_time": True}
        self.setup_game()

    def exit_game(self):
        """Exit to main menu with proper cleanup"""
        print("[QuizGame] Exit game called")
        self.cleanup()
        
        # Call return callback after cleanup
        if self.return_callback and not self.is_cleaned_up:
            try:
                self.return_callback()
            except Exception as e:
                print(f"[QuizGame] Error calling return callback: {e}")

    def cleanup(self):
        """Comprehensive cleanup method called by GameManager"""
        if self.is_cleaned_up:
            return
            
        print("[QuizGame] Starting cleanup...")
        
        # Set cleanup flag first to prevent any further operations
        self.is_cleaned_up = True
        
        # CRITICAL: Stop timer with proper cancellation
        self.stop_timer()
        
        # Stop all game operations
        self.game_over = True
        
        # Clear all UI widgets
        try:
            self.clear_widgets()
        except Exception as e:
            print(f"[QuizGame] Error clearing widgets during cleanup: {e}")
        
        # Clear references to UI elements
        self.timer_label = None
        self.progress_bar = None
        self.option_buttons = []
        self.question_label = None
        self.score_label = None
        self.question_counter = None
        
        print("[QuizGame] Cleanup completed")

    def clear_widgets(self):
        """Clear all current widgets safely"""
        for widget in self.current_widgets:
            try:
                if widget.winfo_exists():
                    widget.destroy()
            except Exception as e:
                print(f"[QuizGame] Error destroying widget: {e}")
        self.current_widgets.clear()

    # Add method to set return callback (for GameManager compatibility)
    def set_return_callback(self, callback: Callable):
        """Set the return callback function"""
        self.return_callback = callback


def start_quiz_game(parent_frame: ctk.CTkFrame, return_callback: Callable = None):
    """
    Entry point function to start the quiz game
    This function should be called from the main app
    """
    try:
        from data.Questions import questions
        from data.Options import options
        from data.CorrectAnswer import correct_answers
    except ImportError:
        # Fallback data if files don't exist
        questions = ["What is 2+2?", "What is the capital of France?"]
        options = [["3", "4", "5", "6"], ["London", "Paris", "Berlin", "Madrid"]]
        correct_answers = ["4", "Paris"]

    return QuizGame(parent_frame, questions, options, correct_answers, return_callback)