# Brined Cheese D7 Co-Sign — Product Agent

**Task:** brined-cheese-d7-cosign
**Date:** 2026-06-13
**Author:** Product Agent
**Verdict: CO-SIGN APPROVED (with conditions)**
**Scope:** EV-053 (cap-45 fix) + EV-054 (HP_FAT_SODIUM_COMBO suppression) — both conditionals, ship together

---

## Verdict

**CO-SIGN APPROVED.** Both conditionals ship together. No published-score movement permitted. EV-053 and EV-054 must be formally registered before any code lands.

---

## 1. Precedent Question — The Central Issue

The central risk in this co-sign is whether exempting `brined_food` context from the 2-label cap and the HP penalty opens a loophole: any high-fat/high-sodium category claiming "our sodium is structural" to escape penalty.

The answer is no. Here is why this case is genuinely narrow and not special-pleading:

**The precedent is already set.** The `brined_food` context flag and its `sodium_weight = 0.7` are a previously D7-approved mechanism specifically for foods whose sodium derives from preservation brine rather than formulation choice. Olives and pickles already carry this treatment. EV-052 extended the flag to brined cheeses by keyword — that extension was already approved. The EV-053/054 proposals are not creating a new precedent; they are fixing a logical inconsistency inside the existing brined_food architecture.

**The inconsistency is real and documented.** The engine holds two irreconcilable positions simultaneously: (a) "this sodium is brine-structural — penalize at 70% weight" (the 0.7 multiplier, Position 1) and (b) "this sodium red label counts equally in the 2-label compound cap" (Position 2). The cap then fires at 45 and overrides the 72-cap produced by Position 1. This is not a borderline tradeoff — it is a logical contradiction within a single scoring pass. The Nutrition Agent's ruling correctly names it as double-accounting.

**The HP_FAT_SODIUM_COMBO compounds the same error.** The rule was designed for reformulated products where fat and sodium are co-engineered to maximize palatability — chips, crackers, processed snacks. Structural dairy fat in a cheese that is 100% fat-from-milk, combined with brine-preservation sodium, is not a hyper-palatability engineering choice. The penalty fires on 48/48 of the shelf (the entire corpus), including products with three-item ingredient lists (milk, salt, culture). A penalty that fires on every product without discrimination is not functioning as a differentiating signal — it is a universal tax on a food class.

**The loophole risk is contained by the gate structure.** The `brined_food` flag requires: (a) a name match against a controlled keyword list of canonical Hebrew brined-food names, AND (b) sodium > 500mg. A category cannot self-declare into the flag; it must pass through the keyword gate. A future category claiming "structural sodium" would need a new EV entry, a D7 co-sign, and keyword-level evidence — the same process this proposal followed. The gate is the answer to the slippery-slope concern.

**Ruling: brine is genuinely, narrowly different.** The physical mechanism (cheese produced and preserved in saturated NaCl brine) is well-established and production-method-observable. The analogy to olives and pickles is exact. This is not special-pleading — it is the correct application of an existing, already-approved mechanism to a food class that belongs in it.

---

## 2. Scope Discipline

**Both conditionals must ship together.** The Nutrition Agent's ruling deferred HP_FAT_SODIUM_COMBO to a "separate D7 batch" but explicitly flagged that shipping only the cap-45 fix would leave the full-fat brined cheeses in the ~49–62 range instead of the ~55–68 range — requiring a second re-run and a second D7 cycle. That is unnecessary engineering overhead for a fix that is equally well-justified.

More importantly: the HP_FAT_SODIUM_COMBO fires on 48/48 products, including every NOVA-1 clean product. Even after the cap-45 fix, the HP penalty would continue to suppress NOVA differentiation in the full-fat tier. Shipping cap-45 alone does not solve the stated problem (NOVA re-expression); it solves half of it and creates a follow-up cycle. That is overbuild through fragmentation.

**Scope tightness assessment: PASS.** Both fixes are gated on `context_flag == "brined_food"`. There is zero spillover to any other category. The keyword gate controls which products reach the flag. Cottage, hard yellow cheeses, and cream-cheese spreads are not matched. The fixes are surgically scoped.

