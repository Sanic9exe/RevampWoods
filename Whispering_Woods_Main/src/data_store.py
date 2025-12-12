"""
Game data store containing NPCs, items, creatures, quests, locations, etc.
Streamlined version with appropriate content levels.
"""

from typing import Tuple, Dict, List, Optional, TYPE_CHECKING
import random
import time

if TYPE_CHECKING:
    from .models import Item
    from .player import Player
    from .utils import DifficultyMode
else:
    # Import DifficultyMode at runtime
    from .utils import DifficultyMode

from .colors import Colors
from .utils import instant_print, colored_text

# ============================================================================
# CREATURES DATABASE (50 Quality Enemies)
# ============================================================================

EXPANDED_CREATURES = {
    # Basic Forest Creatures
    "dire_wolf": {
        "name": "Dire Wolf",
        "description": "A massive wolf with glowing red eyes and razor-sharp teeth.",
        "creature_type": "HOSTILE",
        "health": 80,
        "damage": 15,
        "defense": 6,
        "experience": 50,
        "loot": ["wolf pelt", "sharp fang"],
        "level": 4
    },
    "forest_troll": {
        "name": "Forest Troll",
        "description": "A hulking troll covered in moss and lichen.",
        "creature_type": "HOSTILE",
        "health": 150,
        "damage": 25,
        "defense": 12,
        "experience": 100,
        "loot": ["troll hide", "regeneration potion"],
        "level": 7
    },
    "treant": {
        "name": "Treant",
        "description": "An ancient tree come to life, guardian of the forest.",
        "creature_type": "NEUTRAL",
        "health": 200,
        "damage": 30,
        "defense": 20,
        "experience": 150,
        "loot": ["ancient wood", "nature essence"],
        "level": 10
    },
    # Cave/Underground Creatures
    "giant_spider": {
        "name": "Giant Spider",
        "description": "A massive spider with venomous fangs.",
        "creature_type": "HOSTILE",
        "health": 60,
        "damage": 20,
        "defense": 5,
        "experience": 40,
        "loot": ["spider silk", "venom sac"],
        "level": 3
    },
    "cave_bat": {
        "name": "Cave Bat",
        "description": "A large bat with leathery wings.",
        "creature_type": "HOSTILE",
        "health": 30,
        "damage": 10,
        "defense": 2,
        "experience": 20,
        "loot": ["bat wing"],
        "level": 2
    },
    "crystal_golem": {
        "name": "Crystal Golem",
        "description": "A construct made of living crystal, protecting ancient treasures.",
        "creature_type": "HOSTILE",
        "health": 180,
        "damage": 35,
        "defense": 25,
        "experience": 120,
        "loot": ["crystal shard", "magic gem"],
        "level": 9
    },
    # Elite Enemies
    "shadow_assassin": {
        "name": "Shadow Assassin",
        "description": "An elite assassin who moves through shadows.",
        "creature_type": "HOSTILE",
        "health": 120,
        "damage": 40,
        "defense": 15,
        "experience": 200,
        "loot": ["shadow cloak", "assassin's blade"],
        "level": 11,
        "is_elite": True
    },
    "corrupted_knight": {
        "name": "Corrupted Knight",
        "description": "A once-noble knight corrupted by dark magic.",
        "creature_type": "HOSTILE",
        "health": 250,
        "damage": 45,
        "defense": 30,
        "experience": 250,
        "loot": ["corrupted armor", "cursed sword"],
        "level": 13,
        "is_elite": True
    },
    # Bosses
    "ancient_dragon": {
        "name": "Ancient Dragon",
        "description": "A legendary dragon that has lived for millennia.",
        "creature_type": "BOSS",
        "health": 500,
        "damage": 80,
        "defense": 40,
        "experience": 1000,
        "loot": ["dragon scale", "dragon heart", "legendary treasure"],
        "level": 20,
        "is_boss": True
    },
    "lich_lord": {
        "name": "Lich Lord",
        "description": "An undead sorcerer of immense power.",
        "creature_type": "BOSS",
        "health": 400,
        "damage": 70,
        "defense": 35,
        "experience": 800,
        "loot": ["lich's phylactery", "necromantic staff"],
        "level": 18,
        "is_boss": True
    },
    # Mini-bosses
    "werewolf_alpha": {
        "name": "Werewolf Alpha",
        "description": "The pack leader, strongest of all werewolves.",
        "creature_type": "HOSTILE",
        "health": 200,
        "damage": 50,
        "defense": 20,
        "experience": 300,
        "loot": ["alpha pelt", "moonstone"],
        "level": 12,
        "is_miniboss": True
    },
    "ogre_chieftain": {
        "name": "Ogre Chieftain",
        "description": "The brutal leader of the ogre tribe.",
        "creature_type": "HOSTILE",
        "health": 280,
        "damage": 55,
        "defense": 25,
        "experience": 350,
        "loot": ["ogre club", "tribal totem"],
        "level": 14,
        "is_miniboss": True
    },
    # Standard enemies continued
    "goblin": {
        "name": "Goblin",
        "description": "A small, cunning creature.",
        "creature_type": "HOSTILE",
        "health": 20,
        "damage": 5,
        "defense": 1,
        "experience": 10,
        "loot": ["rusty dagger"],
        "level": 1
    },
    "wolf": {
        "name": "Wolf",
        "description": "A wild forest wolf.",
        "creature_type": "HOSTILE",
        "health": 40,
        "damage": 10,
        "defense": 3,
        "experience": 15,
        "loot": ["wolf pelt"],
        "level": 2
    },
    "bear": {
        "name": "Bear",
        "description": "A massive brown bear.",
        "creature_type": "NEUTRAL",
        "health": 100,
        "damage": 25,
        "defense": 8,
        "experience": 60,
        "loot": ["bear pelt", "bear meat"],
        "level": 5
    },
    "skeleton": {
        "name": "Skeleton",
        "description": "Animated bones held together by dark magic.",
        "creature_type": "HOSTILE",
        "health": 30,
        "damage": 8,
        "defense": 2,
        "experience": 12,
        "loot": ["bone"],
        "level": 2
    },
    "zombie": {
        "name": "Zombie",
        "description": "A shambling undead creature.",
        "creature_type": "HOSTILE",
        "health": 50,
        "damage": 12,
        "defense": 4,
        "experience": 18,
        "loot": ["rotten flesh"],
        "level": 3
    },
    "bandit": {
        "name": "Bandit",
        "description": "A dangerous highway robber.",
        "creature_type": "HOSTILE",
        "health": 45,
        "damage": 15,
        "defense": 5,
        "experience": 25,
        "loot": ["gold coins", "iron sword"],
        "level": 3
    },
    "orc_warrior": {
        "name": "Orc Warrior",
        "description": "A brutish orc with crude weapons.",
        "creature_type": "HOSTILE",
        "health": 90,
        "damage": 22,
        "defense": 10,
        "experience": 45,
        "loot": ["orcish axe", "leather armor"],
        "level": 5
    },
    "dark_mage": {
        "name": "Dark Mage",
        "description": "A practitioner of forbidden magic.",
        "creature_type": "HOSTILE",
        "health": 60,
        "damage": 30,
        "defense": 6,
        "experience": 80,
        "loot": ["magic scroll", "mana potion"],
        "level": 6
    },
    "harpy": {
        "name": "Harpy",
        "description": "A winged creature with a woman's face and bird's body.",
        "creature_type": "HOSTILE",
        "health": 55,
        "damage": 18,
        "defense": 4,
        "experience": 35,
        "loot": ["feather", "talon"],
        "level": 4
    },
    "swamp_troll": {
        "name": "Swamp Troll",
        "description": "A troll adapted to swamp life.",
        "creature_type": "HOSTILE",
        "health": 130,
        "damage": 28,
        "defense": 14,
        "experience": 90,
        "loot": ["swamp moss", "troll tooth"],
        "level": 7
    },
    "fire_elemental": {
        "name": "Fire Elemental",
        "description": "Living flame from the elemental plane.",
        "creature_type": "HOSTILE",
        "health": 80,
        "damage": 35,
        "defense": 8,
        "experience": 70,
        "loot": ["fire essence", "ember core"],
        "level": 6
    },
    "ice_wraith": {
        "name": "Ice Wraith",
        "description": "A ghostly figure made of frost and cold.",
        "creature_type": "HOSTILE",
        "health": 70,
        "damage": 25,
        "defense": 7,
        "experience": 65,
        "loot": ["frost crystal", "icy heart"],
        "level": 6
    },
    "giant_scorpion": {
        "name": "Giant Scorpion",
        "description": "A massive scorpion with deadly venom.",
        "creature_type": "HOSTILE",
        "health": 75,
        "damage": 20,
        "defense": 12,
        "experience": 55,
        "loot": ["scorpion carapace", "venom gland"],
        "level": 5
    },
    "gargoyle": {
        "name": "Gargoyle",
        "description": "A stone creature that comes to life.",
        "creature_type": "HOSTILE",
        "health": 110,
        "damage": 26,
        "defense": 18,
        "experience": 85,
        "loot": ["stone fragment", "gargoyle wing"],
        "level": 7
    },
    "wyvern": {
        "name": "Wyvern",
        "description": "A lesser dragon with poisonous breath.",
        "creature_type": "HOSTILE",
        "health": 150,
        "damage": 40,
        "defense": 16,
        "experience": 180,
        "loot": ["wyvern scale", "poison sac"],
        "level": 10
    },
    "minotaur": {
        "name": "Minotaur",
        "description": "A bull-headed humanoid with a massive axe.",
        "creature_type": "HOSTILE",
        "health": 180,
        "damage": 45,
        "defense": 20,
        "experience": 160,
        "loot": ["minotaur horn", "battle axe"],
        "level": 10
    },
    "ghost": {
        "name": "Ghost",
        "description": "The spirit of someone who died in the woods.",
        "creature_type": "HOSTILE",
        "health": 40,
        "damage": 15,
        "defense": 2,
        "experience": 30,
        "loot": ["ectoplasm"],
        "level": 3
    },
    "vampire": {
        "name": "Vampire",
        "description": "An undead creature that feeds on blood.",
        "creature_type": "HOSTILE",
        "health": 140,
        "damage": 35,
        "defense": 12,
        "experience": 140,
        "loot": ["vampire fang", "blood vial"],
        "level": 9
    },
    "demon": {
        "name": "Demon",
        "description": "A creature from the infernal planes.",
        "creature_type": "HOSTILE",
        "health": 160,
        "damage": 50,
        "defense": 18,
        "experience": 200,
        "loot": ["demon horn", "hellfire gem"],
        "level": 11
    },
    "basilisk": {
        "name": "Basilisk",
        "description": "A serpent whose gaze can turn victims to stone.",
        "creature_type": "HOSTILE",
        "health": 120,
        "damage": 30,
        "defense": 15,
        "experience": 110,
        "loot": ["basilisk eye", "petrified scale"],
        "level": 8
    },
    "chimera": {
        "name": "Chimera",
        "description": "A three-headed beast: lion, goat, and snake.",
        "creature_type": "HOSTILE",
        "health": 220,
        "damage": 55,
        "defense": 22,
        "experience": 280,
        "loot": ["chimera hide", "tri-element essence"],
        "level": 13
    },
    "forest_spirit": {
        "name": "Forest Spirit",
        "description": "A benevolent nature spirit.",
        "creature_type": "NEUTRAL",
        "health": 60,
        "damage": 15,
        "defense": 10,
        "experience": 50,
        "loot": ["nature blessing", "spirit essence"],
        "level": 4
    },
    "corrupted_treant": {
        "name": "Corrupted Treant",
        "description": "A once-noble treant twisted by dark magic.",
        "creature_type": "HOSTILE",
        "health": 230,
        "damage": 40,
        "defense": 24,
        "experience": 180,
        "loot": ["corrupted wood", "dark seed"],
        "level": 11
    },
    "shadow_beast": {
        "name": "Shadow Beast",
        "description": "A creature born from pure darkness.",
        "creature_type": "HOSTILE",
        "health": 100,
        "damage": 32,
        "defense": 10,
        "experience": 95,
        "loot": ["shadow essence", "void shard"],
        "level": 7
    },
    "lightning_sprite": {
        "name": "Lightning Sprite",
        "description": "A tiny elemental creature crackling with electricity.",
        "creature_type": "NEUTRAL",
        "health": 35,
        "damage": 25,
        "defense": 3,
        "experience": 40,
        "loot": ["lightning crystal"],
        "level": 4
    },
    "sea_serpent": {
        "name": "Sea Serpent",
        "description": "A massive serpent that lurks in deep waters.",
        "creature_type": "HOSTILE",
        "health": 190,
        "damage": 48,
        "defense": 16,
        "experience": 190,
        "loot": ["serpent scale", "water gem"],
        "level": 11
    },
    "earth_guardian": {
        "name": "Earth Guardian",
        "description": "A powerful elemental made of living stone.",
        "creature_type": "NEUTRAL",
        "health": 240,
        "damage": 38,
        "defense": 30,
        "experience": 170,
        "loot": ["earth core", "mountain shard"],
        "level": 12
    },
    "necromancer": {
        "name": "Necromancer",
        "description": "A dark wizard who commands the undead.",
        "creature_type": "HOSTILE",
        "health": 85,
        "damage": 42,
        "defense": 8,
        "experience": 140,
        "loot": ["necromantic tome", "soul gem"],
        "level": 9
    },
    "plague_rat": {
        "name": "Plague Rat",
        "description": "A diseased rat carrying deadly infections.",
        "creature_type": "HOSTILE",
        "health": 15,
        "damage": 6,
        "defense": 1,
        "experience": 8,
        "loot": ["diseased fur"],
        "level": 1
    },
    "dire_bear": {
        "name": "Dire Bear",
        "description": "An enormous bear of legendary size.",
        "creature_type": "NEUTRAL",
        "health": 200,
        "damage": 48,
        "defense": 14,
        "experience": 150,
        "loot": ["dire bear pelt", "bear claw"],
        "level": 10
    },
    "chaos_spawn": {
        "name": "Chaos Spawn",
        "description": "A twisted abomination of chaotic energy.",
        "creature_type": "HOSTILE",
        "health": 170,
        "damage": 44,
        "defense": 12,
        "experience": 165,
        "loot": ["chaos shard", "mutation essence"],
        "level": 10
    },
    "ancient_guardian": {
        "name": "Ancient Guardian",
        "description": "The final boss protecting the heart of the forest.",
        "creature_type": "BOSS",
        "health": 600,
        "damage": 90,
        "defense": 45,
        "experience": 1500,
        "loot": ["guardian's crown", "ancient relic", "master key"],
        "level": 22,
        "is_boss": True,
        "is_final_boss": True
    }
}

