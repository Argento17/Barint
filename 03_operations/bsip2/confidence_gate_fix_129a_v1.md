# P0 Confidence-Gate Fix — Validation Quality, not Presence (TASK-129A)

**Task:** TASK-129A (sub-task of TASK-129 — BSIP Calibration & Confidence, launch slice)
**Owner:** nutrition-agent
**Date:** 2026-06-01
**Origin:** `confidence_reaudit_launch_v1.md` §3 P0 #1, §6 #1
**Status:** Investigation + corrected logic delivered; **corpus fix = implementation plan (NOT auto-applied — see §6).**

---

## 1. Root cause

The display data-sufficiency gate (Launch-Definition `launch_definition_v1.md` §5) is **presence-based**:

> `verified` only when **≥3/6 nutrition fields** *and* **ingredients present**; else `partial`; null → `insufficient`.

"Ingredients present" is implemented as `bool(ingredients_text)` (or, in maadanim, an internal
`confidence_score ≥ 75` threshold) — **nothing inspects what the ingredient field actually contains.**
Any non-empty string earns `verified`, so three classes of non-ingredient text pass the gate:

| Defect class | What's in the field | Why it slipped through |
|---|---|---|
| **nutrition-bleed** | the scraped nutrition panel ("…ערכים תזונתיים 100 גרם 17.4 גרם…") | non-empty string |
| **marketing prose** | promo copy ("עשיר בחלבון המסייע ל…") | non-empty string |
| **handling/allergen tail** | "מכיל חלב עלול להכיל…" with no real list | non-empty string |

**Two compounding harms:** (a) the row is mislabelled `verified`; (b) the explanation engine then
derives *ingredient-based positive signals* from that same garbage text (NOVA / additive-free /
"high protein" claims), so a false label produces false consumer-facing claims.

The gate is also **implemented inconsistently** across build scripts — there is no single gate function:
- `02_products/maadanim/build_frontend_json.py::confidence_vm` → `confidence_score ≥ 75`
- `03_operations/bsip2/proto_v0/src/build_frontend_dataset.py` (bread) → degradation-map + `bool(ingredients_text)`
- `02_products/hummus/frontend/build_hummus_frontend_v1.py` → its own path
- the spec of record is `launch_definition_v1.md` §5

---

## 2. Demonstrated failure cases (reproduced against shipping corpora)

Reproduced live against `02_products/maadanim/maadanim_frontend_v2.json` and
`02_products/hummus/frontend/hummus_frontend_v3.json` (the snacks/milk corpora ship from the
frontend repo not checked out in this environment — see §6).

**hummus — `חומוס לבן ענק שופרסל` / `חומוס גדול שופרסל` (score 85/A, `confidence: verified`)**
Ingredient field =
`"גרגירי חומוס ערכים תזונתיים 100 גרם 17.4 גרם סיבים תזונתיים 10.7 גרם סוכרים מתוך פחמימות 339 קל אנרגיה …"`
— one real word (*chickpeas*) followed by the entire nutrition table scraped as text. The row's
`positiveSignals` then quote the bled-in numbers ("חלבון גבוה — 19.3 גרם", "סיבים — 17.4 גרם").
This is the textbook failure: presence-gate + ingredient-derived signals firing on a nutrition panel.

**maadanim — `מעדן חלבון בטעם וניל` (54/C, verified)** real list with an allergen prose tail
(`"…מכיל חלב עלול להכיל…"`); **`גמדים לשתיה תות בננה` (46/D, verified)** is also a §2.2
category-instability survivor (drinkable, routed `default`).

**snacks — `snk-001 חטיף תמרים במילוי חמאת שקדים` (70/B, verified)** — per audit §2.4, all six
nutrition fields null yet labelled `verified`. (A separate facet: verified with *no* nutrition,
not prose — the corrected gate catches it via the ≥3/6 arm.)

**milk (LEGACY, non-gating)** — audit §1 reports 2 over-labelled rows; not reproduced here (corpus absent).

---

## 3. Proposed corrected logic

New shared, pure validator — delivered and unit-tested:
`03_operations/bsip2/sprint1/ingredient_quality_gate.py` (`assess_ingredients`, `gate_confidence`).

```
verified  ⇐  (≥3/6 nutrition fields)  AND  assess_ingredients(text).is_real_list
partial   ⇐  some data present but below the verified bar
insufficient ⇐ effectively no usable data
```

`assess_ingredients` rejects (→ `is_real_list = False`): empty, **nutrition-bleed** (nutrition-panel
tokens + high digit density), **marketing prose** (narrow promo token set — deliberately excludes
common real-list words like "טרי"/fresh to avoid false positives), **long flat prose** (>200 chars,
≤3 list tokens), and **handling-only** tails.

**On a downgrade the consumer MUST also suppress ingredient-derived positive signals**
(additive-free / NOVA / sweetener / "high-protein-from-ingredients" claims) for that row, since
those were computed from non-ingredient text. This is the half of the fix that prevents false claims
surviving the relabel.

---

## 4. Affected products / impact assessment

