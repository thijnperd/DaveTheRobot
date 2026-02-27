"""Lightweight embedded-style app runtime (mini OS shell)."""

from __future__ import annotations

import time
from dataclasses import dataclass, field

from dave_the_robot.apps.base import AppHost, MiniApp, OSContext
from dave_the_robot.apps.file_manager import FileManagerApp
from dave_the_robot.apps.launcher import LauncherApp
from dave_the_robot.apps.notes import NotesApp
from dave_the_robot.apps.settings import SettingsApp
from dave_the_robot.platform.base import Display, InputAdapter


@dataclass
class MiniOS(AppHost):
    display: Display
    controls: InputAdapter
    apps: dict[str, MiniApp] = field(default_factory=dict)
    current_app_id: str = "launcher"
    settings: dict[str, int] = field(default_factory=lambda: {"tick_ms": 200, "max_notes": 15})
    status_text: str = ""
    status_deadline: float = 0.0

    def __post_init__(self) -> None:
        launcher = LauncherApp()
        self.apps = {
            "launcher": launcher,
            "files": FileManagerApp(),
            "settings": SettingsApp(),
            "notes": NotesApp(),
        }
        launcher.set_entries(["files", "settings", "notes"])
        self.apps[self.current_app_id].on_open()

    def run(self) -> None:
        while not self.controls.should_quit():
            events = self.controls.poll()
            app = self.apps[self.current_app_id]

            for event in events:
                app.on_event(self._map_action(event.action), self)

            self._render_frame()
            time.sleep(self.settings["tick_ms"] / 1000.0)

    def launch(self, app_id: str) -> None:
        if app_id in self.apps:
            self.current_app_id = app_id
            self.apps[app_id].on_open()

    def home(self) -> None:
        self.launch("launcher")

    def get_setting(self, key: str) -> int:
        return self.settings[key]

    def set_setting(self, key: str, value: int) -> None:
        self.settings[key] = value

    def status(self, message: str) -> None:
        self.status_text = message
        self.status_deadline = time.monotonic() + 3.0

    def _render_frame(self) -> None:
        app = self.apps[self.current_app_id]
        context = OSContext(
            current_app=self.current_app_id,
            app_count=len(self.apps),
            settings=self.settings.copy(),
        )
        app.render(self.display, context)

        if time.monotonic() < self.status_deadline:
            self.display.draw_rect((0, 0, 0), (0, 224, 240, 16))
            self.display.draw_text(self.status_text[:30], (4, 226), (255, 255, 255), size=12)

        self.display.present(None, self.current_app_id)

    @staticmethod
    def _map_action(action: str) -> str:
        mapping = {
            "feed": "up",
            "play": "select",
            "sleep": "back",
        }
        return mapping.get(action, action)
