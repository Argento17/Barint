# P29 / TASK-257 Phase 2 — The Copy Engine (route: C1)

**➡️ OWNER: after you send this prompt, tick the P29 line in `tasks\DISPATCH_BOARD.md`.**

---

CONTEXT: Repo C:\Bari. The generator (P27) produces complete, gated page JSONs with
every copy field = "PENDING_COPY". You build the COPY ENGINE — the repeatable layer
that fills them — and run it on yogurts (the pilot: 80 products at
`03_operations/page_generator/out/` or regenerate via
`python 03_operations/page_generator/generate_page.py --config 03_operations/page_generator/configs/yogurts.json --out <out>`).
Read first: `tasks/TASK-257.md` + the failure audit
`02_products/yogurt_system/yogurt_relaunch_failure_audit_v1.md` (RC3 = weak copy is
why the last launch died) + `.claude/agents/content-agent.md` (your Pre-Return
Self-Check is law).

THE ENGINE IS THREE PARTS (so any category can re-run it — this is a machine,
not a one-off writing job):

## PART 1 — build_copy_inputs.py (deterministic)
`03_operations/page_generator/copy/build_copy_inputs.py --config <category config> --page <generated json> --out <fact_sheets.json>`
Per product, assemble the FACT SHEET — the only material the author may use:
- score, grade, name, retailer
- real driver from the trace: binding cap + rule family if one binds; else the
  lowest dimension (explanation_drivers). CRITICAL: if binding_cap > score the cap
  did NOT bind — mark `cap_misclaim_risk: true` and name the dimension story.
- key numbers from the product's OWN expansion.nutrition (protein, sugar, fat,
  kcal, sodium) — null stays null, never invent.
- ingredients head (first 3) if present; additive count from d4_additives.
- CORPUS STATS for superlative safety: percentile of protein/sugar/kcal within
  THIS category's displayed products + min/max/median. A superlative ("הגבוה
  בקטגוריה") is only usable if the stat proves it — the fact sheet either grants
  it explicitly (`superlatives_allowed: [...]`) or it is banned for that product.
- For the 2 S products (7290112336712, 7290110565527): inject the
  Nutrition-APPROVED verbatim Hebrew from
  `02_products/yogurt_system/s_grade_explanations_v1.md` — the author may NOT
  paraphrase these.

## PART 2 — author the Hebrew copy (you, from fact sheets ONLY)
Fields per product: `insightLine` + `expansion.positiveSignals[]` +
`expansion.limitingFactors[]` (+ `comparisonContext`/`rowVerdict` ONLY if the live
canonical schema for this category carries them — check schema v2).
Page-level: hero (eyebrow+title), prologue (4 sentences), methodology lines,
category_note — 3 blocks: (a) same-label-two-ends caveat, (b) the shared S caveat
VERBATIM from s_grade_explanations_v1.md §SHARED METHODOLOGY NOTE, (c) dairy fiber
caveat. The page tells the real structural story: 80 products, S=2 at the top
(plain 2-ingredient high-protein), the fall through B/C/D as flavor/additives/
crunch are added.

EDITORIAL LAW (each violation = automatic revision):
1. STANDALONE rule — every line fully informs a reader who sees only that card.
   No "כמו ה-X", "אותו עיקרון", "הפרש של N ציונים מ-Y". (RC3 killed the last copy
   with exactly this.)
2. Grade letter in prose = badge grade. Sodium and fat are NEVER causal.
3. The named driver = the fact sheet's real driver. Products flagged
   `cap_misclaim_risk` must NOT claim a cap/processing limit.
4. Numbers: only from the product's own fact sheet. Superlatives: only if granted.
5. No framework leakage (NOVA/BSIP/cap/dimension/proxy), no banned phrases
   (Explanation Engine v2 list — incl. "חלבון נמוך" as a bare dismissal), no
   prior-run references, honest-S framing (structural finding, never "a ceiling").
6. Quality bar = the live granola/snacks/milk lines: finding-first, assertive,
   concrete. If a line reads thinner than those, rewrite before returning.

## PART 3 — merge_copy.py + self-gate
`03_operations/page_generator/copy/merge_copy.py --page <generated json> --copy <authored json> --out <final json>`
Merges authored strings into the page JSON (replacing PENDING_COPY; structure
untouched), then:
(a) runs `integrations/clients/hebrew_readability.py` on EVERY string — 100%
    `is_clean` required;
(b) runs the full gate suite (run_gates.py with corpus/run/schema/baseline) —
    all gates must PASS including G6 COPY-SAFETY;
(c) emits a 10-card random sample (seeded, reproducible) into
    `copy_sample_for_review.md` for the orchestrator's editorial read.
Non-zero exit if any check fails.

RULES: no OFF; no score/grade/data changes; never touch live page JSONs; the two
S explanations + shared caveat byte-verbatim; stdlib only for the scripts.

ACCEPTANCE: final yogurts JSON exists with ZERO "PENDING_COPY" remaining; gates
G1–G7 PASS verbatim summary; readability 100% (state N strings checked); the
10-card sample file. Expect ONE budgeted revision loop after the orchestrator's
editorial read — design your fact sheets so a revision is a re-author of named
cards, not a rebuild.

RETURN BLOCK: file paths (3 scripts + fact sheets + final JSON + sample); gate
summary verbatim; readability N/N; which superlatives were granted and used;
any fact sheet where the real driver was ambiguous. End with the JSON return
contract — counts must include `strings_authored: N/M`, `pending_remaining: 0/N`,
`readability_clean: N/N`. Propose RETURNED.
