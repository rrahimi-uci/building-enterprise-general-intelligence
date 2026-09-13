PYTHON ?= python3
ROOT := $(CURDIR)
ZIP ?= $(abspath ../Enterprise-Agentic-AI-Book-v1.0.0-Development-Package.zip)

.PHONY: all assemble cover build references validate deterministic qa-pdf package release clean

all: build validate

assemble:
	$(PYTHON) tools/assemble_manuscript.py --root "$(ROOT)"

cover:
	$(PYTHON) tools/generate_cover.py --root "$(ROOT)"

build: assemble cover
	$(PYTHON) tools/build_book.py --root "$(ROOT)"
	$(PYTHON) tools/build_book.py --root "$(ROOT)" --template-only

references: assemble
	$(PYTHON) tools/check_references.py --root "$(ROOT)"

validate: build references
	$(PYTHON) tools/validate_book.py --root "$(ROOT)"

deterministic: build
	$(PYTHON) tools/deterministic_build_check.py --root "$(ROOT)"

qa-pdf: build
	$(PYTHON) tools/render_pdf_qa.py --root "$(ROOT)"

package:
	$(PYTHON) tools/package_release.py --root "$(ROOT)" --output "$(ZIP)"

release: build references validate deterministic qa-pdf package

clean:
	rm -rf qa/determinism
	rm -f qa/validation-report.json reports/validation-summary.md reports/assembly-report.json
