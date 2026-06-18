# P11 → Content Agent — send after P10 lands (or in parallel; touches cereals only)

```
P11 / TASK-254 — Regenerate ALL 34 live cereal card texts (rowVerdict + insightLine).
LIVE INCIDENT: 11+ cards contradict their own badge (e.g. ריבועי דגנים badge 36/D,
text says "יורד ל-C"; הרדוף badge 69/B, text says "יורד ל-C" citing the MoH red
threshold) and/or fabricate causes. Calibration evidence:
C:\Bari\03_operations\claim_entailment\calibration\cereals_calibration_v1.json + .md

GROUND TRUTH (two layers, fixed by orchestrator):
- Numeric score/grade statements = the LIVE frontend values in cereals_frontend_v2
  .json (badges are NOT changing in this pass — text must match them).
- Mechanism/cause statements = the product's reconstructed trace:
  02_products/breakfast_cereals/bsip2_outputs/run_cereals_008_reconstruction/
  (+ run_cereals_multiretailer_001_reconstruction for the 8 multiretailer products).
  A cause may be stated ONLY if the trace shows it fired.

HARD RULES (Nutrition-ratified, rubric §11):
- Sodium is NEVER a grade cause for cereals (no engine rule exists, TASK-189) —
  sodium may appear as a displayed fact only ("320 מ"ג נתרן ל-100 גרם"), never
  with causal language (יורד בגלל/כי).
- NEVER invoke משרד הבריאות / red label unless an ISRAELI_RED_LABEL_* rule fired
  in that product's trace.
- BHT and vitamin enrichment are not scored factors — no grade attribution to them.
- Every factual claim must be entailed by trace or live frontend (rubric:
  C:\Bari\03_operations\claim_entailment\claim_entailment_rubric_v1.md §1-6).
- Editorial standards apply: verdict model (2-line human verdict: standing → why →
  catch → grade), assertive writing (finding-first, no apology), calorie density +
  real fired driver named in every verdict.

OUTPUT: a DRAFT file only — C:\Bari\02_products\breakfast_cereals\
cereals_copy_remediation_draft_v1.json: [{product_id, barcode, name, badge
(score/grade, unchanged), OLD rowVerdict/insightLine, NEW rowVerdict/insightLine,
trace_drivers_cited}]. DO NOT touch cereals_frontend_v2.json or any live file —
the read-every-string owner gate applies before anything ships.

RETURN BLOCK: count regenerated; list of products whose OLD text had grade
contradictions or fabricated causes (the confirmed-incident list); any product
where the trace gives too little for an honest verdict (say so, don't invent).
Propose RETURNED.
```

---
**After you paste this to the agent:** open `tasks\DISPATCH_BOARD.md` and put an `x` in the P11 line under 📬 Signals (`- [ ]` becomes `- [x]`). That is how the orchestrator knows it's in flight.