# Total: 50 creatures (includes normal, elite, mini-bosses, and bosses)

# ============================================================================
# ITEMS DATABASE (60 Purposeful Items)
# ============================================================================

EXPANDED_ITEMS = {
    # Weapons (15)
    "rusty_knife": {"name": "Rusty Knife", "type": "WEAPON", "damage": 3, "value": 5},
    "iron_sword": {"name": "Iron Sword", "type": "WEAPON", "damage": 10, "value": 50},
    "steel_sword": {"name": "Steel Sword", "type": "WEAPON", "damage": 18, "value": 150},
    "silver_sword": {"name": "Silver Sword", "type": "WEAPON", "damage": 25, "value": 300},
    "ancient_sword": {"name": "Ancient Sword", "type": "WEAPON", "damage": 35, "value": 800},
    "battle_axe": {"name": "Battle Axe", "type": "WEAPON", "damage": 22, "value": 200},
    "war_hammer": {"name": "War Hammer", "type": "WEAPON", "damage": 28, "value": 250},
    "magic_staff": {"name": "Magic Staff", "type": "WEAPON", "damage": 20, "magic": 15, "value": 400},
    "bow": {"name": "Bow", "type": "WEAPON", "damage": 15, "value": 80},
    "longbow": {"name": "Longbow", "type": "WEAPON", "damage": 24, "value": 180},
    "dagger": {"name": "Dagger", "type": "WEAPON", "damage": 8, "value": 30},
    "poison_dagger": {"name": "Poison Dagger", "type": "WEAPON", "damage": 12, "effect": "poison", "value": 120},
    "flame_sword": {"name": "Flame Sword", "type": "WEAPON", "damage": 30, "effect": "fire", "value": 600},
    "frost_blade": {"name": "Frost Blade", "type": "WEAPON", "damage": 28, "effect": "ice", "value": 550},
    "lightning_spear": {"name": "Lightning Spear", "type": "WEAPON", "damage": 32, "effect": "lightning", "value": 700},
    
    # Armor (10)
    "leather_armor": {"name": "Leather Armor", "type": "ARMOR", "defense": 5, "value": 40},
    "chainmail": {"name": "Chainmail", "type": "ARMOR", "defense": 10, "value": 100},
    "plate_armor": {"name": "Plate Armor", "type": "ARMOR", "defense": 18, "value": 250},
    "dragon_scale_armor": {"name": "Dragon Scale Armor", "type": "ARMOR", "defense": 28, "value": 1000},
    "mystic_robes": {"name": "Mystic Robes", "type": "ARMOR", "defense": 8, "magic": 12, "value": 200},
    "shadow_cloak": {"name": "Shadow Cloak", "type": "ARMOR", "defense": 12, "stealth": 20, "value": 300},
    "iron_helmet": {"name": "Iron Helmet", "type": "ARMOR", "defense": 4, "value": 35},
    "steel_gauntlets": {"name": "Steel Gauntlets", "type": "ARMOR", "defense": 6, "value": 60},
    "boots_of_speed": {"name": "Boots of Speed", "type": "ARMOR", "defense": 3, "speed": 15, "value": 180},
    "ring_of_protection": {"name": "Ring of Protection", "type": "ARMOR", "defense": 8, "value": 250},
    
    # Consumables (15)
    "healing_potion": {"name": "Healing Potion", "type": "CONSUMABLE", "heal": 50, "value": 25},
    "greater_healing_potion": {"name": "Greater Healing Potion", "type": "CONSUMABLE", "heal": 100, "value": 75},
    "mana_potion": {"name": "Mana Potion", "type": "CONSUMABLE", "mana": 50, "value": 30},
    "stamina_potion": {"name": "Stamina Potion", "type": "CONSUMABLE", "stamina": 50, "value": 20},
    "antidote": {"name": "Antidote", "type": "CONSUMABLE", "cure": "poison", "value": 40},
    "bread": {"name": "Bread", "type": "CONSUMABLE", "hunger": 20, "value": 5},
    "dried_meat": {"name": "Dried Meat", "type": "CONSUMABLE", "hunger": 35, "value": 15},
    "water_flask": {"name": "Water Flask", "type": "CONSUMABLE", "thirst": 30, "value": 5},
    "elixir_of_strength": {"name": "Elixir of Strength", "type": "CONSUMABLE", "buff": "strength", "value": 100},
    "elixir_of_wisdom": {"name": "Elixir of Wisdom", "type": "CONSUMABLE", "buff": "wisdom", "value": 100},
    "poison": {"name": "Poison", "type": "CONSUMABLE", "damage": 30, "value": 50},
    "smoke_bomb": {"name": "Smoke Bomb", "type": "CONSUMABLE", "effect": "escape", "value": 60},
    "fire_bomb": {"name": "Fire Bomb", "type": "CONSUMABLE", "damage": 40, "value": 80},
    "regeneration_potion": {"name": "Regeneration Potion", "type": "CONSUMABLE", "buff": "regen", "value": 120},
    "resurrection_scroll": {"name": "Resurrection Scroll", "type": "CONSUMABLE", "revive": True, "value": 500},
    
    # Tools (8)
    "torch": {"name": "Torch", "type": "TOOL", "light": True, "value": 5},
    "lantern": {"name": "Lantern", "type": "TOOL", "light": True, "duration": 100, "value": 30},
    "rope": {"name": "Rope", "type": "TOOL", "climbing": True, "value": 15},
    "lockpick": {"name": "Lockpick", "type": "TOOL", "lockpicking": True, "value": 25},
    "shovel": {"name": "Shovel", "type": "TOOL", "digging": True, "value": 20},
    "fishing_rod": {"name": "Fishing Rod", "type": "TOOL", "fishing": True, "value": 40},
    "compass": {"name": "Compass", "type": "TOOL", "navigation": True, "value": 50},
    "map": {"name": "Map", "type": "TOOL", "reveals_locations": True, "value": 100},
    
    # Materials (7)
    "wood": {"name": "Wood", "type": "MATERIAL", "value": 5},
    "iron_ore": {"name": "Iron Ore", "type": "MATERIAL", "value": 10},
    "leather": {"name": "Leather", "type": "MATERIAL", "value": 8},
    "herbs": {"name": "Herbs", "type": "MATERIAL", "value": 6},
    "crystal": {"name": "Crystal", "type": "MATERIAL", "magic": True, "value": 50},
    "dragon_scale": {"name": "Dragon Scale", "type": "MATERIAL", "rare": True, "value": 200},
    "ancient_rune": {"name": "Ancient Rune", "type": "MATERIAL", "magic": True, "value": 150},
    
    # Treasures (5)
    "gold_coins": {"name": "Gold Coins", "type": "TREASURE", "gold": 50, "value": 50},
    "gem": {"name": "Gem", "type": "TREASURE", "value": 100},
    "ancient_artifact": {"name": "Ancient Artifact", "type": "TREASURE", "quest": True, "value": 500},
    "magic_tome": {"name": "Magic Tome", "type": "TREASURE", "teaches_spell": True, "value": 300},
    "legendary_treasure": {"name": "Legendary Treasure", "type": "TREASURE", "value": 2000}
}

