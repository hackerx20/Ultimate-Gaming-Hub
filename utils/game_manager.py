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
                "Who painted the Mona Lisa?"
            ]
            fallback_options = [
                ["London", "Berlin", "Paris", "Madrid"],
                ["Venus", "Mars", "Jupiter", "Saturn"],
                ["Van Gogh", "Picasso", "Leonardo da Vinci", "Monet"]
            ]
            fallback_correct = [2, 1, 2]  # 0-indexed correct answers
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
            
            # Import game module dynamically
            try:
                module = importlib.import_module(game_info['module'])
                game_class = getattr(module, game_info['class'])
            except ImportError as e:
                print(f"Failed to import game module {game_info['module']}: {e}")
                return False
            except AttributeError as e:
                print(f"Game class {game_info['class']} not found in {game_info['module']}: {e}")
                return False
            
            # Clear parent frame
            for widget in parent_frame.winfo_children():
                widget.destroy()
            
            # Create game instance with proper arguments based on game type
            try:
                if game_id == 'quiz':
                    # Load quiz data
                    questions, options, correct_answers = self.load_quiz_data()
                    game_instance = game_class(parent_frame, questions, options, correct_answers)
                
                elif game_id == 'memory':
                    # Try different initialization patterns for MemoryGame
                    try:
                        game_instance = game_class(parent_frame, self.return_to_menu)
                    except TypeError:
                        try:
                            game_instance = game_class(parent_frame, return_callback=self.return_to_menu)
                        except TypeError:
                            game_instance = game_class(parent_frame)
                
                elif game_id == 'snake':
                    # SnakeGame initialization with return callback
                    try:
                        game_instance = game_class(parent_frame, return_callback=self.return_to_menu)
                    except TypeError:
                        try:
                            game_instance = game_class(parent_frame ,self.return_to_menu)
                        except TypeError:
                            try:
                                game_instance = game_class(parent_frame, self)
                            except TypeError:
                                game_instance = game_class(parent_frame)
                
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
                
                # Set return callback if the game instance has a method to set it
                if hasattr(game_instance, 'set_return_callback'):
                    game_instance.set_return_callback(self.return_to_menu)
                elif hasattr(game_instance, 'return_callback') and game_instance.return_callback is None:
                    game_instance.return_callback = self.return_to_menu
                
                self.game_instances[game_id] = game_instance
                self.current_game = game_id
                
                # Update session data
                self.session_data['games_played'] += 1
                
                print(f"Successfully launched game: {game_id}")
                return True
                
            except Exception as init_error:
                print(f"Error initializing game {game_id}: {init_error}")
                print(f"Game class signature might be incompatible")
                
                # Show error message in the parent frame
                error_label = ctk.CTkLabel(
                    parent_frame, 
                    text=f"Error loading {game_info['name']}\n{str(init_error)}", 
                    text_color="red"
                )
                error_label.pack(pady=20)
                
                back_button = ctk.CTkButton(
                    parent_frame, 
                    text="Back to Menu", 
                    command=self.return_to_menu
                )
                back_button.pack(pady=10)
                
                return False
            
        except Exception as e:
            print(f"Error launching game {game_id}: {e}")
            return False
    
    def return_to_menu(self):
        """Return to main menu with proper cleanup"""
        print("Returning to main menu...")
        
        if self.current_game and self.current_game in self.game_instances:
            game_instance = self.game_instances[self.current_game]
            if hasattr(game_instance, 'cleanup'):
                try:
                    game_instance.cleanup()
                except Exception as e:
                    print(f"Error during game cleanup: {e}")
            
            # Remove the game instance
            del self.game_instances[self.current_game]
        
        self.current_game = None
        self.save_all_data()
        
        # Call the main app's method to show main menu
        if hasattr(self.main_app, 'show_main_menu'):
            self.main_app.show_main_menu()
        elif hasattr(self.main_app, 'return_to_menu'):
            self.main_app.return_to_menu()
        else:
            print("Warning: Main app doesn't have a method to return to menu")
    
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