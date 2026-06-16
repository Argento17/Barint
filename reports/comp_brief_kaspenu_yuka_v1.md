# Competitive-Intelligence Brief — Kaspenu & Yuka (P1)

**Prepared:** 2026-06-13 · **Priority:** P1 · **Status:** Governance/strategy brief — NOT consumer copy.
**Scope guardrails:** No scoring/methodology change is authorized by this document. Bari inherits **no data** from either competitor (OFF ban + no-inherit rule). Competitor scores (Nutri-Score/NOVA-derived) are **signal, never evidence** (Source Registry Rule 4).
**Registry action taken:** Kaspenu added as `il-033` (direct IL competitor) in `01_framework/operations/comp/source_registry_v1.yaml`. Yuka already present as `gl-001`.

---

## 1. Kaspenu (כספנו — "הסריקה החכמה")

The most direct competitor to Bari found to date: an **Israeli** barcode scanner that fuses a 0–100 health score **with** price transparency and healthier/cheaper alternatives, in Hebrew, on the same Israeli shelf Bari scores.

| Dimension | Finding (cited) |
|---|---|
| **App status** | Live and actively maintained on both App Store and Google Play. Free, no ads. [App Store IL] [Google Play] |
| **Launch / version history** | Launched **April 2025** [JPost]. App Store version history: v2.1.0 (25/04/2025, language selection) → v2.1.12 (08/07/2025, Hebrew) → v2.1.13 (12/07/2025) → **v2.1.16 (21/10/2025, "add donation buttons")** = current. Steady iteration over ~6 months. [App Store IL] |
| **Product count** | **~40,000 products in the database, of which 15,000–18,000 are live in the app.** [JPost; App Store description: "15,000+ products"] |
| **Data sources** | International scoring systems **Nutri-Score and NOVA**, **Israeli Health Ministry labeling**, and **user-submitted feedback**; price data from **Ministry of Economy** public price-transparency data (Price Transparency Law). [JPost] **No verified OFF dependency** in cited sources — but irrelevant to Bari, which inherits nothing regardless. |
| **Scoring claims** | A **health score out of 100** shown with a color-coded rating plus Nutri-Score, NOVA and additive detail. The score is **derived from Nutri-Score/NOVA**, not original analysis — same dependency Yuka has. [App Store description; JPost] |
| **Pricing / economic features** | Displays **average and lowest price across Israel without naming the store**; a **petition feature** lets users flag overpriced items — at enough signatures, petitions go to retailers and are published. This price+health fusion is Kaspenu's signature and a layer **Yuka does not have**. [JPost] |
| **Alternatives feature** | AI recommends **healthier *or* cheaper alternatives** when a product is scanned, across the 15,000+ live products. [JPost; App Store description] |
| **Hebrew UX** | Built for Israeli shoppers; Hebrew added v2.1.12; multilingual (he/en/fr — founder is a French immigrant). Hebrew-native consumer experience on Israeli shelves. [App Store IL; JPost] |
| **Nonprofit / independence** | Operates as a **nonprofit (amuta)**, **donor-funded** (founder cites "only one foundation – French"), founder and co-founder **take no salary**, **no ads, no commercial collaborations**. Independence is its sharpest positioning claim. [JPost; App Store description: "completely independent and non-profit, with no ads or commercial collaborations"] |
| **People** | Founder **Yaelle Ifrah** (French immigrant, ex-TV producer, culinary entrepreneur, parliamentary adviser); CTO **Jeremy Atia**. [JPost] |
| **Adoption evidence** | **Google Play: 10,000+ installs, 74 reviews, 4.0★. Apple: 34 ratings, 4.9★.** Press coverage in the Jerusalem Post. Founder's stated target: **200,000 users within 5 years** (i.e. not yet there). [Google Play; App Store IL; JPost] |

**Adoption read (evidence-based, per instruction):** Adoption is **early-stage but real and growing** — 10K+ Android installs ~14 months post-launch, active biweekly-to-monthly releases, national press, and a clear 5-year growth target. This is **not** a dormant project. It is **not** yet at scale. Threat is therefore driven by **strategic positioning and shelf coverage**, not by current raw user numbers (see §3).

---

## 2. Yuka

The global reference model for the barcode-scanner category and Kaspenu's blueprint.

