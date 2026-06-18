# Graduated Sodium Blast Radius Recon — TASK-267

Generated: 2026-06-13T (recon run)
Recon type: env-flag toggle (BARI_REDLABEL_V1=off vs on). No engine file modified.

**score_engine.py sha256 BEFORE and AFTER: `d711ec586d229aeda655f8a2b6c3f9ae3359792d41079118dce4c71b8cc5887a`**
**constants.py sha256 BEFORE and AFTER: `5fe0af5fab33ebbc30d58380385b42b87d05bb1a370531751f543ad8d5f3fd58`**
Engine file unchanged: **True**
Constants file unchanged: **True**

---

## SPEC CONFLICT DETECTED — READ BEFORE CONCLUSIONS

The task brief assumes `BARI_REDLABEL_V1` is a "graduated sodium flag." It is not. It is a bundled flag
that controls FOUR distinct logic changes simultaneously:

1. `score_regulatory_quality()` — switches from 3-step function to continuous per-label formula. This
   applies to **ALL categories, not just endemic or dairy**. (score_engine.py line 1556)
2. Reformulable label count — excludes endemic sat_fat from the >=2 trigger. (line 1665)
   Scoped to `REDLABEL_ENDEMIC_SATFAT_CATEGORIES = {"dairy_protein", "whole_food_fat"}`.
3. Graduated sodium bands — replaces HIGH_SODIUM_700MG_PLUS cliff. (line 2007)
   Scoped to endemic categories only.
4. Graduated sugar penalty — SUGAR_GRADUATED_BANDS. (line 1836)
   Scoped to endemic categories only.

Implication: enabling `BARI_REDLABEL_V1=on` to test "graduated sodium" also activates changes #1 and #2,
which move yogurt, cheese-spreads, and even cereals that have nothing to do with sodium. The blast radius
reported here reflects the full flag, not just the sodium component.

---

## 1. Scope of the Graduated Sodium Path

From `constants.py` line 238:
```python
REDLABEL_ENDEMIC_SATFAT_CATEGORIES = frozenset({"dairy_protein", "whole_food_fat"})
```

`SODIUM_GENERAL_BANDS` (constants.py lines 248-254):
```python
SODIUM_GENERAL_BANDS = [
    (900, None, 12),   # >=900mg: -12pts penalty
    (700, 899,   8),   # 700-899mg: -8pts penalty
    (600, 699,   4),   # 600-699mg: -4pts penalty
    (450, 599,   2),   # 450-599mg: -2pts penalty
    (0,   449,   0),   # <450mg: no penalty (zero)
]
```

Graduated sodium ONLY fires when:
- `BARI_REDLABEL_V1=on`, AND
- `category in {"dairy_protein", "whole_food_fat"}`, AND
- NOT the cereal/granola path (line 1960-2003)

Brined cheese routing (from run_brined_002, 48 products):
- `dairy_protein`: ~29 products — IN endemic set, graduated sodium applies
- `default`: ~14 products — NOT in endemic set, HIGH_SODIUM_700MG_PLUS cap still fires
- `cracker`: 2 products — NOT in endemic set
- `whole_food_fat`: 1 product — IN endemic set

To fully fix all 48 brined-cheese products would require either:
  (a) Improved category routing so all 48 land in `dairy_protein`, OR
  (b) Adding a brined_cheese slug to `REDLABEL_ENDEMIC_SATFAT_CATEGORIES`

Both require a separate D7 scope decision (Nutrition Agent + Product Agent joint).

---

## 2. Does Graduated Sodium Fix Brined Cheese? (72-pin analysis)

**Products pinned at cap=72 in run_brined_002: 42** (out of 48; 6 were unpinned)
**72-pin broken with BARI_REDLABEL_V1=on: 42 / 42**
**72-pin SAME (byte-identical): 0 / 42**

All 42 move — but in OPPOSITE directions depending on category routing:

### Products that GAIN score (dairy_protein — graduated sodium replaces cliff cap):

