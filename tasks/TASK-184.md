---
id: TASK-184
title: Cereals + Granola/Muesli multi-retailer re-run (Carrefour / Rami-Levi / Yohananof) — broaden corpus + validate EV-045/045b ruling
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-05
closed_at: 2026-06-05
depends_on: [TASK-183]
blocks: []
category_id: breakfast-cereals
cc_close_note: >
  Close-readiness gate PASS (orchestrator-verified 2026-06-05). Multi-retailer run delivered
  (Carrefour + Yochananof reachable; Rami-Levy blocked, owner dropped). EV-045/045b held on unseen
  data; EV-045c added (savory Fitness crackers, flag-AND-drop for live). Data + Nutrition sign-offs
  filed (DATA_SIGNOFF.md / NUTRITION_SIGNOFF.md); owner gave GATE-3 approval. 33 new products promoted
  live after Content authoring — cereals 31->46, granola/muesli 35->53; merge add-only, no score drift
  on the existing 66, GATE-2 holds, next build PASS. Held: the 81.2/A confidence-artifact (->TASK-188)
  and 7613032045753 (sodium=1272 OFF artifact, re-verify). Engine byte-identical throughout.
summary: >
  Initiate a fresh BSIP0->BSIP2 run for BOTH breakfast-cereals and granola/muesli across additional retailers (Carrefour / Rami-Levi / Yohananof) to (a) broaden the corpus beyond the single Shufersal source and (b) validate the new corpus-purity ruling (EV-045/045b: ptitim/pasta/flour/bread/chocolate/drink exclusions + energy floor) on fresh, unseen data. Apply origination upgrades from TASK-183. First-batch owner-consult gate applies before any live promotion.
---

# TASK-184 — Cereals + Granola/Muesli multi-retailer re-run — broaden corpus + validate EV-045/045b ruling

## Why
Both categories currently rest on a **single Shufersal source** (run_cereals_005). A fresh multi-retailer
run (a) broadens the corpus and surfaces brands Shufersal doesn't carry, and (b) is the real test of the
new corpus-purity ruling (EV-045/045b) on **unseen** data — the strongest validation that the
contaminant exclusions generalize rather than overfit the Shufersal shelf.

## Scope
1. Acquire **breakfast-cereals AND granola/muesli** from additional retailers — **Carrefour, Rami-Levi,
   Yohananof** (use the Shufersal scrape path as the template; verify each retailer's access first —
   some block scraping; Playwright fallback if needed).
2. Apply the **origination upgrades from TASK-183** (category-code anchoring, contaminant/energy
   pre-scan) at BSIP0.
3. Run the full BSIP0→BSIP1→BSIP2 chain with the **EV-045/045b filters active**; report the contaminant
   exclusion tally per retailer (did the ruling catch ptitim/pasta/flour/bread/chocolate/drink on new
   data? any false positives like the שמרים⊂משמרים trap?).
4. Merge/dedup against the existing 66-product corpus; re-split into cereals + granola/muesli.
5. Produce the run summary + leaderboard top-5 per category for owner review.

## Definition of Done
- New multi-retailer corpus scored, contaminants excluded with reasons, dedup vs. Shufersal done.
- A validation note: EV-045/045b precision/recall on fresh data, plus any new contaminant class found.
- **First-batch owner-consult gate (`corpus_purity_gates_v1.md` GATE 3) applies** — no live promotion
  until owner sign-off. Proposes RETURNED with the summary; CC records CLOSED.

