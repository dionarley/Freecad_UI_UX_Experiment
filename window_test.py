# This file is part of the FreeCAD UI/UX Experiment.
# It is licensed under the GNU LGPL v3. See LICENSE-CODE for details.

"""Janela de teste com botão, compatível com o FreeCAD.

Este arquivo é autônomo e **não modifica** `ui_lab_probe.py` nem qualquer outro
código original do repositório.

Funciona de duas formas:
1. Dentro do FreeCAD (PySide já carregado): reutiliza a main window do
   FreeCAD e imprime no Console Python do aplicativo.
2. Fora do FreeCAD (standalone): cria sua própria janela independente.

Compatível com PySide6 (FreeCAD >= 1.0) e PySide2 (FreeCAD < 1.0).
Se PySide não estiver instalado, o módulo pode ser importado sem erro, mas
qualquer tentativa de instanciar a janela lançará ModuleNotFoundError com
mensagem clara.
"""

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


def _require_qt():
    """Lança ModuleNotFoundError com mensagem clara se PySide não estiver instalado."""
    if not HAS_QT:
        raise ModuleNotFoundError(
            "PySide6 ou PySide2 não instalado. Rode: uv sync --extra window"
        )


def make_app_icon(size=64):
    """Cria um ícone programático (sem arquivo externo) para a janela e botões."""
    _require_qt()
    pixmap = QtGui.QPixmap(size, size)
    pixmap.fill(QtCore.Qt.transparent)

    painter = QtGui.QPainter(pixmap)
    painter.setRenderHint(QtGui.QPainter.Antialiasing)

    painter.setBrush(QtGui.QColor("#007acc"))  # azul FreeCAD
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

    class TestWindow(QtWidgets.QMainWindow):
        """Janela principal com um botão de teste."""

        def __init__(self, parent=None, freeCAD_mode=False):
            super().__init__(parent)
            self.freeCAD_mode = freeCAD_mode
            self.setWindowTitle(
                f"FreeCAD UI-LAB — Teste de Janela ({QT_BINDING})"
            )
            self.setWindowIcon(make_app_icon())
            self.resize(400, 200)

            central = QtWidgets.QWidget()
            self.setCentralWidget(central)

            layout = QtWidgets.QVBoxLayout(central)

            # Título
            title = QtWidgets.QLabel("Laboratório de UI/UX — Teste Rápido")
            title.setAlignment(QtCore.Qt.AlignCenter)
            font = title.font()
            font.setPointSize(14)
            font.setBold(True)
            title.setFont(font)
            layout.addWidget(title)

            # Botão de teste (com ícone)
            self.btn_test = QtWidgets.QPushButton(make_app_icon(24), "Executar Teste")
            self.btn_test.setMinimumHeight(40)
            self.btn_test.setIconSize(QtCore.QSize(20, 20))
            self.btn_test.clicked.connect(self.on_test_clicked)
            layout.addWidget(self.btn_test)

            # Botão de sair/fechar
            self.btn_close = QtWidgets.QPushButton("Fechar")
            self.btn_close.setMinimumHeight(32)
            self.btn_close.clicked.connect(self.close)
            layout.addWidget(self.btn_close)

            # Área de log (saída)
            self.log = QtWidgets.QPlainTextEdit()
            self.log.setReadOnly(True)
            self.log.setPlaceholderText(
                "Os resultados do teste aparecerão aqui..."
            )
            self.log.setMaximumHeight(120)
            layout.addWidget(self.log)

            layout.addStretch()

        def log_msg(self, msg):
            """Escreve uma mensagem na área de log e no console do FreeCAD, se houver."""
            self.log.appendPlainText(msg)
            try:
                import FreeCAD as App  # noqa: F401
                App.Console.PrintMessage(f"[UI-LAB] {msg}\n")
            except Exception:
                pass

        def on_test_clicked(self):
            """Ação disparada ao clicar no botão de teste."""
            self.log_msg(">>> Botão de teste pressionado")
            self.log_msg(f"Binding Qt: {QT_BINDING}")
            self.log_msg(f"Janela visível: {self.isVisible()}")
            self.log_msg(">>> Teste concluído com sucesso")

    def run_standalone():
        """Executa a janela de modo standalone (fora do FreeCAD)."""
        _require_qt()
        app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
        win = TestWindow(freeCAD_mode=False)
        win.show()
        if __name__ == "__main__":
            app.exec()

    def run_in_freecad():
        """Integra a janela de teste na main window do FreeCAD."""
        _require_qt()
        try:
            import FreeCADGui as Gui
        except ImportError:
            raise RuntimeError(
                "FreeCADGui não disponível; rode em modo standalone."
            )

        mw = Gui.getMainWindow()
        if mw is None:
            raise RuntimeError("MainWindow do FreeCAD não encontrada.")

        win = TestWindow(parent=mw, freeCAD_mode=True)
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
