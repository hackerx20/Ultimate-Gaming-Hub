import json
import os
from datetime import datetime
import importlib
import sys
import customtkinter as ctk

class GameManager:
    def __init__(self, main_app):
        self.main_app = main_app
        self.current_game = None
        self.game_instances = {}
        self.game_states = {}
        self.current_game_frame = None  # Track the current game frame
        self.data_dir = "data"
        self.states_file = os.path.join(self.data_dir, "game_states.json")
        
        # Ensure data directory exists
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.session_data = {
            'games_played': 0,
            'total_time': 0,
            'session_start': datetime.now(),
            'achievements': []
        }
        
        # Game registry
        self.games = {
            'quiz': {
                'name': 'KBC Quiz',
                'description': 'Test your knowledge with challenging questions',
                'icon': '🧠',
                'module': 'games.quiz_game',
                'class': 'QuizGame',
                'category': 'Knowledge'
            },
            'snake': {
                'name': 'Snake Game',
                'description': 'Classic snake game with modern twists',
                'icon': '🐍',
                'module': 'games.snake_game',
                'class': 'SnakeGame',
                'category': 'Arcade'
            },
            'memory': {
                'name': 'Memory Match',
                'description': 'Match cards and test your memory',
                'icon': '🧩',
                'module': 'games.memory_game',
                'class': 'MemoryGame',
                'category': 'Puzzle'
            }
        }
        
        self.load_all_data()
    
    def load_quiz_data(self):
        """Load quiz data with error handling"""
        try:
            from data.CorrectAnswer import correct_answers
            from data.Questions import questions
            from data.Options import options
            return questions, options, correct_answers
        except ImportError as e:
            print(f"Warning: Could not load quiz data files: {e}")
            # Provide fallback quiz data
            fallback_questions = [
                "What is the capital of France?",
                "Which planet is known as the Red Planet?",
                "Who painted the Mona Lisa?",
                "What is the largest ocean on Earth?",
                "Which year did World War II end?"
            ]
            fallback_options = [
                ["London", "Berlin", "Paris", "Madrid"],
                ["Venus", "Mars", "Jupiter", "Saturn"],
                ["Van Gogh", "Picasso", "Leonardo da Vinci", "Monet"],
                ["Atlantic", "Pacific", "Indian", "Arctic"],
                ["1944", "1945", "1946", "1947"]
            ]
            fallback_correct = ["Paris", "Mars", "Leonardo da Vinci", "Pacific", "1945"]
            return fallback_questions, fallback_options, fallback_correct
    
    def load_all_data(self):
        """Load saved game states from file"""
        try:
            if os.path.exists(self.states_file):
                with open(self.states_file, 'r') as f:
                    self.game_states = json.load(f)
        except Exception as e:
            print(f"Error loading game states: {e}")
            self.game_states = {}
    
    def save_all_data(self):
        """Save all game states to file"""
        try:
            with open(self.states_file, 'w') as f:
                json.dump(self.game_states, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving game states: {e}")
    
    def launch_game(self, game_id: str, parent_frame: ctk.CTkFrame) -> bool:
        """Launch a specific game with proper error handling"""
        try:
            if game_id not in self.games:
                raise ValueError(f"Game '{game_id}' not found")
            
            game_info = self.games[game_id]
            
            # Store reference to the parent frame
            self.current_game_frame = parent_frame
            
            # Import game module dynamically
            try:
                module = importlib.import_module(game_info['module'])
                game_class = getattr(module, game_info['class'])
            except ImportError as e:
                print(f"Failed to import game module {game_info['module']}: {e}")
                self.show_error_message(parent_frame, f"Failed to load {game_info['name']}", str(e))
                return False
            except AttributeError as e:
                print(f"Game class {game_info['class']} not found in {game_info['module']}: {e}")
                self.show_error_message(parent_frame, f"Game class not found", str(e))
                return False
            
            # Clear parent frame
            self.clear_frame(parent_frame)
            
            # Create game instance with proper arguments based on game type
            try:
                if game_id == 'quiz':
                    # Load quiz data
                    questions, options, correct_answers = self.load_quiz_data()
                    game_instance = game_class(parent_frame, questions, options, correct_answers, self.return_to_menu)
                
                elif game_id == 'memory':
                    # Try different initialization patterns for MemoryGame
                    try:
                        game_instance = game_class(parent_frame, self.return_to_menu)
                    except TypeError:
                        try:
                            game_instance = game_class(parent_frame, return_callback=self.return_to_menu)
                        except TypeError:
                            game_instance = game_class(parent_frame)
                            if hasattr(game_instance, 'set_return_callback'):
                                game_instance.set_return_callback(self.return_to_menu)
                
                elif game_id == 'snake':
                    # SnakeGame initialization with return callback
                    try:
                        game_instance = game_class(parent_frame, return_callback=self.return_to_menu)
                    except TypeError:
                        try:
                            game_instance = game_class(parent_frame, self.return_to_menu)
                        except TypeError:
                            try:
                                game_instance = game_class(parent_frame, self)
                            except TypeError:
                                game_instance = game_class(parent_frame)
                                if hasattr(game_instance, 'set_return_callback'):
                                    game_instance.set_return_callback(self.return_to_menu)
                
                else:
                    # For other games, try the standard patterns
                    try:
                        game_instance = game_class(parent_frame, return_callback=self.return_to_menu)
                    except TypeError:
                        try:
                            game_instance = game_class(parent_frame, self.return_to_menu)
                        except TypeError:
                            try:
                                game_instance = game_class(parent_frame, self)
                            except TypeError:
                                game_instance = game_class(parent_frame)
                                if hasattr(game_instance, 'set_return_callback'):
                                    game_instance.set_return_callback(self.return_to_menu)
                
                # Set return callback if the game instance has a method to set it
                if hasattr(game_instance, 'return_callback') and game_instance.return_callback is None:
                    game_instance.return_callback = self.return_to_menu
                
                self.game_instances[game_id] = game_instance
                self.current_game = game_id
                
                # Update session data
                self.session_data['games_played'] += 1
                
                print(f"Successfully launched game: {game_id}")
                return True
                
            except Exception as init_error:
                print(f"Error initializing game {game_id}: {init_error}")
                self.show_error_message(parent_frame, f"Error loading {game_info['name']}", str(init_error))
                return False
            
        except Exception as e:
            print(f"Error launching game {game_id}: {e}")
            self.show_error_message(parent_frame, "Game Launch Error", str(e))
            return False
    
    def show_error_message(self, parent_frame: ctk.CTkFrame, title: str, message: str):
        """Show error message with back button"""
        self.clear_frame(parent_frame)
        
        # Create error display
        error_frame = ctk.CTkFrame(parent_frame, fg_color="#1a1a2e", corner_radius=20)
        error_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Error icon and title
        title_label = ctk.CTkLabel(
            error_frame,
            text=f"❌ {title}",
            font=("Arial", 24, "bold"),
            text_color="#ff6b6b"
        )
        title_label.pack(pady=(40, 20))
        
        # Error message
        message_label = ctk.CTkLabel(
            error_frame,
            text=message,
            font=("Arial", 16),
            text_color="#cccccc",
            wraplength=400
        )
        message_label.pack(pady=20)
        
        # Back button
        back_button = ctk.CTkButton(
            error_frame,
            text="🏠 Back to Menu",
            width=200,
            height=50,
            font=("Arial", 16, "bold"),
            fg_color="#00d4ff",
            hover_color="#0099cc",
            command=self.return_to_menu
        )
        back_button.pack(pady=30)
    
    def clear_frame(self, frame: ctk.CTkFrame):
        """Safely clear all widgets from a frame"""
        try:
            for widget in frame.winfo_children():
                widget.destroy()
        except Exception as e:
            print(f"Error clearing frame: {e}")
    
    def return_to_menu(self):
        """Return to main menu with proper cleanup and UI handling"""
        print("Returning to main menu...")
        
        # Clean up current game
        if self.current_game and self.current_game in self.game_instances:
            game_instance = self.game_instances[self.current_game]
            
            # Stop any running timers or threads
            if hasattr(game_instance, 'timer_running'):
                game_instance.timer_running = False
            if hasattr(game_instance, 'game_over'):
                game_instance.game_over = True
            
            # Call cleanup method if available
            if hasattr(game_instance, 'cleanup'):
                try:
                    game_instance.cleanup()
                except Exception as e:
                    print(f"Error during game cleanup: {e}")
            
            # Remove the game instance
            del self.game_instances[self.current_game]
        
        # Clear the current game frame if it exists
        if self.current_game_frame:
            try:
                self.clear_frame(self.current_game_frame)
            except Exception as e:
                print(f"Error clearing game frame: {e}")
        
        # Reset game state
        self.current_game = None
        self.current_game_frame = None
        
        # Save data
        self.save_all_data()
        
        # Return to main menu with proper error handling
        try:
            if hasattr(self.main_app, 'show_main_menu'):
                self.main_app.show_main_menu()
                print("Successfully returned to main menu via show_main_menu")
            elif hasattr(self.main_app, 'return_to_menu'):
                self.main_app.return_to_menu()
                print("Successfully returned to main menu via return_to_menu")
            elif hasattr(self.main_app, 'create_main_menu'):
                self.main_app.create_main_menu()
                print("Successfully returned to main menu via create_main_menu")
            else:
                print("Warning: Main app doesn't have a method to return to menu")
                # Create a temporary menu as fallback
                self.create_fallback_menu()
        except Exception as e:
            print(f"Error returning to main menu: {e}")
            self.create_fallback_menu()
    
    def create_fallback_menu(self):
        """Create a basic fallback menu if main app menu fails"""
        if not self.current_game_frame:
            return
        
        try:
            self.clear_frame(self.current_game_frame)
            
            fallback_frame = ctk.CTkFrame(self.current_game_frame, fg_color="#0f0f23", corner_radius=20)
            fallback_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            title_label = ctk.CTkLabel(
                fallback_frame,
                text="🎮 Game Center",
                font=("Arial", 32, "bold"),
                text_color="#ffd700"
            )
            title_label.pack(pady=40)
            
            message_label = ctk.CTkLabel(
                fallback_frame,
                text="Please restart the application to access the main menu.",
                font=("Arial", 16),
                text_color="#cccccc"
            )
            message_label.pack(pady=20)
            
            # Show available games as buttons
            games_frame = ctk.CTkFrame(fallback_frame, fg_color="transparent")
            games_frame.pack(pady=30)
            
            for game_id, game_info in self.games.items():
                if self.is_game_available(game_id):
                    game_btn = ctk.CTkButton(
                        games_frame,
                        text=f"{game_info['icon']} {game_info['name']}",
                        width=200,
                        height=50,
                        font=("Arial", 14, "bold"),
                        fg_color="#1a1a2e",
                        hover_color="#00d4ff",
                        command=lambda gid=game_id: self.launch_game(gid, self.current_game_frame)
                    )
                    game_btn.pack(pady=5)
            
        except Exception as e:
            print(f"Error creating fallback menu: {e}")
    
    def get_session_stats(self) -> dict:
        """Get current session statistics"""
        current_time = datetime.now()
        session_duration = (current_time - self.session_data['session_start']).total_seconds()
        
        return {
            'games_played': self.session_data['games_played'],
            'session_duration': session_duration,
            'achievements': self.session_data['achievements']
        }
    
    def get_game_state(self, game_id: str) -> dict:
        """Get saved state for a specific game"""
        return self.game_states.get(game_id, {})
    
    def save_game_state(self, game_id: str, state: dict):
        """Save state for a specific game"""
        self.game_states[game_id] = state
        self.save_all_data()
    
    def get_available_games(self) -> dict:
        """Get list of available games"""
        return self.games
    
    def is_game_available(self, game_id: str) -> bool:
        """Check if a game module can be imported"""
        if game_id not in self.games:
            return False
        
        try:
            game_info = self.games[game_id]
            importlib.import_module(game_info['module'])
            return True
        except ImportError:
            return False
    
    def force_cleanup(self):
        """Force cleanup of all resources"""
        print("Performing force cleanup...")
        
        # Stop all running games
        for game_id, game_instance in self.game_instances.items():
            try:
                if hasattr(game_instance, 'timer_running'):
                    game_instance.timer_running = False
                if hasattr(game_instance, 'game_over'):
                    game_instance.game_over = True
                if hasattr(game_instance, 'cleanup'):
                    game_instance.cleanup()
            except Exception as e:
                print(f"Error cleaning up game {game_id}: {e}")
        
        # Clear all instances
        self.game_instances.clear()
        self.current_game = None
        self.current_game_frame = None
        
        # Save final state
        self.save_all_data()