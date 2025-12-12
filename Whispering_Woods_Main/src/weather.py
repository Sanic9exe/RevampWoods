"""Time and weather system."""

import random
from datetime import datetime, timedelta
from typing import Optional, Tuple

from .utils import Weather, TimeOfDay
from .colors import Colors

# ============================================================================
# TIME AND WEATHER SYSTEM
# ============================================================================

class TimeWeatherSystem:
    """Manages game time and weather."""
    
    def __init__(self):
        self.game_minutes = 480  # Start at 8:00 AM
        self.current_weather = Weather.CLEAR
        self.weather_duration = 60
        self.day_count = 1
    
    def advance_time(self, minutes: int):
        """Advance game time by specified minutes."""
        self.game_minutes += minutes
        
        # Handle day rollover
        while self.game_minutes >= 1440:  # 24 hours
            self.game_minutes -= 1440
            self.day_count += 1
        
        # Update weather
        self.weather_duration -= minutes
        if self.weather_duration <= 0:
            self._change_weather()
    
    def _change_weather(self):
        """Randomly change the weather."""
        weather_weights = {
            Weather.CLEAR: 40,
            Weather.FOGGY: 15,
            Weather.RAINY: 15,
            Weather.MISTY: 15,
            Weather.WINDY: 10,
            Weather.STORMY: 5
        }
        
        roll = random.randint(1, 100)
        cumulative = 0
        for weather, weight in weather_weights.items():
            cumulative += weight
            if roll <= cumulative:
                self.current_weather = weather
                break
        
        self.weather_duration = random.randint(30, 180)
    
    def get_time_of_day(self) -> TimeOfDay:
        """Get current time of day period."""
        hour = self.game_minutes // 60
        
        if 5 <= hour < 7:
            return TimeOfDay.DAWN
        elif 7 <= hour < 12:
            return TimeOfDay.MORNING
        elif 12 <= hour < 14:
            return TimeOfDay.NOON
        elif 14 <= hour < 17:
            return TimeOfDay.AFTERNOON
        elif 17 <= hour < 19:
            return TimeOfDay.DUSK
        elif 19 <= hour < 22:
            return TimeOfDay.EVENING
        elif 22 <= hour or hour < 1:
            return TimeOfDay.NIGHT
        else:
            return TimeOfDay.MIDNIGHT
    
    def get_time_string(self) -> str:
        """Get formatted time string."""
        hours = self.game_minutes // 60
        minutes = self.game_minutes % 60
        period = "AM" if hours < 12 else "PM"
        display_hour = hours if hours <= 12 else hours - 12
        if display_hour == 0:
            display_hour = 12
        return f"{display_hour}:{minutes:02d} {period}"
    
    def get_status_display(self) -> str:
        """Get formatted time and weather display."""
        time_of_day = self.get_time_of_day()
        
        weather_icons = {
            Weather.CLEAR: "☀️",
            Weather.FOGGY: "🌫️",
            Weather.RAINY: "🌧️",
            Weather.STORMY: "⛈️",
            Weather.MISTY: "🌁",
            Weather.SNOWY: "❄️",
            Weather.WINDY: "💨"
        }
        
        time_icons = {
            TimeOfDay.DAWN: "🌅",
            TimeOfDay.MORNING: "🌄",
            TimeOfDay.NOON: "☀️",
            TimeOfDay.AFTERNOON: "🌤️",
            TimeOfDay.DUSK: "🌆",
            TimeOfDay.EVENING: "🌇",
            TimeOfDay.NIGHT: "🌙",
            TimeOfDay.MIDNIGHT: "🌑"
        }
        
        return f"""
╭────────────────────────────────────╮
│ {time_icons.get(time_of_day, '🕐')} Day {self.day_count}, {self.get_time_string()}
│ {weather_icons.get(self.current_weather, '🌤️')} Weather: {self.current_weather.value.capitalize()}
│ 🕐 Period: {time_of_day.value.capitalize()}
╰────────────────────────────────────╯"""



