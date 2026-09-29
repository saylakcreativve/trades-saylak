#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'

if [ ! -f .env ]; then
  cp .env.example .env
  echo '.env created. Set TELEGRAM_BOT_TOKEN before starting the bot.'
fi

mkdir -p data
python -m app.main
