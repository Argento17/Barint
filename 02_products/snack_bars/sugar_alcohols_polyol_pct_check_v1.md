# Polyol On-Pack Signal Check — Maltitol Protein Bars
**Task:** TASK-379 | **Date:** 2026-06-23 | **Author:** Research Agent

## Purpose

Owner question: producers don't disclose maltitol grams — how do we know if a bar exceeds 10% added polyols?

Legal answer under Israeli תקנות הגנה על בריאות הציבור (מזון) (סימון מזון המכיל ממתיק מסוגים מסוימים), התשע"ח-2018, Section 2(2) (in force January 2021, mirroring EU Reg 1169/2011 Annex III): products where added polyols exceed 10% by weight must carry the mandatory warning "צריכה מופרזת עלולה לגרום לפעילות מעיים מוגברת." Presence of that warning = confirmed >10%. Absence is ambiguous (compliant ≤10%, or non-compliant).

The "עם ממתיק/ממתיקים" declaration is separately mandatory for any product using sweeteners; it is not a proxy for the >10% threshold.

---

## Bars Checked

Three bars with `key_signals.maltitol: true` were specified in the task. All three appear in `protein_combined_frontend_v2.json`. A fourth bar (pb-009, פרו שטראוס שוקולד עוגיות, barcode 7290119371129) also carries `maltitol: true` and appears alongside pb-010 in the same PRO Strauss line — noted in the findings section.

| ID | Barcode | Name | Brand | Bar weight |
|----|---------|------|-------|------------|
| pb-007 | 7290019766025 | אול אין סופט פיסטוק | all in | 55 g |
| pb-010 | 7290119371112 | פרו שטראוס חטיף חלבון קרמל ואגוזים | פרו שטראוס | 60 g |
| pb-013 | 7290015130035 | WIN חטיף חלבון קרם קרמל | WIN | 65 g |

---

## Per-Bar Findings

### pb-007 — אול אין סופט פיסטוק (barcode 7290019766025)

**Sources consulted:**
- Shufersal digital product page: `https://www.shufersal.co.il/online/he/p/P_7290019766025` (live fetch, 2026-06-23)
- bealion.co.il AllIn Extra Soft product listing: `https://bealion.co.il/product/allin-extra-soft-protein-bars/` (live fetch, 2026-06-23)
- Web search results aggregating multiple Israeli sport-nutrition retailer listings (caveret.org, myshake.co.il, super-pharm.co.il)

**1. Voluntary polyol gram declaration ("מתוכם רב-כהלים")**
YES — the Shufersal nutritional panel lists:
- Per 100 g: **34.1 g רב כהלים**
- Per 55 g serving: **18.8 g רב כהלים**

This is a voluntary panel disclosure, not the mandatory on-pack warning. It is the full polyol load (maltitol + maltitol syrup + polydextrose + glycerol all count toward the panel figure; only "added polyols" count toward the 10% regulatory trigger — see interpretation note below).

**2. "עם ממתיק/ממתיקים" declaration**
NOT VISIBLE on the Shufersal digital page. Web search results do not surface this phrasing either. The ingredients list uses "ממתיקים (מלטיטול, סירופ מלטיטול, סוכרלוז)" but the standalone "עם ממתיקים" front-of-pack statement is not confirmed on any source retrieved.

**3. Laxative / >10% warning**
CONFIRMED PRESENT — multiple Israeli sport-nutrition retailer listings (bealion.co.il, web search aggregations) reproduce the on-pack text:
**"צריכה מופרזת עלולה לגרום לפעילות מעיים מוגברת."**
Source: bealion.co.il product listing (live fetch). This is the mandatory Israeli wording for the >10% polyol threshold signal.

**4. Maltitol position in ingredient list (Shufersal data)**
Second ingredient group, immediately after protein blend: "ממתיקים (מלטיטול, סירופ מלטיטול, סוכרלוז)" — maltitol is the first-named sweetener and appears early in the list, indicating a substantial proportion of the product weight.

