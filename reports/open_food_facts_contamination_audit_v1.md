# Open Food Facts (OFF) Contamination Audit — v1

**Date:** 2026-06-10 · **Trigger:** Owner hard-rule directive — OFF banned as a Bari data source.
**Mode:** READ-ONLY (no fixes applied, per instruction). **Scope:** entire `C:\Bari` repo.

# FINAL VERDICT: 🔴 PARTIALLY CONTAMINATED — BLOCK LAUNCH UNTIL REMEDIATED

**All comparison-page launches and regenerations are HALTED** pending remediation. This supersedes
the in-flight TASK-233F / snacks-confidence / dead-file work until OFF is removed.

OFF is not a marginal dependency. It is woven into the **nutrition-panel acquisition layer** for
multiple categories, so OFF-derived data reached **published scores, grades, and "verified"
confidence claims** — not only images. One category (yogurts) was scraped **entirely** from OFF.

---

## 1. Root capability — the OFF integration client

| File | Role |
|---|---|
| `integrations/clients/open_food_facts.py` | The OFF API client (`get_product`, search). The enabling dependency. |
| `integrations/README.md` | Documents OFF as an admitted external client under EDPG (TASK-170). |

The EDPG framing ("engine never reads OFF directly; OFF data is `candidate`, must clear BSIP0+QA")
was **insufficient** — the BSIP0 acquisition scripts below import this client and write
`source: open_food_facts` panels straight into the corpus that feeds scoring. The ban is stricter
than EDPG and overrides it.

