# Tests

The project uses [pytest](https://docs.pytest.org/) with minimal tests that do
not take up much disk space.

## Run the tests

```sh
uv run pytest -q
```

Expected output (without PySide6): `3 passed in 0.01s`.  
Expected output (with PySide6 + libGL): all tests pass.

## Test structure

| File | What it tests |
|---|---|
| `tests/test_ui_lab.py` | Minimal test: imports `ui_lab_probe.py` without FreeCAD, validates constants and `get_lab()`. |
| `tests/test_window_quick.py` | Quick window/dock test: creates QMainWindow, registers QDockWidget, applies QSS, saves state. Requires PySide6. |
| `tests/test_app.py` | Test of `ui_lab_app.py`: instantiates the window, checks tabs, log, QSS editor. Requires PySide6. |
| `tests/test_dependencies.py` | Verifies that modules import without error when PySide is available. Requires PySide6. |

## Window tests (require PySide6)

The tests in `test_window_quick.py`, `test_app.py`, and part of
`test_dependencies.py` need PySide6 and `libGL.so.1`. In environments without
`libGL` (e.g. NixOS), they are skipped automatically:

```sh
# Install PySide6
uv sync --extra window

# Run all tests (including window tests)
uv run pytest -q
```

## Basic tests (without PySide)

The 3 tests in `test_ui_lab.py` run without any extra dependency:

```sh
uv run pytest tests/test_ui_lab.py -q
```

## Via `run.sh`

```sh
./run.sh test     # basic tests only
./run.sh window   # installs PySide6 and runs all tests
```
