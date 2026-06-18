# P6 → Frontend/Data Agent (cheap model) — READY TO SEND (amended after P9 results)

**P9 AMENDMENT:** the real hostname is **yochananof.co.il** (with 'c', NO www —
www.yohananof.co.il is NXDOMAIN from the Israeli DC). The page is an SPA that
renders only ~14 cards with no barcodes on naive load — the working interaction
patterns (click into results, wait for product modals) live in the existing
scraper at 03_operations/bsip0/scrape/yohananof/ — mine THAT for selectors and
waits, plus C:\Bari\03_operations\bsip0\scrape_runner\probe_v2_rollout_map.md.

```
TASK-255 Phase 4 (pulled forward) — Yohananof Playwright storefront scraper,
fetch-only, BSIP0.5-conformant.

CONTEXT: Repo C:\Bari. The old yohananof_yogurt acquisition
(03_operations/bsip0/scrape/yohananof_yogurt/01_acquire_yohananof_yogurt.py) used
the il_prices+OFF model. OFF is banned project-wide (TASK-238); that model is dead
and must NOT be copied. The working storefront pattern to follow is the
yohananof_milk Playwright scraper — locate it under 03_operations/bsip0/scrape/
(cite the path you used). IMPORTANT: probe v1 hit an SSL hostname mismatch on
www.yochananof.co.il — use the correct hostname from probe v2 results
(C:\Bari\03_operations\bsip0\scrape_runner\probe_v2_results\).

THE VM: 45.93.95.32 — live validation runs THERE (ssh root@45.93.95.32 "<cmd>";
python = /opt/bari/venv/bin/python3; browsers need
PLAYWRIGHT_BROWSERS_PATH=/opt/bari/playwright-browsers; store root on VM =
/opt/bari/raw_store).

BUILD: 03_operations/bsip0/raw_store/fetch_yohananof.py — a fetch-only Playwright
scraper conforming to the raw-store contract (store.py from P5 if merged; else
write to the same documented layout: raw_store/yohananof/<category>/<id>/<ts>.html
+ manifest.jsonl). Given a listing config {category, listing_urls[]}: enumerate
listing pages -> product URLs; fetch each product page; persist raw HTML +
full-page screenshot + manifest row. NO nutrition/ingredient parsing in this
script — extraction is offline, someone else's job. Pilot category config: yogurts.

RULES: storefront only; no OFF, no il_prices panels; respect the site (delays
≥2s, no parallel hammering); do not modify existing scrapers or corpora. If live
validation on the VM fails, validate selectors against any cached/sample pages in
the repo and mark live validation BLOCKED with the exact error.

RETURN BLOCK: file path; pattern source path you followed; correct hostname used;
selector strategy; whether a live run succeeded on the VM (counts: listings,
product pages persisted); blockers. Propose RETURNED or BLOCKED.
```

---
**After you paste this to the agent:** open `tasks\DISPATCH_BOARD.md` and put an `x` in the P6 line under 📬 Signals (`- [ ]` becomes `- [x]`). That is how the orchestrator knows it's in flight.