**≥9 BSIP0 acquisition scripts import/use the OFF client:**
`03_operations/bsip0/scrape/` → `off_yogurt/01_scrape_off_yogurt.py` (search.openfoodfacts.org),
`multiretailer_cereals/01_acquire_multiretailer.py`, `salty_snacks_real/01_bsip0_off_panels.py`,
`carrefour_butter/01_scrape_carrefour_butter.py`, `yohananof_butter/01_scrape_yohananof_butter.py`,
`yohananof_cheese/01_acquire_yohananof_cheese.py`, `shufersal_olive_oil/_build_corpus_from_sources.py`,
`victory/01_acquire_victory.py`, plus `salty_snacks_real/fix_*trans*.py` ("corrected_at_source:
open_food_facts", `off_reprobe_task234.json`).

---

## 2. Per-category contamination table (shipped comparison pages)

Default = CONTAMINATED unless proven clean (0 OFF in frontend JSON **and** 0 OFF in source dir).
"OFF img (JSON)" = `images.openfoodfacts.org` URLs in the shipped frontend JSON (consumer-visible).
"OFF src files" = files under the category's `02_products/` source dir referencing OFF.

| Category | OFF img in JSON | OFF src files | Reached consumer? | Affects | Severity | Verdict |
|---|---|---|---|---|---|---|
| **yogurts** (`yogurts_frontend_v3`) | **6** | 48 | YES — images **+ entire corpus scraped from OFF** (`off_yogurt`: identity, names, barcodes, nutrition, images) | image + score + confidence + copy + identity | 🔴 CRITICAL | **CONTAMINATED** |
| **hard_cheeses** (`hard_cheeses_frontend_v2`) | **15** | 47 | YES — images + OFF nutrition panels (`yohananof_cheese` `nutrition_raw_source: open_food_facts`) | image + score + confidence | 🔴 CRITICAL | **CONTAMINATED** |
| **cereals** (`cereals_frontend_v2`) | **8** | 3 | YES — images + OFF panel (`multiretailer_cereals` `panel_source: open_food_facts`) | image + score + confidence | 🔴 CRITICAL | **CONTAMINATED** |
| **granola** (`granola_frontend_v1`) | **9** | 3 | YES — images + OFF panel (cereals split) | image + score + confidence | 🔴 CRITICAL | **CONTAMINATED** |
| **butter** (`butter_frontend_v2`) | 0 | 8 | Source chain — OFF nutrition panels (`carrefour_butter`/`yohananof_butter` `source: open_food_facts`); generator image cascade includes OFF tier | score + confidence (+ latent image) | 🔴 CRITICAL | **CONTAMINATED** |
| **salty_snacks** (live `v4`) | 0 | 50 | Source chain — `01_bsip0_off_panels.py` `panel_source: open_food_facts`; TASK-234 re-probed from OFF (`off_reprobe_task234.json`) | score + confidence | 🔴 CRITICAL | **CONTAMINATED** |
| **cheese** (`cheese_frontend_v3`) | 0 | 2 | Source chain — `yohananof_cheese` OFF `nutrition_raw_source` | score + confidence | 🟠 HIGH | **CONTAMINATED** |
| **juices** (`juices_frontend_v3`) | 0 | 16 | Source chain — OFF references in `02_products/juices` | score + confidence (verify per-product) | 🟠 HIGH | **CONTAMINATED** |
| olive_oil (`olive_oil_frontend_v1`) | 0 | 6 | NOT shipped (imported by 0 source files) but OFF-sourced (`shufersal_olive_oil` `nutrition_source: open_food_facts`) | n/a (dead file) | 🟡 MED | **CONTAMINATED (dead — delete)** |
| crackers_staged (`crackers_staged_v1`) | 0 | — | NOT shipped (dead file) | n/a | 🟡 MED | quarantine/delete |
| **bread** (`bread_frontend_v2`, src `bread_retail_003`) | 0 | 0 | No | — | — | ✅ **CLEAN (proven)** |
| **hummus** (`hummus_frontend_v5`) | 0 | 0 | No | — | — | ✅ **CLEAN (proven)** |
| **maadanim** (`maadanim_frontend_v3`) | 0 | 0 | No | — | — | ✅ **CLEAN (proven)** |
| **snacks** (`snacks_frontend_v2`, src `snack_bars`) | 0 | 0 | No | — | — | ✅ **CLEAN (proven)** |
| **milk** (`milk-comparison`) | 0 | 0 | No | — | — | ✅ **CLEAN (proven)** |

**Contaminated shipped categories: 8** (yogurts, hard_cheeses, cereals, granola, butter,
salty_snacks, cheese, juices) + 2 dead files (olive_oil, crackers_staged).
**Proven clean: 5** (bread, hummus, maadanim, snacks, milk).

---

## 3. Consumer-visible OFF images (CRITICAL — confirmed rendering)

These `imageUrl` values point at `images.openfoodfacts.org` and render on live pages (thumbnails
use a plain `<img>`, so `next.config` whitelisting is irrelevant — they load regardless):

| Category / file | OFF image count | Example (line) |
|---|---|---|
| hard_cheeses_frontend_v2.json | 15 | L23 `.../729/011/032/4872/front_en.5.400.jpg` |
| granola_frontend_v1.json | 9 | L58 `.../729/012/087/1069/front_en.3.400.jpg` |
| cereals_frontend_v2.json | 8 | L61 `.../761/303/768/6906/front_en.5.400.jpg` |
| yogurts_frontend_v3.json | 6 | L416 `.../729/011/056/5527/front_he.65.400.jpg` |

**38 OFF images across 4 live pages.**

---

## 4. OFF-derived nutrition → scores (deepest contamination)

OFF was used as the **nutrition panel source**, so OFF numbers drove dimension scores, final
grades, and the "verified / מבוסס על נתונים מלאים" confidence label:

| Category | Evidence (file:line / function) |
|---|---|
| yogurts | `off_yogurt/01_scrape_off_yogurt.py:30` `ENDPOINT=search.openfoodfacts.org`; `02_curate_and_bsip1.py:128` `source_retailers:["openfoodfacts"]` — full corpus from OFF |
| cereals/granola | `multiretailer_cereals/01_acquire_multiretailer.py:173` `nutrition_raw_source {source: open_food_facts}`; `:189` `panel_source: open_food_facts`; `02_build_bsip1_multiretailer.py:87` `bsip0_status: off_candidate` |
| salty_snacks | `salty_snacks_real/01_bsip0_off_panels.py:103` `panel_source: open_food_facts`; `:116` acquisition_method includes `open_food_facts_panel_by_real_ean`; TASK-234 `fix_trans_artifacts_corpus.py:95` `open_food_facts (authoritative serving-level re-probe)` |
| butter | `carrefour_butter/01_scrape_carrefour_butter.py:272/284` `source: open_food_facts` + `import ... open_food_facts`; `yohananof_butter/01_scrape_yohananof_butter.py:203/245` same |
| cheese / hard_cheeses | `yohananof_cheese/01_acquire_yohananof_cheese.py:112` `nutrition_raw_source {source: open_food_facts}` |
| olive_oil (dead) | `shufersal_olive_oil/_build_corpus_from_sources.py:140/170` `source/nutrition_source: open_food_facts` |

**Implication:** for the 8 contaminated categories, the published scores and the "verified"
confidence claims rest partly on OFF data. Remediation that removes OFF nutrition will likely
change some scores/grades — that is correct and must be reported as corrected-input deltas.

---

## 5. Historical / non-shipped OFF (context, lower urgency)

- `02_products/bread_retail_001/bsip1/*` — ~40+ records with `source_url: world.openfoodfacts.org`.
  This is the **superseded** OFF-based bread run. The **shipped** bread is `bread_retail_003`
  (frozen invariant), which is **proven clean** (§2). Keep 001 out of any rebuild; recommend archiving.
- `03_operations/bsip1/*` (204 hits), `bsip0/*` (63) — pipeline scaffolding + the OFF-based runs above.
- Docs/memory referencing OFF (EDPG, agent files, `external_integration_layer_task170`): these are
  policy/inventory references, not data contamination, but the EDPG client admission must be revoked.

---

## 6. Clean confirmation (no OFF in source chain)

bread (`bread_retail_003`), hummus, maadanim, snacks (`snack_bars`), milk: **0** OFF in frontend
JSON **and 0** OFF references in their `02_products` source dirs. These pass the launch gate's OFF
conditions. (Other launch blockers may still apply — e.g. the snacks confidence bug from the prior
verification — but they are OFF-clean.)

---

## 7. bari-web frontend code

**0 OFF references in `bari-web/src` TypeScript/TSX.** Contamination is in **data + Python
pipeline only**, not frontend logic. `next.config` does not whitelist `openfoodfacts` as an image
host (the OFF images render via plain `<img>` thumbnails).

---

## 8. Required remediation (NOT executed — awaiting instruction)

Per the directive's action list. Each contaminated category is blocked until all are true:
0 OFF in source chain · 0 OFF-derived frontend fields · 0 OFF images · 0 OFF fallback · provenance
= retailer/manufacturer/manual-verified only.

1. **Disable/remove the OFF client** (`integrations/clients/open_food_facts.py`) and revoke its
   EDPG admission in `integrations/README.md`.
2. **Remove OFF from the ≥9 BSIP0 scrapers** (§1) — no OFF import, no OFF panel/image/source writes.
3. **OFF images → NULL** in the 4 shipped JSONs (cereals, granola, hard_cheeses, yogurts). Do **not**
   substitute another guessed URL; NULL/unknown until a retailer/manufacturer/manual image exists.
4. **OFF nutrition → NULL + re-score** for the 8 contaminated categories. Where no
   retailer/manufacturer/manual panel exists, the nutrient is NULL and the product visibly
   incomplete (confidence → partial/insufficient). Report all score/grade deltas.
5. **yogurts** likely cannot stand on a non-OFF source at all (entire corpus was OFF) — flag for
   owner decision: re-acquire from retailer scrape, or pull the category.
6. **Delete the dead OFF files** `olive_oil_frontend_v1.json`, `crackers_staged_v1.json` (and
   archive `bread_retail_001`).
7. **Re-run the QA launch gate** per category: confirm the 5 OFF conditions before any go-live.

---

## 9. Launch-gate status (this audit)

| Category | OFF launch gate |
|---|---|
| bread, hummus, maadanim, snacks, milk | ✅ PASS (OFF-clean) |
| cereals, granola, hard_cheeses, yogurts, butter, salty_snacks, cheese, juices | 🔴 FAIL — BLOCK |
| olive_oil, crackers_staged (dead) | 🔴 FAIL — delete |

**Overall: PARTIALLY CONTAMINATED — BLOCK LAUNCH UNTIL REMEDIATED.**
