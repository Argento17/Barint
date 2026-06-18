# P130 Return — TASK-278 Phase-11: Salty Snacks × Sodium D6 Enrollment

**Agent:** Nutrition Agent
**Task:** TASK-278
**Phase:** Phase-11 salty_snacks × sodium D6 enrollment
**Return date:** 2026-06-14
**Status:** RETURNED

---

## Summary

Phase-11 D6 enrollment proposal complete. Sodium shelf stats computed from 54/54 authoritative BSIP2 traces (run_salty_snacks_002). SR parameters proposed. Two named inversions identified. EV-093 designated. Methodology doc written.

---

## Deliverables

| Artifact | Path | Purpose |
|----------|------|---------|
| D6 Enrollment Proposal | `C:\Bari\02_products\salty_snacks\methodology\salty_snacks_sodium_d6_enrollment_v1.md` | Full methodology doc with stats, SR params, inversions, open questions |
| Return Block | `C:\Bari\tasks\returns\P130_return.md` | This file |

---

## Key Findings

**Corpus:** 54 salty-snack products, all carrying `category: "salty_snack"` in BSIP1 (confirmed 54/54). All 54 have sodium data — zero missing.

**Scope guard:** `product.get("category") == "salty_snack" and nn.get("sodium_mg") is not None`

**SR parameters proposed:**
- median: 560.0 mg
- IQR: 190 mg, MAD: 85.0 mg
- robust_scale: 140.85 (IQR-primary)
- P_max: 6, B_max: 3, floor: 62
- floor_threshold_mg: 630 mg (Q3, de-anchored from 600 mg binary red-label cliff)
- Anti-immunity: 62 + 3 = 65 < 70 PASS
- Scale guard: 140.85 >> 3.0 PASS

**Named inversions:**
- INV-A: Pringles Original (Na=480mg, 52.4/C) vs Bisli Spaghetti (Na=800mg, 52.9/C) — 320mg more sodium, score gap = 0.5 pts (should be ~6.8 pts under SR)
- INV-B: Bisli Spaghetti (Na=800mg, 52.9/C) vs Baked Pretzels (Na=920mg, 57.0/C) — actual score inversion: 120mg more sodium scores 4.1 pts HIGHER, driven by cap saturation at the 700mg binary cliff

**EV designated:** EV-093 (extends EV-087 through EV-092)
**Engine modified:** No
**Score movement:** 0

---

## Not Done

- EV-093 formal registration in `bsip2_evidence_registry_v1.md` — pending D7 co-sign before registration
- D7 co-sign from Product Agent — this is a D6 proposal only
- D8 implementation (Data Agent lane, post-D7)
- 5 D7 open questions require resolution: scope guard sub-pool exclusions, rice-cake relief behavior, dimension target for sodium SR, HP_FAT_SODIUM_COMBO stacking budget, P_max value confirmation

---

## Return Contract

```json
{
  "task_id": "TASK-278",
  "phase": "Phase-11 salty_snacks×sodium D6",
  "status": "RETURNED",
  "return_date": "2026-06-14",
  "agent": "nutrition-agent",
  "artifacts": [
    {
      "path": "C:\\Bari\\02_products\\salty_snacks\\methodology\\salty_snacks_sodium_d6_enrollment_v1.md",
      "sha256": "pending-orchestrator-verify",
      "purpose": "D6 enrollment proposal with sodium shelf stats, SR parameters, named inversions, EV-093"
    },
    {
      "path": "C:\\Bari\\tasks\\returns\\P130_return.md",
      "sha256": "pending-orchestrator-verify",
      "purpose": "Return block"
    }
  ],
  "counts": {
    "corpus_products_total": 54,
    "corpus_products_with_sodium": 54,
    "products_in_dead_zone": 15,
    "products_above_dead_zone": 18,
    "products_below_dead_zone": 21,
    "named_inversions": 2,
    "ev_designated": 1,
    "d7_open_questions": 5
  },
  "commands_run": [
    {
      "cmd": "python3 (sodium stats extraction from run_salty_snacks_002 traces)",
      "exit_code": 0,
      "note": "54/54 traces read, all with sodium_mg populated"
    },
    {
      "cmd": "python3 (inversion analysis, z-score computation)",
      "exit_code": 0,
      "note": "INV-A and INV-B identified from corpus data"
    }
  ],
  "key_stats": {
    "n_corpus": 54,
    "n_with_sodium": 54,
    "median_sodium_mg": 560.0,
    "q1_sodium_mg": 440,
    "q3_sodium_mg": 630,
    "iqr_sodium_mg": 190,
    "mad_sodium_mg": 85.0,
    "robust_scale": 140.85,
    "floor_threshold_mg": 630,
    "dead_zone_lo_mg": 517.7,
    "dead_zone_hi_mg": 602.3,
    "dead_zone_pct": 27.8,
    "mean_sodium_mg": 543.4,
    "stdev_sodium_mg": 192.1
  },
  "ev_designated": "EV-093",
  "engine_modified": false,
  "score_movement": 0,
  "off_used": false,
  "not_done": [
    "EV-093 formal registration in bsip2_evidence_registry_v1.md (pending D7)",
    "D7 co-sign from Product Agent",
    "D8 implementation (Data Agent, post-D7)",
    "Resolution of 5 D7 open questions"
  ],
  "acceptance_test": "Orchestrator: verify methodology doc exists at cited path, n_corpus=54, n_with_sodium=54, median=560, robust_scale=140.85, floor_threshold_mg=630, two named inversions at barcodes 7290005204001/7290009900003/7290011350002, EV-093 designated, engine_modified=false, off_used=false",
  "propose": "RETURNED"
}
```
