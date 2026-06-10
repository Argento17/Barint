---
id: TASK-170
title: External-data integration layer — grant agents authoritative APIs (price feeds, OFF, PubMed/Europe PMC, Tzameret, PageSpeed, GitHub-verify)
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-03
depends_on: []
blocks: []
category_id: null
roadmap_impact: true
cc_reviewed: 2026-06-03
close_reason: >
  Verified independently against artifacts: 10 clients + http.py + README + CSV
  present; all 10 import clean; OFF live spot-check real (Nutella kcal=539 nova=4,
  matches return); 5 agent grants present; TASK-170 changeset is integrations/ +
  5 agent docs only — no scoring engine / published-score JSON touched (capability-
  only confirmed). Pesticide=preparations-registry caveat recorded in README+code;
  Semantic-Scholar/Google-Trends not-built caveat recorded in task body.
cc_comments:
  - flag: fyi
    note: >
      Capability grant, not a scoring/data change. No published score moves. Adds an
      integrations/ client layer + grants 5 agents read-only external sources. Two
      sources (publishedprices multi-chain host, gov.il Tzameret) are blocked from the
      build sandbox (DNS/SSL) and ship as documented-contract clients flagged
      NEEDS-ENV-VERIFY — they must be smoke-tested in the owner's network before use.
  - flag: verify
    note: >
      CLOSED after gate. Verified: 10 clients import clean, OFF live (Nutella 539kcal/
      nova4), 5 grants landed, changeset capability-only (no scorer/score JSON touched).
      Minor: README omits the Semantic-Scholar/Google-Trends "not built" caveat (it lives
      in the task body) — add to README if it should be the durable record.
summary: >
  Owner-approved (2026-06-03) after a capability evaluation found the agents are served
  almost entirely by fragile HTML scraping when authoritative structured sources exist.
  Builds a thin `integrations/` client layer and grants six external sources across five
  agents, split into two opportunity types: (1) ingest authoritative data — Israeli
  price-transparency feeds + Open Food Facts API (Data/Nutrition), PubMed + Europe PMC
  (Research), MoH Tzameret food-composition (Nutrition); (2) verify against ground truth —
  Google PageSpeed Insights (Frontend, mobile-comprehension metric) + GitHub artifact
  state (CC, hardens the closing-authority gate). Read-only, mostly free/no-auth. No
  scoring logic changes. Clients are smoke-verified against live endpoints where the build
  sandbox allows; the rest ship flagged for owner-env verification.
---

# TASK-170 — External-data integration layer

## Trigger (2026-06-03)
Owner asked "which external APIs/websites can we grant to our agents — I think we're
missing opportunity." Evaluation found: agents already have Firecrawl + WebFetch (general
web), but every *authoritative* data need is served by brittle storefront scraping —
which recurs as a blocker across memory (retailer sites blocked, Playwright recommended,
OFF ingredient blocker). The opportunity is **structured/authoritative APIs replacing
scraping**, plus near-free **ground-truth verification reach** for the agents with
authority (CC) and the only measurable user metric (Frontend mobile comprehension).

Owner approved the full set: Tier-1 items 1–4 + Frontend + CC.

## Scope — six sources, two types

| # | Source | Agent(s) | Type | Build-sandbox status |
|---|--------|----------|------|----------------------|
| 1 | Israeli price-transparency feeds | Data | ingest | Shufersal portal LIVE-200; multi-chain host DNS-blocked here → flagged |
| 2 | Open Food Facts REST API | Data + Nutrition | ingest | LIVE-VERIFIED (200) |
| 3 | PubMed E-utilities + Europe PMC | Research | ingest | LIVE-VERIFIED (both 200) |
| 4 | MoH Tzameret food-composition | Nutrition | ingest | gov.il SSL-blocked here → flagged NEEDS-ENV-VERIFY |
| 5 | Google PageSpeed Insights | Frontend | verify | endpoint LIVE (429 w/o key) → needs API key |
| 6 | GitHub artifact state (via `gh`) | CC | verify | `gh` already authorized |