# Total: 60 items

# ============================================================================
# NPC DATABASE (17 Unique Characters)
# ============================================================================

NPC_DATABASE = {}

NPC_DATABASE["merchant"] = {
    "id": "merchant",
    "name": "Thomas the Merchant",
    "profession": "merchant",
    "description": "A friendly traveling merchant with a weathered pack full of goods.",
    "backstory": "Thomas has traveled these woods for 20 years, trading with villages and adventurers alike.",
    "personality": "Cheerful and business-minded, always looking for a good deal.",
    "location": "village_square",
    "sells": ["healing_potion", "bread", "torch", "rope"],
    "buys_items": True,
    "dialogue": {
        "greeting": "Greetings, traveler! Care to see my wares?",
        "trade": "I've got the finest goods in the region!",
        "farewell": "Safe travels, and come back soon!"
    }
}

NPC_DATABASE["blacksmith"] = {
    "id": "blacksmith",
    "name": "Grom the Blacksmith",
    "profession": "blacksmith",
    "description": "A burly dwarf with soot-stained hands and a booming voice.",
    "backstory": "Once forged weapons for kings, now retired to this quiet village.",
    "personality": "Gruff but kind-hearted, takes pride in his craft.",
    "location": "village_square",
    "sells": ["iron_sword", "steel_sword", "chainmail", "plate_armor"],
    "can_repair": True,
    "can_upgrade": True,
    "dialogue": {
        "greeting": "What do ye want? Got somethin' to fix?",
        "trade": "Fine steel, forged with care.",
        "farewell": "May yer blade never dull!"
    }
}

