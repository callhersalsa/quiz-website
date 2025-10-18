"""
weather_icons.py
Mapping of WMO weather codes to OpenWeather icons.
"""

from collections import Counter

# Map WMO weather codes → OpenWeather icons
icon_map = {
    0: ("01d", "01n"),  # Clear sky
    1: ("02d", "02n"),  # Mainly clear
    2: ("03d", "03n"),  # Partly cloudy
    3: ("04d", "04n"),  # Overcast
    45: ("50d", "50n"), # Fog
    48: ("50d", "50n"),
    51: ("09d", "09n"), # Drizzle
    53: ("09d", "09n"),
    55: ("09d", "09n"),
    61: ("10d", "10n"), # Rain
    63: ("10d", "10n"),
    65: ("10d", "10n"),
    80: ("09d", "09n"), # Showers
    81: ("09d", "09n"),
    82: ("09d", "09n"),
    95: ("11d", "11n"), # Thunderstorm
    96: ("11d", "11n"),
    99: ("11d", "11n")
}

def icon_for(codes, is_day=True):
    """Return the most common weather icon for the given codes."""
    if not codes:
        return "01d" if is_day else "01n"
    code = Counter(codes).most_common(1)[0][0]
    return icon_map.get(code, ("01d", "01n"))[0 if is_day else 1]