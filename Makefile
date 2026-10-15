# Build entry points for the book. Run `make` (or `make help`) for the list.
#
# Prefer the project virtualenv when one exists so `make build` cannot silently
# run against a system Python that is missing python-docx, Pillow, or fontTools.
PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)
ROOT := $(CURDIR)
ZIP ?= $(abspath ../Enterprise-Agentic-AI-Book-v1.0.0-Complete-Package-with-LaTeX.zip)
TEX_ENTRY := latex/Enterprise-General-Intelligence-v1.0.0.tex
PDF_OUT := dist/Enterprise-General-Intelligence-v1.0.0.pdf

.DEFAULT_GOAL := help

PYTHON_EXAMPLES ?= $(if $(wildcard .venv-examples/bin/python),.venv-examples/bin/python,python3)

.PHONY: help setup setup-examples all assemble cover cover-art chapter-covers diagrams build latex draft pdf references \
        examples examples-run latex-validate validate deterministic qa-pdf latex-pdf dist-pdf \
        package release clean distclean

## help: show the available targets
help:
	@echo "Authoring loop"
	@echo "  setup           create .venv, install Python deps, install missing TeX packages"
	@echo "  draft           assemble + one XeLaTeX pass; fastest way to eyeball a change"
	@echo "  pdf             full three-pass XeLaTeX build -> dist/*.pdf"
	@echo "  all             build + latex + validate + the PDF in dist/ (rebuilt only when stale)"
	@echo ""
	@echo "Generation"
	@echo "  assemble        source/parts/*.md -> book/manuscript.md + dist/*.md"
	@echo "  cover           compose the cover (title over the committed cover art)"
	@echo "  cover-art       redraw the cover artwork from code (needs rsvg-convert)"
	@echo "  diagrams        render every diagram from its editable source"
	@echo "  chapter-covers  render the Letter-size chapter cover visuals"
	@echo "  build           assemble + cover + DOCX"
	@echo "  latex           generate latex/content/book-content.tex"
	@echo ""
	@echo "Verification"
	@echo "  examples        validate the code-example registry and markers"
	@echo "  examples-run    execute the example test suite against the pinned SDKs"
	@echo "  references      check every [Rxx] against config/references.json"
	@echo "  latex-validate  structural/contrast/asset checks on the LaTeX source"
	@echo "  validate        build + references + latex-validate + structural validators"
	@echo "  deterministic   rebuild twice and compare hashes"
	@echo "  qa-pdf          DOCX pagination QA (requires LibreOffice)"
	@echo ""
	@echo "Release"
	@echo "  package         regenerate manifest + checksums, write the release ZIP"
	@echo "  release         validate + deterministic + qa-pdf + pdf + package"
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
	$(MAKE) setup-examples
	@echo "Setup complete. Run 'make draft' or 'make pdf'."

## setup-examples: separate venv for the book's runnable examples.
## The SDKs the examples pin (openai-agents, mlflow) are heavy and must never
## become dependencies of the book build itself.
setup-examples:
	python3 -m venv .venv-examples
	.venv-examples/bin/python -m pip install --upgrade pip
	.venv-examples/bin/python -m pip install -r examples/requirements.txt

## all: everything a reader or reviewer needs in dist/ -- Markdown, DOCX, TeX and
## the XeLaTeX PDF. The PDF step is skipped with a notice when XeLaTeX is not
## installed, so `make all` still works on a machine without TeX.
all: build latex validate dist-pdf

assemble:
	$(PYTHON) tools/assemble_manuscript.py --root "$(ROOT)"

cover:
	$(PYTHON) tools/generate_cover.py --root "$(ROOT)"

## cover-art: redraw assets/cover/cover-art.png from tools/render_cover_art.py. Run it
## locally after changing the artwork; the PNG is committed so CI never needs rsvg.
cover-art:
	$(PYTHON) tools/render_cover_art.py --root "$(ROOT)"

