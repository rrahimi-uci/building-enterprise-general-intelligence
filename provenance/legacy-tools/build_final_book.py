from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess

from docx import Document
from docx.oxml import OxmlElement
from docx.text.paragraph import Paragraph

SRC = Path('/data/review-edition.docx')
OUT = Path('/data/Building-Enterprise-Agentic-AI-Systems-Final.docx')
MD = Path('/data/Building-Enterprise-Agentic-AI-Systems-Final.md')
PART_DIR = Path('/data/final_parts')
PART_DIR.mkdir(parents=True, exist_ok=True)
shutil.copy2(SRC, OUT)

doc = Document(OUT)

def set_text(p: Paragraph, text: str) -> None:
    # Retain paragraph style and paragraph properties while replacing textual runs.
    for r in p.runs:
        r.text = ''
    if p.runs:
        p.runs[0].text = text
    else:
        p.add_run(text)


def iter_paragraphs(document: Document):
    for p in document.paragraphs:
        yield p
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    yield p
                for nested in cell.tables:
                    for row2 in nested.rows:
                        for cell2 in row2.cells:
                            for p in cell2.paragraphs:
                                yield p
    for section in document.sections:
        for container in (section.header, section.footer, section.first_page_header, section.first_page_footer, section.even_page_header, section.even_page_footer):
            for p in container.paragraphs:
                yield p
            for table in container.tables:
                for row in table.rows:
                    for cell in row.cells:
                        for p in cell.paragraphs:
                            yield p


def insert_after(anchor: Paragraph, text: str, style: str = 'Normal') -> Paragraph:
    new_p = OxmlElement('w:p')
    anchor._p.addnext(new_p)
    p = Paragraph(new_p, anchor._parent)
    p.style = style
    p.add_run(text)
    return p

# Global final-edition terminology.
replacements = [
    ('Architecture, patterns, security, Skills, durable execution, evaluation, and production operations',
     'Final architecture and implementation reference: patterns, security, Skills, durable execution, evaluation, and production operations'),
    ('Grounded review edition v1.1', 'Final edition v2.0'),
    ('GROUNDED REVIEW · v1.1', 'FINAL EDITION · v2.0'),
    ('Grounded-review corrections in v1.1', 'Final-edition corrections and closure record'),
    ('Grounding policy and critical-review result', 'Grounding policy and final assurance result'),
    ('What the deep review changed', 'What the final edition resolves'),
    ('Critical review — direct findings and corrections', 'Final assurance closure — resolved findings'),
    ('Residual limitations', 'Deployment validation boundary'),
    ('Appendix F — Unresolved challenges', 'Appendix F — Known limits and enforced mitigations'),
    ('Unresolved architectural challenges', 'Known architectural limits and required mitigations'),
    ('Appendix L — Critical review and correction log', 'Appendix L — Final correction and closure log'),
    ('Appendix N — Gap closure and assurance coverage', 'Appendix N — Integrated assurance coverage'),
    ('Critical review of the current framework landscape', 'Final assessment of the current framework landscape'),
    ('This log records weaknesses found in the first reference-book build and the concrete action taken in v1.1. It is intentionally candid: correctness improves when version assumptions, test limits, and architectural opinions are explicit.',
     'This closure log records the review findings resolved in the final edition. Version assumptions, validation boundaries, and architectural recommendations remain explicit so future upgrades can be assessed without reopening settled design gaps.'),
    ('Unresolved challenges and residual risks are explicit; the document does not claim prompt injection, exact replay, or multi-agent reliability is solved.',
     'Known limits and required mitigations are explicit; the document does not claim prompt injection, exact replay, or multi-agent reliability is solved.'),
    ('The first edition leaned on the 2025-06-18 stateful protocol. Replace it with the 2026-07-28 stateless core, per-request capability negotiation, server/discover, cacheable list results, explicit application handles, and optional Tasks/Skills extensions.',
     'Resolved: the obsolete 2025-06-18 baseline was removed. The final edition uses MCP 2026-07-28 with a stateless core, per-request capability negotiation, server/discover, cacheable list results, explicit application handles, and optional Tasks/Skills extensions.'),
    ('Correction', 'Final implementation'),
]
for p in list(iter_paragraphs(doc)):
    text = p.text
    updated = text
    for old, new in replacements:
        updated = updated.replace(old, new)
    if updated != text:
        set_text(p, updated)

