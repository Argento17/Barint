# Yogurt × Sugar — Product Agent D7 Co-Sign (Phase 6 Enrollment)

**Task:** TASK-278 — Project Rescore (Phase 6: yogurt × sugar enrollment)
**Date:** 2026-06-14
**Author:** Product Agent
**Verdict: CO-SIGN APPROVED WITH CONDITIONS**
**Scope:** Governance co-sign only. No engine code change. No pilot rescore. Zero score movement.
**Enrollment proposal (D6):** `02_products/yogurt_system/methodology/shelf_relative_sugar_enrollment_yogurt_v1.md`
**Phase-1 D7 reference:** `01_framework/bsip2_framework/project_rescore/shelf_relative_d7_cosign_v1.md`
**Phase-4 D7 reference:** `01_framework/bsip2_framework/project_rescore/cereals_d7_cosign_v1.md`
**EV registry:** `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md` — EV-088 appended

---

## Verdict: CO-SIGN APPROVED WITH CONDITIONS

The D6 enrollment proposal is sound. The stats are orchestrator-verified from committed traces
(exact match to P103 pilot: median=5.45g, IQR=5.80, scale=4.299, 0.0g divergence). The scope
guard is correct and elegant — `CULTURED_YOGURT_SUBTYPES` already exists in constants.py and
is already used by the fermentation bonus gate, requiring zero new infrastructure. The floor is
calibrated to the highest-scoring high-sugar yogurt in the corpus. The Anti-Immunity proof is
airtight.

Five open questions from D6 are resolved below (Sections 2–6). All decisions are made and
binding. EV-088 is registered on this co-sign. The pilot acceptance gate (11 criteria) is locked
in Section 7.

Six conditions from Phase-1 carry forward. Three yogurt-specific conditions are added. Condition
on frozen-milk byte-identity (C10) is the critical safety gate for this enrollment.

---

## Section 1 — D6 Ratification

### Elements reviewed and confirmed

**1. Scope guard — Option A confirmed**

`category == "dairy_protein" AND category_subtype in CULTURED_YOGURT_SUBTYPES` is the correct
and only defensible scope. No router edit required. `CULTURED_YOGURT_SUBTYPES` is already defined
in constants.py and populated by router_v2.py `_build_anchor_result()` for all anchor-routed
yogurt products. Options B (dedicated router category) and C (barcode frozenset) are rejected:
Option B requires router_v2.py edits that are not justified given the subtype field already works;
Option C is brittle.

The subtype discriminator correctly excludes all non-yogurt dairy_protein products. Kefir,
cottage, cream cheese, hard cheeses, brined cheeses, ricotta, and mascarpone each carry distinct
subtypes outside `CULTURED_YOGURT_SUBTYPES`. The field has been stable since TASK-139C.

**2. Corpus n=74 confirmed**

88 total, 87 yogurt-only (1 cereal outlier excluded), 74 with non-null sugars_g. The 14 null-sugars
products are handled under D7-YS-05. Source: `L1_observed_signals.sugars_g` in committed trace
files — direct product scrape only. OFF=0.

**3. Stats confirmed — IQR-primary, scale=4.299g**

Median=5.45g, IQR=5.80g, MAD=2.55g, IQR/1.349=4.299, 1.4826×MAD=3.781. Robust_scale=4.299
(IQR-primary). Scale formula: `max(IQR/1.349, 1.4826×MAD, 1.4)`. This is the canonical
IQR-primary formula from Phase-1 D7 (EV-084). Exact match to P103 pilot calibration: 0.0g divergence.

**4. Asymmetric P>B structure confirmed**

P_max > B_max is the mandatory design per Phase-1 D7. Ratified. Exact P_max and B_max values
are set under D7-YS-01.

**5. Floor=62 / threshold=12.0g / Anti-Immunity confirmed**

Floor and threshold are ratified in Sections 3 and 4. Anti-Immunity proof: floor(62) + B_max(3) = 65 < 70. PASS.

**6. Named inversions confirmed — directionally correct and structurally real**

Both inversions are derived from committed `run_yogurt_006` trace files.

Inversion 1 (7290110321697 vs 7290102397600): 9.8g product scores 1.2pts lower than 13.6g
product. Cause is verified: lower additive count in the 13.6g product outweighs the sugar gap
in the current backbone. SR corrects this cleanly (both products in surcharge zone; higher sugar
→ higher z → larger penalty → ranking reversal). Pair is real and directionally correct.

