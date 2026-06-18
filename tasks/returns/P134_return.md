# P134 Return — TASK-278 Phase-12: Hummus × Sodium D7 Co-Sign

**Agent:** Product Agent
**Date:** 2026-06-14
**Task:** TASK-278 Phase-12

---

## Summary

EV-094 co-signed and registered. Five D7 questions resolved. One hard blocker identified:
n=60 stat re-run is required before the Data Agent can finalize implementation constants.
No engine changes. Zero score movement.

---

## Q1–Q5 Decisions

### Q1 — Dead Zone (~50–58%): ENROLL

Dead zone reflects genuine hummus category physiology — commercial hummus is formulated around a narrow sodium target (~360–400mg). The dense core receiving delta=0 is correct behavior. The differentiation at the extremes (17 products below 360mg, ~12 above 395mg) is real and the named inversions are resolvable. C6 threshold revised to ≤60% hummus-specific. Precedent: maadanim C6 revised to 55% (P132). Does not propagate to other categories.

### Q2 — Floor Threshold: PENDING n=60 re-run

n=69 Q3=395mg is 3mg above median=392mg — too thin a margin to use as a floor that caps 25% of the shelf. Floor threshold must be re-derived from n=60 distribution. If n=60 Q3 is still within 5mg of n=60 median, escalate to Nutrition Agent to select a higher percentile. Anti-immunity proof (62+3=65<70) holds regardless of exact floor_threshold value.

### Q3 — Stat Re-Run: REQUIRED — hard blocker

9 out-of-scope products (eggplant spread + matbucha) have structurally different sodium profiles. Including them in the distribution skews IQR and Q3. Phase-5 cereals precedent applies directly. Data Agent must compute n=60 stats before any constants are wired. EV-094 registered with PENDING constant fields until re-run completes.

### Q4 — HIGH_SODIUM_700MG_PLUS Stacking: SUPPRESS

SR penalty suppressed when binary cap fires (sodium_mg ≥ 700). Binary cap already prevents grade inflation for the 3 extreme products; SR stacking is redundant noise. Implement as: `if sodium_mg >= 700: skip SR`. Traced clearly in engine.

### Q5 — Scope Guard: ACCEPT with grep-verify gate

`product.get("bsip0_source", {}).get("product_category")` accepted. Nested accessor confirmed present in all 69 BSIP1 files per D6. Data Agent must grep-verify on canonical_bsip1 before wiring (expected count: 60). New constant `HUMMUS_PRODUCT_CATEGORIES = frozenset({"hummus_spread", "hummus_and_savory_dips"})` required in constants.py.

**Bonus: Q5-B (insufficient_data products):** SKIP SR. Two products with `score_basis=insufficient_data` must not have their 50-floor score modified by SR. Log sr_delta=0, sr_reason="skipped: insufficient_data".

---

## Locked Constants (distribution-independent)

| Constant | Value |
|---|---|
| P_max | 6 |
| B_max | 3 |
| floor | 62 |
| z_threshold | 0.30 |
| direction | asymmetric |
| Anti-immunity | 62+3=65<70 PASS |

## Pending Constants (require n=60 re-run)

median_mg, Q1_mg, Q3_mg, IQR, MAD, robust_scale, floor_threshold_mg

---

## EV-094

Registered at line 2345 of `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md`.
Status: `pilot_pending — BLOCKED on n=60 stat re-run`.

---

## Decision Log

| | |
|---|---|
| Options considered Q1 | (A) ENROLL with relaxed C6 ≤60%; (B) REJECT enrollment as distribution too tight |
| Chosen | A — ENROLL |
| Decisive reason | 26–34 products genuinely move; inversions are resolvable; tight core correctly receives delta=0; maadanim precedent at 47.9%/C6=55%; distribution tightness is category physiology not a mechanism flaw |
| Reversal condition | If n=60 dead_zone >60%, re-examine enrollment viability with Nutrition Agent |

| | |
|---|---|
| Options considered Q3 | (A) Accept n=69 as conservative proxy; (B) Require n=60 re-run |
| Chosen | B — require re-run |
| Decisive reason | Q3=395mg is 3mg above median on n=69 — too tight to treat as defensible floor; eggplant/matbucha sodium profiles differ from hummus; Phase-5 precedent is unambiguous |
| Reversal condition | If Data Agent confirms eggplant/matbucha sodium distribution is statistically identical to hummus (implausible given different food types), proxy is acceptable |

---

## Not Done

