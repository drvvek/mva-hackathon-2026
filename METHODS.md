# Track 1 methods — BUB1B (MVA1)

**Not a clinical report.** Interpretation of gated WGS `WGS_EX2312012` (GRCh38). VCF contig names are `15`; the official CSV template uses `chr15` / `PROBAND01`.

Reproduce with the scripts in this repo against a local copy of the gated dataset. Do not redistribute sequence data.

## Phenotype (challenge HPO file)

Rhabdomyosarcoma (HP:0002859), growth restriction / SGA (HP:0001518, HP:0004322), failure to thrive / muscle atrophy (HP:0001508, HP:0003202), prematurity (HP:0001622), nephrocalcinosis (HP:0000121), parental recurrent miscarriage (HP:0200067). Compatible with spindle-assembly-checkpoint failure / mosaic variegated aneuploidy, not a singleton sarcoma gene.

## Pipeline

1. Unannotated GATK VCFv4.2, GRCh38 `no_chr` analysis set, sample `WGS_EX2312012`.
2. Window all major MVA/SAC genes (see `config/mva_genes.json`) ±50 bp. Flag canonical-exon overlap via Ensembl.
3. Keep non-ref genotypes. Discard low-quality / common-intronic background by rsID and depth.
4. Annotate remaining coding SNVs with Ensembl VEP REST, **MANE Select** `NM_001211.6` / `ENST00000287598.11`.
5. One primary CSV row: both alleles of the candidate pair. Scorer matches `chrom,pos,ref,alt` only.

## Primary pair — submit VCF alleles, not HGVS

One primary row. `epcr=0.85`: gene + phenotype + truncating ClinVar hit pull up; **phase unknown** and allele 2's in silico support is unresolved rather than clean (SIFT/PolyPhen disagree with Ambry on the identical protein change) — pull down.

| | Genomic (GRCh38, as in VCF) | MANE NM_001211.6 | Protein | What is actually known |
|---|---|---|---|---|
| Allele 1 | **chr15:40209701 T>G** | c.2210T>G | p.Leu737Ter | Exact ClinVar record (VCV000533901; rs759242053). Pathogenic / likely pathogenic for MVA1. PASS het, DP=46 AD=21,25. Do **not** treat gnomAD AF as clean — ClinVar notes frequency at this position as unreliable. |
| Allele 2 | **chr15:40220612 T>G** | c.3006T>G | p.Asn1002Lys | This nucleotide (c.3006T>G) is not in ClinVar, but the **same amino-acid change** is: c.3006T>A → VCV004600147, Ambry Genetics, **VUS (1 star)**, submitter states in silico prediction is inconclusive. Submitting c.3006T>G because that is the VCF allele. PASS het, DP=28 AD=15,13. Circumstantial: 29 bp from Hanks 2004 founder c.3035T>C p.Leu1012Pro (rs28989185), kinase domain. |

If the gold key were T>A at 40220612, a T>G row scores zero on that allele.

## SIFT / PolyPhen vs Ambry

Re-queried Ensembl VEP on GRCh38 `15:40220612`.

- Transcript is MANE Select, not stale: `ENST00000287598.11` = **NM_001211.6**.
- Scores are protein-level and identical for T>G (VCF) and T>A (ClinVar VUS): both `p.Asn1002Lys`, SIFT **0.01 deleterious**, PolyPhen-2 **0.997 probably_damaging**. Third-position wobble cannot explain the split.
- Ambry SCV on c.3006T>A: Asn→Lys “similar properties”; in silico inconclusive; VUS, 1 star.

Same MANE transcript, same AA change, **tools disagree**. Do not cite SIFT/PolyPhen as independent support for pathogenicity of N1002K.

## Phase — do not overstate

No parents. No PGT/PID on these sites. ~11 kb is beyond short-read local phasing. **Trans is an inference from AR MVA1 + this genotype, not a demonstrated compound-het.**

## Negative screen (this extract only)

Windows: BUB1B, CEP57, TRIP13, CENATAC, SLF2, SMC5, MAD1L1, BUB1, MAD2L1BP, CEP192, BUB3, MAD2L1.

- BUB1B: only two canonical-exon hits are the pair above. Other BUB1B hets (rs185599777, rs372589327, rs28570325, rs28620590) are named polymorphisms. `15:40180642 CT>C` is DP=13 QUAL=19.8 — discard.
- CEP57 / TRIP13 / CENATAC: no AR coding pair. TRIP13 has two DP=7 hets — quality fail.
- MAD2L1BP rs7106: one common coding het, not biallelic LoF.
- MAD1L1 `7:2225526 G>A` rs121908982 (p.Arg59Cys) is a reported somatic prostate-cancer allele, not MVA7 (MVA7 alleles are Q66* / E628*). One het ≠ MVA7.

This is **not** “the genome contains nothing else.” Structural variants, deep-intronic splice, and genes outside these windows were not tested.

## Limits

Single-sample WGS, no VEP in the released VCF, no parental BAM, no Western / SAC assay / parental PCS karyotype.

## Acknowledgement

This work was made possible through the Hackathon, organized by Sage Bionetworks in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking, Evaluation, and Assessment Consortium for Science), with prize sponsorship from AWS and Anthropic. We are deeply grateful to the child and their family who generously contributed their data and their story to advance research into this rare disease. We acknowledge their trust in making this Hackathon possible.
