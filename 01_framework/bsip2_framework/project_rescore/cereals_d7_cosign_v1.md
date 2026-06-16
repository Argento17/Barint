# Cereals × Sugar — Product Agent D7 Co-Sign (Phase 4 Enrollment)

**Task:** TASK-278 — Project Rescore (Phase 4: cereals × sugar first production enrollment)
**Date:** 2026-06-14
**Author:** Product Agent
**Verdict: CO-SIGN APPROVED WITH CONDITIONS**
**Scope:** Governance co-sign only. No engine code change. No pilot rescore. Zero score movement.
**Enrollment proposal (D6):** `01_framework/bsip2_framework/project_rescore/cereals_sugar_enrollment_v1.md`
**Phase-1 D7 reference:** `01_framework/bsip2_framework/project_rescore/shelf_relative_d7_cosign_v1.md`
**Phase-2 D7 reference:** `02_products/cookies_coffee/methodology/shelf_relative_sugar_enrollment_d7_cosign_v1.md`
**EV registry:** `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md` — EV-087 appended

---

## Verdict: CO-SIGN APPROVED WITH CONDITIONS

The D6 enrollment proposal is sound. The stats are orchestrator-verified from traces (exact match:
n=45, median=14.0g, IQR=11.0, robust_scale=8.896). The scope is bounded with zero dairy bleed risk.
The band structure is correctly calibrated to r-units and the larger cereal scale. The floor is set
appropriately higher than biscuits given cereal corpus score levels. The Anti-Immunity proof is
airtight.

One open question — family budget raise — is resolved below. The answer is Option A: no budget raise.

EV-087 is registered on this co-sign. The pilot acceptance gate is locked in Section 4.

Six conditions carry forward from Phase-1. One enrollment-specific condition is added. None waived.

---

## Section 1 — Scope Ratification

### Decision: `"cereal"` router category key — CONFIRMED

Scope `frozenset({"biscuit", "cereal"})` (adding `"cereal"` to the existing enrolled set) is
correct and bounded.

Structural confirmation from D6 §2:
- All 45 corpus products carry `category="cereal"` in trace output — confirmed from `run_cereals_synthesis_001`
- Hard anchors in `router_v2.py` Stage 1 enforce the `"cereal"` key for every relevant Hebrew term
- The `DAIRY_HEAD_TERMS` suppression guard prevents dairy products from being routed to `"cereal"`
- `snack_bar_granola` is a distinct router category and is explicitly excluded from this enrollment —
  granola bars without the "לבוקר" qualifier route to `snack_bar_granola`, not `"cereal"`, and are
  not enrolled here

**Dairy bleed risk: NONE.** A dairy product cannot receive `category="cereal"`. The enrollment
fires exclusively when `category == "cereal"`, which dairy products structurally cannot receive.

**Granola bar bleed risk: NONE.** The `snack_bar_granola` split is clean. If `snack_bar_granola`
is ever enrolled separately, it requires its own D7 — this ruling does not cover it and does not
create any precedent for skipping that gate.

Published categories affected by adding `"cereal"` to scope: **zero live published categories.**
The cereals category is not yet live on the consumer frontend. This enrollment is therefore
zero-risk for published-score contamination, parallel to the biscuits enrollment in Phase-2.

---

## Section 2 — Floor Ratification

### Decision: `formulation_absolute_floor = 62`, trigger at `sugars_g ≥ 25g/100g` — CONFIRMED

**Why 62, not lower:** The high-sugar cereals in the current corpus (sugar ≥ 25g) score between
30–52 from the absolute backbone alone. A floor at 62 is above their current scores, which means
it functions as a precautionary ceiling — not a redundant duplicate of existing penalty. Setting
the floor at 45 or 50 (below actual scores) would make it non-binding for the current corpus
while creating a target that future reformulation could approach. 62 is the right binding point:
above the current range, below grade B (70).