NPC_DATABASE["healer"] = {
    "id": "healer",
    "name": "Sister Elena",
    "profession": "healer",
    "description": "A kind elderly woman in white robes, radiating warmth.",
    "backstory": "Dedicated her life to healing the sick and wounded of the forest.",
    "personality": "Compassionate and wise, speaks in a gentle voice.",
    "location": "old_church",
    "services": ["heal", "cure_poison", "cure_curse"],
    "dialogue": {
        "greeting": "Welcome, child. Do you need healing?",
        "heal": "Let the light mend your wounds.",
        "farewell": "Go with blessings upon you."
    }
}

NPC_DATABASE["wizard"] = {
    "id": "wizard",
    "name": "Aldric the Wise",
    "profession": "wizard",
    "description": "An ancient wizard with a long white beard and star-covered robes.",
    "backstory": "Has lived for centuries, guarding ancient knowledge and secrets.",
    "personality": "Mysterious and enigmatic, speaks in riddles.",
    "location": "tower_interior",
    "teaches_magic": True,
    "sells_spells": True,
    "dialogue": {
        "greeting": "Ah, a seeker of knowledge approaches.",
        "wisdom": "Magic flows through all things, young one.",
        "farewell": "May the arcane guide your path."
    }
}

NPC_DATABASE["hunter"] = {
    "id": "hunter",
    "name": "Marcus the Hunter",
    "profession": "hunter",
    "description": "A skilled hunter with a bow slung over his shoulder.",
    "backstory": "Knows every trail in these woods and has survived countless dangers.",
    "personality": "Quiet and observant, prefers actions over words.",
    "location": "dense_forest",
    "teaches_skills": ["archery", "tracking", "survival"],
    "dialogue": {
        "greeting": "Quiet now. The forest has ears.",
        "advice": "Track your prey, move with the wind.",
        "farewell": "Good hunting."
    }
}

