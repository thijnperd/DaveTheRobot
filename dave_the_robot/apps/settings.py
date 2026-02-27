"""Settings app for runtime tuning with tiny memory footprint."""

from __future__ import annotations

from dataclasses import dataclass

from dave_the_robot.apps.base import AppHost, MiniApp, OSContext
from dave_the_robot.platform.base import Display

BG = (24, 20, 30)
FG = (230, 228, 236)
ACCENT = (200, 145, 255)


@dataclass
class SettingsApp(MiniApp):
    app_id: str = "settings"
    title: str = "Settings"

    keys: tuple[str, ...] = ("tick_ms", "max_notes")
    selected: int = 0

    def on_open(self) -> None:
        self.selected = 0

    def on_event(self, event: str, host: AppHost) -> None:
        if event == "up":
            self.selected = (self.selected + 1) % len(self.keys)
            return

        current_key = self.keys[self.selected]
        value = host.get_setting(current_key)

        if event == "select":
            if current_key == "tick_ms":
                value = 100 if value >= 350 else value + 50
            elif current_key == "max_notes":
                value = 5 if value >= 25 else value + 5
            host.set_setting(current_key, value)
            host.status(f"{current_key}={value}")
        elif event == "back":
            host.home()

    def render(self, display: Display, context: OSContext) -> None:
        display.clear(BG)
        display.draw_text("Settings", (76, 14), ACCENT, size=18)
        display.draw_text("UP=next SEL=change", (38, 36), FG, size=14)

        y = 76
        for idx, key in enumerate(self.keys):
            marker = ">" if idx == self.selected else " "
            color = ACCENT if idx == self.selected else FG
            display.draw_text(f"{marker} {key}", (20, y), color, size=16)
            y += 30
