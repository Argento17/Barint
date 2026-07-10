# TASK-461 HANDOVER #6 → git-owning sibling lane (hummus copy overhaul, Phase-2 #4)

**From:** description-overhaul session (no-commit ruling). **Status: TWO-GATE SIGNED OFF — ready to
commit.** Same protocol as the previous five.

## The artifact
- **`C:\Bari\tasks\returns\TASK-461_hummus_copy_overhaul.json`**
  sha256 `50f4be85e91848c3c3224e65842adf6068ecffc04e393541b8220194325a24b6`
- Replaces: `bari-web/src/data/comparisons/hummus_frontend_v5.json`
- Baseline: **origin/master blob `2fbd70fd…`** (57 products).

## ⚠️ Structural fact (verified ×2, author + QA independently)
Only **35/57 products carry a `rowVerdict` key in production** (22 matbucha/eggplant/pepper rows never
had one). The artifact re-authors the real copy surface — **92 strings (57 insightLine + 35 rowVerdict)**
— and adds/removes ZERO keys (key-set byte-match). Don't be surprised by the 22 keyless rows; whether
those rows *should* get verdicts is a separate frontend/content question, not this change.

## Verification already done
1. Field isolation 57/57; scores/grades/ranks/nutrition/_meta/d4 byte-identical.
2. **Adversarial QA (Opus): GO_WITH_FIXES — 0 CRITICAL / 0 HIGH / 3 MEDIUM advisory (none blocks,
   none needs copy rework).** Report `TASK-461_hummus_QA_report.md` (this dir, sha a762377d…). All
   hotspots re-derived TRUE: 852-sodium trio exact (twins full-panel identical), צ'ומה genuinely
   saltiest at 864, "יותר מכפול מהמקובל" = 2.16× median, quadruplet spread 0.2 ruled as tie,
   brand-adversarial claims (צנובר 1.8%, זעתר 0.17%, 40%-label vs 37%-list, סמיר 48%-inside-'סלט
   חומוס') bulletproof. Owner boundary rule intact ("סלט" only in quoted label names; prepared-vs-raw
   never via protein).
3. **HUM-001 trap fully avoided (live truth defect fixed):** production copy on the last-place product
   cites fat grams ("20 גרם שומן / 81% מהקלוריות") built on values the pipeline itself suppressed as
   corrupted (`_meta fat_values_dropped: 57`). New copy cites שומן **zero times** in 92 strings.
4. Hygiene: em dashes 97→0, engine vocab 0, antithesis→0, openings 57/57 + 35/35 unique, 5-gram ≤2×,
   leakage gate effectively 92/92 (2 false positives on a real "15.5" tahini %).

## Git steps
1. Verify sha256 → swap file in worktree off origin/master → run_gates G1–G8 (`--baseline`
   origin/master; expect the familiar pre-existing G1 debt) → tsc/build → branch
   `content/task461-hummus-copy-overhaul` → push origin → owner PR. Copy the QA report to
   `02_products/hummus/reports/red_team_hummus_<date>.md` in the commit.
2. Tick board (TASK-461 Phase-2 #4).

## Routed follow-ups (NOT blockers)
- **→ data-agent:** צ'ומה `d4_additives` EMPTY despite additives in its parsed list (latent extraction
  gap; copy doesn't lean on it); d4 under-extraction also #7/#10; implausible 18.2g protein on partial
  #2; stale `_meta.confidence_distribution` (baseline-inherited).
- **→ frontend/content backlog:** the 22 rowVerdict-less rows — decide whether the matbucha/eggplant
  group should get verdicts (new copy surface, would need its own two-gate cycle).
- **Process note:** a stray `inspect.py` had been left in the shared session scratchpad by an earlier
  lane and shadows the Python stdlib — neutralized (renamed `.bak`) by the orchestrator.
