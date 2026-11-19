"""Teste rápido de janela/dock, inspirado no mínimo do FreeCAD.

Modelado em:
  - src/Gui/DockWindow.h      (classe base de dock: QWidget + BaseView)
  - src/Gui/DockWindowManager.h (singleton que gerencia QDockWidget)
  - src/Gui/Stylesheets/      (padrões QSS)

Roda sem display (QT_QPA_PLATFORM=offscreen) e não precisa do FreeCAD instalado,
apenas PySide6 (ou PySide2). Para evitar ocupar disco, PySide6 é uma
dependência opcional: o teste de janela é pulado se não estiver instalado.
"""
import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest

try:
    from PySide6 import QtCore, QtGui, QtWidgets
    HAS_QT = True
except ImportError:  # pragma: no cover
    try:
        from PySide2 import QtCore, QtGui, QtWidgets  # type: ignore[no-redef,assignment]
        HAS_QT = True
    except ImportError:  # pragma: no cover
        HAS_QT = False


if HAS_QT:  # pragma: no cover

    # --- Mínimo extraído do FreeCAD (adaptado para teste autônomo) -------------

    DOCK_NAMES = {
        "Report view",
        "Python console",
        "Selection view",
        "DAG view",
    }

    TEST_QSS = """
    QDockWidget {
        titlebar-close-icon: none;
    }
    QDockWidget::title {
        padding: 5px 8px;
        font-weight: 600;
    }
    QMenu {
        padding: 4px;
        border-radius: 6px;
    }
    QMenu::item {
        padding: 5px 16px;
        border-radius: 4px;
    }
    """

    @pytest.fixture
    def app():
        """Cria uma QApplication para os testes."""
        instance = QtWidgets.QApplication.instance()
        if instance is None:
            instance = QtWidgets.QApplication([])
        return instance

    def test_cria_janela_principal(app):
        """Cria uma QMainWindow simples."""
        mw = QtWidgets.QMainWindow()
        mw.setWindowTitle("FreeCAD UI-LAB")
        assert mw.windowTitle() == "FreeCAD UI-LAB"

    def test_adiciona_dock_visivel(app):
        """Registra um QDockWidget e verifica que está visível."""
        mw = QtWidgets.QMainWindow()

        docks = {}

        def register(name, widget, area=QtCore.Qt.LeftDockWidgetArea):
            dock = QtWidgets.QDockWidget(name, mw)
            dock.setObjectName(name)
            dock.setWidget(widget)
            mw.addDockWidget(area, dock)
            docks[name] = dock
            return dock

        widget = QtWidgets.QWidget()
        dock = register("Painel Teste", widget, QtCore.Qt.LeftDockWidgetArea)
        assert dock is not None
        assert docks["Painel Teste"] is dock
        assert dock.isVisible()

    def test_esconde_docks_padrao(app):
        """Esconde docks padrão do FreeCAD."""
        mw = QtWidgets.QMainWindow()

        docks = {}
        for name in DOCK_NAMES:
            dock = QtWidgets.QDockWidget(name, mw)
            dock.setObjectName(name)
            dock.setWidget(QtWidgets.QWidget())
            mw.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)
            docks[name] = dock

        for name in DOCK_NAMES:
            docks[name].setVisible(False)

        for name in DOCK_NAMES:
            assert not docks[name].isVisible()

    def test_aplica_qss(app):
        """Aplica QSS na janela principal."""
        mw = QtWidgets.QMainWindow()
        mw.setStyleSheet(TEST_QSS)
        assert mw.styleSheet().strip()

    def test_lista_docks_retorna_info(app):
        """Lista docks com nome e visibilidade."""
        mw = QtWidgets.QMainWindow()

        dock = QtWidgets.QDockWidget("Relatório", mw)
        dock.setObjectName("Relatório")
        dock.setWidget(QtWidgets.QWidget())
        mw.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)

        info = []
        for d in mw.findChildren(QtWidgets.QDockWidget):
            info.append({
                "name": d.objectName() or d.windowTitle() or "sem nome",
                "isVisible": d.isVisible(),
            })

        assert len(info) == 1
        assert info[0]["name"] == "Relatório"

    def test_save_state_preserva_visibilidade(app):
        """Salva o estado de visibilidade de um dock."""
        mw = QtWidgets.QMainWindow()

        dock = QtWidgets.QDockWidget("Estado", mw)
        dock.setObjectName("Estado")
        dock.setWidget(QtWidgets.QWidget())
        mw.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)
        dock.setVisible(False)

        state = {}
        for d in mw.findChildren(QtWidgets.QDockWidget):
            state[d.objectName()] = d.isVisible()

        assert state["Estado"] is False
