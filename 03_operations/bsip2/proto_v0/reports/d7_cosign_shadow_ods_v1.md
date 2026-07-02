# D7 Co-Sign — Shadow Run Open Decisions (OD-1 through OD-4)
**Proposal Class:** D7 (Product Agent — business and scope defensibility co-sign)
**Task:** TASK-395
**Date authored:** 2026-06-25
**Status:** D7 CO-SIGN — design authorization only. No engine code changed. No scores changed.
**Depends on:**
- `d6_ratify_shadow_ods_v1.md` (Nutrition ratification — read in full before this ruling)
- `shadow_run_plan_v1.md` (Part A integration design + four ODs — read in full)

---

## Preamble

This co-sign applies the defensibility lens: for each ratified value, will the resulting score movement be EXPLAINABLE — to the owner as a methodology decision and to a consumer as a product verdict? I am not re-litigating the nutritional science (D6 owns that) nor the implementation design (Data Agent owns that). I am ruling on whether each value, as calibrated, clears the "would we be embarrassed if this ran live" bar — while holding firmly to the shadow-only constraint that the owner gates any deploy after seeing the movement table.

A value can be defensible as a shadow-run parameter even if it would need tuning before production. The standard here is: can we stand behind the measurement? A shadow run that produces a wrong number at a defensible value teaches us exactly the right thing. A shadow run at an indefensible value teaches us nothing actionable.

---

## OD-1 — Flat Per-Additive Penalty P = 14

**D7 Ruling: CO-SIGN**

**Defensibility verdict:** Explainable. "This product contains N additives; each costs 14 points on the processing load score" is a simple, auditable rule. A consumer or owner can reconstruct the Component A score from the ingredient count in the trace. There is no black box.

**Business defensibility check:** The D6 rationale correctly identifies P = 14 as a weighted-average approximation of the D4 tier hierarchy — approximately right for Tier 2 additives (the modal case in Israeli retail processed foods), too harsh for five-additive products where all five are low-risk. I accept that as a known and intentional distortion: it is the cost of running D4 off, and the shadow run is explicitly designed to make that distortion visible in the top-movers table. A finding that P = 14 over-penalizes citric acid + lactic acid + ascorbic acid bundles is a productive shadow finding, not a failure.

**Clean-label refined-starch exposure at P = 14:** a zero-additive product scores 95 on Component A. D6 flags this correctly. At 0.60 weight, it contributes 57 to the combined score. Component B must carry the guard for clean-label junk. This is the right architectural assignment — the shadow run's job is to verify whether Component B can hold it. P = 14 does not make that verification harder; it keeps Component A honest for genuinely additive-heavy products while letting Component B carry its weight.

**Reversal condition:** If the shadow movement table shows systematic over-penalization in categories where the dominant additive profile is demonstrably low-risk (e.g., juices scoring D on processing_quality because of citric acid + color alone), P should be reduced to 10 or D4 should be activated for Stage 1. That is a post-shadow calibration decision, not a reason to block the shadow now.

---

## OD-2 — Component A / B Blend 0.60 / 0.40

**D7 Ruling: CO-SIGN**

**The specific question I was asked to judge:** Does 0.60/0.40 adequately stop clean-label refined-starch junk from winning?

**Answer: Yes — barely, and correctly barely.** The D6 rationale demonstrates the arithmetic: a palm-oil + refined-flour + sugar product with zero additives scores 0.60 × 95 + 0.40 × 14 = 62.6 combined, before the NOVA modifier. After a NOVA-4 modifier of −10 (high confidence) it lands at 52.6, which is solidly C. That is the right verdict for a product that is nutritionally unremarkable but not a health risk. A C is not a win for refined-starch junk — it is the verdict that correctly says "this is a processed product with no redeeming structural complexity." The guard holds.

**Would 0.70/0.30 fail it?** At 0.70/0.30, the same product scores 0.70 × 95 + 0.30 × 14 = 70.7, minus NOVA modifier → 60.7. That is a borderline C/B, which I would consider too permissive. 0.40 is the minimum weight that makes Component B a genuine structural guard. D6 confirms this with the same arithmetic. I agree.

