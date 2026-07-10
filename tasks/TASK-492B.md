---
id: TASK-492B
title: Creatine / functional-dairy signal — framework ruling + blog
owner: nutrition-agent
status: BLOCKED
priority: MEDIUM
created_at: 2026-07-03
blocker: "PARKED on owner stop 2026-07-04 (supplements re-direction, TASK-504). Blog gate-1 authored+committed 68381ebb (worktree C:\\bari_wt_t492b, branch content/task492b-dairy-blog, NOT pushed); gate-2 red-team killed mid-run on the stop. Substance (dose-honesty, dairy) likely survives the pivot but the piece links /hashvaot/creatine — re-frame-check + full re-gate after the TASK-504 plan lands."
depends_on: [TASK-504]
blocks: []
category_id: null
summary: >
  Tnuva GO creatine-in-dairy signal. Nutrition rules on functional-dose bucket (not nutrient, not additive; recommend editorial-only annotation lane, never a score move). Then high-protein-dairy shelf scrape supplies the evidence table. Blog: when food becomes a supplement + dose-honesty. Two-gate before publish.
---

# TASK-492B — Creatine / functional-dairy signal — framework ruling + blog

## Chain
1. **✅ Nutrition framework ruling — DONE** (`01_framework/nutrition/functional_dose_ingredient_ruling_v1.md`, orchestrator-verified 2026-07-03): functional-dose = new annotation-only lane, borrows SIE Dose-Adequacy §2.2 read-only; 0 score moves / 0 EV / 0 engine files; all 5 tripwires clear. §3.1 = scrape field list, §3.2 = dose bands.
2. **✅ Shelf scrape RETURNED (Shufersal live, 53 products, 0 fetch failures) — ⚠️ PREMISE-BREAK.** Headline: of 44 functional dairy drinks, **2 advertise creatine on-label, 0 disclose a computable daily dose** (both "amount not disclosed" per §3.2, no hedge). **The trigger premise does not hold on the live shelf: Tnuva GO is a COLLAGEN drink, not creatine** (orchestrator spot-confirmed קולגן on Tnuva GO barcode 7290116935607). The 2 real creatine-declaring SKUs are **Yoplait GO** (different brand; surfaced via Shufersal fuzzy keyword match). Excluded: 4 standalone creatine-monohydrate powder tubs + 5 non-drink protein snacks. Victory still 403; Yochananof storefront now 200 but search path differs. Report: `03_operations/reports/research/functional_dairy_shelf_scrape_v1.md`. **Owner input requested** (did he see creatine specifically in Tnuva GO — new/regional SKU? — or was it collagen). Blog REFRAME recommended: functional additives (collagen Tnuva GO / creatine Yoplait GO) are arriving in Israeli dairy AND none disclose a verifiable dose → the dose-honesty story is 0/2, sharper + more honest than the original premise.
3. **⏳ Blog authoring** — Content Agent, through mandatory two-gate (Content + Adversarial QA). Needs the scrape table. NOT started.
