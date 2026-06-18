# Shelf-Relative Differentiator — Product Agent D7 Co-Sign
**Task:** TASK-278 — Project Rescore (Bari-wide program)
**Date:** 2026-06-14
**Author:** Product Agent
**Verdict: CO-SIGN APPROVED WITH CONDITIONS**
**Scope:** Design governance only — `shelf_relative_design_v1.md` (Nutrition Agent, sha `a2f3e9ef…`).
No engine code change. Zero score movement.

---

## Verdict: CO-SIGN APPROVED WITH CONDITIONS

The design is sound. The architecture is correct. The owner's two philosophy calls (A and B) are
correctly baked in. The one divergence between the design and C3 (one-sided-high vs. asymmetric
limited relief) is resolved below with a single call. Six hard conditions are recorded; none are
waived.

EV-084 is registered on this co-sign (§7 of the design, trigger fulfilled).

---

## Section 1 — Design Soundness

### 1.1 Parameterized `shelf_relative_differentiator()` — CONFIRMED

The function contract is clean: `value`, `nutrient`, `scope_categories`, `surcharge_bands`,
`low_variance_guard`, `direction`, `mapping`. All policy inputs are parameters — the function
contains no hardcoded category or nutrient logic. Any per-category configuration is a constants
lookup external to the function. This is the correct architecture for a category-agnostic module
and directly prevents the rule-accumulation failure mode C3 identified as the 3-month risk.

One note: the `mapping` parameter currently routes `clamped_linear` and `tanh` to the banded
fallback with a comment "Pending C3 decision." This is acceptable for the design phase — the
banded fallback is safe and auditable — but the final implementation must resolve the mapping
choice at D7 per nutrient enrollment, not leave the dead paths as permanent stubs. Banded is
the co-signed default (see §3 below).

### 1.2 `BARI_SHELF_RELATIVE_V1` default-off flag — CONFIRMED

Flag design is correct. Default-off, env-var gated, byte-identical guarantee when off. The
existing EV-056 path (`_shelf_sodium_active` block) is not touched by the new flag. Both flags
coexist independently. The flag declaration is explicit on this; the call-site architecture
(`if BARI_SHELF_RELATIVE_V1:`) is the correct guard pattern.

### 1.3 EV-056 COEXISTENCE, not premature replacement — CONFIRMED

