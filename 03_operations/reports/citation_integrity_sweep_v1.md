# Citation Integrity Sweep v1

**Date:** 2026-06-23
**Author:** Research Agent (TASK-383)
**Tool:** `03_operations/validators/verify_citations.py`
**Scope:** All governance/evidence files carrying PMIDs or DOIs under `01_framework/` and `03_operations/`

---

## Why This Sweep Was Run

LLM agents hallucinate exact identifiers — PMIDs and DOIs — even when the underlying claim is scientifically real. Two confirmed fabrications triggered this sweep:

1. EV-104 (hard cheese sat-fat relief) cited three studies by PMID. All three PMIDs resolve to unrelated papers (stroke neurology, yogurt-diabetes review, leukemia miRNA paper).
2. The registry's "Monteiro 2019 NOVA" citation (PMID 31122155) resolves to an unrelated nursing workplace case study.

The fix is deterministic machine-verification, not a prompt instruction. This report is the output of the first full run.

---

## Sweep Summary

| Status | Count |
|--------|-------|
| Total identifiers checked | 51 |
| PASS | 40 |
| MISMATCH | 8 |
| FABRICATED | 0 |
| UNRESOLVED-DOI | 3 |

**Exit code: 1** (MISMATCH found — action required)

Note: The validator classifies wrong-id citations as MISMATCH (resolves, but to a different paper). FABRICATED is reserved for ids that return no record at all from PubMed. All 8 MISMATCHes confirmed below to be identifiers that resolve to unrelated papers — functionally fabricated wrong ids for claims that may be real.

A ninth mismatch (PMID 28615384, Thorning cheese RCT) was classified as PASS by the heuristic because the resolved paper (yogurt/diabetes review) shares "dairy" vocabulary with the context, but is semantically wrong. It is recorded separately in the known-gaps section below.

---

## Files Scanned

| File | Citations Extracted |
|------|---------------------|
| `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md` | 61 |
| `01_framework/governance/evidence_registry_v1.md` | 0 |
| `01_framework/glass_box/additive_tiered_library_v1.md` | 19 |
| `01_framework/glass_box/w2_additive_copy_v1.md` | 1 |
| `01_framework/glass_box/diaas_source_table_v1.md` | 33 |
| `01_framework/supplement_framework/methodology_v1.md` | 0 |
| `01_framework/editorial/editorial_intelligence_v3.md` | 0 |

---

## MISMATCH Findings — Full Detail

### FINDING-01: PMID 31122155 — Monteiro 2019 NOVA

| Field | Value |
|-------|-------|
| **Identifier** | PMID 31122155 |
| **File** | `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md` (lines 2550, 2555, 2558, 2560, 2768, 3076) |
| **Claimed as** | Monteiro et al. 2019, Public Health Nutrition — foundational NOVA framework paper classifying cheese as NOVA 1-2 |
| **Real paper** | "The Nurse With a Profound Disability: A Case Study." (2019, Workplace Health & Safety) |
| **Real URL** | https://pubmed.ncbi.nlm.nih.gov/31122155/ |
| **Verdict** | MISMATCH — wrong PMID for a claim that may be real |
| **Owning EV** | EV-099 (hard-cheese NOVA 1 governance), EV-104 |
| **Owning agent** | Nutrition Agent |
| **Notes** | The Monteiro 2019 NOVA paper exists and is real (doi 10.1017/S1368980019001307 also fails — see FINDING-02). The PMID is simply wrong. The actual Monteiro 2019 NOVA paper appears to have a different PMID. This fabrication propagated into multiple registry entries citing the same wrong PMID. |

---

### FINDING-02: DOI 10.1017/S1368980019001307 — Monteiro 2019 NOVA (DOI companion)

| Field | Value |
|-------|-------|
| **Identifier** | DOI 10.1017/S1368980019001307 |
| **File** | `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md` (line 2550) |
| **Claimed as** | Monteiro et al. 2019, Public Health Nutrition — NOVA classification paper |
| **Real paper** | "Skinfold thickness and the incidence of type 2 diabetes mellitus and hypertension: an analysis of the PERU MIGRANT study" (2019, Public Health Nutrition) |
| **Real URL** | https://doi.org/10.1017/S1368980019001307 |
| **Verdict** | MISMATCH — wrong DOI; both PMID and DOI for the Monteiro NOVA paper are fabricated |
| **Owning EV** | EV-099, EV-104 |
| **Owning agent** | Nutrition Agent |
| **Notes** | This is a different paper in the same journal (Public Health Nutrition) and same year. The real Monteiro 2019 NOVA DOI needs to be sourced from PubMed directly. Correct citation path: search PubMed for "Monteiro ultra-processed NOVA 2019 Public Health Nutrition" and verify the actual PMID and DOI before re-registering. |

---

