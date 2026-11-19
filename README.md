# FreeCAD UI/UX Experiment

<!-- English -->
## Overview

This repository is a laboratory of UI/UX experiments for FreeCAD. The goal is to
test whether FreeCAD is viable for customizing the interface (hiding docks,
applying QSS, quick context menu, managing docks, editing styles live) and, if
it works well, contribute improvements to the community.

## Visão Geral (Português)

Este repositório é um laboratório de experimentos de UI/UX para o FreeCAD. O
objetivo é testar se o FreeCAD é viável para customizar a interface (esconder
docks, aplicar QSS, menu contextual rápido, gerenciar docks, editar estilos ao
vivo) e, se der certo, enviar melhorias para a comunidade.

---

<!-- English -->
## What this project does

The script `ui_lab_probe.py` creates a small UI laboratory inside FreeCAD:

- **List docks** — shows all active `QDockWidget` with name, title, and visibility (useful to find exact names in your version/workbench).
- **Apply layout and QSS** — hides default docks (Report view, Python console, Selection view, DAG view) and applies a test stylesheet with contrast, spacing, and borders for docks and menus.
- **Quick context menu** — shortcut `Ctrl+Shift+Space` opens a light menu with: active document, recompute document, fit all view, and restore original UI.
- **Restore** — undoes everything (visibility and stylesheet) without restarting FreeCAD.

The file `ui_lab_app.py` is a **real UI/UX application** (not just a test),
standalone and compatible with FreeCAD:

- **Docks tab** — lists and controls visibility of all application docks.
- **QSS / Style tab** — live stylesheet editor applied to the FreeCAD MainWindow or the app window.
- **Info / Control tab** — FreeCAD status, buttons to recompute document and fit all view.
- **Integrated log** — writes to the FreeCAD Python Console when run inside it.
- Works **standalone** (without FreeCAD) and **inside FreeCAD**.

## Visão Geral (Português)

O script `ui_lab_probe.py` cria um pequeno "laboratório" de UI dentro do FreeCAD:

- **Listar docks** — mostra todos os `QDockWidget` ativos com nome, título e visibilidade (útil para descobrir nomes exatos na sua versão/bancada).
- **Aplicar layout e QSS** — esconde docks padrão (Report view, Python console, Selection view, DAG view) e aplica uma folha de estilo de teste com contraste, espaçamento e bordas para docks e menus.
- **Menu contextual rápido** — atalho `Ctrl+Shift+Space` abre um menu leve com: documento ativo, recalcular documento, ajustar visualização (Fit All) e restaurar UI original.
- **Restaurar** — desfaz tudo (visibilidade e stylesheet) sem reiniciar o FreeCAD.

O arquivo `ui_lab_app.py` é uma **aplicação real de UI/UX** (não só um teste),
autônoma e compatível com o FreeCAD:

- **Aba Docks** — lista e controla a visibilidade de todos os docks da aplicação.
- **Aba QSS / Estilo** — editor de folha de estilo com aplicação ao vivo na MainWindow do FreeCAD ou na janela do app.
- **Aba Info / Controle** — status do FreeCAD, botões para recalcular documento e ajustar visualização (Fit All).
- **Log integrado** — escreve no Console Python do FreeCAD quando rodado dentro dele.
- Funciona **standalone** (sem FreeCAD) e **dentro do FreeCAD**.

---

## Repository structure

```
freecad-ui-ux-experiment/
├── .gitignore
├── .mise.toml          # Python 3.11 via mise (optional)
├── LICENSE             # CC BY 4.0
├── README.md
├── docs/index.html          # bilingual project overview (En/PT-BR)
├── USO.md              # usage example inside FreeCAD (PT-BR)
├── USO_EN.md           # usage example inside FreeCAD (English)
├── pyproject.toml      # uv project + pytest (dev dependency)
├── uv.lock             # locked dependencies
├── ui_lab_probe.py     # UI laboratory script (probe)
├── ui_lab_app.py       # real UI/UX application
├── window_test.py      # test window with button
├── Dockerfile          # minimal container for tests
├── .dockerignore
├── run.sh              # execution script (sync, test, window, app, clean)
├── docs/               # detailed documentation
│   ├── visao-geral.md  # project overview (PT-BR)
│   ├── overview.md     # project overview (English)
│   ├── instalacao.md   # installation (PT-BR)
│   ├── installation.md # installation (English)
│   ├── uso-probe.md    # how to use ui_lab_probe.py (PT-BR)
│   ├── use-probe.md    # how to use ui_lab_probe.py (English)
│   ├── uso-app.md      # how to use ui_lab_app.py (PT-BR)
│   ├── use-app.md      # how to use ui_lab_app.py (English)
│   ├── testes.md       # tests (PT-BR)
│   ├── tests.md        # tests (English)
│   └── arquitetura.md  # architecture (PT-BR/English)
└── tests/
    ├── test_ui_lab.py              # minimal test (no FreeCAD or PySide needed)
    ├── test_window_quick.py        # quick window/dock test (needs PySide6)
    ├── test_app.py                 # app test (needs PySide6)
    └── test_dependencies.py        # dependency check (needs PySide6)
```

