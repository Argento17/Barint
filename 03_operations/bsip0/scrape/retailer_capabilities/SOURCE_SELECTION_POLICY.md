# BSIP0 Source-Selection Policy — try ALL retailers, never default to one

**Owner ruling 2026-06-20.** Acquisition must **not** default to a single retailer (the snacks corpus was built only from yochananof, which turned out to publish physically-impossible nutrition panels AND is unreachable from our scrape environments — a single-source dead end). Every BSIP0 acquisition **attempts all four Israeli retailers** below, uses whichever are reachable, and **cross-checks nutrition across sources** for plausibility.

## The four retailers — try in this priority order
1. **Shufersal** — `https://www.shufersal.co.il` · primary. Public search endpoint returns structured product data without login:
   `GET https://www.shufersal.co.il/online/he/search/results?q=<urlencoded-hebrew-term>%3Arelevance&limit=N`
   Existing working scrapers: `03_operations/bsip0/scrape/shufersal_hummus/`, `shufersal_cereals/`, `shufersal_cheese/`, `shufersal_maadanim/`.
2. **Victory** — `https://www.victoryonline.co.il` · secondary / cross-check. Scrapers: `03_operations/bsip0/scrape/victory/01_acquire_victory.py`, `02_products/juices/scrape_juices_victory.py`.
3. **Yochananof** — `https://www.yochananof.co.il` (modal nutrition). Scraper pattern: `02_products/hard_cheeses/scrape_cheeses_yohananof.py`.
4. **Rami-Levy** — `https://www.ramilevi.co.il` + price-transparency portal. See `rami_levy.yaml`.

## Reachability is per-environment — TEST it each run, do not assume
Reachability depends on where the scraper runs (this sandbox vs the owner's machine vs an Israeli VM). **Always probe before a full run.** As measured **2026-06-20 from the Claude Code sandbox**:

| Retailer | From sandbox (2026-06-20) | Note |
|---|---|---|
| **Shufersal** | ✅ reachable via `requests` | home 200; search API 200 (~87 KB structured) |
| **Victory** | ✅ reachable | home 200 |
| Yochananof | ❌ blocked | `www` TLS `ERR_CERT_COMMON_NAME_INVALID`; `api` HTTP 403 bot-block — fails even with sandbox off. **May work from an Israeli IP / owner machine — still attempt it.** |
| Rami-Levy | ❌ blocked | connection refused / DNS (consistent with `rami_levy.yaml` DEFERRED) |

Probe snippet (requests works in-sandbox; Playwright may hit cert issues on some hosts — prefer the requests/API path):
```python
import requests
UA={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"}
requests.get(url, timeout=20, headers=UA)  # check status_code + body size
```

## Rules
- **Attempt all four**, in the order above. Use every reachable one; skip the blocked ones for that run and record which were blocked.
- **Cross-check nutrition:** when a barcode is found at ≥2 retailers, compare panels. Prefer the value that passes the per-100g plausibility gate; if they materially disagree, flag it. Cross-source agreement = higher confidence.
- **Plausibility gate is mandatory** on every panel regardless of source: reject `accounted_mass = carbs+fat+protein+fiber < 70 g/100g` (dry foods), reject `sugars_g==0` against a sugar-bearing ingredient, reject implausibly-low kcal; convert from per-serving if a serving size exists, else quarantine. (Built under TASK-360.)
- **OFF stays banned** — multi-retailer means *Israeli retailers only*, never Open Food Facts, any field, ever.
- If **all four are unreachable** for a category, STOP and report — never fabricate or carry forward stale/implausible numbers.

Related: per-retailer capability files in this dir (`rami_levy.yaml`, `carrefour.yaml`, …). Memory: `scrape_source_selection_policy`.
