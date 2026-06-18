# Additive-Cocktail Cluster — D6 Scoring-Rule Proposal v1

**Status:** PROPOSED (Nutrition-initiated 2026-06-12) — **awaiting Product D7 co-sign**
**Evidence:** EV-051 (extends EV-045) — `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md`
**Tracking:** TASK-261
**Flag (proposed):** `BARI_ADDITIVE_COCKTAIL` (default OFF → byte-identical)

---

## 1. What this is (and is not)

**Is:** a single, bounded *interaction term* added inside the existing EV-045 emulsifier/stabilizer
complexity tier, anchored on a human prospective-cohort T2D outcome (NutriNet-Santé).

**Is not:** a new scoring dimension, a new per-additive penalty, or a replacement for any existing
rule. EV-045 already counts multiple texture-stabilizing agents as a complexity signal; EV-003
already differentiates individual concern-tier emulsifiers; EV-041/043 already tier additives for
D4 display. This proposal does **one** thing on top of those: it recognises the *specific
co-occurring cluster* the evidence flags as carrying interaction risk that the linear sum of
EV-045 + EV-003 does not capture.

This deliberately avoids rule accumulation (B2 scoring-governance): the default outcome if
calibration shows no marginal discrimination is **do nothing** — the evidence upgrade to EV-045
stands on its own.

## 2. Evidence basis

| Source | Design | Finding used |
|---|---|---|
| PLOS Medicine 2025, doi `10.1371/journal.pmed.1004570` (NutriNet-Santé, N=108,643, 7.7y) | Prospective cohort, mixture modelling | "Mixture 2" — modified starches + pectin + guar gum + carrageenan + polyphosphates + potassium sorbate + curcumin + xanthan gum — associated with higher T2D incidence |
| Lancet Diabetes & Endocrinol 2024, doi `10.1016/S2213-8587(24)00086-X` (NutriNet-Santé) | Prospective cohort | Individual emulsifiers (E407, tripotassium phosphate, E471) independently associated with T2D — corroborates EV-003 |

Evidence tier **B** (observational; no RCT on the mixture endpoint). Per Nutrition Hard Rule #6,
this supports a **bounded** effect with a flag/disclosure posture — never a large deduction.

## 3. Proposed signal (presence-based; quantities are not label-observable)

```
modified_starch_present = any(E1404|E1412|E1414|E1422 | "עמילן מומס" | "עמילן מעובד" | "modified starch")
gum_count               = count(guar | xanthan | carrageenan | pectin | locust bean | tara)   # EXCLUDES gum arabic / acacia (EV-019)
emulsifier_count        = tax_emulsifier_concern ∪ tax_emulsifier_medium ∪ tax_emulsifier_low   # EV-045 signals, reused

cocktail_flag = modified_starch_present AND (gum_count >= 1) AND (emulsifier_count >= 1)
```

`modified_starch_present` is a **mandatory** AND-term: it is the engineered signature that prevents
naturally pectin/gum-containing whole foods (fruit prep, plant foods) from tripping the flag.

## 4. Activation scope & the four gates (all must clear before any score moves)

1. **Anti-double-counting (load-bearing).** Most `cocktail_flag = true` products are already
   NOVA-4 and already carry EV-045 complexity + EV-003 deltas. **Required proof before activation:**
   a golden-corpus + per-live-category simulation reporting the *marginal* Δscore attributable to
   the flag, **net of EV-045 / EV-003 / NOVA**. If marginal discrimination ≈ 0, the rule is **not
   activated** (evidence upgrade to EV-045 only).
2. **Bounded penalty.** Proposed ceiling **−3**, applied **inside EV-045's existing −6 complexity
   cap** (not additive beyond it). Observational evidence does not justify more.
3. **Natural-matrix false-positive guard.** Mandatory `modified_starch_present` + EV-019 gum-arabic
   exclusion. Calibration must report any clean whole-food caught.
4. **D7 co-sign.** Nutrition (initiated) + **Product (pending)**. Frozen invariants re-verified
   unmoved: milk `run_005_headpin` (85/A), snack `snk-001` (70/B), bread `retail_003`.

## 5. Calibration plan (TASK-261)

| Step | Owner | Output |
|---|---|---|
| a | Research Agent | Confirm both DOIs; extract mixture-2 additive list verbatim into an evidence sheet |
| b | Data Agent | Run `cocktail_flag` over golden corpus + each live category; report cluster-positive frequency + marginal Δscore net of EV-045/EV-003/NOVA; list any clean whole-food false positives |
| c | Nutrition Agent | Set bounded penalty (≤ −3, within EV-045 cap) **only if** marginal discrimination is shown; else recommend no-activation |
| d | Product Agent | D7 go/no-go |

## 6. Consumer-facing framing (Hard Rule #5)

Permitted: *"combines modified starch with several texture-stabilising additives."*
Forbidden: any health-outcome claim — "causes diabetes," "toxic," "unsafe," "high dose." The study
is an association, not causation, and Bari scores nutritional architecture, not health outcomes.

## 7. Rollback

Single flag `BARI_ADDITIVE_COCKTAIL`, default OFF → engine byte-identical; no published score moves
while OFF. No engine code ships with this proposal. Reverting = `git revert` of EV-051 + this doc.
