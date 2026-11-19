# Usage — example execution

The example below **only runs inside FreeCAD** (where `App` and `Gui` are
available). It is outside of `ui_lab_probe.py` so that importing the module
outside FreeCAD is not prevented.

## 1. Inspect exact dock names before hiding

```python
from ui_lab_probe import get_lab

lab = get_lab()
for item in lab.list_docks():
    print(item)
```

## 2. Apply the test (uncomment to run immediately)

```python
lab.apply_layout_and_qss()   # hides default docks and applies test QSS
lab.open_quick_menu()        # opens the light context menu
```

## 3. Undo everything without restarting FreeCAD

```python
lab.restore()   # restores original dock visibility and previous stylesheet
```

### Quick shortcut

After `apply_layout_and_qss()`, press **Ctrl+Shift+Space** to open the light
contextual menu with: active document, recompute document, fit all view
(Fit All), and restore original UI.
