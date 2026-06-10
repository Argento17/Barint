---
id: TASK-228
title: "Salty-snacks REAL rebuild — replace fabricated-identity corpus with real storefront scrape (real barcodes + real images + verified nutrition), rescore, reship"
owner: data-agent
status: CLOSED
closed_at: 2026-06-10
close_reason: "Orchestrator-verified against artifacts: salty_snacks_frontend_v4.json = 47 products, 100% imageUrl host api.yochananof.co.il, 0 fake images.{retailer} hosts; live-sampled images return HTTP 200; sodium populated 44/47, fiber 27/47; grade dist B:12 C:21 D:5 E:9 (A:0, ceiling 77/B); tsc --noEmit exit 0. Page wired to v4; stale metadata description corrected 54→47. Real-image + data rebuild DELIVERED. CARVE-OUT: the 2 score-0/E products (engine floor artifact, esp. פיטנס קרקר דק סלק which is decent-macro) are a SCORING-ENGINE issue routed to TASK-229 (Nutrition + owner sign-off) — not part of this data-rebuild scope."
priority: HIGH
created_at: 2026-06-10
depends_on: [TASK-213, TASK-216]
blocks: []
roadmap_impact: true
work_type: category-rebuild
owner_signoff: "Owner (tbarhaim) approved the rebuild on 2026-06-10 — chose 'Rebuild category for real' over partial-image / fallback-only options. This authorizes the published-score change (tripwire #1 satisfied)."
---

# TASK-228 — Salty-snacks REAL rebuild

## Why this exists (root cause, confirmed 2026-06-10)

The live salty-snacks shelf (`salty_snacks_frontend_v3.json`, 54 products, provenance
`bsip1_manual_corpus`) was **hand-assembled with fabricated barcodes and fake image hosts.**
The image URLs are `https://images.{retailer}.co.il/{barcode}.jpg` — those domains **do not
resolve in DNS**. This is why "real product images" has failed every prior attempt.

Exhaustive source testing on 2026-06-10 (see `rescraper/` scripts under
`03_operations/bsip0/scrape/shufersal_frozen_vegetables/`):
- Open Food Facts by barcode: **1/54** have an image.
- Shufersal by barcode: **0/54** — Shufersal's catalog uses internal codes (Bamba = `66295`),
  its JSON-LD `gtin13` is the internal code, not the EAN. No EAN key to match on.
- Shufersal by name: attaches **wrong products** (Pringles → Colgate toothpaste, cracker → bread).
- Yohananof by barcode: **0/54** — corpus EANs (e.g. Bisli `7290000630006`) do not exist in
  Yohananof's catalog; real Bisli there is `7290115201741`. **The corpus barcodes are wrong.**
- Yohananof by name: only ~3 correct (Bisli Grill, Bisli Onion, Bamba); rest wrong-variant.

Conclusion: the products **cannot be reliably identified**, so no automated image source can
hit. The only correct fix is to rebuild the category from a real storefront scrape, the same
way every other live category got real images.

## Already done in this session (reuse — do NOT redo)

1. **Sodium metric SHIPPED** to the live page (separate from this rebuild, already merged in
   working tree): `SODIUM_METRIC` in `bari-web/src/components/shared/comparison-metric-column.tsx`,
   added to `salty-snacks-comparison-page.tsx` specs, `sodium_mg` populated in
   `salty-snacks-page-data.ts`, `sodium_mg` added to `BariProductMetricsVM`. Typechecks clean.
   **Keep this.** The rebuilt corpus must keep `expansion.nutrition.sodium` so the bar keeps working.
2. **Yohananof real image catalog harvested:** 952 `{name, url}` pairs at
   `rescraper/yoh_named_catalog.json` (real `api.yochananof.co.il/media/catalog/...` URLs that
   embed real barcodes). Reusable Playwright harvester: `rescraper/harvest_yohananof_named.py`.
3. Resolver experiments (name + barcode, Shufersal + Yohananof) in `rescraper/` — read them to
   avoid repeating dead ends.

## Scope

Rebuild the salty-snacks category through the real pipeline (the bari-category-factory flow):

1. **Real BSIP0 scrape** of the salty-snacks shelf from a real storefront (Yohananof is proven
   accessible via Playwright and exposes real barcode + image + product page with nutrition/
   ingredients; Shufersal static-HTTP also works per `02_scrape_shufersal_v2.py`). Capture per
   product: real EAN, real image URL, name, brand, nutrition panel, ingredients. Target the
   real salty-snacks shelf (chips, puffs, popcorn, pretzels, rice cakes, baked legume snacks,
   crackers). Aim for a comparable shelf size (~40–60 products).
