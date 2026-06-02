# BSIP2 Recalibration — P0 Design Spec (TASK-169A)

> **⚠ v1.1 REVISION (2026-06-02) supersedes R7 and R4 below.** After the Data Agent's
> blast-radius model (`02_products/_recal_p0_model/TASK-169A_blast_radius_model_v1.md`)
> showed the stack overshoots — dairy mass-produces S grades and the live-culture +8 leaked
> onto plain fluid milk (85/A breach) — the owner ruled (binding, 2026-06-02): **keep the
> live-culture bonus but gate it to genuinely cultured products only; no hard grade cap.**
> The authoritative R7 gate and the R4 flavored-variant fix are now in the **§ v1.1
> REVISION** at the end of this document. R1, R2, R3, R5, R6 are unchanged (model confirmed
> well-behaved). Where R7/R4 below conflict with v1.1, **v1.1 wins.**

**Status:** DESIGN ONLY. No engine edit, no shipped score. Data Agent implements in a modeling harness (P1) behind an env flag after owner approval.
**Engine target:** BSIP2 proto_v0 0.4.1 — `03_operations/bsip2/proto_v0/src/score_engine.py` + `constants.py`.
**Authored by:** Nutrition Agent. Co-signer for D7 approval: Product Agent. Frozen-category moves: owner sign-off (P2).
**Rollback:** all changes gated by a single new env flag `BARI_RECAL_P0` (precedent: `BARI_TASK144_FIXES`). Flag unset → engine behaves exactly as 0.4.1. Document previous-state per change (done inline below).

All numbers below are grounded in the live traces `run_cheese_003` (n=59 scored), `run_hummus_002` (n=69 scored). Verified protein distributions: **cheese** min/Q1/median/Q3/max = 0 / 4.4 / 7.9 / 10.0 / 23.0 g; **hummus/sauce_spread** = 0 / 2.0 / 7.7 / 8.3 / 22.0 g. Worked anchors: cottage 1% = 11.5g protein / 1g fat / 0.6g sat / 62 kcal → live 74.9/B; white+garlic = 9g protein → live 76.9/B; the inversion that triggered the sprint.

---

## R1 — Category-relative protein scale

**Problem (verified).** A single supplement-calibrated breakpoint table `[(0,0),(3,15),(6,30),(10,50),(15,70),(20,85),(25,95)]` is used in BOTH `score_nutrient_density` (line ~192) and `score_protein_quality` (line ~446). It is calibrated so 20–25g (whey-isolate territory) reaches the top. Whole-food protein ceilings sit far lower: dairy tops ~11.5g, hummus ~8g. On this curve, a category-leading 11.5g cottage scores only 56, and the within-shelf spread between mediocre (9g→45) and best (11.5g→56) is just 11 points — no differentiation. The protein dimensions are 25% of the composite (nutrient_density 15% + protein_quality 10%), so this single mis-calibration compresses the whole shelf.

**Fix.** Replace the single hard-coded breakpoint list with a **per-category protein breakpoint table**, looked up exactly like `CALORIE_DENSITY_TABLES`. The map yields a 0–100 *mass* score; `score_protein_quality` then applies the existing source/matrix factors (`source_factors`, `PROTEIN_QUALITY_MATRIX_DISCOUNT`) on top, unchanged. The curve is anchored so that **the real top-of-shelf protein for the category reaches ~95 and the shelf median lands near 55–60** — i.e. protein is scored *relative to what is achievable in that food*, not against an absolute supplement ceiling.

```python
# NEW in constants.py — gated by BARI_RECAL_P0
# breakpoints: list of (protein_g_ceiling, score); first ceiling where g <= ceiling wins,
# linear-interpolated between adjacent breakpoints (same interpolation as today).
PROTEIN_SCALE_TABLES = {
    # dairy_protein / cheese — shelf 0..23g, median 7.9, Q3 10. Whole-food dairy
    # protein is complete & high-DIAAS; a lean 11–12g cottage is the category apex.
    "dairy_protein": [(0,0),(3,20),(5,35),(7,50),(9,65),(11,85),(13,95),(99,100)],
    # sauce_spread (hummus) — shelf 0..22g, median 7.7, Q3 8.3. Classic hummus ~7–8g
    # is "good"; 12g+ (extra-tahini / high-legume) is the apex; veg-only spreads sit low.
    "sauce_spread": [(0,0),(2,12),(4,28),(6,45),(8,62),(11,82),(14,95),(99,100)],
    # --- FROZEN categories (modelled here; require P2 owner sign-off before shipping) ---
    # milk — fluid dairy ~3–3.5g protein is normal; >6g is high-protein UHT/filtered.
    "milk_dairy": [(0,0),(2,30),(3,55),(4,70),(6,88),(8,95),(99,100)],
    # yogurt — plain 3–5g, Greek/skyr 8–10g is the apex.
    "yogurt": [(0,0),(2,20),(3.5,40),(5,58),(7,75),(9,90),(11,95),(99,100)],
    # bread — protein is a secondary virtue; 8–12g (high-protein/seeded) is good,
    # 4–6g (white) mediocre. Kept conservative so bread isn't rewarded as a protein food.
    "bread": [(0,0),(4,30),(6,45),(8,60),(10,72),(13,85),(99,95)],
    # snack_bar_granola — KEEP the current supplement curve: bars genuinely compete on
    # 15–25g reconstructed protein and the F2 matrix discount already governs gaming.
    "snack_bar_granola": [(0,0),(3,15),(6,30),(10,50),(15,70),(20,85),(25,95),(99,95)],
    # default — unchanged supplement curve, so untouched categories are byte-identical.
    "default": [(0,0),(3,15),(6,30),(10,50),(15,70),(20,85),(25,95),(99,95)],
}
```

