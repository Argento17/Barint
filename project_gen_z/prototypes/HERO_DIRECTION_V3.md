# Hero direction v3 — owner verdict (2026-06-29)

## Keep

| Element | Verdict |
|---------|---------|
| Front vs Inside card | **Keep** — core hook |
| Bottom carousel | **Keep** — duels/spotlights = scroll + tap |

## Correct now

### 1. Front vs Inside — harsher signal

- Inside panel: strong visual alarm **before** user reads text
- Prototype uses: red border, warning icon, high-contrast badge
- Owner asked for "Lie Detected" tag
- **Governance note:** Agent block list rejects "Lie of the Week" / accusatory lie framing. Prototype shows two badge options:
  - **A (Bari-safe):** "פער שזוהה" — gap detected, analytical
  - **B (owner override):** "Lie Detected" / שקר שזוהה — requires explicit owner unlock of Bundle B copy rules

### 2. Layout — break the grid

- Drop symmetric 50/50 columns
- Front/Inside card **overlaps** headline block (offset, rotation ~-2deg, z-index)
- Feels less corporate portal, more editorial/disruptive
- Still RTL-safe and mobile-stacked

### 3. Primary CTA — utility not reading

Owner requirement: **Scan Barcode** or **Search a Product** — immediate utility.

| Phase | CTA | Route / behavior |
|-------|-----|------------------|
| **Phase 1 (now)** | חפשו מוצר / בחרו מוצר | Category shelf flow (P1-07) or product search if built |
| **Phase 2** | סרקו ברקוד | `/scan` + camera API — not in Phase 1 scope |

**Prototype v3:** Primary button = scan icon + "חפשו מוצר" with chip "סריקה בקרוב" until barcode ships.
Alternative if owner insists: primary = scan label now, disabled state with "בקרוב".

Secondary CTA: methodology or browse categories.

## Wireframe

`prototypes/mocks/hero-wireframe-v3.html`

## Supersedes

v2 symmetric layout — archived, not deleted.
