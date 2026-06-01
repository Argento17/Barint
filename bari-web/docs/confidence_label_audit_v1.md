# Confidence Label Audit v1

**Date:** 2026-05-29  
**Scope:** 18 products on `/hashvaot/snacks`  
**Reference:** CE red-team claim — products labeled `verified` should be `partial` when nutrition data is absent

---

## Label systems in play

| Layer | Field | Values | What it measures today |
|-------|-------|--------|------------------------|
| Frontend shelf | `confidence` | `verified` / `partial` / `insufficient` | Mapped from legacy `confidence_level` |
| Legacy engine | `confidence_level` | `full` / `partial` | Structural metadata completeness (NOVA, tags, ingredient count) |
| Expansion UI | `confidenceLabel` | Hebrew string | Copy from legacy label — **not** nutrition-panel completeness |
| BSIP2 trace | `confidence_band` | low/medium/high | Scoring confidence with nutrition-field reductions |

**User-visible badge:** `ProductRow` displays `confidence` via `CONFIDENCE_LABELS` in `expansion-section.tsx` (`verified` → "נתונים מלאים").

---

## Audit criterion (this pass)

A product should **not** display `verified` on the shelf when:
1. `expansion.nutrition` has all-null values, **and**
2. `expansion.ingredients` is null

This matches the consumer interpretation CE describes: "verified" implies inspectable product facts on the panel, not only structural inference.

**Exception policy:** If BSIP1 has complete nutrition but frontend not yet hydrated, recommended label is `partial` until display sync (Phase 1 recovery plan).

---

## Full product table

| Product | Current Confidence | Recommended Confidence | Reason |
|---------|-------------------|------------------------|--------|
| snk-001 — חטיף תמרים חמאת שקדים | verified | **partial** | Frontend nutrition all-null; ingredients null. BSIP1 has data but not surfaced. Structural `full` ≠ display-verified. |
| snk-002 — תמרים ציפוי קקאו | verified | **partial** | Same — 0/6 nutrition fields populated; ingredients null on shelf. |
| snk-003 — קראנצ'י שיבולת דבש | verified | **partial** | Same. BSIP0/BSIP1 complete; frontend empty. |
| snk-004 — סלים דליס שוקולד מריר | partial | **partial** | Already correct for absent frontend nutrition. |
| snk-005 — פיטנס קלאסי | verified | **partial** | Same as snk-001 pattern. |
| snk-006 — פיטנס בר גרנולה | verified | **partial** | No yohananof BSIP0; Carrefour-only BSIP1. Frontend null. Single-source → partial minimum. |
| snk-007 — פיטנס שוקולד מריר | partial | **partial** | Already correct. |
| snk-009 — NV פרוטאין בוטנים שוקולד | verified | **partial** | Frontend null despite BSIP1 196 kcal + 356-char ingredients. |
| snk-010 — NV פרוטאין קרמל מלוח | verified | **partial** | Same. |
| snk-011 — פרי מארז תמרים לוז | partial | **partial** | Already correct. |
| snk-012 — פרי מארז תמרים קקאו | partial | **partial** | Already correct. |
| snk-013 — קורני שחור לבן | verified | **partial** | Frontend null; BSIP1 has 451 kcal + long ingredient list. |
| snk-015 — תמרים חמאת בוטנים | verified | **partial** | Frontend null. |
| snk-016 — סלים טופינג לוז | partial | **partial** | Already correct. |
| snk-017 — NV צ'ואי שוקולד מריר | verified | **partial** | Frontend null. |
| snk-018 — קראנצ'י שוקולד | verified | **partial** | Frontend null. |
| snk-019 — פיטנס שיבולת דבש | verified | **partial** | Frontend null; BSIP1 complete (89 kcal). Folder alias only affects BSIP0 path. |
| snk-020 — סלים קריספי אוכמניות | partial | **partial** | Already correct; BSIP0 `partial_raw` (truncated ingredients) reinforces partial. |

---

## Summary counts

| Label | Current | Recommended |
|-------|--------:|------------:|
| verified | **12** | **0** |
| partial | 6 | **18** |
| insufficient | 0 | 0 |

---

## CE claim verification

| Claim | Verdict |
|-------|---------|
| All 18 have null nutrition on shelf | **CONFIRMED** |
| All 18 have null ingredients on shelf | **CONFIRMED** |
| 12 products labeled `verified` should be `partial` | **CONFIRMED** |
| All 18 should be `partial` until frontend hydrated | **CONFIRMED** (recommended governance) |
| Any product should be `insufficient` | **NOT RECOMMENDED** — BSIP1 canonical data exists for all 18 |

---

## Post-recovery label guidance (Phase 1, not implemented here)

After BSIP1 → frontend hydration, CE may upgrade individual products to `verified` when:

| Criterion | Threshold |
|-----------|-----------|
| Nutrition fields | ≥3 of 6 populated (energy, protein, sugar, fat, fiber, sodium) |
| Ingredients | Non-empty Hebrew string |
| Source | BSIP1 `nutrition_confidence` = `confirmed_per_100g` or equivalent |
| Quality flags | No open parse disputes (snk-001 kcal review closed) |

Products with Carrefour-only source (snk-006) should remain `partial` until cross-retailer confirmation or explicit CE single-source policy.

---

## Governance note

Misleading `verified` labels are a **transparency defect**, not evidence that BSIP2 scored without nutrition. Scoring used BSIP1; the badge reflects an outdated structural confidence mapping copied into the frontend corpus.

**Fix order:** (1) hydrate nutrition display, (2) relabel confidence, (3) optionally rescore only if BSIP1 values change.

---

## Conclusion

CE red-team is **correct** on confidence mislabeling for the 12 `verified` products. All 18 should read `partial` on the shelf until expansion fields are populated from existing BSIP1 assets.
