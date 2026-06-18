# P113 — TASK-278 Phase-6: D6 Yogurt × Sugar Enrollment Proposal (route: C1 Nutrition Agent)
# Design the yogurt×sugar shelf-relative enrollment — scope guard, stats, bands, floor, inversions, EV-088

**Repo:** `C:\Bari`
**Task:** `C:\Bari\tasks\TASK-278.md` (Phase-6 rollout — yogurt×sugar)
**Reads:** `02_products/yogurt_system/bsip2_outputs/run_yogurt_006/` (authoritative yogurt corpus, ~88 products)
**Prior diagnostic:** `tasks/returns/P103_return.md` (yogurt sugar pilot: 61 movers, 8 grade changes, 0% absorption — mechanism LANDS)

---

## Context

TASK-278 Phase-5 (cereals×sugar) is CLOSED — mechanism validated on the cereal shelf. Rollout queue:
#2 yogurt×sugar (this task) → #3 cheese_spreads×sat_fat → etc.

**What you are doing:** design-only D6 enrollment proposal. No engine edits. No rescore. No score movement.
Product D7 co-signs this proposal before any pilot wiring.

**Why yogurt is the priority next candidate:**
- P103 diagnostic confirmed 61 movers / 8 grade changes / 0% absorption on yogurt shelf (bimodal: plain 0–3g vs dessert 12–20g+)
- IQR≈5.80 / robust_scale≈4.299 from pilot calibration
- Clean discrimination story: plain yogurt relief (gets lifted toward real quality) vs dessert yogurt penalty (pulled toward what it is)

**Key open question:** Yogurt routes to `dairy_protein` in router_v2.py — same category as milk, hard cheeses, cheese spreads. The SR scope for cereals used `frozenset({"biscuit", "cereal"})` — distinct router categories. Enrolling `dairy_protein` as-is would bleed SR sugar-scoring into milk, hard cheeses, etc. **You must design the scope guard** that correctly discriminates yogurt within `dairy_protein`.

---

## Step 1: Read the router to understand dairy_protein sub-typing

Read `03_operations/bsip2/proto_v0/src/router_v2.py`. Find:
- How products route to `dairy_protein`
- Whether there is any sub_type, product_type, or tag that already distinguishes yogurt from milk/cheese within `dairy_protein`
- Whether a `yogurt` sub-category already exists or could be added

Also check `03_operations/bsip2/proto_v0/src/score_engine.py` for any existing yogurt-specific branches.

Report the routing mechanism and what discriminator options are available.

---

## Step 2: Identify the authoritative yogurt corpus

Read `02_products/yogurt_system/bsip2_outputs/run_yogurt_006/run_record.json` (or whichever run is the authoritative corpus — the one with the most products, or the one closest to production).

Identify:
- n (total products)
- Which router category each product is assigned to
- Whether all n products actually route to `dairy_protein` or if some route elsewhere

If `run_yogurt_006/` has full traces, extract `sugars_g` from `bsip2_trace.json` for each product.

---

## Step 3: Compute yogurt-only sugar stats (n ≥ 20)

From the yogurt corpus (all products that route to `dairy_protein` AND are genuine yogurt products — not milk, not cheese):

Compute:
- n (yogurt-only)
- sugars_g distribution (sorted)
- Q1, median, Q3, IQR
- MAD (median absolute deviation from median)
- robust_scale = max(IQR/1.349, 1.4826×MAD, 1.4)
- Which is primary (IQR-primary per D7 co-sign)

Compare to P103 pilot calibration: median ≈ 5.3g, IQR ≈ 5.80, scale ≈ 4.299. If significant divergence (>1.0), flag.

**Guardrail:** n < 20 → do NOT propose enrollment for this category; flag to orchestrator.

---

## Step 4: Scope guard design

Design the scope discriminator for yogurt within `dairy_protein`. Options (evaluate all, recommend one):

**(A) router sub-type tag:** If router already has or can easily add a `product_sub_type == "yogurt"` discriminator, SR enrollment checks `category == "dairy_protein" AND sub_type == "yogurt"`. This requires a small router edit.

**(B) Dedicated yogurt router category:** Add `yogurt` as a distinct category in router_v2.py (alongside `dairy_protein`; products that currently route to `dairy_protein` but are yogurt → reclassify). This is the cleanest boundary but more invasive.

**(C) Explicit barcode/BSIP1 enrollment list:** Enumerate the n yogurt barcodes in a frozenset constant and gate SR on `barcode in YOGURT_SR_SUGAR_BARCODES`. Avoids router change; brittle for new products.

**(D) Name-signal discriminant:** Product name contains יוגורט / קוטג' / טעמים etc. — fragile, not recommended unless necessary.

**Recommendation:** State which option you recommend and why. If Option A or B, describe what router change is needed (1-2 lines of code, minimum footprint). The D7 co-sign will decide.

---

## Step 5: Band design and floor

Design the SR bands for yogurt × sugar, following the P>B asymmetric pattern (D7 co-sign condition 4):

- **P_max** (penalty for above-median): recommend 6 (same as cereals/biscuits) or justify a different value
- **B_max** (relief for below-median): recommend 3 (same; Anti-Immunity requires floor + B_max < 70)
- **Floor** (formulation_absolute_floor for high-sugar yogurts): must exist per D7 condition 5.
  - For yogurts: "dessert yogurt" typically 12–20g sugar. What floor prevents a 20g dessert yogurt from reaching grade A/B?
  - Anti-Immunity formula: `floor + B_max < 70` (grade B threshold). If floor=55, then 55+3=58<70 ✓ (same as biscuits, but yogurts score higher from backbone — may need floor adjustment)
  - Look at flagged yogurt backbone scores (flag-off) for high-sugar products and design the floor accordingly.
