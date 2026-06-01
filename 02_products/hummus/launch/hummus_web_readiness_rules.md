# Hummus Web Readiness Rules — v1

**Task:** TASK-085
**Owner:** Product Agent
**Date:** 2026-05-31
**Status:** DRAFT — gates Hummus v1 go-live (DEC-002)
**Applies to:** `hummus_frontend_v1.json` (run_hummus_002, authoritative) → `/hashvaot/hummus`
**Parent contract:** `01_framework/editorial/bsip2_to_web_translation_contract_v1.md`
**Co-sign required:** Nutrition Agent (fact-check) + QA Agent (verdict) per `ownership_matrix_v2.md`

---

## 0. Purpose

This document applies the BSIP2→Web Translation Contract to the hummus corpus. It defines, per product type, how a scored record becomes web copy, and the per-product acceptance criteria a record must pass to ship on the hummus comparison page.

Corpus reference (run_hummus_002): 69 analysed → ranked set of prepared spreads after the chickpea boundary is applied; product types `hummus_spread` (44), `matbucha` (11), `eggplant_spread` (7), `pepper_spread` (5), `masabacha` (2).

---

## 1. Boundary Application (this corpus)

Per parent contract §1, applied to the 69 records:

| Group | Products | Destination |
|---|---|---|
| Prepared hummus spreads | hummus_spread (excl. raw chickpeas) | **Ranked comparison** |
| Masabacha | 2 (whole chickpeas in tahini/sauce base) | **Ranked comparison** — a prepared dip, NOT raw material |
| Matbucha / Turkish / pepper / eggplant spreads | 23 | **Ranked comparison** |
| Single-ingredient raw / frozen chickpeas (NOVA-1, 85–86/A) | 6 (Batch 1) | **Informational section** — "גרגירי חומוס — חומר גלם, לא ממרח מוכן" |
| Canned branded whole chickpeas | 2 (Batch 2: הקיסר, יכין) | **Informational section** — ingredient text was marketing copy, not a verified list |
| Whole chickpeas, no nutrition panel | 2 (Batch 4) | Stay **unavailable** (already suppressed) |

> After the boundary, the **#1 ranked product is a real prepared spread (סלט חומוס, 80.2/A)** — not a bag of chickpeas. Grade-A among ranked spreads correctly drops to ~1–2: very few *prepared* hummus reach A. That is a more truthful distribution, not a worse one (`hummus_boundary_review.md §5`).

The 8 chickpea products in the informational section render with **no rank, no grade badge, no score-vs-score ordering**.

---

## 2. Type-Specific Translation Rules

Each row gives the dominant Section-1 (`positiveSignals` / `insightLine`) and Section-2 (`limitingFactors`) patterns. Section-3 (`unknowns`) is in §3.

### 2.1 Hummus spreads

- **`positiveSignals`:** the chickpea-to-tahini balance, from declared percentages — "X% גרגירי חומוס ו-Y% טחינה גולמית"; short clean list when `additive_count` ≤ 1.
- **`limitingFactors`:** the additive load and kind — single preservative → "תוספת בודדת על בסיס פשוט"; preservative + acidity regulator → "מספר תוספות מעבר לבסיס"; stabilizers/modified starch → "מבנה רכיבים מורכב יותר מממרח פשוט".
- High-tahini and restaurant-style: surface the declared tahini share as the differentiating fact.

### 2.2 Matbucha

- **`positiveSignals`:** the vegetable base — "X% עגבניות ו-Y% פלפל — בסיס ירקות **מבושל**".
- **`limitingFactors`:** added sugar is the dominant limiter where present — "סוכר מצוין ברשימת הרכיבים — תוספת סוכר על בסיס ירקות".
- **Hard rule:** matbucha is **מבושל** (stewed), never **קלוי** (roasted) — TASK-064 B-6.

### 2.3 Eggplant spreads

- **`positiveSignals`:** "חציל קלוי כרכיב מרכזי, עם שמן ותבלינים" (eggplant *is* roasted/chargrilled — קלוי is correct here, unlike matbucha).
- **`limitingFactors`:** oil + multiple additives; modified starch where present ("44% חציל… עם מייצבים, עמילן מעובד ומשמר").

### 2.4 Tahini-heavy spreads

- A spread that is **sold and eaten as a spread** stays in this category even with a high tahini share; surface the declared tahini % as a `positiveSignal`.
- A product that is a **ready-to-eat tahini *dip*** routes to the **Tahini category** (`whole_food_fat`), not here — TASK-026 locked decision. Do not pull tahini dips into the hummus ranked set.

### 2.5 Unavailable products

- `confidence = insufficient` → `score = null`, `grade = null`.
- Render the explicit no-score state (`score_presentation_v1 §5`): "לא נוקד" + the `unavailable` caveat: "לא ניתן להציג ציון למוצר זה בשל היעדר נתוני תזונה מלאים ממקור המידע."
- **Never** a blank cell, `—`, or `N/A`. The two Batch-4 products are the live cases.

### 2.6 Caveated products

When `display_state = "caveated"`, the matching string from `caveated_product_messages` goes in `caveats[]` (in addition to `unknowns[]`):