NPC_DATABASE["hermit"] = {
    "id": "hermit",
    "name": "Old Tobias",
    "profession": "hermit",
    "description": "A reclusive old man living alone in the woods.",
    "backstory": "Left civilization long ago, now lives in harmony with nature.",
    "personality": "Eccentric but knowledgeable about the forest's secrets.",
    "location": "hermit_hut",
    "gives_quests": True,
    "knows_secrets": True,
    "dialogue": {
        "greeting": "Rare to see visitors here. What brings you?",
        "lore": "The woods remember everything...",
        "farewell": "Come back if you survive."
    }
}

NPC_DATABASE["innkeeper"] = {
    "id": "innkeeper",
    "name": "Martha the Innkeeper",
    "profession": "innkeeper",
    "description": "A plump, friendly woman who runs the village inn.",
    "backstory": "Her inn has been a safe haven for travelers for generations.",
    "personality": "Motherly and warm, always has a meal ready.",
    "location": "village_inn",
    "provides_rest": True,
    "provides_food": True,
    "dialogue": {
        "greeting": "Welcome to my inn, dear! Hungry?",
        "rest": "Room and board for 10 gold.",
        "farewell": "Sleep well, and don't let the bed bugs bite!"
    }
}

NPC_DATABASE["guard"] = {
    "id": "guard",
    "name": "Captain Bran",
    "profession": "guard",
    "description": "A stern captain of the village guard in polished armor.",
    "backstory": "Sworn to protect the village from any threat.",
    "personality": "Duty-bound and serious, but fair.",
    "location": "village_square",
    "gives_quests": True,
    "provides_bounties": True,
    "dialogue": {
        "greeting": "Halt! State your business.",
        "quest": "We could use someone brave like you.",
        "farewell": "Stay vigilant."
    }
}

