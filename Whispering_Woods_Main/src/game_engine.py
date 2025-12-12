"""Main game engine class."""

import random
import time
import sys
import os
from typing import Dict, List, Optional, Tuple, Any, Set
from datetime import datetime

from .colors import Colors
from .utils import slow_print, clear_screen, GAME_TITLE, GAME_VERSION, instant_print, colored_text, print_separator, get_input, SETTINGS
from .player import Player
from .location import Location
from .world_builder import WorldBuilder
from .item_factory import ItemFactory
from .creature_factory import CreatureFactory
from .crafting import CraftingSystem
from .combat import CombatSystem
from .weather import TimeWeatherSystem as WeatherSystem
from .quest_system import QuestSystem as QuestManager
from .achievement_system import AchievementSystem
from .admin import AdminPanel
from .save_system import SaveLoadSystem as SaveSystem
from .models import Item, Creature, Quest
from .data_store import select_difficulty_mode, get_difficulty_multipliers, select_starting_location

# ============================================================================
# MAIN GAME CLASS
# ============================================================================

class Game:
    """Main game class that manages the game loop and state."""
    
    def __init__(self):
        self.player = Player()
        self.world = WorldBuilder.create_world()
        self.time_weather = WeatherSystem()
        self.running = True
        
        # Integrate new routes from NEW_ROUTES_DATABASE and ADDITIONAL_ROUTES
        self._integrate_new_routes()
        
        # Initialize systems
        ItemFactory.initialize_database()
        CreatureFactory.initialize_database()
        CraftingSystem.initialize_recipes()
        QuestManager.initialize_quests()
        AchievementSystem.initialize_achievements()
    
    def _integrate_new_routes(self):
        """Integrate NEW_ROUTES_DATABASE and ADDITIONAL_ROUTES into existing locations."""
        # Check if NEW_ROUTES_DATABASE exists (defined at end of file)
        if 'NEW_ROUTES_DATABASE' in globals():
            for route_name, route_data in NEW_ROUTES_DATABASE.items():
                from_loc = route_data.get('from')
                to_loc = route_data.get('to')
                
                if from_loc in self.world:
                    location = self.world[from_loc]
                    # Find next available route number
                    max_num = max([r.number for r in location.routes] + [0])
                    new_route = Route(
                        number=max_num + 1,
                        destination=to_loc,
                        description=route_data.get('description', f"Path to {to_loc}"),
                        danger_level=route_data.get('danger_level', 1)
                    )
                    location.routes.append(new_route)
        
        # Also integrate ADDITIONAL_ROUTES if it exists
        if 'ADDITIONAL_ROUTES' in globals():
            for route_name, route_data in ADDITIONAL_ROUTES.items():
                from_loc = route_data.get('from')
                to_loc = route_data.get('to')
                
                if from_loc in self.world:
                    location = self.world[from_loc]
                    # Find next available route number
                    max_num = max([r.number for r in location.routes] + [0])
                    new_route = Route(
                        number=max_num + 1,
                        destination=to_loc,
                        description=route_data.get('description', f"Path to {to_loc}"),
                        danger_level=route_data.get('danger_level', 1)
                    )
                    location.routes.append(new_route)
    
    def start(self):
        """Start the game."""
        clear_screen()
        instant_print(colored_text(GAME_TITLE, Colors.BOLD_GREEN))
        print()
        
        slow_print(colored_text("Welcome to Lost in the Whispering Woods!", Colors.BOLD_CYAN))
        slow_print(colored_text("A text-based adventure game of mystery and survival.", Colors.CYAN))
        print()
        
        # Menu
        instant_print(colored_text("  [1] New Game", Colors.GREEN))
        instant_print(colored_text("  [2] Load Game", Colors.YELLOW))
        instant_print(colored_text("  [3] Options", Colors.CYAN))
        instant_print(colored_text("  [4] Quit", Colors.RED))
        print()
        
        choice = get_input("Choose: ")
        
        if choice == "1":
            self._new_game()
        elif choice == "2":
            loaded = SaveLoadSystem.load_game()
            if loaded:
                self.player = loaded.player
                self.world = loaded.world
                self.time_weather = loaded.time_weather
            else:
                self._new_game()
        elif choice == "3":
            self._show_options()
            self.start()
            return
        elif choice == "4":
            self.running = False
            return
        else:
            self.start()
            return
        
        # Start main game loop
        self._game_loop()
    
    def _new_game(self):
        """Start a new game."""
        clear_screen()
        
        # Select difficulty mode
        difficulty = select_difficulty_mode()
        
        # Select starting location  
        starting_location_id, starting_data = select_starting_location()
        
        slow_print(colored_text("\n═══ CHARACTER CREATION ═══\n", Colors.BOLD_CYAN))
        
        name = get_input("Enter your name (or press Enter for 'Traveler'): ")
        if not name:
            name = "Traveler"
        
        self.player = Player(name)
        self.player.difficulty_mode = difficulty
        self.player.current_location = starting_location_id
        
        # Give starting items from chosen location
        for item_id in starting_data.get('items', []):
            item = ItemFactory.create_item(item_id)
            if item:
                self.player.add_item(item)
        
        # Introduction
        self._show_introduction()
        
        # Start initial quest
        QuestManager.start_quest("escape_forest", self.player)
    
    def _show_introduction(self):
        """Show game introduction."""
        clear_screen()
        
        intro_text = """
You wake with a start, your head pounding and your memory a blank slate.

The first thing you notice is the smell - damp earth, decaying leaves, 
and something else... something ancient and strange.

You're lying on a bed of soft moss in a small clearing, surrounded by 
towering trees that seem to watch you with ancient, unknowing eyes. 
Sunlight filters through the canopy in dancing patterns, but beyond 
the clearing, the forest grows dark and dense.

You have no memory of how you got here. No memory of where you came 
from. All you know is a single, desperate urge burning in your chest:

You must find a way out of these woods.

The forest seems to stretch endlessly in every direction. Strange 
sounds echo from the shadows - birds, you hope, or perhaps something 
else entirely.

Your adventure begins...
"""
        
        for line in intro_text.strip().split('\n'):
            slow_print(colored_text(line, Colors.CYAN))
            time.sleep(0.3)
        
        get_input("\nPress Enter to continue...")
    
    def _game_loop(self):
        """Main game loop."""
        while self.running and self.player.health > 0:
            # Get current location
            location = self.world.get(self.player.current_location)
            if not location:
                slow_print(colored_text("Error: Invalid location!", Colors.RED))
                break
            
            # Clear screen and show location
            clear_screen()
            self._display_location(location)
            
            # Check for achievements
            AchievementSystem.check_achievements(self.player)
            
            # Check for victory
            if self.player.current_location == "freedom":
                self._handle_victory()
                break
            
            # Get player input
            command = get_input("\nWhat do you do? ")
            
            # Process command
            self._process_command(command, location)
            
            # Update game state
            self.player.update_status(5)
            self.time_weather.advance_time(5)
            self.player.play_time += 5
            
            # Auto-save
            if SETTINGS.auto_save and self.player.play_time % 60 == 0:
                SaveLoadSystem.save_game(self)
        
        # Handle death
        if self.player.health <= 0:
            self._handle_death()
    
    def _display_location(self, location: Location):
        """Display the current location."""
        # Mark as visited
        if not location.visited:
            location.visited = True
            if location.location_id not in self.player.discovered_locations:
                self.player.discovered_locations.append(location.location_id)
        location.visit_count += 1
        
        # Time and weather header
        instant_print(self.time_weather.get_status_display())
        
        # Location name
        print_separator("═", 78, Colors.BOLD_CYAN)
        instant_print(colored_text(f"  📍 {location.name}", Colors.BOLD_YELLOW))
        print_separator("═", 78, Colors.BOLD_CYAN)
        print()
        
        # Description
        description = location.get_description(
            self.time_weather.get_time_of_day(),
            self.time_weather.current_weather,
            self.player.has_light(),
            self.player.skills[SkillType.PERCEPTION]
        )
        slow_print(description, delay=0.01)
        
        # Items
        if location.items:
            instant_print(location.get_items_display())
        
        # Creatures
        if location.creatures:
            instant_print(location.get_creatures_display())
        
        # Routes
        instant_print(location.get_routes_display(self.player))
        
        # Quick commands
        instant_print(colored_text(
            "\n[Commands: 1-8 to move, look, take, use, inv, stats, map, craft, quests, help, admin]",
            Colors.DIM
        ))
    
    def _process_command(self, command: str, location: Location):
        """Process player command."""
        # Route navigation (numbers)
        if command.isdigit():
            self._handle_move(int(command), location)
            return
        
        # Text commands
        parts = command.split(maxsplit=1)
        cmd = parts[0] if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        
        if cmd in ["look", "l", "examine", "x"]:
            self._handle_look(args, location)
        elif cmd in ["take", "get", "grab", "pick"]:
            self._handle_take(args, location)
        elif cmd in ["use", "eat", "drink"]:
            self._handle_use(args)
        elif cmd in ["inv", "inventory", "i"]:
            instant_print(self.player.get_inventory_display())
            get_input("\nPress Enter...")
        elif cmd in ["equip", "wear"]:
            instant_print(self.player.equip_item(args))
        elif cmd in ["unequip", "remove"]:
            instant_print(self.player.unequip_item(args))
        elif cmd in ["equipment", "eq"]:
            instant_print(self.player.get_equipment_display())
            get_input("\nPress Enter...")
        elif cmd in ["stats", "status", "st"]:
            instant_print(self.player.get_status())
            get_input("\nPress Enter...")
        elif cmd in ["skills", "sk"]:
            instant_print(self.player.get_skills_display())
            get_input("\nPress Enter...")
        elif cmd in ["map", "m"]:
            self._show_map()
        elif cmd in ["craft", "c"]:
            self._handle_craft(args)
        elif cmd in ["quests", "q", "quest"]:
            instant_print(self.player.get_quests_display())
            get_input("\nPress Enter...")
        elif cmd in ["achievements", "ach"]:
            instant_print(AchievementSystem.get_achievements_display(self.player))
            get_input("\nPress Enter...")
        elif cmd in ["talk", "speak"]:
            self._handle_talk(args, location)
        elif cmd in ["attack", "fight", "kill"]:
            self._handle_attack(args, location)
        elif cmd in ["rest", "sleep"]:
            self._handle_rest(location)
        elif cmd in ["save"]:
            SaveLoadSystem.save_game(self)
        elif cmd in ["load"]:
            loaded = SaveLoadSystem.load_game()
            if loaded:
                self.player = loaded.player
                self.world = loaded.world
                self.time_weather = loaded.time_weather
        elif cmd in ["admin"]:
            AdminPanel.show_panel(self)
        elif cmd in ["fish", "fishing"]:
            self._start_fishing_minigame(location)
        elif cmd in ["lockpick", "pick"]:
            self._start_lockpicking_minigame(location)
        elif cmd in ["cards", "blackjack", "play"]:
            self._start_card_game()
        elif cmd in ["puzzle"]:
            self._start_puzzle_game()
        elif cmd in ["discover", "explore", "search"]:
            self._discover_expanded_content(location)
        elif cmd in ["summon"]:
            self._summon_creature(args)
        elif cmd in ["reveal", "revealmap", "showmap"]:
            self._reveal_all_locations()
        elif cmd in ["weather", "changeweather", "setweather"]:
            self._change_weather()
        elif cmd in ["time", "settime", "changetime"]:
            self._change_time()
        elif cmd in ["teleport", "goto", "warp"]:
            self._teleport_to_location()
        elif cmd in ["spawn", "spawnc", "creature"]:
            self._spawn_creature_command(args)
        elif cmd in ["learn", "train", "skill"]:
            self._train_skill()
        elif cmd in ["cast", "spell", "magic"]:
            self._cast_spell(args)
        elif cmd in ["read", "book", "lore"]:
            self._read_lore()
        elif cmd in ["faction", "reputation", "rep"]:
            self._view_factions()
        elif cmd in ["recruit", "companion", "hire"]:
            self._recruit_companion()
        elif cmd in ["event", "encounter", "random"]:
            self._trigger_random_event()
        elif cmd in ["dialogue"]:
            self._use_dialogue_system(location)
        elif cmd in ["maneuver", "move", "combatmove"]:
            self._view_combat_maneuvers()
        elif cmd in ["addgold", "gold+"]:
            self._add_gold(args)
        elif cmd in ["additem", "item+"]:
            self._add_item_command(args)
        elif cmd in ["heal", "fullheal"]:
            self._full_heal()
        elif cmd in ["levelup", "lvlup"]:
            self._level_up()
        elif cmd in ["addquest", "quest+"]:
            self._add_quest_command(args)
        elif cmd in ["complete", "completequest"]:
            self._complete_quest_command(args)
        elif cmd in ["unlock", "unlockach"]:
            self._unlock_achievement_command(args)
        elif cmd in ["addrecipe", "recipe+"]:
            self._add_recipe_command(args)
        elif cmd in ["help", "h", "?"]:
            self._show_help()
        elif cmd in ["quit", "exit"]:
            if self._confirm_quit():
                self.running = False
        else:
            slow_print(colored_text(f"Unknown command: {command}. Type 'help' for commands.", Colors.RED))
    
    def _start_fishing_minigame(self, location: Location):
        """Start the fishing mini-game"""
        if location and "fish" in location.special_actions:
            fishing_game = FishingGame()
            success, reward = fishing_game.play()
            if success:
                item = ItemFactory.create_item(reward)
                if item:
                    self.player.add_item(item)
                    slow_print(colored_text(f"🎣 You caught a {reward}!", Colors.GREEN))
        else:
            slow_print(colored_text("This is not a good fishing spot.", Colors.RED))
    
    def _start_lockpicking_minigame(self, location: Location):
        """Start the lockpicking mini-game"""
        if location and ("locked chest" in location.features or "locked door" in location.features):
            lockpick_game = LockpickingGame()
            if lockpick_game.play():
                slow_print(colored_text("🔓 You successfully picked the lock!", Colors.GREEN))
                # Give reward
                item = ItemFactory.create_item("golden key")
                if item:
                    self.player.add_item(item)
            else:
                slow_print(colored_text("🔒 You failed to pick the lock.", Colors.RED))
        else:
            slow_print(colored_text("There's nothing to lockpick here.", Colors.RED))
    
    def _start_card_game(self):
        """Start the card game"""
        card_game = CardGame(self.player)
        card_game.play()
    
    def _start_puzzle_game(self):
        """Start the puzzle game"""
        puzzle_game = PuzzleGame()
        if puzzle_game.play():
            slow_print(colored_text("🧩 You solved the puzzle!", Colors.GREEN))
            self.player.secrets_found += 1
        else:
            slow_print(colored_text("The puzzle remains unsolved.", Colors.YELLOW))
    
    def _discover_expanded_content(self, location: Location):
        """Discover expanded content through exploration"""
        if not hasattr(self, '_discovery_count'):
            self.player._discovery_count = 0
        
        if chance(40):  # 40% chance to find something
            self.player._discovery_count += 1
            
            discoveries = [
                ("legendary_weapon", "You discovered a legendary weapon hidden here!", "excalibur"),
                ("rare_creature", "A rare creature emerges from the shadows!", "ancient dragon"),
                ("epic_item", "You found an epic artifact!", "philosopher's stone"),
                ("boss_encounter", "A powerful boss appears!", "lich"),
                ("legendary_armor", "You uncovered legendary armor!", "dragon scale armor"),
            ]
            
            discovery_type, message, item_or_creature = discoveries[self.player._discovery_count % len(discoveries)]
            
            slow_print(colored_text(f"\n🌟 DISCOVERY! {message}", Colors.GOLD))
            
            if "weapon" in discovery_type or "item" in discovery_type or "armor" in discovery_type:
                # Try to create from expanded items
                item = ItemFactory.create_item(item_or_creature)
                if item:
                    self.player.add_item(item)
                    slow_print(colored_text(f"✓ Added {item.name} to inventory!", Colors.GREEN))
            elif "creature" in discovery_type or "boss" in discovery_type:
                # Try to create from expanded creatures
                creature = CreatureFactory.create_creature(item_or_creature)
                if creature:
                    slow_print(colored_text(f"⚔️ {creature.name} appeared! Prepare for battle!", Colors.RED))
                    from combat import Combat
                    combat = Combat(self.player, creature, self.time_weather)
                    combat.start_combat()
        else:
            slow_print(colored_text("You search thoroughly but find nothing unusual here.", Colors.YELLOW))
    
    def _summon_creature(self, creature_name: str):
        """Summon a creature from expanded database"""
        if not creature_name:
            slow_print(colored_text("Usage: summon <creature_name>", Colors.YELLOW))
            return
        
        creature = CreatureFactory.create_creature(creature_name.lower())
        if creature:
            slow_print(colored_text(f"🌀 You summon {creature.name}!", Colors.CYAN))
            if creature.creature_type == "HOSTILE":
                slow_print(colored_text("It attacks!", Colors.RED))
                from combat import Combat
                combat = Combat(self.player, creature, self.time_weather)
                combat.start_combat()
            else:
                slow_print(colored_text(f"{creature.name} appears friendly.", Colors.GREEN))
        else:
            slow_print(colored_text(f"Could not summon '{creature_name}'. Unknown creature.", Colors.RED))
    
    def _reveal_all_locations(self):
        """Reveal all locations on the map"""
        slow_print(colored_text("\n🗺️  Mystical Map Unfolds...", Colors.CYAN))
        self.player.known_locations = set(self.world.keys())
        slow_print(colored_text(f"All {len(self.world)} locations are now revealed!", Colors.GREEN))
        slow_print(colored_text("Use 'map' to see the full list.", Colors.YELLOW))
        get_input("\nPress Enter...")
    
    def _change_weather(self):
        """Change the current weather"""
        slow_print(colored_text("\n🌤️  Weather Control", Colors.CYAN))
        instant_print("1. Clear Skies\n2. Light Rain\n3. Heavy Rain\n4. Thunderstorm\n5. Snow\n6. Fog\n7. Blizzard")
        choice = get_input("Choose weather (1-7): ").strip()
        weather_map = {
            "1": "clear", "2": "light_rain", "3": "heavy_rain",
            "4": "thunderstorm", "5": "snow", "6": "fog", "7": "blizzard"
        }
        if choice in weather_map:
            self.time_weather.current_weather = weather_map[choice]
            slow_print(colored_text(f"Weather changed to: {self.time_weather.current_weather}", Colors.GREEN))
        else:
            slow_print(colored_text("Invalid choice.", Colors.RED))
        get_input("\nPress Enter...")
    
    def _change_time(self):
        """Change the time of day"""
        slow_print(colored_text("\n⏰ Time Control", Colors.CYAN))
        instant_print("1. Dawn (6:00)\n2. Morning (9:00)\n3. Noon (12:00)\n4. Afternoon (15:00)\n5. Dusk (18:00)\n6. Night (21:00)\n7. Midnight (0:00)")
        choice = get_input("Set time (1-7): ").strip()
        time_map = {
            "1": 6, "2": 9, "3": 12, "4": 15, "5": 18, "6": 21, "7": 0
        }
        if choice in time_map:
            self.time_weather.hour = time_map[choice]
            slow_print(colored_text(f"Time set to {self.time_weather.hour}:00", Colors.GREEN))
        else:
            slow_print(colored_text("Invalid choice.", Colors.RED))
        get_input("\nPress Enter...")
    
    def _teleport_to_location(self):
        """Teleport to a known location"""
        slow_print(colored_text("\n🌀 Teleportation", Colors.CYAN))
        slow_print(colored_text("Known locations:", Colors.YELLOW))
        known_locs = sorted(self.player.known_locations)
        for i, loc_id in enumerate(known_locs, 1):
            loc = self.world.get(loc_id)
            if loc:
                instant_print(f"{i}. {loc.name} ({loc_id})")
        
        choice = get_input("\nEnter location number or ID: ").strip()
        try:
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(known_locs):
                    target = known_locs[idx]
                else:
                    slow_print(colored_text("Invalid number.", Colors.RED))
                    get_input("\nPress Enter...")
                    return
            else:
                target = choice.lower()
            
            if target in self.world:
                self.player.current_location = target
                slow_print(colored_text("\n✨ Teleported!", Colors.GREEN))
                get_input("\nPress Enter...")
            else:
                slow_print(colored_text("Location not found.", Colors.RED))
                get_input("\nPress Enter...")
        except Exception as e:
            slow_print(colored_text(f"Error: {e}", Colors.RED))
            get_input("\nPress Enter...")
    
    def _spawn_creature_command(self, creature_name: str):
        """Spawn a creature for combat"""
        if not creature_name:
            slow_print(colored_text("Usage: spawn <creature_name>", Colors.YELLOW))
            return
        self._summon_creature(creature_name)
    
    def _train_skill(self):
        """Train a skill"""
        slow_print(colored_text("\n📚 Skill Training", Colors.CYAN))
        slow_print(colored_text("\nYour Skills:", Colors.YELLOW))
        for skill, level in self.player.skills.items():
            instant_print(f"  {skill}: {level}")
        
        instant_print("\n1. Train a skill (+1 level, costs 50 gold)")
        instant_print("2. Go back")
        choice = get_input("\nChoice: ").strip()
        
        if choice == "1":
            skill_name = get_input("Enter skill name: ").strip().lower()
            if skill_name in self.player.skills:
                if self.player.gold >= 50:
                    self.player.gold -= 50
                    self.player.skills[skill_name] += 1
                    slow_print(colored_text(f"\n✨ Skill improved! {skill_name}: {self.player.skills[skill_name]}", Colors.GREEN))
                else:
                    slow_print(colored_text("Not enough gold! Need 50 gold.", Colors.RED))
            else:
                slow_print(colored_text(f"Skill '{skill_name}' not found.", Colors.RED))
        get_input("\nPress Enter...")
    
    def _cast_spell(self, spell_name: str):
        """Cast a magic spell"""
        slow_print(colored_text("\n✨ Cast Spell", Colors.CYAN))
        if hasattr(self.player, 'mana'):
            instant_print(f"Mana: {self.player.mana}/100")
            if not spell_name:
                spell_name = get_input("Enter spell name: ").strip()
            if self.player.mana >= 20:
                self.player.mana -= 20
                slow_print(colored_text(f"\n✨ You cast {spell_name}!", Colors.MAGENTA))
                slow_print(colored_text("Magical energy surges through you!", Colors.CYAN))
            else:
                slow_print(colored_text("Not enough mana!", Colors.RED))
        else:
            self.player.mana = 100
            slow_print(colored_text("Magic awakens within you! You now have mana.", Colors.GREEN))
        get_input("\nPress Enter...")
    
    def _read_lore(self):
        """Read lore entries"""
        slow_print(colored_text("\n📖 Read Lore", Colors.CYAN))
        slow_print(colored_text("You search for readable materials...", Colors.YELLOW))
        instant_print("\nAvailable lore:")
        instant_print("1. The Creation of the World")
        instant_print("2. The Ancient Wars")
        instant_print("3. The Whispering Woods Legend")
        instant_print("4. The Lost Civilizations")
        instant_print("5. Return")
        choice = get_input("\nChoose: ").strip()
        if choice == "1":
            instant_print("\n" + "="*60)
            instant_print("THE CREATION OF THE WORLD")
            instant_print("="*60)
            slow_print("In the beginning, there was only void...")
            slow_print("Then came the First Light, and with it, life.")
            slow_print("The gods shaped the world from chaos.")
            instant_print("="*60)
        elif choice == "2":
            instant_print("\n" + "="*60)
            instant_print("THE ANCIENT WARS")
            instant_print("="*60)
            slow_print("For a thousand years, the kingdoms warred...")
            slow_print("Until the Treaty of Eternal Peace was signed.")
            slow_print("But peace never lasts forever...")
            instant_print("="*60)
        elif choice == "3":
            instant_print("\n" + "="*60)
            instant_print("THE WHISPERING WOODS LEGEND")
            instant_print("="*60)
            slow_print("They say the woods are alive, watching...")
            slow_print("Few who enter ever return the same.")
            slow_print("The trees whisper secrets of the ancient past.")
            instant_print("="*60)
        elif choice == "4":
            instant_print("\n" + "="*60)
            instant_print("THE LOST CIVILIZATIONS")
            instant_print("="*60)
            slow_print("Before our time, great civilizations rose and fell...")
            slow_print("Their ruins still dot the landscape.")
            slow_print("What knowledge did they possess?")
            instant_print("="*60)
        get_input("\nPress Enter...")
    
    def _view_factions(self):
        """View faction reputations"""
        slow_print(colored_text("\n⚔️  Faction Reputation", Colors.CYAN))
        if hasattr(self.player, 'reputation') and self.player.reputation:
            slow_print(colored_text("\nYour Standing:", Colors.YELLOW))
            for faction, rep in self.player.reputation.items():
                status = "Allied" if rep > 50 else "Friendly" if rep > 0 else "Neutral" if rep == 0 else "Hostile"
                instant_print(f"  {faction}: {rep} ({status})")
        else:
            slow_print(colored_text("No faction reputations yet.", Colors.YELLOW))
            self.player.reputation = {}
        get_input("\nPress Enter...")
    
    def _recruit_companion(self):
        """Recruit a companion"""
        slow_print(colored_text("\n👥 Recruit Companion", Colors.CYAN))
        instant_print("Available companions:")
        instant_print("1. Aria Stormborn (Warrior) - 100 gold")
        instant_print("2. Thorne Blackforge (Blacksmith) - 100 gold")
        instant_print("3. Luna Shadowstep (Rogue) - 100 gold")
        instant_print("4. Eldrin Magelight (Mage) - 150 gold")
        instant_print("5. Return")
        choice = get_input("\nChoose: ").strip()
        companions_map = {
            "1": ("Aria Stormborn", 100),
            "2": ("Thorne Blackforge", 100),
            "3": ("Luna Shadowstep", 100),
            "4": ("Eldrin Magelight", 150)
        }
        if choice in companions_map:
            companion_name, cost = companions_map[choice]
            if self.player.gold >= cost:
                self.player.gold -= cost
                if not hasattr(self.player, 'companions'):
                    self.player.companions = []
                self.player.companions.append(companion_name)
                slow_print(colored_text(f"\n✨ {companion_name} joins your party!", Colors.GREEN))
            else:
                slow_print(colored_text(f"Need {cost} gold to recruit this companion!", Colors.RED))
        get_input("\nPress Enter...")
    
    def _trigger_random_event(self):
        """Trigger a random event"""
        import random
        slow_print(colored_text("\n🎲 Random Encounter!", Colors.YELLOW))
        events = [
            "You hear distant drums in the forest...",
            "A mysterious stranger approaches...",
            "The ground begins to shake!",
            "You find an ancient altar...",
            "A child appears, looking lost...",
            "Strange lights dance in the distance...",
            "You hear a dragon's roar...",
            "A merchant's caravan passes by...",
        ]
        event = random.choice(events)
        slow_print(colored_text(f"\n{event}", Colors.CYAN))
        instant_print("\nWhat do you do?")
        instant_print("1. Investigate")
        instant_print("2. Ignore and continue")
        choice = get_input("Choice: ").strip()
        if choice == "1":
            slow_print(colored_text("You investigate the occurrence...", Colors.YELLOW))
            if random.random() < 0.5:
                reward = random.randint(10, 50)
                self.player.gold += reward
                slow_print(colored_text(f"You found {reward} gold!", Colors.GREEN))
            else:
                slow_print(colored_text("Nothing of interest...", Colors.YELLOW))
        get_input("\nPress Enter...")
    
    def _use_dialogue_system(self, location: Location):
        """Use the dialogue system"""
        slow_print(colored_text("\n💬 Dialogue", Colors.CYAN))
        slow_print(colored_text("You look for someone to talk to...", Colors.YELLOW))
        if location and location.creatures:
            instant_print(f"\nYou can talk to:")
            for i, creature_id in enumerate(location.creatures, 1):
                instant_print(f"{i}. {creature_id}")
            choice = get_input("\nWho? (number): ").strip()
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(location.creatures):
                    creature_id = location.creatures[idx]
                    creature = CreatureFactory.create_creature(creature_id)
                    if creature and creature.dialogue:
                        slow_print(colored_text(f"\n{creature.name}:", Colors.YELLOW))
                        slow_print(colored_text(creature.dialogue[0] if creature.dialogue else "...", Colors.CYAN))
                    else:
                        slow_print(colored_text("They don't want to talk.", Colors.RED))
                else:
                    slow_print(colored_text("Invalid choice.", Colors.RED))
            except:
                slow_print(colored_text("Invalid input.", Colors.RED))
        else:
            slow_print(colored_text("No one here to talk to.", Colors.YELLOW))
        get_input("\nPress Enter...")
    
    def _view_combat_maneuvers(self):
        """View available combat maneuvers"""
        slow_print(colored_text("\n⚔️  Combat Maneuvers", Colors.CYAN))
        instant_print("\nAvailable maneuvers:")
        instant_print("1. Power Strike - Extra damage, costs stamina")
        instant_print("2. Defensive Stance - Reduce incoming damage")
        instant_print("3. Quick Attack - Fast but less damage")
        instant_print("4. Combo Strike - Chain attacks")
        instant_print("5. Counter Attack - Parry and strike")
        instant_print("6. Whirlwind - Hit multiple enemies")
        instant_print("\nUse these in combat for tactical advantages!")
        get_input("\nPress Enter...")
    
    def _add_gold(self, amount_str: str):
        """Add gold to player"""
        try:
            amount = int(amount_str) if amount_str else 100
            self.player.gold += amount
            slow_print(colored_text(f"\n💰 Added {amount} gold! Total: {self.player.gold}", Colors.GOLD))
        except:
            slow_print(colored_text("Usage: addgold <amount>", Colors.RED))
        get_input("\nPress Enter...")
    
    def _add_item_command(self, item_name: str):
        """Add an item to player inventory"""
        if not item_name:
            slow_print(colored_text("Usage: additem <item_name>", Colors.RED))
        else:
            item = ItemFactory.create_item(item_name.lower())
            if item:
                self.player.add_item(item)
                slow_print(colored_text(f"\n✨ Added {item.name} to inventory!", Colors.GREEN))
            else:
                slow_print(colored_text(f"Item '{item_name}' not found.", Colors.RED))
        get_input("\nPress Enter...")
    
    def _full_heal(self):
        """Fully heal the player"""
        self.player.health = self.player.max_health
        if hasattr(self.player, 'mana'):
            self.player.mana = 100
        if hasattr(self.player, 'stamina'):
            self.player.stamina = 100
        slow_print(colored_text("\n💚 Fully healed! HP, mana, and stamina restored!", Colors.GREEN))
        get_input("\nPress Enter...")
    
    def _level_up(self):
        """Level up the player"""
        self.player.level += 1
        self.player.max_health += 10
        self.player.health = self.player.max_health
        self.player.attack += 2
        self.player.defense += 1
        slow_print(colored_text(f"\n⭐ Level Up! Now level {self.player.level}!", Colors.GOLD))
        slow_print(colored_text(f"HP +10, ATK +2, DEF +1", Colors.GREEN))
        get_input("\nPress Enter...")
    
    def _add_quest_command(self, quest_name: str):
        """Add a quest to the player"""
        if not quest_name:
            slow_print(colored_text("Usage: addquest <quest_name>", Colors.RED))
        else:
            slow_print(colored_text(f"\n📜 Added quest: {quest_name}", Colors.GREEN))
            # Add to player's active quests if quest system exists
        get_input("\nPress Enter...")
    
    def _complete_quest_command(self, quest_name: str):
        """Complete a quest"""
        if not quest_name:
            slow_print(colored_text("Usage: completequest <quest_name>", Colors.RED))
        else:
            slow_print(colored_text(f"\n✅ Completed quest: {quest_name}", Colors.GREEN))
            slow_print(colored_text("Reward: 100 gold, 50 XP", Colors.GOLD))
            self.player.gold += 100
        get_input("\nPress Enter...")
    
    def _unlock_achievement_command(self, ach_name: str):
        """Unlock an achievement"""
        if not ach_name:
            slow_print(colored_text("Usage: unlockach <achievement_name>", Colors.RED))
        else:
            slow_print(colored_text(f"\n🏆 Achievement Unlocked: {ach_name}!", Colors.GOLD))
        get_input("\nPress Enter...")
    
    def _add_recipe_command(self, recipe_name: str):
        """Add a crafting recipe"""
        if not recipe_name:
            slow_print(colored_text("Usage: addrecipe <recipe_name>", Colors.RED))
        else:
            slow_print(colored_text(f"\n📋 Learned recipe: {recipe_name}", Colors.GREEN))
        get_input("\nPress Enter...")
    
    def _handle_move(self, route_num: int, location: Location):
        """Handle movement to a new location."""
        route = location.get_route_by_number(route_num)
        
        if not route:
            slow_print(colored_text(f"There is no path {route_num} here.", Colors.RED))
            return
        
        # Check accessibility
        accessible, reason = route.is_accessible(self.player)
        if not accessible:
            slow_print(colored_text(reason, Colors.RED))
            return
        
        # Move to new location
        self.player.previous_location = self.player.current_location
        self.player.current_location = route.destination
        self.player.steps_taken += 1
        
        # Check for random encounters
        if route.danger_level > 0 and chance(route.danger_level * 10):
            self._random_encounter()
    
    def _handle_look(self, target: str, location: Location):
        """Handle looking at something."""
        if not target:
            slow_print(location.get_description(
                self.time_weather.get_time_of_day(),
                self.time_weather.current_weather,
                self.player.has_light(),
                self.player.skills[SkillType.PERCEPTION]
            ))
            return
        
        # Look at item in location
        for item in location.items:
            if target.lower() in item.name.lower():
                slow_print(colored_text(f"{item.name}: {item.description}", item.get_rarity_color()))
                return
        
        # Look at creature
        for creature in location.creatures:
            if target.lower() in creature.name.lower() and creature.alive:
                slow_print(colored_text(f"{creature.name}: {creature.description}", Colors.MAGENTA))
                return
        
        # Look at feature
        for feature in location.features:
            if target.lower() in feature.lower():
                slow_print(colored_text(f"You examine the {feature}.", Colors.CYAN))
                return
        
        slow_print(colored_text(f"You don't see '{target}' here.", Colors.RED))
    
    def _handle_take(self, item_name: str, location: Location):
        """Handle taking an item."""
        if not item_name:
            slow_print(colored_text("Take what?", Colors.YELLOW))
            return
        
        for item in location.items[:]:
            if item_name.lower() in item.name.lower():
                success, msg = self.player.add_item(item)
                if success:
                    location.items.remove(item)
                    slow_print(colored_text(msg, Colors.GREEN))
                else:
                    slow_print(colored_text(msg, Colors.RED))
                return
        
        slow_print(colored_text(f"There's no '{item_name}' here to take.", Colors.RED))
    
    def _handle_use(self, item_name: str):
        """Handle using an item."""
        if not item_name:
            slow_print(colored_text("Use what?", Colors.YELLOW))
            return
        
        item = self.player.get_item(item_name)
        if not item:
            slow_print(colored_text(f"You don't have '{item_name}'.", Colors.RED))
            return
        
        if not item.usable:
            slow_print(colored_text(f"You can't use {item.name}.", Colors.RED))
            return
        
        result = item.use_effect(self.player)
        slow_print(colored_text(result, Colors.GREEN))
        self.player.remove_item(item.name)
    
    def _handle_talk(self, target: str, location: Location):
        """Handle talking to a creature."""
        for creature in location.creatures:
            if creature.alive and (not target or target.lower() in creature.name.lower()):
                if creature.dialogue:
                    dialogue = creature.get_dialogue()
                    slow_print(colored_text(f"\n{creature.name} says:", Colors.CYAN))
                    slow_print(colored_text(f'"{dialogue}"', Colors.WHITE))
                    return
                else:
                    slow_print(colored_text(f"The {creature.name} doesn't respond.", Colors.DIM))
                    return
        
        slow_print(colored_text("There's no one here to talk to.", Colors.RED))
    
    def _handle_attack(self, target: str, location: Location):
        """Handle attacking a creature."""
        for creature in location.creatures:
            if creature.alive and (not target or target.lower() in creature.name.lower()):
                if CombatSystem.start_combat(self.player, creature):
                    # Victory - creature is dead
                    pass
                else:
                    # Fled or died
                    pass
                return
        
        slow_print(colored_text("There's nothing here to attack.", Colors.RED))
    
    def _handle_rest(self, location: Location):
        """Handle resting."""
        if not location.rest_allowed:
            slow_print(colored_text("You can't rest here - it's too dangerous.", Colors.RED))
            return
        
        # Check for hostile creatures
        hostile = [c for c in location.creatures if c.alive and c.hostile]
        if hostile:
            slow_print(colored_text("You can't rest with enemies nearby!", Colors.RED))
            return
        
        result = self.player.rest(8)
        self.time_weather.advance_time(480)
        slow_print(result)
    
    def _handle_craft(self, recipe_name: str):
        """Handle crafting."""
        if not recipe_name:
            instant_print(CraftingSystem.get_craftable_display(self.player))
            recipe_name = get_input("Craft which item? (or 'cancel'): ")
            if recipe_name == "cancel":
                return
        
        success, msg = CraftingSystem.craft_item(recipe_name, self.player)
        slow_print(msg)
    
    def _show_map(self):
        """Show discovered locations."""
        lines = [colored_text("\n╔══════════════════════════════════════════════════════════════╗", Colors.CYAN)]
        lines.append(colored_text("║                    DISCOVERED LOCATIONS                      ║", Colors.CYAN))
        lines.append(colored_text("║══════════════════════════════════════════════════════════════║", Colors.CYAN))
        
        for loc_id in sorted(self.player.discovered_locations):
            location = self.world.get(loc_id)
            if location:
                if loc_id == self.player.current_location:
                    lines.append(colored_text(f"║  📍 {location.name} (Current)", Colors.BOLD_GREEN))
                else:
                    lines.append(colored_text(f"║     {location.name}", Colors.WHITE))
        
        lines.append(colored_text(f"║──────────────────────────────────────────────────────────────║", Colors.CYAN))
        lines.append(colored_text(f"║  Discovered: {len(self.player.discovered_locations)}/{len(self.world)} locations", Colors.YELLOW))
        lines.append(colored_text("╚══════════════════════════════════════════════════════════════╝", Colors.CYAN))
        
        instant_print("\n".join(lines))
        get_input("\nPress Enter...")
    
    def _show_help(self):
        """Show help information."""
        help_text = """
╔══════════════════════════════════════════════════════════════╗
║                         COMMANDS                             ║
║══════════════════════════════════════════════════════════════║
║  MOVEMENT & WORLD:                                           ║
║    1-8          - Take numbered path                         ║
║    reveal       - Reveal all locations on map                ║
║    teleport     - Teleport to a known location               ║
║    weather      - Change weather                             ║
║    time         - Change time of day                         ║
║                                                              ║
║  ACTIONS & EXPLORATION:                                      ║
║    look [thing] - Examine surroundings or specific thing     ║
║    take [item]  - Pick up an item                            ║
║    use [item]   - Use an item from inventory                 ║
║    talk [npc]   - Talk to a creature                         ║
║    dialogue     - Use advanced dialogue system               ║
║    attack [foe] - Attack a creature                          ║
║    rest         - Rest to recover (8 hours)                  ║
║    discover     - Search for legendary items/creatures       ║
║    event        - Trigger random encounter                   ║
║                                                              ║
║  CREATURES & COMBAT:                                         ║
║    summon [name]- Summon a creature                          ║
║    spawn [name] - Spawn creature for combat                  ║
║    maneuver     - View combat maneuvers                      ║
║                                                              ║
║  CHARACTER DEVELOPMENT:                                      ║
║    inv          - Show inventory                             ║
║    equip [item] - Equip an item                              ║
║    unequip slot - Unequip from slot                          ║
║    equipment    - Show equipment                             ║
║    stats        - Show character status                      ║
║    skills       - Show skills                                ║
║    learn        - Train a skill (+1 level, 50 gold)          ║
║    levelup      - Level up your character                    ║
║    heal         - Fully restore health/mana/stamina          ║
║                                                              ║
║  MAGIC & ABILITIES:                                          ║
║    cast [spell] - Cast a magic spell                         ║
║    read         - Read lore entries and books                ║
║                                                              ║
║  SOCIAL & FACTIONS:                                          ║
║    faction      - View faction reputations                   ║
║    recruit      - Recruit a companion (costs gold)           ║
║                                                              ║
║  PROGRESSION:                                                ║
║    quests       - Show active quests                         ║
║    addquest     - Add a quest                                ║
║    complete     - Complete a quest                           ║
║    achievements - Show achievements                          ║
║    unlock       - Unlock an achievement                      ║
║    addrecipe    - Learn a crafting recipe                    ║
║                                                              ║
║  RESOURCES:                                                  ║
║    addgold [n]  - Add gold to inventory                      ║
║    additem [i]  - Add item to inventory                      ║
║                                                              ║
║  MINI-GAMES:                                                 ║
║    fish         - Try fishing (at fishing spots)             ║
║    lockpick     - Pick locks (on chests/doors)               ║
║    cards        - Play blackjack card game                   ║
║    puzzle       - Solve a puzzle                             ║
║                                                              ║
║  SYSTEM:                                                     ║
║    map          - Show discovered locations                  ║
║    craft        - Open crafting menu                         ║
║    save         - Save game                                  ║
║    load         - Load game                                  ║
║    admin        - Open admin panel (advanced features)       ║
║    help         - Show this help                             ║
║    quit         - Quit game                                  ║
╚══════════════════════════════════════════════════════════════╝
"""
        instant_print(colored_text(help_text, Colors.CYAN))
        get_input("\nPress Enter...")
    
    def _show_options(self):
        """Show and modify game options."""
        while True:
            clear_screen()
            instant_print(colored_text("\n═══ OPTIONS ═══\n", Colors.BOLD_CYAN))
            instant_print(f"[1] Text Speed: {SETTINGS.text_speed}")
            instant_print(f"[2] Enable Colors: {SETTINGS.enable_colors}")
            instant_print(f"[3] Auto-Save: {SETTINGS.auto_save}")
            instant_print(f"[4] Show Hints: {SETTINGS.show_hints}")
            instant_print("[0] Back")
            
            choice = get_input("\nOption: ")
            
            if choice == "0":
                break
            elif choice == "1":
                try:
                    speed = float(get_input("Text speed (0-0.1): "))
                    SETTINGS.text_speed = max(0, min(0.1, speed))
                except ValueError:
                    pass
            elif choice == "2":
                SETTINGS.enable_colors = not SETTINGS.enable_colors
            elif choice == "3":
                SETTINGS.auto_save = not SETTINGS.auto_save
            elif choice == "4":
                SETTINGS.show_hints = not SETTINGS.show_hints
    
    def _random_encounter(self):
        """Handle a random encounter."""
        if chance(30):
            # Hostile encounter
            creature_choices = ["wolf", "goblin", "giant spider", "bandit"]
            creature = CreatureFactory.create_creature(random.choice(creature_choices))
            if creature:
                CombatSystem.start_combat(self.player, creature)
    
    def _confirm_quit(self) -> bool:
        """Confirm quitting the game."""
        response = get_input("Save before quitting? (y/n): ")
        if response == "y":
            SaveLoadSystem.save_game(self)
        return True
    
    def _handle_death(self):
        """Handle player death."""
        self.player.deaths += 1
        
        death_text = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║                              💀 YOU HAVE DIED 💀                              ║
