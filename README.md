# DaveTheRobot

A small cross-platform virtual pet app designed for:

- **PC mode** (Windows/Linux/macOS): pygame simulator with a 240x240 virtual LCD and clickable buttons.
- **Pi mode** (Raspberry Pi Zero 2 W): Waveshare 1.3" ST7789 LCD + GPIO buttons.

## Project layout

```text
dave_the_robot/
  __init__.py
  config.py
  main.py
  core/
    pet.py
    faces.py
  platform/
    base.py
    pc_display.py
    pc_input.py
    pi_display.py
    pi_input.py
assets/
requirements.txt
README.md
```

## Architecture overview

- `core/` contains hardware-agnostic logic:
  - `pet.py`: state model + behavior (`feed`, `play`, `sleep`, periodic decay).
  - `faces.py`: expression system with condition-based face selection and rendering.
- `platform/` contains adapters:
  - `Display`-style drawing primitives are implemented by PC and Pi display classes.
  - `Input` adapters return logical button events so core logic never touches GPIO directly.

## Install (Windows 10 / PC mode)

1. Create a venv (recommended):
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\activate
   ```
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Run in PC mode:
   ```powershell
   python -m dave_the_robot.main --platform=pc
   ```

### PC mode controls

- On-screen buttons: **Feed**, **Play**, **Sleep**
- Keyboard shortcuts: `F`, `P`, `S`
- `Esc` or window close button exits

## Install (Raspberry Pi Zero 2 W / Pi mode)

1. Install base dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Install Pi-specific dependencies:
   ```bash
   pip install adafruit-circuitpython-rgb-display gpiozero RPi.GPIO
   ```
3. Enable SPI on your Pi (`raspi-config` -> Interface Options -> SPI).
4. Run in Pi mode:
   ```bash
   python3 -m dave_the_robot.main --platform=pi
   ```

## Configuration and customization

- Edit `dave_the_robot/config.py`:
  - `DEFAULT_PI_BUTTON_PINS` to match your exact Waveshare HAT button wiring.
  - `STATE_UPDATE_SECONDS` and `TICK_SECONDS` for game speed.
- Tweak behavior in `dave_the_robot/core/pet.py`.
- Add new expressions in `dave_the_robot/core/faces.py` by creating new `Face(...)` entries with:
  - a unique `face_id`
  - a condition function
  - a render function using drawing primitives

## Notes

- Pi display defaults in `pi_display.py` target a common ST7789 setup; adjust CS/DC/RST pins if needed for your board.
- This is an initial framework intended to be easy to extend with sprites, animations, and additional actions.
