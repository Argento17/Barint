# P5 → Data Agent (cheap model) — READY TO SEND (amended after P9 results)

**P9 AMENDMENT (overrides anything contrary below):** Shufersal is CAPTCHA-GATED
from the VM's DC IP — do NOT attempt Shufersal live fetching beyond step 5 below.
The LIVE leg of this pilot pivots to **Tiv Taam** (114 cards, 15 barcodes, F5
bypassed with vanilla Playwright) with **Hazi Hinam** as fallback (46 barcodes,
widest open). Read C:\Bari\03_operations\bsip0\scrape_runner\probe_v2_rollout_map.md
first — it has the working endpoints per retailer. The REPLAY leg stays on
Shufersal fixtures (the 222 persisted frozen-veg pages) as written. Add step 5:
a bounded Shufersal stealth retry — Playwright with crawlee-style fingerprint
randomization (NO proxies), max 5 pages; report whether the captcha clears.
Report-only; if it fails, Shufersal continuous crawl waits for a residential-proxy
decision (owner) or the owner's relocation to Israel (~Aug 2026).

```
TASK-255 Phase 1 — BSIP0.5 pilot: raw-store fetcher + replay proof + listing sweep
(Shufersal yogurts). Recon context: 01_framework/operations/task255_scrape_recon_v1.md.
Probe v2 results (read first): C:\Bari\03_operations\bsip0\scrape_runner\probe_v2_results\

ARCHITECTURE (fixed by orchestrator — implement, don't redesign):
Fetch/parse split. A scrape session ONLY fetches and persists raw evidence; all
extraction runs offline against the store, replayable without any network access.

THE VM: 45.93.95.32 — run fetches THERE (ssh root@45.93.95.32 "<cmd>", scp for
upload; python = /opt/bari/venv/bin/python3 always; store root on VM =
/opt/bari/raw_store). Build the code in the repo; deploy to VM for live runs.

BUILD under 03_operations/bsip0/raw_store/:
1. store.py — raw store: pages saved as
   raw_store/<retailer>/<category>/<barcode-or-pageid>/<fetch_ts>.html plus a
   manifest.jsonl per category: {url, retailer, category, barcode_hint, fetch_ts,
   content_sha256, http_status, bytes, fetch_engine}. content_sha256 = hash of the
   raw bytes — this IS the Leap 4 change-detection substrate. Helper:
   latest(barcode), changed_since_last_fetch(barcode) -> bool.
2. fetch_shufersal.py — ONE Shufersal fetcher (reuse the existing shufersal
   scraper's request/session logic — find it under
   03_operations/bsip0/scrape/shufersal_yogurt/, and use the endpoints probe v2
   validated): given a listing config {category, listing_urls[]}, it
   (a) enumerates listing pages -> product URLs + barcodes, (b) fetches each
   product page, (c) persists to the raw store. NO parsing in this script beyond
   what enumeration needs. Categories are config entries, not code.
3. replay_parse.py — offline extraction: run the EXISTING yogurt parser logic
   against stored raw pages (no network) producing BSIP0-shaped output. Prove
   replay: for products already in the BSIP1 run_yogurt_006 corpus where raw can
   be fetched this session, parsed-from-store output must match the corpus fields
   (report match/mismatch per field — mismatches are findings, do not fix).
4. sweep_report.py — listing sweep diff: barcodes discovered on Shufersal yogurt
   listings vs barcodes in the run_yogurt_006 BSIP1 corpus -> new_candidates.json
   (NEW products for the TASK-255 admission pipeline) + delisted_candidates.json
   (in corpus, no longer listed). REPORT ONLY — nothing is added to any corpus.

RULES: Direct storefront scrape only — no Open Food Facts (banned, client
hard-fails), no il_prices panels (identity/price discovery only), no other source.
Do not modify existing scrapers, corpora, BSIP1+, or the engine. Modest delays
(≥1.5s), polite volume. If probe v2 says Shufersal is captcha-gated, build
everything + unit-test store/replay on the 222 persisted shufersal_frozen_
vegetables HTML pages as fixtures and mark live-fetch BLOCKED(captcha) in return.

RETURN BLOCK: files created; raw store layout sample; replay match/mismatch table;
sweep counts (corpus n / listed n / new / delisted); whether the live fetch ran on
the VM; blockers. Propose RETURNED or BLOCKED.
```

---
**After you paste this to the agent:** open `tasks\DISPATCH_BOARD.md` and put an `x` in the P5 line under 📬 Signals (`- [ ]` becomes `- [x]`). That is how the orchestrator knows it's in flight.
