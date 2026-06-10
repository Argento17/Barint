# Fiber Functional Vocabulary Registry — Soluble / Viscous / Prebiotic-Active

**Document ID:** FFV-v1
**Date:** 2026-06-10
**Evidence registry:** EV-006 (Viscous vs Non-Viscous Soluble Fiber) — primary; touches EV-007 (intrinsic vs isolated), EV-019 (prebiotic gum exemption), EV-020 (resistant starch)
**Status:** Vocabulary registry — ungates EV-006 detection. **No scoring change in this document.**
**Owner:** Research → Scoring Governance

---

## 1. Purpose

EV-006 is gated on a single missing input: *"requires viscous fiber vocabulary dictionary to parse ingredient text reliably."* This document supplies that dictionary. It maps each fiber to:

- its **functional class** — the only distinction EV-006 actually scores on (viscous/gel-forming vs non-viscous/prebiotic), because viscosity is what produces postprandial glycemic dampening;
- **Hebrew label patterns** and **English label patterns** as they actually appear in Israeli retail ingredient lists (`מרכיבים`);
- **E-number** where the ingredient is a regulated additive (gelling agent / stabilizer);
- **false-positive risks** — the disambiguations that must hold or the signal mis-fires;
- **Israeli-label context** where a real appearance pattern is known.

This is a presence/identity dictionary only. EV-006's own `risk_of_misuse` stands: **quantity is not label-observable**, so detection is presence-only and the downstream signal must be credit-capped accordingly. Vocabulary first; scoring second.

---

## 2. Functional classification (the EV-006 axis)

The scored distinction is **viscosity**, not solubility and not "prebiotic" marketing. A fiber earns glycemic-dampening credit only if it forms a viscous gel in the small intestine.

| Fiber | Functional class (EV-006) | Gel / glycemic dampening | Fermentable / prebiotic | E-number |
|-------|---------------------------|--------------------------|-------------------------|----------|
| Oat/barley β-glucan | **Viscous soluble** | Yes (strong) | Yes | — |
| Psyllium (husk) | **Viscous soluble** | Yes (strong) | Partial | — |
| Guar gum (native) | **Viscous soluble** | Yes | Yes | E412 |
| Pectin | **Viscous soluble** | Yes (gelling) | Yes | E440 |
| Partially hydrolyzed guar gum (PHGG) | **Non-viscous prebiotic** ⚠ | **No** (hydrolysis strips viscosity) | Yes (strong) | — |
| Inulin | Non-viscous prebiotic | No | Yes | — |
| Chicory fiber (inulin/oligofructose source) | Non-viscous prebiotic | No | Yes | — |
| FOS / oligofructose | Non-viscous prebiotic | No | Yes | — |
| GOS | Non-viscous prebiotic | No | Yes | — |
| Resistant dextrin / resistant maltodextrin | Non-viscous prebiotic | No (mild at best) | Yes | — |
| Arabinogalactan (larch) | Non-viscous prebiotic | No | Yes | — |
| Acacia fiber / gum arabic | Non-viscous prebiotic | No | Yes | E414 |

**Two non-obvious calls, both load-bearing:**

1. **PHGG is NOT viscous.** Native guar gum is one of the most viscous food fibers; *partial hydrolysis is performed specifically to destroy that viscosity* (to make a clear, non-thickening, well-tolerated soluble fiber — e.g. Sunfiber). So native guar → viscous class; PHGG → non-viscous prebiotic class. A single `guar` substring match cannot tell them apart — see §4.6.

2. **"Resistant maltodextrin" ≠ "maltodextrin."** Plain maltodextrin (מלטודקסטרין) is a rapidly-digestible glucose polymer — the *opposite* of a fiber. Only the resistant form (Nutriose, Fibersol-2, "דקסטרין עמיד") is fiber. A bare `maltodextrin`/`מלטודקסטרין` match must NOT enter the fiber dictionary — see §4.8.

---

## 3. Vocabulary entries

Patterns are for case-insensitive substring matching, consistent with `signal_extractor.py` (`_search`). Hebrew variants include spacing and hyphen variants seen on Israeli labels. Listed `אינדקס` order is not meaningful.

