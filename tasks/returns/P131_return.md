# P131 Return — TASK-278 Phase-12: Hummus × Sodium D6 Enrollment Proposal

**Task:** TASK-278
**Phase:** Phase-12 hummus×sodium D6 enrollment proposal
**Agent:** Nutrition Agent
**Return date:** 2026-06-14
**Status:** RETURNED

---

## Summary

D6 enrollment proposal for hummus × sodium completed. Stats computed from 69 BSIP1 files (100% sodium coverage). Five D7 open questions identified; Q1 (tight IQR / dead-zone absorption) and Q3 (stats should be re-run on n=60 in-scope products) are the critical items before Data Agent wiring.

Engine unmodified. Zero score movement. OFF not used.

---

## Key Findings

**Sodium shelf distribution:** The hummus corpus has a bimodal structure. A tight core of 40 products clusters at 360–395mg (IQR = 35mg), while 17 products fall substantially below 360mg (down to 6mg) and 12 products exceed 395mg (up to 864mg). This is not a uniform distribution — the IQR reflects core physiological uniformity, not a spread-y shelf.

**Robust scale = 25.945** (IQR-primary, 8.6x above the 3.0 standard guard). Scale >> 3.0 guard passes easily.

**Scope guard:** `bsip0_source.product_category in ("hummus_spread", "hummus_and_savory_dips")` — 60/69 products. Eggplant (4) and matbucha (5) excluded. Field confirmed present in all 69 BSIP1 files.

**Critical D7 flag (Q1):** With robust_scale = 25.945 and z_threshold = 0.3, the dead zone (|z| < 0.3) covers sodium between ~384mg and ~400mg, capturing ~30–35 of 60 in-scope products. Absorption may approach 50–58%. This resembles the Phase-3 "mixed signal / 59% pinned" salty_snacks characterization. D7 must rule on whether enrollment is justified at this absorption rate. My recommendation: enroll — outlier differentiation is the goal, not median-cluster differentiation.

**Q3 flag:** Current stats computed on n=69 (includes 9 out-of-scope eggplant/matbucha). Per Phase-5 cereals precedent (n=45→n=34 correction), D7 should require re-run on n=60 before Data Agent wires constants.

**Named inversions:** Both involve the 480mg "סלט חומוס" outlier (high protein, no seed oil), which currently scores A while products with 328mg sodium score B.

---

## Stats Summary

| Metric | Value |
|---|---|
| n_corpus | 69 |
| n_with_sodium | 69 |
| min | 6.0 mg |
| max | 864.0 mg |
| Q1 | 360.0 mg |
| median | 392.0 mg |
| Q3 (floor_threshold) | 395.0 mg |
| IQR | 35.0 mg |
| MAD | 12.0 mg |
| mean | 354.2 mg |
| stdev | 185.2 mg |
| IQR/1.349 | 25.945 |
| 1.4826×MAD | 17.791 |
| robust_scale | 25.945 (IQR-primary) |
| Anti-immunity | 62 + 3 = 65 < 70 PASS |

---

## Named Inversions

**INV-A: הקיסר חומוס ענק (150mg/80.4/A) vs סלט חומוס (480mg/80.2/A)**
Gap = 0.2 pts. Near-identical grades despite 3.2x sodium difference. SR widens gap by ~7 pts (both remain A, sodium becomes visible).

**INV-B: חומוס אבו גוש (328mg/69.9/B) vs סלט חומוס (480mg/80.2/A)**
True rank inversion — higher-sodium product scores 10.3 pts higher. SR narrows gap by ~7 pts (partial correction; full swap exceeds B_max+P_max = 9 pt ceiling). Gap-narrowing accepted per Phase-7 precedent.

Both inversions verified against bsip2_trace.json files in run_hummus_002.

---

## D7 Open Questions

| # | Priority | Question |
|---|---|---|
| Q1 | CRITICAL | Dead-zone absorption ~50–58%: is enrollment justified? |
| Q2 | Medium | Scope guard implementation: new constant (recommended) vs inline expression |
| Q3 | CRITICAL | Re-run stats on n=60 in-scope products only (per Phase-5 precedent) |
| Q4 | Medium | HIGH_SODIUM_700MG_PLUS cap interaction: suppress SR when binary cap fires? |
| Q5 | Low | insufficient_data products (2): apply SR or skip? (Recommendation: skip) |

---

## Artifacts

