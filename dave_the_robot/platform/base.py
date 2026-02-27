"""Shared interfaces for display and input adapters."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


Color = tuple[int, int, int]


@dataclass(frozen=True)
class ButtonEvent:
    action: str


class Display(Protocol):
    width: int
    height: int

    def clear(self, color: Color) -> None:
        ...

    def draw_circle(self, color: Color, center: tuple[int, int], radius: int, width: int = 0) -> None:
        ...

    def draw_rect(self, color: Color, rect: tuple[int, int, int, int], width: int = 0) -> None:
        ...

    def draw_line(self, color: Color, start: tuple[int, int], end: tuple[int, int], width: int = 1) -> None:
        ...

    def draw_text(self, text: str, position: tuple[int, int], color: Color, size: int = 16) -> None:
        ...

    def draw_image(
        self,
        image_path: str,
        position: tuple[int, int],
        size: tuple[int, int] | None = None,
    ) -> None:
        ...

    def present(self, state: object | None, active_face: str) -> None:
        ...


class InputAdapter(Protocol):
    def poll(self) -> list[ButtonEvent]:
        ...

    def should_quit(self) -> bool:
        ...
