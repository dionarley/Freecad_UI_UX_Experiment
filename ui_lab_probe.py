# This file is part of the FreeCAD UI/UX Experiment.
# It is licensed under the GNU LGPL v3. See LICENSE-CODE for details.

try:
    import FreeCAD as App
    import FreeCADGui as Gui
except ImportError:
    App = None
    Gui = None

try:
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError:
    try:
        from PySide2 import QtCore, QtGui, QtWidgets
    except ImportError:
        QtCore = None
        QtGui = None
        QtWidgets = None


# Nomes comuns de dock widgets no FreeCAD (ajuste conforme a sua versão/bancada)
DEFAULT_HIDE_DOCK_OBJECT_NAMES = {
    "Report view",
    "Python console",
    "Selection view",
    "DAG view",
}

TEST_QSS = """
/* Teste isolado de contraste, espaçamento e bordas em docks/menus */
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


class FreeCadUiLab:
    def __init__(self):
        self.mw = Gui.getMainWindow() if Gui else None
        self._saved_docks_visible = {}
        self._saved_qss = None
        self._shortcut = None
        self._applied = False

    def list_docks(self):
        """Lista todos os QDockWidget ativos com objectName, título e visibilidade."""
        if not self.mw:
            return []
        docks = self.mw.findChildren(QtWidgets.QDockWidget)
        info = []
        for d in docks:
            info.append({
                "objectName": d.objectName(),
                "windowTitle": d.windowTitle(),
                "isVisible": d.isVisible(),
            })
        return info

    def apply_layout_and_qss(self, hide_names=None, qss=TEST_QSS):
        """Salva o estado atual e aplica ocultação de docks + QSS de teste."""
        if not self.mw:
            App.Console.PrintError("[UI-LAB] MainWindow não disponível.\n")
            return

        target_names = set(hide_names) if hide_names is not None else DEFAULT_HIDE_DOCK_OBJECT_NAMES

        # Salva apenas na primeira aplicação para preservar o baseline real
        if not self._applied:
            self._saved_qss = self.mw.styleSheet()
            for d in self.mw.findChildren(QtWidgets.QDockWidget):
                key = d.objectName() or id(d)
                self._saved_docks_visible[key] = (d, d.isVisible())

        for _, (dock, _) in self._saved_docks_visible.items():
            if dock.objectName() in target_names:
                dock.setVisible(False)

        if qss:
            merged = (self._saved_qss or "") + "\n" + qss
            self.mw.setStyleSheet(merged)

        self._install_context_shortcut()
        self._applied = True
        App.Console.PrintMessage("[UI-LAB] Layout e QSS de teste aplicados.\n")

    def restore(self):
        """Restaura visibilidade original dos docks e stylesheet anterior."""
        if not self.mw:
            return

        for _, (dock, was_visible) in self._saved_docks_visible.items():
            try:
                dock.setVisible(was_visible)
            except RuntimeError:
                pass

        if self._saved_qss is not None:
            self.mw.setStyleSheet(self._saved_qss)

        self._remove_context_shortcut()
        self._applied = False
        App.Console.PrintMessage("[UI-LAB] Estado original restaurado.\n")

    def _install_context_shortcut(self):
        """Registra um atalho rápido (Ctrl+Shift+Space) para abrir um menu contextual."""
        if self._shortcut is not None:
            return
        seq = QtGui.QKeySequence("Ctrl+Shift+Space")
        sc = QtGui.QShortcut(seq, self.mw)
        sc.setContext(QtCore.Qt.ApplicationShortcut)
        sc.activated.connect(self.open_quick_menu)
        self._shortcut = sc

    def _remove_context_shortcut(self):
        if self._shortcut is not None:
            self._shortcut.setParent(None)
            self._shortcut.deleteLater()
            self._shortcut = None

    def open_quick_menu(self):
        """Abre um menu contextual leve na posição atual do cursor."""
        if not self.mw:
            return

        menu = QtWidgets.QMenu(self.mw)
        menu.setObjectName("UiLabQuickMenu")

        act_active_doc = menu.addAction("Documento ativo")
        act_active_doc.setEnabled(False)
        doc = App.activeDocument()
        if doc:
            act_active_doc.setText(f"Doc: {doc.Name} ({len(doc.Objects)} objs)")
        else:
            act_active_doc.setText("Nenhum documento aberto")

        menu.addSeparator()

        act_recompute = menu.addAction("Recalcular documento")
        act_recompute.setEnabled(doc is not None)
        act_recompute.triggered.connect(lambda: doc.recompute() if doc else None)

        act_fit = menu.addAction("Ajustar visualização (Fit All)")
        act_fit.triggered.connect(lambda: Gui.SendMsgToActiveView("ViewFit"))

        menu.addSeparator()

        act_restore = menu.addAction("Restaurar UI original")
        act_restore.triggered.connect(self.restore)

        pos = QtGui.QCursor.pos()
        menu.exec(pos) if hasattr(menu, "exec") else menu.exec_(pos)


def get_lab():
    if App is None:
        return FreeCadUiLab()
    lab = getattr(App, "_FC_UI_LAB", None)
    if lab is None:
        lab = FreeCadUiLab()
        setattr(App, "_FC_UI_LAB", lab)
    return lab
