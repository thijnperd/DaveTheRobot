"""Base app interfaces for the lightweight mini OS."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from dave_the_robot.platform.base import Display


@dataclass(frozen=True)
class OSContext:
    """Restricted context shared with apps."""

    current_app: str
    app_count: int
    settings: dict[str, int] = field(default_factory=dict)


class AppHost(Protocol):
    def launch(self, app_id: str) -> None:
        ...

    def home(self) -> None:
        ...

    def get_setting(self, key: str) -> int:
        ...

    def set_setting(self, key: str, value: int) -> None:
        ...

    def status(self, message: str) -> None:
        ...


class MiniApp(Protocol):
    app_id: str
    title: str

    def on_open(self) -> None:
        ...

    def on_event(self, event: str, host: AppHost) -> None:
        ...

    def render(self, display: Display, context: OSContext) -> None:
        ...
