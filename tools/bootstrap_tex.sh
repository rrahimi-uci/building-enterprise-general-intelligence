#!/usr/bin/env bash
# Install the TeX packages the XeLaTeX edition needs, into the user tree.
#
# A full TeX Live installation already satisfies everything here and the script
# exits immediately. Minimal distributions (BasicTeX on macOS, texlive-base on
# Debian/Ubuntu) ship only a fraction of these; this installs the remainder into
# ~/texmf or ~/Library/texmf via `tlmgr --usermode`, which needs no root.
#
# Idempotent: re-running it after everything is present is a no-op.
#
#   ./tools/bootstrap_tex.sh          # install what is missing
#   ./tools/bootstrap_tex.sh --check  # report only, exit 1 if anything is missing
#   ./tools/bootstrap_tex.sh --diagrams  # also the packages `make diagrams` needs
#                                        # to compile the TikZ figures (the book
#                                        # build itself never needs them)
set -euo pipefail

CHECK_ONLY=0
WITH_DIAGRAMS=0
for arg in "$@"; do
  [[ "$arg" == "--check" ]] && CHECK_ONLY=1
  [[ "$arg" == "--diagrams" ]] && WITH_DIAGRAMS=1
done

# style-file -> tlmgr package. The style file is what \RequirePackage asks for;
# the tlmgr package is what actually has to be installed, and the two differ
# whenever a bundle ships several styles (graphicx lives in `graphics`,
# longtable in `tools`, amssymb in `amsfonts`, ragged2e in `ms`).
#
# The last four are *transitive* dependencies of tcolorbox[most] rather than
# direct requirements of bookstyle.sty: tcbskins pulls tikzfill.image, and
# tcbbreakable pulls pdfcol. They are easy to miss because latex/README.md's
# dependency list names only the direct requirements.
REQUIREMENTS=(
  "fontspec:fontspec"     "microtype:microtype"   "xcolor:xcolor"
  "graphicx:graphics"     "longtable:tools"       "array:tools"
  "booktabs:booktabs"     "ragged2e:ms"           "enumitem:enumitem"
  "fancyhdr:fancyhdr"     "titlesec:titlesec"     "caption:caption"
  "hyperref:hyperref"     "bookmark:bookmark"     "listings:listings"
  "tcolorbox:tcolorbox"   "needspace:needspace"   "setspace:setspace"
  "lastpage:lastpage"     "pdflscape:pdflscape"   "amssymb:amsfonts"
  "etoolbox:etoolbox"     "tikz:pgf"
  "environ:environ"       "trimspaces:trimspaces"
  "tikzfill.image:tikzfill" "pdfcol:pdfcol"
)

# Needed only to render TikZ figures (tools/render_diagrams.py), not to build the
# book from the committed renders; CI therefore never asks for them.
if [[ $WITH_DIAGRAMS -eq 1 ]]; then
  REQUIREMENTS+=("standalone:standalone" "fontawesome5:fontawesome5")
fi

# BasicTeX installs here but does not always put it on a non-login shell's PATH.
[[ -d /Library/TeX/texbin ]] && PATH="/Library/TeX/texbin:$PATH"

if ! command -v xelatex >/dev/null 2>&1; then
  cat >&2 <<'MSG'
error: xelatex not found.

  macOS:          brew install --cask basictex     (then reopen your shell)
  Debian/Ubuntu:  sudo apt-get install texlive-xetex texlive-fonts-recommended
  Any platform:   use the repository's Dockerfile.latex, which needs no local TeX

MSG
  exit 2
fi

missing_pkgs=()
missing_styles=()
for entry in "${REQUIREMENTS[@]}"; do
  style="${entry%%:*}"
  pkg="${entry##*:}"
  if ! kpsewhich "${style}.sty" >/dev/null 2>&1; then
    missing_styles+=("${style}.sty")
    # A bundle can satisfy several styles; only ask tlmgr for it once.
    [[ " ${missing_pkgs[*]:-} " == *" ${pkg} "* ]] || missing_pkgs+=("${pkg}")
  fi
done

if [[ ${#missing_styles[@]} -eq 0 ]]; then
  echo "All required TeX packages are present. Run 'make pdf' to build the book."
  exit 0
fi

echo "Missing style files: ${missing_styles[*]}"
echo "Corresponding tlmgr packages: ${missing_pkgs[*]}"

if [[ $CHECK_ONLY -eq 1 ]]; then
  echo "Run ./tools/bootstrap_tex.sh to install them."
  exit 1
fi

if ! command -v tlmgr >/dev/null 2>&1; then
  echo "error: tlmgr not found; install the packages with your system package manager." >&2
  exit 2
fi

# --usermode keeps everything under the user's texmf tree, so no sudo and no
# writes into the shared TeX Live installation. init-usertree is safe to repeat.
tlmgr init-usertree >/dev/null 2>&1 || true
tlmgr --usermode install "${missing_pkgs[@]}"

still_missing=()
for entry in "${REQUIREMENTS[@]}"; do
  style="${entry%%:*}"
  kpsewhich "${style}.sty" >/dev/null 2>&1 || still_missing+=("${style}.sty")
done

if [[ ${#still_missing[@]} -gt 0 ]]; then
  echo "error: still missing after install: ${still_missing[*]}" >&2
  exit 1
fi

echo "TeX dependencies satisfied. Run 'make pdf' to build the book."