2. **BSIP1 enrich** from real scraped data (not manual).
3. **BSIP2 score** using the CURRENT frozen engine (`engine-baseline-2026-06-04` family +
   the TASK-216 extrusion signal already in `score_engine.py`). Reuse
   `03_operations/bsip2/proto_v0/src/batch_run_salty_snacks_002.py` /
   `build_salty_snacks_frontend_v2.py` adapted to the new BSIP0 input. Do NOT change scoring
   logic — this is a data rebuild, not a scoring change.
4. **Frontend JSON**: produce `salty_snacks_frontend_v4.json` (real images, real barcodes,
   keep `expansion.nutrition.sodium` + `fiber` for the metric bars; keep the v3 editorial
   shape: insightLine 2-line verdict, positiveSignals, limitingFactors, bottomLine,
   comparisonContext, confidence fields). Wire `salty-snacks-page-data.ts` to v4.
5. **QA**: every shipped `imageUrl` must return HTTP 200 (verify, like other categories require).
   `next.config.ts` must allow the image host (`api.yochananof.co.il` / `res.cloudinary.com` —
   check `images.remotePatterns`). Build + typecheck clean.

## Acceptance criteria

- [ ] Real BSIP0 scrape output committed under `02_products/salty_snacks/bsip0_outputs/` (real EANs + images)
- [ ] Every product has a real image URL verified HTTP 200; no `images.{retailer}.co.il` fake hosts remain
- [ ] `next.config.ts` remotePatterns allows the image host used
- [ ] Rescored with the unchanged current engine; grade distribution reported (old v3 vs new v4)
- [ ] `salty_snacks_frontend_v4.json` shipped; page wired to it; sodium + fiber bars still populated
- [ ] Build + typecheck clean; page renders with real photos on the shelf

## Return block

Report: shelf size scraped, image-verification pass rate (N/N return 200), grade distribution
old→new, any products that dropped/changed vs v3, the image host added to next.config, and
confirmation the sodium/fiber bars still render. Flag any score moves for orchestrator review
before close (published-score change — owner already authorized the rebuild itself).

---

## RETURN BLOCK (data-agent, 2026-06-10)

status: RETURNED — orchestrator to verify claims and close.

### Pipeline run
- run_id: run_salty_snacks_002 (re-run on REAL BSIP1 corpus; engine BARI_RECAL_P0=on,
  engine-baseline-2026-06-04 family + TASK-216 extrusion signal — UNCHANGED, no scoring edits)
- Scripts (all under 03_operations/bsip0/scrape/salty_snacks_real/ unless noted):
  - 01_bsip0_off_panels.py — BSIP0: Yochananof catalog (real EAN + real image) + OFF panel by real EAN
  - 02_build_bsip1.py — curate + emit BSIP1 v0.1 into 02_products/salty_snacks/bsip1_outputs/
  - 03_build_frontend_v4.py — BSIP2 traces → salty_snacks_frontend_v4.json (editorial from real traces)
  - D4 wiring: 03_operations/bsip2/proto_v0/reports/glass_box/w2/wire_d4_salty_snacks_v4.py

### Shelf size
- 273 real salty-snack candidates harvested (real EAN+image) → 181 with usable OFF panel
  → curated/deduped to 49 BSIP1 → 47 scored & shipped (2 dropped insufficient data).

### Image verification
- 47/47 imageUrl return HTTP 200. Host: api.yochananof.co.il (single host).
- 0 fake images.{retailer}.co.il hosts remain.
- next.config.ts: api.yochananof.co.il ALREADY present in images.remotePatterns — no change needed.

### Grade distribution old(v3) → new(v4)
- v3 (54, FABRICATED corpus): A:7  B:16  C:18  D:9  E:4
- v4 (47, REAL corpus):       A:0  B:12  C:21  D:5  E:9
- NOVA v4: {2:37, 3:7, 4:3}. Retailer: yochananof:47. Subpools: chips13/puffed9/rice_cakes8/pretzels7/popcorn5/baked5.
- Ingredient coverage: 13/47 (27.7%) — OFF lacks ingredient text for most Israeli SKUs (honest gap);
  panel-only products marked confidence=partial / source_traceability_status=panel_only.

