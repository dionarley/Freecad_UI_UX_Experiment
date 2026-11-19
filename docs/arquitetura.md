# Arquitetura do Projeto

## Componentes

```
Freecad_UI_UX_Experiment/
├── ui_lab_probe.py     # Script de probe dentro do FreeCAD (não modificado)
├── ui_lab_app.py       # Aplicação real de UI/UX (autônomo)
├── window_test.py      # Janela simples com botão de teste (autônomo)
├── tests/              # Testes pytest
├── docs/               # Esta documentação
├── run.sh              # Script de execução
├── Dockerfile          # Container mínimo
├── pyproject.toml      # Projeto uv + dependências
├── uv.lock             # Dependências travadas
├── .mise.toml          # Python 3.11 via mise
└── LICENSE             # CC BY 4.0
```

## Dependências entre arquivos

```
ui_lab_probe.py  ← (nunca modificado, importado quando necessário)
window_test.py   ← usa PySide6/PySide2 (opcional)
ui_lab_app.py    ← usa PySide6/PySide2 (opcional)
tests/           ← importam ui_lab_probe.py, ui_lab_app.py, window_test.py
```

## Fontes de referência do FreeCAD

O projeto foi modelado em partes do [FreeCAD/FreeCAD](https://github.com/FreeCAD/FreeCAD):

| Fonte | O que foi extraído |
|---|---|
| `src/Gui/DockWindow.h` | Classe base de dock (`QWidget` + `BaseView`) |
| `src/Gui/DockWindowManager.h` | Singleton gerenciando `QDockWidget` |
| `src/Gui/Stylesheets/` | Padrões QSS para docks, menus, botões |

## Licença

Todo o conteúdo está sob **Creative Commons Attribution 4.0 International
(CC BY 4.0)**. Veja `LICENSE` para o texto completo.
