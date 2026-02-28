"""Home launcher app."""

from __future__ import annotations

from dataclasses import dataclass

from dave_the_robot.apps.base import AppHost, MiniApp, OSContext
from dave_the_robot.platform.base import Display

BG = (12, 18, 28)
FG = (230, 235, 240)
ACCENT = (88, 166, 255)


@dataclass
class LauncherApp(MiniApp):
    app_id: str = "launcher"
    title: str = "Home"

    entries: list[str] | None = None
    selected: int = 0

    def set_entries(self, entries: list[str]) -> None:
        self.entries = entries
        self.selected = 0

    def on_open(self) -> None:
        self.selected = 0

    def on_event(self, event: str, host: AppHost) -> None:
        if not self.entries:
            return
        if event == "up":
            self.selected = (self.selected + 1) % len(self.entries)
        elif event == "select":
            host.launch(self.entries[self.selected])

    def render(self, display: Display, context: OSContext) -> None:
        display.clear(BG)
        display.draw_text("DaveOS", (84, 16), ACCENT, size=20)
        display.draw_text("UP=Next SEL=Open", (40, 40), FG, size=14)

        if not self.entries:
            display.draw_text("No apps installed", (52, 110), FG, size=16)
            return

        start_y = 72
        for idx, app_id in enumerate(self.entries):
            y = start_y + idx * 32
            marker = ">" if idx == self.selected else " "
            color = ACCENT if idx == self.selected else FG
            display.draw_text(f"{marker} {app_id}", (28, y), color, size=16)
