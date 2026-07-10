# TASK-461 HANDOVER #2 → git-owning sibling lane (cheese_v5 copy overhaul, Phase-2 #1)

**From:** description-overhaul session (no-commit ruling). **Status: TWO-GATE SIGNED OFF — ready to
commit.** Same protocol as the shipped brined pilot (`TASK-461_handover.md`, PR #44).

## The artifact
- **`C:\Bari\tasks\returns\TASK-461_cheese_v5_copy_overhaul.json`**
  sha256 `0a490cc55d8ba78e4859da67600eca1293e165251d9a8fac7ef231938cabf4ab`
- Replaces: `bari-web/src/data/comparisons/cheese_frontend_v5.json`
- Baseline: **origin/master blob `deec2e91…`** (the de-anchored v5 from PR #34) — verified identical
  by 3 independent extractions (author sha cc10d803, orchestrator, QA).

## Verification already done
1. **Field isolation ×3 (author / orchestrator / QA, independent scripts):** 47/47 products changed on
   exactly {insightLine, rowVerdict}; scores/grades/ranks/nutrition/ingredients/_meta/page_copy
   byte-identical. Zero score movement by construction.
2. **Adversarial QA (Opus): GO_WITH_FIXES — 0 CRITICAL / 0 HIGH / 3 MEDIUM (advisory, routed, none
   block).** `TASK-461_cheese_QA_report.md` (this dir, sha 158f5cf5…). 11/11 hotspots TRUE (Tvorog
   protein max 17g + sodium min 30mg ×6.33; zaatar 558mg sodium max; 18%-label/22g-panel; sole
   E407+E466 product; 2.8g protein min; 10.4 bottom gap), 6/6 ingredient percentages, 5/5 twin
   families, "שנוי במחלוקת" 6/6 tied to genuinely engine-contested additives (E466/E407).
3. Hygiene: em 0 (was 94), engine vocab 0, openings 47/47 unique both fields, OFF 0.
4. Orchestrator read all 47 blocks (verifier read).

## ⚠️ THREE live truth-defect fixes riding in (PR-body material)
Production copy today: (1) bagel-spice 5% claims **שמן קנולה** — not in its ingredient list;
(2) olives-5% same canola fabrication; (3) 9% mehadrin cottage claims its classification lowers its
score — false (identical score to siblings). All corrected by this artifact (QA-confirmed 3/3).

## Git steps (same as pilot)
1. Verify sha256 → swap file in worktree off origin/master → `run_gates.py` G1–G8 with `--baseline` =
   origin/master copy (expect the pre-existing G1 schema fail-set byte-identical to live; TASK-453 debt)
   → tsc/build → branch `content/task461-cheese-copy-overhaul` → push origin → owner PR.
2. Tick board (TASK-461 Phase-2 #1).

## Routed follow-ups from QA (registry notes, not blockers)
- **MED-1 → TASK-453 gate backlog:** `hebrew_readability` false-FAILs on 'נובה' inside brand **תנובה**
  (4 strings). Needs word-boundary/brand allowlist before it can be a hard dairy gate. (Brand-masked
  re-run = 0/94 real leaks.)
- **MED-2 + MED-3 → adopted as TASK-461 fan-out house rules** (recorded in TASK-461.md): provenance
  adjectives must be label/parse-derived; partial-scan narration = only when material (chip already
  discloses), consistent per category.
- **Data-lane flag (author):** cheese product barcode …635116-family item #37 has EMPTY `d4_additives`
  despite corrupted "E2 02" (E202) in raw label text — parser gap, not copy. Route to data-agent.
