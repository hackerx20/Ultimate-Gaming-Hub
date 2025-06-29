__version__ = "1.0.0"
__author__ = "Ultimate Gaming Platform"

# Game registry for dynamic loading
AVAILABLE_GAMES = {
    'quiz': {
        'name': 'KBC Quiz Game',
        'class': 'QuizGame',
        'module': 'quiz_game',
        'description': 'Test your knowledge with challenging questions',
        'category': 'Knowledge'
    },
    'snake': {
        'name': 'Snake Game',
        'class': 'SnakeGame', 
        'module': 'snake_game',
        'description': 'Classic snake game with modern features',
        'category': 'Arcade'
    },
    'memory': {
        'name': 'Memory Match',
        'class': 'MemoryGame',
        'module': 'memory_game', 
        'description': 'Test your memory with card matching',
        'category': 'Puzzle'
    }
}

def get_game_info(game_id):
    """Get information about a specific game"""
    return AVAILABLE_GAMES.get(game_id)

def get_all_games():
    """Get information about all available games"""
    return AVAILABLE_GAMES

def get_games_by_category(category):
    """Get games filtered by category"""
    return {
        game_id: game_info 
        for game_id, game_info in AVAILABLE_GAMES.items() 
        if game_info.get('category') == category
    }