**The only implementation guard:** the HP suppression must be a conditional suppression (`if context_flag == "brined_food": skip HP_FAT_SODIUM_COMBO`), not a removal of the rule. The rule stays active for all non-brined contexts.

---

## 3. Honesty Check — Does the Fix Produce Honest Spread?

The predicted post-fix distribution (A:2, B:15-18, C:20-25, D:3-6) is checked against three honesty tests:

**Test 1: Fat-tier ordering preserved.** A 16-28% fat brined cheese should still rank below a 5% one. Post-fix: the 5% low-fat products are unaffected by either fix (they do not hit the sat-fat red label threshold and thus were never caught by the 2-label cap). They remain in A/B. The 16-28% fat products move from D into C/B depending on NOVA and additives. The ordering fat-5% > fat-16% > fat-28% is preserved through the sat-fat dimension scoring, which neither fix touches.

**Test 2: NOVA re-expresses.** A clean NOVA-1 13%-fat Bulgarian (~62/C) must sit clearly above a NOVA-3 same-fat-tier product (~48-54/C). Post-fix: the cap-45 lift and HP suppression remove the floor that collapsed NOVA-1 and NOVA-3 to identical scores. Processing penalties and additive signals then differentiate the two. This is the stated goal of the methodology brief's PRIMARY differentiator (§4). Confirmed plausible.

**Test 3: No flattery of full-fat cheese.** The fixes do not award bonus credit — they remove incorrect deductions. A 28%-fat brined cheese with additives does not reach A or B after the fix; it reaches high-C or low-B depending on its processing score, which is correct. Full-fat brined cheese is not excellent food; the fix correctly places it in C, not in D alongside NOVA-4 processed products.

**Honesty verdict: the fix produces honest spread, not flattery.** The butter rule (never manufacture differentiation) does not apply here in reverse — the current collapse is demonstrably manufactured by a mechanical artifact, not a genuine nutritional equivalence.

---

## 4. Overbuild Check

The proposed implementation is two 5-to-10-line conditionals in `score_engine.py`, two EV entries, one D7 co-sign document, and a no-regression gate. This is proportionate. There is no simpler path that produces the same result — the fixes must be engine-level because the problem is engine-level.

The alternative of using DISTORTION-010 (disclosure-only, no score change) was considered by the Nutrition Agent and correctly rejected: a consumer-facing D with a footnote explaining "but the sodium is structural" is not an honest score, it is an apology for a wrong score. That path would be cheaper to build and more expensive to the product's credibility.

**Overbuild verdict: proportionate.** Proceed.

---

## 5. Conditions of Co-Sign

Implementation is approved subject to all of the following. Any condition not met before the code merge is a co-sign violation and the change must not ship:

### 5.1 Evidence registry (pre-code, mandatory)
- **EV-053** formally registered in `bsip2_evidence_registry_v1.md`: cap-45 exclusion for brined_food sodium label. The draft in `brined_cheeses_cap45_ruling_v1.md` §7 is the content; it must be formally committed to the registry file.
- **EV-054** formally registered: HP_FAT_SODIUM_COMBO suppression under brined_food context. Content: structural dairy fat + brine-preservation sodium is not a hyper-palatability engineering stack; suppression is scoped to `brined_food` context flag only; zero effect on any other category or food class.

### 5.2 No-regression gate (mandatory, hard stop)
- `engine_invariants.py` 342-case suite: **zero regressions**. Any case that moves = STOP, do not merge.
- Golden-corpus byte-identical check for every published category: **milk, yogurt, bread, cereals, granola, snack bars, cheese-spreads**. All 7 corpora must produce byte-identical output against the patched engine. A single score change in any published category = STOP, escalate to owner (frozen-invariant tripwire).
- Dedicated regression test confirming non-brined dairy (cottage, yogurt, white cheese) are byte-identical before and after the patch.

### 5.3 Implementation constraints
- Both fixes gated on `context_flag == "brined_food"` only — no other condition triggers the exemption.
- HP_FAT_SODIUM_COMBO suppression is a conditional skip, not a rule deletion. The rule must remain active for all non-brined contexts.
- Each changed block tagged `# EV-053` and `# EV-054` respectively for rollback locatability.
- Score engine change is the only file modified (plus the EV registry). No frontend, no copy, no JSON outputs until run_brined_002 completes and QA approves.

