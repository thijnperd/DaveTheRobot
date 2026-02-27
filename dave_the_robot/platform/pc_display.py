"""PC display adapter using pygame to mimic a Waveshare-style screen and buttons."""

from __future__ import annotations

from dataclasses import dataclass

import pygame

from dave_the_robot.config import SCREEN_SIZE
from dave_the_robot.platform.base import Color


@dataclass(frozen=True)
class ButtonWidget:
    action: str
    label: str
    rect: pygame.Rect


class PCDisplay:
    width = SCREEN_SIZE
    height = SCREEN_SIZE

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Dave The Robot - PC Simulator")
        self.window = pygame.display.set_mode((520, 340))
        self.canvas = pygame.Surface((SCREEN_SIZE, SCREEN_SIZE))
        self.clock = pygame.time.Clock()
        self.font_cache: dict[int, pygame.font.Font] = {}
        self.image_cache: dict[str, pygame.Surface] = {}

        self.buttons = [
            ButtonWidget("feed", "Feed (F)", pygame.Rect(290, 40, 180, 56)),
            ButtonWidget("play", "Play (P)", pygame.Rect(290, 120, 180, 56)),
            ButtonWidget("sleep", "Sleep (S)", pygame.Rect(290, 200, 180, 56)),
        ]

    def clear(self, color: Color) -> None:
        self.canvas.fill(color)

    def draw_circle(self, color: Color, center: tuple[int, int], radius: int, width: int = 0) -> None:
        pygame.draw.circle(self.canvas, color, center, radius, width)

    def draw_rect(self, color: Color, rect: tuple[int, int, int, int], width: int = 0) -> None:
        pygame.draw.rect(self.canvas, color, pygame.Rect(rect), width)

    def draw_line(self, color: Color, start: tuple[int, int], end: tuple[int, int], width: int = 1) -> None:
        pygame.draw.line(self.canvas, color, start, end, width)

    def draw_text(self, text: str, position: tuple[int, int], color: Color, size: int = 16) -> None:
        font = self._get_font(size)
        glyph = font.render(text, True, color)
        self.canvas.blit(glyph, position)

    def draw_image(
        self,
        image_path: str,
        position: tuple[int, int],
        size: tuple[int, int] | None = None,
    ) -> None:
        image = self._get_image(image_path)
        if size is not None:
            image = pygame.transform.smoothscale(image, size)
        self.canvas.blit(image, position)

    def present(self, state: object | None, active_face: str) -> None:
        self.window.fill((28, 31, 37))

        self.window.blit(self.canvas, (20, 20))
        pygame.draw.rect(self.window, (200, 200, 200), pygame.Rect(20, 20, 240, 240), width=2)

        self._draw_buttons()
        self._draw_status(state, active_face)

        pygame.display.flip()
        self.clock.tick(30)

    def _draw_buttons(self) -> None:
        for button in self.buttons:
            pygame.draw.rect(self.window, (58, 134, 255), button.rect, border_radius=8)
            pygame.draw.rect(self.window, (230, 238, 255), button.rect, width=2, border_radius=8)
            txt = self._get_font(22).render(button.label, True, (255, 255, 255))
            txt_rect = txt.get_rect(center=button.rect.center)
            self.window.blit(txt, txt_rect)

    def _draw_status(self, state: object | None, active_face: str) -> None:
        base_y = 276
        lines = [f"Screen: {active_face}"]

        if state is not None and all(hasattr(state, attr) for attr in ("hunger", "happiness", "energy")):
            lines.append(
                f"Hunger: {state.hunger:3d}   Happiness: {state.happiness:3d}   Energy: {state.energy:3d}"
            )
        else:
            lines.append("F=UP  P=SELECT  S=BACK")
        for i, line in enumerate(lines):
            txt = self._get_font(18).render(line, True, (225, 225, 225))
            self.window.blit(txt, (20, base_y + i * 26))

    def action_for_click(self, pos: tuple[int, int]) -> str | None:
        for button in self.buttons:
            if button.rect.collidepoint(pos):
                return button.action
        return None

    def close(self) -> None:
        pygame.quit()

    def _get_font(self, size: int) -> pygame.font.Font:
        if size not in self.font_cache:
            self.font_cache[size] = pygame.font.SysFont("consolas", size)
        return self.font_cache[size]

    def _get_image(self, image_path: str) -> pygame.Surface:
        if image_path not in self.image_cache:
            self.image_cache[image_path] = pygame.image.load(image_path).convert_alpha()
        return self.image_cache[image_path]
