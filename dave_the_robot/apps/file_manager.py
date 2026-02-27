"""Tiny file manager app with constrained directory listing."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from dave_the_robot.apps.base import AppHost, MiniApp, OSContext
from dave_the_robot.platform.base import Display

BG = (22, 26, 32)
FG = (225, 230, 235)
MUTED = (150, 160, 172)
ACCENT = (120, 200, 140)


@dataclass
class FileManagerApp(MiniApp):
    app_id: str = "files"
    title: str = "Files"

    root: Path = field(default_factory=lambda: Path.cwd())
    current: Path = field(default_factory=lambda: Path.cwd())
    entries: list[Path] = field(default_factory=list)
    selected: int = 0

    def on_open(self) -> None:
        self._refresh_entries()

    def on_event(self, event: str, host: AppHost) -> None:
        if not self.entries:
            if event == "back":
                host.home()
            return

        if event == "up":
            self.selected = (self.selected + 1) % len(self.entries)
        elif event == "select":
            target = self.entries[self.selected]
            if target.is_dir():
                self.current = target
                self._refresh_entries()
            else:
                host.status(f"file: {target.name[:18]}")
        elif event == "back":
            if self.current != self.root and self.current.parent.exists():
                self.current = self.current.parent
                self._refresh_entries()
            else:
                host.home()

    def render(self, display: Display, context: OSContext) -> None:
        display.clear(BG)
        display.draw_text("Files", (96, 12), ACCENT, size=18)
        display.draw_text(self.current.name[:16] or str(self.current), (10, 34), MUTED, size=14)

        if not self.entries:
            display.draw_text("(empty)", (90, 108), FG, size=16)
            return

        y = 58
        for idx, entry in enumerate(self.entries[:5]):
            marker = ">" if idx == self.selected else " "
            suffix = "/" if entry.is_dir() else ""
            color = ACCENT if idx == self.selected else FG
            display.draw_text(f"{marker} {entry.name[:18]}{suffix}", (10, y), color, size=14)
            y += 30

        display.draw_text("SEL=open BACK=up/home", (8, 214), MUTED, size=12)

    def _refresh_entries(self) -> None:
        try:
            listed = sorted(self.current.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
        except (PermissionError, FileNotFoundError):
            listed = []
        self.entries = listed[:12]
        self.selected = 0
