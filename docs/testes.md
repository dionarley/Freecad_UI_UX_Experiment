# Testes

O projeto usa [pytest](https://docs.pytest.org/) com testes mínimos que não
ocupam muito espaço em disco.

## Rodar os testes

```sh
uv run pytest -q
```

Saída esperada (sem PySide6): `3 passed in 0.01s`.  
Saída esperada (com PySide6 + libGL): `21 passed`.

## Estrutura dos testes

| Arquivo | O que testa |
|---|---|
| `tests/test_ui_lab.py` | Teste mínimo: importa `ui_lab_probe.py` sem FreeCAD, valida constantes e `get_lab()`. |
| `tests/test_window_quick.py` | Teste rápido de janela/dock: cria QMainWindow, registra QDockWidget, aplica QSS, salva estado. Requer PySide6. |
| `tests/test_app.py` | Teste do `ui_lab_app.py`: instancia a janela, verifica abas, log, editor QSS. Requer PySide6. |
| `tests/test_dependencies.py` | Verifica que os módulos importam sem erro quando PySide está disponível. Requer PySide6. |

## Testes de janela (requerem PySide6)

Os testes de `test_window_quick.py`, `test_app.py` e parte de
`test_dependencies.py` precisam de PySide6 e de `libGL.so.1`. Em ambientes sem
`libGL` (ex: NixOS), eles são pulados automaticamente:

```sh
# Instalar PySide6
uv sync --extra window

# Rodar todos os testes (incluindo janela)
uv run pytest -q
```

## Testes básicos (sem PySide)

Os 3 testes de `test_ui_lab.py` rodam sem qualquer dependência extra:

```sh
uv run pytest tests/test_ui_lab.py -q
```

## Via run.sh

```sh
./run.sh test     # apenas testes básicos
./run.sh window   # instala PySide6 e roda todos os testes
```
