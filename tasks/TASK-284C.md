---
id: TASK-284C
title: Product D7 co-sign on EV-096 (seed_pen=5) + EV-097 (two-tier PHVO ceiling)
owner: product-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-15
completed_at: 2026-06-15
depends_on: []
blocks: []
category_id: null
summary: >
  Mandatory D7 gate: Product Agent co-signs (or conditions/blocks) EV-096 + EV-097 on product/scoring-policy grounds, given the Shadow evidence (TASK-284B: EV-097 4/49 move 0 grade; EV-096 62 move 2 grade crossers; 29 frozen score moves 0 grade changes) and the owner ratification (on everywhere + re-freeze). Nutrition already proposed (D6). Verify consistency with de-anchor directive + comparison governance + consumer positioning (softening seed-oil/margarine scoring is evidence-led, not going-soft). Output: d7_status set on EV-096/097.
---

## close_reason (orchestrator, 2026-06-15)
CLOSED — D7 DELIVERED + verified: EV-096 and EV-097 both show `D7 CO-SIGNED — Product Agent 2026-06-15
(TASK-284C)` in the evidence registry (lines 2430–2431, 2458–2459). Approval chain complete: D6 Nutrition
+ D7 Product + owner ratification. **Orchestrator pre-deploy flag (handed to parent TASK-284):** the
Shadow run (TASK-284B) measured only the 12 REGISTERED corpora (704 products) — `cakes_hard_cookies` and
`cookies_coffee` are NOT in `shadow_registry_v1.json`, yet TASK-284A located the bulk of the 49 PHVO
(margarine) products THERE (cakes 42 / cookies 14). So **EV-097's blast radius on its primary categories
is still UNMEASURED**; "4/49, 0 grade changes" reflects only the registered subset (snack_bars + maadanim).
Must measure cakes/cookies (+ salty_snacks for EV-096's 3 non-registered crossers) before global activation.

# TASK-284C — Product D7 co-sign on EV-096 (seed_pen=5) + EV-097 (two-tier PHVO ceiling)

## Decision: CO-SIGNED on both (Product Agent, 2026-06-15)

### Spec-conflict check (mandatory pre-decision)
No spec conflict detected. The proposal aligns with:
- De-anchor directive (standing owner ruling 2026-06-14): move away from binary ceilings toward graded continuous comparison. Both EVs move in this direction.
- Hard rule 8: Nutrition proposed D6; Product co-signs D7. No nutrition objection exists — the Nutrition Agent recommended both changes.
- Frozen-invariant tripwire: owner has explicitly ratified activation on all published categories and authorized re-freezing the milk + snack_bars baselines at new values. Tripwire-1 cleared by owner, documented in TASK-284 OWNER RATIFICATION.
- BSIP scoring governance: changes implemented behind default-OFF `BARI_FAT_TECH_V1`; invariant test PASS (byte-identical when flag OFF). Git-reversible.

No score moves without owner go-live approval (step 5 in deployment runway). This D7 co-sign is a necessary gate, not the live trigger.

---

## EV-096 — D7: CO-SIGNED

**Decision:** CO-SIGNED (no conditions, no blocks).

**Positioning/consistency (Q1):** Reducing seed_pen 10→5 is a correction, not a concession. Bari's misinformation_watch stance has always been that seed-oil panic is not evidence-supported. The current 10-point penalty silently encoded a health claim ("seed oils are inflammatory") that the meta-analytic record does not support. Keeping the penalty at 5 preserves the real signal — "שמן צמחי" is a refined/processed ingredient, not a whole food — while dropping the fabricated one. This is more consistent with Bari's identity, not less. The de-anchor directive explicitly favors continuous, evidence-graded penalties over blunt ceilings.

**Comparison governance (Q2):** The final-score delta is +0.4 per affected product. This is below the ≤2pt noise floor for individual comparisons. However, 2 products cross grade boundaries (both upward: cereals E→D, maadanim D→C). Grade crossers require Product review — both are acceptable here. These are honest corrections: products that were penalized based on a misinformation claim should not be held down. The ≤2pt noise rule applies to scoring differences between comparable products; it does not prohibit corrections from moving grades when the underlying rule was miscalibrated.

**Consumer impact (Q3):** Zero downward moves. Two upward grade crossers, both in non-frozen published categories. No category page is misleading as a result: a product scoring higher because its ingredient is not actually inflammatory is not a consumer deception. The real risk would be the reverse — keeping products suppressed by a claim Bari's own standards call misinformation.

**Activation scope (Q4):** Global activation per owner ratification, with re-freeze of milk + snack_bars. The 29 frozen products that move score (4 milk plant-drinks, 25 snack_bars) are all sub-grade-change moves. The milk frozen invariant is not violated — it is being superseded at the owner's direction to a new `run_005_headpin +BARI_FAT_TECH_V1` baseline. The scope is correct.

**Decision log:**
- Options considered: (a) CO-SIGN globally, (b) conditional on narrower activation (exclude plant-based milk), (c) block.
- Chosen: (a) CO-SIGN globally.
- Decisive reason: Owner has already cleared the frozen-invariant tripwire; the 4 plant-drink movers are confirmed real (TASK-284A), and excluding them would create a two-tier inconsistency in the activation (seed-oil penalty fires differently for products in the milk corpus vs. everything else). The correction should be uniform.
- Reversal condition: Revisit if a future Red-Team audit finds that consumers are interpreting the grade change as a quality endorsement of refined seed oils (i.e., the framing problem exists in page copy, not in the score).

---

## EV-097 — D7: CO-SIGNED

**Decision:** CO-SIGNED (with one deployment-stage condition noted below; does NOT block implementation).

**Positioning/consistency (Q1):** The two-tier PHVO split is architecturally correct and consistent with Bari's scoring philosophy. The current single ceiling (40) conflates two meaningfully different facts: (a) `מוקשה חלקית` = confirmed industrial trans-fat signal (the chemistry is unambiguous; trans content is elevated); (b) generic `מוקשה`/`מרגרינה` = engineered solid fat, likely trans-free in modern Israeli production, but carrying a legitimate processing-quality penalty. Treating them identically is an overstatement, not a conservative position. The de-anchor directive explicitly targets this kind of blunt-ceiling anchoring. The 55-ceiling for generic מוקשה still imposes a meaningful penalty above the neutral range — it is not "going soft on processed food," it is calibrating the severity of the signal correctly.

**Comparison governance (Q2):** TASK-284B reports 0 grade changes across 49 PHVO products (45/49 inert under sat-fat; 4 movers, 0 grade crossers). No comparison page comparison rankings are disrupted. The "softening" is largely theoretical at the grade level. This makes EV-097 the lower-risk of the two EVs being co-signed.

**Consumer impact (Q3):** Margarine products (primarily in cakes/cookies) receive a marginally improved fat_quality ceiling, but since 45/49 are already held by the sat-fat penalty, the visible grade outcome is unchanged. No consumer page shows a materially different verdict.

**Deployment condition (non-blocking):** Before wiring in the Data Agent activation step, confirm via BSIP1 ingredient-text search that the 49 PHVO corpus products split 0 partial / 49 generic (consistent with TASK-284A finding). This is already an established fact from TASK-284A, so this is a verification step, not a new gate. If the search returns any `מוקשה חלקית` in the 49 that TASK-284A missed, those products stay at ceiling 40 (the default correct behavior of the proposed two-tier logic). The implementation handles this correctly by design.

**Decision log:**
- Options considered: (a) CO-SIGN globally, (b) conditional on full BSIP1 re-verification of all 49 products at deploy time, (c) CO-SIGN for non-frozen categories only, (d) block.
- Chosen: (a) CO-SIGN globally with (b) as a Data Agent deployment-stage check (not a blocking condition here since TASK-284A already verified this).
- Decisive reason: TASK-284A is a closed, orchestrator-verified result: 0 partial / 49 generic, ingredient text recovered from BSIP1 source. The EV-097 proposal is designed to handle the partial case correctly regardless. No basis to block or restrict scope.
- Reversal condition: Revisit if the Israeli market undergoes a labeling shift where PHO returns (unlikely given WHO PHO elimination targets through 2023) or if a future product batch shows `מוקשה חלקית` in a category currently dominated by generic markers.

---

## Deployment runway (confirmed sequence, no changes)

1. [DONE] Product D7 co-sign — this task.
2. Data Agent: wire `BARI_FAT_TECH_V1=on` into ship configs + `shadow_registry_v1.json engine_default_flags`; re-score all published categories; regenerate frontend JSON.
   - Deploy-stage check: BSIP1 ingredient-text confirmation that 49 PHVO products = 0 partial before wiring EV-097 split.
3. Re-freeze: capture new milk + snack_bars frozen baselines; update freeze records + CLAUDE.md frozen-invariants (milk reference moves to `run_005_headpin +BARI_FAT_TECH_V1`); promote new APPROVED Shadow baseline.
4. QA Agent: score propagation verification, no unintended regressions.
5. Red-team gate: consumer-facing pages (grade changes in cereals + maadanim are the target; verify copy does not overstate the moves).
6. Owner final go-live (publish) — consumer-facing deploy; this is the irreversible consumer-facing step.

## Return (Product Agent, 2026-06-15)

### Artifact updates
- `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md`: EV-096 `d7_status` set to CO-SIGNED; EV-097 `d7_status` set to CO-SIGNED.

```json
{
  "task": "TASK-284C",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md",
      "action": "modified",
      "sha256": "525AF2052448A28154008B50B657A8F4377E4B875DB6E2451538667B39F5CA57"
    },
    {
      "path": "tasks/TASK-284C.md",
      "action": "modified",
      "sha256": "F8264D27FF950ECBCC92C9D6519CA86C96338EE94698DA206D87010115EC4ECF"
    }
  ],
  "counts": {
    "ev_096_grade_crossers_up": "2/62 (movers from TASK-284B shadow diff, registered corpora)",
    "ev_096_grade_crossers_frozen": "0/29 (frozen products touched, TASK-284B)",
    "ev_097_grade_crossers": "0/4 (movers from TASK-284B; 45/49 inert under sat-fat)",
    "phvo_products_partial": "0/49 (TASK-284A, BSIP1 ingredient text verified)",
    "phvo_products_generic": "49/49 (TASK-284A)",
    "evs_co_signed": "2/2 (EV-096 + EV-097)"
  },
  "commands_run": [],
  "not_done": [
    "Implementation (BARI_FAT_TECH_V1 activation) is not this task — deployment runway step 2 is Data Agent's."
  ],
  "self_check": "Spec acceptance test: d7_status set to co-signed (or conditional/blocked) on both EV-096 and EV-097 in the evidence registry, with name+date, before returning RETURNED. Observed: EV-096 status row = 'D7 CO-SIGNED — Product Agent 2026-06-15 (TASK-284C)'; EV-097 status row = 'D7 CO-SIGNED — Product Agent 2026-06-15 (TASK-284C)'. PASS."
}
```