║                                                                               ║
║        The Whispering Woods have claimed another victim...                    ║
║                                                                               ║
║        Your journey ends here, lost and forgotten in the                      ║
║        endless depths of the ancient forest.                                  ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""
        print_event_box(death_text, EventType.DEATH)
        
        response = get_input("\n[1] Load last save\n[2] Start new game\n[3] Quit\n\nChoice: ")
        
        if response == "1":
            loaded = SaveLoadSystem.load_game()
            if loaded:
                self.player = loaded.player
                self.world = loaded.world
                self.time_weather = loaded.time_weather
                self._game_loop()
        elif response == "2":
            self.__init__()
            self._new_game()
            self._game_loop()
    
    def _handle_victory(self):
        """Handle game victory."""
        victory_text = f"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║                        🎉 CONGRATULATIONS! 🎉                                  ║
║                                                                               ║
║             You have escaped the Whispering Woods!                            ║
║                                                                               ║
║        After facing countless dangers, solving ancient puzzles,               ║
║        and battling fearsome creatures, you finally found                     ║
║        your way out of the mysterious forest.                                 ║
║                                                                               ║
║══════════════════════════════════════════════════════════════════════════════║
║                           FINAL STATISTICS                                    ║
║══════════════════════════════════════════════════════════════════════════════║
║                                                                               ║
║   Time Played: {format_time(self.player.play_time):>10}                                        ║
║   Days Survived: {self.time_weather.day_count:>8}                                          ║
║   Steps Taken: {self.player.steps_taken:>10}                                          ║
║   Enemies Defeated: {self.player.kills:>5}                                             ║
║   Bosses Slain: {self.player.boss_kills:>8}                                            ║
║   Items Collected: {self.player.items_collected:>6}                                           ║
║   Items Crafted: {self.player.items_crafted:>8}                                           ║
║   Quests Completed: {len(self.player.completed_quests):>5}                                            ║
║   Gold Collected: {self.player.gold:>7}                                            ║
║   Final Level: {self.player.level:>10}                                            ║
║   Achievements: {len(self.player.achievements):>9}                                             ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""
        
        clear_screen()
        slow_print(colored_text(victory_text, Colors.BOLD_GREEN))
        
        # Unlock escape achievement
        AchievementSystem._try_unlock("escape_artist", self.player)
        
        # Check for special achievements
        if self.player.kills == 0:
            AchievementSystem._try_unlock("pacifist", self.player)
        if self.time_weather.day_count <= 3:
            AchievementSystem._try_unlock("speedrunner", self.player)
        
        get_input("\nPress Enter to continue...")
        
        # Show final achievements
        instant_print(AchievementSystem.get_achievements_display(self.player))
        
        get_input("\nThank you for playing Lost in the Whispering Woods!")



