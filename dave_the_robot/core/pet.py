"""Core virtual pet state and behavior."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from dave_the_robot.config import STAT_BOUNDS

PetAction = Literal["feed", "play", "sleep"]


@dataclass
class PetState:
    hunger: int = 30
    happiness: int = 70
    energy: int = 70


class VirtualPet:
    """Encapsulates the pet's internal state and transitions."""

    def __init__(self) -> None:
        self.state = PetState()

    def apply_action(self, action: PetAction) -> None:
        if action == "feed":
            self.state.hunger -= 20
            self.state.happiness += 8
            self.state.energy += 2
        elif action == "play":
            self.state.hunger += 10
            self.state.happiness += 18
            self.state.energy -= 14
        elif action == "sleep":
            self.state.energy += 25
            self.state.hunger += 8
            self.state.happiness += 3
        self._clamp_all()

    def time_step(self) -> None:
        """Natural decay that happens every few seconds."""
        self.state.hunger += 4
        self.state.energy -= 3

        if self.state.hunger > 70:
            self.state.happiness -= 5
        else:
            self.state.happiness -= 1

        self._clamp_all()

    def _clamp_all(self) -> None:
        self.state.hunger = self._clamp(self.state.hunger)
        self.state.happiness = self._clamp(self.state.happiness)
        self.state.energy = self._clamp(self.state.energy)

    @staticmethod
    def _clamp(value: int) -> int:
        return max(STAT_BOUNDS.min_value, min(value, STAT_BOUNDS.max_value))
