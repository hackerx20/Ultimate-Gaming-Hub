import customtkinter as ctk
from typing import Dict, Any, Union, Tuple

class ThemeManager:
    """Manages UI themes and styling for the gaming platform"""
    
    def __init__(self):
        self.current_theme = "dark"
        self.themes = self._initialize_themes()
        self.fonts = self._initialize_fonts()
        self._tk_root_available = False
        
    def _initialize_themes(self) -> Dict[str, Dict[str, Any]]:
        """Initialize all available themes"""
        return {
            "dark": {
                "name": "Dark Gaming",
                "colors": {
                    "primary_bg": "#1a1a2e",
                    "secondary_bg": "#16213e",
                    "tertiary_bg": "#0f0f23",
                    "card_bg": "#2a2a4a",
                    "accent": "#ffd700",
                    "accent_hover": "#ffcc00",
                    "success": "#00ff88",
                    "warning": "#ffa500",
                    "danger": "#ff6b6b",
                    "danger_hover": "#ff5252",
                    "text_primary": "#ffffff",
                    "text_secondary": "#cccccc",
                    "text_muted": "#888888",
                    "border": "#333366",
                    "shadow": "#000000"
                },
                "gradients": {
                    "main": ["#1a1a2e", "#16213e"],
                    "card": ["#2a2a4a", "#1e1e3f"],
                    "button": ["#ffd700", "#ffb300"],
                    "accent": ["#00ff88", "#00cc66"]
                }
            },
            "light": {
                "name": "Light Gaming",
                "colors": {
                    "primary_bg": "#f5f5f5",
                    "secondary_bg": "#ffffff",
                    "tertiary_bg": "#e8e8e8",
                    "card_bg": "#ffffff",
                    "accent": "#2196f3",
                    "accent_hover": "#1976d2",
                    "success": "#4caf50",
                    "warning": "#ff9800",
                    "danger": "#f44336",
                    "danger_hover": "#d32f2f",
                    "text_primary": "#212121",
                    "text_secondary": "#757575",
                    "text_muted": "#9e9e9e",
                    "border": "#e0e0e0",
                    "shadow": "#00000020"
                },
                "gradients": {
                    "main": ["#f5f5f5", "#ffffff"],
                    "card": ["#ffffff", "#f8f8f8"],
                    "button": ["#2196f3", "#1565c0"],
                    "accent": ["#4caf50", "#388e3c"]
                }
            },
            "neon": {
                "name": "Neon Cyberpunk",
                "colors": {
                    "primary_bg": "#0a0a0a",
                    "secondary_bg": "#1a0a1a",
                    "tertiary_bg": "#050505",
                    "card_bg": "#1a1a2e",
                    "accent": "#00ffff",
                    "accent_hover": "#00e6e6",
                    "success": "#39ff14",
                    "warning": "#ffff00",
                    "danger": "#ff073a",
                    "danger_hover": "#e6062f",
                    "text_primary": "#ffffff",
                    "text_secondary": "#00ffff",
                    "text_muted": "#666666",
                    "border": "#00ffff",
                    "shadow": "#00ffff20"
                },
                "gradients": {
                    "main": ["#0a0a0a", "#1a0a1a"],
                    "card": ["#1a1a2e", "#2a1a4a"],
                    "button": ["#00ffff", "#0099cc"],
                    "accent": ["#39ff14", "#00cc11"]
                }
            },
            "retro": {
                "name": "Retro Arcade",
                "colors": {
                    "primary_bg": "#2e1065",
                    "secondary_bg": "#1a0040",
                    "tertiary_bg": "#0d001a",
                    "card_bg": "#4a1a7a",
                    "accent": "#ff6b35",
                    "accent_hover": "#ff5722",
                    "success": "#7ed321",
                    "warning": "#f5a623",
                    "danger": "#d0021b",
                    "danger_hover": "#b71c1c",
                    "text_primary": "#ffffff",
                    "text_secondary": "#ffccff",
                    "text_muted": "#cc99cc",
                    "border": "#ff6b35",
                    "shadow": "#ff6b3540"
                },
                "gradients": {
                    "main": ["#2e1065", "#1a0040"],
                    "card": ["#4a1a7a", "#6a2a9a"],
                    "button": ["#ff6b35", "#ff4500"],
                    "accent": ["#7ed321", "#5cb85c"]
                }
            }
        }
    
    def _initialize_fonts(self) -> Dict[str, Dict[str, Any]]:
        """Initialize font configurations"""
        return {
            "headers": {
                "family": "Arial",
                "sizes": {
                    "xl": 32,
                    "large": 24,
                    "medium": 20,
                    "small": 16
                },
                "weight": "bold"
            },
            "body": {
                "family": "Arial",
                "sizes": {
                    "large": 18,
                    "medium": 16,
                    "small": 14,
                    "xs": 12
                },
                "weight": "normal"
            },
            "buttons": {
                "family": "Arial",
                "sizes": {
                    "large": 18,
                    "medium": 16,
                    "small": 14
                },
                "weight": "bold"
            },
            "monospace": {
                "family": "Courier New",
                "sizes": {
                    "large": 16,
                    "medium": 14,
                    "small": 12
                },
                "weight": "normal"
            }
        }
    
    def set_theme(self, theme_name: str):
        """Set the current theme"""
        if theme_name in self.themes:
            self.current_theme = theme_name
            ctk.set_appearance_mode("dark" if theme_name in ["dark", "neon", "retro"] else "light")
    
    def set_tk_root_available(self, available: bool = True):
        """Set whether Tk root is available for CTkFont creation"""
        self._tk_root_available = available
    
    def get_color(self, color_name: str) -> str:
        """Get a color from the current theme"""
        return self.themes[self.current_theme]["colors"].get(color_name, "#ffffff")
    
    def get_gradient(self, gradient_name: str) -> list:
        """Get a gradient from the current theme"""
        return self.themes[self.current_theme]["gradients"].get(gradient_name, ["#ffffff", "#f0f0f0"])
    
    def get_font(self, font_type: str, size: str = "medium") -> Union[ctk.CTkFont, Tuple[str, int, str]]:
        """Get font - returns CTkFont if Tk root available, otherwise tuple"""
        font_config = self.fonts.get(font_type, self.fonts["body"])
        family = font_config["family"]
        font_size = font_config["sizes"].get(size, 16)
        weight = font_config["weight"]
        
        if self._tk_root_available:
            try:
                return ctk.CTkFont(family=family, size=font_size, weight=weight)
            except Exception:
                # Fallback to tuple if CTkFont creation fails
                return (family, font_size, weight)
        else:
            return (family, font_size, weight)
    
    def get_font_tuple(self, font_type: str, size: str = "medium") -> Tuple[str, int, str]:
        """Always return font as tuple (safe before Tk root exists)"""
        font_config = self.fonts.get(font_type, self.fonts["body"])
        return (
            font_config["family"],
            font_config["sizes"].get(size, 16),
            font_config["weight"]
        )
    
    def create_styled_frame(self, parent, style: str = "default", **kwargs) -> ctk.CTkFrame:
        """Create a styled frame with theme colors"""
        styles = {
            "default": {
                "fg_color": self.get_color("secondary_bg"),
                "border_color": self.get_color("border"),
                "border_width": 1
            },
            "card": {
                "fg_color": self.get_color("card_bg"),
                "corner_radius": 15,
                "border_color": self.get_color("border"),
                "border_width": 1
            },
            "transparent": {
                "fg_color": "transparent"
            },
            "primary": {
                "fg_color": self.get_color("primary_bg"),
                "corner_radius": 10
            }
        }
        
        style_config = styles.get(style, styles["default"])
        style_config.update(kwargs)
        
        return ctk.CTkFrame(parent, **style_config)
    
    def create_styled_button(self, parent, text: str, style: str = "default", **kwargs) -> ctk.CTkButton:
        """Create a styled button with theme colors"""
        styles = {
            "default": {
                "fg_color": self.get_color("accent"),
                "hover_color": self.get_color("accent_hover"),
                "text_color": self.get_color("text_primary"),
                "font": self.get_font("buttons", "medium"),
                "corner_radius": 8
            },
            "primary": {
                "fg_color": self.get_color("accent"),
                "hover_color": self.get_color("accent_hover"),
                "text_color": "white",
                "font": self.get_font("buttons", "large"),
                "corner_radius": 10,
                "height": 40
            },
            "success": {
                "fg_color": self.get_color("success"),
                "hover_color": self.get_color("success"),
                "text_color": "white",
                "font": self.get_font("buttons", "medium"),
                "corner_radius": 8
            },
            "danger": {
                "fg_color": self.get_color("danger"),
                "hover_color": self.get_color("danger_hover"),
                "text_color": "white",
                "font": self.get_font("buttons", "medium"),
                "corner_radius": 8
            },
            "ghost": {
                "fg_color": "transparent",
                "hover_color": self.get_color("card_bg"),
                "text_color": self.get_color("accent"),
                "border_color": self.get_color("accent"),
                "border_width": 2,
                "font": self.get_font("buttons", "medium"),
                "corner_radius": 8
            },
            "game_card": {
                "fg_color": self.get_color("accent"),
                "hover_color": self.get_color("accent_hover"),
                "text_color": "white",
                "font": self.get_font("buttons", "medium"),
                "corner_radius": 20,
                "height": 35,
                "width": 120
            }
        }
        
        style_config = styles.get(style, styles["default"])
        style_config.update(kwargs)
        
        return ctk.CTkButton(parent, text=text, **style_config)
    
    def create_styled_label(self, parent, text: str, style: str = "default", **kwargs) -> ctk.CTkLabel:
        """Create a styled label with theme colors"""
        styles = {
            "default": {
                "text_color": self.get_color("text_primary"),
                "font": self.get_font("body", "medium")
            },
            "title": {
                "text_color": self.get_color("accent"),
                "font": self.get_font("headers", "xl")
            },
            "subtitle": {
                "text_color": self.get_color("text_secondary"),
                "font": self.get_font("headers", "medium")
            },
            "heading": {
                "text_color": self.get_color("text_primary"),
                "font": self.get_font("headers", "large")
            },
            "caption": {
                "text_color": self.get_color("text_muted"),
                "font": self.get_font("body", "small")
            },
            "accent": {
                "text_color": self.get_color("accent"),
                "font": self.get_font("body", "medium")
            },
            "success": {
                "text_color": self.get_color("success"),
                "font": self.get_font("body", "medium")
            },
            "warning": {
                "text_color": self.get_color("warning"),
                "font": self.get_font("body", "medium")
            },
            "danger": {
                "text_color": self.get_color("danger"),
                "font": self.get_font("body", "medium")
            }
        }
        
        style_config = styles.get(style, styles["default"])
        style_config.update(kwargs)
        
        return ctk.CTkLabel(parent, text=text, **style_config)
    
    def create_game_card_style(self, color: str, hover_color: str) -> dict:
        """Create a game card style configuration"""
        return {
            "fg_color": color,
            "corner_radius": 15,
            "width": 350,
            "height": 200,
            "hover_color": hover_color,
            "border_width": 0
        }
    
    def get_animation_config(self) -> dict:
        """Get animation configuration for the current theme"""
        return {
            "hover_scale": 1.05,
            "animation_duration": 0.2,
            "easing": "ease_in_out",
            "glow_effect": self.current_theme in ["neon", "retro"],
            "particle_effects": self.current_theme == "neon"
        }