**Rationale for the breakpoints (per category).**
- *dairy_protein/cheese:* "mediocre" = below the Q1 (~4–5g) → ≤35; "good" = median–Q3 (7–10g) → 50–65; "top" = the lean high-protein apex (11g+) → 85–95. This makes a lean 11.5g cottage the protein leader of its shelf, which is the owner's stated target.
- *sauce_spread:* classic hummus (7–8g) is solidly "good" (~62), not penalised as if it should hit 20g; the rare 12g+ legume-dense / extra-tahini items become the apex; veg-only spreads (1–2g) still score low on *protein* but are rescued by R6, not by inflating this curve.
- *frozen:* curves chosen so each frozen category's real shelf leaders land ~88–95 without re-ranking within-category (to be confirmed by the P1 before/after diff; any re-rank is a P2 owner decision).

**Worked numbers (mass score, before source/matrix factor):**

| product | protein | OLD curve | NEW curve | source factor | NEW protein_quality |
|---|---|---|---|---|---|
| cottage 1% | 11.5g | 56.0 | 90.0 (interp 11→13: 85 + 0.25×10) | dairy ×1.0 | **90.0** |
| white cheese | 9.0g | 45.0 | 65.0 | dairy ×1.0 | **65.0** |
| hummus (classic) | 7.0g | 35.0 | 53.5 (interp 6→8) | mixed ×0.85 | **45.5** |
| hummus (legume-dense) | 22.0g | 95→89 (×0.94 after factor) | 100 | mixed ×0.85 | **85.0** |

The same NEW `PROTEIN_SCALE_TABLES` value feeds the protein term of `nutrient_density` (R2 handles the fiber blend). For cottage that raises the nutrient_density protein component from 56 → 90 *before* the fiber re-normalization.

**Evidence registry.** **NEW: EV-029 — category-relative protein scale.** Signal: protein mass scored against the achievable per-category distribution rather than an absolute supplement ceiling. Source: `run_cheese_003` (n=59) + `run_hummus_002` (n=69) measured protein distributions, 2026-06-02. Tier: **Moderate** (distribution is real and observed; the apex anchors are a judgement call — see open questions). Cross-category → frozen categories need P2 owner sign-off.

---

## R2 — Fiber-blend fix (fiber "absent ≠ zero" for dairy)

**Confirmed mechanism.** `score_nutrient_density` blends `0.65×protein + 0.35×fiber`. EV-027 already implements a protein-only re-normalization (65/35 → 100/0) when `category ∈ FIBER_NOT_APPLICABLE_CATEGORIES` AND fiber is genuinely absent/≤0. It is correct and tightly gated. It is currently gated behind `TASK144_FIXES_ON` (`BARI_TASK144_FIXES=on`, maadanim-only in practice) and the allowlist is `("dessert","dairy_protein","yogurt")`. Cheese is routed under the **`dairy_protein`** category key (verified: cottage trace `category` resolves into the dairy_protein calorie table family), so the mechanism *would* fire for cheese — it is simply not active because the flag is off in the cheese runs.

**Fix.** No new code. Two changes:
1. Bind the EV-027 path to the new `BARI_RECAL_P0` flag (OR it with the existing `TASK144_FIXES_ON` so maadanim behavior is unchanged): `fiber_not_applicable = (TASK144_FIXES_ON or RECAL_P0_ON) and category in FIBER_NOT_APPLICABLE_CATEGORIES and (fiber_raw is None or fiber_raw <= 0)`.
2. Confirm membership. `dairy_protein` is already on the allowlist → cheese/cottage/white-cheese inherit it. **Do NOT add `sauce_spread`** — hummus is chickpea-based and fiber IS expected and IS a genuine virtue there (the hummus fiber blend is correct; veg spreads are handled by R6). No category is added beyond what's already listed; we are only *activating* the existing allowlist for the cheese run.

**Dairy/cheese inclusion criterion (the rule that justifies it):** a category joins `FIBER_NOT_APPLICABLE_CATEGORIES` only if **near-zero fiber is the structurally correct, expected value for the whole category** (a fiber-free animal/dairy matrix). Bread/cereal/bars/crackers/sauces/spreads/beverages stay excluded because missing fiber there is a real deficiency.

**Worked number.** Cottage 1%: OLD nutrient_density = 0.65×56 + 0.35×0 = 36.4. With R1+R2: protein mass 90 → protein-only (fiber N/A) = **90.0**. (No fortification on plain cottage, so no ×0.80.)

**Evidence registry.** **Extends EV-027 (TASK-144).** Same signal/source; the only change is activation scope (cheese run via the new flag) and the lineage note that `dairy_protein` already covers cheese. Tier: **Strong** (parallels the owner-approved whole-food-fat-floor principle).

---

## R3 — Leanness reward in fat_quality

**Problem (verified).** `_score_fat_quality_sprint1` (and the v1 `score_fat_quality`) return a flat **neutral 50** when `fat < 0.5g` OR `sat_fat is None`, and otherwise compute a penalty-only curve (`100 - sat_f×3 - sat_frac×25`). A genuinely lean product never scores *above* what its low sat-fat passively earns, and a near-zero-fat product with a missing/None sat-fat field is stranded at 50. There is no positive leanness signal. (Note: cottage 1% already lands at 83.2 via the v1 path because it *has* sat_fat=0.6g; the neutral-50 trap bites the <0.5g-fat and missing-sat-fat cases — e.g. fat-free dairy and the veg spreads.)

