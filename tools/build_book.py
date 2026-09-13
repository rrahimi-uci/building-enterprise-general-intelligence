#!/usr/bin/env python3
"""Deterministically build the publication DOCX from canonical Markdown.

Supported canonical constructs:
  headings H1-H4, paragraphs, bullet/number lists, blockquotes, GFM pipe
  tables, fenced code, inline bold/italic/code/links, [Rxx] citations,
  [[COVER]], and [[DIAGRAM:id|caption]].

The script owns all DOCX layout and style decisions. Do not hand-format release
artifacts; change book/manuscript.md, config, assets, or this renderer.
"""
from __future__ import annotations
from pathlib import Path
from datetime import datetime,timezone
from zipfile import ZipFile,ZipInfo,ZIP_DEFLATED
import argparse,hashlib,json,re,subprocess,sys,tempfile
from PIL import Image
from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT,WD_ROW_HEIGHT_RULE
from docx.enum.text import WD_ALIGN_PARAGRAPH,WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.shared import Inches,Pt,RGBColor

FIXED_DT=datetime(2026,9,13,12,0,0,tzinfo=timezone.utc)

def load(root:Path):
    return json.loads((root/'config/book.json').read_text(encoding='utf-8'))

def color(v): return RGBColor.from_string(v)

def shade(cell,fill):
    tcPr=cell._tc.get_or_add_tcPr(); shd=tcPr.find(qn('w:shd'))
    if shd is None: shd=OxmlElement('w:shd'); tcPr.append(shd)
    shd.set(qn('w:fill'),fill)

def cell_margins(cell,top=70,left=90,bottom=70,right=90):
    tcPr=cell._tc.get_or_add_tcPr(); mar=tcPr.first_child_found_in('w:tcMar')
    if mar is None: mar=OxmlElement('w:tcMar'); tcPr.append(mar)
    for name,val in [('top',top),('start',left),('bottom',bottom),('end',right)]:
        n=mar.find(qn('w:'+name))
        if n is None: n=OxmlElement('w:'+name); mar.append(n)
        n.set(qn('w:w'),str(val)); n.set(qn('w:type'),'dxa')

def repeat_table_header(row):
    trPr=row._tr.get_or_add_trPr(); h=OxmlElement('w:tblHeader'); h.set(qn('w:val'),'true'); trPr.append(h)

def prevent_row_split(row):
    trPr=row._tr.get_or_add_trPr(); trPr.append(OxmlElement('w:cantSplit'))

def add_hyperlink(p,text,url,hex_color='1769D2',underline=True):
    rid=p.part.relate_to(url,RT.HYPERLINK,is_external=True)
    h=OxmlElement('w:hyperlink'); h.set(qn('r:id'),rid)
    r=OxmlElement('w:r'); rPr=OxmlElement('w:rPr')
    c=OxmlElement('w:color'); c.set(qn('w:val'),hex_color); rPr.append(c)
    if underline:
        u=OxmlElement('w:u'); u.set(qn('w:val'),'single'); rPr.append(u)
    r.append(rPr); t=OxmlElement('w:t'); t.text=text; r.append(t); h.append(r); p._p.append(h)

