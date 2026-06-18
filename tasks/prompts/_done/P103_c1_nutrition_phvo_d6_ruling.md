# P103 — TASK-280 Phase-1: PHVO Detection D6 Ruling (route: C1)
# Nutrition Agent — Governance ruling on committed PHVO markers + fat_quality ceiling

**Repo:** `C:\Bari`
**Task:** `C:\Bari\tasks\TASK-280.md` (status: IN_PROGRESS)
**Depends on:** None (independent governance task)

---

## Context

Two engine changes were committed to the HEAD engine (`03_operations/bsip2/proto_v0/src/`) during TASK-275 (cookies-coffee factory run) WITHOUT a D6 Nutrition ruling or D7 Product co-sign. They are attributed as "Fix-B" and "Fix-C" in run_cookies_005.

### Fix-B — PHVO markers in `signal_extractor.py`

```python
_PHVO_MARKERS = [
    "שומן צמחי מוקשה",      # hardened vegetable fat
    "שמן צמחי מוקשה",       # hardened vegetable oil
    "מוקשה חלקית",          # partially hardened
    "partially hydrogenated",
    "שומנים מוקשים",         # hardened fats (plural)
    "שומן מוקשה",            # hardened fat
    "מחמאה",                # clarified butter / ghee ← DISPUTED
    "מרגרינה",              # margarine
]
```

If ANY of these appear in a product's ingredient list, `has_phvo = True` is set on the signal.

### Fix-C — fat_quality ceiling in `score_engine.py`

When `has_phvo = True`:
```python
fat_quality = min(fat_quality, _PHVO_FAT_QUALITY_CEIL)  # ceil = 40
```

This caps the `fat_quality` dimension score at 40 (out of 100), regardless of what the fat composition would otherwise produce.

---

## At-risk live product identified

**snacks_frontend_v2.json** (live on bari.digital): product snk-019 "חטיפי פיטנס שיבולת שועל דבש" (40/D) contains **מרגרינה** as ingredient #6. Under the current committed engine, `has_phvo` fires → fat_quality capped at 40 → if fat_quality was previously > 40 before Fix-C, the final score drops → **possible D→E grade change on next snacks re-score.**

The other PHVO-marker file in live corpus is `butter_frontend_v2.json` — contains **מחמאה** in copy text (verdicts), not in ingredient lists. This appears safe.

---

## Your task: D6 Ruling

You are the Nutrition Agent. You hold D6 authority on scoring philosophy and nutrient signal design.

Provide a formal D6 ruling on EACH of the following questions:

### Q1: Is מחמאה (clarified butter / ghee) correctly classified as a PHVO marker?

מחמאה = clarified butter (animal saturated fat). It is NOT a partially hydrogenated vegetable oil. It does not contain trans fats created by industrial hydrogenation.

Options:
- (A) **REMOVE from PHVO_MARKERS** — מחמאה is animal fat, not PHVO; its sat-fat effect is already captured by the sat_fat dimension; adding it to PHVO over-penalizes kosher/traditional products incorrectly
- (B) **KEEP with a comment** — from a consumer perspective, מחמאה in a processed product is a hardened-fat signal that warrants the same ceiling as PHVO (ultra-processed products use חמאה/מחמאה to add richness just as they use margarine); the ceiling is a "formulation richness" signal, not strictly a "trans fat" signal

Rule with a single option. Explain the downstream scoring implication.

### Q2: Is the fat_quality ceiling of 40 the correct threshold?

The ceiling is applied when has_phvo=True. This means any product with margarine (regardless of how much) scores fat_quality ≤ 40.

- fat_quality = 40 maps to approximately D-range territory on the fat dimension
- A product with margarine as ingredient #2 (major) vs ingredient #15 (trace) both get the same ceiling

