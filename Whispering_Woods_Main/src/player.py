"""Player character class."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Set, Tuple
from datetime import datetime
import random

from .colors import Colors
from .utils import ItemType, StatusEffect, slow_print, SkillType
from .models import Item, Creature, Quest, Achievement

# ============================================================================
# PLAYER CLASS
# ============================================================================

class Player:
    """Represents the player character with all stats and inventory."""
    
    def __init__(self, name: str = "Traveler"):
        self.name = name
        self.health = 100
        self.max_health = 100
        self.stamina = 100
        self.max_stamina = 100
        self.mana = 50
        self.max_mana = 50
        self.hunger = 100
        self.thirst = 100
        self.sanity = 100
        self.experience = 0
        self.level = 1
        self.skill_points = 0
        self.inventory: List[Item] = []
        self.equipped: Dict[str, Optional[Item]] = {
            'weapon': None,
            'armor': None,
            'helmet': None,
            'boots': None,
            'gloves': None,
            'light': None,
            'accessory1': None,
            'accessory2': None
        }
        self.skills: Dict[SkillType, int] = {
            skill: 1 for skill in SkillType
        }
        self.current_location = "clearing"
        self.previous_location = ""
        self.discovered_locations: List[str] = ["clearing"]
        self.active_quests: List[Quest] = []
        self.completed_quests: List[str] = []
        self.failed_quests: List[str] = []
        self.known_recipes: List[str] = ["torch", "bandage", "rope", "campfire"]
        self.status_effects: Dict[str, int] = {}
        self.notes: List[str] = []
        self.play_time = 0
        self.deaths = 0
        self.kills = 0
        self.boss_kills = 0
        self.steps_taken = 0
        self.items_collected = 0
        self.items_crafted = 0
        self.secrets_found = 0
        self.treasures_found = 0
        self.achievements: List[str] = []
        self.unlocked_achievements: Dict[str, Achievement] = {}
        self.companions: List[str] = []
        self.gold = 25
        self.reputation: Dict[str, int] = {}
        self.kill_count: Dict[str, int] = {}
        self.visited_locations_count: Dict[str, int] = {}
        self.total_damage_dealt = 0
        self.total_damage_taken = 0
        self.total_healing = 0
        self.highest_combo = 0
        self.current_combo = 0
        self.last_rest_time = 0
        self.is_resting = False
        self.is_hidden = False
        self.is_in_combat = False
        
    def get_attack_damage(self) -> Tuple[int, str]:
        """Calculate player's attack damage with weapon effects."""
        base_damage = 5
        weapon_damage = 0
        damage_type = "physical"
        
        if self.equipped['weapon']:
            weapon = self.equipped['weapon']
            weapon_damage = weapon.damage
            if weapon.special_effects:
                if "fire" in weapon.special_effects:
                    damage_type = "fire"
                elif "ice" in weapon.special_effects:
                    damage_type = "ice"
                elif "silver" in weapon.special_effects:
                    damage_type = "silver"
        
        skill_bonus = self.skills[SkillType.COMBAT] // 2
        
        # Check for status effects
        modifier = 0
        if "strengthened" in self.status_effects:
            modifier += 5
        if "weakened" in self.status_effects:
            modifier -= 5
        
        total_damage = base_damage + weapon_damage + skill_bonus + roll_dice(6, modifier=-3) + modifier
        return max(1, total_damage), damage_type
    
    def get_defense(self) -> int:
        """Calculate player's total defense."""
        base_defense = 2
        armor_defense = 0
        
        for slot in ['armor', 'helmet', 'boots', 'gloves']:
            if self.equipped[slot]:
                armor_defense += self.equipped[slot].defense
        
        # Status effects
        modifier = 0
        if "protected" in self.status_effects:
            modifier += 5
        
        return base_defense + armor_defense + modifier
    
    def take_damage(self, amount: int) -> int:
        """Apply damage to player and return actual damage taken."""
        if SETTINGS.god_mode:
            return 0
        
        defense = self.get_defense()
        actual_damage = max(1, amount - defense // 2)
        self.health -= actual_damage
        self.total_damage_taken += actual_damage
        self.current_combo = 0
        
        if self.health <= 0:
            self.health = 0
        
        return actual_damage
    
    def heal(self, amount: int) -> int:
        """Heal the player and return actual amount healed."""
        healed = min(amount, self.max_health - self.health)
        self.health += healed
        self.total_healing += healed
        return healed
    
    def restore_stamina(self, amount: int) -> int:
        """Restore stamina and return actual amount restored."""
        restored = min(amount, self.max_stamina - self.stamina)
        self.stamina += restored
        return restored
    
    def restore_mana(self, amount: int) -> int:
        """Restore mana and return actual amount restored."""
        restored = min(amount, self.max_mana - self.mana)
        self.mana += restored
        return restored
    
    def use_stamina(self, amount: int) -> bool:
        """Use stamina for an action. Returns False if not enough stamina."""
        if self.stamina >= amount:
            self.stamina -= amount
            return True
        return False
    
    def use_mana(self, amount: int) -> bool:
        """Use mana for a spell. Returns False if not enough mana."""
        if self.mana >= amount:
            self.mana -= amount
            return True
        return False
    
    def gain_experience(self, amount: int) -> bool:
        """Add experience and check for level up. Returns True if leveled up."""
        self.experience += amount
        exp_needed = self.get_exp_to_next_level()
        
        leveled_up = False
        while self.experience >= exp_needed:
            self.experience -= exp_needed
            self.level_up()
            exp_needed = self.get_exp_to_next_level()
            leveled_up = True
        
        return leveled_up
    
    def get_exp_to_next_level(self) -> int:
        """Calculate experience needed for next level."""
        return int(100 * (self.level ** 1.5))
    
    def level_up(self):
        """Level up the player with stat increases."""
        self.level += 1
        self.max_health += 10
        self.health = self.max_health
        self.max_stamina += 5
        self.stamina = self.max_stamina
        self.max_mana += 5
        self.mana = self.max_mana
        self.skill_points += 2
        
        # Display level up message
        level_up_text = f"""
╔═══════════════════════════════════════════════════════╗
║                    🎉 LEVEL UP! 🎉                     ║
║═══════════════════════════════════════════════════════║
║  You are now Level {self.level}!                              
║                                                       ║
║  ❤️  Max Health: {self.max_health}                           
║  ⚡ Max Stamina: {self.max_stamina}                          
║  ✨ Max Mana: {self.max_mana}                                
║  🎯 Skill Points: +2 (Total: {self.skill_points})           
╚═══════════════════════════════════════════════════════╝
"""
        print_event_box(level_up_text.strip(), EventType.LEVEL_UP)
        log_event(f"Player leveled up to {self.level}")
    
    def add_item(self, item: Item) -> Tuple[bool, str]:
        """Add item to inventory. Returns success and message."""
        if SETTINGS.infinite_inventory:
            if item.stackable:
                for inv_item in self.inventory:
                    if inv_item.name.lower() == item.name.lower():
                        inv_item.quantity += item.quantity
                        self.items_collected += 1
                        return True, f"Added {item.quantity}x {item.name} to inventory."
            self.inventory.append(item)
            self.items_collected += 1
            return True, f"Added {item.name} to inventory."
        
        total_weight = sum(i.weight * i.quantity for i in self.inventory)
        max_weight = 50 + self.skills[SkillType.SURVIVAL] * 5
        
        if total_weight + (item.weight * item.quantity) <= max_weight:
            if item.stackable:
                for inv_item in self.inventory:
                    if inv_item.name.lower() == item.name.lower():
                        inv_item.quantity += item.quantity
                        self.items_collected += 1
                        return True, f"Added {item.quantity}x {item.name} to inventory."
            self.inventory.append(item)
            self.items_collected += 1
            return True, f"Added {item.name} to inventory."
        
        return False, "Your inventory is too full to carry this item."
    
    def remove_item(self, item_name: str, quantity: int = 1) -> bool:
        """Remove item from inventory."""
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                if item.stackable and item.quantity > quantity:
                    item.quantity -= quantity
                    return True
                else:
                    self.inventory.remove(item)
                    return True
        return False
    
    def has_item(self, item_name: str, quantity: int = 1) -> bool:
        """Check if player has an item with specified quantity."""
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                if item.stackable:
                    return item.quantity >= quantity
                return True
        
        # Also check equipped items
        for slot_item in self.equipped.values():
            if slot_item and slot_item.name.lower() == item_name.lower():
                return True
        
        return False
    
    def get_item(self, item_name: str) -> Optional[Item]:
        """Get item from inventory by name."""
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                return item
        return None
    
    def get_item_count(self, item_name: str) -> int:
        """Get total count of an item in inventory."""
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                return item.quantity
        return 0
    
    def equip_item(self, item_name: str) -> str:
        """Equip an item from inventory."""
        item = self.get_item(item_name)
        if not item:
            return colored_text(f"You don't have a {item_name}.", Colors.RED)
        if not item.equippable:
            return colored_text(f"You can't equip {item.name}.", Colors.RED)
        if item.level_requirement > self.level:
            return colored_text(f"You need to be level {item.level_requirement} to equip this.", Colors.RED)
        
        # Determine slot
        slot = None
        if item.item_type == ItemType.WEAPON:
            slot = 'weapon'
        elif item.item_type == ItemType.ARMOR:
            slot = 'armor'
        elif item.item_type == ItemType.LIGHT:
            slot = 'light'
        else:
            slot = 'accessory1' if not self.equipped['accessory1'] else 'accessory2'
        
        # Unequip current item if any
        if self.equipped[slot]:
            old_item = self.equipped[slot]
            self.inventory.append(old_item)
        
        self.equipped[slot] = item
        self.inventory.remove(item)
        
        return colored_text(f"You equipped {item.name}.", Colors.GREEN)
    
    def unequip_item(self, slot: str) -> str:
        """Unequip an item from a slot."""
        if slot not in self.equipped:
            return colored_text(f"Invalid equipment slot: {slot}", Colors.RED)
        if not self.equipped[slot]:
            return colored_text(f"Nothing equipped in {slot} slot.", Colors.YELLOW)
        
        item = self.equipped[slot]
        success, msg = self.add_item(item)
        if success:
            self.equipped[slot] = None
            return colored_text(f"You unequipped {item.name}.", Colors.GREEN)
        return colored_text(f"Can't unequip - inventory is full!", Colors.RED)
    
    def has_light(self) -> bool:
        """Check if player has an active light source."""
        if self.equipped['light'] and self.equipped['light'].durability > 0:
            return True
        for item in self.inventory:
            if item.item_type == ItemType.LIGHT and item.light_radius > 0:
                return True
        return False
    
    def update_status(self, minutes: int = 5):
        """Update player status over time."""
        if not SETTINGS.no_hunger:
            self.hunger = max(0, self.hunger - minutes * 0.3)
        if not SETTINGS.no_thirst:
            self.thirst = max(0, self.thirst - minutes * 0.5)
        
        # Starvation effects
        if self.hunger < 10:
            self.stamina = max(0, self.stamina - 3)
            if self.hunger == 0 and chance(10):
                self.health = max(1, self.health - 1)
        
        # Dehydration effects
        if self.thirst < 10:
            if self.thirst == 0 and chance(20):
                self.health = max(1, self.health - 2)
        
        # Natural stamina regeneration
        if self.hunger > 20 and not self.is_in_combat:
            self.stamina = min(self.max_stamina, self.stamina + minutes // 2)
        
        # Natural mana regeneration
        if self.sanity > 30 and not self.is_in_combat:
            self.mana = min(self.max_mana, self.mana + minutes // 3)
        
        # Process status effects
        expired_effects = []
        for effect, duration in list(self.status_effects.items()):
            self.status_effects[effect] = duration - minutes
            if self.status_effects[effect] <= 0:
                expired_effects.append(effect)
            else:
                self._apply_status_effect(effect)
        
        for effect in expired_effects:
            del self.status_effects[effect]
            slow_print(colored_text(f"The {effect} effect has worn off.", Colors.CYAN))
        
        # Update light source durability
        if self.equipped['light']:
            self.equipped['light'].durability -= minutes
            if self.equipped['light'].durability <= 0:
                slow_print(colored_text(
                    f"Your {self.equipped['light'].name} has burned out!",
                    Colors.YELLOW
                ))
                self.equipped['light'] = None
        
        # Update quest timers
        for quest in self.active_quests:
            quest.update_time(minutes)
            if quest.is_failed and quest.quest_id not in self.failed_quests:
                self.failed_quests.append(quest.quest_id)
                slow_print(colored_text(f"Quest '{quest.name}' has failed!", Colors.RED))
    
    def _apply_status_effect(self, effect: str):
        """Apply ongoing status effect damage/healing."""
        if effect == "poison":
            damage = 2
            self.health = max(1, self.health - damage)
        elif effect == "bleeding":
            damage = 3
            self.health = max(1, self.health - damage)
        elif effect == "burning":
            damage = 4
            self.health = max(1, self.health - damage)
        elif effect == "regenerating":
            self.heal(2)
        elif effect == "frozen":
            self.stamina = max(0, self.stamina - 5)
    
    def add_status_effect(self, effect: str, duration: int):
        """Add a status effect to the player."""
        self.status_effects[effect] = duration
        effect_messages = {
            "poison": "You have been poisoned!",
            "bleeding": "You are bleeding!",
            "burning": "You are on fire!",
            "frozen": "You have been frozen!",
            "stunned": "You have been stunned!",
            "regenerating": "You feel your wounds healing.",
            "strengthened": "You feel stronger!",
            "weakened": "You feel weaker...",
            "protected": "A protective aura surrounds you.",
            "invisible": "You fade from sight."
        }
        msg = effect_messages.get(effect, f"You are affected by {effect}.")
        slow_print(colored_text(msg, Colors.MAGENTA))
    
    def remove_status_effect(self, effect: str):
        """Remove a status effect from the player."""
        if effect in self.status_effects:
            del self.status_effects[effect]
            return True
        return False
    
    def improve_skill(self, skill: SkillType, amount: int = 1) -> bool:
        """Improve a skill and return True if successful."""
        old_level = self.skills[skill]
        self.skills[skill] = min(10, self.skills[skill] + amount)
        if self.skills[skill] > old_level:
            slow_print(colored_text(
                f"Your {skill.value} skill improved to level {self.skills[skill]}!",
                Colors.BOLD_GREEN
            ))
            return True
        return False
    
    def spend_skill_point(self, skill: SkillType) -> str:
        """Spend a skill point to improve a skill."""
        if self.skill_points <= 0:
            return colored_text("You have no skill points to spend.", Colors.RED)
        if self.skills[skill] >= 10:
            return colored_text(f"{skill.value} is already at maximum level.", Colors.YELLOW)
        
        self.skill_points -= 1
        self.skills[skill] += 1
        return colored_text(
            f"Improved {skill.value} to level {self.skills[skill]}! ({self.skill_points} points remaining)",
            Colors.GREEN
        )
    
    def rest(self, hours: int = 8) -> str:
        """Rest to recover health, stamina, and mana."""
        if self.is_in_combat:
            return colored_text("You can't rest during combat!", Colors.RED)
        
        # Calculate recovery
        health_recovered = min(self.max_health - self.health, hours * 5)
        stamina_recovered = min(self.max_stamina - self.stamina, hours * 10)
        mana_recovered = min(self.max_mana - self.mana, hours * 8)
        
        self.health += health_recovered
        self.stamina += stamina_recovered
        self.mana += mana_recovered
        
        # Rest also restores some sanity
        sanity_recovered = min(100 - self.sanity, hours * 5)
        self.sanity += sanity_recovered
        
        # Pass time
        self.update_status(hours * 60)
        
        result = f"""
You rest for {hours} hours.
  ❤️  Health restored: +{health_recovered}
  ⚡ Stamina restored: +{stamina_recovered}
  ✨ Mana restored: +{mana_recovered}
  🧠 Sanity restored: +{sanity_recovered}
"""
        return colored_text(result, Colors.GREEN)
    
    def get_status(self) -> str:
        """Get formatted status display."""
        # Health bar
        health_pct = int((self.health / self.max_health) * 20)
        health_bar = colored_text("█" * health_pct, Colors.RED) + colored_text("░" * (20 - health_pct), Colors.DIM)
        
        # Stamina bar
        stamina_pct = int((self.stamina / self.max_stamina) * 20)
        stamina_bar = colored_text("█" * stamina_pct, Colors.GREEN) + colored_text("░" * (20 - stamina_pct), Colors.DIM)
        
        # Mana bar
        mana_pct = int((self.mana / self.max_mana) * 20)
        mana_bar = colored_text("█" * mana_pct, Colors.BLUE) + colored_text("░" * (20 - mana_pct), Colors.DIM)
        
        # Hunger bar
        hunger_pct = int(self.hunger / 5)
        hunger_color = Colors.GREEN if self.hunger > 50 else (Colors.YELLOW if self.hunger > 20 else Colors.RED)
        hunger_bar = colored_text("█" * hunger_pct, hunger_color) + colored_text("░" * (20 - hunger_pct), Colors.DIM)
        
        # Thirst bar
        thirst_pct = int(self.thirst / 5)
        thirst_color = Colors.CYAN if self.thirst > 50 else (Colors.YELLOW if self.thirst > 20 else Colors.RED)
        thirst_bar = colored_text("█" * thirst_pct, thirst_color) + colored_text("░" * (20 - thirst_pct), Colors.DIM)
        
        # Sanity bar
        sanity_pct = int(self.sanity / 5)
        sanity_color = Colors.MAGENTA if self.sanity > 50 else (Colors.YELLOW if self.sanity > 20 else Colors.RED)
        sanity_bar = colored_text("█" * sanity_pct, sanity_color) + colored_text("░" * (20 - sanity_pct), Colors.DIM)
        
        # Experience bar
        exp_needed = self.get_exp_to_next_level()
        exp_pct = int((self.experience / exp_needed) * 20)
        exp_bar = colored_text("█" * exp_pct, Colors.YELLOW) + colored_text("░" * (20 - exp_pct), Colors.DIM)
        
        status_effects_str = ""
        if self.status_effects:
            effects = ", ".join([f"{e}({d}m)" for e, d in self.status_effects.items()])
            status_effects_str = f"\n║  Status Effects: {effects}"
        
        status = f"""
╔══════════════════════════════════════════════════════════════╗
║  {colored_text(self.name, Colors.BOLD_CYAN)} - Level {self.level}
║  EXP: [{exp_bar}] {self.experience}/{exp_needed}
║══════════════════════════════════════════════════════════════║
║  ❤️  Health:  [{health_bar}] {self.health}/{self.max_health}
║  ⚡ Stamina: [{stamina_bar}] {self.stamina}/{self.max_stamina}
║  ✨ Mana:    [{mana_bar}] {self.mana}/{self.max_mana}
║──────────────────────────────────────────────────────────────║
║  🍖 Hunger:  [{hunger_bar}] {int(self.hunger)}%
║  💧 Thirst:  [{thirst_bar}] {int(self.thirst)}%
║  🧠 Sanity:  [{sanity_bar}] {int(self.sanity)}%{status_effects_str}
║──────────────────────────────────────────────────────────────║
║  💰 Gold: {self.gold}  |  ⚔️ Kills: {self.kills}  |  👣 Steps: {self.steps_taken}
║  🎯 Skill Points: {self.skill_points}  |  🏆 Achievements: {len(self.achievements)}
╚══════════════════════════════════════════════════════════════╝"""
        return status
    
    def get_inventory_display(self) -> str:
        """Get formatted inventory display."""
        if not self.inventory:
            return colored_text("Your inventory is empty.", Colors.DIM)
        
        total_weight = sum(i.weight * i.quantity for i in self.inventory)
        max_weight = 50 + self.skills[SkillType.SURVIVAL] * 5
        
        lines = [colored_text("╔══════════════════════════════════════════════════════════════╗", Colors.YELLOW)]
        lines.append(colored_text("║                        INVENTORY                             ║", Colors.YELLOW))
        lines.append(colored_text("║══════════════════════════════════════════════════════════════║", Colors.YELLOW))
        
        # Group items by type
        items_by_type = {}
        for item in self.inventory:
            type_name = item.item_type.name
            if type_name not in items_by_type:
                items_by_type[type_name] = []
            items_by_type[type_name].append(item)
        
        for type_name, items in items_by_type.items():
            lines.append(colored_text(f"║  ─── {type_name} ───", Colors.CYAN))
            for item in items:
                qty = f" x{item.quantity}" if item.quantity > 1 else ""
                weight = f"({item.weight * item.quantity:.1f}kg)"
                item_line = f"║    • {item.name}{qty} {weight}"
                lines.append(colored_text(item_line, item.get_rarity_color()))
        
        lines.append(colored_text("║──────────────────────────────────────────────────────────────║", Colors.YELLOW))
        
        weight_color = Colors.GREEN if total_weight < max_weight * 0.75 else (
            Colors.YELLOW if total_weight < max_weight else Colors.RED
        )
        lines.append(colored_text(f"║  Weight: {total_weight:.1f}/{max_weight} kg", weight_color))
        lines.append(colored_text("╚══════════════════════════════════════════════════════════════╝", Colors.YELLOW))
        
        return "\n".join(lines)
    
    def get_equipment_display(self) -> str:
        """Get formatted equipment display."""
        lines = [colored_text("╔══════════════════════════════════════════════════════════════╗", Colors.MAGENTA)]
        lines.append(colored_text("║                        EQUIPMENT                             ║", Colors.MAGENTA))
        lines.append(colored_text("║══════════════════════════════════════════════════════════════║", Colors.MAGENTA))
        
        slot_icons = {
            'weapon': '⚔️',
            'armor': '🛡️',
            'helmet': '⛑️',
            'boots': '👢',
            'gloves': '🧤',
            'light': '🔦',
            'accessory1': '💍',
            'accessory2': '📿'
        }
        
        for slot, item in self.equipped.items():
            icon = slot_icons.get(slot, '•')
            if item:
                item_name = colored_text(item.name, item.get_rarity_color())
                if item.durability < item.max_durability:
                    durability_pct = int((item.durability / item.max_durability) * 100)
                    item_name += f" [{durability_pct}%]"
                lines.append(f"║  {icon} {slot.capitalize():12}: {item_name}")
            else:
                lines.append(colored_text(f"║  {icon} {slot.capitalize():12}: (empty)", Colors.DIM))
        
        lines.append(colored_text("║──────────────────────────────────────────────────────────────║", Colors.MAGENTA))
        lines.append(colored_text(f"║  Total Defense: {self.get_defense()}", Colors.CYAN))
        lines.append(colored_text(f"║  Attack Damage: {self.get_attack_damage()[0]} ({self.get_attack_damage()[1]})", Colors.RED))
        lines.append(colored_text("╚══════════════════════════════════════════════════════════════╝", Colors.MAGENTA))
        
        return "\n".join(lines)
    
    def get_skills_display(self) -> str:
        """Get formatted skills display."""
        lines = [colored_text("╔══════════════════════════════════════════════════════════════╗", Colors.CYAN)]
        lines.append(colored_text("║                          SKILLS                              ║", Colors.CYAN))
        lines.append(colored_text("║══════════════════════════════════════════════════════════════║", Colors.CYAN))
        
        for skill, level in self.skills.items():
            bar = colored_text("█" * level, Colors.GREEN) + colored_text("░" * (10 - level), Colors.DIM)
            lines.append(f"║  {skill.value.capitalize():12} [{bar}] {level}/10")
        
        lines.append(colored_text("║──────────────────────────────────────────────────────────────║", Colors.CYAN))
        lines.append(colored_text(f"║  Available Skill Points: {self.skill_points}", Colors.YELLOW))
        lines.append(colored_text("╚══════════════════════════════════════════════════════════════╝", Colors.CYAN))
        
        return "\n".join(lines)
    
    def get_quests_display(self) -> str:
        """Get formatted quests display."""
        if not self.active_quests:
            return colored_text("You have no active quests.", Colors.DIM)
        
        lines = [colored_text("╔══════════════════════════════════════════════════════════════╗", Colors.YELLOW)]
        lines.append(colored_text("║                       ACTIVE QUESTS                          ║", Colors.YELLOW))
        lines.append(colored_text("║══════════════════════════════════════════════════════════════║", Colors.YELLOW))
        
        for quest in self.active_quests:
            if quest.is_failed:
                status = colored_text("[FAILED]", Colors.RED)
            elif quest.is_complete:
                status = colored_text("[COMPLETE]", Colors.GREEN)
            else:
                status = colored_text("[ACTIVE]", Colors.CYAN)
            
            lines.append(f"║  {status} {quest.name}")
            lines.append(f"║    {quest.get_progress()}")
            
            for i, obj in enumerate(quest.objectives):
                if quest.completed_objectives[i]:
                    lines.append(colored_text(f"║      ✓ {obj}", Colors.GREEN))
                else:
                    lines.append(colored_text(f"║      ○ {obj}", Colors.DIM))
            
            if quest.time_limit > 0:
                time_color = Colors.GREEN if quest.time_remaining > 60 else Colors.RED
                lines.append(colored_text(f"║    Time remaining: {format_time(quest.time_remaining)}", time_color))
            
            lines.append(colored_text("║──────────────────────────────────────────────────────────────║", Colors.YELLOW))
        
        lines[-1] = colored_text("╚══════════════════════════════════════════════════════════════╝", Colors.YELLOW)
        
        return "\n".join(lines)
    
    def to_dict(self) -> Dict:
        """Convert player to dictionary for saving."""
        return {
            'name': self.name,
            'health': self.health,
            'max_health': self.max_health,
            'stamina': self.stamina,
            'max_stamina': self.max_stamina,
            'mana': self.mana,
            'max_mana': self.max_mana,
            'hunger': self.hunger,
            'thirst': self.thirst,
            'sanity': self.sanity,
            'experience': self.experience,
            'level': self.level,
            'skill_points': self.skill_points,
            'inventory': [item.to_dict() for item in self.inventory],
            'equipped': {k: v.to_dict() if v else None for k, v in self.equipped.items()},
            'skills': {k.name: v for k, v in self.skills.items()},
            'current_location': self.current_location,
            'previous_location': self.previous_location,
            'discovered_locations': self.discovered_locations,
            'completed_quests': self.completed_quests,
            'failed_quests': self.failed_quests,
            'known_recipes': self.known_recipes,
            'status_effects': self.status_effects,
            'notes': self.notes,
            'play_time': self.play_time,
            'deaths': self.deaths,
            'kills': self.kills,
            'boss_kills': self.boss_kills,
            'steps_taken': self.steps_taken,
            'items_collected': self.items_collected,
            'items_crafted': self.items_crafted,
            'secrets_found': self.secrets_found,
            'treasures_found': self.treasures_found,
            'achievements': self.achievements,
            'companions': self.companions,
            'gold': self.gold,
            'reputation': self.reputation,
            'kill_count': self.kill_count,
            'total_damage_dealt': self.total_damage_dealt,
            'total_damage_taken': self.total_damage_taken,
            'total_healing': self.total_healing
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Player':
        """Create player from dictionary."""
        player = Player(data.get('name', 'Traveler'))
        player.health = data.get('health', 100)
        player.max_health = data.get('max_health', 100)
        player.stamina = data.get('stamina', 100)
        player.max_stamina = data.get('max_stamina', 100)
        player.mana = data.get('mana', 50)
        player.max_mana = data.get('max_mana', 50)
        player.hunger = data.get('hunger', 100)
        player.thirst = data.get('thirst', 100)
        player.sanity = data.get('sanity', 100)
        player.experience = data.get('experience', 0)
        player.level = data.get('level', 1)
        player.skill_points = data.get('skill_points', 0)
        player.inventory = [Item.from_dict(i) for i in data.get('inventory', [])]
        player.equipped = {
            k: Item.from_dict(v) if v else None 
            for k, v in data.get('equipped', {}).items()
        }
        player.skills = {
            SkillType[k]: v for k, v in data.get('skills', {}).items()
        }
        player.current_location = data.get('current_location', 'clearing')
        player.previous_location = data.get('previous_location', '')
        player.discovered_locations = data.get('discovered_locations', ['clearing'])
        player.completed_quests = data.get('completed_quests', [])
        player.failed_quests = data.get('failed_quests', [])
        player.known_recipes = data.get('known_recipes', ['torch', 'bandage', 'rope'])
        player.status_effects = data.get('status_effects', {})
        player.notes = data.get('notes', [])
        player.play_time = data.get('play_time', 0)
        player.deaths = data.get('deaths', 0)
        player.kills = data.get('kills', 0)
        player.boss_kills = data.get('boss_kills', 0)
        player.steps_taken = data.get('steps_taken', 0)
        player.items_collected = data.get('items_collected', 0)
        player.items_crafted = data.get('items_crafted', 0)
        player.secrets_found = data.get('secrets_found', 0)
        player.treasures_found = data.get('treasures_found', 0)
        player.achievements = data.get('achievements', [])
        player.companions = data.get('companions', [])
        player.gold = data.get('gold', 0)
        player.reputation = data.get('reputation', {})
        player.kill_count = data.get('kill_count', {})
        player.total_damage_dealt = data.get('total_damage_dealt', 0)
        player.total_damage_taken = data.get('total_damage_taken', 0)
        player.total_healing = data.get('total_healing', 0)
        return player


