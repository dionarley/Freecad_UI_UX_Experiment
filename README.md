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
    └── test_ui_lab.py  # teste mínimo (não precisa de FreeCAD)
```

## Requisitos

- Python >= 3.10 (via [mise](https://mise.jdx.dev/) ou [uv](https://github.com/astral-sh/uv))
- FreeCAD (para usar o script dentro da aplicação)
- pytest (somente para rodar os testes)

## Como instalar

```sh
cd /home/dionarley/codes-area/Freecad_UI_UX_Experiment

# Com uv (cria o .venv e instala só o pytest)
uv sync

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

## Testes

Os testes não precisam de FreeCAD instalado e ocupam pouco espaço em disco:

```sh
uv run pytest -q
```

Saída esperada: `3 passed in 0.01s`.

## Licença

Todos os docs estão sob licença CC por enquanto.
