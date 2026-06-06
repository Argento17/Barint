# Bari Integrations — external-data capability layer

Read-only clients that grant agents authoritative external sources instead of fragile
HTML scraping. Built under TASK-170 (owner-approved 2026-06-03). No scoring logic, no
published-score movement, no invented data — these acquire data; the pipeline/governance
decides how it's used.

## Why this exists
Agents already had Firecrawl + WebFetch (general web). The gap was that every
*authoritative* data need was served by brittle storefront scraping, which recurs as a
blocker across the project memory. These clients replace scraping with structured APIs,
and add near-free ground-truth verification reach for the agents with authority (CC) and
the only measurable user metric (Frontend mobile comprehension).

## Layout
```
integrations/
  clients/
    http.py             shared stdlib GET (UA, timeout, retry/backoff, JSON) — read-only
    open_food_facts.py  product nutrition + ingredients + image by barcode [Data,Nutrition,Frontend]
    il_prices.py        Israeli price-transparency feeds (Shufersal/laib/Super-Pharm) [Data]
    iherb_panel.py      iHerb Supplement-Facts panel extract (firecrawl)  [Data, Nutrition]
    supplement_bridge.py  Super-Pharm SKU <-> iHerb panel barcode/name bridge [Data]
    il_gov_data.py      data.gov.il regulatory layer (CKAN)             [Data, Nutrition]
    dsld.py             NIH supplement-label DB                          [Nutrition, Data]
    usda_fdc.py         USDA FoodData Central — global nutrient comp.    [Nutrition, Data]
    food_additives.py   OFF additives taxonomy: E-number identity+class  [Nutrition D4, Red-Team]
    literature.py       PubMed + Europe PMC + OpenAlex + ClinicalTrials  [Research]
    semantic_scholar.py citation-weighted evidence (TLDR + influence)    [Research, Red-Team, Nutrition]
    biorxiv.py          bioRxiv/medRxiv preprints (leading indicator)    [Research, Red-Team, Nutrition]
    crossref.py         DOI metadata + reference counts + retraction     [Research, Red-Team]
    openfda.py          food recalls/enforcement + adverse events        [Red-Team, Research, Nutrition]
    pubchem.py          compound / ingredient identity                   [Research, Nutrition]
    tzameret.py         Israeli MoH food-composition DB (DIRECTIONAL ONLY) [Nutrition]
    pagespeed.py        Google PageSpeed Insights (CWV)                  [Frontend]
    hebrew_readability.py  offline Hebrew readability + framework-leakage scan [Content, QA]
    search_console.py   Google Search Console — organic SEO performance  [Marketing]
    analytics.py        Plausible — site traffic + behaviour             [Marketing, Product]
    figma.py            Figma file/components/styles (token source)      [Design, Frontend]
    github_artifacts.py merged-commit / CI / deploy state via git+gh     [CC]
    google_workspace.py Gmail + Calendar READ-ONLY — Tom's inbox/calendar [CC — Chief of Staff]
    google_trends.py    Hebrew demand signal — DORMANT, fenced          [Product, Marketing]
    provenance.py       shared source/fetch stamp (no fetch; data-only)  [all ingestion]
```

Two more capability surfaces ship alongside this layer (outside `integrations/clients/`):
```
  bari-web/                      QA harness (devDeps only — no runtime/bundle cost)
    playwright.config.ts         mobile-first E2E (Pixel 5) + desktop
    e2e/smoke.spec.ts            comparison routes render, RTL Hebrew, rows paint
    e2e/a11y.spec.ts             axe-core WCAG2 A/AA gate (fails on serious/critical)
    lighthouserc.json            Lighthouse CI mobile budgets (LCP/CLS/a11y)
    (bundle analysis: `next experimental-analyze`, built into Next 16.1+)  [QA, Frontend, Design]
  05_command_center/
    registry_health_log.py       append-only health time-series + degradation alerts + CI probe [CC]
```
Run any client directly for a live smoke test: `python -m integrations.clients.<name>`.
Zero install footprint — clients use only the Python standard library.

