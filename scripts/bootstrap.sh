#!/usr/bin/env bash
set -euo pipefail

python -m pip install --upgrade pip
pip install -e ".[dev]"

echo "Bootstrap complete."
echo "Next:"
echo "  - run: make lint"
echo "  - run: make test"

