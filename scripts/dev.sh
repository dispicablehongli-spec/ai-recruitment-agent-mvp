#!/usr/bin/env bash
# 本地同时启动后端（8000）与前端（5173）。前端进程在前台，Ctrl+C 会结束后端子进程。
# 用法：
#   bash scripts/dev.sh
#   bash scripts/dev.sh --open    # macOS：额外用默认浏览器打开前端
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

OPEN_BROWSER=false
for arg in "$@"; do
  case "$arg" in
    --open) OPEN_BROWSER=true ;;
    -h|--help)
      echo "Usage: bash scripts/dev.sh [--open]"
      echo "  --open   (macOS) open http://localhost:5173 in the default browser"
      exit 0
      ;;
    *)
      echo "Unknown option: $arg (try --help)" >&2
      exit 1
      ;;
  esac
done

BACKEND_PID=""

cleanup() {
  if [[ -n "$BACKEND_PID" ]] && kill -0 "$BACKEND_PID" 2>/dev/null; then
    kill "$BACKEND_PID" 2>/dev/null || true
    wait "$BACKEND_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT INT TERM

if [[ ! -x "$ROOT/.venv/bin/python" ]]; then
  echo "Missing $ROOT/.venv/bin/python — create venv and install deps first:" >&2
  echo "  python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt" >&2
  exit 1
fi

if [[ ! -d "$ROOT/frontend/node_modules" ]]; then
  echo "Missing frontend/node_modules — run: (cd frontend && npm install)" >&2
  exit 1
fi

echo "[dev] starting backend http://127.0.0.1:8000"
"$ROOT/.venv/bin/python" -m uvicorn backend.main:app --reload --port 8000 &
BACKEND_PID=$!
sleep 1

if [[ "$OPEN_BROWSER" == true ]]; then
  if [[ "$(uname -s)" == "Darwin" ]] && command -v open >/dev/null 2>&1; then
    echo "[dev] opening http://localhost:5173/"
    open "http://localhost:5173/"
  else
    echo "[dev] --open skipped (only supported on macOS with 'open')" >&2
  fi
fi

echo "[dev] starting frontend (Vite) — press Ctrl+C to stop both"
cd "$ROOT/frontend"
npm run dev
