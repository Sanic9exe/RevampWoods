"""Creature factory for creating game creatures."""

import random
from typing import Dict, List, Optional

from .utils import CreatureType
from .models import Creature, Item

# ============================================================================
# CREATURE FACTORY
# ============================================================================

class CreatureFactory:
    """Factory for creating game creatures."""
    
    _creatures_database: Dict[str, Dict] = {}
    
    @classmethod
    def initialize_database(cls):
        """Initialize the creatures database."""
        cls._creatures_database = {
            # ===== PASSIVE CREATURES =====
            "deer": {
                "name": "Forest Deer",
                "description": "A graceful deer with large, gentle eyes.",
                "creature_type": CreatureType.PASSIVE,
                "health": 15, "max_health": 15,
                "damage": 0, "defense": 0,
                "experience": 5,
                "loot": ["dried meat"],
                "loot_chance": 80,
                "hostile": False,
                "gold_drop": (0, 0)
            },
            "rabbit": {
                "name": "Wild Rabbit",
                "description": "A small brown rabbit, nose twitching nervously.",
                "creature_type": CreatureType.PASSIVE,
                "health": 5, "max_health": 5,
                "damage": 0, "defense": 0,
                "experience": 2,
                "loot": ["wild berries"],
                "loot_chance": 50,
                "hostile": False,
                "gold_drop": (0, 0)
            },
            "owl": {
                "name": "Wise Owl",
                "description": "A large owl with piercing golden eyes that seem to see into your soul.",
                "creature_type": CreatureType.PASSIVE,
                "health": 10, "max_health": 10,
                "damage": 0, "defense": 0,
                "experience": 0,
                "hostile": False,
                "dialogue": [
                    "Hoo... The path you seek lies beyond the ravine.",
                    "Hoo... Beware the shadows that move without light.",
                    "Hoo... The old tower holds the key to your escape.",
                    "Hoo... Trust not all who offer help in these woods."
                ],
                "gold_drop": (0, 0)
            },
            "squirrel": {
                "name": "Squirrel",
                "description": "A bushy-tailed squirrel gathering nuts.",
                "creature_type": CreatureType.PASSIVE,
                "health": 3, "max_health": 3,
                "damage": 0, "defense": 0,
                "experience": 1,
                "loot": ["wild berries"],
                "loot_chance": 30,
                "hostile": False,
                "gold_drop": (0, 0)
            },
            
            # ===== HOSTILE CREATURES =====
            "wolf": {
                "name": "Forest Wolf",
                "description": "A lean, hungry wolf with gleaming yellow eyes.",
                "creature_type": CreatureType.HOSTILE,
                "health": 30, "max_health": 30,
                "damage": 8, "defense": 2,
                "experience": 20,
                "loot": ["wolf pelt"],
                "loot_chance": 60,
                "hostile": True,
                "level": 2,
                "gold_drop": (0, 5)
            },
            "dire wolf": {
                "name": "Dire Wolf",
                "description": "A massive wolf, twice the size of a normal wolf, with blood-red eyes.",
                "creature_type": CreatureType.HOSTILE,
                "health": 60, "max_health": 60,
                "damage": 15, "defense": 5,
                "experience": 50,
                "loot": ["wolf pelt", "wolf pelt"],
                "loot_chance": 80,
                "hostile": True,
                "level": 5,
                "gold_drop": (5, 20)
            },
            "giant spider": {
                "name": "Giant Spider",
                "description": "A massive spider the size of a dog, with dripping fangs.",
                "creature_type": CreatureType.HOSTILE,
                "health": 25, "max_health": 25,
                "damage": 10, "defense": 1,
                "experience": 25,
                "loot": ["spider silk"],
                "loot_chance": 70,
                "hostile": True,
                "special_abilities": ["poison"],
                "level": 3,
                "gold_drop": (0, 10)
            },
            "spider queen": {
                "name": "Spider Queen",
                "description": "An enormous spider with a bloated abdomen, surrounded by smaller spiders.",
                "creature_type": CreatureType.BOSS,
                "health": 100, "max_health": 100,
                "damage": 18, "defense": 5,
                "experience": 150,
                "loot": ["spider silk", "spider silk", "spider silk", "gemstone"],
                "loot_chance": 90,
                "hostile": True,
                "special_abilities": ["poison", "web", "summon_spiders"],
                "level": 8,
                "gold_drop": (50, 100)
            },
            "bear": {
                "name": "Forest Bear",
                "description": "A massive brown bear, standing on its hind legs.",
                "creature_type": CreatureType.NEUTRAL,
                "health": 60, "max_health": 60,
                "damage": 15, "defense": 5,
                "experience": 40,
                "loot": ["bear claw"],
                "loot_chance": 50,
                "hostile": False,
                "level": 4,
                "gold_drop": (0, 0)
            },
            "goblin": {
                "name": "Forest Goblin",
                "description": "A small, green-skinned creature with sharp teeth and cunning eyes.",
                "creature_type": CreatureType.HOSTILE,
                "health": 20, "max_health": 20,
                "damage": 6, "defense": 1,
                "experience": 15,
                "loot": ["rusty knife"],
                "loot_chance": 30,
                "hostile": True,
                "dialogue": [
                    "Give us your shinies!",
                    "Fresh meat!",
                    "Kill! Kill!"
                ],
                "level": 1,
                "gold_drop": (5, 15)
            },
            "goblin scout": {
                "name": "Goblin Scout",
                "description": "A goblin wearing crude leather armor and carrying a short bow.",
                "creature_type": CreatureType.HOSTILE,
                "health": 25, "max_health": 25,
                "damage": 8, "defense": 2,
                "experience": 20,
                "loot": ["hunting bow"],
                "loot_chance": 20,
                "hostile": True,
                "level": 2,
                "gold_drop": (10, 25)
            },
            "goblin shaman": {
                "name": "Goblin Shaman",
                "description": "A goblin covered in bones and feathers, wielding dark magic.",
                "creature_type": CreatureType.HOSTILE,
                "health": 35, "max_health": 35,
                "damage": 12, "defense": 1,
                "experience": 40,
                "loot": ["mana potion", "healing potion"],
                "loot_chance": 50,
                "hostile": True,
                "special_abilities": ["heal_allies", "curse"],
                "level": 4,
                "gold_drop": (20, 40)
            },
            "skeleton": {
                "name": "Skeleton Warrior",
                "description": "The animated bones of a long-dead warrior, wielding a rusty sword.",
                "creature_type": CreatureType.HOSTILE,
                "health": 35, "max_health": 35,
                "damage": 12, "defense": 3,
                "experience": 30,
                "loot": ["ancient sword"],
                "loot_chance": 10,
                "hostile": True,
                "weakness": "blunt",
                "level": 4,
                "gold_drop": (5, 20)
            },
            "skeleton archer": {
                "name": "Skeleton Archer",
                "description": "A skeleton wielding a cracked bow, arrows rattling in its quiver.",
                "creature_type": CreatureType.HOSTILE,
                "health": 25, "max_health": 25,
                "damage": 10, "defense": 1,
                "experience": 25,
                "loot": ["hunting bow", "feather"],
                "loot_chance": 25,
                "hostile": True,
                "weakness": "blunt",
                "level": 3,
                "gold_drop": (5, 15)
            },
            "ghost": {
                "name": "Restless Ghost",
                "description": "A translucent spirit drifting through the air, its face twisted in anguish.",
                "creature_type": CreatureType.HOSTILE,
                "health": 40, "max_health": 40,
                "damage": 10, "defense": 0,
                "experience": 35,
                "loot": ["spirit essence"],
                "loot_chance": 40,
                "hostile": True,
                "weakness": "silver",
                "resistance": "physical",
                "special_abilities": ["intangible", "fear"],
                "level": 5,
                "gold_drop": (0, 0)
            },
            "wraith": {
                "name": "Wraith",
                "description": "A dark spirit wreathed in shadow, radiating cold malice.",
                "creature_type": CreatureType.HOSTILE,
                "health": 70, "max_health": 70,
                "damage": 18, "defense": 0,
                "experience": 75,
                "loot": ["shadow essence", "spirit essence"],
                "loot_chance": 60,
                "hostile": True,
                "weakness": "silver",
                "resistance": "physical",
                "special_abilities": ["intangible", "life_drain", "fear"],
                "level": 7,
                "gold_drop": (0, 0)
            },
            "bandit": {
                "name": "Forest Bandit",
                "description": "A rough-looking man with a scarred face and dangerous eyes.",
                "creature_type": CreatureType.HOSTILE,
                "health": 40, "max_health": 40,
                "damage": 12, "defense": 4,
                "experience": 35,
                "loot": ["gold coins", "lockpick"],
                "loot_chance": 50,
                "hostile": True,
                "dialogue": [
                    "Hand over your valuables!",
                    "This is our territory!",
                    "You shouldn't have come here alone..."
                ],
                "level": 4,
                "gold_drop": (15, 40)
            },
            "bandit archer": {
                "name": "Bandit Archer",
                "description": "A bandit keeping distance with a longbow at the ready.",
                "creature_type": CreatureType.HOSTILE,
                "health": 30, "max_health": 30,
                "damage": 14, "defense": 2,
                "experience": 30,
                "loot": ["hunting bow", "feather"],
                "loot_chance": 40,
                "hostile": True,
                "level": 3,
                "gold_drop": (10, 30)
            },
            "troll": {
                "name": "Forest Troll",
                "description": "A hulking creature with greenish skin and enormous fists.",
                "creature_type": CreatureType.HOSTILE,
                "health": 80, "max_health": 80,
                "damage": 20, "defense": 8,
                "experience": 60,
                "loot": ["gold nugget"],
                "loot_chance": 30,
                "hostile": True,
                "special_abilities": ["regenerate"],
                "weakness": "fire",
                "level": 6,
                "gold_drop": (20, 50)
            },
            "harpy": {
                "name": "Harpy",
                "description": "A winged creature with the body of a bird and face of a woman.",
                "creature_type": CreatureType.HOSTILE,
                "health": 35, "max_health": 35,
                "damage": 11, "defense": 2,
                "experience": 35,
                "loot": ["feather", "feather", "feather"],
                "loot_chance": 80,
                "hostile": True,
                "special_abilities": ["flight", "screech"],
                "level": 4,
                "gold_drop": (5, 25)
            },
            "swamp creature": {
                "name": "Swamp Creature",
                "description": "A shambling mass of rotting vegetation and mud.",
                "creature_type": CreatureType.HOSTILE,
                "health": 50, "max_health": 50,
                "damage": 14, "defense": 6,
                "experience": 45,
                "loot": ["healing herb", "healing herb"],
                "loot_chance": 60,
                "hostile": True,
                "special_abilities": ["poison"],
                "weakness": "fire",
                "resistance": "water",
                "level": 5,
                "gold_drop": (0, 10)
            },
            
            # ===== NPCS =====
            "witch": {
                "name": "Forest Witch",
                "description": "An old woman with wild hair and glowing green eyes.",
                "creature_type": CreatureType.NPC,
                "health": 50, "max_health": 50,
                "damage": 15, "defense": 2,
                "experience": 50,
                "loot": ["healing potion", "antidote"],
                "hostile": False,
                "dialogue": [
                    "Ah, another lost soul wandering my woods...",
                    "Looking for a way out? Perhaps I can help... for a price.",
                    "The forest keeps many secrets. I know them all.",
                    "Beware the Guardian of the Deep Woods. It does not forgive trespassers."
                ],
                "gold_drop": (0, 0)
            },
            "hermit": {
                "name": "Old Hermit",
                "description": "A weathered old man living alone in the forest.",
                "creature_type": CreatureType.NPC,
                "health": 30, "max_health": 30,
                "damage": 0, "defense": 0,
                "experience": 0,
                "hostile": False,
                "dialogue": [
                    "I've lived in these woods for forty years. I know every path.",
                    "You seek the way out? Follow the river east, then climb the ridge.",
                    "Take this map fragment. It shows the safe paths through the swamp.",
                    "The old tower... yes, I remember. The witch knows how to open it."
                ],
                "gold_drop": (0, 0)
            },
            "lost traveler": {
                "name": "Lost Traveler",
                "description": "A frightened-looking person in torn clothes.",
                "creature_type": CreatureType.NPC,
                "health": 20, "max_health": 20,
                "damage": 0, "defense": 0,
                "experience": 0,
                "hostile": False,
                "dialogue": [
                    "Thank goodness, another person! I've been lost for days!",
                    "Please, do you have any food or water to spare?",
                    "I saw something terrible in the swamp... glowing eyes...",
                    "If we work together, maybe we can find a way out."
                ],
                "gold_drop": (0, 0)
            },
            "tree spirit": {
                "name": "Tree Spirit",
                "description": "A luminous being that seems to emerge from an ancient oak.",
                "creature_type": CreatureType.NEUTRAL,
                "health": 60, "max_health": 60,
                "damage": 12, "defense": 4,
                "experience": 45,
                "hostile": False,
                "dialogue": [
                    "Why do you disturb our woods, mortal?",
                    "The forest was here long before your kind. It will remain long after.",
                    "Prove your respect for nature, and I may aid you.",
                    "Harm the sacred grove, and face our wrath."
                ],
                "gold_drop": (0, 0)
            },
            "merchant": {
                "name": "Traveling Merchant",
                "description": "A jovial merchant with a heavy pack of goods.",
                "creature_type": CreatureType.MERCHANT,
                "health": 40, "max_health": 40,
                "damage": 5, "defense": 3,
                "experience": 0,
                "hostile": False,
                "dialogue": [
                    "Welcome, traveler! Care to see my wares?",
                    "The finest goods this side of the forest!",
                    "I've traveled far and wide. You won't find better prices!",
                    "Need supplies for your journey? I have just the thing!"
                ],
                "gold_drop": (0, 0)
            },
            "wounded soldier": {
                "name": "Wounded Soldier",
                "description": "A soldier in torn armor, leaning against a tree.",
                "creature_type": CreatureType.NPC,
                "health": 15, "max_health": 50,
                "damage": 8, "defense": 5,
                "experience": 0,
                "hostile": False,
                "dialogue": [
                    "Help... ambushed by bandits...",
                    "The bandit camp is to the northwest... be careful...",
                    "If you find my sword... the family crest... please return it...",
                    "They took everything... left me to die..."
                ],
                "gold_drop": (0, 0)
            },
            
            # ===== BOSS CREATURES =====
            "forest guardian": {
                "name": "Forest Guardian",
                "description": "A massive creature of wood and vine, ancient and powerful.",
                "creature_type": CreatureType.BOSS,
                "health": 200, "max_health": 200,
                "damage": 25, "defense": 12,
                "experience": 300,
                "loot": ["forest heart", "guardian token", "guardian blade"],
                "loot_chance": 100,
                "hostile": True,
                "weakness": "fire",
                "special_abilities": ["regenerate", "root_bind", "summon_treants"],
                "level": 10,
                "gold_drop": (100, 200)
            },
            "shadow beast": {
                "name": "Shadow Beast",
                "description": "A creature of pure darkness, with glowing red eyes.",
                "creature_type": CreatureType.BOSS,
                "health": 150, "max_health": 150,
                "damage": 22, "defense": 5,
                "experience": 200,
                "loot": ["shadow essence", "shadow essence", "shadow cloak"],
                "loot_chance": 100,
                "hostile": True,
                "weakness": "light",
                "resistance": "physical",
                "special_abilities": ["shadow_step", "fear", "life_drain"],
                "level": 8,
                "gold_drop": (75, 150)
            },
            "bandit leader": {
                "name": "Bandit Leader",
                "description": "A tall, muscular man in leather armor, clearly the leader of the bandits.",
                "creature_type": CreatureType.BOSS,
                "health": 100, "max_health": 100,
                "damage": 18, "defense": 8,
                "experience": 150,
                "loot": ["chainmail", "master key", "gold coins", "gold coins"],
                "loot_chance": 100,
                "hostile": True,
                "dialogue": [
                    "So you've made it this far. Impressive.",
                    "Join us or die. Those are your only options.",
                    "I'll enjoy taking everything you own."
                ],
                "level": 7,
                "gold_drop": (100, 200)
            },
            "ancient dragon": {
                "name": "Ancient Dragon",
                "description": "A colossal dragon with scales like armor and eyes like molten gold.",
                "creature_type": CreatureType.BOSS,
                "health": 500, "max_health": 500,
                "damage": 40, "defense": 20,
                "experience": 1000,
                "loot": ["dragon scale", "dragon scale", "royal crown", "flame sword"],
                "loot_chance": 100,
                "hostile": True,
                "special_abilities": ["fire_breath", "flight", "tail_sweep", "terrifying_roar"],
                "resistance": "fire",
                "weakness": "ice",
                "level": 15,
                "gold_drop": (500, 1000)
            },
            "lich": {
                "name": "The Lich",
                "description": "An undead sorcerer crackling with dark energy, a crown of bone upon its head.",
                "creature_type": CreatureType.BOSS,
                "health": 180, "max_health": 180,
                "damage": 30, "defense": 5,
                "experience": 400,
                "loot": ["shadow essence", "shadow essence", "enchanted staff", "crypt key"],
                "loot_chance": 100,
                "hostile": True,
                "weakness": "silver",
                "resistance": "physical",
                "special_abilities": ["dark_magic", "summon_undead", "life_drain", "teleport"],
                "level": 12,
                "gold_drop": (200, 400)
            },
        }
    
    @classmethod
    def create_creature(cls, creature_name: str) -> Optional[Creature]:
        """Create a creature by name."""
        if not cls._creatures_database:
            cls.initialize_database()
        
        creature_data = cls._creatures_database.get(creature_name.lower())
        if not creature_data:
            return None
        
        return Creature(
            name=creature_data.get("name", creature_name),
            description=creature_data.get("description", ""),
            creature_type=creature_data.get("creature_type", CreatureType.HOSTILE),
            health=creature_data.get("health", 10),
            max_health=creature_data.get("max_health", 10),
            damage=creature_data.get("damage", 5),
            defense=creature_data.get("defense", 0),
            experience=creature_data.get("experience", 10),
            loot=creature_data.get("loot", []),
            loot_chance=creature_data.get("loot_chance", 50),
            dialogue=creature_data.get("dialogue", []),
            hostile=creature_data.get("hostile", False),
            special_abilities=creature_data.get("special_abilities", []),
            weakness=creature_data.get("weakness"),
            resistance=creature_data.get("resistance"),
            level=creature_data.get("level", 1),
            gold_drop=creature_data.get("gold_drop", (0, 10))
        )
    
    @classmethod
    def get_all_creatures(cls) -> List[str]:
        """Get list of all creature names."""
        if not cls._creatures_database:
            cls.initialize_database()
        return list(cls._creatures_database.keys())
    
    @classmethod
    def get_creatures_by_type(cls, creature_type: CreatureType) -> List[str]:
        """Get list of creature names by type."""
        if not cls._creatures_database:
            cls.initialize_database()
        return [
            name for name, data in cls._creatures_database.items()
            if data.get("creature_type") == creature_type
        ]