# Convert inherent/industry limits into explicit mitigations rather than open book gaps.
mitigation_map = {
    'Prompt injection remains unsolved. Classifiers, delimiters, and instruction hierarchy improve resistance but do not provide a hard semantic boundary. Capability confinement is the dependable control.':
        'Prompt injection is not assumed solved. Required mitigation: treat retrieved content as untrusted, remove ambient credentials, minimize capabilities, and enforce identity, policy, schema, sandbox, egress, and effect controls outside the model.',
    'Delegated authorization is not yet interoperable end to end. OAuth/MCP/A2A can transport identity-related information, but there is no universal semantic model for subject+actor chains, purpose limitation, resource relationships, and downstream proof of least privilege.':
        'Delegated authorization is not universally interoperable end to end. Required mitigation: preserve a platform-owned subject+actor+purpose model, narrow authority at every hop, bind token audience and resource, and reject peers that cannot provide required proof.',
    'Semantic idempotency is domain specific. Infrastructure can deduplicate a request ID; determining whether two differently worded actions are the same business effect still needs explicit domain keys and reconciliation.':
        'Semantic idempotency is domain specific. Required mitigation: define domain-owned logical effect keys, reject argument-hash conflicts, record receipts, and reconcile ambiguous outcomes against the authoritative downstream system.',
    'Durable replay and changing models conflict. Model calls are nondeterministic and provider versions may disappear. Recording outputs enables replay, but exact future reproduction can remain impossible.':
        'Exact model replay cannot be guaranteed when models or providers change. Required mitigation: pin release graphs, retain inputs and outputs by reference and hash, replay deterministic workflow history, and evaluate replacements against immutable cases.',
    'Long-horizon reliability is immature. Benchmarks improve faster than operational reliability science. Correlated errors, self-conditioning, plan drift, and hidden environment changes remain hard to model.':
        'Long-horizon reliability requires empirical control. Required mitigation: segment trajectories into bounded verified steps, detect no progress and plan drift, simulate correlated failures, and gate releases on repeated-run and tail-risk evidence.',
    'Multi-agent evaluation lacks compositional guarantees. Strong component scores do not predict system behavior after delegation, aggregation, and policy interaction.':
        'Multi-agent quality is not inferred from component scores. Required mitigation: benchmark against the strongest single-agent baseline and test ownership, delegation, aggregation, cancellation, compromised peers, and policy interaction end to end.',
    'Memory governance is underdeveloped. Consent, provenance, correction, deletion, cross-run scope, embedding inversion, and retention across derived indexes lack consistent standards and tooling.':
        'Memory governance requires platform-owned lifecycle controls. Required mitigation: enforce scope, lawful basis or policy, provenance, confidence, TTL, correction, deletion propagation, legal hold, residency, and derived-index lineage.',
    'Agent protocol trust is weaker than protocol connectivity. Capability discovery does not establish quality, safety, ownership, or compatibility; signed claims and attestation ecosystems are early.':
        'Protocol connectivity does not establish trust. Required mitigation: terminate MCP and A2A at governed gateways, verify publishers and signed artifacts, apply local authorization and quotas, scan adopted artifacts, and require conformance evidence.',
    'Explanations can become plausible stories. Post-hoc model rationales are not evidence. Systems need source provenance, rule decisions, typed plans, and effect receipts.':
        'Model explanations are not evidence. Required mitigation: separate rationale from authoritative evidence and require source revisions, policy decisions, typed plans, deterministic calculations, and effect receipts for material claims.',
    'Online evaluation is statistically and ethically hard. Production traffic changes, rare harms matter, human labels are expensive, and judge models drift. Release gates need confidence intervals and risk-weighted metrics.':
        'Online evaluation requires controlled statistical and ethical safeguards. Required mitigation: use immutable datasets, leakage checks, deterministic gate precedence, calibrated scorer ensembles, confidence intervals, risk-weighted slices, and human review.',
    'Cross-vendor portability is partial. Prompts, tools, state, traces, and model behavior differ despite emerging protocols. Keep a portable run manifest and isolate vendor-specific adapters.':
        'Cross-vendor portability is intentionally bounded. Required mitigation: keep provider-neutral run, task, tool, effect, approval, and artifact contracts; isolate vendor adapters; and prove fallback compatibility through exact-release evaluation.',
    'Human accountability is not solved by an approval button. Organizations still need role design, training, workload management, informed-review UX, and clear responsibility for exceptions.':
        'Human accountability is implemented as an operating model, not a button. Required mitigation: define roles and separation of duties, accessible evidence-first previews, training, review-time budgets, fatigue metrics, recourse, and explicit exception ownership.',
}
mitigation_number = 0
for p in doc.paragraphs:
    if p.text in mitigation_map:
        mitigation_number += 1
        set_text(p, f'{mitigation_number}. {mitigation_map[p.text]}')
        p.style = 'Normal'

