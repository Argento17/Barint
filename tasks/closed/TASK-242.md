---
id: TASK-242
title: "Emergency Production Integrity Release — close the prod/local split (salty v4, OFF ban enforcement, frozen-veg removal, de-OFF, confidence)"
owner: orchestrator
status: CLOSED
closed_at: 2026-06-11
priority: CRITICAL
created_at: 2026-06-11
depends_on: [TASK-228, TASK-237, TASK-241]
blocks: []
roadmap_impact: true
work_type: release
release_branch: release/prod-integrity-242
reviewers: [data-agent, frontend-agent]
qa_owner: qa-agent
close_reason: >
  SUPERSEDED / NOT EXECUTED — owner ruling 2026-06-11. The release's core production assumption
  was invalidated by the deploy-topology investigation: bari.digital deploys from
  Argento17/bari@main (standalone app layout; production commit 10cc84fa via Vercel project
  'bari'), NOT from Argento17/Barint, which has ZERO Vercel deployments in its entire history.
  release/prod-integrity-242 (head ab3f0c94) exists only in Barint, so merging it could never
  have updated production. NO production merge or deploy occurred; nothing shipped to consumers
  under this task. Production baseline correction: the fabricated salty v3 was NEVER live (no
  salty-snacks route exists in production) and frozen-vegetables was NEVER live — both defects
  existed only on the never-deployed Barint master. The ACTUAL live issues are narrower: 21 OFF
  imageUrls on /hashvaot/breakfast-cereals (9, cereals_frontend_v1.json) and /hashvaot/granola
  (12, granola_frontend_v1.json); snacks confidence inflation on the PRODUCTION snacks JSON
  (12 of 18 products 'verified' with null nutrition — worse than the monorepo copy's 4);
  yogurts_frontend_v2 OFF-derived per reports/open_food_facts_contamination_audit_v1.md (no
  literal OFF strings, silently contaminated); and the production repo being a stale fork
  (diverged at 11c6ea4b) disconnected from all active Bari work. Disposition: do NOT port the
  full tree; do NOT merge the branch; release/prod-integrity-242 in Barint is retained as
  REFERENCE EVIDENCE ONLY (its content — salty v4, OFF client stub, CLAUDE.md hard rule,
  reinstated TASK-238, de-OFF'd JSONs, snacks 4-row hotfix, all gates green incl. real
  next build — remains valid work product for whatever ships next). Follow-up recommendation:
  handle the real production issues (OFF images on 2 pages, prod snacks confidence, yogurts
  ruling) as separate, narrowly-scoped actions against Argento17/bari@main, decoupled from any
  future full-repo-sync decision; re-point TASK-243/TASK-244 baselines from the monorepo copy
  to the production copy accordingly.
---

# TASK-242 — Emergency Production Integrity Release

> **CLOSED 2026-06-11 — SUPERSEDED / NOT EXECUTED.** See `close_reason`. The branch
> `release/prod-integrity-242` (Barint, head `ab3f0c94`) is reference evidence only: do not
> merge, do not deploy from it. Production was never served from Barint; the task's "prod/local
> split" framing was based on the wrong production source. The validated work product on the
> branch (and the §below scope/gates record) feeds the successor production-remediation work.

> ~~**This release blocks all other Bari work** until merged + verified on the production URL.~~
> (Block lifted at closure — the release was not executed.)

## Why
The external **Full Cycle Health Audit** found a **production/local split**: production master still
serves broken or contaminated pages while the fixes exist only locally or on unmerged branches
(chiefly `salty-snacks-v4`). Confirmed live defects on master:
- **salty-snacks** page imports `salty_snacks_frontend_v3.json` (54-product, pre-rebuild) — the
  verified real v4 corpus (29 products, real Yochananof panels, TASK-237 + TASK-241 rescue) is not shipped.
- **frozen-vegetables** route is **live in production** (merged `eae626e3` / `bfc87ea2` / `c061b82e`)
  but is governed as **score-free, Phase-1-locked, NOT a launch precedent** (memory
  `frozen_vegetables_v2_scorefree`). It should not be publicly routed in this release.
- **OFF**: the project-wide ban (CLAUDE.md Hard rules; memory `off_ban_hard_rule`; TASK-238) is **not
  enforced in code** — the OFF client is live, and OFF literal strings remain in shipped production data.
- **Registry contradiction**: TASK-241's `owner_signoff` still says "OFF stays LOCAL / TASK-238
  retracted" — contradicting the reinstated project-wide ban.
- **Confidence inflation** + **dead/leaky JSONs** present in the production data tree.

## Scope (release-only — architecture backlog explicitly EXCLUDED)
1. Ship verified **salty-snacks v4** real corpus + flip the page import v3 → v4 (29 products).
2. **Enforce the OFF ban in code**: commit the CLAUDE.md Hard rule + hard-disable the OFF client
   (`OffDisabledError` on every entry point).
3. **Reconcile TASK-238 / TASK-241** registry contradiction (project-wide ban wins; salty complies).
4. **De-OFF contaminated live JSONs**: scrub OFF literal strings from shipped data; remove OFF-bearing
   archive JSONs so `grep` over production data = 0.
5. **Remove the frozen-vegetables route** from production (7 files + registry + hashvaot card).
6. **Fix live snacks confidence inflation** (no verified/full-data confidence where the nutrition
   panel is missing) — *reviewer-gated, see Open items*.
7. **Remove dead/leaky JSONs** from `bari-web/src/data/comparisons/` (crackers_staged, olive_oil,
   superseded salty v1/v2/v3, OFF archive files).
8. **Image first-paint fix** — include ONLY because it is already clean + isolated (additive `eager`
   prop on `BariProductThumbnail`, defaults `false`, backward-compatible).

## Out of scope (DO NOT ship in this release)
Category copy-polish on bread/butter/cereals/yogurts JSONs; shared-component refactors
(`comparison-row`, `comparison-table`, `comparison-metric-column`, `corpus.ts`, `view-models`);
the evals / project-comp / governance backlog on `salty-snacks-v4`. These stay on their branches.

## Approach
- Clean release branch `release/prod-integrity-242` cut **from production master** in an isolated
  git worktree (no disturbance to the active working tree).
- **Manually stage only reviewed files** (no wholesale branch merge — `salty-snacks-v4` carries a
  large unrelated backlog).
- Produce a **release_gate report** (`03_operations/reports/release_gate_242.md`) before merge.

## Validation gates (all must pass before merge)
- [ ] `git diff master...release/prod-integrity-242` contains only release-scope files
- [ ] `tsc --noEmit` + `next build` pass
- [ ] frontend JSON validator passes
- [ ] OFF grep across production data (`bari-web/src/data`) = **0**
- [ ] frozen-vegetables production route removed (no file, no registry id, no card, no dangling import)
- [ ] salty-snacks page imports **v4**, not v3
- [ ] no fake barcodes / dead image hosts in salty snacks (real EANs, single real retailer host)
- [x] no verified/full-data confidence where the nutrition panel is missing — **PASS corpus-wide
      for release scope.** Salty v4 clean by construction; snacks inflation (snk-003/007/009/020,
      DA-013 class) confirmed by data-agent review and FIXED in-release via the copy-free 4-field
      hotfix (2026-06-11). Structural fallback fix + LIVE_FILES staleness remain TASK-244.
- [ ] **post-merge production URL verification** (the live site, not local)

## Deliverables
TASK file · release branch · exact file list · validation report · preview URL · production
verification checklist · PASS / PASS WITH FIXES / FAIL verdict.

## Open items / reviewer sign-off required before merge
- **data-agent**: confirm the snacks confidence fix (item 6) is isolated from copy-polish before it
  is staged (if not isolatable → TASK-244 fast-follow); re-affirm salty v4 panel provenance
  (Yochananof + 4 Shufersal rescues, zero OFF).
- **Registered fast-follows:** TASK-243 (retailer image backfill for the 39 nulled OFF images —
  not a merge blocker; "unknown is acceptable, OFF is not") · TASK-244 (snacks confidence
  structural fix, DA-013 class — merge blocker ONLY if data-agent lands it copy-free in time).
- **frontend-agent**: confirm the pulled salty component does not depend on the EXCLUDED shared-
  component changes; confirm `tsc` + `next build` clean after frozen-veg removal.
- **owner**: the **merge to production master** is the irreversible, consumer-facing step (decision
  tripwire #2) — orchestrator stages + gates; owner authorizes the merge/deploy.

## Return block
Branch name, exact staged file list, validation report path, gate verdict, preview URL, and the
production verification checklist. Do NOT self-close — orchestrator records CLOSED only after
post-merge production-URL verification passes.
