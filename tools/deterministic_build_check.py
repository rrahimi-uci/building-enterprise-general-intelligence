#!/usr/bin/env python3
"""Build DOCX twice in isolated paths and compare byte hashes."""
from __future__ import annotations
import argparse, hashlib, json, subprocess, sys
from pathlib import Path

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default=str(Path(__file__).resolve().parents[1])); args=ap.parse_args(); root=Path(args.root).resolve()
    outdir=root/'qa/determinism'; outdir.mkdir(parents=True,exist_ok=True)
    a=outdir/'build-a.docx'; b=outdir/'build-b.docx'; build=root/'tools/build_book.py'
    for p in (a,b):
        if p.exists(): p.unlink()
        subprocess.run([sys.executable,str(build),'--root',str(root),'--output',str(p)],check=True)
    ha,hb=sha(a),sha(b); result={'build_a_sha256':ha,'build_b_sha256':hb,'byte_identical':ha==hb,'bytes':a.stat().st_size}
    (outdir/'determinism-report.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2)); return 0 if result['byte_identical'] else 1
if __name__=='__main__': sys.exit(main())
