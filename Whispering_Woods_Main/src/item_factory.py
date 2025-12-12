"""Item factory for creating game items."""

import random
from typing import Dict, List, Optional

from .utils import ItemType
from .models import Item

# ============================================================================
# ITEM FACTORY
# ============================================================================

class ItemFactory:
    """Factory for creating game items."""
    
    _items_database: Dict[str, Dict] = {}
    
    @classmethod
    def initialize_database(cls):
        """Initialize the items database."""
        cls._items_database = {
            # ===== WEAPONS =====
            "rusty knife": {
                "name": "Rusty Knife",
                "description": "A weathered knife with a dull blade. Better than nothing.",
                "item_type": ItemType.WEAPON,
                "weight": 0.5, "value": 5, "equippable": True, "damage": 5,
                "rarity": "common"
            },
            "wooden club": {
                "name": "Wooden Club",
                "description": "A sturdy branch fashioned into a crude weapon.",
                "item_type": ItemType.WEAPON,
                "weight": 2.0, "value": 3, "equippable": True, "damage": 7,
                "rarity": "common"
            },
            "hunting knife": {
                "name": "Hunting Knife",
                "description": "A sharp knife designed for skinning game.",
                "item_type": ItemType.WEAPON,
                "weight": 0.4, "value": 15, "equippable": True, "damage": 8,
                "rarity": "common"
            },
            "iron sword": {
                "name": "Iron Sword",
                "description": "A standard iron sword, well-balanced and reliable.",
                "item_type": ItemType.WEAPON,
                "weight": 3.0, "value": 50, "equippable": True, "damage": 12,
                "rarity": "uncommon"
            },
            "hunting bow": {
                "name": "Hunting Bow",
                "description": "A well-crafted bow for hunting game.",
                "item_type": ItemType.WEAPON,
                "weight": 1.5, "value": 25, "equippable": True, "damage": 10,
                "rarity": "uncommon"
            },
            "silver dagger": {
                "name": "Silver Dagger",
                "description": "A gleaming dagger made of pure silver. Effective against supernatural creatures.",
                "item_type": ItemType.WEAPON,
                "weight": 0.5, "value": 75, "equippable": True, "damage": 8,
                "special_effects": {"silver": True},
                "rarity": "rare"
            },
            "ancient sword": {
                "name": "Ancient Sword",
                "description": "A magnificent sword from a forgotten age, still sharp as the day it was forged.",
                "item_type": ItemType.WEAPON,
                "weight": 3.0, "value": 200, "equippable": True, "damage": 18,
                "rarity": "epic"
            },
            "woodcutter axe": {
                "name": "Woodcutter's Axe",
                "description": "A heavy axe for chopping wood. Also effective in combat.",
                "item_type": ItemType.WEAPON,
                "weight": 3.5, "value": 20, "equippable": True, "damage": 14,
                "special_effects": {"chop_wood": True},
                "rarity": "common"
            },
            "enchanted staff": {
                "name": "Enchanted Staff",
                "description": "A wooden staff imbued with magical energy.",
                "item_type": ItemType.WEAPON,
                "weight": 2.0, "value": 150, "equippable": True, "damage": 10,
                "special_effects": {"magic_boost": 5},
                "rarity": "rare"
            },
            "flame sword": {
                "name": "Flame Sword",
                "description": "A sword wreathed in magical fire.",
                "item_type": ItemType.WEAPON,
                "weight": 3.5, "value": 300, "equippable": True, "damage": 20,
                "special_effects": {"fire": True, "light": 3},
                "rarity": "epic"
            },
            "frost blade": {
                "name": "Frost Blade",
                "description": "A blade of eternal ice that never melts.",
                "item_type": ItemType.WEAPON,
                "weight": 3.0, "value": 300, "equippable": True, "damage": 18,
                "special_effects": {"ice": True, "freeze_chance": 20},
                "rarity": "epic"
            },
            "shadow dagger": {
                "name": "Shadow Dagger",
                "description": "A dagger that seems to absorb light around it.",
                "item_type": ItemType.WEAPON,
                "weight": 0.3, "value": 250, "equippable": True, "damage": 15,
                "special_effects": {"stealth_bonus": 3, "critical_chance": 15},
                "rarity": "epic"
            },
            "guardian blade": {
                "name": "Guardian's Blade",
                "description": "The legendary sword of the Forest Guardian, pulsing with nature's power.",
                "item_type": ItemType.WEAPON,
                "weight": 4.0, "value": 1000, "equippable": True, "damage": 30,
                "special_effects": {"nature": True, "regenerate": 1},
                "rarity": "legendary",
                "level_requirement": 10
            },
            
            # ===== ARMOR =====
            "leather vest": {
                "name": "Leather Vest",
                "description": "A simple leather vest offering basic protection.",
                "item_type": ItemType.ARMOR,
                "weight": 2.0, "value": 20, "equippable": True, "defense": 5,
                "rarity": "common"
            },
            "ranger cloak": {
                "name": "Ranger's Cloak",
                "description": "A forest-green cloak that provides protection and camouflage.",
                "item_type": ItemType.ARMOR,
                "weight": 1.5, "value": 40, "equippable": True, "defense": 8,
                "special_effects": {"stealth_bonus": 2},
                "rarity": "uncommon"
            },
            "chainmail": {
                "name": "Chainmail Shirt",
                "description": "Interlocking metal rings provide excellent protection.",
                "item_type": ItemType.ARMOR,
                "weight": 8.0, "value": 100, "equippable": True, "defense": 15,
                "rarity": "rare"
            },
            "plate armor": {
                "name": "Plate Armor",
                "description": "Heavy plate armor offering superior protection.",
                "item_type": ItemType.ARMOR,
                "weight": 15.0, "value": 300, "equippable": True, "defense": 25,
                "special_effects": {"stamina_penalty": 10},
                "rarity": "epic"
            },
            "shadow cloak": {
                "name": "Shadow Cloak",
                "description": "A cloak woven from shadows themselves.",
                "item_type": ItemType.ARMOR,
                "weight": 0.5, "value": 400, "equippable": True, "defense": 10,
                "special_effects": {"stealth_bonus": 5, "shadow_step": True},
                "rarity": "epic"
            },
            "nature's embrace": {
                "name": "Nature's Embrace",
                "description": "Armor made of living vines and leaves.",
                "item_type": ItemType.ARMOR,
                "weight": 3.0, "value": 500, "equippable": True, "defense": 18,
                "special_effects": {"regenerate": 1, "poison_immunity": True},
                "rarity": "legendary"
            },
            
            # ===== TOOLS =====
            "rope": {
                "name": "Rope",
                "description": "A sturdy length of rope, useful for climbing and binding.",
                "item_type": ItemType.TOOL,
                "weight": 1.0, "value": 5,
                "special_effects": {"climbing_bonus": 3},
                "rarity": "common"
            },
            "lockpick": {
                "name": "Lockpick",
                "description": "A thin metal tool for opening locks.",
                "item_type": ItemType.TOOL,
                "weight": 0.1, "value": 15, "stackable": True,
                "durability": 3, "max_durability": 3,
                "rarity": "uncommon"
            },
            "shovel": {
                "name": "Shovel",
                "description": "A sturdy shovel for digging.",
                "item_type": ItemType.TOOL,
                "weight": 2.5, "value": 10,
                "rarity": "common"
            },
            "fishing rod": {
                "name": "Fishing Rod",
                "description": "A simple fishing rod with line and hook.",
                "item_type": ItemType.TOOL,
                "weight": 1.0, "value": 8,
                "rarity": "common"
            },
            "compass": {
                "name": "Compass",
                "description": "A magnetic compass that always points north.",
                "item_type": ItemType.TOOL,
                "weight": 0.2, "value": 30,
                "special_effects": {"navigation": True},
                "rarity": "uncommon"
            },
            "map fragment": {
                "name": "Map Fragment",
                "description": "A torn piece of an old map showing part of the forest.",
                "item_type": ItemType.TOOL,
                "weight": 0.1, "value": 20,
                "rarity": "uncommon"
            },
            "grappling hook": {
                "name": "Grappling Hook",
                "description": "A hook attached to rope for climbing difficult surfaces.",
                "item_type": ItemType.TOOL,
                "weight": 2.0, "value": 50,
                "special_effects": {"climbing_bonus": 5},
                "rarity": "rare"
            },
            "thieves tools": {
                "name": "Thieves' Tools",
                "description": "A complete set of lockpicking and trap-disarming tools.",
                "item_type": ItemType.TOOL,
                "weight": 0.5, "value": 100,
                "special_effects": {"lockpicking_bonus": 3},
                "rarity": "rare"
            },
            
            # ===== CONSUMABLES =====
            "healing herb": {
                "name": "Healing Herb",
                "description": "A medicinal plant with restorative properties.",
                "item_type": ItemType.CONSUMABLE,
                "weight": 0.1, "value": 5, "usable": True, "stackable": True,
                "healing": 15,
                "rarity": "common"
            },
            "healing potion": {
                "name": "Healing Potion",
                "description": "A red potion that restores health.",
                "item_type": ItemType.CONSUMABLE,
                "weight": 0.3, "value": 25, "usable": True, "stackable": True,
                "healing": 40,
                "rarity": "uncommon"
            },
            "greater healing potion": {
                "name": "Greater Healing Potion",
                "description": "A powerful red potion that restores significant health.",
                "item_type": ItemType.CONSUMABLE,
                "weight": 0.3, "value": 75, "usable": True, "stackable": True,
                "healing": 80,
                "rarity": "rare"
            },
            "antidote": {
                "name": "Antidote",
                "description": "A bitter medicine that cures poison.",
                "item_type": ItemType.CONSUMABLE,
                "weight": 0.2, "value": 20, "usable": True, "stackable": True,
                "special_effects": {"cure_poison": True},
                "rarity": "uncommon"
            },
            "dried meat": {
                "name": "Dried Meat",
                "description": "Preserved meat that restores hunger.",
                "item_type": ItemType.CONSUMABLE,
                "weight": 0.3, "value": 8, "usable": True, "stackable": True,
                "special_effects": {"hunger": 30},
                "rarity": "common"
            },
            "fresh water": {
                "name": "Fresh Water",
                "description": "Clean drinking water in a waterskin.",
                "item_type": ItemType.CONSUMABLE,
                "weight": 0.5, "value": 2, "usable": True, "stackable": True,
                "special_effects": {"thirst": 40},
                "rarity": "common"
            },
            "wild berries": {
                "name": "Wild Berries",
                "description": "A handful of edible forest berries.",
                "item_type": ItemType.CONSUMABLE,
                "weight": 0.1, "value": 2, "usable": True, "stackable": True,
                "special_effects": {"hunger": 10, "thirst": 5},
                "rarity": "common"
            },
            "mushroom": {
                "name": "Forest Mushroom",
                "description": "A common forest mushroom. Hopefully not poisonous.",
                "item_type": ItemType.CONSUMABLE,
                "weight": 0.1, "value": 3, "usable": True, "stackable": True,
                "special_effects": {"hunger": 15},
                "rarity": "common"
            },
            "stamina potion": {
                "name": "Stamina Potion",
                "description": "A green potion that restores energy.",
                "item_type": ItemType.CONSUMABLE,
                "weight": 0.3, "value": 20, "usable": True, "stackable": True,
                "special_effects": {"stamina": 50},
                "rarity": "uncommon"
            },
            "mana potion": {
                "name": "Mana Potion",
                "description": "A blue potion that restores magical energy.",
                "item_type": ItemType.CONSUMABLE,
                "weight": 0.3, "value": 30, "usable": True, "stackable": True,
                "special_effects": {"mana": 40},
                "rarity": "uncommon"
            },
            "strength potion": {
                "name": "Strength Potion",
                "description": "A bubbling potion that temporarily increases strength.",
                "item_type": ItemType.CONSUMABLE,
                "weight": 0.3, "value": 50, "usable": True, "stackable": True,
                "special_effects": {"buff_strength": 30},
                "rarity": "rare"
            },
            "invisibility potion": {
                "name": "Invisibility Potion",
                "description": "A shimmering potion that makes you invisible.",
                "item_type": ItemType.CONSUMABLE,
                "weight": 0.3, "value": 100, "usable": True, "stackable": True,
                "special_effects": {"invisible": 60},
                "rarity": "epic"
            },
            "elixir of life": {
                "name": "Elixir of Life",
                "description": "A legendary potion that fully restores health and cures all ailments.",
                "item_type": ItemType.CONSUMABLE,
                "weight": 0.3, "value": 500, "usable": True, "stackable": True,
                "healing": 999,
                "special_effects": {"cure_all": True, "remove_effects": True},
                "rarity": "legendary"
            },
            "cooked fish": {
                "name": "Cooked Fish",
                "description": "A freshly cooked fish, nutritious and satisfying.",
                "item_type": ItemType.CONSUMABLE,
                "weight": 0.3, "value": 10, "usable": True, "stackable": True,
                "special_effects": {"hunger": 40},
                "rarity": "common"
            },
            "traveler's ration": {
                "name": "Traveler's Ration",
                "description": "A compact package of dried food for long journeys.",
                "item_type": ItemType.CONSUMABLE,
                "weight": 0.5, "value": 15, "usable": True, "stackable": True,
                "special_effects": {"hunger": 50, "thirst": 20},
                "rarity": "common"
            },
            "bandage": {
                "name": "Bandage",
                "description": "A cloth bandage for treating wounds.",
                "item_type": ItemType.CONSUMABLE,
                "weight": 0.1, "value": 5, "usable": True, "stackable": True,
                "healing": 10,
                "special_effects": {"stop_bleeding": True},
                "rarity": "common"
            },
            "sanity tonic": {
                "name": "Sanity Tonic",
                "description": "A calming herbal mixture that restores mental clarity.",
                "item_type": ItemType.CONSUMABLE,
                "weight": 0.2, "value": 40, "usable": True, "stackable": True,
                "special_effects": {"sanity": 30},
                "rarity": "rare"
            },
            
            # ===== LIGHT SOURCES =====
            "torch": {
                "name": "Torch",
                "description": "A wooden torch that provides light.",
                "item_type": ItemType.LIGHT,
                "weight": 0.5, "value": 3, "equippable": True, "stackable": True,
                "light_radius": 5, "durability": 30, "max_durability": 30,
                "rarity": "common"
            },
            "lantern": {
                "name": "Lantern",
                "description": "An oil lantern providing steady light.",
                "item_type": ItemType.LIGHT,
                "weight": 1.0, "value": 20, "equippable": True,
                "light_radius": 8, "durability": 100, "max_durability": 100,
                "rarity": "uncommon"
            },
            "glowing crystal": {
                "name": "Glowing Crystal",
                "description": "A mysterious crystal that emits a soft, eternal glow.",
                "item_type": ItemType.LIGHT,
                "weight": 0.5, "value": 100, "equippable": True,
                "light_radius": 6, "durability": 999, "max_durability": 999,
                "rarity": "rare"
            },
            "sunstone": {
                "name": "Sunstone",
                "description": "A magical stone that radiates warm, sun-like light.",
                "item_type": ItemType.LIGHT,
                "weight": 0.3, "value": 200, "equippable": True,
                "light_radius": 10, "durability": 999, "max_durability": 999,
                "special_effects": {"undead_fear": True},
                "rarity": "epic"
            },
            
            # ===== KEYS =====
            "rusty key": {
                "name": "Rusty Key",
                "description": "An old, rusty key. It must unlock something.",
                "item_type": ItemType.KEY,
                "weight": 0.1, "value": 0,
                "rarity": "common"
            },
            "cabin key": {
                "name": "Cabin Key",
                "description": "A brass key with 'Cabin' etched on it.",
                "item_type": ItemType.KEY,
                "weight": 0.1, "value": 0,
                "rarity": "uncommon"
            },
            "tower key": {
                "name": "Tower Key",
                "description": "An ornate key made of dark iron.",
                "item_type": ItemType.KEY,
                "weight": 0.2, "value": 0,
                "rarity": "rare"
            },
            "crypt key": {
                "name": "Crypt Key",
                "description": "A bone key carved with strange symbols.",
                "item_type": ItemType.KEY,
                "weight": 0.1, "value": 0,
                "rarity": "rare"
            },
            "master key": {
                "name": "Master Key",
                "description": "A magical key that glows faintly. Opens many locks.",
                "item_type": ItemType.KEY,
                "weight": 0.1, "value": 500,
                "rarity": "legendary"
            },
            "golden key": {
                "name": "Golden Key",
                "description": "A key made of pure gold, covered in intricate engravings.",
                "item_type": ItemType.KEY,
                "weight": 0.3, "value": 250,
                "rarity": "epic"
            },
            
            # ===== QUEST ITEMS =====
            "ancient amulet": {
                "name": "Ancient Amulet",
                "description": "A golden amulet inscribed with forgotten runes.",
                "item_type": ItemType.QUEST,
                "weight": 0.2, "value": 0,
                "rarity": "epic"
            },
            "spirit essence": {
                "name": "Spirit Essence",
                "description": "A glowing vial containing pure spiritual energy.",
                "item_type": ItemType.QUEST,
                "weight": 0.1, "value": 0,
                "rarity": "rare"
            },
            "forest heart": {
                "name": "Forest Heart",
                "description": "A pulsing green gem that seems alive with nature's power.",
                "item_type": ItemType.QUEST,
                "weight": 0.5, "value": 0,
                "rarity": "legendary"
            },
            "witch letter": {
                "name": "Witch's Letter",
                "description": "A sealed letter addressed to someone in the village.",
                "item_type": ItemType.QUEST,
                "weight": 0.1, "value": 0,
                "rarity": "uncommon"
            },
            "guardian token": {
                "name": "Guardian's Token",
                "description": "A stone medallion proving you have the Guardian's blessing.",
                "item_type": ItemType.QUEST,
                "weight": 0.3, "value": 0,
                "rarity": "epic"
            },
            "old journal": {
                "name": "Old Journal",
                "description": "A weathered journal filled with cryptic notes about the forest.",
                "item_type": ItemType.QUEST,
                "weight": 0.3, "value": 0,
                "special_effects": {"readable": True},
                "rarity": "uncommon"
            },
            "mysterious map": {
                "name": "Mysterious Map",
                "description": "A complete map of the forest, marking several locations.",
                "item_type": ItemType.QUEST,
                "weight": 0.1, "value": 100,
                "special_effects": {"reveal_locations": True},
                "rarity": "rare"
            },
            
            # ===== MATERIALS =====
            "wood": {
                "name": "Wood",
                "description": "A bundle of wood suitable for crafting.",
                "item_type": ItemType.MATERIAL,
                "weight": 1.0, "value": 2, "stackable": True,
                "rarity": "common"
            },
            "stone": {
                "name": "Stone",
                "description": "A piece of stone useful for crafting.",
                "item_type": ItemType.MATERIAL,
                "weight": 1.5, "value": 1, "stackable": True,
                "rarity": "common"
            },
            "cloth": {
                "name": "Cloth",
                "description": "A piece of fabric for bandages or crafting.",
                "item_type": ItemType.MATERIAL,
                "weight": 0.2, "value": 3, "stackable": True,
                "rarity": "common"
            },
            "iron ore": {
                "name": "Iron Ore",
                "description": "Raw iron ore that could be smelted.",
                "item_type": ItemType.MATERIAL,
                "weight": 2.0, "value": 10, "stackable": True,
                "rarity": "uncommon"
            },
            "silver ore": {
                "name": "Silver Ore",
                "description": "Raw silver ore, valuable and useful against dark creatures.",
                "item_type": ItemType.MATERIAL,
                "weight": 1.5, "value": 25, "stackable": True,
                "rarity": "rare"
            },
            "gold nugget": {
                "name": "Gold Nugget",
                "description": "A small nugget of pure gold.",
                "item_type": ItemType.MATERIAL,
                "weight": 0.5, "value": 50, "stackable": True,
                "rarity": "rare"
            },
            "wolf pelt": {
                "name": "Wolf Pelt",
                "description": "The fur of a forest wolf.",
                "item_type": ItemType.MATERIAL,
                "weight": 2.0, "value": 15,
                "rarity": "common"
            },
            "bear claw": {
                "name": "Bear Claw",
                "description": "A massive claw from a forest bear.",
                "item_type": ItemType.MATERIAL,
                "weight": 0.5, "value": 20,
                "rarity": "uncommon"
            },
            "spider silk": {
                "name": "Spider Silk",
                "description": "Strong, sticky silk from a giant spider.",
                "item_type": ItemType.MATERIAL,
                "weight": 0.2, "value": 30, "stackable": True,
                "rarity": "uncommon"
            },
            "feather": {
                "name": "Feather",
                "description": "A large feather, useful for fletching arrows.",
                "item_type": ItemType.MATERIAL,
                "weight": 0.1, "value": 2, "stackable": True,
                "rarity": "common"
            },
            "ember crystal": {
                "name": "Ember Crystal",
                "description": "A crystal that burns with inner fire.",
                "item_type": ItemType.MATERIAL,
                "weight": 0.3, "value": 100, "stackable": True,
                "rarity": "rare"
            },
            "frost shard": {
                "name": "Frost Shard",
                "description": "A shard of eternal ice that never melts.",
                "item_type": ItemType.MATERIAL,
                "weight": 0.3, "value": 100, "stackable": True,
                "rarity": "rare"
            },
            "shadow essence": {
                "name": "Shadow Essence",
                "description": "Concentrated darkness in physical form.",
                "item_type": ItemType.MATERIAL,
                "weight": 0.1, "value": 150, "stackable": True,
                "rarity": "epic"
            },
            "dragon scale": {
                "name": "Dragon Scale",
                "description": "A scale from an ancient dragon, incredibly rare.",
                "item_type": ItemType.MATERIAL,
                "weight": 1.0, "value": 500,
                "rarity": "legendary"
            },
            
            # ===== TREASURES =====
            "gold coins": {
                "name": "Gold Coins",
                "description": "A pouch of gold coins.",
                "item_type": ItemType.TREASURE,
                "weight": 0.5, "value": 100, "stackable": True,
                "rarity": "uncommon"
            },
            "gemstone": {
                "name": "Gemstone",
                "description": "A beautiful gemstone that sparkles in the light.",
                "item_type": ItemType.TREASURE,
                "weight": 0.1, "value": 75,
                "rarity": "rare"
            },
            "royal crown": {
                "name": "Royal Crown",
                "description": "A magnificent crown studded with jewels.",
                "item_type": ItemType.TREASURE,
                "weight": 1.0, "value": 1000,
                "rarity": "legendary"
            },
            "ancient artifact": {
                "name": "Ancient Artifact",
                "description": "A mysterious artifact from a long-lost civilization.",
                "item_type": ItemType.TREASURE,
                "weight": 2.0, "value": 500,
                "rarity": "epic"
            },
            
            # ===== MAGIC ITEMS =====
            "lucky charm": {
                "name": "Lucky Charm",
                "description": "A rabbit's foot that brings good fortune.",
                "item_type": ItemType.MAGIC,
                "weight": 0.1, "value": 50, "equippable": True,
                "special_effects": {"luck": 5},
                "rarity": "rare"
            },
            "spirit ward": {
                "name": "Spirit Ward",
                "description": "A protective talisman that wards off evil spirits.",
                "item_type": ItemType.MAGIC,
                "weight": 0.2, "value": 75, "equippable": True,
                "special_effects": {"spirit_protection": True},
                "rarity": "rare"
            },
            "ring of regeneration": {
                "name": "Ring of Regeneration",
                "description": "A ring that slowly heals the wearer.",
                "item_type": ItemType.MAGIC,
                "weight": 0.1, "value": 300, "equippable": True,
                "special_effects": {"regenerate": 1},
                "rarity": "epic"
            },
            "amulet of protection": {
                "name": "Amulet of Protection",
                "description": "An amulet that provides magical protection.",
                "item_type": ItemType.MAGIC,
                "weight": 0.2, "value": 200, "equippable": True,
                "defense": 5,
                "special_effects": {"magic_resistance": 10},
                "rarity": "epic"
            },
            "boots of speed": {
                "name": "Boots of Speed",
                "description": "Enchanted boots that make you run faster.",
                "item_type": ItemType.ARMOR,
                "weight": 1.0, "value": 250, "equippable": True,
                "defense": 2,
                "special_effects": {"speed_bonus": 20, "stamina_efficiency": 20},
                "rarity": "epic"
            },
        }
    
    @classmethod
    def create_item(cls, item_name: str) -> Optional[Item]:
        """Create an item by name."""
        if not cls._items_database:
            cls.initialize_database()
        
        item_data = cls._items_database.get(item_name.lower())
        if not item_data:
            return None
        
        return Item(
            name=item_data.get("name", item_name),
            description=item_data.get("description", ""),
            item_type=item_data.get("item_type", ItemType.TOOL),
            weight=item_data.get("weight", 1.0),
            value=item_data.get("value", 0),
            usable=item_data.get("usable", False),
            equippable=item_data.get("equippable", False),
            stackable=item_data.get("stackable", False),
            quantity=item_data.get("quantity", 1),
            damage=item_data.get("damage", 0),
            defense=item_data.get("defense", 0),
            healing=item_data.get("healing", 0),
            light_radius=item_data.get("light_radius", 0),
            durability=item_data.get("durability", 100),
            max_durability=item_data.get("max_durability", 100),
            special_effects=item_data.get("special_effects", {}),
            rarity=item_data.get("rarity", "common"),
            level_requirement=item_data.get("level_requirement", 1)
        )
    
    @classmethod
    def get_all_items(cls) -> List[str]:
        """Get list of all item names."""
        if not cls._items_database:
            cls.initialize_database()
        return list(cls._items_database.keys())
    
    @classmethod
    def get_items_by_type(cls, item_type: ItemType) -> List[str]:
        """Get list of item names by type."""
        if not cls._items_database:
            cls.initialize_database()
        return [
            name for name, data in cls._items_database.items()
            if data.get("item_type") == item_type
        ]
    
    @classmethod
    def get_items_by_rarity(cls, rarity: str) -> List[str]:
        """Get list of item names by rarity."""
        if not cls._items_database:
            cls.initialize_database()
        return [
            name for name, data in cls._items_database.items()
            if data.get("rarity") == rarity
        ]


