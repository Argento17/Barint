---
id: TASK-255
title: "Leap 4+ — continuous scrape with change detection AND shelf expansion (owner amendment: new products auto-enter approved shelves)"
owner: orchestrator
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-12
depends_on: [TASK-254]
blocks: []
category_id: null
summary: >
  Owner approval 2026-06-12 (tech leap 4, "Self-Maintaining Corpus") WITH
  owner amendment: do not only re-verify known products — EXPAND approved
  shelves. A shelf's configuration (mapping, corpus filters, flags, scoring,
  copy rules) is human-approved law; a newly discovered product on that shelf
  is a new row under existing law, not a new decision. Scheduled crawler
  content-hashes known product pages (change -> re-extract + re-score that
  product only; delisted -> removal review) and sweeps shelf listings for
  unknown products (new -> full BSIP0->BSIP2->copy chain under the shelf's
  approved config). Auto-admission is gated (see admission contract); the
  scheduled-retailer-access problem (VPN/session) is the critical-path
  unknown, not the hashing.
---

# TASK-255 — Leap 4+: continuous scrape + shelf expansion

## Owner amendment (2026-06-12, verbatim intent)
"The system already has all configurations to the shelves, approved by human —
so why not just add more? On yogurts, if the scraper finds a new yogurt, add
it with the same logic that applies for all yogurts."

## Admission contract for auto-added products (the safety core)
A new product auto-publishes ONLY if every machine gate passes; any ambiguity
-> quarantine for human review, never silent add, never silent drop:
1. Direct-scrape data only (OFF ban absolute; unparseable nutrition = NULL
   fields / transparency row or quarantine — never filled from elsewhere).
2. Shelf corpus filters pass (the same human-approved filters as the
   existing corpus).
3. Router/classifier agrees the product belongs to the shelf (granola-in-
   yogurt misroute class; converges with Leap 5 embedding identity graph —
   v1 can use router + filters without embeddings).
4. Plausibility gates pass (macros_plausible etc. — the protein=190g class).
5. Duplicate check vs existing corpus (barcode + name; salty-snacks
   fabricated-identity class).
6. Generated copy passes the Leap 6 entailment gate (hence depends_on
   TASK-254) + banned-phrase linter.
7. TOP-DISPLACEMENT HOLD: if the newcomer would become the shelf's top
   recommendation, earn its best grade, or disturb a frozen-category framing
   (e.g. milk "top = 85/A"), it is HELD for human review — auto-admission is
   for body ranks. Frozen invariants are never re-framed by a crawler.
8. Lineage recorded in Spine datastore (TASK-252); rescores diffed by Shadow
   semantics — a re-extraction that moves existing scores is a finding, not
   an auto-ship.

## Recon findings (Phase 0 returned 2026-06-12 — task255_scrape_recon_v1.md)
- Shufersal: HTTP+BS4, can enumerate listing pages + barcodes → sweep feasible.
- Yohananof: yogurt acquisition = "il_prices + OFF panel" model → DEAD BY LAW
  (TASK-238 project-wide OFF ban; client hard-fails since TASK-242). Continuous
  scrape for Yohananof requires a NEW Playwright storefront scraper
  (yohananof_milk pattern). No OFF path is ever rebuilt.
- Raw HTML persisted only by shufersal_frozen_vegetables; yogurt scraper keeps
  only the nutrition-table inner HTML (EV-029). No content-hash substrate yet.
- #1 blocker: Israeli-IP access for Shufersal is a manual ad-hoc VPN step —
  unschedulable. Code cannot fix; needs an access decision (owner, spend).

## BSIP0.5 — owner directive 2026-06-12 ("consider improving BSIP0;
## firecrawl dropped, not an option")
Architectural ruling for the rebuild (orchestrator):
- **Fetch/parse split — store raw first.** The scrape session does ONLY
  fetch-and-persist: raw HTML (+ screenshot where Playwright) + fetch metadata
  into a raw store with a manifest. ALL extraction runs OFFLINE against the
  raw store, replayable forever. This decouples the scarce fragile resource
  (Israeli-IP session) from the frequently-changed code (parsers); gives
  content-hashing for free (hash stored raw); gives provenance evidence for
  the Leap 6 gate; and is the substrate Leap 1 dual-extraction needs (parser
  and vision-LLM read the SAME stored artifact).
- **One fetcher per retailer, not per category.** A category = a listing-URL
  config entry, not a new script. Playwright default engine; BS4 fast path
  where plain HTTP suffices (Shufersal).
- **No third-party acquisition dependencies** (firecrawl dropped; OFF banned;
  il_prices allowed for IDENTITY/price discovery only — never panels).

## Phase plan (amended)
1. BSIP0.5 pilot on Shufersal yogurts: raw-store fetcher + manifest +
   content hash; offline re-parse of the existing corpus from stored raw
   (replay proof); listing sweep diffing discovered barcodes vs corpus.
2. Shelf-listing sweep + admission pipeline (owner amendment) on yogurts,
   quarantine report for holds.
