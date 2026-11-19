# Overview — FreeCAD UI/UX Experiment

This repository is a laboratory of UI/UX experiments for FreeCAD. The goal is to
test whether FreeCAD is viable for customizing the interface (hiding docks,
applying QSS, quick context menu, managing docks, editing styles live) and, if
it works well, contribute improvements to the community.

## What is in this repository

| File | Description |
|---|---|
| `ui_lab_probe.py` | UI laboratory script (probe) |
| `ui_lab_app.py` | Real UI/UX application |
| `window_test.py` | Test window with button |
| `tests/` | Automated tests with pytest (minimal, low disk usage) |
| `run.sh` | Execution script (sync, test, window, app, clean) |
| `Dockerfile` | Minimal container for tests |
| `pyproject.toml` / `uv.lock` | Dependency management with `uv` |
| `LICENSE` | CC BY 4.0 |

## Two modes of use

1. **Inside FreeCAD**: the script hooks into the application's main window and
   can list/hide real docks, apply QSS to the MainWindow, recompute documents,
   etc.
2. **Outside FreeCAD (standalone)**: creates its own independent window to
   develop and test the interface without needing FreeCAD installed.

## Original code untouched

The file `ui_lab_probe.py` is never modified by other files in this project.
All new features (`ui_lab_app.py`, `window_test.py`, tests) are standalone
files that import `ui_lab_probe.py` only when needed, without altering it.