**Why 62, not higher (e.g., 65):** Floor=65 plus max_relief B=3 yields 68, which approaches
grade B territory (70). Given that the relative component for products with sugar ≥ 25g will
always be a surcharge (not relief — 25g is well above the 14g median at r=+1.24), this scenario
is structurally impossible in the current corpus. But the floor exists to guard against
not-yet-present products. A floor of 62 provides 8 points of headroom to grade B; that headroom
is the guard. 65 narrows the headroom to 2 points — too close to be defensible as a formulation
nutrient floor.

**Why 62 rather than biscuits' 55:** Cereal absolute-backbone scores occupy a lower range than
biscuits. Biscuit products at 20–25g sugar score 60–75 from the absolute backbone (a range where
floor=55 binds meaningfully). Cereal products at 25–39g sugar score 30–52 — the floor at 55
would be non-binding (products are already below it). The floor must be set above the current
range to function as an Anti-Immunity guard. 62 is the calibrated level where it provides genuine
protection without over-constraining within-floor differentiation.

**Anti-Immunity proof:**
- Grade B threshold: 70
- Floor: 62
- Max below-median relief (B_max): 3 pts
- Maximum composite for any product entering at floor: 62 + 3 = 65
- 65 < 70 (grade B) — **PROOF HOLDS**
- Note: for products with sugar ≥ 25g, the relative component fires as a surcharge (positive
  penalty), not relief, since 25g > 14g median. The floor+relief scenario is structurally
  impossible for this cohort; the floor is belt-and-suspenders for an unrepresented edge case.

**Confirmed:** floor=62 at threshold=25g. Anti-Immunity is mechanically guaranteed.

---

## Section 3 — Band Ratification

### Decision: P_max=6, B_max=3 (same structure as biscuits EV-085) — CONFIRMED WITH EXPLANATION

The bands are in r-units, where r = (value − median) / robust_scale. Because cereals have a
larger robust_scale (8.896g vs. biscuits' 5.115g), the same r-breakpoints cover larger raw gram
ranges. This is the correct behavior: the mechanism normalizes to the shelf's own spread, so
a cereal product needs to be further in raw grams from its shelf median to receive the same
penalty tier as a biscuit product was from its median.

**P=6 is proportionate for cereals:**
- r=2.5 requires being 22.2g above the 14g median → sugar ≥ 36.2g to reach max penalty
- Only the most extreme sweetened kids' cereals (Frosties at 38–39g) reach maximum surcharge
- Products at 22–26g sugar (moderate-high) receive 1–2pt surcharges — proportionate residuals
- At r=1.5–2.5 (sugar 27–36g): 4pt surcharge — strong signal for heavily sweetened cereals
- This is not double-counting: the absolute backbone's sugar penalties are category-calibrated;
  the 6pt relative maximum is the within-shelf ranking residual that the absolute backbone does
  not express

**B=3 is appropriate and bounded:**
- Max relief applies to plain oats/bran at 0.5g sugar: r_below=1.52 → 2 pts (not even max)
- Maximum relief (3pts) would require sugar near 0g: r_below = 14/8.896 = 1.57 → band [1.5,3.0] → 2pts
- True 3pt relief requires r_below ≥ 3.0, i.e., sugar ≤ 14 − (3.0 × 8.896) = −12.7g — structurally impossible
- Practical maximum relief in this corpus: **2pts** (for 0.5g sugar plain oats at r_below=1.52)
- B_max=3 is a theoretical ceiling that cannot be reached on this shelf. Anti-Immunity is
  doubly protected: by the floor (62) AND by the physics of the distribution

**Asymmetry confirmed: P=6 > B=3.** Below-median relief cannot launder a product the absolute
backbone has penalized. The relief for the genuinely low-sugar cereals (0.5–5g) is modest and
accurate — these products are already scoring 85+ from the absolute backbone; the 1–2pt relief
is resolution, not distortion.

**Calibration note for pilot:** Verify that within-cereal grade-boundary inflation is absent.
Specifically, confirm no product with sugar ≥ 12g (within-median range) receives a relief term
that crosses a letter-grade boundary. Expected: all r_below < 0.5 for products above 9.5g sugar,
placing them in the zero-relief band.

---

## Section 4 — Family Budget Raise Decision

### Decision: Option A — NO budget raise for cereals — BINDING PRODUCT RULING

**The ruling:**

No `SUGAR_CEREAL_BUDGET_RAISE` constant is needed. The existing `SUGAR_FAMILY_BUDGET` accommodates
the 6pt relative surcharge without double-counting.

**Reasoning, distinct from the Nutrition Agent's statement:**

The biscuit enrollment added `SUGAR_SHELF_BISCUIT_BUDGET_RAISE=6` because the biscuit absolute
backbone includes `HP_SUGAR` penalties that are heavy and compound — biscuit products at the
high end of the corpus had already consumed substantial family budget, making the additional 6pt
relative surcharge a double-count risk against the budget cap. The budget raise was a relief
valve for the surcharge path (not the relief path) to prevent the penalty from being clipped
before the relative term fires.

For cereals, the high-sugar products (sugar ≥ 25g, r_above ≥ 1.24) score 30–52 from the
absolute backbone — they have substantial remaining budget headroom. The 6pt relative surcharge
stacks on top of the absolute penalty without hitting the budget ceiling. The budget raise in
biscuits was a pre-emptive guard against a specific corpus pattern (heavy HP_SUGAR + heavy
absolute penalties approaching the budget cap); that pattern is not present in cereals.

Furthermore, the surcharge direction makes the budget analysis asymmetric: for high-sugar
cereals, the relative term is a penalty addition, not a relief addition. Budget caps constrain
how large a combined penalty can be. At 30–52 absolute + 2–6 relative = 32–58 total penalty
equivalent — still far from any budget ceiling. For low-sugar cereals, the relief path adds
up to 2pts — the relief is bounded and the budget is not a limiting factor in either direction.

**The Nutrition Agent's rationale** (that absolute backbone sugar penalties for cereals are lower
than for biscuits) is directionally correct but understates the decisive reason: the cereal
corpus absolute-backbone scoring range for high-sugar products (30–52) is low enough that the
budget ceiling is non-binding regardless of the 6pt relative surcharge. No budget raise is needed
because the budget is not the binding constraint.