def configure(doc:Document,cfg:dict):
    C=cfg['design']['colors']; font=cfg['design']['fonts']; m=cfg['design']['margins_inches']
    sec=doc.sections[0]; sec.top_margin=Inches(m['top']); sec.bottom_margin=Inches(m['bottom']); sec.left_margin=Inches(m['left']); sec.right_margin=Inches(m['right']); sec.header_distance=Inches(.25); sec.footer_distance=Inches(.28); sec.different_first_page_header_footer=True
    styles=doc.styles
    normal=styles['Normal']; normal.font.name=font['sans']; normal.font.size=Pt(9.6); normal.font.color.rgb=color(C['ink']); normal.paragraph_format.space_after=Pt(5); normal.paragraph_format.line_spacing=1.06
    specs={'Title':(30,C['navy'],True,14,7),'Subtitle':(14,C['teal'],False,8,5),'Heading 1':(24,C['navy'],True,14,7),'Heading 2':(16,C['blue'],True,9,5),'Heading 3':(12,C['navy2'],True,7,4),'Heading 4':(10,C['teal'],True,5,3)}
    for name,(size,clr,bold,before,after) in specs.items():
        st=styles[name]; st.font.name=font['sans']; st.font.size=Pt(size); st.font.bold=bold; st.font.color.rgb=color(clr); st.paragraph_format.space_before=Pt(before); st.paragraph_format.space_after=Pt(after); st.paragraph_format.keep_with_next=True
    cap=styles['Caption']; cap.font.name=font['sans']; cap.font.size=Pt(8.5); cap.font.italic=True; cap.font.color.rgb=color('4A6078'); cap.paragraph_format.space_before=Pt(2); cap.paragraph_format.space_after=Pt(6)
    for name,base in [('Book Callout','Normal'),('Book Evidence','Normal'),('Book Reference','Normal'),('Book Code Label','Normal'),('Book Part','Title')]:
        if name not in [s.name for s in styles]: styles.add_style(name,WD_STYLE_TYPE.PARAGRAPH)
        st=styles[name]; st.base_style=styles[base]; st.font.name=font['sans'] if name!='Book Code Label' else font['mono']
    styles['Book Evidence'].font.color.rgb=color(C['navy2']); styles['Book Evidence'].font.italic=True
    styles['Book Reference'].font.size=Pt(8.6); styles['Book Reference'].paragraph_format.left_indent=Inches(.18); styles['Book Reference'].paragraph_format.first_line_indent=Inches(-.18)
    styles['Book Code Label'].font.size=Pt(7.5); styles['Book Code Label'].font.bold=True; styles['Book Code Label'].font.color.rgb=color(C['white'])
    styles['Book Part'].font.size=Pt(28); styles['Book Part'].font.bold=True; styles['Book Part'].font.color.rgb=color(C['white'])
    # Header and footer.
    hp=sec.header.paragraphs[0]; hp.clear(); hp.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    r=hp.add_run(cfg['book']['title'].upper()); r.font.name=font['sans']; r.font.size=Pt(7.2); r.font.bold=True; r.font.color.rgb=color('4A6078')
    fp=sec.footer.paragraphs[0]; fp.clear(); fp.alignment=WD_ALIGN_PARAGRAPH.CENTER
    r=fp.add_run(f"BOOK v{cfg['book']['version']}    |    PAGE "); r.font.name=font['sans']; r.font.size=Pt(7.5); r.font.color.rgb=color('4A6078')
    begin=OxmlElement('w:fldChar'); begin.set(qn('w:fldCharType'),'begin'); instr=OxmlElement('w:instrText'); instr.set(qn('xml:space'),'preserve'); instr.text=' PAGE '; sep=OxmlElement('w:fldChar'); sep.set(qn('w:fldCharType'),'separate'); txt=OxmlElement('w:t'); txt.text='1'; end=OxmlElement('w:fldChar'); end.set(qn('w:fldCharType'),'end'); rr=OxmlElement('w:r'); rr.extend([begin,instr,sep,txt,end]); fp._p.append(rr)
    sec.first_page_header.paragraphs[0].clear(); sec.first_page_footer.paragraphs[0].clear()

def split_row(line):
    text=line.strip().strip('|'); cells=[]; buf=[]; esc=False; code=False
    for ch in text:
        if esc: buf.append(ch); esc=False; continue
        if ch=='\\': esc=True; buf.append(ch); continue
        if ch=='`': code=not code; buf.append(ch); continue
        if ch=='|' and not code: cells.append(''.join(buf).strip().replace('\\|','|')); buf=[]
        else: buf.append(ch)
    cells.append(''.join(buf).strip().replace('\\|','|')); return cells

def sep_row(line):
    cs=split_row(line); return bool(cs) and all(re.fullmatch(r':?-{3,}:?',c.replace(' ','')) for c in cs)