## Sources, auth, and verification status

| Client | Source | Auth | Status (2026-06-03) |
|---|---|---|---|
| `open_food_facts` | Open Food Facts REST v2 | none | **LIVE-VERIFIED** |
| `literature` | NCBI E-utilities + Europe PMC + OpenAlex + ClinicalTrials.gov | none (`NCBI_API_KEY` raises limits) | **LIVE-VERIFIED** (all 4 backends) |
| `dsld` | NIH Dietary Supplement Label DB | none | **LIVE-VERIFIED** — structured ingredient rows (supplement corpus) |
| `pubchem` | PubChem PUG REST | none | **LIVE-VERIFIED** — compound identity (formula/weight/synonyms) |
| `il_gov_data` | data.gov.il CKAN datastore | none | **LIVE-VERIFIED** — imported foods (32k), manufacturers, max-prices; *pesticide resource is the preparations registry, not residues-per-food* |
| `google_trends` | Google Trends (unofficial endpoint) | none | **LIVE** (interest-over-time verified, Hebrew); related-queries 429-prone under rapid use. **DORMANT + fenced — sequencing only, never scoring** |
| `il_prices` (Shufersal) | `prices.shufersal.co.il` (Azure blob .gz XML) | none | **LIVE-VERIFIED** |
| `il_prices` (multi-chain: Victory +others) | `laibcatalog.co.il` (open .gz, no login) | none | **LIVE-VERIFIED** 2026-06-03 |
| `il_prices` (Super-Pharm) | `prices.super-pharm.co.il` (PriceTransparency.WS grid, no login) | none | **LIVE-VERIFIED** 2026-06-03 (TASK-171G) — supplement shelf identity+price |
| `iherb_panel` | iHerb PDP via firecrawl_scrape(json) | firecrawl | **LIVE-VERIFIED** 2026-06-03 (probe 5/5; TASK-171G) — Supplement-Facts panel (candidate) |
| `supplement_bridge` | (no fetch) Super-Pharm SKU <-> iHerb panel | — | **BUILT** 2026-06-03 (TASK-171G) — barcode-first then brand+dose name; assembles BSIP0-S candidate |
| ~~Cerberus `url.publishedprices.co.il`~~ | — | — | **DEAD** (DNS gone 2026-06-03) → replaced by laibcatalog |
| `tzameret` | MoH nutrition-database export (`integrations/data/moh_mitzrachim.csv`) | none | **DIRECTIONAL ONLY** (owner directive 2026-06-04 — known data-quality issues, **not authoritative**; never a value of record or calibration anchor — prefer USDA FDC + BSIP0 panel). Loads 4,624 foods via `load_table()` |
| `pagespeed` | Google PageSpeed Insights v5 | `PAGESPEED_API_KEY` (Windows **User** env var) | **LIVE-VERIFIED with key earlier**, but **2026-06-04 runtime re-probe: 429** — the key is a *User* env var that the agent's spawned processes do **not inherit** (`os.environ` sees it as absent), so it runs keyless and is throttled. Fix: set it Machine/Process-level or pass it into the agent's shell. |
| `github_artifacts` | local `git` + `gh` CLI | existing gh auth | git **LIVE-VERIFIED**; gh degrades gracefully when absent |
| `usda_fdc` | USDA FoodData Central API | `FDC_API_KEY` (free; falls back to `DEMO_KEY`) | **LIVE-VERIFIED** 2026-06-04 — SR-Legacy panels (lentils, tahini) normalised to canonical per-100g keys; `DEMO_KEY` is rate-limited, set `FDC_API_KEY` for production |
| `food_additives` | Open Food Facts additives taxonomy (disk-cached) | none | **LIVE-VERIFIED** 2026-06-04 — E330/E951/E621/E102 resolved with class + EFSA-eval link + over-exposure flag (E621=high). Honest limit: no numeric ADI / IL-divergence |
| `semantic_scholar` | Semantic Scholar Graph API | **`SEMANTIC_SCHOLAR_API_KEY` effectively required** | **LIVE-VERIFIED then DEGRADED** — verified 2026-06-04 (first call in a fresh window), but re-probe confirms the unauthenticated tier now returns **429 on a clean single request** from a shared IP. Treat as **NEEDS-KEY**: reliable only with `SEMANTIC_SCHOLAR_API_KEY`. Code is correct; the free tier is throttled. |
| `biorxiv` | bioRxiv / medRxiv API (Cold Spring Harbor) | none | **LIVE-VERIFIED** 2026-06-04 — date-window recent + DOI fetch + `published_doi` upgrade flag; preprints tagged `peer_reviewed=False` |
| `crossref` | Crossref REST API | none (polite pool via UA) | **LIVE-VERIFIED** 2026-06-04 — DOI metadata, cited-by + references counts, retraction/`update-to` integrity signal |
| `openfda` | openFDA food enforcement + CAERS events | none (`OPENFDA_API_KEY` raises limit) | **LIVE-VERIFIED** 2026-06-04 — tahini recalls (Class I) + spirulina adverse-event reaction counts. Honest limit: US jurisdiction, passive reporting |
| `hebrew_readability` | offline heuristic (no network) | — | **LIVE-VERIFIED** 2026-06-04 — readability profile + framework-leakage gate (NOVA/cap/BSIP/score-mechanic/recommendation). Leakage scan is a precise gate; readability score is a transparent heuristic, not a validated index |
| `search_console` | Google Search Console (Search Analytics) | OAuth2 `GSC_ACCESS_TOKEN` + `GSC_SITE_URL` | **NEEDS-ENV-VERIFY** — endpoints/payloads correct; awaits a verified property + OAuth token. POST query (read-only) via local stdlib helper |
| `analytics` | Plausible Stats API | `PLAUSIBLE_API_KEY` + `PLAUSIBLE_SITE_ID` | **NEEDS-ENV-VERIFY** — clean Bearer-key GET API; awaits a connected site |
| `figma` | Figma REST API | `FIGMA_TOKEN` + file key | **NEEDS-ENV-VERIFY** — files/components/styles GET endpoints; awaits a token + the Bari file key |
| bari-web `e2e/smoke` | Playwright (`@playwright/test`) | — (devDep) | **LIVE-VERIFIED** 2026-06-04 — 5/5 mobile against dev server |
| bari-web `e2e/a11y` | `@axe-core/playwright` | — (devDep) | **LIVE-VERIFIED** 2026-06-04 — harness runs; surfaced a real WCAG 1.4.3 contrast finding on grade chips (true positive for Design) |
| bari-web `lhci` | `@lhci/cli` | — (devDep) | **CONFIGURED** — mobile budgets wired; run after `next build` |
| `registry_health_log` | reads `command_center_live.json` (+ `github_artifacts` CI probe) | — | **LIVE-VERIFIED** 2026-06-04 — append-only JSONL series + degradation diff (blocked/returned/CR/WIP/alerts/drift/CI) |

