# 1 — Voice Sources (Tom / Bari Hebrew)

Provenance catalogue for the Tom-Bari voice system. Every source is ranked by how
much weight it carries when distilling the fingerprint. **Gold** = imitate the
structure and rhythm directly. **Directional** = use for instincts/tone, not as a
template. **Research-only** = ambient context, never copied.

> Firewall reminder: sources here teach **voice**, never facts. No nutrition,
> ingredient, or score value enters copy from this catalogue — facts come only from
> the product's own data, and any health claim needs Nutrition Agent sign-off
> (see `5_banned_phrases_and_claims.md`).

---

## S1 — Milk page: "what helps / what limits" lists  · **GOLD (structure)**
- Path: `bari-web/src/lib/comparisons/milk-product-insights.ts`
- What to take: the **`positives[]` and `cautions[]` lists** and the `comparisonContext` + `takeaway` one-liners. These are the gold standard for how Bari frames a single product's benefit/limit balance: short, concrete, one idea per bullet, no moralizing.
- What to **reject**: the `whatMatters` descriptive sentence. Owner ruling (2026-06-18): *"the description of the product in the current version is BAD."* Do not imitate that line. The fingerprint rebuilds the opening from a real supermarket situation instead (see `2_voice_fingerprint.md`).
- Representative gold bullets:
  - `"רשימת רכיבים קצרה: חלב בלבד"` · `"חלבון טבעי סביר ל־100 מ״ל"`
  - `"המים הם הרכיב הראשון — אחוז שקדים נמוך בפועל"`
  - `"חלבון זניח — אינו תחליף לחלבון מהמדף"`
  - takeaway pattern: `"משקה קל — לא מקור חלבון."` (claim → sharp limit, em-dash pivot)

## S2 — Tom's cake intros + cake product notes  · **GOLD (voice)**
- The Friday-hosting intro, the home-made-contrast intro, the red-label intro, and the per-cake reviews (מוס בלגי, שמרים, פרווה, שיש, תפוזים, קרם, מאפין אישי, "טעם שוקולד").
- Carries: the situation-first opening, the perception→evidence pivot, the "שורת בארי" closer, the "it's not that you can't eat it" stance.
- Stored verbatim as raw material in `6_dummy_reviews.md`.

## S3 — Tom's cereal feedback notes  · **GOLD (voice)**
- The morning-rush intro, clean-but-flat intro, kids intro, and the per-cereal reviews (ויטביקס, פצפוצי אורז, קורנפלקס ללא גלוטן, ליון, נסקוויק, סיני מיניס).
- Carries: the **balanced mode** ("נקי לא תמיד אומר חזק"), the kids framing ("ילד לא אוכל אריזה, הוא אוכל את מה שיש בקערה"), the "קינוח בתחפושת" move.

## S4 — Existing Bari shelf copy Tom heavily edited  · **DIRECTIONAL**
- Live category copy where Tom rewrote drafts (milk lists above; future: cakes/cereals once shipped).
- Use to confirm the fingerprint against real published lines, not to invent new structure.

## S5 — Future Tom edits  · **GROWING (the real engine)**
- Every time Tom edits a draft, the diff is captured as a before/after pair in `8_edit_feedback_log.md` and, once it shows a repeatable move, promoted into `2_voice_fingerprint.md` / `3_before_after_pairs.md`.
- This is the strongest signal of voice and the only source that compounds over time. Treat it as highest-weight as it accumulates.

## S6 — Israeli food blogs & consumer writing  · **RESEARCH-ONLY**  → see `9_israeli_food_blog_research.md`
- Hebrew food/nutrition writing across four strands: recipe/lifestyle blogs (idiom), dietitian blogs (the **anti-voice** — prescriptive), consumer-investigative journalism (**the model** — TheMarker), and label/reference guides.
- Use **only** to calibrate natural Hebrew register, idiom, and what a real Israeli shopper recognizes. **Never** copy phrasing, claims, or numbers. Israeli product DBs (Foodiepedia) are **not** a data source. Any factual claim sourced here is fabrication risk and is banned.
- **Comprehensive first pass done 2026-06-18** (full write-up + sources in file 9). Decisive finding: credible Israeli food writing wins by *discriminating* (TheMarker's "סירופ תירס נשמע בריאותי, אבל…", comparative harm-reduction, methodology-first) and loses trust by *scaring* (ynet's "ניסוי על מיליארדים", risk claims). Tom's voice = the discriminating register, externally validated.
- Provenance: each reference logged inline per the citations discipline (file 9 §5).

---

## Weighting (when sources disagree)
1. **S5 Tom edits** (most recent, most specific to Tom) →
2. **S2/S3 Tom intros & notes** →
3. **S1 milk gold lists** (structure for benefit/limit bullets) →
4. **S4 edited shelf copy** →
5. **S6 blogs** (register calibration only).

If a fingerprint rule can't be traced to S1–S5, it is a guess and must be marked as such until a Tom edit confirms it.
