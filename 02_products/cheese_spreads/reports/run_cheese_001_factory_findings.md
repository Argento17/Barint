# Cottage / White Cheese — Factory Run Findings (run_cheese_001)

**Task:** TASK-142 (Data Agent) · **Date:** 2026-06-01 · **Engine:** proto_v0 / 0.4.0 (UNMODIFIED)
**Governance:** `cheese_spreads_stress_test_001.md` (TASK-141, verdict **B**, PO-ratified 2026-06-01)
**Dairy calibration inherited:** TASK-139A (A-ceiling ruling), 139B (FERMENTATION_TERMS), 139D/EV-023 (A≥80)
**Verdict:** **RETURNED-candidate** — full cycle executed; blocked on an out-of-scope router gap. Frontend package **NON-AUTHORITATIVE**.

---

## 1. What was executed (bari-category-factory, all 7 stages)

| Stage | Result | Artifact |
|---|---|---|
| 1 Shelf mapping | pass | `factory_run_001/shelf_map.json` |
| 2 Corpus filter | pass | `factory_run_001/corpus_filter.json` |
| 3 BSIP0 gate | **pass** | `factory_run_001/bsip0_gate_result.json` |
| 4 BSIP1 enrichment | pass | `bsip1/run_cheese_001/output/` + `curation_report.json` + `cheese_constructs_report.json` |
| 5 QA gate | **HARD FAIL** | `factory_run_001/qa_gate_result.json` |
| 6 BSIP2 readiness | conditional | `factory_run_001/bsip2_readiness_checklist.json` |
| 7 Frontend packaging | pass (non-authoritative) | `factory_run_001/frontend_package.json` |

Pipeline scripts: `03_operations/bsip0/scrape/shufersal_cheese/{01_scrape,02_build_bsip1,03_package_frontend}_cheese.py`;
scorer `03_operations/bsip2/proto_v0/src/batch_run_cheese_001.py`.

## 2. Corpus

- **116** real Shufersal products scraped (0 fetch failures) → **57 displayable** after corpus-purity curation (59 excluded).
- Displayable coverage: **nutrition 100%, ingredients 91.2%, Hebrew 100%, images 100%**, gtin13 57.9% strict (rest valid retailer SKUs).
- Excluded (corpus purity): cooking cheese 24 (ricotta/mascarpone/cooking cream, Sec 2.2), plant-based spreads 9 (tofu/soy/almond/coconut — out of scope for dairy v1), no-nutrition 7, butter/butter-spread 6, prepared meals/sauces 5, non-cheese "white" items 3 (white beans שעועית לבנה, fish roe איקרה לבנה), napoleon **cake** 2, gruyère 1, other 2.
- **No overlap** with yogurt_system / maadanim: yogurt/kefir/drinkables and sweetened dessert-cheese (→ maadanim) excluded; brined/yellow/processed-slice excluded.

## 3. Sub-pool structure (Constitution Sec 2.9 four-pool standing precedent) — APPLIED + DOCUMENTED

| Pool | n | Routing | Grades (correctly routed) |
|---|---|---|---|
| Cottage (קוטג') | 11 | ✅ dairy_protein | all B, median 70.4 |
| White cheese / quark (גבינה לבנה / קוורק) | 17 | ✅ dairy_protein | B 10 / C 6 / A 1, median 70.9 |
| Labaneh (לבנה) | 3 | ✅ dairy_protein | B 2 / C 1, median 72.0 |
| Cream cheese / spread (גבינת שמנת / ממרח גבינה) | 26 | ❌ **misroute** | NOT RELIABLE (misrouted) |
| Developmental (Sec 2.8, D3≤20g) | 0 | — | none in corpus |

Fat tiers (3/5/9%) treated as **variants**, not pools. Labaneh small (3) is truthful — most "לבנה" SKUs are "גבינה לבנה" (white cheese), correctly pooled to white_cheese_quark (the labaneh/white disambiguation was a real bug fixed during the build).

## 4. Governance constructs — all applied, label-observable, no new scoring rule

- **Light / reduced-fat (Sec 5.2.1, relative ≥25% vs same-sub-pool reference):** 1 light claim (Philadelphia Light 13%), **0 Marketing Divergence Findings**. A bare fat-% tier (5%/3%) is correctly NOT treated as a light claim (Sec 4.3 — 5% white cheese is the default, not "light" vs itself).
- **Fermentation (EV-015 + 139B FERMENTATION_TERMS, flavor-vs-marker guard):** 3/57 credited, **0 flavor-vs-marker violations**. Credit reads ingredient text only.
- **A-ceiling (EV-021 / RULING-DAIRY-A-01, C1–C6; A≥80):** **0 A-eligible pre-routing.** The single raw-macro grade-A — **גבינה טבורוג 5% (81.0)** — fails C1 (added sugar), C2 (engineered additives), C3 (no culture credit), C4 → **WITHHELD**. The ruling caught a macro-only A exactly as designed.
- **Endemic distortion (Sec 6.4):** both Product-Owner-approved disclosure texts wired in **clean RTL Hebrew** — category-wide sodium/sat-fat (DISTORTION-010, all pools) + pool-specific light reformulation (DISTORTION-006/009, cream + light only; not shown on plain cottage/labaneh).

## 5. The blocker — QA-CHS-001 (misroute 47.4%)

**ALL 26 cream-cheese/spread products misroute** (→ default 16, whole_food_fat 8, bread 1, snack_bar 1) + 1 white-pool 32% goat. **Cottage (11), white-cheese/quark (16), labaneh (3) route correctly** to `dairy_protein`.

**Root cause:** `router_v2.py` has a hard anchor for cottage (`קוטג'→dairy_protein`) and Stage-2 dairy signals carry plain white cheese / labaneh, but there is **no anchor for the cream-cheese/spread pool**. "גבינת שמנת" (high fat, low protein, often flavored) lacks dairy signal strength → `default`/`whole_food_fat`. Same class as run_cereals_002 (QA-CER-001) and run_yogurt_003.

**Remediation (scoped follow-up, NOT done here — engine change, out of scope per CLAUDE.md + cereals precedent):** add cream-cheese/spread hard anchors (`גבינת שמנת` / `ממרח גבינה` / `פילדלפיה` / `נפוליאון` → dairy_protein) carrying a dairy category prior from the BSIP0 cheese-shelf query, with regression-lock (mirrors TASK-139C). **Re-run as run_cheese_002.** The 3 BSIP2-insufficient SKUs are the same root cause (cream cheese → default → cannot score).

## 6. DoD scorecard

| DoD criterion | Status |
|---|---|
| coverage ≥90% | ✅ MET (nutrition 100%, ingredients 91.2%) |
| INSUFFICIENT 0% displayable | ❌ 5.3% (3 cream-cheese misroutes-to-default; same root cause as misroute) |
| misroute <5% | ❌ 47.4% (router cream-cheese-anchor gap — out of scope) |
| sub-pool structure applied + documented | ✅ MET |
| QA green | ❌ QA-CHS-001 hard fail |
| frontend_package.json ready | ✅ MET as NON-AUTHORITATIVE (29/57 display-approved) |

## 7. Recommendation

Propose **RETURNED**. The category is **governance-ready (verdict B) and data-ready**; the cottage / white-cheese / labaneh pools (31 products) are launch-quality on the unmodified engine. Two scoped follow-ups gate live launch: **(1)** router cream-cheese anchor + regression-lock → run_cheese_002 (its own governed engine task, like TASK-139C); **(2)** Nutrition sign-off (A-ceiling withhold + correctly-routed grades). Do **not** promote run_cheese_001 to the live site.
