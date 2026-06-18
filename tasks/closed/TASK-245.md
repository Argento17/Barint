---
id: TASK-245
title: "Production re-point program (Option C): bari.digital from Argento17/bari@main to Barint master + bari-web/ root"
owner: orchestrator
status: CLOSED
priority: CRITICAL
created_at: 2026-06-11
closed_at: 2026-06-11
cc_reviewed: 2026-06-11
deployed:
  repo: Argento17/Barint
  commit: 5fbac579
  url: https://bari.digital
  verified_at: 2026-06-11
close_reason: >
  All phases executed and live-verified by CC. Phase 0: 245A/245B closed with deployed
  evidence (separate records). Phase 1: release branch merged to Barint master (a9b29566).
  Phase 2: payload resolved — salty v4 shipped (live markers verified: partial=22, verified=7,
  0 stale labels, 0 OFF refs); yogurts hold resolved by owner-endorsed decoupling (master v3
  ships interim with 0 OFF refs live-verified; re-acquired v4 in remediation under
  TASK-249/250 after QA+red-team FAIL). Phase 3a: throwaway project barint.vercel.app built
  from Barint+bari-web root, 8/8 routes 200, 0 OFF refs. Phase 3b: owner flipped Vercel
  project 'bari' (root dir bari-web, repo Barint, branch master) and triggered the production
  deployment; bari.digital live-verified by CC: 9/9 routes 200 (incl. salty-snacks newly live
  and breakfast-cereals), 0 openfoodfacts/off_api refs on every page. The production/local
  split (audit F-01) is closed: the repo where work happens is the repo that deploys.
  Known non-blocking finding logged at close: "NOVA" appears in consumer-visible insight
  prose on the live yogurts v3 page (9 hits; replaced wholesale by TASK-249's v4) and in
  metric cells on maadanim (86) / hummus (70) where it may be the designed column — routed
  for an editorial ruling, not a rollback condition.
blocks: []
category_id: null
summary: >
  Owner-approved 2026-06-11 (Option C, phased). Phase 0: port 4 defect fixes directly to
  Argento17/bari (OFF image nulls on cereals/granola, snacks confidence hotfix) — 245A/245B.
  Phase 1: merge release/prod-integrity-242 into Barint master as a straight PR (build-green
  reference unit: salty v3->v4, de-OFF 4 JSONs, frozen-veg removal, snacks hotfix, OFF client
  stub). Phase 2: owner sign-off on the full enumerated re-point payload; HOLD CANDIDATES:
  salty route (de-wire if unsigned by re-point) + yogurts (OFF-born corpus, pull-vs-reacquire
  ruling pending). Phase 3a: throwaway Vercel project on Barint+bari-web/ for real-infra
  validation (env vars, root dir, branch=master). Phase 3b: edit existing Vercel project
  'bari' repo pointer (2-min revert rollback).
---

# TASK-245 — Production re-point program (Option C)

## Owner ruling (2026-06-11)
Option C selected over A (no git merge path between monorepo `bari-web/` subtree and the
standalone-layout production repo — only an unreviewable scripted flatten) and B (surgical
ports forever; the two-repo drift class stays alive). Re-pointing Vercel to Barint +
root directory `bari-web/` makes the repo where work happens the repo that deploys —
permanently closing the local/production split (audit F-01 class).

## Supersession clause (registry coherence)
**TASK-242's closure disposition "do NOT merge the branch" is SUPERSEDED for the Phase 1
purpose by this owner-approved program.** That clause was written when merge-to-Barint was
being mistaken for a production action (Barint had no deploy integration). Under Option C,
merging `release/prod-integrity-242` (head `a5b4171b`) into Barint master is a **monorepo
prep step** — not a production action until Phase 3b flips the Vercel pointer. The branch's
"reference evidence only" status converts to "Phase 1 merge source." All other parts of the
TASK-242 close_reason (topology facts, production baseline correction, no-deploy-occurred)
stand unchanged.

## Phases
- **Phase 0 — stop the bleeding on current production (no tripwire; runs in parallel).**
  Sub-tasks **TASK-245A** (null 21 OFF imageUrls in `cereals_frontend_v1.json` (9) +
  `granola_frontend_v1.json` (12) on `Argento17/bari@main`) and **TASK-245B** (flip the 12/18
  verified-with-null-panel snacks rows to partial/missing_nutrition, canonical strings from
  `confidence_annotation.py:43-44`). Fix branches pushed to Argento17/bari; owner merges the
  PRs; Vercel auto-deploys.
- **Phase 1 — clean Barint master.** Straight PR `release/prod-integrity-242` → `master`
  (same repo, same tree shape, all gates green incl. real `next build`; contents: salty
  v3→v4 + de-OFF'd v2 JSONs + frozen-veg removal + snacks 4-row hotfix + OFF client stub +
  CLAUDE.md hard rule + reinstated TASK-238). Owner merges.
- **Phase 2 — payload sign-off.** Orchestrator produces the full enumerated diff of Barint
  master `bari-web/` vs `Argento17/bari@main` (routes added/changed + data-version bumps +
  shared-surface changes). Owner signs the §8 decisions against that list, bundle or
  sequence. **Hold candidates:** (1) **salty-snacks** — if v4 sign-off hasn't landed by
  re-point, de-wire the route from master before Phase 3b; (2) **yogurts** — master's
  `yogurts_frontend_v3.json` is OFF-born at the data level (images nulled, corpus identity
  still OFF); must NOT ship silently — held until the pull-vs-re-acquire ruling.
- **Phase 3a — dress rehearsal.** Throwaway Vercel project pointed at Barint, root directory
  `bari-web/`, production branch `master` (Barint has no `main`), env vars replicated from
  the `bari` project (incl. `NEXT_PUBLIC_GLASSBOX_D5D6`). Real preview URL on real infra;
  run the release smoke checklist against it.
- **Phase 3b — the flip (owner-only, tripwire #2).** Edit the existing Vercel project
  `bari`: repo pointer → `Argento17/Barint`, root dir `bari-web/`, branch `master`. No DNS
  change. **Rollback = revert the repo pointer (≈2 minutes).** Post-flip: production smoke
  vs bari.digital, then this task's close requires `deployed:` evidence per the new close
  convention.

## DoD
- [x] 245A merged + live: 0 `openfoodfacts` requests on /hashvaot/breakfast-cereals + /hashvaot/granola (re-verified post-flip 2026-06-11: both 200, off-refs=0)
- [x] 245B merged + live: 0 verified-with-null-panel rows on /hashvaot/snacks (TASK-244 structural fix also merged + live)
- [x] Phase 1 PR merged to Barint master (a9b29566); master build green
- [x] Phase 2 payload resolved: salty v4 shipped + live-verified; yogurts hold resolved by owner-endorsed decoupling (v3 interim, v4 in TASK-249 remediation)
- [x] Phase 3a staging project (barint.vercel.app) built + 8/8 smoke green on real infra
- [x] Phase 3b flipped by owner; bari.digital serves Barint master @ 5fbac579; post-flip smoke 9/9 green, 0 OFF refs corpus-wide
- [x] close_reason cites deployed: {repo: Argento17/Barint, commit: 5fbac579, url: https://bari.digital, verified_at: 2026-06-11}
