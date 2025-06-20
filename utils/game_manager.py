import json
import os
from datetime import datetime
import importlib
import sys
import customtkinter as ctk
from data.CorrectAnswer import correct_answers
from data.Questions import questions
from data.Options import options
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
            },
            'tetris': {
                'name': 'Tetris',
                'description': 'Classic block-falling puzzle game',
                'icon': '🟩',
                'module': 'games.tetris_game',
                'class': 'TetrisGame',
                'category': 'Puzzle'
            },
            'puzzle': {
                'name': '2048 Puzzle',
                'description': 'Slide and merge numbers to reach 2048',
                'icon': '🔢',
                'module': 'games.number_puzzle',
                'class': 'NumberPuzzle',
                'category': 'Strategy'
            }
        }
        
        self.load_all_data()
    
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
            
            # Clear parent frame
            for widget in parent_frame.winfo_children():
                widget.destroy()
            
            # Create game instance with proper arguments based on game type
            try:
                if game_id == 'quiz':
                    # QuizGame needs specific arguments - provide sample data or load from file  # Indices of correct answers
                    game_instance = game_class(parent_frame, questions, options, correct_answers)
                
                elif game_id == 'memory':
                    # MemoryGame likely expects only parent frame
                    game_instance = game_class(parent_frame)
                
                elif game_id == 'snake':
                    # SnakeGame might have specific initialization requirements
                    # Try different initialization patterns
                    try:
                        game_instance = game_class(parent_frame, self)
                    except TypeError:
                        # If that fails, try with just parent frame
                        game_instance = game_class(parent_frame)
                
                else:
                    # For other games, try the standard pattern first
                    try:
                        game_instance = game_class(parent_frame, self)
                    except TypeError:
                        # If that fails, try with just parent frame
                        game_instance = game_class(parent_frame)
                
                self.game_instances[game_id] = game_instance
                self.current_game = game_id
                
                # Update session data
                self.session_data['games_played'] += 1
                
                return True
                
            except Exception as init_error:
                print(f"Error initializing game {game_id}: {init_error}")
                print(f"Game class signature might be incompatible")
                return False
            
        except Exception as e:
            print(f"Error launching game {game_id}: {e}")
            return False
    
    def return_to_menu(self):
        """Return to main menu with proper cleanup"""
        if self.current_game and self.current_game in self.game_instances:
            game_instance = self.game_instances[self.current_game]
            if hasattr(game_instance, 'cleanup'):
                game_instance.cleanup()
        
        self.current_game = None
        self.save_all_data()
        
        if hasattr(self.main_app, 'show_main_menu'):
            self.main_app.show_main_menu()
    
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