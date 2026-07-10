# TASK-461 HANDOVER #10 → git-owning sibling lane (granola copy overhaul, Phase-2 #9)

**From:** description-overhaul session (no-commit ruling). **Status: TWO-GATE SIGNED OFF — ready to
commit.** Same protocol as the previous nine.

## The artifact
- **`C:\Bari\tasks\returns\TASK-461_granola_copy_overhaul.json`**
  sha256 `1d2fa0c66ecd7ac84d404e90aa2e59fcce8ec18a89c4ddb5fe0aa8ea859f61c5`
- Replaces: `bari-web/src/data/comparisons/granola_frontend_v2.json`
- Baseline: **origin/master blob `60539d49…`** (22 products).

## Verification already done
1. Field isolation ×3 + post-fix re-proof: 22/22 only {insightLine, rowVerdict}; _meta (incl.
   `off_used:false`) /scores/grades/ranks/expansion byte-identical.
2. **Adversarial QA (Opus): GO_WITH_FIXES (0C/0H/3M) → M2 attribution fix applied (single leaf) →
   micro-recheck GO.** Final report `TASK-461_granola_QA_report.md` (this dir). 44/44 truth claims,
   8/8 sweetener-source counts vs parse, fitness twins literally equal (41.0), TASK-189 sodium guard
   PASS (fact stated, no score-punishment implication), image-vs-label exposures ruled sharp-not-snide.
3. **FIVE live truth defects fixed (PR-body material):** a verdict calling a D product "ציון E";
   two sweetener-source undercounts; a sole-lowest claim over a 0.6pt (noise) gap; an "all fruits
   candied" overstatement trimmed to the four that are.
4. Hygiene: em dashes 52→0, engine vocab 0, openings 44/44 unique, readability 43/44 (1 decimal
   false-positive), panel-number products 2/22 justified. Grade-group letters ×2 kept deliberately
   (pilot-register-consistent framing, orchestrator ruling documented).

## Git steps
1. Verify sha256 → swap file in worktree off origin/master → run_gates G1–G8 (`--baseline`
   origin/master) → tsc/build → branch `content/task461-granola-copy-overhaul` → push origin →
   owner PR. Copy the QA report to `02_products/granola/reports/red_team_granola_<date>.md`.
2. Tick board (TASK-461 Phase-2 #9).

## 🔴 Routed follow-ups — one LOUD
- **→ data-agent (INTEGRITY, loud):** product barcode-class #19 (גרנולה עשירה family): **three-way
  inconsistency** — `_meta` claims the TASK-385 D→E refresh (38.0→33.0) was applied, the score fields
  still carry 38.0/D, and the expansion prose says "E" twice. Someone shipped a partial refresh. The
  new copy survives under BOTH values (QA-verified), but the underlying record needs adjudication
  (which value is truth?) — likely wants a TASK of its own.
- **→ data-agent:** #3 "תמר" in product name with no date in parse; #5 positiveSignals "ללא סוכר
  מוסף" vs סילאן in parse (copy phrased around it); OCR corruption ×4.
- **→ expansion-pass accumulator (5 entries now):** granola #19 stale "E" prose + choctab רק-C +
  bread r16/r20 + juices tails.
