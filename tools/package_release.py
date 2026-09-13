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

# Directories that never belong in a release: version control, local virtual
# environments, editor/tool caches, and the regenerable XeLaTeX build directory.
SKIP_DIRS={'.git','venv','env','__pycache__','node_modules','.pytest_cache',
           '.mypy_cache','.ruff_cache','.idea','.vscode','.DS_Store','.tox','htmlcov'}
# Any virtualenv, however it is named: .venv, .venv-examples, .venv-anything.
SKIP_DIR_PREFIXES=('.venv',)
# Regenerable or environment-specific outputs.
SKIP_PATH_PREFIXES=('latex/build/',)
SKIP_NAMES={'release-package.json'}
SKIP_SUFFIXES={'.pyc','.tmp','.zip'}


def excluded(rel):
    """True when a repo-relative path must stay out of the manifest and ZIP."""
    posix=rel.as_posix()
    if any(part in SKIP_DIRS for part in rel.parts): return True
    if any(part.startswith(SKIP_DIR_PREFIXES) for part in rel.parts): return True
    if posix.startswith(SKIP_PATH_PREFIXES): return True
    if rel.name in SKIP_NAMES: return True
    if rel.suffix in SKIP_SUFFIXES: return True
    # Compiled PDFs are produced by latex/compile.sh, the Dockerfile, or CI.
    # They are published as release assets, never packaged as source.
    if posix.startswith('dist/') and rel.suffix=='.pdf': return True
    return False


def files(root):
    for p in sorted(root.rglob('*')):
        if p.is_file() and not excluded(p.relative_to(root)):
            yield p

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default=str(Path(__file__).resolve().parents[1])); ap.add_argument('--output'); args=ap.parse_args(); root=Path(args.root).resolve(); out=Path(args.output).resolve() if args.output else root.parent/'Enterprise-Agentic-AI-Book-v2.0.0-Complete-Package-with-LaTeX.zip'
    for name in ('RELEASE-MANIFEST.json','CHECKSUMS.sha256'):
        p=root/name
        if p.exists(): p.unlink()
    inventory=[]
    for p in files(root):
        inventory.append({'path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)})
    manifest={'schema_version':'1.0.0','release':'1.0.0','title':'Enterprise Agentic AI Architecture & Developer Platform Guide','author':'Reza Rahimi, PhD','release_date':'2026-09-13','canonical_source':'source/parts/*.md','representations':{'markdown':'final','docx':'final','latex_source':'source-validated','latex_pdf':'compile with included XeLaTeX workflow','notion':'synchronized release metadata'},'file_count':len(inventory),'files':inventory}
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