Inversion 2 (7290102396740 vs 7290102393060): 4.5g product scores 7.1pts lower than 14.0g
product. Cause is verified: different NOVA_PROXY_4 confidence paths. SR partially corrects:
14.0g product receives +4pt surcharge; 4.5g product at z=−0.22 receives 0 under 0.5 threshold
(or minimal relief under the revised 0.3 threshold per D7-YS-04). Partial correction is the
correct and honest expectation — the 7.1pt gap reflects multiple backbone signals, not only sugar.
SR moves the relative signal in the correct direction. Both barcodes are confirmed movers in P103.

Both inversions are structurally real. Both qualify as named inversions per D6 rationale.

---

## Section 2 — D7-YS-01: P_max Decision

### Decision: P_max = 6 — BINDING

**The ruling:** Standardize at P_max=6. The pilot value of 8 is not adopted.

**Reasoning:**

The yogurt shelf's IQR=5.80g is tight relative to cereals (IQR=13.5g, scale=11.86) and biscuits
(IQR=6.9g, scale=5.115). However, the relevant calibration is in r-units (standardized), not
raw grams. At P_max=6, reaching the maximum surcharge requires z ≥ 2.5, i.e., sugars_g ≥
5.45 + (2.5 × 4.299) = 16.2g above median. No product in the corpus exceeds 14.0g — the maximum
surcharge band [2.5,∞) is populated only if a future product with >16.2g sugar is added. The
top practical surcharge in this corpus is band [1.5,2.5) → 4pts, applying to products at 9.1–16.2g
(the flavored and mix-in segment). This is proportionate.

Raising to P_max=8 would only change the behavior of products with z ≥ 2.5 — which are not
currently in the corpus. An 8-point maximum for a not-yet-present tier is speculation about
future products, not calibration to the current shelf. The principle of not over-designing for
hypothetical corpus expansions applies here. Standardization at 6 is the correct governance choice.

The pilot (P103) used P_max=8 as a diagnostic probe — that result confirmed mechanism validity
but does not bind the production enrollment parameters.

**Anti-Immunity check:** P_max does not affect anti-immunity. The floor (62) + B_max (3) = 65 < 70
regardless of P_max. PASS confirmed.

**Reversal condition:** If a corpus expansion adds products with sugars_g ≥ 16g and pilot shows
the 6pt maximum surcharge is insufficient to create meaningful rank separation from 12–14g
products, raise to P_max=8 at that time with a fresh D7.

---

## Section 3 — D7-YS-02: Floor Value Decision

### Decision: floor = 62 — CONFIRMED

**The ruling:** Floor=62 is confirmed at the proposed value.

**Reasoning:**

The calibration evidence from D6 is decisive: the highest-scoring product in the high-sugar
segment (7290102397600, 13.6g sugar) scores 62.4 at baseline — exactly at the proposed floor.
This means the floor binds at the correct precision: it is at the natural upper bound of the
current high-sugar yogurt backbone score range, not above it (which would impose additional
penalty beyond the backbone) and not below it (which would make it non-binding).

The floor's purpose is forward-looking: it prevents SR relief, backbone drift, or score inflation
from future model changes from pushing a high-sugar yogurt above grade C. Setting it at 62 (vs 63
or 65) uses the tightest defensible value while remaining above 60 (grade D boundary). This maximizes
the Anti-Immunity guard without over-constraining backbone behavior.

Note from D6: high-sugar yogurts (≥12g) receive surcharges under SR, not relief. The floor is
therefore a belt-and-suspenders guard against hypothetical future states, not a constraint that
fires today. The sole product near the floor (62.4) is already above it by 0.4pts — the floor
would round it to 62 in practice, which is the correct calibration.

**Anti-Immunity proof:** floor(62) + B_max(3) = 65 < 70. PASS. A high-sugar yogurt cannot reach
grade B (70) under any combination of floor + maximum below-median relief, because high-sugar
products are in the surcharge zone (above median), not the relief zone. The proof is doubly
protected.

---

## Section 4 — D7-YS-03: Floor Threshold Decision

### Decision: threshold = 12.0g — CONFIRMED

**The ruling:** The floor activates at sugars_g ≥ 12.0g.

**Reasoning:**

The corpus distribution shows Q3=9.7g. At 12.0g a product is approximately 4.2 raw grams above
Q3, placing it in the top ~15% of the corpus by sugar content. This is clearly "high sugar" in
the yogurt context — not borderline.

