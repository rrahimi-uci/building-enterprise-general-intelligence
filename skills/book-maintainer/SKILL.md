# Skill: Book Maintainer

## Use when

Adding, changing, moving, or deleting chapters, appendices, front matter, or design-system components.

## Inputs

- User-approved editorial intent.
- Canonical files under `source/parts/`.
- `config/book.json`, `config/diagrams.json`, and `config/references.json`.
- Adjacent chapters and transitions.

## Procedure

1. Read `AGENTS.md`, both style documents, the complete affected Part, and the previous/next chapter endings.
2. Map impact: TOC, headings, numbering, cross-references, diagrams, tables, examples, citations, appendices, and release metadata.
3. Edit only canonical source/configuration/assets. Preserve stable pattern/reference/diagram identifiers where semantics remain the same.
4. Re-establish narrative progression: motivation → definitions → architecture → implementation → operation → synthesis.
5. Assemble with `python3 tools/assemble_manuscript.py --root .` and review a source diff.
6. Build with `python3 tools/build_book.py --root .`.
7. Run reference and structural validation.
8. For visual/topology changes, run PDF QA and inspect the contact sheet.
9. Update changelog and, for releases, package and clean-extraction test.
10. Synchronize Notion only after exact artifacts pass.

## Guardrails

- Do not edit generated Markdown/DOCX.
- Do not run the legacy migration tool during normal maintenance.
- Do not add unsourced factual claims or imply illustrative values are benchmarks.
- Do not weaken security/governance controls to simplify an example.
- Do not broaden private content when publishing without approval.

## Output

A coherent source change plus regenerated Markdown/DOCX, passing reports, updated changelog, and—only for approved releases—updated package and Notion representation.