- n=60 stat re-run (Data Agent, next dispatch)
- Final constant lock (Product Agent, after n=60 stats received)
- Scope guard grep-verify (Data Agent)
- Engine wiring: constants.py + score_engine.py (Data Agent, after constant lock)
- Pilot run against 11-criteria gate (Data Agent)
- Pilot gate review (Product Agent)

---

```json
{
  "task_id": "TASK-278",
  "phase": "Phase-12 hummus×sodium D7 co-sign",
  "status": "RETURNED",
  "return_date": "2026-06-14",
  "agent": "product-agent",
  "artifacts": [
    {
      "path": "02_products/hummus/methodology/hummus_sodium_d7_cosign_v1.md",
      "sha256": "011d9cecc3b8594c3131c90f02b92e8c64074dc656d42363009c1e720b973dd4"
    },
    {
      "path": "03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md",
      "sha256": "d9e98ef711ccadcf295c944b4254f53e056838f01f1ed176e8c5ed932fda8efd",
      "note": "EV-094 appended after EV-093 at line 2345"
    },
    {
      "path": "tasks/returns/P134_return.md",
      "sha256": "self"
    }
  ],
  "counts": {
    "questions_resolved": 6,
    "question_denominators": "Q1/Q2/Q3/Q4/Q5/Q5-B",
    "constants_locked": 5,
    "constants_locked_denominators": "P_max/B_max/floor/z_threshold/direction",
    "constants_pending": 7,
    "constants_pending_denominators": "median_mg/Q1_mg/Q3_mg/IQR/MAD/robust_scale/floor_threshold_mg",
    "ev_registered": 1,
    "ev_registered_denominators": "EV-094",
    "pilot_gate_criteria": 11,
    "engine_files_modified": 0,
    "score_movement": 0,
    "off_sources_used": 0
  },
  "commands_run": [
    {"cmd": "Read hummus_sodium_d6_enrollment_v1.md", "exit": 0},
    {"cmd": "Read bsip2_evidence_registry_v1.md (offset 2265)", "exit": 0},
    {"cmd": "grep EV-09 evidence_registry", "exit": 0},
    {"cmd": "Read evidence_registry (offset 2340)", "exit": 0},
    {"cmd": "Read P132_return.md (maadanim gate precedent)", "exit": 0},
    {"cmd": "Edit evidence_registry — append EV-094", "exit": 0},
    {"cmd": "Write hummus_sodium_d7_cosign_v1.md", "exit": 0},
    {"cmd": "sha256sum d7_cosign + evidence_registry", "exit": 0}
  ],
  "q1_dead_zone": "ENROLL — C6 revised to ≤60% hummus-specific; tight core correctly delta=0; 26-34 movers; INV-A/INV-B resolvable",
  "q2_floor_threshold_mg": "PENDING n=60 re-run — n=69 Q3=395mg too close to n=69 median=392mg (3mg margin)",
  "q3_stat_rerun": "REQUIRED — hard blocker; Data Agent must compute n=60 stats before constants wired",
  "q4_stacking": "SUPPRESS SR when sodium_mg >= 700 (HIGH_SODIUM_700MG_PLUS already fires); sr_delta=0 for 3 extreme products",
  "q5_scope_guard_field": "product.get('bsip0_source', {}).get('product_category') — ACCEPTED; Data Agent grep-verify required before wiring; new constant HUMMUS_PRODUCT_CATEGORIES",
  "ev094_registered": true,
  "ev094_line": 2345,
  "c6_threshold_pct": 60,
  "anti_immunity_proof": "floor(62) + B_max(3) = 65 < 70 PASS",
  "engine_modified": false,
  "off_used": false,
  "not_done": [
    "n=60 stat re-run (Data Agent — immediate next dispatch)",
    "Final constant lock (Product Agent — after n=60 stats)",
    "Scope guard grep-verify (Data Agent — before wiring)",
    "constants.py HUMMUS_PRODUCT_CATEGORIES definition (Data Agent)",
    "score_engine.py SR call site (Data Agent — after constant lock)",
    "Pilot run + 11-criteria gate evaluation (Data Agent)",
    "Pilot gate review (Product Agent)"
  ],
  "acceptance_test": "EV-094 appended to evidence registry at correct position (after EV-093, before footer); D7 co-sign doc written with 5+1 decisions; locked constants confirmed distribution-independent; blocked constants correctly marked PENDING with Data Agent dispatch instruction; anti-immunity PASS proven structurally; 0 engine edits; 0 score movement",
  "propose": "RETURNED"
}
```
