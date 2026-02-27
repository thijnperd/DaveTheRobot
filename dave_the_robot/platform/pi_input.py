"""Raspberry Pi input adapter for Waveshare HAT buttons."""

from __future__ import annotations

from gpiozero import Button

from dave_the_robot.config import DEFAULT_PI_BUTTON_PINS
from dave_the_robot.platform.base import ButtonEvent


class PiInput:
    """Maps GPIO button presses to logical actions."""

    def __init__(self) -> None:
        self._quit = False
        self._event_queue: list[ButtonEvent] = []

        self.action_buttons = {
            "feed": Button(DEFAULT_PI_BUTTON_PINS["feed"], pull_up=True, bounce_time=0.05),
            "play": Button(DEFAULT_PI_BUTTON_PINS["play"], pull_up=True, bounce_time=0.05),
            "sleep": Button(DEFAULT_PI_BUTTON_PINS["sleep"], pull_up=True, bounce_time=0.05),
        }

        for action, button in self.action_buttons.items():
            button.when_pressed = self._make_handler(action)

    def _make_handler(self, action: str):
        def _handler() -> None:
            self._event_queue.append(ButtonEvent(action=action))

        return _handler

    def poll(self) -> list[ButtonEvent]:
        events = self._event_queue.copy()
        self._event_queue.clear()
        return events

    def should_quit(self) -> bool:
        return self._quit
