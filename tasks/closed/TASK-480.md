---
id: TASK-480
title: Cakes live-page accuracy fix: caveat 63->62 + filter-chip counts + antithesis/em-dash (from TASK-474 red-team CRITICAL)
owner: content-agent
status: CLOSED
priority: CRITICAL
created_at: 2026-07-03
closed_at: 2026-07-03
close_reason: >
  SHIPPED LIVE. PR #60 merged → origin/master 8244382e (verified: commit 6a969d0f ancestor of origin/master). Cakes caveat 63→62 + 3 filter-chip counts corrected to true corpus values (D=1, has_phvo=18, no_phvo=44), 3 antithesis lines reworded to positive declaratives, scoped-field em-dashes 7→0. Two-gate: content author ×2 + Adversarial QA GO-WITH-FIXES (sole HIGH RT-480-1 resolved round 2, orchestrator-verified). Isolation 1 file 13/13, 0 score/grade/rank change (G7 PARITY PASS 62=62). Worktree C:\bari_wt_t480 pruned. Follow-ups routed (non-blocking): RT-480-2 stale code comment (frontend), RT-480-3 systemic d4_additives em-dash/antithesis site-wide (generator pass).
depends_on: []
blocks: []
category_id: null
summary: >
  Cakes live-page accuracy fix: caveat 63->62 + filter-chip counts + antithesis/em-dash (from TASK-474 red-team CRITICAL)
---

# TASK-480 — Cakes live-page accuracy fix: caveat 63->62 + filter-chip counts + antithesis/em-dash (from TASK-474 red-team CRITICAL)

Source: TASK-474 cakes red-team CRITICAL F-C1 (+ HIGH F-C2, MED F-C4). Worktree C:\bari_wt_t480, branch fix/task480-cakes-accuracy off origin/master de8c7801.

## Fix round 1 (Content lane, commit 796275f7) — orchestrator-verified + Adversarial QA gate = GO-WITH-FIXES
- **Counts corrected (QA independently recomputed, all TRUE):** caveat 63→62; least_bad(grade D) 2→1; has_phvo label 20→18 (count field already 18); no_phvo 45→44. Partition 18+44=62 ✓. Grade dist C:1/D:1/E:60.
- **Antithesis:** caveat body + product 1361207 rowVerdict reworded to positive declarative, meaning preserved (QA confirmed). Em-dash 0 remaining in scoped consumer copy. Isolation: 1 file, 13/13, 0 score/grade/rank/nutrition touched, 0 dropped signals (arrays 3=3/112=112).
- **QA HIGH RT-480-1 (in-scope, must fix before ship):** residual antithesis on product cake_7290119030095 `limitingFactors[1]` = "עדיין מוצר מעובד, לא קינוח ביתי" — em-dash removed but "X,not Y" negation kept. → sent back to content author (round 2, resume) for positive-declarative rework. THEN re-verify → push → owner PR (tripwire-2 consumer deploy).

## Fix round 2 (Content lane resume, commit 6a969d0f) + FINAL VERIFY → SHIPPED PR #60
- RT-480-1 resolved: `limitingFactors[1]` "עדיין מוצר מעובד, לא קינוח ביתי" → **"מוצר תעשייתי מעובד, רחוק ממטבח ביתי"** (positive declarative, states what it IS + "far from" instead of "not"; meaning preserved).
- **Orchestrator FINAL VERIFY (delta only, QA already cleared counts/isolation/voice on 796275f7):** commit 6a969d0f, diff still 1 file 13/13; consumer-copy antithesis = **0**; TRUE em-dash in scoped consumer fields **7→0** (whole-file 187→180, the 180 = out-of-scope d4_additives = RT-480-3, my 13-line change added 0); valid JSON. Counts unchanged from QA-verified TRUE set. **Two-gate satisfied** (content author ×2 + Adversarial QA GO-WITH-FIXES, sole condition met+verified).
- **Pushed → PR #60: https://github.com/Argento17/Barint/pull/60** (owner merge = tripwire-2 consumer deploy). CLOSE on owner merge; prune worktree C:\bari_wt_t480 after.

## Routed follow-ups (out of TASK-480 scope, do NOT block)
- **RT-480-2 (MED, frontend/data):** stale CODE COMMENT `cakes-hard-cookies-comparison-page.tsx:99-101` misstates grades post-fix — says product 7290119030095 "moved C→D" + "no A/B/C exist"; it's actually grade **C** (50.5) and C exists. Non-consumer (comment only). Also surfaces a filter-semantics Q: `least_bad` predicate = `grade==="D"` but the true least-bad product is the C-grade one that outranks it — confirm intended filter scope. → new task.
- **RT-480-3 (MED, systemic — content/generator):** `d4_additives[].function_he/explanation_he` carry ~180 em-dashes + 6 antithesis, consumer-visible in the expansion panel but NOT in the 5 named copy fields. Almost certainly a TEMPLATED/generated pattern across ALL categories, not cakes-specific → do NOT fix per-category; route to a generator/template phrasing pass + a scope decision on whether d4_additives is inside the two-gate sign-off surface. → new task / backlog.