## Hard rules
- Do NOT change published scores / engine — engine stays byte-identical; this is acquisition + curation.
- If a retailer is inaccessible, document it and proceed with those reachable (don't block the whole run).

**Assigned:** data-agent. **Depends on:** TASK-183 (origination upgrades). **Related:** TASK-140, TASK-185.

---

## Return block (proposes RETURNED — 2026-06-05, data-agent)

**Run:** `run_cereals_multiretailer_001` (engine byte-identical to run_005; `BARI_RECAL_P0=on`).
**GATE 3 (first-batch owner consult) APPLIES — NOT promoted to live.** Produced for owner review only.

**Reachability (probed live):** Carrefour REACHABLE (self-hosted `prices.carrefour.co.il`, 11,418 SKUs);
Yochananof REACHABLE (via `laibcatalog.co.il`, chain 7290455000004); **Rami-Levy BLOCKED** (all price
portals ConnectionError/DNS-dead; storefront a login-gated SPA, no public catalog API) — documented, not
fabricated. Acquisition = transparency-feed identity + OFF candidate panels (no scraping, EDPG candidate).

**Counts:** 311 cereal candidates → 60 curated IN → 251 excluded; **42 new** after dedup vs the 66-product
Shufersal baseline (16 cross-retailer EAN duplicates + 2 Carrefour∩Yochananof). 40/42 scored:
1 A · 14 B · 17 C · 7 D · 1 E, median 60.2.

**EV-045/045b validation — HELD on unseen data.** Precision: every contaminant exclusion correct
(bars 50, breads/drinks/crackers/desserts/capsules 39, chocolate confections 5, drink 1, energy-floor 5);
no false drop of a real cereal. Recall: ONE NEW contaminant class found — **Nestlé "Fitness" savory
crackers** slip via the `fitness/פיטנס` brand token (caught downstream as router misroutes, not by
curation). Concrete ready extension proposed (EV-045c: fat≥13g/100g + savory-descriptor guard,
flag-not-drop) — NOT implemented (curation, not scoring). Yeast-trap (שמרים≠משמרים) not re-exercised
(thin OFF ingredient coverage) — flag for next storefront run.

**Structural note:** category-code anchoring (TASK-183 #2) is NOT available on the price-feed path — the
transparency XML has no category code; the EV-045b pre-scan is the only door-gate there.

**Artifacts:**
- Run record + validation note: `03_operations/bsip1/run_cereals_multiretailer_001/RUN_RECORD_and_EV045_validation.md`
- Run summary + leaderboards: `02_products/breakfast_cereals/reports/run_cereals_multiretailer_001_run_summary.json`
- Curation reports: `03_operations/bsip1/run_cereals_{carrefour,yohananof}_001/curation_report.json`
- Dedup report: `03_operations/bsip1/run_cereals_multiretailer_001/dedup_report.json`
- BSIP2 traces: `02_products/breakfast_cereals/bsip2_outputs/run_cereals_multiretailer_001/`

**Escalations:** FYI to Nutrition Agent — 81.2/A "גרנולה בתוספת חלבון" (Carrefour) is a new category-high
above the run_005 ceiling (79.9/B), earned on real macros by the unchanged engine (Hard Rule 7 surfaced,
not a halt). FYI to Product — Rami-Levy needs a Playwright/publishedprices-login path to be reachable.

**Proposes:** RETURNED. CC records CLOSED after the close-readiness gate + owner GATE-3 sign-off.

---

## OWNER DIRECTIVE (2026-06-05)
- **GATE-3 promotion of the 42 new products: APPROVED**, conditional on a **clear sign-off from BOTH
  the Data Agent and the Nutrition Agent** on the new products before they go live.
- **EV-045c ADOPTED** (Nestlé "Fitness" savory-cracker gap: fat≥13g/100g + savory-descriptor guard,
  flag-not-drop). Data Agent to implement.
- **Rami-Levy path: DROPPED** (do not pursue Playwright/login).
- Promotion (frontend merge + Content authoring of insightLine/rowVerdict for the new products) proceeds
  only after both sign-offs are in. Task stays RETURNED until then.

## SIGN-OFFS IN (2026-06-05)
- **Data sign-off** (`run_cereals_multiretailer_001/DATA_SIGNOFF.md`): **GO, 35 of 42**. Held 7 (6 EV-045c
  savory "Fitness" crackers + 1 insufficient-data). EV-045c implemented flag-not-drop; did NOT change the
  42-set. Provenance real (EDPG candidate), dedup correct, engine byte-identical.
- **Nutrition sign-off** (`run_cereals_multiretailer_001/NUTRITION_SIGNOFF.md`): **CONDITIONAL GO.** Grade
  distribution defensible. THREE conditions: (1) **81.2/A "גרנולה בתוספת חלבון" NOT defensible** — the A is
  a data-completeness artifact (ingredient_count=0; cleared the A boundary only because OFF had a sodium
  cell, giving confidence=60/medium-band → escaped the 75-cap its two identical siblings got at
  confidence=55/low-band). Withhold the A. Confidence-architecture exposure → flagged to Product (D7).
  (2) **EV-045c must be flag-AND-DROP for live**, not flag-not-drop (a bare "Fitness" 70.3/B @17g fat is a
  cracker still scored). (3) Drop the savory Fitness B-band items; HOLD "Fitness Thin" pending ingredients.
- **Reconciled promotable set: ~34** (Data's 35 minus the held 81.2/A). EV-045c → drop-for-live.

## PROMOTED TO LIVE (2026-06-05) — TASK COMPLETE
Both sign-offs in + owner GATE-3 approval → **33 new products promoted** (Content authored all 34 verdicts;
1 held at merge). Merge add-only, validated (no score drift on the existing 66, no id collisions, GATE-2
#1 holds, all rows have authored copy). `next build` PASS.
- **דגני בוקר: 31 → 46** (B17/C21/D8; top שיבולת שועל עבה 80/B; no A)
- **גרנולה ומוזלי: 35 → 53** (B12/C25/D15/E1; top גרנולה ממותקת בסילאן 76/B; no A)
- Scripts: `bsip2/proto_v0/src/merge_multiretailer_promote.py`; staging `run_cereals_multiretailer_001/promote_staging.json`.

**Follow-ups (not blocking close):**
- TASK-188 (Product) — confidence-rule for the held 81.2/A artifact.
- **Held for data re-verify:** `7613032045753` "Nestle Fitness Chocolate & Rice" — OFF sodium=1272 mg/100g implausible; score built on it; re-verify panel before re-adding.
- **Cosmetic:** a few OFF-sourced product names are English ("Protein granola") on the Hebrew pages — Hebraize in a later pass (Content/Data).
