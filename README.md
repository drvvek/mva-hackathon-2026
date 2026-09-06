# Rare Disease, Real Kid — MVA Hackathon 2026 (Track 1)

Private methods + code for SageBio / MVA Society / Hugging Face hackathon Track 1 (variant prediction).

**This repository must not contain the child's genome.** VCF, FASTQ, BAM, and the phenotype `.docx` stay on the local gated copy only. Do not open this repo until hackathon close (rules: public after close, CC BY 4.0).

## What is here

| Path | Purpose |
|---|---|
| `METHODS.md` | Write-up to upload with the Track 1 form |
| `config/mva_genes.json` | GRCh38 windows for MVA / SAC genes |
| `config/primary_pair.json` | Chosen BUB1B pair (VCF alleles, not HGVS) |
| `scripts/extract_mva_windows.py` | Pull non-ref variants in those windows from a **local** VCF |
| `scripts/vep_snv.py` | Ensembl VEP REST for one SNV |
| `scripts/build_track1_csv.py` | Emit the official CSV template |

## Run (local data, not in git)

```bash
# 1. Window extract (optional --exons needs Ensembl)
python scripts/extract_mva_windows.py \
  --vcf D:/Hackathon/WGS_EX2312012_HGWCNDSX7.vcf.gz \
  --exons \
  --out output/mva_gene_window_variants.tsv

# 2. Confirm MANE consequences
python scripts/vep_snv.py --chrom 15 --pos 40209701 --alt G
python scripts/vep_snv.py --chrom 15 --pos 40220612 --alt G
python scripts/vep_snv.py --chrom 15 --pos 40220612 --alt A   # ClinVar VUS nucleotide

# 3. Build submission CSV
python scripts/build_track1_csv.py --out output/track1_submission.csv
```

Python 3.11+, stdlib only.

## Track 1 form

1. `output/track1_submission.csv`
2. `METHODS.md` (or PDF export)
3. This GitHub URL (private until close)

## Acknowledgement

This work was made possible through the Hackathon, organized by Sage Bionetworks in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking, Evaluation, and Assessment Consortium for Science), with prize sponsorship from AWS and Anthropic. We are deeply grateful to the child and their family who generously contributed their data and their story to advance research into this rare disease. We acknowledge their trust in making this Hackathon possible.
