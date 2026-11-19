# This file is part of the FreeCAD UI/UX Experiment.
# It is licensed under the GNU LGPL v3. See LICENSE-CODE for details.

"""Teste mínimo do ui_lab_probe.py.

Não requer FreeCAD instalado. Valida apenas que o módulo é importável fora do
FreeCAD e que as constantes/UI de teste estão presentes.
"""
import ui_lab_probe


def test_default_hide_docks_is_non_empty_set():
    assert isinstance(ui_lab_probe.DEFAULT_HIDE_DOCK_OBJECT_NAMES, set)
    assert len(ui_lab_probe.DEFAULT_HIDE_DOCK_OBJECT_NAMES) > 0


def test_test_qss_is_non_empty():
    assert ui_lab_probe.TEST_QSS.strip()


def test_get_lab_returns_instance():
    lab = ui_lab_probe.get_lab()
    assert isinstance(lab, ui_lab_probe.FreeCadUiLab)
