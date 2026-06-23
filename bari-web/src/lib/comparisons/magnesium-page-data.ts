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
// All consumer strings marked [PLACEHOLDER] — Content two-gate required before go-live.

import type { BariProductVM } from "@/lib/view-models";

// ─── Copy (PLACEHOLDER — awaiting Content two-gate sign-off) ─────────────────

export const magnesiumHero = {
  eyebrow: "תוספי מגנזיום",
  title: "קונים תוסף מגנזיום? הנה מה שהמספר הגדול על האריזה לא אומר לכם",
} as const;

// 18 displayed: 15 scored + 3 no-score. Updated to v3 run date.
export const magnesiumMetadataLine = "18 מוצרים · יוני 2026";

export const magnesiumPrologueSentences = [
  "בדקנו 18 תוספי מגנזיום מהמדף הישראלי לפי שני פרמטרים: כמה מגנזיום יסודי המוצר מספק ביום, ובאיזו צורה כימית — כי שני הדברים קובעים יחד את הערך בפועל.",
  "הצורה הכימית חשובה כי ציטראט וביסגליצינט נספגים טוב יותר מאוקסיד, אבל מינון קטן מדי גם בצורה טובה ייתן פחות מגנזיום בסוף היום — ולכן שני הפרמטרים הוצלבו יחד לציון אחד.",
  "ארבעה מוצרים מכילים 450 עד 520 מ\"ג מגנזיום יסודי ליום — מעל הגבול העליון המומלץ לתוספים (350 מ\"ג/יום, IOM/NASEM). הגבול הזה עניינו נוחות העיכול בלבד; אין כאן חשש רעילות. בכל זאת, מוצרים אלה מקבלים ציון D ואזהרת מינון ברורה.",
  "שלושה מוצרים לא קיבלו ציון — התווית שלהם לא מאפשרת חישוב מינון אמין, וזה עצמו מידע שכדאי לדעת לפני שרוכשים.",
] as const;

export const magnesiumCategoryNote =
  "איך נקבע הציון — וביחס למה\n\n" +
  "הציון משקף כמה מגנזיום יסודי המוצר מספק ביום לפי התווית, ובאיזו צורה כימית — כי צורות שנספגות טוב יותר (ציטראט, ביסגליצינט) נותנות ערך גבוה יותר ממינון זהה של אוקסיד, שנספג פחות. ציון גבוה פירושו מינון משמעותי בצורה עם ספיגה גבוהה יחסית.\n\n" +
  "ארבעה מוצרים מכילים מגנזיום מעל 350 מ\"ג ליום — הגבול העליון המומלץ לתוספים של IOM/NASEM. חשוב להבין: גבול זה עניינו נוחות העיכול בלבד; עודף מגנזיום מתוסף עלול לגרום לאי-נוחות עיכולית בחלק מהאנשים, וזו אינה שאלה של רעילות. בכל זאת, מוצרים אלה מקבלים ציון D ואזהרת מינון ברורה — הגבול חל על תוספים בלבד; מגנזיום שמגיע מהמזון אינו נספר.\n\n" +
  "שלושה מוצרים מוצגים ללא ציון כי התווית שלהם לא מאפשרת חישוב מינון אמין — בין אם מינון לא מוגדר כ'יסודי', בין אם הרכב הצורות לא פורסם. מדובר במגבלת נתונים בלבד; המוצר עצמו לא נפסל.\n\n" +
  "הערת קטגוריה — מה חשוב לדעת לפני שבוחרים\n\n" +
  "ברי קוראת תוויות — לא בודקת במעבדה. כל המינונים המוצגים הם מה שכתוב על האריזה הישראלית. המידע כאן הוא לצורך הכרה בלבד, ולא תחליף לייעוץ רפואי.";