class GameThemes:
    """Specific themes for individual games"""
    
    @staticmethod
    def get_quiz_theme():
        """Get KBC Quiz game theme"""
        return {
            "background": "#1a1a2e",
            "question_bg": "#2a2a4a",
            "option_colors": {
                "default": "#16213e",
                "hover": "#2a2a5a",
                "correct": "#00ff88",
                "incorrect": "#ff6b6b",
                "selected": "#ffd700"
            },
            "text_colors": {
                "question": "#ffffff",
                "options": "#cccccc",
                "score": "#ffd700",
                "timer": "#ff6b6b"
            },
            "lifeline_colors": {
                "available": "#00ff88",
                "used": "#666666",
                "hover": "#00cc66"
            }
        }
    
    @staticmethod
    def get_snake_theme():
        """Get Snake game theme"""
        return {
            "background": "#0a0a0a",
            "grid_color": "#1a1a1a",
            "snake_colors": {
                "head": "#00ff88",
                "body": "#00cc66",
                "tail": "#009944"
            },
            "food_color": "#ff6b6b",
            "power_up_colors": {
                "speed": "#ffd700",
                "grow": "#ff6b35",
                "score": "#00ffff"
            },
            "ui_colors": {
                "score": "#ffffff",
                "level": "#ffd700",
                "game_over": "#ff6b6b"
            }
        }
    
    @staticmethod
    def get_memory_theme():
        """Get Memory game theme"""
        return {
            "background": "#16213e",
            "card_back": "#2a2a4a",
            "card_front": "#ffffff",
            "card_border": "#ffd700",
            "matched_glow": "#00ff88",
            "flip_animation": {
                "duration": 0.3,
                "easing": "ease_in_out"
            },
            "themes": {
                "classic": ["#ff6b6b", "#4ecdc4", "#45b7d1", "#96ceb4", "#ffeaa7", "#dda0dd"],
                "animals": ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼"],
                "fruits": ["🍎", "🍊", "🍋", "🍌", "🍇", "🍓", "🍑", "🍒"]
            }
        }
    
    @staticmethod
    def get_tetris_theme():
        """Get Tetris game theme"""
        return {
            "background": "#1a1a2e",
            "grid_color": "#2a2a4a",
            "ghost_piece": "#666666",
            "block_colors": {
                "I": "#00ffff",  # Cyan
                "O": "#ffff00",  # Yellow
                "T": "#800080",  # Purple
                "S": "#00ff00",  # Green
                "Z": "#ff0000",  # Red
                "J": "#0000ff",  # Blue
                "L": "#ffa500"   # Orange
            },
            "effects": {
                "line_clear": "#ffffff",
                "level_up": "#ffd700",
                "game_over": "#ff6b6b"
            },
            "ui_colors": {
                "score": "#ffffff",
                "level": "#ffd700",
                "lines": "#00ff88",
                "next_piece": "#cccccc"
            }
        }
    
    @staticmethod
    def get_number_puzzle_theme():
        """Get Number Puzzle (2048) game theme"""
        return {
            "background": "#faf8ef",
            "grid_color": "#bbada0",
            "empty_cell": "#cdc1b4",
            "tile_colors": {
                2: {"bg": "#eee4da", "text": "#776e65"},
                4: {"bg": "#ede0c8", "text": "#776e65"},
                8: {"bg": "#f2b179", "text": "#f9f6f2"},
                16: {"bg": "#f59563", "text": "#f9f6f2"},
                32: {"bg": "#f67c5f", "text": "#f9f6f2"},
                64: {"bg": "#f65e3b", "text": "#f9f6f2"},
                128: {"bg": "#edcf72", "text": "#f9f6f2"},
                256: {"bg": "#edcc61", "text": "#f9f6f2"},
                512: {"bg": "#edc850", "text": "#f9f6f2"},
                1024: {"bg": "#edc53f", "text": "#f9f6f2"},
                2048: {"bg": "#edc22e", "text": "#f9f6f2"}
            },
            "animations": {
                "slide_duration": 0.15,
                "merge_duration": 0.1,
                "appear_duration": 0.2
            },
            "ui_colors": {
                "score": "#776e65",
                "best": "#776e65",
                "game_over": "#ff6b6b",
                "you_win": "#00ff88"
            }
        }


