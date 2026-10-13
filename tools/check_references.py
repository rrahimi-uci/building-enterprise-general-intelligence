#!/usr/bin/env python3
"""Validate citation registry, in-text markers, scopes, and verification records."""
from __future__ import annotations
import argparse, json, re, sys
import json
from pathlib import Path
from urllib.request import Request, urlopen


def book_release(root: Path) -> str:
    """The single source of the release identifier.

    Hard-coding it meant a generated report could claim 1.0.0 while every other
    artifact said 2.0.0 -- the evidence disagreeing with the thing it certifies.
    """
    return json.loads((root / "config" / "book.json").read_text(encoding="utf-8"))["book"]["version"]


LIVING = ("Current documentation","Living guidance","Development status","Implementation overview")
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
        year=str(r.get("year",""))
        if not re.fullmatch(r"\d{4}|n\.d\.",year): errors.append(f"{r.get('id')}: year must be YYYY or n.d.")
        rec=verification.get(r.get("id"))
        # Dating rule: living documentation is n.d. unless the page itself shows
        # a date, and then the verification caveat must record that date's year.
        if str(r.get("publication_or_version","")).startswith(LIVING) and year!="n.d." and year not in str((rec or {}).get("caveat","")):
            errors.append(f"{r.get('id')}: living documentation must use n.d. unless its verification caveat records the date shown on the page")
        if not rec: errors.append(f"{r.get('id')}: missing verification record")
        elif rec.get("status") not in {"verified","verified_with_caveat"}: errors.append(f"{r.get('id')}: verification status is {rec.get('status')!r}")
        elif rec.get("verified")!=(r.get("verification") or {}).get("checked_on"): errors.append(f"{r.get('id')}: verification record date {rec.get('verified')!r} differs from registry checked_on")
    markers=re.findall(r"\[(R\d{2})\]",manuscript)
    marker_ids=sorted(set(markers))
    unknown=sorted(set(marker_ids)-set(ids)); uncited=sorted(set(ids)-set(marker_ids))
    if unknown: errors.append(f"Unknown citation markers: {unknown}")
    if uncited: errors.append(f"Uncited registry entries: {uncited}")
    if manuscript.count("# Appendix J — References")!=1: errors.append("Appendix J References heading must occur exactly once")
    # The traceability matrix lives in Appendix J, next to the entries it scopes.
    if manuscript.count("## Where each claim is supported")!=1: errors.append("Where each claim is supported must occur exactly once inside Appendix J")
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
        "release":book_release(root),"checked":refs_doc.get("verified_on",""),"references":len(refs),
        "citation_occurrences":len(markers),"cited_ids":marker_ids,
        "unknown_ids":unknown,"uncited_ids":uncited,"errors":errors,"warnings":warnings,
        "online_check":online,"verification_records":list(verification.values()),
        "pass":not errors,
        "scope_note":"Verification establishes source support only for each registry scope; it does not validate book-authored recommendations."
    }
    (root/"reports").mkdir(exist_ok=True)
    (root/"reports/citation-verification.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    lines=["# Citation Audit — Book v1.0.0","",f"**Result:** {'PASS' if not errors else 'FAIL'}",f"**References:** {len(refs)}",f"**Citation occurrences:** {len(markers)}",f"**Verified:** {refs_doc.get('verified_on','')}","","All sources were checked against their recorded claim scope. The audit validates attribution, not the book's independently authored architecture recommendations.","","## Source-by-source status", "", "| ID | Status | Method | Caveat |", "|---|---|---|---|"]
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