**Reversal condition:** If the Data Agent's pilot implementation reveals that any cereal product's
combined penalty (absolute + relative) is being clipped by `SUGAR_FAMILY_BUDGET` before the floor
logic runs, add `SUGAR_CEREAL_BUDGET_RAISE=6` at that point. The pilot output must include a flag
on any product where the budget cap fires during the relative computation. If that flag is absent
on all 45 products, Option A is confirmed.

---

## Section 5 — Pilot Acceptance Gate

Locked before pilot runs. All criteria must pass. Any failure is a hard stop.

| # | Criterion | Pass Condition |
|---|---|---|
| 1 | Resolution restored | Fewer products pinned at identical absolute-backbone scores vs. baseline run |
| 2 | Inversion A corrected | 7290100000029 (24g/33.0) ranks above 5054568100011 (38g/35.0) after SR — direction flipped |
| 3 | Inversion B gap widened | Gap between 7290100000042 (5g/74.9) and 5054568100022 (16g/70.4) widens from 4.5 to ≥5.5pts |
| 4 | Min movers | n_movers ≥ 15 (of 45 products). A mechanism that fires on 32/45+ products (per band analysis) and produces <15 score changes is an absorption signal — stop and investigate |
| 5 | Min grade changes | n_grade_changes ≥ 1. Cereals is a spread-y shelf; the mechanism must produce at least one grade change to confirm it is not absorbed |
| 6 | Max absorption rate | Absorption rate ≤ 40% (≤18/45 products show zero net movement despite relative term firing). If >40% absorbed, the shelf is degenerate and the pilot fails |
| 7 | Anti-Immunity holds | No cereal with sugars_g ≥ 25g reaches grade B (score ≥ 70). Grade A is structurally impossible given corpus scores |
| 8 | Floor enforced | All 9 products with sugars_g ≥ 25g: composite score ≤ 62. Full distribution, not spot-check |
| 9 | No dairy bleed | All products with `category != "cereal"` are byte-identical to flag-off baseline. Zero exceptions |
| 10 | Brined byte-identical | `run_brined_004` output is byte-identical at flag-on. This is the frozen invariant guard — zero exceptions |
| 11 | Flag-off byte-identical | `BARI_SHELF_RELATIVE_V1=off` across all published categories → zero movement vs. committed baselines |