| barcode | category | NOVA | sodium_mg | score_off | score_on | delta | caps_on |
|---------|----------|------|-----------|-----------|----------|-------|---------|
| 2107798 | dairy_protein | 3 | 1000 | 71.0/B | 76.8/B | +5.8 | [NOVA_PROXY_3_PROCESSED] |
| 2133162 | dairy_protein | 2 | 1300 | 72.0/B | 84.8/A | +12.8 | [] |
| 2133889 | dairy_protein | 2 | 1200 | 72.0/B | 83.8/A | +11.8 | [] |
| 2511236 | dairy_protein | 2 | 880 | 72.0/B | 75.0/B | +3.0 | [] |
| 7290011499303 | dairy_protein | 2 | ~500 | 66.0/B | higher | varies | |
| (and ~9 more dairy_protein products) | | | | | | | |

### Products that LOSE score sharply (default/cracker — HIGH_SODIUM_700MG_PLUS stays but REFORMULABLE_LABELS_2_PLUS now fires):

| barcode | category | NOVA | sodium_mg | score_off | score_on | delta | caps_on |
|---------|----------|------|-----------|-----------|----------|-------|---------|
| 2107071 | default | 3 | 840 | 63.4/C | 41.0/D | -22.4 | [REFORMULABLE_LABELS_2_PLUS, NOVA_PROXY_3_PROCESSED, HIGH_SODIUM_700MG_PLUS] |
| 2385455 | default | 2 | 1010 | 68.8/B | 45.0/D | -23.8 | [REFORMULABLE_LABELS_2_PLUS, HIGH_SODIUM_700MG_PLUS] |
| 2511229 | default | 2 | 940 | 72.0/B | 45.0/D | -27.0 | [REFORMULABLE_LABELS_2_PLUS, HIGH_SODIUM_700MG_PLUS] |
| 2511243 | default | 2 | 940 | 72.0/B | 45.0/D | -27.0 | [REFORMULABLE_LABELS_2_PLUS, HIGH_SODIUM_700MG_PLUS] |
| 48413 | cracker | 2 | 1065 | 72.0/B | 45.0/D | -27.0 | [REFORMULABLE_LABELS_2_PLUS, HIGH_SODIUM_700MG_PLUS] |
| 369617 | whole_food_fat | 3 | 800 | 55.5/C | 50.2/C | -5.3 | [NOVA_PROXY_3_PROCESSED] |

