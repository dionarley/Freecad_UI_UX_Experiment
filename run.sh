#!/usr/bin/env bash
# Script de execução mínimo para o Freecad_UI_UX_Experiment.
# Requer: uv (e mise, opcional).
set -euo pipefail

cd "$(dirname "$0")"

usage() {
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
    uv run python ui_lab_app.py
    ;;
  clean)
    rm -rf .venv __pycache__ tests/__pycache__
    echo "limpo."
    ;;
  *)
    usage
    ;;
esac