### Ratified Named Inversions

**Inversion A — 7290100000029 (24g sugar) vs. 5054568100011 (38g sugar)**

- 7290100000029: sugar=24g, current score=33.0. Expected post-pilot: r_above=(24−14)/8.896=1.124 → band [1.0,1.5] → surcharge=2pts → score ~31.0
- 5054568100011: sugar=38g, current score=35.0. Expected post-pilot: r_above=(38−14)/8.896=2.698 → band [2.5,∞) → surcharge=6pts → score ~29.0
- Pass condition: 5054568100011 scores BELOW 7290100000029 after SR. Minimum gap: 5054568100011 ≤ 31.0 AND 7290100000029 ≥ 31.0, with 5054568100011 < 7290100000029. Inversion direction must be fully corrected.
- Both products must remain grade E (score < 65). No grade-boundary crossing expected or permitted.

**Inversion B — 7290100000042 (5g sugar) vs. 5054568100022 (16g sugar)**

- 7290100000042: sugar=5g, current score=74.9. Expected: r_below=(14−5)/8.896=1.012 → band [0.5,1.5] → relief=1pt → score ~75.9
- 5054568100022: sugar=16g, current score=70.4. Expected: r_above=(16−14)/8.896=0.225 → band [0.0,0.5] → surcharge=0 → score unchanged at 70.4
- Pass condition: gap widens from 4.5pts to ≥5.5pts. 7290100000042 remains grade B (score ≥ 70); 5054568100022 remains grade B/C boundary area (unchanged).
- Minimum: 7290100000042 post-pilot score ≥ 75.5 AND gap ≥ 5.5pts. Full gap closure is not expected (other dimensions dominate).

Both inversions must be verified by trace inspection (not summary statistics). The trace for each
product must show the `SUGAR_SHELF_REL_V1` rule tag when the surcharge or relief fires.

---

## Section 6 — Hard Conditions (All Blocking)

**Carried from Phase-1 D7 co-sign:**

1. EV-084 registered — done at Phase-1 co-sign (line 1881, confirmed in registry).
2. `compute_shelf_stats()` IQR-primary default before any pilot run. The cereals corpus IQR=11.0 and robust_scale=8.896 were derived with IQR-primary (max(IQR/1.349, 1.4826·MAD, min_scale)). The engine must implement the same formula — verified by the orchestrator for the biscuit pilot; must re-verify for cereals.
3. n≥20 guard — non-binding on this corpus (n=45 >> 20). Cereal corpus n_with_sugar=45 confirmed.
4. Asymmetric P>B — confirmed. P=6, B=3.
5. `formulation_absolute_floor` non-None — floor=62, threshold=25g. Confirmed.
6. Six-guard no-regression plan executes before merge. Guards 1 (milk byte-identical to run_005_headpin) and 2 (all published categories byte-identical at flag-off) are mandatory hard gates. Both must pass with zero exceptions.

**Enrollment-specific (added here):**

7. Budget cap non-binding confirmation: pilot output must include a flag or log line for any product where `SUGAR_FAMILY_BUDGET` clips the combined penalty during the relative computation. If any product is clipped, Option A (no budget raise) must be revisited before the pilot is accepted.
8. Trace verification: `SUGAR_SHELF_REL_V1` rule tag must appear in traces for the 2 named inversion barcodes (7290100000029, 5054568100011, 7290100000042, 5054568100022) when the surcharge or relief fires. Tagless application is not auditable.
9. Floor compliance full-distribution: all 9 products with sugars_g ≥ 25g must individually confirm composite score ≤ 62 in pilot output. Spot-check is not sufficient.
10. EV-085 biscuit path byte-identical: biscuit scores from the committed `run_cookies_005_shelfrel_pilot` baseline must be byte-identical when cereals enrollment is added. Adding `"cereal"` to scope must not move any biscuit product's score.