### FINDING-03: PMID 39133879 — Kay 2024 Cheese LDL Study

| Field | Value |
|-------|-------|
| **Identifier** | PMID 39133879 |
| **File** | `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md` (lines 2758, 3074) |
| **Claimed as** | Kay et al. (2024), Am J Clin Nutr — controlled crossover trial (n=18) showing cheese produces lower LDL-C than butter at matched fat/sat_fat |
| **Real paper** | "Teaching NeuroImage: Short-Lasting Egocentric and Allocentric Visual Neglect After Right-Middle Cerebral Artery Stroke." (2024, Neurology) |
| **Real URL** | https://pubmed.ncbi.nlm.nih.gov/39133879/ |
| **Verdict** | MISMATCH — completely unrelated clinical field (stroke neurology) |
| **Owning EV** | EV-104 |
| **Owning agent** | Nutrition Agent |
| **Notes** | The Kay 2024 study and the DOI 10.1093/ajcn/nqae052 are cited together on line 2758. The DOI itself returns UNRESOLVED-DOI from CrossRef (not found), so both identifiers for this study are unverifiable. A search on PubMed for "Kay 2024 cheese butter LDL Am J Clin Nutr" is required to find the correct PMID if the study exists. |

---

### FINDING-04: DOI 10.1093/ajcn/nqae052 — Kay 2024 Cheese LDL Study (DOI)

| Field | Value |
|-------|-------|
| **Identifier** | DOI 10.1093/ajcn/nqae052 |
| **File** | `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md` (line 2758) |
| **Claimed as** | Kay et al. (2024), Am J Clin Nutr — same study as FINDING-03 |
| **Real paper** | UNRESOLVED — CrossRef returned no record |
| **Real URL** | https://doi.org/10.1093/ajcn/nqae052 |
| **Verdict** | UNRESOLVED-DOI (cannot confirm or deny existence) |
| **Owning EV** | EV-104 |
| **Owning agent** | Nutrition Agent |
| **Notes** | Together with FINDING-03, this means the Kay 2024 study cannot be verified by any identifier. Human research required: search PubMed for Kay + 2024 + cheese + LDL. If the study is real, both identifiers need correction. |

---

### FINDING-05: PMID 31022985 — Lordan 2019 Fermented Dairy Review

| Field | Value |
|-------|-------|
| **Identifier** | PMID 31022985 |
| **File** | `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md` (lines 2760, 3075) |
| **Claimed as** | Lordan et al. (2019), Nutrients — narrative review of hard fermented cheeses producing lower LDL-C than butter at equivalent sat_fat |
| **Real paper** | "MicroRNAs Mediated Regulation of Expression of Nucleoside Analog Pathway Genes in Acute Myeloid Leukemia." (2019, Genes) |
| **Real URL** | https://pubmed.ncbi.nlm.nih.gov/31022985/ |
| **Verdict** | MISMATCH — completely unrelated clinical field (leukemia miRNA) |
| **Owning EV** | EV-104 |
| **Owning agent** | Nutrition Agent |
| **Notes** | This is EV-104's second fabricated PMID. The DOI for this entry (10.3390/nu11040900) also fails — see FINDING-06. |

---

### FINDING-06: DOI 10.3390/nu11040900 — Lordan 2019 (DOI companion)

| Field | Value |
|-------|-------|
| **Identifier** | DOI 10.3390/nu11040900 |
| **File** | `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md` (line 2760) |
| **Claimed as** | Lordan et al. (2019), Nutrients — fermented dairy bioactives review |
| **Real paper** | "Factors Associated with Increased Alpha-Tocopherol Content in Milk in Response to Maternal Supplementation with 800 IU of Vitamin E" (2019, Nutrients) |
| **Real URL** | https://doi.org/10.3390/nu11040900 |
| **Verdict** | MISMATCH — wrong paper in same journal (Nutrients, same year) |
| **Owning EV** | EV-104 |
| **Owning agent** | Nutrition Agent |
| **Notes** | Both the PMID and the DOI for the Lordan 2019 claim are wrong. These are the classic hallucination pattern: real author + real year + real journal, wrong article-level identifiers. Search PubMed for "Lordan 2019 cheese fermented dairy LDL bioactive Nutrients" to find the correct identifiers. |

---

### FINDING-07: DOI 10.3945/ajcn.117.158543 — Thorning 2017 Cheese RCT (DOI)

