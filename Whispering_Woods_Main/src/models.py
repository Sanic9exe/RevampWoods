"""Data models and classes."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable, Tuple
from datetime import datetime
import random

from .utils import (
    ItemType, CreatureType, Weather, TimeOfDay, StatusEffect, DifficultyMode, SkillType
)

# ============================================================================
# ROUTE CLASS FOR NUMBERED NAVIGATION
# ============================================================================

@dataclass
class Route:
    """Represents a numbered route option."""
    number: int
    destination: str
    description: str
    visible: bool = True
    requires_item: Optional[str] = None
    requires_skill: Optional[Tuple[SkillType, int]] = None
    blocked_message: str = ""
    danger_level: int = 0
    hidden: bool = False
    one_way: bool = False
    
    def is_accessible(self, player: 'Player') -> Tuple[bool, str]:
        """Check if the route is accessible to the player."""
        if self.requires_item:
            if not player.has_item(self.requires_item):
                return False, f"You need a {self.requires_item} to go this way."
        
        if self.requires_skill:
            skill_type, level = self.requires_skill
            if player.skills.get(skill_type, 0) < level:
                return False, f"Your {skill_type.value} skill is not high enough."
        
        return True, ""



# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class Item:
    """Represents an item in the game."""
    name: str
    description: str
    item_type: ItemType
    weight: float = 1.0
    value: int = 0
    usable: bool = False
    equippable: bool = False
    stackable: bool = False
    quantity: int = 1
    damage: int = 0
    defense: int = 0
    healing: int = 0
    light_radius: int = 0
    durability: int = 100
    max_durability: int = 100
    special_effects: Dict[str, Any] = field(default_factory=dict)
    rarity: str = "common"
    level_requirement: int = 1
    
    def get_rarity_color(self) -> str:
        """Get color based on item rarity."""
        rarity_colors = {
            "common": Colors.WHITE,
            "uncommon": Colors.GREEN,
            "rare": Colors.BLUE,
            "epic": Colors.MAGENTA,
            "legendary": Colors.BOLD_YELLOW,
            "mythic": Colors.BOLD_RED
        }
        return rarity_colors.get(self.rarity, Colors.WHITE)
    
    def use_effect(self, player: 'Player') -> str:
        """Apply the item's effect when used."""
        results = []
        
        if self.healing > 0:
            healed = min(self.healing, player.max_health - player.health)
            player.health += healed
            results.append(f"Restored {healed} health.")
        
        if "hunger" in self.special_effects:
            restored = min(self.special_effects["hunger"], 100 - player.hunger)
            player.hunger += restored
            results.append(f"Restored {restored}% hunger.")
        
        if "thirst" in self.special_effects:
            restored = min(self.special_effects["thirst"], 100 - player.thirst)
            player.thirst += restored
            results.append(f"Restored {restored}% thirst.")
        
        if "stamina" in self.special_effects:
            restored = min(self.special_effects["stamina"], player.max_stamina - player.stamina)
            player.stamina += restored
            results.append(f"Restored {restored} stamina.")
        
        if "cure_poison" in self.special_effects:
            if "poison" in player.status_effects:
                del player.status_effects["poison"]
                results.append("Cured poison.")
        
        if "sanity" in self.special_effects:
            restored = min(self.special_effects["sanity"], 100 - player.sanity)
            player.sanity += restored
            results.append(f"Restored {restored}% sanity.")
        
        if results:
            return f"You used {self.name}. " + " ".join(results)
        return f"You used {self.name}."
    
    def to_dict(self) -> Dict:
        """Convert item to dictionary for saving."""
        return {
            'name': self.name,
            'description': self.description,
            'item_type': self.item_type.name,
            'weight': self.weight,
            'value': self.value,
            'usable': self.usable,
            'equippable': self.equippable,
            'stackable': self.stackable,
            'quantity': self.quantity,
            'damage': self.damage,
            'defense': self.defense,
            'healing': self.healing,
            'light_radius': self.light_radius,
            'durability': self.durability,
            'max_durability': self.max_durability,
            'special_effects': self.special_effects,
            'rarity': self.rarity,
            'level_requirement': self.level_requirement
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Item':
        """Create item from dictionary."""
        return Item(
            name=data['name'],
            description=data['description'],
            item_type=ItemType[data['item_type']],
            weight=data.get('weight', 1.0),
            value=data.get('value', 0),
            usable=data.get('usable', False),
            equippable=data.get('equippable', False),
            stackable=data.get('stackable', False),
            quantity=data.get('quantity', 1),
            damage=data.get('damage', 0),
            defense=data.get('defense', 0),
            healing=data.get('healing', 0),
            light_radius=data.get('light_radius', 0),
            durability=data.get('durability', 100),
            max_durability=data.get('max_durability', 100),
            special_effects=data.get('special_effects', {}),
            rarity=data.get('rarity', 'common'),
            level_requirement=data.get('level_requirement', 1)
        )

@dataclass
class Creature:
    """Represents a creature in the game."""
    name: str
    description: str
    creature_type: CreatureType
    health: int
    max_health: int
    damage: int
    defense: int
    experience: int = 10
    loot: List[str] = field(default_factory=list)
    loot_chance: int = 50
    dialogue: List[str] = field(default_factory=list)
    hostile: bool = False
    alive: bool = True
    special_abilities: List[str] = field(default_factory=list)
    weakness: Optional[str] = None
    resistance: Optional[str] = None
    level: int = 1
    gold_drop: Tuple[int, int] = (0, 10)
    respawn: bool = True
    unique_id: str = ""
    
    def __post_init__(self):
        if not self.unique_id:
            self.unique_id = f"{self.name}_{random.randint(1000, 9999)}"
    
    def attack(self) -> Tuple[int, str]:
        """Calculate creature's attack damage and return with description."""
        base_damage = max(1, self.damage + roll_dice(6, modifier=-3))
        
        # Check for special abilities
        ability_used = ""
        if self.special_abilities and chance(30):
            ability = random.choice(self.special_abilities)
            ability_used = ability
            if ability == "poison":
                base_damage += 2
            elif ability == "rage":
                base_damage = int(base_damage * 1.5)
            elif ability == "vampiric":
                self.health = min(self.max_health, self.health + base_damage // 2)
        
        return base_damage, ability_used
    
    def take_damage(self, amount: int, damage_type: str = "physical") -> int:
        """Apply damage to creature and return actual damage dealt."""
        # Check weakness
        if self.weakness and self.weakness.lower() in damage_type.lower():
            amount = int(amount * 1.5)
        
        # Check resistance
        if self.resistance and self.resistance.lower() in damage_type.lower():
            amount = int(amount * 0.5)
        
        actual_damage = max(1, amount - self.defense // 2)
        self.health -= actual_damage
        
        if self.health <= 0:
            self.alive = False
            self.health = 0
        
        return actual_damage
    
    def get_dialogue(self) -> str:
        """Get random dialogue from creature."""
        if self.dialogue:
            return random.choice(self.dialogue)
        return f"The {self.name} stares at you silently."
    
    def get_loot(self) -> List[str]:
        """Get loot dropped by creature."""
        dropped_loot = []
        for item in self.loot:
            if chance(self.loot_chance):
                dropped_loot.append(item)
        return dropped_loot
    
    def get_gold_drop(self) -> int:
        """Get random gold drop amount."""
        return random.randint(self.gold_drop[0], self.gold_drop[1])

@dataclass
class Quest:
    """Represents a quest in the game."""
    quest_id: str
    name: str
    description: str
    objectives: List[str]
    completed_objectives: List[bool] = field(default_factory=list)
    rewards: List[str] = field(default_factory=list)
    experience_reward: int = 50
    gold_reward: int = 0
    is_complete: bool = False
    is_active: bool = False
    is_failed: bool = False
    prerequisite_quests: List[str] = field(default_factory=list)
    time_limit: int = 0
    time_remaining: int = 0
    quest_giver: str = ""
    quest_type: str = "main"
    
    def __post_init__(self):
        if not self.completed_objectives:
            self.completed_objectives = [False] * len(self.objectives)
        if self.time_limit > 0 and self.time_remaining == 0:
            self.time_remaining = self.time_limit
    
    def complete_objective(self, index: int) -> bool:
        """Mark an objective as complete."""
        if 0 <= index < len(self.objectives):
            self.completed_objectives[index] = True
            if all(self.completed_objectives):
                self.is_complete = True
            return True
        return False
    
    def check_objective(self, objective_text: str) -> bool:
        """Check and complete an objective by text match."""
        for i, obj in enumerate(self.objectives):
            if objective_text.lower() in obj.lower() and not self.completed_objectives[i]:
                self.completed_objectives[i] = True
                if all(self.completed_objectives):
                    self.is_complete = True
                return True
        return False
    
    def get_progress(self) -> str:
        """Get quest progress string."""
        completed = sum(self.completed_objectives)
        total = len(self.objectives)
        percentage = int((completed / total) * 100)
        bar = "█" * (percentage // 10) + "░" * (10 - percentage // 10)
        return f"[{bar}] {completed}/{total} ({percentage}%)"
    
    def update_time(self, minutes: int):
        """Update time remaining for timed quests."""
        if self.time_limit > 0 and not self.is_complete:
            self.time_remaining -= minutes
            if self.time_remaining <= 0:
                self.is_failed = True
                self.time_remaining = 0

@dataclass
class CraftingRecipe:
    """Represents a crafting recipe."""
    recipe_id: str
    name: str
    result_item: str
    result_quantity: int = 1
    ingredients: Dict[str, int] = field(default_factory=dict)
    required_skill: SkillType = SkillType.CRAFTING
    skill_level_required: int = 1
    description: str = ""
    crafting_time: int = 1
    tool_required: Optional[str] = None
    
    def can_craft(self, inventory: List['Item'], skill_level: int) -> Tuple[bool, str]:
        """Check if recipe can be crafted."""
        if skill_level < self.skill_level_required:
            return False, f"Requires {self.required_skill.value} level {self.skill_level_required}"
        
        inv_counts = {}
        for item in inventory:
            inv_counts[item.name.lower()] = inv_counts.get(item.name.lower(), 0) + item.quantity
        
        for ingredient, amount in self.ingredients.items():
            if inv_counts.get(ingredient.lower(), 0) < amount:
                return False, f"Missing {ingredient} (need {amount})"
        
        return True, "Can craft"

@dataclass
class Achievement:
    """Represents an achievement."""
    achievement_id: str
    name: str
    description: str
    hidden: bool = False
    unlocked: bool = False
    unlock_date: str = ""
    points: int = 10
    category: str = "general"
    
    def unlock(self):
        """Unlock the achievement."""
        if not self.unlocked:
            self.unlocked = True
            self.unlock_date = datetime.now().strftime("%Y-%m-%d %H:%M")
            return True
        return False


