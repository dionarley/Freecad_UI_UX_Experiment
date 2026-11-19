# Como usar o ui_lab_probe.py (dentro do FreeCAD)

O script `ui_lab_probe.py` é um pequeno "laboratório" de UI que roda **dentro
do FreeCAD**. Ele não modifica nenhum arquivo original do repositório.

## Carregando o script

Abra o Console Python do FreeCAD e execute:

```python
from ui_lab_probe import get_lab

lab = get_lab()
```

## Funcionalidades

### 1. Listar docks

Mostra todos os `QDockWidget` ativos com nome, título e visibilidade:

```python
for item in lab.list_docks():
    print(item)
```

### 2. Aplicar layout e QSS

Esconde docks padrão (Report view, Python console, Selection view, DAG view) e
aplica uma folha de estilo de teste:

```python
lab.apply_layout_and_qss()
```

### 3. Menu contextual rápido

Atalho `Ctrl+Shift+Space` abre um menu leve com:

- Documento ativo
- Recalcular documento
- Ajustar visualização (Fit All)
- Restaurar UI original

Ou chame diretamente:

```python
lab.open_quick_menu()
```

### 4. Restaurar

Desfaz tudo (visibilidade e stylesheet) sem reiniciar o FreeCAD:

```python
lab.restore()
```

## Exemplo completo (USO.md)

Veja o arquivo `USO.md` na raiz do repositório para um exemplo passo a passo.