NPC_DATABASE["child"] = {
    "id": "child",
    "name": "Little Amy",
    "profession": "child",
    "description": "A curious young girl with braided hair.",
    "backstory": "Lost her favorite doll in the woods and needs help finding it.",
    "personality": "Innocent and cheerful, but scared of the dark forest.",
    "location": "village_square",
    "has_quest": True,
    "dialogue": {
        "greeting": "Mister/Miss, can you help me?",
        "quest": "I lost my dolly in the scary forest!",
        "farewell": "Thank you so much!"
    }
}

NPC_DATABASE["thief"] = {
    "id": "thief",
    "name": "Shadow",
    "profession": "thief",
    "description": "A mysterious figure in dark clothing, face hidden.",
    "backstory": "Master thief who can acquire anything... for a price.",
    "personality": "Cunning and secretive, speaks in whispers.",
    "location": "dark_alley",
    "teaches_skills": ["lockpicking", "stealth"],
    "fence_items": True,
    "dialogue": {
        "greeting": "Looking for something... special?",
        "trade": "I can get you anything. Gold talks.",
        "farewell": "We were never here."
    }
}

NPC_DATABASE["alchemist"] = {
    "id": "alchemist",
    "name": "Morgana the Alchemist",
    "profession": "alchemist",
    "description": "An eccentric woman surrounded by bubbling potions.",
    "backstory": "Experiments with rare ingredients to create powerful concoctions.",
    "personality": "Brilliant but slightly mad, mutters to herself.",
    "location": "alchemist_shop",
    "sells": ["healing_potion", "mana_potion", "antidote", "elixir_of_strength"],
    "teaches_crafting": True,
    "dialogue": {
        "greeting": "Ah! A test subject—I mean, customer!",
        "craft": "Mix this with that, and... BOOM! Wait, no boom. Good.",
        "farewell": "Don't drink the purple one!"
    }
}

NPC_DATABASE["bard"] = {
    "id": "bard",
    "name": "Finnegan the Bard",
    "profession": "bard",
    "description": "A charismatic musician with a lute and a ready smile.",
    "backstory": "Travels the land collecting stories and songs.",
    "personality": "Charming and witty, always has a tale to tell.",
    "location": "village_inn",
    "tells_stories": True,
    "provides_lore": True,
    "dialogue": {
        "greeting": "Ho there! Care to hear a tale?",
        "story": "Gather 'round for the legend of...",
        "farewell": "May your journey be worthy of song!"
    }
}

NPC_DATABASE["priestess"] = {
    "id": "priestess",
    "name": "High Priestess Lyra",
    "profession": "priestess",
    "description": "A regal woman in ceremonial robes, radiating divine power.",
    "backstory": "Leads the faithful and performs sacred rituals.",
    "personality": "Devout and serene, speaks with authority.",
    "location": "temple_altar",
    "provides_blessings": True,
    "removes_curses": True,
    "dialogue": {
        "greeting": "The gods smile upon you, traveler.",
        "blessing": "May divine light protect you.",
        "farewell": "Walk in the light."
    }
}

