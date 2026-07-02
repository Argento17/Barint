# P271 / TASK-418 refresh copy regen — grade movers + invalidated claims (route: C1-Sonnet content)

## Context
The TASK-418 bundled refresh (owner-approved) re-scored hard_cheeses + cheese + cereals. Scores/grades are
already patched in the worktree frontend JSONs (verified). Now the score-dependent COPY must be made coherent
with the new scores BEFORE deploy — a page whose grade changed but whose verdict still argues the old grade is
a content failure. This is DRAFT copy; it does NOT ship until BOTH the Content gate and the Adversarial QA gate
sign off (content sign-off HARD RULE). You are the Content lane. Do not deploy, do not close.

## Environment
- Work in the EXISTING isolated worktree **C:\bari_p270** (its build agent has finished; it already holds the
  PATCHED score JSONs + the input artifacts). Work only there. Run NO git commands (zero git ops).
- Patched score JSONs to edit copy in (already carry the NEW scores/grades — do NOT change those):
  `C:\bari_p270\bari-web\src\data\comparisons\{hard_cheeses_frontend_v4,cheese_frontend_v4,cereals_frontend_v2}.json`.
- Inputs: `C:\bari_p270\tasks\returns\P270_audit_pack.json` (per-barcode deltas + mechanism) and
  `C:\bari_p270\tasks\returns\P270_copy_impact.json` (19 impacted barcodes).

## Scope — edit ONLY what the score move actually invalidated
1. **The 5 GRADE MOVERS — full rewrite** of insightLine + rowVerdict + expansion.comparisonContext (and any
   other prose that argues the grade) to the NEW grade and NEW standing:
   - hard_cheeses `4122270` C→B (67.0) and `7290110320850` C→B (67.0): they are NO LONGER "among the lowest"
     — at 67.0 they sit in the mid B-cluster. Remove the "C / among the lowest / B-C border" framing; state
     the real new standing. Verify the new rank against the FULL corpus (do NOT assert lowest/highest without
     checking) — [[superlative_claims_need_corpus_rankcheck]].
   - cheese `3523230065467` C→B (68.0), `7290019635581` E→D (37.0); cereals `7290017894911` D→C (50.0).
2. **Ranking / superlative claims on ANY moved product** (even same-grade): re-check every "הנמוך/הגבוה/מבין/
   בין ה… בסקירה" claim for the 30 moved barcodes against the new corpus order; fix any now-false one.
3. **Number citations:** if a moved product's prose cites the OLD score number, update to the new number.
   Same-grade moves that cite only the grade letter (unchanged) and no ranking = LEAVE UNTOUCHED (most of the
   14 non-grade movers are ≤2pt and need no edit — do not churn copy for its own sake).
4. Leave every non-impacted product's copy byte-for-byte unchanged.

## Voice + hard gates (Tom's voice v1.0)
- Carry the real number; finding-first; no apology. **HARD BANS (auto-fail):** code-tokens/E-codes in prose
  (use plain additive names), nutrition-fact tails in verdicts, brand-directed rhetoric, information-dumping.
- Never invent data. OFF BANNED. Do not touch scores/grades/nutrition/ingredients — copy fields only.

## Return (write `C:\bari_p271\tasks\returns\P271_return.md` + final message)
- Table: barcode | category | old→new grade | fields rewritten | rank-claim check result.
- List of moved products you INTENTIONALLY left untouched (same-grade, no ranking/number citation) with why.
- Confirm 0 score/grade/nutrition edits (copy only); git-diff-style field list.
- Machine-readable return contract (`01_framework/operations/return_contract_v1.md`): artifacts w/ sha256,
  counts w/ named denominators, distribution marker. Propose RETURNED (DRAFT — awaiting Adversarial QA gate).
