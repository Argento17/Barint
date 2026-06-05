---
name: external-integration-layer-task170
description: "integrations/ client layer (TASK-170) granting agents authoritative external APIs — what's built, verified, and still needs owner-env verification"
metadata: 
  node_type: memory
  type: project
  originSessionId: c7f160bd-00cf-49a9-915d-5060e6916c1a
---

TASK-170 (owner-approved 2026-06-03) built `C:\Bari\integrations\` — a read-only, stdlib-only
client layer that grants agents authoritative external sources instead of fragile storefront
scraping. Capability grant only: no scoring logic, no published-score movement.

Six clients under `integrations/clients/` (run `python -m integrations.clients.<name>` to smoke-test):
- `open_food_facts` (Data+Nutrition) — barcode→panel; **LIVE-VERIFIED**
- `literature` (Research) — PubMed E-utilities + Europe PMC, returns pub_types/citations; **LIVE-VERIFIED**
- `il_prices` (Data) — Israeli price-transparency feeds, both portals **LIVE-VERIFIED**: Shufersal (`prices.shufersal.co.il`, Azure .gz) + multi-chain `laibcatalog.co.il` (Victory +4 chains, **NO login**). ⚠️ old Cerberus host `url.publishedprices.co.il` is **DEAD** (DNS gone 2026-06-03, both networks) — laibcatalog replaced it. `discover_laibcatalog_chains()` reports the live (rotating) chain subset. Other live hosts exist (prices.mega.co.il, matrixcatalog.co.il) addable via same `_descriptors`+`parse_price_xml`
- `tzameret` (Nutrition) — Israeli MoH צמרת composition DB, **LIVE-VERIFIED**: owner downloaded the data.gov.il `nutrition-database` per-100g export to `integrations/data/moh_mitzrachim.csv` → `load_table()` loads **4,624 foods**; headers are transliterated-English (shmmitzrach=name, food_energy, total_fat, total_dietary_fiber, sodium, saturated_fat...), COLMAP set accordingly; has the exact cottage/milk lines TASK-169 rescores
- `pagespeed` (Frontend) — PageSpeed Insights/CWV, **LIVE-VERIFIED**: owner created a Google API key (restricted to PageSpeed), set as user env var `PAGESPEED_API_KEY`. NB: no public Bari URL deployed yet → can't measure a real comparison page until the site is live
- `github_artifacts` (CC) — verifies return-block claims against actual git/GitHub state (`file_on_default_branch`, `ci_status`); git path **LIVE-VERIFIED**, gh path degrades gracefully when gh absent

**Phase 2 (2026-06-03, "build everything new")** — a probe-first completeness re-run added 4 more clients + 2 extensions, all LIVE-VERIFIED, totaling **10 clients**:
- `dsld` (Nutrition+Data) — NIH supplement-label DB, structured ingredient amounts (creatine 1.5g/2caps). Fills the biggest pass-1 gap: supplements are scored but had NO data source. US data → generic actives/doses, not Israeli SKUs
- `open_food_facts` +image fields — `image_url`/`image_small_url` by barcode; serves the frontend "packaging imagery mandatory" rule (Tnuva milk image returned)
- `il_gov_data` (Data+Nutrition) — data.gov.il CKAN: imported foods (32,620, identity/importer), licensed manufacturers (4,825, legitimacy), official max-prices (597, backup price source). ⚠️ the "pesticide" resource is the approved-PREPARATIONS registry, NOT residues-per-food (reference only). Resource IDs hardcoded + `resolve_resource()` re-resolves on 404
- `literature` +`openalex()` +`clinicaltrials()` (Research) — scholarly graph + trial registry beyond PubMed (null/unpublished results)
- `pubchem` (Research+Nutrition) — compound/additive/active identity (formula, weight, synonyms)
- NOT built: Semantic Scholar (429 w/o key), Google Trends Hebrew demand (noted for Product/Marketing). Bug fixed during phase-2: `http.get` hardcoded `Accept: application/json` → 406 on binary .gz; now `*/*`

**Post-close hardening (2026-06-03)** — TASK-170 CLOSED by CC (verified against artifacts). Then 4 agents (Data/QA/Nutrition/Product) assessed implications and converged on one thing: the layer is a FETCH capability, NEVER an ADMISSION capability — external data must not silently become a scoring input. Acted on owner approval:
- **Provenance stamping (EDPG foundation) — DONE.** New `integrations/clients/provenance.py`; the 5 ingestion clients (OFF, il_prices, il_gov_data, dsld, tzameret) now stamp every record with source/source_id/source_url/fetched_at/client_version/`verification_status` — **born `candidate` always** ("LIVE-VERIFIED"=client reached source, NOT data-is-true). Rule: engine reads in-house BSIP0 labels only; external data calibrates/justifies a rule (w/ evidence-registry cite) but is quarantined from scoring until a BSIP0/QA pass promotes candidate→verified. Documented in `integrations/README.md` "External Data Admission rule (EDPG)" + cross-ref in `.claude/scoring.md`. The full QA enforcement spec (EXT-001…007: provenance-present, candidate-quarantine, source-appropriate, freshness, resource-id-pinning, completeness-reconcile) is DEFERRED to when the first category actually ingests external data (Product ruling) — not yet built.
- **`google_trends` client — DONE (dormant + fenced).** Hebrew demand signal for Product/Marketing D1 category SEQUENCING only, NEVER scoring (popularity≠quality). `interest_over_time()` LIVE-VERIFIED (חלב 53 pts); `rising_queries()` works but 429-prone (unofficial endpoint). Grants added to product+marketing agent docs.
- **Registry health:** fixed broken YAML (unquoted colon in `title:`) on TASK-162/165/166/167/168A — were invisible on the board; now restored.
- **Product rationalization:** 5 clients earn keep now (OFF, il_prices, tzameret, github_artifacts, PubMed-core); 5 dormant-until-needed (dsld, il_gov_data, pubchem, OpenAlex/ClinicalTrials, pagespeed). DSLD existing does NOT move supplements up the roadmap (data source ≠ demand+methodology).

Two opportunity types: **ingest** (OFF, il_prices, il_gov_data, dsld, literature, pubchem, tzameret) vs **verify against ground truth** (pagespeed for Frontend, github_artifacts for CC's closing gate). Price feeds = identity+price only, NEVER nutrition — pair barcode with OFF/tzameret. OFF = candidate panel, still passes BSIP0/QA. No `settings.json` change needed (stdlib urllib unaffected by curl/wget deny).

**Why:** agents had Firecrawl+WebFetch (general web) but every authoritative need was brittle scraping — a recurring blocker (retailer sites blocked, OFF ingredient blocker). **How to apply:** for corpus/evidence/composition/perf/close-verify tasks, reach for the matching client; finish owner-env verification of the 3 open items (Cerberus login, Tzameret resource_id/export, PageSpeed key) before relying on the flagged sources. Each agent doc has an "External Data Access (TASK-170)" section. See `integrations/README.md`. Related: [[cc_agent_v2_upgrade]], [[bsip0_fat_overwrite_ev029]].
