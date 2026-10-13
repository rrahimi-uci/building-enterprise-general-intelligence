#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT"
ENTRY="latex/Enterprise-General-Intelligence-v1.0.0.tex"
OUT="latex/build"
PDF_SOURCE="$OUT/Enterprise-General-Intelligence-v1.0.0.pdf"
PDF_DEST="dist/Enterprise-General-Intelligence-v1.0.0-LaTeX.pdf"
mkdir -p "$OUT" "dist"
if command -v latexmk >/dev/null 2>&1; then
  latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error -outdir="$OUT" "$ENTRY"
elif command -v xelatex >/dev/null 2>&1; then
  xelatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory="$OUT" "$ENTRY"
  # The index: makeindex sorts the marks the first pass wrote.
  makeindex -q -s latex/bookindex.ist -o "$OUT/Enterprise-General-Intelligence-v1.0.0.ind" "$OUT/Enterprise-General-Intelligence-v1.0.0.idx"
  for pass in 2 3; do xelatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory="$OUT" "$ENTRY"; done
else
  echo "XeLaTeX is required. Use the included Dockerfile.latex or CI workflow." >&2
  exit 2
fi
if [[ ! -s "$PDF_SOURCE" ]]; then
  echo "XeLaTeX did not produce a non-empty PDF at $PDF_SOURCE." >&2
  exit 1
fi
cp "$PDF_SOURCE" "$PDF_DEST"
if [[ ! -s "$PDF_DEST" ]]; then
  echo "The final XeLaTeX PDF is missing or empty at $PDF_DEST." >&2
  exit 1
fi
printf 'XeLaTeX PDF written to %s\n' "$PDF_DEST"
