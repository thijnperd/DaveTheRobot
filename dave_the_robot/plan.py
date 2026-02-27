"""Step-by-step operator plans for common customization/setup tasks."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Plan:
    plan_id: str
    title: str
    steps: list[str]


PLANS: dict[str, Plan] = {
    "run-pc": Plan(
        plan_id="run-pc",
        title="Run DaveTheRobot on your PC",
        steps=[
            "Create and activate a Python virtual environment.",
            "Install dependencies with: pip install -r requirements.txt",
            "Start the simulator with: python -m dave_the_robot.main --platform=pc",
            "Use Feed/Play/Sleep buttons (or F/P/S keys) to interact.",
        ],
    ),
    "run-pi": Plan(
        plan_id="run-pi",
        title="Run DaveTheRobot on Raspberry Pi",
        steps=[
            "Enable SPI in raspi-config (Interface Options -> SPI).",
            "Create and activate a virtual environment.",
            "Install dependencies: pip install -r requirements.txt",
            "Install Pi-only libs: pip install adafruit-circuitpython-rgb-display gpiozero RPi.GPIO",
            "Verify button pin mapping in dave_the_robot/config.py.",
            "Run: python3 -m dave_the_robot.main --platform=pi",
        ],
    ),
    "change-buttons": Plan(
        plan_id="change-buttons",
        title="Change button mappings",
        steps=[
            "Open dave_the_robot/config.py.",
            "Edit DEFAULT_PI_BUTTON_PINS to match your HAT wiring.",
            "(Optional) edit DEFAULT_PC_KEYS for keyboard bindings.",
            "Restart the app and verify button actions.",
        ],
    ),
    "add-face": Plan(
        plan_id="add-face",
        title="Add a new pet face/expression",
        steps=[
            "Open dave_the_robot/core/faces.py.",
            "Add a new render_<name>(display, state) function using draw primitives.",
            "Add a Face(...) entry to DEFAULT_FACES with a condition and face_id.",
            "Place your new face above the default happy fallback in DEFAULT_FACES.",
            "Run python -m compileall dave_the_robot to verify syntax.",
            "Run pc mode and validate the new face triggers under expected stats.",
        ],
    ),
    "tune-pet": Plan(
        plan_id="tune-pet",
        title="Tune pet behavior",
        steps=[
            "Open dave_the_robot/core/pet.py.",
            "Adjust action values in apply_action() for feed/play/sleep.",
            "Adjust decay in time_step() to control game pacing.",
            "Optionally adjust STATE_UPDATE_SECONDS in config.py.",
            "Run in pc mode and test interactions for balance.",
        ],
    ),
}


def available_plan_ids() -> list[str]:
    return sorted(PLANS.keys())


def render_plan(plan_id: str) -> str:
    plan = PLANS.get(plan_id)
    if plan is None:
        known = ", ".join(available_plan_ids())
        raise ValueError(f"Unknown plan '{plan_id}'. Available: {known}")

    lines = [f"{plan.title} ({plan.plan_id})"]
    for idx, step in enumerate(plan.steps, start=1):
        lines.append(f"{idx}. {step}")
    return "\n".join(lines)
