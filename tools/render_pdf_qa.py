#!/usr/bin/env python3
"""Render DOCX with LibreOffice, inspect pagination, and create a contact sheet."""
from __future__ import annotations
import argparse, json, re, shutil, subprocess, sys, tempfile
from pathlib import Path
import pymupdf
from PIL import Image, ImageDraw, ImageFont

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default=str(Path(__file__).resolve().parents[1])); args=ap.parse_args(); root=Path(args.root).resolve()
    docx=root/'dist/Enterprise-Agentic-AI-Architecture-Developer-Platform-Guide-v1.0.0.docx'; out=root/'qa/render'; out.mkdir(parents=True,exist_ok=True)
    if not shutil.which('soffice'): raise SystemExit('LibreOffice soffice is required for PDF QA')
    pdf=out/(docx.stem+'.pdf');
    if pdf.exists(): pdf.unlink()
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(['soffice',f'-env:UserInstallation=file://{td}/lo','--headless','--convert-to','pdf','--outdir',str(out),str(docx)],check=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    d=pymupdf.open(pdf); page_count=len(d); blank=[]; sizes=[]
    manuscript=(root/'book/manuscript.md').read_text(encoding='utf-8')
    headings=re.findall(r'^# ((?:\d{2}|Appendix [A-Z]) — .+)$',manuscript,re.M)
    part_titles=re.findall(r'^# (PART [IVXLCDM]+ — .+)$',manuscript,re.M)
    normalized=[]
    for i,p in enumerate(d):
        txt=p.get_text().strip(); imgs=p.get_images(full=True)
        if len(txt)<8 and not imgs: blank.append(i+1)
        sizes.append([round(p.rect.width,1),round(p.rect.height,1)])
        normalized.append(re.sub(r'\s+',' ',txt).strip())
    found=[]
    for title in headings:
        needle=re.sub(r'\s+',' ',title).strip()
        candidates=[i+1 for i,txt in enumerate(normalized) if needle in txt]
        if candidates:
            pno=candidates[-1]
            found.append({'title':title,'page':pno,'text_offset':normalized[pno-1].find(needle)})
    unique_starts=len({x['page'] for x in found}); max_offset=max((x['text_offset'] for x in found),default=None)
    part_pages=[]
    for title in part_titles:
        needle=re.sub(r'\s+',' ',title.replace(' — ',' ')).strip()
        candidates=[i+1 for i,txt in enumerate(normalized) if needle in txt]
        if candidates: part_pages.append(candidates[-1])
    appendix_a=next((x['page'] for x in found if x['title'].startswith('Appendix A —')),page_count+1)
    appendix_dividers=[i+1 for i,txt in enumerate(normalized) if 'APPENDICES' in txt.upper() and i+1<appendix_a and len(txt)<1000]
    divider_pages=sorted(set(part_pages+appendix_dividers[-1:]))
    report={'release':'1.0.0','pdf':pdf.relative_to(root).as_posix(),'pages':page_count,'page_size_points':sizes[0] if sizes else None,'headings_expected':len(headings),'headings_found':len(found),'unique_heading_start_pages':unique_starts,'maximum_heading_text_offset':max_offset,'standalone_divider_pages':divider_pages,'blank_pages':blank,'pass':page_count>0 and len(found)==len(headings) and unique_starts==len(headings) and max_offset is not None and max_offset<200 and len(divider_pages)==13 and not blank}
    (root/'qa/pagination-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    sample=[1,2,3,4]+divider_pages+([x['page'] for x in found[::5]])
    sample=[] if not d else list(dict.fromkeys(p for p in sample if 1<=p<=page_count))[:28]
    thumbs=[]
    for pno in sample:
        pix=d[pno-1].get_pixmap(matrix=pymupdf.Matrix(.32,.32),alpha=False)
        im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples); thumbs.append((pno,im))
    cols=4; label=24; cellw=max((im.width for _,im in thumbs),default=200)+18; cellh=max((im.height for _,im in thumbs),default=260)+label+18
    sheet=Image.new('RGB',(cols*cellw,((len(thumbs)+cols-1)//cols)*cellh),(225,232,240)); draw=ImageDraw.Draw(sheet)
    for idx,(pno,im) in enumerate(thumbs):
        x=(idx%cols)*cellw+9; y=(idx//cols)*cellh+label; sheet.paste(im,(x,y)); draw.text((x,y-label+4),f'Page {pno}',fill=(16,42,76))
    sheet.save(out/'visual-contact-sheet.png'); d.close(); print(json.dumps(report,indent=2)); return 0 if report['pass'] else 1
if __name__=='__main__': sys.exit(main())
