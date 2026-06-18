# P15 → Data Agent (cheapest lane — fully specified, zero judgment) — send anytime

```
P15 / TASK-254 — Implement the display_values spec (rubric v2 §9) in the claims
inventory builder.

SPEC (authoritative, do not deviate):
C:\Bari\03_operations\claim_entailment\claim_entailment_rubric_v2.md §9 — the
14-field display_values block per product, with ingredient_list_sha256 instead
of raw ingredient text (Nutrition's implementation note).

DO:
1. Update C:\Bari\03_operations\claim_entailment\inputs\_build_claims_v2.py (or
   create _build_claims_v3.py if cleaner) so every product entry carries a
   display_values block populated per §9: numeric display fields from the LIVE
   frontend JSON (display_score, display_grade, etc.) and label-derived fields
   (nutrition values, ingredient_first, ingredient_percentages,
   ingredient_list_sha256) from the BSIP1 corpus product files. A field with no
   source data = null (never invent, never substitute — no Open Food Facts).
2. Regenerate both inventories:
   - yogurts_claims_input_v2.json (from the same sources as v1 + display_values)
   - cereals_claims_input_v3.json (v2 + display_values)
3. Self-check: report per category how many products have each field non-null;
   spot-print 2 full product entries for eyeball verification.

RULES: read-only outside 03_operations/claim_entailment/inputs/; do not touch
traces, frontend, or the rubric.

RETURN BLOCK: builder path; output paths; per-field non-null counts; the 2
sample entries. Propose RETURNED.
```

---
**After you paste this to the agent:** open `tasks\DISPATCH_BOARD.md` and put an `x` in the P15 line under 📬 Signals (`- [ ]` becomes `- [x]`). That is how the orchestrator knows it's in flight.
