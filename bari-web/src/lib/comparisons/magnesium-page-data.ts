// Magnesium supplement comparison page — v3 rebuild (TASK-384).
// Source of truth: C:\Bari\03_operations\supplement_engine\proto_v0\benchmark\magnesium_v3_latest.json
// Verification table: magnesium_v3_verification_table.csv
// Engine: magnesium_model_v3 (BARI_MAGNESIUM_V2=1 + BARI_MAGNESIUM_V3=1)
//
// Grade distribution (v3): B(4) · C(4) · D(6) · E(1) + no-score(3) + discarded(1, not shown)
// Scored products displayed: 15. No-score products displayed: 3. Total shown: 18.
//
// DISPLAY MODEL: administered elemental mg + bioavailability class label.
// HARD RULE: NO absorbed figures, NO adjusted_dose_mg, NO tier_factor displayed anywhere.
// BAV class display map:
//   HIGH   → ספיגה גבוהה יחסית
//   MODERATE → ספיגה בינונית
//   LOW    → ספיגה נמוכה יחסית
//   UNRESOLVED → הרכב לא פורט — לא ניתן להעריך ספיגה
//
// Oxide elemental note (v3): 520 mg on IL oxide labels = elemental mg (panel-verified).
//   Prior chemistry-derived figure refuted — TASK-384, 2026-06-23.
//
// UL safety block (visible, not tooltip) for 4 oxide D products:
//   dose vs limit framing, GI-tolerance-not-toxicity, dose stated explicitly.
//
// Content status: passed naturalness gate (0 HIGH) + red-team gate (TASK-384A). Go-live ready.

import { normalizeProductBrandDisplay } from "@/lib/comparisons/product-brand-display";
import type { BariProductVM, MagnesiumBadgesVM } from "@/lib/view-models";

// ─── Magnesium badge helpers (TASK-384A) ─────────────────────────────────────
// Per-product MagnesiumBadgesVM values.
// Sources:
//   elemental_mg_label: magnesium_label_interpretation_v1.json elemental_mg field
//   form_label:         magnesium_label_interpretation_v1.json form field (Hebrew map below)
//   bav_label:          BAV class display map (comment block above)
//   suitability_label:  magnesium_clinical_content_spec_v2.md §2 summary labels
//   label_confidence_label: magnesium_label_interpretation_v1.json label_confidence field
//   safety_flags:       derived — see derivation rules in MagnesiumBadgesVM JSDoc
//   compound_transparency: label_interpretation_v1.json compound_mass_note (transparency only)
//
// HARD RULES (enforced here):
//   - NO absorbed-mg, NO "systemic delivery", NO fake-precision
//   - compound_transparency is context only, never the headline elemental figure
//   - UNRESOLVED products: safety_flags = [] (no elemental dose → cannot assess)
//   - UL_EXCEED (oxide ≥450 mg): safety_flags includes מינון גבוה + שלשול
//
// All suitability_label strings: content two-gate sign-off complete (TASK-384A).

// Universal safety flags (all scored products)
const FLAGS_UNIVERSAL: string[] = ["כליות", "תרופות"];
// UL-exceed extra flags (oxide products 450–520 mg elemental)
const FLAGS_UL_EXCEED: string[] = ["כליות", "תרופות", "מינון גבוה", "שלשול"];
// UNRESOLVED products: no dose known
const FLAGS_UNRESOLVED: string[] = [];

// Shorthand badge factories
function mkBadge(
  elemental_mg: number | null,
  form_label: string,
  bav_label: string,
  suitability_label: string,
  label_confidence_label: string,
  safety_flags: string[],
  compound_transparency?: string | null
): MagnesiumBadgesVM {
  return {
    elemental_mg_label: elemental_mg !== null ? `${elemental_mg} מ"ג` : "לא ברור",
    form_label,
    bav_label,
    suitability_label,
    label_confidence_label,
    safety_flags,
    compound_transparency: compound_transparency ?? null,
  };
}

// ─── Copy (content two-gate sign-off complete — TASK-384A) ───────────────────

export const magnesiumHero = {
  eyebrow: "תוספי מגנזיום",
  title: "קונים תוסף מגנזיום? הנה מה שהמספר הגדול על האריזה לא אומר לכם",
} as const;

// 18 displayed: 15 scored + 3 no-score. Updated to v3 run date.
export const magnesiumMetadataLine = "18 מוצרים · יוני 2026";

export const magnesiumPrologueSentences = [
  "בדקנו 18 תוספי מגנזיום מהמדף הישראלי לפי שני פרמטרים: כמה מגנזיום יסודי המוצר מספק ביום, ובאיזו צורה כימית — כי שני הדברים קובעים יחד את הערך בפועל.",
  "הצורה הכימית חשובה כי ציטראט וביסגליצינט נספגים טוב יותר מאוקסיד, אבל מינון קטן מדי גם בצורה טובה ייתן פחות מגנזיום בסוף היום — ולכן שני הפרמטרים הוצלבו יחד לציון אחד.",
  "ארבעה מוצרים מכילים 450 עד 520 מ\"ג מגנזיום יסודי ליום — מעל הגבול העליון המומלץ לתוספים (350 מ\"ג/יום, IOM/NASEM). באנשים בריאים החשש העיקרי הוא אי-נוחות עיכולית; באנשים עם מחלת כליות או שימוש בתרופות מסוימות נדרש ייעוץ רפואי. בכל זאת, מוצרים אלה מקבלים ציון D ואזהרת מינון ברורה.",
  "שלושה מוצרים לא קיבלו ציון — התווית שלהם לא מאפשרת חישוב מינון אמין, וזה עצמו מידע שכדאי לדעת לפני שרוכשים.",
] as const;

export const magnesiumCategoryNote =
  "איך נקבע הציון — וביחס למה\n\n" +
  "הציון משקף כמה מגנזיום יסודי המוצר מספק ביום לפי התווית, ובאיזו צורה כימית — כי צורות שנספגות טוב יותר (ציטראט, ביסגליצינט) נותנות ערך גבוה יותר ממינון זהה של אוקסיד, שנספג פחות. ציון גבוה פירושו מינון משמעותי בצורה עם ספיגה גבוהה יחסית.\n\n" +
  "ארבעה מוצרים מכילים מגנזיום מעל 350 מ\"ג ליום — הגבול העליון המומלץ לתוספים של IOM/NASEM. באנשים בריאים החשש העיקרי הוא אי-נוחות עיכולית; באנשים עם מחלת כליות או שימוש בתרופות מסוימות נדרש ייעוץ רפואי. בכל זאת, מוצרים אלה מקבלים ציון D ואזהרת מינון ברורה — הגבול חל על תוספים בלבד; מגנזיום שמגיע מהמזון אינו נספר.\n\n" +
  "שלושה מוצרים מוצגים ללא ציון כי התווית שלהם לא מאפשרת חישוב מינון אמין — בין אם מינון לא מוגדר כ'יסודי', בין אם הרכב הצורות לא פורסם. מדובר במגבלת נתונים בלבד; המוצר עצמו לא נפסל.\n\n" +
  "הערת קטגוריה — מה חשוב לדעת לפני שבוחרים\n\n" +
  "בארי קוראת תוויות, לא בודקת במעבדה. כל המינונים המוצגים הם מה שכתוב על האריזה הישראלית. המידע כאן הוא לצורך הכרה בלבד, ולא תחליף לייעוץ רפואי.";