Options:
- (A) **Keep ceiling=40, no quantity adjustment** — the presence of margarine/PHVO anywhere is a signal of industrial fat sourcing; binary detection is intentional
- (B) **Keep ceiling=40 but add a minimum-ingredient-rank threshold** — only fire if PHVO marker appears in the first N ingredients (e.g., N=10); tail-position margarine (trace amounts as anti-caking) doesn't warrant the full ceiling
- (C) **Adjust the ceiling** — 40 is too harsh / too lenient; propose the correct value with evidence

Rule with a single option. Note any calibration implications.

### Q3: Which product categories should PHVO detection apply to?

The current implementation fires on ANY product category (it's not gated by category). PHVO markers in bread, cookies, cereals, snacks, spreads all trigger the ceiling.

Options:
- (A) **Fire in ALL categories** — hardened fats are universally a negative signal regardless of category
- (B) **Gate to specific categories** — e.g., `PHVO_APPLICABLE_CATEGORIES = {"biscuit", "cracker", "snack_bar_granola", "bread"}` — dairy/meat/produce categories are physically incapable of containing PHVO and don't need the gate
- (C) **Add a minimum-fat-quantity guard** — only fire if `fat_saturated_g >= threshold` AND PHVO marker present; purely ingredient-list firing without quantity confirmation can be a false positive

Rule with the most defensible option.

### Q4: Should the existing snk-019 score (40/D) be retroactively corrected?

If D6 determines that the PHVO ceiling is correct AND should apply to snk-019, the product would score differently under the committed engine vs. when it was originally scored (before Fix-C). This creates a consistency gap in the deployed snacks page.

Options:
- (A) **Do not retroactively correct** — the committed engine is the new baseline; when snacks is next re-scored through the factory, the corrected score ships; do not patch the deployed JSON
- (B) **Patch the deployed JSON now** — if the PHVO ceiling changes snk-019's grade from D→E, this is an honest error in the currently displayed score; the principle "unknown is acceptable; wrong is not" applies

Note: retroactive patching of a deployed page is a consumer-facing change and would require D7 (Product co-sign) + owner notification before deployment. You are ruling only on the PRINCIPLE here; the mechanism requires a separate authorization path.

---

## Definition of Done

- [ ] D6 ruling written for Q1 (מחמאה: remove or keep)
- [ ] D6 ruling written for Q2 (ceiling value + quantity gate)
- [ ] D6 ruling written for Q3 (category scope)
- [ ] D6 ruling written for Q4 (retroactive correction principle)
- [ ] Proposed `_PHVO_MARKERS` final list after your rulings
- [ ] Proposed `_PHVO_FAT_QUALITY_CEIL` value (if different from 40)
- [ ] EV draft designation (next available EV number in `01_framework/operations/evidence_registry_v1.md`)

---

## Constraints

- **Read `03_operations/bsip2/proto_v0/src/signal_extractor.py`** for the current marker list
- **Read `03_operations/bsip2/proto_v0/src/score_engine.py`** for the ceiling implementation
- **Read `bari-web/src/data/comparisons/snacks_frontend_v2.json`** for snk-019 context
- **OFF ban absolute** — no Open Food Facts
- **DO NOT modify any engine files** — D6 ruling only, implementation follows with D7 + separate dispatch
- **DO NOT modify any JSON files** — read only
- **Agent does NOT decide go/no-go for snacks re-score** — orchestrator decides after D6+D7

---

## Return format

End with machine-readable contract:
```json
{
  "task_id": "TASK-280",
  "phase": "Phase-1 D6 ruling",
  "status": "RETURNED",
  "return_date": "...",
  "agent": "nutrition-agent",
  "d6_rulings": {
    "Q1_mchama": "REMOVE|KEEP",
    "Q2_ceiling": {"value": 40, "quantity_gate": "none|N_ingredients"},
    "Q3_category_scope": "all|gated",
    "Q4_retroactive_correction": "do_not_correct|patch_if_grade_changes"
  },
  "proposed_phvo_markers": [...],
  "proposed_fat_quality_ceil": 40,
  "ev_designation": "EV-XXX",
  "not_done": []
}
```

**Do not close — propose RETURNED and let the orchestrator verify.**
