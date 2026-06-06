# BSIP0 Retailer Coverage Standard — v1

**Effective:** 2026-06-06
**Owner:** Data Agent
**Status:** ACTIVE

## Rule

Every BSIP0 category scrape **must target at least 4 Israeli retailers**. A single-retailer or 2-retailer baseline is insufficient — it misses brand diversity, regional stocking differences, and demographic variation across chains.

## Target Retailer Set (Israel, 2026)

| Retailer | Status | Scrape Pattern |
|---|---|---|
| שופרסל (Shufersal) | ✅ Active | Server-rendered HTML; direct category URLs |
| יוחננוף (Yochananof) | ✅ Active | MUI React; Playwright headless; cookie popup `[data-aria-desc="dialog_cookies_accept"]` → force-remove `.MuiBackdrop-root` |
| קרפור (Carrefour) | 🔧 In Progress | AngularJS (`ng-app="ZuZ"`); JS-rendered; needs longer wait (5–10s) after page load before extraction |
| רמי לוי (Rami-Levi) | ⚠️ Blocked | Nuxt.js; all API endpoints 404; confirmed blocked for cereals (TASK-184) and olive oil (2026-06-06) |

## Coverage Gate

A category is **not scrape-complete** until:
1. Shufersal — scraped
2. Yochananof — scraped
3. Carrefour — attempted and either scraped or documented as blocked with reason
4. Rami-Levi — attempted and either scraped or documented as blocked with reason

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
