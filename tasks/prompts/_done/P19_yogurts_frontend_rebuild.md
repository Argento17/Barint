# P19 → Frontend/Data Agent — rebuild the yogurts page data from the clean run (after P18 returns)

```
P19 / TASK-249 — Rebuild yogurts frontend data from run_yogurt_006_shipcfg2
(the authoritative clean run). Launch scope ruling: Shufersal-only.

SOURCES:
- Run: 02_products/yogurt_system/bsip2_outputs/run_yogurt_006_shipcfg2/ +
  reports/run_yogurt_006_shipcfg2_run_record.json (S=2, A=10, B=32, C=19,
  D=23, E=1 over 87)
- Page scope: the 18 products of the current v3 page minus 7290000408316
  (Yohananof-only, excluded as OFF-contaminated; returns post-P6 re-scrape) —
  i.e. every page product now maps to exactly ONE Shufersal-sourced trace.
- Dedup ruling: one card per barcode (the Greek yogurt 7290107936309 appears
  ONCE, from its Shufersal record).

DO:
1. Build yogurts_frontend_v4.json from shipcfg2 scores/grades for the page
   products, following the existing v3 file's schema exactly. _meta.provenance
   must state: run_yogurt_006_shipcfg2, Shufersal-only scope, the OFF exclusion
   (TASK-238), and the dedup ruling.
2. S-GRADE DISPLAY CHECK: verify the comparison page components + score badge
   render an S grade correctly (the live site has never shown S). Check
   bari-web/src/lib/comparisons/yogurts-* and shared score components for
   grade-S handling (styling, sort order above A, RTL layout). Report what
   exists vs what's missing — implement ONLY data-layer fixes; visual/component
   work gets reported for Design/Frontend review, not improvised (frozen pixel
   values / canonical component rules apply).
3. DO NOT wire the new file into the live route — produce it alongside v3 and
   report the one-line import change needed. Copy strings are NOT in scope
   (P14 regenerates them next; carry over NOTHING from v3 strings — leave
   string fields empty/marked PENDING_P14 so stale claims cannot leak through).

RULES: no engine/score changes; no live-route changes; no string authoring;
no Open Food Facts.

RETURN BLOCK: v4 file path + product count + grade distribution (must match
shipcfg2 exactly for the 18); S-display findings; the import change needed;
anything blocking. Propose RETURNED.
```

---
**After you paste this to the agent:** open `tasks\DISPATCH_BOARD.md` and put an `x` in the P19 line under 📬 Signals.