| Caveat | When |
|---|---|
| `structural_emptiness` | partial-data score (e.g. the two D-grade matbucha `bsip1_7290111563492`, `bsip1_7290106577572`) — "ציון מבוסס על נתונים חלקיים" |
| `low_nova_confidence` | no ingredient list, processing assessed from nutrition only |
| `category_routing_imprecise` | shown as a spread but classification not unambiguous from the name |

For these, Section-3 carries the caveat string; do not also assert a confident processing limiter you cannot support.

---

## 3. Mandatory `unknowns[]` for this category

- **Fat (always, 94% of corpus):** "ערכי השומן לא היו זמינים במקור הנתונים — מדד זה לא נכלל בניתוח." — verbatim, on every scored product. Mirrors the methodology footer Line 3 (HUM-001 / KL-1). Must not be paraphrased.
- **Ingredient list absent (Batch 3, e.g. `bsip1_1990261`, `bsip1_3643714`):** "פירוט הרכיבים המלא לא אומת ממקור הנתונים."
- **Canned chickpea marketing copy (Batch 2):** "פירוט הרכיבים המלא לא אומת — לא ניתן לאשר נוכחות או היעדר חומר משמר." — and **never** repeat the unverified "ללא חומר משמר" claim (TASK-064 R-2).

---

## 4. Suppressed / Prohibited (this corpus)

- **Fat & saturated fat:** `null`, hidden row, panel still shown (DEC-001 Option B; TASK-080 ruling). Footer disclosure mandatory.
- **Sugar:** `null` (HUM-002, 0% coverage); not shown as "0".
- **Prohibited language:** NOVA / cap / floor / dimension / weight / BSIP; health words (בריא/נקי/מסוכן); recommendations (מומלץ/כדאי/עדיף); generic grade text ("פרופיל הרכב טוב ביחס לקטגוריה"); taste/price/brand.

---

## 5. Acceptance Criteria — per product

A hummus product is **web-ready** only if **all** hold. QA verifies each as a gate; any fail blocks the product (and, if it is a structural failure, blocks launch per DEC-002).

| # | Criterion | Check |
|---|---|---|
| 1 | **Correct boundary** | Product is in the ranked set only if it is a prepared spread; raw/canned/frozen chickpeas are in the informational section, not ranked |
| 2 | **Product-specific `insightLine`** | Not a per-grade band sentence; names *this* product's base/composition; ≤80 chars; unique enough that two different products do not share it verbatim by grade |
| 3 | **At least one signal** | `positiveSignals[]` OR `limitingFactors[]` is non-empty (scored products) |
| 4 | **Unknowns shown when data missing** | `unknowns[]` includes the fat line; includes ingredient/sugar gaps where they apply |
| 5 | **Fat suppressed** | `nutrition.fat = null`, `nutrition.saturated_fat = null`; no fat row rendered; footer disclosure present |
| 6 | **No prohibited health language** | No health claim, recommendation, or framework vocabulary in any copy field |
| 7 | **Expansion answers "why this score?"** | The detail block, from `positiveSignals` + `limitingFactors` + `unknowns`/`caveats`, lets the reader reconstruct why this product landed where it did — the "I could have noticed that" test (`explainability_v1 §1.1`) |
| 8 | **No-score products explicit** | `confidence = insufficient` → "לא נוקד" + `unavailable` caveat; never blank/`—`/`N/A` |

### 5.1 Worked checks (live products)

- **`bsip1_6666307` · סלט חומוס · 80.2/A** — ✅ ranked (prepared spread); insight names short clean list; `limitingFactors` = single preservative; `unknowns` = fat. Web-ready, becomes #1.
- **`bsip1_7290104061417` · חומוס עם טחינה אחלה · 63.5/C** — ✅ insight "56% חומוס, 17% טחינה"; `limitingFactors` = "מייצבים וחומר משמר — מבנה רכיבים מורכב"; the lower chickpea share + multi-agent list make the C visible.
- **`bsip1_7290010931330` · סלט מטבוחה · 61.8/C** — ✅ base "63% עגבניות… בסיס ירקות **מבושל**"; limiter "סוכר לבן מצוין ברשימה"; `מבושל` not `קלוי`.
- **`bsip1_7290018359686` · הקיסר חומוס ענק · 80.4/A** — ⛔ NOT ranked → informational section; `unknowns` = list unverified; no "ללא חומר משמר".
- **`bsip1_7296073733317`** — no panel → "לא נוקד" + `unavailable` caveat.

---

## 6. Handoff

| Area | Change | Owner |
|---|---|---|
| `hummus_frontend_v1.json` | Add `positiveSignals[]`, `limitingFactors[]`, `unknowns[]`, `caveats[]`; tag chickpeas `ranked:false`; recompute ranked-set `grade_distribution` | Data Agent |
| Per-product Hebrew strings | Author per §2–§3 from this contract | Content Agent (Nutrition co-sign) |
| Hummus page | Render expansion sections; informational section; exclude chickpeas from sort/filter | Frontend Agent |
| Methodology | Note raw chickpeas shown separately and unranked | Content Agent |
| Verdict | Verify §5 criteria per product; ranked top is a prepared spread; no orphaned counts | QA Agent |
| DEC-002 | Go-live after QA clears W-1 against these rules | Product Agent |

---

*Hummus Web Readiness Rules v1 — TASK-085 — Product Agent — 2026-05-31*
*Parent: `bsip2_to_web_translation_contract_v1.md`. Gates DEC-002 (Hummus v1 go-live).*
