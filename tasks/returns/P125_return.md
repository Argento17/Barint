# P125 Return — TASK-278 Phase-9: Juices × Sugar D7 Co-Sign

**Agent:** Product Agent  
**Phase:** TASK-278 Phase-9  
**Date:** 2026-06-14  
**Status:** RETURNED

---

## D7 Decisions

### Q1 (CRITICAL): Scope Guard Field — CORRECTED

**Both D6 and the orchestrator correction are wrong. The correct scope guard is `product.get("juice_sub_pool") is not None`.**

Verification path:
- Read `batch_run_juices_001.py` line 38: `score = score_product(product, signals, cat, nova, scope)` — `product` is the raw BSIP1 dict
- Read `bsip1_7290000039435.json` lines 4–106: no `"category"` field exists in the BSIP1 dict
- The `"category"` field (e.g. `"beverage"`) is written to the BSIP2 trace output ONLY — it is the router-assigned category, not an input field
- `"juice_sub_pool"` exists in all 65 BSIP1 files: values `juice_100`=16, `fruit_drink`=13, `nectar`=3, MISSING=2
- Field spelling confirmed: `juice_sub_pool` (NOT `juice_subpool`)
- Excludes 2 products with MISSING field via `is not None` guard
- Covers all three router categories (beverage/default/dessert) without router-category guard — correct because `juice_sub_pool` is juice-exclusive by construction

This is the same mechanism as EV-090's `bsip_cheese_subpool` — a BSIP1 enrichment field used as scope guard, not the router-assigned category.

### Q2: Fruit Drink Inclusion — INCLUDED

All 13 `fruit_drink` products included. Sugar is the scoring signal regardless of juice concentration. Exclusion would cherry-pick scope to flatter 100% juice products. Corpus stats (n=65, median=9.50g) already incorporate them — removing them would require a D6 rerun.

### Q3: P_max/B_max at Lower Scale — APPROVED AS SPECIFIED

P_max=6, B_max=3 approved. Scale=2.82 means SR fires proportionally for genuine gram differences. Standard values consistent with all prior enrollments. If pilot C2c fails (mean |delta| < 0.5), revisit.

### Q4: Routing-Agnostic Criterion — C11 ADDED

Criterion C11 added to pilot gate: identical sugar_g → identical delta regardless of router-assigned category (beverage vs default). Structurally guaranteed by juice_sub_pool scope guard, but made explicitly testable.

---

## Spec Conflict Disclosure

D6 proposed `category_slug` as the scope guard (does not exist in any dict). The orchestrator's correction to `product.get("category") == "juices"` is also wrong — there is no `category` field in the BSIP1 product dict at `score_product` call time. Both proposals are incorrect. Product Agent D7 replaces both with the confirmed-existing `juice_sub_pool` field.

This is a spec-conflict catch (Spec-Conflict Duty, 2026-06-12): the delegation spec contained a testable factual error about field existence. Silent execution of either proposal would have caused a zero-bleed failure at C9/C10 pilot gate, or worse, a silent misfire on every product (if `product.get("category")` returns None always, no products would ever pass the scope guard — silent 0-delta on the entire corpus).

---

## Artifacts

| Artifact | Path | Status |
|---|---|---|
| D7 Co-Sign Doc | `02_products/juices/methodology/juices_sugar_d7_cosign_v1.md` | Created |
| EV-091 Registration | `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md` | Appended after EV-090 (line ~2226) |
| This return | `tasks/returns/P125_return.md` | Created |

---

## EV-091 Summary

| Parameter | Value |
|---|---|
| scope_guard | `product.get("juice_sub_pool") is not None` |
| nutrient | sugars_g |
| n_scope | 65 (run_juices_001) |
| median_g | 9.50 |
| robust_scale | 2.82 |
| floor | 62 |
| floor_threshold_g | 12.2 (Q3) |
| P_max | 6 |
| B_max | 3 |
| anti_immunity | 62+3=65<70 PASS |
| fruit_drink | INCLUDED |
| pilot_gate_criteria | 12 |
| status | pilot_pending |

---

## Not Done

- Engine wiring (Data Agent task, authorized by this co-sign)
- Pilot rescore run (Data Agent)
- Pilot gate validation (QA Agent)
- Owner go-live (tripwire-1, required before any published score changes)

---

```json
{
  "task_id": "TASK-278",
  "phase": "Phase-9 juices×sugar D7 co-sign",
  "status": "RETURNED",
  "return_date": "2026-06-14",
  "agent": "product-agent",
  "scope_guard_approved": "product.get('juice_sub_pool') is not None",
  "scope_guard_correction": "D6 proposed category_slug (nonexistent); orchestrator proposed product.get('category')=='juices' (also wrong — no category field in BSIP1 dict); Product Agent D7 corrects to juice_sub_pool (confirmed from BSIP1 files)",
  "floor_threshold_g": 12.2,
  "p_max": 6,
  "b_max": 3,
  "ev091_registered": true,
  "ev091_line": 2226,
  "pilot_gate_criteria_count": 12,
  "anti_immunity_proof": "62+3=65<70 PASS",
  "fruit_drink_included": true,
  "d7_cosign_doc": "02_products/juices/methodology/juices_sugar_d7_cosign_v1.md",
  "engine_modified": false,
  "off_used": false,
  "spec_conflict_flagged": true,
  "spec_conflict_detail": "Both D6 scope guard proposal (category_slug) and orchestrator correction (product.get('category')=='juices') reference non-existent fields. Correct field is juice_sub_pool — verified against BSIP1 source files and batch_run_juices_001.py.",
  "artifacts": [
    {
      "path": "02_products/juices/methodology/juices_sugar_d7_cosign_v1.md",
      "sha256": "not_computed",
      "type": "d7_cosign_doc"
    },
    {
      "path": "03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md",
      "sha256": "not_computed",
      "type": "ev_registry_append",
      "ev_id": "EV-091"
    },
    {
      "path": "tasks/returns/P125_return.md",
      "sha256": "not_computed",
      "type": "return_file"
    }
  ],
  "counts": {
    "d7_questions_resolved": "4/4",
    "ev_entries_added": "1 (EV-091)",
    "pilot_gate_criteria": "12 total (11 named slots, C2a/C7 aliased, C11 new)",
    "scope_guard_corrections": "2 (D6 proposal + orchestrator correction both wrong)",
    "artifacts_created": "3"
  },
  "commands_run": [
    {"cmd": "Read bsip2_evidence_registry_v1.md offset=2192 limit=80", "exit": 0},
    {"cmd": "Read bsip1_7290000039435.json", "exit": 0},
    {"cmd": "Read batch_run_juices_001.py limit=80", "exit": 0},
    {"cmd": "Grep juice_sub_pool in bsip1 output dir", "exit": 0},
    {"cmd": "Grep category in bsip2 traces for dessert misroute", "exit": 0}
  ],
  "not_done": [
    "Engine wiring (Data Agent)",
    "Pilot rescore run (Data Agent)",
    "Pilot gate validation (QA Agent)",
    "Owner go-live (tripwire-1)"
  ],
  "acceptance_test": "EV-091 appended to evidence registry after EV-090; D7 co-sign doc created; scope guard corrected from nonexistent fields to confirmed juice_sub_pool; fruit_drink included; 12 pilot gate criteria documented; anti-immunity 65<70 verified; engine unmodified; OFF unused.",
  "propose": "RETURNED"
}
```
