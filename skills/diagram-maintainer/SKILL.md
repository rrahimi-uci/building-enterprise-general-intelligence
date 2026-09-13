# Skill: Diagram Maintainer

## Objective

Create or revise diagrams that teach an architectural concept while preserving visual, accessibility, registry, and cross-format integrity.

## Procedure

1. Define the lesson in one sentence. If the lesson is not distinct from nearby prose/table, do not add a diagram.
2. Model nodes, flows, trust boundaries, state ownership, policy points, failure paths, and evidence capture before styling.
3. Start from `templates/diagram-spec.template.json` or edit a source asset with deterministic tools.
4. Use the book tokens: Navy/Blue/Cyan/Teal for structure and controlled flow; Amber/Red only for decisions/risks. Pair color with labels or line semantics.
5. Export at publication scale (maximum 6.85 in in DOCX, ideally 300 dpi equivalent).
6. Add/update `config/diagrams.json` with stable ID, file, caption, chapter, lesson, and accessibility description.
7. Insert `[[DIAGRAM:id|caption]]` on its own line in canonical Markdown.
8. Run asset/reference validators, rebuild DOCX, render PDF, and inspect at 100% plus contact-sheet scale.
9. Confirm labels are legible, arrows unambiguous, captions descriptive, and surrounding prose explains the visual.

## Guardrails

- No decorative chapter art.
- No meaning by color alone.
- No unregistered asset, ambiguous unlabeled arrow, tiny text, unexplained acronym, or screenshot containing private data.
- Replacing an existing ID means the same architectural lesson; otherwise allocate a new ID.

## Output

Registered source/export asset, canonical marker/caption, passing hash/visual checks, and updated changelog for release changes.
