"""Entry point for Dave the Robot virtual pet and mini OS runtime."""

from __future__ import annotations

import argparse
import os
import time

from dave_the_robot.config import STATE_UPDATE_SECONDS, TICK_SECONDS
from dave_the_robot.core.faces import FaceEngine
from dave_the_robot.core.pet import VirtualPet
from dave_the_robot.os_core import MiniOS
from dave_the_robot.plan import available_plan_ids, render_plan


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Dave The Robot virtual pet")
    parser.add_argument(
        "--platform",
        choices=["pc", "pi"],
        default=os.getenv("DAVE_PLATFORM", "pc"),
        help="Runtime platform: pc (pygame simulator) or pi (ST7789 + GPIO buttons)",
    )
    parser.add_argument(
        "--system",
        choices=["os", "pet"],
        default=os.getenv("DAVE_SYSTEM", "os"),
        help="Runtime system: os (multi-app shell) or pet (single virtual pet)",
    )
    parser.add_argument(
        "--plan",
        choices=available_plan_ids(),
        help="Print a step-by-step plan for common tasks and exit",
    )
    return parser.parse_args()


def make_platform(platform_name: str):
    if platform_name == "pi":
        from dave_the_robot.platform.pi_display import PiDisplay
        from dave_the_robot.platform.pi_input import PiInput

        display = PiDisplay()
        controls = PiInput()
        closer = None
    else:
        from dave_the_robot.platform.pc_display import PCDisplay
        from dave_the_robot.platform.pc_input import PCInput

        display = PCDisplay()
        controls = PCInput(display)
        closer = display.close
    return display, controls, closer


def run_pet(platform_name: str) -> None:
    pet = VirtualPet()
    face_engine = FaceEngine()
    display, controls, closer = make_platform(platform_name)

    last_state_update = time.monotonic()

    try:
        while not controls.should_quit():
            for button_event in controls.poll():
                pet.apply_action(button_event.action)

            now = time.monotonic()
            if now - last_state_update >= STATE_UPDATE_SECONDS:
                pet.time_step()
                last_state_update = now

            active_face = face_engine.select_face(pet.state)
            active_face.render(display, pet.state)
            display.present(pet.state, active_face.face_id)

            time.sleep(TICK_SECONDS / 2)
    finally:
        if closer is not None:
            closer()


def run_os(platform_name: str) -> None:
    display, controls, closer = make_platform(platform_name)
    os_shell = MiniOS(display=display, controls=controls)
    try:
        os_shell.run()
    finally:
        if closer is not None:
            closer()


def main() -> None:
    args = parse_args()
    if args.plan:
        print(render_plan(args.plan))
        return

    if args.system == "pet":
        run_pet(args.platform)
        return

    run_os(args.platform)


if __name__ == "__main__":
    main()
