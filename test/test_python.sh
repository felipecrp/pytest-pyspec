#!/bin/sh

for v in 3.10 3.11 3.12 3.13 3.14; do
  echo "Python $v"
  if ! mise exec python@$v -- python -m uv --version >/dev/null 2>&1; then
    mise exec python@$v -- pip install uv
  fi
  mise exec python@$v -- uv run pytest -q
done

