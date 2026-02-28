"""PC input adapter translating keyboard/mouse into virtual button events."""

from __future__ import annotations

import pygame

from dave_the_robot.config import DEFAULT_PC_KEYS
from dave_the_robot.platform.base import ButtonEvent
from dave_the_robot.platform.pc_display import PCDisplay


class PCInput:
    def __init__(self, display: PCDisplay) -> None:
        self.display = display
        self._quit = False
        self.key_map = {value: key for key, value in DEFAULT_PC_KEYS.items()}

    def poll(self) -> list[ButtonEvent]:
        events: list[ButtonEvent] = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit = True
            elif event.type == pygame.KEYDOWN:
                action = self.key_map.get(event.key)
                if action:
                    events.append(ButtonEvent(action=action))
                elif event.key == pygame.K_ESCAPE:
                    self._quit = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                action = self.display.action_for_click(event.pos)
                if action:
                    events.append(ButtonEvent(action=action))
        return events

    def should_quit(self) -> bool:
        return self._quit