## Estrutura do repositório

```
freecad-ui-ux-experiment/
├── .gitignore
├── .mise.toml          # Python 3.11 via mise (opcional)
├── LICENSE             # CC BY 4.0
├── README.md
├── docs/index.html          # visão geral bilíngue do projeto (En/PT-BR)
├── USO.md              # exemplo de uso dentro do FreeCAD (PT-BR)
├── USO_EN.md           # exemplo de uso dentro do FreeCAD (Inglês)
├── pyproject.toml      # projeto uv + pytest (dependência de dev)
├── uv.lock             # dependências travadas
├── ui_lab_probe.py     # script do laboratório de UI (probe)
├── ui_lab_app.py       # aplicação real de UI/UX
├── window_test.py      # janela de teste com botão
├── Dockerfile          # container mínimo para testes
├── .dockerignore
├── run.sh              # script de execução (sync, test, window, app, clean)
├── docs/               # documentação detalhada
│   ├── visao-geral.md  # visão geral do projeto (PT-BR)
│   ├── overview.md     # visão geral do projeto (Inglês)
│   ├── instalacao.md   # instalação (PT-BR)
│   ├── installation.md # instalação (Inglês)
│   ├── uso-probe.md    # como usar o ui_lab_probe.py (PT-BR)
│   ├── use-probe.md    # como usar o ui_lab_probe.py (Inglês)
│   ├── uso-app.md      # como usar o ui_lab_app.py (PT-BR)
│   ├── use-app.md      # como usar o ui_lab_app.py (Inglês)
│   ├── testes.md       # testes (PT-BR)
│   ├── tests.md        # testes (Inglês)
│   └── arquitetura.md  # arquitetura (PT-BR/Inglês)
└── tests/
    ├── test_ui_lab.py              # teste mínimo (não precisa de FreeCAD nem PySide)
    ├── test_window_quick.py        # teste rápido de janela/dock (precisa de PySide6)
    ├── test_app.py                 # teste do app (precisa de PySide6)
    └── test_dependencies.py        # verificação de dependências (precisa de PySide6)
```

## Requirements / Requisitos