**Fix.** Replace the two neutral-50 short-circuits with an explicit **leanness credit** for genuinely lean foods, while keeping the existing penalty curve for fatty foods. A food is "lean" when `fat ≤ 3g/100g`. Within lean, reward lower fat AND require low sat-fat (don't reward a 2g-fat product that is 100% saturated):

```python
# applies when fat < 0.5  OR  (fat <= 3.0 and sat_fat is not None)
# leanness_base on total fat, then a small sat-fat haircut; floor at the old neutral 50
def _leanness_score(fat, sat_f):
    sat = sat_f or 0.0
    base = 92 - fat * 6.0          # 0g→92, 1g→86, 2g→80, 3g→74
    base -= sat * 4.0              # mild: 0.6g sat → -2.4
    return round(max(50.0, min(95.0, base)), 1)
```
- `fat < 0.5g` and `sat_fat is None` (the old stranded case): treat sat as 0 → score 92 (a fat-free dairy/veg product is genuinely lean, not "neutral").
- `fat < 0.5g` with sat present: same formula, sat haircut applies.
- `0.5 ≤ fat ≤ 3g`: leanness credit replaces the *lower* of (penalty-curve value, leanness value)? **No** — to avoid double-crediting, take `max(penalty_curve, leanness_score)` only in the lean band so a lean product is never *worse* than the penalty curve and gains a modest positive floor. Above 3g fat the behavior is byte-identical to today (penalty curve only).

**Worked numbers.**
- cottage 1% (fat 1g, sat 0.6g): leanness = 92 − 6 − 2.4 = 83.6; penalty-curve (current) = 83.2 → `max` = **83.6** (≈ unchanged, intended — cottage was already fine here).
- fat-free white cheese (fat 0.3g, sat None): OLD neutral 50 → NEW **92** (the real fix — lean product credited).
- matbucha (fat ~2g olive-oil-based, sat ~0.3g): leanness = 92 − 12 − 1.2 = **78.8** vs whatever penalty-curve gave (helps R6 too).

**Evidence registry.** **NEW: EV-030 — leanness reward.** Signal: a genuinely lean whole-food matrix (low total fat AND low saturated fat) earns positive fat_quality credit rather than a neutral default. Source: cottage/white-cheese/veg-spread traces, `run_cheese_003`/`run_hummus_002`, 2026-06-02. Tier: **Moderate**. This modifies the existing dimension functions; no shadow rule.

---

## R4 — NOVA proxy refinement (cultured/fortified plain dairy stays NOVA 2)

**Problem (verified).** NOVA-3 classification carries a triple cost: processing_quality 65, whole_food_integrity 60, and a processing cap of 87 (`NOVA_PROXY_3_PROCESSED`), plus the false consumer line "מבנה רכיבים מעובד". Cottage was NOVA **2** in run_001 and regressed to NOVA **3** in run_003 (verified: run_003 cottage trace `nova_proxy=3`). The hummus shelf is 59/69 at NOVA 3. The proxy is over-counting benign dairy additions (salt, cultures, added calcium) as "processing."

**Fix.** Add a NOVA-2 retention criterion in the proxy: a product stays at **NOVA 2 (not 3)** when ALL of —
- `product_type_dairy == True`, AND
- it is **plain** (no flavor/sweetener/added-sugar signals: `added_sugar_sources_count == 0`, `sweetener_detected == False`), AND
- every non-base ingredient beyond the dairy base is on a **culinary/culturing allowlist** only: `{salt/מלח, dairy cultures/תרבית/חיידקי מחמצת, rennet/מיתוש, added calcium/סידן, vitamin fortification}`, AND
- additive_marker_count from genuine ultra-processing markers (thickeners, gums, emulsifiers, stabilizers, colors, flavors) == 0.

If a thickener/gum/stabilizer/emulsifier/flavor/color IS present (the marker of a genuinely processed spread — e.g. a cream cheese with carob gum + flavor), the product **stays NOVA 3**. This is the discriminator that keeps cultured/fortified plain dairy at 2 without letting engineered spreads escape. Implement as a guard in the NOVA proxy that *demotes a tentative 3 back to 2* only when the allowlist test passes; never promotes a 4.

This also retires the false "מבנה רכיבים מעובד" line for products that pass the test (R4 is the upstream fix; the L8 fallback at `build_cheese_signals.py:166` should be reached only for genuine NOVA-3 — Content/Frontend handle the line text in P3).

**Evidence registry.** **Extends EV-024 / EV-026 lineage** (the plain-dairy / culture-credit family from the yogurt run, where cultures were detected-but-not-credited). Signal: benign culinary/culturing/fortification additions to a plain dairy base do not constitute culinary→industrial processing (NOVA-2-consistent). Source: cottage NOVA 2→3 regression run_001 vs run_003; hummus NOVA dist 3:59/1:6/2:4. Tier: **Moderate**. Label observability: relies on ingredient-list coverage + `product_type_dairy` + additive markers — confirm coverage in P1 (some scanned panels are sparse).

---

## R5 — Red-label sat-fat cap → graded penalty

**Problem (verified).** `ISRAELI_RED_LABEL_1_SAT_FAT` is a hard cap → 55 in `FAT_QUALITY_CAPS`. It is a cliff: a 1.6g sat-fat difference flips a 16-point swing, and once it fires it flattens everything above it — a 10.5g-protein cottage 9% (52/C) ends up == a 4.3g-protein / 25g-fat napoleon (52/C). The 23g-protein parmesan-type scores 42/D for the same reason (cap crushes a high-protein food). The cliff destroys protein differentiation precisely where it matters.

**Fix.** Convert the cap to a **graded penalty on the fat_quality dimension** (not a composite cap), scaled to how far over the 5.0g/100g red-label threshold the product sits. Remove `ISRAELI_RED_LABEL_1_SAT_FAT` from `FAT_QUALITY_CAPS`; add a penalty in `FAT_QUALITY_PENALTIES`:

```python
# graded: 0 at threshold, growing with excess sat-fat, capped so it can't exceed the
# old cliff's worst effect. Excess = sat_fat - 5.0 (g/100g).
def _red_satfat_penalty(sat_f):
    if sat_f is None or sat_f <= 5.0:
        return 0
    excess = sat_f - 5.0
    return round(min(25.0, 3.0 + excess * 2.5), 1)   # 5g→0, 6g→5.5, 8g→10.5, 12g→20.5, cap 25
```
This lands on the fat_quality dimension *before* the family budget (`FAT_QUALITY_FAMILY_BUDGET=8` still clamps the coordinated total), so it degrades gracefully and never flattens protein. A 16% sat-fat napoleon still drops hard (penalty ~25, fat_quality near floor), but a 5.5g-sat cottage 9% takes only a small hit and keeps its protein lead.

**Worked numbers (fat_quality dimension, illustrative).**
- cottage 9% (sat ~5.5g): OLD → composite capped at 55 (cliff). NEW → fat_quality penalty 4.25; cottage 9% protein (54→~85 under R1) flows through → expect high-C/low-B, *above* the napoleon. ✔ resolves the R5 collapse.
- napoleon 16% (sat ~10g): NEW penalty 15.5 → fat_quality stays low; correctly remains below cottage.

**Evidence registry.** **NEW: EV-031 — graded saturated-fat penalty.** Signal: saturated fat above the Israeli red-label threshold degrades fat quality proportionally rather than via a single composite cliff. Source: cottage-9% vs napoleon-16% inversion `run_cheese_003`, 2026-06-02. Israeli MoH red-label sat-fat threshold = 5.0g/100g (existing `RED_LABEL_THRESHOLDS`). Tier: **Moderate**. NOTE: `regulatory_quality` STILL counts the red label (1 label → 60), so the regulatory signal is not lost — we only remove the *fat-dimension cliff*. Label observability: reads `red_labels`/sat_fat — already covered.

---

## R6 — Vegetable-spread category fit

**Problem (verified).** Veg spreads (matbucha / roasted-pepper / eggplant, 1–2g protein) are scored on the same 25%-protein-weighted rubric as legume/dairy protein foods → protein_quality 5–10 and nutrient_density 4–18 drag ~25% of the score, bottoming them at **42.8–61.8** despite clean ingredients, low additives, and good calorie density (75–90). A whole-vegetable spread is being punished for not being a protein food.

**Fix.** Introduce a **`veg_spread` archetype** within `sauce_spread` (detected at routing: legume protein < 3g AND base is whole vegetable — tomato/pepper/eggplant/onion — AND no tahini-dominant signal; reuse the existing raw-vs-prepared boundary logic, see memory `feedback_raw_vs_prepared_boundary`). For this archetype, **re-weight** so the score reflects what a veg spread *should* be judged on:

```python
# NEW in constants.py — applied only to the veg_spread archetype, gated by BARI_RECAL_P0
VEG_SPREAD_WEIGHTS = {
    "processing_quality":   0.15,
    "nutrient_density":     0.08,   # ↓ from 0.15 (protein-dominated; less relevant)
    "calorie_density":      0.18,   # ↑ a light whole-veg spread should be rewarded
    "glycemic_quality":     0.12,
    "protein_quality":      0.03,   # ↓ from 0.10 (not a protein food)
    "additive_quality":     0.16,   # ↑ clean ingredient list is the core virtue
    "satiety_support":      0.06,
    "fat_quality":          0.08,
    "regulatory_quality":   0.08,   # ↑ sodium discipline matters for a brined/salted spread
    "whole_food_integrity": 0.06,   # ↑ whole-veg base rewarded
}   # sums to 1.0
```
Judged on: clean ingredients (additive_quality 16%), whole-veg base (WFI + processing), low calorie density (18%), and sodium discipline (regulatory 8%). Protein is nearly removed. This is a **re-weighting, not a new dimension** (no scope expansion). A clean matbucha (additives 0, kcal low, whole-tomato base) should land mid-B; a sodium-bomb pepper spread stays C/D via regulatory + sodium cap.

**Evidence registry.** **NEW: EV-032 — vegetable-spread category fit.** Signal: a whole-vegetable spread is judged on ingredient cleanliness, whole-food base, low energy density, and sodium discipline — not protein density. Source: matbucha/pepper-spread traces 42.8–61.8/D-C, `run_hummus_002`, 2026-06-02. Tier: **Moderate**. Anti-immunity guard (per `bari_usecase_guardrails_v2`): the re-weight must NOT let an engineered/sodium-heavy spread reach A — verify in P1 that no `veg_spread` crosses 80 without clean additives + sub-threshold sodium.

---

## R7 — Ranking-inversion run-down (for Data Agent; hypothesis only)

**Do not solve — instrument and report.** Verified anomaly: white+garlic cheese reports `weighted_dimension_score = final = 76.9`, but the weighted sum recomputed from its own published dimension_scores = **68.9** (using the canonical `DIMENSION_WEIGHTS`). That is **+8.0 unexplained**, and `fermentation_bonus_applied` in the trace is `None`. Cottage 1% has no such gap (published 74.92 = recomputed 74.92).

**Hypothesis (high confidence):** the +8.0 is `FERMENTATION_DIRECT_BONUS` (`constants.py`, value 8, applied pre-cap to NOVA1–3 when `has_fermentation`). White cheese fires a fermentation signal (cultured cheese) and gets +8; cottage's culture is detected-but-not-credited (the same EV-024 detected-not-credited gap seen in yogurt run_003). Two things to run to ground in P1:
1. Confirm the +8 source: re-run white+garlic with a trace that captures `fermentation_bonus_applied`/`fermentation_bonus_note`. If the field is populated on re-run, the run_003 trace simply wasn't writing it (trace-completeness bug, not a scoring bug).
2. Decide consistency: either cottage's culture should *also* earn the fermentation credit (raising cottage, preserving correct ranking), OR the +8 fermentation bonus is too coarse for cultured dairy where culturing is table-stakes and should be down-weighted within dairy. **Nutrition recommendation:** prefer crediting cottage's culture (option 1 alignment) so the lean high-protein product wins, consistent with R1's intent. This is an open question for owner/Product (below).

No evidence-registry change for R7 yet — it is a diagnostic, not a rule. If option-2 (down-weight fermentation within dairy) is chosen, that becomes a new EV entry in P1.

---

## Cross-cutting governance

- **Activation scope:** every change is CROSS-CATEGORY (owner-approved per TASK-169). Frozen categories (milk run_004, bread retail_003, snack bars snk-001, yogurt) are modelled here but **require per-move owner sign-off in P2** before any frozen score ships. R1 deliberately keeps `snack_bar_granola` on the existing supplement curve, so the snack-bar ceiling (snk-001 = 70/B) is *not* moved by R1; R2–R5 may still nudge frozen scores — P1 diff will quantify.
- **Rollback:** single new flag `BARI_RECAL_P0` (default off). Unset → 0.4.1 behavior byte-identical. Document each previous state (done inline: R1 old curve, R2 flag binding, R3 neutral-50, R4 NOVA-3 path, R5 cap, R6 uniform weights).
- **Rule-accumulation discipline:** R1 replaces a hard-coded list with a table (no new rule); R2 activates an existing path (no new rule); R3/R5 modify existing dimension/penalty functions; R6 is a re-weight of existing dimensions; R4 refines an existing classifier. **No shadow rules added.** R5 removes one cap and adds one penalty (net-neutral rule count).
- **Label observability:** R4 (ingredient allowlist + dairy flag) and R5 (sat-fat red label) — confirm coverage in P1; sparse scanned panels may leave R4's allowlist test indeterminate (then default to NOVA 3, the safe/conservative outcome).
- **Evidence registry summary:** NEW — EV-029 (R1 protein scale), EV-030 (R3 leanness), EV-031 (R5 graded sat-fat), EV-032 (R6 veg-spread fit). EXTENDS — EV-027 (R2), EV-024/026 (R4). All need their registry entries written before P1 merges.

---

## (a) Key judgement calls — owner may want to weigh in

1. **Protein apex anchors (R1).** I set dairy 11g→85 / 13g→95 so a lean 11.5g cottage reaches ~90/protein-quality (owner's stated ~90/A target). This is a calibration *choice*, not a measured fact — the shelf shows 11.5g is near the top but the exact apex point is a values call. If the owner wants cottage at a clean 90/A composite, the dairy curve and R2/R4/R5 must combine to land there; P1's worked composite will confirm and may need a 1–2 point nudge.
2. **Crediting cottage's culture vs down-weighting fermentation within dairy (R7).** Both fix the inversion. Crediting culture (my recommendation) raises lean dairy; down-weighting fermentation lowers cultured cheese. Different philosophies about whether culturing is a virtue or table-stakes in dairy. **Owner/Product call.**
3. **Veg-spread re-weighting vs dedicated rubric (R6).** I chose a re-weight (smaller blast radius, no new dimension). A fully dedicated rubric would be cleaner but is more scope. Also: where exactly is the `veg_spread` detection boundary (some products are tahini+veg blends)? Reuse of the raw-vs-prepared boundary is proposed but needs a P1 false-positive audit.
4. **Frozen blast radius (R2–R5).** R2 (dairy fiber) and R5 (sat-fat) will move milk and yogurt scores. The owner froze milk top = 85/A; R1+R2 could push a high-protein milk above that. P1 must surface every frozen delta for explicit P2 sign-off — flagging now that "no frozen score moves without owner approval."
5. **R3 leanness ceiling (95) and `fat ≤ 3g` band edge.** The 3g cutoff and 95 ceiling are judgement calls; a cheese at 3.1g fat sees no leanness credit (small discontinuity at the band edge). Acceptable, but worth an owner eye if smoothness matters.

## (b) Readiness statement

This P0 design is ready for owner review and, on approval, for Data Agent to implement in a modeling harness behind `BARI_RECAL_P0` — pending Product Agent co-sign (D7) and explicit P2 owner sign-off for every frozen-category delta the P1 diff surfaces.

---

# § v1.1 REVISION (2026-06-02) — R7 culture gate + R4 flavored-variant fix

**Trigger.** The blast-radius model proved all fix *directions* correct but the combined
*magnitude* too hot. Two precise, owner-blessed corrections. R1, R2, R3, R5, R6 stand as
written above (model: well-behaved). This revision **replaces R7 §179–187 and amends R4
§109–123**.

**Owner decisions (binding):**
1. Keep the live-culture +8, but gate it to GENUINELY cultured/fermented products only —
   never plain fluid milk.
2. No hard grade cap. Frozen dairy ceilings (milk/yogurt) may rise; the owner approves
   specific products once the re-tuned numbers are in front of them. Only the *unintended*
   leakage is removed.

---

## R7 v1.1 — gate the live-culture bonus to genuinely cultured dairy

### Grounding the cottage-culture question in the trace (resolves my earlier note)

My v1 R7 note said "prefer crediting cottage's culture." Having read the engine, that note
was **wrong about the mechanism** and I am correcting it. The facts from the code:

- `has_fermentation` is set in `signal_extractor.py:800–801` by pure substring matching of
  `FERMENTATION_MARKERS_HE` (תרבית / תרבויות / מחמצת / לקטובציל / ביפידוס / חומצה לקטית …)
  against the ingredient text. **It is purely label-derived.**
- Plain cottage's L1 `ingredient_list` is **חלב / מלח** (milk + salt) with
  `has_fermentation = false`. **No culture word is declared in its panel.** So cottage's
  culture is **NOT detectable** in the trace — it is not declared.
- The v1-as-implemented R7 (`score_engine.py:1140–1154`) fires *because* `has_fermentation`
  is false: it grants +8 to **any** product that is `product_type_dairy` + plain + NOVA≤3,
  "even when the culture word is absent." That is an *assumption* ("plain dairy ⇒ cultured"),
  not a detected signal.
- **`product_type_dairy` cannot separate fluid milk from cottage/cheese/yogurt** — it is set
  (`signal_extractor.py:730–732`) when any of `{חלב, יוגורט, גבינת, מי גבינה, קזאין}` appears
  in the first three ingredients. Plain fluid milk's first ingredient is **חלב**, so it
  matches → R7 fires on fluid milk → the 85/A breach. The model's root-cause is exactly this.

**Conclusion: the "plain-dairy ⇒ cultured" assumption is unsound.** It conflates an
*uncultured* food (fluid milk; plain cottage as labelled) with genuinely cultured foods
(yogurt, labaneh, cultured/aged cheese). The bonus must key off **either a declared culture
marker OR membership in a known-cultured product type**, not off "plain dairy."

### The R7 v1.1 gate (authoritative)

Grant the +8 `FERMENTATION_DIRECT_BONUS` when **EITHER** path qualifies, and the product is
NOVA≤3:

**Path A — declared culture (existing, keep):** `has_fermentation == True`
(any `FERMENTATION_MARKERS_HE` hit: תרבית / תרבויות / תרבויות חיות / מחמצת / לקטובציל /
ביפידוס / אצידופילוס / חומצה לקטית / fermented / lactobacillus). This is the genuine,
label-observable signal and is unchanged from HEAD.

**Path B — known-cultured product TYPE (new, replaces the v1 "plain dairy" assumption):**
the product routes to a category/subtype whose food identity is *inherently* cultured, so
absence of the culture word is a sparse-panel artifact rather than evidence of no culture.
Qualifying types ONLY:
- `category == "yogurt"` OR `cat_result.category_subtype == "yogurt"` (yogurt is cultured by
  definition), AND
- within `dairy_protein` (cheese family): a **cultured-cheese subtype** — cottage / white
  cheese / labaneh / quark / sour-cream-style / aged or ripened cheese. Detect via the
  cheese-family product-name / subtype markers
  `{קוטג', קוטג, גבינה לבנה, לבנה, לבנייה, גבינת שמנת, קממבר, גאודה, מוצרלה, פרמזן, רוקפור,
  שמנת חמוצה, קוואַרק}` (reuse / extend the existing cheese routing subtype, not a new
  classifier).

**EXPLICIT EXCLUSIONS (never get the bonus via Path B):**
- `category == "milk_dairy"` (plain/flavored **fluid milk**, drinking milk, UHT, filtered/
  high-protein milk) — fluid milk is NOT a cultured product. **Hard exclude.**
- Plant drinks (soy/rice/oat/almond "משקה") — not dairy, not cultured.
- Cream / butter / sweet (uncultured) cream products with no declared culture.
- Any product that fails Path A AND is not in the Path-B cultured-type allowlist.

Implementation shape (replaces `score_engine.py:1138–1148`):
```python
# R7 v1.1 — bonus only for GENUINELY cultured dairy
eligible_ferm = has_fermentation                      # Path A: declared culture (unchanged)
r7_culture_credit = False
if RECAL_P0_ON and not has_fermentation and nova_level <= 3:
    subtype = cat_result.get("category_subtype")
    is_yogurt        = (category == "yogurt" or subtype == "yogurt")
    is_cultured_chz  = (category == "dairy_protein"
                        and subtype in CULTURED_CHEESE_SUBTYPES)   # NEW allowlist constant
    is_fluid_milk    = (category == "milk_dairy")                  # HARD EXCLUDE
    if (is_yogurt or is_cultured_chz) and not is_fluid_milk:
        eligible_ferm = True
        r7_culture_credit = True
# … then the existing `if eligible_ferm and nova_level <= 3:` +8 block, unchanged
```
The v1 `product_type_dairy + plain` test is **removed** from the bonus path (it was the
leak). `product_type_dairy` stays where it belongs — R4's NOVA demotion and the EV-028
dairy-source factor — untouched.

### The plain-cottage ruling (the key call)

**Recommendation: plain cottage does NOT receive the live-culture bonus via Path A, but DOES
qualify via Path B as a cultured-cheese subtype.** Read carefully — this needs a sub-ruling,
because Path B as written *would* re-admit cottage:

- **Cottage as a food IS cultured** (lactic-acid bacteria are intrinsic to cottage-cheese
  manufacture). So on pure food science, Path B (known-cultured type) defensibly includes it.
- **BUT the model is explicit:** R1+R2+R4 alone land cottage 1% at **≈89.76 ≈ the owner's
  90/A target.** Adding the +8 pushes cottage 1% to **~97.8/S**. The owner's stated target is
  **90/A, not S.**

Therefore my ruling, reconciling food science with the owner's numeric target:

> **Plain cottage (and plain white cheese) — EXCLUDE from the R7 bonus in P0.** Define
> `CULTURED_CHEESE_SUBTYPES` to cover the genuinely-cultured *cheese* identities that are NOT
> already at their target without the bonus, and **deliberately exclude the
> cottage / white-cheese (`גבינה לבנה`) fresh-cheese subtypes** from Path B. Net effect:
> plain cottage 1% lands at **~89.76 → 90/A** (owner target hit almost exactly, no further
> tuning), instead of ~97.8/S.

**Why this is the right call, not a fudge:**
1. The owner gave a specific number (90/A) for the flagship cottage. A rule that overshoots
   the owner's own stated target by 7+ points and a whole grade tier is mis-calibrated by
   definition — the bonus is double-counting culturing that R1's category-relative protein
   curve already rewards (cottage's apex protein is *why* it hits ~90).
2. Within fresh dairy, **culturing is table-stakes** (this is the v1 R7 "option 2"
   intuition, now made precise): every cottage and white cheese is cultured, so a flat +8
   does not *differentiate* — it just inflates the whole fresh-cheese shelf uniformly. A
   differentiator that fires on the entire shelf is not a differentiator.
3. For yogurt and aged/specialty cultured cheeses, culturing genuinely varies in
   prominence and *is* a label-observable virtue (live/probiotic claims) — Path A already
   credits those, and Path B credits yogurt-type identity. So the bonus does real work
   exactly where culturing is a differentiating signal, and is silent where it is table-stakes.

**Cottage's culture is therefore credited NOT via the fermentation bonus but via R1
(category-relative protein) + R2 (fiber-N/A) + R4 (NOVA-2 retention).** That is the correct
home for "this is a clean, lean, high-protein cultured food" — it lifts cottage to its 90/A
apex without the coarse +8.

**Resulting cottage score under v1.1: ~89.76 → 90/A** (R1+R2+R4 only; R7 excluded). This is
the owner's target, hit without a hard cap.

> **Owner/Product call (flagged, not mine to settle):** whether to *include* the
> cottage/white-cheese fresh subtypes in Path B and let cottage reach ~97/S. The owner stated
> 90/A as the target, so my recommendation is EXCLUDE; if the owner wants the fresh-cheese
> shelf to reach S, flip these two subtypes into the allowlist and re-model. Either is a
> values call about where the fresh-dairy ceiling sits — the *mechanism* (Path A + Path B,
> milk hard-excluded) is sound regardless.

### What R7 v1.1 fixes vs the model
- **Fluid milk (`חלב נטול לקטוז … 2%`, `חלב … מהדרין`): bonus removed.** Both milk products'
  +8 vanishes. `חלב נטול לקטוז 2%` 87.3 → ~79 (no longer crosses 85/A from R7; any residual
  A-crossing is now from R1 milk_dairy curve alone and is a clean P2 owner decision, not
  leakage). The `מהדרין 1%` 69.8 → ~62. **The frozen 85/A milk-ceiling leakage is closed.**
- **Yogurt: bonus retained (legitimate).** Yogurt is cultured; Path B keeps the +8. The
  yogurt A/S spread is now a genuine, owner-reviewable distribution — not leakage. (Trim via
  the `yogurt` protein-apex anchors in R1 if the owner wants fewer S's; that's a separate
  P1 calibration knob, not an R7 defect.)
- **Cottage / white cheese: bonus removed → lands at the 90/A target** (above).

---

## R4 v1.1 — flavored / seasoned-variant exclusion from NOVA-3→2 demotion

**The hole (verified in `nova_proxy.py:166–169`).** The `is_plain` test is
`added_sugar_ct == 0 and not has_sweetener and not has_flavor_enhancer and not has_color`.
Garlic, dill, onion, herbs, jalapeño etc. are **whole-food ingredients**, NOT
`flavor_enhancer` additive markers (`has_flavor_enhancer` keys off חומרי טעם וריח / MSG-type
markers). So a **napoleon שום שמיר (garlic + dill, 16% fat)** passes `is_plain = True`, gets
demoted NOVA 3→2, and rides R1/R2 to A. A seasoned 16%-fat cheese reaching A is wrong: the
NOVA-2 retention was designed for *plain* cultured/fortified dairy, and a flavored variant is
no longer plain.

**Fix.** Add a **seasoning/flavor-variant marker test** to the `is_plain` gate so any
declared flavoring ingredient — even a whole-food one — disqualifies the demotion. The
product **stays NOVA 3** if a seasoning marker appears in the product name OR ingredient list.

```python
# NEW in constants.py — gated by BARI_RECAL_P0
# Whole-food / culinary flavorings that are NOT additive markers but DO make a dairy
# product a "flavored variant" — disqualifies the R4 plain-dairy NOVA-2 retention.
FLAVORED_VARIANT_MARKERS_HE = [
    "שום", "שמיר", "בצל", "בצלים", "עירית", "פטרוזיליה", "כוסברה", "בזיליקום",
    "נענע", "תבלין", "תבלינים", "עשבי תיבול", "זעתר", "פפריקה", "צ'ילי", "חריף",
    "חלפיניו", "ג'לפינו", "פלפל", "עגבני", "עגבניות מיובשות", "זית", "זיתים",
    "פטריות", "ירקות", "בטעם",            # "בטעם X" = "X-flavored"
    "תות", "וניל", "אגוז", "דבש", "קינמון",   # sweet flavor variants too
]
```
In `nova_proxy.py`, extend the plain test:
```python
name = (product.get("canonical_name_he") or product.get("product_name_he") or "")
hay  = (name + " " + " ".join(ingredients)).lower()
has_flavor_variant = any(m in hay for m in FLAVORED_VARIANT_MARKERS_HE)
is_plain = (added_sugar_ct == 0 and not has_sweetener
            and not has_flavor_enhancer and not has_color
            and not has_flavor_variant)        # NEW clause
```

**Scope / safety:** this only ever *blocks* a demotion (keeps a tentative NOVA 3 at 3); it
never promotes and never demotes anything new — so it can only *lower* scores relative to the
v1 model, never raise. Plain cottage (חלב/מלח) and plain white cheese contain none of these
markers → still demote to NOVA 2 as intended. Napoleon שום שמיר → `has_flavor_variant=True`
→ stays NOVA 3 → does not reach A. **The flavored-variant A leak is closed.**

> **Note for Data Agent on the R7↔R4 interaction:** the same seasoning markers should also
> make a product *non-plain* for any place R7 Path B touches fresh cheese — but since v1.1
> R7 excludes cottage/white-cheese subtypes from Path B entirely, a flavored cottage is
> already excluded from the bonus. Keep the two tests independent (R4 in `nova_proxy.py`, R7
> in `score_engine.py`); do not share state.

---

## v1.1 evidence-registry & rollback framing

- **EV-024/026 lineage (R4 + R7) — REVISED, still under `BARI_RECAL_P0`.** The signal is
  refined from "benign additions to a plain dairy base ⇒ NOVA-2 / cultured" to two precise,
  label-grounded claims:
  - *R4:* benign **culinary/culturing/fortification** additions to a plain dairy base keep
    NOVA 2 — **but a declared flavoring (even whole-food: garlic/dill/herbs/etc.) makes it a
    flavored variant and forfeits the retention.** Label observability: name + ingredient
    substring match; Tier **Moderate**.
  - *R7:* the live-culture +8 fires only on **(A) a declared culture marker, OR (B) an
    inherently-cultured product TYPE (yogurt; specified cultured-cheese subtypes)** — and is
    **hard-excluded for fluid milk (`milk_dairy`)** and plant drinks. The earlier
    "plain-dairy ⇒ cultured" assumption is **retracted as unsound** (it credited uncultured
    fluid milk and over-credited table-stakes fresh-cheese culturing). Tier **Moderate**;
    label observability: Path A is fully label-observable, Path B is product-type-derived and
    must be confirmed against the router subtype coverage in P1.
- **No new rule, no shadow rule.** R7 v1.1 *narrows* an existing bonus path (fewer products
  qualify than v1); R4 v1.1 *adds one disqualifier clause* to an existing demotion guard
  (only ever blocks). Net rule count unchanged; blast radius strictly *smaller* than the v1
  model. New constant `CULTURED_CHEESE_SUBTYPES` is a routing allowlist, not a scoring rule;
  `FLAVORED_VARIANT_MARKERS_HE` is a marker list feeding an existing test.
- **Rollback unchanged:** still the single `BARI_RECAL_P0` flag (default OFF → 0.4.1
  byte-identical). Previous state to document inline: R7 v1 path (`product_type_dairy + plain`
  ⇒ +8) and R4 v1 `is_plain` (additive-marker-only). Flag-OFF safety contract (59/59
  byte-identical) is unaffected — both changes are inside the existing `RECAL_P0_ON` guards.

---

## v1.1 precise change-list for the Data Agent (implement directly)

1. **`score_engine.py` ~L1138–1148 (R7 block):** replace the `is_plain_dairy_cult`
   (`product_type_dairy + plain`) test with the **Path A / Path B** logic above. Add
   `category == "milk_dairy"` as a hard exclude. Use `category` (L1035) and
   `cat_result.get("category_subtype")`. Keep the downstream `if eligible_ferm and
   nova_level <= 3:` +8 application unchanged.
2. **`constants.py`:** add `CULTURED_CHEESE_SUBTYPES` (yogurt-type and aged/specialty
   cultured-cheese subtypes) — **excluding** the cottage and white-cheese (`גבינה לבנה`)
   fresh subtypes per the cottage ruling. Confirm the exact subtype string values against the
   cheese router's emitted `category_subtype` labels (P1 — the model author has the live
   subtype vocabulary).
3. **`constants.py`:** add `FLAVORED_VARIANT_MARKERS_HE` (list above).
4. **`nova_proxy.py` ~L166–169 (R4 `is_plain`):** add the `has_flavor_variant` clause
   (name + ingredient substring match against `FLAVORED_VARIANT_MARKERS_HE`); product stays
   NOVA 3 when it fires.
5. **Re-model OFF/ON** on cheese / hummus / milk / yogurt / snack_bars and re-confirm:
   (a) cottage 1% ≈ 89.76 → **90/A** (no +8);
   (b) both fluid-milk products no longer get +8 (milk 85/A leakage closed);
   (c) napoleon שום שמיר stays NOVA 3 and does **not** reach A;
   (d) yogurt retains its (legitimate) bonus;
   (e) flag-OFF still 59/59 byte-identical.
6. **R1, R2, R3, R5, R6 — no change.** Re-run only to capture the new combined distribution.

---

## v1.1 — calls that are the owner's / Product's, not mine

1. **Cottage/white-cheese into Path B?** I recommend EXCLUDE (lands the owner's stated 90/A;
   culturing is table-stakes in fresh cheese). Including them → ~97/S. **Owner values call.**
2. **Yogurt A/S distribution** (15 A / 3 S in the v1 model) — legitimate now that R7 is
   gated, but whether that many A's/S's is the desired yogurt ceiling is a **P2 owner
   decision** per frozen product (no hard cap, per owner ruling 2). Trim, if wanted, via the
   `yogurt` R1 protein-apex anchors — a calibration knob, not an R7 defect.
3. **Any residual milk A-crossing from the R1 `milk_dairy` curve alone** (after R7 leakage is
   removed) is a clean frozen-ceiling decision for **P2 owner sign-off**, not leakage.
4. **`CULTURED_CHEESE_SUBTYPES` exact membership** for specialty/aged cheeses — a food-science
   list I own, but the precise router subtype strings must be reconciled with live routing
   (Data Agent in P1); flag any cheese subtype the router does not actually emit.
5. **Product Agent D7 co-sign** still required before any P1 engine edit ships.
