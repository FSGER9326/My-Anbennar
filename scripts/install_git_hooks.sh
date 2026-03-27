#!/usr/bin/env bash
set -euo pipefail

if [[ ! -f .githooks/pre-commit || ! -f .githooks/pre-push ]]; then
  echo "Missing .githooks hook files."
  exit 1
fi

git config core.hooksPath .githooks
chmod +x .githooks/pre-commit .githooks/pre-push

echo "Installed repo hooks via core.hooksPath=.githooks"
echo "Active hooks:"
echo " - .githooks/pre-commit"
echo " - .githooks/pre-push"
