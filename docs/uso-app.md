# Como usar o ui_lab_app.py (aplicação real de UI/UX)

O `ui_lab_app.py` é uma **aplicação completa** de laboratório de UI/UX, não só
um teste. Funciona dentro do FreeCAD e também em modo standalone.

## Dentro do FreeCAD

Abra o Console Python do FreeCAD:

```python
from ui_lab_app import run_in_freecad
win = run_in_freecad()
```

A janela se acopla à main window do FreeCAD e oferece:

| Aba | O que faz |
|---|---|
| **Docks** | Lista todos os `QDockWidget` da aplicação e permite mostrar/esconder cada um, individualmente ou em massa. |
| **QSS / Estilo** | Editor de folha de estilo com aplicação ao vivo na MainWindow do FreeCAD ou na janela do app. Inclui carregar/salvar arquivos `.qss`. |
| **Info / Controle** | Mostra binding Qt, status do FreeCAD (documento/objetos), e botões para recalcular documento e ajustar visualização (Fit All). |

O log integrado escreve tanto na área de texto quanto no Console Python do
FreeCAD.

## Modo standalone (fora do FreeCAD)

```sh
uv sync --extra window
uv run python ui_lab_app.py
```

Ou via script:

```sh
./run.sh app
```

Cria uma janela independente com as mesmas abas (Docks, QSS, Info) para
desenvolver e testar a interface sem precisar do FreeCAD.

## Ícone programático

A janela e o botão de teste usam um ícone desenhado com QPainter (círculo azul
com letra "F"), sem depender de arquivo de imagem externo.

## Configuração persistente

O app salva o QSS editado em `ui_lab_config.json` na raiz do projeto, para que
as customizações de estilo persistam entre sessões.