**Is Component B too light at 0.40?** No — not for a shadow run. 0.40 is a meaningful weight, not a token one. Its limitation is not structural weakness but coverage: if too many products fall into the position-only inference path, the 0.40 weight amplifies noise rather than signal. The read-mode breakdown artifact (shadow_read_mode_breakdown_v1.json) is the right diagnostic for this. I flag the following: if that report shows >30% of the shadow corpus on position-only inference (not the 20% D6 mentions — I am setting a tighter alert threshold for the owner review), the D7 co-sign on OD-2 carries a conditional: we should revisit whether 0.40 is appropriate or whether Component B's weight should be reduced to 0.30 until the stated-percentage coverage improves. This is a post-shadow decision gate, not a blocker now.

**Defensibility verdict:** Explainable. "The additive load carries 60% of the processing quality score because it is more precisely observable; the ingredient structure carries 40%" is a clean methodology statement. We can say this publicly.

**Reversal condition:** If the shadow read-mode breakdown shows >30% position-only inference AND those products show unexpectedly large and directionally inconsistent movements, revisit the weight downward to 0.30 for Stage 1.

---

## OD-3 — NOVA Subordination Modifier NOVA-4 = −10, NOVA 1-2 = +5, NOVA-3 = 0

**D7 Ruling: CO-SIGN**

**The specific question I was asked to judge:** Is −10 "meaningful but subordinate" as intended, or so small that NOVA effectively stops mattering?

**Answer:** −10 is meaningful and correctly subordinate. Here is the defensibility arithmetic. A NOVA-4 product with Component A = 58 and neutral Component B = 50 combines to 54.8 pre-NOVA. After −10 it lands at 44.8 — a move of roughly one sub-grade, from mid-C toward D. That is real movement. It is not a cliff (the old step-lookup cliff to 35 is gone), but it is not noise either. A consumer can understand: "this is a heavily processed product — its NOVA-4 classification pushed it further down than its ingredient count alone would."

**The risk D6 identifies — does −10 disappear for clean-label NOVA-4 products?** A NOVA-4 product with additive_marker_count = 0 scores 95 on Component A. With a modest matrix signal (Component B = 50): combined = 0.60 × 95 + 0.40 × 50 = 77. After −10 modifier: 67. The N-3 cap at 68 then fires and brings it to 68. So the combined effect of OD-3 (−10) and OD-4 (cap at 68) correctly caps this clean-label NOVA-4 product at 68 — a C+. That is borderline acceptable but not generous. If a product is genuinely NOVA-4 (correct classification, high confidence) and has zero detectable additives and a modest matrix, 68 is a defensible ceiling: we are saying "we know this is an ultra-processed product; the structural signals cannot see why, but the ceiling holds." This is what the N-3 cap is for. The two ODs are complementary guards for precisely this case.

**Would −15 be better?** D6 argues persuasively that −15 risks making NOVA dominant again — a NOVA-4 misclassification on a genuinely minimal product would impose a 15-point penalty on a clean structural signal. I agree. −10 is the right magnitude to trust in a shadow where we have not yet validated NOVA classification accuracy at scale. If the shadow shows NOVA-4 products systematically escaping via low additive counts AND Component B is also failing them (read-mode = no_markers or position-only), then −15 is the Stage 1 correction. But that decision should be made on the movement table, not preemptively.

**On NOVA-3 = 0:** Defensible and correct. NOVA-3 is too heterogeneous for a directional modifier. Any modifier applied to NOVA-3 as a class would produce unexplainable movements for sourdough bread (correct NOVA-3) vs protein bars with isolated protein (also sometimes NOVA-3). Letting Components A and B differentiate is the right design.

**Defensibility verdict:** Explainable. "NOVA-4 classification gives an additional −10-point depression on the processing quality score. NOVA is a check on the structural signals, not the primary driver" is a clean public statement. We can defend this to a food scientist and a consumer.

**Reversal condition:** If the shadow shows NOVA-4 products with additive_marker_count ≤ 1 scoring above 60 in Column D (the specific cross-check D6 flags in the Cross-OD Notes), and the read-mode breakdown shows these products are NOT on position-only inference (i.e., the matrix signal has genuine data and is still failing), revisit modifier to −15 for Stage 1.

---

## OD-4 — N-3 NOVA-4 Composite Cap at 68

**D7 Ruling: CO-SIGN**

**This is the clearest of the four.** Keeping the cap at 68 during the shadow run is unambiguously correct from a product defensibility standpoint: we are measuring the candidate engine under the existing safety structure, not designing a new one. A shadow run that relaxes the cap would produce results we cannot compare against the current baseline — we would not know whether movement comes from the candidate engine or from cap relaxation. That conflation would make the movement table useless as an owner input.

