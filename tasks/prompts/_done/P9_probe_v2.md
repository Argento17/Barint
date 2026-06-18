# P9 → Data Agent (cheap model)

```
TASK-255 — Probe v2: render-based retailer access verification from the Bari VM,
using the repo's REAL endpoints (probe v1 was naive and its verdicts are not
trusted).

CONTEXT: Repo C:\Bari. A scrape-runner VM is live at 45.93.95.32 (Ubuntu 24.04).
You can run commands on it directly from this machine:
  ssh root@45.93.95.32 "<command>"        (key auth, no password needed)
  scp <localfile> root@45.93.95.32:/opt/bari/   (upload)
Python on the VM: ALWAYS /opt/bari/venv/bin/python3 (never plain python3);
Playwright browsers: prefix commands with
PLAYWRIGHT_BROWSERS_PATH=/opt/bari/playwright-browsers
Probe v1 results: /opt/bari/logs/probe_all.txt (read it first). Key v1 errors to
fix: Shufersal product-URL pattern 404'd; Yohananof hostname had an SSL CN
mismatch (try without www / find the real storefront host); Osher Ad search
paths 404'd; barcode extraction grabbed the same widget barcode on every page.

DO:
1. Mine the REAL endpoints from the repo's working scrapers — these scraped
   successfully in June 2026: 03_operations/bsip0/scrape/shufersal_yogurt/,
   yohananof_milk (Playwright pattern), carrefour_butter, victory, and
   multiretailer_cereals. Extract: actual listing/search/product URL formats,
   headers/session bootstrap, and selectors each one uses.
2. Write probe_v2.py: for each of the 9 retailers (Shufersal, Yohananof,
   Victory, Carrefour IL, Rami Levy, Tiv Taam, Machsaney Hashuk, Hazi Hinam,
   Osher Ad): use the repo-mined endpoint where one exists, else the corrected
   guess; fetch via requests first, AND render via headless Playwright when the
   response is a JS shell (<10KB) or has anti-bot markers. Per retailer collect:
   final HTTP status, rendered DOM size, whether ≥3 DISTINCT product barcodes
   are extractable from one listing, whether a product page shows
   nutrition/ingredients content, screenshot saved to /opt/bari/logs/shots/,
   and an honest verdict: CLEAN / JS_OK (works with Playwright) / CAPTCHA_GATED
   / WRONG_ENDPOINT (needs storefront recon) / BLOCKED. For Shufersal
   specifically: determine whether the captcha marker is an ACTIVE challenge
   (rendered page shows challenge) or dormant script (content renders fine).
3. Run it on the VM (upload via scp, execute via ssh, modest delays ≥1.5s,
   ≤8 pages per retailer). Pull back /opt/bari/logs/probe_v2.txt and 2-3
   representative screenshots per problematic retailer to
   C:\Bari\03_operations\bsip0\scrape_runner\probe_v2_results\.
4. Update the rollout map table with the honest verdicts.

RULES: read-only against the repo scrapers (mine, don't modify); no Open Food
Facts (hard ban); no proxies (we are testing whether the DC IP suffices); stay
polite per site (~8 pages max, delays). Do not scrape beyond the probe scope.

RETURN BLOCK: per-retailer honest verdict table with evidence (DOM size,
distinct barcodes found, nutrition visible Y/N, screenshot path); Shufersal
captcha answer (active vs dormant); Yohananof correct hostname; which retailers
are Phase-1-ready TODAY. Propose RETURNED.
```
