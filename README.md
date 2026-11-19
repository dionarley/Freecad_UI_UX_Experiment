# FreeCAD UI/UX Experiment

Experimento de UI/UX para o FreeCAD. O objetivo é testar se o FreeCAD é viável
para customizar a interface (esconder docks, aplicar QSS, menu contextual rápido)
e, se der certo, enviar para a comunidade.

:)

> p.s. i'm not a good programmer yet, and i'm portuguese native speaking.  
> by Dionatley R V  
> God And Odin Bless us !

## O que este projeto faz

O script `ui_lab_probe.py` cria um pequeno "laboratório" de UI dentro do FreeCAD:

- **Listar docks** — mostra todos os `QDockWidget` ativos com nome, título e visibilidade (útil para descobrir nomes exatos na sua versão/bancada).
- **Aplicar layout e QSS** — esconde docks padrão (Report view, Python console, Selection view, DAG view) e aplica uma folha de estilo de teste com contraste, espaçamento e bordas em docks e menus.
- **Menu contextual rápido** — atalho `Ctrl+Shift+Space` que abre um menu leve com: documento ativo, recalcular documento, ajustar visualização (Fit All) e restaurar UI original.
- **Restaurar** — desfaz tudo sem reiniciar o FreeCAD.

## Estrutura do repositório

```
Freecad_UI_UX_Experiment/
├── .gitignore
├── .mise.toml          # Python 3.11 via mise
├── README.md
├── USO.md              # exemplo de execução dentro do FreeCAD
├── pyproject.toml      # projeto uv + pytest (dependência de dev)
├── uv.lock             # dependências travadas
├── ui_lab_probe.py     # script do laboratório de UI/UX
└── tests/
    ├── test_ui_lab.py  # teste mínimo (não precisa de FreeCAD nem PySide)
    └── test_window_quick.py  # teste rápido de janela/dock (precisa de PySide6)
```

## Requisitos

- Python >= 3.10 (via [mise](https://mise.jdx.dev/) ou [uv](https://github.com/astral-sh/uv))
- FreeCAD (para usar o script dentro da aplicação)
- pytest (somente para rodar os testes)
- PySide6 (opcional, somente para o `test_window_quick.py`)

## Como instalar

```sh
cd /home/dionarley/codes-area/Freecad_UI_UX_Experiment

# Com uv (cria o .venv e instala só o pytest)
uv sync

# Com o teste de janela (instala também o PySide6; ~200 MB)
uv sync --extra window

# Com mise (instala o Python 3.11 se necessário)
mise exec python@3.11 -- uv sync
```

## Como usar (dentro do FreeCAD)

Veja `USO.md` para o exemplo completo. Resumo:

```python
from ui_lab_probe import get_lab

lab = get_lab()

# 1. Ver nomes exatos dos docks
for item in lab.list_docks():
    print(item)

# 2. Aplicar o teste (esconde docks + QSS)
lab.apply_layout_and_qss()

# 3. Abrir menu contextual (também com Ctrl+Shift+Space)
lab.open_quick_menu()

# 4. Desfazer tudo
lab.restore()
```

## Teste rápido de janela/dock (`test_window_quick.py`)

O teste em `tests/test_window_quick.py` replica o mínimo da API de janela/dock do
FreeCAD, sem precisar do FreeCAD instalado. Usa apenas PySide6 (ou PySide2) com
`QT_QPA_PLATFORM=offscreen` (sem display).

Foi modelado em três fontes do [FreeCAD/FreeCAD](https://github.com/FreeCAD/FreeCAD):

| Fonte do FreeCAD | O que foi extraído |
|---|---|
| `src/Gui/DockWindow.h` | Classe base de dock (`QWidget` + `BaseView`, métodos `onUpdate`, `getName`, `canClose`) |
| `src/Gui/DockWindowManager.h` | Singleton que gerencia `QDockWidget`: `addDockWindow`, `getDockContainer`, `registerDockWindow`, `saveState`/`loadState` |
| `src/Gui/Stylesheets/` | Padrões QSS para docks, menus, botões, etc. |

A réplica mínima (`DockWindowManager` no teste) oferece:

- `register(name, widget, area)` — registra widget num `QDockWidget`
- `get_dock(name)` / `get_widget(name)` — recupera por nome
- `set_visible(name, bool)` / `is_visible(name)` — controla visibilidade
- `hide_names(names)` / `show_names(names)` — esconde/mostra vários docks
- `apply_qss(qss)` — aplica folha de estilo na janela principal
- `list_docks()` / `save_state()` — inspeção e persistência de estado

```sh
# Roda o teste de janela (precisa do extra "window")
uv run pytest tests/test_window_quick.py -q
```

Saída esperada (com PySide6 instalado): `6 passed in 0.XXs`.

> **Nota:** este ambiente de desenvolvimento não tem `libGL.so.1`, então o PySide6 não
> pode ser importado aqui. O teste é pulado automaticamente quando PySide6 não está
> disponível. Funciona em qualquer máquina com PySide6 + OpenGL.
```

## Testes

Os testes não precisam de FreeCAD instalado e ocupam pouco espaço em disco:

```sh
uv run pytest -q
```

Saída esperada (sem PySide6): `3 passed in 0.01s`.  
Saída esperada (com PySide6 + libGL): `9 passed`.

Os testes de janela (`test_window_quick.py`) são pulados automaticamente quando
PySide6 não está instalado — não ocupam disco se não forem usados.

## Licença

Todos os docs estão sob licença CC por enquanto.
