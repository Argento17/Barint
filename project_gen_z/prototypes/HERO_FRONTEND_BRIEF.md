# P1-01 Hero — Frontend implementation brief

**Status:** Owner-approved copy + visual direction. Ready for Frontend Agent when implementation opens.  
**North star image:** `prototypes/mocks/reference/hero-north-star-v3.png` (owner screenshot — adapt, do not pixel-copy)  
**Codebase:** `bari-web/` only — adapt to existing tokens, components, RTL patterns.

---

## Rule for the implementing agent

Adapt the north-star **mood and structure** to the real Bari codebase. Do **not** rebuild pixel-perfect from the screenshot. Reuse `HomeHero`, `HomeComparisons`, carousel schema, comparison tokens, cream/green palette.

---

## Hero — replace current `home-hero.tsx`

### Copy (locked — owner)

| Slot | Hebrew |
|------|--------|
| Headline line 1 | האריזה מספרת סיפור. |
| Headline line 2 | בארי בודקת את הרכיבים. |
| Subline | חפשו מוצר מהסופר וקבלו תשובה פשוטה: מה טוב, מה בעייתי, ומה בעיקר שיווק. |
| Primary CTA | חפשו מוצר |
| Secondary CTA | סריקת ברקוד בקרוב |

- Primary CTA: single action — **חפשו מוצר** only (no barcode text inside the button).
- Secondary: separate text link below — **סריקת ברקוד בקרוב** (disabled / coming soon until Phase 2 scan).
- Primary href (Phase 1): `/hashvaot` or product-search flow when built.

### Visual — north star qualities

- Light Bari palette (cream/white + green accents — not dark, not neon).
- **Polished grocery still-life** on one side: cereal/granola, yogurt, milk/plant milk, olive oil, protein bar.
- **Subtle Bari analysis UI overlays** on the composition:
  - Score badge (e.g. circular or chip — use real score only if tied to a real corpus product).
  - Small radar or dimension card (decorative / illustrative in hero — not a second scoring engine).
  - Ingredient-quality chip (e.g. עיבוד מינימלי style — illustrative OK in hero).
- Large Hebrew headline, premium rounded cards, clean non-scientific feel.
- **No** "פער שיווקי" badge or lie-detected framing in hero.

### Hero imagery — data rules (HARD)

| Context | Rule |
|---------|------|
| Hero still-life | **Generic illustrated or realistic packs** — not invented branded scores. Blurred/abstract OK if legal concern. |
| Comparison cards | **Real Bari corpus** — scrape image URLs, real scores, real names only. |
| Production | Generic hero products + real data in comparison module only. |

**Never invent** product names, barcodes, scores, or nutrition for live UI.

---

## Comparison section — replace current carousel header + featured module

### Section title (replace "ראש בראש מהמדף")

**Title:** השוואות מהמוצרים שאתם צורכים ביום יום  
**Subtitle:** לא כל מה שנראה דומה — באמת דומה.

### Featured comparison card (one pilot)

Build **one** featured duel card above or beside the existing carousel (carousel P1-02 stays — do not remove live cards).

| Field | Spec |
|-------|------|
| Category | דגני בוקר |
| Title | מי באמת פחות מתוק? |
| Layout | Two product panels, VS circle center, score badges |
| Scores | Example layout 52 vs 81 — **must use real corpus scores when live** |
| Body | Short consumer takeaway from signed copy or insightLine |
| CTA | לצפייה בהשוואה → `/hashvaot/breakfast-cereals` |

**Pilot data (real):** e.g. נסקוויק vs קוקומן from `cereals_frontend_v2.json` — verify scores at implementation time; do not hardcode 52/81 unless they match corpus.

### Winner/loser framing

- **No** red loser / green winner moral labels.
- Scores may differ visually (grade colors OK per existing Bari grade palette) but copy stays category-relative, not "מנצח/מפסיד".

---

## Files to touch (when implementing)

| Area | Path |
|------|------|
| Hero | `bari-web/src/components/home/home-hero.tsx` |
| Hero copy | new JSON or extend `home/content.ts` — Content gate before owner-facing if copy changes |
| Comparisons | `home-comparisons.tsx`, `homepage-carousel-data.ts` (header strings only unless adding featured card component) |
| New component | `featured-comparison-card.tsx` (suggested) |

---

## Gates before production

1. Owner copy above is approved for structure; Content + Red Team sign-off still required per `content/CONTENT_GATES.md` if any wording changes.
2. Hero generic art vs real packs — owner prefers generic in hero, real in comparisons.
3. Build on `/dev/project-genz` or feature branch first; no scoring changes.

---

## Supersedes

- `hero-wireframe-v4.html` tilted card + פער שיווקי — **deprecated** for hero direction.
- Gemini winner/loser duel specs — **rejected**.
