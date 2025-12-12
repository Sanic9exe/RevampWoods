#!/usr/bin/env python3
"""
LOST IN THE WHISPERING WOODS
A Text-Based Adventure Game - COMPLETE REVAMP
By Claude

You wake up in a mysterious forest with no memory of how you got there.
Your goal: Find your way out before the forest claims you forever.

Features:
- Numbered route selection (1-8 options)
- Slow-typed text for immersion
- Colored text for special events
- Extensive admin panel
- 50+ unique locations
- Complex quest system
- Crafting system
- Combat system
- Day/night cycle
- Weather system
- Achievement system
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import all necessary components
from src.game_engine import Game
from src.utils import log_event

def main():
    """Main entry point for the game."""
    try:
        game = Game()
        game.start()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Goodbye!")
    except Exception as e:
        print(f"\n\nAn error occurred: {e}")
        log_event(f"Error: {e}")
        raise

if __name__ == "__main__":
    main()
