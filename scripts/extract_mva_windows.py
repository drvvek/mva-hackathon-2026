#!/usr/bin/env python3
"""Extract PASS/non-ref variants in MVA-gene windows from a local GATK VCF.

Does not download or redistribute challenge data. Point MVA_VCF at your
gated local copy.

  python scripts/extract_mva_windows.py --vcf D:/Hackathon/WGS_EX2312012_HGWCNDSX7.vcf.gz

Optional: Ensembl REST for canonical exons (needs network).
"""
from __future__ import annotations

import argparse
import csv
import gzip
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_genes(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def chrom_norm(chrom: str) -> str:
    return chrom[3:] if chrom.lower().startswith("chr") else chrom


def fetch_canonical_exons(symbol: str) -> list[tuple[int, int]]:
    url = (
        f"https://rest.ensembl.org/lookup/symbol/homo_sapiens/{symbol}"
        "?content-type=application/json;expand=1"
    )
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        d = json.loads(r.read().decode())
    tid = None
    tlen = -1
    for t in d.get("Transcript") or []:
        if t.get("is_canonical"):
            tid = t["id"]
            break
        if t.get("biotype") == "protein_coding" and (t.get("length") or 0) > tlen:
            tlen = t.get("length") or 0
            tid = t["id"]
    if not tid:
        return []
    url2 = f"https://rest.ensembl.org/lookup/id/{tid}?content-type=application/json;expand=1"
    req2 = urllib.request.Request(url2, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req2, timeout=30) as r:
        td = json.loads(r.read().decode())
    return [(int(e["start"]), int(e["end"])) for e in td.get("Exon") or []]


def overlaps(exons: list[tuple[int, int]], pos: int, endpos: int) -> bool:
    return any(pos <= e and endpos >= s for s, e in exons)


def open_vcf(path: Path):
    if str(path).endswith(".gz"):
        return gzip.open(path, "rt", errors="replace")
    return path.open("rt", encoding="utf-8", errors="replace")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--vcf", required=True, type=Path)
    p.add_argument("--genes", type=Path, default=ROOT / "config" / "mva_genes.json")
    p.add_argument("--out", type=Path, default=ROOT / "output" / "mva_gene_window_variants.tsv")
    p.add_argument("--exons", action="store_true", help="flag canonical-exon overlap via Ensembl")
    args = p.parse_args()
    if not args.vcf.is_file():
        print(f"VCF not found: {args.vcf}", file=sys.stderr)
        return 2

    cfg = load_genes(args.genes)
    pad = int(cfg.get("pad_bp", 50))
    intervals = []
    for g, rec in cfg["genes"].items():
        intervals.append((g, str(rec["chrom"]), rec["start"] - pad, rec["end"] + pad))

    exons: dict[str, list[tuple[int, int]]] = {g: [] for g, *_ in intervals}
    if args.exons:
        for g in list(exons):
            try:
                exons[g] = fetch_canonical_exons(g)
                print(f"{g}: {len(exons[g])} exons", file=sys.stderr)
            except Exception as e:
                print(f"{g}: exon fetch failed ({e})", file=sys.stderr)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "gene", "chrom", "pos", "id", "ref", "alt", "qual", "filter",
        "gt", "dp", "ad", "in_exon",
    ]
    n_var = n_hit = 0
    with open_vcf(args.vcf) as f, args.out.open("w", encoding="utf-8", newline="") as w:
        wr = csv.DictWriter(w, fieldnames=fields, delimiter="\t")
        wr.writeheader()
        for line in f:
            if line.startswith("#"):
                continue
            n_var += 1
            cols = line.rstrip("\n").split("\t")
            chrom_n = chrom_norm(cols[0])
            pos = int(cols[1])
            hits = [g for g, c, s, e in intervals if chrom_n == c and s <= pos <= e]
            if not hits:
                continue
            fmt = cols[8].split(":") if len(cols) > 8 else []
            samp = cols[9].split(":") if len(cols) > 9 else []
            kv = dict(zip(fmt, samp)) if fmt and samp else {}
            gt = kv.get("GT", "")
            if gt in ("", ".", "./.", "0/0", "0|0"):
                continue
            ref, alt = cols[3], cols[4]
            endpos = pos + max(len(ref), 1) - 1
            for g in hits:
                n_hit += 1
                wr.writerow({
                    "gene": g,
                    "chrom": cols[0],
                    "pos": pos,
                    "id": cols[2],
                    "ref": ref,
                    "alt": alt,
                    "qual": cols[5],
                    "filter": cols[6],
                    "gt": gt,
                    "dp": kv.get("DP", ""),
                    "ad": kv.get("AD", ""),
                    "in_exon": overlaps(exons[g], pos, endpos) if exons[g] else "",
                })
    print(f"scanned={n_var} written={n_hit} -> {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