Full ingredient list (Shufersal): "תערובת חלבונים 21.5% (חלבון חלב איזולט, חלבון מי גבינה איזולט), ממתיקים (מלטיטול, סירופ מלטיטול, סוכרלוז), חומר הלחה (גליצרול), חמאת קקאו, אבקת חלב מלא, הידרוליזט גלוטן חיטה, חומר מילוי (פולידקסטרוז), פיסטוק 2.8%, סיבי תירס מסיסים, שמן סויה, חומרי טעם וריח, מלח, מתחלב (לציטין סויה), צבע מאכל (תרכובות נחושת של כלורופיל)."

**Verdict for pb-007:** Warning present → **confirmed >10% added polyols.** Evidence tier: Moderate (warning text confirmed via multiple secondary retailer listings, not direct physical label photograph; Shufersal panel corroborates with 34.1 g polyols/100 g total).

---

### pb-010 — פרו שטראוס חטיף חלבון קרמל ואגוזים (barcode 7290119371112)

**Sources consulted:**
- Shufersal digital product page: `https://www.shufersal.co.il/online/he/p/P_7290119371112` (live fetch, 2026-06-23)
- Web search for Strauss PRO product + warning phrases (2026-06-23)
- kipa.co.il and pnns.co.il brand launch coverage confirming the PRO line

**1. Voluntary polyol gram declaration**
YES — the Shufersal nutritional panel lists:
- Per 100 g: **24 g רב כהלים**
- Per 60 g serving: **14.4 g רב כהלים**

**2. "עם ממתיק/ממתיקים" declaration**
NOT VISIBLE on any source retrieved.

**3. Laxative / >10% warning**
NOT CONFIRMED from any source retrieved. The Shufersal digital page does not reproduce it. Web search returned no source explicitly confirming the laxative warning on this specific bar. The PRO Strauss brand launch coverage (pnns.co.il, kipa.co.il) discusses the product nutritionally but does not mention the warning.

**Important caveat:** Absence of the warning in digital retailer pages is not proof of its absence on physical packaging. Shufersal web pages for pb-007 and pb-013 also did not show the warning in their HTML yet we confirmed it exists on those bars through other retailer sources. The 24 g/100 g polyol figure from the nutrition panel strongly suggests the >10% threshold is met (sorbitol + maltitol both present, glycerol also present), but we cannot assign "confirmed present" without a source that reproduces the warning text.

**4. Maltitol position in ingredient list (Shufersal data)**
Maltitol appears mid-list, after the caramel layer sub-ingredient (which itself leads with sorbitol): "חלבוני חלב (26%), שכבה בטעם קרמל (13%) [ממתיק (סורביטול), שמנים ושומנים מהצומח, דקסטרין (חיטה - גלוטן), חומר הלחה (גליצרול), אבקת חלב, מים, מתחלב (E471), מלח, מווסת חומציות (סודיום ציטרט), חומרי טעם וריח], חומר הלחה (גליצרול), שברי אגוזי לוז (8.1%), מים, ממתיק (מלטיטול), חמאת קקאו, אבקת חלב, פצפוצי סויה [חלבון סויה איזולט (2.4%), עמילן טפיוקה, אבקת קקאו], עיסת קקאו, סיבים תזונתיים, שמנים ושומנים מהצומח, שומן חלב, אבקת קקאו, חומרי טעם וריח, מלח, מתחלב (לציטין סויה), ממתיק (סוכרלוז)."

**Verdict for pb-010:** **Warning not confirmed from any reachable source.** The 24 g/100 g panel polyol figure is consistent with the product exceeding the 10% threshold — but per the honesty constraints of this task, we cannot state the warning is present without finding a source that reproduces it. Status: **warning not found in sources reached (panel polyol figure = 24 g/100 g strongly suggestive but insufficient to confirm).**

---

### pb-013 — WIN חטיף חלבון קרם קרמל (barcode 7290015130035)

**Sources consulted:**
- Shufersal digital product page: `https://www.shufersal.co.il/online/he/p/P_7290015130035` (live fetch, 2026-06-23)
- bealion.co.il WIN protein bar listing: `https://bealion.co.il/product/win-protein-bar/` (live fetch, 2026-06-23)
- israelbody.org WIN protein bar page: `https://www.israelbody.org/products/win-protein-bar` (live fetch, 2026-06-23)
- Web search for WIN protein bar + warning phrases (2026-06-23)

