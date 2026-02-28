"""Configuration values used by platform adapters and game defaults."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

SCREEN_SIZE = 240
TICK_SECONDS = 1.0
STATE_UPDATE_SECONDS = 5.0

# Default pin mapping for Waveshare 1.3" LCD HAT style button layout.
# Adjust these values for your exact board revision.
DEFAULT_PI_BUTTON_PINS: Dict[str, int] = {
    "feed": 5,
    "play": 6,
    "sleep": 16,
    "up": 17,
    "down": 22,
    "left": 23,
    "right": 27,
    "center": 24,
}

# Keyboard fallbacks for PC mode (pygame key names).
DEFAULT_PC_KEYS: Dict[str, int] = {
    "feed": 102,  # f
    "play": 112,  # p
    "sleep": 115,  # s
}


@dataclass(frozen=True)
class StatBounds:
    min_value: int = 0
    max_value: int = 100


STAT_BOUNDS = StatBounds()
