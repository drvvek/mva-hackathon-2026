#!/usr/bin/env python3
"""Write a Track 1 CSV from config/primary_pair.json (no VCF required).

Chromosomes are emitted with the hackathon template prefix (chr).
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def chrom(cfg: dict, c: str) -> str:
    """Hackathon template uses chr15, not 15."""
    c = str(c)
    if c.lower().startswith("chr"):
        return "chr" + c[3:]
    return "chr" + c


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--pair", type=Path, default=ROOT / "config" / "primary_pair.json")
    p.add_argument("--out", type=Path, default=ROOT / "output" / "track1_submission.csv")
    args = p.parse_args()
    cfg = json.loads(args.pair.read_text(encoding="utf-8"))
    a1, a2 = cfg["allele_1"], cfg["allele_2"]
    notes = (
        "BUB1B MVA1 candidate (GRCh38): "
        f"{a1['chrom']}:{a1['pos']} {a1['ref']}>{a1['alt']} = {a1['hgvs']} {a1['protein']} "
        f"({a1['note']}) + "
        f"{a2['chrom']}:{a2['pos']} {a2['ref']}>{a2['alt']} = {a2['hgvs']} {a2['protein']} "
        f"({a2['note']}). Both PASS het, balanced AD, WGS_EX2312012. "
        "Phase unproven (no parents). Other MVA-gene windows in this extract lack a second rare coding hit. "
        "same AA change as ClinVar VCV004600147 (c.3006T>A, Ambry VUS, in silico inconclusive per submitter "
        "— conflicts with our SIFT/PolyPhen call, unresolved)"
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "proband_id", "chrom_1", "pos_1", "ref_1", "alt_1",
        "chrom_2", "pos_2", "ref_2", "alt_2", "epcr", "finding_type", "notes",
    ]
    with args.out.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerow({
            "proband_id": cfg["proband_id"],
            "chrom_1": chrom(cfg, a1["chrom"]),
            "pos_1": a1["pos"],
            "ref_1": a1["ref"],
            "alt_1": a1["alt"],
            "chrom_2": chrom(cfg, a2["chrom"]),
            "pos_2": a2["pos"],
            "ref_2": a2["ref"],
            "alt_2": a2["alt"],
            "epcr": cfg["epcr"],
            "finding_type": cfg["finding_type"],
            "notes": notes,
        })
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
