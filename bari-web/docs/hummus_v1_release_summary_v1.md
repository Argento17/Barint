# Hummus v1 — Final Release Summary

**Decision:** DEC-002
**Status:** **APPROVED — GO_LIVE_APPROVED**
**Decision date:** 2026-05-31
**Owner:** Head of Product
**Recorded by:** Command Center
**Production route:** `/hashvaot/hummus`
**Category:** חומוס וממרחים — Hummus & Savory Spreads
**Authoritative corpus:** `src/data/comparisons/hummus_frontend_v3.json` (`run_hummus_002`, v3 explanation layer)

---

## 1. Decision

Hummus v1 is **approved for go-live**.

The decision is grounded in the TASK-090 Final QA Verdict (`READY_FOR_DEC002`), independently re-validated by Command Center against the live data path (corpus → exclusion layer → rendered components). All five acceptance dimensions pass. **No blockers. No required fixes.**

---

## 2. Acceptance evidence (validated)

| Dimension | Requirement | Result |
|-----------|-------------|--------|
| Display — count | 59 products shown | ✅ 69 corpus − 10 excluded = 59 |
| Display — scored | 59 scored, 0 unscored | ✅ all `score != null` |
| Display — grade A | 1 product grade A | ✅ A=1 (B=27, C=27, D=4) |
| Display — chickpea | 0 canned/raw chickpea | ✅ 6 NOVA-1 + 2 canned-whole excluded |
| Display — unavailable | 0 "score unavailable" | ✅ 2 insufficient-data products excluded |
| Ranking — #1 | genuine prepared spread | ✅ "סלט חומוס", 80, grade A, `hummus_spread` |
| Ranking — purity | no non-spread anywhere | ✅ all 59 are spreads (hummus 34 / matbucha 11 / eggplant 7 / pepper 5 / masabacha 2) |
| Ranking — order | sorted by Bari score | ✅ corpus pre-sorted desc; exclusion preserves order |
| Explanation | useful signals/factors/unknowns/caveats | ✅ 0 empty expansions; product-specific; removed per-grade boilerplate confirmed absent |
| Explanation — caveats | present where relevant | ✅ caveats on exactly the 6 partial-confidence products, none on the 53 verified |
| Copy/stats | visible stats match rendered set | ✅ hero stats derived live (59/59/1); "37-point gap" = 80−43 |
| Build/regression | build passes, no category breaks | ✅ `next build` clean; 30/30 static pages; all sibling categories intact |

---

## 3. Launch-gating tasks — CLOSED

| Task | Scope | Status |
|------|-------|--------|
| TASK-086 | Remove per-grade boilerplate; product-specific insight + deterministic explanation arrays | CLOSED |
| TASK-087A | Category-boundary decision (non-spread chickpea products) | CLOSED |
| TASK-087B | Implement combined exclusion set (NOVA-1 + non-spread = 10 IDs) | CLOSED |
| TASK-087C | Hero/display counts derived from rendered products, not factory-audit metadata | CLOSED |
| TASK-089 | BSIP2 spread-subtype calibration assessment | CLOSED |
| TASK-090 | Final acceptance QA — verdict `READY_FOR_DEC002` | CLOSED |

---

## 4. Category state transition

**PRE_LAUNCH → LIVE.**

No code gate to flip: the category is already wired and shipping in source.

- Route `/hashvaot/hummus` builds and prerenders as static content.
- Registry entry present (`src/lib/comparisons/registry/categories/hummus.ts`, registered in `registry/index.ts`).
- Landing-page card live under "ניתוח עדכני" (`src/app/hashvaot/page.tsx` → `FeaturedHummusIntelligenceCard`).

LIVE state is hereby recorded operationally as of the DEC-002 approval date.

---

## 5. Scope of exclusions (for the record)

10 products removed from the ranked experience (rankings, table, count, grade tally, explanation layer). Audit record: `excluded_products_hummus_v1.md`; exclusion sets in `src/lib/comparisons/hummus-comparison-page-data.ts`.

- **6 × NOVA-1 whole/raw/frozen chickpea** — minimally processed but not comparable to prepared spreads.
- **2 × canned whole chickpea** — preserved whole chickpeas ("מבנה רכיבים מעובד — מעבר לממרח בסיסי"), not a spread.
- **2 × insufficient nutrition data** — rendered an empty "score unavailable" state.

The corpus on disk retains all 69 products; exclusion is applied at the display layer only.

---

## 6. Carry-forward notes (non-blocking)

Logged for post-launch maintenance — none gate go-live:

- **N1 — Hardcoded copy constants.** `hummusPrologueSentences` ("69"/"59") and `HUMMUS_INSIGHT_LINES` ("59", "37-point gap") are literals, not derived from `products` like the hero stats / `metadataLine`. Correct today; will drift if the corpus changes. Recommend deriving post-launch.
- **N2 — Stale comment.** `hummus-comparison-page.tsx:49` still labels insight lines a "category-level fallback... pending content integration." Cosmetic; rendered values are accurate.

---

## 7. Verdict

# GO_LIVE_APPROVED

Hummus v1 is approved and recorded LIVE at `/hashvaot/hummus`. DEC-002 closed APPROVED; launch-gating tasks closed; carry-forward notes N1–N2 handed to post-launch maintenance.
