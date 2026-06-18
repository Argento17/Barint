# Probe v2: Rollout Map

Run: 2026-06-12 07:42 UTC | VM: 45.93.95.32 (Kamatera Tel Aviv, Ubuntu 24.04, 1 vCPU 2GB)
Script: `probe_v2.py` (9 retailers, ~5 min full run, 14 screenshots)

## Verdicts

| Retailer | Verdict | Static HTTP | REST API | Playwright | Barcodes | Phase |
|----------|---------|-------------|----------|------------|----------|-------|
| Hazi Hinam | **JS_OK** | OK (JS shell) | N/A | OK | 46 ✓ | **1A** |
| Victory | **JS_OK** | OK (JS shell) | blocked | OK | 6 ✓ | **1A** |
| Carrefour | **JS_OK** | OK (JS shell) | blocked | OK | 7 ✓ | **1A** |
| Tiv Taam | **JS_OK** | OK (JS shell) | N/A | OK | 15 ✓ | **1A** |
| Yohananof | **DEGRADED** | OK (JS shell) | N/A | degraded | NO | **1B** |
| Machsaney Hashuk | **DEGRADED** | OK (JS shell) | N/A | captcha | 9 | **2** |
| Rami Levy | **DEGRADED** | OK (static) | 404 | CF challenge | 1 | **2** |
| Osher Ad | **DEGRADED** | OK (homepage) | N/A | CF challenge | NO | **2** |
| Shufersal | **BLOCKED** | captcha | 404 | captcha | NO | **3** |

## Phase 1A (JS_OK — Playwright works)

### Hazi Hinam (`shop.hazi-hinam.co.il`)
- **WIDEST OPEN.** No WAF, no anti-bot. Angular SPA loads via Playwright.
- Homepage: 1,195 product cards, 46 barcodes extracted
- Dairy catalog: 799 product cards, 40 barcodes
- Category URL: `/catalog/{id}/{slug}`
- Search: client-side only (Angular routing)
- **Playwright config:** `locale="he-IL"`, `timezone_id="Asia/Jerusalem"`, dismiss popups via `button:has-text("סגור")`
- Screenshots confirm rich product grid with prices visible.
- **Rollout: ready for Playwright-based scrape.**

### Victory (`www.victoryonline.co.il`)
- Same SaaS platform as Yohananof but resolves better from Israeli DC.
- Playwright: 169 product cards, 6 barcodes (`7290001594568`, etc.)
- `/category?search={q}` works for search
- REST API endpoints (`/api/products`, `/v2/retailers/1470/...`) return 200 but no valid JSON (JS shells returned).
- **Rollout: use Playwright only. REST APIs do not work.**

### Carrefour (`www.carrefour.co.il`)
- F5 BIG-IP WAF blocks static HTTP (1.8KB JS shell).
- Playwright bypasses the WAF — 94 cards, 7 barcodes.
- `/product/{barcode}` and `/search?q={q}` both render via Playwright.
- REST API endpoints same pattern: return JS shell, not JSON.
- **Rollout: Playwright works. Need to handle cookie consent popups.**

### Tiv Taam (`www.tivtaam.co.il`)
- F5 WAF bypassed by Playwright — 114 cards, 15 barcodes.
- `/category/{slug}` or `/?s={q}` search pattern.
- **Newly unblocked** (v1 had F5 block). Israeli IP + Playwright is sufficient.
- **Rollout: Playwright works.**

## Phase 1B (DEGRADED — needs investigation)

### Yohananof (`yochananof.co.il`)
- Two hostname variants tested:
  - `www.yohananof.co.il` — **DNS does not resolve** (NXDOMAIN from Israeli DC)
  - `yochananof.co.il` (scraper legacy) — resolves, page title "יוחננוף - סופר שוק", HTTP 200
- BUT: only 14 "product cards" detected, 395 chars of rendered text, NO barcodes.
- The SPA loads the shell but product data does not render via vanilla Playwright.
- The working scraper does additional interaction (scrolling, clicking into product cards, waiting for modals).
- **Not blocked — just needs better Playwright interaction patterns.** The scraper code at `03_operations/bsip0/scrape/yohananof/` should be consulted for the correct interaction sequence.

## Phase 2 (DEGRADED/BLOCKED — needs advanced stealth)

### Machsaney Hashuk (`www.mck.co.il`)
- Static: 2KB JS shell (F5 WAF)
- Playwright: loads with **captcha**. 73 cards and 9 barcodes were still extracted despite captcha.
- The F5 WAF allows partial content through. May work with longer delays or headful mode.

### Rami Levy (`www.rami-levy.co.il`)
- Static: 100KB HTML loads (no anti-bot) but **no product data** — search page shell only.
- Playwright: Cloudflare challenge triggers (access_denied, cf_challenge). 1 barcode found in page boilerplate.
- API endpoint `/api/catalog/search?store=331` returns 404.
- **Cloudflare Bot Management (paid tier) — requires residential proxy.**

### Osher Ad (`www.osherad.co.il`)
- Homepage loads via static HTTP (44KB, static HTML).
- Search (`/search?q=`) returns 404 (search path wrong).
- Playwright: Cloudflare challenge on both pages. No barcodes.
- **Needs correct search URL discovery + residential proxy for Cloudflare.**

## Phase 3 (BLOCKED — proxy/stealth mandatory)

### Shufersal (`www.shufersal.co.il`)
- **All methods blocked.** Static HTTP returns captcha (754KB). Playwright also shows captcha (3.7KB rendered text, 93 product cards but no real product data).
- Vanilla Playwright fingerprint not enough — the scraper uses `crawlee.crawlers.PlaywrightCrawler` + `DefaultFingerprintGenerator` with Chrome fingerprints.
- Product URL `/A{barcode}` returns 404 (SPA routing — needs JS execution with proper state).
- OCC API and v2 API both return 404 or captcha responses.
- **Requires crawlee with DefaultFingerprintGenerator or residential proxy.**

## Summary

```
               Static    API     PW   Barcodes  Verdict  Phase
Hazi Hinam       OK      N/A     OK    46 ✓     JS_OK    1A
Victory          OK     blocked  OK     6 ✓     JS_OK    1A
Carrefour        OK     blocked  OK     7 ✓     JS_OK    1A
Tiv Taam         OK      N/A     OK    15 ✓     JS_OK    1A
Yohananof        OK      N/A   deg      NO     DEGRADED 1B
Machsaney H.     OK      N/A   cap      9 ✓    DEGRADED 2
Rami Levy        OK     blocked CF      1       DEGRADED 2
Osher Ad         OK      N/A    CF      NO      DEGRADED 2
Shufersal       cap      404    cap     NO      BLOCKED  3
```

**4 retailers JS_OK → Phase 1 ready for Playwright-based scrape.**
**4 retailers DEGRADED → 1 needs investigation (Yohananof), 3 need proxies.**
**1 retailer BLOCKED → Shufersal needs crawlee + residential proxy.**

## Files

- `probe_v2.py` — the probe script (on VM at `/opt/bari/probe_v2.py`)
- `probe_v2_results.json` — full structured results (VM: `/opt/bari/probe_v2_output/`)
- Screenshots (14 PNGs, VM: `/opt/bari/probe_v2_output/screenshots/`)