- Python >= 3.10 (via [mise](https://mise.jdx.dev/) or [uv](https://github.com/astral-sh/uv))
- FreeCAD (to use the script inside the application / para usar o script dentro da aplicação)
- pytest (only to run tests / somente para rodar os testes)
- PySide6 (optional, only for `test_window_quick.py`, `window_test.py` and `ui_lab_app.py` / opcional, somente para `test_window_quick.py`, `window_test.py` e `ui_lab_app.py`)

## Installation / Instalação

```sh
# Clone or download this repository, then:
cd freecad-ui-ux-experiment

# With uv (creates .venv and installs only pytest)
uv sync

# With window/app support (also installs PySide6; ~200 MB)
uv sync --extra window

# With mise (installs Python 3.11 if needed)
mise exec python@3.11 -- uv sync
```

```sh
# Clone ou baixe este repositório, então:
cd freecad-ui-ux-experiment

# Com uv (cria .venv e instala apenas o pytest)
uv sync

# Com suporte a janela/app (instala também o PySide6; ~200 MB)
uv sync --extra window

# Com mise (instala o Python 3.11 se necessário)
mise exec python@3.11 -- uv sync
```

## Using the `run.sh` script / Usando o script `run.sh`

```sh
./run.sh sync     # sync dependencies (uv sync)
./run.sh test     # run tests (pytest)
./run.sh window   # run including window test (uv sync --extra window)
./run.sh app      # run the real UI/UX app (standalone, needs PySide6)
./run.sh clean    # remove .venv and __pycache__
```

```sh
./run.sh sync     # sincroniza dependências (uv sync)
./run.sh test     # roda os testes (pytest)
./run.sh window   # roda incluindo o teste de janela (uv sync --extra window)
./run.sh app      # executa o app real de UI/UX (standalone, requer PySide6)
./run.sh clean    # remove .venv e __pycache__
```

## How to use (inside FreeCAD) / Como usar (dentro do FreeCAD)

See `USO.md` (PT-BR) or `USO_EN.md` (English) for the complete `ui_lab_probe.py`
example. Summary:

```python
from ui_lab_probe import get_lab

lab = get_lab()

# 1. List dock names
for item in lab.list_docks():
    print(item)

# 2. Apply test (hide docks + QSS)
lab.apply_layout_and_qss()

# 3. Open context menu (also Ctrl+Shift+Space)
lab.open_quick_menu()

# 4. Undo everything
lab.restore()
```

Veja `USO.md` (PT-BR) ou `USO_EN.md` (Inglês) para o exemplo completo do
`ui_lab_probe.py`. Resumo:

```python
from ui_lab_probe import get_lab

lab = get_lab()

# 1. Listar nomes dos docks
for item in lab.list_docks():
    print(item)

# 2. Aplicar teste (esconder docks + QSS)
lab.apply_layout_and_qss()

# 3. Abrir menu contextual (também Ctrl+Shift+Space)
lab.open_quick_menu()

# 4. Desfazer tudo
lab.restore()
```

For the **real app** (`ui_lab_app.py`), open the FreeCAD Python Console:

```python
from ui_lab_app import run_in_freecad
win = run_in_freecad()
```

O app se acopla à janela principal do FreeCAD e oferece gerenciamento de docks,
editor de QSS ao vivo e controles de informação.

Para o **app real** (`ui_lab_app.py`), abra o Console Python do FreeCAD:

```python
from ui_lab_app import run_in_freecad
win = run_in_freecad()
```

O app se acopla à janela principal do FreeCAD e oferece gerenciamento de docks,
editor de QSS ao vivo e controles de informação.

## Quick window/dock test (`test_window_quick.py`)

The test in `tests/test_window_quick.py` replicates the minimum FreeCAD
window/dock API, without needing FreeCAD installed. It uses only PySide6 (or
PySide2) with `QT_QPA_PLATFORM=offscreen` (no display).

Modeled on three sources from [FreeCAD/FreeCAD](https://github.com/FreeCAD/FreeCAD):

| FreeCAD source | What was extracted |
|---|---|
| `src/Gui/DockWindow.h` | Dock base class (`QWidget` + `BaseView`, methods `onUpdate`, `getName`, `canClose`) |
| `src/Gui/DockWindowManager.h` | Singleton managing `QDockWidget`: `addDockWindow`, `getDockContainer`, `registerDockWindow`, `saveState`/`loadState` |
| `src/Gui/Stylesheets/` | QSS patterns for docks, menus, buttons, etc. |

The minimal replica (`DockWindowManager` in the test) offers:

- `register(name, widget, area)` — registers a widget in a `QDockWidget`
- `get_dock(name)` / `get_widget(name)` — retrieves by name
- `set_visible(name, bool)` / `is_visible(name)` — controls visibility
- `hide_names(names)` / `show_names(names)` — hides/shows multiple docks
- `apply_qss(qss)` — applies stylesheet to the main window
- `list_docks()` / `save_state()` — inspection and state persistence

```sh
# Run window test (needs the "window" extra)
uv run pytest tests/test_window_quick.py -q
```

Expected output (with PySide6 installed): `6 passed in 0.XXs`.

> **Note:** This development environment does not have `libGL.so.1`, so PySide6
> cannot be imported here. Tests are automatically skipped when PySide6 is not
> available. Works on any machine with PySide6 + OpenGL.

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

> **Nota:** este ambiente de desenvolvimento não tem `libGL.so.1`, então o PySide6
> não pode ser importado aqui. O teste é pulado automaticamente quando PySide6 não
> está disponível. Funciona em qualquer máquina com PySide6 + OpenGL.

## Tests / Testes

Tests do not need FreeCAD installed and take little disk space:

```sh
uv run pytest -q
```

Expected output (without PySide6): `3 passed in 0.01s`.  
Expected output (with PySide6 + libGL): all tests pass.

Window tests (`test_window_quick.py`) are automatically skipped when PySide6 is
not installed — they do not use disk if unused.

Os testes não precisam do FreeCAD instalado e ocupam pouco espaço em disco:

```sh
uv run pytest -q
```

Saída esperada (sem PySide6): `3 passed in 0.01s`.  
Saída esperada (com PySide6 + libGL): todos os testes passam.

Os testes de janela (`test_window_quick.py`) são pulados automaticamente quando
PySide6 não está instalado — não ocupam disco se não forem usados.

## Run the real app (standalone) / Executar o app real (standalone)

Outside FreeCAD, to develop and test the UI without the application:

```sh
./run.sh app
# or
uv sync --extra window && uv run python ui_lab_app.py
```

Fora do FreeCAD, para desenvolver e testar a UI sem precisar do aplicativo:

```sh
./run.sh app
# ou
uv sync --extra window && uv run python ui_lab_app.py
```

## Container (podman / docker)

```sh
podman build -t freecad-ui-lab .
podman run --rm freecad-ui-lab
```

The container runs the tests automatically when it starts.

## Container (podman / docker)

```sh
podman build -t freecad-ui-lab .
podman run --rm freecad-ui-lab
```

O container roda os testes automaticamente ao iniciar.

## Documentation / Documentação

Detailed documentation in `docs/`:

| File | Description |
|---|---|
| `docs/overview.md` | Project overview (English) |
| `docs/visao-geral.md` | Visão geral do projeto (PT-BR) |
| `docs/installation.md` | Installation (English) |
| `docs/instalacao.md` | Instalação (PT-BR) |
| `docs/use-probe.md` | How to use `ui_lab_probe.py` (English) |
| `docs/uso-probe.md` | Como usar o `ui_lab_probe.py` (PT-BR) |
| `docs/use-app.md` | How to use `ui_lab_app.py` (English) |
| `docs/uso-app.md` | Como usar o `ui_lab_app.py` (PT-BR) |
| `docs/tests.md` | How to run tests (English) |
| `docs/testes.md` | Como rodar os testes (PT-BR) |
| `docs/arquitetura.md` | Architecture and dependencies (PT-BR/English) |

Documentação detalhada em `docs/`:

| Arquivo | Descrição |
|---|---|
| `docs/overview.md` | Visão geral do projeto (Inglês) |
| `docs/visao-geral.md` | Visão geral do projeto (PT-BR) |
| `docs/installation.md` | Instalação (Inglês) |
| `docs/instalacao.md` | Instalação (PT-BR) |
| `docs/use-probe.md` | Como usar o `ui_lab_probe.py` (Inglês) |
| `docs/uso-probe.md` | Como usar o `ui_lab_probe.py` (PT-BR) |
| `docs/use-app.md` | Como usar o `ui_lab_app.py` (Inglês) |
| `docs/uso-app.md` | Como usar o `ui_lab_app.py` (PT-BR) |
| `docs/tests.md` | Como rodar os testes (Inglês) |
| `docs/testes.md` | Como rodar os testes (PT-BR) |
| `docs/arquitetura.md` | Arquitetura e dependências (PT-BR/Inglês) |

## Troubleshooting / Solução de problemas

### "PySide6 ou PySide2 não instalado. Rode: uv sync --extra window"

Este erro acontece quando você tenta abrir a janela (`window_test.py` ou
`ui_lab_app.py`) sem ter o PySide6 instalado. Corrija com:

```sh
uv sync --extra window
uv run python ui_lab_app.py   # ou window_test.py
```

Ou use o script:

```sh
./run.sh app
```

### PySide6 instalado mas não pode ser importado (erro `libGL.so.1`)

Se você instalou o PySide6 mas recebe um erro como
`ImportError: libGL.so.1: cannot open shared object file`, o seu sistema
está faltando bibliotecas OpenGL. Instale-as:

- **Debian/Ubuntu:** `sudo apt-get install libgl1-mesa-glx`
- **Fedora:** `sudo dnf install mesa-libGL`
- **Arch:** `sudo pacman -S libgl`
- **NixOS:** adicione `mesa` ou `libgl` ao seu `environment.systemPackages`

Após instalar, rode novamente:

```sh
uv sync --extra window
./run.sh app
```

## Licenses / Licenças

### Código (Python) — GNU LGPL v3

Todos os arquivos Python (`ui_lab_probe.py`, `ui_lab_app.py`, `window_test.py`,
`tests/`) estão licenciados sob a **GNU Lesser General Public License v3.0**.
Veja o arquivo `LICENSE-CODE` para o texto completo.

Isso é compatível com o FreeCAD (que usa LGPL), permitindo que o código seja
integrado ou vinculado ao FreeCAD sem restrições adicionais.

LGPL v3 summary: você pode usar, modificar e distribuir o código, inclusive em
produtos proprietários, desde que as modificações na biblioteca (ou partes
cobertas pela LGPL) sejam disponibilizadas sob a mesma licença.

### Documentação — CC BY 4.0

Toda a documentação (`README.md`, `docs/`, `docs/index.html`, `USO.md`,
`USO_EN.md`) está licenciada sob **Creative Commons Attribution 4.0
International (CC BY 4.0)**. Veja o arquivo `LICENSE` para o texto completo.

CC BY 4.0 summary: você é livre para compartilhar e adaptar a documentação,
mesmo para fins comerciais, desde que dê o crédito apropriado, forneça um link
para a licença e indique se foram feitas alterações.

## Estrutura de arquivos atualizada

```
freecad-ui-ux-experiment/
├── .gitignore
├── .mise.toml          # Python 3.11 via mise (optional)
├── LICENSE             # CC BY 4.0 (documentação)
├── LICENSE-CODE        # GNU LGPL v3 (código Python)
├── README.md
├── pyproject.toml      # projeto uv + pytest (dependência de dev)
├── uv.lock             # dependências travadas
├── ui_lab_probe.py     # UI laboratory script (probe) — LGPL
├── ui_lab_app.py       # real UI/UX application — LGPL
├── window_test.py      # test window with button — LGPL
├── Dockerfile          # minimal container for tests
├── .dockerignore
├── run.sh              # execution script (sync, test, window, app, clean)
├── docs/               # detailed documentation (CC BY 4.0)
│   ├── docs/index.html      # bilingual project overview (En/PT-BR)
│   ├── overview.md     # project overview (English)
│   ├── visao-geral.md  # visão geral do projeto (PT-BR)
│   ├── installation.md # installation (English)
│   ├── instalacao.md   # instalação (PT-BR)
│   ├── use-probe.md    # how to use ui_lab_probe.py (English)
│   ├── uso-probe.md    # como usar o ui_lab_probe.py (PT-BR)
│   ├── use-app.md      # how to use ui_lab_app.py (English)
│   ├── uso-app.md      # como usar o ui_lab_app.py (PT-BR)
│   ├── tests.md        # how to run tests (English)
│   ├── testes.md       # como rodar os testes (PT-BR)
│   └── arquitetura.md  # architecture and dependencies (PT-BR/English)
├── USO.md              # exemplo de uso dentro do FreeCAD (PT-BR)
├── USO_EN.md           # exemplo de uso dentro do FreeCAD (English)
└── tests/
    ├── test_ui_lab.py              # minimal test (no FreeCAD or PySide needed) — LGPL
    ├── test_window_quick.py        # quick window/dock test (needs PySide6) — LGPL
    ├── test_app.py                 # app test (needs PySide6) — LGPL
    └── test_dependencies.py        # dependency check (needs PySide6) — LGPL
```

## Estrutura do repositório (Português)

```
freecad-ui-ux-experiment/
├── .gitignore
├── .mise.toml          # Python 3.11 via mise (opcional)
├── LICENSE             # CC BY 4.0 (documentação)
├── LICENSE-CODE        # GNU LGPL v3 (código Python)
├── README.md
├── pyproject.toml      # projeto uv + pytest (dependência de dev)
├── uv.lock             # dependências travadas
├── ui_lab_probe.py     # script do laboratório de UI (probe) — LGPL
├── ui_lab_app.py       # aplicação real de UI/UX — LGPL
├── window_test.py      # janela de teste com botão — LGPL
├── Dockerfile          # container mínimo para testes
├── .dockerignore
├── run.sh              # script de execução (sync, test, window, app, clean)
├── docs/               # documentação detalhada (CC BY 4.0)
│   ├── docs/index.html      # visão geral bilíngue do projeto (En/PT-BR)
│   ├── overview.md     # visão geral do projeto (Inglês)
│   ├── visao-geral.md  # visão geral do projeto (PT-BR)
│   ├── installation.md # instalação (Inglês)
│   ├── instalacao.md   # instalação (PT-BR)
│   ├── use-probe.md    # como usar o ui_lab_probe.py (Inglês)
│   ├── uso-probe.md    # como usar o ui_lab_probe.py (PT-BR)
│   ├── use-app.md      # como usar o ui_lab_app.py (Inglês)
│   ├── uso-app.md      # como usar o ui_lab_app.py (PT-BR)
│   ├── tests.md        # como rodar os testes (Inglês)
│   ├── testes.md       # como rodar os testes (PT-BR)
│   └── arquitetura.md  # arquitetura e dependências (PT-BR/Inglês)
├── USO.md              # exemplo de uso dentro do FreeCAD (PT-BR)
├── USO_EN.md           # exemplo de uso dentro do FreeCAD (Inglês)
└── tests/
    ├── test_ui_lab.py              # teste mínimo (não precisa de FreeCAD nem PySide) — LGPL
    ├── test_window_quick.py        # teste rápido de janela/dock (precisa de PySide6) — LGPL
    ├── test_app.py                 # teste do app (precisa de PySide6) — LGPL
    └── test_dependencies.py        # verificação de dependências (precisa de PySide6) — LGPL
```
