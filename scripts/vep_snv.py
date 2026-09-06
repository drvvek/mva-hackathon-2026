#!/usr/bin/env python3
"""Query Ensembl VEP REST for a GRCh38 SNV (no local VCF required).

  python scripts/vep_snv.py --chrom 15 --pos 40220612 --alt G
  python scripts/vep_snv.py --chrom 15 --pos 40220612 --alt A
"""
from __future__ import annotations

import argparse
import json
import urllib.request


def vep(chrom: str, pos: int, alt: str) -> list:
    chrom = chrom[3:] if chrom.lower().startswith("chr") else chrom
    url = (
        f"https://rest.ensembl.org/vep/human/region/{chrom}:{pos}-{pos}/{alt}"
        "?content-type=application/json;hgvs=1;canonical=1"
    )
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.loads(r.read().decode())


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--chrom", required=True)
    p.add_argument("--pos", required=True, type=int)
    p.add_argument("--alt", required=True)
    p.add_argument("--gene", default="BUB1B")
    args = p.parse_args()
    rec = vep(args.chrom, args.pos, args.alt)[0]
    print("most_severe", rec.get("most_severe_consequence"))
    for t in rec.get("transcript_consequences") or []:
        if t.get("gene_symbol") != args.gene:
            continue
        if not t.get("canonical"):
            continue
        keep = [
            "transcript_id", "hgvsc", "hgvsp", "amino_acids", "codons",
            "consequence_terms", "sift_prediction", "sift_score",
            "polyphen_prediction", "polyphen_score", "impact",
        ]
        print(json.dumps({k: t.get(k) for k in keep}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
