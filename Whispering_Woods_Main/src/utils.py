"""Utility functions, constants, and enumerations."""

import time
import sys
import random
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple, Any

from .colors import Colors

# ============================================================================
# CONSTANTS AND CONFIGURATION
# ============================================================================

GAME_VERSION = "2.0.0"
ADMIN_PASSWORD = "forestmaster2024"
SAVE_FILE = "whispering_woods_save.json"
CONFIG_FILE = "game_config.json"
LOG_FILE = "game_log.txt"

GAME_TITLE = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     ██╗      ██████╗ ███████╗████████╗    ██╗███╗   ██╗                       ║
║     ██║     ██╔═══██╗██╔════╝╚══██╔══╝    ██║████╗  ██║                       ║
║     ██║     ██║   ██║███████╗   ██║       ██║██╔██╗ ██║                       ║
║     ██║     ██║   ██║╚════██║   ██║       ██║██║╚██╗██║                       ║
║     ███████╗╚██████╔╝███████║   ██║       ██║██║ ╚████║                       ║
║     ╚══════╝ ╚═════╝ ╚══════╝   ╚═╝       ╚═╝╚═╝  ╚═══╝                       ║
║                                                                               ║
║          ████████╗██╗  ██╗███████╗                                            ║
║          ╚══██╔══╝██║  ██║██╔════╝                                            ║
║             ██║   ███████║█████╗                                              ║
║             ██║   ██╔══██║██╔══╝                                              ║
║             ██║   ██║  ██║███████╗                                            ║
║             ╚═╝   ╚═╝  ╚═╝╚══════╝                                            ║
║                                                                               ║
║  ██╗    ██╗██╗  ██╗██╗███████╗██████╗ ███████╗██████╗ ██╗███╗   ██╗ ██████╗   ║
║  ██║    ██║██║  ██║██║██╔════╝██╔══██╗██╔════╝██╔══██╗██║████╗  ██║██╔════╝   ║
║  ██║ █╗ ██║███████║██║███████╗██████╔╝█████╗  ██████╔╝██║██╔██╗ ██║██║  ███╗  ║
║  ██║███╗██║██╔══██║██║╚════██║██╔═══╝ ██╔══╝  ██╔══██╗██║██║╚██╗██║██║   ██║  ║
║  ╚███╔███╔╝██║  ██║██║███████║██║     ███████╗██║  ██║██║██║ ╚████║╚██████╔╝  ║
║   ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝   ║
║                                                                               ║
║              ██╗    ██╗ ██████╗  ██████╗ ██████╗ ███████╗                     ║
║              ██║    ██║██╔═══██╗██╔═══██╗██╔══██╗██╔════╝                     ║
║              ██║ █╗ ██║██║   ██║██║   ██║██║  ██║███████╗                     ║
║              ██║███╗██║██║   ██║██║   ██║██║  ██║╚════██║                     ║
║              ╚███╔███╔╝╚██████╔╝╚██████╔╝██████╔╝███████║                     ║
║               ╚══╝╚══╝  ╚═════╝  ╚═════╝ ╚═════╝ ╚══════╝                     ║
║                                                                               ║
║                           Version 2.0 - Complete Revamp                       ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

# ============================================================================
# ENUMERATIONS
# ============================================================================

class ItemType(Enum):
    WEAPON = auto()
    TOOL = auto()
    CONSUMABLE = auto()
    KEY = auto()
    QUEST = auto()
    MATERIAL = auto()
    ARMOR = auto()
    LIGHT = auto()
    CONTAINER = auto()
    TREASURE = auto()
    BOOK = auto()
    MAGIC = auto()

class CreatureType(Enum):
    PASSIVE = auto()
    HOSTILE = auto()
    NEUTRAL = auto()
    BOSS = auto()
    NPC = auto()
    MERCHANT = auto()

class Weather(Enum):
    CLEAR = "clear"
    FOGGY = "foggy"
    RAINY = "rainy"
    STORMY = "stormy"
    MISTY = "misty"
    SNOWY = "snowy"
    WINDY = "windy"

class TimeOfDay(Enum):
    DAWN = "dawn"
    MORNING = "morning"
    NOON = "noon"
    AFTERNOON = "afternoon"
    DUSK = "dusk"
    EVENING = "evening"
    NIGHT = "night"
    MIDNIGHT = "midnight"

class SkillType(Enum):
    SURVIVAL = "survival"
    COMBAT = "combat"
    STEALTH = "stealth"
    PERCEPTION = "perception"
    CRAFTING = "crafting"
    FORAGING = "foraging"
    CLIMBING = "climbing"
    SWIMMING = "swimming"
    LOCKPICKING = "lockpicking"
    PERSUASION = "persuasion"
    MAGIC = "magic"
    ARCHERY = "archery"


class DifficultyMode(Enum):
    """Difficulty modes for the game."""
    STORY = auto()      # Easy mode - focus on story
    NORMAL = auto()     # Balanced gameplay
    HARD = auto()       # Challenging experience
    NIGHTMARE = auto()  # Extreme difficulty with permadeath

class StatusEffect(Enum):
    POISON = "poison"
    BLEEDING = "bleeding"
    BURNING = "burning"
    FROZEN = "frozen"
    STUNNED = "stunned"
    BLESSED = "blessed"
    CURSED = "cursed"
    INVISIBLE = "invisible"
    REGENERATING = "regenerating"
    WEAKENED = "weakened"
    STRENGTHENED = "strengthened"
    PROTECTED = "protected"

