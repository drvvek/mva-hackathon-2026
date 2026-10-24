Team MosaicTrace · Rare Disease, Real Kid: MVA Hackathon 2026

This folder holds the supporting files for the Track 2 report. The report itself is submitted as a PDF through the challenge portal. The method abstract and the methods description form are in Appendix B of that report, so there is no separate form file here.

The report screens 40 drugs and drug classes against a child with biallelic *BUB1B* disease. It ranks six as ALLOW-CONTINGENT, each with an unlock condition, a pre-declared readout and a stop rule. Three are supportive, two exposures are flagged for withdrawal review, one lies outside the question, and 28 are excluded. Nothing has been measured in the child, so no ranked agent is unlocked. Nothing here is a treatment recommendation.

## Files

| File | What it is | Where it appears in the report |
|---|---|---|
| `reconciled_candidate_ledger_final.csv` | The 40-row ledger of record: route of identification, baseline and final verdict, rank, and the PMIDs from the written search for contradictory evidence (separated by semicolons) | Tables 6, 9 and 13 to 21 |
| `fig1_bubr1_domain_map_final.png` | Figure 1, BUBR1 domain map | Figure 1 |
| `fig2_candidate_filter_screen_v3.png` | Figure 2, each candidate against filters f1 to f7 and the cytotoxic firewall | Figure 2 |
| `fig3_decision_sequence_v2.png` | Figure 3, the assay sequence that decides which ranked agents can be unlocked | Figure 3, Table 11 |
| `viewer/sensitivity_viewer.html` | Companion viewer (below) | Section 8 |
| `viewer/candidate_filter_matrix.csv` | The Figure 2 cells for all 40 candidates | Figure 2 |
| `viewer/exclusion_reasons.csv` | The 60 recorded reasons for exclusion, each coded to a filter and, where it applies, to the assumption it rests on | Tables 17 to 21 |
| `viewer/row_dependencies.csv` | What each switch does to each ranked, supportive and review row | Tables 11, 12, 14 and 22 |

## The viewer

`viewer/sensitivity_viewer.html` is one self-contained file. Open it in a browser; it needs no installation and makes no network requests except when you click a PubMed link.

It can also be accessed via: https://drvvek.github.io/mva-hackathon-2026/Track%202/viewer/sensitivity_viewer.html 

It answers one question: if an assumption or a filter were removed, which of the report's recorded reasons would no longer hold? The switches follow the report: Assumptions W, Q, O and T, filters f1 to f7 and the gates f7a, f7b and f8, the stability result for p.(Asn1002Lys), the interferon-stimulated gene readout, and the treatment phase. One further switch stands for the rhabdomyosarcoma that the arimoclomol exclusion rests on, which Table 22 marks as not transferable. The preset "General MVA1 family (Table 22)" applies that table's list of what transfers to another family.

It reads the reasons the report already wrote. It does not run a new screen, re-rank anything or recalculate an unlock condition. "Re-opens" means that no recorded reason for exclusion remains, which is not an endorsement of that agent. The three CSV files are the same data in readable form, so each claim can be checked against the report without reading the page's code.

## What is not here

No patient genome file, participant reference document or Track 1 scorer output is in this folder. Track 1 is elsewhere in this repository.
