# BSIP0 Retailer Coverage Standard — v1

**Effective:** 2026-06-06
**Owner:** Data Agent
**Status:** ACTIVE

## Rule

Every BSIP0 category scrape **must target at least 4 Israeli retailers**. A single-retailer or 2-retailer baseline is insufficient — it misses brand diversity, regional stocking differences, and demographic variation across chains.

## Target Retailer Set (Israel, 2026)

| Retailer | Status | Scrape Pattern |
|---|---|---|
| יוחננוף (Yochananof) | ✅ PRIMARY | MUI React SaaS; local Playwright (headless=False); cookie popup `[data-aria-desc="dialog_cookies_accept"]`; product modal tabs "ערכים תזונתיים" / "רכיבים"; barcodes in CDN image paths |
| ויקטורי (Victory) | 🔧 SECONDARY | Same SaaS as Yohananof (CDN retailer ID 1470); adapter at `03_operations/bsip0/scrape/victory/01_acquire_victory.py`; Playwright port of Yohananof — needs first live category run to confirm modal/tab pattern |
| שופרסל (Shufersal) | ⚠️ BLOCKED | TLS fingerprint fake-200; il_prices identity feed is LIVE; storefront needs playwright-stealth + residential proxy |
| קרפור (Carrefour) | ⚠️ BLOCKED | F5 BIG-IP WAF HTTP 403; il_prices identity feed is LIVE |
| רמי לוי (Rami-Levi) | ⚠️ BLOCKED | Cloudflare Bot Management HTTP 403; no il_prices chain_id confirmed yet |
| טיב טעם (Tiv Taam) | 🔍 INVESTIGATE | F5 BIG-IP WAF HTTP 403; il_prices chain_id not confirmed; needs stealth Playwright probe |
| מחסני השוק (mck.co.il) | 🔍 INVESTIGATE | F5 BIG-IP WAF HTTP 403 (same class as Tiv Taam); full e-commerce catalog confirmed in Google index; needs stealth Playwright probe |

## Coverage Gate

A category is **not scrape-complete** until:
1. Yochananof — scraped (PRIMARY, local Playwright)
2. Victory — scraped or documented as blocked with reason (SECONDARY, same Playwright adapter)
3. Shufersal — attempted and documented (BLOCKED until stealth proxy in place)
4. At least one of: Carrefour / Tiv Taam / Machsaney HaShuk — attempted and documented

**Scraping stack (default — no Firecrawl in production):**
- Identity: `il_prices` feeds (laibcatalog for Yohananof/Victory/Carrefour; self-hosted for Shufersal)
- Panel (SPA retailers): local Playwright — open product modal, click nutrition/ingredients tabs
- Panel (SSR retailers, when unblocked): `requests` + `BeautifulSoup` — direct HTML parse
- Panel (enrichment): OFF API — supplement where Playwright modal is empty (imported goods)
- Firecrawl: diagnostic and access probes only, never production scrape path

Blocked = documented, not skipped. The gap must appear in the category README and in any article that draws conclusions from the data.

## Why This Standard Exists

The olive oil scrape (2026-06-06) revealed that Shufersal and Yochananof carry almost entirely different brand universes:
- **שופרסל**: BORGES, MATTEO, FERNANDO, נריה (primarily imported — Spain, Italy)
- **יוחננוף**: יד מרדכי, סבא חביב, ג'השאן, זיתא (primarily Israeli producers)

A Shufersal-only scrape would have characterized the Israeli olive oil market as import-dominated — the opposite of what Yochananof's shelf shows. This brand-universe split likely generalizes across categories.

## Blocked Retailer Protocol

When a retailer cannot be scraped:
1. Document the blocking mechanism (auth-wall, JS-render timeout, API 404, CAPTCHA)
2. Record in the category `README` under `## Retailer Coverage`
3. Note the gap in any consumer-facing article or comparison
4. Retry on the next category refresh with an updated Playwright strategy
5. Do NOT suppress the gap from editorial conclusions

## History

- **2026-06-06**: Standard established. User directive: "the next scrape on FOUR different retailers — i want that in our framework." Triggered by olive oil article exposing the Shufersal-only blind spot. Olive oil article updated to reflect 2-retailer data as the current state; Carrefour and Rami-Levi documented as pending.
- **2026-06-07**: Retailer set updated after live probe. Victory elevated to SECONDARY (same SaaS as Yohananof — Playwright adapter written). Tiv Taam and mck.co.il added as INVESTIGATE (F5 WAF, need stealth Playwright). Scraping stack updated to Playwright-first; Firecrawl demoted to diagnostics-only. Standard moved from Shufersal-centric to Yohananof-primary.