NPC_DATABASE["elder"] = {
    "id": "elder",
    "name": "Elder Thaddeus",
    "profession": "elder",
    "description": "The village elder, ancient and wise beyond measure.",
    "backstory": "Has led the village for 50 years, knows all its history.",
    "personality": "Patient and thoughtful, commands respect.",
    "location": "village_hall",
    "provides_lore": True,
    "gives_main_quests": True,
    "dialogue": {
        "greeting": "Welcome, young one. Seeking wisdom?",
        "lore": "In my youth, these woods were different...",
        "farewell": "Go with the wisdom of ages."
    }
}

NPC_DATABASE["scout"] = {
    "id": "scout",
    "name": "Kira the Scout",
    "profession": "scout",
    "description": "A nimble scout with keen eyes and quick reflexes.",
    "backstory": "Explores dangerous areas and reports back to the village.",
    "personality": "Adventurous and bold, always ready for action.",
    "location": "forest_edge",
    "sells_maps": True,
    "provides_info": True,
    "dialogue": {
        "greeting": "Hey! You look like you can handle yourself.",
        "info": "I've mapped most of these woods. For a price.",
        "farewell": "Watch your back out there!"
    }
}

NPC_DATABASE["apprentice"] = {
    "id": "apprentice",
    "name": "Young Pip",
    "profession": "apprentice",
    "description": "An eager young apprentice to the wizard.",
    "backstory": "Dreams of becoming a great wizard someday.",
    "personality": "Enthusiastic and naive, asks many questions.",
    "location": "tower_base",
    "has_quest": True,
    "dialogue": {
        "greeting": "Oh wow, an adventurer! Can I come with you?",
        "quest": "Master needs these ingredients from the forest!",
        "farewell": "I hope I can be brave like you someday!"
    }
}

NPC_DATABASE["stranger"] = {
    "id": "stranger",
    "name": "The Hooded Stranger",
    "profession": "mysterious",
    "description": "A figure in a dark hood, identity unknown.",
    "backstory": "Appears at key moments, purpose unclear.",
    "personality": "Cryptic and ominous, speaks in prophecies.",
    "location": "various",
    "plot_important": True,
    "dialogue": {
        "greeting": "We meet again... as fate decreed.",
        "prophecy": "The woods awaken. Darkness stirs. Your destiny awaits.",
        "farewell": "Until the stars align once more..."
    }
}

# Total: 17 unique NPCs


# ============================================================================
# MINIGAMES
# ============================================================================

class LockpickingGame:
    """Lockpicking mini-game."""
    
    @staticmethod
    def play(difficulty: int, player: 'Player') -> Tuple[bool, str]:
        """Play the lockpicking mini-game."""
        instant_print(colored_text(f"\n=== LOCKPICKING ===", Colors.YELLOW))
        instant_print("Simple lockpicking minigame")
        import random
        success = random.random() > 0.5
        if success:
            return True, "Lock picked successfully!"
        return False, "Failed to pick the lock."

class FishingGame:
    """Fishing mini-game."""
    
    @staticmethod
    def play(player: 'Player') -> Tuple[bool, str, Optional['Item']]:
        """Play the fishing mini-game."""
        if not hasattr(player, 'has_item') or not player.has_item("fishing rod"):
            return False, "You need a fishing rod!", None
        
        instant_print(colored_text("\n=== FISHING ===", Colors.CYAN))
        instant_print("Cast your line...")
        import random
        if random.random() > 0.6:
            return True, "You caught a fish!", None
        return False, "The fish got away!", None

class CardGame:
    """Dice game mini-game."""
    
    @staticmethod
    def play(bet: int, player: 'Player') -> Tuple[bool, str]:
        """Play a simple dice game."""
        instant_print(colored_text("\n=== DICE GAME ===", Colors.YELLOW))
        instant_print(f"Betting {bet} gold...")
        import random
        player_roll = random.randint(1, 6)
        dealer_roll = random.randint(1, 6)
        instant_print(f"You rolled: {player_roll}")
        instant_print(f"Dealer rolled: {dealer_roll}")
        
        if player_roll > dealer_roll:
            return True, f"You win {bet*2} gold!"
        elif player_roll < dealer_roll:
            return False, f"You lose {bet} gold."
        return False, "Tie! No gold exchanged."

# ============================================================================
# ESSENTIAL FUNCTIONS
# ============================================================================

