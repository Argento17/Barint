---
id: TASK-484
title: Page-narrative phrasing sweep: antithesis+em-dash in 6 *-comparison-page-data.ts (+milk JSON) hero/prologue/SEO — editorial two-gate, preserve owner-voice
owner: content-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-03
closed_at: 2026-07-03
close_reason: "SHIPPED LIVE PR #63 (merged 7756eab8). Page-narrative antithesis+em-dash sweep, 5 page-data.ts + milk page_copy; ~24 reworded, em-dash 39→0, 12 keeps QA-agreed, 3 meaning-drifts caught by QA + fixed round-2 + orchestrator-verified; 0 score/row touched. Two-gate satisfied. Follow-ups logged: milk product-row antithesis, bread/snacks SEO."
depends_on: []
blocks: []
category_id: null
summary: >
  Page-narrative phrasing sweep: antithesis+em-dash in 6 *-comparison-page-data.ts (+milk JSON) hero/prologue/SEO — editorial two-gate, preserve owner-voice
---

# TASK-484 — Page-narrative phrasing sweep (from TASK-474 systemic finding)

Worktree C:\bari_wt_t484, branch content/task484-phrasing. 5 page-data.ts (bread/choc-bars/choc-tablets/hummus/snacks) + milk JSON page_copy. protein-bars EXCLUDED (defer w/ TASK-477). Ledger: tasks/returns/TASK-484_ledger.md.

## Round 1 (Content/Sonnet, commit 8469f28f) + Adversarial QA = GO-WITH-FIXES
- ~25 antithesis found, ~24.5 reworded, 12 kept (owner-voice signature, disclaimer boilerplate, myth-corrections, two-sided comparisons, "הערת קטגוריה —" header convention, UI label); narrative em-dash 39→0. Isolation clean (6 files, 0 score/grade/rowVerdict/insightLine, tsc 0, JSON valid) — orchestrator + QA both verified.
- **QA independently AGREED all 12 keeps + the snacks item-10 partial hedge.** Residual-antithesis scan clean.
- **QA caught 3 MEDIUM meaning-drifts (genuine, not cosmetic) → round 2 (content author resumed):**
  1. choc-tablets hero+prologue[0]: epistemic "name doesn't tell you what's inside" → overclaiming causal "healthiness = cocoa:sugar ratio" (methodology weighs more). Restore epistemic framing.
  2. choc-tablets categoryNote[0]: dropped explicit "not a health product" health-halo guard → weak "still in candy family". Restore strong misreading-guard (guarded-negation form allowed, QA-approved class).
  3. milk caveat.notes[1]: "measured against its own peers" → "exactly like cow's milk" introduces cross-category equivalence claim not in original. Rephrase to own-family scope.
- On round-2 return: orchestrator verifies the 3 strings only → push → owner PR (tripwire-2 consumer copy deploy).
## Round 2 (content author resumed, commit a6fe671b→rebased 86384a9e) — 3 meaning-drift fixes, orchestrator-VERIFIED
- Fix 1 choc-tablets hero/prologue: restored epistemic "השם מספר פחות מההרכב שבפנים" framing, no single-ratio overclaim. Fix 2 categoryNote[0]: strong health-halo guard back in approved `ולא ש` form ("ולא שהמוצר הוא מוצר בריאות"). Fix 3 milk caveat: "נמדד מול משקאות מאותה משפחה" peer-scope, no cow's-milk equivalence.
- Verified: round-2 delta = only the 3 strings (+ledger); rebased onto current master (1b021bd2) CLEAN (no overlap w/ #62); 6 files+ledger, tsc 0, JSON valid. Two-gate SATISFIED (author + QA cleared-all-but-3 + 3 fixed per QA's explicit guidance + orchestrator-verified).
- **SHIPPED → PR #63** https://github.com/Argento17/Barint/pull/63 (consumer copy = tripwire-2, owner merge). CLOSE on merge; prune worktree t484.

## Follow-ups logged
- **Scope gap:** bread + snacks SEO metaDescription live in separate files (bread-analysis-content.ts, data/blog/snack-analysis.json), OUT of the 6-file scope → extend the sweep there.
- **Milk PRODUCT-ROW antithesis (NEW):** milk's rowVerdict/positiveSignals/limitingFactors carry ~10 "X, לא Y" (e.g. "נגיעת שקדים, לא בסיס שקדים"; 1 "אלא") — milk was excluded from the PR#51/#53 overhaul as the old "gold standard" (now retired) → milk product copy needs the same antithesis sweep the other categories got. → new content task.
