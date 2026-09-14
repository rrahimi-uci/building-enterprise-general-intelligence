#!/usr/bin/env python3
"""Offline structural, semantic, asset, and DOCX validation for Book v2.0.0."""
from __future__ import annotations
import argparse, hashlib, json, re, sys, zipfile
import json
from pathlib import Path
from collections import Counter
from docx import Document
from PIL import Image


def book_release(root: Path) -> str:
    """The single source of the release identifier.

    Hard-coding it meant a generated report could claim 1.0.0 while every other
    artifact said 2.0.0 -- the evidence disagreeing with the thing it certifies.
    """
    return json.loads((root / "config" / "book.json").read_text(encoding="utf-8"))["book"]["version"]



def sha(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()


def check_table_shapes(text: str) -> list[str]:
    errors=[]; lines=text.splitlines(); i=0
    while i<len(lines):
        if lines[i].lstrip().startswith('|'):
            start=i; block=[]
            while i<len(lines) and lines[i].lstrip().startswith('|'):
                block.append(lines[i]); i+=1
            if len(block)>=2 and re.search(r'\|\s*:?-{3,}',block[1]):
                widths=[]
                for row in block:
                    widths.append(len(re.split(r'(?<!\\)\|',row.strip().strip('|'))))
                if len(set(widths))>1: errors.append(f"Markdown table near line {start+1} has inconsistent columns: {widths}")
            continue
        i+=1
    return errors


def docx_callout_contrast(docx_path):
    """Every shaded callout cell must carry readable body text.

    v2.0.0 shaded NORTHSTAR/DESIGN DECISION callouts navy while the paragraph
    style inherited Normal's dark ink -- 44 callouts at 1.09:1. The LaTeX
    contrast gate never saw it because it only reads the LaTeX palette, so the
    DOCX edition needs its own check.
    """
    from docx import Document
    from docx.oxml.ns import qn

    def luminance(value):
        channels = [int(value[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
        return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]

    def ratio(a, b):
        la, lb = luminance(a), luminance(b)
        return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)

    document = Document(str(docx_path))
    failures = []
    for table in document.tables:
        if len(table.columns) != 1 or len(table.rows) != 1:
            continue
        cell = table.cell(0, 0)
        paragraph = cell.paragraphs[0]
        if paragraph.style.name != 'Book Callout':
            continue
        properties = cell._tc.tcPr
        shading = properties.find(qn('w:shd')) if properties is not None else None
        fill = shading.get(qn('w:fill')) if shading is not None else 'FFFFFF'
        # 'Book Callout' inherits Normal, so the body ink is the book ink.
        measured = ratio('12233F', fill)
        if measured < 4.5:
            failures.append({'fill': fill, 'ratio': round(measured, 2),
                             'text': cell.text.strip()[:60]})
    return failures


def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default=str(Path(__file__).resolve().parents[1])); args=ap.parse_args()
    root=Path(args.root).resolve(); errors=[]; warnings=[]; checks={}
    md=root/'book/manuscript.md'; distmd=root/'dist/Enterprise-Agentic-AI-Architecture-Developer-Platform-Guide-v2.0.0.md'; docx_path=root/'dist/Enterprise-Agentic-AI-Architecture-Developer-Platform-Guide-v2.0.0.docx'
    required=[root/'README.md',root/'AGENTS.md',root/'CHANGELOG.md',root/'styles/DESIGN-SYSTEM.md',root/'styles/CROSS-FORMAT-CONTRACT.md',root/'config/book.json',root/'config/references.json',root/'config/reference-verification.json',root/'config/diagrams.json',md,distmd,docx_path,root/'assets/cover/cover-v2.0.0.png',root/'templates/book-style-template.docx']
    missing=[p.relative_to(root).as_posix() for p in required if not p.exists()]
    if missing: errors.append(f"Missing required files: {missing}")
    if not md.exists(): raise SystemExit(1)
    text=md.read_text(encoding='utf-8'); b=text.encode('utf-8')
    checks['canonical_markdown_sha256']=hashlib.sha256(b).hexdigest(); checks['canonical_markdown_bytes']=len(b)
    if not text.endswith('\n'): errors.append('Canonical Markdown needs one trailing newline')
    if '\r' in text: errors.append('Canonical Markdown contains CR characters')
    if distmd.exists() and distmd.read_bytes()!=md.read_bytes(): errors.append('Canonical and distributable Markdown are not byte-identical')
    checks['parts']=len(re.findall(r'^# PART [IVXLCDM]+ — ',text,re.M)); checks['chapters']=len(re.findall(r'^# \d{2} — ',text,re.M)); checks['appendices']=len(re.findall(r'^# Appendix [A-Z] — ',text,re.M))
    # v2.0.0 topology: four single-chapter Parts dissolved, four chapter pairs
    # merged, Appendices L and N cut and M folded into K.
    expected={'parts':8,'chapters':27,'appendices':12}
    for k,v in expected.items():
        if checks[k]!=v: errors.append(f"Expected {v} {k}, found {checks[k]}")
    chapter_nums=[int(x) for x in re.findall(r'^# (\d{2}) — ',text,re.M)]
    if chapter_nums!=list(range(1,28)): errors.append(f"Chapter sequence is invalid: {chapter_nums}")
    appendix_ids=re.findall(r'^# Appendix ([A-Z]) — ',text,re.M)
    if appendix_ids!=[chr(ord('A')+i) for i in range(12)]: errors.append(f"Appendix sequence is invalid: {appendix_ids}")
    # Fenced code must be masked before scanning for headings: a Python comment
    # like "# Captures OpenAI calls" is indistinguishable from an H1 otherwise,
    # and the book's examples are full of them. Replacing each fenced block with
    # blank lines of equal length keeps reported line numbers accurate.
    def _mask_code(source):
        out, in_code = [], False
        for line in source.split('\n'):
            if line.startswith('```'):
                in_code = not in_code
                out.append('')
            else:
                out.append('' if in_code else line)
        return '\n'.join(out)
    prose=_mask_code(text)
    headings=[(len(m.group(1)),m.group(2),prose.count('\n',0,m.start())+1) for m in re.finditer(r'^(#{1,4})\s+(.+)$',prose,re.M)]
    prev=1
    for level,title,line in headings:
        if level>prev+1: errors.append(f"Heading level skips from H{prev} to H{level} at line {line}: {title}")
        prev=level
    if text.count('```')%2: errors.append('Unbalanced fenced code blocks')
    checks['code_blocks']=len(re.findall(r'^```[^\n]*$',text,re.M))//2
    errors.extend(check_table_shapes(text))
    # Legacy pre-1.0 labels. The negative lookahead stops the real v2.0.0 release
    # string from matching the v2.0 legacy pattern.
    stale=sorted(set(re.findall(r'\bv(?:2\.[01]|3\.[01])(?!\.\d)\b',text)))
    if stale: errors.append(f"Stale release labels remain: {stale}")
    for bad in ['25 August 2026','MLflow 3.16.0 exists','Amazon Bedrock Agents / AgentCore']:
        if bad in text: errors.append(f"Unsupported/stale claim remains: {bad}")
    if 'Reza Rahimi, PhD' not in text: errors.append('Author string missing from Markdown')
    if 'Bedrock Agents Classic' not in text or 'maintenance mode' not in text: errors.append('Bedrock Classic maturity caveat missing')
    if '3.15.2 as a reproducibility baseline' not in text: errors.append('MLflow reproducibility-pin caveat missing')
    refs=json.loads((root/'config/references.json').read_text(encoding='utf-8'))['references']
    ref_ids=[r['id'] for r in refs]; citations=re.findall(r'\[(R\d{2})\]',text)
    checks['reference_count']=len(refs); checks['citation_occurrences']=len(citations); checks['cited_reference_ids']=len(set(citations))
    if set(citations)!=set(ref_ids): errors.append(f"Reference/citation set mismatch: missing={sorted(set(ref_ids)-set(citations))}, unknown={sorted(set(citations)-set(ref_ids))}")
    if any(citations.count(x)==0 for x in ref_ids): errors.append('At least one reference is uncited')
    diags=json.loads((root/'config/diagrams.json').read_text(encoding='utf-8'))['diagrams']; diag_by_id={d['id']:d for d in diags}; markers=re.findall(r'^\[\[DIAGRAM:([^|\]]+)\|([^\]]+)\]\]$',text,re.M)
    checks['diagram_markers']=len(markers); checks['registered_diagrams']=len(diags)
    marker_ids=[x[0] for x in markers]
    if Counter(marker_ids)!=Counter(diag_by_id.keys()): errors.append(f"Diagram registry/marker mismatch: markers={sorted(marker_ids)}, registry={sorted(diag_by_id)}")
    for d in diags:
        p=root/d['file']
        if not p.exists(): errors.append(f"Missing diagram asset {d['file']}"); continue
        if sha(p)!=d['sha256']: errors.append(f"Diagram checksum mismatch: {d['file']}")
        try:
            with Image.open(p) as im:
                if im.width<1200 or im.height<600: warnings.append(f"Diagram may be low resolution: {d['file']} ({im.width}x{im.height})")
        except Exception as exc: errors.append(f"Cannot decode diagram {d['file']}: {exc}")
    cover=root/'assets/cover/cover-v2.0.0.png'
    if cover.exists():
        with Image.open(cover) as im:
            checks['cover_dimensions']=[im.width,im.height]
            if (im.width,im.height)!=(2550,3300): errors.append(f"Unexpected cover dimensions: {im.size}")
    if docx_path.exists():
        try:
            with zipfile.ZipFile(docx_path) as z:
                bad=z.testzip()
                if bad: errors.append(f"Corrupt DOCX member: {bad}")
            doc=Document(docx_path)
            checks['docx_sha256']=sha(docx_path); checks['docx_bytes']=docx_path.stat().st_size; checks['docx_paragraphs']=len(doc.paragraphs); checks['docx_tables']=len(doc.tables); checks['docx_inline_images']=len(doc.inline_shapes)
            style_names={s.name for s in doc.styles}; required_styles={'Normal','Title','Subtitle','Heading 1','Heading 2','Heading 3','Heading 4','Caption','Book Part','Book Callout','Book Evidence','Book Reference','Book Code Label'}
            missing_styles=sorted(required_styles-style_names)
            if missing_styles: errors.append(f"DOCX styles missing: {missing_styles}")
            doc_chapters=sum(1 for p in doc.paragraphs if p.style.name=='Heading 1' and re.match(r'^\d{2} — ',p.text))
            doc_appendices=sum(1 for p in doc.paragraphs if p.style.name=='Heading 1' and p.text.startswith('Appendix '))
            checks['docx_chapters']=doc_chapters; checks['docx_appendices']=doc_appendices
            if doc_chapters!=27 or doc_appendices!=12: errors.append(f"DOCX heading counts differ: chapters={doc_chapters}, appendices={doc_appendices}")
            # Derived, not fixed: cover + registered diagrams + registered Part
            # panels. A literal only proved the book had not gained an image.
            pv=root/'config/part-visuals.json'
            visuals=json.loads(pv.read_text(encoding='utf-8'))['visuals'] if pv.exists() else []
            expected_images=1+len(diags)+len(visuals)
            checks['expected_docx_images']=expected_images
            if len(doc.inline_shapes)!=expected_images: errors.append(f"Expected {expected_images} DOCX images (cover + {len(diags)} diagrams + {len(visuals)} Part panels), found {len(doc.inline_shapes)}")
            for v in visuals:
                asset=root/v['file']
                if not asset.exists(): errors.append(f"Missing Part {v['part']} panel {v['file']}"); continue
                if v.get('sha256') and sha(asset)!=v['sha256']: errors.append(f"Part {v['part']} panel checksum mismatch: {v['file']}")
            callout_failures=docx_callout_contrast(docx_path)
            checks['docx_callout_contrast_failures']=len(callout_failures)
            for failure in callout_failures:
                errors.append(f"DOCX callout is unreadable: ink on #{failure['fill']} = {failure['ratio']}:1 — {failure['text']}")
            cp=doc.core_properties
            if cp.title!='Enterprise Agentic AI Architecture & Developer Platform Guide — Book v2.0.0': errors.append(f"Unexpected DOCX title metadata: {cp.title}")
            if cp.author!='Reza Rahimi, PhD': errors.append(f"Unexpected DOCX author metadata: {cp.author}")
        except Exception as exc: errors.append(f"DOCX validation error: {exc}")
    pdf=root/'qa/render/Enterprise-Agentic-AI-Architecture-Developer-Platform-Guide-v2.0.0.pdf'
    if pdf.exists():
        try:
            import pymupdf
            d=pymupdf.open(pdf); checks['pdf_pages']=len(d)
            # 213 was the v1.0.0 LibreOffice baseline. v2.0.0 deliberately changed the
            # topology, so asserting it would warn about the expected result; the page
            # count is recorded as a measurement until a v2.0.0 baseline is rendered
            # with `make qa-pdf`. Structural and blank-page checks below still apply.
            blank=[]
            for i,p in enumerate(d):
                if len(p.get_text().strip())<8 and not p.get_images(full=True): blank.append(i+1)
            checks['blank_pdf_pages']=blank
            if blank: errors.append(f"Unintended blank PDF pages: {blank}")
            d.close()
        except Exception as exc: warnings.append(f"PDF QA inspection unavailable: {exc}")
    report={'release':book_release(root),'validated_on':'2026-09-13','checks':checks,'errors':errors,'warnings':warnings,'pass':not errors}
    (root/'qa').mkdir(exist_ok=True); (root/'reports').mkdir(exist_ok=True)
    (root/'qa/validation-report.json').write_text(json.dumps(report,indent=2)+"\n",encoding='utf-8')
    summary=["# Validation Summary — Book v2.0.0","",f"**Result:** {'PASS' if not errors else 'FAIL'}","", "## Measurements","",* [f"- **{k}:** `{v}`" for k,v in checks.items()],"","## Errors","",*([f"- {x}" for x in errors] or ["- None."]),"","## Warnings","",*([f"- {x}" for x in warnings] or ["- None."])]
    (root/'reports/validation-summary.md').write_text('\n'.join(summary)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2)); return 0 if not errors else 1

if __name__=='__main__': sys.exit(main())
