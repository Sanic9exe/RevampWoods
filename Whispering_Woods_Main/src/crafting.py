"""Crafting system."""

from typing import Dict, List, Optional, Tuple
import random

from .models import CraftingRecipe, Item
from .colors import Colors
from .utils import slow_print

# ============================================================================
# CRAFTING SYSTEM
# ============================================================================

class CraftingSystem:
    """Manages crafting recipes and crafting operations."""
    
    _recipes: Dict[str, CraftingRecipe] = {}
    
    @classmethod
    def initialize_recipes(cls):
        """Initialize all crafting recipes."""
        cls._recipes = {
            "torch": CraftingRecipe(
                recipe_id="torch",
                name="Torch",
                result_item="torch",
                ingredients={"wood": 1, "cloth": 1},
                skill_level_required=1,
                description="A simple torch for lighting dark places."
            ),
            "bandage": CraftingRecipe(
                recipe_id="bandage",
                name="Bandage",
                result_item="bandage",
                ingredients={"cloth": 2},
                skill_level_required=1,
                description="A cloth bandage for treating wounds."
            ),
            "rope": CraftingRecipe(
                recipe_id="rope",
                name="Rope",
                result_item="rope",
                ingredients={"cloth": 3},
                skill_level_required=2,
                description="A sturdy rope for climbing."
            ),
            "healing potion": CraftingRecipe(
                recipe_id="healing_potion",
                name="Healing Potion",
                result_item="healing potion",
                ingredients={"healing herb": 3, "fresh water": 1},
                skill_level_required=3,
                description="A potion that restores health."
            ),
            "antidote": CraftingRecipe(
                recipe_id="antidote",
                name="Antidote",
                result_item="antidote",
                ingredients={"healing herb": 2, "mushroom": 1},
                skill_level_required=3,
                description="Cures poison effects."
            ),
            "lantern": CraftingRecipe(
                recipe_id="lantern",
                name="Lantern",
                result_item="lantern",
                ingredients={"iron ore": 2, "cloth": 1},
                skill_level_required=4,
                description="A long-lasting light source."
            ),
            "iron sword": CraftingRecipe(
                recipe_id="iron_sword",
                name="Iron Sword",
                result_item="iron sword",
                ingredients={"iron ore": 5, "wood": 1},
                skill_level_required=5,
                description="A reliable iron sword."
            ),
            "leather vest": CraftingRecipe(
                recipe_id="leather_vest",
                name="Leather Vest",
                result_item="leather vest",
                ingredients={"wolf pelt": 2, "cloth": 2},
                skill_level_required=4,
                description="Basic armor for protection."
            ),
            "silver dagger": CraftingRecipe(
                recipe_id="silver_dagger",
                name="Silver Dagger",
                result_item="silver dagger",
                ingredients={"silver ore": 3, "wood": 1},
                skill_level_required=6,
                description="Effective against supernatural creatures."
            ),
            "greater healing potion": CraftingRecipe(
                recipe_id="greater_healing_potion",
                name="Greater Healing Potion",
                result_item="greater healing potion",
                ingredients={"healing potion": 2, "spirit essence": 1},
                skill_level_required=6,
                description="A powerful healing potion."
            ),
            "spirit ward": CraftingRecipe(
                recipe_id="spirit_ward",
                name="Spirit Ward",
                result_item="spirit ward",
                ingredients={"silver ore": 2, "spirit essence": 2, "cloth": 1},
                skill_level_required=7,
                description="Protects against spiritual attacks."
            ),
        }
    
    @classmethod
    def get_recipe(cls, recipe_id: str) -> Optional[CraftingRecipe]:
        """Get a recipe by ID."""
        if not cls._recipes:
            cls.initialize_recipes()
        return cls._recipes.get(recipe_id.lower())
    
    @classmethod
    def get_all_recipes(cls) -> Dict[str, CraftingRecipe]:
        """Get all crafting recipes."""
        if not cls._recipes:
            cls.initialize_recipes()
        return cls._recipes.copy()
    
    @classmethod
    def craft_item(cls, recipe_id: str, player: 'Player') -> Tuple[bool, str]:
        """Attempt to craft an item."""
        if not cls._recipes:
            cls.initialize_recipes()
        
        recipe = cls._recipes.get(recipe_id.lower())
        if not recipe:
            return False, colored_text("Unknown recipe.", Colors.RED)
        
        if recipe_id not in player.known_recipes:
            return False, colored_text("You don't know this recipe.", Colors.RED)
        
        skill_level = player.skills.get(recipe.required_skill, 1)
        can_craft, reason = recipe.can_craft(player.inventory, skill_level)
        
        if not can_craft:
            return False, colored_text(f"Cannot craft: {reason}", Colors.RED)
        
        # Remove ingredients
        for ingredient, amount in recipe.ingredients.items():
            player.remove_item(ingredient, amount)
        
        # Create result item
        result_item = ItemFactory.create_item(recipe.result_item)
        if result_item:
            result_item.quantity = recipe.result_quantity
            success, msg = player.add_item(result_item)
            if success:
                player.items_crafted += 1
                # Chance to improve skill
                if chance(30):
                    player.improve_skill(recipe.required_skill)
                return True, colored_text(
                    f"Successfully crafted {recipe.result_quantity}x {result_item.name}!",
                    Colors.GREEN
                )
            return False, msg
        
        return False, colored_text("Failed to create item.", Colors.RED)
    
    @classmethod
    def get_craftable_display(cls, player: 'Player') -> str:
        """Get display of recipes the player can craft."""
        if not cls._recipes:
            cls.initialize_recipes()
        
        lines = [colored_text("╔══════════════════════════════════════════════════════════════╗", Colors.CYAN)]
        lines.append(colored_text("║                     CRAFTING RECIPES                         ║", Colors.CYAN))
        lines.append(colored_text("║══════════════════════════════════════════════════════════════║", Colors.CYAN))
        
        for recipe_id in player.known_recipes:
            recipe = cls._recipes.get(recipe_id)
            if not recipe:
                continue
            
            skill_level = player.skills.get(recipe.required_skill, 1)
            can_craft, reason = recipe.can_craft(player.inventory, skill_level)
            
            if can_craft:
                status = colored_text("[CAN CRAFT]", Colors.GREEN)
            else:
                status = colored_text(f"[{reason}]", Colors.RED)
            
            lines.append(f"║  {recipe.name}: {status}")
            
            ingredients_str = ", ".join([f"{v}x {k}" for k, v in recipe.ingredients.items()])
            lines.append(colored_text(f"║    Ingredients: {ingredients_str}", Colors.DIM))
        
        lines.append(colored_text("╚══════════════════════════════════════════════════════════════╝", Colors.CYAN))
        return "\n".join(lines)



