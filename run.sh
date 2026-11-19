#!/usr/bin/env bash
# Script de execução mínimo para o Freecad_UI_UX_Experiment.
# Requer: uv (e mise, opcional).
set -euo pipefail

cd "$(dirname "$0")"

usage() {
  echo "Uso: $0 {sync|test|window|clean}"
  echo ""
  echo "  sync     - sincroniza dependências (uv sync)"
  echo "  test     - roda os testes (pytest)"
  echo "  window   - roda incluindo o teste de janela (uv sync --extra window)"
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
  clean)
    rm -rf .venv __pycache__ tests/__pycache__
    echo "limpo."
    ;;
  *)
    usage
    ;;
esac
