# P101 — TASK-277 CHANGES_REQUESTED Retry (route: C1)
# Nutrition Agent — SIE primary-claim tier discipline fix

**Repo:** `C:\Bari`
**Task:** `C:\Bari\tasks\TASK-277.md` (status: CHANGES_REQUESTED)
**Engine:** `03_operations/supplement_engine/proto_v0/`
**Corpus:** `02_products/supplements/real_corpus_v3/`
**Golden:** `03_operations/supplement_engine/proto_v0/golden/` (17 fixtures)

---

## What was already accepted (DO NOT redo)

The previous dispatch fixed three items correctly — these changes are already in the engine:
- **Item 2 (cap_3 misfire):** `detect_over_promise()` now uses word-boundary regex for single-token markers. R3 golden still fires.
- **Item 3 (omega-3 reclassify):** 3 Life omega-3 SKUs (7290118206118 / 7290118206101 / 7290119911011) → `unscoreable_incomplete` in cache.
- **Item 4 (detector noise):** `decaf_guard` + `_omega5_or_ala_guard` in `detect_active_slug()`.

**Preserve all three.** Do not touch them.

---

## The one remaining defect — primary-claim tier discipline

**What the engine does now (wrong):** `resolve_claim_tier` returns the **best tier among ANY matched token** in the full concatenated claim string (raw Hebrew + English translation). So Altman Vitamin C 500 — whose actual marketed claim is "immune support / antioxidant" (Weak) — resolves to **Strong** (91.2/S) because its concatenated string also matches a "vitamin C deficiency / scurvy" endpoint.

This violates SIE claim-specificity: **score the claim the product makes, not the active's best-ever possible endpoint.** The creatine principle: creatine marketed for strength → A; creatine marketed for fat-loss → Insufficient. The grade follows the CLAIM, not the molecule's best dossier entry.

**Result of the overshoot:** 26/82 products at S/A — implausibly generous. Altman Vit C immune → S/91.2; Zinc picolinate "immune support" → S. Both are wrong.

---

## Your task — one targeted fix

### What to fix
Implement PRIMARY-CLAIM discipline in the claim resolution path so that:
1. A product whose on-label primary claim is "immune support" scores on the **immune/antioxidant** endpoint tier, not on a deficiency endpoint that happens to match a token somewhere in its concatenated claim string.
2. The fix must be principled and generalizable — not a product-specific hack.

### Recommended approach (you decide the best implementation)
One viable path: instead of resolving to `max(tier for all matched tokens)`, resolve to the tier of the **PRIMARY claim** — the first / highest-weight claim in `curate_claim()`'s output. If the product markets multiple co-equal claims, resolve to `min(tier among primary claims)` (conservative) rather than `max(across all including secondary mentions).`

Alternative path: add an explicit `primary_claim_key` field to each curated product cache (or derive it from the first listed `structure_function_umbrella` entry), and resolve ONLY that claim's tier, ignoring secondary tokens.

You have full D6 latitude on which implementation is cleanest. Document the choice in the return with a 2-sentence rationale.

### What to re-run
After fixing `resolve_claim_tier`:
1. **Golden corpus 17/17** — must still pass. R3 (over-promise → cap_3_honesty_core) must still fire. R1–R17 unchanged.
2. **Full corpus re-score** → `_corpus_run_full_v3.json` (v3, not v2).
3. **Cross-corpus food invariants** — confirm food category files are byte-identical (SIE is a separate tree).

---

## Definition of Done

- [ ] `resolve_claim_tier` fix implemented + described (code path + rationale)
- [ ] Items 2/3/4 still intact (confirm no regression to the fixes)
- [ ] Golden 17/17 PASS (R3 still fires; include the exact command + exit code)
- [ ] `_corpus_run_full_v3.json` generated — grade distribution v3 vs v2 vs v1
- [ ] **S/A count defensible** — list every S and A product with its primary claim + tier ruling (this is the review table; orchestrator will spot-check)
- [ ] Cross-corpus food byte-identical confirmed
- [ ] Return includes: stable barcode/score/grade/primary-claim/binding-constraint table for ALL products; before→after distribution v1→v2→v3; exact command + output for each guard

---

## Constraints (always on)
- **EDPG candidate.** No published food score movement — food category files must be byte-identical. Confirm with `git diff --name-only HEAD -- 02_products/` filtered to food (not supplements).
- **OFF ban is absolute** — no OFF source anywhere, not even for reference.
- Engine changes follow `bari-bsip2-scoring-governance` (evidence registry update if a new ruling is made; activation scope = SIE only).
- Recommend single best fix — no A/B menus.
- **Do not launch.** SIE category go-live (D10/D1) is a separate owner call after a QA freeze on v3 corpus. Product D7 co-sign still required before any grade is consumer-facing.

---

## Return format
End your return with the machine-readable contract:
```json
{
  "task_id": "TASK-277",
  "status": "RETURNED",
  "return_date": "...",
  "agent": "nutrition-agent",
  "artifacts": [...],
  "counts": {
    "golden_fixtures_pass": "17/17",
    "grade_distribution_v1": {"S": 7, "A": 0, "B": 13, "C": 1, "D": 15, "E": 49},
    "grade_distribution_v2": {"S": 18, "A": 8, "B": 10, "C": 1, "D": 12, "E": 33},
    "grade_distribution_v3": {...},
    "s_a_products_v3": [{"barcode": "...", "name": "...", "score": ..., "grade": "...", "primary_claim": "...", "tier": "..."}],
    "regressions_vs_v2_excluding_targeted": 0
  },
  "primary_claim_fix_description": "...",
  "not_done": [...]
}
```

**Do not close this task — propose RETURNED and let the orchestrator verify.**