- **Threshold (g)**: above what sugar level does the floor apply? Suggest ≥ 12g (dessert territory) or justify.

State the Anti-Immunity proof explicitly: floor + B_max < 70 ✓.

---

## Step 6: Named inversions (≥2)

Identify ≥2 inversions in the current yogurt corpus that SR would fix — pairs where a lower-sugar yogurt scores below a higher-sugar yogurt today (backbone only) but should score higher once SR fires.

From run_yogurt_006 traces, find:
- Product A: lower sugar, lower current score
- Product B: higher sugar, higher current score (or close scores where SR would widen the gap correctly)
- Explain why this inversion exists (what drives the current backbone score higher for B)

Inversion pairs should be real barcodes with real sugars_g and flag-off scores (use the run_yogurt_006 traces).

---

## Step 7: EV-088 draft

Write a concise EV-088 draft (6–8 lines) for the evidence registry. Format consistent with existing EV entries in `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md`.

EV-088 covers: yogurt×sugar shelf-relative enrollment. Include: category, nutrient, scope guard design choice, stats (median/IQR/scale), bands (P_max/B_max), floor, anti-immunity proof, named inversions (barcodes), enrollment date.

---

## Step 8: Enrollment document

Write to: `02_products/yogurt_system/methodology/shelf_relative_sugar_enrollment_yogurt_v1.md`

Sections:
1. Background (why yogurt, what P103 showed)
2. Authoritative corpus (run id, n, date)
3. Scope guard (recommendation + router change needed)
4. Sugar stats (n, median, IQR, MAD, scale, formula, primary)
5. Band design (P_max, B_max, asymmetric, with formula)
6. Floor design (threshold_g, floor value, Anti-Immunity proof)
7. Named inversions (≥2, barcode + sugars_g + current score)
8. EV-088 draft
9. What D7 must decide (scope guard option, any router change, any param adjustments)

---

## Definition of Done

- [ ] Router analysis: dairy_protein sub-typing mechanism documented; 3+ scope guard options evaluated; 1 recommended
- [ ] Authoritative yogurt corpus identified: run id, n, date
- [ ] Yogurt-only sugar stats: n, median, IQR, MAD, scale, formula (IQR-primary per D7)
- [ ] Stats match P103 pilot calibration within 1.0 (or flag divergence)
- [ ] Band design: P_max, B_max, floor, threshold_g — all with Anti-Immunity proof
- [ ] ≥2 named inversions: barcode + sugars_g + current score + why inversion exists
- [ ] EV-088 draft written
- [ ] Enrollment document created at `02_products/yogurt_system/methodology/shelf_relative_sugar_enrollment_yogurt_v1.md`
- [ ] engine_invariants 342 PASS (verify after reading — confirm no engine edits occurred)
- [ ] OFF=0

---

## Constraints

- **NO engine edits** — this is design + proposal only. score_engine.py, constants.py, router_v2.py MUST NOT be modified.
- **NO rescore** — no pilot run, no batch scripts.
- **NO score movement** — 0 published movement. This is a D6 design proposal.
- **OFF ban absolute** — never use Open Food Facts for any data field.
- **Do NOT invent nutrition data** — all sugars_g values must come from BSIP0/BSIP1 scrape, not fabricated.
- **Frozen invariants**: milk run_005_headpin UNTOUCHED. Do not read or reference milk scores.

---

## Return format

Write to `C:\Bari\tasks\returns\P113_return.md`:

```json
{
  "task_id": "TASK-278",
  "phase": "Phase-6 yogurt×sugar D6 enrollment proposal",
  "status": "RETURNED",
  "return_date": "2026-06-14",
  "agent": "nutrition-agent",
  "authoritative_run": "<run_id>",
  "corpus_n_total": <n>,
  "corpus_n_yogurt_only": <n>,
  "scope_guard_recommendation": "<option A/B/C/D + one-line summary>",
  "router_change_needed": true/false,
  "router_change_description": "<one line or null>",
  "yogurt_sugar_stats": {
    "median_g": <f>,
    "IQR_g": <f>,
    "MAD_g": <f>,
    "robust_scale": <f>,
    "scale_formula": "max(IQR/1.349, 1.4826×MAD, 1.4)",
    "scale_primary": "IQR-primary or MAD-primary",
    "divergence_from_p103_pilot": "<small/flag>"
  },
  "bands": {
    "P_max": <n>,
    "B_max": <n>,
    "floor_g": <f>,
    "floor_threshold_g": <f>,
    "anti_immunity_proof": "floor(<f>) + B_max(<n>) = <sum> < 70 PASS"
  },
  "named_inversions": [
    {"barcode_a": "...", "sugars_a": <f>, "score_a": <f>, "barcode_b": "...", "sugars_b": <f>, "score_b": <f>, "why": "..."},
    ...
  ],
  "ev_number": "EV-088",
  "enrollment_doc": "02_products/yogurt_system/methodology/shelf_relative_sugar_enrollment_yogurt_v1.md",
  "engine_invariants": "342 PASS",
  "off_used": false,
  "d7_open_questions": ["scope guard option A/B/C decision", "..."],
  "not_done": []
}
```

**Do not close. Do not edit any engine files. Propose RETURNED — orchestrator reads and dispatches Product D7 next.**

Machine-readable return contract (01_framework/operations/return_contract_v1.md):

```json
{
  "artifacts_claimed": [
    {"path": "02_products/yogurt_system/methodology/shelf_relative_sugar_enrollment_yogurt_v1.md", "sha256": "<sha>"}
  ],
  "claims_verified_by_agent": false,
  "propose": "RETURNED"
}
```
