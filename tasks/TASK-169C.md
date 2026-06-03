---
id: TASK-169C
title: P2/P3 frozen wave — milk run_004 recal re-approval + rescore (BARI_RECAL_P0)
owner: data-agent
status: BLOCKED
priority: MEDIUM
created_at: 2026-06-03
blocker: "Owner per-move sign-off to begin frozen run_004 rescore (TASK-169 P2 gate); frozen milk invariant (run_004, 85/A) cannot move without owner re-approval."
depends_on: []
blocks: []
category_id: null
summary: >
  Frozen wave under TASK-169. P0 v1.1 model showed the recal leak CLOSED on fluid milk (lactose-free 87.3->79.3/B, 0 A-crossings, 85/A HELD) — expected to be a confirm-and-hold wave, not a promotion. Deliverable: rescore milk run_004 with BARI_RECAL_P0=on into a new run id, diff vs live, confirm no frozen-invariant breach, owner per-move sign-off, then reship milk frontend JSON (or formally confirm no change). Flag OFF = byte-identical rollback.
---

# TASK-169C — P2/P3 frozen wave — milk run_004 recal re-approval + rescore (BARI_RECAL_P0)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
