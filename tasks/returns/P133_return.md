# P133 Return — TASK-278 Phase-11: Salty Snacks × Sodium D7 Co-Sign

**Agent:** Product Agent
**Date:** 2026-06-14
**Phase:** Phase-11 salty_snacks×sodium D7 co-sign
**Status:** RETURNED

---

## Summary

Five open D7 questions resolved, anti-immunity proof verified, EV-093 registered, 11-criterion pilot gate locked. No engine edits. Zero score movement. D8 (implementation) is now unblocked for Data Agent, gated on this co-sign.

---

## Q1–Q5 Decisions

| Q | Decision | Decisive Reason | Reversal Condition |
|---|----------|----------------|-------------------|
| Q1 scope guard | ACCEPT `product.get("category") == "salty_snack"` | 54/54 coverage, no bleed, BSIP1-field pattern consistent with EV-090/091; sub-pool filter rejected | New product class with conflicting enrollment category added to corpus |
| Q2 rice-cake relief | ACCEPT B_max=3, no exclusion | Floor(62)+B_max(3)=65<70 structural protection; relief is honest and bounded | Pilot shows rice_cakes crossing grade boundary via SR alone |
| Q3 HP_FAT_SODIUM stacking | NO combined budget | Targets distinct constructs; SODIUM_FAMILY_BUDGET already caps family; stacking is correct signal | Pilot: products reach implausible floor (<30) without other supporting signals |
| Q4 P_max | 6 (not 8) | Cross-category consistency EV-087–092; sufficient for INV-B gap correction | Post-pilot: highest-Na cluster undifferentiated within 6pt ceiling |
| Q5 wiring | Standalone post-dimension pre-floor | Preserves regulatory_quality signal integrity; consistent with all prior SR phases | Data Agent D8 finds ordering conflict in standalone path |

---

## Anti-Immunity Proof

floor(62) + B_max(3) = **65 < 70 PASS**

Products at or above Q3 (630mg) sit in the surcharge zone — they receive negative delta and cannot receive B_max relief. The floor-plus-relief scenario applies only to products with very low sodium. No salty_snack product can reach B-grade (70) through SR mechanics alone.

---

## Pilot Gate — 11 Criteria (Locked)

| # | Name | Pass Condition | Fail Type |
|---|------|----------------|-----------|
| C1 | directional_distribution | Mean delta above-median ≤ 0; mean delta below-median ≥ 0 | Soft |
| C2a | grade_dist | Net A+B+C count not degraded vs run_salty_snacks_002 | Soft |
| C2b | grade_absorption | No single grade absorbs >40% of movers | Soft |
| C2c | magnitude | Mean |delta| for movers in [0.5, 6] | Soft |
| C3 | gap_narrows_inversion | INV-A: gap widens, Pringles above Bisli. INV-B: |gap_on|<|gap_off| or direction flips. Both must pass. | Soft |
| C4 | min_movers | ≥5 products with |delta| ≥ 1pt | Soft |
| C5 | min_grade_changes | ≥1 grade change at flag-on | Soft |
| C6 | max_absorption | Dead zone ≤ 40% (pre-pilot: 27.8%) | Soft |
| C7 | anti_immunity | 0 products with sodium ≥ 630mg reach grade B (≥70) at flag-on | **HARD FAIL** |
| C8 | floor_compliance | All products with sodium ≥ 630mg: flag-on score ≤ 62 | **HARD FAIL** |
| C9 | no_scope_bleed | 0 non-salty_snack products with SODIUM_SALTY_SNACK_SHELF_REL_V1 fired | **HARD FAIL** |
| C10 | frozen_byte_id_milk | CRITICAL: 20/20 milk run_005_headpin products delta=0.0 | **HARD FAIL** |
| C11 | flag_off_drift | Flag-off scores match run_salty_snacks_002 ±5pts (docs only) | Documentation |

---

## Artifacts

| Artifact | Path | Action |
|----------|------|--------|
| D7 co-sign doc | `C:\Bari\02_products\salty_snacks\methodology\salty_snacks_sodium_d7_cosign_v1.md` | Created |
| EV-093 registration | `C:\Bari\03_operations\bsip2\evidence_registry\bsip2_evidence_registry_v1.md` L2303 | Appended after EV-092 |
| Return block | `C:\Bari\tasks\returns\P133_return.md` | This file |

---

## Not Done

- D8 implementation (Data Agent, gated on this co-sign)
- Pilot run execution and gate verification (Data Agent + QA Agent)
- D9 QA baseline freeze (QA Agent)
- D10 go-live (Product Agent — separate decision, post-QA)

---

```json
{
  "task_id": "TASK-278",
  "phase": "Phase-11 salty_snacks×sodium D7 co-sign",
  "status": "RETURNED",
  "return_date": "2026-06-14",
  "agent": "product-agent",
  "scope_guard": "product.get('category') == 'salty_snack'",
  "q1_scope": "ACCEPT: category==salty_snack single BSIP1 field. Sub-pool filter rejected.",
  "q2_relief": "ACCEPT B_max=3: floor+B_max=65<70 structural; rice-cake relief is honest and bounded.",
  "q3_budget": "NO combined budget: distinct constructs; SODIUM_FAMILY_BUDGET already caps family; stacking correct.",
  "q4_p_max": "P_max=6: cross-category consistency; sufficient for INV-B gap correction.",
  "q5_wiring": "Standalone post-dimension pre-floor: preserves regulatory_quality integrity.",
  "floor_threshold_mg": 630,
  "ev093_registered": true,
  "ev093_line": 2303,
  "pilot_gate_criteria_count": 11,
  "pilot_gate_hard_fail_count": 4,
  "anti_immunity_proof": "62+3=65<70 PASS",
  "engine_modified": false,
  "score_movement": 0,
  "off_used": false,
  "artifacts": [
    {
      "path": "02_products/salty_snacks/methodology/salty_snacks_sodium_d7_cosign_v1.md",
      "sha256": "not_computed",
      "action": "created"
    },
    {
      "path": "03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md",
      "sha256": "not_computed",
      "action": "appended_ev093_at_L2303"
    },
    {
      "path": "tasks/returns/P133_return.md",
      "sha256": "not_computed",
      "action": "created"
    }
  ],
  "counts": {
    "q_resolved": "5/5",
    "pilot_gate_criteria": "11 total (4 hard fails: C7, C8, C9, C10)",
    "ev_registered": "1 (EV-093)",
    "engine_files_modified": "0",
    "score_files_modified": "0",
    "corpus_size": "54/54 salty_snack products"
  },
  "commands_run": [],
  "not_done": [
    "D8 implementation (Data Agent)",
    "Pilot run and gate verification (Data Agent + QA Agent)",
    "D9 QA baseline freeze (QA Agent)",
    "D10 go-live (Product Agent, post-QA)"
  ],
  "acceptance_test": "EV-093 appears in evidence registry at L2303 with all 5 Q-decisions recorded; D7 co-sign doc exists at salty_snacks/methodology/salty_snacks_sodium_d7_cosign_v1.md with locked 11-criterion gate; anti-immunity proof = 65<70 PASS; engine_modified=false; score_movement=0; off_used=false.",
  "propose": "RETURNED"
}
```
