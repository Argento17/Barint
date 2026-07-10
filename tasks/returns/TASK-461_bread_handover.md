# TASK-461 HANDOVER #7 → git-owning sibling lane (bread copy overhaul, Phase-2 #7)

**From:** description-overhaul session (no-commit ruling). **Status: TWO-GATE SIGNED OFF — ready to
commit.** Same protocol as the previous six.

## The artifact
- **`C:\Bari\tasks\returns\TASK-461_bread_copy_overhaul.json`**
  sha256 `67cddb3c81b0b6f7e80d3c40ff06049e6b8fda23b55fb2401d0dbbd2cd07a56c`
- Replaces: `bari-web/src/data/comparisons/bread_frontend_v4.json`
- Baseline: **origin/master blob `b2fb0fd4…`** (23 products, post-crackers-split v4).

## Verification already done
1. Field isolation ×3: 23/23 only {insightLine, rowVerdict}; scores/grades/ranks/_meta byte-identical.
2. **Adversarial QA (Opus): GO_WITH_FIXES — 0 CRITICAL / 0 HIGH / 3 MEDIUM advisory (optional
   content polish, none blocks).** Report `TASK-461_bread_QA_report.md` (this dir, sha 4c1a7f4c…).
   46/46 claims TRUE; 13/13 composition percentages vs parse; **emulsifier-controversy phrasing 4/4
   engine-backed** (each = E471, tiered `contested` in that product's d4_additives); sodium triangle
   (126-min / 500-max / 434-2nd) consistent; tie discipline on the 83.0-knot and 69.0-trio.
3. **Category diseases killed:** worst-in-corpus opening-template stamping (43.5% shared → 46/46
   unique) AND a "ציון X." grade-recitation stamped on 23/23 production verdicts → 0.
4. **Live truth-defect fix riding in (PR-body material):** production copy claims a loaf is
   white-flour-dominant (40%) while its own parsed label says whole rye = 80% of flours (first
   ingredient). Candidate matches the parse; QA verified the reversal as bulletproof. The same stale
   claim in `expansion.comparisonContext` is pre-existing, out of two-field scope, untouched (verified
   byte-identical) → future expansion pass (same class as the choc-tablets "רק C" defect).
5. Hygiene: em dashes 47→0, engine vocab 0, hebrew_readability 45/46 (1 known decimal false-positive
   on the shelf-max 27.5g protein), openings 46/46, 5-gram ≤2×.

## Git steps
1. Verify sha256 → swap file in worktree off origin/master → run_gates G1–G8 (`--baseline`
   origin/master; expect familiar pre-existing G1 debt) → tsc/build → branch
   `content/task461-bread-copy-overhaul` → push origin → owner PR. Copy the QA report to
   `02_products/bread/reports/red_team_bread_<date>.md` in the commit.
2. Tick board (TASK-461 Phase-2 #7).

## Routed follow-ups (NOT blockers)
- **→ data-agent:** uniform fat=0.25 across 16/23 products (implausible, esp. the tahini bread; copy
  cites fat 0×); r11 d4 preservative under-extraction (label typos); r23 retail-disclaimer text inside
  the ingredients field; minor parse-corruption tokens (r1/r2/r6).
- **→ future expansion pass:** r16 + r20 stale `expansion.comparisonContext` claims (pre-existing).
- **→ TASK-453 backlog:** hebrew_readability decimal false-positive class (recurring).
