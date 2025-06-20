__version__ = "1.0.0"
__author__ = "Ultimate Gaming Platform"

# Initialize utility components
GameManager = None
ScoreManager = None

# Import utility components
try:
    from .game_manager import GameManager
    GAME_MANAGER_LOADED = True
except ImportError as e:
    print(f"Warning: Could not load GameManager: {e}")
    GAME_MANAGER_LOADED = False

try:
    from .score_manager import ScoreManager
    SCORE_MANAGER_LOADED = True
except ImportError as e:
    print(f"Warning: Could not load ScoreManager: {e}")
    SCORE_MANAGER_LOADED = False

# Utility components
UTILITY_COMPONENTS = []
if GAME_MANAGER_LOADED:
    UTILITY_COMPONENTS.append("GameManager")
if SCORE_MANAGER_LOADED:
    UTILITY_COMPONENTS.append("ScoreManager")

def get_utils_info():
    """Get information about utility components"""
    return {
        'version': __version__,
        'components': UTILITY_COMPONENTS,
        'author': __author__,
        'game_manager_loaded': GAME_MANAGER_LOADED,
        'score_manager_loaded': SCORE_MANAGER_LOADED
    }

# Helper functions
def format_time(seconds):
    """Format seconds into MM:SS format"""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

def format_score(score):
    """Format score with commas for thousands"""
    return f"{score:,}"

def validate_game_class(game_class):
    """Validate that a game class has required methods"""
    if game_class is None:
        return {
            'valid': False,
            'error': 'Game class is None',
            'missing_required': [],
            'missing_optional': [],
            'has_methods': []
        }
    
    # Check if it's a class or has callable methods
    if not hasattr(game_class, '__class__') and not callable(game_class):
        return {
            'valid': False,
            'error': 'Invalid game class object',
            'missing_required': [],
            'missing_optional': [],
            'has_methods': []
        }
    
    required_methods = ['initialize', 'cleanup']
    optional_methods = ['pause', 'resume', 'save_state', 'load_state']
    
    validation_result = {
        'valid': True,
        'missing_required': [],
        'missing_optional': [],
        'has_methods': []
    }
    
    for method in required_methods:
        if hasattr(game_class, method) and callable(getattr(game_class, method)):
            validation_result['has_methods'].append(method)
        else:
            validation_result['missing_required'].append(method)
            validation_result['valid'] = False
    
    for method in optional_methods:
        if hasattr(game_class, method) and callable(getattr(game_class, method)):
            validation_result['has_methods'].append(method)
        else:
            validation_result['missing_optional'].append(method)
    
    return validation_result