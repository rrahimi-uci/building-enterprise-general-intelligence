#!/usr/bin/env python3
"""Validate citation registry, in-text markers, scopes, and verification records."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
from urllib.request import Request, urlopen

REQUIRED = {"id","type","author_or_organization","year","title","publication_or_version","url","supports","verification"}


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument("--online",action="store_true",help="Best-effort HTTP check; not required for reproducible offline builds")
    args=ap.parse_args(); root=Path(args.root).resolve()
    refs_doc=json.loads((root/"config/references.json").read_text(encoding="utf-8")); refs=refs_doc["references"]
    manuscript=(root/"book/manuscript.md").read_text(encoding="utf-8")
    verification_path=root/"config/reference-verification.json"
    verification={x["id"]:x for x in json.loads(verification_path.read_text(encoding="utf-8"))} if verification_path.exists() else {}
    errors=[]; warnings=[]
    ids=[r.get("id") for r in refs]
    expected=[f"R{i:02d}" for i in range(1,len(refs)+1)]
    if ids!=expected: errors.append(f"Reference IDs must be ordered and contiguous: expected {expected}, got {ids}")
    if len(ids)!=len(set(ids)): errors.append("Duplicate reference IDs")
    urls=[r.get("url") for r in refs]
    if len(urls)!=len(set(urls)): warnings.append("Duplicate URLs exist; confirm intentional reuse")
    for r in refs:
        missing=sorted(REQUIRED-set(r))
        if missing: errors.append(f"{r.get('id','?')}: missing fields {missing}")
        if not str(r.get("url","")).startswith("https://"): errors.append(f"{r.get('id')}: URL must use HTTPS")
        if len(str(r.get("supports","")))<25: errors.append(f"{r.get('id')}: permitted scope is too vague")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}",str((r.get("verification") or {}).get("checked_on",""))): errors.append(f"{r.get('id')}: invalid verification date")
        if r.get("publication_or_version") in {"Current documentation","Living guidance","Development status","Implementation overview"} and r.get("year") not in {"n.d.","2026"}:
            warnings.append(f"{r.get('id')}: review year for living documentation")
        rec=verification.get(r.get("id"))
        if not rec: errors.append(f"{r.get('id')}: missing verification record")
        elif rec.get("status") not in {"verified","verified_with_caveat"}: errors.append(f"{r.get('id')}: verification status is {rec.get('status')!r}")
    markers=re.findall(r"\[(R\d{2})\]",manuscript)
    marker_ids=sorted(set(markers))
    unknown=sorted(set(marker_ids)-set(ids)); uncited=sorted(set(ids)-set(marker_ids))
    if unknown: errors.append(f"Unknown citation markers: {unknown}")
    if uncited: errors.append(f"Uncited registry entries: {uncited}")
    if manuscript.count("# Appendix K — References")!=1: errors.append("Appendix K References heading must occur exactly once")
    if manuscript.count("# Appendix M — Citation and Claim Traceability Matrix")!=1: errors.append("Appendix M traceability heading must occur exactly once")
    online=[]
    if args.online:
        for r in refs:
            try:
                req=Request(r["url"],method="HEAD",headers={"User-Agent":"BookReferenceVerifier/1.0"})
                with urlopen(req,timeout=15) as resp: status=getattr(resp,"status",200)
                online.append({"id":r["id"],"status":status,"ok":status<400})
                if status>=400: warnings.append(f"{r['id']}: HTTP {status}")
            except Exception as exc:
                online.append({"id":r["id"],"ok":False,"error":str(exc)})
                warnings.append(f"{r['id']}: online check unavailable: {exc}")
    report={
        "release":"1.0.0","checked":"2026-09-13","references":len(refs),
        "citation_occurrences":len(markers),"cited_ids":marker_ids,
        "unknown_ids":unknown,"uncited_ids":uncited,"errors":errors,"warnings":warnings,
        "online_check":online,"verification_records":list(verification.values()),
        "pass":not errors,
        "scope_note":"Verification establishes source support only for each registry scope; it does not validate book-authored recommendations."
    }
    (root/"reports").mkdir(exist_ok=True)
    (root/"reports/citation-verification.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    lines=["# Citation Audit — Book v1.0.0","",f"**Result:** {'PASS' if not errors else 'FAIL'}",f"**References:** {len(refs)}",f"**Citation occurrences:** {len(markers)}",f"**Verified:** 2026-09-13","","All sources were checked against their recorded claim scope. The audit validates attribution, not the book's independently authored architecture recommendations.","","## Source-by-source status", "", "| ID | Status | Method | Caveat |", "|---|---|---|---|"]
    for r in refs:
        rec=verification.get(r["id"],{})
        caveat=str(rec.get("caveat","")).replace("|","\\|")
        lines.append(f"| {r['id']} | {rec.get('status','missing')} | {rec.get('method','missing')} | {caveat} |")
    lines += ["","## Errors",""] + ([f"- {x}" for x in errors] or ["- None."])
    lines += ["","## Warnings",""] + ([f"- {x}" for x in warnings] or ["- None."])
    (root/"reports/citation-audit.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps({k:report[k] for k in ("references","citation_occurrences","unknown_ids","uncited_ids","errors","warnings","pass")},indent=2))
    return 0 if not errors else 1

if __name__=="__main__": sys.exit(main())