def parse(md):
    lines=md.splitlines(); i=0
    # Optional YAML front matter.
    if lines and lines[0].strip()=='---':
        i=1
        while i<len(lines) and lines[i].strip()!='---': i+=1
        i+=1
    while i<len(lines):
        line=lines[i]; stripped=line.strip()
        if not stripped: i+=1; continue
        if stripped=='[[COVER]]': yield ('cover',); i+=1; continue
        dm=re.fullmatch(r'\[\[DIAGRAM:([^|\]]+)\|(.+)\]\]',stripped)
        if dm: yield ('diagram',dm.group(1),dm.group(2)); i+=1; continue
        pm=re.match(r'^# PART (.+?) — (.+)$',line)
        if pm:
            ident,title=pm.groups(); i+=1
            while i<len(lines) and not lines[i].strip(): i+=1
            intro=[]
            while i<len(lines) and lines[i].strip() and not lines[i].startswith('#'):
                intro.append(lines[i].strip()); i+=1
            yield ('part',ident,title,' '.join(intro)); continue
        if line.startswith('```'):
            lang=line[3:].strip() or 'text'; code=[]; i+=1
            while i<len(lines) and not lines[i].startswith('```'): code.append(lines[i]); i+=1
            if i>=len(lines): raise ValueError('Unclosed code fence')
            i+=1; yield ('code',lang,'\n'.join(code)); continue
        hm=re.match(r'^(#{1,4})\s+(.+)$',line)
        if hm: yield ('heading',len(hm.group(1)),hm.group(2).strip()); i+=1; continue
        if stripped.startswith('|') and i+1<len(lines) and sep_row(lines[i+1]):
            rows=[split_row(line)]; i+=2
            while i<len(lines) and lines[i].strip().startswith('|'): rows.append(split_row(lines[i])); i+=1
            yield ('table',rows); continue
        if re.match(r'^[-*]\s+\[[ xX]\]\s+',line):
            checked='☑' if re.match(r'^[-*]\s+\[[xX]\]',line) else '☐'; yield ('bullet',checked+' '+re.sub(r'^[-*]\s+\[[ xX]\]\s+','',line)); i+=1; continue
        if re.match(r'^[-*]\s+',line): yield ('bullet',re.sub(r'^[-*]\s+','',line)); i+=1; continue
        if re.match(r'^\d+\.\s+',line): yield ('number',re.sub(r'^\d+\.\s+','',line)); i+=1; continue
        if line.startswith('> '): yield ('quote',line[2:].strip()); i+=1; continue
        para=[stripped]; i+=1
        while i<len(lines):
            n=lines[i]; ns=n.strip()
            if not ns: break
            if n.startswith(('#','```','> ')) or ns.startswith('|') or ns.startswith('[[DIAGRAM:') or ns=='[[COVER]]' or re.match(r'^[-*]\s+',n) or re.match(r'^\d+\.\s+',n): break
            para.append(ns); i+=1
        yield ('para',' '.join(para))

def add_inline(p,text,cfg,bold_override=False):
    C=cfg['design']['colors']; mono=cfg['design']['fonts']['mono']
    token=re.compile(r'(\*\*.+?\*\*|`[^`]+`|\[[^\]]+\]\(https?://[^)]+\)|\[R\d{2}\]|(?<!\*)\*[^*\n]+\*)')
    pos=0
    for m in token.finditer(text):
        if m.start()>pos:
            r=p.add_run(text[pos:m.start()]); r.bold=bold_override or None
        t=m.group(0)
        if t.startswith('**'):
            r=p.add_run(t[2:-2]); r.bold=True
        elif t.startswith('`'):
            r=p.add_run(t[1:-1]); r.font.name=mono; r.font.size=Pt(8.7); r.font.color.rgb=color('405A75'); r.font.highlight_color=None
        elif re.match(r'^\[[^\]]+\]\(https?://',t):
            mm=re.match(r'^\[([^\]]+)\]\((https?://[^)]+)\)$',t); add_hyperlink(p,mm.group(1),mm.group(2),C['blue'])
        elif re.fullmatch(r'\[R\d{2}\]',t):
            r=p.add_run(t); r.bold=True; r.font.color.rgb=color(C['blue'])
        elif t.startswith('*'):
            r=p.add_run(t[1:-1]); r.italic=True
        pos=m.end()
    if pos<len(text):
        r=p.add_run(text[pos:]); r.bold=bold_override or None

