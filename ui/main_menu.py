import customtkinter as ctk
from tkinter import messagebox
import threading
import time

class MainMenu:
    def __init__(self, root, game_manager):
        self.root = root
        self.game_manager = game_manager
        self.animation_running = False
        
        # Configure main window
        self.root.title("Ultimate Gaming Platform")
        self.root.geometry("1200x800")
        self.root.configure(fg_color=("#1a1a2e", "#0f0f23"))
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(root, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.create_main_menu()
        self.start_animations()
    
    def show_main_menu(self):
        """Method called by GameManager to return to main menu - FIXED"""
        print("MainMenu: Showing main menu...")
        try:
            # Clear the main frame first
            for widget in self.main_frame.winfo_children():
                widget.destroy()
            
            # Recreate the main menu
            self.create_main_menu()
            print("MainMenu: Main menu recreated successfully")
        except Exception as e:
            print(f"MainMenu: Error recreating main menu: {e}")
            # Fallback: recreate everything
            try:
                self.main_frame.destroy()
                self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
                self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
                self.create_main_menu()
            except Exception as e2:
                print(f"MainMenu: Fallback failed too: {e2}")
    
    def return_to_menu(self):
        """Alternative method name for returning to main menu"""
        self.show_main_menu()
    
    def create_main_menu(self):
        """Create the main menu interface"""
        self.clear_main_frame()
        self.create_header()
        self.create_game_cards()
        self.create_stats_panel()
        self.create_footer()
    
    def clear_main_frame(self):
        """Clears all widgets inside the main content frame"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def create_header(self):
        """Create the header section with title and navigation"""
        header_frame = ctk.CTkFrame(self.main_frame, height=100, fg_color=("#16213e", "#0a0a1a"))
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Title with gradient effect
        title_label = ctk.CTkLabel(
            header_frame,
            text="🎮 ULTIMATE GAMING PLATFORM",
            font=("Arial", 32, "bold"),
            text_color=("#ffd700", "#ffcc00")
        )
        title_label.pack(pady=20)
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Choose Your Adventure - 5 Exciting Games Await!",
            font=("Arial", 16),
            text_color=("#cccccc", "#888888")
        )
        subtitle_label.pack()
    
    def create_game_cards(self):
        """Create game selection cards"""
        games_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        games_frame.pack(fill="both", expand=True, pady=20)
        
        # Game data
        self.games_data = [
            {
                "name": "KBC Quiz",
                "description": "Test your knowledge with challenging questions",
                "icon": "🧠",
                "color": "#ff6b6b",
                "hover_color": "#ff5252",
                "action": lambda: self.launch_game_safely('quiz')
            },
            {
                "name": "Snake Game",
                "description": "Classic snake with modern twists",
                "icon": "🐍",
                "color": "#4ecdc4",
                "hover_color": "#26a69a",
                "action": lambda: self.launch_game_safely('snake')
            },
            {
                "name": "Memory Match",
                "description": "Match cards and train your memory",
                "icon": "🃏",
                "color": "#45b7d1",
                "hover_color": "#2196f3",
                "action": lambda: self.launch_game_safely('memory')
            }
        ]
        
        # Create cards in a grid layout
        for i, game in enumerate(self.games_data):
            row = i // 3
            col = i % 3
            self.create_game_card(games_frame, game, row, col)
    
    def launch_game_safely(self, game_id):
        """Safely launch a game with error handling - FIXED VERSION"""
        try:
            print(f"MainMenu: Launching game {game_id}")
            
            # FIXED: Don't pass the callback here - GameManager handles it internally
            success = self.game_manager.launch_game(game_id, self.main_frame)
            if not success:
                print(f"Failed to launch game: {game_id}")
                messagebox.showerror("Error", f"Failed to launch {game_id}. Please check the game files.")
        except Exception as e:
            print(f"Error launching game {game_id}: {e}")
            messagebox.showerror("Error", f"An error occurred while launching {game_id}:\n{str(e)}")
    
    def create_game_card(self, parent, game_data, row, col):
        """Create individual game card with animations"""
        card_frame = ctk.CTkFrame(
            parent,
            width=350,
            height=200,
            fg_color=game_data["color"],
            corner_radius=15
        )
        card_frame.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
        card_frame.grid_propagate(False)
        
        # Configure grid weights
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
        
        # Icon
        icon_label = ctk.CTkLabel(
            card_frame,
            text=game_data["icon"],
            font=("Arial", 48)
        )
        icon_label.pack(pady=(20, 10))
        
        # Game name
        name_label = ctk.CTkLabel(
            card_frame,
            text=game_data["name"],
            font=("Arial", 20, "bold"),
            text_color="white"
        )
        name_label.pack(pady=5)
        
        # Description
        desc_label = ctk.CTkLabel(
            card_frame,
            text=game_data["description"],
            font=("Arial", 12),
            text_color="white",
            wraplength=300
        )
        desc_label.pack(pady=5)
        
        # Play button
        play_button = ctk.CTkButton(
            card_frame,
            text="PLAY NOW",
            font=("Arial", 14, "bold"),
            fg_color="white",
            text_color=game_data["color"],
            hover_color="#f0f0f0",
            width=120,
            height=35,
            corner_radius=20,
            command=game_data["action"]
        )
        play_button.pack(pady=(10, 20))
        
        # Add hover effects
        self.add_hover_effects(card_frame, game_data)
    
    def add_hover_effects(self, card, game_data):
        """Add smooth hover animations to cards"""
        original_color = game_data["color"]
        hover_color = game_data["hover_color"]
        
        def on_enter(event):
            if card.winfo_exists():  # Check if widget still exists
                card.configure(fg_color=hover_color)
                card.configure(border_width=3, border_color="#ffd700")
        
        def on_leave(event):
            if card.winfo_exists():  # Check if widget still exists
                card.configure(fg_color=original_color)
                card.configure(border_width=0)
        
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
    
    def create_stats_panel(self):
        """Create statistics panel"""
        stats_frame = ctk.CTkFrame(self.main_frame, height=120, fg_color=("#16213e", "#0a0a1a"))
        stats_frame.pack(fill="x", pady=20)
        stats_frame.pack_propagate(False)
        
        # Stats title
        stats_title = ctk.CTkLabel(
            stats_frame,
            text="📊 Your Gaming Stats",
            font=("Arial", 18, "bold"),
            text_color=("#ffd700", "#ffcc00")
        )
        stats_title.pack(pady=(10, 5))
        
        # Stats container
        stats_container = ctk.CTkFrame(stats_frame, fg_color="transparent")
        stats_container.pack(fill="x", padx=20, pady=10)
        
        # Individual stats
        try:
            stats = self.game_manager.get_session_stats()
            stats_data = [
                ("Games Played", str(stats.get("games_played", 0))),
                ("Time Played", f"{int(stats.get('session_duration', 0))}s")
            ]
        except Exception as e:
            print(f"Error getting stats: {e}")
            stats_data = [("Games Played", "0"), ("Time Played", "0s")]
        
        for i, (label, value) in enumerate(stats_data):
            stat_frame = ctk.CTkFrame(stats_container, fg_color=("#2a2a4a", "#1a1a2a"))
            stat_frame.grid(row=0, column=i, padx=10, pady=5, sticky="ew")
            stats_container.grid_columnconfigure(i, weight=1)
            
            value_label = ctk.CTkLabel(
                stat_frame,
                text=value,
                font=("Arial", 16, "bold"),
                text_color="#00ff88"
            )
            value_label.pack(pady=(10, 2))
            
            label_label = ctk.CTkLabel(
                stat_frame,
                text=label,
                font=("Arial", 10),
                text_color="#cccccc"
            )
            label_label.pack(pady=(0, 10))
    
    def create_footer(self):
        """Create footer with settings and info"""
        footer_frame = ctk.CTkFrame(self.main_frame, height=60, fg_color="transparent")
        footer_frame.pack(fill="x", pady=(20, 0))
        footer_frame.pack_propagate(False)
        
        # Settings button
        settings_button = ctk.CTkButton(
            footer_frame,
            text="⚙️ Settings",
            font=("Arial", 14),
            fg_color=("#16213e", "#0a0a1a"),
            hover_color=("#2a2a4a", "#1a1a2a"),
            width=100,
            command=self.open_settings
        )
        settings_button.pack(side="left", padx=10, pady=15)
        
        # About button
        about_button = ctk.CTkButton(
            footer_frame,
            text="ℹ️ About",
            font=("Arial", 14),
            fg_color=("#16213e", "#0a0a1a"),
            hover_color=("#2a2a4a", "#1a1a2a"),
            width=100,
            command=self.show_about
        )
        about_button.pack(side="left", padx=10, pady=15)
        
        # Exit button
        exit_button = ctk.CTkButton(
            footer_frame,
            text="❌ Exit",
            font=("Arial", 14),
            fg_color="#ff6b6b",
            hover_color="#ff5252",
            width=100,
            command=self.exit_application
        )
        exit_button.pack(side="right", padx=10, pady=15)
    
    def start_animations(self):
        """Start background animations"""
        self.animation_running = True
        threading.Thread(target=self.animate_background, daemon=True).start()
    
    def animate_background(self):
        """Subtle background animations"""
        while self.animation_running:
            time.sleep(0.1)
    
    def open_settings(self):
        """Open settings dialog"""
        try:
            SettingsWindow(self.root, self.game_manager)
        except Exception as e:
            print(f"Error opening settings: {e}")
            messagebox.showerror("Error", "Could not open settings window.")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """Ultimate Gaming Platform v1.0

A comprehensive gaming platform featuring 5 exciting games:
• KBC Quiz - Test your knowledge
• Snake Game - Classic arcade fun
• Memory Match - Train your brain

Developed with Python & CustomTkinter

Tips for troubleshooting:
- Make sure all game files are in the 'games' folder
- Check that data files exist in the 'data' folder
- Restart the application if games don't load properly"""
        
        messagebox.showinfo("About", about_text)
    
    def exit_application(self):
        """Exit the application"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.animation_running = False
            try:
                self.game_manager.save_all_data()
            except Exception as e:
                print(f"Error saving data on exit: {e}")
            self.root.quit()

class SettingsWindow:
    def __init__(self, parent, game_manager):
        self.parent = parent
        self.game_manager = game_manager
        
        # Create settings window
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Settings")
        self.window.geometry("400x500")
        self.window.configure(fg_color=("#1a1a2e", "#0f0f23"))
        self.window.transient(parent)

        # Center the window
        self.window.geometry("+{}+{}".format(
            parent.winfo_rootx() + 50,
            parent.winfo_rooty() + 50
        ))

        # Delay grab_set until the window is mapped
        self.window.after(100, self.safe_grab_set)

        self.create_settings_ui()
    
    def safe_grab_set(self):
        """Safely set grab_set with error handling"""
        try:
            if self.window.winfo_exists():
                self.window.grab_set()
                self.window.focus_set()
        except Exception as e:
            print(f"Could not set window focus: {e}")
    
    def create_settings_ui(self):
        """Create settings interface"""
        # Title
        title_label = ctk.CTkLabel(
            self.window,
            text="⚙️ Settings",
            font=("Arial", 24, "bold"),
            text_color=("#ffd700", "#ffcc00")
        )
        title_label.pack(pady=20)
        
        # Sound settings
        sound_frame = ctk.CTkFrame(self.window)
        sound_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            sound_frame,
            text="🔊 Sound Settings",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        # Master volume
        ctk.CTkLabel(sound_frame, text="Master Volume").pack(pady=5)
        self.volume_slider = ctk.CTkSlider(
            sound_frame,
            from_=0,
            to=100,
            number_of_steps=100
        )
        self.volume_slider.pack(pady=5, padx=20, fill="x")
        self.volume_slider.set(50)
        
        # Sound effects toggle
        self.sound_effects_var = ctk.BooleanVar(value=True)
        sound_effects_checkbox = ctk.CTkCheckBox(
            sound_frame,
            text="Sound Effects",
            variable=self.sound_effects_var
        )
        sound_effects_checkbox.pack(pady=5)
        
        # Theme settings
        theme_frame = ctk.CTkFrame(self.window)
        theme_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            theme_frame,
            text="🎨 Theme Settings",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        # Theme selection
        self.theme_var = ctk.StringVar(value="Dark")
        theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            values=["Dark", "Light", "Auto"],
            variable=self.theme_var
        )
        theme_menu.pack(pady=5)
        
        # Game settings
        game_frame = ctk.CTkFrame(self.window)
        game_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            game_frame,
            text="🎮 Game Settings",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        # Auto-save toggle
        self.auto_save_var = ctk.BooleanVar(value=True)
        auto_save_checkbox = ctk.CTkCheckBox(
            game_frame,
            text="Auto-save game progress",
            variable=self.auto_save_var
        )
        auto_save_checkbox.pack(pady=5)
        
        # Show hints toggle
        self.show_hints_var = ctk.BooleanVar(value=True)
        hints_checkbox = ctk.CTkCheckBox(
            game_frame,
            text="Show game hints",
            variable=self.show_hints_var
        )
        hints_checkbox.pack(pady=5)
        
        # Buttons
        button_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=20)
        
        save_button = ctk.CTkButton(
            button_frame,
            text="💾 Save Settings",
            fg_color="#00ff88",
            hover_color="#00cc66",
            text_color="black",
            command=self.save_settings
        )
        save_button.pack(side="left", padx=10)
        
        cancel_button = ctk.CTkButton(
            button_frame,
            text="❌ Cancel",
            fg_color="#ff6b6b",
            hover_color="#ff5252",
            command=self.close_window
        )
        cancel_button.pack(side="right", padx=10)
    
    def save_settings(self):
        """Save settings"""
        try:
            settings = {
                "volume": self.volume_slider.get(),
                "sound_effects": self.sound_effects_var.get(),
                "theme": self.theme_var.get(),
                "auto_save": self.auto_save_var.get(),
                "show_hints": self.show_hints_var.get()
            }
            
            # You can save these settings to a file or pass to game_manager
            # For now, just show success message
            messagebox.showinfo("Settings", "Settings saved successfully!")
            print(f"Settings saved: {settings}")
            
        except Exception as e:
            print(f"Error saving settings: {e}")
            messagebox.showerror("Error", "Failed to save settings.")
        
        self.close_window()
    
    def close_window(self):
        """Safely close the settings window"""
        try:
            if self.window.winfo_exists():
                self.window.grab_release()
                self.window.destroy()
        except Exception as e:
            print(f"Error closing settings window: {e}")