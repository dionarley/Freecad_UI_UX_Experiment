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
    from PySide6 import QtCore, QtWidgets
    HAS_QT = True
except ImportError:  # pragma: no cover
    try:
        from PySide2 import QtCore, QtWidgets  # type: ignore[no-redef,assignment]
        HAS_QT = True
    except ImportError:  # pragma: no cover
        QtCore = None
        QtWidgets = None
        HAS_QT = False


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


if HAS_QT:  # pragma: no cover

    class DockWindowManager:
        """Réplica mínima do Gui::DockWindowManager do FreeCAD.

        Gerencia QDockWidgets dentro de um QMainWindow, com registro por nome,
        área de encaixe, visibilidade e persistência de estado.
        """

        def __init__(self, main_window):
            self._mw = main_window
            self._docks = {}          # name -> QDockWidget
            self._widgets = {}        # name -> QWidget (conteúdo)
            self._areas = {}          # name -> Qt::DockWidgetArea

        def register(self, name, widget, area=QtCore.Qt.LeftDockWidgetArea):
            """Registra um widget e o coloca num QDockWidget na janela principal."""
            dock = QtWidgets.QDockWidget(name, self._mw)
            dock.setObjectName(name)
            dock.setWidget(widget)
            self._mw.addDockWidget(area, dock)
            self._docks[name] = dock
            self._widgets[name] = widget
            self._areas[name] = area
            return dock

        def get_dock(self, name):
            """Retorna o QDockWidget pelo nome."""
            return self._docks.get(name)

        def get_widget(self, name):
            """Retorna o widget de conteúdo pelo nome."""
            return self._widgets.get(name)

        def set_visible(self, name, visible):
            dock = self._docks.get(name)
            if dock is not None:
                dock.setVisible(visible)

        def is_visible(self, name):
            dock = self._docks.get(name)
            return dock.isVisible() if dock is not None else False

        def hide_names(self, names):
            for name in names:
                self.set_visible(name, False)

        def show_names(self, names):
            for name in names:
                self.set_visible(name, True)

        def apply_qss(self, qss):
            self._mw.setStyleSheet(qss)

        def list_docks(self):
            info = []
            for name, dock in self._docks.items():
                info.append({
                    "name": name,
                    "objectName": dock.objectName(),
                    "isVisible": dock.isVisible(),
                    "area": self._areas[name],
                })
            return info

        def save_state(self):
            return {
                name: {"area": str(area), "visible": dock.isVisible()}
                for name, (dock, area) in {
                    n: (self._docks[n], self._areas[n]) for n in self._docks
                }.items()
            }


# --- Testes ----------------------------------------------------------------

def _app():
    return QtWidgets.QApplication.instance() or QtWidgets.QApplication([])


@pytest.mark.skipif(not HAS_QT, reason="PySide6/PySide2 não instalado")
def test_cria_janela_principal():
    _app()
    mw = QtWidgets.QMainWindow()
    mw.setWindowTitle("FreeCAD UI-LAB")
    assert mw.windowTitle() == "FreeCAD UI-LAB"


@pytest.mark.skipif(not HAS_QT, reason="PySide6/PySide2 não instalado")
def test_adiciona_dock_visivel():
    _app()
    mw = QtWidgets.QMainWindow()
    mgr = DockWindowManager(mw)
    widget = QtWidgets.QWidget()
    dock = mgr.register("Painel Teste", widget, QtCore.Qt.LeftDockWidgetArea)
    assert dock is not None
    assert mgr.get_dock("Painel Teste") is dock
    assert mgr.get_widget("Painel Teste") is widget
    assert mgr.is_visible("Painel Teste")


@pytest.mark.skipif(not HAS_QT, reason="PySide6/PySide2 não instalado")
def test_esconde_docks_padrao():
    _app()
    mw = QtWidgets.QMainWindow()
    mgr = DockWindowManager(mw)
    for name in DOCK_NAMES:
        mgr.register(name, QtWidgets.QWidget())
    mgr.hide_names(DOCK_NAMES)
    for name in DOCK_NAMES:
        assert not mgr.is_visible(name)


@pytest.mark.skipif(not HAS_QT, reason="PySide6/PySide2 não instalado")
def test_aplica_qss():
    _app()
    mw = QtWidgets.QMainWindow()
    mgr = DockWindowManager(mw)
    mgr.register("Painel QSS", QtWidgets.QWidget())
    mgr.apply_qss(TEST_QSS)
    assert mw.styleSheet().strip()


@pytest.mark.skipif(not HAS_QT, reason="PySide6/PySide2 não instalado")
def test_lista_docks_retorna_info():
    _app()
    mw = QtWidgets.QMainWindow()
    mgr = DockWindowManager(mw)
    mgr.register("Relatório", QtWidgets.QWidget())
    info = mgr.list_docks()
    assert len(info) == 1
    assert info[0]["name"] == "Relatório"


@pytest.mark.skipif(not HAS_QT, reason="PySide6/PySide2 não instalado")
def test_save_state_preserva_visibilidade():
    _app()
    mw = QtWidgets.QMainWindow()
    mgr = DockWindowManager(mw)
    mgr.register("Estado", QtWidgets.QWidget())
    mgr.set_visible("Estado", False)
    state = mgr.save_state()
    assert state["Estado"]["visible"] is False
