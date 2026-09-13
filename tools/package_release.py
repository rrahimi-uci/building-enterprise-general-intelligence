#!/usr/bin/env python3
"""Create deterministic manifest, checksums, and self-contained release ZIP."""
from __future__ import annotations
import argparse, hashlib, json, os, sys, zipfile
from pathlib import Path
FIXED=(2026,9,13,0,0,0)

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''): h.update(c)
    return h.hexdigest()

def files(root):
    skip={'__pycache__','.DS_Store'}
    for p in sorted(root.rglob('*')):
        rel=p.relative_to(root)
        if p.is_file() and not any(x in skip for x in rel.parts) and p.suffix not in {'.pyc','.tmp'}:
            yield p

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default=str(Path(__file__).resolve().parents[1])); ap.add_argument('--output'); args=ap.parse_args(); root=Path(args.root).resolve(); out=Path(args.output).resolve() if args.output else root.parent/'Enterprise-Agentic-AI-Book-v1.0.0-Development-Package.zip'
    for name in ('RELEASE-MANIFEST.json','CHECKSUMS.sha256'):
        p=root/name
        if p.exists(): p.unlink()
    inventory=[]
    for p in files(root):
        inventory.append({'path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)})
    manifest={'schema_version':'1.0.0','release':'1.0.0','title':'Enterprise Agentic AI Architecture & Developer Platform Guide','author':'Reza Rahimi, PhD','release_date':'2026-09-13','canonical_source':'source/parts/*.md','file_count':len(inventory),'files':inventory}
    (root/'RELEASE-MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    checksum_files=list(files(root)); checksum_lines=[f"{sha(p)}  {p.relative_to(root).as_posix()}" for p in checksum_files if p.name!='CHECKSUMS.sha256']
    (root/'CHECKSUMS.sha256').write_text('\n'.join(checksum_lines)+'\n',encoding='utf-8')
    if out.exists(): out.unlink()
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in files(root):
            rel=Path(root.name)/p.relative_to(root); info=zipfile.ZipInfo(rel.as_posix(),FIXED); info.compress_type=zipfile.ZIP_DEFLATED; info.external_attr=(0o644&0xFFFF)<<16
            z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    result={'zip':str(out),'bytes':out.stat().st_size,'sha256':sha(out),'entries':len(zipfile.ZipFile(out).namelist()),'manifest_files':manifest['file_count']+2}
    (root/'reports/release-package.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2)); return 0
if __name__=='__main__': sys.exit(main())
