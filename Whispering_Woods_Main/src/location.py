"""Location class for game areas."""

from typing import Dict, List, Optional, Any
import random

from .colors import Colors
from .models import Route
from .utils import slow_print

# ============================================================================
# LOCATION CLASS WITH NUMBERED ROUTES
# ============================================================================

@dataclass
class Location:
    """Represents a location in the game world with numbered routes."""
    location_id: str
    name: str
    description: str
    long_description: str
    routes: List[Route] = field(default_factory=list)
    items: List[Item] = field(default_factory=list)
    creatures: List[Creature] = field(default_factory=list)
    features: List[str] = field(default_factory=list)
    visited: bool = False
    visit_count: int = 0
    dark: bool = False
    dangerous: bool = False
    danger_level: int = 0
    water: bool = False
    climbable: bool = False
    swimmable: bool = False
    events: List[str] = field(default_factory=list)
    ambient_sounds: List[str] = field(default_factory=list)
    required_item: Optional[str] = None
    blocked_message: str = ""
    special_actions: List[str] = field(default_factory=list)
    discovered_secrets: List[str] = field(default_factory=list)
    treasure_found: bool = False
    rest_allowed: bool = True
    shop_available: bool = False
    save_point: bool = False
    
    def get_description(self, time_of_day: TimeOfDay, weather: Weather, 
                       has_light: bool = True, perception_level: int = 1) -> str:
        """Get location description based on conditions."""
        if self.dark and not has_light:
            return colored_text(
                "It's too dark to see anything. You need a light source to proceed safely.",
                Colors.DIM
            )
        
        # Use long description on first visit, short description after
        desc = self.long_description if not self.visited else self.description
        
        # Add time-based descriptions
        time_descriptions = {
            TimeOfDay.DAWN: "\nThe first light of dawn paints the sky in soft pinks and oranges.",
            TimeOfDay.MORNING: "\nMorning sunlight filters through the trees.",
            TimeOfDay.NOON: "\nThe sun is high overhead, casting short shadows.",
            TimeOfDay.AFTERNOON: "\nThe afternoon sun casts long golden rays.",
            TimeOfDay.DUSK: "\nThe sky is painted in shades of orange and purple as the sun sets.",
            TimeOfDay.EVENING: "\nTwilight settles over the forest.",
            TimeOfDay.NIGHT: "\nDarkness blankets everything, with only starlight to guide you.",
            TimeOfDay.MIDNIGHT: "\nThe deepest hour of night surrounds you in shadow."
        }
        desc += time_descriptions.get(time_of_day, "")
        
        # Add weather descriptions
        weather_descriptions = {
            Weather.RAINY: "\nRain patters steadily on the leaves above, creating a constant rhythm.",
            Weather.FOGGY: "\nA thick fog hangs in the air, limiting your visibility.",
            Weather.STORMY: "\nThunder rumbles ominously and lightning flashes in the distance.",
            Weather.MISTY: "\nA light mist swirls around your feet.",
            Weather.SNOWY: "\nSnowflakes drift lazily down from the grey sky.",
            Weather.WINDY: "\nA strong wind rustles through the trees.",
            Weather.CLEAR: ""
        }
        desc += weather_descriptions.get(weather, "")
        
        # Add ambient sounds based on perception
        if self.ambient_sounds and perception_level >= 2:
            desc += f"\n\nYou hear {random.choice(self.ambient_sounds)}."
        
        # High perception reveals secrets
        if perception_level >= 5 and self.features:
            hidden_detail = random.choice(self.features)
            desc += f"\n\nYour keen eyes notice: {hidden_detail}"
        
        return desc
    
    def get_routes_display(self, player: 'Player' = None) -> str:
        """Get formatted display of available routes."""
        if not self.routes:
            return colored_text("There are no obvious paths from here.", Colors.DIM)
        
        lines = [colored_text("\n═══ AVAILABLE PATHS ═══", Colors.BOLD_CYAN)]
        
        for route in self.routes:
            if route.hidden and player:
                if player.skills.get(SkillType.PERCEPTION, 1) < 3:
                    continue
            
            if not route.visible:
                continue
            
            # Check if route is accessible
            accessible = True
            blocked_reason = ""
            if player:
                accessible, blocked_reason = route.is_accessible(player)
            
            # Build route display
            danger_indicator = ""
            if route.danger_level > 0:
                danger_indicator = colored_text(f" [Danger: {'!' * min(route.danger_level, 5)}]", Colors.RED)
            
            if accessible:
                route_text = f"  [{route.number}] {route.description}{danger_indicator}"
                lines.append(colored_text(route_text, Colors.GREEN))
            else:
                route_text = f"  [{route.number}] {route.description} (Blocked: {blocked_reason})"
                lines.append(colored_text(route_text, Colors.RED))
        
        lines.append(colored_text("═" * 24, Colors.BOLD_CYAN))
        return "\n".join(lines)
    
    def get_route_by_number(self, number: int) -> Optional[Route]:
        """Get a route by its number."""
        for route in self.routes:
            if route.number == number:
                return route
        return None
    
    def add_route(self, destination: str, description: str, **kwargs):
        """Add a new route to this location."""
        next_number = len(self.routes) + 1
        route = Route(
            number=next_number,
            destination=destination,
            description=description,
            **kwargs
        )
        self.routes.append(route)
    
    def get_items_display(self) -> str:
        """Get formatted display of items in location."""
        if not self.items:
            return ""
        
        lines = [colored_text("\n╭─── Items Here ───╮", Colors.YELLOW)]
        for item in self.items:
            qty = f" x{item.quantity}" if item.quantity > 1 else ""
            lines.append(colored_text(f"│ • {item.name}{qty}", item.get_rarity_color()))
        lines.append(colored_text("╰──────────────────╯", Colors.YELLOW))
        return "\n".join(lines)
    
    def get_creatures_display(self) -> str:
        """Get formatted display of creatures in location."""
        alive_creatures = [c for c in self.creatures if c.alive]
        if not alive_creatures:
            return ""
        
        lines = [colored_text("\n╭─── Creatures Present ───╮", Colors.MAGENTA)]
        for creature in alive_creatures:
            health_pct = int((creature.health / creature.max_health) * 100)
            health_bar = "█" * (health_pct // 10) + "░" * (10 - health_pct // 10)
            
            if creature.hostile:
                lines.append(colored_text(
                    f"│ ⚠ {creature.name} [{health_bar}] {health_pct}%",
                    Colors.RED
                ))
            else:
                lines.append(colored_text(
                    f"│ • {creature.name} [{health_bar}] {health_pct}%",
                    Colors.GREEN
                ))
        lines.append(colored_text("╰─────────────────────────╯", Colors.MAGENTA))
        return "\n".join(lines)


