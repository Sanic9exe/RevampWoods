"""Combat system."""

from typing import Optional, List, Dict, Tuple
import random
import time

from .models import Creature, Item
from .colors import Colors
from .utils import slow_print, CreatureType

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class CombatSystem:
    """Handles combat between player and creatures."""
    
    @staticmethod
    def start_combat(player: Player, creature: Creature) -> bool:
        """
        Start and manage combat between player and creature.
        Returns True if player wins, False if player dies or flees.
        """
        player.is_in_combat = True
        
        print_event_box(
            f"A {creature.name} attacks!\n{creature.description}",
            EventType.COMBAT
        )
        
        while player.health > 0 and creature.alive:
            # Display combat status
            CombatSystem._display_combat_status(player, creature)
            
            # Get player action
            action = CombatSystem._get_combat_action()
            
            if action == "1":  # Attack
                CombatSystem._player_attack(player, creature)
            elif action == "2":  # Defend
                CombatSystem._player_defend(player)
            elif action == "3":  # Use item
                CombatSystem._use_combat_item(player)
            elif action == "4":  # Flee
                if CombatSystem._attempt_flee(player, creature):
                    player.is_in_combat = False
                    return False
            elif action == "5" and SETTINGS.skip_combat:  # Admin skip
                creature.health = 0
                creature.alive = False
            
            # Creature's turn (if still alive)
            if creature.alive and player.health > 0:
                CombatSystem._creature_attack(player, creature)
        
        player.is_in_combat = False
        
        if player.health <= 0:
            return False
        
        # Victory
        CombatSystem._handle_victory(player, creature)
        return True
    
    @staticmethod
    def _display_combat_status(player: Player, creature: Creature):
        """Display current combat status."""
        player_health_pct = int((player.health / player.max_health) * 20)
        player_bar = colored_text("█" * player_health_pct, Colors.GREEN) + \
                    colored_text("░" * (20 - player_health_pct), Colors.DIM)
        
        creature_health_pct = int((creature.health / creature.max_health) * 20)
        creature_bar = colored_text("█" * creature_health_pct, Colors.RED) + \
                      colored_text("░" * (20 - creature_health_pct), Colors.DIM)
        
        print()
        instant_print(colored_text("═══════════════ COMBAT ═══════════════", Colors.BOLD_RED))
        instant_print(f"  You:    [{player_bar}] {player.health}/{player.max_health}")
        instant_print(f"  {creature.name}: [{creature_bar}] {creature.health}/{creature.max_health}")
        instant_print(colored_text("═══════════════════════════════════════", Colors.BOLD_RED))
        print()
        instant_print(colored_text("  [1] Attack", Colors.RED))
        instant_print(colored_text("  [2] Defend", Colors.BLUE))
        instant_print(colored_text("  [3] Use Item", Colors.GREEN))
        instant_print(colored_text("  [4] Flee", Colors.YELLOW))
        if SETTINGS.skip_combat:
            instant_print(colored_text("  [5] [ADMIN] Skip Combat", Colors.MAGENTA))
    
    @staticmethod
    def _get_combat_action() -> str:
        """Get player's combat action."""
        return get_input("Your action: ", Colors.BOLD_RED)
    
    @staticmethod
    def _player_attack(player: Player, creature: Creature):
        """Handle player's attack."""
        damage, damage_type = player.get_attack_damage()
        
        if SETTINGS.instant_kill:
            damage = 9999
        
        actual_damage = creature.take_damage(damage, damage_type)
        player.total_damage_dealt += actual_damage
        player.current_combo += 1
        
        if player.current_combo > player.highest_combo:
            player.highest_combo = player.current_combo
        
        slow_print(colored_text(
            f"You strike the {creature.name} for {actual_damage} {damage_type} damage!",
            Colors.BOLD_GREEN
        ))
        
        if not creature.alive:
            slow_print(colored_text(f"The {creature.name} falls!", Colors.BOLD_YELLOW))
    
    @staticmethod
    def _player_defend(player: Player):
        """Handle player's defend action."""
        player.add_status_effect("protected", 1)
        slow_print(colored_text("You raise your guard, preparing to defend.", Colors.BLUE))
    
    @staticmethod
    def _use_combat_item(player: Player):
        """Handle using an item in combat."""
        usable_items = [i for i in player.inventory if i.usable]
        
        if not usable_items:
            slow_print(colored_text("You have no usable items!", Colors.RED))
            return
        
        instant_print(colored_text("\nUsable items:", Colors.YELLOW))
        for i, item in enumerate(usable_items, 1):
            instant_print(f"  [{i}] {item.name}")
        instant_print("  [0] Cancel")
        
        choice = get_input("Use which item? ")
        
        try:
            index = int(choice)
            if index == 0:
                return
            if 1 <= index <= len(usable_items):
                item = usable_items[index - 1]
                result = item.use_effect(player)
                slow_print(colored_text(result, Colors.GREEN))
                player.remove_item(item.name)
        except ValueError:
            slow_print(colored_text("Invalid choice.", Colors.RED))
    
    @staticmethod
    def _attempt_flee(player: Player, creature: Creature) -> bool:
        """Attempt to flee from combat."""
        flee_chance = 30 + player.skills[SkillType.STEALTH] * 5
        
        if chance(flee_chance):
            slow_print(colored_text("You successfully escape!", Colors.GREEN))
            return True
        else:
            slow_print(colored_text("You fail to escape!", Colors.RED))
            # Creature gets a free attack
            CombatSystem._creature_attack(player, creature)
            return False
    
    @staticmethod
    def _creature_attack(player: Player, creature: Creature):
        """Handle creature's attack."""
        damage, ability = creature.attack()
        actual_damage = player.take_damage(damage)
        
        attack_msg = f"The {creature.name} attacks you for {actual_damage} damage!"
        if ability:
            attack_msg += f" (Used {ability}!)"
            if ability == "poison":
                player.add_status_effect("poison", 3)
        
        slow_print(colored_text(attack_msg, Colors.BOLD_RED))
    
    @staticmethod
    def _handle_victory(player: Player, creature: Creature):
        """Handle victory rewards."""
        player.kills += 1
        player.kill_count[creature.name] = player.kill_count.get(creature.name, 0) + 1
        
        if creature.creature_type == CreatureType.BOSS:
            player.boss_kills += 1
        
        # Experience
        leveled = player.gain_experience(creature.experience)
        
        # Gold
        gold = creature.get_gold_drop()
        if gold > 0:
            player.gold += gold
        
        # Loot
        loot = creature.get_loot()
        
        victory_text = f"""
╔═══════════════════════════════════════════════════════╗
║                    ⚔️  VICTORY! ⚔️                      ║
║═══════════════════════════════════════════════════════║
║  You defeated the {creature.name}!
║  
║  Rewards:
║    ✨ Experience: +{creature.experience}
║    💰 Gold: +{gold}
"""
        if loot:
            victory_text += f"║    📦 Loot: {', '.join(loot)}\n"
        victory_text += "╚═══════════════════════════════════════════════════════╝"
        
        print_event_box(victory_text.strip(), EventType.TREASURE)
        
        # Add loot to inventory
        for item_name in loot:
            item = ItemFactory.create_item(item_name)
            if item:
                player.add_item(item)