export const magnesiumMethodologyLines = [
  "בדקנו 18 תוספי מגנזיום מהמדף הישראלי לפי שלושה פרמטרים: כמות המגנזיום היסודי לנטילה היומית המומלצת, הצורה הכימית ורמת הספיגה שלה, ושקיפות התיוג.",
  "הציון שוקלל מהמינון היסודי (55%), מהצורה הכימית ועדות הספיגה (20%), ומשקיפות התיוג (25%) — כך שמוצר עם צורה טובה ומינון קטן לא מקבל ציון גבוה, ומוצר עם מינון גבוה בצורה פחות נספגת לא מקבל ציון כאילו הכמות על האריזה היא כל הסיפור.",
  "מוצרים עם מינון מעל 350 מ\"ג יסודי ליום (הגבול העליון המומלץ לתוספים של IOM/NASEM) מקבלים תקרת ציון D עם אזהרת מינון ברורה — ללא קשר לאיכות הצורה הכימית.",
  "מוצרים שנושאים טענת ספיגה שאינה נתמכת בעדות מדעית מספקת מקבלים ציון E.",
] as const;

// ─── Products (BariProductVM[]) ──────────────────────────────────────────────
// Sort: score desc. Within grade: score desc. UL_EXCEED products (all tie at 49.0/D)
// sorted after non-UL D products. UNRESOLVED appended after all scored.
// Discarded product (Supherb Max 550) NOT shown per spec.
//
// imageUrl: brand/retailer sites only. NO Open Food Facts. NO OFF.
// All consumer strings marked [PLACEHOLDER] — Content two-gate required.

