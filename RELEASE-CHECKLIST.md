# Release Checklist

## Editorial

- [ ] Read the manuscript end-to-end or perform a documented full-book review.
- [ ] Verify Part/chapter progression, prerequisites, transitions, and conclusion alignment.
- [ ] Remove duplication, contradictions, placeholder text, and stale version labels.
- [ ] Confirm terminology and capitalization against the design system.

## Technical and evidence

- [ ] Validate architecture diagrams, formulas, tables, examples, code, and maturity caveats.
- [ ] Confirm every attributed claim has a scoped `[Rxx]` marker.
- [ ] Confirm every registry URL, title, version/date, and permitted scope.
- [ ] Record unavailable sources honestly; weaken unsupported claims.
- [ ] Run `python3 tools/check_references.py --root .`.

## Build and visual QA

- [ ] Run `make clean build validate`.
- [ ] Run `make pdf` and confirm the log reports zero errors and zero undefined references.
- [ ] Confirm the DOCX and XeLaTeX editions agree on structure: Part dividers standalone, every chapter/appendix starting a new page, all 18 diagrams present.
- [ ] Run deterministic build twice and confirm equal hashes.
- [ ] Run `make qa-pdf` and inspect cover, title, TOC, every Part, representative chapter starts, tables, code, callouts, diagrams, appendices, and references.
- [ ] Confirm every Part/chapter/appendix starts on a new page.
- [ ] Confirm no unintended blank pages, clipped diagrams, orphan headings, or illegible tables.

## Package

- [ ] Update version, date, README, CHANGELOG, and release notes.
- [ ] Generate `RELEASE-MANIFEST.json` and `CHECKSUMS.sha256`.
- [ ] Run `make package`.
- [ ] Extract the ZIP into a clean directory.
- [ ] Run `make validate` using only extracted contents.
- [ ] Confirm the final DOCX and Markdown hashes match the manifest.
- [ ] Tag the release so CI attaches the compiled PDF, DOCX, and Markdown to the GitHub Release.

## Notion

- [ ] Read the destination pages and permission metadata.
- [ ] Preserve child pages and approved sharing scope.
- [ ] Publish the exact validated DOCX, Markdown, ZIP, and cover.
- [ ] Record version, author, date, counts, hashes, citation status, and QA status.
- [ ] Verify the published page after mutation.

Release is complete only when every applicable item is checked or an explicit, reviewable exception is recorded.
