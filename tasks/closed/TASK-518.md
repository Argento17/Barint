---
id: TASK-518
title: BSIP0 retailer fleet - reach 5-6 BSIP0-ready retailers (infrastructure only, no category builds)
owner: data-agent
status: CLOSED
close_reason: >
  Owner-re-scoped DoD met and orchestrator-verified: fleet = 4 BSIP0-READY retailers (Shufersal,
  Hazi Hinam, Yohananof, Tiv Taam — owner added Tiv Taam as the 4th, 2026-07-05). All four proven by
  butter smoke probes; Yohananof + Tiv Taam additionally re-probed FRESH by the orchestrator on owner
  request (agents elsewhere reported reach trouble): Tiv Taam 30/25/23-25/22-25 identical to prior run;
  Yohananof 19 discovered / 16 scraped / 16-16 parsed (its raw 4/16 gate = probe-harness FoodClass
  artifact — butter routed to dairy_solid's 450-kcal cheese cap; parsed data correct). Reach guidance:
  use the engines (yohananof/acquire_yohananof.py, tiv_taam/acquire_tivtaam.py, hazi_hinam/
  acquire_hazi_hinam.py) — raw HTTP hits Cloudflare on yochananof. Set aside per owner: Victory,
  Carrefour (self-point WAF cool-down path documented), Super Yuda (Radware edge ACL, owner-browser
  test = future option), Rami-Levy (HAR), Osher Ad (no store). All work uncommitted in
  03_operations/bsip0/scrape/.
priority: HIGH
created_at: 2026-07-05
depends_on: []
blocks: []
category_id: null
summary: >
  Fix/extend the BSIP0 acquisition layer so 5-6 retailers are BSIP0-ready (today effectively Shufersal only). Fix Yohananof pacing/thinness, crack Victory via untried hypotheses (branch cookie / HAR / API replay), attempt Rami-Levy HAR, verify Carrefour, add Osher Ad / Tiv Taam / Hazi Hinam as needed. Readiness proven by per-retailer smoke probe through the plausibility gate. No category page work; TASK-515 stays parked.
---

# TASK-518 — BSIP0 retailer fleet - reach 5-6 BSIP0-ready retailers (infrastructure only, no category builds)

## FINAL FLEET — 2026-07-05 (owner decision): Shufersal · Hazi Hinam · Yohananof · Tiv Taam = 4 READY, enough for now

Owner added Tiv Taam back as the 4th after Super Yuda came back BLOCKED. Orchestrator fresh re-probe of the
two "hard to reach" retailers (same day, direct runs):
- **Tiv Taam**: 30 discovered / 25 scraped (5 no-barcode) / 23-25 parsed / 22-25 gate — byte-identical
  profile to the verified earlier run. Raw: `_smoke_probes/outputs/tivtaam_butter/tivtaam_bsip0_raw_20260705T085621.json`.
- **Yohananof**: 19 discovered / 16 scraped (3 empty-panel) / 16-16 parsed. The raw 4/16 gate number is a
  PROBE-HARNESS artifact: the smoke script passed butter as `dairy_solid` (cheese class, kcal cap 450) while
  real butter is ~730-750 kcal/100g — correct parses "failed" a wrong class. Tiv Taam's probe used the spread
  class and behaved. For future category runs: pass the right FoodClass per category; the gate itself is fine.
  Raw: `_smoke_probes/outputs/yohananof_butter/yohananof_bsip0_raw_20260705T090032.json`.
**Reach guidance for future agents** (owner reported agents struggle to reach these two): do NOT probe with
raw HTTP — yochananof.co.il sits behind Cloudflare (false DOWN on HEAD) and Tiv Taam needs its API pattern.
Use the proven engines: `yohananof/acquire_yohananof.py` (Playwright, scroll-pacing + fixed EAN regex),
`tiv_taam/acquire_tivtaam.py` (self-point JSON API), `hazi_hinam/acquire_hazi_hinam.py` (JSON API).

## OWNER RE-SCOPE — 2026-07-05 (superseded 5-6 → core-3 + probe Super Yuda; then finalized above)

Owner: **core fleet = Shufersal → Hazi Hinam → Yohananof, in this priority order.** Victory, Carrefour, and
Tiv Taam are SET ASIDE (parked — no retries; the WAF cool-down path is shelved, the Tiv Taam engine is kept
as a proven self-point reference). **Probe Super Yuda (yuda.co.il, own storefront, plain-HTTP 403 bot-gate)
as the candidate 4th — 4 READY is enough for now.** Wolt/Yango Deli assessed and rejected as sources
(aggregator provenance / market exit); Super-Pharm reserved as a category-specific source for supplements
(SAP Hybris platform), not part of this fleet. Super Yuda probe DISPATCHED to the P518 Data Agent (resumed)
2026-07-05.

## Super Yuda probe — 2026-07-05 (P518 continuation), orchestrator-VERIFIED → BLOCKED

Radware Cloud WAF (`server: rdwr`) at the network edge: instant 403 with only a Transaction ID on every
path tried (`/`, `/robots.txt`, `/sitemap.xml`, `/he`, `/shop`, `/online`), zero cookies set, zero XHR ever
fired — content is blocked BEFORE the storefront platform can even be identified. Headless Playwright,
headed + anti-automation flags + desktop UA: all identical. Shufersal control from the same run returned 200
(not a connectivity issue). Orchestrator independently reproduced the instant 403 + `Server: rdwr` header
with a separate client stack. Distinct from Victory's Cloudflare JS-challenge (which a headed page passes) —
this is a pre-content edge ACL. No in-constraint fix (different egress IP = proxy = banned).
Verdict = BLOCKED (not NOT-VIABLE — the site was never reached, so its nutrition-data quality is unknown).
Diagnostics: `_smoke_probes/diag_superyuda_{platform_id,headed,radware_probe}.py` + `outputs/superyuda_xhr_log.json`.

## Progress — 2026-07-05 Data Agent return (P518), orchestrator-VERIFIED

**READY = 4** (target 5-6, short by 1-2):

| Retailer | Status | Verified evidence (butter smoke probes, fresh final-run numbers) |
|---|---|---|
| Shufersal | READY | 22 discovered/captured, 22/22 ingredients, 20/22 nutrition parsed, gate 16/22 (6 genuine data edges). Reused `shufersal_butter/01_scrape_butter.py`. |
| Yohananof | READY (fixed) | Root cause of chronic under-capture FOUND: candidate-discovery EAN regex `_(\d{13})_` required underscores on BOTH sides — real image filenames use >=4 patterns; 702 of ~900 DOM occurrences silently dropped. Fixed to lookaround `(?<!\d)(\d{13})(?!\d)`. Probe: 19 discovered, 16/19 scraped (3 empty-panel), parse 16/16, gate 13/16. New engine `yohananof/acquire_yohananof.py`. |
| Hazi Hinam | READY (new) | Structured JSON API (`getItemsBySubCategory` + `GetItemGS1Details`), no WAF, no DOM scroll. Probe: 28 discovered, 27/28 scraped, parse 26/27, gate 25/27. New engine `hazi_hinam/acquire_hazi_hinam.py`. |
| Tiv Taam | READY (new) | Same self-point `v2/retailers/.../products` platform as Victory/Carrefour but WAF-free AND returns inline per-100g `nutritionValues`. Probe: 30 discovered (of 184 available), 25/30 scraped (5 no-barcode), parse 23/25, gate 22/25. New engine `tiv_taam/acquire_tivtaam.py`. |
| Victory | BLOCKED | Hard WAF block ("you have been blocked", self-point.com) on storefront + API, incl. plain homepage — a NEW harder layer than the 3 previously diagnosed failures; likely rate-limit tripped by this session. Next: retry the Tiv-Taam-proven API pattern after cool-down / fresh IP. |
| Carrefour | BLOCKED (new finding) | Same self-point hard WAF block on storefront + `v2/retailers/1540/...` API. Same next step as Victory. |
| Rami-Levy | BLOCKED | Not re-attempted (exhaustively re-probed same day, `retailer_capabilities/rami_levy_task515_reprobe.md`). Next: real headed-Playwright HAR capture in a future session. |
| Osher Ad | NOT VIABLE | No online store at all (WordPress marketing/recipes site). Dropped from candidate list. |

**Orchestrator verification (2026-07-05):** all 7 claimed artifacts exist with fresh timestamps; independent
recount of the 4 raw probe JSONs matches the return exactly (shufersal 22/22 ing+nut; yohananof 19 rec /
16 ingredients = 3 empty-panel; hazi_hinam 27/28; tivtaam 25/30 with-barcode); OFF census clean on all new
engines (0 hits); `_shared/plausibility_gate.py` yogurt FoodClasses intact (7 refs) and sugar-parser fix
preserved; tree scope confined to `03_operations/bsip0/scrape/` (everything else = pre-existing ambient dirt).

**Artifacts (uncommitted, working tree):** 3 new engines (`yohananof/acquire_yohananof.py`,
`hazi_hinam/acquire_hazi_hinam.py`, `tiv_taam/acquire_tivtaam.py`), `_smoke_probes/` (4 probe entry points,
27 diagnostics, raw outputs under `_smoke_probes/outputs/`).

**Remaining to close:** +1-2 READY retailers. Cheapest path = Victory and/or Carrefour via the proven
self-point API pattern from a fresh session/IP after WAF cool-down; fallback = Rami-Levy HAR capture.
