#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [ ! -f .venv/pyvenv.cfg ]; then
  echo "Missing backend/.venv/pyvenv.cfg"
  echo "Create env: python3 -m venv .venv"
  exit 1
fi

exec ./.venv/bin/python -m uvicorn app.main:app --reload
