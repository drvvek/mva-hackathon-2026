# Track 1 methods — BUB1B (MVA1)

**Not a clinical report.** Interpretation of gated WGS `WGS_EX2312012` (GRCh38). VCF contig names are `15`; the official CSV template uses `chr15` / `PROBAND01`.

Reproduce with the scripts in this repo against a local copy of the gated dataset. Do not redistribute sequence data.

CSV alleles are unchanged from submission 1 (full match at rank 1). This document updates the methods write-up only.

## Phenotype (challenge HPO file)

Rhabdomyosarcoma (HP:0002859), growth restriction / SGA (HP:0001518, HP:0004322), failure to thrive / muscle atrophy (HP:0001508, HP:0003202), prematurity (HP:0001622), nephrocalcinosis (HP:0000121), parental recurrent miscarriage (HP:0200067). Compatible with spindle-assembly-checkpoint failure / mosaic variegated aneuploidy, not a singleton sarcoma gene.

## Pipeline

1. Unannotated GATK VCFv4.2, GRCh38 `no_chr` analysis set, sample `WGS_EX2312012`.
2. Window all major MVA/SAC genes (see `config/mva_genes.json`) ±50 bp. Flag canonical-exon overlap via Ensembl MANE exons.
3. Keep non-ref genotypes. Discard low-quality calls by GATK FILTER / depth. **Absence of an rsID is not used as evidence of rarity** (83/1,467 window calls lack an rsID; one novel-looking exonic indel is a 26% 3′UTR polymorphism). Frequency comes from gnomAD r4 (direct lookup for the candidate pair; VEP colocated frequencies otherwise).
4. Annotate remaining coding SNVs with Ensembl VEP REST, **MANE Select** `NM_001211.6` / `ENST00000287598.11`.
5. One primary CSV row: both alleles of the candidate pair. Scorer matches `chrom,pos,ref,alt` only.

## Primary pair — submit VCF alleles, not HGVS

One primary row. `epcr=0.85`. Gene + phenotype + truncating ClinVar hit + allele-2 gnomAD singleton pull up. **Phase unknown**, in-silico disagreement on N1002K, and **untested coverage in TRIP13/CEP57 windows** pull down.

| | Genomic (GRCh38, as in VCF) | MANE NM_001211.6 | Protein | What is actually known |
|---|---|---|---|---|
| Allele 1 | **chr15:40209701 T>G** | c.2210T>G | p.Leu737Ter | Exact ClinVar record **VCV000533901**, rs759242053. Pathogenic / likely pathogenic for MVA1; **2-star**, criteria provided, multiple submitters, no conflicts. **Exon 17/23** — NMD-competent (not last-exon). PASS het, DP=46 AD=21,25. gnomAD r4: **115/1,461,846** exome + **5/152,174** genome heterozygotes, **0 homozygotes**, no gnomAD filter flags. ClinVar still warns that frequency *at this site* may be unreliable; we therefore do not use the point AF as evidence. We use **0 homozygotes** plus BUB1B constraint (pLI ≈ 0, LOEUF 0.75): heterozygous LoF is tolerated, which is the expected AR/MVA1 pattern. |
| Allele 2 | **chr15:40220612 T>G** | c.3006T>G | p.Asn1002Lys | **This nucleotide is not in ClinVar or dbSNP.** Direct gnomAD r4 lookup: **15-40220612-T-G, AC=1, AN=1,461,878 (AF 6.8×10⁻⁷), 0 homozygotes, no filters; absent from genomes.** Same amino-acid change as ClinVar **c.3006T>A** VCV004600147 (Ambry, VUS, 1 star, in silico inconclusive). Same codon T>C is VCV004842697, synonymous p.Asn1002=, likely benign — so the third base matters between synonymous and missense, not between T>A and T>G (both Lys). Submitting **T>G** because that is the VCF allele. PASS het, DP=28 AD=15,13. Circumstantial: 29 bp from Hanks 2004 founder c.3035T>C p.Leu1012Pro (rs28989185), kinase domain. |

If the gold key were T>A at 40220612, a T>G row scores zero on that allele. Submission 1 already confirmed full match on these VCF alleles.

Site-level QC (neither call breaches GATK SNV hard filters):