| Field | Value |
|-------|-------|
| **Identifier** | DOI 10.3945/ajcn.117.158543 |
| **File** | `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md` (line 2762) |
| **Claimed as** | Thorning et al. (2017), Am J Clin Nutr — RCT (n=57, crossover) cheese vs butter vs control on LDL-C |
| **Real paper** | "Long-term weight-loss maintenance in obese patients with knee osteoarthritis: a randomized trial" (2017, Am J Clin Nutr) |
| **Real URL** | https://doi.org/10.3945/ajcn.117.158543 |
| **Verdict** | MISMATCH — correct journal and year, completely wrong paper |
| **Owning EV** | EV-104 |
| **Owning agent** | Nutrition Agent |
| **Notes** | See also FINDING-08: the companion PMID 28615384 resolves to "Yogurt and Diabetes" — another wrong paper. EV-104's Thorning 2017 citation has no verified identifier. Search PubMed for "Thorning 2017 cheese butter LDL crossover Am J Clin Nutr" to locate the correct identifiers. |

---

### FINDING-08: DOI 10.1016/j.cell.2021.12.019 — Chassaing 2022 CMC Human Trial

| Field | Value |
|-------|-------|
| **Identifier** | DOI 10.1016/j.cell.2021.12.019 |
| **File** | `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md` (line 115) |
| **Claimed as** | Chassaing et al. 2022 — controlled human feeding trial (n=16, crossover), CMC gut microbiota disruption at food-achievable doses |
| **Real paper** | "We like neurons" (2022, Cell) — editorial/comment piece |
| **Real URL** | https://doi.org/10.1016/j.cell.2021.12.019 |
| **Verdict** | MISMATCH — wrong article in the same journal |
| **Owning EV** | EV-003 (emulsifier risk), study_objects block |
| **Owning agent** | Nutrition Agent |
| **Notes** | The Chassaing 2022 CMC human trial is a real and important study (foundational for EV-003's Strong tier for CMC). The correct Cell reference is likely "Dietary emulsifiers directly alter human microbiota composition and gene expression ex vivo potentiating intestinal inflammation" — search PubMed for "Chassaing 2022 CMC human microbiota Cell" to find the correct DOI. The claim itself (CMC disrupts gut microbiota in humans) is well-established and EV-003's tier is not in question — only the cited DOI is wrong. |

---

### FINDING-09: DOI 10.3390/nu11081781 — Fermented Dairy Systematic Review

| Field | Value |
|-------|-------|
| **Identifier** | DOI 10.3390/nu11081781 |
| **File** | `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md` (line 627) |
| **Claimed as** | Systematic review of fermented dairy and gut health outcomes — support for EV-024 fermentation bonus |
| **Real paper** | "The Safety and Impact of a Model of Intermittent, Time-Restricted Circadian Fasting ('Ramadan Fasting') on Hidradenitis Suppurativa" (2019, Nutrients) |
| **Real URL** | https://doi.org/10.3390/nu11081781 |
| **Verdict** | MISMATCH — completely unrelated (dermatology/fasting) |
| **Owning EV** | EV-024 (fermentation is beneficial processing), study_objects block |
| **Owning agent** | Nutrition Agent |
| **Notes** | The EV-024 claim (fermentation benefits, dairy context) is well-grounded in the food science literature — the citation is simply wrong. The wrong DOI is likely a journal-number collision within Nutrients 2019. Search for "fermented dairy systematic review gut health Nutrients 2019" to locate the correct paper. |

---

### FINDING-10 (Heuristic PASS, Semantic Mismatch): PMID 28615384 — Thorning 2017

| Field | Value |
|-------|-------|
| **Identifier** | PMID 28615384 |
| **File** | `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md` (lines 2762, 3074) |
| **Claimed as** | Thorning et al. (2017), Am J Clin Nutr — cheese vs butter RCT |
| **Real paper** | "Yogurt and Diabetes: Overview of Recent Observational Studies." (2017, Journal of Nutrition) |
| **Tool verdict** | PASS (heuristic — "yogurt", "dairy" match food domain) |
| **Actual verdict** | MISMATCH — correct year, food topic, but wrong study; yogurt/diabetes vs cheese/LDL |
| **Notes** | The keyword heuristic correctly identifies the paper as nutrition-related but cannot detect within-food mismatches. This is a known heuristic limitation. The companion DOI (FINDING-07) correctly shows MISMATCH. EV-104 has no verified Thorning 2017 identifier. |

---

## UNRESOLVED-DOI Entries (Human Review Required)

| DOI | File | Claimed Source | Notes |
|-----|------|----------------|-------|
| 10.1016/S2213-8587(24)00086-X | bsip2_evidence_registry_v1.md:1636 | NutriNet-Sante cohort paper (source_doi in study_objects block) | Lancet Diabetes & Endocrinology — CrossRef may require polite-pool access; retry manually |
| 10.2903/j.efsa.2019.5625 (in compound source_doi field) | bsip2_evidence_registry_v1.md:2670 | EFSA sorbate re-evaluation | Compound source_doi field containing semicolons; parser extracted first component; manual check |
| 10.1093/ajcn/nqae052 | bsip2_evidence_registry_v1.md:2758 | Kay 2024 cheese LDL (see FINDING-04) | See FINDING-04 |

---

## Clean Citations (PASS) — Summary

40 identifiers resolved and were topic-consistent with their claimed context. These include:

- All additive-library PMIDs (PMID 38349899, 37673430, 35303088, 22889633, 9771853) — verified against NutriNet-Sante cohort papers and Ramsden/Willett meta-analyses
- All DIAAS source table PMIDs (28382889, 33133540, 39703894, 34203642, 29200310, 28573795, 36986077, 37357639, 40075933) — verified as DIAAS/protein quality papers
- All EV-003 DOIs (10.1038/nature14232, 10.1053/j.gastro.2021..., 10.1016/j.cgh.2025...) — verified as emulsifier/gut studies
- NOVA-related: DOI 10.1136/bmj.k322 (Fiolet 2018, UPF/cancer — correct)
- Additive regulatory DOIs in EV-101/102 cluster (EHJ 2026, BMJ 2025, EFSA opinions)

---

## Routing — Who Fixes What

| Finding | Action Required | Route To |
|---------|----------------|----------|
| FINDING-01: PMID 31122155 | Find correct Monteiro 2019 NOVA PMID; update all 6 registry occurrences | Nutrition Agent |
| FINDING-02: DOI 10.1017/S1368980019001307 | Find correct Monteiro 2019 NOVA DOI (companion to FINDING-01) | Nutrition Agent |
| FINDING-03: PMID 39133879 | Find correct Kay 2024 cheese LDL PMID | Nutrition Agent |
| FINDING-04: DOI 10.1093/ajcn/nqae052 | Verify if Kay 2024 study exists; find correct DOI | Nutrition Agent |
| FINDING-05: PMID 31022985 | Find correct Lordan 2019 Nutrients PMID | Nutrition Agent |
| FINDING-06: DOI 10.3390/nu11040900 | Find correct Lordan 2019 Nutrients DOI | Nutrition Agent |
| FINDING-07: DOI 10.3945/ajcn.117.158543 | Find correct Thorning 2017 cheese RCT DOI | Nutrition Agent |
| FINDING-08: DOI 10.1016/j.cell.2021.12.019 | Find correct Chassaing 2022 CMC human trial DOI | Nutrition Agent |
| FINDING-09: DOI 10.3390/nu11081781 | Find correct fermented dairy systematic review DOI | Nutrition Agent |
| FINDING-10: PMID 28615384 | Tool-PASS but semantic MISMATCH — find correct Thorning 2017 PMID | Nutrition Agent |
| 3 UNRESOLVED-DOI entries | Manual CrossRef retry; compound source_doi parse | Research Agent |

**All 10 findings route to Nutrition Agent** as the owning agent for EV-003, EV-024, EV-099, and EV-104. No score changes follow from citation correction alone — citations support claims that must be separately evaluated against the corrected sources.

---

## Validator Gate Wiring Proposal

The validator is ready to run as a standing gate. Proposed integration point:

**Two-gate / red-team wiring:** Add `python 03_operations/validators/verify_citations.py --all` as the first check in the red-team gate before any EV-### entry is marked `should_affect_score_now: true`. Any MISMATCH or FABRICATED blocks D7 co-sign until the owning agent corrects the identifier.

**CI wiring (if a CI pipeline is added):** Add as a pre-commit hook or CI step on any commit touching `evidence_registry_v1.md` or `bsip2_evidence_registry_v1.md`. Exit code 1 blocks merge.

**Command:**
```bash
python 03_operations/validators/verify_citations.py --all
# exit 0 = clean; exit 1 = MISMATCH/FABRICATED (block); exit 2 = UNRESOLVED-DOI (warn)
```

**Extend scan targets** by editing the `DEFAULT_SCAN_FILES` list at the bottom of the validator. As new evidence documents are added (supplement EV-### registry, w2_copy files, knowledge KB), add them there.

---

## Evidence Tier Note

The fabricated citations in EV-104 (Kay, Lordan, Thorning) supported the claim "hard cheese produces attenuated LDL response vs butter at matched sat_fat." This claim has biological plausibility (dairy matrix effects are documented in food science) and the authors cited as holding these findings are credible researchers in this field. However: **no verified identifier exists for any of the three claimed studies.** Until correct PMIDs/DOIs are sourced and resolve to the claimed content, the EV-104 claim tier cannot be independently validated. The underlying scientific claim may be real — the evidence is currently unverifiable at identifier level.

Evidence tier for EV-104 sat_fat attenuation claim, as of this sweep: **Insufficient** (cannot assign Moderate-Strong without verified citations; the biology is plausible but the specific citations are unverifiable).

This is a research finding, not a scoring decision. Nutrition Agent owns the tier assessment once correct citations are sourced.
