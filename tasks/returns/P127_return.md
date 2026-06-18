# P127 Return — TASK-278 Phase-10: Maadanim × Sugar D6 Enrollment Proposal

**Agent:** Nutrition Agent  
**Task:** TASK-278 Phase-10  
**Phase:** D6 shelf-relative sugar enrollment proposal — maadanim (מעדנים)  
**Return date:** 2026-06-14  
**Status:** RETURNED — awaiting D7 Product Agent co-sign  

---

## Summary

D6 proposal complete. Authoritative run found (`run_maadanim_001`), BSIP1 scope guard field verified (100% coverage), shelf sugar statistics computed from 146/200 trace files, SR parameters designed, inversions named, and enrollment doc written.

**Key findings:**

- Corpus: 200 products, 146 with `sugars_g` data. No OFF used.
- Scope guard: `product.get("bsip_maadanim_subtype") is not None` — confirmed in 200/200 BSIP1 files
- Router categories: `dessert` (91), `default` (48), `dairy_protein` (33), others (28) — scope guard operates on BSIP1 field, not router
- Sugar distribution: median=9.70g, IQR=11.78g, robust_scale=8.75 (LAND, not COSMETIC; scale >> 3.0)
- SR params: P_max=6, B_max=3, floor=62, z_dead=±0.30, floor_threshold_g=16.08g (Q3-based, de-anchored from 10g)
- Anti-Immunity: 62+3=65 < 70 PASS
- Named inversions: INV-A (7290110573751 vs 7290110573737, 14.6g sugar diff, same NOVA+additive); INV-B (7290110321697 vs 7290014762800, near-median compression)
- Next EV: EV-092
- 4 D7 open questions identified

**No engine edits. 0 score movement.**

---

## Artifacts

| Artifact | Path | sha256 |
|----------|------|--------|
| D6 enrollment doc | `02_products/maadanim/methodology/shelf_relative_sugar_enrollment_maadanim_v1.md` | (write-time sha not computed — verify via git status) |

---

```json
{
  "task_id": "TASK-278",
  "phase": "Phase-10 maadanim×sugar D6 enrollment proposal",
  "status": "RETURNED",
  "return_date": "2026-06-14",
  "agent": "nutrition-agent",
  "corpus_found": true,
  "n_maadanim_products": 200,
  "n_with_sugar": 146,
  "bsip1_source_dir": "C:\\Bari\\03_operations\\bsip1\\run_maadanim_001\\output\\",
  "scope_guard_field": "product.get('bsip_maadanim_subtype')",
  "scope_guard_field_verified": true,
  "scope_guard_coverage": "200/200 BSIP1 files",
  "router_category": "multiple: dessert(91), default(48), dairy_protein(33), snack_bar_granola(13), cracker(5), beverage(4), others(6) — scope guard uses BSIP1 field, not router",
  "shelf_stats": {
    "n": 146,
    "min": 0.00,
    "max": 97.12,
    "mean": 14.56,
    "stdev": 16.75,
    "q1": 4.30,
    "median": 9.70,
    "q3": 16.08,
    "iqr": 11.78,
    "mad": 5.90,
    "iqr_div_1349": 8.73,
    "1_4826_x_mad": 8.75,
    "robust_scale": 8.75,
    "scale_ge_3": true,
    "dead_zone_lo": 7.08,
    "dead_zone_hi": 12.32,
    "near_median_dead_pct": 27.4
  },
  "sr_params": {
    "direction": "asymmetric",
    "p_max": 6,
    "b_max": 3,
    "floor": 62,
    "z_dead": 0.30,
    "floor_threshold_g": 16.08
  },
  "anti_immunity_proof": "floor(62) + B_max(3) = 65 < 70 PASS",
  "recommended_scope_n": 146,
  "next_ev_number": "EV-092",
  "named_inversions": [
    "INV-A: 7290110573751 (18.0g, 28.5/E) vs 7290110573737 (3.4g, 56.3/C) — same NOVA=4, same additive_count=4; 14.6g sugar diff drives 27.8pt gap; SR adds continuous surcharge/relief on top of existing binary cap",
    "INV-B: 7290110321697 (9.8g, 56.4/C) vs 7290014762800 (12.0g, 42.9/D) — both near median, both in dead zone [7.08,12.32]; SR correctly assigns near-zero delta to both, preventing 13.5pt gap from being falsely attributed to a sugar signal that barely registers on this shelf"
  ],
  "enrollment_doc": "02_products/maadanim/methodology/shelf_relative_sugar_enrollment_maadanim_v1.md",
  "d7_open_questions": [
    "Q1: Should scope guard additionally filter to router category in ('dessert','dairy_protein','default') to exclude misbinned snack_bar_granola/cracker/beverage? Would narrow n from 146 to ~97. Product Agent decision.",
    "Q2: reduced_sugar_dessert subtype (n=5, sugar≈0-3g): these earn full B_max relief under SR AND are already capped by sweetener detection — potential double-benefit. Confirm intended behavior or add subtype exclusion.",
    "Q3: kids_dessert subtype (n=2): statistically thin. Include in scope but flag for re-evaluation when corpus expands.",
    "Q4: Dead zone 27.4% (40/146) — within 40% ceiling but higher than yogurt. Product Agent should confirm or request z_dead tightening to ±0.25."
  ],
  "commands_run": [
    {"cmd": "find C:/Bari/02_products -type d -name '*maadanim*'", "exit_code": 0},
    {"cmd": "python3 category/router analysis from batch_run_maadanim_001.py", "exit_code": 0},
    {"cmd": "python3 BSIP1 field survey (200 files)", "exit_code": 0},
    {"cmd": "python3 BSIP2 trace category distribution (200 traces)", "exit_code": 0},
    {"cmd": "python3 shelf sugar stats computation (146 products)", "exit_code": 0},
    {"cmd": "grep EV-09 evidence_registry_v1.md", "exit_code": 0}
  ],
  "not_done": [
    "D7 co-sign (Product Agent required)",
    "EV-092 registry entry (post-D7)",
    "Engine implementation (D8, Data Agent post-D7)",
    "Pilot run and gate check (D8)"
  ],
  "acceptance_test": "enrollment_doc exists at stated path AND scope_guard_field_verified=true AND robust_scale >= 3.0 AND anti_immunity 65 < 70",
  "acceptance_test_result": "PASS",
  "engine_modified": false,
  "off_used": false,
  "propose": "RETURNED"
}
```
