# SEO Brief — יוגורט Blog Article
**Task:** TASK-201
**URL slug:** `/blog/yogurt`
**Published:** יוני 2026
**Author:** Content Agent

---

## Page Metadata

| Field | Value | Char count |
|---|---|---|
| `title` | `19 יוגורטים. שתי רשתות. מה שמניע את הציונים. \| Bari` | 55 |
| `description` | `סרקנו 19 יוגורטים משופרסל ויוחננוף. יוגורט לבן פשוט הגיע ל-A. יוגורט 0% שומן בטעם תות — C. מה באמת מבדיל בין הגביעים.` | 118 |
| `openGraph.type` | `article` | — |

Both values are within limits (title ≤60, description ≤155).

---

## Keyword Strategy

### Primary keyword
`יוגורט בריא` — high consumer intent, informational query. Captures the user who is scanning the yogurt shelf and wants to know what "healthy yogurt" actually means. Naturally embedded in article prose without forced insertion.

### Secondary keywords

| Keyword | Intent | Placement |
|---|---|---|
| `יוגורט 0 שומן` | Informational — debunking | Finding card 2, lead para 2 |
| `יוגורט לבן מול ממותק` | Comparison | Matrix section heading, finding card 1 |
| `יוגורט עם חלבון` | Product/feature | Science section, finding card 5 |
| `יוגורט תרביות חיות` | Informational | Science section, buying guide signal 1 |
| `יוגורט יווני` | Category | Finding card 4, score chart cluster label |
| `יוגורט השוואה` | Navigation | CTA inline link to `/hashvaot/yogurt` |

---

## Internal Links

| Link text | Target | Location |
|---|---|---|
| "לדף השוואת יוגורטים" | `/hashvaot/yogurt` | CTA aside after buying guide |
| "לכל השוואות היוגורט" | `/hashvaot/yogurt` | Conclusion CTA button |
| "כל ניתוחי המדף" | `/hashvaot` | Footer |
| "חזרה לבלוג" | `/blog` | Hero + footer |
| "13 מוצרי שמן זית..." | `/blog/shemen-zayit` | Recent articles card |
| "מה באמת קורה במדף החלב?" | `/blog/milk-analysis` | Recent articles card |

---

## Corpus scope declaration

- **Retailers in corpus:** שופרסל (11 products) + יוחננוף (8 products) = 19 total
- **All quantitative claims (19 מוצרים, 56 נקודות פער, 7 דרגת A)** are traceable to `yogurts_frontend_v3.json`
- **No retailer outside the corpus** appears in data claims. יוחננוף is named accurately as a second source.
- **Score range cited:** 40/D (יוגורט קראנצ תות קורנפלקס) → 89/A (יופלה GO מועשר בחלבון) for Shufersal-verified products. 96/A for Yohananof partial-confidence product named accurately as partial.

---

## Structural SEO notes

- H1 (article title) contains primary finding — not generic category name
- H2s name specific editorial findings (not "מה מצאנו" only — each finding card has its own declarative H3)
- Score chart uses semantic `<ul>/<li>` — accessible and crawlable
- Comparison matrix uses `<table>` with proper `<thead>/<tbody>` — crawlable
- All external citation links have `rel="noopener noreferrer"` — no PR leakage
- Internal comparison page CTA uses standard `<Link>` — full Next.js prefetch

---

## Forbidden terms audit (pre-publish gate)

Terms checked and confirmed absent from all consumer-facing copy:

- [ ] BSIP, BSIP2 — absent
- [ ] NOVA, nova_proxy — absent
- [ ] cap, floor, penalty, weight — absent
- [ ] dimension, structural_class — absent
- [ ] "בריא יותר" / "מומלץ" — absent
- [ ] Raw score mechanics (e.g. "78.7 נקודות") — absent; scores shown as `81/A` format only
- [ ] Alarmist language — absent

---

*Yogurt SEO Brief v1 — Content Agent — TASK-201 — 2026-06-07*