## diagrams: render assets/diagrams/src/*.{gv,mmd,tikz.tex} to vector PDF for XeLaTeX
## and raster PNG for DOCX. Needs graphviz (.gv), mermaid-cli (.mmd) and XeLaTeX +
## poppler (.tikz.tex; ./tools/bootstrap_tex.sh --diagrams installs the TeX packages).
diagrams:
	$(PYTHON) tools/render_diagrams.py --root "$(ROOT)"

## chapter-covers: render one US Letter (8.5x11 in, 300 dpi) cover visual per
## chapter into cover-images/ from config/chapter-covers.json. Needs rsvg-convert.
chapter-covers:
	$(PYTHON) tools/render_chapter_covers.py --root "$(ROOT)"

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

## examples: registry/marker validation only -- no SDKs needed, so it runs in
## the book venv and belongs in `validate`.
examples:
	$(PYTHON) tools/check_examples.py --root "$(ROOT)"

## examples-run: actually executes the examples. Needs the examples venv.
examples-run:
	$(PYTHON) tools/check_examples.py --root "$(ROOT)" --run --python "$(PYTHON_EXAMPLES)"
	$(PYTHON_EXAMPLES) -m pytest tests/mortgage_case -q

latex-validate: latex
	$(PYTHON) tools/validate_latex.py --root "$(ROOT)"

validate: build references examples latex-validate
	$(PYTHON) tools/validate_book.py --root "$(ROOT)"

deterministic: build
	$(PYTHON) tools/deterministic_build_check.py --root "$(ROOT)"

qa-pdf: build
	$(PYTHON) tools/render_pdf_qa.py --root "$(ROOT)"

latex-pdf: latex-validate
	@./tools/bootstrap_tex.sh --check
	./latex/compile.sh

## dist-pdf: keep dist/*.pdf current. Compiles only when the PDF is missing
## or the content of anything it is built from (generated LaTeX, styles, diagram
## and cover renders, fonts) changed since the last compile -- compared by hash,
## because the generated LaTeX is rewritten on every run and timestamps would
## always look stale. Skips with a notice when XeLaTeX is unavailable. The PDF is
## gitignored and never committed (see AGENTS.md); CI publishes it as an artifact.
PDF_INPUT_DIRS := latex/content latex/styles latex/fonts assets/diagrams assets/cover cover-images
PDF_STAMP := latex/build/.pdf-inputs.sha256
dist-pdf: latex-validate
	@if ! PATH="/Library/TeX/texbin:$$PATH" command -v xelatex >/dev/null 2>&1; then \
		echo "dist-pdf: XeLaTeX not found; skipping $(PDF_OUT). Install TeX or use Dockerfile.latex / CI."; \
	else \
		mkdir -p latex/build; \
		cur=$$( { find $(PDF_INPUT_DIRS) -type f ! -name '.DS_Store' ; ls latex/*.tex latex/*.sty ; } | LC_ALL=C sort | xargs shasum -a 256 | shasum -a 256 | cut -d' ' -f1 ); \
		if [ -s "$(PDF_OUT)" ] && [ -f "$(PDF_STAMP)" ] && [ "$$(cat $(PDF_STAMP))" = "$$cur" ]; then \
			echo "dist-pdf: $(PDF_OUT) is up to date."; \
		else \
			PATH="/Library/TeX/texbin:$$PATH" ./tools/bootstrap_tex.sh --check && PATH="/Library/TeX/texbin:$$PATH" ./latex/compile.sh && echo "$$cur" > $(PDF_STAMP); \
		fi; \
	fi

## package: runs the examples for real first, so the committed
## reports/examples-report.json is evidence of execution rather than of a
## metadata-only check. `validate` runs the checker without --run, which would
## otherwise overwrite the executed report with tests_executed:false.
package: validate examples-run
	$(PYTHON) tools/package_release.py --root "$(ROOT)" --output "$(ZIP)"

release: validate deterministic qa-pdf pdf package

clean:
	rm -rf qa/determinism latex/build
	rm -f qa/validation-report.json qa/latex-validation-report.json reports/validation-summary.md reports/latex-validation.md reports/assembly-report.json

distclean: clean
	rm -rf .venv .venv-examples
