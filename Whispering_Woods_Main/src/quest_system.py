"""Quest system."""

from typing import Dict, List, Optional
import random

from .models import Quest, Item, Creature
from .utils import QuestType, QuestStatus, slow_print
from .colors import Colors

# ============================================================================
# QUEST SYSTEM
# ============================================================================

class QuestSystem:
    """Manages game quests."""
    
    _quests: Dict[str, Quest] = {}
    
    @classmethod
    def initialize_quests(cls):
        """Initialize all available quests."""
        cls._quests = {
            "escape_forest": Quest(
                quest_id="escape_forest",
                name="Escape the Whispering Woods",
                description="Find a way out of this mysterious forest.",
                objectives=[
                    "Explore the forest to find clues",
                    "Find the tower key",
                    "Reach the tower",
                    "Defeat the guardian",
                    "Escape through the portal"
                ],
                experience_reward=500,
                gold_reward=0,
                quest_type="main"
            ),
            "help_hermit": Quest(
                quest_id="help_hermit",
                name="The Hermit's Request",
                description="Help the old hermit with his problems.",
                objectives=[
                    "Speak with the hermit",
                    "Collect 5 healing herbs",
                    "Return to the hermit"
                ],
                rewards=["healing potion", "healing potion", "map fragment"],
                experience_reward=100,
                gold_reward=50,
                quest_giver="hermit",
                quest_type="side"
            ),
            "witch_bargain": Quest(
                quest_id="witch_bargain",
                name="The Witch's Bargain",
                description="The witch will help you... for a price.",
                objectives=[
                    "Speak with the witch",
                    "Bring her 3 spider silk",
                    "Bring her a spirit essence",
                    "Receive her aid"
                ],
                rewards=["tower key", "greater healing potion"],
                experience_reward=150,
                gold_reward=0,
                quest_giver="witch",
                quest_type="side"
            ),
            "free_prisoners": Quest(
                quest_id="free_prisoners",
                name="Liberation",
                description="Free the prisoners from the goblin slave pens.",
                objectives=[
                    "Find the goblin warren",
                    "Get the cage keys",
                    "Free the prisoners",
                    "Escort them to safety"
                ],
                rewards=["gold coins", "gold coins", "gemstone"],
                experience_reward=200,
                gold_reward=100,
                quest_type="side"
            ),
            "defeat_guardian": Quest(
                quest_id="defeat_guardian",
                name="The Forest Guardian",
                description="The Guardian of the forest has been corrupted. Free it or destroy it.",
                objectives=[
                    "Find the corrupted grove",
                    "Confront the Forest Guardian",
                    "Cleanse or destroy the corruption"
                ],
                rewards=["forest heart", "guardian token"],
                experience_reward=400,
                gold_reward=200,
                quest_type="main"
            ),
            "dragon_threat": Quest(
                quest_id="dragon_threat",
                name="The Dragon's Lair",
                description="A dragon lurks in the mountains. Slay it or bargain with it.",
                objectives=[
                    "Find the volcanic chamber",
                    "Confront the dragon",
                    "Survive the encounter"
                ],
                rewards=["dragon scale", "flame sword"],
                experience_reward=1000,
                gold_reward=500,
                quest_type="legendary"
            ),
        }
    
    @classmethod
    def get_quest(cls, quest_id: str) -> Optional[Quest]:
        """Get a quest by ID."""
        if not cls._quests:
            cls.initialize_quests()
        return cls._quests.get(quest_id)
    
    @classmethod
    def start_quest(cls, quest_id: str, player: Player) -> str:
        """Start a quest for the player."""
        if not cls._quests:
            cls.initialize_quests()
        
        quest = cls._quests.get(quest_id)
        if not quest:
            return colored_text("Quest not found.", Colors.RED)
        
        # Check if already active or completed
        for active_quest in player.active_quests:
            if active_quest.quest_id == quest_id:
                return colored_text("Quest already active.", Colors.YELLOW)
        
        if quest_id in player.completed_quests:
            return colored_text("Quest already completed.", Colors.YELLOW)
        
        # Create a copy of the quest for the player
        import copy
        player_quest = copy.deepcopy(quest)
        player_quest.is_active = True
        player.active_quests.append(player_quest)
        
        print_event_box(
            f"New Quest: {quest.name}\n\n{quest.description}",
            EventType.QUEST
        )
        
        return colored_text(f"Quest '{quest.name}' started!", Colors.BOLD_YELLOW)
    
    @classmethod
    def complete_quest(cls, quest_id: str, player: Player) -> str:
        """Complete a quest and give rewards."""
        for quest in player.active_quests:
            if quest.quest_id == quest_id and quest.is_complete:
                # Give rewards
                player.gain_experience(quest.experience_reward)
                player.gold += quest.gold_reward
                
                for item_name in quest.rewards:
                    item = ItemFactory.create_item(item_name)
                    if item:
                        player.add_item(item)
                
                player.completed_quests.append(quest_id)
                player.active_quests.remove(quest)
                
                rewards_text = f"Experience: +{quest.experience_reward}\n"
                if quest.gold_reward > 0:
                    rewards_text += f"Gold: +{quest.gold_reward}\n"
                if quest.rewards:
                    rewards_text += f"Items: {', '.join(quest.rewards)}"
                
                print_event_box(
                    f"Quest Complete: {quest.name}\n\nRewards:\n{rewards_text}",
                    EventType.QUEST
                )
                
                return colored_text(f"Quest '{quest.name}' completed!", Colors.BOLD_GREEN)
        
        return colored_text("Quest not found or not complete.", Colors.RED)