## Hard rules (all clients)
1. **Read-only.** No writes, pushes, merges, or state changes anywhere.
2. **Identity ≠ nutrition.** Price feeds carry barcode + price, never panels. Pair a
   barcode with `open_food_facts` (candidate) or `usda_fdc` (lab-measured generic) for
   composition. `tzameret` is **directional only** — never the value of record.
3. **Candidate, not truth.** OFF is crowd-sourced — its panels still pass BSIP0/QA gates.
4. **No fabricated greens.** A source that couldn't be reached in the build sandbox is
   marked `NEEDS-ENV-VERIFY`, not assumed working. Verify in the owner's network first.
5. **Record provenance.** Log source + fetch date for any data entering the corpus.

## External Data Admission rule (EDPG) — the inbound gate

The four-agent review (Data, QA, Nutrition, Product) converged on one principle:
**this layer is a *fetch* capability, never an *admission* capability.** A structured API
feels more authoritative than a scrape — that feeling is the backdoor. The controls:

- **Every ingestion client stamps a `Provenance` envelope** (`provenance.py`): `source`,
  `source_id`, `source_url`, `fetched_at` (UTC), `client_version`, `verification_status`.
  Carried on `OffProduct`, `PriceItem`, `GovRecords`, `SupplementLabel`, `FoodComposition`.