The alternative of 10.0g (above Q3) would include products that are only 0.3g above Q3 — the
boundary between the upper quartile and the 76th percentile is not a meaningful nutritional
distinction. The 10.0g threshold would apply the floor to products that receive only a 1–2pt
surcharge (z ≈ 1.06, band [1.0,1.5) → 2pts) — products that are moderately elevated, not
dessert-adjacent. The floor is a strong signal; it should apply only where the designation is
unambiguous.

At 12.0g, the z-score is (12.0 − 5.45) / 4.299 = 1.52, placing products at the [1.5,2.5)
surcharge band → 4pt penalty. This is the segment where the engine already signals "substantially
above shelf median." The floor at exactly this threshold creates clean alignment between the
maximum-surcharge activation and the floor activation — a product that receives a 4pt surcharge
also gets the floor guard, which is the intended behavior.

**Confirmed:** floor triggers at sugars_g ≥ 12.0g. Products below this threshold are not affected
by the floor regardless of their backbone score.

---

## Section 5 — D7-YS-04: Near-Median Relief Threshold Decision

### Decision: z-threshold = 0.3 — BINDING

**The ruling:** Products must have |z| ≥ 0.3 before SR fires. The 0.5 threshold is not adopted
for yogurt.

**Reasoning:**

The yogurt shelf has a clear bimodal structure: plain cluster at 2.5–5.0g vs flavored/mix-in
cluster at 9–14g. The plain cluster spans Q1 (3.9g) to near-median (5.45g). At a 0.5 z-threshold,
products within ±2.15g of the median receive zero SR adjustment. This means yogurts at 3.9g
(Q1) — genuinely low-sugar plain yogurts — fall within the dead zone (|z| = (5.45−3.9)/4.299 = 0.36
< 0.5) and receive no relief despite being meaningfully below median.

At a 0.3 threshold, products with |z| ≥ 0.3 (i.e., |sugars_g − 5.45| ≥ 1.29g) fire SR. This
captures the Q1-area plain yogurts at 3.9g (|z|=0.36 > 0.3 → band [0.5,1.5) via actual |z|
for the relief band lookup — wait: the threshold gates whether SR fires at all, and the relief
band is then looked up by the actual |z| magnitude). Products at 3.9g: z=−0.36 → |z|=0.36 ≥
0.3 → SR fires → z in [0.3,0.5) is still band [0,0.5) → 0pts. So the practical difference
between 0.3 and 0.5 is for products with |z| in [0.3,0.5): z-threshold gate passes but band
still returns 0.

Re-examination: the bands are [0,0.5)→0, [0.5,1.5)→2, [1.5,3.0)→3, [3.0,∞)→3. With a 0.3
z-threshold, products with |z| = 0.3–0.5 pass the gate but receive 0 relief from the band lookup.
With a 0.5 z-threshold, these same products are excluded at the gate before the band is consulted.
The outcome is identical for relief bands. The practical difference is only in the surcharge zone:
products with z in [0.3,0.5) above median would receive 0 surcharge from the band lookup, which
is also consistent with the 0.5 threshold approach.

However, the 0.3 threshold has value as a forward guard: it allows the implementation to fire and
log SR for near-median products without adjusting their score (band returns 0), which preserves
observability. This is better for the pilot audit than a hard gate exclusion that makes the
computation invisible in traces.

**Decision stands: z-threshold = 0.3.** Products with |z| < 0.3 (|sugars_g − 5.45| < 1.29g)
are excluded from SR computation entirely. Products with 0.3 ≤ |z| < 0.5 pass the gate, compute
the band, and receive 0 pts (band [0,0.5)). Products with |z| ≥ 0.5 proceed to the active
adjustment bands.

This is more traceable than 0.5 (near-median products appear in the SR trace with delta=0 rather
than being absent) and is consistent with the cereals implementation pattern where z=0.464 was
observed to have fired.

**Reversal condition:** If the pilot shows the 0.3 threshold creates trace noise without consumer
value (e.g., >20% of products appear as SR-fired with delta=0), raise to 0.5 for standardization.

---

## Section 6 — D7-YS-05: Null-Sugars Treatment Decision

### Decision: Option A — No adjustment (delta=0 for null sugars_g products) — BINDING

**The ruling:** Products with null sugars_g receive zero SR adjustment. They are excluded from
the SR computation entirely.

**Reasoning:**

