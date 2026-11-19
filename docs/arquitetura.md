# Architecture / Arquitetura

## Components

```
freecad-ui-ux-experiment/
├── ui_lab_probe.py     # Probe script inside FreeCAD (not modified)
├── ui_lab_app.py       # Real UI/UX application (standalone)
├── window_test.py      # Simple window with test button (standalone)
├── tests/              # pytest tests
├── docs/               # This documentation
├── run.sh              # Execution script
├── Dockerfile          # Minimal container
├── pyproject.toml      # uv project + dependencies
├── uv.lock             # Locked dependencies
├── .mise.toml          # Python 3.11 via mise
└── LICENSE             # CC BY 4.0
```

## Dependencies between files

```
ui_lab_probe.py  ← (never modified, imported when needed)
window_test.py   ← uses PySide6/PySide2 (optional)
ui_lab_app.py    ← uses PySide6/PySide2 (optional)
tests/           ← import ui_lab_probe.py, ui_lab_app.py, window_test.py
```

## FreeCAD reference sources

The project was modeled on parts of [FreeCAD/FreeCAD](https://github.com/FreeCAD/FreeCAD):

| FreeCAD source | What was extracted |
|---|---|
| `src/Gui/DockWindow.h` | Dock base class (`QWidget` + `BaseView`) |
| `src/Gui/DockWindowManager.h` | Singleton managing `QDockWidget` |
| `src/Gui/Stylesheets/` | QSS patterns for docks, menus, buttons |

## License / Licença

All content is under **Creative Commons Attribution 4.0 International
(CC BY 4.0)**. See `LICENSE` for the full text.

Todo o conteúdo está sob **Creative Commons Attribution 4.0 International
(CC BY 4.0)**. Veja `LICENSE` para o texto completo.