## Hard constraints
- Read-only. No scoring logic, no published-score movement, no invented data.
- Clients live under `C:\Bari\integrations\` (new capability layer, not a pipeline stage).
- Never hardcode an unverified endpoint as if confirmed — flag NEEDS-ENV-VERIFY.
- Price feeds give identity+price, NOT nutrition; OFF/Tzameret give the panels.

## Deliverables
- `integrations/` client layer (shared HTTP + 6 clients) with inline smoke tests
- Capability grants in Data / Nutrition / Research / Frontend / CC agent docs
- `integrations/README.md` (sources, contracts, auth, verification status)
- Memory entry; dashboard regen

## Return block (orchestrator → CC) — proposed RETURNED

Built `C:\Bari\integrations\` (read-only, stdlib-only) + granted 5 agents. Smoke-tested
against live endpoints where the build sandbox allowed:

| Client | Agent | Live-verify result |
|---|---|---|
| `open_food_facts` | Data + Nutrition | ✅ LIVE — fetched real panels (Nutella kcal=539, NOVA=4) |
| `literature` | Research | ✅ LIVE — PubMed returned creatine meta-analyses w/ pub_types + abstracts; Europe PMC returned citation/OA flags |
| `il_prices` (Shufersal) | Data | ✅ LIVE — listed 20 portal .gz files, downloaded+gunzipped+parsed real items (barcodes, ₪ prices, Hebrew names/units) |
| `il_prices` (multi-chain) | Data | ✅ LIVE — old Cerberus host `url.publishedprices.co.il` found DEAD (DNS gone, both networks); replaced with `laibcatalog.co.il` (Victory +4 chains, **no login**); parsed real items end-to-end |
| `tzameret` | Nutrition | ✅ LIVE — owner downloaded MoH export → `load_table()` loaded **4,624 Israeli foods**; COLMAP set to real per-100g headers; verified cottage/milk/lentils macros |
| `pagespeed` | Frontend | ✅ LIVE — owner created API key (set as user env var); verified mobile run (Wikipedia perf=100, LCP=1.35s). NB: no public Bari URL deployed yet → measure once site is live |
| `github_artifacts` | CC | ✅ git path LIVE (correctly flagged comparisons dir `on_default=False` on this branch); gh path degrades gracefully (gh not on sandbox PATH) |

Agent grants: Data, Nutrition, Research, Frontend, CC each got an "External Data Access
(TASK-170)" section with client table + guardrails. No `settings.json` change needed —
stdlib `urllib` is unaffected by the `curl`/`wget` deny.

**All 3 owner-env items resolved (2026-06-03):** PageSpeed key ✅, Tzameret export ✅,
price feeds ✅ (dead host replaced by laibcatalog). Bug found+fixed during verification:
shared `http.get` hardcoded `Accept: application/json` → 406 on binary .gz; now `*/*`,
JSON clients regression-tested clean.

**Residual (non-blocking):** (a) laibcatalog landing lists a rotating chain subset —
`discover_laibcatalog_chains()` reports the live set; 4 chain_ids name-unconfirmed pending
their Stores file. (b) PageSpeed has no Bari URL to measure until deployment.

**CC note:** roadmap_impact:true. All 6 clients live-verified; no published scores moved
(capability-only). Ready for close-readiness gate.

## Phase 2 — second-pass discovery (2026-06-03, owner: "build everything new")

A deliberate completeness re-run (probe-first, aimed at pass-1 blind spots: supplement-
light, PubMed-only evidence, no imagery, no demand/regulatory) found and **live-verified**
6 more sources, all free:

| New client/extension | Agent | Fills gap | Verified |
|---|---|---|---|
| `dsld` | Nutrition + Data | **Supplements** — structured labels w/ ingredient amounts (creatine 1.5g/2 caps). Biggest miss: supplements are scored, had no source. | ✅ |
| `open_food_facts` +image fields | Frontend + Data | **Packaging imagery** (design spec mandates it) — `image_url` by barcode (Tnuva milk image returned). | ✅ |
| `il_gov_data` | Data + Nutrition | **Israeli regulatory** — imported foods (32,620), licensed manufacturers (4,825), official max-prices (597, backup price source). | ✅ |
| `literature` +OpenAlex +ClinicalTrials.gov | Research | **Evidence depth** beyond PubMed — scholarly graph + trial registry (null/unpublished results). | ✅ |
| `pubchem` | Research + Nutrition | **Ingredient/additive identity** (formula, weight, synonyms). | ✅ |

Total layer now **10 clients, all live-verified**. Accuracy notes: the data.gov.il
"pesticide" resource is the approved-**preparations** registry, not residues-per-food
(reference only, not a per-product quality signal). Semantic Scholar live but 429s w/o a
key (not wired). Google Trends (Hebrew demand) noted for Product/Marketing, not built.
Grants extended in Data/Nutrition/Research/Frontend docs.
