# Homepage layout — owner reference v5

**Source file:** `c:\Users\HP\Downloads\bari_homepage_v5_layout_fix.html`  
**Status:** Layout authority (visuals are embedded PNG mocks; production swaps in real assets)

## Core principle (from file comment)

> No CSS-drawn product packaging. Product visuals are **image assets**.  
> In production: replace embedded mock crops with real transparent pack shots from Bari corpus / approved library.

The page is **not** built from individually positioned HTML product tiles. The hero and comparison blocks are **single composed images** inside styled shells.

---

## Hero layout (critical fix)

| Rule | v5 spec |
|------|---------|
| Page | `dir=rtl` globally |
| Hero grid | **`direction: ltr`** on `.hero` to lock physical columns |
| Columns | `grid-template-areas: "visual copy"` |
| Physical layout | **Visual LEFT** · **Copy RIGHT** (Hebrew copy column still `direction: rtl`) |
| Column ratio | `minmax(540px, 1.05fr)` visual · `minmax(420px, 0.95fr)` copy |
| Gap / height | `gap: 72px`, `min-height: 650px`, `padding: 62px 0 48px` |
| Mobile | Stack **copy first**, then visual |

### Hero visual shell (`.hero-visual`)

- Large rounded card (`border-radius: 38px`), white/cream gradient fill, soft shadow
- Green glow blob top-right inside card (`::before`)
- **One `<img class="hero-stage-img">` fills the card** — not 5 separate packs in CSS
- Optional `stage-note` pill bottom-left (prototype only)

### Hero copy (`.hero-copy`)

- Eyebrow: **ניתוח מוצרים · המדף הישראלי**
- H1: very large (`clamp(48px, 6.5vw, 82px)`), heavy weight
  - Line 1: האריזה מספרת סיפור.
  - Line 2 (green): בארי בודקת את / הרכיבים. (line break inside green span)
- Subline: ~22px, max-width ~620px
- CTA: full-width search button ~390×70px, gradient green, heavy shadow
- Secondary: סריקת ברקוד בקרוב (muted, below button)

---

## Comparisons section

| Rule | v5 spec |
|------|---------|
| Section head | **Centered** (not split row with blog links) |
| Label | ניתוחי קטגוריה · מוצרים אמיתיים |
| Title | השוואות מהמוצרים שאתם צורכים ביום יום |
| Subtitle | לא כל מה שנראה דומה — באמת דומה. |
| Card | `.comparison-shell` — white rounded frame, padding, soft shadow |
| Content | **One full-width comparison image** inside shell — not HTML grid columns |

The duel layout (story | A | VS | B | bullets) should match the **comparison PNG** as one editorial panel.

---

## Page atmosphere

- Background: dual radial gradients (sage green top-left, warm cream bottom-right) on `#f7f7f2`
- Tokens: `--green: #087a51`, larger radius (`32–38px`), deeper shadows

---

## Gap vs current `bari-web` pass 3

| Area | Current build | v5 target |
|------|---------------|-----------|
| Hero columns | RTL `grid-cols-2` (can flip) | **LTR grid** locked visual-left / copy-right |
| Hero visual | 5 CSS-positioned pack images + UI chips | **Single stage image** (or one React canvas that renders like one photo) |
| Hero eyebrow | Missing | Add ניתוח מוצרים · המדף הישראלי |
| Typography | Smaller | Scale up h1, subline, CTA per v5 |
| Comparison | HTML editorial grid | **One cohesive card** matching comparison mock (image or pixel-faithful React) |
| Section header | Left-aligned + side links | **Centered** title block |

---

## Implementation path (recommended)

1. **Layout pass:** Fix hero grid (LTR areas), typography, centered comparison header — no asset change.
2. **Asset pass:** Export hero-stage PNG + comparison PNG from owner mocks OR compose in code to match mocks, using **real Shufersal pack URLs** only.
3. **Wire real data** into comparison panel (scores, bullets) while keeping v5 visual structure.

Do **not** ship another CSS collage of floating PNGs.
