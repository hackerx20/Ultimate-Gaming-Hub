"""
Score Manager for Ultimate Gaming Platform
Handles high scores, statistics, and player achievements
"""

import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Set
import customtkinter as ctk

class ScoreManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.scores_file = os.path.join(data_dir, "scores.json")
        self.stats_file = os.path.join(data_dir, "statistics.json")
        self.achievements_file = os.path.join(data_dir, "achievements.json")
        
        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize data structures
        self.scores = self.load_scores()
        self.statistics = self.load_statistics()
        self.achievements = self.load_achievements()
        
        # Track earned achievement IDs for faster lookup
        self.earned_achievement_ids: Set[str] = {a['id'] for a in self.achievements}
        
        # Achievement definitions
        self.achievement_definitions = {
            'first_game': {
                'name': 'First Steps',
                'description': 'Play your first game',
                'icon': '🎮'
            },
            'quiz_master': {
                'name': 'Quiz Master',
                'description': 'Answer 10 quiz questions correctly in a row',
                'icon': '🧠'
            },
            'snake_charmer': {
                'name': 'Snake Charmer',
                'description': 'Reach 100 points in Snake Game',
                'icon': '🐍'
            },
            'memory_expert': {
                'name': 'Memory Expert',
                'description': 'Complete Memory Game in under 60 seconds',
                'icon': '🧩'
            },
            'tetris_champion': {
                'name': 'Tetris Champion',
                'description': 'Clear 10 lines in a single Tetris game',
                'icon': '🟩'
            },
            'puzzle_solver': {
                'name': 'Puzzle Solver',
                'description': 'Reach 1024 in Number Puzzle',
                'icon': '🔢'
            },
            'multi_player': {
                'name': 'Multi-Player',
                'description': 'Play all 5 games in one session',
                'icon': '🏆'
            },
            'high_scorer': {
                'name': 'High Scorer',
                'description': 'Achieve a high score in any game',
                'icon': '⭐'
            },
            'persistent': {
                'name': 'Persistent Player',
                'description': 'Play games for 10 days',
                'icon': '📅'
            },
            'speedster': {
                'name': 'Speedster',
                'description': 'Complete any timed game under target time',
                'icon': '⚡'
            }
        }
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp with timezone info"""
        return datetime.now(timezone.utc).isoformat()
    
    def _safe_file_operation(self, operation_func, error_message: str, show_error: bool = True) -> bool:
        """Safely perform file operations with error handling"""
        try:
            operation_func()
            return True
        except Exception as e:
            if show_error:
                print(f"{error_message}: {e}")
            return False
    
    def load_scores(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load high scores from file"""
        def load_operation():
            if os.path.exists(self.scores_file):
                with open(self.scores_file, 'r') as f:
                    return json.load(f)
            return {}
        
        result = {}
        def wrapped_load():
            nonlocal result
            result = load_operation()
        
        success = self._safe_file_operation(wrapped_load, "Error loading scores")
        return result if success else {}
    
    def save_scores(self) -> bool:
        """Save high scores to file"""
        def save_operation():
            with open(self.scores_file, 'w') as f:
                json.dump(self.scores, f, indent=2, default=str)
        
        return self._safe_file_operation(save_operation, "Error saving scores")
    
    def load_statistics(self) -> Dict[str, Any]:
        """Load game statistics from file"""
        def load_operation():
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
            return {
                'games_played': {},
                'total_time_played': {},
                'first_play_date': None,
                'last_play_date': None,
                'total_sessions': 0,
                'achievements_earned': 0,
                'unique_play_dates': []  # Track unique dates for persistent achievement
            }
        
        result = {}
        def wrapped_load():
            nonlocal result
            result = load_operation()
        
        success = self._safe_file_operation(wrapped_load, "Error loading statistics")
        if success:
            # Ensure all required fields exist
            default_stats = {
                'games_played': {},
                'total_time_played': {},
                'first_play_date': None,
                'last_play_date': None,
                'total_sessions': 0,
                'achievements_earned': 0,
                'unique_play_dates': []
            }
            for key, default_value in default_stats.items():
                if key not in result:
                    result[key] = default_value
        
        return result if success else default_stats
    
    def save_statistics(self) -> bool:
        """Save game statistics to file"""
        def save_operation():
            with open(self.stats_file, 'w') as f:
                json.dump(self.statistics, f, indent=2, default=str)
        
        return self._safe_file_operation(save_operation, "Error saving statistics")
    
    def load_achievements(self) -> List[Dict[str, Any]]:
        """Load achievements from file"""
        def load_operation():
            if os.path.exists(self.achievements_file):
                with open(self.achievements_file, 'r') as f:
                    return json.load(f)
            return []
        
        result = []
        def wrapped_load():
            nonlocal result
            result = load_operation()
        
        success = self._safe_file_operation(wrapped_load, "Error loading achievements")
        return result if success else []
    
    def save_achievements(self) -> bool:
        """Save achievements to file"""
        def save_operation():
            with open(self.achievements_file, 'w') as f:
                json.dump(self.achievements, f, indent=2, default=str)
        
        return self._safe_file_operation(save_operation, "Error saving achievements")
    
    def add_score(self, game_id: str, score: int, player_name: str = "Player", 
                  additional_data: Optional[Dict[str, Any]] = None) -> bool:
        """Add a new score and return True if it's a high score"""
        if game_id not in self.scores:
            self.scores[game_id] = []
        
        score_entry = {
            'score': score,
            'player': player_name,
            'date': self._get_current_timestamp(),
            'additional_data': additional_data or {}
        }
        
        self.scores[game_id].append(score_entry)
        
        # Sort by score (descending) and keep top 10
        self.scores[game_id].sort(key=lambda x: x['score'], reverse=True)
        self.scores[game_id] = self.scores[game_id][:10]
        
        # Check if it's a high score (top 10)
        is_high_score = score_entry in self.scores[game_id]
        
        if is_high_score:
            self.check_achievement('high_scorer')
        
        self.save_scores()
        return is_high_score
    
    def get_high_scores(self, game_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get high scores for a specific game"""
        return self.scores.get(game_id, [])[:limit]
    
    def get_all_high_scores(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get high scores for all games"""
        return self.scores
    
    def get_player_best_score(self, game_id: str, player_name: str = "Player") -> Optional[int]:
        """Get player's best score for a specific game"""
        game_scores = self.scores.get(game_id, [])
        player_scores = [score['score'] for score in game_scores if score['player'] == player_name]
        return max(player_scores) if player_scores else None
    
    def update_statistics(self, game_id: str, play_time: float = 0):
        """Update game statistics"""
        # Update games played
        if 'games_played' not in self.statistics:
            self.statistics['games_played'] = {}
        
        self.statistics['games_played'][game_id] = self.statistics['games_played'].get(game_id, 0) + 1
        
        # Update total time played
        if 'total_time_played' not in self.statistics:
            self.statistics['total_time_played'] = {}
        
        self.statistics['total_time_played'][game_id] = self.statistics['total_time_played'].get(game_id, 0) + play_time
        
        # Update dates and track unique play dates
        current_date = self._get_current_timestamp()
        current_date_only = current_date.split('T')[0]  # Get just the date part
        
        if not self.statistics.get('first_play_date'):
            self.statistics['first_play_date'] = current_date
        
        self.statistics['last_play_date'] = current_date
        
        # Track unique play dates for persistent achievement
        if 'unique_play_dates' not in self.statistics:
            self.statistics['unique_play_dates'] = []
        
        if current_date_only not in self.statistics['unique_play_dates']:
            self.statistics['unique_play_dates'].append(current_date_only)
        
        # Check achievements
        total_games_played = sum(self.statistics['games_played'].values())
        if total_games_played == 1:  # First game ever
            self.check_achievement('first_game')
        
        # Check if played all games
        if len(self.statistics['games_played']) >= 5:
            self.check_achievement('multi_player')
        
        # Check persistent player achievement
        if len(self.statistics['unique_play_dates']) >= 10:
            self.check_achievement('persistent')
        
        self.save_statistics()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get all statistics"""
        return self.statistics
    
    def get_game_statistics(self, game_id: str) -> Dict[str, Any]:
        """Get statistics for a specific game"""
        return {
            'games_played': self.statistics.get('games_played', {}).get(game_id, 0),
            'total_time': self.statistics.get('total_time_played', {}).get(game_id, 0),
            'best_score': self.get_player_best_score(game_id)
        }
    
    def check_achievement(self, achievement_id: str, **kwargs) -> bool:
        """Check and unlock achievement if conditions are met"""
        # Check if already earned
        if achievement_id in self.earned_achievement_ids:
            return False
        
        # Achievement logic with proper conditions
        should_earn = False
        
        if achievement_id == 'first_game':
            # Only earn on first game play
            total_games = sum(self.statistics.get('games_played', {}).values())
            should_earn = total_games <= 1
        
        elif achievement_id == 'quiz_master':
            # This would be called from the quiz game with streak info
            should_earn = kwargs.get('correct_streak', 0) >= 10
        
        elif achievement_id == 'snake_charmer':
            should_earn = kwargs.get('score', 0) >= 100
        
        elif achievement_id == 'memory_expert':
            should_earn = kwargs.get('time', float('inf')) < 60
        
        elif achievement_id == 'tetris_champion':
            should_earn = kwargs.get('lines_cleared', 0) >= 10
        
        elif achievement_id == 'puzzle_solver':
            should_earn = kwargs.get('highest_tile', 0) >= 1024
        
        elif achievement_id == 'multi_player':
            should_earn = len(self.statistics.get('games_played', {})) >= 5
        
        elif achievement_id == 'high_scorer':
            # Only earn if not already earned (called when achieving high score)
            should_earn = True
        
        elif achievement_id == 'persistent':
            # Check if played on 10 different days
            unique_dates = len(self.statistics.get('unique_play_dates', []))
            should_earn = unique_dates >= 10
        
        elif achievement_id == 'speedster':
            should_earn = kwargs.get('under_target_time', False)
        
        if should_earn:
            achievement_data = self.achievement_definitions.get(achievement_id, {})
            new_achievement = {
                'id': achievement_id,
                'name': achievement_data.get('name', achievement_id),
                'description': achievement_data.get('description', ''),
                'icon': achievement_data.get('icon', '🏆'),
                'earned_date': self._get_current_timestamp()
            }
            
            self.achievements.append(new_achievement)
            self.earned_achievement_ids.add(achievement_id)
            
            self.statistics['achievements_earned'] = len(self.achievements)
            
            # Save both achievements and statistics
            if self.save_achievements() and self.save_statistics():
                return True
            else:
                # Rollback if save failed
                self.achievements.pop()
                self.earned_achievement_ids.discard(achievement_id)
                self.statistics['achievements_earned'] = len(self.achievements)
                return False
        
        return False
    
    def get_achievements(self) -> List[Dict[str, Any]]:
        """Get all earned achievements"""
        return self.achievements
    
    def get_achievement_progress(self) -> Dict[str, Any]:
        """Get achievement progress information"""
        total_achievements = len(self.achievement_definitions)
        earned_achievements = len(self.achievements)
        
        return {
            'total': total_achievements,
            'earned': earned_achievements,
            'percentage': (earned_achievements / total_achievements) * 100 if total_achievements > 0 else 0,
            'available': [
                {
                    'id': aid,
                    'name': data['name'],
                    'description': data['description'],
                    'icon': data['icon']
                }
                for aid, data in self.achievement_definitions.items()
                if aid not in self.earned_achievement_ids
            ]
        }
    
    def export_data(self, filepath: str) -> bool:
        """Export all data to a file"""
        def export_operation():
            export_data = {
                'scores': self.scores,
                'statistics': self.statistics,
                'achievements': self.achievements,
                'export_date': self._get_current_timestamp(),
                'version': '1.0'  # For future compatibility
            }
            
            with open(filepath, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
        
        return self._safe_file_operation(export_operation, "Error exporting data")
    
    def import_data(self, filepath: str) -> bool:
        """Import data from a file with duplicate prevention"""
        def import_operation():
            with open(filepath, 'r') as f:
                import_data = json.load(f)
            
            # Merge scores with duplicate prevention
            if 'scores' in import_data:
                for game_id, scores in import_data['scores'].items():
                    if game_id not in self.scores:
                        self.scores[game_id] = []
                    
                    # Create a set of existing score signatures to prevent duplicates
                    existing_signatures = {
                        (score['score'], score['player'], score.get('date', ''))
                        for score in self.scores[game_id]
                    }
                    
                    # Only add scores that don't already exist
                    for score in scores:
                        signature = (score['score'], score['player'], score.get('date', ''))
                        if signature not in existing_signatures:
                            self.scores[game_id].append(score)
                            existing_signatures.add(signature)
                    
                    # Sort and keep top 10
                    self.scores[game_id].sort(key=lambda x: x['score'], reverse=True)
                    self.scores[game_id] = self.scores[game_id][:10]
            
            # Merge achievements with duplicate prevention
            if 'achievements' in import_data:
                for achievement in import_data['achievements']:
                    if achievement['id'] not in self.earned_achievement_ids:
                        self.achievements.append(achievement)
                        self.earned_achievement_ids.add(achievement['id'])
        
        success = self._safe_file_operation(import_operation, "Error importing data")
        
        if success:
            # Save merged data
            return (self.save_scores() and 
                   self.save_achievements() and 
                   self.save_statistics())
        
        return False
    
    def reset_all_data(self) -> bool:
        """Reset all scores, statistics, and achievements"""
        try:
            self.scores = {}
            self.statistics = {
                'games_played': {},
                'total_time_played': {},
                'first_play_date': None,
                'last_play_date': None,
                'total_sessions': 0,
                'achievements_earned': 0,
                'unique_play_dates': []
            }
            self.achievements = []
            self.earned_achievement_ids = set()
            
            # Save all reset data
            return (self.save_scores() and 
                   self.save_statistics() and 
                   self.save_achievements())
        
        except Exception as e:
            print(f"Error resetting data: {e}")
            return False