"""Example app: lightweight notes with capped in-memory storage."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from dave_the_robot.apps.base import AppHost, MiniApp, OSContext
from dave_the_robot.platform.base import Display

BG = (18, 28, 24)
FG = (232, 240, 236)
ACCENT = (106, 230, 170)


@dataclass
class NotesApp(MiniApp):
    app_id: str = "notes"
    title: str = "Notes"

    notes: list[str] = field(default_factory=lambda: ["Welcome to DaveOS notes"])
    selected: int = 0

    def on_open(self) -> None:
        self.selected = min(self.selected, max(len(self.notes) - 1, 0))

    def on_event(self, event: str, host: AppHost) -> None:
        if event == "up" and self.notes:
            self.selected = (self.selected + 1) % len(self.notes)
        elif event == "select":
            stamp = datetime.now().strftime("%H:%M:%S")
            self.notes.append(f"note {len(self.notes)+1} @ {stamp}")
            max_notes = host.get_setting("max_notes")
            if len(self.notes) > max_notes:
                self.notes = self.notes[-max_notes:]
            self.selected = len(self.notes) - 1
            host.status("note added")
        elif event == "back":
            host.home()

    def render(self, display: Display, context: OSContext) -> None:
        display.clear(BG)
        display.draw_text("Notes", (96, 12), ACCENT, size=18)
        display.draw_text("SEL=add UP=next", (52, 34), FG, size=14)

        y = 64
        start = max(0, len(self.notes) - 5)
        visible = self.notes[start:]
        for idx, note in enumerate(visible):
            absolute_idx = start + idx
            marker = ">" if absolute_idx == self.selected else " "
            color = ACCENT if absolute_idx == self.selected else FG
            display.draw_text(f"{marker} {note[:24]}", (10, y), color, size=13)
            y += 30
