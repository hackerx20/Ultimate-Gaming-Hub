__version__ = "1.0.0"
__author__ = "Ultimate Gaming Platform"

# Initialize component variables
MainMenu = None
GameThemes = None

# Import main UI components for easy access
try:
    from .main_menu import MainMenu
    UI_LOADED = True
except ImportError as e:
    print(f"Warning: Could not load MainMenu: {e}")
    UI_LOADED = False

try:
    from .themes import GameThemes
    THEMES_LOADED = True
except ImportError as e:
    print(f"Warning: Could not load GameThemes: {e}")
    THEMES_LOADED = False

# UI Module metadata
UI_COMPONENTS = []
if UI_LOADED:
    UI_COMPONENTS.append("MainMenu")
if THEMES_LOADED:
    UI_COMPONENTS.append("GameThemes")

# Color constants used throughout the UI
COLORS = {
    'primary': '#1a1a2e',
    'secondary': '#16213e',
    'accent': '#ffd700',
    'success': '#00ff88',
    'danger': '#ff6b6b',
    'text': '#ffffff',
    'text_secondary': '#cccccc'
}

def get_ui_info():
    """Get information about the UI module"""
    return {
        'version': __version__,
        'author': __author__,
        'components': UI_COMPONENTS,
        'colors': COLORS,
        'main_menu_loaded': UI_LOADED,
        'themes_loaded': THEMES_LOADED
    }