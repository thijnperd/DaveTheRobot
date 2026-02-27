# DaveTheRobot / DaveOS

A lightweight virtual pet project evolved into a tiny embedded-style shell (**DaveOS**) that can run multiple mini-apps.

## High-level architecture overview

### 1) Core runtime (`os_core.py`)
- Handles the main event loop.
- Loads and switches apps.
- Provides small shared services through a restricted host API (`launch`, `home`, `get_setting`, `set_setting`, `status`).
- Keeps runtime settings in memory (`tick_ms`, `max_notes`) to control responsiveness and memory usage.

### 2) Platform adapters (`platform/`)
- `pc_display.py` / `pc_input.py`: pygame simulator.
- `pi_display.py` / `pi_input.py`: ST7789 + GPIO adapters.
- Both implement a common drawing/input interface (`platform/base.py`) so apps remain device-agnostic.

### 3) App modules (`apps/`)
Each app is a small module implementing:
- `on_open()`
- `on_event(event, host)`
- `render(display, context)`

Built-in apps:
- `launcher` (home menu)
- `files` (minimal file manager)
- `settings` (runtime tuning)
- `notes` (example app with capped note list)

### 4) Pet mode (`core/`)
Original pet system remains available as a separate runtime mode (`--system=pet`), while DaveOS shell is default (`--system=os`).

---

## Example code structure (OS core + app)

```text
dave_the_robot/
  main.py                # CLI + system/platform selection
  os_core.py             # MiniOS loop, app host API, app switching
  apps/
    base.py              # MiniApp protocol + OSContext
    launcher.py
    file_manager.py
    settings.py
    notes.py             # example app
  core/                  # pet mode runtime
  platform/              # PC/Pi adapters
```

### Pseudocode: OS core

```python
while not input.should_quit():
    events = input.poll()
    app = apps[current_app]

    for event in events:
        app.on_event(map_buttons(event), host_api)

    app.render(display, context)
    draw_status_bar_if_needed()
    display.present()
    sleep(tick_ms)
```

### Pseudocode: example app (Notes)

```python
on_event(event):
    if event == "select":
        notes.append(new_timestamped_note())
        notes = notes[-max_notes:]  # ring-buffer-like cap
    elif event == "up":
        selected = next_index()
    elif event == "back":
        host.home()
```

---

## Resource-constrained design notes

To stay efficient on Pi Zero 2 W:
- Keep app state in small Python structures (lists/dicts), no heavy frameworks.
- Avoid recursive scans; file manager lists only a small bounded subset.
- Reuse display assets via small in-memory caches (avoid repeated decode).
- Use coarse tick timing (`tick_ms`) rather than high-FPS loops.
- Cap user-generated data (`max_notes`) to avoid unbounded growth.
- Keep IPC simple: direct host method calls instead of background workers.

Expansion strategy under constraints:
1. Add one app at a time with strict memory caps.
2. Keep app APIs minimal (event in, draw out).
3. Use lazy loading for data-heavy features.
4. Prefer text/primitive UI before sprites/animations.
5. Add persistence carefully (small JSON files, bounded size).

---

## Run (Windows 10 / PC)

```powershell
py -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python -m dave_the_robot.main --system=os --platform=pc
```

Controls (PC):
- `F` = UP
- `P` = SELECT
- `S` = BACK
- `Esc` = quit

Pet mode (legacy runtime):

```powershell
python -m dave_the_robot.main --system=pet --platform=pc
```

## Run (Pi)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install adafruit-circuitpython-rgb-display gpiozero RPi.GPIO
python3 -m dave_the_robot.main --system=os --platform=pi
```

## Built-in plans

```bash
python -m dave_the_robot.main --plan=run-os
python -m dave_the_robot.main --plan=run-pc
python -m dave_the_robot.main --plan=run-pi
python -m dave_the_robot.main --plan=change-buttons
python -m dave_the_robot.main --plan=add-face
python -m dave_the_robot.main --plan=tune-pet
```