**1. Voluntary polyol gram declaration**
YES — the Shufersal nutritional panel lists:
- Per 100 g: **27 g רב כהלים**
- Per 65 g unit: **17 g רב כהלים**

**2. "עם ממתיק/ממתיקים" declaration**
NOT VISIBLE on any source retrieved.

**3. Laxative / >10% warning**
CONFIRMED PRESENT — bealion.co.il product listing reproduces on-pack text:
**"צריכה מופרזת עלולה לגרום לפעילות מעיים מוגברת."**
Source: bealion.co.il (live fetch, 2026-06-23). Web search results for WIN bars also consistently cite this warning.

**4. Maltitol position in ingredient list (Shufersal data)**
Maltitol is the first listed sweetener after the protein blend: "תערובת חלבונים 30% (חלבון חלב, פפטידי קולגן, חלבון ביצה), ממתיק (מלטיטול), שקדים קלויים (12%), סיבי תירס מסיסים, חמאת קקאו, חומר הלחה (גליצרול), עיסת קקאו, ממתיק (סורביטול), אבקת חלב מלא (19.9%), חמאה, ממתיק (אריתריטול), סיבי פולידקסטרוז, חומרי טעם וריח טבעיים, צבע מאכל (קרמל), מתחלבים (לציטין, חמניות), מלח, ממתיק (סוכרלוז)."

Maltitol is the 2nd ingredient by position (after the protein blend), before almonds — indicating it is a major weight contributor.

**Verdict for pb-013:** Warning present → **confirmed >10% added polyols.** Evidence tier: Moderate (same caveats as pb-007 — bealion.co.il secondary listing, not physical label photograph; Shufersal panel corroborates with 27 g polyols/100 g total).

---

## Summary Table

| ID | Barcode | Name | Retailer source URL | Polyol g/100g (panel) | "עם ממתיק" present? | Laxative warning present? | Maltitol ingredient position | Status |
|----|---------|------|---------------------|-----------------------|----------------------|--------------------------|------------------------------|--------|
| pb-007 | 7290019766025 | אול אין סופט פיסטוק | shufersal.co.il/p/P_7290019766025 | 34.1 g | Not confirmed in sources | **CONFIRMED PRESENT** (bealion.co.il) | 2nd position (first sweetener group) | **Confirmed >10%** |
| pb-010 | 7290119371112 | פרו שטראוס קרמל ואגוזים | shufersal.co.il/p/P_7290119371112 | 24 g | Not confirmed | **NOT FOUND** in any source reached | Mid-list (after caramel sub-layer) | **Warning not confirmed — panel figure suggestive** |
| pb-013 | 7290015130035 | WIN חטיף חלבון קרם קרמל | shufersal.co.il/p/P_7290015130035 | 27 g | Not confirmed | **CONFIRMED PRESENT** (bealion.co.il) | 2nd position (first sweetener after protein) | **Confirmed >10%** |

---

## Interpretation Notes

### On the polyol panel figures

All three bars report polyol grams in the nutrition panel ("רב כהלים"). These figures represent total sugar alcohol content, which typically includes maltitol, sorbitol, erythritol, and other polyols (and may include glycerol depending on how the manufacturer calculates it). The regulatory 10% threshold refers to "added polyols" — the precise figure depends on whether glycerol is excluded (glycerol is classified separately under EU law). Even if glycerol is excluded:

- pb-007: 34.1 g/100 g total polyols. Even excluding glycerol substantially, this is far above 10%.
- pb-010: 24 g/100 g total polyols. Even with glycerol exclusion, this remains above 10%.
- pb-013: 27 g/100 g total polyols. Same conclusion.

All three are structurally above the threshold. The laxative warning should be mandatory on all three under תקנות התשע"ח-2018 Section 2(2).

### On warning text variation

The Israeli regulatory text is "צריכה מופרזת עלולה לגרום לפעילות מעיים מוגברת" (excessive consumption may cause increased bowel activity). The EU Reg 1169/2011 Annex III English text is "excessive consumption may produce laxative effects." These are equivalent mandated warnings; the Israeli version uses "פעילות מעיים מוגברת" rather than "שלשול" (diarrhea). Task spec cited "שלשול" as the expected phrasing; the actual Israeli regulatory text uses "פעילות מעיים מוגברת." Both confirmed sources (bealion.co.il for pb-007 and pb-013) reproduce "פעילות מעיים מוגברת."

