---
name: rescore
description: Flip a Bari scoring switch, re-score every affected category through the spine, diff against the committed baseline, and emit a self-verifying movement table. Use for any scoring-flag what-if or spine_flip.
---

# /rescore — Scoring switch → re-score → movement table

**Owner lane:** Orchestrator (C4) + Nutrition (co-sign on rule semantics). Re-scoring is
expected work — an owner-initiated `spine_flip` that re-flows every category is **NOT** a
tripwire. Changing the *scoring philosophy or a published rule's intent* still is (escalate).

## Use this when
- "Re-score with `BARI_X` on", "what does flipping <flag> do", "run a spine flip", "re-score <category>".
- Any change that could move published scores and you need the before/after movement, verified.

## The pipeline (do not reorder)

1. **Run the flip.**
   ```
   python 03_operations/page_generator/spine_flip.py --set BARI_X=on [--set BARI_Y=off ...] --note "<why>"
   ```
   - Repeat `--set FLAG=VAL` per flag. Output bundle lands in
     `_rescore_staging/_spine_runs/<utc-ts>/` (override with `--out-dir`).
   - Add `--via-spine` for the incremental DAG (skips unchanged stages, records lineage in
     `spine.db`); add `--force` to re-run all stages anyway.
   - Internally this runs: re-score (`rescore_all.py`, drop-in via `render_fields.py`) →
     `copy_stage` (carry + author-set) → gates (OFF=0, score==trace) → deploy-ready bundle.

2. **Nothing is frozen — no exceptions.** Every live category re-flows on every flip:
   **no category freeze gate, no exit-2 hard block, and no per-category carve-out.** Never
   re-arm the old `class: frozen` gate. **Milk is no longer a carve-out** (owner 2026-06-22:
   "de-freeze Milk — I instructed not to have freeze pages again; it just complicates
   everything"). Milk re-flows and ships exactly like every other category; do not pause it
   for special approval.

3. **Build the movement table by diffing against the COMMITTED baseline** — never against a
   self-capture (Shadow1 CI law). `rescore_all.py` writes the per-shelf delta report to
   `_rescore_staging/`. Compare `--approved` (new) vs the promoted committed baseline JSON.

4. **Verify the re-flow** before reporting:
   ```
   python 03_operations/page_generator/conformance.py --all
   ```
   12/12 categories must still re-flow.

## Return contract (self-verifying — required)
A re-score report is untrustworthy without distributions. For **each** affected shelf report:
- Full grade distribution + count + stdev + most-common-score-count (trace-derived, with the
  command that produced them — not self-reported).
- A **stable table**: `barcode · old_score · new_score · old_grade · new_grade · caps_fired`.
- Cross-corpus baseline diff vs the committed baseline (Δ per product, net movement).
- Honest confidence: separate what you *verified* (and how) from what you *believe*.

## Never
- Never auto-deploy. The bundle is deploy-*ready*; the owner merges (deploy topology is a
  separate gated step — publishing the monorepo is a migration, not a push).
- Never manufacture differentiation: genuine score clustering is an honest finding, not a bug.
- Never cap an engine-recognized grade to enforce a framing.
- Never use OFF data anywhere in the re-score.

## Related
`bari-bsip2-scoring-governance` (rule/evidence registry), `conformance` skill, `telemetry` skill.