Option A (no adjustment) is the correct choice and aligns with the missing-data discard rule
(owner standing, 2026-06-13: "if a product's data isn't found one-shot, DISCARD it"). The SR
mechanism expresses an opinion about a product's relative sugar position within the shelf — a
null value means we have no data to base that opinion on, so the opinion is withheld.

Option B (median imputation → z=0 → 0pt adjustment) is functionally equivalent to Option A
for any product that falls in the z < 0.3 dead zone — but it adds unnecessary computation and
creates a misleading trace entry where the SR computation appears to have fired with imputed data.
Imputed data in traces violates the data-provenance standard.

The pilot used median imputation because the diagnostic proxy (enrolling all `dairy_protein`)
needed a decision; the 14 null products received z=0 → band [0,0.5) → delta=0 in practice.
The outcome was identical to Option A for these products. Option A is cleaner: null → skip → no
trace entry → no imputation artifact.

The 14 null-sugars products are plain yogurt variants (כד yogurts, lactose-free, GO variants) —
based on product type, they are likely low-sugar. However, the engine does not infer values; it
requires observed data. These products are not penalized or rewarded by SR. Their backbone scores
are unchanged.

---

## Section 7 — Pilot Acceptance Gate (11 Criteria — Locked)

All criteria must pass before Phase-6 wire+pilot results are accepted. Any hard fail = stop.
C11 is documentation-only (not a blocker).

| # | Criterion | Name | Pass Condition | Class |
|---|---|---|---|---|
| C1 | resolution_restored | Resolution check | Fewer tied-score clusters at flag-on vs flag-off among the 74 yogurt products with non-null sugars_g. Measure: max products sharing an identical score decreases. | Hard |
| C2 | grade_dist_and_magnitude | Grade distribution + magnitude evidence | (A) 0 yogurts with sugars_g ≥ 12g at grade B (score ≥ 70) at flag-on. (B) ≥ 2 yogurts with sugars_g ≤ 5g at grade A or S (score ≥ 80) at flag-on. (C) mean\|clean_delta\| ≥ 0.5 among SR-firing yogurts. (D) mean clean_delta ≥ 0 for sugars_g ≤ 5g products (low-sugar cluster is not net-penalized). All four sub-conditions must hold. | Hard |
| C3 | inversion_gap | Named inversion gap | For at least 1 named inversion pair: lower-sugar barcode flag-on score minus higher-sugar barcode flag-on score ≥ +2.0 pts (inversion direction corrected with minimum gap). Inversion 1 pair: 7290110321697 (9.8g, baseline 61.2) vs 7290102397600 (13.6g, baseline 62.4) — after SR, 7290110321697 must score ABOVE 7290102397600 by ≥ 2.0 pts. Inversion 2 partial correction is expected but not required for gate pass (documented as directional, not full reversal). | Hard |
| C4 | min_movers | Minimum movers | ≥ 25 yogurt products (of 74 with sugars_g non-null) with clean_delta ≠ 0. P103 pilot showed 61 movers at 69% of corpus; the production scope guard (yogurt-only subtypes) may reduce this. 25 movers = ~34% of 74 — conservative floor. Below 25 movers with a spread shelf (IQR 5.8g) suggests scope or absorption issue. | Hard |
| C5 | min_grade_changes | Minimum grade changes | ≥ 1 yogurt grade change at flag-on vs flag-off. P103 pilot showed 8 grade changes; the production scope guard may reduce this. 1 is the minimum threshold below which the mechanism is meaningless. | Hard |
| C6 | max_absorption | Absorption rate | ≤ 40% of SR-firing yogurts show clean_delta = 0 despite SR term being non-zero before final application. P103 showed 0% absorption; ≤ 40% is a wide guard for a spread-y shelf. Absorption > 40% signals floor saturation or budget constraint — halt and investigate. | Hard |
| C7 | anti_immunity | Anti-Immunity hold | 0 yogurts with sugars_g ≥ 12g reach grade B (score ≥ 70) at flag-on. Applies the Anti-Immunity Rule to the full distribution, not spot-check. Any high-sugar yogurt at grade B = gate fail. | Hard |
| C8 | floor_compliance | Floor compliance | All yogurts with sugars_g ≥ 12g: flag-on score ≤ 62. Full distribution check, not spot-check. Include all products above the threshold regardless of baseline score. | Hard |
| C9 | no_scope_bleed | Scope isolation | 0 non-yogurt dairy_protein products (milk, hard cheese, brined cheese, kefir, cottage, cream cheese, ricotta) with non-zero clean_delta. Any movement outside CULTURED_YOGURT_SUBTYPES = scope enforcement failure. Verify by product subtype, not by assumption. | Hard |
| C10 | frozen_byte_id | Frozen milk byte-identity | milk run_005_headpin is byte-identical when BARI_SHELF_RELATIVE_V1=True (yogurt SR flag-on) vs committed milk baseline. This is the most critical safety check for yogurt×sugar: milk and yogurt share `dairy_protein`. If any milk product has `category_subtype in CULTURED_YOGURT_SUBTYPES` due to miscoding, SR would fire on milk scores — which are a FROZEN INVARIANT. Zero exceptions. Any milk score movement = immediate pilot FAIL regardless of other criteria. | Hard — CRITICAL |
| C11 | flag_off_drift | Flag-off documentation | Flag-off scores for all 87 yogurt-only products match run_yogurt_006 committed baseline. Mismatches documented (engine drift acceptable if explained; threshold: ≤ 10 mismatches out of 87 is informational). Documentation-only, non-blocking for gate pass. | Docs only |