| Dimension | Finding (cited) |
|---|---|
| **User scale** | **~80 million users across 14 countries** (founded France 2017); ~41M downloads, ~19k downloads/day trailing 30 days. [FoodNavigator 2026-02-09; app-store aggregators] |
| **Scoring methodology** | 0–100 score: **nutrition 60%** (Nutri-Score basis — positives for protein/fiber, penalties for calories/sugar/salt/sat-fat), **additives 30%** ("high-risk" flags), **organic 10%** bonus. [FoodNavigator; multiple methodology reviews] |
| **Reformulation impact** | Measurable industry effect: high-risk additives per product **down 13% since 2019** (France DB); **breakfast cereals −58%**, **pre-prepared meals −48%**; **>3/4 of French manufacturers** say Yuka scores influence formulation; Intermarché reformulated 900 products (142 additives removed, 2019); Walmart committed to removing artificial dyes + 30 additives by Jan 2027. [FoodNavigator] |
| **Transparency limits** | **Shuts manufacturers out** — Yuka declines all manufacturer requests for help improving scores; no paid pathway, but also **no manufacturer dialogue/appeal**. Pro-independence, but a closed black box to the makers it scores. [FoodNavigator] |
| **Criticism** | Methodology critiques: over-reliance on Nutri-Score **oversimplifies**; **never independently validated** the way Nutri-Score itself was; **hazard- not dose-based** additive flagging (flags presence regardless of amount, precautionary not toxicological); ignores the **additive "cocktail" effect** and hyperpalatability (Federica Amati, Imperial College London); beauty-industry insiders dispute its cosmetic ratings. [FoodNavigator; Beauty Independent; Glossy; dietitian reviews] |

---

## 3. Bari Threat Matrix

### 3a. Direct overlap (where they compete with Bari head-on)

| | Kaspenu | Yuka |
|---|---|---|
| Same core promise (decode a product → simple verdict) | ✅ **Direct** | ✅ Direct (category template) |
| **Israeli shelf, Hebrew** | ✅ **Direct — same market** | ❌ Not localized to IL |
| Health score 0–100 | ✅ | ✅ |
| Additive / UPF flagging | ✅ | ✅ |
| Healthier-alternative recommendations | ✅ | ✅ |
| **Price/economic layer** | ✅ **(unique vs Yuka)** | ❌ |
| Broad SKU coverage (15k–80k+) | ✅ 15–18k live | ✅ massive |

**Kaspenu is the sharper threat**: it occupies Bari's exact square — Israeli shelf, Hebrew, health verdict — and adds a **price dimension Bari does not have**, with **coverage breadth far beyond Bari's curated category pages**.

### 3b. Bari's unique advantage (what neither competitor has)

1. **Original, transparent scoring engine (BSIP).** Bari computes from a **direct product scrape** with an auditable trace; Kaspenu and Yuka both **resell Nutri-Score/NOVA** as their backbone. Bari can answer *"why this score"* at the trace level — they structurally cannot.
2. **Editorial interpretation, not just a number.** Bari ships a **human verdict per row** (standing → why → catch → grade) and category-level framing ("best ≠ excellent", category caveat). Yuka/Kaspenu give a number + tags; Bari gives **judgment**.
3. **Dose-aware, evidence-governed additive treatment.** Yuka's documented weakness is **hazard-based, presence-only** additive flagging that ignores dose and the cocktail effect. Bari's evidence-registry-governed approach is a **direct, defensible differentiator** — *if* Bari keeps additive scoring dose- and evidence-grounded (see counter-positioning).
4. **Curated, comparison-first depth.** Bari compares within a shelf with provenance (e.g. bread: 256 scanned → 31 curated). Scanners are single-product lookups; Bari is **shelf reasoning**.

### 3c. Bari's weak points (where competitors are ahead — honest)

1. **Coverage breadth.** Kaspenu live = 15k–18k SKUs; Yuka = millions. Bari = a handful of curated categories. A consumer scanning a random product is served by them, not Bari.
2. **The scan-in-store use case.** Both are **barcode scanners** answering an in-aisle question. Bari is a **web comparison destination** — different, slower-to-reach moment of need.
3. **Price.** Kaspenu answers "is this overpriced?" in the same tap. Bari is silent on price entirely.
4. **Independence narrative.** Kaspenu's **nonprofit, no-salary, donor-funded, no-ads** story is a clean, press-friendly trust claim. Bari needs an equally crisp independence/trust story.
5. **Distribution/virality.** Yuka's 80M and Kaspenu's app+petition mechanics are inherently shareable; Bari's distribution is unproven.

