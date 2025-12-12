"""Achievement system."""

from typing import Dict, List, Set
from datetime import datetime
import random

from .models import Achievement
from .utils import slow_print
from .colors import Colors

# ============================================================================
# ACHIEVEMENT SYSTEM
# ============================================================================

class AchievementSystem:
    """Manages game achievements."""
    
    _achievements: Dict[str, Achievement] = {}
    
    @classmethod
    def initialize_achievements(cls):
        """Initialize all achievements."""
        cls._achievements = {
            "first_steps": Achievement(
                achievement_id="first_steps",
                name="First Steps",
                description="Take your first steps in the forest.",
                points=10
            ),
            "explorer": Achievement(
                achievement_id="explorer",
                name="Explorer",
                description="Discover 25 different locations.",
                points=25
            ),
            "cartographer": Achievement(
                achievement_id="cartographer",
                name="Cartographer",
                description="Discover all locations in the forest.",
                points=100
            ),
            "first_blood": Achievement(
                achievement_id="first_blood",
                name="First Blood",
                description="Defeat your first enemy.",
                points=10
            ),
            "hunter": Achievement(
                achievement_id="hunter",
                name="Hunter",
                description="Defeat 25 enemies.",
                points=25
            ),
            "slayer": Achievement(
                achievement_id="slayer",
                name="Slayer",
                description="Defeat 100 enemies.",
                points=50
            ),
            "boss_slayer": Achievement(
                achievement_id="boss_slayer",
                name="Boss Slayer",
                description="Defeat a boss creature.",
                points=50
            ),
            "dragon_slayer": Achievement(
                achievement_id="dragon_slayer",
                name="Dragon Slayer",
                description="Defeat the ancient dragon.",
                points=100,
                hidden=True
            ),
            "survivor": Achievement(
                achievement_id="survivor",
                name="Survivor",
                description="Survive for 7 days in the forest.",
                points=50
            ),
            "wealthy": Achievement(
                achievement_id="wealthy",
                name="Wealthy",
                description="Accumulate 1000 gold.",
                points=25
            ),
            "master_crafter": Achievement(
                achievement_id="master_crafter",
                name="Master Crafter",
                description="Craft 50 items.",
                points=50
            ),
            "treasure_hunter": Achievement(
                achievement_id="treasure_hunter",
                name="Treasure Hunter",
                description="Find 10 treasures.",
                points=25
            ),
            "quest_master": Achievement(
                achievement_id="quest_master",
                name="Quest Master",
                description="Complete all side quests.",
                points=100
            ),
            "escape_artist": Achievement(
                achievement_id="escape_artist",
                name="Escape Artist",
                description="Escape the Whispering Woods.",
                points=200
            ),
            "pacifist": Achievement(
                achievement_id="pacifist",
                name="Pacifist",
                description="Escape without killing any creatures.",
                points=100,
                hidden=True
            ),
            "speedrunner": Achievement(
                achievement_id="speedrunner",
                name="Speedrunner",
                description="Escape in under 3 days.",
                points=100,
                hidden=True
            ),
        }
    
    @classmethod
    def check_achievements(cls, player: Player):
        """Check and unlock any earned achievements."""
        if not cls._achievements:
            cls.initialize_achievements()
        
        unlocked = []
        
        # First Steps
        if player.steps_taken >= 1:
            unlocked.append(cls._try_unlock("first_steps", player))
        
        # Explorer
        if len(player.discovered_locations) >= 25:
            unlocked.append(cls._try_unlock("explorer", player))
        
        # First Blood
        if player.kills >= 1:
            unlocked.append(cls._try_unlock("first_blood", player))
        
        # Hunter
        if player.kills >= 25:
            unlocked.append(cls._try_unlock("hunter", player))
        
        # Slayer
        if player.kills >= 100:
            unlocked.append(cls._try_unlock("slayer", player))
        
        # Boss Slayer
        if player.boss_kills >= 1:
            unlocked.append(cls._try_unlock("boss_slayer", player))
        
        # Wealthy
        if player.gold >= 1000:
            unlocked.append(cls._try_unlock("wealthy", player))
        
        # Master Crafter
        if player.items_crafted >= 50:
            unlocked.append(cls._try_unlock("master_crafter", player))
        
        # Treasure Hunter
        if player.treasures_found >= 10:
            unlocked.append(cls._try_unlock("treasure_hunter", player))
        
        # Display unlocked achievements
        for achievement in unlocked:
            if achievement:
                print_event_box(
                    f"🏆 {achievement.name}\n\n{achievement.description}\n\n+{achievement.points} points",
                    EventType.ACHIEVEMENT
                )
    
    @classmethod
    def _try_unlock(cls, achievement_id: str, player: Player) -> Optional[Achievement]:
        """Try to unlock an achievement."""
        if achievement_id in player.achievements:
            return None
        
        achievement = cls._achievements.get(achievement_id)
        if achievement and achievement.unlock():
            player.achievements.append(achievement_id)
            player.unlocked_achievements[achievement_id] = achievement
            return achievement
        return None
    
    @classmethod
    def get_achievements_display(cls, player: Player) -> str:
        """Get formatted display of achievements."""
        if not cls._achievements:
            cls.initialize_achievements()
        
        lines = [colored_text("╔══════════════════════════════════════════════════════════════╗", Colors.BOLD_YELLOW)]
        lines.append(colored_text("║                       ACHIEVEMENTS                           ║", Colors.BOLD_YELLOW))
        lines.append(colored_text("║══════════════════════════════════════════════════════════════║", Colors.BOLD_YELLOW))
        
        total_points = 0
        unlocked_count = 0
        
        for achievement_id, achievement in cls._achievements.items():
            if achievement.hidden and achievement_id not in player.achievements:
                continue
            
            if achievement_id in player.achievements:
                status = colored_text("✓", Colors.GREEN)
                name_color = Colors.GREEN
                unlocked_count += 1
                total_points += achievement.points
            else:
                status = colored_text("○", Colors.DIM)
                name_color = Colors.DIM
            
            lines.append(f"║  {status} {colored_text(achievement.name, name_color)} (+{achievement.points})")
            lines.append(colored_text(f"║      {achievement.description}", Colors.DIM))
        
        lines.append(colored_text("║──────────────────────────────────────────────────────────────║", Colors.BOLD_YELLOW))
        lines.append(f"║  Unlocked: {unlocked_count}/{len(cls._achievements)}  |  Points: {total_points}")
        lines.append(colored_text("╚══════════════════════════════════════════════════════════════╝", Colors.BOLD_YELLOW))
        
        return "\n".join(lines)



