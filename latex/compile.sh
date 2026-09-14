#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT"
ENTRY="latex/Enterprise-Agentic-AI-Architecture-Developer-Platform-Guide-v2.0.0.tex"
OUT="latex/build"
mkdir -p "$OUT"
if command -v latexmk >/dev/null 2>&1; then
  latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error -outdir="$OUT" "$ENTRY"
elif command -v xelatex >/dev/null 2>&1; then
  for pass in 1 2 3; do xelatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory="$OUT" "$ENTRY"; done
else
  echo "XeLaTeX is required. Use the included Dockerfile.latex or CI workflow." >&2
  exit 2
fi
cp "$OUT/Enterprise-Agentic-AI-Architecture-Developer-Platform-Guide-v2.0.0.pdf" "dist/Enterprise-Agentic-AI-Architecture-Developer-Platform-Guide-v2.0.0-LaTeX.pdf"