### SCORE MOVES — FLAGGED FOR REVIEW (published-score change; rebuild owner-authorized)
- This is a full corpus REPLACEMENT, not a re-score of the same products — barcodes/identities
  in v3 were fabricated, so per-product deltas are not meaningful. Category-level move:
  the v3 A-tier (7 products, mostly fabricated baked-legume snacks) DOES NOT EXIST in the real
  shelf. Real category ceiling = 77/B (פריכיות משולשות מלח ים, rice cakes). Bamba = C (matches
  prior framing "הבמבה מקבל C"). This is consistent with the "best ≠ excellent" invariant —
  no real salty snack reaches A.
- HARD-RULE-7 NOTE (2 products scored exactly 0 with no caps/penalties applied):
  "פיטנס קרקר דק סלק" (macros plausible — score 0 looks like an engine edge for products lacking
  positive-driver signals) and "אפרופו קרמל" (35g sugar/13g sat-fat — E plausible). I did NOT alter
  scoring logic. Surfacing for Nutrition Agent to confirm the score-0 path is expected behavior
  vs. a data-driver gap; not a blocker for the rebuild.

### Frontend
- salty_snacks_frontend_v4.json shipped to bari-web/src/data/comparisons/ (+ 02_products copy).
- Page wired: salty-snacks-page-data.ts now imports v4 (was v3).
- Editorial shape preserved: insightLine (2-line verdict), expansion.{positiveSignals,
  limitingFactors, bottomLine, comparisonContext, confidenceLabel, servingNote}, confidence fields.
- expansion.nutrition.sodium populated 44/47; expansion.nutrition.fiber populated 27/47
  (remaining are genuine OFF nulls; the expansion bar cells collapse on null — sodium & fiber
  bars RENDER and stay populated). Did NOT touch the SODIUM_METRIC UI code shipped this session.
- Hero/methodology copy corrected for factual accuracy to the real corpus (no Carrefour, no A,
  47 products, Yochananof): title → "הבמבה מקבל C — והכי גבוה במדף עוצר ב-B."; methodology line → 47 / יוחננוף.
- D4 additive wiring: 27.7% coverage (>15% gate), 5 products enriched with real E-numbers from
  ingredient text, INVARIANT (score/grade/glassBox) PASS.

### Gates
- Typecheck: PASS (npx tsc --noEmit, exit 0).
- Build: PASS (npx next build — "Compiled successfully", /hashvaot/salty-snacks prerendered).
- Fabricated v3 BSIP1 backed up to 02_products/salty_snacks/bsip1_outputs_FABRICATED_backup/.

### Acceptance criteria status
- [x] Real BSIP0 scrape output under 02_products/salty_snacks/bsip0_outputs/ (real EANs + images)
- [x] Every product real image URL HTTP 200; no fake hosts
- [x] next.config.ts remotePatterns allows host (already present)
- [x] Rescored, unchanged engine; grade dist reported v3→v4
- [x] v4 shipped; page wired; sodium + fiber bars populated
- [x] Build + typecheck clean; page renders with real photos

---

## ORCHESTRATOR VERIFICATION (2026-06-10) — CLOSED

Verified each return-block claim against artifacts:
- `salty_snacks_frontend_v4.json`: 47 products; image host 100% `api.yochananof.co.il`; **0** fake
  `images.{retailer}.co.il` hosts. Live-sampled 4 images → all HTTP 200. ✔
- sodium populated 44/47, fiber 27/47 (matches return block); SODIUM_METRIC UI from this session
  untouched and `sodium_mg` wired in page-data → bars render. ✔
- grade dist B:12 C:21 D:5 E:9 (A:0); shelf ceiling 77/B (פריכיות משולשות מלח ים). ✔
- `tsc --noEmit` exit 0 after correcting stale metadata description (54→47). ✔
- Page wired to v4 (import confirmed). ✔

**Closed for the data/image rebuild scope.** CARVE-OUT → **TASK-229**: the two exactly-0/E products
(`פיטנס קרקר דק סלק`, 6.5g fiber + 12g protein + 8.8g sugar yet 0/E — its own positiveSignals
contradict the grade; `אפרופו קרמל` directionally E but literal 0 is a floor artifact) are a
**scoring-engine** edge (tripwire #1, frozen scoring) requiring Nutrition diagnosis + owner sign-off.
Not a defect of this rebuild.