### 3.1 β-glucan — VISCOUS
- **English:** `beta-glucan`, `beta glucan`, `β-glucan`, `betaglucan`, `oat beta-glucan`, `barley beta-glucan`
- **Hebrew:** `בטא גלוקן`, `בטא-גלוקן`, `ביתא גלוקן`, `ביתא-גלוקן`, `בטא גלוקאן`
- **E-number:** none (fiber, not an additive)
- **False-positive risk:** **Source matters.** Cereal β-glucan (oat/barley, 1,3/1,4-linked) is the viscous, glycemic-active one. **Yeast / mushroom / reishi β-glucan (1,3/1,6-linked)** is an immune-modulation ingredient with *no* viscous/glycemic action — common in supplements. If the match co-occurs with `שמרים`/`yeast`/`mushroom`/`פטריות`/`reishi`/`ריישי`, do **not** assign viscous credit. Cereal context (`שיבולת שועל`/`oat`, `שעורה`/`barley`) confirms the viscous class.
- **Israeli-label context:** Appears on oat-based products and oat-bran cereals; explicitly called out on products carrying a cholesterol-lowering claim (EFSA/MoH β-glucan claim threshold). Often written as `בטא גלוקן משיבולת שועל`.

### 3.2 Psyllium — VISCOUS
- **English:** `psyllium`, `psyllium husk`, `ispaghula`, `plantago ovata`, `plantago`
- **Hebrew:** `פסיליום`, `פסיליום הוסק`, `קליפת פסיליום`, `זרעי פסיליום`, `איספגולה`, `פלנטגו`
- **E-number:** none
- **False-positive risk:** Low on intent, but watch the **registry error in EV-006's note** — it lists `קליפת צ'יה` ("chia husk") for psyllium. That is wrong; chia (`צ'יה`) is a separate seed and is **not** psyllium. Do **not** add `צ'יה`/`chia` to the psyllium pattern set. (Correction logged in §5.)
- **Israeli-label context:** Rare in mainstream food; appears in fiber supplements, "fiber loaf"/diet breads, and bowel-regularity products. Usually transliterated `פסיליום`.

### 3.3 Guar gum (native) — VISCOUS
- **English:** `guar gum`, `guar`, `cyamopsis`, `E412`, `E-412`
- **Hebrew:** `גואר`, `גומי גואר`, `גואר גאם`, `שרף גואר`, `E412`, `E-412`
- **E-number:** E412
- **False-positive risk:** **Two distinct risks.** (a) *Dose:* guar is most often present as a trace **stabilizer/thickener** (well under 1%), not a meaningful fiber dose — presence ≠ functional fiber. Credit must stay presence-capped per EV-006. (b) *PHGG collision:* the bare token `גואר`/`guar` also matches **partially hydrolyzed guar gum**, which is non-viscous (§3.4). Resolve PHGG **before** assigning guar to the viscous class — see §4.6.
- **Israeli-label context:** Extremely common as `גואר`/E412 in dairy, ice cream, sauces, and gluten-free baked goods — almost always trace-level stabilizer use.

### 3.4 Partially hydrolyzed guar gum (PHGG) — NON-VISCOUS prebiotic ⚠
- **English:** `partially hydrolyzed guar gum`, `partially hydrolysed guar gum`, `PHGG`, `hydrolyzed guar`, `sunfiber`
- **Hebrew:** `גואר מפורק חלקית`, `גואר מהידרוליזה חלקית`, `גומי גואר מפורק חלקית`, `סאנפייבר`
- **E-number:** none (sold as a dietary fiber, not as the E412 additive)
- **False-positive risk:** **This is itself the disambiguator for §3.3.** The hydrolysis qualifier (`מפורק`/`hydrolyz`/`PHGG`/`sunfiber`) must be tested first; if it fires, classify **non-viscous** and suppress the viscous-guar assignment.
- **Israeli-label context:** Niche — appears in "gut health"/IBS-tolerance fiber supplements and some functional drinks, usually under the brand `Sunfiber`/`סאנפייבר`. Rarely written in full Hebrew.

### 3.5 Pectin — VISCOUS
- **English:** `pectin`, `apple pectin`, `citrus pectin`, `E440`, `E-440`, `E440a`, `E440b`, `amidated pectin`
- **Hebrew:** `פקטין`, `פקטין תפוחים`, `פקטין הדרים`, `E440`, `E-440`
- **E-number:** E440 (a = pectin, b = amidated pectin)
- **False-positive risk:** Pectin is genuinely viscous/gelling, but in jams/jellies/fruit fillings it is a **gelling agent at functional dose for texture**, not added as a "fiber." Class assignment (viscous) is correct; the **scoring** layer should not read pectin presence as a health-fortification signal — it is endemic to fruit-preserve categories. Presence-cap applies.
- **Israeli-label context:** Ubiquitous as `פקטין`/E440 in jams (`ריבה`), fruit yogurts, and gummies.

### 3.6 Inulin — NON-VISCOUS prebiotic
- **English:** `inulin`, `chicory inulin`, `agave inulin`, `oligofructose-enriched inulin`
- **Hebrew:** `אינולין`, `אינולין משורש עולש`, `אינולין מעולש`
- **E-number:** none
- **False-positive risk:** Low. Inulin is unambiguous and is the canonical "high-fiber claim with no glycemic gel" ingredient EV-006 exists to catch. Do not confuse with `insulin`/`אינסולין` (a hormone — different word, but visually close; exact-token match avoids it).
- **Israeli-label context:** Very common as `אינולין` in "high-fiber" yogurts, protein/diet bars, fiber-enriched breads, and children's probiotic products.

### 3.7 Chicory fiber — NON-VISCOUS prebiotic (inulin/FOS source)
- **English:** `chicory`, `chicory root`, `chicory fiber`, `chicory root fiber`, `cichorium`
- **Hebrew:** `עולש`, `שורש עולש`, `סיבי עולש`, `סיבים משורש עולש`, `סיבי שורש עולש`
- **E-number:** none
- **False-positive risk:** **Roasted chicory as a coffee ingredient.** `עולש קלוי` / `roasted chicory` in coffee substitutes and instant-coffee blends is a flavoring, **not** added fiber. If the match co-occurs with `קלוי`/`roasted`/`קפה`/`coffee`/`תחליף קפה`, suppress the fiber assignment. The fiber sense almost always carries `סיב`/`שורש`/`fiber`/`root`.
- **Israeli-label context:** `סיבי עולש`/`שורש עולש` appears on fiber-fortified products; `עולש קלוי` appears on coffee-substitute and chicory-coffee products (distinct meaning).

### 3.8 FOS / oligofructose — NON-VISCOUS prebiotic
- **English:** `FOS`, `fructo-oligosaccharides`, `fructooligosaccharides`, `oligofructose`, `fructo oligosaccharide`
- **Hebrew:** `פרוקטו-אוליגוסכרידים`, `פרוקטו אוליגוסכרידים`, `פרוקטואוליגוסכרידים`, `אוליגופרוקטוז`, `FOS`
- **E-number:** none
- **False-positive risk:** Bare `FOS` is a short token — guard against matching inside unrelated strings/SKU codes. Require word-boundary or co-occurrence with a fiber/prebiotic context, or prefer the spelled-out Hebrew/English forms. Functionally overlaps with chicory/inulin (often the same chicory source).
- **Israeli-label context:** Common in infant/toddler formula (`תמ"ל`) and prebiotic-marketed dairy, frequently paired with GOS as `GOS/FOS`.

