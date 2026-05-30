# Snack Nutrition Recovery Plan v1

**Date:** 2026-05-29  
**Status:** Plan only — no implementation in this audit pass  
**Constraint:** No scoring redesign, no score changes, no explanation changes in Phase 1

---

## Questions answered

| Question | Answer |
|----------|--------|
| Can nutrition and ingredient data be restored **without rescoring**? | **Yes** — hydrate `snacks_frontend_v2.json` expansion fields from BSIP1 |
| Can it be restored **automatically**? | **Yes** — deterministic barcode → BSIP1 field mapping |
| Can it be restored from **existing assets**? | **Yes** — BSIP1 is complete for 18/18; BSIP0 is provenance fallback |

---

## Important distinction

Current scores were **already computed with BSIP1 nutrition and ingredients** in BSIP2 (`L1_observed_signals`). Restoring data to the frontend corpus is a **display and transparency fix**, not a scoring fix.

Re-running BSIP2 after recovery is **optional Phase 2** and would only be needed if:
- Parse errors are corrected (e.g. snk-001 kcal basis)
- CE approves score recalibration

---

## Phase 1 — Frontend hydration (no rescoring)

### Goal

Populate `expansion.nutrition` and `expansion.ingredients` in `snacks_frontend_v2.json` from BSIP1 without touching `score`, `grade`, or editorial copy fields.

### Source mapping

| BSIP1 field | Frontend field |
|-------------|----------------|
| `normalized_nutrition_per_100g.energy_kcal` | `expansion.nutrition.energyKcal` |
| `normalized_nutrition_per_100g.protein_g` | `expansion.nutrition.protein` |
| `normalized_nutrition_per_100g.sugars_g` | `expansion.nutrition.sugar` |
| `normalized_nutrition_per_100g.fat_g` | `expansion.nutrition.fat` |
| `normalized_nutrition_per_100g.dietary_fiber_g` | `expansion.nutrition.fiber` |
| `normalized_nutrition_per_100g.sodium_mg` | `expansion.nutrition.sodium` |
| `ingredients_text_he` | `expansion.ingredients` |
| `nutrition_basis_claimed` or `"ל-100 גרם"` | `expansion.servingNote` (already set) |

Null BSIP1 fields → leave frontend field `null` (partial panel — same as Maadanim).

### Product ↔ barcode map

Use verified map from `scripts/sync-snacks-corpus-images.mjs` (18 IDs).

### Implementation sketch

```text
scripts/sync-snacks-corpus-nutrition.mjs
  ├── read snacks_frontend_v2.json
  ├── for each product id → barcode
  ├── read bsip1_{barcode}.json from C:\Bari\...\canonical_bsip1\run_001\
  ├── map nutrition + ingredients
  ├── write JSON (pretty)
  └── log: populated / partial / flagged
```

### QA gates

1. `npm run lint && npm run build`
2. `/hashvaot/snacks` — expansion panel shows nutrition grid for products with values
3. `ExpansionSection` ingredient list visible where string non-empty
4. No score/grade/insightLine/bottomLine diff in git
5. snk-001 flagged in `_meta` or sidecar for CE kcal review — do not block other 17

### Confidence label follow-up (separate CE task)

After hydration, CE should decide whether `confidence: "verified"` is appropriate per product based on **displayed** nutrition completeness — see `confidence_label_audit_v1.md`.

---

## Phase 2 — Data quality fixes (optional, CE-gated)

| Product | Issue | Action |
|---------|-------|--------|
| snk-001 | 92 kcal/100g implausible | Re-read label photo / HTML; confirm per-serving vs per-100g; update BSIP1 if wrong |
| snk-020 | Truncated BSIP0 ingredients | Prefer full BSIP1 string; optionally re-parse HTML |
| snk-019 | Folder barcode alias | Document alias; no data change needed if BSIP1 correct |

Any BSIP1 correction → **requires BSIP2 re-run and CE score review** before shelf score update.

---

## Phase 3 — Rescoring (out of scope unless CE approves)

CE advisory estimate: ~30–40% of products may shift ±8 points when nutritional layer recalibrated after parse fixes.

**Not required** for Phase 1 display recovery because BSIP2 already consumed BSIP1 values.

Trigger rescoring only if:
- BSIP1 nutrition values change materially
- Category-specific cap policy changes (separate CE initiative)

---

## What not to do

| Action | Reason |
|--------|--------|
| Re-run `build-snacks-frontend-v2.ts` | Deprecated; overwrites CE v2 corpus with null nutrition template |
| Invent nutrition from editorial copy | Violates CE data integrity rule |
| Change scores in same PR as hydration | Conflates display fix with scoring revision |
| Re-scrape Yohananof | Unnecessary for 18-product cohort |

---

## Effort estimate

| Phase | Effort | Risk |
|-------|--------|------|
| Phase 1 script + 18-product sync | ~2–4 hours | Low |
| Phase 1 QA | ~1 hour | Low |
| Phase 2 snk-001 kcal review | CE + 2–4 hours | Medium |
| Phase 3 rescoring | CE sprint | High |

---

## Success criteria

- [ ] 17+ products show non-null nutrition in expansion panel
- [ ] 18 products show ingredient strings
- [ ] Scores unchanged from current CE v2 corpus
- [ ] Audit script confirms `fe_nut_populated > 0` for hydrated products
- [ ] Confidence labels reviewed per CE governance (separate change)

---

## Conclusion

Recovery is **straightforward, automatic, and non-scoring**. The blocking item was never missing scrape data — it was the CE v2 decision to ship editorial expansion without BSIP1 field mapping. Phase 1 closes the user-visible gap; Phase 2 addresses one suspected parse error before any score reconsideration.
