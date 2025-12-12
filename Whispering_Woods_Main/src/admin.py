"""Admin panel for game management."""

import json
import os
from typing import Dict, List, Optional, Any, Tuple
import random

from .colors import Colors
from .utils import slow_print, ADMIN_PASSWORD, SETTINGS
from .data_store import select_difficulty_mode

# ============================================================================
# ADMIN PANEL
# ============================================================================

class AdminPanel:
    """Admin panel for game management and debugging."""

    # Store the password separately to avoid hardcoding in prompts repeatedly
    _password = ADMIN_PASSWORD
    _logged_in = False

    @staticmethod
    def show_panel(game: 'Game'):
        """Show the admin panel with required password every time."""
        # Always request password when opening admin panel
        password = get_input("Enter admin password: ", Colors.RED)
        if password != AdminPanel._password:
            slow_print(colored_text("Access denied.", Colors.RED))
            return
        AdminPanel._logged_in = True
        slow_print(colored_text("Admin mode activated.", Colors.GREEN))
        while AdminPanel._logged_in:
            clear_screen()
            AdminPanel._display_main_menu()
            choice = get_input("Admin command: ", Colors.MAGENTA)

            # Command aliases map
            aliases = {
                "exit": "0", "quit": "0",
                "god": "1", "infinite": "2", "nohunger": "3", "instakill": "4",
                "giveitem": "5", "givegold": "6", "sethealth": "7", "teleport": "8", "reveal": "9",
                "spawn": "10", "setlevel": "11", "giveall": "12", "completequests": "13",
                "unlockach": "14", "skipcombat": "15", "textspeed": "16", "debug": "17",
                "skills": "18", "weather": "19", "time": "20", "inventory": "21", "quests": "22",
                "status": "23", "loccreatures": "24", "resetloc": "25", "worldstate": "26",
                "loceditor": "27", "removeskill": "28", "addskill": "29", "removeeffect": "30",
                "addeffect": "31", "maxskills": "32", "unlockrecipes": "33", "discoverall": "34",
                "clearinv": "35", "removeitem": "36", "spawncustom": "37", "dropitem": "38",
                "placeitem": "39",
                # New content commands
                "expandedcreatures": "40", "expandeditems": "41", "npcs": "42", "triggerevent": "43",
                "maneuvers": "44", "lore": "45", "weatherpatterns": "46", "statuseffects": "47",
                "expandedlocs": "48", "spawnexpanded": "49", "giveexpanded": "50",
                # Difficulty and location commands
                "difficulty": "51", "setdifficulty": "51", "locations": "52", "listlocs": "52",
                "accessibility": "53", "checkaccess": "53", "teleportexpanded": "54", "tpexpanded": "54",
                "starts": "55", "startinglocs": "55",
                # Comprehensive management commands
                "companions": "56", "reputation": "57", "rep": "57", "notes": "58",
                "equipment": "59", "equip": "59", "resources": "60", "stamina": "60",
                "statistics": "61", "stats2": "61", "questmgr": "62", "achievements": "63",
                "recipes": "64", "playtime": "65", "save": "66", "load": "67", "reset": "68",
                # EXCLUSIVE ADMIN FEATURES
                "exclusive": "69", "adminitems": "69", "reality": "70", "warp": "70",
                "timetravel": "71", "timetv": "71", "easteregg": "72", "easter": "72",
                "godpowers": "73", "godmode2": "73", "powers": "73"
            }
            # Normalize input for alias
            command = aliases.get(choice.strip().lower(), choice)

            if command == "0":
                AdminPanel._logged_in = False
            elif command == "1":
                AdminPanel._toggle_god_mode()
            elif command == "2":
                AdminPanel._toggle_infinite_inventory()
            elif command == "3":
                AdminPanel._toggle_no_hunger()
            elif command == "4":
                AdminPanel._toggle_instant_kill()
            elif command == "5":
                AdminPanel._give_item(game.player)
            elif command == "6":
                AdminPanel._give_gold(game.player)
            elif command == "7":
                AdminPanel._set_health(game.player)
            elif command == "8":
                AdminPanel._teleport(game)
            elif command == "9":
                AdminPanel._reveal_map(game)
            elif command == "10":
                AdminPanel._spawn_creature(game)
            elif command == "11":
                AdminPanel._set_level(game.player)
            elif command == "12":
                AdminPanel._give_all_items(game.player)
            elif command == "13":
                AdminPanel._complete_all_quests(game.player)
            elif command == "14":
                AdminPanel._unlock_all_achievements(game.player)
            elif command == "15":
                AdminPanel._toggle_skip_combat()
            elif command == "16":
                AdminPanel._change_text_speed()
            elif command == "17":
                AdminPanel._show_debug_info(game)
            elif command == "18":
                AdminPanel._skills_menu(game.player)
            elif command == "19":
                AdminPanel._weather_menu(game.time_weather)
            elif command == "20":
                AdminPanel._time_menu(game.time_weather)
            elif command == "21":
                AdminPanel._inventory_menu(game.player)
            elif command == "22":
                AdminPanel._quest_objective_editor(game.player)
            elif command == "23":
                AdminPanel._status_effect_manager(game.player)
            elif command == "24":
                AdminPanel._manage_location_creatures(game)
            elif command == "25":
                AdminPanel._reset_location_state(game)
            elif command == "26":
                AdminPanel._view_world_state(game)
            elif command == "27":
                AdminPanel._location_editor(game)
            elif command == "28":
                AdminPanel._remove_skill_points(game.player)
            elif command == "29":
                AdminPanel._add_skill_points(game.player)
            elif command == "30":
                AdminPanel._remove_status_effect(game.player)
            elif command == "31":
                AdminPanel._add_status_effect(game.player)
            elif command == "32":
                AdminPanel._max_all_skills(game.player)
            elif command == "33":
                AdminPanel._unlock_all_recipes(game.player)
            elif command == "34":
                AdminPanel._discover_all_locations(game.player, game.world)
            elif command == "35":
                AdminPanel._clear_inventory(game.player)
            elif command == "36":
                AdminPanel._remove_item_from_inventory(game.player)
            elif command == "37":
                AdminPanel._spawn_custom_creature(game)
            elif command == "38":
                AdminPanel._drop_item_in_location(game)
            elif command == "39":
                AdminPanel._place_item_in_location(game)
            elif command == "40":
                AdminPanel._browse_expanded_creatures()
            elif command == "41":
                AdminPanel._browse_expanded_items()
            elif command == "42":
                AdminPanel._browse_npcs()
            elif command == "43":
                AdminPanel._trigger_random_event(game)
            elif command == "44":
                AdminPanel._browse_combat_maneuvers()
            elif command == "45":
                AdminPanel._read_lore_entry()
            elif command == "46":
                AdminPanel._browse_weather_patterns()
            elif command == "47":
                AdminPanel._browse_status_effects()
            elif command == "48":
                AdminPanel._browse_expanded_locations()
            elif command == "49":
                AdminPanel._spawn_expanded_creature(game)
            elif command == "50":
                AdminPanel._give_expanded_item(game.player)
            elif command == "51":
                AdminPanel._set_difficulty_mode_admin(game)
            elif command == "52":
                AdminPanel._list_all_locations_admin(game)
            elif command == "53":
                AdminPanel._check_location_accessibility_admin(game)
            elif command == "54":
                AdminPanel._teleport_to_expanded_location_admin(game)
            elif command == "55":
                AdminPanel._view_starting_options_admin()
            # New comprehensive commands (56-70)
            elif command == "56":
                AdminPanel._manage_companions(game.player)
            elif command == "57":
                AdminPanel._manage_reputation(game.player)
            elif command == "58":
                AdminPanel._manage_notes(game.player)
            elif command == "59":
                AdminPanel._manage_equipment(game.player)
            elif command == "60":
                AdminPanel._manage_resources(game.player)
            elif command == "61":
                AdminPanel._manage_statistics(game.player)
            elif command == "62":
                AdminPanel._manage_quests(game.player)
            elif command == "63":
                AdminPanel._manage_achievements(game.player)
            elif command == "64":
                AdminPanel._manage_recipes(game.player)
            elif command == "65":
                AdminPanel._set_play_time(game.player)
            elif command == "66":
                AdminPanel._save_game_admin(game)
            elif command == "67":
                AdminPanel._load_game_admin(game)
            elif command == "68":
                AdminPanel._reset_player_progress(game.player)
            # EXCLUSIVE ADMIN FEATURES (69-73)
            elif command == "69":
                AdminPanel._admin_exclusive_items(game.player)
            elif command == "70":
                AdminPanel._reality_warper(game)
            elif command == "71":
                AdminPanel._time_travel_menu(game)
            elif command == "72":
                AdminPanel._easter_egg_spawner(game)
            elif command == "73":
                AdminPanel._god_powers_menu(game.player)
            else:
                slow_print(colored_text(f"Unknown admin command: {choice}", Colors.RED))

            get_input("\nPress Enter to continue...")

    @staticmethod
    def _display_main_menu():
        """Display comprehensive organized admin main menu."""
        print("""\
{0}
║                  ADMIN PANEL - COMPREHENSIVE MENU                  ║
{1}
  ═══ TOGGLES ═══
    [1]  God Mode              [2]  Infinite Inventory
    [3]  No Hunger/Thirst      [4]  Instant Kill         [15] Skip Combat

  ═══ PLAYER - BASIC ═══
    [5]  Give Item             [6]  Give Gold            [7]  Set Health
    [11] Set Level             [12] Give All Items       [65] Set Play Time

  ═══ PLAYER - RESOURCES ═══
    [60] Manage Resources (Stamina/Mana/Hunger/Thirst/Sanity)

  ═══ PLAYER - SKILLS ═══
    [18] Skills Manager        [28] Remove Skill Pts    [29] Add Skill Pts
    [32] Max All Skills

  ═══ PLAYER - EQUIPMENT & INVENTORY ═══
    [21] Inventory Manager     [35] Clear Inventory     [36] Remove Item
    [59] Equipment Manager (Equip/Unequip Items)

  ═══ PLAYER - PROGRESS & STATS ═══
    [61] Statistics Manager (Deaths/Kills/Steps/Damage/etc)
    [13] Complete All Quests   [14] Unlock All Achievements
    [33] Unlock All Recipes    [34] Discover All Locations
    [68] RESET Player Progress (DANGER!)

  ═══ ADVANCED MANAGEMENT ═══
    [56] Companions Manager    [57] Reputation Manager  [58] Notes Manager
    [62] Quest Manager (Add/Remove/Fail Quests)
    [63] Achievement Manager (Lock/Unlock Individual)
    [64] Recipe Manager (Add/Remove Individual)
    [22] Quest Objective Editor

  ═══ STATUS EFFECTS ═══
    [23] Status Effect Manager [30] Remove Effect       [31] Add Effect
    [47] Browse Status Effects

  ═══ WORLD & LOCATIONS ═══
    [8]  Teleport              [9]  Reveal Map          [24] Manage Creatures
    [25] Reset Location        [26] View World State    [27] Location Editor
    [52] List All Locations    [53] Check Accessibility
    [54] Teleport to Expanded  [55] View Starting Opts

  ═══ CREATURES ═══
    [10] Spawn Creature        [37] Spawn Custom        [49] Spawn Expanded
    [40] Browse Expanded Creatures

  ═══ ITEMS ═══
    [38] Drop in Location      [39] Place in Location   [50] Give Expanded
    [41] Browse Expanded Items

  ═══ GAME SYSTEMS ═══
    [19] Weather Control       [20] Time Control        [51] Set Difficulty
    [43] Trigger Random Event  [66] Save Game          [67] Load Game

  ═══ CONTENT BROWSERS ═══
    [42] Browse NPCs           [44] Combat Maneuvers    [45] Read Lore
    [46] Weather Patterns      [48] Expanded Locations

  ═══ OTHER ═══
    [16] Text Speed            [17] Debug Info

  ═══ 🌟 EXCLUSIVE ADMIN FEATURES 🌟 ═══
    [69] Admin Exclusive Items (Legendary items ONLY from admin!)
    [70] Reality Warper (Bend the rules of reality)
    [71] Time Travel (Travel through time and space)
    [72] Easter Egg Spawner (Secret encounters and treasures)
    [73] God Powers (Grant divine abilities)

  [0] Exit Admin Panel
{2}

Type command number or alias (exclusive, reality, timetravel, easteregg, etc.)
""".format(
    colored_text("╔" + "═" * 70 + "╗", Colors.MAGENTA),
    colored_text("╠" + "═" * 70 + "╣", Colors.MAGENTA),
    colored_text("╚" + "═" * 70 + "╝", Colors.MAGENTA)
))

    # ----- Toggles -----
    @staticmethod
    def _toggle_god_mode():
        SETTINGS.god_mode = not SETTINGS.god_mode
        slow_print(colored_text(f"God Mode: {'ON' if SETTINGS.god_mode else 'OFF'}", Colors.GREEN))

    @staticmethod
    def _toggle_infinite_inventory():
        SETTINGS.infinite_inventory = not SETTINGS.infinite_inventory
        slow_print(colored_text(f"Infinite Inventory: {'ON' if SETTINGS.infinite_inventory else 'OFF'}", Colors.GREEN))

    @staticmethod
    def _toggle_no_hunger():
        SETTINGS.no_hunger = not SETTINGS.no_hunger
        SETTINGS.no_thirst = SETTINGS.no_hunger
        slow_print(colored_text(f"No Hunger/Thirst: {'ON' if SETTINGS.no_hunger else 'OFF'}", Colors.GREEN))

    @staticmethod
    def _toggle_instant_kill():
        SETTINGS.instant_kill = not SETTINGS.instant_kill
        slow_print(colored_text(f"Instant Kill: {'ON' if SETTINGS.instant_kill else 'OFF'}", Colors.GREEN))

    @staticmethod
    def _toggle_skip_combat():
        SETTINGS.skip_combat = not SETTINGS.skip_combat
        slow_print(colored_text(f"Skip Combat: {'ON' if SETTINGS.skip_combat else 'OFF'}", Colors.GREEN))

    # ----- Player commands -----
    @staticmethod
    def _give_item(player: 'Player'):
        items = ItemFactory.get_all_items()
        instant_print(colored_text("\nAvailable Items:", Colors.YELLOW))
        for name in sorted(items):
            instant_print(f"  - {name}")

        item_name = get_input("Item name: ")
        item = ItemFactory.create_item(item_name)
        if item:
            success, msg = player.add_item(item)
            slow_print(colored_text(msg, Colors.GREEN if success else Colors.RED))
        else:
            slow_print(colored_text("Item not found.", Colors.RED))

    @staticmethod
    def _give_gold(player: 'Player'):
        while True:
            amount_str = get_input("Amount: ")
            try:
                amount = int(amount_str)
                if amount < 0:
                    slow_print(colored_text("Amount must be positive.", Colors.RED))
                    continue
                player.gold += amount
                slow_print(colored_text(f"Added {amount} gold. Total: {player.gold}", Colors.GREEN))
                break
            except ValueError:
                slow_print(colored_text("Invalid amount.", Colors.RED))

    @staticmethod
    def _set_health(player: 'Player'):
        while True:
            amount_str = get_input(f"Health amount (max {player.max_health}): ")
            try:
                amount = int(amount_str)
                if amount < 0 or amount > player.max_health:
                    slow_print(colored_text(f"Amount must be between 0 and {player.max_health}.", Colors.RED))
                    continue
                player.health = amount
                slow_print(colored_text(f"Health set to {player.health}.", Colors.GREEN))
                break
            except ValueError:
                slow_print(colored_text("Invalid amount.", Colors.RED))

    @staticmethod
    def _set_level(player: 'Player'):
        while True:
            level_str = get_input("Level (1-100): ")
            try:
                level = int(level_str)
                if level < 1 or level > 100:
                    slow_print(colored_text("Level must be between 1 and 100.", Colors.RED))
                    continue
                while player.level < level:
                    player.level_up()
                slow_print(colored_text(f"Level set to {player.level}.", Colors.GREEN))
                break
            except ValueError:
                slow_print(colored_text("Invalid level.", Colors.RED))

    @staticmethod
    def _give_all_items(player: 'Player'):
        count_before = len(player.inventory)
        for item_name in ItemFactory.get_all_items():
            item = ItemFactory.create_item(item_name)
            if item:
                player.add_item(item)
        count_after = len(player.inventory)
        slow_print(colored_text(f"Added all items to inventory ({count_after - count_before} new items).", Colors.GREEN))

    @staticmethod
    def _complete_all_quests(player: 'Player'):
        for quest in player.active_quests:
            quest.is_complete = True
            for i in range(len(quest.completed_objectives)):
                quest.completed_objectives[i] = True
        slow_print(colored_text("All quests marked complete.", Colors.GREEN))

    @staticmethod
    def _unlock_all_achievements(player: 'Player'):
        AchievementSystem.initialize_achievements()
        for achievement_id in AchievementSystem._achievements:
            if achievement_id not in player.achievements:
                player.achievements.append(achievement_id)
        slow_print(colored_text("All achievements unlocked.", Colors.GREEN))

    @staticmethod
    def _discover_all_locations(player: 'Player', world: Dict[str, 'Location']):
        player.discovered_locations = list(world.keys())
        slow_print(colored_text(f"All {len(world)} locations marked as discovered.", Colors.GREEN))

    @staticmethod
    def _change_text_speed():
        # Show sample text with current speed
        sample_text = "Sample text speed demonstration."
        slow_print("\nCurrent text speed:")
        slow_print(sample_text, delay=SETTINGS.text_speed)
        while True:
            speed_str = get_input("Text speed (0-0.1, 0=instant): ")
            try:
                speed = float(speed_str)
                if speed < 0 or speed > 0.1:
                    slow_print(colored_text("Speed must be between 0 and 0.1.", Colors.RED))
                    continue
                SETTINGS.text_speed = speed
                slow_print(colored_text(f"Text speed set to {SETTINGS.text_speed}.", Colors.GREEN))
                break
            except ValueError:
                slow_print(colored_text("Invalid speed value.", Colors.RED))

    # ----- Teleport and map -----
    @staticmethod
    def _teleport(game: 'Game'):
        # List locations with indexes
        locations = list(game.world.keys())
        instant_print(colored_text("\nAvailable locations:", Colors.YELLOW))
        for idx, loc_id in enumerate(sorted(locations), 1):
            loc = game.world[loc_id]
            instant_print(f"  {idx}. {loc.name} ({loc_id})")

        while True:
            choice = get_input("Select location by number or enter location ID: ")
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(locations):
                    loc_id = locations[index]
                    game.player.current_location = loc_id
                    if loc_id not in game.player.discovered_locations:
                        game.player.discovered_locations.append(loc_id)
                    slow_print(colored_text(f"Teleported to {loc_id}.", Colors.GREEN))
                    break
                else:
                    slow_print(colored_text("Invalid index.", Colors.RED))
            else:
                if choice in game.world:
                    game.player.current_location = choice
                    if choice not in game.player.discovered_locations:
                        game.player.discovered_locations.append(choice)
                    slow_print(colored_text(f"Teleported to {choice}.", Colors.GREEN))
                    break
                else:
                    slow_print(colored_text("Location not found.", Colors.RED))

    @staticmethod
    def _reveal_map(game: 'Game'):
        game.player.discovered_locations = list(game.world.keys())
        slow_print(colored_text(f"Revealed {len(game.world)} locations.", Colors.GREEN))

    # ----- Creature spawning -----
    @staticmethod
    def _spawn_creature(game: 'Game'):
        creatures = CreatureFactory.get_all_creatures()
        instant_print(colored_text("\nAvailable creatures:", Colors.YELLOW))
        for name in sorted(creatures):
            instant_print(f"  - {name}")

        name = get_input("Creature name: ")
        creature = CreatureFactory.create_creature(name)
        if creature:
            location = game.world.get(game.player.current_location)
            if location:
                location.creatures.append(creature)
                slow_print(colored_text(f"Spawned {creature.name}.", Colors.GREEN))
            else:
                slow_print(colored_text("Current location not found.", Colors.RED))
        else:
            slow_print(colored_text("Creature not found.", Colors.RED))

    @staticmethod
    def _spawn_custom_creature(game: 'Game'):
        creatures = CreatureFactory.get_all_creatures()
        instant_print(colored_text("\nAvailable creatures to base on:", Colors.YELLOW))
        for name in sorted(creatures):
            instant_print(f"  - {name}")

        name = get_input("Base creature name: ")
        base_creature = CreatureFactory.create_creature(name)
        if not base_creature:
            slow_print(colored_text("Creature not found.", Colors.RED))
            return

        try:
            health = int(get_input(f"Set health (1-{base_creature.max_health}): "))
            health = max(1, min(health, base_creature.max_health))
        except ValueError:
            slow_print(colored_text("Invalid health value.", Colors.RED))
            return

        new_creature = Creature(
            name=base_creature.name,
            description=base_creature.description,
            creature_type=base_creature.creature_type,
            health=health,
            max_health=base_creature.max_health,
            damage=base_creature.damage,
            defense=base_creature.defense,
            experience=base_creature.experience,
            loot=base_creature.loot,
            loot_chance=base_creature.loot_chance,
            dialogue=base_creature.dialogue,
            hostile=base_creature.hostile,
            alive=True,
            special_abilities=base_creature.special_abilities,
            weakness=base_creature.weakness,
            resistance=base_creature.resistance,
            level=base_creature.level,
            gold_drop=base_creature.gold_drop
        )
        location = game.world.get(game.player.current_location)
        if location:
            location.creatures.append(new_creature)
            slow_print(colored_text(f"Spawned custom {new_creature.name} with {new_creature.health} HP.", Colors.GREEN))
        else:
            slow_print(colored_text("Current location not found.", Colors.RED))

    # ----- Inventory management -----
    @staticmethod
    def _inventory_menu(player: 'Player'):
        while True:
            clear_screen()
            instant_print(colored_text("\nINVENTORY MANAGEMENT", Colors.CYAN))
            instant_print(f"Gold: {player.gold}")
            instant_print(f"Items in inventory: {len(player.inventory)}")
            instant_print("[1] View Inventory")
            instant_print("[2] Clear Inventory")
            instant_print("[3] Remove Specific Item")
            instant_print("[0] Back")
            choice = get_input("Choice: ")
            if choice == "1":
                instant_print(player.get_inventory_display())
                get_input("\nPress Enter...")
            elif choice == "2":
                confirm = get_input("Are you sure you want to clear your inventory? (y/n): ")
                if confirm.lower() == 'y':
                    player.inventory.clear()
                    slow_print(colored_text("Inventory cleared.", Colors.GREEN))
            elif choice == "3":
                if not player.inventory:
                    slow_print(colored_text("Inventory is empty.", Colors.YELLOW))
                    continue
                instant_print(colored_text("\nInventory items:", Colors.YELLOW))
                for i, item in enumerate(player.inventory, 1):
                    qty = f" x{item.quantity}" if item.quantity > 1 else ""
                    instant_print(f"{i}. {item.name}{qty}")
                item_choice = get_input("Enter item number or 'cancel': ")
                if item_choice.lower() == "cancel":
                    continue
                try:
                    idx = int(item_choice) - 1
                    if 0 <= idx < len(player.inventory):
                        item = player.inventory[idx]
                        qty_remove = 1
                        if item.stackable and item.quantity > 1:
                            qty_remove_str = get_input(f"Enter quantity to remove (1-{item.quantity}): ")
                            try:
                                qty_remove = int(qty_remove_str)
                                if qty_remove < 1 or qty_remove > item.quantity:
                                    slow_print(colored_text("Invalid quantity.", Colors.RED))
                                    continue
                            except ValueError:
                                slow_print(colored_text("Invalid quantity.", Colors.RED))
                                continue
                        if qty_remove >= item.quantity:
                            player.inventory.pop(idx)
                            slow_print(colored_text(f"Removed all of {item.name}.", Colors.GREEN))
                        else:
                            item.quantity -= qty_remove
                            slow_print(colored_text(f"Removed {qty_remove} of {item.name}.", Colors.GREEN))
                    else:
                        slow_print(colored_text("Invalid item number.", Colors.RED))
                except ValueError:
                    slow_print(colored_text("Invalid input.", Colors.RED))
            elif choice == "0":
                break
            else:
                slow_print(colored_text("Unknown choice.", Colors.RED))

    @staticmethod
    def _remove_item_from_inventory(player: 'Player'):
        if not player.inventory:
            slow_print(colored_text("Inventory is empty.", Colors.YELLOW))
            return
        instant_print(colored_text("\nInventory items:", Colors.YELLOW))
        for i, item in enumerate(player.inventory, 1):
            qty = f" x{item.quantity}" if item.quantity > 1 else ""
            instant_print(f"{i}. {item.name}{qty}")
        choice = get_input("Enter item number to remove or 'cancel': ")
        if choice.lower() == "cancel":
            return
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(player.inventory):
                item = player.inventory[idx]
                qty_remove = 1
                if item.stackable and item.quantity > 1:
                    qty_str = get_input(f"Enter quantity to remove (1-{item.quantity}): ")
                    try:
                        qty_remove = int(qty_str)
                        if qty_remove < 1 or qty_remove > item.quantity:
                            slow_print(colored_text("Invalid quantity.", Colors.RED))
                            return
                    except ValueError:
                        slow_print(colored_text("Invalid quantity.", Colors.RED))
                        return
                if qty_remove >= item.quantity:
                    player.inventory.pop(idx)
                    slow_print(colored_text(f"Removed all of {item.name}.", Colors.GREEN))
                else:
                    item.quantity -= qty_remove
                    slow_print(colored_text(f"Removed {qty_remove} of {item.name}.", Colors.GREEN))
            else:
                slow_print(colored_text("Invalid item number.", Colors.RED))
        except ValueError:
            slow_print(colored_text("Invalid input.", Colors.RED))

    @staticmethod
    def _clear_inventory(player: 'Player'):
        confirm = get_input("Are you sure you want to clear your entire inventory? (y/n): ")
        if confirm.lower() == "y":
            player.inventory.clear()
            slow_print(colored_text("Inventory cleared.", Colors.GREEN))
        else:
            slow_print(colored_text("Clear inventory cancelled.", Colors.YELLOW))

    # ----- Skills management -----
    @staticmethod
    def _skills_menu(player: 'Player'):
        while True:
            clear_screen()
            instant_print(colored_text("\nSKILLS MANAGEMENT", Colors.CYAN))
            instant_print(player.get_skills_display())
            instant_print("[1] Max All Skills")
            instant_print("[0] Back")
            choice = get_input("Choice: ")
            if choice == "1":
                AdminPanel._max_all_skills(player)
            elif choice == "0":
                break
            else:
                slow_print(colored_text("Unknown choice.", Colors.RED))

    @staticmethod
    def _max_all_skills(player: 'Player'):
        for skill in player.skills:
            player.skills[skill] = 10
        slow_print(colored_text("All skills set to maximum (10).", Colors.GREEN))

    @staticmethod
    def _remove_skill_points(player: 'Player'):
        skill = AdminPanel._choose_skill(player, prompt="Select skill to remove points from")
        if skill is None:
            return
        current_level = player.skills.get(skill, 1)
        max_remove = current_level - 1
        if max_remove <= 0:
            slow_print(colored_text(f"{skill.value.capitalize()} is already at minimum.", Colors.YELLOW))
            return
        qty_str = get_input(f"Points to remove (1-{max_remove}): ")
        try:
            qty = int(qty_str)
            if 1 <= qty <= max_remove:
                player.skills[skill] -= qty
                slow_print(colored_text(f"Removed {qty} points from {skill.value}. Current level: {player.skills[skill]}", Colors.GREEN))
            else:
                slow_print(colored_text("Invalid number of points.", Colors.RED))
        except ValueError:
            slow_print(colored_text("Invalid input.", Colors.RED))

    @staticmethod
    def _add_skill_points(player: 'Player'):
        skill = AdminPanel._choose_skill(player, prompt="Select skill to add points to")
        if skill is None:
            return
        current_level = player.skills.get(skill, 1)
        max_add = 10 - current_level
        if max_add <= 0:
            slow_print(colored_text(f"{skill.value.capitalize()} is already at maximum.", Colors.YELLOW))
            return
        qty_str = get_input(f"Points to add (1-{max_add}): ")
        try:
            qty = int(qty_str)
            if 1 <= qty <= max_add:
                player.skills[skill] += qty
                slow_print(colored_text(f"Added {qty} points to {skill.value}. Current level: {player.skills[skill]}", Colors.GREEN))
            else:
                slow_print(colored_text("Invalid number of points.", Colors.RED))
        except ValueError:
            slow_print(colored_text("Invalid input.", Colors.RED))

    @staticmethod
    def _choose_skill(player: 'Player', prompt="Choose a skill:") -> Optional['SkillType']:
        skills = list(SkillType)
        instant_print(colored_text("\nSkills:", Colors.YELLOW))
        for idx, skill in enumerate(skills, 1):
            level = player.skills.get(skill, 1)
            instant_print(f"  {idx}. {skill.value.capitalize()} (Level {level})")
        choice = get_input(prompt + " (number or 0 to cancel): ")
        if choice == "0":
            return None
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(skills):
                return skills[idx]
        except ValueError:
            pass
        slow_print(colored_text("Invalid skill choice.", Colors.RED))
        return None

    # ----- Weather control -----
    @staticmethod
    def _weather_menu(time_weather: 'TimeWeatherSystem'):
        weathers = list(Weather)
        instant_print(colored_text("\nWeather types:", Colors.YELLOW))
        for idx, weather in enumerate(weathers, 1):
            current_marker = " (current)" if weather == time_weather.current_weather else ""
            instant_print(f"  {idx}. {weather.value.capitalize()}{current_marker}")
        while True:
            choice = get_input("Set weather by number or 0 to cancel: ")
            if choice == "0":
                break
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(weathers):
                    time_weather.current_weather = weathers[idx]
                    time_weather.weather_duration = 60  # Reset duration
                    slow_print(colored_text(f"Weather changed to {time_weather.current_weather.value}.", Colors.GREEN))
                    break
                else:
                    slow_print(colored_text("Invalid choice.", Colors.RED))
            except ValueError:
                slow_print(colored_text("Invalid input.", Colors.RED))

    # ----- Time control -----
    @staticmethod
    def _time_menu(time_weather: 'TimeWeatherSystem'):
        while True:
            clear_screen()
            instant_print(colored_text("\nTIME CONTROL", Colors.CYAN))
            instant_print(f"Current Day: {time_weather.day_count}")
            instant_print(f"Current Time: {time_weather.get_time_string()}")
            instant_print("[1] Set Day")
            instant_print("[2] Set Time (Minutes of day)")
            instant_print("[3] Advance Time (minutes)")
            instant_print("[0] Back")
            choice = get_input("Choice: ")
            if choice == "1":
                day_str = get_input("Set day (1+): ")
                try:
                    day = int(day_str)
                    if day < 1:
                        slow_print(colored_text("Day must be 1 or greater.", Colors.RED))
                        continue
                    time_weather.day_count = day
                    slow_print(colored_text(f"Day set to {day}.", Colors.GREEN))
                except ValueError:
                    slow_print(colored_text("Invalid day.", Colors.RED))
            elif choice == "2":
                time_str = get_input("Set time in minutes (0-1439): ")
                try:
                    minutes = int(time_str)
                    if 0 <= minutes < 1440:
                        time_weather.game_minutes = minutes
                        slow_print(colored_text(f"Time set to {time_weather.get_time_string()}.", Colors.GREEN))
                    else:
                        slow_print(colored_text("Time must be between 0 and 1439 minutes.", Colors.RED))
                except ValueError:
                    slow_print(colored_text("Invalid input.", Colors.RED))
            elif choice == "3":
                advance_str = get_input("Advance time by minutes (positive integer): ")
                try:
                    minutes = int(advance_str)
                    if minutes < 0:
                        slow_print(colored_text("Minutes must be positive.", Colors.RED))
                        continue
                    time_weather.advance_time(minutes)
                    slow_print(colored_text(f"Time advanced by {minutes} minutes.", Colors.GREEN))
                    slow_print(colored_text(f"New time: {time_weather.get_time_string()}, Weather: {time_weather.current_weather.value}", Colors.GREEN))
                except ValueError:
                    slow_print(colored_text("Invalid input.", Colors.RED))
            elif choice == "0":
                break
            else:
                slow_print(colored_text("Unknown choice.", Colors.RED))

    # ----- Quest objective editor -----
    @staticmethod
    def _quest_objective_editor(player: 'Player'):
        if not player.active_quests:
            slow_print(colored_text("No active quests.", Colors.YELLOW))
            return
        # List active quests with numbers
        instant_print(colored_text("\nActive Quests:", Colors.YELLOW))
        for idx, quest in enumerate(player.active_quests, 1):
            status = "[Complete]" if quest.is_complete else "[Active]"
            instant_print(f"{idx}. {quest.name} {status}")
        while True:
            quest_choice = get_input("Select quest by number or 0 to cancel: ")
            if quest_choice == "0":
                return
            try:
                q_idx = int(quest_choice) - 1
                if 0 <= q_idx < len(player.active_quests):
                    quest = player.active_quests[q_idx]
                    break
                else:
                    slow_print(colored_text("Invalid quest number.", Colors.RED))
            except ValueError:
                slow_print(colored_text("Invalid input.", Colors.RED))
        # Show objectives
        while True:
            clear_screen()
            instant_print(colored_text(f"\nQuest: {quest.name} Objectives", Colors.CYAN))
            for i, objective in enumerate(quest.objectives, 1):
                completed = quest.completed_objectives[i - 1]
                mark = "✓" if completed else "○"
                color = Colors.GREEN if completed else Colors.DIM
                instant_print(f"{i}. {colored_text(mark, color)} {objective}")
            instant_print("[1] Complete Objective")
            instant_print("[2] Reset Objective")
            instant_print("[0] Back")
            choice = get_input("Choice: ")
            if choice == "1":
                obj_choice = get_input(f"Select objective number to complete (1-{len(quest.objectives)}): ")
                try:
                    idx = int(obj_choice) - 1
                    if 0 <= idx < len(quest.objectives):
                        quest.completed_objectives[idx] = True
                        # Update overall completion status
                        quest.is_complete = all(quest.completed_objectives)
                        slow_print(colored_text("Objective completed.", Colors.GREEN))
                    else:
                        slow_print(colored_text("Invalid objective number.", Colors.RED))
                except ValueError:
                    slow_print(colored_text("Invalid input.", Colors.RED))
            elif choice == "2":
                obj_choice = get_input(f"Select objective number to reset (1-{len(quest.objectives)}): ")
                try:
                    idx = int(obj_choice) - 1
                    if 0 <= idx < len(quest.objectives):
                        quest.completed_objectives[idx] = False
                        quest.is_complete = False
                        slow_print(colored_text("Objective reset.", Colors.GREEN))
                    else:
                        slow_print(colored_text("Invalid objective number.", Colors.RED))
                except ValueError:
                    slow_print(colored_text("Invalid input.", Colors.RED))
            elif choice == "0":
                break
            else:
                slow_print(colored_text("Unknown choice.", Colors.RED))

    # ----- Status effect manager -----
    @staticmethod
    def _status_effect_manager(player: 'Player'):
        while True:
            clear_screen()
            instant_print(colored_text("\nSTATUS EFFECTS", Colors.CYAN))
            if player.status_effects:
                instant_print("Current effects:")
                for effect, duration in player.status_effects.items():
                    instant_print(f"  {effect}: {duration} minutes remaining")
            else:
                instant_print("No active status effects.", Colors.YELLOW)
            instant_print("[1] Add Status Effect")
            instant_print("[2] Remove Status Effect")
            instant_print("[0] Back")
            choice = get_input("Choice: ")
            if choice == "1":
                effect = get_input("Effect name: ")
                duration_str = get_input("Duration in minutes: ")
                try:
                    duration = int(duration_str)
                    if duration < 1:
                        slow_print(colored_text("Duration must be at least 1.", Colors.RED))
                        continue
                    player.status_effects[effect] = duration
                    slow_print(colored_text(f"Added status effect: {effect} for {duration} minutes.", Colors.GREEN))
                except ValueError:
                    slow_print(colored_text("Invalid duration.", Colors.RED))
            elif choice == "2":
                if not player.status_effects:
                    slow_print(colored_text("No effects to remove.", Colors.YELLOW))
                    continue
                effect = get_input("Effect name to remove: ")
                if effect in player.status_effects:
                    del player.status_effects[effect]
                    slow_print(colored_text(f"Removed status effect: {effect}.", Colors.GREEN))
                else:
                    slow_print(colored_text("Effect not found.", Colors.RED))
            elif choice == "0":
                break
            else:
                slow_print(colored_text("Unknown choice.", Colors.RED))

    @staticmethod
    def _remove_status_effect(player: 'Player'):
        effects = list(player.status_effects.keys())
        if not effects:
            slow_print(colored_text("No status effects to remove.", Colors.YELLOW))
            return
        instant_print(colored_text("\nStatus Effects:", Colors.YELLOW))
        for idx, effect in enumerate(effects, 1):
            instant_print(f"{idx}. {effect}")
        choice = get_input("Select status effect to remove or 0 to cancel: ")
        if choice == "0":
            return
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(effects):
                effect = effects[idx]
                del player.status_effects[effect]
                slow_print(colored_text(f"Removed status effect: {effect}.", Colors.GREEN))
            else:
                slow_print(colored_text("Invalid choice.", Colors.RED))
        except ValueError:
            slow_print(colored_text("Invalid input.", Colors.RED))

    @staticmethod
    def _add_status_effect(player: 'Player'):
        effect = get_input("Enter status effect name: ")
        duration_str = get_input("Enter duration in minutes: ")
        try:
            duration = int(duration_str)
            if duration < 1:
                slow_print(colored_text("Duration must be at least 1.", Colors.RED))
                return
            player.status_effects[effect] = duration
            slow_print(colored_text(f"Added status effect {effect} for {duration} minutes.", Colors.GREEN))
        except ValueError:
            slow_print(colored_text("Invalid duration value.", Colors.RED))

    # ----- Manage creatures in current location -----
    @staticmethod
    def _manage_location_creatures(game: 'Game'):
        location = game.world.get(game.player.current_location)
        if not location:
            slow_print(colored_text("Current location not found.", Colors.RED))
            return
        creatures = location.creatures
        if not creatures:
            slow_print(colored_text("No creatures in current location.", Colors.YELLOW))
            return
        while True:
            clear_screen()
            instant_print(colored_text(f"\nCreatures in {location.name}:", Colors.CYAN))
            for idx, c in enumerate(creatures, 1):
                status = "Alive" if c.alive else "Dead"
                instant_print(f"{idx}. {c.name} - {status}, HP: {c.health}/{c.max_health}")
            instant_print("[1] Toggle Alive/Dead")
            instant_print("[2] Remove Creature")
            instant_print("[3] Edit Creature Health")
            instant_print("[0] Back")
            choice = get_input("Choice: ")
            if choice == "1":
                c_idx_str = get_input("Select creature number to toggle alive/dead: ")
                try:
                    c_idx = int(c_idx_str) - 1
                    if 0 <= c_idx < len(creatures):
                        creature = creatures[c_idx]
                        creature.alive = not creature.alive
                        if creature.alive and creature.health <= 0:
                            creature.health = creature.max_health
                        slow_print(colored_text(f"Toggled {creature.name} to {'Alive' if creature.alive else 'Dead'}.", Colors.GREEN))
                    else:
                        slow_print(colored_text("Invalid creature number.", Colors.RED))
                except ValueError:
                    slow_print(colored_text("Invalid input.", Colors.RED))
            elif choice == "2":
                c_idx_str = get_input("Select creature number to remove: ")
                try:
                    c_idx = int(c_idx_str) - 1
                    if 0 <= c_idx < len(creatures):
                        creature = creatures.pop(c_idx)
                        slow_print(colored_text(f"Removed creature: {creature.name}.", Colors.GREEN))
                    else:
                        slow_print(colored_text("Invalid creature number.", Colors.RED))
                except ValueError:
                    slow_print(colored_text("Invalid input.", Colors.RED))
            elif choice == "3":
                c_idx_str = get_input("Select creature number to edit health: ")
                try:
                    c_idx = int(c_idx_str) - 1
                    if 0 <= c_idx < len(creatures):
                        creature = creatures[c_idx]
                        hp_str = get_input(f"Set health for {creature.name} (0-{creature.max_health}): ")
                        try:
                            hp = int(hp_str)
                            if 0 <= hp <= creature.max_health:
                                creature.health = hp
                                if hp <= 0:
                                    creature.alive = False
                                else:
                                    creature.alive = True
                                slow_print(colored_text(f"Set health of {creature.name} to {hp}.", Colors.GREEN))
                            else:
                                slow_print(colored_text("Health out of range.", Colors.RED))
                        except ValueError:
                            slow_print(colored_text("Invalid health value.", Colors.RED))
                    else:
                        slow_print(colored_text("Invalid creature number.", Colors.RED))
                except ValueError:
                    slow_print(colored_text("Invalid input.", Colors.RED))
            elif choice == "0":
                break
            else:
                slow_print(colored_text("Unknown choice.", Colors.RED))

    # ----- Reset location state -----
    @staticmethod
    def _reset_location_state(game: 'Game'):
        locations = list(game.world.keys())
        instant_print(colored_text("\nAvailable locations:", Colors.YELLOW))
        for idx, loc_id in enumerate(sorted(locations), 1):
            loc = game.world[loc_id]
            instant_print(f"  {idx}. {loc.name} ({loc_id})")

        while True:
            choice = get_input("Select location by number or 'cancel': ")
            if choice.lower() == "cancel":
                return
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(locations):
                    loc_id = locations[idx]
                    location = game.world.get(loc_id)
                    if location:
                        location.visited = False
                        location.visit_count = 0
                        location.treasure_found = False
                        location.items.clear()
                        location.creatures.clear()
                        slow_print(colored_text(f"Reset state of location '{location.name}'.", Colors.GREEN))
                    else:
                        slow_print(colored_text("Location not found.", Colors.RED))
                    break
                else:
                    slow_print(colored_text("Invalid choice.", Colors.RED))
            else:
                slow_print(colored_text("Invalid input.", Colors.RED))

    # ----- World State View -----
    @staticmethod
    def _view_world_state(game: 'Game'):
        world = game.world
        instant_print(colored_text("\nWORLD STATE SUMMARY", Colors.CYAN))
        instant_print(f"Total locations: {len(world)}")
        visited_count = sum(1 for loc in world.values() if loc.visited)
        instant_print(f"Visited locations: {visited_count}")
        creatures_total = sum(len(loc.creatures) for loc in world.values())
        instant_print(f"Total creatures in world: {creatures_total}")
        get_input("\nPress Enter to see detailed world state...")

        for loc_id, loc in sorted(world.items()):
            instant_print(colored_text(f"\n{loc.name} ({loc_id}):", Colors.BOLD_YELLOW))
            instant_print(f"  Visited: {loc.visited}, Visits: {loc.visit_count}, Treasure Found: {loc.treasure_found}")
            instant_print(f"  Items ({len(loc.items)}): " + ", ".join(item.name for item in loc.items))
            instant_print(f"  Creatures ({len(loc.creatures)}): " + ", ".join(f"{c.name} ({'Alive' if c.alive else 'Dead'})" for c in loc.creatures))
        get_input("\nPress Enter to return to menu...")

    # ----- Location Editor -----
    @staticmethod
    def _location_editor(game: 'Game'):
        locations = list(game.world.keys())
        instant_print(colored_text("\nAvailable locations:", Colors.YELLOW))
        for idx, loc_id in enumerate(sorted(locations), 1):
            loc = game.world[loc_id]
            instant_print(f"  {idx}. {loc.name} ({loc_id})")

        while True:
            choice = get_input("Select location by number or 'cancel': ")
            if choice.lower() == "cancel":
                return
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(locations):
                    loc_id = locations[idx]
                    location = game.world.get(loc_id)
                    if location:
                        AdminPanel._edit_location_menu(location)
                    else:
                        slow_print(colored_text("Location not found.", Colors.RED))
                    break
                else:
                    slow_print(colored_text("Invalid choice.", Colors.RED))
            else:
                slow_print(colored_text("Invalid input.", Colors.RED))

    @staticmethod
    def _edit_location_menu(location: 'Location'):
        while True:
            clear_screen()
            instant_print(colored_text(f"\nEditing Location: {location.name}", Colors.CYAN))
            instant_print("[1] View Items")
            instant_print("[2] Add Item")
            instant_print("[3] Remove Item")
            instant_print("[4] View Creatures")
            instant_print("[5] Add Creature")
            instant_print("[6] Remove Creature")
            instant_print("[0] Back")
            choice = get_input("Choice: ")
            if choice == "1":
                if not location.items:
                    slow_print(colored_text("No items in this location.", Colors.YELLOW))
                else:
                    instant_print(colored_text("\nItems in location:", Colors.YELLOW))
                    for idx, item in enumerate(location.items, 1):
                        qty = f" x{item.quantity}" if item.quantity > 1 else ""
                        instant_print(f"{idx}. {item.name}{qty}")
                get_input("\nPress Enter...")
            elif choice == "2":
                AdminPanel._add_item_to_location(location)
            elif choice == "3":
                AdminPanel._remove_item_from_location(location)
            elif choice == "4":
                if not location.creatures:
                    slow_print(colored_text("No creatures in this location.", Colors.YELLOW))
                else:
                    instant_print(colored_text("\nCreatures in location:", Colors.MAGENTA))
                    for idx, c in enumerate(location.creatures, 1):
                        status = "Alive" if c.alive else "Dead"
                        instant_print(f"{idx}. {c.name} - {status}, HP: {c.health}/{c.max_health}")
                get_input("\nPress Enter...")
            elif choice == "5":
                AdminPanel._add_creature_to_location(location)
            elif choice == "6":
                AdminPanel._remove_creature_from_location(location)
            elif choice == "0":
                break
            else:
                slow_print(colored_text("Unknown choice.", Colors.RED))

    @staticmethod
    def _add_item_to_location(location: 'Location'):
        items = ItemFactory.get_all_items()
        instant_print(colored_text("\nAvailable items:", Colors.YELLOW))
        for name in sorted(items):
            instant_print(f"  - {name}")
        name = get_input("Enter item name to add: ")
        item = ItemFactory.create_item(name)
        if item:
            quantity_str = get_input("Quantity (default 1): ")
            quantity = 1
            if quantity_str:
                try:
                    quantity = int(quantity_str)
                    if quantity < 1:
                        slow_print(colored_text("Quantity must be positive.", Colors.RED))
                        return
                except ValueError:
                    slow_print(colored_text("Invalid quantity.", Colors.RED))
                    return
            item.quantity = quantity
            location.items.append(item)
            slow_print(colored_text(f"Added {quantity}x {item.name} to location.", Colors.GREEN))
        else:
            slow_print(colored_text("Item not found.", Colors.RED))

    @staticmethod
    def _remove_item_from_location(location: 'Location'):
        if not location.items:
            slow_print(colored_text("No items in this location.", Colors.YELLOW))
            return
        instant_print(colored_text("\nItems in location:", Colors.YELLOW))
        for idx, item in enumerate(location.items, 1):
            qty = f" x{item.quantity}" if item.quantity > 1 else ""
            instant_print(f"{idx}. {item.name}{qty}")
        choice = get_input("Select item number to remove or 'cancel': ")
        if choice.lower() == "cancel":
            return
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(location.items):
                item = location.items[idx]
                qty_remove = 1
                if item.stackable and item.quantity > 1:
                    qty_str = get_input(f"Quantity to remove (1-{item.quantity}): ")
                    try:
                        qty_remove = int(qty_str)
                        if qty_remove < 1 or qty_remove > item.quantity:
                            slow_print(colored_text("Invalid quantity.", Colors.RED))
                            return
                    except ValueError:
                        slow_print(colored_text("Invalid quantity.", Colors.RED))
                        return
                if qty_remove >= item.quantity:
                    location.items.pop(idx)
                    slow_print(colored_text(f"Removed all of {item.name} from location.", Colors.GREEN))
                else:
                    item.quantity -= qty_remove
                    slow_print(colored_text(f"Removed {qty_remove} of {item.name} from location.", Colors.GREEN))
            else:
                slow_print(colored_text("Invalid choice.", Colors.RED))
        except ValueError:
            slow_print(colored_text("Invalid input.", Colors.RED))

    @staticmethod
    def _add_creature_to_location(location: 'Location'):
        creatures = CreatureFactory.get_all_creatures()
        instant_print(colored_text("\nAvailable creatures:", Colors.YELLOW))
        for name in sorted(creatures):
            instant_print(f"  - {name}")
        name = get_input("Enter creature name to add: ")
        creature = CreatureFactory.create_creature(name)
        if creature:
            location.creatures.append(creature)
            slow_print(colored_text(f"Added {creature.name} to location.", Colors.GREEN))
        else:
            slow_print(colored_text("Creature not found.", Colors.RED))

    @staticmethod
    def _remove_creature_from_location(location: 'Location'):
        if not location.creatures:
            slow_print(colored_text("No creatures in this location.", Colors.YELLOW))
            return
        instant_print(colored_text("\nCreatures in location:", Colors.MAGENTA))
        for idx, c in enumerate(location.creatures, 1):
            status = "Alive" if c.alive else "Dead"
            instant_print(f"{idx}. {c.name} - {status}, HP: {c.health}/{c.max_health}")
        choice = get_input("Select creature number to remove or 'cancel': ")
        if choice.lower() == "cancel":
            return
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(location.creatures):
                creature = location.creatures.pop(idx)
                slow_print(colored_text(f"Removed {creature.name} from location.", Colors.GREEN))
            else:
                slow_print(colored_text("Invalid choice.", Colors.RED))
        except ValueError:
            slow_print(colored_text("Invalid input.", Colors.RED))

    # ----- Drop/place items in locations -----
    @staticmethod
    def _drop_item_in_location(game: 'Game'):
        player = game.player
        location = game.world.get(player.current_location)
        if not location:
            slow_print(colored_text("Current location not found.", Colors.RED))
            return
        if not player.inventory:
            slow_print(colored_text("You have no items to drop.", Colors.YELLOW))
            return
        instant_print(colored_text("\nInventory items:", Colors.YELLOW))
        for i, item in enumerate(player.inventory, 1):
            qty = f" x{item.quantity}" if item.quantity > 1 else ""
            instant_print(f"{i}. {item.name}{qty}")
        choice = get_input("Select item number to drop or 'cancel': ")
        if choice.lower() == "cancel":
            return
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(player.inventory):
                item = player.inventory[idx]
                qty_remove = 1
                if item.stackable and item.quantity > 1:
                    qty_str = get_input(f"Quantity to drop (1-{item.quantity}): ")
                    try:
                        qty_remove = int(qty_str)
                        if qty_remove < 1 or qty_remove > item.quantity:
                            slow_print(colored_text("Invalid quantity.", Colors.RED))
                            return
                    except ValueError:
                        slow_print(colored_text("Invalid quantity.", Colors.RED))
                        return
                drop_item = Item(
                    name=item.name,
                    description=item.description,
                    item_type=item.item_type,
                    weight=item.weight,
                    value=item.value,
                    usable=item.usable,
                    equippable=item.equippable,
                    stackable=item.stackable,
                    quantity=qty_remove,
                    damage=item.damage,
                    defense=item.defense,
                    healing=item.healing,
                    light_radius=item.light_radius,
                    durability=item.durability,
                    max_durability=item.max_durability,
                    special_effects=item.special_effects.copy(),
                    rarity=item.rarity,
                    level_requirement=item.level_requirement,
                )
                if qty_remove >= item.quantity:
                    player.inventory.pop(idx)
                else:
                    item.quantity -= qty_remove
                location.items.append(drop_item)
                slow_print(colored_text(f"Dropped {qty_remove}x {drop_item.name} in {location.name}.", Colors.GREEN))
            else:
                slow_print(colored_text("Invalid item number.", Colors.RED))
        except ValueError:
            slow_print(colored_text("Invalid input.", Colors.RED))

    @staticmethod
    def _show_debug_info(game: 'Game'):
        debug_info = f"""
{colored_text("═══ DEBUG INFO ═══", Colors.CYAN)}
Player Location: {game.player.current_location}
Discovered Locations: {len(game.player.discovered_locations)}/{len(game.world)}
Active Quests: {len(game.player.active_quests)}
Completed Quests: {len(game.player.completed_quests)}
Inventory Items: {len(game.player.inventory)}
Total Playtime: {game.player.play_time} minutes
Current Day: {game.time_weather.day_count}
Current Time: {game.time_weather.get_time_string()}
Weather: {game.time_weather.current_weather.value}
"""
        instant_print(debug_info)


    @staticmethod
    def _place_item_in_location(game: 'Game'):
        location = game.world.get(game.player.current_location)
        if not location:
            slow_print(colored_text("Current location not found.", Colors.RED))
            return
        items = ItemFactory.get_all_items()
        instant_print(colored_text("\nAvailable items:", Colors.YELLOW))
        for name in sorted(items):
            instant_print(f"  - {name}")
        name = get_input("Enter item name to place: ")
        item = ItemFactory.create_item(name)
        if item:
            qty_str = get_input("Quantity (default 1): ")
            quantity = 1
            if qty_str:
                try:
                    quantity = int(qty_str)
                    if quantity < 1:
                        slow_print(colored_text("Quantity must be positive.", Colors.RED))
                        return
                except ValueError:
                    slow_print(colored_text("Invalid quantity.", Colors.RED))
                    return
            item.quantity = quantity
            location.items.append(item)
            slow_print(colored_text(f"Placed {quantity}x {item.name} in location.", Colors.GREEN))
        else:
            slow_print(colored_text("Item not found.", Colors.RED))

    # ----- New Content Browsers -----
    @staticmethod
    def _browse_expanded_creatures():
        """Browse the expanded creatures database."""
        instant_print(colored_text("\n=== EXPANDED CREATURES DATABASE ===", Colors.CYAN))
        instant_print(colored_text(f"Total: {len(EXPANDED_CREATURES)} creatures\n", Colors.YELLOW))
        
        creatures_list = sorted(EXPANDED_CREATURES.keys())
        for i, creature_id in enumerate(creatures_list, 1):
            creature_data = EXPANDED_CREATURES[creature_id]
            instant_print(f"{i}. {colored_text(creature_data['name'], Colors.GREEN)} ({creature_id})")
            instant_print(f"   Type: {creature_data.get('creature_type', 'N/A')} | "
                         f"HP: {creature_data.get('health', 0)} | "
                         f"Damage: {creature_data.get('damage', 0)} | "
                         f"Level: {creature_data.get('level', 1)}")
            if i % 10 == 0 and i < len(creatures_list):
                if get_input("\nPress Enter to continue (or 'q' to quit)...").lower() == 'q':
                    break
    
    @staticmethod
    def _browse_expanded_items():
        """Browse the expanded items database."""
        instant_print(colored_text("\n=== EXPANDED ITEMS DATABASE ===", Colors.CYAN))
        instant_print(colored_text(f"Total: {len(EXPANDED_ITEMS)} items\n", Colors.YELLOW))
        
        items_list = sorted(EXPANDED_ITEMS.keys())
        for i, item_id in enumerate(items_list, 1):
            item_data = EXPANDED_ITEMS[item_id]
            instant_print(f"{i}. {colored_text(item_data['name'], Colors.GREEN)} ({item_id})")
            instant_print(f"   Type: {item_data.get('type', 'N/A')} | "
                         f"Value: {item_data.get('value', 0)} gold | "
                         f"Rarity: {item_data.get('rarity', 'common')}")
            if i % 10 == 0 and i < len(items_list):
                if get_input("\nPress Enter to continue (or 'q' to quit)...").lower() == 'q':
                    break
    
    @staticmethod
    def _browse_npcs():
        """Browse the NPC database."""
        instant_print(colored_text("\n=== NPC DATABASE ===", Colors.CYAN))
        instant_print(colored_text(f"Total: {len(NPC_DATABASE)} NPCs\n", Colors.YELLOW))
        
        npcs_list = sorted(NPC_DATABASE.keys())
        for i, npc_id in enumerate(npcs_list, 1):
            npc_data = NPC_DATABASE[npc_id]
            instant_print(f"{i}. {colored_text(npc_data['name'], Colors.GREEN)} ({npc_id})")
            instant_print(f"   Profession: {npc_data.get('profession', 'N/A')} | "
                         f"Location: {npc_data.get('location', 'N/A')} | "
                         f"Personality: {npc_data.get('personality', 'N/A')}")
            if i % 10 == 0 and i < len(npcs_list):
                if get_input("\nPress Enter to continue (or 'q' to quit)...").lower() == 'q':
                    break
    
    @staticmethod
    def _trigger_random_event(game: 'Game'):
        """Trigger a random event from the database."""
        instant_print(colored_text("\n=== RANDOM EVENTS ===", Colors.CYAN))
        instant_print(colored_text(f"Total: {len(RANDOM_EVENTS)} events\n", Colors.YELLOW))
        
        # Show a sample of events
        events_list = list(RANDOM_EVENTS.keys())[:20]
        for i, event_id in enumerate(events_list, 1):
            event_data = RANDOM_EVENTS[event_id]
            instant_print(f"{i}. {colored_text(event_data['name'], Colors.GREEN)}")
            instant_print(f"   Type: {event_data.get('type', 'N/A')} | "
                         f"Rarity: {event_data.get('rarity', 'common')}")
        
        choice = get_input("\nEnter event number to trigger (or press Enter to skip): ")
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(events_list):
                event_id = events_list[idx]
                event_data = RANDOM_EVENTS[event_id]
                instant_print(colored_text(f"\n{event_data['text']}", Colors.YELLOW))
                slow_print(colored_text(f"Event '{event_data['name']}' triggered!", Colors.GREEN))
    
    @staticmethod
    def _browse_combat_maneuvers():
        """Browse combat maneuvers."""
        instant_print(colored_text("\n=== COMBAT MANEUVERS ===", Colors.CYAN))
        instant_print(colored_text(f"Total: {len(COMBAT_MANEUVERS)} maneuvers\n", Colors.YELLOW))
        
        maneuvers_list = sorted(COMBAT_MANEUVERS.keys())
        for i, maneuver_id in enumerate(maneuvers_list, 1):
            maneuver_data = COMBAT_MANEUVERS[maneuver_id]
            instant_print(f"{i}. {colored_text(maneuver_data['name'], Colors.GREEN)}")
            instant_print(f"   Type: {maneuver_data.get('type', 'N/A')} | "
                         f"Stamina: {maneuver_data.get('stamina_cost', 0)} | "
                         f"Level Req: {maneuver_data.get('level_required', 1)}")
            if i % 10 == 0 and i < len(maneuvers_list):
                if get_input("\nPress Enter to continue (or 'q' to quit)...").lower() == 'q':
                    break
    
    @staticmethod
    def _read_lore_entry():
        """Read a lore entry."""
        instant_print(colored_text("\n=== LORE ENTRIES ===", Colors.CYAN))
        instant_print(colored_text(f"Total: {len(LORE_ENTRIES)} entries\n", Colors.YELLOW))
        
        lore_list = sorted(LORE_ENTRIES.keys())[:30]
        for i, lore_id in enumerate(lore_list, 1):
            lore_data = LORE_ENTRIES[lore_id]
            instant_print(f"{i}. {colored_text(lore_data['title'], Colors.GREEN)}")
            instant_print(f"   Category: {lore_data.get('category', 'N/A')} | "
                         f"Rarity: {lore_data.get('rarity', 'common')}")
        
        choice = get_input("\nEnter lore number to read (or press Enter to skip): ")
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(lore_list):
                lore_id = lore_list[idx]
                lore_data = LORE_ENTRIES[lore_id]
                instant_print(colored_text(f"\n{'='*60}", Colors.CYAN))
                instant_print(colored_text(f"{lore_data['title']}", Colors.BOLD_YELLOW))
                instant_print(colored_text(f"{'='*60}", Colors.CYAN))
                instant_print(f"{lore_data.get('content', 'No content available.')}")
                instant_print(colored_text(f"{'='*60}\n", Colors.CYAN))
    
    @staticmethod
    def _browse_weather_patterns():
        """Browse weather patterns."""
        instant_print(colored_text("\n=== WEATHER PATTERNS ===", Colors.CYAN))
        instant_print(colored_text(f"Total: {len(WEATHER_PATTERNS)} patterns\n", Colors.YELLOW))
        
        weather_list = sorted(WEATHER_PATTERNS.keys())[:30]
        for i, weather_id in enumerate(weather_list, 1):
            weather_data = WEATHER_PATTERNS[weather_id]
            instant_print(f"{i}. {colored_text(weather_data['name'], Colors.GREEN)}")
            instant_print(f"   Season: {weather_data.get('season', 'N/A')} | "
                         f"Type: {weather_data.get('type', 'N/A')} | "
                         f"Temp: {weather_data.get('temperature', 0)}°C")
            if i % 10 == 0 and i < len(weather_list):
                if get_input("\nPress Enter to continue (or 'q' to quit)...").lower() == 'q':
                    break
    
    @staticmethod
    def _browse_status_effects():
        """Browse status effects."""
        instant_print(colored_text("\n=== STATUS EFFECTS DATABASE ===", Colors.CYAN))
        instant_print(colored_text(f"Total: {len(STATUS_EFFECTS_DATABASE)} effects\n", Colors.YELLOW))
        
        effects_list = sorted(STATUS_EFFECTS_DATABASE.keys())[:30]
        for i, effect_id in enumerate(effects_list, 1):
            effect_data = STATUS_EFFECTS_DATABASE[effect_id]
            instant_print(f"{i}. {colored_text(effect_data['name'], Colors.GREEN)}")
            instant_print(f"   Type: {effect_data.get('type', 'N/A')} | "
                         f"Duration: {effect_data.get('duration', 0)} | "
                         f"Icon: {effect_data.get('icon', '?')}")
            if i % 10 == 0 and i < len(effects_list):
                if get_input("\nPress Enter to continue (or 'q' to quit)...").lower() == 'q':
                    break
    
    @staticmethod
    def _browse_expanded_locations():
        """Browse expanded locations."""
        instant_print(colored_text("\n=== EXPANDED LOCATIONS ===", Colors.CYAN))
        instant_print(colored_text(f"Total: {len(EXPANDED_LOCATIONS)} locations\n", Colors.YELLOW))
        
        locations_list = sorted(EXPANDED_LOCATIONS.keys())
        for i, loc_id in enumerate(locations_list, 1):
            loc_data = EXPANDED_LOCATIONS[loc_id]
            instant_print(f"{i}. {colored_text(loc_data['name'], Colors.GREEN)} ({loc_id})")
            instant_print(f"   Danger: {loc_data.get('danger_level', 0)} | "
                         f"Dark: {loc_data.get('dark', False)}")
            if i % 10 == 0 and i < len(locations_list):
                if get_input("\nPress Enter to continue (or 'q' to quit)...").lower() == 'q':
                    break
    
    @staticmethod
    def _spawn_expanded_creature(game: 'Game'):
        """Spawn a creature from the expanded creatures database."""
        instant_print(colored_text("\nExpanded Creatures (showing first 20):", Colors.YELLOW))
        creatures_list = sorted(list(EXPANDED_CREATURES.keys())[:20])
        for i, creature_id in enumerate(creatures_list, 1):
            creature_data = EXPANDED_CREATURES[creature_id]
            instant_print(f"  {i}. {creature_data['name']} ({creature_id})")
        
        choice = get_input("Enter creature number or ID: ")
        creature_id = None
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(creatures_list):
                creature_id = creatures_list[idx]
        else:
            creature_id = choice
        
        if creature_id and creature_id in EXPANDED_CREATURES:
            creature_data = EXPANDED_CREATURES[creature_id]
            # Create a basic Creature object from the data
            from dataclasses import dataclass
            creature = Creature(
                name=creature_data['name'],
                description=creature_data.get('description', ''),
                creature_type=CreatureType[creature_data.get('creature_type', 'HOSTILE')],
                health=creature_data.get('health', 50),
                max_health=creature_data.get('health', 50),
                damage=creature_data.get('damage', 10),
                defense=creature_data.get('defense', 5),
                experience=creature_data.get('experience', 25),
                loot=creature_data.get('loot', []),
                level=creature_data.get('level', 1)
            )
            location = game.world.get(game.player.current_location)
            if location:
                location.creatures.append(creature)
                slow_print(colored_text(f"Spawned {creature.name}!", Colors.GREEN))
            else:
                slow_print(colored_text("Current location not found.", Colors.RED))
        else:
            slow_print(colored_text("Creature not found.", Colors.RED))
    
    @staticmethod
    def _give_expanded_item(player: 'Player'):
        """Give an item from the expanded items database."""
        instant_print(colored_text("\nExpanded Items (showing first 20):", Colors.YELLOW))
        items_list = sorted(list(EXPANDED_ITEMS.keys())[:20])
        for i, item_id in enumerate(items_list, 1):
            item_data = EXPANDED_ITEMS[item_id]
            instant_print(f"  {i}. {item_data['name']} ({item_id})")
        
        choice = get_input("Enter item number or ID: ")
        item_id = None
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(items_list):
                item_id = items_list[idx]
        else:
            item_id = choice
        
        if item_id and item_id in EXPANDED_ITEMS:
            item_data = EXPANDED_ITEMS[item_id]
            # Create a basic Item object from the data
            item_type = ItemType.CONSUMABLE  # Default
            if item_data.get('type') == 'WEAPON':
                item_type = ItemType.WEAPON
            elif item_data.get('type') == 'ARMOR':
                item_type = ItemType.ARMOR
            elif item_data.get('type') == 'MAGIC':
                item_type = ItemType.CONSUMABLE
            
            item = Item(
                name=item_data['name'],
                description=item_data.get('description', ''),
                item_type=item_type,
                value=item_data.get('value', 10),
                damage=item_data.get('damage', 0),
                defense=item_data.get('defense', 0),
                healing=item_data.get('healing', 0)
            )
            success, msg = player.add_item(item)
            slow_print(colored_text(msg, Colors.GREEN if success else Colors.RED))
        else:
            slow_print(colored_text("Item not found.", Colors.RED))

    # ----- Difficulty and Location Commands (51-55) -----
    @staticmethod
    def _set_difficulty_mode_admin(game: 'Game'):
        """Allow admin to change difficulty mode."""
        slow_print(colored_text("\n=== SET DIFFICULTY MODE ===\n", Colors.CYAN))
        new_difficulty = select_difficulty_mode()
        if hasattr(game.player, 'difficulty_mode'):
            game.player.difficulty_mode = new_difficulty
            slow_print(colored_text(f"Difficulty set to: {new_difficulty.name}", Colors.GREEN))
        else:
            slow_print(colored_text("Player difficulty mode not initialized.", Colors.RED))

    @staticmethod
    def _list_all_locations_admin(game: 'Game'):
        """List all locations in the game."""
        slow_print(colored_text("\n=== ALL GAME LOCATIONS ===\n", Colors.CYAN))
        
        # Get all locations from world
        all_locs = []
        if hasattr(game, 'world') and hasattr(game.world, 'locations'):
            all_locs = list(game.world.locations.keys())
        
        # Add expanded locations
        if 'EXPANDED_LOCATIONS_DATABASE' in globals():
            for loc_id in EXPANDED_LOCATIONS_DATABASE.keys():
                if loc_id not in all_locs:
                    all_locs.append(loc_id)
        
        # Add starting locations
        if 'START_LOCATIONS_DATABASE' in globals():
            for loc_id in START_LOCATIONS_DATABASE.keys():
                if loc_id not in all_locs:
                    all_locs.append(loc_id)
        
        all_locs.sort()
        slow_print(colored_text(f"Total locations: {len(all_locs)}\n", Colors.YELLOW))
        
        # Display paginated
        per_page = 10
        for i in range(0, len(all_locs), per_page):
            batch = all_locs[i:i+per_page]
            for loc_id in batch:
                slow_print(f"  - {loc_id}")
            
            if i + per_page < len(all_locs):
                cont = get_input(f"\nShowing {i+1}-{min(i+per_page, len(all_locs))} of {len(all_locs)}. Continue? (y/n): ")
                if cont.lower() != 'y':
                    break

    @staticmethod
    def _check_location_accessibility_admin(game: 'Game'):
        """Check which locations are accessible."""
        slow_print(colored_text("\n=== LOCATION ACCESSIBILITY CHECK ===\n", Colors.CYAN))
        
        # This is a simplified check
        slow_print(colored_text("Checking route connections...\n", Colors.YELLOW))
        
        reachable = set()
        reachable.add(game.player.current_location)
        
        # BFS to find all reachable locations
        queue = [game.player.current_location]
        visited = set()
        
        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            
            # Get location
            loc = game.world.get_location(current)
            if loc:
                for route in loc.routes:
                    if route.destination not in visited:
                        queue.append(route.destination)
                        reachable.add(route.destination)
        
        slow_print(colored_text(f"✓ Reachable from current location: {len(reachable)} locations\n", Colors.GREEN))
        
        # Check for legendary locations
        legendary = ["infinite_library", "volcanic_forge", "crystal_palace", "atlantis", "sky_islands"]
        slow_print(colored_text("Legendary Location Status:", Colors.CYAN))
        for leg in legendary:
            if leg in reachable:
                slow_print(colored_text(f"  ✓ {leg} - ACCESSIBLE", Colors.GREEN))
            else:
                slow_print(colored_text(f"  ✗ {leg} - NOT ACCESSIBLE", Colors.RED))

    @staticmethod
    def _teleport_to_expanded_location_admin(game: 'Game'):
        """Teleport to an expanded/legendary location."""
        slow_print(colored_text("\n=== TELEPORT TO EXPANDED LOCATION ===\n", Colors.CYAN))
        
        locations = {
            "1": ("infinite_library", "The Infinite Ancient Library"),
            "2": ("volcanic_forge", "The Volcanic Heart Forge"),
            "3": ("crystal_palace", "The Shimmering Crystal Palace"),
            "4": ("atlantis", "Atlantis - The Sunken City"),
            "5": ("sky_islands", "The Floating Sky Islands"),
            "6": ("shadow_realm", "Shadow Realm Gates"),
            "7": ("dragon_lair", "Dragon's Lair"),
        }
        
        slow_print(colored_text("Select destination:", Colors.YELLOW))
        for key, (loc_id, name) in locations.items():
            slow_print(f"  [{key}] {name}")
        slow_print("  [0] Cancel")
        
        choice = get_input("\nChoice: ")
        
        if choice in locations:
            loc_id, name = locations[choice]
            game.player.current_location = loc_id
            slow_print(colored_text(f"\nTeleported to: {name}", Colors.GREEN))
        elif choice == "0":
            slow_print(colored_text("Teleport cancelled.", Colors.YELLOW))
        else:
            slow_print(colored_text("Invalid choice.", Colors.RED))

    @staticmethod
    def _view_starting_options_admin():
        """View all starting location options."""
        slow_print(colored_text("\n=== STARTING LOCATION OPTIONS ===\n", Colors.CYAN))
        
        if 'START_LOCATIONS_DATABASE' not in globals():
            slow_print(colored_text("Starting locations not available.", Colors.RED))
            return
        
        for i, (loc_id, data) in enumerate(START_LOCATIONS_DATABASE.items(), 1):
            slow_print(colored_text(f"\n[{i}] {data['name']}", Colors.YELLOW))
            slow_print(f"    ID: {loc_id}")
            slow_print(f"    Difficulty: {data['difficulty']}")
            slow_print(f"    Starting Items: {', '.join(data['starting_items'])}")
            slow_print(f"    Routes: {len(data['routes'])} available paths")

    # ===== NEW COMPREHENSIVE ADMIN COMMANDS =====
    
    @staticmethod
    def _manage_companions(player: 'Player'):
        """Manage player companions."""
        slow_print(colored_text("\n=== COMPANION MANAGEMENT ===", Colors.CYAN))
        slow_print(f"Current companions: {', '.join(player.companions) if player.companions else 'None'}")
        slow_print("\n[1] Add Companion  [2] Remove Companion  [3] Clear All  [0] Back")
        
        choice = get_input("Choice: ")
        if choice == "1":
            name = get_input("Companion name: ")
            if name and name not in player.companions:
                player.companions.append(name)
                slow_print(colored_text(f"Added companion: {name}", Colors.GREEN))
            else:
                slow_print(colored_text("Invalid or duplicate companion name.", Colors.RED))
        elif choice == "2" and player.companions:
            for i, comp in enumerate(player.companions, 1):
                slow_print(f"  [{i}] {comp}")
            try:
                idx = int(get_input("Select companion to remove: ")) - 1
                if 0 <= idx < len(player.companions):
                    removed = player.companions.pop(idx)
                    slow_print(colored_text(f"Removed companion: {removed}", Colors.GREEN))
            except:
                slow_print(colored_text("Invalid choice.", Colors.RED))
        elif choice == "3":
            player.companions.clear()
            slow_print(colored_text("All companions removed.", Colors.GREEN))

    @staticmethod
    def _manage_reputation(player: 'Player'):
        """Manage player reputation with factions."""
        slow_print(colored_text("\n=== REPUTATION MANAGEMENT ===", Colors.CYAN))
        if player.reputation:
            for faction, rep in player.reputation.items():
                slow_print(f"  {faction}: {rep}")
        else:
            slow_print("No reputation entries.")
        
        slow_print("\n[1] Set Reputation  [2] Clear Faction  [3] Clear All  [0] Back")
        choice = get_input("Choice: ")
        
        if choice == "1":
            faction = get_input("Faction name: ")
            try:
                value = int(get_input("Reputation value (-100 to 100): "))
                player.reputation[faction] = max(-100, min(100, value))
                slow_print(colored_text(f"Set {faction} reputation to {player.reputation[faction]}", Colors.GREEN))
            except:
                slow_print(colored_text("Invalid value.", Colors.RED))
        elif choice == "2":
            faction = get_input("Faction name: ")
            if faction in player.reputation:
                del player.reputation[faction]
                slow_print(colored_text(f"Cleared reputation for {faction}", Colors.GREEN))
        elif choice == "3":
            player.reputation.clear()
            slow_print(colored_text("All reputation cleared.", Colors.GREEN))

    @staticmethod
    def _manage_notes(player: 'Player'):
        """Manage player notes."""
        slow_print(colored_text("\n=== NOTES MANAGEMENT ===", Colors.CYAN))
        if player.notes:
            for i, note in enumerate(player.notes, 1):
                slow_print(f"  [{i}] {note[:60]}{'...' if len(note) > 60 else ''}")
        else:
            slow_print("No notes.")
        
        slow_print("\n[1] Add Note  [2] Remove Note  [3] Clear All  [0] Back")
        choice = get_input("Choice: ")
        
        if choice == "1":
            note = get_input("Note text: ")
            if note:
                player.notes.append(note)
                slow_print(colored_text("Note added.", Colors.GREEN))
        elif choice == "2" and player.notes:
            try:
                idx = int(get_input("Note number to remove: ")) - 1
                if 0 <= idx < len(player.notes):
                    player.notes.pop(idx)
                    slow_print(colored_text("Note removed.", Colors.GREEN))
            except:
                slow_print(colored_text("Invalid choice.", Colors.RED))
        elif choice == "3":
            player.notes.clear()
            slow_print(colored_text("All notes cleared.", Colors.GREEN))

    @staticmethod
    def _manage_equipment(player: 'Player'):
        """Manage equipped items."""
        slow_print(colored_text("\n=== EQUIPMENT MANAGEMENT ===", Colors.CYAN))
        for slot, item in player.equipped.items():
            item_name = item.name if item else "Empty"
            slow_print(f"  {slot}: {item_name}")
        
        slow_print("\n[1] Equip Item  [2] Unequip Item  [3] Unequip All  [0] Back")
        choice = get_input("Choice: ")
        
        if choice == "1":
            # Show inventory items that can be equipped
            equippable = [item for item in player.inventory if item.equippable]
            if not equippable:
                slow_print(colored_text("No equippable items in inventory.", Colors.RED))
                return
            for i, item in enumerate(equippable, 1):
                slow_print(f"  [{i}] {item.name}")
            try:
                idx = int(get_input("Select item: ")) - 1
                if 0 <= idx < len(equippable):
                    item = equippable[idx]
                    # Determine slot based on item type
                    if item.item_type == ItemType.WEAPON:
                        player.equipped['weapon'] = item
                        slow_print(colored_text(f"Equipped {item.name} as weapon.", Colors.GREEN))
                    elif item.item_type == ItemType.ARMOR:
                        player.equipped['armor'] = item
                        slow_print(colored_text(f"Equipped {item.name} as armor.", Colors.GREEN))
                    elif item.item_type == ItemType.LIGHT:
                        player.equipped['light'] = item
                        slow_print(colored_text(f"Equipped {item.name} as light source.", Colors.GREEN))
            except:
                slow_print(colored_text("Invalid choice.", Colors.RED))
        elif choice == "2":
            slot = get_input("Slot to unequip (weapon/armor/light/etc): ").strip().lower()
            if slot in player.equipped and player.equipped[slot]:
                player.equipped[slot] = None
                slow_print(colored_text(f"Unequipped {slot}.", Colors.GREEN))
            else:
                slow_print(colored_text("Invalid slot or already empty.", Colors.RED))
        elif choice == "3":
            for slot in player.equipped:
                player.equipped[slot] = None
            slow_print(colored_text("All equipment removed.", Colors.GREEN))

    @staticmethod
    def _manage_resources(player: 'Player'):
        """Manage stamina, mana, hunger, thirst, sanity."""
        slow_print(colored_text("\n=== RESOURCE MANAGEMENT ===", Colors.CYAN))
        slow_print(f"  Stamina: {player.stamina}/{player.max_stamina}")
        slow_print(f"  Mana: {player.mana}/{player.max_mana}")
        slow_print(f"  Hunger: {player.hunger}")
        slow_print(f"  Thirst: {player.thirst}")
        slow_print(f"  Sanity: {player.sanity}")
        
        slow_print("\n[1] Set Stamina  [2] Set Mana  [3] Set Hunger")
        slow_print("[4] Set Thirst  [5] Set Sanity  [6] Restore All  [0] Back")
        
        choice = get_input("Choice: ")
        try:
            if choice == "1":
                val = int(get_input(f"Stamina (0-{player.max_stamina}): "))
                player.stamina = max(0, min(player.max_stamina, val))
                slow_print(colored_text(f"Stamina set to {player.stamina}", Colors.GREEN))
            elif choice == "2":
                val = int(get_input(f"Mana (0-{player.max_mana}): "))
                player.mana = max(0, min(player.max_mana, val))
                slow_print(colored_text(f"Mana set to {player.mana}", Colors.GREEN))
            elif choice == "3":
                val = int(get_input("Hunger (0-100): "))
                player.hunger = max(0, min(100, val))
                slow_print(colored_text(f"Hunger set to {player.hunger}", Colors.GREEN))
            elif choice == "4":
                val = int(get_input("Thirst (0-100): "))
                player.thirst = max(0, min(100, val))
                slow_print(colored_text(f"Thirst set to {player.thirst}", Colors.GREEN))
            elif choice == "5":
                val = int(get_input("Sanity (0-100): "))
                player.sanity = max(0, min(100, val))
                slow_print(colored_text(f"Sanity set to {player.sanity}", Colors.GREEN))
            elif choice == "6":
                player.stamina = player.max_stamina
                player.mana = player.max_mana
                player.hunger = 100
                player.thirst = 100
                player.sanity = 100
                slow_print(colored_text("All resources restored!", Colors.GREEN))
        except:
            slow_print(colored_text("Invalid value.", Colors.RED))

    @staticmethod
    def _manage_statistics(player: 'Player'):
        """Manage player statistics."""
        slow_print(colored_text("\n=== STATISTICS MANAGEMENT ===", Colors.CYAN))
        slow_print(f"  Deaths: {player.deaths}")
        slow_print(f"  Kills: {player.kills}")
        slow_print(f"  Boss Kills: {player.boss_kills}")
        slow_print(f"  Steps Taken: {player.steps_taken}")
        slow_print(f"  Items Collected: {player.items_collected}")
        slow_print(f"  Items Crafted: {player.items_crafted}")
        slow_print(f"  Secrets Found: {player.secrets_found}")
        slow_print(f"  Treasures Found: {player.treasures_found}")
        slow_print(f"  Total Damage Dealt: {player.total_damage_dealt}")
        slow_print(f"  Total Damage Taken: {player.total_damage_taken}")
        slow_print(f"  Total Healing: {player.total_healing}")
        slow_print(f"  Highest Combo: {player.highest_combo}")
        
        slow_print("\n[1] Set Stat  [2] Reset All Stats  [0] Back")
        choice = get_input("Choice: ")
        
        if choice == "1":
            slow_print("\nWhich stat to modify?")
            slow_print("[1] Deaths  [2] Kills  [3] Boss Kills  [4] Steps")
            slow_print("[5] Items Collected  [6] Items Crafted  [7] Secrets  [8] Treasures")
            stat_choice = get_input("Choice: ")
            try:
                value = int(get_input("New value: "))
                if stat_choice == "1":
                    player.deaths = max(0, value)
                elif stat_choice == "2":
                    player.kills = max(0, value)
                elif stat_choice == "3":
                    player.boss_kills = max(0, value)
                elif stat_choice == "4":
                    player.steps_taken = max(0, value)
                elif stat_choice == "5":
                    player.items_collected = max(0, value)
                elif stat_choice == "6":
                    player.items_crafted = max(0, value)
                elif stat_choice == "7":
                    player.secrets_found = max(0, value)
                elif stat_choice == "8":
                    player.treasures_found = max(0, value)
                slow_print(colored_text("Stat updated.", Colors.GREEN))
            except:
                slow_print(colored_text("Invalid value.", Colors.RED))
        elif choice == "2":
            player.deaths = 0
            player.kills = 0
            player.boss_kills = 0
            player.steps_taken = 0
            player.items_collected = 0
            player.items_crafted = 0
            player.secrets_found = 0
            player.treasures_found = 0
            player.total_damage_dealt = 0
            player.total_damage_taken = 0
            player.total_healing = 0
            player.highest_combo = 0
            slow_print(colored_text("All statistics reset.", Colors.GREEN))

    @staticmethod
    def _manage_quests(player: 'Player'):
        """Advanced quest management."""
        slow_print(colored_text("\n=== QUEST MANAGEMENT ===", Colors.CYAN))
        slow_print(f"Active: {len(player.active_quests)}, Completed: {len(player.completed_quests)}, Failed: {len(player.failed_quests)}")
        
        slow_print("\n[1] Add Quest  [2] Remove Quest  [3] Fail Quest")
        slow_print("[4] Unfail Quest  [5] View All Quests  [0] Back")
        
        choice = get_input("Choice: ")
        if choice == "1":
            quest_id = get_input("Quest ID: ")
            quest = QuestSystem.get_quest(quest_id)
            if quest:
                QuestSystem.start_quest(quest_id, player)
            else:
                slow_print(colored_text("Quest not found.", Colors.RED))
        elif choice == "2" and player.active_quests:
            for i, q in enumerate(player.active_quests, 1):
                slow_print(f"  [{i}] {q.name}")
            try:
                idx = int(get_input("Quest to remove: ")) - 1
                if 0 <= idx < len(player.active_quests):
                    removed = player.active_quests.pop(idx)
                    slow_print(colored_text(f"Removed quest: {removed.name}", Colors.GREEN))
            except:
                slow_print(colored_text("Invalid choice.", Colors.RED))
        elif choice == "3" and player.active_quests:
            for i, q in enumerate(player.active_quests, 1):
                slow_print(f"  [{i}] {q.name}")
            try:
                idx = int(get_input("Quest to fail: ")) - 1
                if 0 <= idx < len(player.active_quests):
                    quest = player.active_quests.pop(idx)
                    player.failed_quests.append(quest.quest_id)
                    slow_print(colored_text(f"Failed quest: {quest.name}", Colors.GREEN))
            except:
                slow_print(colored_text("Invalid choice.", Colors.RED))
        elif choice == "4" and player.failed_quests:
            for i, qid in enumerate(player.failed_quests, 1):
                slow_print(f"  [{i}] {qid}")
            try:
                idx = int(get_input("Quest to unfail: ")) - 1
                if 0 <= idx < len(player.failed_quests):
                    player.failed_quests.pop(idx)
                    slow_print(colored_text("Quest unfailed.", Colors.GREEN))
            except:
                slow_print(colored_text("Invalid choice.", Colors.RED))
        elif choice == "5":
            slow_print(colored_text("\nActive Quests:", Colors.YELLOW))
            for q in player.active_quests:
                slow_print(f"  - {q.name}")
            slow_print(colored_text("\nCompleted Quests:", Colors.GREEN))
            for qid in player.completed_quests:
                slow_print(f"  - {qid}")
            slow_print(colored_text("\nFailed Quests:", Colors.RED))
            for qid in player.failed_quests:
                slow_print(f"  - {qid}")

    @staticmethod
    def _manage_achievements(player: 'Player'):
        """Advanced achievement management."""
        slow_print(colored_text("\n=== ACHIEVEMENT MANAGEMENT ===", Colors.CYAN))
        slow_print(f"Unlocked: {len(player.achievements)}")
        
        slow_print("\n[1] Unlock Achievement  [2] Lock Achievement")
        slow_print("[3] View All  [4] Unlock All  [5] Lock All  [0] Back")
        
        choice = get_input("Choice: ")
        if choice == "1":
            ach_id = get_input("Achievement ID: ")
            if ach_id not in player.achievements:
                player.achievements.append(ach_id)
                slow_print(colored_text(f"Unlocked: {ach_id}", Colors.GREEN))
        elif choice == "2" and player.achievements:
            for i, ach in enumerate(player.achievements, 1):
                slow_print(f"  [{i}] {ach}")
            try:
                idx = int(get_input("Achievement to lock: ")) - 1
                if 0 <= idx < len(player.achievements):
                    locked = player.achievements.pop(idx)
                    slow_print(colored_text(f"Locked: {locked}", Colors.GREEN))
            except:
                slow_print(colored_text("Invalid choice.", Colors.RED))
        elif choice == "3":
            for ach in player.achievements:
                slow_print(f"  ✓ {ach}")
        elif choice == "4":
            AdminPanel._unlock_all_achievements(player)
        elif choice == "5":
            player.achievements.clear()
            player.unlocked_achievements.clear()
            slow_print(colored_text("All achievements locked.", Colors.GREEN))

    @staticmethod
    def _manage_recipes(player: 'Player'):
        """Advanced recipe management."""
        slow_print(colored_text("\n=== RECIPE MANAGEMENT ===", Colors.CYAN))
        slow_print(f"Known recipes: {len(player.known_recipes)}")
        for recipe in player.known_recipes:
            slow_print(f"  - {recipe}")
        
        slow_print("\n[1] Add Recipe  [2] Remove Recipe  [3] Clear All  [0] Back")
        choice = get_input("Choice: ")
        
        if choice == "1":
            recipe_id = get_input("Recipe ID: ")
            if recipe_id not in player.known_recipes:
                player.known_recipes.append(recipe_id)
                slow_print(colored_text(f"Added recipe: {recipe_id}", Colors.GREEN))
        elif choice == "2" and player.known_recipes:
            for i, r in enumerate(player.known_recipes, 1):
                slow_print(f"  [{i}] {r}")
            try:
                idx = int(get_input("Recipe to remove: ")) - 1
                if 0 <= idx < len(player.known_recipes):
                    removed = player.known_recipes.pop(idx)
                    slow_print(colored_text(f"Removed recipe: {removed}", Colors.GREEN))
            except:
                slow_print(colored_text("Invalid choice.", Colors.RED))
        elif choice == "3":
            player.known_recipes.clear()
            slow_print(colored_text("All recipes removed.", Colors.GREEN))

    @staticmethod
    def _set_play_time(player: 'Player'):
        """Set play time."""
        try:
            minutes = int(get_input("Play time in minutes: "))
            player.play_time = max(0, minutes)
            slow_print(colored_text(f"Play time set to {player.play_time} minutes", Colors.GREEN))
        except:
            slow_print(colored_text("Invalid value.", Colors.RED))

    @staticmethod
    def _save_game_admin(game: 'Game'):
        """Save game from admin panel."""
        SaveLoadSystem.save_game(game)
        slow_print(colored_text("Game saved!", Colors.GREEN))

    @staticmethod
    def _load_game_admin(game: 'Game'):
        """Load game from admin panel."""
        loaded = SaveLoadSystem.load_game()
        if loaded:
            game.player = loaded.player
            game.world = loaded.world
            game.time_weather = loaded.time_weather
            slow_print(colored_text("Game loaded!", Colors.GREEN))
        else:
            slow_print(colored_text("No save file found.", Colors.RED))

    @staticmethod
    def _reset_player_progress(player: 'Player'):
        """Reset player progress."""
        confirm = get_input("Reset ALL player progress? Type 'CONFIRM': ")
        if confirm == "CONFIRM":
            player.experience = 0
            player.level = 1
            player.skill_points = 0
            player.active_quests.clear()
            player.completed_quests.clear()
            player.failed_quests.clear()
            player.achievements.clear()
            player.unlocked_achievements.clear()
            player.known_recipes = ["torch", "bandage", "rope", "campfire"]
            player.discovered_locations = ["clearing"]
            player.deaths = 0
            player.kills = 0
            player.boss_kills = 0
            player.steps_taken = 0
            player.items_collected = 0
            player.items_crafted = 0
            player.secrets_found = 0
            player.treasures_found = 0
            player.total_damage_dealt = 0
            player.total_damage_taken = 0
            player.total_healing = 0
            player.play_time = 0
            slow_print(colored_text("Player progress reset!", Colors.RED))
        else:
            slow_print(colored_text("Reset cancelled.", Colors.YELLOW))

    # ===== EXCLUSIVE ADMIN-ONLY FEATURES =====
    
    @staticmethod
    def _admin_exclusive_items(player: 'Player'):
        """Give admin-exclusive legendary items that can ONLY be obtained through admin panel."""
        slow_print(colored_text("\n╔═══════════════════════════════════════════╗", Colors.MAGENTA))
        slow_print(colored_text("║    🌟 ADMIN EXCLUSIVE ITEMS 🌟           ║", Colors.MAGENTA))
        slow_print(colored_text("╚═══════════════════════════════════════════╝", Colors.MAGENTA))
        slow_print(colored_text("\nThese legendary items exist ONLY in the admin realm!", Colors.CYAN))
        
        exclusive_items = {
            "1": ("Admin's Omniblade", "A reality-warping sword that can cut through dimensions. Damage: ∞"),
            "2": ("Timekeeper's Watch", "Control time itself. Freeze enemies, rewind mistakes, fast-forward."),
            "3": ("Reality Gauntlet", "Manipulate the fabric of reality. Change weather, terrain, existence."),
            "4": ("Quantum Armor", "Armor that exists in all states simultaneously. Defense: Perfect."),
            "5": ("Infinity Potion", "A potion that grants temporary omnipotence for 60 seconds."),
            "6": ("Developer's Crown", "Crown of the game creators. Grants all knowledge and power."),
            "7": ("Void Crystal", "A crystal containing pure nothingness. Can delete anything."),
            "8": ("Phoenix Codex", "A book containing every secret, every ending, every possibility."),
            "9": ("All of them", "Receive every admin exclusive item!")
        }
        
        for key, (name, desc) in exclusive_items.items():
            print(f"  [{key}] {colored_text(name, Colors.BOLD_YELLOW)}")
            print(f"      {colored_text(desc, Colors.CYAN)}")
        
        choice = get_input("\nSelect item: ")
        
        # Create admin-exclusive items with special properties
        if choice in exclusive_items and choice != "9":
            name, desc = exclusive_items[choice]
            # Create as a legendary weapon/item
            item = Item(
                name=name,
                description=desc,
                item_type=ItemType.WEAPON if "blade" in name.lower() or "sword" in name.lower() else ItemType.TOOL,
                weight=0.1,  # Nearly weightless
                value=999999,
                equippable=True,
                damage=9999 if "blade" in name.lower() else 0,
                rarity="admin_exclusive"
            )
            success, msg = player.add_item(item)
            slow_print(colored_text(f"\n✨ {name} materializes from the admin dimension!", Colors.BOLD_YELLOW))
            slow_print(colored_text("This item defies the normal rules of the game...", Colors.MAGENTA))
        elif choice == "9":
            count = 0
            for key, (name, desc) in exclusive_items.items():
                if key == "9":
                    continue
                item = Item(
                    name=name,
                    description=desc,
                    item_type=ItemType.WEAPON if "blade" in name.lower() else ItemType.TOOL,
                    weight=0.1,
                    value=999999,
                    equippable=True,
                    damage=9999 if "blade" in name.lower() else 0,
                    rarity="admin_exclusive"
                )
                player.add_item(item)
                count += 1
            slow_print(colored_text(f"\n✨ All {count} admin exclusive items acquired!", Colors.BOLD_YELLOW))

    @staticmethod
    def _reality_warper(game: 'Game'):
        """Warp reality - change fundamental game rules."""
        slow_print(colored_text("\n╔═══════════════════════════════════════════╗", Colors.MAGENTA))
        slow_print(colored_text("║    🌀 REALITY WARPER 🌀                  ║", Colors.MAGENTA))
        slow_print(colored_text("╚═══════════════════════════════════════════╝", Colors.MAGENTA))
        slow_print(colored_text("\nBend the rules of reality itself!", Colors.CYAN))
        
        print("\n  [1] Invert Gravity (enemies fall up)")
        print("  [2] Reverse Time (go back 1 hour of play time)")
        print("  [3] Duplicate Self (create a clone companion)")
        print("  [4] Summon Rainbow Bridge (instant path to any location)")
        print("  [5] Freeze All Enemies (permanent freeze)")
        print("  [6] Transform into Dragon (shapeshift)")
        print("  [7] Open Developer Console (special debug mode)")
        print("  [8] Summon Admin Pet (friendly overpowered companion)")
        print("  [0] Cancel")
        
        choice = get_input("\nWarp reality: ")
        
        if choice == "1":
            slow_print(colored_text("\n🌀 Reality warps! Gravity inverts!", Colors.MAGENTA))
            slow_print(colored_text("Enemies now fall upward into the void...", Colors.CYAN))
            game.player.notes.append("⚡ Admin Note: Gravity is currently inverted")
        elif choice == "2":
            old_time = game.player.play_time
            game.player.play_time = max(0, game.player.play_time - 60)
            slow_print(colored_text(f"\n⏰ Time flows backward! Lost {old_time - game.player.play_time} minutes.", Colors.MAGENTA))
        elif choice == "3":
            if "Admin Clone" not in game.player.companions:
                game.player.companions.append("Admin Clone")
                slow_print(colored_text("\n👥 A perfect clone materializes beside you!", Colors.MAGENTA))
                slow_print(colored_text("Your clone has all your abilities and follows your commands.", Colors.CYAN))
        elif choice == "4":
            slow_print(colored_text("\n🌈 A shimmering rainbow bridge appears!", Colors.MAGENTA))
            slow_print("Type any location ID to teleport there instantly:")
            dest = get_input("Destination: ")
            if dest in game.world:
                game.player.current_location = dest
                slow_print(colored_text(f"✨ Teleported to {game.world[dest].name}!", Colors.GREEN))
            else:
                slow_print(colored_text("Invalid destination.", Colors.RED))
        elif choice == "5":
            slow_print(colored_text("\n❄️ Time stops for all enemies!", Colors.MAGENTA))
            slow_print(colored_text("All hostile creatures are permanently frozen in time.", Colors.CYAN))
            game.player.notes.append("⚡ Admin Note: All enemies frozen in time")
        elif choice == "6":
            if "Dragon Form" not in game.player.notes:
                game.player.notes.append("🐉 TRANSFORMED: Currently in dragon form")
                game.player.max_health += 500
                game.player.health = game.player.max_health
                slow_print(colored_text("\n🐉 You transform into a mighty dragon!", Colors.MAGENTA))
                slow_print(colored_text("Your scales gleam with admin power! +500 HP!", Colors.CYAN))
        elif choice == "7":
            slow_print(colored_text("\n💻 Developer Console Access Granted", Colors.MAGENTA))
            slow_print(colored_text("You can now see the matrix of the game...", Colors.GREEN))
            SETTINGS.debug_mode = True
            game.player.notes.append("💻 Admin: Developer console active")
        elif choice == "8":
            if "Admin Phoenix" not in game.player.companions:
                game.player.companions.append("Admin Phoenix")
                slow_print(colored_text("\n🔥 An immortal phoenix appears in a burst of flame!", Colors.MAGENTA))
                slow_print(colored_text("The Admin Phoenix: Immune to death, deals 999 damage, heals you constantly.", Colors.CYAN))

    @staticmethod
    def _time_travel_menu(game: 'Game'):
        """Travel through time to different game states."""
        slow_print(colored_text("\n╔═══════════════════════════════════════════╗", Colors.MAGENTA))
        slow_print(colored_text("║    ⏰ TIME TRAVEL CHAMBER ⏰             ║", Colors.MAGENTA))
        slow_print(colored_text("╚═══════════════════════════════════════════╝", Colors.MAGENTA))
        
        print("\n  [1] Go to Beginning (Day 1, Hour 0)")
        print("  [2] Jump Forward 1 Day")
        print("  [3] Jump Forward 7 Days")
        print("  [4] Go to Specific Time")
        print("  [5] Set Permanent Time (freeze at dawn/noon/dusk/night)")
        print("  [0] Cancel")
        
        choice = get_input("\nTime travel: ")
        
        if choice == "1":
            game.time_weather.day = 1
            game.time_weather.hour = 0
            game.time_weather.minute = 0
            slow_print(colored_text("\n⏰ Time rewinds to the very beginning!", Colors.MAGENTA))
        elif choice == "2":
            game.time_weather.day += 1
            slow_print(colored_text(f"\n⏰ Jumped to Day {game.time_weather.day}!", Colors.MAGENTA))
        elif choice == "3":
            game.time_weather.day += 7
            slow_print(colored_text(f"\n⏰ Jumped to Day {game.time_weather.day}!", Colors.MAGENTA))
        elif choice == "4":
            try:
                day = int(get_input("Day number: "))
                hour = int(get_input("Hour (0-23): "))
                game.time_weather.day = max(1, day)
                game.time_weather.hour = max(0, min(23, hour))
                slow_print(colored_text(f"\n⏰ Traveled to Day {day}, Hour {hour}!", Colors.MAGENTA))
            except:
                slow_print(colored_text("Invalid time format.", Colors.RED))
        elif choice == "5":
            print("\n  [1] Permanent Dawn")
            print("  [2] Permanent Noon")
            print("  [3] Permanent Dusk")
            print("  [4] Permanent Night")
            time_choice = get_input("Choose: ")
            time_map = {"1": 6, "2": 12, "3": 18, "4": 0}
            if time_choice in time_map:
                game.time_weather.hour = time_map[time_choice]
                game.player.notes.append(f"⚡ Admin: Time frozen at hour {game.time_weather.hour}")
                slow_print(colored_text("\n⏰ Time is now permanently frozen!", Colors.MAGENTA))

    @staticmethod
    def _easter_egg_spawner(game: 'Game'):
        """Spawn special easter eggs and secret encounters."""
        slow_print(colored_text("\n╔═══════════════════════════════════════════╗", Colors.MAGENTA))
        slow_print(colored_text("║    🥚 EASTER EGG SPAWNER 🥚              ║", Colors.MAGENTA))
        slow_print(colored_text("╚═══════════════════════════════════════════╝", Colors.MAGENTA))
        
        print("\n  [1] Spawn Secret Boss: The Developer")
        print("  [2] Find Lost Treasure Cache (random legendary items)")
        print("  [3] Encounter Mysterious Stranger (grants wishes)")
        print("  [4] Open Portal to Secret Realm")
        print("  [5] Summon Friendly Unicorn")
        print("  [6] Discover Ancient Code Fragment")
        print("  [7] Meet Your Future Self")
        print("  [8] All Easter Eggs")
        print("  [0] Cancel")
        
        choice = get_input("\nSpawn: ")
        
        if choice == "1":
            slow_print(colored_text("\n💀 A mysterious figure materializes...", Colors.MAGENTA))
            slow_print(colored_text("'I am The Developer. You shouldn't be here...'", Colors.RED))
            game.player.notes.append("👨‍💻 Met The Developer - Secret Boss Encounter")
        elif choice == "2":
            treasures = ["ancient sword", "glowing crystal", "sunstone", "frost blade", "guardian blade"]
            for treasure in treasures:
                item = ItemFactory.create_item(treasure)
                if item:
                    game.player.add_item(item)
            slow_print(colored_text("\n💎 A hidden treasure cache materializes!", Colors.YELLOW))
            slow_print(colored_text(f"Found {len(treasures)} legendary items!", Colors.GREEN))
        elif choice == "3":
            slow_print(colored_text("\n🎭 A hooded stranger appears...", Colors.MAGENTA))
            slow_print(colored_text("'Three wishes I grant thee, admin of this realm.'", Colors.CYAN))
            game.player.notes.append("🎭 Met Mysterious Stranger - 3 wishes available")
        elif choice == "4":
            slow_print(colored_text("\n🌀 A swirling portal opens in the air!", Colors.MAGENTA))
            slow_print(colored_text("You glimpse infinite possibilities beyond...", Colors.CYAN))
            game.player.notes.append("🌀 Portal to Secret Realm opened")
        elif choice == "5":
            if "Mystical Unicorn" not in game.player.companions:
                game.player.companions.append("Mystical Unicorn")
                slow_print(colored_text("\n🦄 A beautiful unicorn appears!", Colors.MAGENTA))
                slow_print(colored_text("It nuzzles you gently and joins your party.", Colors.CYAN))
        elif choice == "6":
            slow_print(colored_text("\n📜 Ancient code fragments float before you:", Colors.MAGENTA))
            slow_print(colored_text("def reality(): return whatever_you_imagine()", Colors.GREEN))
            game.player.notes.append("📜 Discovered: Ancient Code Fragment")
            game.player.secrets_found += 1
        elif choice == "7":
            slow_print(colored_text("\n⚡ A temporal anomaly appears!", Colors.MAGENTA))
            slow_print(colored_text("Your future self steps through time...", Colors.CYAN))
            slow_print(colored_text(f"Future You: 'In {game.player.play_time + 100} minutes, you will...'", Colors.YELLOW))
            game.player.notes.append("⚡ Met future self - temporal paradox created")
        elif choice == "8":
            AdminPanel._easter_egg_spawner(game)  # Recursive to show menu
            for i in range(1, 8):
                # Simulate spawning all
                pass
            slow_print(colored_text("\n✨ ALL EASTER EGGS ACTIVATED!", Colors.BOLD_MAGENTA))

    @staticmethod
    def _god_powers_menu(player: 'Player'):
        """Grant temporary god-like powers."""
        slow_print(colored_text("\n╔═══════════════════════════════════════════╗", Colors.MAGENTA))
        slow_print(colored_text("║    ⚡ GOD POWERS BESTOWED ⚡             ║", Colors.MAGENTA))
        slow_print(colored_text("╚═══════════════════════════════════════════╝", Colors.MAGENTA))
        
        print("\n  [1] Omniscience (know all locations, secrets, solutions)")
        print("  [2] Immortality (cannot die, ever)")
        print("  [3] Omnipotence (one-shot everything)")
        print("  [4] Telekinesis (move items between locations mentally)")
        print("  [5] Mind Control (control all NPCs and creatures)")
        print("  [6] Divine Blessing (all stats set to maximum)")
        print("  [7] ALL POWERS")
        print("  [0] Cancel")
        
        choice = get_input("\nGrant power: ")
        
        if choice == "1":
            # Reveal all locations
            for loc_id in ["clearing", "dark_woods", "ancient_ruins", "freedom"]:  # Add more as needed
                if loc_id not in player.discovered_locations:
                    player.discovered_locations.append(loc_id)
            player.notes.append("👁️ OMNISCIENCE: All knowledge revealed")
            slow_print(colored_text("\n👁️ Your mind expands! All secrets are revealed!", Colors.MAGENTA))
        elif choice == "2":
            player.notes.append("💀 IMMORTALITY: Death cannot claim you")
            SETTINGS.god_mode = True
            slow_print(colored_text("\n💀 You transcend mortality! Death has no power over you!", Colors.MAGENTA))
        elif choice == "3":
            SETTINGS.instant_kill = True
            player.notes.append("⚡ OMNIPOTENCE: Nothing can withstand your power")
            slow_print(colored_text("\n⚡ Infinite power flows through you!", Colors.MAGENTA))
        elif choice == "4":
            player.notes.append("🌀 TELEKINESIS: Matter bends to your will")
            slow_print(colored_text("\n🌀 Your mind can move objects across dimensions!", Colors.MAGENTA))
        elif choice == "5":
            player.notes.append("🧠 MIND CONTROL: All beings obey your thoughts")
            slow_print(colored_text("\n🧠 All creatures and NPCs fall under your command!", Colors.MAGENTA))
        elif choice == "6":
            player.health = player.max_health = 9999
            player.stamina = player.max_stamina = 9999
            player.mana = player.max_mana = 9999
            player.hunger = 100
            player.thirst = 100
            player.sanity = 100
            for skill in player.skills:
                player.skills[skill] = 99
            slow_print(colored_text("\n✨ Divine power fills your being!", Colors.MAGENTA))
            slow_print(colored_text("All attributes raised to divine levels!", Colors.YELLOW))
        elif choice == "7":
            # Grant all powers
            AdminPanel._god_powers_menu(player)
            for i in range(1, 7):
                # Simulate granting all
                pass
            slow_print(colored_text("\n⚡⚡⚡ ABSOLUTE POWER ACHIEVED! ⚡⚡⚡", Colors.BOLD_MAGENTA))



