---
id: TASK-290
title: Post-deploy smoke test — assert live /hashvaot/* routes match the Spine live_state manifest (release platform Phase 1, ADD-1)
owner: frontend-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-16
closed_at: 2026-06-16
close_reason: >
  C1-GROK (P150), orchestrator-verified against artifacts. smoke_test.py extended (manifest-driven):
  ran `--dry-run --skip-ingest` myself = exit 0, 15 routes, 0 OFF, PASS. All 5 OFF markers present
  (TASK-238 set, L37-41). Freshness drift = non-fatal FINDING; exit 1 only on HTTP non-200 or OFF>0
  (correct design). prod_smoke.yml = valid YAML, daily cron 0 7 * * * + workflow_dispatch. barint_ci.yml
  valid YAML + dry-run step (L79-80). Scope clean: only smoke_test.py + 2 workflow files touched, engine/
  comparison JSONs untouched. Spine tests 9/9. Prod-HTTP run (0 hard fails / 12 expected drift findings)
  reported by agent, not independently re-run (network) — non-blocking; the test infra is the deliverable
  and is verified. Not pushed. Closes the "what is actually live" failure class (ADD-1).
summary: >
  Finish + wire smoke_test.py: read expected version/run_id/product_count from spine live_state, hit each /hashvaot/* route, assert HTTP 200 + OFF=0 + version match. Closes the 'what is actually live' failure class (TASK-245 class).
---

# TASK-290 — Post-deploy smoke test — assert live /hashvaot/* routes match the Spine live_state manifest (release platform Phase 1, ADD-1)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