class AnimationHelper:
    """Helper class for UI animations"""
    
    @staticmethod
    def fade_in(widget, duration=0.3):
        """Fade in animation for widgets"""
        try:
            if hasattr(widget, 'winfo_exists') and widget.winfo_exists():
                # Basic fade in using alpha (placeholder implementation)
                widget.configure(state='normal')
                return True
        except Exception:
            pass
        return False
    
    @staticmethod
    def fade_out(widget, duration=0.3):
        """Fade out animation for widgets"""
        try:
            if hasattr(widget, 'winfo_exists') and widget.winfo_exists():
                # Basic fade out using alpha (placeholder implementation)
                widget.configure(state='disabled')
                return True
        except Exception:
            pass
        return False
    
    @staticmethod
    def slide_in(widget, direction="left", duration=0.3):
        """Slide in animation for widgets"""
        try:
            if hasattr(widget, 'winfo_exists') and widget.winfo_exists():
                # Placeholder for slide animation
                widget.grid() if hasattr(widget, 'grid') else widget.pack()
                return True
        except Exception:
            pass
        return False
    
    @staticmethod
    def scale_animation(widget, scale_factor=1.1, duration=0.2):
        """Scale animation for hover effects"""
        try:
            if hasattr(widget, 'winfo_exists') and widget.winfo_exists():
                # Placeholder for scale animation
                # In a real implementation, this would modify widget size
                return True
        except Exception:
            pass
        return False
    
    @staticmethod
    def glow_effect(widget, color="#ffd700", duration=0.5):
        """Glow effect for special elements"""
        try:
            if hasattr(widget, 'winfo_exists') and widget.winfo_exists():
                # Placeholder for glow effect
                # In a real implementation, this would modify border/shadow
                return True
        except Exception:
            pass
        return False


