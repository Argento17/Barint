---
id: TASK-245B
title: "Phase 0: production snacks confidence hotfix - verified-with-null-panel rows to partial/missing_nutrition (Argento17/bari@main)"
owner: data-agent
status: CLOSED
closed_at: 2026-06-11
close_reason: "LIVE-VERIFIED. Fix merged to main via PR #5 (0745ac0d) after PR #4 was merged into its stacked base by mistake (recorded; net diff to main verified = exactly the 12-line confidence flip). Live probe bari.digital/hashvaot/snacks: embedded confidence verified=0, partial=18 (was 12 inflated). Schema note: prod file predates the 4-field confidence schema; 1-field flip is the complete consumer fix. 12 render-dead 'נתונים מלאים יחסית' expansion strings remain (parked in TASK-244). deployed: {repo: Argento17/bari, commit: 0745ac0d, url: https://bari.digital, verified_at: 2026-06-11}."
priority: CRITICAL
created_at: 2026-06-11
depends_on: []
blocks: []
category_id: null
summary: >
  TASK-245 Phase 0. Production src/data/comparisons/snacks_frontend_v2.json on
  Argento17/bari@main ships 12 of 18 products as confidence=verified with an all-null
  nutrition panel (DA-013 class; older/worse than the monorepo copy's 4). Flip every
  verified-with-null-panel row to partial/missing_nutrition using the canonical strings
  from confidence_annotation.py:43-44; only the 4 confidence fields per row; no copy edits.
  Display hotfix only — the structural fallback fix stays TASK-244.
---

# TASK-245B — Phase 0: production snacks confidence hotfix

Baseline = `Argento17/bari@main` (10cc84fa). Identify ALL rows with `confidence: "verified"`
and a null nutrition panel (preliminary scan found 12/18 — re-verify, don't trust). Per
affected row change exactly: `confidence` → `"partial"`, `confidence_label_he` →
`"חסרים נתוני תזונה"`, `confidence_tooltip_he` → the canonical partial tooltip,
`confidence_sub_reason` → `"missing_nutrition"` (strings from
`C:\Bari\03_operations\bsip2\proto_v0\src\confidence_annotation.py:43-44`).
`expansion.confidenceLabel` and all other consumer strings UNTOUCHED. PR → main
(owner merges). May share a PR train with TASK-245A (same clone).

## DoD
- [ ] Confirmed inflation set listed per product id (confidence value + panel state)
- [ ] 4-field diff per row; no other strings changed
- [ ] Branch pushed; PR opened; Vercel preview URL reported
- [ ] Preview: 0 "מבוסס על נתונים מלאים" where panel is null on /hashvaot/snacks
- [ ] Note in PR body: display hotfix; structural DA-013 fix = TASK-244

## ORCHESTRATOR VERIFICATION (2026-06-11) — claims checked against remote artifacts
- Branch + PR refs confirmed: refs/pull/3/head == fix/task-245a-off-images @ 6a6bc14d; refs/pull/4/head == fix/task-245b-snacks-confidence @ 7c26634e.
- 245A diff vs bari/main: exactly 2 files / 21 line-pairs, all imageUrl nulls (cereals 9, granola 12). VERIFIED.
- 245B own diff (vs 245A head): exactly 1 file / 12 line-pairs, ALL on "confidence" keys. VERIFIED.
- Schema-surprise claim TRUE: prod snacks_frontend_v2.json contains 0 occurrences of confidence_label_he — the 1-field flip is the complete consumer-facing fix at this schema; canonical 4-field strings not applicable.
- Post-fix: 0 verified rows / 18 partial. VERIFIED.
- Stray leftover remote branch fix/off-images-prod (d2aef595) — delete after merge (housekeeping).
- CLOSE BLOCKED ON: owner merges PR #3 then PR #4 (production action, tripwire #2) + post-deploy live check; close requires deployed: evidence per protocol.