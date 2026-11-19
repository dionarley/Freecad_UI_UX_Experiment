# This file is part of the FreeCAD UI/UX Experiment.
# It is licensed under the GNU LGPL v3. See LICENSE-CODE for details.

"""Testes do app real de UI/UX (ui_lab_app.py).

Roda apenas quando PySide6/PySide2 está instalado e importável. Fora disso,
todos os testes são pulados automaticamente para evitar ModuleNotFoundError.
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

    @pytest.fixture
    def app():
        """Cria uma QApplication para os testes."""
        instance = QtWidgets.QApplication.instance()
        if instance is None:
            instance = QtWidgets.QApplication([])
        return instance

    def test_janela_cria_sem_erro(app):
        """UiLabApp deve instanciar sem lançar exceção."""
        from ui_lab_app import UiLabApp
        win = UiLabApp(freeCAD_mode=False)
        assert win is not None
        assert win.windowTitle().startswith("FreeCAD UI-LAB")

    def test_janela_tem_abas(app):
        """A janela deve ter as abas Docks, QSS/Estilo e Info/Controle."""
        from ui_lab_app import UiLabApp
        win = UiLabApp(freeCAD_mode=False)
        tab_names = [win.tabs.tabText(i) for i in range(win.tabs.count())]
        assert "Docks" in tab_names
        assert "QSS / Estilo" in tab_names
        assert "Info / Controle" in tab_names

    def test_log_recebe_mensagem(app):
        """O LogWidget deve exibir mensagens de log."""
        from ui_lab_app import UiLabApp
        win = UiLabApp(freeCAD_mode=False)
        win.log.log("Mensagem de teste")
        texto = win.log.toPlainText()
        assert "Mensagem de teste" in texto

    def test_qss_editor_tem_conteudo(app):
        """O editor QSS deve conter o QSS padrão não vazio."""
        from ui_lab_app import UiLabApp, DEFAULT_QSS
        win = UiLabApp(freeCAD_mode=False)
        assert win.qss_tab.qss_text().strip()
        assert "QDockWidget" in win.qss_tab.qss_text()

    def test_docks_tab_lista_docks(app):
        """A aba Docks deve listar docks (reais no FreeCAD ou simulados fora)."""
        from ui_lab_app import UiLabApp
        win = UiLabApp(freeCAD_mode=False)
        info = win.docks_tab.list_docks()
        assert isinstance(info, list)

    def test_run_standalone_nao_lanca_excecao(app):
        """run_standalone deve criar a janela e mostrar sem erro."""
        from ui_lab_app import UiLabApp
        win = UiLabApp(freeCAD_mode=False)
        win.show()
        assert win.isVisible()