def add_page_break(doc):
    p=doc.add_paragraph(); p.add_run().add_break(WD_BREAK.PAGE)

def add_paragraph(doc,text,cfg,style='Normal',align=None):
    p=doc.add_paragraph(style=style); add_inline(p,text,cfg)
    if align is not None: p.alignment=align
    return p

def add_part(doc,ident,title,intro,cfg):
    C=cfg['design']['colors']; add_page_break(doc)
    t=doc.add_table(rows=1,cols=1); t.autofit=False; row=t.rows[0]; row.height=Inches(8.45); row.height_rule=WD_ROW_HEIGHT_RULE.EXACTLY; cell=t.cell(0,0); cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER; shade(cell,C['navy']); cell_margins(cell,300,320,300,320)
    p=cell.paragraphs[0]; p.alignment=WD_ALIGN_PARAGRAPH.CENTER; r=p.add_run('PART '+ident); r.font.name=cfg['design']['fonts']['sans']; r.font.size=Pt(15); r.font.bold=True; r.font.color.rgb=color(C['cyan'])
    p=cell.add_paragraph(style='Book Part'); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.add_run(title.upper())
    if intro:
        p=cell.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_before=Pt(18); r=p.add_run(intro); r.font.name=cfg['design']['fonts']['sans']; r.font.size=Pt(11); r.font.color.rgb=color('D8E8F5')
    add_page_break(doc)

def add_code_run(p,text,lang,cfg):
    # Lightweight deterministic lexical colors; source text is never changed.
    C=cfg['design']['colors']; kw=set('class def return if else elif for while try except finally with as import from async await raise yield True False None and or not in is lambda match case switch const let function public private new'.split())
    pieces=re.split(r'("[^"\n]*"|\'[^\'\n]*\'|\b\w+\b)',text)
    for piece in pieces:
        r=p.add_run(piece if piece else ''); r.font.name=cfg['design']['fonts']['mono']; r.font.size=Pt(7.25)
        if piece in kw: r.font.bold=True; r.font.color.rgb=color(C['blue'])
        elif (piece.startswith('"') and piece.endswith('"')) or (piece.startswith("'") and piece.endswith("'")): r.font.color.rgb=color(C['teal'])
        elif piece.strip().startswith(('#','//')): r.font.color.rgb=color('6A7E92')
        else: r.font.color.rgb=color('19324D')

def add_code(doc,lang,code,cfg):
    C=cfg['design']['colors']; t=doc.add_table(rows=1,cols=2); t.autofit=False; t.columns[0].width=Inches(.42); t.columns[1].width=Inches(6.42)
    h=t.rows[0].cells[0]; h.merge(t.rows[0].cells[1]); shade(h,C['navy']); cell_margins(h,45,90,45,90); p=h.paragraphs[0]; p.style='Book Code Label'; p.add_run((lang or 'text').upper())
    for i,line in enumerate(code.splitlines() or [''],1):
        cells=t.add_row().cells; prevent_row_split(t.rows[-1]); shade(cells[0],'E5ECF3'); shade(cells[1],'F7F9FC'); cell_margins(cells[0],15,55,15,55); cell_margins(cells[1],15,80,15,80)
        lp,rp=cells[0].paragraphs[0],cells[1].paragraphs[0]
        for p in (lp,rp): p.paragraph_format.space_before=Pt(0); p.paragraph_format.space_after=Pt(0); p.paragraph_format.line_spacing=1
        rr=lp.add_run(str(i)); rr.font.name=cfg['design']['fonts']['mono']; rr.font.size=Pt(7); rr.font.color.rgb=color('6A7E92'); add_code_run(rp,line or ' ',lang,cfg)
    doc.add_paragraph().paragraph_format.space_after=Pt(1)