**Calibration iteration (TASK-129A, important correction to the audit).** Three detector cuts were
run against the live corpora. A naive token set false-flagged ~80% of genuine lists; even a "narrow"
set still tripped on tokens that legitimately appear *inside* real Hebrew lists or footnotes
(`סיבים תזונתיים` = an ingredient; `ל-100 גרם` = a per-100g vitamin note; `מיחזור`/`מתכון`/`האריזה` =
packaging/Passover footnotes appended after a real list). The shipped detector therefore (a) uses
**panel-only** phrases for bleed detection and (b) **strips the trailing footnote/allergen tail and
judges the head**. Per-row results: `confidence_gate_relabel_delta_129a.md`.

| Category | Verified rows | Audit estimate | **Calibrated relabel set** | Reasons | Notes |
|---|---:|---:|---:|---|---|
| hummus | 61 | 15 | **5** | 3 nutrition_bleed + 2 empty | **score-FROZEN** (`run_hummus_002/AUTHORITATIVE.md`) |
| maadanim | 87 | 63 | **0** | — (all audit flags were footnote false-positives) | real maadanim issue is category-contamination, not prose ingredients — owned by TASK-129 finalization |
| snacks | — | 14 (+snk-001) | n/a (corpus absent here) | snk-001 caught by the ≥3/6 arm | NEAR-READY per audit §4 |
| milk | — | 2 | n/a (corpus absent, LEGACY) | — | out of launch gate (DEC-003 Amend A) |

**Headline correction:** the audit's `verified`-inflation counts (hummus 15, maadanim 63) were
**themselves inflated by the same naive-detector false-positive class** this fix removes. With a
high-precision detector the true ingredient-quality relabel set is **5 hummus rows and 0 maadanim**.
The 5 hummus rows are unambiguous: ingredient field = the word *chickpeas* + a scraped nutrition
panel (×3), or empty (×2). maadanim's genuine defects are category-routing (audit §2.1/§2.2), a
different fix.

**Score/ordering impact: none.** Per audit §2.5 there are no inversions; this changes the
`confidence` **label** (verified→partial on those 5 hummus rows) and suppresses their bled-in
positive signals. No score or grade moves.

**Score/ordering impact: none.** Per audit §2.5 there are no score inversions; this changes the
`confidence` **label** (verified→partial) and suppresses some positive-signal lines — it does **not**
move any score or grade. Downside is contained to honesty of the data-sufficiency badge.

---

## 5. Cross-checks

- Self-test green: `python 03_operations/bsip2/sprint1/ingredient_quality_gate.py` (real lists pass,
  the three defect classes fail with correct reason codes, gate transitions assert).
- The two hummus 85/A rows that drove the headline example are exactly the `nutrition_bleed` flags.

---

## 6. Implementation recommendation — **PLAN, not auto-apply**

This is **not low-risk**; do not hand-edit the corpora. Four reasons:

1. **hummus is score-frozen** (`AUTHORITATIVE.md` + `baseline_freeze_report.md`). Relabeling its rows
   alters frozen display data → requires a governed re-freeze, not an ad-hoc edit.
2. **Shipping corpora are not in this environment.** snacks_frontend_v2 / the milk comparison / the
   deployed copies live in the frontend repo (`…/src/data/comparisons`), not checked out here.
3. **No single gate to fix** — the logic is duplicated across ≥3 build scripts + the §5 spec; a correct
   fix is a shared validator + a spec amendment, spanning nutrition (build scripts) and frontend
   (deployed corpora + §5).
4. **P0, 4 categories** — blast radius warrants review at each step.

### Phased plan
- **Phase 1 — DONE:** shared, unit-tested validator `ingredient_quality_gate.py` (calibrated through
  3 cuts to zero false-positives on genuine lists); this write-up; TASK-129A registered.
- **Phase 2 — DONE:** `launch_definition_v1.md` §5 amended to require a **real ingredient list**
  (no nutrition-bleed / marketing prose / handling-only) and to suppress ingredient-derived signals
  on failure. Cites the shared validator. *(governance change; flag for frontend/Controller awareness.)*
- **Phase 2.5 — DONE:** relabel set locked via dry-run delta (`confidence_gate_relabel_delta_129a.md`):
  **5 hummus rows, 0 maadanim** — far below the audit estimate (false-positives removed).
- **Phase 3 — wire in (code, pending):** import `gate_confidence`/`assess_ingredients` into the
  `build_*.py` scripts and gate positiveSignals on `is_real_list`. For maadanim this is a **verified
  no-op** (0 deltas) — safe to land as forward protection. For hummus the build is freeze-bound (below).
- **Phase 4 — hummus re-freeze (the only real relabel, pending Controller):** the 5 rows live in the
  **frozen** `run_hummus_002`. Apply as a documented label-only patch (verified→partial on those 5,
  suppress their bled-in signals) + freeze-report note, with Controller sign-off — the audit already
  lists the hummus ingredient defect under P1, so this ships as a documented launch limitation and
  **does not block hummus GO**. **snacks/milk** corpora are not in this repo; snk-001 (null-nutrition
  verified) is handled by the ≥3/6 arm during the snacks freeze (TASK-129 follow-up); milk is LEGACY.

**Net:** scope collapsed from a feared 4-category sweep (≤94 rows) to a **5-row, hummus-only,
freeze-governed relabel** plus a forward-protective gate. Spec + validator + locked relabel set are
delivered; the only remaining action requiring approval is the hummus label-only re-freeze.