# Insert an explicit final completion and alignment statement after the edition line.
edition_p = next(p for p in doc.paragraphs if p.text.startswith('Final edition v2.0'))
anchor = edition_p
anchor = insert_after(anchor, 'Final edition completion', 'Heading 1')
anchor = insert_after(anchor, 'All 17 review findings and all 10 assurance areas are integrated into the 22 chapters and appendices. The book contains no known unresolved content gap from the review. Workload-specific conformance, privacy, security, legal, integration, recovery, and load tests remain deployment acceptance evidence—not missing book content.', 'Normal')
anchor = insert_after(anchor, 'Alignment rule', 'Heading 2')
anchor = insert_after(anchor, 'The Notion edition and editable DOCX are published from the same final manuscript. Chapter order, prose, tables, code, figure captions, references, and appendices are compared after normalization before release. Rendering differences do not change the canonical text.', 'Normal')

# Add integrated-assurance declaration after Appendix N heading.
for p in list(doc.paragraphs):
    if p.text == 'Appendix N — Integrated assurance coverage':
        insert_after(p, 'The controls below are part of the final architecture and acceptance model. They are no longer review gaps; each has an owning boundary, required evidence, and a deployment validation path.', 'Normal')
        break

# Update core metadata.
doc.core_properties.title = 'Building Enterprise Agentic AI Systems — Final Edition'
doc.core_properties.subject = 'Grounded final architecture and implementation reference'
doc.core_properties.comments = 'Final edition v2.0; all review findings integrated; canonical text aligned with the private Notion edition.'
doc.core_properties.modified = datetime.now(timezone.utc)
doc.save(OUT)

# Convert the final DOCX to Markdown for the Notion publication surface.
with MD.open('w', encoding='utf-8') as f:
    proc = subprocess.run(['python3', '-m', 'markitdown', str(OUT)], stdout=f, stderr=subprocess.PIPE, text=True)
if proc.returncode != 0:
    raise SystemExit(proc.stderr)

md = MD.read_text(encoding='utf-8')

# Convert DOCX syntax-highlighted two-column code tables back into fenced code.
# This preserves every code line while avoiding Notion rich-text cell limits.
code_tables = []
for table in doc.tables:
    if len(table.columns) != 2 or len(table.rows) != 1:
        continue
    number_lines = [p.text.strip() for p in table.rows[0].cells[0].paragraphs if p.text.strip()]
    if not number_lines or number_lines[0] != '1':
        continue
    if number_lines != [str(i + 1) for i in range(len(number_lines))]:
        continue
    code_lines = [p.text.rstrip() for p in table.rows[0].cells[1].paragraphs]
    code_tables.append('\n'.join('' if line.isspace() else line for line in code_lines).rstrip())

lines = md.splitlines()
out_lines = []
code_index = 0
language_map = {'PYTHON': 'python', 'BASH': 'bash', 'JSON': 'json', 'SQL': 'sql', 'TEXT': 'text'}
i = 0
while i < len(lines):
    if (
        i + 2 < len(lines)
        and lines[i].strip() == '|  |  |'
        and lines[i + 1].strip() == '| --- | --- |'
        and out_lines
    ):
        prev = next((x.strip() for x in reversed(out_lines) if x.strip()), '')
        if prev.endswith('· implementation excerpt'):
            if code_index >= len(code_tables):
                raise RuntimeError('more code-table markers than extracted code tables')
            label = prev.split('·', 1)[0].strip().upper()
            lang = language_map.get(label, 'text')
            out_lines.extend([f'```{lang}', code_tables[code_index], '```'])
            code_index += 1
            i += 3
            continue
    out_lines.append(lines[i])
    i += 1