def add_table(doc,rows,cfg):
    C=cfg['design']['colors']; cols=max(len(r) for r in rows)
    # One-column two-row Markdown tables are semantic callouts.
    if cols==1 and rows and not rows[0][0].strip() and len(rows)>=2:
        text=' '.join(r[0] for r in rows[1:] if r and r[0].strip()); t=doc.add_table(rows=1,cols=1); cell=t.cell(0,0); label=text.upper(); fill=C['navy'] if any(k in label for k in ['NORTHSTAR','DESIGN DECISION','SOURCE DISCIPLINE']) else ('FFF4DF' if any(k in label for k in ['CAUTION','EVIDENCE CAVEAT']) else 'EAF3FB'); shade(cell,fill); cell_margins(cell,120,160,120,160); p=cell.paragraphs[0]; p.style='Book Callout'; add_inline(p,text,cfg); doc.add_paragraph().paragraph_format.space_after=Pt(1); return
    t=doc.add_table(rows=len(rows),cols=cols); t.style='Table Grid'; t.autofit=True
    size=6.8 if cols>=7 else (7.3 if cols>=5 else 8.1)
    for ri,row in enumerate(rows):
        tr=t.rows[ri]; prevent_row_split(tr)
        if ri==0: repeat_table_header(tr)
        for ci in range(cols):
            cell=t.cell(ri,ci); cell.text=''; cell_margins(cell,65,80,65,80); cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            p=cell.paragraphs[0]; p.paragraph_format.space_after=Pt(0); p.paragraph_format.line_spacing=1
            val=row[ci] if ci<len(row) else ''; add_inline(p,val,cfg,bold_override=ri==0)
            for run in p.runs: run.font.name=cfg['design']['fonts']['sans']; run.font.size=Pt(size)
            if ri==0:
                shade(cell,C['navy']);
                for run in p.runs: run.font.color.rgb=color(C['white']); run.bold=True
            elif ri%2==0: shade(cell,'F3F7FB')
    doc.add_paragraph().paragraph_format.space_after=Pt(1)

def add_diagram(doc,root,key,caption,cfg):
    path=root/'assets/diagrams'/f'{key}.png'
    if not path.exists(): raise FileNotFoundError(f'Missing diagram {path}')
    p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_before=Pt(4); p.paragraph_format.space_after=Pt(2); p.add_run().add_picture(str(path),width=Inches(cfg['design']['diagram_width_inches']))
    c=doc.add_paragraph(style='Caption'); c.alignment=WD_ALIGN_PARAGRAPH.CENTER; add_inline(c,caption,cfg)

def normalize_zip(path:Path):
    tmp=path.with_suffix('.normalized.docx')
    with ZipFile(path,'r') as zin, ZipFile(tmp,'w',ZIP_DEFLATED,compresslevel=9) as zout:
        for name in sorted(zin.namelist()):
            info=ZipInfo(name,date_time=(1980,1,1,0,0,0)); info.compress_type=ZIP_DEFLATED; info.external_attr=0o600<<16; info.create_system=3; zout.writestr(info,zin.read(name))
    tmp.replace(path)

