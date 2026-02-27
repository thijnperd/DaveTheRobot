"""Face definitions and selection logic."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from dave_the_robot.core.pet import PetState
from dave_the_robot.platform.base import Color, Display

FaceCondition = Callable[[PetState], bool]

BG: Color = (240, 242, 245)
BLACK: Color = (20, 20, 20)
BLUE: Color = (58, 134, 255)
RED: Color = (230, 57, 70)


@dataclass
class Face:
    face_id: str
    condition: FaceCondition
    render: Callable[[Display, PetState], None]


def _draw_base_head(display: Display) -> None:
    display.clear(BG)
    display.draw_circle(BLACK, (120, 120), 88, width=3)


def render_happy(display: Display, state: PetState) -> None:
    _draw_base_head(display)
    display.draw_circle(BLACK, (88, 100), 10)
    display.draw_circle(BLACK, (152, 100), 10)
    display.draw_circle((255, 255, 255), (92, 96), 3)
    display.draw_circle((255, 255, 255), (156, 96), 3)
    display.draw_line(BLACK, (80, 148), (160, 148), width=3)
    display.draw_line(BLACK, (80, 148), (98, 165), width=3)
    display.draw_line(BLACK, (160, 148), (142, 165), width=3)
    display.draw_text("Feeling great!", (62, 198), BLUE, size=16)


def render_hungry(display: Display, state: PetState) -> None:
    _draw_base_head(display)
    display.draw_circle(BLACK, (88, 102), 9)
    display.draw_circle(BLACK, (152, 102), 9)
    display.draw_rect(BLACK, (85, 146, 70, 24), width=3)
    display.draw_text("Need food", (72, 198), RED, size=16)


def render_sleepy(display: Display, state: PetState) -> None:
    _draw_base_head(display)
    display.draw_line(BLACK, (74, 96), (102, 104), width=4)
    display.draw_line(BLACK, (138, 104), (166, 96), width=4)
    display.draw_circle(BLACK, (120, 156), 20, width=3)
    display.draw_text("ZzZ", (100, 62), BLUE, size=18)
    display.draw_text("So sleepy", (76, 198), BLUE, size=16)


def render_sad(display: Display, state: PetState) -> None:
    _draw_base_head(display)
    display.draw_circle(BLACK, (88, 104), 9)
    display.draw_circle(BLACK, (152, 104), 9)
    display.draw_line(BLACK, (88, 164), (152, 164), width=3)
    display.draw_line(BLACK, (88, 164), (102, 150), width=3)
    display.draw_line(BLACK, (152, 164), (138, 150), width=3)
    display.draw_text("I miss you", (76, 198), RED, size=16)


DEFAULT_FACES: list[Face] = [
    Face("sleepy", lambda s: s.energy < 30, render_sleepy),
    Face("hungry", lambda s: s.hunger > 70, render_hungry),
    Face("sad", lambda s: s.happiness < 35, render_sad),
    Face("happy", lambda s: True, render_happy),
]


class FaceEngine:
    def __init__(self, faces: list[Face] | None = None) -> None:
        self.faces = faces or DEFAULT_FACES

    def select_face(self, state: PetState) -> Face:
        for face in self.faces:
            if face.condition(state):
                return face
        return self.faces[-1]
