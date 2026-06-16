P23 / TASK-254 — Integrate the tightened cereals copy into the live site + QA
propagation. The remediation copy is gate-clean (P17 machine gate: 0 hard fails;
orchestrator read; P21 tightening; orchestrator re-gate: PASS). Now ship it.

SOURCE (authored copy, do NOT re-edit the words):
`02_products/breakfast_cereals/cereals_copy_remediation_draft_v2.json`
— per product: `barcode`, `badge{score,grade}`, `new_insightLine`, `new_rowVerdict`.

DO (Frontend):
1. Locate where the live cereals page reads its per-product copy (start at
   `bari-web/src/data/comparisons/cereals_frontend_v2.json` and the registry
   `bari-web/src/lib/comparisons/registry/categories/breakfast-cereals.ts`). Cite the file + the
   exact field names the page renders for the collapsed row verdict + insight line.
2. For each of the 34 products, write the draft's `new_insightLine` → the live
   insightLine field and `new_rowVerdict` → the live row-verdict field, MATCHED BY
   BARCODE. Change ONLY those two string fields. Do not touch score, grade, nutrition,
   ingredients, confidence, or any other product field. Do not change page-level
   strings (hero/prologue/methodology) — this remediation is per-product copy only.
3. If the live JSON has a product the draft doesn't cover (or vice-versa), STOP and
   report the mismatch — do not guess.

DO (QA, after integration):
4. Verify propagation: the rendered cereals page shows the new strings (no stale
   copy); all 34 grades/scores unchanged vs before; `tsc --noEmit` + `next build`
   clean; no broken routes. Spot-check the 5 products that had the worst live lies
   (סיני מיני C, קוקומן C, דליפקאן D, ריבועי קינמון D, טריקס E) now read correct
   grade + no sodium causation.

RULES: only the two string fields per product change; no score/grade/data changes;
no page-string changes; no OFF; reversible (one PR/commit). Do NOT deploy — leave it
as a committed change for review.

RETURN BLOCK: file(s) changed + exact field names; confirm 34/34 mapped by barcode
with no leftover/missing; grades unchanged (before/after identical); build+tsc clean;
the 5 spot-checks; anything blocking. Propose RETURNED.

NOTE for the authoring agent (process, not content): the P21 pass overwrote draft_v1
in place (v1 == v2 byte-identical). Going forward, leave each draft vN immutable and
write the next version as a new file so diffs stay verifiable.

---
After you send this to the agent: open tasks\DISPATCH_BOARD.md and put an `x` in the
P23 line under 📬 Signals.