class EventType(Enum):
    COMBAT = auto()
    DISCOVERY = auto()
    QUEST = auto()
    TREASURE = auto()
    DANGER = auto()
    STORY = auto()
    ACHIEVEMENT = auto()
    LEVEL_UP = auto()
    DEATH = auto()
    BOSS = auto()



# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def slow_print(text: str, delay: float = None, newline: bool = True, color: str = None):
    """Print text character by character for dramatic effect."""
    if delay is None:
        delay = SETTINGS.text_speed
    
    if color and SETTINGS.enable_colors:
        text = f"{color}{text}{Colors.RESET}"
    
    for char in text:
        print(char, end='', flush=True)
        if delay > 0:
            time.sleep(delay)
    if newline:
        print()

def slow_print_lines(lines: List[str], delay: float = None, color: str = None):
    """Print multiple lines with slow typing effect."""
    for line in lines:
        slow_print(line, delay, color=color)

def instant_print(text: str, color: str = None, newline: bool = True):
    """Print text instantly with optional color."""
    if color and SETTINGS.enable_colors:
        text = f"{color}{text}{Colors.RESET}"
    if newline:
        print(text)
    else:
        print(text, end='', flush=True)

def colored_text(text: str, color: str) -> str:
    """Return text wrapped in color codes."""
    if SETTINGS.enable_colors:
        return f"{color}{text}{Colors.RESET}"
    return text

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_separator(char: str = "═", length: int = 78, color: str = None):
    """Print a separator line."""
    line = char * length
    slow_print(line, delay=0.001, color=color)

def print_box(text: str, width: int = 76, color: str = None, title: str = None):
    """Print text in a decorative box."""
    lines = text.split('\n')
    border_color = color if color else Colors.CYAN
    
    slow_print("╔" + "═" * width + "╗", delay=0.001, color=border_color)
    
    if title:
        title_line = f"║ {title.center(width - 2)} ║"
        slow_print(title_line, delay=0.001, color=border_color)
        slow_print("║" + "─" * width + "║", delay=0.001, color=border_color)
    
    for line in lines:
        padding = width - len(line) - 1
        slow_print(f"║ {line}" + " " * padding + "║", delay=0.002, color=border_color)
    
    slow_print("╚" + "═" * width + "╝", delay=0.001, color=border_color)

def print_event_box(text: str, event_type: EventType, width: int = 76):
    """Print a colored event box based on event type."""
    color_map = {
        EventType.COMBAT: Colors.RED,
        EventType.DISCOVERY: Colors.CYAN,
        EventType.QUEST: Colors.YELLOW,
        EventType.TREASURE: Colors.BOLD_YELLOW,
        EventType.DANGER: Colors.BOLD_RED,
        EventType.STORY: Colors.MAGENTA,
        EventType.ACHIEVEMENT: Colors.BOLD_GREEN,
        EventType.LEVEL_UP: Colors.BOLD_CYAN,
        EventType.DEATH: Colors.BOLD_RED,
        EventType.BOSS: Colors.BOLD_MAGENTA
    }
    
    title_map = {
        EventType.COMBAT: "⚔️  COMBAT",
        EventType.DISCOVERY: "🔍 DISCOVERY",
        EventType.QUEST: "📜 QUEST",
        EventType.TREASURE: "💎 TREASURE",
        EventType.DANGER: "⚠️  DANGER",
        EventType.STORY: "📖 STORY",
        EventType.ACHIEVEMENT: "🏆 ACHIEVEMENT",
        EventType.LEVEL_UP: "⬆️  LEVEL UP",
        EventType.DEATH: "💀 DEATH",
        EventType.BOSS: "👹 BOSS ENCOUNTER"
    }
    
    color = color_map.get(event_type, Colors.WHITE)
    title = title_map.get(event_type, "EVENT")
    
    print_box(text, width, color, title)

def get_input(prompt: str = "> ", color: str = Colors.GREEN) -> str:
    """Get user input with a colored prompt."""
    try:
        if SETTINGS.enable_colors:
            user_input = input(f"{color}{prompt}{Colors.RESET}").strip().lower()
        else:
            user_input = input(prompt).strip().lower()
        return user_input
    except EOFError:
        return "quit"
    except KeyboardInterrupt:
        print()
        return "quit"

def roll_dice(sides: int = 20, count: int = 1, modifier: int = 0) -> int:
    """Roll dice with optional count and modifier."""
    total = sum(random.randint(1, sides) for _ in range(count))
    return total + modifier

def chance(percentage: int) -> bool:
    """Return True with given percentage chance."""
    return random.randint(1, 100) <= percentage

def format_time(minutes: int) -> str:
    """Format minutes into hours and minutes string."""
    hours = minutes // 60
    mins = minutes % 60
    if hours > 0:
        return f"{hours}h {mins}m"
    return f"{mins}m"

def log_event(event: str):
    """Log an event to the log file."""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, 'a') as f:
            f.write(f"[{timestamp}] {event}\n")
    except Exception:
        pass

def hash_password(password: str) -> str:
    """Hash a password for comparison."""
    return hashlib.sha256(password.encode()).hexdigest()