- **`verification_status` is born `candidate` — always.** "LIVE-VERIFIED" in this README
  means *the client reached the source*, NOT *the datum is true*. Those are different
  claims; conflating them is the failure mode. Only the (future) admission gate, after a
  BSIP0/QA pass, may promote `candidate → verified`.
- **No external value reaches BSIP2 scoring unless it is `verified`** — i.e. it cleared
  the existing BSIP0 + QA gates exactly as a scrape would. The integration layer does not
  create a new path into the corpus; it feeds the existing one. Admission stays at D3/D4
  (Product) + QA freeze + D10, unchanged.
- **The engine reads in-house labels only.** External sources may *calibrate/justify* a
  rule (cite source + release in the evidence registry); they may never be a label the
  engine *reads*. (Nutrition firewall.)

QA's enforcement spec (EXT-001…007: provenance present, candidate-quarantine, source-
appropriate-for-catalog, freshness, resource-id pinning, completeness reconciliation) is
recorded in the TASK-170 follow-up for when the first category actually ingests external
data. Cross-ref: `.claude/scoring.md`.

## Environment keys
Optional (raise rate limits / improve reliability):
- `NCBI_API_KEY` — higher PubMed rate limit.
- `PAGESPEED_API_KEY` — reliable PageSpeed runs (avoids 429).
- `TZAMERET_RESOURCE_ID` — data.gov.il CKAN resource id, once confirmed in-env.
- `FDC_API_KEY` — USDA FoodData Central (free; `DEMO_KEY` works but is rate-limited).
- `SEMANTIC_SCHOLAR_API_KEY` — higher Semantic Scholar limit.
- `OPENFDA_API_KEY` — higher openFDA limit.

Required for the credential-gated clients (NEEDS-ENV-VERIFY until set):
- `GSC_ACCESS_TOKEN` + `GSC_SITE_URL` — Search Console (OAuth2 `webmasters.readonly`).
- `PLAUSIBLE_API_KEY` + `PLAUSIBLE_SITE_ID` — Plausible Stats API (`PLAUSIBLE_BASE_URL` for self-hosted).
- `FIGMA_TOKEN` + `FIGMA_FILE_KEY` — Figma REST API.

> **Honest caveat (Marketing/Product/Design):** `search_console`, `analytics`, and `figma`
> are complete and correct but their live verification depends on a *connected account*
> (a verified Search Console property, a Plausible site, a Figma token + file key). Their
> capability reaches the target; the green check waits on credentials, by design — we do
> not fabricate a LIVE-VERIFIED for a source we couldn't reach.

## Windows note
Clients return clean Unicode; only the `__main__` smoke prints can trip the cp1252
console on Hebrew output. Run with `PYTHONUTF8=1` when smoke-testing Hebrew sources
(`il_prices`, `tzameret`).

## Verification to do in the owner's network
- `il_prices`: confirm Cerberus host + per-chain login; `parse_price_xml` is already
  schema-shared, so only listing/auth differs.
- `tzameret`: download the official MoH export → `load_table(path)` (reliable), or
  confirm the CKAN `resource_id` and set `TZAMERET_RESOURCE_ID`.
- `pagespeed`: obtain a free API key, set `PAGESPEED_API_KEY`.