### On the "עם ממתיקים" statement

The "עם ממתיקים" front-of-pack declaration is separately mandated for any food containing sweeteners (EU Reg 1169/2011 Annex III, mirrored in Israeli regulations). It is NOT a proxy for the >10% polyol threshold — it is a different, lower-bar requirement. None of the three Shufersal digital pages reproduced this text, but absence from digital pages does not equal absence from physical packaging. This task's question was about the laxative warning (the >10% signal), not the "עם ממתיקים" declaration; no conclusion should be drawn about "עם ממתיקים" compliance from these findings.

### On pb-010 specifically

pb-010 is the only bar where we could not confirm the warning from any reachable source. This is not a finding that the warning is absent — it is a finding that the sources we could reach did not reproduce it. The structural evidence (24 g/100 g polyols, maltitol + sorbitol + sucralose in ingredient list) is consistent with mandatory warning applicability. A physical label check or a Strauss consumer-service inquiry would resolve this.

---

## Honest Article Framing — What the Evidence Supports

**What we can say with evidence:**
- pb-007 (אול אין סופט פיסטוק) and pb-013 (WIN קרם קרמל) are confirmed to carry the mandatory ">10% polyol" on-pack warning — meaning the manufacturer itself has established (and declared) that these bars exceed the 10% added-polyol threshold.
- All three bars voluntarily disclose polyol grams on the nutrition panel (34.1 g, 24 g, 27 g per 100 g respectively), which is far above the 10% level regardless of how glycerol is treated.
- The relevant warning text is "צריכה מופרזת עלולה לגרום לפעילות מעיים מוגברת" — not "שלשול" — though in plain Hebrew these are practically equivalent.

**What we cannot say with current evidence:**
- That pb-010 (פרו שטראוס) carries the warning — we did not find a source confirming it, though the nutrition panel is consistent with the threshold being met.
- That any bar is "non-compliant" — absence of warning in digital sources does not establish non-compliance.
- An exact gram figure for maltitol alone (as opposed to total polyols) — the panel bundles all polyols together.
- That the "עם ממתיקים" statement is absent from physical packaging — digital pages do not reliably reproduce it.

**Recommended framing:**
The article can legitimately state that pb-007 and pb-013 exceed the 10% added-polyol threshold, citing the manufacturers' own mandatory on-pack declarations as evidence. For pb-010, the article should note that the nutrition panel declares 24 g/100 g polyols — consistent with exceeding the threshold — but that the warning was not confirmed in online sources. A hedge like "all three show polyol panel levels well above 10% by weight; two of the three carry the mandatory on-pack warning" is honest and defensible.

---

## Source List

1. `https://www.shufersal.co.il/online/he/p/P_7290019766025` — Shufersal product page pb-007 (live fetch 2026-06-23). Polyol panel: 34.1 g/100 g. Warning text not reproduced in HTML. **Credibility: High for nutrition panel data; incomplete for on-pack text.**
2. `https://www.shufersal.co.il/online/he/p/P_7290119371112` — Shufersal product page pb-010 (live fetch 2026-06-23). Polyol panel: 24 g/100 g. Warning text not reproduced. **Credibility: High for nutrition panel; incomplete for on-pack text.**
3. `https://www.shufersal.co.il/online/he/p/P_7290015130035` — Shufersal product page pb-013 (live fetch 2026-06-23). Polyol panel: 27 g/100 g. Warning text not reproduced. **Credibility: High for nutrition panel; incomplete for on-pack text.**
4. `https://bealion.co.il/product/allin-extra-soft-protein-bars/` — Israeli sport-nutrition retailer; reproduces on-pack warning text for AllIn Soft. Confirms: "צריכה מופרזת עלולה לגרום לפעילות מעיים מוגברת" (live fetch 2026-06-23). **Credibility: Moderate — secondary retail listing, not physical label scan.**
5. `https://bealion.co.il/product/win-protein-bar/` — Israeli sport-nutrition retailer; reproduces on-pack warning text for WIN bars. Confirms: "צריכה מופרזת עלולה לגרום לפעילות מעיים מוגברת" (live fetch 2026-06-23). **Credibility: Moderate — secondary retail listing, not physical label scan.**
6. `https://oknesset.org/meetings/2/0/2071924.html` — Knesset committee meeting protocol for תקנות הגנה על בריאות הציבור (מזון) (סימון מזון המכיל ממתיק מסוגים מסוימים), התשע"ח-2018. Confirms: 10% threshold, Section 2(2), mandatory text "צריכה מופרזת עלולה לגרום לפעילות מעיים מוגברת", in force January 2021. **Credibility: High — primary legislative/regulatory source.**
7. `https://pharmaline.co.il/articles/244630/` — Israeli pharmacy/health media coverage of the 2021 sweetener labeling regulation changes. Corroborates regulatory requirements. **Credibility: Moderate.**