def select_difficulty_mode():
    """Display difficulty selection menu and return chosen difficulty."""
    print("\n" + "="*60)
    print(" "*15 + "DIFFICULTY SELECTION")
    print("="*60 + "\n")
    print("Choose your difficulty level:\n")
    print("[1] STORY MODE - Easy, focus on story")
    print("    Damage taken: 50%, Damage dealt: 150%")
    print("    Drop rates: 150%, Survival drain: 50%\n")
    print("[2] NORMAL MODE - Balanced gameplay") 
    print("    Standard values for all mechanics\n")
    print("[3] HARD MODE - Challenging")
    print("    Damage taken: 150%, Damage dealt: 75%")
    print("    Drop rates: 70%, Survival drain: 150%\n")
    print("[4] NIGHTMARE MODE - Extreme + Permadeath")
    print("    Damage taken: 200%, Damage dealt: 50%")
    print("    Drop rates: 50%, Survival drain: 200%\n")
    
    while True:
        choice = input("Select difficulty [1-4]: ").strip()
        if choice == "1":
            print("\nStory Mode selected!")
            return DifficultyMode.STORY
        elif choice == "2":
            print("\nNormal Mode selected!")
            return DifficultyMode.NORMAL
        elif choice == "3":
            print("\nHard Mode selected!")
            return DifficultyMode.HARD
        elif choice == "4":
            confirm = input("\nWARNING: Nightmare has PERMADEATH. Continue? (yes/no): ").lower()
            if confirm in ['yes', 'y']:
                print("\nNightmare Mode selected!")
                return DifficultyMode.NIGHTMARE
        else:
            print("Invalid choice. Enter 1-4.")

def get_difficulty_multipliers(difficulty):
    """Get multipliers for difficulty mode."""
    mults = {
        DifficultyMode.STORY: {'dmg_taken': 0.5, 'dmg_dealt': 1.5, 'drops': 1.5, 'survival': 0.5},
        DifficultyMode.NORMAL: {'dmg_taken': 1.0, 'dmg_dealt': 1.0, 'drops': 1.0, 'survival': 1.0},
        DifficultyMode.HARD: {'dmg_taken': 1.5, 'dmg_dealt': 0.75, 'drops': 0.7, 'survival': 1.5},
        DifficultyMode.NIGHTMARE: {'dmg_taken': 2.0, 'dmg_dealt': 0.5, 'drops': 0.5, 'survival': 2.0}
    }
    return mults.get(difficulty, mults[DifficultyMode.NORMAL])

STARTING_LOCATIONS = {
    "clearing": {
        "name": "Forest Clearing",
        "description": "A sunlit clearing surrounded by ancient trees.",
        "items": ["rusty_knife", "torch", "bread"],
        "routes": ["dark_woods", "stream", "dense_forest"],
        "difficulty": "Beginner"
    },
    "stream": {
        "name": "Babbling Stream",
        "description": "An abandoned campsite beside a flowing river.",
        "items": ["fishing_rod", "torch", "dried_meat"],
        "routes": ["waterfall", "clearing"],
        "difficulty": "Easy"
    },
    "mountain_path": {
        "name": "Mountain Path",
        "description": "A narrow mountain trail with the world spread far below.",
        "items": ["shovel", "rope", "torch"],
        "routes": ["mountain_cave"],
        "difficulty": "Moderate"
    },
    "abandoned_village": {
        "name": "Abandoned Village",
        "description": "A deserted village with weathered buildings.",
        "items": ["iron_sword", "map", "lantern"],
        "routes": ["village_square", "old_church"],
        "difficulty": "Moderate"
    },
    "ancient_ruins": {
        "name": "Ancient Ruins",
        "description": "Crumbling stone pillars covered in ancient runes.",
        "items": ["ancient_sword", "healing_potion", "torch"],
        "routes": ["ruined_temple"],
        "difficulty": "Moderate-Hard"
    },
    "hidden_cave": {
        "name": "Hidden Cave Entrance",
        "description": "The mouth of a vast cave system.",
        "items": ["torch", "shovel", "rope"],
        "routes": ["crystal_cavern"],
        "difficulty": "Hard"
    },
    "swamp_edge": {
        "name": "Swamp Edge",
        "description": "You stand at the edge of a misty swamp.",
        "items": ["dagger", "fishing_rod", "torch"],
        "routes": ["swamp_path"],
        "difficulty": "Moderate"
    },
    "fairy_grove": {
        "name": "Enchanted Fairy Grove",
        "description": "A mystical glade bathed in ethereal light.",
        "items": ["silver_sword", "healing_potion", "crystal"],
        "routes": ["fairy_throne"],
        "difficulty": "Hard"
    }
}

def select_starting_location():
    """Display starting location menu and return choice."""
    print("\n" + "="*60)
    print(" "*15 + "STARTING LOCATION")
    print("="*60 + "\n")
    print("Choose where your adventure begins:\n")
    
    locs = list(STARTING_LOCATIONS.items())
    for i, (loc_id, data) in enumerate(locs, 1):
        print(f"[{i}] {data['name']} - {data['difficulty']}")
    
    while True:
        try:
            choice = int(input(f"\nSelect [1-{len(locs)}]: "))
            if 1 <= choice <= len(locs):
                loc_id, data = locs[choice-1]
                print(f"\n{data['name']} selected!")
                print(f"\n{data['description']}\n")
                return loc_id, data
        except ValueError:
            pass
        print("Invalid choice.")
