---
id: TASK-460
title: Stale hardcoded grade-distribution prose in page-data adapters (live defect, found post-#38 deploy)
owner: content-agent
status: CLOSED
priority: CRITICAL
created_at: 2026-07-02
closed_at: 2026-07-02
close_reason: >
  Both passes merged: PR #39 (pass 1: 55 claims audited, 9 stale fixed, QA gate-2 GO_WITH_FIXES + re-verify
  GO 83e09811) and PR #40 (pass 2: 21 files incl. featured cards + SEO descriptions; five QA gates, final GO
  fc1f93e3; several cards now derive stats live from JSON). 105 total claims audited / 33 stale fixed.
  Production re-verify by orchestrator 2026-07-02 post-#37-deploy with cache-bust: "655" = 0 hits and
  "38 פרמטרים" = 0 hits on /hashvaot and /hashvaot/supermarket (earlier suspicion was Vercel cache — resolved).
  Follow-ups routed, HELD under owner description freeze: RT-4 orphaned copy, RT-5 prologue leakage,
  cookies-coffee page_copy regen. Gate gap (no gate audits numeric claims in TS prose) → TASK-453 backlog.
depends_on: []
blocks: []
category_id: null
summary: >
  Hero/prologue strings hardcoded in bari-web/src/lib/comparisons/*-page-data.ts carry grade distributions/counts that predate the de-anchor sweep and TASK-449 (brined says 9A/20B/5C/2D vs true 3A/18B/13C/2D — LIVE now; cereals + juices also hit). Audit EVERY adapter's numeric/grade claim vs its category JSON, fix by re-deriving or removing hardcoded numbers, two-gate, PR. Root cause: copy with numbers living in TS adapters outside the JSON pipeline that gates audit.
---

# TASK-460 — Stale hardcoded grade-distribution prose in page-data adapters (live defect, found post-#38 deploy)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
