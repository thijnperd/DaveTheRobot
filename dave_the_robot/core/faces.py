"""Face definitions and selection logic."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from dave_the_robot.core.pet import PetState
from dave_the_robot.platform.base import Color, Display

FaceCondition = Callable[[PetState], bool]

ASSET_DIR = Path(__file__).resolve().parents[2] / "assets" / "faces"

BG: Color = (240, 242, 245)
BLACK: Color = (20, 20, 20)
BLUE: Color = (58, 134, 255)
RED: Color = (230, 57, 70)


@dataclass
class Face:
    face_id: str
    condition: FaceCondition
    render: Callable[[Display, PetState], None]
    purpose: str


def _draw_base_head(display: Display) -> None:
    display.clear(BG)
    display.draw_circle(BLACK, (120, 120), 88, width=3)


def _draw_fallback_happy(display: Display, _: PetState) -> None:
    _draw_base_head(display)
    display.draw_circle(BLACK, (88, 100), 10)
    display.draw_circle(BLACK, (152, 100), 10)
    display.draw_line(BLACK, (80, 148), (160, 148), width=3)
    display.draw_line(BLACK, (80, 148), (98, 165), width=3)
    display.draw_line(BLACK, (160, 148), (142, 165), width=3)


def _draw_fallback_calm(display: Display, _: PetState) -> None:
    _draw_base_head(display)
    display.draw_line(BLACK, (74, 96), (102, 104), width=4)
    display.draw_line(BLACK, (138, 104), (166, 96), width=4)
    display.draw_line(BLACK, (90, 156), (150, 156), width=3)


def _draw_fallback_angry(display: Display, _: PetState) -> None:
    _draw_base_head(display)
    display.draw_line(BLACK, (72, 90), (102, 102), width=4)
    display.draw_line(BLACK, (138, 102), (168, 90), width=4)
    display.draw_circle(BLACK, (88, 105), 8)
    display.draw_circle(BLACK, (152, 105), 8)
    display.draw_rect(BLACK, (92, 146, 56, 22), width=3)


def _draw_fallback_sad(display: Display, _: PetState) -> None:
    _draw_base_head(display)
    display.draw_circle(BLACK, (88, 104), 9)
    display.draw_circle(BLACK, (152, 104), 9)
    display.draw_line(BLACK, (88, 164), (152, 164), width=3)
    display.draw_line(BLACK, (88, 164), (102, 150), width=3)
    display.draw_line(BLACK, (152, 164), (138, 150), width=3)


def _render_sprite_or_fallback(
    display: Display,
    filename: str,
    fallback: Callable[[Display, PetState], None],
    state: PetState,
) -> None:
    image_path = ASSET_DIR / filename
    if image_path.exists():
        display.clear(BG)
        display.draw_image(str(image_path), (0, 0), (240, 240))
        return
    fallback(display, state)


def render_excited(display: Display, state: PetState) -> None:
    """Big-eyed grin: used when happiness is high and needs are under control."""
    _render_sprite_or_fallback(display, "excited.png", _draw_fallback_happy, state)
    display.draw_text("Let's play!", (72, 210), BLUE, size=14)


def render_calm(display: Display, state: PetState) -> None:
    """Relaxed closed-eyes smile: used when energy is healthy and mood is stable."""
    _render_sprite_or_fallback(display, "calm.png", _draw_fallback_calm, state)
    display.draw_text("All good", (88, 210), BLUE, size=14)


def render_angry(display: Display, state: PetState) -> None:
    """Frustrated/angry face: used when neglect pushes hunger very high."""
    _render_sprite_or_fallback(display, "angry.png", _draw_fallback_angry, state)
    display.draw_text("Feed me now!", (70, 210), RED, size=14)


def render_sad(display: Display, state: PetState) -> None:
    """Crying/sad face: used when happiness drops from lack of attention."""
    _render_sprite_or_fallback(display, "sad.png", _draw_fallback_sad, state)
    display.draw_text("I feel lonely", (68, 210), RED, size=14)


DEFAULT_FACES: list[Face] = [
    Face(
        "angry",
        lambda s: s.hunger >= 80,
        render_angry,
        "Critical hunger warning so feeding gets top priority.",
    ),
    Face(
        "sad",
        lambda s: s.happiness <= 30,
        render_sad,
        "Low-happiness signal that encourages play or attention.",
    ),
    Face(
        "calm",
        lambda s: s.energy >= 65 and s.hunger <= 60,
        render_calm,
        "Stable/healthy baseline expression when needs are balanced.",
    ),
    Face(
        "excited",
        lambda s: True,
        render_excited,
        "Default upbeat expression for normal gameplay.",
    ),
]


class FaceEngine:
    def __init__(self, faces: list[Face] | None = None) -> None:
        self.faces = faces or DEFAULT_FACES

    def select_face(self, state: PetState) -> Face:
        for face in self.faces:
            if face.condition(state):
                return face
        return self.faces[-1]
