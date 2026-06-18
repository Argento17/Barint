# P17 → QA Agent (cheap model) — claim-gate check on the cereals remediation draft. Send before the owner reads it.

```
P17 / TASK-254 — Entailment check over the NEW cereals copy draft (the gate's
first use on pre-ship copy — this is the production rehearsal).

INPUTS:
- Draft: C:\Bari\02_products\breakfast_cereals\cereals_copy_remediation_draft_v1.json
  (34 products, NEW rowVerdict + insightLine per product)
- Rubric: C:\Bari\03_operations\claim_entailment\claim_entailment_rubric_v2.md
  (v2 — two-layer rule §4 applies: numeric score/grade claims vs the draft's own
  badge values / live frontend; mechanism claims vs the reconstruction traces at
  02_products/breakfast_cereals/bsip2_outputs/run_cereals_008_reconstruction/ and
  run_cereals_multiretailer_001_reconstruction/)

DO: decompose every NEW string into atomic claims; verdict each (PASS / REVIEW /
HARD-FAIL / UNVERIFIABLE per rubric v2); aggregate per string. Special attention:
- sodium causal language (auto HARD-FAIL per Nutrition ruling — sodium may appear
  as displayed fact only);
- MoH/red-label invocations (must match a fired ISRAELI_RED_LABEL_* rule);
- grade letters in text vs the badge field in the same draft entry (must match
  exactly);
- the known 9 drift products: mechanism claims judged vs reconstruction traces,
  numeric claims vs the badge (drift itself is never a copy HARD-FAIL).

OUTPUT: C:\Bari\03_operations\claim_entailment\calibration\cereals_draft_gate_v1.md
— verdict counts + every non-PASS with evidence. RULES: read-only except that
output file; ground truth = traces + draft badges + methodology docs only; no
external knowledge; no Open Food Facts.

RETURN BLOCK: totals by verdict; every HARD-FAIL/UNVERIFIABLE with one-line
evidence; verdict on whether the draft is owner-read-ready (all-PASS/REVIEW) or
needs a Content fix loop first. Propose RETURNED.
```

---
**After you paste this to the agent:** open `tasks\DISPATCH_BOARD.md` and put an `x` in the P17 line under 📬 Signals.
