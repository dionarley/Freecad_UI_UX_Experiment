"""FreeCAD UI-LAB — Aplicação real de laboratório de UI/UX.

Este arquivo é autônomo e **não modifica** `ui_lab_probe.py` nem qualquer outro
código original do repositório.

Funciona de duas formas:
1. Dentro do FreeCAD: anexa à janela principal, lista/esconde docks reais,
   edita o QSS da aplicação em tempo real e escreve no Console Python.
2. Fora do FreeCAD (standalone): cria sua própria janela com uma simulação
   de docks, para desenvolver e testar a UI sem precisar do FreeCAD instalado.

Compatível com PySide6 (FreeCAD >= 1.0) e PySide2 (FreeCAD < 1.0).
Se PySide não estiver instalado, o módulo pode ser importado sem erro, mas
qualquer tentativa de instanciar a janela lançará ModuleNotFoundError com
mensagem clara.
"""

import json
import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

try:
    from PySide6 import QtCore, QtGui, QtWidgets
    QT_BINDING = "PySide6"
    HAS_QT = True
except ImportError:  # pragma: no cover
    try:
        from PySide2 import QtCore, QtGui, QtWidgets  # type: ignore[no-redef,assignment]
        QT_BINDING = "PySide2"
        HAS_QT = True
    except ImportError:
        QtCore = None
        QtGui = None
        QtWidgets = None
        QT_BINDING = None
        HAS_QT = False

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "ui_lab_config.json")

# Nomes comuns de docks no FreeCAD (ajuste conforme sua versão/bancada)
DEFAULT_DOCK_NAMES = {
    "Report view",
    "Python console",
    "Selection view",
    "DAG view",
}

# QSS inicial de exemplo
DEFAULT_QSS = """
/* FreeCAD UI-LAB — QSS de teste */
QDockWidget {
    titlebar-close-icon: none;
}
QDockWidget::title {
    padding: 6px 10px;
    font-weight: 600;
    background: #2d2d2d;
    color: #ffffff;
}
QMenu {
    padding: 4px;
    border: 1px solid #555555;
    border-radius: 6px;
    background: #3a3a3a;
}
QMenu::item {
    padding: 6px 18px;
    border-radius: 4px;
    color: #ffffff;
}
QMenu::item:selected {
    background: #007acc;
}
QPushButton {
    padding: 6px 14px;
    border-radius: 4px;
    background: #3a3a3a;
    border: 1px solid #555555;
    color: #ffffff;
}
QPushButton:hover {
    background: #4a4a4a;
    border: 1px solid #007acc;
}
QPushButton:pressed {
    background: #007acc;
}
QPlainTextEdit {
    background: #1e1e1e;
    border: 1px solid #333333;
    color: #dcdcdc;
    border-radius: 4px;
}
QTabWidget::pane {
    border: 1px solid #333333;
    background: #2d2d2d;
}
QTabBar::tab {
    background: #252525;
    color: #bbbbbb;
    padding: 6px 14px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}
QTabBar::tab:selected {
    background: #2d2d2d;
    color: #ffffff;
    border-bottom: 2px solid #007acc;
}
"""


def _require_qt():
    """Lança ModuleNotFoundError com mensagem clara se PySide não estiver instalado."""
    if not HAS_QT:
        raise ModuleNotFoundError(
            "PySide6 ou PySide2 não instalado. Rode: uv sync --extra window"
        )


def make_app_icon(size=64):
    """Cria um ícone programático (sem arquivo externo)."""
    _require_qt()
    pixmap = QtGui.QPixmap(size, size)
    pixmap.fill(QtCore.Qt.transparent)

    painter = QtGui.QPainter(pixmap)
    painter.setRenderHint(QtGui.QPainter.Antialiasing)

    painter.setBrush(QtGui.QColor("#007acc"))
    painter.setPen(QtCore.Qt.NoPen)
    painter.drawEllipse(4, 4, size - 8, size - 8)

    painter.setPen(QtGui.QPen(QtCore.Qt.white, 6))
    font = painter.font()
    font.setPointSize(int(size * 0.45))
    font.setBold(True)
    painter.setFont(font)
    painter.drawText(
        QtCore.QRectF(0, 0, size, size),
        QtCore.Qt.AlignCenter,
        "F",
    )
    painter.end()

    return QtGui.QIcon(pixmap)