| Artifact | Path |
|---|---|
| Enrollment doc | `02_products/hummus/methodology/hummus_sodium_d6_enrollment_v1.md` |
| BSIP1 corpus | `02_products/hummus/canonical_bsip1/bsip1_*.json` (69 files) |
| BSIP2 traces | `02_products/hummus/intelligence_bsip2/run_hummus_002/products/` (69 traces) |
| This return | `tasks/returns/P131_return.md` |

---

```json
{
  "task_id": "TASK-278",
  "phase": "Phase-12 hummus×sodium D6 enrollment proposal",
  "status": "RETURNED",
  "return_date": "2026-06-14",
  "agent": "nutrition-agent",
  "artifacts": [
    {
      "path": "02_products/hummus/methodology/hummus_sodium_d6_enrollment_v1.md",
      "sha256": "pending-orchestrator-verify",
      "role": "D6 enrollment proposal"
    },
    {
      "path": "tasks/returns/P131_return.md",
      "sha256": "self",
      "role": "return block"
    }
  ],
  "counts": {
    "n_corpus": {"value": 69, "denominator": "BSIP1 files in canonical_bsip1/"},
    "n_with_sodium": {"value": 69, "denominator": "corpus products"},
    "n_in_scope_hummus": {"value": 60, "denominator": "hummus_spread + hummus_and_savory_dips product_category"},
    "n_out_of_scope": {"value": 9, "denominator": "eggplant_spread (4) + matbucha_pepper_spread (5)"},
    "n_insufficient_data": {"value": 2, "denominator": "score=50/insufficient_data in run_hummus_002"},
    "inversions_named": {"value": 2, "denominator": "D6 requirement"},
    "d7_open_questions": {"value": 5, "denominator": "Q1 CRITICAL, Q3 CRITICAL, Q2/Q4/Q5 medium/low"}
  },
  "stats": {
    "median_sodium_mg": 392.0,
    "q1_sodium_mg": 360.0,
    "q3_sodium_mg": 395.0,
    "iqr_sodium_mg": 35.0,
    "mad_sodium_mg": 12.0,
    "mean_sodium_mg": 354.2,
    "stdev_sodium_mg": 185.2,
    "robust_scale": 25.945,
    "robust_scale_primary": "IQR/1.349=25.945",
    "floor_threshold_mg": "395.0 (Q3-based, de-anchored from 600mg binary cap)"
  },
  "sr_parameters": {
    "direction": "asymmetric",
    "p_max": 6,
    "b_max": 3,
    "z_threshold": 0.3,
    "floor": 62,
    "anti_immunity_check": "62+3=65<70 PASS"
  },
  "commands_run": [
    {
      "cmd": "python3 (inline): compute sodium stats from 69 BSIP1 files",
      "exit_code": 0,
      "note": "Unicode display error on console (Hebrew product names); computation completed fully"
    },
    {
      "cmd": "python3 (inline): BSIP2 trace read for scores + inversion analysis",
      "exit_code": 0
    },
    {
      "cmd": "python3 (inline): distribution bands + z-score analysis",
      "exit_code": 0
    }
  ],
  "not_done": [
    "EV-094 registry registration (held pending D7 co-sign)",
    "Stats re-run on n=60 in-scope products (recommended as D7 binding condition — Q3)",
    "Engine wiring (Data Agent, post-D7)",
    "Pilot rescore"
  ],
  "n_corpus": 69,
  "n_with_sodium": 69,
  "median_sodium_mg": 392.0,
  "iqr_sodium_mg": 35.0,
  "robust_scale": 25.945,
  "floor_threshold_mg": "395.0 (Q3-based)",
  "ev_designated": "EV-094",
  "engine_modified": false,
  "score_movement": 0,
  "off_used": false,
  "propose": "RETURNED",
  "acceptance_test": "WOULD_PASS if: (a) enrollment doc exists at stated path, (b) no engine edits (verified, engine files not opened), (c) EV-094 not yet registered (confirmed — no EV-094 hits in registry grep), (d) both named inversions verified against run_hummus_002 bsip2_trace.json (confirmed: INV-A sodium values 150mg/480mg, INV-B 328mg/480mg, scores match traces), (e) anti-immunity 62+3=65<70 PASS, (f) floor_threshold=Q3=395mg (de-anchored from binary 600mg), (g) 5 D7 open questions documented, Q1+Q3 flagged CRITICAL, (h) OFF=0"
}
```