### 5.4 Re-run sequence
1. Register EV-053 + EV-054.
2. Implement both conditionals with inline EV tags.
3. Run 342-case invariants suite + published-category golden check.
4. If zero regressions: trigger run_brined_002 on the 48-product corpus.
5. QA baseline freeze on run_brined_002 output.
6. Confirm NOVA re-expresses (a NOVA-1 clean product in full-fat tier scores above a NOVA-3 same-fat-tier product) — this is the acceptance test.
7. Route to Data Agent for frontend packaging only after QA hard-pass.

---

## 6. What is NOT Approved

- Vocabulary gap (construct-form names, barcode 3075805) — deferred item, no EV required, Data Agent scope in a future sprint.
- `brined_flag_fired` counter bug in batch_run script — Data Agent scope, fix before run_brined_002.
- Any score change in any published category. The no-regression gate is absolute.
- Shipping the brined-cheese frontend before run_brined_002 QA hard-pass.

---

## 7. Decision Log

| Field | Value |
|---|---|
| Options considered | (A) Approve both conditionals together; (B) Approve cap-45 only, defer HP; (C) Reject both, use DISTORTION-010 disclosure only |
| Chosen option | A — both conditionals together |
| Decisive reason | HP fires on 48/48 (the entire corpus); shipping cap-45 alone does not solve NOVA re-expression (the stated goal) and creates a second D7 cycle for a fix that is equally justified and equally scoped |
| Reversal condition | Revisit if run_brined_002 shows the HP suppression produces implausible B-scores for full-fat processed NOVA-3 products (i.e., if removing the HP penalty creates flattery rather than honest spread in that tier) |

---

```json
{
  "task_id": "brined-cheese-d7-cosign",
  "proposed_status": "RETURNED",
  "verdict": "APPROVED",
  "artifacts": [
    {
      "path": "02_products/brined_cheeses/methodology/brined_cheeses_d7_cosign_v1.md",
      "action": "created",
      "sha256": "pending"
    }
  ],
  "counts": {
    "products_in_run": "48/48 (orchestrator-verified run_brined_001)",
    "nova1_products_stuck_at_D": "10/48 (orchestrator-verified)",
    "products_with_binding_cap_45": "28/48 (orchestrator-verified)",
    "hp_fat_sodium_combo_fired": "48/48 (orchestrator-verified — fires on entire corpus)",
    "published_categories_requiring_no_regression": "7/7 (milk, yogurt, bread, cereals, granola, snack-bars, cheese-spreads)",
    "invariants_suite_cases": "342/342 (must pass zero-regression before merge)"
  },
  "commands_run": [],
  "not_done": [
    "EV-053 not yet formally registered in bsip2_evidence_registry_v1.md — Data Agent scope, required before code",
    "EV-054 not yet drafted or registered — Data Agent + Nutrition Agent scope, required before code",
    "score_engine.py not modified — co-sign decision only; Data Agent implements",
    "engine_invariants.py 342-case suite not run — post-implementation gate",
    "Golden-corpus check on 7 published categories not run — post-implementation gate",
    "run_brined_002 not triggered — blocked until EV registration + implementation + invariants pass",
    "brined_flag_fired counter bug in batch_run script not fixed — flag for Data Agent before run_brined_002",
    "Vocabulary gap (construct-form names) not addressed — deferred item"
  ],
  "self_check": {
    "precedent_assessed": true,
    "precedent_finding": "Not a new precedent — fixes a logical contradiction inside an already-D7-approved brined_food architecture; keyword gate prevents category self-declaration",
    "scope_bounded": true,
    "scope_finding": "Both fixes gated on context_flag==brined_food only; zero spillover confirmed by architecture review",
    "no_regression_required": true,
    "no_regression_finding": "342-case invariants suite + 7 published-category golden-corpus check required before merge; any movement = hard stop",
    "acceptance_test": "BLOCKED pending implementation — test is: run_brined_002 shows a NOVA-1 clean product in the full-fat tier scoring above a NOVA-3 same-fat-tier product"
  }
}
```