class ResponsiveDesign:
    """Handles responsive design for different screen sizes"""
    
    def __init__(self):
        self.breakpoints = {
            "small": 800,
            "medium": 1200,
            "large": 1600
        }
    
    def get_layout_config(self, screen_width: int) -> dict:
        """Get layout configuration based on screen width"""
        if screen_width < self.breakpoints["small"]:
            return {
                "columns": 1,
                "card_width": 300,
                "card_height": 180,
                "padding": 10,
                "font_scale": 0.8
            }
        elif screen_width < self.breakpoints["medium"]:
            return {
                "columns": 2,
                "card_width": 350,
                "card_height": 200,
                "padding": 15,
                "font_scale": 0.9
            }
        elif screen_width < self.breakpoints["large"]:
            return {
                "columns": 3,
                "card_width": 350,
                "card_height": 200,
                "padding": 20,
                "font_scale": 1.0
            }
        else:
            return {
                "columns": 4,
                "card_width": 400,
                "card_height": 220,
                "padding": 25,
                "font_scale": 1.1
            }
    
    def adjust_font_sizes(self, base_sizes: dict, scale_factor: float) -> dict:
        """Adjust font sizes based on scale factor"""
        return {key: int(size * scale_factor) for key, size in base_sizes.items()}


# Global theme manager instance
theme_manager = ThemeManager()

