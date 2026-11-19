#!/usr/bin/env bash
# Execution script for freecad-ui-ux-experiment.
# Requires: uv (and mise, optional).
set -euo pipefail

cd "$(dirname "$0")"

usage() {
  echo "Usage: $0 {sync|test|window|app|clean}"
  echo ""
  echo "  sync     - sync dependencies (uv sync)"
  echo "  test     - run tests (pytest)"
  echo "  window   - run including window test (uv sync --extra window)"
  echo "  app      - run the real UI/UX app (standalone, needs PySide6)"
  echo "  clean    - remove .venv and __pycache__"
  echo ""
  echo "Uso: $0 {sync|test|window|app|clean}"
  echo ""
  echo "  sync     - sincroniza dependências (uv sync)"
  echo "  test     - roda os testes (pytest)"
  echo "  window   - roda incluindo o teste de janela (uv sync --extra window)"
  echo "  app      - executa o app real de UI/UX (standalone, requer PySide6)"
  echo "  clean    - remove .venv e __pycache__"
  exit 1
}

cmd="${1:-}"

case "$cmd" in
  sync)
    uv sync
    ;;
  test)
    uv run pytest -q
    ;;
  window)
    uv sync --extra window
    uv run pytest -q
    ;;
  app)
    uv sync --extra window
    # Verifica se o PySide6 está disponível após o sync
    if [ "${SKIP_QT_CHECK:-0}" != "1" ]; then
      if ! uv run python -c "from PySide6 import QtCore, QtGui, QtWidgets" 2>/dev/null; then
        echo ""
        echo "ERRO: PySide6 não pôde ser importado após a instalação."
        echo "Isso geralmente significa que falta libGL.so.1 no seu sistema."
        echo "Instale as bibliotecas OpenGL do seu sistema (ex: libgl1-mesa-glx no Debian/Ubuntu)."
        echo ""
        echo "Se não puder instalar OpenGL, pule a verificação com:"
        echo "  SKIP_QT_CHECK=1 ./run.sh app"
        echo ""
        exit 1
      fi
    fi
    uv run python ui_lab_app.py
    ;;
  clean)
    rm -rf .venv __pycache__ tests/__pycache__
    echo "cleaned. / limpo."
    ;;
  *)
    usage
    ;;
esac
