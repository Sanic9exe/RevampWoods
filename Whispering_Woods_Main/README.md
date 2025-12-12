# Lost in the Whispering Woods

A comprehensive text-based adventure game with deep RPG mechanics, rich storytelling, and extensive content.

## Overview

You wake up in a mysterious forest with no memory of how you got there. Your goal: Find your way out before the forest claims you forever. Explore over 70 unique locations, meet diverse NPCs, complete quests, craft items, battle creatures, and uncover the secrets of the Whispering Woods.

## Features

### Core Gameplay
- **Numbered route selection** (1-8 options) for intuitive navigation
- **Slow-typed text** for immersive storytelling
- **Colored terminal output** for visual enhancement
- **Multiple difficulty modes** (Story, Normal, Hard, Nightmare with permadeath)
- **Save/Load system** to preserve your progress
- **Day/night cycle** with dynamic time progression
- **Weather system** affecting gameplay and atmosphere

### Game Systems

#### Quest System (25+ Quests)
- Main storyline quests
- Side quests with branching paths
- Character-specific quests
- Hidden achievement quests
- Dynamic quest objectives

#### Combat System
- Turn-based combat with strategy elements
- 100+ unique combat maneuvers
- 50+ creature types (Normal, Elite, Bosses, Legendary)
- Special abilities and status effects
- Tactical retreat options

#### Crafting System (20+ Recipes)
- Resource gathering and combination
- Weapon and armor crafting
- Potion brewing
- Tool creation
- Upgradable equipment

#### Companion System (15+ Unique Allies)
- Beast, magical, human, and construct companions
- Each with distinct abilities and personality
- Special recruitment quests
- Companion-specific dialogue and interactions

#### Magic System
- Spellcasting with resource management
- 80+ unique spells
- Spell learning and progression
- Elemental affinities

#### Achievement System (150+ Achievements)
- Combat achievements
- Exploration milestones
- Quest completions
- Hidden discoveries
- Collectible tracking

### Content

#### Locations (70+ Unique Areas)
- Diverse biomes (Forest, Mountain, Swamp, Ruins, Caves, Villages)
- Each location with unique description and features
- Dynamic environmental descriptions (500+ variations)
- Interconnected world map
- Hidden areas and secrets

#### NPCs (300+ Unique Characters)
- Each with unique personality and backstory
- Profession-based interactions
- Dynamic dialogue trees
- Location-specific characters
- Quest givers and merchants

#### Items (200+ Purposeful Items)
- Weapons with varied stats and abilities
- Armor and accessories for defense
- Consumables for survival and buffs
- Tools for exploration and crafting
- Quest items and treasures
- Materials for crafting

#### Creatures (100+ Quality Enemies)
- Appropriate difficulty progression
- Unique abilities and loot drops
- Boss encounters and mini-bosses
- Legendary creatures with special mechanics

#### Lore System (200+ Entries)
- Discoverable books and scrolls
- World history and mythology
- Character backstories
- Hidden secrets and mysteries

### Additional Features
- **Random Events System** (300+ unique events)
- **Faction System** (15+ factions with relationships)
- **Status Effects** (80+ conditions)
- **Weather Patterns** (100+ variations)
- **Mini-games** for variety and rewards
- **Reputation System** affecting NPC interactions
- **Admin Panel** for debugging and content management

## Installation

### Requirements
- Python 3.7 or higher
- Terminal with ANSI color support (most modern terminals)

### Quick Start

1. Clone or download the repository
2. Navigate to the `Whispering_Woods_Main` directory
3. Run the game:

```bash
# On Unix/Linux/Mac
./run_game.sh

# Or directly with Python
python3 game.py

# On Windows
python game.py
```

## Project Structure

```
Whispering_Woods_Main/
├── game.py                 # Main game entry point
├── run_game.sh            # Launch script (Unix/Linux/Mac)
├── README.md              # This file
├── src/                   # Python modules
│   ├── __init__.py       # Package initialization
│   ├── colors.py         # Terminal color codes
│   ├── utils.py          # Utility functions and constants
│   ├── models.py         # Data models and classes
│   ├── player.py         # Player character class
│   ├── location.py       # Location class
│   ├── item_factory.py   # Item creation system
│   ├── creature_factory.py  # Creature creation system
│   ├── world_builder.py  # World generation
│   ├── crafting.py       # Crafting system
│   ├── combat.py         # Combat mechanics
│   ├── weather.py        # Time and weather system
│   ├── quest_system.py   # Quest management
│   ├── achievement_system.py  # Achievement tracking
│   ├── admin.py          # Admin panel
│   ├── save_system.py    # Save/load functionality
│   ├── game_engine.py    # Main game loop and logic
│   └── data_store.py     # Game content data
└── data/                  # (Future: JSON data files)
```

## Gameplay Guide

### Starting the Game
1. Choose your difficulty mode
2. Select your starting location (8 options with varying difficulty)
3. Begin your adventure!

### Controls
- Enter numbers (1-8) to select routes/options
- Follow on-screen prompts for combat and interactions
- Type 'help' for available commands during gameplay
- Type 'admin' for admin panel access (password required)

### Tips for Survival
- Manage your health, hunger, and thirst carefully
- Explore thoroughly to find items and resources
- Complete quests for experience and rewards
- Build relationships with NPCs for better interactions
- Save your progress frequently
- Craft items to improve your chances of survival
- Pay attention to environmental descriptions for clues
- Choose companions wisely for their unique abilities

### Admin Panel
The admin panel provides powerful tools for content management and debugging:
- Password: `forestmaster2024`
- Modify player stats and inventory
- Spawn creatures and items
- Teleport to any location
- View game state and debug information
- Manage quests and achievements

## Development

### Code Organization
The game code is organized into logical modules:
- **colors.py**: ANSI color codes for terminal formatting
- **utils.py**: Shared utilities, constants, and enumerations
- **models.py**: Data classes for game entities
- **player.py**: Player character with stats, inventory, and abilities
- **location.py**: Location system with numbered routes
- **item_factory.py**: Dynamic item creation
- **creature_factory.py**: Dynamic creature creation
- **world_builder.py**: World generation and location connections
- **combat.py**: Turn-based combat system
- **crafting.py**: Item crafting mechanics
- **weather.py**: Time and weather simulation
- **quest_system.py**: Quest tracking and management
- **achievement_system.py**: Achievement unlocking
- **admin.py**: Administrative tools
- **save_system.py**: Game state persistence
- **game_engine.py**: Main game loop and orchestration
- **data_store.py**: All game content (NPCs, items, creatures, etc.)

### Content Management
All game content is stored in the `data_store.py` module:
- Easy to find and modify content
- Centralized data management
- No need to hunt through code for content
- Future migration to JSON files possible

### External Data System (Future Enhancement)
The structure supports future migration to JSON files in the `data/` directory:
- `npcs.json` - NPC definitions
- `items.json` - Item database
- `creatures.json` - Creature types
- `locations.json` - Location descriptions
- `quests.json` - Quest definitions
- `achievements.json` - Achievement criteria
- And more...

## Version History

### Version 2.0.0 - Complete Revamp
- Reorganized into modular structure
- Separated code and data
- 70+ unique locations
- 300+ NPCs
- 200+ items
- 100+ creatures
- 150+ achievements
- 25+ quests
- 20+ crafting recipes
- 15+ companions
- Complete game systems
- Admin panel
- Save/load system

## Credits

**Game Design & Development**: Claude
**Platform**: Text-based terminal game
**Engine**: Python 3

## License

This game is provided as-is for educational and entertainment purposes.

---

**Enjoy your adventure in the Whispering Woods!**