export const magnesiumProducts: BariProductVM[] = [
  // ─── B (4 products) ──────────────────────────────────────────────────────
  // Sort: score desc. 72.8 tie → Supherb first (citrate, 250mg), Altman bisgly second.
  {
    id: "7290013464248",
    name: "סופהרב מגנזיום ציטראט+B6 בדץ 60 טבליות",
    // Source: teva-call.co.il
    imageUrl: "https://www.teva-call.co.il/wp-content/uploads/2015/11/7290013464248-510x510.webp",
    score: 73,
    grade: "B",
    // BAV: HIGH / ספיגה גבוהה יחסית. Administered elemental: 250 mg. Form: citrate.
    // GI_NOTE_EFSA: 250 mg >= EFSA GI onset threshold (display only, no score deduction).
    insightLine: "250 מ\"ג ציטראט — מינון גבוה בצורה עם ספיגה גבוהה יחסית. ציון B.",
    rowVerdict:
      "מדובר בציטראט מגנזיום עם 250 מ\"ג יסודי ליום — שילוב של מינון גבוה וצורה עם ספיגה גבוהה יחסית; בזכות זה הוא מוביל בקטגוריה. כשרות בדץ. יחד עם זאת, EFSA קבעה ש-250 מ\"ג מגנזיום תוסף ביום הוא הסף שבו חלק מהאנשים עלולים לחוש אי-נוחות עיכולית — כדאי לדעת.",
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
    name: "אלטמן מגנזיום ביסגליצינט 250 קפליות",
    // Source: vitamins4all.co.il
    imageUrl: "https://vitamins4all.co.il/wp-content/uploads/2026/01/7290019444480.png",
    score: 73,
    grade: "B",
    // BAV: HIGH / ספיגה גבוהה יחסית. Administered elemental: 250 mg. Form: bisglycinate.
    // GI_NOTE_EFSA: 250 mg >= EFSA GI onset threshold (display only, no score deduction).
    insightLine: "250 מ\"ג ביסגליצינט — ספיגה גבוהה יחסית, ידידותי יחסית לקיבה. ציון B.",
    rowVerdict:
      "ביסגליצינט נסבלת בדרך כלל טוב יותר על ידי מערכת העיכול, כך שהיתרון כאן כפול: 250 מ\"ג יסודי בצורה עם ספיגה גבוהה יחסית שגם נוחה יחסית לקיבה. יחד עם זאת, EFSA קבעה ש-250 מ\"ג מגנזיום תוסף ביום הוא הסף שמתחתיו אי-נוחות עיכולית נדירה — גם מוצר זה נמצא בסף.",
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
    name: "אלטמן מגנזיום ציטראט 120 קפליות",
    // Source: vitamins4all.co.il
    imageUrl: "https://vitamins4all.co.il/wp-content/uploads/2020/08/7290011899967.jpg",
    score: 69,
    grade: "B",
    // BAV: HIGH / ספיגה גבוהה יחסית. Administered elemental: 200 mg. Form: citrate.
    insightLine: "200 מ\"ג ציטראט — ספיגה גבוהה יחסית, מתחת לסף EFSA. ציון B.",
    rowVerdict:
      "ציטראט 200 מ\"ג יסודי — מינון טוב בצורה עם ספיגה גבוהה יחסית, ומתחת לסף ה-250 מ\"ג שעליו EFSA ציינה אפשרות לאי-נוחות עיכולית. 120 קפליות הן אספקה ארוכה יחסית בקטגוריה הזאת.",
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
    name: "נוטריקר מגנזיום WELL כמוסות 90",
    // Source: vitamins4all.co.il
    imageUrl: "https://vitamins4all.co.il/wp-content/uploads/2020/09/7290018439043.png",
    score: 66,
    grade: "B",
    // BAV: HIGH / ספיגה גבוהה יחסית. Administered elemental: 168 mg. Form: bisglycinate.
    // cap_1 NOT fired — WELL is line branding, not a delivery-mechanism claim (v3 ruling).
    insightLine: "168 מ\"ג ביסגליצינט — ספיגה גבוהה יחסית, מינון סביר. ציון B.",
    rowVerdict:
      "ביסגליצינט 168 מ\"ג יסודי — צורה עם ספיגה גבוהה יחסית במינון סביר. המינון נמוך מעט מהמוצרים הראשונים בדירוג, כך שהציון B משקף מינון B ולא A. 'WELL' הוא שם קו המוצרים של נוטריקר בלבד; הוא אינו מציין ספיגה עדיפה על פני ביסגליצינט רגיל.",
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
    name: "NT L.C. כמוסות מגנזיום אנטי לג קרמפס",
    // Source: vitamins4all.co.il
    imageUrl: "https://vitamins4all.co.il/wp-content/uploads/2021/01/7290010207640.png",
    score: 64,
    grade: "C",
    // BAV: MODERATE / ספיגה בינונית. Administered elemental: 190 mg. Form: hydroxide.
    // cramps_footnote: claims not supported by Cochrane 2020 — carry as limiting factor.
    insightLine: "190 מ\"ג הידרוקסיד — ספיגה בינונית. טענת העוויתות לא מגובה במחקר. ציון C.",
    rowVerdict:
      "הידרוקסיד מגנזיום הוא צורה עם ספיגה בינונית — לא גרועה, אבל מתחת לציטראט ולביסגליצינט. הציון C כאן נובע מהצורה הכימית ולא מהמינון. אומנם 190 מ\"ג יסודי הוא מינון סביר, אבל הטענה הכתובה על האריזה בנוגע לעזרה בעוויתות שרירים לא נתמכת בסקירת קוקריין 2020 (PMID 32956536), שבחנה בדיוק את השאלה הזאת ולא מצאה תועלת.",
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
    name: "פול-מג הדס ביסגליצינט 600 כמוסות",
    // Source: vitamins4all.co.il — using existing image URL pattern for this barcode
    imageUrl: null,
    score: 62,
    grade: "C",
    // BAV: HIGH / ספיגה גבוהה יחסית. Administered elemental: 122 mg. Form: bisglycinate.
    insightLine: "ביסגליצינט — צורה טובה, אבל 122 מ\"ג יסודי הם מתחת לציון B. ציון C.",
    rowVerdict:
      "זה המקרה שבו הצורה הכימית לא מספיקה לבדה. ביסגליצינט היא צורה עם ספיגה גבוהה יחסית — אותה צורה שנמצאת בראשוני הדירוג — אבל 122 מ\"ג יסודי ביום הם מינון נמוך יחסית לאותה צורה, ולכן הציון יורד ל-C. 600 כמוסות הן אספקה ארוכה מאוד, אבל המינון הוא שקובע כאן.",
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
    name: "טינק מגנזיום מלאט 60 כמוסות",
    // Source: biogaya.co.il
    imageUrl: "https://www.biogaya.co.il/media/catalog/product/7/2/7290015318532_1.jpg",
    score: 61,
    grade: "C",
    // BAV: MODERATE / ספיגה בינונית. Administered elemental: 136 mg. Form: malate.
    insightLine: "136 מ\"ג מלאט — ספיגה בינונית, מינון בינוני. ציון C.",
    rowVerdict:
      "מלאט מגנזיום היא צורה עם ספיגה בינונית — טובה יותר מאוקסיד, אבל לא מגיעה לרמת הציטראט או הביסגליצינט. 136 מ\"ג יסודי ביום הם מינון סביר לצורה בינונית, ולכן הציון C מגיע משני הכיוונים יחד.",
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
    name: "נוטריקר מגנזיום מלאט 90 כמוסות",
    // Source: vitamins4all.co.il
    imageUrl: "https://vitamins4all.co.il/wp-content/uploads/2025/11/7290001066973-1.jpg",
    score: 59,
    grade: "C",
    // BAV: MODERATE / ספיגה בינונית. Administered elemental: 135 mg. Form: malate.
    // elemental_range: 133-137 (chemistry_derived_range).
    insightLine: "כ-135 מ\"ג מלאט — ספיגה בינונית, מינון יסודי לא מוצהר ישירות. ציון C.",
    rowVerdict:
      "מלאט מגנזיום עם ספיגה בינונית ומינון דומה מאוד למוצר הקודם בדירוג — ההבדל הוא שהמינון היסודי כאן אינו מוצהר ישירות על התווית הישראלית, ונגזר מחישוב כימי לטווח 133–137 מ\"ג. בפועל המוצר ממוצב דומה לקודמו, אבל שקיפות התיוג נמוכה מעט יותר.",
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
    name: "סולגר סידן ומגנזיום +D ויטמין 150 טבליות",
    // Source: solgar.co.il
    imageUrl: "https://www.solgar.co.il/wp-content/uploads/2022/12/%D7%A1%D7%99%D7%93%D7%9F-%D7%95%D7%9E%D7%92%D7%A0%D7%96%D7%99%D7%95%D7%9D-%D7%91%D7%AA%D7%95%D7%A1%D7%A4%D7%AA-%D7%95%D7%99%D7%98%D7%9E%D7%99%D7%9F-D3.png",
    score: 49,
    grade: "D",
    // BAV: UNRESOLVED / הרכב לא פורט — לא ניתן להעריך ספיגה. Form: oxide_citrate_blend.
    // Elemental: 100 mg (US label only, IL unverified). Blend ratios undisclosed.
    // SOLGAR_EXCEPTION path: combination product (Ca+Mg+D3).
    insightLine: "מוצר משולב (סידן, מגנזיום, D3) — יחס הצורות לא מפורסם; ספיגה אינה ניתנת להערכה. ציון D.",
    rowVerdict:
      "זהו מוצר משולב שכולל סידן, מגנזיום וויטמין D3 — הציון מתייחס רק לרכיב המגנזיום. הבעיה כאן אינה המותג, אלא שהתווית הישראלית לא מפרסמת את יחס האוקסיד לציטראט בתערובת, כך שאי אפשר להעריך כמה מגנזיום נספג בפועל. מוצר ייעודי לתוסף מגנזיום יאפשר ודאות גדולה יותר.",
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
    name: "נוטריקר מגנזיום טאוראט 90 כמוסות",
    // Source: vitamins4all.co.il
    imageUrl: "https://vitamins4all.co.il/wp-content/uploads/2022/02/7290018439579.webp",
    score: 46,
    grade: "D",
    // BAV: MODERATE / ספיגה בינונית. Administered elemental: 76 mg. Form: taurate.
    insightLine: "76 מ\"ג טאוראט — מינון נמוך מרוב המוצרים בקטגוריה. ציון D.",
    rowVerdict:
      "טאוראט מגנזיום הוא צורה עם ספיגה בינונית — בעצמה לא הבעיה — אבל 76 מ\"ג יסודי ביום הם מינון נמוך ביחס לשאר הקטגוריה. מוצר עם צורה בינונית ומינון מתחת לחלק ניכר מהמוצרים הקיימים נמצא בתחתית הדירוג.",
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
    name: "נוטריקר מגנזיום אוקסיד 520 100 כמוסות",
    // Source: vitamins4all.co.il
    imageUrl: "https://vitamins4all.co.il/wp-content/uploads/2024/05/7290001065662.webp",
    score: 49,
    grade: "D",
    // BAV: LOW / ספיגה נמוכה יחסית. Administered elemental: 520 mg (panel-verified).
    // UL_EXCEED: 520 mg > 350 mg IOM/NASEM supplemental UL.
    // SAFETY BLOCK — VISIBLE (requirement 4). GI-tolerance-not-toxicity framing.
    bandNote: "המוצרים הבאים מכילים מגנזיום מעל הגבול העליון המומלץ לתוספים (350 מ\"ג/יום, IOM) — ראו אזהרה בכל מוצר",
    // SAFETY BLOCK (visible, collapsed row): requirement 4. Dose vs limit stated.
    claimShortfallFlag: "520 מ\"ג — כ-1.5× מעל הגבול העליון המומלץ לתוסף (350 מ\"ג)",
    insightLine: "אוקסיד 520 מ\"ג יסודי — ספיגה נמוכה יחסית ומינון מעל הגבול המומלץ לתוספים. ציון D עם אזהרת מינון.",
    rowVerdict:
      "אוקסיד מגנזיום הוא הצורה הנפוצה ביותר בתוספים זולים, ויחד עם זאת הצורה עם הספיגה הנמוכה ביותר בקטגוריה. 520 מ\"ג יסודי ביום — כ-1.5 פעם מעל הגבול העליון המומלץ לתוספים (350 מ\"ג/יום, IOM/NASEM). גבול זה מבוסס על סבלנות מערכת העיכול: כמות גדולה של אוקסיד מגנזיום עלולה לגרום לאי-נוחות עיכולית כמו שלשול. לא מדובר ברעילות, אבל כדאי לדעת לפני נטילה.",
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
        "אזהרת מינון: 520 מ\"ג יסודי ביום עולה על הגבול העליון המומלץ לתוספי מגנזיום (350 מ\"ג/יום, IOM/NASEM). הגבול הזה עניינו נוחות העיכול בלבד — עודף מגנזיום מאוקסיד עלול לגרום לאי-נוחות עיכולית. מומלץ להתייעץ עם איש מקצוע לפני נטילה.",
      ],
    },
  },
  {
    id: "7290017218564",
    name: "אלטמן מגנזיום 520 60 כמוסות",
    // Source: vitamins4all.co.il
    imageUrl: "https://vitamins4all.co.il/wp-content/uploads/2024/08/7290017218564-2.webp",
    score: 49,
    grade: "D",
    // BAV: LOW / ספיגה נמוכה יחסית. Administered elemental: 520 mg (panel-verified).
    // UL_EXCEED: 520 mg > 350 mg IOM/NASEM supplemental UL.
    // SAFETY BLOCK (visible, collapsed row): requirement 4.
    claimShortfallFlag: "520 מ\"ג — כ-1.5× מעל הגבול העליון המומלץ לתוסף (350 מ\"ג)",
    insightLine: "אוקסיד 520 מ\"ג יסודי — ספיגה נמוכה יחסית ומינון מעל הגבול המומלץ לתוספים. ציון D עם אזהרת מינון.",
    rowVerdict:
      "אוקסיד מגנזיום 520 מ\"ג יסודי — הצורה עם הספיגה הנמוכה ביותר בקטגוריה, ובמינון שעולה על הגבול העליון המומלץ לתוספים (350 מ\"ג/יום, IOM/NASEM). הגבול הזה עניינו נוחות העיכול בלבד; עודף מגנזיום מאוקסיד עלול לגרום לאי-נוחות עיכולית. כדאי לדעת לפני נטילה.",
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
        "אזהרת מינון: 520 מ\"ג יסודי ביום עולה על הגבול העליון המומלץ לתוספי מגנזיום (350 מ\"ג/יום, IOM/NASEM). הגבול הזה עניינו נוחות העיכול בלבד — עודף מגנזיום מאוקסיד עלול לגרום לאי-נוחות עיכולית. מומלץ להתייעץ עם איש מקצוע לפני נטילה.",
      ],
    },
  },
  {
    id: "7290013142894",
    name: "אלטמן מגנזיום UP 60 כמוסות",
    // Source: altman.co.il
    imageUrl: "https://www.altman.co.il/wp-content/uploads/batc/_i/bd7e8878-3115-4e63-9646-d28e5d617979.webp",
    score: 49,
    grade: "D",
    // BAV: LOW / ספיגה נמוכה יחסית. Administered elemental: 450 mg (panel-verified).
    // UL_EXCEED: 450 mg > 350 mg IOM/NASEM supplemental UL.
    // SAFETY BLOCK (visible, collapsed row): requirement 4.
    claimShortfallFlag: "450 מ\"ג — כ-1.3× מעל הגבול העליון המומלץ לתוסף (350 מ\"ג)",
    insightLine: "אוקסיד 450 מ\"ג יסודי — ספיגה נמוכה יחסית ומינון מעל הגבול המומלץ לתוספים. ציון D עם אזהרת מינון.",
    rowVerdict:
      "אוקסיד מגנזיום 450 מ\"ג יסודי — ספיגה נמוכה יחסית ומינון שעולה כ-1.3 פעם על הגבול העליון המומלץ לתוספים (350 מ\"ג/יום, IOM/NASEM). הגבול הזה עניינו נוחות העיכול בלבד. כדאי לדעת לפני נטילה.",
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
        "אזהרת מינון: 450 מ\"ג יסודי ביום עולה על הגבול העליון המומלץ לתוספי מגנזיום (350 מ\"ג/יום, IOM/NASEM). הגבול הזה עניינו נוחות העיכול בלבד — עודף מגנזיום מאוקסיד עלול לגרום לאי-נוחות עיכולית. מומלץ להתייעץ עם איש מקצוע לפני נטילה.",
      ],
    },
  },
  {
    id: "7290019444206",
    name: "אלטמן מגנזיום באלאנס 60 כמוסות",
    // Source: vitamins4all.co.il
    imageUrl: "https://vitamins4all.co.il/wp-content/uploads/2025/05/7290019444206.webp",
    score: 49,
    grade: "D",
    // BAV: LOW / ספיגה נמוכה יחסית. Administered elemental: 450 mg (panel-verified).
    // UL_EXCEED: 450 mg > 350 mg IOM/NASEM supplemental UL.
    // SAFETY BLOCK (visible, collapsed row): requirement 4.
    claimShortfallFlag: "450 מ\"ג — כ-1.3× מעל הגבול העליון המומלץ לתוסף (350 מ\"ג)",
    insightLine: "אוקסיד 450 מ\"ג יסודי עם צמחי מרגוע — ספיגה נמוכה יחסית ומינון מעל הגבול המומלץ לתוספים. ציון D עם אזהרת מינון.",
    rowVerdict:
      "אוקסיד מגנזיום 450 מ\"ג יסודי, עם אשווגנדה וולריאן — ספיגה נמוכה יחסית ומינון שעולה על הגבול המומלץ לתוספים (350 מ\"ג/יום, IOM/NASEM). הצמחים הם תוספת שאינה משנה את כמות המגנזיום שמגיעה. הגבול עניינו נוחות העיכול בלבד. כדאי לדעת לפני נטילה.",
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
        "אשווגנדה וולריאן — צמחים שאינם משנים את הספיגה או כמות המגנזיום היסודי",
      ],
      // SAFETY BLOCK — visible per requirement 4. GI-tolerance-not-toxicity framing.
      caveats: [
        "אזהרת מינון: 450 מ\"ג יסודי ביום עולה על הגבול העליון המומלץ לתוספי מגנזיום (350 מ\"ג/יום, IOM/NASEM). הגבול הזה עניינו נוחות העיכול בלבד — עודף מגנזיום מאוקסיד עלול לגרום לאי-נוחות עיכולית. מומלץ להתייעץ עם איש מקצוע לפני נטילה.",
      ],
    },
  },

  // ─── E (1 product) ───────────────────────────────────────────────────────
  // Nutricare Nano: cap_1_insufficient_evidence. binding_constraint = cap_1.
  // Score capped at 34.0. "nano liposomal" claim insufficient evidence.
  {
    id: "7290001065594",
    name: "נוטריקר נאנו מגנזיום ליפוזומלי 60 כמוסות",
    // Source: vitamins4all.co.il
    imageUrl: "https://vitamins4all.co.il/wp-content/uploads/2024/07/%D7%A0%D7%90%D7%A0%D7%95-%D7%9E%D7%92%D7%A0%D7%96%D7%99%D7%95%D7%9D-Copy.webp",
    score: 34,
    grade: "E",
    // BAV: HIGH class for base form (bisglycinate). Administered elemental: 88 mg.
    // cap_1_insufficient_evidence: "נאנו ליפוזומלי" claim → insufficient evidence.
    // HARD: do NOT show absorbed figures. This is a cap_1 product.
    insightLine: "88 מ\"ג ביסגליצינט עם טענת 'נאנו ליפוזומלי' — הטענה לא נתמכת בעדות מדעית מספקת. ציון E.",
    rowVerdict:
      "הבסיס הוא ביסגליצינט — צורה עם ספיגה גבוהה יחסית — אבל האריזה נושאת טענה לטכנולוגיית 'נאנו ליפוזומלי' שמעלה שאלה פתוחה: האם הגוף מטפל במולקולה כמו ביסגליצינט רגיל, או אחרת? אין עדות מדעית מספקת לטענת השיפור, ולכן הציון יורד ל-E. בנוסף, 88 מ\"ג יסודי ביום הם מינון נמוך ביחס לשאר הקטגוריה.",
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
    name: "טינק מגנזיום אוקסיד 520 90 כמוסות",
    // Source: tinc.co.il
    imageUrl: "https://www.tinc.co.il/GoopSitesFiles/83206/User/catalog_941469-l.jpg?637595154336530000",
    score: null,
    grade: null,
    // UNRESOLVED: label declares "520 מ\"ג מגנזיום אוקסיד" without elemental qualifier.
    // [PLACEHOLDER] insightLine — Content to author (must match unresolved framing)
    insightLine: "לא ניתן לדרג — נתוני תווית חסרים",
    rowVerdict:
      "לא ניתן לדרג — התווית מציינת '520 מ\"ג מגנזיום אוקסיד' ללא אישור שמדובר במגנזיום יסודי. לא ניתן לחשב מינון יסודי ממקור אמין.",
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
    name: "אמורפיקיור pH מגנזיום 60 קפסולות",
    // Source: vitamins4all.co.il
    imageUrl: "https://vitamins4all.co.il/wp-content/uploads/2023/12/7290015429245-1.jpg",
    score: null,
    grade: null,
    // UNRESOLVED: 160 mg elemental-vs-compound ambiguous (carbonate 0.288 fraction). ~3.5x uncertainty.
    insightLine: "לא ניתן לדרג — נתוני תווית חסרים",
    rowVerdict:
      "לא ניתן לדרג — האם '160 מ\"ג' מתייחס למגנזיום יסודי או לתרכובת? אי-בהירות של פי 3.5 במינון; ציון אינו ניתן לחישוב.",
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
    name: "סופהרב TRIOMAG מגנזיום 60 כמוסות",
    // Source: vitamins4all.co.il
    imageUrl: "https://vitamins4all.co.il/wp-content/uploads/2026/01/7290118816065-1.jpg",
    score: null,
    grade: null,
    // UNRESOLVED: 200 mg likely elemental but unconfirmed; form ratios undisclosed.
    insightLine: "לא ניתן לדרג — נתוני תווית חסרים",
    rowVerdict:
      "לא ניתן לדרג — פיצול שלוש הצורות (ציטראט / ביסגליצינט / טאוראט) לא מפורסם על האריזה. לא ניתן להעריך ספיגה ללא יחסי הצורות.",
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

// Supherb Max 550 (7290118818205) — DISCARDED. Missing-data discard rule. NOT displayed.
