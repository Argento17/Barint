P24 / TASK-256 — Yogurts launch integration → PREVIEW (Frontend + QA).
**DO NOT deploy to production.** The owner reviews the rendered page first and may
have comments; publishing is a separate, explicit step after that.

SOURCE (gate-passed + orchestrator-verified copy):
`02_products/yogurt_system/yogurts_copy_regen_draft_v1.json` (17 products + page_strings;
both S explanations are Nutrition-approved verbatim — do NOT reword anything).
TARGET DATA: `bari-web/src/data/comparisons/yogurts_frontend_v4.json` (all string
fields currently PENDING_P14).

DO (Frontend):
1. PER-PRODUCT COPY (17, matched by barcode) — write from draft into v4 JSON:
   - `insightLine` → product.insightLine
   - `expansion.confidenceLabel` / `positiveSignals[]` / `limitingFactors[]` → product.expansion.*
   - `confidence_label_he` / `confidence_tooltip_he` / `confidence_sub_reason` → top-level
   Replace EVERY PENDING_P14. Change ONLY these string fields — no score, grade,
   nutrition, ingredient, or any other field changes.
2. PAGE-LEVEL STRINGS — write the draft's `page_strings` (hero_*, prologue_*,
   methodology_*, category_note) into `bari-web/src/lib/comparisons/yogurts-comparison-page-data.ts`,
   REPLACING the old page copy. CRITICAL: the old copy says "no product reaches S /
   'הכי טוב' הוא A" — every trace of that must be gone. category_note must carry the
   shared S caveat verbatim.
3. S EXPLANATIONS — the 2 S products (7290112336712, 7290110565527) carry an
   `s_grade_explanation` paragraph. Render it on those cards within the CANONICAL
   expansion surface (no new color encoding; canonical component + frozen pixels per
   `bari_score_presentation_v1` / `bari_canonical_reference_v1`). If placement needs a
   Design call, render it in the most consistent existing slot and FLAG for owner/Design
   — do NOT block the preview.
4. FLIP THE TWO IMPORTS v3→v4:
   - `bari-web/src/lib/comparisons/yogurts-comparison-page-data.ts:3`
   - `bari-web/src/lib/comparisons/yogurts-shelf-filters.ts:1`
   (Leave `yogurt-article-content.ts:8` — it's a doc comment, not an import; blog is separate.)
5. Clear `.next`, then `tsc --noEmit` + `next build`. Confirm clean (this branch had stale
   .next validator types referencing deleted maadanim/preview pages — the clear fixes that).

DO (QA):
6. On a local/preview render verify: 17 products show the new copy; the 2 S products show
   the S badge + the S explanation; grade distribution unchanged (S=2,A=2,B=7,C=4,D=2);
   prologue + category_note reflect S=2 (NO "no-S" language anywhere on the page); RTL
   correct; no console errors.
7. Provide the preview method (npm run dev URL or preview deploy) + screenshots of: the
   top of the shelf (2 S + 2 A), one C/D card, and the category_note block.

RULES: integrate only — **NO production deploy**; no score/grade/data changes; no new
color encoding; no OFF; reversible (one branch/commit).

RETURN BLOCK: files changed; confirm 17 PENDING_P14 all replaced by barcode + 2 imports
flipped + old "no-S" page copy fully gone; S-explanation render location (+ any Design
flag); `.next` cleared + tsc/build clean; preview URL + screenshots; anything blocking.
Propose RETURNED.

---
After you send this to the agent: open tasks\DISPATCH_BOARD.md and put an `x` in the
P24 line under 📬 Signals.
