# Build entry points for the book. Run `make` (or `make help`) for the list.
#
# Prefer the project virtualenv when one exists so `make build` cannot silently
# run against a system Python that is missing python-docx, Pillow, or fontTools.
PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)
ROOT := $(CURDIR)
ZIP ?= $(abspath ../Enterprise-Agentic-AI-Book-v1.0.0-Complete-Package-with-LaTeX.zip)
TEX_ENTRY := latex/Enterprise-Agentic-AI-Architecture-Developer-Platform-Guide-v1.0.0.tex

.DEFAULT_GOAL := help

.PHONY: help setup all assemble cover build latex draft pdf references \
        latex-validate validate deterministic qa-pdf latex-pdf package release \
        clean distclean

## help: show the available targets
help:
	@echo "Authoring loop"
	@echo "  setup           create .venv, install Python deps, install missing TeX packages"
	@echo "  draft           assemble + one XeLaTeX pass; fastest way to eyeball a change"
	@echo "  pdf             full three-pass XeLaTeX build -> dist/*-LaTeX.pdf"
	@echo ""
	@echo "Generation"
	@echo "  assemble        source/parts/*.md -> book/manuscript.md + dist/*.md"
	@echo "  cover           regenerate the cover image"
	@echo "  build           assemble + cover + DOCX"
	@echo "  latex           generate latex/content/book-content.tex"
	@echo ""
	@echo "Verification"
	@echo "  references      check every [Rxx] against config/references.json"
	@echo "  latex-validate  structural/contrast/asset checks on the LaTeX source"
	@echo "  validate        build + references + latex-validate + structural validators"
	@echo "  deterministic   rebuild twice and compare hashes"
	@echo "  qa-pdf          DOCX pagination QA (requires LibreOffice)"
	@echo ""
	@echo "Release"
	@echo "  package         regenerate manifest + checksums, write the release ZIP"
	@echo "  release         validate + deterministic + qa-pdf + package"
	@echo ""
	@echo "Housekeeping"
	@echo "  clean           remove generated QA/build artifacts"
	@echo "  distclean       clean + remove .venv"

## setup: one command to get from a fresh clone to a working build
setup:
	python3 -m venv .venv
	.venv/bin/python -m pip install --upgrade pip
	.venv/bin/python -m pip install -r requirements.txt
	./tools/bootstrap_tex.sh
	@echo "Setup complete. Run 'make draft' or 'make pdf'."

all: build latex validate

assemble:
	$(PYTHON) tools/assemble_manuscript.py --root "$(ROOT)"

cover:
	$(PYTHON) tools/generate_cover.py --root "$(ROOT)"

build: assemble cover
	$(PYTHON) tools/build_book.py --root "$(ROOT)"
	$(PYTHON) tools/build_book.py --root "$(ROOT)" --template-only

latex: assemble
	$(PYTHON) tools/build_latex.py --root "$(ROOT)"

## draft: single XeLaTeX pass. Cross-references and page numbers will be stale;
## use it while writing, and `make pdf` before sharing anything.
draft: latex
	@./tools/bootstrap_tex.sh --check
	@mkdir -p latex/build
	@PATH="/Library/TeX/texbin:$$PATH" xelatex -interaction=nonstopmode -halt-on-error \
		-file-line-error -output-directory=latex/build "$(TEX_ENTRY)" >/dev/null \
		|| { echo "XeLaTeX failed; see latex/build/*.log"; exit 1; }
	@echo "Draft written to latex/build/ (cross-references not resolved)."

## pdf: the real build — validates first, then compiles to convergence
pdf: latex-pdf

references: assemble
	$(PYTHON) tools/check_references.py --root "$(ROOT)"

latex-validate: latex
	$(PYTHON) tools/validate_latex.py --root "$(ROOT)"

validate: build references latex-validate
	$(PYTHON) tools/validate_book.py --root "$(ROOT)"

deterministic: build
	$(PYTHON) tools/deterministic_build_check.py --root "$(ROOT)"

qa-pdf: build
	$(PYTHON) tools/render_pdf_qa.py --root "$(ROOT)"

latex-pdf: latex-validate
	@./tools/bootstrap_tex.sh --check
	./latex/compile.sh

package: validate
	$(PYTHON) tools/package_release.py --root "$(ROOT)" --output "$(ZIP)"

release: validate deterministic qa-pdf package

clean:
	rm -rf qa/determinism latex/build
	rm -f qa/validation-report.json qa/latex-validation-report.json reports/validation-summary.md reports/latex-validation.md reports/assembly-report.json

distclean: clean
	rm -rf .venv