### Named Inversions for C3

**Inversion 1 (primary C3 anchor):**

| Field | Product A (should rank higher after SR) | Product B (should rank lower after SR) |
|---|---|---|
| Barcode | 7290110321697 | 7290102397600 |
| Product | יופלה GO אפרסק | מולר מיקס שקדים ובוטנים |
| sugars_g | 9.8g | 13.6g |
| Baseline score | 61.2 / C | 62.4 / C |
| Expected z (surcharge) | (9.8−5.45)/4.299 = 1.01 → band [1.0,1.5) → 2pts | (13.6−5.45)/4.299 = 1.90 → band [1.5,2.5) → 4pts |
| Expected flag-on score | ~59.2 | ~58.4 |
| C3 pass condition | 7290110321697 flag-on > 7290102397600 flag-on by ≥ 2.0 pts | — |

**Inversion 2 (expected partial correction, informational):**

| Field | Product A | Product B |
|---|---|---|
| Barcode | 7290102396740 | 7290102393060 |
| Product | יוגורט אפרסק+תות 0% | יוגורט מולר מיקס גליליות |
| sugars_g | 4.5g | 14.0g |
| Baseline score | 36.4 / D | 43.5 / D |
| Expected z | (4.5−5.45)/4.299 = −0.22 → |z|=0.22 < 0.3 → excluded (delta=0) | (14.0−5.45)/4.299 = 1.99 → band [1.5,2.5) → 4pts surcharge |
| Expected flag-on score | 36.4 (unchanged) | ~39.5 |
| Direction | Gap reduced from 7.1 to ~3.1 pts — partial correction in correct direction | — |

Note: Under D7-YS-04 (z-threshold = 0.3), Product A (z=−0.22) is excluded from SR. Product B
receives 4pt surcharge. The gap narrows from 7.1pts to ~3.1pts — directional correction without
full inversion. This is the expected and honest outcome. C3 is gated on Inversion 1 only.

---

## Section 8 — Hard Conditions (All Blocking)

**Carried from Phase-1 D7 co-sign (EV-084):**

1. EV-084 registered — done at Phase-1 co-sign (line 1881, confirmed in registry).
2. `compute_shelf_stats()` IQR-primary default confirmed. Stats: median=5.45g, IQR=5.80g,
   scale=4.299g (IQR-primary). The engine must use the same formula: `max(IQR/1.349, 1.4826×MAD, 1.4)`.
3. n≥20 guard: non-binding (n=74 >> 20). Guard met.
4. Asymmetric P>B: P=6, B=3. Confirmed.
5. `formulation_absolute_floor` non-None: floor=62, threshold=12.0g. Confirmed.
6. Six-guard no-regression plan executes before merge. Guard-1 (milk byte-identical to
   run_005_headpin) is a hard gate — this is the same condition as pilot gate C10. Guard-2
   (all published categories byte-identical at flag-off) is mandatory. Both must pass.

**Yogurt-enrollment specific (added here):**

7. **Scope guard trace verification:** In the pilot output, at least 5 yogurt-subtype products
   must show the SR rule tag (`SUGAR_SHELF_REL_V1` or equivalent) firing in their BSIP2 trace.
   Tagless score movement is not auditable and is a gate fail.
8. **Non-yogurt dairy_protein trace verification (C9 extension):** Explicitly run one milk product
   (e.g., 7290000051352 from run_005_headpin) and one brined cheese product through the engine
   with BARI_SHELF_RELATIVE_V1=True. Confirm the SR tag is absent and delta=0. These are the
   highest-risk bleed targets given the shared `dairy_protein` routing.
