"""Raspberry Pi display adapter for Waveshare ST7789 displays."""

from __future__ import annotations

from typing import Any

from PIL import Image, ImageDraw, ImageFont

from dave_the_robot.config import SCREEN_SIZE
from dave_the_robot.core.pet import PetState
from dave_the_robot.platform.base import Color


class PiDisplay:
    width = SCREEN_SIZE
    height = SCREEN_SIZE

    def __init__(self) -> None:
        try:
            import board
            import digitalio
            from adafruit_rgb_display import st7789
        except ImportError as exc:
            raise RuntimeError(
                "Pi mode requires board, digitalio and adafruit-circuitpython-rgb-display."
            ) from exc

        cs_pin = digitalio.DigitalInOut(board.CE0)
        dc_pin = digitalio.DigitalInOut(board.D25)
        reset_pin = digitalio.DigitalInOut(board.D27)

        baudrate = 64_000_000
        spi = board.SPI()
        self.disp = st7789.ST7789(
            spi,
            cs=cs_pin,
            dc=dc_pin,
            rst=reset_pin,
            baudrate=baudrate,
            width=SCREEN_SIZE,
            height=SCREEN_SIZE,
            x_offset=0,
            y_offset=0,
            rotation=0,
        )

        self.image = Image.new("RGB", (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)
        self.font_cache: dict[int, Any] = {}

    def clear(self, color: Color) -> None:
        self.draw.rectangle((0, 0, self.width, self.height), fill=color)

    def draw_circle(self, color: Color, center: tuple[int, int], radius: int, width: int = 0) -> None:
        x, y = center
        bbox = (x - radius, y - radius, x + radius, y + radius)
        if width == 0:
            self.draw.ellipse(bbox, fill=color)
        else:
            self.draw.ellipse(bbox, outline=color, width=width)

    def draw_rect(self, color: Color, rect: tuple[int, int, int, int], width: int = 0) -> None:
        x, y, w, h = rect
        bbox = (x, y, x + w, y + h)
        if width == 0:
            self.draw.rectangle(bbox, fill=color)
        else:
            self.draw.rectangle(bbox, outline=color, width=width)

    def draw_line(self, color: Color, start: tuple[int, int], end: tuple[int, int], width: int = 1) -> None:
        self.draw.line((start, end), fill=color, width=width)

    def draw_text(self, text: str, position: tuple[int, int], color: Color, size: int = 16) -> None:
        font = self._get_font(size)
        self.draw.text(position, text, fill=color, font=font)

    def present(self, state: PetState, active_face: str) -> None:
        self.disp.image(self.image)

    def _get_font(self, size: int) -> ImageFont.ImageFont:
        if size not in self.font_cache:
            self.font_cache[size] = ImageFont.load_default()
        return self.font_cache[size]
