# Instalação

Este projeto usa [uv](https://github.com/astral-sh/uv) para gerenciar
dependências e [mise](https://mise.jdx.dev/) para fixar a versão do Python.

## Pré-requisitos

- Python >= 3.10 (via `mise` ou `uv`)
- FreeCAD (para usar os scripts dentro da aplicação)
- PySide6 ou PySide2 (opcional, somente para `ui_lab_app.py`, `window_test.py`
  e testes de janela)

## Passo a passo

```sh
cd freecad-ui-ux-experiment

# 1. Instalar dependências de desenvolvimento (pytest)
uv sync

# 2. (Opcional) Instalar PySide6 para usar o app e rodar testes de janela
uv sync --extra window

# 3. Rodar os testes básicos (não precisa de PySide)
uv run pytest -q

# Com mise (instala o Python 3.11 se necessário)
mise exec python@3.11 -- uv sync
```

## Usando o script `run.sh`

```sh
./run.sh sync     # sincroniza dependências (uv sync)
./run.sh test     # roda os testes (pytest)
./run.sh window   # roda incluindo o teste de janela (uv sync --extra window)
./run.sh app      # executa o app real de UI/UX (standalone, requer PySide6)
./run.sh clean    # remove .venv e __pycache__
```

## Container (podman / docker)

```sh
podman build -t freecad-ui-lab .
podman run --rm freecad-ui-lab
```

O container roda os testes automaticamente ao iniciar.

## Nota sobre libGL

Se você estiver em um ambiente sem `libGL.so.1` (ex: NixOS, containers
mínimos), o PySide6 não pode ser importado. Nesse caso:
- Os testes básicos continuam funcionando (`3 passed`).
- Os testes de janela e o app são pulados automaticamente.
- Para rodá-los, instale `libGL` e use `uv sync --extra window`.
