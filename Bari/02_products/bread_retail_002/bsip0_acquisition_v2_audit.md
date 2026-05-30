# BSIP0 Acquisition Audit v2

**Run:** `real_bread_retail_002_v2_20260525T165557` | **Date:** 2026-05-25 | **Method:** Playwright browser automation

This audit documents all browser-based retailer access attempts and the BSIP0 acceptance gate result.
No products are added to the corpus until the gate passes.

---

## 1. Gate Result

**Status: PASSED ✓**

Products collected: 110 (gate: ≥20)
Nutrition coverage: 76% (gate: ≥70%)
Ingredient coverage: 76% (gate: ≥40%)
Retailers: shufersal

**Proceed to BSIP1/BSIP2 pipeline.**

---

## 2. Retailer Access Summary (v2 — Browser Automation)

| Retailer | Access Method | Status | Blocker | Products | Manual Action? |
|:---------|:-------------|:-------|:--------|:---------|:--------------|
| שופרסל | http_static | accessible | OK | 110 | No |
| ויקטורי | playwright_browser | blocked | BLOCKED (JS) — AngularJS SPA, browser rendered but no products | 0 | No |
| קרפור ישראל | playwright_browser | partial | PARTIAL — requires authentication/session cookie | 0 | YES — see report |
| וולט מרקט | playwright_browser | partial | PARTIAL — requires authentication/session cookie | 0 | YES — see report |

---

## 3. Retailer-by-Retailer Findings

### שופרסל

**Status:** OK
**Products extracted:** 110

**Probe log:**
- Maintenance check passed — searching for bread/cracker products
- Search 'לחם' → 20 items, 20 new unique food products
- Search 'קרקר' → 20 items, 20 new unique food products
- Search 'כוסמין' → 20 items, 18 new unique food products
- Search 'שיפון' → 20 items, 16 new unique food products
- Search 'פיתה' → 20 items, 17 new unique food products
- Search 'לחמניה' → 20 items, 19 new unique food products
- Total unique products to fetch: 110
- Product pages fetched: 110 OK, 0 failed
- Coverage: 83/110 nutrition, 83/110 ingredients

### ויקטורי

**Status:** BLOCKED (JS) — AngularJS SPA, browser rendered but no products
**Products extracted:** 0
**Blocker detail:** Angular SPA did not render product content

**Probe log:**
- Angular NOT detected — page may not be AngularJS or failed to render
- https://www.victory.co.il/category/%D7%9C%D7%97%D7%9D → no product cards found
- https://www.victory.co.il/category/%D7%A7%D7%A8%D7%A7%D7%A8%D7%99%D7%9D → no product cards found
- https://www.victory.co.il/search?q=%D7%9C%D7%97%D7%9D → no product cards found
- https://www.victory.co.il/search?q=%D7%A7%D7%A8%D7%A7%D7%A8 → no product cards found

**Screenshots:**
- `C:\Bari\03_operations\bsip0\acquisition_v2\screenshots\failure_states\victory_homepage_loaded_20260525T170039.png`
- `C:\Bari\03_operations\bsip0\acquisition_v2\screenshots\failure_states\victory_no_cards__D7_9C_D7_97_D7_9D_20260525T170120.png`
- `C:\Bari\03_operations\bsip0\acquisition_v2\screenshots\failure_states\victory_no_cards__D7_A7_D7_A8_D7_A7_D_20260525T170200.png`
- `C:\Bari\03_operations\bsip0\acquisition_v2\screenshots\failure_states\victory_no_cards_search_q=_D7_9C_D7_9_20260525T170240.png`
- `C:\Bari\03_operations\bsip0\acquisition_v2\screenshots\failure_states\victory_no_cards_search_q=_D7_A7_D7_A_20260525T170320.png`

### קרפור ישראל

**Status:** PARTIAL — requires authentication/session cookie
**Products extracted:** 0
**Blocker detail:** Login wall detected on Carrefour homepage
**MANUAL ACTION REQUIRED:** Carrefour requires login to browse products. Manual step: open a browser, log in to carrefour.co.il, then export the session cookies so the probe can reuse them. Alternatively: browse to a product category manually and document the URL structure.

**Probe log:**
- Homepage loaded: קרפור Online