# Convenience functions for easy access
def get_color(color_name: str) -> str:
    """Get a color from the current theme"""
    return theme_manager.get_color(color_name)

def get_font(font_type: str, size: str = "medium") -> Union[ctk.CTkFont, Tuple[str, int, str]]:
    """Get a configured font - returns CTkFont if available, otherwise tuple"""
    return theme_manager.get_font(font_type, size)

def get_font_tuple(font_type: str, size: str = "medium") -> Tuple[str, int, str]:
    """Get font as tuple (safe before Tk root exists)"""
    return theme_manager.get_font_tuple(font_type, size)

def create_styled_frame(parent, style: str = "default", **kwargs) -> ctk.CTkFrame:
    """Create a styled frame"""
    return theme_manager.create_styled_frame(parent, style, **kwargs)

def create_styled_button(parent, text: str, style: str = "default", **kwargs) -> ctk.CTkButton:
    """Create a styled button"""
    return theme_manager.create_styled_button(parent, text, style, **kwargs)

def create_styled_label(parent, text: str, style: str = "default", **kwargs) -> ctk.CTkLabel:
    """Create a styled label"""
    return theme_manager.create_styled_label(parent, text, style, **kwargs)

def set_tk_root_available(available: bool = True):
    """Set whether Tk root is available for font creation"""
    theme_manager.set_tk_root_available(available)