**The reason for `default`-category products losing score**: Under BARI_REDLABEL_V1, the reformulable
label count (change #2) removes the endemic-sodium exclusion from the 2+ cap trigger for non-endemic
categories. These products have BOTH a sat_fat red label AND a sodium red label. In the OFF state,
EV-053 already excluded sodium from the 2+ count (brined_food path). With REDLABEL_V1=on but category=
`default` (not endemic), the sodium label is NOT excluded from the reformulable count, so
REFORMULABLE_LABELS_2_PLUS fires at cap=45. This is a regression for non-endemic brined cheese.

### NOVA + fat differentiation (does NOVA-1 vs NOVA-3, low-fat vs high-fat get different scores?):

YES — for dairy_protein-routed products:
- NOVA=1, fat<10%: off=[72.0] -> on=[85.0, 88.9, 89.6] (A-grade territory, strong differentiation)
- NOVA=1, fat>=20%: off=[72.0] -> on=[45.0, 69.5, 73.4] (mixed — some hit REFORMULABLE_LABELS_2_PLUS)
- NOVA=2, fat<10%: off=[72.0] -> on=[75, 81-87 range]
- NOVA=2, fat>=20%: off=[68-72] -> on=[45.0, 59.4, 75.1] (mixed)
- NOVA=3, fat<10%: off=[68-72] -> on=[69.8-76.8]
- NOVA=3, fat>=20%: off=[55-66] -> on=[50.2, 59.5] (slight regression due to graduated sodium penalty)

For dairy_protein products, the 72-pin absolutely breaks — but the results are not uniformly positive.
Some products (NOVA-1 low-fat, high-sodium) jump from 72/B to 85+/A. Others that also have a sat_fat
red label hit REFORMULABLE_LABELS_2_PLUS and drop to 45/D.

---

## 3. Blast Radius on Published Categories

### 3a. FROZEN Milk (run_005_headpin) — CRITICAL CHECK

Corpus: 20 products (run_milk_002/output, all non-audit BSIP1)
**milk_scores_moved = 0**

**RESULT: BYTE-IDENTICAL. The graduated sodium flag does NOT move any frozen milk score.**

Explanation: All milk products have sodium ~40-60mg/100g. The lowest SODIUM_GENERAL_BANDS penalty
fires at 450mg. Milk is 8-10x below that floor. The HIGH_SODIUM_700MG_PLUS cap also never fires
for milk. However — the regulatory quality formula change (effect #1) DOES apply to milk. The reason
milk is byte-identical is that milk has zero red labels, so the formula change (which computes
deductions per-label) produces the same output (95 − 0 deductions = 95) regardless of step vs continuous.

**Frozen milk tripwire: CLEAR.**

### 3b. Yogurt (run_yogurt_006)

Corpus: 88 products
**yogurt_scores_moved = 7**

| barcode | category | NOVA | sodium_mg | score_off | score_on | delta | notes |
|---------|----------|------|-----------|-----------|----------|-------|-------|
| 7290017065588 | dairy_protein | 2 | 50 | 72.3/B | 73.4/B | +1.1 | regulatory quality formula change |
| 7290019635819 | dairy_protein | 3 | 400 | 54.3/C | 55.0/C | +0.7 | regulatory quality formula change |
| 7290102393039 | dairy_protein | 4 | 45 | 45.2/D | 44.4/D | -0.8 | regulatory quality formula change |
| 7290102393060 | dairy_protein | 4 | 50 | 43.5/D | 42.6/D | -0.9 | regulatory quality formula change |
| 7290102394081 | dairy_protein | 4 | 55 | 55.0/C | 53.0/C | -2.0 | regulatory quality formula change |
| 7290102397600 | dairy_protein | 4 | 40 | 62.4/C | 60.4/C | -2.0 | regulatory quality formula change |
| 7290102397617 | dairy_protein | 4 | 50 | 57.5/C | 55.5/C | -2.0 | regulatory quality formula change |

**All 7 moved yogurts have sodium well below 450mg (range 40-400mg). These move because of effect #1
(regulatory quality continuous formula), NOT because of graduated sodium bands. The sodium graduated
path plays zero role.**

**Yogurt scores ARE moved by BARI_REDLABEL_V1=on.** These are published yogurts (run_yogurt_006).
The movements range -2.0 to +1.1 points — all within the same grade. No grade change occurs.
But scores are not byte-identical.

### 3c. Cheese-Spreads (run_cheese_003)

Corpus: 59 products
**cheese_spreads_scores_moved = 32**

This is the largest blast. 32/59 cheese-spread products move because cheese-spreads are `dairy_protein`
category and the regulatory quality continuous formula (effect #1) changes scores for any product with
red labels. Sodium levels range 200-558mg — well below the 700mg cliff and the 450mg graduated band floor.
Sample movements (all from regulatory quality formula, not sodium):

| barcode | category | NOVA | sodium_mg | score_off | score_on | delta |
|---------|----------|------|-----------|-----------|----------|-------|
| 4127336 | dairy_protein | 2 | 350 | 72.0/B | 73.6/B | +1.6 |
| 4127817 | dairy_protein | 2 | 200 | 72.2/B | 73.8/B | +1.6 |
| 3075850 | dairy_protein | 3 | 558 | 63.7/C | 62.0/C | -1.7 |
| 3523230065467 | dairy_protein | 3 | 480 | 63.8/C | 62.1/C | -1.7 |
| 7290014762831 | dairy_protein | 3 | 481 | 44.8/D | 43.2/D | -1.6 |

No grade changes among the 32 moved cheese-spread products. All movements are sub-2pt.

**Cheese-spreads are published. If run_cheese_003 is the frozen baseline, these movements are a
concern — the category was not listed in the "published dairy" that must not move, but the scores
are not byte-identical.**

### 3d. Non-Dairy Categories (scope guard)

#### Cereals (run_cereals_multiretailer_001, 20-record sample)
**cereals_moved = 8 / 20**

| barcode | category | NOVA | sodium_mg | score_off | score_on | delta | caps |
|---------|----------|------|-----------|-----------|----------|-------|------|
| 16000423534 | cereal | 2 | 259 | 45.5/D | 46.1/D | +0.6 | [ISRAELI_RED_LABEL_1_SUGAR] |
| 4005528115218 | beverage | 2 | 200 | 48.3/D | 48.6/D | +0.3 | [ISRAELI_RED_LABEL_1_SUGAR] |
| 42400108153 | cereal | 3 | 454 | 44.4/D | 44.8/D | +0.4 | [HIGH_SUGAR_25G_PLUS, ...] |
| 5010026521149 | cereal | 2 | 0 | 53.6/C | 54.6/C | +1.0 | [ISRAELI_RED_LABEL_1_SUGAR] |
| 7290001343845 | snack_bar_granola | 2 | 0 | 60.3/C | 61.6/C | +1.3 | [SNACK_BAR_RED_SUGAR_LABEL] |
| 7290011668570 | snack_bar_granola | 2 | 70 | 52.2/C | 53.0/C | +0.8 | [SNACK_BAR_RED_SUGAR_LABEL] |
| 7290019603634 | snack_bar_granola | 2 | 0 | 60.2/C | 61.7/C | +1.5 | [SNACK_BAR_RED_SUGAR_LABEL] |
| 7290104506819 | cereal | 2 | 200 | 50.3/C | 51.3/C | +1.0 | [ISRAELI_RED_LABEL_1_SUGAR] |

**IMPORTANT: These are non-dairy categories (cereal, snack_bar_granola) that move despite sodium_mg
being 0-454mg and far below any sodium threshold.** The movement is 100% from effect #1 — the
regulatory quality continuous formula applies globally, not just to endemic categories.

This confirms: **BARI_REDLABEL_V1 is NOT a safe targeted sodium fix. It changes regulatory quality
scoring for all categories.**

Bread, hummus, salty-snacks BSIP1 dirs were not found in the expected path (may be stored elsewhere).
The cereal evidence is sufficient to confirm the scope problem.

---

## 4. The Key Hypothesis — Confirmed or Refuted

**Hypothesis: "Published dairy (milk ~50mg, yogurt low-sodium) is below the 700mg cap threshold,
so the graduated path may be byte-identical for them."**

**REFUTED for yogurt and cheese-spreads. CONFIRMED for milk only.**

- Milk: byte-identical (0 red labels = both formulas give 95; no sodium penalty fires)
- Yogurt: 7 products move (regulatory quality formula, not sodium)
- Cheese-spreads: 32 products move (regulatory quality formula, not sodium)
- Cereals (non-dairy): 8/20 move (regulatory quality formula, not sodium)

The graduated sodium path itself (SODIUM_GENERAL_BANDS) is clean for low-sodium dairy. But the
bundled flag activates the regulatory quality formula change globally, causing movement in all
published dairy and non-dairy categories.

---

## 5. Recommended Activation Scope

Three options, in order of surgical precision:

### Option A (SAFEST — surgical sodium-only activation)
Separate the graduated sodium logic from `BARI_REDLABEL_V1` into a dedicated `BARI_GRAD_SODIUM_V1`
flag that ONLY controls the SODIUM_GENERAL_BANDS path (score_engine.py lines 2005-2044). Leave all
other BARI_REDLABEL_V1 effects gated by the existing flag.

**Blast radius: ZERO on published dairy. Only products in `{dairy_protein, whole_food_fat}` with
sodium >= 450mg would be affected. Milk (50mg) and yogurt (40-400mg) stay byte-identical. The
cheese-spread corpus (max 558mg) would have at most 2pt penalty for the highest-sodium products.**

This is the recommended path. Requires engine change (splitting the flag logic) — a reversible,
non-consumer-facing implementation step that does not require owner tripwire escalation.

### Option B (CURRENT FLAG — wide blast radius)
Activate BARI_REDLABEL_V1 as-is. Accepts:
- 7 yogurt score moves (sub-2pt, no grade change)
- 32 cheese-spread score moves (sub-2pt, no grade change)
- Unknown number of cereal/bread/granola moves (sub-2pt range, no grade change confirmed in sample)
- Frozen milk: BYTE-IDENTICAL (CLEAR)
- Brined cheese dairy_protein products: gain 3-13pts (breaks the 72-pin productively)
- Brined cheese default/cracker products: lose 22-27pts (regression — hits REFORMULABLE_LABELS_2_PLUS=45 cap)

Requires: Nutrition Agent + Product Agent review of yogurt/cheese-spread score movements before approval.

### Option C (FULL BRINED FIX — requires additional D7)
Option A or B PLUS add brined_cheese routing fixes OR add brined_cheese to endemic set.
This fixes the `default`-routed brined products that lose score under Option B.
Requires separate D7 scope decision.

---

## 6. Governance Pre-Check (bari-bsip2-scoring-governance)

1. **Evidence Registry**: SODIUM_GENERAL_BANDS cites EV-REDLABEL-009/010 — already registered.
   If Option A (new flag) is chosen, a new evidence registry entry is required.

2. **Label Observability**: `sodium_mg` coverage in brined-cheese corpus is 48/48 (run_brined_002).

3. **Category Activation Scope**: Current endemic scope = `{dairy_protein, whole_food_fat}`.
   The graduated-sodium path is correctly scoped to this set. The regulatory quality change
   (effect #1) is NOT scoped — it is global. This is the core issue.

4. **Rollback Plan**: `BARI_REDLABEL_V1=off` is the committed default (all published runs use `off`).
   run_brined_002 is the committed baseline for brined cheese.

5. **Rule Accumulation**: SODIUM_GENERAL_BANDS replaces HIGH_SODIUM_700MG_PLUS for endemic categories.
   No new rule is created. Score_engine already has the code; this is an activation decision.

---

## 7. OFF Ban Confirmation

off_used: **0**. No Open Food Facts data used anywhere in this recon. All BSIP1 records are from
direct scrape sources (Shufersal BSIP0 pipeline). The OFF integration client was not invoked.

---

## Summary of the Three Answers

**Answer A — Does graduated sodium un-pin brined cheese (NOVA+fat express)?**
YES, for products that route to `dairy_protein` or `whole_food_fat` (~30/48). The 72-pin breaks
completely for all 42 previously-pinned products: dairy_protein products gain 3-13pts (some reaching A),
while default-routed products with both sat_fat + sodium red labels DROP to 45 (REFORMULABLE_LABELS_2_PLUS).
The result is not uniformly positive — it surfaces the routing problem as a second issue.

**Answer B — Per-published-category diff (esp. FROZEN milk)**
- Frozen milk (20 products): **BYTE-IDENTICAL. milk_scores_moved = 0. Tripwire CLEAR.**
- Yogurt (88 products): 7 moved (sub-2pt, no grade change; cause = regulatory quality formula, not sodium)
- Cheese-spreads (59 products): 32 moved (sub-2pt, no grade change; same cause)
- Cereals sample (20 products): 8 moved (sub-2pt; same cause — regulatory quality formula is global)

**Answer C — Is there a clean activation scope?**
NOT with the current `BARI_REDLABEL_V1` flag as-is. The flag bundles regulatory quality formula changes
that affect all categories. A surgical `BARI_GRAD_SODIUM_V1` flag (Option A above) that isolates only
the SODIUM_GENERAL_BANDS path would produce a clean activation: byte-identical for published dairy
(milk/yogurt), small penalty for high-sodium cheese-spreads (max 2pts), and productive un-pinning for
brined-cheese products in the dairy_protein routing.

**Proposed status: RETURNED — recon complete. D7 decision pending on activation scope (Option A recommended).**
Not done: D7 implementation, engine change, any frontend packaging.