def build(root:Path,out:Path,template_only=False):
    cfg=load(root); C=cfg['design']['colors']; doc=Document(); configure(doc,cfg)
    doc.core_properties.title=cfg['book']['title']+f" — Book v{cfg['book']['version']}"; doc.core_properties.subject='Enterprise Agentic AI architecture and developer platform'; doc.core_properties.author=cfg['book']['author']; doc.core_properties.last_modified_by=cfg['book']['author']; doc.core_properties.keywords='agentic AI, enterprise architecture, developer platform, AI agents, LLM gateway, security, evaluation'; doc.core_properties.comments='Generated deterministically from book/manuscript.md; do not hand-edit the release DOCX.'; doc.core_properties.created=FIXED_DT; doc.core_properties.modified=FIXED_DT
    if template_only:
        add_paragraph(doc,'Book Style Template','Title',cfg) if False else None
        p=doc.add_paragraph(style='Title'); p.add_run('Book Style Template')
        for i,name in enumerate(['Heading 1','Heading 2','Heading 3','Heading 4'],1): doc.add_paragraph(f'{name} sample',style=name)
        add_paragraph(doc,'Normal paragraph with **bold**, *italic*, `inline code`, [R01], and a [link](https://example.com).',cfg)
        add_table(doc,[['Column A','Column B'],['Value','Value']],cfg); add_code(doc,'python','def example():\n    return True',cfg)
    else:
        cover=root/'assets/cover/cover-v1.0.0.png'
        if not cover.exists(): subprocess.run([sys.executable,str(root/'tools/generate_cover.py'),'--root',str(root)],check=True)
        md=(root/cfg['source']['canonical_markdown']).read_text(encoding='utf-8')
        after_part=False; title_seen=False; blocks=0
        for b in parse(md):
            blocks+=1; kind=b[0]
            if kind=='cover':
                p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_after=Pt(0); p.add_run().add_picture(str(cover),width=Inches(7.05)); add_page_break(doc); continue
            if kind=='part': add_part(doc,b[1],b[2],b[3],cfg); after_part=True; continue
            if kind=='heading':
                level,text=b[1],b[2]
                if level==1 and text==cfg['book']['title'] and not title_seen:
                    p=doc.add_paragraph(style='Title'); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; add_inline(p,text,cfg); title_seen=True; continue
                style=f'Heading {level}'
                p=doc.add_paragraph(style=style); add_inline(p,text,cfg); p.paragraph_format.keep_with_next=True
                if level==1:
                    is_chapter=bool(re.match(r'^\d{2} — ',text) or text.startswith('Appendix '))
                    p.paragraph_format.page_break_before=False if after_part and is_chapter else True
                    after_part=False
                continue
            if kind=='diagram': add_diagram(doc,root,b[1],b[2],cfg); continue
            if kind=='code': add_code(doc,b[1],b[2],cfg); continue
            if kind=='table': add_table(doc,b[1],cfg); continue
            if kind=='bullet': p=add_paragraph(doc,b[1],cfg,'List Bullet'); p.paragraph_format.keep_together=True; continue
            if kind=='number': p=add_paragraph(doc,b[1],cfg,'List Number'); p.paragraph_format.keep_together=True; continue
            if kind=='quote':
                style='Book Evidence' if b[1].startswith('**Evidence note.') else 'Book Callout'; p=add_paragraph(doc,b[1],cfg,style); p.paragraph_format.left_indent=Inches(.22); p.paragraph_format.right_indent=Inches(.12); p.paragraph_format.space_before=Pt(5); p.paragraph_format.space_after=Pt(7); continue
            if kind=='para':
                txt=b[1]
                if txt.startswith('Book v1.0.0') or txt=='**'+cfg['book']['author']+'**': p=add_paragraph(doc,txt,cfg,'Subtitle',WD_ALIGN_PARAGRAPH.CENTER)
                elif txt.startswith('A structured enterprise reference') and title_seen: p=add_paragraph(doc,txt,cfg,'Normal',WD_ALIGN_PARAGRAPH.CENTER)
                else:
                    style='Book Reference' if txt.startswith('* **[R') else 'Normal'; p=add_paragraph(doc,txt,cfg,style)
                continue
    out.parent.mkdir(parents=True,exist_ok=True); doc.save(out); normalize_zip(out)
    report={'output':str(out.relative_to(root)),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'bytes':out.stat().st_size,'template_only':template_only}
    if not template_only:
        from docx import Document as D
        check=D(out); report.update({'paragraphs':len(check.paragraphs),'tables':len(check.tables),'inline_images':len(check.inline_shapes),'chapter_headings':sum(1 for p in check.paragraphs if p.style.name=='Heading 1' and re.match(r'^\d{2} — ',p.text)),'appendix_headings':sum(1 for p in check.paragraphs if p.style.name=='Heading 1' and p.text.startswith('Appendix '))})
        (root/'qa/build-report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2)); return report

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]); ap.add_argument('--output',type=Path); ap.add_argument('--template-only',action='store_true'); a=ap.parse_args(); root=a.root.resolve(); default=root/('templates/book-style-template.docx' if a.template_only else 'dist/Enterprise-Agentic-AI-Architecture-Developer-Platform-Guide-v1.0.0.docx'); build(root,(a.output or default).resolve(),a.template_only)