9. **Null-sugars pass-through confirmation:** At least 3 of the 14 null-sugars yogurt products
   must appear in pilot output with delta=0 and no SR trace tag — confirming Option A (no
   adjustment) was implemented correctly.
10. **EV-085 and EV-087 biscuit/cereal path byte-identical:** Adding yogurt to scope must not
    move any biscuit or cereal product's score. Confirm from pilot traces.

---

## Section 9 — Tripwire Assessment

**No tripwire fires on this co-sign.**

- Frozen invariants: not touched. Milk scores (run_005_headpin) are unchanged by this co-sign.
  The pilot gate C10 enforces this at implementation time. Flag default=off. Zero score movement.
- Consumer-facing / irreversible: not applicable. The yogurt category is not live with SR enabled.
  The pilot rescore is internal. Owner go-live gate (tripwire-1) is required before any published
  movement — that gate is separate and not part of this co-sign.
- Major program start/kill: this is Phase 6 of an already-approved program (TASK-278, D7 Phase-1
  co-signed 2026-06-14).
- External commitment/spend/legal: none.
- Strategy redefinition: not applicable.

**Owner escalation: NOT required.** This co-sign is within the D7 lane. The first published
score movement (owner go-live for yogurt page with SR) is the tripwire-1 gate that escalates.

---

## Decision Log

| Item | Options considered | Choice | Decisive reason | Reversal condition |
|---|---|---|---|---|
| P_max | (a) P_max=6 (standardized); (b) P_max=8 (pilot value) | (a) P_max=6 | No corpus product reaches z≥2.5 (the band that differs between 6 and 8); pilot used 8 as a diagnostic probe, not a production commitment; standardization reduces rule accumulation risk | Raise to P_max=8 if corpus expands to include yogurts ≥16g sugar and 6pt maximum fails to differentiate them from the 12–14g segment |
| Floor value | (a) 62 (proposed); (b) lower (e.g., 60); (c) higher (e.g., 65) | (a) 62 | Highest-scoring high-sugar corpus product (62.4) is exactly at this value; floor=60 would be inside the product's current range; floor=65 narrows Anti-Immunity headroom to 2pts (too close to grade B at 70) | Recalibrate if corpus adds products scoring above 62 baseline despite ≥12g sugar |
| Threshold | (a) 12.0g (proposed); (b) 10.0g (above Q3) | (a) 12.0g | 10.0g is only 0.3g above Q3 — not a meaningful nutritional boundary; 12.0g aligns floor activation with the 4pt-surcharge band (z≥1.52) — both signals fire at the same threshold; "dessert territory" is the correct designation frame | Lower to 10.0g if pilot shows 10–12g products are systematically misranked and the floor would help |
| Near-median z-threshold | (a) 0.5 (D6 proposal); (b) 0.3 (more inclusive); (c) none (let B_max cap) | (b) 0.3 | 0.3 captures the Q1 plain yogurt cluster (3.9g, z=0.36) in the SR trace with delta=0, which is more observable; cereals fired at z=0.464 (below 0.5), setting a practical precedent; B_max=3 alone at 0.5 threshold would exclude plain-cluster products from traceability | Raise to 0.5 if pilot traces show >20% of products appearing as SR-fired with delta=0 (noise without value) |
| Null-sugars treatment | (A) no adjustment; (B) median imputation → z=0 → delta≈0 | (A) no adjustment | Missing data = no SR opinion; imputation creates misleading trace entries; outcome is identical to (A) for all current corpus products at z=0 → band[0,0.5)→0pts; aligns with owner's missing-data discard rule | No reversal — if future implementation requires a default, confirm with Nutrition Agent |
| Scope guard option | (A) category_subtype in CULTURED_YOGURT_SUBTYPES; (B) dedicated yogurt router category; (C) barcode frozenset | (A) subtype check | Zero new infrastructure; constant already in codebase; fermentation bonus gate uses same pattern; options B and C are more invasive or brittle | Move to Option B (router category) only if subtype field is found absent for yogurt products in production corpus |

---

## EV-088 Registration

EV-088 is registered in `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md`
as part of this co-sign. See the append operation for the full registry entry.

The D7 decisions above (P_max=6, floor=62, threshold=12.0g, z-threshold=0.3, null→no adjustment)
are the binding parameters for the implementation in the next phase (wire + pilot rescore by Data Agent).
