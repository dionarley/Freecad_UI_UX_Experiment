# This file is part of the FreeCAD UI/UX Experiment.
# It is licensed under the GNU LGPL v3. See LICENSE-CODE for details.

"""Teste de dependências opcionais (PySide6/PySide2).

Verifica que:
1. Se PySide6 ou PySide2 estiver instalado e importável, os módulos ui_lab_app e
   window_test importam corretamente (sem ModuleNotFoundError cru).
2. Se não estiver disponível (ex: libGL ausente), os testes são pulados.
"""
import os
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest


def _check_pyside():
    """Retorna True se PySide6 ou PySide2 estiver importável (incluindo QtGui/QtWidgets)."""
    try:
        from PySide6 import QtCore, QtGui, QtWidgets  # noqa: F401
        return True
    except ImportError:
        try:
            from PySide2 import QtCore, QtGui, QtWidgets  # noqa: F401
            return True
        except ImportError:
            return False


HAS_PYSIDE = _check_pyside()


if HAS_PYSIDE:  # pragma: no cover

    def test_pyside_esta_instalado():
        """PySide6 ou PySide2 deve estar disponível para rodar os testes de UI."""
        assert HAS_PYSIDE is True

    def test_ui_lab_app_importa_sem_erro():
        """ui_lab_app deve importar sem ModuleNotFoundError quando PySide está instalado."""
        for mod in ("ui_lab_app", "window_test"):
            sys.modules.pop(mod, None)
        import ui_lab_app  # noqa: F401
        assert ui_lab_app.QT_BINDING in ("PySide6", "PySide2")

    def test_window_test_importa_sem_erro():
        """window_test deve importar sem ModuleNotFoundError quando PySide está instalado."""
        for mod in ("ui_lab_app", "window_test"):
            sys.modules.pop(mod, None)
        import window_test  # noqa: F401
        assert window_test.QT_BINDING in ("PySide6", "PySide2")

    def test_make_app_icon_retorna_qicon():
        """make_app_icon deve retornar um QIcon válido (não nulo)."""
        from window_test import make_app_icon
        icon = make_app_icon()
        assert not icon.isNull()

    def test_ui_lab_app_tem_classes_esperadas():
        """ui_lab_app deve expor as classes principais."""
        import ui_lab_app
        assert hasattr(ui_lab_app, "UiLabApp")
        assert hasattr(ui_lab_app, "DocksTab")
        assert hasattr(ui_lab_app, "QssTab")
        assert hasattr(ui_lab_app, "InfoTab")
        assert hasattr(ui_lab_app, "LogWidget")

    def test_default_qss_nao_esta_vazio():
        """DEFAULT_QSS deve conter regras para QDockWidget."""
        import ui_lab_app
        assert ui_lab_app.DEFAULT_QSS.strip()
        assert "QDockWidget" in ui_lab_app.DEFAULT_QSS