if HAS_QT:  # pragma: no cover

    class DocksTab(QtWidgets.QWidget):
        """Aba de gerenciamento de docks."""

        dock_visibility_changed = QtCore.Signal(str, bool)

        def __init__(self, parent=None):
            super().__init__(parent)
            self._docks = {}          # nome -> QDockWidget (real) ou None (simulado)
            self._visible = {}        # nome -> bool

            layout = QtWidgets.QVBoxLayout(self)

            # Instruções
            info = QtWidgets.QLabel(
                "Lista os docks da aplicação e controla a visibilidade de cada um. "
                "Dentro do FreeCAD, esses são os docks reais da interface."
            )
            info.setWordWrap(True)
            info.setStyleSheet("color: #aaaaaa; font-size: 12px;")
            layout.addWidget(info)

            # Botões de ação em massa
            btn_row = QtWidgets.QHBoxLayout()
            self.btn_show_all = QtWidgets.QPushButton("Mostrar todos")
            self.btn_hide_all = QtWidgets.QPushButton("Esconder todos")
            self.btn_refresh = QtWidgets.QPushButton("Atualizar lista")
            self.btn_show_all.clicked.connect(self.show_all)
            self.btn_hide_all.clicked.connect(self.hide_all)
            self.btn_refresh.clicked.connect(self.refresh)
            btn_row.addWidget(self.btn_show_all)
            btn_row.addWidget(self.btn_hide_all)
            btn_row.addWidget(self.btn_refresh)
            btn_row.addStretch()
            layout.addLayout(btn_row)

            # Área rolável com checklists
            scroll = QtWidgets.QScrollArea()
            scroll.setWidgetResizable(True)
            self.docks_container = QtWidgets.QWidget()
            self.docks_layout = QtWidgets.QVBoxLayout(self.docks_container)
            self.docks_layout.addStretch()
            scroll.setWidget(self.docks_container)
            layout.addWidget(scroll)

            self.refresh()

        def refresh(self):
            """Recarrega a lista de docks."""
            # Limpa checklists existentes (exceto o stretch final)
            while self.docks_layout.count() > 1:
                item = self.docks_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

            self._docks.clear()
            self._visible.clear()

            docks = self._enumerate_docks()
            if not docks:
                empty = QtWidgets.QLabel(
                    "Nenhum dock encontrado (ou rodando em modo standalone)."
                )
                empty.setStyleSheet("color: #888888; font-style: italic;")
                self.docks_layout.insertWidget(0, empty)
                return

            for name in sorted(docks):
                row = QtWidgets.QHBoxLayout()
                cb = QtWidgets.QCheckBox(name)
                cb.setChecked(self._visible.get(name, True))
                cb.stateChanged.connect(
                    lambda state, n=name: self._toggle(n, state == QtCore.Qt.Checked)
                )
                row.addWidget(cb)
                btn_show = QtWidgets.QPushButton("Mostrar")
                btn_hide = QtWidgets.QPushButton("Esconder")
                btn_show.setFixedWidth(70)
                btn_hide.setFixedWidth(70)
                btn_show.clicked.connect(lambda _, n=name: self._set_visible(n, True))
                btn_hide.clicked.connect(lambda _, n=name: self._set_visible(n, False))
                row.addWidget(btn_show)
                row.addWidget(btn_hide)
                row.addStretch()

                container = QtWidgets.QWidget()
                container.setLayout(row)
                self.docks_layout.insertWidget(
                    self.docks_layout.count() - 1, container
                )

                self._docks[name] = docks[name]
                self._visible[name] = self._is_visible(name)

        def _enumerate_docks(self):
            """Retorna dict {nome: QDockWidget ou None} dos docks disponíveis."""
            result = {}
            try:
                import FreeCADGui as Gui  # noqa: F401
                mw = Gui.getMainWindow()
                if mw is not None:
                    for d in mw.findChildren(QtWidgets.QDockWidget):
                        name = d.objectName() or d.windowTitle() or "sem nome"
                        result[name] = d
            except Exception:
                # Modo standalone: simula docks
                for name in DEFAULT_DOCK_NAMES:
                    result[name] = None
            return result

        def _is_visible(self, name):
            dock = self._docks.get(name)
            if dock is not None:
                try:
                    return dock.isVisible()
                except RuntimeError:
                    return False
            return self._visible.get(name, True)

        def _toggle(self, name, visible):
            self._set_visible(name, visible)
            self.dock_visibility_changed.emit(name, visible)

        def _set_visible(self, name, visible):
            dock = self._docks.get(name)
            if dock is not None:
                try:
                    dock.setVisible(visible)
                except RuntimeError:
                    pass
            self._visible[name] = visible

        def show_all(self):
            for name in list(self._docks.keys()):
                self._set_visible(name, True)
            self.refresh()

        def hide_all(self):
            for name in list(self._docks.keys()):
                self._set_visible(name, False)
            self.refresh()

    class QssTab(QtWidgets.QWidget):
        """Aba de editor de QSS (folhas de estilo) com aplicação ao vivo."""

        qss_applied = QtCore.Signal(str)

        def __init__(self, parent=None):
            super().__init__(parent)
            self._target = None  # QWidget alvo para aplicar o QSS

            layout = QtWidgets.QVBoxLayout(self)

            info = QtWidgets.QLabel(
                "Edite a folha de estilo (QSS) da aplicação. Clique em 'Aplicar' para "
                "enviar para a janela alvo (FreeCAD ou janela standalone)."
            )
            info.setWordWrap(True)
            info.setStyleSheet("color: #aaaaaa; font-size: 12px;")
            layout.addWidget(info)

            # Selector de alvo
            target_row = QtWidgets.QHBoxLayout()
            target_row.addWidget(QtWidgets.QLabel("Aplicar QSS em:"))
            self.cmb_target = QtWidgets.QComboBox()
            self.cmb_target.addItems(
                ["Janela do UI-LAB", "MainWindow do FreeCAD", "Todos os widgets"]
            )
            target_row.addWidget(self.cmb_target)
            target_row.addStretch()
            layout.addLayout(target_row)

            # Editor
            self.editor = QtWidgets.QPlainTextEdit()
            self.editor.setPlainText(DEFAULT_QSS)
            self.editor.setFont(QtGui.QFont("Consolas, Monaco, monospace", 10))
            layout.addWidget(self.editor, stretch=1)

            # Botões
            btn_row = QtWidgets.QHBoxLayout()
            self.btn_apply = QtWidgets.QPushButton("Aplicar QSS")
            self.btn_reset = QtWidgets.QPushButton("Resetar padrão")
            self.btn_load = QtWidgets.QPushButton("Carregar arquivo…")
            self.btn_save = QtWidgets.QPushButton("Salvar arquivo…")
            self.btn_apply.clicked.connect(self.apply)
            self.btn_reset.clicked.connect(self.reset)
            self.btn_load.clicked.connect(self.load_file)
            self.btn_save.clicked.connect(self.save_file)
            btn_row.addWidget(self.btn_apply)
            btn_row.addWidget(self.btn_reset)
            btn_row.addWidget(self.btn_load)
            btn_row.addWidget(self.btn_save)
            btn_row.addStretch()
            layout.addLayout(btn_row)

        def set_target(self, widget):
            self._target = widget

        def qss_text(self):
            return self.editor.toPlainText()

        def apply(self):
            qss = self.qss_text()
            target = self._target
            mode = self.cmb_target.currentText()

            applied = False
            try:
                if mode == "MainWindow do FreeCAD":
                    import FreeCADGui as Gui
                    mw = Gui.getMainWindow()
                    if mw is not None:
                        mw.setStyleSheet(qss)
                        applied = True
                elif mode == "Todos os widgets":
                    import FreeCADGui as Gui
                    mw = Gui.getMainWindow()
                    if mw is not None:
                        mw.setStyleSheet(qss)
                        applied = True
                else:
                    if target is not None:
                        target.setStyleSheet(qss)
                        applied = True
            except Exception:
                pass

            if applied:
                self.qss_applied.emit(qss)

        def reset(self):
            self.editor.setPlainText(DEFAULT_QSS)

        def load_file(self):
            path, _ = QtWidgets.QFileDialog.getOpenFileName(
                self, "Carregar QSS", "", "Folha de estilo (*.qss);;Todos (*)"
            )
            if path:
                with open(path, "r", encoding="utf-8") as f:
                    self.editor.setPlainText(f.read())

        def save_file(self):
            path, _ = QtWidgets.QFileDialog.getSaveFileName(
                self, "Salvar QSS", "ui_lab.qss", "Folha de estilo (*.qss)"
            )
            if path:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(self.qss_text())

    class InfoTab(QtWidgets.QWidget):
        """Aba com informações do ambiente e controles gerais."""

        def __init__(self, parent=None):
            super().__init__(parent)
            layout = QtWidgets.QVBoxLayout(self)

            self.lbl_binding = QtWidgets.QLabel()
            self.lbl_freecad = QtWidgets.QLabel()
            self.lbl_platform = QtWidgets.QLabel()
            for lbl in (self.lbl_binding, self.lbl_freecad, self.lbl_platform):
                lbl.setStyleSheet("color: #dcdcdc; font-family: monospace;")
                layout.addWidget(lbl)

            self.btn_recompute = QtWidgets.QPushButton(
                "Recalcular documento (FreeCAD)"
            )
            self.btn_recompute.clicked.connect(self._recompute)
            layout.addWidget(self.btn_recompute)

            self.btn_fit = QtWidgets.QPushButton("Ajustar visualização (Fit All)")
            self.btn_fit.clicked.connect(self._fit)
            layout.addWidget(self.btn_fit)

            layout.addStretch()
            self._refresh_info()

        def _refresh_info(self):
            self.lbl_binding.setText(f"Binding Qt: {QT_BINDING}")
            try:
                import FreeCAD as App
                doc = App.activeDocument()
                doc_name = doc.Name if doc else "nenhum"
                n_objs = len(doc.Objects) if doc else 0
                self.lbl_freecad.setText(
                    f"FreeCAD: ativo | documento: {doc_name} | objetos: {n_objs}"
                )
            except Exception:
                self.lbl_freecad.setText("FreeCAD: não disponível (modo standalone)")
            self.lbl_platform.setText(
                f"Plataforma: {QtCore.QSysInfo.kernelType() if hasattr(QtCore, 'QSysInfo') else 'desconhecida'}"
            )

        def _recompute(self):
            try:
                import FreeCAD as App
                doc = App.activeDocument()
                if doc:
                    doc.recompute()
            except Exception:
                pass

        def _fit(self):
            try:
                import FreeCADGui as Gui
                Gui.SendMsgToActiveView("ViewFit")
            except Exception:
                pass

    class LogWidget(QtWidgets.QPlainTextEdit):
        """Área de log que também escreve no Console do FreeCAD."""

        def __init__(self, parent=None):
            super().__init__(parent)
            self.setReadOnly(True)
            self.setFont(QtGui.QFont("Consolas, Monaco, monospace", 9))
            self.setStyleSheet(
                "background: #1e1e1e; color: #dcdcdc; border: 1px solid #333333;"
            )

        def log(self, msg):
            self.appendPlainText(msg)
            try:
                import FreeCAD as App
                App.Console.PrintMessage(f"[UI-LAB] {msg}\n")
            except Exception:
                pass

    class UiLabApp(QtWidgets.QMainWindow):
        """Janela principal do aplicativo FreeCAD UI-LAB."""

        def __init__(self, parent=None, freeCAD_mode=False):
            _require_qt()
            super().__init__(parent)
            self.freeCAD_mode = freeCAD_mode
            self.setWindowTitle(
                f"FreeCAD UI-LAB — Laboratório de UI/UX ({QT_BINDING})"
            )
            self.setWindowIcon(make_app_icon())
            self.resize(900, 700)

            self._config = self._load_config()

            central = QtWidgets.QWidget()
            self.setCentralWidget(central)
            root = QtWidgets.QVBoxLayout(central)

            # Abas
            self.tabs = QtWidgets.QTabWidget()
            self.docks_tab = DocksTab()
            self.qss_tab = QssTab()
            self.info_tab = InfoTab()

            self.tabs.addTab(self.docks_tab, "Docks")
            self.tabs.addTab(self.qss_tab, "QSS / Estilo")
            self.tabs.addTab(self.info_tab, "Info / Controle")

            root.addWidget(self.tabs, stretch=1)

            # Log embutido na parte inferior
            self.log = LogWidget()
            self.log.setMaximumHeight(150)
            self.log.log("UI-LAB iniciado.")
            self.log.log(
                f"Modo: {'FreeCAD' if freeCAD_mode else 'standalone'} | Binding: {QT_BINDING}"
            )
            root.addWidget(self.log)

            # Conecta QSS
            self.qss_tab.set_target(self)
            self.qss_tab.qss_applied.connect(
                lambda qss: self.log.log("QSS aplicado.")
            )

            # Carrega configuração salva
            self._apply_config()

        # --- Configuração persistente ---------------------------------------

        def _load_config(self):
            if os.path.exists(CONFIG_FILE):
                try:
                    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                        return json.load(f)
                except Exception:
                    return {}
            return {}

        def _save_config(self):
            try:
                with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                    json.dump(self._config, f, indent=2, ensure_ascii=False)
            except Exception:
                pass

        def _apply_config(self):
            qss = self._config.get("qss")
            if qss:
                self.qss_tab.editor.setPlainText(qss)

        def closeEvent(self, event):
            self._config["qss"] = self.qss_tab.qss_text()
            self._save_config()
            super().closeEvent(event)

        # --- Log -----------------------------------------------------------

        def log(self, msg):
            self.log.log(msg)


# --- Ponto de entrada --------------------------------------------------

def run_standalone():
    """Executa o app em modo standalone (fora do FreeCAD)."""
    _require_qt()
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    app.setWindowIcon(make_app_icon())
    win = UiLabApp(freeCAD_mode=False)
    win.show()
    if __name__ == "__main__":
        app.exec()


def run_in_freecad():
    """Integra o app como uma janela dockável/dialog dentro do FreeCAD."""
    _require_qt()
    try:
        import FreeCADGui as Gui
    except ImportError:
        raise RuntimeError("FreeCADGui não disponível; rode em modo standalone.")

    mw = Gui.getMainWindow()
    if mw is None:
        raise RuntimeError("MainWindow do FreeCAD não encontrada.")

    win = UiLabApp(parent=mw, freeCAD_mode=True)
    win.setWindowModality(QtCore.Qt.NonModal)
    win.show()
    win.raise_()
    win.activateWindow()
    return win


if __name__ == "__main__":
    if HAS_QT:
        run_standalone()
    else:
        print("PySide6 ou PySide2 não instalado. Rode: uv sync --extra window")
