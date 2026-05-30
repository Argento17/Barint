# Bread-Light — Seed Halo Examples

**Run:** run_bread_light_001  **Date:** 2026-05-20

## Definition

Seed halo: seeds (sesame, flax, chia, sunflower, pumpkin) are visually prominent
on product packaging and appear in the name/claims, but constitute <10-15% of
product weight. The refined flour base remains dominant.

The halo creates three distortions:
1. Routing: seed/WFF signals contaminate category routing
2. Marketing: 'superfood' and 'omega-3' claims attach to trace amounts
3. Structural class: seed presence may pull toward A-B classes inappropriately

## Detected Cases (Group C Products)

### לחמי קריספ שיפון וגרעינים נורדי [Group C]

**Score:** 81.6  **Grade:** A  **Category:** whole_food_fat
**Claims:** גרעינים מלאים, עשיר בסיבים, ללא תוספת סוכר
**Seed positions in ingredient order:** pos3='זרעי פשתן (8%)' (8.0%); pos4='זרעי שומשום (5%)' (5.0%)
**Ingredients:** `קמח שיפון מלא (65%), זרעי חמנייה (12%), זרעי פשתן (8%), זרעי שומשום (5%), מלח, שמרים...`

_Assessment:_ Partial halo: seeds at positions [3, 4] with declared amounts <10%. Structurally secondary despite name prominence.

### לחם גרעינים אמיתי [Group C]

**Score:** 76.5  **Grade:** B  **Category:** default
**Claims:** עשיר בגרעינים, ללא מוסיפים, טבעי
**Seed positions in ingredient order:** pos3='שומשום (8%)' (8.0%); pos5='פשתן (5%)' (5.0%)
**Ingredients:** `קמח חיטה מלאה (55%), מים, שומשום (8%), זרעי חמנייה (7%), פשתן (5%), מלח, שמרים...`

_Assessment:_ Partial halo: seeds at positions [3, 5] with declared amounts <10%. Structurally secondary despite name prominence.

### קרקרים "שבעת המינים" גרעינים [Group C]

**Score:** 59.1  **Grade:** C  **Category:** whole_food_fat
**Claims:** שבעת המינים, עשיר בגרעינים, טבעי, ארץ ישראל
**Seed positions in ingredient order:** pos5='שומשום (3%)' (3.0%); pos7='זרעי פשתן (2%)' (2.0%)
**Ingredients:** `קמח חיטה, שמן סויה, מלח, גרגרי שיבולת שועל (4%), שומשום (3%), כוסמין (2%), זרעי פשתן (2%), זרעי חמנייה (2%), לציטין (E-322), E-471, E-500...`

_Assessment:_ Seed halo confirmed: seeds appear at ingredient position(s) [5, 7] (minor ingredient). Category routed to 'whole_food_fat' — WFF signals contaminated routing.

### קרקר "גרעינים זהובים" פרמיום [Group C]

**Score:** 57.9  **Grade:** C  **Category:** whole_food_fat
**Claims:** גרעינים זהובים, טבעי, ללא GMO, פרמיום
**Seed positions in ingredient order:** pos3='זרעי שומשום מזהב (5%)' (5.0%)
**Ingredients:** `קמח חיטה, שמן קנולה, זרעי שומשום מזהב (5%), מלח, דבש (2%), לציטין (E-322), E-471, E-481...`

_Assessment:_ Partial halo: seeds at positions [3] with declared amounts <10%. Structurally secondary despite name prominence.

### קרקר "פשתן וצ'יה" סופר-פוד [Group C]

**Score:** 52.6  **Grade:** C  **Category:** snack_bar_granola
**Claims:** אומגה 3, פשתן וצ'יה, סופר-פוד, ברא-טבע
**Seed positions in ingredient order:** pos3='זרעי פשתן (4%)' (4.0%); pos4='זרעי צ'יה (3%)' (3.0%)
**Ingredients:** `קמח חיטה (70%), שמן צמחי, זרעי פשתן (4%), זרעי צ'יה (3%), מלח, לציטין (E-322), E-471, E-500, טעם טבעי...`

_Assessment:_ Partial halo: seeds at positions [3, 4] with declared amounts <10%. Structurally secondary despite name prominence.

### לחמי קריספ חלבון ופשתן "17 גרם" [Group E]

**Score:** 71.1  **Grade:** B  **Category:** dairy_protein
**Claims:** 17 גרם חלבון, עשיר בפשתן, ללא תוספת סוכר, חיטה מלאה
**Seed positions in ingredient order:** pos4='פשתן (8%)' (8.0%)
**Ingredients:** `קמח שיפון מלא (45%), חלבון מי גבינה מרוכז (15%), קמח חיטה מלאה (20%), פשתן (8%), מלח, שמרים, לציטין (E-322)...`

_Assessment:_ Seed halo confirmed: seeds appear at ingredient position(s) [4] (minor ingredient). Category routed to 'dairy_protein' — WFF signals contaminated routing.

## Routing Impact

Seed presence in ingredient text triggers `whole_food_fat` WFF signals even when
seeds are a minor ingredient. This is the WFF context gate failure mode for
bread products: the gate prevents nut contamination in cereal but does not have
an equivalent gate for bread products (because no bread category exists).

A bread/cracker archetype would need a seed-position check:
- Seeds at position 1-2 → structural seed cracker (genuine WFF character)
- Seeds at position 3+ with <10% declared → seed halo (refined base + decoration)