**The diagnostic value D6 identifies is exactly right:** the shadow run's anomaly report will distinguish cap-binding (continuous score > 68, cap is doing work) from cap-coincidental (continuous score ≤ 68, cap is inert). High proportion of cap-coincidental NOVA-4 products = the candidate engine has made the cap redundant → empirical evidence for Stage 1B disposition. This is the data we need. We cannot generate it without running the shadow at 68.

**Defensibility verdict:** The cap is a governance instrument, not a scoring claim. Its presence in the shadow run does not need to be explained to a consumer — it is an internal safety backstop. The owner decision on Stage 1B (raise to 78 or remove) is gated on the shadow results, which is the correct sequencing.

**Reversal condition:** None for the shadow run. Stage 1B disposition is governed by the proportion of binding-cap products in the shadow anomaly report, per target spec §5.1.

---

## Cross-OD Defensibility Notes

**The missing-ingredient-text fallback (Component A only):** D6 flags products with unparseable ingredient text as a coverage gap producing an artificially high Component A (score = 95). From a defensibility standpoint, I flag this as an owner-review item: if any of these products appear in the shadow top-movers as large upward movers, the cause is the fallback, not the candidate engine. The anomaly report's COMPONENT_B_NONE class is the right diagnostic. The owner should not interpret upward movement in COMPONENT_B_NONE products as a validation of the candidate engine — it is a coverage gap reporting as a score.

**The OD-1 / OD-3 clean-label NOVA-4 interaction:** I have worked through this in OD-3 above. The N-3 cap (OD-4) acts as the final backstop when both signals fail. The three ODs are coherent as a system.

**What the shadow run can and cannot tell us:** The shadow run can tell us the candidate engine's score distribution, its top movers, its read-mode breakdown, and where the N-3 cap is still doing work. It cannot tell us whether NOVA classifications are correct at scale (that requires a BARI-INVERSION-TEST-001 adversarial fixture set, which D6 correctly flags as not-done). The owner should read the movement table as "what would scores look like under this candidate" — not as "these scores are correct." The deploy gate (owner-reviewed, tripwire 2) is what converts shadow results into published scores.

---

## Summary Table

| OD | D6 Verdict | D7 Ruling | D7 Condition |
|---|---|---|---|
| OD-1 Flat penalty P = 14 | RATIFY | **CO-SIGN** | Watch for systematic over-penalization of low-risk additive bundles in shadow top-movers; recalibrate or activate D4 for Stage 1 if present |
| OD-2 A/B weights 0.60/0.40 | RATIFY | **CO-SIGN** | If shadow read-mode breakdown shows >30% position-only inference AND directionally inconsistent movements, revisit weight downward for Stage 1 |
| OD-3 NOVA modifiers −10/+5/0 | RATIFY | **CO-SIGN** | If NOVA-4 products with additive_marker_count ≤ 1 score above 60 in Column D with genuine (non-position-only) matrix reads, revisit modifier to −15 for Stage 1 |
| OD-4 N-3 cap at 68 | RATIFY | **CO-SIGN** | No condition; Stage 1B disposition governed by binding-cap proportion in shadow anomaly report per target spec §5.1 |

---

## Implementation Authorization

The candidate engine (`BARI_DECHAIN_V1`) is **cleared to be implemented in the isolated worktree** (`task-395-dechain-v1`) and shadow-run against the 460-product scoreable universe (source: `shadow_run_plan_v1.md` Part B §B.1).

Conditions on this authorization:
1. Implementation is in the isolated worktree only. The shared working tree (`task-374-toms-voice`) is not touched.
2. All retained guards (V-1, CC-1, CC-2, SW-1, FL-1 through FL-4, N-3 cap at 68, dominance guardrail) remain unconditionally active. No guard is modified by the implementation.
3. The Column A cross-check self-gate passes (exit code 0, all Column A scores match committed baseline) before Column D results are emitted.
4. The owner reviews the movement table and anomaly report before any deploy decision. No frontend JSON is modified during the shadow run.
5. The COMPONENT_B_NONE products in the anomaly report are explicitly flagged for the owner as a coverage gap, not a candidate engine finding.