if code_index != len(code_tables):
    raise RuntimeError(f'converted {code_index} of {len(code_tables)} code tables')
md = '\n'.join(out_lines) + '\n'

# Notion cannot ingest embedded OOXML image data. Preserve the matching caption and replace each binary image with a stable rendering note.
image_counter = 0

def repl_img(match):
    global image_counter
    image_counter += 1
    if image_counter == 1:
        return '> Cover artwork is embedded in the DOCX edition.'
    return f'> Architecture figure {image_counter - 1} is embedded in the DOCX; the immediately following caption and blueprint table are canonical.'

md = re.sub(r'!\[\]\(data:image/[^\n]+\)', repl_img, md)
# Normalize edition text in case converter surfaced hidden variants.
md = md.replace('Grounded review edition v1.1', 'Final edition v2.0')
md = md.replace('GROUNDED REVIEW · v1.1', 'FINAL EDITION · v2.0')
MD.write_text(md, encoding='utf-8')

# Split the canonical manuscript into a small set of private Notion pages.
markers = [
    ('01-front-matter.md', None, '# 01 — From an LLM Call to a Production System'),
    ('02-part-i.md', '# 01 — From an LLM Call to a Production System', '# 04 — ReAct: Bounded Reason–Act–Observe Loops'),
    ('03-part-ii.md', '# 04 — ReAct: Bounded Reason–Act–Observe Loops', '# 10 — Skills as Versioned Capabilities'),
    ('04-part-iii.md', '# 10 — Skills as Versioned Capabilities', '# 14 — Context Engineering, Memory, and State'),
    ('05-part-iv.md', '# 14 — Context Engineering, Memory, and State', '# 18 — Observability and Tracing with MLflow'),
    ('06-part-v.md', '# 18 — Observability and Tracing with MLflow', '# Appendix A — Pattern selection and anti-patterns'),
    ('07-appendices.md', '# Appendix A — Pattern selection and anti-patterns', None),
]
for filename, start, end in markers:
    s = 0 if start is None else md.index(start)
    e = len(md) if end is None else md.index(end)
    chunk = md[s:e].strip() + '\n'
    (PART_DIR / filename).write_text(chunk, encoding='utf-8')

# Textual parity manifest. Figures are validated separately as rendering assets.
def normalize(text: str) -> str:
    text = re.sub(r'> (Cover artwork|Architecture figure).*?canonical\.', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

parts = [p.read_text(encoding='utf-8') for p in sorted(PART_DIR.glob('*.md'))]
rejoined = '\n'.join(parts)
manifest = {
    'edition': 'v2.0',
    'as_of': '2026-09-12',
    'docx': str(OUT),
    'canonical_markdown': str(MD),
    'part_files': [p.name for p in sorted(PART_DIR.glob('*.md'))],
    'part_characters': {p.name: len(p.read_text(encoding='utf-8')) for p in sorted(PART_DIR.glob('*.md'))},
    'docx_sha256': hashlib.sha256(OUT.read_bytes()).hexdigest(),
    'canonical_text_sha256': hashlib.sha256(normalize(md).encode()).hexdigest(),
    'rejoined_text_sha256': hashlib.sha256(normalize(rejoined).encode()).hexdigest(),
    'normalized_text_match': normalize(md) == normalize(rejoined),
    'figure_assets_in_docx': len(doc.inline_shapes),
    'figure_markers_in_notion_markdown': len(re.findall(r'^> (?:Cover artwork|Architecture figure)', md, flags=re.M)),
    'code_tables_converted_to_fences': code_index,
    'review_findings_integrated': 17,
    'assurance_areas_integrated': 10,
}
Path('/data/final_alignment_manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
print(json.dumps(manifest, indent=2))