**Screenshots:**
- `C:\Bari\03_operations\bsip0\acquisition_v2\screenshots\failure_states\carrefour_homepage_loaded_20260525T170329.png`
- `C:\Bari\03_operations\bsip0\acquisition_v2\screenshots\failure_states\carrefour_login_wall_20260525T170330.png`

### וולט מרקט

**Status:** PARTIAL — requires authentication/session cookie
**Products extracted:** 0
**Blocker detail:** Wolt requires login to view product catalog
**MANUAL ACTION REQUIRED:** Wolt shows a login prompt. To unlock: 1) Log in to wolt.com in a regular browser, 2) Export cookies from the wolt.com domain, 3) Import them into the sessions/wolt_market/ directory. Do NOT provide Wolt account credentials here.

**Screenshots:**
- `C:\Bari\03_operations\bsip0\acquisition_v2\screenshots\failure_states\wolt_market_auth_wall_20260525T170335.png`

---

## 4. Products Extracted

Total: 110

| # | Name | Retailer | Nutrition | Ingredients | Source URL |
|:--|:-----|:---------|:----------|:------------|:-----------|
| 1 | 10 פיתות כוסמין | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 2 | קרקר קרם קרקר | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 3 | מארז פיתות כוסמין | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 4 | מארז לחמניות כוסמין | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 5 | לחם מחמצת כוסמין | שופרסל | ✗ | ✗ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 6 | לחם מחמצת צרפתי פרוס | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 7 | פיתות ג'וניור כוסמין לבן | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 8 | לחמניות קלות כוסמין | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 9 | לחם מחמצת שיפון | שופרסל | ✗ | ✗ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 10 | קרקר כוסמין מלא ושומשום | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 11 | לחם אקסקלוסיבי שיפון מלא | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 12 | לחם מחמצת עגבניות | שופרסל | ✗ | ✗ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 13 | לחם מחמצת אגוזים פרוס | שופרסל | ✗ | ✗ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 14 | לחם מחמצת צרפתי | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 15 | לחם מחמצת שיפון פרוס | שופרסל | ✗ | ✗ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 16 | קרקר טופז מלח הדר | שופרסל | ✗ | ✗ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 17 | מארז שבלול עם צימוקים | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 18 | קרקר כוסמין טבעי | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 19 | קרקר טופז שומשום | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 20 | מארז פיתות אסליות | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 21 | קמח שיפון מלא | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 22 | לחם שיפון מלא פרוס | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 23 | מקלות כוסמין | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 24 | כוסמין מלא 100% | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 25 | קרקר דק כפרי פיטנס | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 26 | פיתות 100% כוסמין מלא | שופרסל | ✗ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 27 | לחם E-FREE מקמח חיטה | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 28 | לחם מחמצת אגוזים צימוקים | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 29 | מארז פיתות בסגנון תימני | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 30 | קרקר דק פיטנס זיתים | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 31 | קרקר דק כפרי | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 32 | מארז פיתות ביס | שופרסל | ✗ | ✗ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 33 | קרקר דק פיטנס סלק | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 34 | קרקר פריך עם קמח שיפון | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 35 | לחמניות אצבע ג'וניור | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 36 | מארז לחמניות קשר | שופרסל | ✗ | ✗ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 37 | לחם מחמצת דגנים | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 38 | מארז לחמניות המבורגר | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 39 | לחם מחמצת אגוזים | שופרסל | ✗ | ✗ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 40 | לחם מחמצת צרפתי | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 41 | לחם שיפון עגול | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 42 | לחמניות לס קיטו | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 43 | מארז פיתות קמח מלא | שופרסל | ✗ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 44 | לחמית שיפון אסם | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 45 | טורטיה כוסמין | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 46 | לחמניות קלות קמח מלא | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 47 | 12 פיתות ביס | שופרסל | ✓ | ✗ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 48 | מיני פיתות כוסמין מלא | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 49 | מארז לחמניות חלה | שופרסל | ✗ | ✗ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 50 | מארז פיתות אסליות | שופרסל | ✗ | ✗ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 51 | קרקר כוסמין דק כפרי | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 52 | מארז לחמניות אצבע | שופרסל | ✗ | ✗ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 53 | לחם שיפון קל | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 54 | לחם מחמצת דגנים | שופרסל | ✗ | ✗ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 55 | קרקר פריך ירקות אורגני | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 56 | לחם מחמצת זיתי קלמטה | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 57 | מארז פיתות אסליות | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 58 | לחם מחמצת אגוזים | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 59 | מארז לחמניות כפריות | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 60 | קרקר פריך בסגנון שוודי | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 61 | לחם מחמצת כוסמין פרוס | שופרסל | ✗ | ✗ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 62 | מארז לחמניות ביס | שופרסל | ✗ | ✗ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 63 | לחם מחמצת עגבניות פרוס | שופרסל | ✗ | ✗ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 64 | קרם קרקר | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 65 | לחם שיפון 100%פרוס | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 66 | לחם כוסמין | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 67 | פיתות אסליות מארז | שופרסל | ✗ | ✗ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 68 | מארז לחמניות חלה מתוקה | שופרסל | ✗ | ✗ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 69 | לחם מחמצת שיפון+אגוזים | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 70 | מארז פיתות כוסמין | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 71 | קרקר כוסמין דק רוזמרין | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 72 | לחמניות כוסמין במתיקות | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 73 | לחם מחמצת דגנים פרוס | שופרסל | ✗ | ✗ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 74 | קרקר כוסמין סלק | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 75 | לחם הארץ שיפון אגוזים | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 76 | פיתות במרקם מיוחד | שופרסל | ✓ | ✗ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 77 | פיתות ביס 100% כוסמין | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 78 | 10 פיתות מחמצת | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 79 | לחם קמח מלא 100% | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 80 | פיתה פיתה | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 81 | מארז לחמניות קלות | שופרסל | ✗ | ✗ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 82 | 10 פיתות כוסמין | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 83 | לחמניות פשתן טרי | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 84 | קרקר דק פיטנס בטטה | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 85 | לחם מחמצת אגוזים+צימוקים | שופרסל | ✗ | ✗ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 86 | קרקר שומשום אסם | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 87 | קרקר מרובע מלוח | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 88 | לחם מחמצת שיפון | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 89 | קרקר דק רוזמרין פיטנס | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 90 | לחם שיפון גרעינים | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 91 | לחם שיפון כהה | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 92 | פיתות קלות כוסמין | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 93 | קרקר | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 94 | קרקר זהב אסם | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 95 | קרקר חומוס מתובל | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 96 | לחם שיפון כפרי | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 97 | לחם מחמצת מכוסמין | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 98 | לחם E-FREE מקמח כוסמין | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 99 | מארז לחמניות חלה קלות | שופרסל | ✗ | ✗ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 100 | כוסמין מלא 100% | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 101 | פיתות אסליות | שופרסל | ✗ | ✗ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 102 | מארז לחמניות דגנים | שופרסל | ✗ | ✗ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 103 | לחם מחמצת שיפון | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 104 | קרקר כוסמין אורגני | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 105 | קרקר דגנים ללת"ס | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 106 | לחמניות מחמצת טבעית | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 107 | פיתות כוסמין קלות | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 108 | לחמניות המבורגר | שופרסל | ✗ | ✗ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 109 | קרקר דק רוזמרין | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |
| 110 | פיתות כוסמין מלא | שופרסל | ✓ | ✓ | https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%… |

---

## 5. API Endpoints Discovered

No XHR/API calls captured.

---

## 6. Manual Actions Required

### קרפור ישראל
Carrefour requires login to browse products. Manual step: open a browser, log in to carrefour.co.il, then export the session cookies so the probe can reuse them. Alternatively: browse to a product category manually and document the URL structure.

### וולט מרקט
Wolt shows a login prompt. To unlock: 1) Log in to wolt.com in a regular browser, 2) Export cookies from the wolt.com domain, 3) Import them into the sessions/wolt_market/ directory. Do NOT provide Wolt account credentials here.


---

## 7. Recommended Next Steps

**Accessible (1):** שופרסל
→ Proceed with these retailers to BSIP1.
**Partial (2):** קרפור ישראל, וולט מרקט
→ Requires session cookies or manual login to unlock product catalog.
**Blocked (1):** ויקטורי
→ Need direct API credentials, proxy rotation, or partnership.

*Generated by acquisition_audit_v2.py — 2026-05-25T16:55:57.575292*