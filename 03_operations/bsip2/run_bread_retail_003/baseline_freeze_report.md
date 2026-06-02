# Bread (לחם) BSIP2 — Baseline Freeze Report

**Run:** real_bread_retail_003_v1
**Task:** TASK-129C
**Owner:** Nutrition Agent
**Date:** 2026-06-01
**Status:** FROZEN — Authoritative launch corpus
**Controller decision:** 2026-06-01 — `bread_retail_003` is authoritative (TASK-129-A confidence re-audit §3 P0 #4, §7)
**Corpus:** Shufersal representative bread shelf (25–26 May 2026)
**Trace path:** `C:\Bari\02_products\bread_retail_003\bsip2\` (256 slim BSIP2 export traces)
**Scored corpus:** `C:\Bari\02_products\bread_retail_003\lechem_frontend_v2.json` (81, Bread Calibration Patch v1 applied)
**Displayed corpus:** `C:\Bari\bari-web\src\data\comparisons\bread_frontend_v2.json` (24, `source_run_id: real_bread_retail_003_v1`)
**Authoritative marker:** `C:\Bari\02_products\bread_retail_003\bsip2\AUTHORITATIVE.md`
**BSIP2 version:** retail export + Bread Calibration Patch v1 (no score tuning, no logic changes in this freeze)

This freeze **versions the numbers under an already-frozen framing** ("best ≠ excellent"). No score, grade, framing, or routing logic is changed by TASK-129C. The displayed 24 are frozen exactly as currently shipped.

---

## Section 1 — Provenance Chain

| Stage | Count | Source |
|-------|-------|--------|
| Scraped (representative shelf) | 256 | `bread_retail_003/bsip2/bsip2_shufersal_*.json` |
| Scored / coherent | 81 | `lechem_frontend_v2.json` |
| Displayed (curated launch shelf) | 24 | `bread_frontend_v2.json` |

Per the CLAUDE.md frozen invariant: 256 scanned → 81 scored → 31 curated (24 scored display rows + 7 transparency rows). This freeze covers the **24 scored display rows**. The 7 transparency rows are not scored and are out of scope.

---

## Section 2 — Frozen Score Distribution (24 displayed rows)

| Statistic | Value |
|-----------|-------|
| Products displayed | 24 |
| Confidence | 24 `partial` (0 `verified`) |
| Mean score | **72.0** |
| Median score | **72.5** |
| Minimum | 59 |
| Maximum | 82 |

### Grade distribution

| Grade | Count | Products |
|-------|-------|----------|
| A | **3** | לחם ירוק מקמח מלא (80), לחם טחינה פרוס (82), קרקר כוסמין מלא ושומשום (82) |
| B | **18** | — |
| C | **3** | לחם מחמצת שיפון+אגוזים (61), לחם מחמצת אגוזים צימוקים (60), קרקר קרם קרקר (59) |
| D | 0 | — |
| E | 0 | — |

Distribution is consistent with the bread framing: the shelf clusters in the B band (18/24, 75%); the top is **80–82/A — good, not excellent** (the "best ≠ excellent" invariant holds — no bread reaches the high-A band the framing reserves). No D/E because the curated display set excludes the commodity-floor and ultra-processed tail (the wider 81-product scored corpus spans 40–82, mean 54.0).

### Cluster composition (display shelf order preserved)

| Cluster | Count |
|---------|-------|
| everyday | 4 |
| strong | 5 |
| fermentation | 5 |
| wellness_ambig | 5 |
| crackers | 5 |

---

## Section 3 — Confidence State

All 24 displayed rows are **`partial`**. This is the disclosed, accepted launch state, not a defect:

- Nutrition panels carry **protein / fiber / sodium**; `energyKcal`, `sugar`, `fat` are `null` across all 24 (retail export captured a partial panel).
- Only **9 of 24** rows carry a real ingredient list (`ingredients` populated); 15 are `ingredients: null`.
- The UI discloses this as `נתונים חלקיים`. The partial-confidence shelf is acceptable for launch per TASK-129-A §7 and the launch-definition §5 confidence gate.

Root re-scrape (full ingredient lists + kcal/sugar/fat) folds into a future `run_bread_retail_004`.

---

## Section 4 — Known Limitations (carried into display)

### KL-1 — Partial nutrition panels — does not block display
`energyKcal`/`sugar`/`fat` null for all 24. Scores rest on structural base + fiber + sodium + fermentation signals. Do not surface kcal/sugar/fat dimension breakdowns as actionable data.

### KL-2 — Ingredient list coverage 9/24 — disclosed
15 rows have no ingredient list. Fermentation and base-grain reads for those rows are inferred from product name + nutrition, at `partial` confidence. Disclosed in-UI and in per-row `limitingFactors`.

### KL-3 — Fiber-source nuance (shufersal_7290016245325, לחם טחינה פרוס, 82/A)
The 18.5g fiber comes from tahini, not the grain matrix. Insight line already discloses ("הסיבים כאן מגיעים מהטחינה"). `limitingFactors` reinforces. Do not present its fiber as whole-grain evidence.

### KL-4 — Fermentation claim vs. ingredient gap
Several "מחמצת"-named rows show industrial yeast where an ingredient list exists (e.g. shufersal_4685027, shufersal_2079217, shufersal_6451507). Per-row `limitingFactors` discloses the marketing-vs-data gap. This is the bread category's endemic distortion and is handled by disclosure, not score penalty.

### KL-5 — Crispbread/cracker base ambiguity
Two Swedish-style crackers (shufersal_7296073134459, _134442) read `בסיס קמח מזוקק` (refined-flour base) under a "whole/rye" presentation. `limitingFactors` notes the base ambiguity.

---

## Section 5 — limitingFactors Authoring (Deliverable 4)

Per-product `limitingFactors` content authored for all 24 displayed rows. Content is grounded strictly in the frozen data (no invented values). Field **rendering** is TASK-128's frontend field-completeness work — this freeze authors the **content only** and stages it at:

`C:\Bari\02_products\bread_retail_003\limiting_factors_v1.json`

Coverage: **24 / 24 non-empty.** No consumer-facing use of the terms NOVA / BSIP / cap / floor / structural_class.

---

## Section 6 — Supersession

The synthesis run `02_products/bread_light/bsip2_outputs/run_synthesis_calibration_001` (32 synthetic products, full traces) is **NON-AUTHORITATIVE / EXPERIMENTAL**. Marker written at:
`C:\Bari\02_products\bread_light\bsip2_outputs\run_synthesis_calibration_001\NON_AUTHORITATIVE.md`

It must never be consumed by the frontend pipeline or treated as a launch source. The authoritative launch source is `real_bread_retail_003_v1` only.

---

## Section 7 — Rollback Plan (governance requirement)

| Field | Value |
|-------|-------|
| Previous state | Shipping corpus `bread_frontend_v2.json` had no authority marker; bread BLOCKED in launch gate |
| This change | Declares `bread_retail_003/bsip2` authoritative; relabels `bread_light` synthesis as experimental; freezes 24 displayed scores; authors `limitingFactors` content |
| Scores changed | **None** — label/freeze/documentation only |
| Restore | Delete `AUTHORITATIVE.md`, `NON_AUTHORITATIVE.md`, this freeze report, and `limiting_factors_v1.json`. No score, JSON product data, or routing logic is touched, so rollback is non-destructive. |
| Notify on rollback | Central Controller, Product Agent |

---

## Section 8 — Frozen Baseline Summary

| Field | Value |
|-------|-------|
| Run ID | real_bread_retail_003_v1 |
| Corpus | Shufersal representative bread shelf (25–26 May 2026) |
| Scraped / scored / displayed | 256 / 81 / 24 |
| Confidence (displayed) | 24 partial, 0 verified |
| Grade A / B / C / D / E | 3 / 18 / 3 / 0 / 0 |
| Mean / median displayed score | 72.0 / 72.5 |
| Min / max displayed | 59 / 82 |
| Authoritative marker | `02_products/bread_retail_003/bsip2/AUTHORITATIVE.md` |
| Non-authoritative run | `bread_light/.../run_synthesis_calibration_001` — `NON_AUTHORITATIVE.md` |
| limitingFactors coverage | 24 / 24 non-empty (`limiting_factors_v1.json`) |
| Next run (post re-scrape) | run_bread_retail_004 (not scheduled) |

---

*Baseline Freeze Report — TASK-129C — Nutrition Agent — 2026-06-01*
*real_bread_retail_003_v1 is frozen. Framing unchanged; numbers versioned. Future re-runs must increment the run ID.*