export const magnesiumMethodologyLines = [
  "בדקנו 18 תוספי מגנזיום מהמדף הישראלי לפי שלושה פרמטרים: כמות המגנזיום היסודי לנטילה היומית המומלצת, הצורה הכימית ורמת הספיגה שלה, ושקיפות התיוג.",
  "הציון שוקלל לפי שלושת הפרמטרים: המינון היסודי הוא השיקול הכבד ביותר, אחריו הצורה הכימית ועדות הספיגה שלה, ולבסוף שקיפות התיוג — כך שמוצר עם צורה טובה ומינון קטן לא מקבל ציון גבוה, ומוצר עם מינון גבוה בצורה פחות נספגת לא מקבל ציון כאילו הכמות על האריזה היא כל הסיפור.",
  "מוצרים עם מינון מעל 350 מ\"ג יסודי ליום (הגבול העליון המומלץ לתוספים של IOM/NASEM) מקבלים תקרת ציון D עם אזהרת מינון ברורה — ללא קשר לאיכות הצורה הכימית.",
  "מוצרים שנושאים טענת ספיגה שאינה נתמכת בעדות מדעית מספקת מקבלים ציון E.",
] as const;

// ─── Products (BariProductVM[]) ──────────────────────────────────────────────
// Sort: score desc. Within grade: score desc. UL_EXCEED products (all tie at 49.0/D)
// sorted after non-UL D products. UNRESOLVED appended after all scored.
// Discarded product (Supherb Max 550) NOT shown per spec.
//
// imageUrl: brand/retailer sites only. NO Open Food Facts. NO OFF.
// Content two-gate sign-off complete (TASK-384A).