| | QUAL | QD | FS | SOR | MQ | GQ | AD | VAF |
|---|---|---|---|---|---|---|---|---|
| 15:40209701 T>G | 708.8 | 15.4 | 1.12 | 0.52 | 60 | 99 | 21,25 | 0.54 |
| 15:40220612 T>G | 344.8 | 12.3 | 1.62 | 0.33 | 60 | 99 | 15,13 | 0.46 |

## SIFT / PolyPhen vs Ambry

Re-queried Ensembl VEP on GRCh38 `15:40220612`.

- Transcript is MANE Select, not stale: `ENST00000287598.11` = **NM_001211.6**.
- Scores are protein-level and identical for T>G (VCF) and T>A (ClinVar VUS): both `p.Asn1002Lys`, SIFT **0.01 deleterious**, PolyPhen-2 **0.997 probably_damaging**. Third-position wobble cannot explain the split.
- Ambry SCV on c.3006T>A: Asn→Lys “similar properties”; in silico inconclusive; VUS, 1 star.

Same MANE transcript, same AA change, **tools disagree**. Do not cite SIFT/PolyPhen as independent support for pathogenicity of N1002K. Rarity for allele 2 is the gnomAD singleton count, not the in-silico scores.

## Phase — do not overstate

No parents. No PGT/PID on these sites. 11.0 kb is beyond short-read local phasing. The only phase set (`PID`) in the BUB1B window is an unrelated adjacent pair at 40216568/40216570. **Trans is an inference from AR MVA1 + this genotype, not a demonstrated compound-het.**

## Negative screen (this extract only)

1,467 non-ref calls in 12 MVA/SAC windows. 34 overlap a MANE exon; **13 are coding**. Only **two coding calls have AF &lt; 10⁻³, and both are the BUB1B pair**.

- BUB1B: only two canonical-exon hits are the pair above. Other BUB1B hets (rs185599777, rs372589327, rs28570325, rs28620590) are named polymorphisms. `15:40180642 CT>C` is DP=13 QUAL=19.8 — discard.
- **BUB3** `10:123164968 CTT>C` is PASS, DP 35, no rsID in the VCF, exon-overlapping: this is **rs34736387**, 3′UTR `c.*1143_*1144del`, AF ~0.16–0.26. Benign; named here because a reader reproducing the screen will hit it.
- **MAD1L1** `7:2225526 G>A` rs121908982 p.Arg59Cys: next-rarest coding call, **AF 4.6×10⁻³** (NFE 5.4×10⁻³), SIFT 0.06 tolerated. Too common for a penetrant recessive MVA allele. (Also a reported somatic prostate-cancer allele; MVA7 alleles are Q66* / E628*.) One het ≠ MVA7.
- CEP192: 7 coding calls in this extract, all common (AF 0.05–0.90). SLF2 / SMC5 likewise.
- MAD2L1BP rs7106: common (AF ~0.15–0.28). Ensembl consequence is transcript-dependent (coding vs upstream); frequency rules it out either way.
- **TRIP13 (MVA3) and CEP57 (MVA2) were not negatively proven.** TRIP13: 3 calls, all DP 7, spanning a fraction of the gene. CEP57: 4 calls, none coding, call density ~20-fold below MAD1L1. A non-reference-only extract cannot distinguish homozygous-reference from not covered. Defensible statement: **no callable coding variant in these windows; coverage undemonstrated.**

This is **not** “the genome contains nothing else.” Structural variants, deep-intronic splice, mosaic aneuploidy from read depth, and genes outside the 12 windows were not tested. No splice-site candidate within 8 bp of a MANE exon boundary was found among QC-passing novel calls in these windows.

## Limits

Single-sample WGS, no VEP in the released VCF, no gVCF/coverage track, no parental BAM, no Western / SAC assay / parental PCS karyotype.

## Acknowledgement

This work was made possible through the Hackathon, organized by Sage Bionetworks in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking, Evaluation, and Assessment Consortium for Science), with prize sponsorship from AWS and Anthropic. We are deeply grateful to the child and their family who generously contributed their data and their story to advance research into this rare disease. We acknowledge their trust in making this Hackathon possible.
