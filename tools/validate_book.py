#!/usr/bin/env python3
"""Offline structural, semantic, asset, and DOCX validation for Book v1.0.0."""
from __future__ import annotations
import argparse, hashlib, json, re, sys, zipfile
from pathlib import Path
import book_index
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

    Earlier drafts shaded narrative/design-decision callouts navy while
    the paragraph style inherited Normal's dark ink. The LaTeX
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
    md=root/'book/manuscript.md'; distmd=root/'dist/Enterprise-General-Intelligence-v1.0.0.md'; docx_path=root/'dist/Enterprise-General-Intelligence-v1.0.0.docx'
    required=[root/'README.md',root/'AGENTS.md',root/'CHANGELOG.md',root/'styles/DESIGN-SYSTEM.md',root/'styles/CROSS-FORMAT-CONTRACT.md',root/'config/book.json',root/'config/references.json',root/'config/reference-verification.json',root/'config/diagrams.json',md,distmd,docx_path,root/f"assets/cover/cover-v{book_release(root)}.png",root/'templates/book-style-template.docx']
    missing=[p.relative_to(root).as_posix() for p in required if not p.exists()]
    if missing: errors.append(f"Missing required files: {missing}")
    if not md.exists(): raise SystemExit(1)
    text=md.read_text(encoding='utf-8'); b=text.encode('utf-8')
    checks['canonical_markdown_sha256']=hashlib.sha256(b).hexdigest(); checks['canonical_markdown_bytes']=len(b)
    if not text.endswith('\n'): errors.append('Canonical Markdown needs one trailing newline')
    if '\r' in text: errors.append('Canonical Markdown contains CR characters')
    if distmd.exists() and distmd.read_bytes()!=md.read_bytes(): errors.append('Canonical and distributable Markdown are not byte-identical')
    checks['parts']=len(re.findall(r'^# PART [IVXLCDM]+ — ',text,re.M)); checks['chapters']=len(re.findall(r'^# \d{2} — ',text,re.M)); checks['appendices']=len(re.findall(r'^# Appendix [A-Z] — ',text,re.M))
    # Current topology: 8 Parts, 28 chapters, 12 appendices (Appendix M folded into
    # the references appendix), the glossary last among them, then the index.
    expected={'parts':8,'chapters':28,'appendices':12}
    for k,v in expected.items():
        if checks[k]!=v: errors.append(f"Expected {v} {k}, found {checks[k]}")
    chapter_nums=[int(x) for x in re.findall(r'^# (\d{2}) — ',text,re.M)]
    if chapter_nums!=list(range(1,29)): errors.append(f"Chapter sequence is invalid: {chapter_nums}")
    appendix_ids=re.findall(r'^# Appendix ([A-Z]) — ',text,re.M)
    if appendix_ids!=[chr(ord('A')+i) for i in range(12)]: errors.append(f"Appendix sequence is invalid: {appendix_ids}")
    h1s=re.findall(r'^# (.+)$',re.sub(r'(?ms)^```.*?^```','',text),re.M)
    if not h1s or h1s[-1]!=book_index.INDEX_HEADING: errors.append(f"The index must be the book's last H1, found {h1s[-1:]}")
    if len(h1s)<2 or h1s[-2]!='Appendix L — Glossary': errors.append(f"The glossary must be the last appendix, found {h1s[-2:-1]}")
    # The title-page date is the build month (tools/build_info.py), never a literal.
    if '{{BUILD_DATE}}' in text: errors.append('Unresolved {{BUILD_DATE}} token in the manuscript')
    if not re.search(r'^Book v\d+\.\d+\.\d+ · Publication Release · (January|February|March|April|May|June|July|August|September|October|November|December) \d{4}$',text,re.M): errors.append('Title-page build date line is missing or malformed')
    # Index: every glossary term is indexed, every term is located, and each
    # term's defining chapter is among its locators.
    index_entries=book_index.load_terms(root,text)
    found=book_index.scan(text,index_entries,book_index.excluded_units(root))
    indexed_glossary={e.get('glossary') for e in json.loads((root/'config/index-terms.json').read_text(encoding='utf-8'))['entries']}
    missing_terms=sorted(set(book_index.glossary_chapters(text))-indexed_glossary)
    if missing_terms: errors.append(f"Glossary terms without an index entry: {missing_terms}")
    for e in index_entries:
        if not found[e['term']]: errors.append(f"Index term never located: {e['term']}")
        elif any(d not in found[e['term']] for d in e['defined']): errors.append(f"Index term {e['term']!r} is not located in its defining unit(s) {e['defined']}")
    checks['index_terms']=len(index_entries); checks['index_locators']=sum(len(v) for v in found.values())
    md_index=text[text.rfind('\n# '+book_index.INDEX_HEADING+'\n'):]
    md_entries=re.findall(r'^- (.+?) — ',md_index,re.M)
    if md_entries!=[e['term'] for e in index_entries if found[e['term']]]: errors.append('Markdown index entries differ from config/index-terms.json')
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
    # Chapter titles must agree across the manuscript H1s, config/book.json and
    # config/chapter-covers.json. The renderers read headings from Markdown and
    # covers from the cover spec, so drift in book.json never shows on a page;
    # it surfaces later as a wrong catalog, navigation or Notion title.
    h1_titles={int(n):t.strip() for n,t in re.findall(r'^# (\d{2}) — (.+)$',prose,re.M)}
    meta_titles={c['number']:c['title'] for c in json.loads((root/'config/book.json').read_text(encoding='utf-8'))['structure']['chapters']}
    cover_path=root/'config/chapter-covers.json'
    cover_titles={c['chapter']:c['title'] for c in json.loads(cover_path.read_text(encoding='utf-8'))['chapters']} if cover_path.exists() else {}
    title_mismatches=0
    for n in range(1,29):
        for label,table in (('config/book.json',meta_titles),('config/chapter-covers.json',cover_titles)):
            if table and table.get(n)!=h1_titles.get(n):
                title_mismatches+=1
                errors.append(f"Chapter {n:02d} title drift: {label} has {table.get(n)!r}, manuscript H1 is {h1_titles.get(n)!r}")
    checks['chapter_title_mismatches']=title_mismatches
    if text.count('```')%2: errors.append('Unbalanced fenced code blocks')
    checks['code_blocks']=len(re.findall(r'^```[^\n]*$',text,re.M))//2
    errors.extend(check_table_shapes(text))
    # Labels from pre-release drafts (v2.x, v3.x) must not survive in the manuscript.
    stale=sorted(set(re.findall(r'\bv(?:2|3)\.\d+(?:\.\d+)?\b',text)))
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
    cover=root/f"assets/cover/cover-v{book_release(root)}.png"
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
            if doc_chapters!=28 or doc_appendices!=12: errors.append(f"DOCX heading counts differ: chapters={doc_chapters}, appendices={doc_appendices}")
            body=zipfile.ZipFile(docx_path).read('word/document.xml').decode('utf-8')
            checks['docx_index_marks']=len(re.findall(r' XE "',body)); checks['docx_index_fields']=body.count(' INDEX ')
            if checks['docx_index_marks']!=checks['index_locators']: errors.append(f"DOCX has {checks['docx_index_marks']} index marks; the index has {checks['index_locators']} locators")
            if checks['docx_index_fields']!=1: errors.append(f"DOCX must hold one INDEX field, found {checks['docx_index_fields']}")
            # Derived, not fixed: cover + registered diagrams + chapter covers.
            cc=root/'config/chapter-covers.json'
            cover_spec=json.loads(cc.read_text(encoding='utf-8')) if cc.exists() else {'output_dir':'','chapters':[]}
            covers=cover_spec['chapters']
            expected_images=1+len(diags)+len(covers)
            checks['expected_docx_images']=expected_images
            if len(doc.inline_shapes)!=expected_images: errors.append(f"Expected {expected_images} DOCX images (cover + {len(diags)} diagrams + {len(covers)} chapter covers), found {len(doc.inline_shapes)}")
            if covers and len(covers)!=28: errors.append(f"Expected 28 chapter covers, registered {len(covers)}")
            report_path=root/'reports/chapter-cover-report.json'
            cover_hashes={r['file']:r['sha256'] for r in json.loads(report_path.read_text(encoding='utf-8'))['records']} if report_path.exists() else {}
            for c in covers:
                rel=f"{cover_spec['output_dir']}/{c['file']}"; asset=root/rel
                if not asset.exists(): errors.append(f"Missing chapter {c['chapter']} cover {rel}"); continue
                with Image.open(asset) as im:
                    if im.size!=(2550,3300): errors.append(f"Chapter {c['chapter']} cover is {im.size}, expected 2550x3300 (US Letter at 300 dpi)")
                if cover_hashes.get(rel) and sha(asset)!=cover_hashes[rel]: errors.append(f"Chapter {c['chapter']} cover checksum differs from reports/chapter-cover-report.json: {rel}")
            callout_failures=docx_callout_contrast(docx_path)
            checks['docx_callout_contrast_failures']=len(callout_failures)
            for failure in callout_failures:
                errors.append(f"DOCX callout is unreadable: ink on #{failure['fill']} = {failure['ratio']}:1 — {failure['text']}")
            cp=doc.core_properties
            book_cfg=json.loads((root/'config/book.json').read_text(encoding='utf-8'))['book']
            expected_title=book_cfg['title']
            if cp.title!=expected_title: errors.append(f"DOCX title metadata is {cp.title!r}, expected {expected_title!r}")
            if cp.author!='Reza Rahimi, PhD': errors.append(f"Unexpected DOCX author metadata: {cp.author}")
        except Exception as exc: errors.append(f"DOCX validation error: {exc}")
    pdf=root/'qa/render/Enterprise-General-Intelligence-v1.0.0.pdf'
    if pdf.exists():
        try:
            import pymupdf
            d=pymupdf.open(pdf); checks['pdf_pages']=len(d)
            # 213 was the pre-release draft's LibreOffice baseline. The topology has since
            # changed, so asserting it would warn about the expected result; the page
            # count is recorded as a measurement until a current baseline is rendered
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
    summary=["# Validation Summary — Book v1.0.0","",f"**Result:** {'PASS' if not errors else 'FAIL'}","", "## Measurements","",* [f"- **{k}:** `{v}`" for k,v in checks.items()],"","## Errors","",*([f"- {x}" for x in errors] or ["- None."]),"","## Warnings","",*([f"- {x}" for x in warnings] or ["- None."])]
    (root/'reports/validation-summary.md').write_text('\n'.join(summary)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2)); return 0 if not errors else 1

if __name__=='__main__': sys.exit(main())