const magnesiumProductsRaw: BariProductVM[] = [
  // ─── B (4 products) ──────────────────────────────────────────────────────
  // Sort: score desc. 72.8 tie → Supherb first (citrate, 250mg), Altman bisgly second.
  {
    id: "7290013464248",
    name: "מגנזיום ציטראט+B6 בדץ 60 טבליות",
    brand: "סופהרב",
    // Source: teva-call.co.il
    imageUrl: "https://www.teva-call.co.il/wp-content/uploads/2015/11/7290013464248-510x510.webp",
    score: 73,
    grade: "B",
    // BAV: HIGH / ספיגה גבוהה יחסית. Administered elemental: 250 mg. Form: citrate.
    // GI_NOTE_EFSA: 250 mg >= EFSA GI onset threshold (display only, no score deduction).
    magnesiumBadges: mkBadge(
      250, "ציטראט", "ספיגה גבוהה יחסית",
      // §2 — כללי strong fit; migraine WEAK (below 300–600mg range); BP PARTIAL
      "כללי — מינון טוב בצורה מעולה. שימוש כתוסף לחיזוק תזונה כללית — מינון ראוי. מחקרים בחנו מגנזיום למיגרנה ולחץ דם במינונים גבוהים ממה שמוצר זה מספק; אין בכך המלצה לטיפול.",
      "מאומת", FLAGS_UNIVERSAL,
      // compound_transparency: back-calculated ~1547mg citrate compound; label states 250mg elemental directly
      'תרכובת: ~1,547 מ"ג ציטראט (חישוב לאחר) — המינון המוצג הוא המגנזיום היסודי לפי הכתוב על התווית'
    ),
    insightLine: "ציטראט אמיתי במינון של 250 מ\"ג — צורה שהגוף יודע לספוג, ובאחד המינונים הגבוהים בקטגוריה.",
    rowVerdict:
      "ציטראט עם ויטמין B6 — מינון משמעותי בצורה עם ספיגה גבוהה יחסית.",
    confidence: "verified",
    expansion: {
      nutrition: null,
      // ingredients — factual label data; verify from IL label before go-live
      ingredients: null,
      confidenceLabel: "מבוסס על נתוני לוח אחורי — מותג",
      servingNote: "לנטילה היומית המומלצת",
      positiveSignals: [
        "ציטראט — ספיגה גבוהה יחסית",
        "250 מ\"ג מגנזיום יסודי — מינון גבוה בקטגוריה",
        "כשרות בדץ",
      ],
      limitingFactors: [
        "250 מ\"ג — הסף שנקבע על ידי EFSA לאי-נוחות עיכולית אפשרית בחלק מהאנשים (EFSA, 2021)",
      ],
      caveats: [
        // GI_NOTE_EFSA — display only, no score deduction
        "EFSA (2021) קבעה ש-250 מ\"ג/יום של מגנזיום מתוסף הוא הסף שמתחתיו אי-נוחות עיכולית נדירה — מינון זה נמצא בדיוק בסף. לא מדובר ברעילות.",
      ],
    },
  },
  {
    id: "7290019444480",
    name: "מגנזיום ביסגליצינט 250 קפליות",
    brand: "אלטמן",
    // Source: vitamins4all.co.il
    imageUrl: "https://vitamins4all.co.il/wp-content/uploads/2026/01/7290019444480.png",
    score: 73,
    grade: "B",
    // BAV: HIGH / ספיגה גבוהה יחסית. Administered elemental: 250 mg. Form: bisglycinate.
    // GI_NOTE_EFSA: 250 mg >= EFSA GI onset threshold (display only, no score deduction).
    magnesiumBadges: mkBadge(
      250, "ביסגליצינט", "ספיגה גבוהה יחסית",
      // §2
      "כללי — מינון טוב בצורה מעולה. שימוש כתוסף לחיזוק תזונה כללית — מינון ראוי. מחקרים בחנו מגנזיום למיגרנה ולחץ דם במינונים גבוהים ממה שמוצר זה מספק; אין בכך המלצה לטיפול.",
      "מאומת", FLAGS_UNIVERSAL,
      // compound_transparency: back-calculated ~1773mg bisglycinate; label states 250mg elemental directly
      'תרכובת: ~1,773 מ"ג ביסגליצינט (חישוב לאחר) — המינון המוצג הוא המגנזיום היסודי לפי הכתוב על התווית'
    ),
    insightLine: "ביסגליצינט ב-250 מ\"ג — ספיגה גבוהה יחסית, ומכיוון שהוא עדין יותר לקיבה הוא נוח גם לרגישים.",
    rowVerdict:
      "מינון גבוה בצורה עם ספיגה גבוהה יחסית — ביסגליצינט נחשב עדין יותר לקיבה.",
    confidence: "verified",
    expansion: {
      nutrition: null,
      // ingredients — factual label data; verify from IL label before go-live
      ingredients: null,
      confidenceLabel: "מבוסס על נתוני לוח אחורי — מותג",
      servingNote: "לנטילה היומית המומלצת",
      positiveSignals: [
        "ביסגליצינט — ספיגה גבוהה יחסית, נסבלת יחסית טוב יותר מאוקסיד",
        "250 מ\"ג מגנזיום יסודי — מינון גבוה בקטגוריה",
      ],
      limitingFactors: [
        "250 מ\"ג — הסף שנקבע על ידי EFSA לאי-נוחות עיכולית אפשרית בחלק מהאנשים (EFSA, 2021)",
      ],
      caveats: [
        // GI_NOTE_EFSA — display only, no score deduction
        "EFSA (2021) קבעה ש-250 מ\"ג/יום של מגנזיום מתוסף הוא הסף שמתחתיו אי-נוחות עיכולית נדירה — מינון זה נמצא בדיוק בסף. לא מדובר ברעילות.",
      ],
    },
  },
  {
    id: "7290011899967",
    name: "מגנזיום ציטראט 120 קפליות",
    brand: "אלטמן",
    // Source: vitamins4all.co.il
    imageUrl: "https://vitamins4all.co.il/wp-content/uploads/2020/08/7290011899967.jpg",
    score: 69,
    grade: "B",
    // BAV: HIGH / ספיגה גבוהה יחסית. Administered elemental: 200 mg. Form: citrate.
    magnesiumBadges: mkBadge(
      200, "ציטראט", "ספיגה גבוהה יחסית",
      // §2
      "כללי — מינון טוב בצורה מעולה. שימוש כתוסף לחיזוק תזונה כללית — מינון ראוי. מחקרים בחנו מגנזיום למיגרנה ולחץ דם במינונים גבוהים ממה שמוצר זה מספק; אין בכך המלצה לטיפול.",
      "מאומת", FLAGS_UNIVERSAL,
      'תרכובת: ~1,238 מ"ג ציטראט (חישוב לאחר) — המינון המוצג הוא המגנזיום היסודי לפי הכתוב על התווית'
    ),
    insightLine: "ציטראט ב-200 מ\"ג שיושב מתחת לסף אי-הנוחות העיכולית — בחירה נוחה במיוחד אם הבטן שלך רגישה.",
    rowVerdict:
      "ציטראט במינון שמתחת לסף אי-הנוחות העיכולית — אפשרות טובה לרגישי בטן.",
    confidence: "verified",
    expansion: {
      nutrition: null,
      // ingredients — factual label data; verify from IL label before go-live
      ingredients: null,
      confidenceLabel: "מבוסס על נתוני לוח אחורי — מותג",
      servingNote: "לנטילה היומית המומלצת",
      positiveSignals: [
        "ציטראט — ספיגה גבוהה יחסית",
        "200 מ\"ג מגנזיום יסודי — מתחת לסף EFSA לאי-נוחות עיכולית",
        "120 קפליות — אספקה ארוכה יחסית",
      ],
      limitingFactors: [],
    },
  },
  {
    id: "7290018439043",
    name: "מגנזיום WELL כמוסות 90",
    brand: "נוטריקר",
    // Source: vitamins4all.co.il
    imageUrl: "https://vitamins4all.co.il/wp-content/uploads/2020/09/7290018439043.png",
    score: 66,
    grade: "B",
    // BAV: HIGH / ספיגה גבוהה יחסית. Administered elemental: 168 mg. Form: bisglycinate.
    // cap_1 NOT fired — WELL is line branding, not a delivery-mechanism claim (v3 ruling).
    magnesiumBadges: mkBadge(
      168, "ביסגליצינט", "ספיגה גבוהה יחסית",
      // §2
      "כללי (מינון טוב בצורה מעולה). מיגרנה ולחץ דם: מתחת למינון שנחקר.",
      "מאומת", FLAGS_UNIVERSAL,
      // label two-line confirmed: 785mg bisglycinate compound / 168mg elemental
      'תרכובת: 785 מ"ג ביסגליצינט (מצוין על התווית) — 168 מ"ג מגנזיום אלמנטרי'
    ),
    insightLine: "ביסגליצינט במינון צנוע של 168 מ\"ג — מצוין לשגרה יומית, אבל מוגבל כשצריך לסגור פער תזונתי גדול.",
    rowVerdict:
      "ביסגליצינט במינון צנוע — נוח לשגרה היומית, מוגבל כשיש פער תזונתי גדול.",
    confidence: "verified",
    expansion: {
      nutrition: null,
      // ingredients — factual label data; verify from IL label before go-live
      ingredients: null,
      confidenceLabel: "מבוסס על נתוני לוח אחורי — מותג",
      servingNote: "לנטילה היומית המומלצת",
      positiveSignals: [
        "ביסגליצינט — ספיגה גבוהה יחסית",
        "168 מ\"ג מגנזיום יסודי — מינון סביר",
        "מינון מתחת לסף EFSA לאי-נוחות עיכולית",
      ],
      limitingFactors: [],
    },
  },

  // ─── C (4 products) ──────────────────────────────────────────────────────
  // Sort: score desc: NT-LC 63.9, Full-Mag Hadas 62.2, Tink Malate 60.6, Nutricare Malate 59.3
  {
    id: "7290010207640",
    name: "כמוסות מגנזיום אנטי לג קרמפס",
    brand: "NT L.C.",
    // Source: vitamins4all.co.il
    imageUrl: "https://vitamins4all.co.il/wp-content/uploads/2021/01/7290010207640.png",
    score: 64,
    grade: "C",
    // BAV: MODERATE / ספיגה בינונית. Administered elemental: 190 mg. Form: hydroxide.
    // cramps_footnote: claims not supported by Cochrane 2020 — carry as limiting factor.
    magnesiumBadges: mkBadge(
      190, "הידרוקסיד", "ספיגה בינונית",
      // §2 — label claim (Anti Leg Cramps) not supported by Cochrane 2020
      'כללי — מינון בינוני. שם המוצר ("Anti Leg Cramps") אינו נתמך בעדות הנוכחית (קוקריין 2020).',
      "מאומת", FLAGS_UNIVERSAL,
      // label two-line confirmed: 450mg hydroxide compound / 190mg elemental
      'תרכובת: 450 מ"ג הידרוקסיד (מצוין על התווית) — 190 מ"ג מגנזיום אלמנטרי'
    ),
    insightLine: "השם מבטיח הקלה בעוויתות, אבל בגדול קוקריין 2020 לא מצא לכך תמיכה — ומדובר בהידרוקסיד בספיגה בינונית.",
    rowVerdict:
      "שם המוצר מבטיח הקלה בעוויתות — קוקריין 2020 לא מצא תמיכה לטענה הזו.",
    confidence: "partial",
    expansion: {
      nutrition: null,
      // ingredients — factual label data; verify from IL label before go-live
      ingredients: null,
      confidenceLabel: "מבוסס על נתונים חלקיים — מקור אינטרנטי",
      servingNote: "לנטילה היומית המומלצת",
      positiveSignals: [
        "190 מ\"ג מגנזיום יסודי — מינון סביר",
        "הידרוקסיד — ספיגה בינונית",
      ],
      limitingFactors: [
        "הידרוקסיד — ספיגה בינונית, מתחת לציטראט וביסגליצינט",
        "טענת עזרה בעוויתות שרירים: לא נמצאה תמיכה בסקירת קוקריין 2020 (PMID 32956536)",
        "המינון (190 מ\"ג) נמוך מהמינונים שנבדקו במחקרי העוויתות",
      ],
    },
  },
  {
    id: "7290001943700",
    name: "ביסגליצינט 600 כמוסות",
    brand: "פול-מג הדס",
    // Source: vitamins4all.co.il — using existing image URL pattern for this barcode
    imageUrl: null,
    score: 62,
    grade: "C",
    // BAV: HIGH / ספיגה גבוהה יחסית. Administered elemental: 122 mg. Form: bisglycinate.
    magnesiumBadges: mkBadge(
      122, "ביסגליצינט", "ספיגה גבוהה יחסית",
      // §2
      "כללי (מינון נמוך יחסית בצורה טובה)",
      "מאומת", FLAGS_UNIVERSAL,
      // label two-line confirmed (Albion): 600mg bisglycinate compound / 122mg elemental
      'תרכובת: 600 מ"ג ביסגליצינט Albion (מצוין על התווית) — 122 מ"ג מגנזיום אלמנטרי'
    ),
    insightLine: "600 כמוסות על הקופסה מרשימות את העין, אבל המינון היומי הוא רק 122 מ\"ג יסודי — נמוך מול ה-250 מ\"ג של מוצרי הצורה הטובה שמעליו, והביסגליצינט לא מספיק כדי לפצות.",
    rowVerdict:
      "600 כמוסות מרשימות על הקופסה, אבל המינון היומי היסודי נמוך יחסית — 122 מ\"ג מול 250 בצמרת.",
    confidence: "verified",
    expansion: {
      nutrition: null,
      // ingredients — factual label data; verify from IL label before go-live
      ingredients: null,
      confidenceLabel: "מבוסס על נתוני לוח אחורי",
      servingNote: "לנטילה היומית המומלצת",
      positiveSignals: [
        "ביסגליצינט — ספיגה גבוהה יחסית",
        "600 כמוסות — אספקה ארוכה מאוד",
        "מינון מתחת לסף EFSA לאי-נוחות עיכולית",
      ],
      limitingFactors: [
        "122 מ\"ג יסודי — נמוך יחסית למוצרי ביסגליצינט בדירוג B (250 מ\"ג), כך שהציון יורד ל-C",
      ],
    },
  },
  {
    id: "7290015318532",
    name: "מגנזיום מלאט 60 כמוסות",
    brand: "טינק",
    // Source: biogaya.co.il
    imageUrl: "https://www.biogaya.co.il/media/catalog/product/7/2/7290015318532_1.jpg",
    score: 61,
    grade: "C",
    // BAV: MODERATE / ספיגה בינונית. Administered elemental: 136 mg. Form: malate.
    magnesiumBadges: mkBadge(
      136, "מלאט", "ספיגה בינונית",
      // §2
      "כללי",
      "מאומת", FLAGS_UNIVERSAL,
      // label two-line confirmed: 850mg malate compound / 136mg elemental
      'תרכובת: 850 מ"ג מלאט (מצוין על התווית) — 136 מ"ג מגנזיום אלמנטרי'
    ),
    insightLine: "מלאט ב-136 מ\"ג יושב בדיוק באמצע — נספג טוב יותר מאוקסיד, אבל לא מגיע לציטראט, וגם המינון בינוני.",
    rowVerdict:
      "מלאט נספג טוב יותר מאוקסיד אך פחות מציטראט, והמינון יושב בדיוק באמצע.",
    confidence: "partial",
    expansion: {
      nutrition: null,
      // ingredients — factual label data; verify from IL label before go-live
      ingredients: null,
      confidenceLabel: "מבוסס על נתונים חלקיים — מקור אינטרנטי",
      servingNote: "לנטילה היומית המומלצת",
      positiveSignals: [
        "מלאט — ספיגה בינונית, טובה מאוקסיד",
        "136 מ\"ג מגנזיום יסודי — מינון סביר",
      ],
      limitingFactors: [
        "מלאט — ספיגה בינונית; ציטראט וביסגליצינט נספגים טוב ממנו",
      ],
    },
  },
  {
    id: "7290001066973",
    name: "מגנזיום מלאט 90 כמוסות",
    brand: "נוטריקר",
    // Source: vitamins4all.co.il
    imageUrl: "https://vitamins4all.co.il/wp-content/uploads/2025/11/7290001066973-1.jpg",
    score: 59,
    grade: "C",
    // BAV: MODERATE / ספיגה בינונית. Administered elemental: 135 mg. Form: malate.
    // elemental_range: 133-137 (chemistry_derived_range).
    magnesiumBadges: mkBadge(
      135, "מלאט", "ספיגה בינונית",
      // §2
      "כללי",
      // label_confidence: חלקי — label declares 700mg compound only; elemental derived
      "חלקי", FLAGS_UNIVERSAL,
      // label declares compound mass only: 700mg malate; elemental ~135mg derived (×0.195)
      'תרכובת: 700 מ"ג מלאט (מצוין על התווית) — ~135 מ"ג מגנזיום אלמנטרי (חישוב כימי, טווח 133–137 מ"ג)'
    ),
    insightLine: "כמו טינק מלאט במהותו, אלא שהתווית כאן מציינת את מסת התרכובת ולא את היסודי, כך שכ-135 מ\"ג זה ערך שמתקבל מחישוב ולא נתון שמופיע ישירות על האריזה.",
    rowVerdict:
      "דומה לטינק מלאט, אך התווית מציינת את התרכובת ולא את היסודי — כך שהמינון טעון חישוב.",
    confidence: "partial",
    expansion: {
      nutrition: null,
      // ingredients — factual label data; verify from IL label before go-live
      ingredients: null,
      confidenceLabel: "מבוסס על נתונים חלקיים — טווח מחושב",
      servingNote: "לנטילה היומית המומלצת",
      positiveSignals: [
        "מלאט — ספיגה בינונית, טובה מאוקסיד",
      ],
      limitingFactors: [
        "מינון יסודי לא מוצהר ישירות על התווית — מחושב בטווח 133–137 מ\"ג",
        "מלאט — ספיגה בינונית; ציטראט וביסגליצינט נספגים טוב ממנו",
      ],
    },
  },

  // ─── D — non-UL products (score < 49.0) ─────────────────────────────────
  // Solgar UNRESOLVED form → D/48.9 (blend_dominant). Taurate D/46.2 (blend_dominant).
  {
    id: "0033984005181",
    name: "סידן ומגנזיום +D ויטמין 150 טבליות",
    brand: "סולגר",
    // Source: solgar.co.il
    imageUrl: "https://www.solgar.co.il/wp-content/uploads/2022/12/%D7%A1%D7%99%D7%93%D7%9F-%D7%95%D7%9E%D7%92%D7%A0%D7%96%D7%99%D7%95%D7%9D-%D7%91%D7%AA%D7%95%D7%A1%D7%A4%D7%AA-%D7%95%D7%99%D7%98%D7%9E%D7%99%D7%9F-D3.png",
    score: 49,
    grade: "D",
    // BAV: UNRESOLVED / הרכב לא פורט — לא ניתן להעריך ספיגה. Form: oxide_citrate_blend.
    // Elemental: 100 mg (US label only, IL unverified). Blend ratios undisclosed.
    // SOLGAR_EXCEPTION path: combination product (Ca+Mg+D3).
    magnesiumBadges: mkBadge(
      100, "תערובת (אוקסיד+ציטראט)", "הרכב לא פורט; ספיגה אינה ניתנת להערכה",
      // §2 — blend ratios unknown → cannot assess indication suitability; US label only
      "כללי בלבד — יחס הצורות לא ידוע, מינון נמוך. מבוסס על תווית ארה\"ב.",
      // label_confidence: חלקי — US label only, IL unverified; blend ratios undisclosed
      "חלקי", FLAGS_UNIVERSAL,
      // compound_mass_mg null (blend undisclosed)
      null
    ),
    insightLine: "מוצר משולב של סידן, מגנזיום ו-D3 שבו יחס הצורות לא מפורסם — ולכן אי אפשר באמת להעריך כמה מגנזיום נספג כאן.",
    rowVerdict:
      "תערובת אוקסיד-ציטראט שיחסיה לא מפורסמים — ספיגה בפועל לא ניתנת להערכה.",
    confidence: "partial",
    expansion: {
      nutrition: null,
      // ingredients — factual label data; IL label NOT verified — see confidenceLabel
      ingredients: null,
      confidenceLabel: "מבוסס על תווית ארה\"ב — תווית ישראל לא אומתה",
      servingNote: "לנטילה היומית המומלצת",
      positiveSignals: [
        "מינון המגנזיום (~100 מ\"ג) מתחת לכל גבולות הבטיחות",
      ],
      limitingFactors: [
        "יחס אוקסיד/ציטראט לא מפורסם; ספיגה בפועל אינה ניתנת להערכה",
        "מוצר משולב: הציון מתייחס למגנזיום בלבד; הסידן ו-D3 אינם בהשוואה",
        "תווית ישראלית לא אומתה — מינון מבוסס על תווית ארה\"ב",
      ],
    },
  },
  {
    id: "7290018439579",
    name: "מגנזיום טאוראט 90 כמוסות",
    brand: "נוטריקר",
    // Source: vitamins4all.co.il
    imageUrl: "https://vitamins4all.co.il/wp-content/uploads/2022/02/7290018439579.webp",
    score: 46,
    grade: "D",
    // BAV: MODERATE / ספיגה בינונית. Administered elemental: 76 mg. Form: taurate.
    magnesiumBadges: mkBadge(
      76, "טאוראט", "ספיגה בינונית",
      // §2 — 76mg < 100mg general-gap band floor
      "מינון נמוך מהנדרש לסגירת פער תזונתי משמעותי",
      // label_confidence: חלקי (retailer source)
      "חלקי", FLAGS_UNIVERSAL,
      // label two-line confirmed: 950mg taurate compound / 76mg elemental
      'תרכובת: 950 מ"ג טאוראט (מצוין על התווית) — 76 מ"ג מגנזיום אלמנטרי'
    ),
    insightLine: "טאוראט בספיגה בינונית, אבל עם 76 מ\"ג יסודי המינון נמוך מרוב המדף — קטן מדי כדי לסגור פער משמעותי.",
    rowVerdict:
      "טאוראט עם ספיגה בינונית ו-76 מ\"ג יסודי — שילוב חלש בקטגוריה הזו.",
    confidence: "partial",
    expansion: {
      nutrition: null,
      // ingredients — factual label data; verify from IL label before go-live
      ingredients: null,
      confidenceLabel: "מבוסס על נתונים חלקיים — מקור אינטרנטי",
      servingNote: "לנטילה היומית המומלצת",
      positiveSignals: [
        "מינון מתחת לסף EFSA לאי-נוחות עיכולית",
      ],
      limitingFactors: [
        "76 מ\"ג יסודי — נמוך יחסית לרוב המוצרים בקטגוריה",
        "טאוראט — ספיגה בינונית; ציטראט וביסגליצינט נספגים טוב ממנו",
      ],
    },
  },

  // ─── D — UL_EXCEED products (4 oxide products, all score 49.0) ──────────
  // All four: binding_constraint = ul_exceed_grade_ceiling_D.
  // VISIBLE safety block REQUIRED (spec requirement 4) — NOT a tooltip.
  // Dose vs limit: "520 מ\"ג — כ-1.5× מעל הגבול העליון המומלץ לתוסף (350 מ\"ג)"
  //                "450 מ\"ג — כ-1.3× מעל הגבול העליון המומלץ לתוסף (350 מ\"ג)"
  // Framing: GI-tolerance-not-toxicity (IOM/NASEM).
  // Oxide elemental note: 520 mg = elemental (panel-verified IL label). Prior 314 mg REFUTED.
  //
  // bandNote on first UL_EXCEED product to signal the sub-group.
  {
    id: "7290001065662",
    name: "מגנזיום אוקסיד 520 100 כמוסות",
    brand: "נוטריקר",
    // Source: vitamins4all.co.il
    imageUrl: "https://vitamins4all.co.il/wp-content/uploads/2024/05/7290001065662.webp",
    score: 49,
    grade: "D",
    // BAV: LOW / ספיגה נמוכה יחסית. Administered elemental: 520 mg (panel-verified).
    // UL_EXCEED: 520 mg > 350 mg IOM/NASEM supplemental UL.
    // SAFETY BLOCK — VISIBLE (requirement 4). GI-tolerance-not-toxicity framing.
    bandNote: "המוצרים הבאים מכילים מגנזיום מעל הגבול העליון המומלץ לתוספים (350 מ\"ג/יום, IOM/NASEM) — ראו אזהרה בכל מוצר",
    // SAFETY BLOCK (visible, collapsed row): requirement 4. Dose vs limit stated.
    claimShortfallFlag: "520 מ\"ג — כ-1.5× מעל הגבול העליון המומלץ לתוסף (350 מ\"ג)",
    magnesiumBadges: mkBadge(
      520, "אוקסיד", "ספיגה נמוכה יחסית",
      // §2 — UL-exceed → risk flag only
      "מינון מעל הגבול המומלץ לתוספים. עיקר ההשפעה — עיכולית.",
      // panel-verified elemental
      "מאומת", FLAGS_UL_EXCEED,
      // back-calculated: 520/0.6031 = ~862mg MgO; label states 520mg elemental directly
      'תרכובת: ~862 מ"ג אוקסיד מגנזיום (חישוב לאחר) — 520 מ"ג מגנזיום יסודי לפי הכתוב על התווית (אומת)'
    ),
    insightLine: "הפורמולה הנפוצה ביותר, וגם המטעה ביותר: 520 מ\"ג אוקסיד נשמע הרבה, אבל זו הצורה שנספגת הכי פחות והמינון חוצה את התקרה המומלצת לתוספים.",
    rowVerdict:
      "הפורמולה הנפוצה ביותר — אוקסיד נספג פחות, אז הספרה הגדולה מטעה.",
    confidence: "verified",
    expansion: {
      nutrition: null,
      // ingredients — factual label data; IL label panel-verified per TASK-384
      ingredients: null,
      confidenceLabel: "מבוסס על נתוני לוח אחורי — ישיר מהמוצר",
      servingNote: "לנטילה היומית המומלצת",
      positiveSignals: [],
      limitingFactors: [
        "אוקסיד — ספיגה נמוכה יחסית בהשוואה לציטראט ולביסגליצינט",
        "520 מ\"ג — כ-1.5× מעל הגבול העליון המומלץ לתוספים (IOM/NASEM 350 מ\"ג/יום)",
      ],
      // SAFETY BLOCK — visible per requirement 4. GI-tolerance-not-toxicity framing.
      caveats: [
        "אזהרת מינון: 520 מ\"ג יסודי ביום עולה על הגבול העליון המומלץ לתוספי מגנזיום (350 מ\"ג/יום, IOM/NASEM). באנשים בריאים החשש העיקרי הוא אי-נוחות עיכולית; באנשים עם מחלת כליות או שימוש בתרופות מסוימות נדרש ייעוץ רפואי.",
      ],
    },
  },
  {
    id: "7290017218564",
    name: "מגנזיום 520 60 כמוסות",
    brand: "אלטמן",
    // Source: vitamins4all.co.il
    imageUrl: "https://vitamins4all.co.il/wp-content/uploads/2024/08/7290017218564-2.webp",
    score: 49,
    grade: "D",
    // BAV: LOW / ספיגה נמוכה יחסית. Administered elemental: 520 mg (panel-verified).
    // UL_EXCEED: 520 mg > 350 mg IOM/NASEM supplemental UL.
    // SAFETY BLOCK (visible, collapsed row): requirement 4.
    claimShortfallFlag: "520 מ\"ג — כ-1.5× מעל הגבול העליון המומלץ לתוסף (350 מ\"ג)",
    magnesiumBadges: mkBadge(
      520, "אוקסיד", "ספיגה נמוכה יחסית",
      "מינון מעל הגבול המומלץ לתוספים. עיקר ההשפעה — עיכולית.",
      // NRV%-verified from label image (altman520.webp)
      "מאומת", FLAGS_UL_EXCEED,
      'תרכובת: ~862 מ"ג אוקסיד מגנזיום (חישוב לאחר) — 520 מ"ג מגנזיום יסודי לפי הכתוב על התווית (אומת NRV%)'
    ),
    insightLine: "520 נראה מרשים על האריזה, אבל זו דווקא הצורה שנספגת הכי פחות במדף — ובמינון הזה היא כבר מעל הגבול המומלץ לתוספים.",
    rowVerdict:
      "520 מרשים על האריזה — אבל אוקסיד הוא הצורה שנספגת הכי פחות בקטגוריה.",
    confidence: "verified",
    expansion: {
      nutrition: null,
      // ingredients — factual label data; IL label panel-verified per TASK-384
      ingredients: null,
      confidenceLabel: "מבוסס על נתוני לוח אחורי — ישיר מהמוצר",
      servingNote: "לנטילה היומית המומלצת",
      positiveSignals: [],
      limitingFactors: [
        "אוקסיד — ספיגה נמוכה יחסית בהשוואה לציטראט ולביסגליצינט",
        "520 מ\"ג — כ-1.5× מעל הגבול העליון המומלץ לתוספים (IOM/NASEM 350 מ\"ג/יום)",
      ],
      // SAFETY BLOCK — visible per requirement 4. GI-tolerance-not-toxicity framing.
      caveats: [
        "אזהרת מינון: 520 מ\"ג יסודי ביום עולה על הגבול העליון המומלץ לתוספי מגנזיום (350 מ\"ג/יום, IOM/NASEM). באנשים בריאים החשש העיקרי הוא אי-נוחות עיכולית; באנשים עם מחלת כליות או שימוש בתרופות מסוימות נדרש ייעוץ רפואי.",
      ],
    },
  },
  {
    id: "7290013142894",
    name: "מגנזיום UP 60 כמוסות",
    brand: "אלטמן",
    // Source: altman.co.il
    imageUrl: "https://www.altman.co.il/wp-content/uploads/batc/_i/bd7e8878-3115-4e63-9646-d28e5d617979.webp",
    score: 49,
    grade: "D",
    // BAV: LOW / ספיגה נמוכה יחסית. Administered elemental: 450 mg (panel-verified).
    // UL_EXCEED: 450 mg > 350 mg IOM/NASEM supplemental UL.
    // SAFETY BLOCK (visible, collapsed row): requirement 4.
    claimShortfallFlag: "450 מ\"ג — כ-1.3× מעל הגבול העליון המומלץ לתוסף (350 מ\"ג)",
    magnesiumBadges: mkBadge(
      450, "אוקסיד", "ספיגה נמוכה יחסית",
      "מינון מעל הגבול המומלץ לתוספים. הצמחים לא הוערכו בהשוואה זו.",
      // label two-line confirmed: 750mg MgO compound / 450mg elemental (magup.webp)
      "מאומת", FLAGS_UL_EXCEED,
      'תרכובת: 750 מ"ג אוקסיד מגנזיום (מצוין על התווית) — 450 מ"ג מגנזיום יסודי (אומת NRV%)'
    ),
    insightLine: "השם אומר UP, אבל מה שמעלה את ערך המגנזיום זו הצורה ולא הכמות — וכאן מדובר באוקסיד ב-450 מ\"ג, מעל התקרה המומלצת לתוספים.",
    rowVerdict:
      "השם מבטיח UP, אבל את ערך המגנזיום קובעת הצורה ולא הכמות — וכאן הבסיס הוא אוקסיד.",
    confidence: "verified",
    expansion: {
      nutrition: null,
      // ingredients — factual label data; IL label panel-verified per TASK-384
      ingredients: null,
      confidenceLabel: "מבוסס על נתוני לוח אחורי — ישיר מהמוצר",
      servingNote: "לנטילה היומית המומלצת",
      positiveSignals: [],
      limitingFactors: [
        "אוקסיד — ספיגה נמוכה יחסית בהשוואה לציטראט ולביסגליצינט",
        "450 מ\"ג — כ-1.3× מעל הגבול העליון המומלץ לתוספים (IOM/NASEM 350 מ\"ג/יום)",
      ],
      // SAFETY BLOCK — visible per requirement 4. GI-tolerance-not-toxicity framing.
      caveats: [
        "אזהרת מינון: 450 מ\"ג יסודי ביום עולה על הגבול העליון המומלץ לתוספי מגנזיום (350 מ\"ג/יום, IOM/NASEM). באנשים בריאים החשש העיקרי הוא אי-נוחות עיכולית; באנשים עם מחלת כליות או שימוש בתרופות מסוימות נדרש ייעוץ רפואי.",
      ],
    },
  },
  {
    id: "7290019444206",
    name: "מגנזיום באלאנס 60 כמוסות",
    brand: "אלטמן",
    // Source: vitamins4all.co.il
    imageUrl: "https://vitamins4all.co.il/wp-content/uploads/2025/05/7290019444206.webp",
    score: 49,
    grade: "D",
    // BAV: LOW / ספיגה נמוכה יחסית. Administered elemental: 450 mg (panel-verified).
    // UL_EXCEED: 450 mg > 350 mg IOM/NASEM supplemental UL.
    // SAFETY BLOCK (visible, collapsed row): requirement 4.
    claimShortfallFlag: "450 מ\"ג — כ-1.3× מעל הגבול העליון המומלץ לתוסף (350 מ\"ג)",
    magnesiumBadges: mkBadge(
      450, "אוקסיד", "ספיגה נמוכה יחסית",
      "מינון מעל הגבול המומלץ לתוספים. הצמחים לא הוערכו בהשוואה זו.",
      // NRV%-verified from label image (balance.webp)
      "מאומת", FLAGS_UL_EXCEED,
      'תרכובת: ~747 מ"ג אוקסיד מגנזיום (חישוב לאחר) — 450 מ"ג מגנזיום יסודי לפי הכתוב על התווית (אומת NRV%)'
    ),
    insightLine: "האשווגנדה והוולריאן הם בעיקר שיווק — הבסיס נשאר אוקסיד ב-450 מ\"ג, ספיגה נמוכה ומינון מעל הגבול המומלץ לתוספים.",
    rowVerdict:
      "האשווגנדה והולריאן הם שיווק — הבסיס הוא עדיין אוקסיד עם ספיגה נמוכה.",
    confidence: "verified",
    expansion: {
      nutrition: null,
      // ingredients — factual label data; IL label panel-verified per TASK-384
      ingredients: null,
      confidenceLabel: "מבוסס על נתוני לוח אחורי — ישיר מהמוצר",
      servingNote: "לנטילה היומית המומלצת",
      positiveSignals: [],
      limitingFactors: [
        "אוקסיד — ספיגה נמוכה יחסית בהשוואה לציטראט ולביסגליצינט",
        "450 מ\"ג — כ-1.3× מעל הגבול העליון המומלץ לתוספים (IOM/NASEM 350 מ\"ג/יום)",
        "אשווגנדה ולריאן — צמחים שאינם משנים את הספיגה או כמות המגנזיום היסודי",
      ],
      // SAFETY BLOCK — visible per requirement 4. GI-tolerance-not-toxicity framing.
      caveats: [
        "אזהרת מינון: 450 מ\"ג יסודי ביום עולה על הגבול העליון המומלץ לתוספי מגנזיום (350 מ\"ג/יום, IOM/NASEM). באנשים בריאים החשש העיקרי הוא אי-נוחות עיכולית; באנשים עם מחלת כליות או שימוש בתרופות מסוימות נדרש ייעוץ רפואי.",
      ],
    },
  },

  // ─── E (1 product) ───────────────────────────────────────────────────────
  // Nutricare Nano: cap_1_insufficient_evidence. binding_constraint = cap_1.
  // Score capped at 34.0. "nano liposomal" claim insufficient evidence.
  {
    id: "7290001065594",
    name: "נאנו מגנזיום ליפוזומלי 60 כמוסות",
    brand: "נוטריקר",
    // Source: vitamins4all.co.il
    imageUrl: "https://vitamins4all.co.il/wp-content/uploads/2024/07/%D7%A0%D7%90%D7%A0%D7%95-%D7%9E%D7%92%D7%A0%D7%96%D7%99%D7%95%D7%9D-Copy.webp",
    score: 34,
    grade: "E",
    // BAV: HIGH class for base form (bisglycinate). Administered elemental: 88 mg.
    // cap_1_insufficient_evidence: "נאנו ליפוזומלי" claim → insufficient evidence.
    // HARD: do NOT show absorbed figures. This is a cap_1 product.
    magnesiumBadges: mkBadge(
      88, "ביסגליצינט", "ספיגה גבוהה יחסית (צורת בסיס)",
      // §2 — nano claim unknown modifier → cannot assess; dose too low
      "הטענה לטכנולוגיה ייחודית לא הוכחה; מינון נמוך. התאמה אינה ניתנת להערכה.",
      "מאומת", FLAGS_UNIVERSAL,
      // back-calculated: 88/0.1410 = ~624mg bisglycinate compound; label states 88mg elemental
      'תרכובת: ~624 מ"ג ביסגליצינט (חישוב לאחר) — 88 מ"ג מגנזיום יסודי לפי הכתוב על התווית'
    ),
    insightLine: "כל הסיפור כאן בנוי על טענת 'נאנו ליפוזומלי' שלא עומדת בבדיקת הראיות — ומתחתיה רק 88 מ\"ג ביסגליצינט, מינון נמוך.",
    rowVerdict:
      "כל הטיעון בנוי על הטכנולוגיה הנאנו-ליפוזומלית — שלא עמדה בבדיקת הראיות.",
    confidence: "partial",
    expansion: {
      nutrition: null,
      // ingredients — factual label data; verify from IL label before go-live
      ingredients: null,
      confidenceLabel: "מבוסס על נתונים חלקיים — מקור אינטרנטי",
      servingNote: "לנטילה היומית המומלצת",
      positiveSignals: [],
      limitingFactors: [
        "טענת 'נאנו ליפוזומלי': עדות מדעית מספקת לשיפור ספיגה לא נמצאה",
        "88 מ\"ג מגנזיום יסודי — מינון נמוך ביחס לשאר הקטגוריה, גם ללא הספק בטענה",
      ],
    },
  },

  // ─── UNRESOLVED (3 products) — "לא ניתן לדרג — נתוני תווית חסרים" ──────
  // score: null, grade: null. Clean card — no broken display.
  // Per spec requirement 6: render cleanly, no fake grade, no blank/broken card.
  {
    id: "7290015318426",
    name: "מגנזיום אוקסיד 520 90 כמוסות",
    brand: "טינק",
    // Source: tinc.co.il
    imageUrl: "https://www.tinc.co.il/GoopSitesFiles/83206/User/catalog_941469-l.jpg?637595154336530000",
    score: null,
    grade: null,
    // UNRESOLVED: label declares "520 מ\"ג מגנזיום אוקסיד" without elemental qualifier.
    // insightLine — unresolved framing
    magnesiumBadges: mkBadge(
      null, "אוקסיד", "הרכב לא פורט; ספיגה אינה ניתנת להערכה",
      // §2 — UNRESOLVED — cannot assess
      "הרכב לא ידוע; התאמה אינה ניתנת להערכה",
      // label_confidence: לא ניתן לחישוב
      "לא ניתן לחישוב",
      // UNRESOLVED: no elemental dose → no flags
      FLAGS_UNRESOLVED
    ),
    insightLine: "לא ניתן לדרג, כי התווית לא מבהירה אם 520 מ\"ג הם מגנזיום יסודי או אוקסיד, וההבדל הזה משנה הכול.",
    rowVerdict:
      "לא ניתן לדרג — האם 520 מ\"ג הם יסודי או אוקסיד? המינון לא ניתן לאימות.",
    confidence: "insufficient",
    expansion: {
      nutrition: null,
      ingredients: null,
      confidenceLabel: "לא ניתן לדרג — נתוני תווית חסרים",
      servingNote: "לנטילה היומית המומלצת",
      limitingFactors: [
        "התווית אינה מציינת 'From Magnesium Oxide' — מינון המגנזיום היסודי אינו ניתן לאימות",
      ],
    },
  },
  {
    id: "7290015429245",
    name: "pH מגנזיום 60 קפסולות",
    brand: "אמורפיקיור",
    // Source: vitamins4all.co.il
    imageUrl: "https://vitamins4all.co.il/wp-content/uploads/2023/12/7290015429245-1.jpg",
    score: null,
    grade: null,
    // UNRESOLVED: 160 mg elemental-vs-compound ambiguous (carbonate 0.288 fraction). ~3.5x uncertainty.
    magnesiumBadges: mkBadge(
      null, "קרבונט", "הרכב לא פורט; ספיגה אינה ניתנת להערכה",
      "הרכב לא ידוע; התאמה אינה ניתנת להערכה",
      "לא ניתן לחישוב",
      FLAGS_UNRESOLVED
    ),
    insightLine: "לא ניתן לדרג — 160 מ\"ג שיכולים להיות יסודי או תרכובת, פער שמגיע עד פי 3.5.",
    rowVerdict:
      "לא ניתן לדרג — 160 מ\"ג: יסודי או תרכובת? הפער מגיע לפי 3.5.",
    confidence: "insufficient",
    expansion: {
      nutrition: null,
      ingredients: null,
      confidenceLabel: "לא ניתן לדרג — נתוני תווית חסרים",
      servingNote: "לנטילה היומית המומלצת",
      limitingFactors: [
        "התווית אינה מבהירה האם '160 מ\"ג' הוא מגנזיום יסודי או קרבונט — אי-בהירות עצומה במינון",
      ],
    },
  },
  {
    id: "7290118816065",
    name: "TRIOMAG מגנזיום 60 כמוסות",
    brand: "סופהרב",
    // Source: vitamins4all.co.il
    imageUrl: "https://vitamins4all.co.il/wp-content/uploads/2026/01/7290118816065-1.jpg",
    score: null,
    grade: null,
    // UNRESOLVED: 200 mg likely elemental but unconfirmed; form ratios undisclosed.
    magnesiumBadges: mkBadge(
      null, "תערובת (ציטראט+ביסגליצינט+טאוראט)", "הרכב לא פורט; ספיגה אינה ניתנת להערכה",
      "הרכב לא ידוע; התאמה אינה ניתנת להערכה",
      "לא ניתן לחישוב",
      FLAGS_UNRESOLVED
    ),
    insightLine: "לא ניתן לדרג — שלוש צורות בתערובת אחת שיחסיהן לא פורסמו, כך שאי אפשר להעריך כמה באמת נספג.",
    rowVerdict:
      "לא ניתן לדרג — יחסי שלוש הצורות לא פורסמו; ספיגה לא ניתנת להערכה.",
    confidence: "insufficient",
    expansion: {
      nutrition: null,
      ingredients: null,
      confidenceLabel: "לא ניתן לדרג — נתוני תווית חסרים",
      servingNote: "לנטילה היומית המומלצת",
      limitingFactors: [
        "פיצול שלוש הצורות (ציטראט / ביסגליצינט / טאוראט) לא מפורסם; ספיגה בפועל אינה ניתנת להערכה",
      ],
    },
  },
];

export const magnesiumProducts: BariProductVM[] = magnesiumProductsRaw.map((product) =>
  normalizeProductBrandDisplay(product)
);

// Supherb Max 550 (7290118818205) — DISCARDED. Missing-data discard rule. NOT displayed.
