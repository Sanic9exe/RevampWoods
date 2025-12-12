"""Save and load system."""

import json
import os
from typing import Dict, Optional, Any
from datetime import datetime

from .utils import SAVE_FILE
from .colors import Colors

# ============================================================================
# SAVE/LOAD SYSTEM
# ============================================================================

class SaveLoadSystem:
    """Handles saving and loading game state."""
    
    @staticmethod
    def save_game(game: 'Game', filename: str = SAVE_FILE) -> bool:
        """Save the game to a file."""
        try:
            save_data = {
                'version': GAME_VERSION,
                'timestamp': datetime.now().isoformat(),
                'player': game.player.to_dict(),
                'time_weather': {
                    'game_minutes': game.time_weather.game_minutes,
                    'current_weather': game.time_weather.current_weather.name,
                    'weather_duration': game.time_weather.weather_duration,
                    'day_count': game.time_weather.day_count
                },
                'settings': SETTINGS.to_dict(),
                'world_state': SaveLoadSystem._save_world_state(game.world)
            }
            
            with open(filename, 'w') as f:
                json.dump(save_data, f, indent=2)
            
            slow_print(colored_text(f"Game saved to {filename}.", Colors.GREEN))
            log_event(f"Game saved to {filename}")
            return True
        except Exception as e:
            slow_print(colored_text(f"Failed to save game: {e}", Colors.RED))
            return False
    
    @staticmethod
    def load_game(filename: str = SAVE_FILE) -> Optional['Game']:
        """Load a game from a file."""
        try:
            if not os.path.exists(filename):
                slow_print(colored_text("No save file found.", Colors.RED))
                return None
            
            with open(filename, 'r') as f:
                save_data = json.load(f)
            
            # Create game instance
            game = Game()
            
            # Load player
            game.player = Player.from_dict(save_data['player'])
            
            # Load time/weather
            tw_data = save_data.get('time_weather', {})
            game.time_weather.game_minutes = tw_data.get('game_minutes', 480)
            game.time_weather.current_weather = Weather[tw_data.get('current_weather', 'CLEAR')]
            game.time_weather.weather_duration = tw_data.get('weather_duration', 60)
            game.time_weather.day_count = tw_data.get('day_count', 1)
            
            # Load settings
            SETTINGS.from_dict(save_data.get('settings', {}))
            
            # Load world state
            SaveLoadSystem._load_world_state(game.world, save_data.get('world_state', {}))
            
            slow_print(colored_text(f"Game loaded from {filename}.", Colors.GREEN))
            log_event(f"Game loaded from {filename}")
            return game
        except Exception as e:
            slow_print(colored_text(f"Failed to load game: {e}", Colors.RED))
            return None
    
    @staticmethod
    def _save_world_state(world: Dict[str, Location]) -> Dict:
        """Save the state of modified locations."""
        state = {}
        for loc_id, location in world.items():
            if location.visited or location.treasure_found or not location.items:
                state[loc_id] = {
                    'visited': location.visited,
                    'visit_count': location.visit_count,
                    'treasure_found': location.treasure_found,
                    'items': [item.to_dict() for item in location.items],
                    'creatures': [
                        {'name': c.name, 'alive': c.alive, 'health': c.health}
                        for c in location.creatures
                    ]
                }
        return state
    
    @staticmethod
    def _load_world_state(world: Dict[str, Location], state: Dict):
        """Load the state of modified locations."""
        for loc_id, loc_state in state.items():
            if loc_id in world:
                location = world[loc_id]
                location.visited = loc_state.get('visited', False)
                location.visit_count = loc_state.get('visit_count', 0)
                location.treasure_found = loc_state.get('treasure_found', False)
                
                # Load items
                location.items = [
                    Item.from_dict(item_data) 
                    for item_data in loc_state.get('items', [])
                ]
                
                # Update creature states
                for c_state in loc_state.get('creatures', []):
                    for creature in location.creatures:
                        if creature.name == c_state['name']:
                            creature.alive = c_state['alive']
                            creature.health = c_state['health']





