---
id: TASK-160
title: Live comparison data cleanup — yogurt images, dead-record scrub, _meta fixes, orphan-JSON archive
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-02
completed_at: 2026-06-02
closed_at: 2026-06-02
closed_by: cc-agent
close_reason: "CC close-gate PASS — verified against artifacts. (a) yogurts_frontend_v2.json = 11/11 imageUrl populated (all Cloudinary/Shufersal urls, none null/empty). (b) dead-record scrub confirmed: vs the import baseline, hummus removed exactly 2 ids (bsip1_7296073733317/348, the insufficient-data records) and maadanim removed exactly 6 — both sets are excluded products only, NOT score edits. (c) _meta correct: hummus scored_count/product_count=64; maadanim product_count=77, corpus_record_count=84, count_note present. (d) orphans archived: hummus_frontend_v1/v2 + yogurts_v1 are git-deleted from src/data/comparisons/ and present in 99_archive/orphaned_comparison_datasets_2026-06-02/. SCORE INTEGRITY (this task): snacks_frontend_v2.json shows 0 surviving-product score/grade changes — display-only, as claimed. snk-006 image confirmed genuinely unrecoverable (no persisted source) -> carved off to BLOCKED TASK-160A so it is not lost."
roadmap_impact: false
depends_on: [TASK-156]
blocks: [TASK-160A]
category_id: null
cc_comments:
  - date: 2026-06-02
    flag: fyi
    text: "Score-integrity (not a defect here): WT score deltas — hummus 58, maadanim 70 — are the shipped EV-029 rescores (TASK-150/149), uncommitted only (no subtree commit since import). Prior bread '73→82 B→A' flag WITHDRAWN: line-diff misread a score re-sort; id-matched diff = 0 score / 0 grade. Bread's only real change = additive `unknowns` transparency field (TASK-130 norm pass). No new task; commit is housekeeping (user holding)."
summary: >
  (a) yogurt images: builder reads image_url from BSIP1, yogurts_frontend_v2.json now 11/11 imageUrl; (b) scrubbed 5 dead records (3 maadanim pudding-powders, 2 hummus non-spreads) from JSON + loader exclusion lists; (c) _meta fixed (hummus scored_count 64/64; maadanim product_count 77 + corpus_record_count 84 + count_note); (d) 3 orphaned JSONs git-mv'd to 99_archive. corpus-validate 0 errors, tsc 0, next build 34 routes. snk-006 thumbnail BLOCKED (no persisted image source) -> follow-up sub-task. NO scores changed (yogurt diff=imageUrl-only).
---

# TASK-160 — Live comparison data cleanup — yogurt images, dead-record scrub, _meta fixes, orphan-JSON archive

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