### 3.9 GOS — NON-VISCOUS prebiotic
- **English:** `GOS`, `galacto-oligosaccharides`, `galactooligosaccharides`, `galacto oligosaccharide`
- **Hebrew:** `גלקטו-אוליגוסכרידים`, `גלקטו אוליגוסכרידים`, `גלקטואוליגוסכרידים`, `GOS`
- **E-number:** none
- **False-positive risk:** Same short-token caution as FOS for bare `GOS`. Prefer spelled-out forms or `GOS/FOS` co-occurrence.
- **Israeli-label context:** Predominantly infant formula and follow-on milks, where the `GOS/FOS 9:1` prebiotic blend is standard and explicitly labeled.

### 3.10 Resistant dextrin / resistant maltodextrin — NON-VISCOUS prebiotic
- **English:** `resistant dextrin`, `resistant maltodextrin`, `soluble corn fiber`, `nutriose`, `fibersol`, `fibersol-2`, `digestion-resistant maltodextrin`, `wheat dextrin`
- **Hebrew:** `דקסטרין עמיד`, `מלטודקסטרין עמיד`, `דקסטרין עמיד לעיכול`, `סיבי תירס מסיסים`, `נוטריוז`, `פיברסול`
- **E-number:** none
- **False-positive risk:** **The single highest-risk term in this registry.** Plain `maltodextrin` / `מלטודקסטרין` / `dextrin` / `דקסטרין` is a **rapidly digestible glucose polymer — not fiber** and arguably a fast-carb negative. The fiber sense **requires the resistance qualifier** (`resistant`/`עמיד`/`לעיכול`) or a brand token (`nutriose`/`fibersol`/`נוטריוז`/`פיברסול`). A bare maltodextrin/dextrin match must be **excluded** from the fiber dictionary entirely. See §4.8.
- **Israeli-label context:** `דקסטרין עמיד` / brand `Nutriose` appears on fiber-fortified diet bars, "added fiber" beverages, and some breads. Plain `מלטודקסטרין` is everywhere as a filler/carrier (do not credit).