---

## Section 7 — Tripwire Assessment

**No tripwire fires on this co-sign.**

- Frozen invariants: not touched. Milk scores (`run_005_headpin`), all published category scores are unchanged. Flag default=off. Zero score movement on this D7.
- Consumer-facing / irreversible: not applicable. The cereals category is unpublished. The flag is default-off. The pilot rescore is internal. Owner go-live gate (tripwire-1) is required before any published movement.
- Major program start/kill: this is Phase 4 of an already-approved program (TASK-278, D7 Phase-1 co-signed 2026-06-14).
- External commitment/spend/legal: none.
- Strategy redefinition: not applicable.

**Owner escalation: NOT required.** This co-sign is within the D7 lane. The first published score
movement (owner go-live for the cereals page) is the tripwire-1 gate that escalates.

---

## Decision Log

| Item | Options considered | Choice | Decisive reason | Reversal condition |
|---|---|---|---|---|
| Scope key | (a) `"cereal"` (proposed); (b) Expand to include `"snack_bar_granola"` | (a) `"cereal"` only | Granola bars need their own D7; bleed risk is zero with `"cereal"` alone; no evidence `snack_bar_granola` requires the same bands | Revisit when `snack_bar_granola` reaches its own D7 enrollment |
| Floor value | (a) 55 (same as biscuits); (b) 62 (proposed, calibrated to cereal corpus); (c) 65 (looser) | (b) 62 | Current high-sugar cereal scores are 30–52; floor=55 would be non-binding; floor=65 is too close to grade B (70); floor=62 is the calibrated Anti-Immunity point | Revisit if the corpus expands to include high-fiber/high-protein cereals that score near 62 despite 25g+ sugar — would need floor recalibration |
| Band structure | (a) Same P=6/B=3 as biscuits (same r-unit structure); (b) Compress bands given larger scale | (a) Same structure | r-unit normalization is the correct abstraction — same breakpoints at different scales correctly produce different raw-gram thresholds; compressing bands would under-penalize the 35–39g sweetened-cereal cluster | Recalibrate to P=4 if pilot shows high-sugar outliers receive penalties that misrepresent their ordinal rank vs. moderate-sugar products |
| Family budget raise | (a) No raise — Option A; (b) SUGAR_CEREAL_BUDGET_RAISE=6 — Option B | (a) No raise | Cereal absolute-backbone scores for high-sugar products (30–52) leave substantial budget headroom; budget ceiling is non-binding; the biscuit budget raise addressed a specific HP_SUGAR accumulation pattern absent in cereals | Add SUGAR_CEREAL_BUDGET_RAISE=6 if pilot shows any product's penalty is clipped by SUGAR_FAMILY_BUDGET before floor logic runs |
| Pilot inversion A type | True inversion (wrong direction): 5054568100011 (38g) outscores 7290100000029 (24g) | Correction mandatory: direction must flip | A higher-sugar product scoring higher than a lower-sugar product is an unambiguous error; the mechanism must correct it | No reversal — if Inversion A does not correct, the enrollment fails |
| Pilot min_movers threshold | (a) 10 movers; (b) 15 movers; (c) 20 movers | (b) 15 movers | Band analysis predicts ~32/45 products in non-zero surcharge/relief bands; 15/45 = 33% is a conservative floor for "mechanism fires"; fewer movers than 15 on a shelf this spread suggests absorption | Revisit if corpus n changes significantly before pilot runs |

---

## EV-087 Registration

EV-087 is registered in `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md`
as part of this co-sign. See the append operation for the full registry entry.
