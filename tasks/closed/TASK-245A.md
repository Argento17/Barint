---
id: TASK-245A
title: "Phase 0: null 21 OFF imageUrls on production cereals_frontend_v1 + granola_frontend_v1 (Argento17/bari@main)"
owner: data-agent
status: CLOSED
closed_at: 2026-06-11
close_reason: "LIVE-VERIFIED. PR #3 merged by owner (merge commit d975704c on Argento17/bari@main). Live probe of bari.digital/hashvaot/breakfast-cereals + /granola: HTTP 200, 0 openfoodfacts references in served HTML (was 21 OFF imageUrls). deployed: {repo: Argento17/bari, commit: d975704c, url: https://bari.digital, verified_at: 2026-06-11}. Residual: 21 products show placeholder cards until TASK-243 image backfill."
priority: CRITICAL
created_at: 2026-06-11
depends_on: []
blocks: []
category_id: null
summary: >
  TASK-245 Phase 0. bari.digital live pages /hashvaot/breakfast-cereals (9) and
  /hashvaot/granola (12) render 21 Open Food Facts imageUrls from cereals_frontend_v1.json
  and granola_frontend_v1.json on Argento17/bari@main. Null them (no substitutes, no other
  fields) on a fix branch; PR to main; owner merges; Vercel deploys. OFF ban: unknown is
  acceptable, OFF is not.
---

# TASK-245A — Phase 0: null the 21 production OFF imageUrls

Baseline = `Argento17/bari@main` (10cc84fa), NOT the monorepo. Fresh clone; fix branch;
change ONLY the `imageUrl` values that point at `images.openfoodfacts.org` → `null` in
`src/data/comparisons/cereals_frontend_v1.json` (9) and `granola_frontend_v1.json` (12).
No copy, no confidence, no other fields. PR → main (owner merges — production action).

## DoD
- [ ] Per-URL diff list (21 entries) in the PR body
- [ ] Branch pushed; PR opened; Vercel preview URL reported
- [ ] Preview: both pages render placeholder cards; 0 openfoodfacts requests
- [ ] No other lines changed (diff proves it)

## ORCHESTRATOR VERIFICATION (2026-06-11) — claims checked against remote artifacts
- Branch + PR refs confirmed: refs/pull/3/head == fix/task-245a-off-images @ 6a6bc14d; refs/pull/4/head == fix/task-245b-snacks-confidence @ 7c26634e.
- 245A diff vs bari/main: exactly 2 files / 21 line-pairs, all imageUrl nulls (cereals 9, granola 12). VERIFIED.
- 245B own diff (vs 245A head): exactly 1 file / 12 line-pairs, ALL on "confidence" keys. VERIFIED.
- Schema-surprise claim TRUE: prod snacks_frontend_v2.json contains 0 occurrences of confidence_label_he — the 1-field flip is the complete consumer-facing fix at this schema; canonical 4-field strings not applicable.
- Post-fix: 0 verified rows / 18 partial. VERIFIED.
- Stray leftover remote branch fix/off-images-prod (d2aef595) — delete after merge (housekeeping).
- CLOSE BLOCKED ON: owner merges PR #3 then PR #4 (production action, tripwire #2) + post-deploy live check; close requires deployed: evidence per protocol.