This is a D7 authorization to implement and measure. It is not a go/no-go for production deployment — that gate is owner-held (tripwire 2) and activates only after the owner reviews the shadow movement table.

---

## Decision Log

| Item | Options considered | Chosen | Decisive reason | Reversal condition |
|---|---|---|---|---|
| OD-1 P=14 | P=10 (too permissive for 5-additive products); P=14; P=18 (over-penalizes low-risk bundles) | CO-SIGN P=14 | Correctly calibrated for the modal NOVA-4 additive profile; known distortions are productive shadow findings | Systematic over-penalization of low-risk additive bundles visible in top-movers |
| OD-2 0.60/0.40 | 0.50/0.50 (amplifies position-inference variance); 0.60/0.40; 0.70/0.30 (too weak to catch clean-label refined-starch junk) | CO-SIGN 0.60/0.40 | 0.40 is the minimum weight that makes Component B a genuine structural guard; arithmetic confirmed | >30% position-only inference AND directionally inconsistent movements in shadow |
| OD-3 −10/+5/0 | −15 (risks NOVA dominance on misclassified products); −10/+5; higher positive bonus | CO-SIGN −10/+5/0 | −10 is meaningful movement without overriding structural signals; N-3 cap backstops the clean-label gap; NOVA-3=0 avoids classifier heterogeneity problem | NOVA-4 products with ≤1 additive AND genuine matrix reads scoring above 60 in Column D |
| OD-4 Cap at 68 | Relax to 78 (Stage 1B value, conflates shadow with Stage 1B); keep at 68 | CO-SIGN keep at 68 | Shadow diagnostic value requires the existing safety structure; binding vs coincidental cap distinction is the key finding | N/A; Stage 1B governed by shadow results per spec §5.1 |

---

```json
{
  "task": "TASK-395",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "03_operations/bsip2/proto_v0/reports/d7_cosign_shadow_ods_v1.md",
      "action": "created",
      "sha256": "1D5CB8942180C89D1DCD072487F7F09E04302C4CE27BE32CEAE11BEAF2B259D6"
    }
  ],
  "counts": {
    "open_decisions_reviewed": "4/4 (OD-1, OD-2, OD-3, OD-4 — denominator: shadow_run_plan_v1.md Part A §Open Decisions)",
    "verdicts_cosign": "4/4 — all ratified values co-signed",
    "verdicts_cosign_with_conditions": "3/4 — OD-1, OD-2, OD-3 carry post-shadow calibration conditions; OD-4 unconditional",
    "verdicts_withhold": "0/4",
    "shadow_scoreable_universe": "460 unique barcodes (source: shadow_run_plan_v1.md §B.1 — not independently verified by Product Agent; cited from Data Agent trace)",
    "owner_review_items_flagged": "2 (COMPONENT_B_NONE products = coverage gap not engine finding; >30% position-only inference threshold for OD-2 revisit)",
    "d6_cosign_already_present": "yes — d6_ratify_shadow_ods_v1.md (authored 2026-06-25)"
  },
  "commands_run": [
    {"cmd": "Read 03_operations/bsip2/proto_v0/reports/d6_ratify_shadow_ods_v1.md", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip2/proto_v0/reports/shadow_run_plan_v1.md", "exit_code": 0}
  ],
  "not_done": [
    "Implementation of BARI_DECHAIN_V1 in worktree — this document authorizes it; Data Agent executes",
    "Shadow run — no movement table exists yet",
    "Stage 1B cap disposition (68→78 or remove) — deferred to post-shadow owner review",
    "BARI-INVERSION-TEST-001 adversarial fixture set — flagged as not-done in shadow_run_plan_v1.md; required before Stage 1B per target spec §6.7",
    "OD-2 position-only inference threshold check — metric (>30%) only evaluable after shadow_read_mode_breakdown_v1.json is produced",
    "SHA256 of this file — orchestrator runs Get-FileHash after write"
  ],
  "self_check": "Acceptance test: Both D6 (d6_ratify_shadow_ods_v1.md) and D7 (this document) have co-signed all four ODs with no WITHHOLD verdicts. Data Agent may now implement BARI_DECHAIN_V1 in the isolated worktree (task-395-dechain-v1), execute the shadow run, and produce the six output artifacts. Column A self-gate must pass (exit code 0) before Column D results are emitted. Owner reviews shadow movement table before any deploy. No published score changes result from this co-sign."
}
```
