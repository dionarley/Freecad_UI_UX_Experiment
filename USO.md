# Uso — exemplo de execução

O exemplo abaixo **só roda dentro do FreeCAD** (onde `App` e `Gui` estão
disponíveis). Ele está fora de `ui_lab_probe.py` para não impedir a importação
do módulo fora do FreeCAD.

## 1. Inspecionar nomes exatos dos docks antes de esconder

```python
from ui_lab_probe import get_lab

lab = get_lab()
for item in lab.list_docks():
    print(item)
```

## 2. Aplicar o teste (descomente para rodar imediatamente)

```python
lab.apply_layout_and_qss()   # esconde docks padrão e aplica QSS de teste
lab.open_quick_menu()        # abre menu contextual (Ctrl+Shift+Space)
```

## 3. Desfazer tudo sem reiniciar o FreeCAD

```python
lab.restore()   # restaura visibilidade original dos docks e stylesheet anterior
```

### Atalho rápido

Após `apply_layout_and_qss()`, pressione **Ctrl+Shift+Space** para abrir o menu
contextual leve com: documento ativo, recalcular documento, ajustar
visualização (Fit All) e restaurar UI original.
