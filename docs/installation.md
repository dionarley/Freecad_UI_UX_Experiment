# Installation

This project uses [uv](https://github.com/astral-sh/uv) to manage
dependencies and [mise](https://mise.jdx.dev/) to pin the Python version.

## Prerequisites

- Python >= 3.10 (via `mise` or `uv`)
- FreeCAD (to use the scripts inside the application)
- PySide6 or PySide2 (optional, only for `ui_lab_app.py`, `window_test.py`
  and window tests)

## Step by step

```sh
# Clone or download this repository, then:
cd freecad-ui-ux-experiment

# 1. Install development dependencies (pytest)
uv sync

# 2. (Optional) Install PySide6 to use the app and run window tests
uv sync --extra window

# 3. Run basic tests (no PySide needed)
uv run pytest -q

# With mise (installs Python 3.11 if needed)
mise exec python@3.11 -- uv sync
```

## Using the `run.sh` script

```sh
./run.sh sync     # sync dependencies (uv sync)
./run.sh test     # run tests (pytest)
./run.sh window   # run including window test (uv sync --extra window)
./run.sh app      # run the real UI/UX app (standalone, needs PySide6)
./run.sh clean    # remove .venv and __pycache__
```

## Container (podman / docker)

```sh
podman build -t freecad-ui-lab .
podman run --rm freecad-ui-lab
```

The container runs the tests automatically when it starts.

## Note about libGL

If you are in an environment without `libGL.so.1` (e.g. NixOS, minimal
containers), PySide6 cannot be imported. In that case:
- Basic tests still work (`3 passed`).
- Window tests and the app are skipped automatically.
- To run them, install `libGL` and use `uv sync --extra window`.