### 3.11 Arabinogalactan — NON-VISCOUS prebiotic
- **English:** `arabinogalactan`, `larch arabinogalactan`, `larix`, `fiberaid`
- **Hebrew:** `ארבינוגלקטן`, `ערבינוגלקטן`, `ארבינוגלקטאן`
- **E-number:** none (larch arabinogalactan; distinct from gum-arabic's arabinogalactan-protein fraction)
- **False-positive risk:** Low frequency; mostly supplements. Note conceptual overlap with gum arabic (§3.12), which is itself an arabinogalactan-protein — keep them as separate tokens but both land in the non-viscous prebiotic class, so misclassification between them is harmless.
- **Israeli-label context:** Rare in food; appears in immune/prebiotic supplements, often brand `FiberAid`.

### 3.12 Acacia fiber / gum arabic — NON-VISCOUS prebiotic
- **English:** `gum arabic`, `acacia gum`, `acacia fiber`, `acacia fibre`, `arabic gum`, `E414`, `E-414`
- **Hebrew:** `גומי ערבי`, `גומי אקאציה`, `גאם ערביק`, `סיבי שיטה`, `שיטה`, `שרף שיטה`, `E414`, `E-414`
- **E-number:** E414
- **False-positive risk:** (a) **Already covered by EV-019** `PREBIOTIC_GUM_PATTERNS` for emulsifier-penalty *exemption* — this entry is for fiber *classification*, not a second exemption; do not let the two double-fire as separate credits. (b) The bare Hebrew `שיטה` also means "method/approach" in ordinary text — only treat it as acacia inside an ingredient-list context (co-occurrence with `גומי`/`סיבי`/`שרף` or an E-number). (c) Trace stabilizer dose caveat as with guar/pectin.
- **Israeli-label context:** `גומי ערבי`/E414 is common as a stabilizer/glazing carrier (soft drinks, candies, supplements); `סיבי שיטה` (acacia *fiber*, functional dose) is the dietary-fiber sense and is far rarer.

---

## 4. Disambiguation rules (must hold before class assignment)

These are ordered guards. Apply top-down; the first matching guard decides the class.

1. **§4.6 PHGG-before-guar:** if PHGG markers fire → non-viscous; suppress viscous-guar.
2. **§4.8 resistant-before-maltodextrin:** credit only with the resistance qualifier/brand; bare maltodextrin/dextrin → exclude.
3. **§4.1 β-glucan source:** yeast/mushroom context → no viscous credit; cereal context → viscous.
4. **§4.7 chicory coffee:** roasted/coffee context → not fiber.
5. **§4.x trace-dose cap:** for E412/E414/E440 (guar/acacia/pectin), presence is stabilizer-level by default — never read as fortification; EV-006 presence-cap applies.
6. **Short-token guard:** `FOS`, `GOS` bare tokens require spelled-out form or fiber-context co-occurrence.

(The numbering references the entry sections above where each rule's evidence lives.)

---

## 5. Registry corrections raised by this work

| Item | Location | Issue | Correction |
|------|----------|-------|------------|
| C-1 | `bsip2_evidence_registry_v1.md` EV-006 `notes` | Psyllium husk glossed as `קליפת צ'יה` ("**chia** husk") | Should be `קליפת פסיליום`. `צ'יה`/chia is a different seed and must not be in the psyllium pattern set. Flag for Nutrition/registry owner to amend the note; **not** changed here (no scoring/registry edit in this task). |

---

## 6. Implementation-ready dictionary (for Data/scoring — not yet wired)

Drop-in shape mirroring `signal_extractor.py` (`HIGH_RISK_EMULSIFIER_PATTERNS`, `POLYOL_TYPE_MAP`). **Not imported anywhere yet** — wiring + signal logic is a separate scoring task gated on EV-006 going `should_affect_score_now: true`.

```python
# EV-006 — viscous (gel-forming, glycemic-dampening) soluble fibers
VISCOUS_FIBER_PATTERNS = {
    "beta_glucan": ["beta-glucan", "beta glucan", "β-glucan", "betaglucan",
                    "בטא גלוקן", "בטא-גלוקן", "ביתא גלוקן", "ביתא-גלוקן", "בטא גלוקאן"],
    "psyllium":    ["psyllium", "ispaghula", "plantago",
                    "פסיליום", "קליפת פסיליום", "זרעי פסיליום", "איספגולה", "פלנטגו"],
    "guar_native": ["guar gum", "guar", "E412", "E-412",
                    "גואר", "גומי גואר", "גואר גאם", "שרף גואר"],
    "pectin":      ["pectin", "E440", "E-440",
                    "פקטין", "פקטין תפוחים", "פקטין הדרים"],
}

# EV-006 — non-viscous / prebiotic-fermentable fibers (NO glycemic-gel credit)
PREBIOTIC_FIBER_PATTERNS = {
    "phgg":        ["partially hydrolyzed guar gum", "partially hydrolysed guar gum",
                    "PHGG", "hydrolyzed guar", "sunfiber",
                    "גואר מפורק חלקית", "גואר מהידרוליזה חלקית", "סאנפייבר"],
    "inulin":      ["inulin", "chicory inulin", "אינולין"],
    "chicory":     ["chicory root", "chicory fiber", "chicory fibre", "chicory root fiber",
                    "סיבי עולש", "שורש עולש", "סיבי שורש עולש", "סיבים משורש עולש"],
    "fos":         ["fructo-oligosaccharides", "fructooligosaccharides", "oligofructose",
                    "פרוקטו-אוליגוסכרידים", "פרוקטו אוליגוסכרידים", "אוליגופרוקטוז"],
    "gos":         ["galacto-oligosaccharides", "galactooligosaccharides",
                    "גלקטו-אוליגוסכרידים", "גלקטו אוליגוסכרידים"],
    "resistant_dextrin": ["resistant dextrin", "resistant maltodextrin", "soluble corn fiber",
                          "nutriose", "fibersol", "wheat dextrin",
                          "דקסטרין עמיד", "מלטודקסטרין עמיד", "נוטריוז", "פיברסול"],
    "arabinogalactan": ["arabinogalactan", "larch arabinogalactan", "fiberaid",
                        "ארבינוגלקטן", "ערבינוגלקטן"],
    "acacia":      ["gum arabic", "acacia gum", "acacia fiber", "acacia fibre", "E414", "E-414",
                    "גומי ערבי", "גומי אקאציה", "גאם ערביק", "סיבי שיטה"],
}

# Suppression guards — must run BEFORE class assignment (see §4)
PHGG_OVERRIDES_GUAR    = ["partially hydrolyzed", "partially hydrolysed", "מפורק חלקית",
                          "מהידרוליזה", "PHGG", "sunfiber", "סאנפייבר"]
BETA_GLUCAN_NON_CEREAL = ["yeast", "שמרים", "mushroom", "פטריות", "reishi", "ריישי",
                          "1,3/1,6"]   # → immune-modulating, NOT viscous
CHICORY_NON_FIBER      = ["roasted", "קלוי", "coffee", "קפה", "תחליף קפה"]  # coffee, not fiber
# Plain maltodextrin/dextrin WITHOUT a resistance qualifier is NOT fiber — never credit:
MALTODEXTRIN_EXCLUDE   = ["maltodextrin", "מלטודקסטרין", "dextrin", "דקסטרין"]
RESISTANCE_QUALIFIER   = ["resistant", "עמיד", "לעיכול", "nutriose", "fibersol",
                          "נוטריוז", "פיברסול", "soluble corn fiber"]
```

---

## 7. Status & next step

- **Deliverable complete:** all 12 requested fibers covered with Hebrew + English patterns, E-numbers, functional class, false-positive risks, and Israeli-label context.
- **EV-006 detection input is now satisfied** (vocabulary dictionary exists). The remaining gate items before `should_affect_score_now: true` are scoring-side, not vocabulary-side: (a) presence-only credit cap, (b) viscous vs non-viscous signal weighting, (c) regression fixtures. Those are out of scope here ("Do not change scoring").
- **One registry correction (C-1)** routed to the EV-006 note owner.
