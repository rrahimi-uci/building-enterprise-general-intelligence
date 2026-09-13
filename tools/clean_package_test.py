#!/usr/bin/env python3
"""Extract a release ZIP into a fresh directory and rebuild using only its contents."""
from __future__ import annotations
import argparse, json, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('zip'); ap.add_argument('--keep'); args=ap.parse_args(); z=Path(args.zip).resolve(); td=Path(args.keep).resolve() if args.keep else Path(tempfile.mkdtemp(prefix='book-v1-clean-'))
    if td.exists() and any(td.iterdir()): raise SystemExit(f'Target is not empty: {td}')
    td.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(z) as f: f.extractall(td)
    roots=[p for p in td.iterdir() if p.is_dir()]
    if len(roots)!=1: raise SystemExit('ZIP must contain exactly one top-level directory')
    root=roots[0]
    commands=[[sys.executable,'tools/assemble_manuscript.py','--root','.'],[sys.executable,'tools/build_book.py','--root','.'],[sys.executable,'tools/check_references.py','--root','.'],[sys.executable,'tools/validate_book.py','--root','.'],[sys.executable,'tools/deterministic_build_check.py','--root','.']]
    for cmd in commands: subprocess.run(cmd,cwd=root,check=True)
    result={'zip':str(z),'extracted_root':str(root),'commands':commands,'pass':True}
    print(json.dumps(result,indent=2))
    if not args.keep: shutil.rmtree(td)
    return 0
if __name__=='__main__': sys.exit(main())
