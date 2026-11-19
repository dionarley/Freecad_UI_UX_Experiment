# How to use `ui_lab_app.py` (real UI/UX application)

The `ui_lab_app.py` is a **complete UI/UX laboratory application**, not just a
test. It works inside FreeCAD and also in standalone mode.

## Inside FreeCAD

Open the FreeCAD Python Console:

```python
from ui_lab_app import run_in_freecad
win = run_in_freecad()
```

The window hooks into the FreeCAD main window and offers:

| Tab | What it does |
|---|---|
| **Docks** | Lists all `QDockWidget` in the application and allows showing/hiding each one, individually or all at once. |
| **QSS / Style** | Live stylesheet editor applied to the FreeCAD MainWindow or the app window. Includes load/save `.qss` files. |
| **Info / Control** | Shows Qt binding, FreeCAD status (document/objects), and buttons to recompute document and fit all view (Fit All). |

The integrated log writes both to the text area and to the FreeCAD Python
Console.

## Standalone mode (outside FreeCAD)

```sh
uv sync --extra window
uv run python ui_lab_app.py
```

Or via script:

```sh
./run.sh app
```

Creates an independent window with the same tabs (Docks, QSS, Info) to develop
and test the interface without needing FreeCAD.

## Programmatic icon

The window and test button use an icon drawn with QPainter (blue circle with
letter "F"), without depending on an external image file.

## Persistent configuration

The app saves the edited QSS in `ui_lab_config.json` at the project root, so
style customizations persist between sessions.