The design correctly defers EV-056 migration to a future validated D7. §8 of the design
flags this explicitly (spec-conflict note #1): the brief's "generalizes/replaces" language is
premature, and the design correctly rejects silent replacement before the generalized mechanism
is validated on the brined-cheese corpus. This is the right call — it is the RC1/RC3 failure
class to execute a migration before validation. The design specifies coexistence; replacement
remains a future separate D7.

---

## Section 2 — Owner Philosophy Calls Baked In Correctly

### 2.1 Call A — One Absolute Scale (CONFIRMED CORRECTLY IMPLEMENTED)

The design implements Call A via Branch A of Fork 1 (§4 design): the absolute backbone uses
global bands (`SODIUM_GENERAL_BANDS`) as the universal anchor. Category specificity comes from
the scope guard and the relative surcharge bands. The `NUTRIENT_ABSOLUTE_BANDS_BY_CATEGORY`
constant is available for per-category overrides but is NOT the default — the default is the
global band. This is exactly right for "one absolute scale with within-envelope relative
refinement."

The `score = clamp(absolute + bounded_relative, floor, ceiling)` integration rule from C3 is
the correct blending mechanism. The design implements this via the additive model with
`clip(absolute_backbone_pen + shelf_relative_surcharge, 0, family_budget)` and the category
ceiling. This is NOT a fixed-weight blend — the absolute backbone score stands on its own and
the relative layer is bounded. Co-signed.

Confirmations required at parameter finalization:
- The relative component may move a product at most one letter grade from its absolute position.
- The relative component may never create A-grade eligibility in an indulgence category.
- Category ceilings (`max_score`) remain authoritative over both layers combined.

### 2.2 Call B — Relative Everywhere + Firm Absolute Floor (CONFIRMED CORRECTLY IMPLEMENTED)

The design implements Call B via Branch B of Fork 2 (§4 design): the `formulation_absolute_floor`
parameter enforces Anti-Immunity for formulation nutrients. Sugar in biscuits gets relative
treatment AND an absolute floor that prevents curve-grading immunity. The old
"endemic→relative / formulation→cliff" binary is retired by this design.

This is sound. The Anti-Immunity Rule is protected architecturally — no biscuit with high sugar
reaches A — without requiring a blanket exclusion of the relative layer. The floor value per
category/nutrient is a D7 rollout decision, not a design-time constant, which is the correct
separation.

Confirmed: `formulation_absolute_floor` is the mechanism. Its per-category value is NOT set in
this co-sign — it is a binding commitment at each rollout D7. No floor, no rollout.

---

## Section 3 — Math Reconciliation: One-Sided Call

### The divergence

The design defaults to `direction="one_sided_high"`: fire only when `value > median`; products
below median receive no shelf-relative penalty AND no shelf-relative reward. This is pure
one-sided-high — no below-median relief at all.

C3 recommends asymmetric two-sided: `penalty P > relief B`, with `r_neg` giving limited
below-median relief. Example: max penalty 6 pts, max relief 3 pts (`P > B`). Products above
median are penalized more than products below median are rewarded. Both directions are active;
asymmetry prevents below-median relief from laundering an otherwise-bad product.

### The call: ADOPT C3 — ASYMMETRIC P>B

Recommendation: asymmetric `P > B`, not pure one-sided-high.

Reason: pure one-sided-high achieves the product ranking goal (above-median products are
differentiated) but fails the consumer honesty test at the bottom of the scale. A biscuit with
sugar at 12g/100g on a shelf where the median is 28g/100g is genuinely better than the median
product — materially, not just marginally. Giving it the same relative treatment as a product
at the median (zero relief either way) misrepresents the differentiation the engine should
provide. If Bari is replacing binary cliffs with resolution, suppressing valid below-median
signal is a half-solution.

The guard is asymmetry. `P > B` (e.g. 6 pts max penalty, 3 pts max relief) means
below-median relief can never launder a product that the absolute backbone has correctly
identified as problematic. A biscuit at 12g sugar still runs through the full absolute backbone
(including NOVA, fat, ingredients penalties). The relative relief is bounded and cannot create
A-eligibility. Anti-Immunity is held by the absolute floor, not by refusing to model the
below-median signal at all.

Reversal condition: if empirical pilot calibration shows below-median relief is consistently
used by the least-bad product on a bad shelf to reach an implausibly good composite score
(above the `formulation_absolute_floor`), revert to one-sided-high for that nutrient/category
and log as a calibration failure.

### IQR-primary scale adoption

The design defaulted to `stdev`. C3 is unambiguous: for right-skewed distributions and
n=20–60, use `max(IQR/1.349, 1.4826·MAD, min_scale)`. The design accommodates this via the
`scale_type` parameter. Co-sign mandates IQR-primary as the implementation default:

```
robust_scale = max(IQR / 1.349, 1.4826 * MAD, nutrient_min_scale)
```

`stdev` is retained as a fallback for future cases where IQR collapses, but it is NOT the
default. The `compute_shelf_stats()` function must implement IQR-primary before any pilot run
executes. The current implementation computes median correctly but defaults to population stdev
— this must be updated at implementation time.

The n≥20 minimum corpus guard (C3's recommendation, more stringent than the design's n≥10)
is adopted. n<20 = relative component suppressed, regardless of IQR spread.

---

## Section 4 — Anti-Rule-Accumulation

C3's primary 3-month risk is rule accumulation — Bari already has absolute penalties, caps,
NOVA, ingredient logic, and category exceptions; adding per-category bespoke relative functions
could make the system impossible to reason about.

Co-sign holds the following constraint as a hard implementation gate, not a preference:

**ONE generic config-driven module. NO bespoke per-category scoring functions.**

This means:
- Every category/nutrient enrollment uses the same `shelf_relative_differentiator()` function.
- Per-category differentiation is entirely in configuration constants (`scope_categories`,
  `surcharge_bands`, `formulation_absolute_floor`, `low_variance_guard`) — not in code branches.
- If a category's enrollment requires a new code function rather than new config, that is a D7
  red flag requiring explicit justification before approval.

The relative component is a "within-shelf differentiation residual" — C3's framing is
adopted. It is NOT a second full nutrient penalty. The family budget mechanism enforces this:
`clip(absolute + relative, 0, family_budget)`. Any family budget raise at rollout is a D7
decision that must justify why the combined penalty is not double-counting the same signal.

---

## Section 5 — Rollout Governance

### 5.1 Each enrollment is its own D7

Every category/nutrient activation requires:
1. Its own EV entry in the evidence registry.
2. A Nutrition Agent + Product Agent D7 co-sign for that enrollment.
3. A full cross-corpus baseline diff across ALL published categories (not just the target).
4. Owner go-live before any published score moves (tripwire-1; non-negotiable).

This is already in the design's §6 "Additional guard for each category enrolled at rollout."
It is ratified here as a governance commitment, not merely a plan.

### 5.2 Phase-2 pilot — biscuits × sugar, sugar alone

The pilot is confirmed as: **biscuits × sugar, sugar only**. Not sugar + satfat together.
The pilot is a stress test, not a safe test — biscuits/sugar is the hardest philosophical
case (formulation-choice nutrient, indulgence category, known cliff damage, high curve-grading
risk). A safer first category would prove the code works but not that the model solves the
real problem.

**Pilot success criteria (all must pass; any failure = do not ship):**

| Criterion | Pass condition |
|---|---|
| Resolution restored | Fewer products pinned at identical cliff scores vs. baseline run |
| Rank order improvement | Obvious rank inversions under hard cliff are corrected (name at least 2 expected inversions before pilot runs, verify each) |
| Shelf average stable | Shelf average score does NOT float materially upward vs. absolute-backbone-only baseline (threshold: ≤1.5 pt average lift) |
| Anti-Immunity holds | No indulgence product (sugar ≥ 20g/100g) reaches grade A |
| Absolute floor enforced | `formulation_absolute_floor` prevents any high-sugar product from reaching the approved score ceiling |
| Flag-off byte-identical | Re-score all published categories with `BARI_SHELF_RELATIVE_V1=off` = zero movement |
| No cross-category contamination | Enrolled biscuit corpus enrollment does not move any non-biscuit published score |

The pilot success criteria must be documented in writing BEFORE the pilot run executes. Writing
them after seeing results is disqualifying.

### 5.3 No published-score movement without owner go-live

This is tripwire-1. No exception. The flag default-off guarantee is the mechanical enforcement;
the owner go-live gate is the governance enforcement. Both must hold simultaneously.

---

## Section 6 — Hard Conditions

All conditions are blocking. Implementation does not proceed without each.

1. **EV-084 registered.** Write EV-084 into `bsip2_evidence_registry_v1.md` as part of this
   co-sign. (Done in this document — see §7 of design; registry line confirmed in §Return below.)

2. **IQR-primary scale at implementation.** `compute_shelf_stats()` defaults to
   `scale_type = "iqr"` (implementing `max(IQR/1.349, 1.4826·MAD, min_scale)`), NOT
   `scale_type = "stdev"`. The function signature may keep `scale_type` as a parameter for
   override capability, but the default must change from `"stdev"` to `"iqr"` before any pilot
   run.

3. **n≥20 minimum guard.** The `min_n` parameter default changes from 10 to 20 in the
   implementation. Any corpus below 20 observed products with the target nutrient = relative
   component suppressed.

4. **Asymmetric P>B direction at pilot.** For biscuits × sugar pilot, `direction` must be set
   to permit below-median relief with `P > B` (not pure `"one_sided_high"`). The exact P and B
   values are a Nutrition Agent call at rollout D7, but the direction parameter must support the
   asymmetric mode (it does — the function signature allows it; this is a parameter config call
   at enrollment, not a code change).

5. **`formulation_absolute_floor` is required at biscuit/sugar enrollment.** The pilot D7
   co-sign is blocked if no floor value is proposed. A pilot run with floor=None for a
   formulation nutrient is not permissible — it removes the Anti-Immunity guard for the
   highest-risk case.

6. **Six-guard no-regression plan (§6 of design) executes before merge, not after.** Guards
   1–6 are prerequisites, not post-merge verifications. Guard 2 (flag-off byte-identical across
   all published categories) and Guard 1 (milk byte-identical) are the hardest gates and must
   pass with zero exceptions.

---

## Section 7 — OFF-Ban Confirmation

The mechanism reads only `normalized_nutrition_per_100g[nutrient]` — the label-panel field
already present in BSIP1 traces from direct product scrape. The `compute_shelf_stats()` function
has an explicit OFF-BAN comment in the design. The corpus shelf stats are computed from those
same BSIP1 label fields; no external source is involved. OFF-ban is architecturally satisfied
by this design. Any future enrollment that attempts to feed `compute_shelf_stats()` from a
non-label source is a D7 blocking condition.

---

## Section 8 — EV-056 Coexistence Verification Requirement

Guard 4 of the no-regression plan (EV-056 sodium path byte-identical with `BARI_SHELF_RELATIVE_V1=off`)
is a required pre-merge check. This is co-signed as a binding commitment. The brined-cheese
corpus is a live published category; any interference from the new general flag with the
existing sodium/dairy path is a hard stop.

At a later date, when migrating EV-056 to use the generalized function:
- That migration is a separate D7 requiring a new EV entry, full brined-cheese corpus diff, and
  owner go-live confirmation.
- The migration may not be bundled with the biscuits×sugar pilot or any other enrollment.

---

## Decision Log

| Item | Options considered | Choice | Decisive reason | Reversal condition |
|---|---|---|---|---|
| One-sided vs asymmetric P>B | (a) Pure one-sided-high (design default); (b) Asymmetric P>B (C3 rec) | (b) Asymmetric P>B | Pure one-sided-high suppresses valid below-median signal; P>B preserves it with guard via asymmetry; Anti-Immunity held by formulation_absolute_floor not by suppressing the signal | Revert to one-sided-high for a nutrient/category if below-median relief enables implausible scores despite floor |
| IQR-primary vs stdev default | (a) stdev (design default); (b) IQR-primary: max(IQR/1.349, 1.4826·MAD, min_scale) (C3 rec) | (b) IQR-primary | Right-skewed distributions at n=20–60 make stdev fragile; IQR is more stable for nutrition labels; C3 unambiguous | Revisit if IQR collapses to zero more often than stdev on real corpora (then stdev as explicit fallback, logged) |
| n≥10 vs n≥20 minimum guard | (a) n≥10 (design default min_n); (b) n≥20 (C3 rec) | (b) n≥20 | Smaller corpora produce unstable stats that create fake precision and audit-hostile outcomes; C3 recommendation with principled basis | Revisit for enrolled categories that structurally cannot reach n=20 — requires explicit evidence that the corpus is stable at that n |
| Pilot scope: sugar alone vs sugar+satfat | (a) Sugar alone; (b) Sugar + satfat together | (a) Sugar alone | Conflating effects prevents clean causal read on pilot results; stress-test the model on one nutrient before adding the second | Satfat enrollment follows the same pilot-then-D7 path, not bundled |
| Owner escalation on this co-sign | (a) Escalate (design-only, no scores move); (b) D7 lane sufficient | (b) D7 lane | No tripwire fires: default-off flag, zero published score movement, design is reversible, no consumer-facing change | Escalate immediately if any guard fails during implementation that moves a published score |