3. Access decision — RESOLVED by owner 2026-06-12: small Israeli VM approved
   as the PERMANENT scrape runner (not temp; owner relocating to Israel
   ~2026-08 — that makes manual sessions free but does not replace an
   always-on scheduled runner). First job on the box: datacenter-IP
   bot-block probe vs Shufersal; if blocked, fallback = residential proxy
   for scrape traffic only (VM keeps scheduler + raw store).
   **Kit DELIVERED + verified 2026-06-12** (03_operations/bsip0/scrape_runner/,
   7 files: provider_pick, setup.sh, OWNER_RUNBOOK, probe_shufersal,
   probe_yohananof, probe_all = 9-retailer rollout map, sync_design; verified
   present, full retailer coverage, zero OFF/firecrawl references).
   Provider pick: Kamatera Tel Aviv, $6/mo (1 vCPU / 2GB / 20GB) — APPROVED
   within already-authorized spend.
   **VM LIVE 2026-06-12**: 45.93.95.32 (Kamatera, Ubuntu 24.04, owner-built via
   OWNER_RUNBOOK_WINDOWS.md; SSH key auth from owner PC; setup.sh hardened —
   4 real-world fixes baked back into the kit: libasound2t64 rename, PEP 668
   venv at /opt/bari/venv, ssh-not-sshd unit name, wrapper-not-symlink for
   bari-python + use full venv path always).
   **PROBE v1 RESULTS** (logs: Desktop + /opt/bari/logs/): headline "0 CLEAN /
   6 BLOCKED" is MISCALIBRATED — zero actual IP/WAF blocks occurred. Truth:
   ALL 9 retailers answered HTTP 200 from the DC IP. Decomposition: Rami Levy =
   static SSR 100KB pages (best candidate, predicted Cloudflare block absent);
   Shufersal = real listing pages w/ barcodes, stale product-URL guess + dormant
   captcha marker to verify by render; Victory/Carrefour/MCK/Hazi Hinam/Tiv
   Taam = JS shells → Playwright; Yohananof = probe used wrong hostname (SSL
   CN mismatch); Osher Ad = wrong URL guesses. NO proxy need demonstrated.
   NEXT: probe v2 (Playwright render + repo's real battle-tested endpoints),
   dispatched to cheap lane; agents now operate the VM directly over SSH.
4. Yohananof Playwright storefront scraper (replaces dead OFF model).
5. Multi-retailer rollout (owner challenge 2026-06-12: "there are literally
   5-7 online retailers" — Shufersal is FIRST, not ONLY). Two fetch
   archetypes prove the contract: HTTP+BS4 (Shufersal, Phase 1) + Playwright
   (Yohananof, Phase 4); every further retailer (Carrefour IL, Victory,
   Rami Levy, Tiv Taam, ...) = stamp-out of an archetype (fetch module +
   listing config), parallelizable to cheap agents. The VM probe (Phase 3
   kit) maps ALL retailers' access posture (DC-IP reachable / JS-only /
   blocked) on day one — that table is the rollout order. Cross-retailer
   same-barcode disagreement feeds Leap 5 identity/duplicate detection.
6. Rollout across live categories; reformulation-detection marketing claim
   only after Phase 1 proves real detections.

## Constraints
- Spine stages + Shadow gates are the substrate; no bespoke one-off scripts.
- Adding a row never moves existing published scores (frozen invariants
  untouched); any existing-score movement = Shadow finding -> Nutrition.
- Go-live of auto-admission itself (first time a crawler-added product goes
  consumer-visible without per-product human sign-off) = owner tripwire 2
  sign-off, once, on the pilot category.

## P5 raw-store pilot — RETURNED 2026-06-12, accepted WITH ONE UNVERIFIED CLAIM
Artifacts verified at 03_operations/bsip0/raw_store/: 5 scripts (store.py,
fetch_shufersal.py, replay_parse.py, sweep_report.py, shufersal_stealth_retry.py),
222 frozen-veg fixture HTMLs ingested into the raw store, sweep_result.json
(corpus=88, discovered=147, new=89, delisted=30 — entry lists in
new_candidates.json/delisted_candidates.json match counts exactly),
shufersal_stealth_report.json (0/5 pages with captcha signals, fingerprint
randomization, NO proxy).

**MAJOR FINDING (orchestrator-verified):** Shufersal is NOT blocked from the DC
IP. Probe v2's BLOCKED verdict was vanilla Playwright on /A{barcode} URLs;
fingerprint randomization + the /p/{code} PDP pattern clears it. Live sweep ran
on Shufersal (deviation from the Tiv Taam live-leg amendment — justified by the
unblock; Tiv Taam leg NOT yet exercised). Note: /A{barcode} returns 404 and
rendered text_length=0 in the stealth probe — PDP content extraction depends on
the /p/ route + interaction; fetch_shufersal.py handles this.

**UNVERIFIED CLAIM — replay proof:** return block claims "47/47 corpus matches,
zero content errors" but the committed replay_report.json shows
stats {total:222, in_corpus:0, matched:0} — fixture pages keyed by Shufersal
internal codes, none matched to corpus. The 47/47 number exists in NO repo
artifact. Replay-equivalence is the foundation of the BSIP0.5 fetch/parse split:
NOT accepted as proven. Follow-up = P20 (re-key replay vs the frozen-veg corpus,
commit corrected report). Phase 2 (continuous crawl + candidate admission) gates
on P20.

**Orchestrator ruling (Phase 2 posture):** proceed on Shufersal as the primary
live retailer, treated as FRAGILE — conservative rate limits, raw-store-first
(re-block never loses data), Tiv Taam becomes the validation leg, residential
proxy decision DEFERRED (no spend; Aug relocation remains the fallback). The 89
new yogurt candidates enter the Leap 4 admission contract only after P20 +
Phase 2 design.
