# How to use `ui_lab_probe.py` (inside FreeCAD)

The script `ui_lab_probe.py` is a small UI laboratory that runs **inside
FreeCAD**. It does not modify any original file in the repository.

## Loading the script

Open the FreeCAD Python Console and run:

```python
from ui_lab_probe import get_lab

lab = get_lab()
```

## Features

### 1. List docks

Shows all active `QDockWidget` with name, title, and visibility:

```python
for item in lab.list_docks():
    print(item)
```

### 2. Apply layout and QSS

Hides default docks (Report view, Python console, Selection view, DAG view)
and applies a test stylesheet:

```python
lab.apply_layout_and_qss()
```

### 3. Quick context menu

Shortcut `Ctrl+Shift+Space` opens a light menu with:

- Active document
- Recompute document
- Fit all view
- Restore original UI

Or call directly:

```python
lab.open_quick_menu()
```

### 4. Restore

Undoes everything (visibility and stylesheet) without restarting FreeCAD:

```python
lab.restore()
```

See `USO_EN.md` for the complete example.