---

```json
{
  "task_id": "TASK-379",
  "agent": "Research Agent",
  "return_date": "2026-06-23",
  "artifacts": [
    {
      "path": "C:\\Bari\\02_products\\snack_bars\\sugar_alcohols_polyol_pct_check_v1.md",
      "sha256": "pending_write_verify",
      "description": "Per-bar polyol on-pack signal check — 3 maltitol bars"
    }
  ],
  "counts": {
    "bars_checked": 3,
    "bars_checked_denominator": "all bars with key_signals.maltitol:true named in task spec",
    "labels_found": 3,
    "labels_found_denominator": "Shufersal digital pages reached (all 3 bars had product pages with nutrition panel data)",
    "warning_confirmed_over10": 2,
    "warning_confirmed_over10_denominator": "bars where laxative warning text confirmed from secondary retailer source",
    "warning_confirmed_bars": ["pb-007", "pb-013"],
    "warning_not_confirmed_bars": ["pb-010"],
    "polyol_grams_disclosed": 3,
    "polyol_grams_disclosed_denominator": "bars with polyol g/100g in Shufersal nutrition panel",
    "polyol_values_g_per_100g": {"pb-007": 34.1, "pb-010": 24.0, "pb-013": 27.0},
    "labels_not_found": 0,
    "labels_not_found_note": "Shufersal pages loaded for all 3 bars; digital pages do not fully reproduce on-pack warning text (limitation flagged)"
  },
  "commands_run": [
    {"tool": "WebFetch", "url": "shufersal.co.il/p/P_7290019766025", "exit": 200},
    {"tool": "WebFetch", "url": "shufersal.co.il/p/P_7290119371112", "exit": 200},
    {"tool": "WebFetch", "url": "shufersal.co.il/p/P_7290015130035", "exit": 200},
    {"tool": "WebFetch", "url": "bealion.co.il/product/allin-extra-soft-protein-bars", "exit": 200},
    {"tool": "WebFetch", "url": "bealion.co.il/product/win-protein-bar", "exit": 200},
    {"tool": "WebFetch", "url": "oknesset.org/meetings/2/0/2071924.html", "exit": 200},
    {"tool": "WebSearch", "query": "אול אין סופט פיסטוק + צריכה מופרזת", "exit": 200},
    {"tool": "WebSearch", "query": "WIN חטיף חלבון + צריכה מופרזת", "exit": 200},
    {"tool": "WebSearch", "query": "פרו שטראוס קרמל ואגוזים + צריכה מופרזת", "exit": 200},
    {"tool": "WebSearch", "query": "Israeli regulation polyols 10% laxative", "exit": 200}
  ],
  "not_done": [
    "Physical label scan or photograph for any of the three bars — would upgrade evidence tier to Strong",
    "Confirmation of laxative warning for pb-010 (פרו שטראוס) from any secondary source",
    "Confirmation of 'עם ממתיקים' front-of-pack statement for any bar",
    "Isolation of maltitol-only gram figure (panel bundles all polyols together)",
    "Victory / Yochananof / Rami-Levy cross-checks (sites returned 404 or were unreachable)"
  ],
  "acceptance_test": {
    "spec_requirement": "Per-bar table with polyol-grams-declared, with-sweetener present, laxative-warning present, maltitol position; verdict on how many bars establish >10%",
    "result": "PASS — table complete for all 3 bars; 2/3 warnings confirmed; 3/3 polyol panel figures obtained; 3/3 maltitol positions identified; honest framing guidance provided; regulatory basis cited"
  }
}
```