### 3d. Required Bari counter-positioning

1. **Lead with the engine, not the verdict alone.** Market Bari as the **only Israeli tool that scores from the actual product and shows its work** — explicitly contrast against "apps that just relabel Nutri-Score/NOVA." This is true of both competitors and is Bari's most durable wedge.
2. **Weaponize Yuka's documented additive flaw.** Position Bari's **dose- and evidence-aware** additive reasoning against presence-only fear flagging and the ignored cocktail effect. *Guardrail:* this only works if Nutrition keeps Bari's additive logic genuinely dose/evidence-grounded — do not drift into the same hazard-only trap. (Note: an additive-cocktail cluster proposal already exists in the framework docs — relevant to this wedge.)
3. **Own "judgment, not just a number."** Double down on the editorial row verdict + category caveat as the experience scanners can't replicate. This is already a Bari standard; make it the marketing spearhead.
4. **Decide deliberately on the two gaps Kaspenu exploits — coverage and price.** Both are **strategic** (target-user/scope) calls, not expert calls:
   - *Coverage:* curated-depth vs broad-scan is a real strategic fork. Recommend **staying curated-depth** and messaging it as a feature ("we don't score everything — we score what matters, properly"), not racing Kaspenu/Yuka on SKU count.
   - *Price:* whether Bari ever adds an economic layer is a scope decision for Product/owner. Flag, don't build.
5. **Build Bari's independence/trust story now.** Kaspenu has a cleaner one today. Bari needs an explicit, public statement of independence (no manufacturer pay-to-improve, no inherited third-party scores, transparent methodology) — turning Yuka's "black box to makers" criticism into Bari's "transparent to everyone" claim.

### 3e. Threat verdict

| Competitor | Threat level | Basis |
|---|---|---|
| **Kaspenu** | **MODERATE–HIGH (rising)** | Same market, same language, same core promise + a price layer Bari lacks + far broader coverage. Adoption still early (10k+ installs) so not an immediate share threat, but **strategically the most dangerous** — it is the Israeli incumbent for "scan → health + price verdict." Monitor adoption quarterly; re-rate up if installs/press accelerate. |
| **Yuka** | **MODERATE (indirect)** | Not localized to Israel, so not a direct share competitor today, but it is the **category template** (and a possible IL entrant) and the **benchmark consumers compare Bari against**. Its methodology weaknesses are Bari's clearest differentiation playbook. |

*Per instruction, neither is rated "low threat": Kaspenu's adoption and exact-square overlap, and Yuka's category-defining scale, both rule that out.*

---

## Sources

- [כספנו — App Store (IL)](https://apps.apple.com/il/app/%D7%9B%D7%A1%D7%A4%D7%A0%D7%95-%D7%94%D7%A1%D7%A8%D7%99%D7%A7%D7%94-%D7%94%D7%97%D7%9B%D7%9E%D7%94/id6740878730) — version history (v2.1.16, 21/10/2025), 34 ratings / 4.9★, description, "independent and non-profit, no ads."
- [כספנו — Google Play](https://play.google.com/store/apps/details?id=com.kaspenu2.mobile&hl=en_US) — 10K+ installs, 74 reviews, 4.0★, PEGI 3.
- [Kaspenu — official site / amuta](https://www.kaspenu.org/en/english) — nonprofit/association status.
- ["French immigrant's app brings food transparency to Israeli shoppers" — Jerusalem Post](https://www.jpost.com/israel-news/article-854169) — launch April 2025, founder Yaelle Ifrah + CTO Jeremy Atia, ~40k DB / 15–18k live, data sources, price + petition features, donor-funded/no-salary, 200k 5-yr target.
- ["Yuka drives reformulation but leaves brands in the dark" — FoodNavigator, 2026-02-09](https://www.foodnavigator.com/Article/2026/02/09/yuka-drives-reformulation-but-shuts-out-food-makers/) — 80M users/14 countries, 60/30/10 methodology, reformulation stats, manufacturer shut-out, Amati cocktail-effect critique.
- [Beauty Independent — Yuka rating veracity questioned](https://www.beautyindependent.com/yuka-beauty-industry-insiders-question-product-ratings/) — industry criticism.
- [Glossy — Yuka's growing cohort of critics](https://www.glossy.co/beauty/yuka-beauty-wellness-product-scanning-app/) — methodology/criticism.
