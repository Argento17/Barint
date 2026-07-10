---
id: TASK-463
title: limitingFactors integrity: ~97 live products (all bread + all cheese + low-grade partials) falsely display 'no material limiting factors'
owner: data-agent
status: IN_PROGRESS
priority: CRITICAL
created_at: 2026-07-02
depends_on: []
blocks: []
category_id: null
summary: >
  Owner-caught on catalog A's; orchestrator census vs origin/master JSONs: bread_frontend_v4 23/23 and cheese_frontend_v5 47/47 have EMPTY expansion.limitingFactors (all grades incl D/E), plus partial empties in cookies_coffee(10, down to E 33.7), granola(7 incl D 40), cakes(4 D/E ~28), crackers(6). Shared expansion-section.tsx renders green-check 'ein gormim magbilim mahutiim' on empty - factually wrong for low grades, live on comparison pages AND catalog (catalog reuses same VMs). Clean categories (hummus/snacks/milk/juices/cereals/protein/chocolate/hard_cheeses) prove the engine CAN emit factors. Phase 1: read-only root-cause (which generator path drops them). Phase 2: fix - NOTE expansion fields are under owner description freeze; regeneration needs owner sequencing.
---

# TASK-463 — limitingFactors integrity: ~97 live products (all bread + all cheese + low-grade partials) falsely display 'no material limiting factors'

## Dispatch log (orchestrator)
- 2026-07-02 **P467 → Data Agent (Sonnet, read-only)** — root-cause the generator path. RETURNED:
  `tasks/reports/task463_limitingfactors_rootcause_2026-07-02.md`.
- 2026-07-03 **P467 ✅ ORCHESTRATOR-VERIFIED (unattended pass).** Spot-checks against code: (1)
  `merge_copy.py:136-140` omit-when-empty quote exact; (2) `author_copy.py::_limiting_factors` at
  :187; (3) `generate_page.py:~572` initializes `"limitingFactors": []` scaffolding — all TRUE.
  Root cause stands: bread + soft-cheese never had ANY explanation pass run in their entire lineage
  (scaffolding `[]` from generate_page, never filled); cookies/cakes partials = same gap on a subset;
  granola = `_limiting_factors()` story-map coverage hole (pass ran, mapping incomplete); crackers
  top-shelf empties plausible on limitingFactors but A-grade rows with 0 positiveSignals = sibling-field
  gap. **One report defect caught: its scope note claims `cheese_frontend_v5.json` does not exist —
  FALSE at origin/master (blob deec2e91); the agent read the stale local tree. Conclusion unaffected:
  orchestrator independently verified origin/master v5 = 47/47 empty limitingFactors AND 47/47 empty
  positiveSignals.** Fix scope must cover positiveSignals too (same producer pass everywhere).
- **Phase 2 (fix) remains BLOCKED on the owner description freeze** (expansion = product-level copy;
  owner sequencing decision). Interim frontend mitigation already LIVE (PR #45, board 2026-07-02).
  Status stays IN_PROGRESS.
