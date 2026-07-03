// Creatine supplement comparison page — TASK-492C.
// Source of truth: C:\Bari\03_operations\reports\content\creatine_comparison_content_package_v2.md
// (two-gate-fixed content package; ported VERBATIM per delegation — no wording changes).
// Structural template: magnesium-page-data.ts (TASK-384).
//
// PRODUCT RULING 1 (bind — Product Agent, applied throughout this file):
//   NO A–E grade and NO numeric Bari score anywhere. Creatine has no scored BSIP2 engine;
//   monohydrate at an honest dose is evidence-equivalent across brands. `score`/`grade` are
//   `null` for ALL 31 products (18 Israeli + 13 worldwide). Primary headline = dose-honesty
//   verdict (honest / below-floor / undisclosed), carried in `rowVerdict`. Primary sort /
//   ranking signal = price-per-effective-gram (₪ per 3g effective dose), computed only where
//   BOTH a per-serving dose AND servings-per-container were disclosed — never estimated.
//
// PRODUCT RULING 2 (two-tier certification, applied throughout):
//   "אומת מול מאגר" ONLY for the 6 NSF-directory-confirmed worldwide rows (Thorne, Momentous,
//   Klean Athlete, BPN, MegaFood, BioSteel). Every other cert claim = "מוצהר על-ידי היצרן".
//   ESN = honest uncertified comparator. 0 Israeli products are directory-confirmed.
//
// Product images: package leaves imageUrls unassigned (no retailer/manufacturer hotlinking,
// no invented URLs). imageUrl: null on all 31 products — BariProductThumbnail's existing
// no-photo fallback tile renders cleanly (same pattern as magnesium's "פול-מג הדס", which also
// carries imageUrl: null). FOLLOW-UP for Frontend/Data: self-host real images under
// bari-web/public/products/ per the product-images-self-hosted rule before go-live.
//
// Content status: DRAFT. Every Hebrew consumer string is unsigned draft copy pending BOTH
// gates (Content Agent + Adversarial QA / Red-Team) per the standing two-gate hard rule.
// This file does not publish anything — orchestrator gates before it reaches the owner.

import { normalizeProductBrandDisplay } from "@/lib/comparisons/product-brand-display";
import type { BariProductVM, CreatineBadgesVM } from "@/lib/view-models";

// ─── Creatine badge helper ────────────────────────────────────────────────────
function mkBadge(
  form_label: string,
  dose_label: string,
  doseHonesty: CreatineBadgesVM["doseHonesty"],
  dose_honesty_label: string,
  certTier: CreatineBadgesVM["certTier"],
  cert_label: string,
  price_per_3g_label: string | null
): CreatineBadgesVM {
  return {
    form_label,
    dose_label,
    doseHonesty,
    dose_honesty_label,
    certTier,
    cert_label,
    price_per_3g_label,
  };
}

const DOSE_HONESTY_LABEL: Record<CreatineBadgesVM["doseHonesty"], string> = {
  honest: "הוגן — מינון משמעותי",
  below_floor: "מוצהר, מתחת לרצפה",
  undisclosed: "לא מפורט",
};

// ─── Copy (content two-gate sign-off PENDING — port verbatim from v2 package) ─

export const creatineHero = {
  eyebrow: "תוספי קריאטין",
  title: "קונים קריאטין? המינון והצורה קובעים את השווי. המחיר מספר סיפור נפרד.",
} as const;

// 31 displayed: 18 Israeli shelf + 13 worldwide benchmark.
export const creatineMetadataLine = "18 מוצרים מהמדף הישראלי · 13 מותגי ייחוס עולמיים · יולי 2026";

export const creatinePrologueSentences = [
  "בדקנו 18 תוספי קריאטין הזמינים לצרכן הישראלי, מול שלושה-עשר מותגי ייחוס עולמיים, לפי ארבעה פרמטרים: כמה קריאטין המוצר מספק במנה, באיזו צורה כימית, האם יש בדיקת צד-שלישי, וכמה עולה גרם אפקטיבי אחד.",
  "המינון היומי שנחקר לתחזוקה הוא 3 עד 5 גרם ליום, במונוהידראט. עשרה מתוך שמונה-עשר המוצרים מצהירים על מינון אמיתי בטווח הזה ובצורה שנחקרה.",
  "ארבעה מוצרים נושאים את המילה קריאטין על האריזה בלי לפרט כמה גרם יש במנה. זו פער שקיפות אמיתי. שלושה מהם נמכרים ברשת המזון שופרסל, והרביעי הוא מוצר טבליות מיובא של MyProtein.",
  "שתי צורות HCl במדף עולות פי שש עד פי עשר לגרם אפקטיבי מהמונוהידראט הרגיל, בלי יתרון מוכח שמצדיק את הפער. המונוהידראט הוא הצורה שרוב המחקר נעשה עליה, והוא גם הזול ביותר לגרם.",
] as const;

// TASK-492C FIX 1 (design-critic C1): the full ~772-word note buried the comparison
// below the fold on desktop (the mobile collapse toggle in comparison-page.tsx is
// `md:hidden`, so it never applied on desktop — the whole block rendered open above
// the product tables). Restructured per delegation: relocate, do not re-author.
//
// Trimmed categoryNote (~150 words, comparable to magnesiumCategoryNote ~175 words):
// keeps only the top-line methodology paragraph, the two-tier-cert explainer, and the
// standard category caveat — the three paragraphs a reader needs before scanning rows.
// Every other paragraph (evidence tiers, effective dose, forms, safety, dairy annotation,
// tier definitions) is the SAME verbatim Hebrew text, moved to `creatineEvidenceSections`
// below and rendered by <CreatineEvidenceSection> below the product tables (see
// creatine-comparison-page.tsx). No sentence was reworded.
export const creatineCategoryNote =
  "איך נקבע הדירוג, וביחס למה\n\n" +
  "הדף הזה אינו נותן ציון מספרי או דירוג אותיות. קריאטין מונוהידראט במינון הוגן עובד באותה מידה בין המותגים, ולכן הדירוג נשען על מה שבאמת משתנה בין המוצרים: שקיפות המינון והשווי לגרם. ארבעה דברים נמדדים: כמה קריאטין המוצר מספק במנה מול הטווח שנחקר (3 עד 5 גרם ליום), באיזו צורה, האם יש בדיקת צד-שלישי, וכמה עולה גרם אפקטיבי אחד.\n\n" +
  "בדיקת צד-שלישי מוצגת בשתי רמות: \"אומת מול מאגר\" כשבדקנו את רישום המוצר ישירות במאגר של גוף ההסמכה, ו\"מוצהר על-ידי היצרן\" כשהטענה מופיעה רק בדף המוצר של המותג ולא אומתה מול המאגר. שש מנות ייחוס עולמיות אומתו מול מאגר NSF. אף מוצר מהמדף הישראלי לא אומת מול מאגר בשלב זה.\n\n" +
  "הערת קטגוריה: מה חשוב לדעת לפני שבוחרים\n\n" +
  "בארי מבססת את ההשוואה על קריאת תוויות ודפי מוצר. כל המינונים והמחירים המוצגים הם מה שכתוב על האריזה או בדף המוצר בעת הבדיקה. המחירים המוצגים נכונים לתאריך הבדיקה (יולי 2026) ועשויים להשתנות. המידע כאן הוא לצורך הכרה בלבד, ואינו תחליף לייעוץ רפואי.";

// TASK-492C FIX 1: evidence prose relocated out of categoryNote, rendered BELOW the
// product comparison tables via <CreatineEvidenceSection> (creatine-comparison-page.tsx).
// Each topic is its own collapsible subsection — mirrors the collapsible-subsection
// pattern already used by MagnesiumSafetyBox (magnesium-safety-box.tsx). Every sentence
// below is copied verbatim from the original single-block categoryNote — no rewording.
export interface CreatineEvidenceTopic {
  id: string;
  heading: string;
  paragraphs: string[];
}

export const creatineEvidenceSections: CreatineEvidenceTopic[] = [
  {
    id: "what-it-does",
    heading: "מה קריאטין באמת עושה",
    paragraphs: [
      "חוזק וכוח באימוני התנגדות — עדות חזקה. זו אחת ההשפעות המשוחזרות ביותר במחקר תזונת הספורט: קריאטין יחד עם אימוני התנגדות מעלה חוזק מעבר לאימון לבדו (עמדת ISSN 2017, PMID 28615996).",
      "מסת שריר רזה באימוני התנגדות — עדות חזקה. מטא-אנליזה מ-2024 של שנים-עשר מחקרים מצאה עלייה ממוצעת של כ-1.14 ק\"ג במסה הרזה מעבר לאימון לבדו (PMID 39074168).",
      "ביצועים בעצימות גבוהה וספרינטים חוזרים — עדות בינונית עד חזקה. תומך במאמצים קצרים וחוזרים בעצימות גבוהה. יתרון מבוסס, פחות מכומת מספרית מהחוזק.",
      "התאוששות — כאן חשוב להפריד. קריאטין עשוי להוריד סמנים ביוכימיים של עומס שריר לאחר אימון קשה (עדות בינונית; Northeast & Clifford 2021, PMID 33631721). באותה סקירה עצמה, הוא לא האיץ את ההתאוששות התפקודית עצמה: חוזק, כאב שרירים או טווח תנועה. ירידה בסמנים ביוכימיים מעידה על פחות עומס נמדד, אך אינה מבטיחה חזרה מהירה יותר לתפקוד.",
      "תפקוד קוגניטיבי — לא מבוסס לאוכלוסייה הכללית. חוות דעת EFSA מ-2024 על טענת הבריאות הקוגניטיבית מצאה שהיא אינה מבוססת לתפקוד קוגניטיבי כללי (DOI 10.2903/j.efsa.2024.9100).",
      "שריפת שומן — אין עדות. אין עדות אמינה שקריאטין שורף שומן ישירות. שינוי בהרכב הגוף משקף עלייה במסה רזה שמגיעה מהאימון עצמו.",
    ],
  },
  {
    id: "effective-dose",
    heading: "המינון האפקטיבי",
    paragraphs: [
      "הטווח שנחקר לתחזוקה הוא 3 עד 5 גרם ליום, בנטילה עקבית. שלושה גרם ליום נמצאים ברצפת הטווח האפקטיבי.",
      "שלב העמסה של כ-20 גרם ליום (4 מנות של 5 גרם) למשך 5 עד 7 ימים מזרז את הרוויה, ואינו הכרחי. נטילה קבועה של 3 עד 5 גרם ליום מגיעה לאותו מקום, לאט יותר.",
    ],
  },
  {
    id: "forms",
    heading: "צורות",
    paragraphs: [
      "מונוהידראט הוא הצורה שכמעט כל העדות נוצרה עליה, והוא ברירת המחדל המבוססת-מחקר. צורות כמו HCl, ביסודי או \"אלקליין\", אתיל אסתר, ציטראט ומלאט אינן מזיקות ואינן נחותות באיכות, אך אין להן עדות אנושית ליתרון על פני המונוהידראט הזול והנחקר יותר. המשמעות המעשית: משלמים יותר על צורה שלא הוכיחה יתרון.",
    ],
  },
  {
    id: "safety",
    heading: "בטיחות",
    paragraphs: [
      "לא נקבע גבול עליון מבוסס לקריאטין. מחקרים במינונים של עד 30 גרם ליום למשך חמש שנים לא דיווחו על נזק תלוי-מינון באנשים בריאים (עמדת ISSN 2017, PMID 28615996).",
      "מיתוס הכליות: קריאטין מעלה סמן מעבדתי בשם קריאטינין, שלעיתים נחשב בטעות לנזק כלייתי. שלוש מטא-אנליזות עצמאיות על תפקוד כלייתי לא מצאו נזק כזה בכליות בריאות (PMID 31375416, 41199218, 42035842).",
      "מי שיש לו מחלת כליות קיימת, כדאי להתייעץ עם רופא לפני שימוש.",
      "מי שיש לו הפרעה דו-קוטבית, כדאי להתייעץ עם רופא לפני שימוש בקריאטין לתמיכה במצב הרוח. קיים סיכון מתועד להשריית אפיזודה מאנית או היפומאנית בהקשר הזה (Roitman ואחרים 2007, PMID 17988366). זהו מחקר ראשוני קטן, אך האזהרה שהוא מעלה אמיתית וראויה לתשומת לב.",
    ],
  },
  {
    id: "dose-honesty-tiers",
    heading: "שלוש רמות שקיפות המינון",
    paragraphs: [
      "מינון ישר: המוצר נוקב בקריאטין בשמו, מציין מספר גרם מדויק למנה, והמספר הזה בטווח שנחקר. זו התוית ההוגנת.",
      "מינון מוצהר מתחת לרצפה: המוצר מציין מספר מדויק, אך מתחת ל-3 גרם. זה לא הסתרה, וזה כן מינון בקצה הנמוך של הטווח.",
      "מינון לא מפורט: המילה קריאטין מופיעה על האריזה, אך אין שום מספר גרם למנה בשום מקום. ארבעה מוצרים במדף הישראלי נמצאים כאן: שלושה מרשת המזון שופרסל ואחד מוצר טבליות מיובא של MyProtein. אי אפשר לחשב מהתווית כמה קריאטין באמת מקבלים.",
    ],
  },
  {
    id: "creatine-in-dairy",
    heading: "קריאטין במשקאות חלב: מה מצאנו",
    paragraphs: [
      "לפעמים קריאטין מופיע גם מחוץ למדף התוספים, בתוך משקה חלב. במדף הישראלי, המשקה החלבי היחיד שמצהיר על קריאטין הוא יופלה גו (Yoplait GO), בשני מוצרים. בשניהם הכמות אינה מפורטת: אחד מציין אחוז ניסוח של 0.6% בלי גודל מנה שמאפשר לחשב כמה מיליגרם מקבלים ביום, והשני אינו מציין מספר כלל. לכן אי אפשר לומר אם מדובר במינון משמעותי או בכמות זניחה. זו כשלעצמה עובדה שכדאי לדעת לפני שקונים. (בדיקה ברשת שופרסל; לא נבדק ברשתות נוספות.)",
      "הבהרה: תנובה GO אינו מוצר קריאטין. המוצר במדף הוא GO קולגן אייס קפה, שהרכיב הפעיל בו הוא קולגן ולא קריאטין.",
    ],
  },
];

export const creatineMethodologyLines = [
  "בדקנו 18 תוספי קריאטין מהמדף הישראלי מול שלושה-עשר מותגי ייחוס עולמיים, לפי ארבעה פרמטרים: מינון הקריאטין למנה מול הטווח שנחקר, הצורה הכימית, בדיקת צד-שלישי, ומחיר לגרם אפקטיבי.",
  "הדף אינו מציג ציון מספרי או דירוג אותיות. המינון הוא השיקול הכבד ביותר, אחריו הצורה — מונוהידראט הוא ברירת המחדל שנחקרה — ואז בדיקת צד-שלישי ומחיר לגרם. כך מוצר בצורה יקרה בלי יתרון מוכח אינו מוצג כאילו הצורה שווה את הפער.",
  "שתי צורות HCl במדף עולות פי שש עד פי עשר לגרם אפקטיבי מהמונוהידראט, בלי עדות ליתרון שמצדיק את המחיר.",
  "מוצרים שנושאים את המילה קריאטין בלי לפרט מינון מוצגים כפער שקיפות; המוצר נשאר על המדף.",
] as const;

// ─── Section headings (rendered by creatine-comparison-page.tsx via renderProducts) ──
export const creatineIsraeliSectionLabel = "המדף הישראלי — 18 מוצרים";
export const creatineWorldwideSectionLabel = "מותגי ייחוס עולמיים — 13 מוצרים, 6 מדינות";

// ─── Israeli shelf — 18 products (§1.2) ──────────────────────────────────────
// Sort within each dose-honesty tier by price-per-3g ascending (cheapest first) —
// the load-bearing finding per §1.0. Undisclosed-dose products (no price-per-3g
// computable) are appended last within their tier, corpus order preserved (source order).
// All cert claims: "מוצהר על-ידי היצרן" (manufacturer-stated) — 0/18 directory-confirmed.

const creatineIsraeliProductsRaw: BariProductVM[] = [
  // ── honest — meaningful dose (10 products), sorted by price-per-3g ascending ──
  {
    id: "733739020383",
    name: "Sports Micronized Creatine",
    brand: "NOW Foods",
    imageUrl: null,
    score: null,
    grade: null,
    creatineBadges: mkBadge(
      "מונוהידראט", "4.2 גרם", "honest", DOSE_HONESTY_LABEL.honest,
      null, "לא נמצאה טענה",
      "₪0.52 ל-3 גרם"
    ),
    insightLine: "מונוהידראט ב-4.2 גרם למנה — מינון הוגן ב-₪0.52 בלבד לגרם אפקטיבי, המחיר הנמוך ביותר במדף הישראלי.",
    rowVerdict: "מינון הוגן — 4.2 גרם מונוהידראט. ₪0.52 ל-3 גרם, המחיר הנמוך ביותר במדף.",
    confidence: "verified",
    expansion: {
      nutrition: null,
      ingredients: null,
      confidenceLabel: "מבוסס על נתוני לוח אחורי — קמעונאי",
      servingNote: "למנה יומית",
      positiveSignals: ["מונוהידראט במינון הוגן (4.2 גרם)", "המחיר הנמוך ביותר לגרם אפקטיבי במדף הישראלי"],
      limitingFactors: ["לא נמצאה טענת בדיקת צד-שלישי"],
    },
  },
  {
    id: "5056555204153",
    name: "Creatine Monohydrate Micronized",
    brand: "ABE",
    imageUrl: null,
    score: null,
    grade: null,
    creatineBadges: mkBadge(
      "מונוהידראט", "4.25 גרם", "honest", DOSE_HONESTY_LABEL.honest,
      "manufacturer_stated", "מוצהר על-ידי היצרן (Informed Sport)",
      "₪0.65 ל-3 גרם"
    ),
    insightLine: "מונוהידראט ב-4.25 גרם, עם טענת Informed Sport שלא אומתה מול מאגר — ₪0.65 ל-3 גרם.",
    rowVerdict: "מינון הוגן — 4.25 גרם מונוהידראט. Informed Sport מוצהר (לא אומת מול מאגר). ₪0.65 ל-3 גרם.",
    confidence: "verified",
    expansion: {
      nutrition: null,
      ingredients: null,
      confidenceLabel: "מבוסס על נתוני לוח אחורי — קמעונאי",
      servingNote: "למנה יומית",
      positiveSignals: ["מונוהידראט במינון הוגן (4.25 גרם)", "מחיר נמוך לגרם אפקטיבי"],
      limitingFactors: ["טענת Informed Sport לא אומתה מול מאגר הבודק"],
    },
  },
  {
    id: "631656705737",
    name: "Platinum 100% Creatine",
    brand: "MuscleTech",
    imageUrl: null,
    score: null,
    grade: null,
    creatineBadges: mkBadge(
      "מונוהידראט", "5.0 גרם", "honest", DOSE_HONESTY_LABEL.honest,
      null, "לא נמצאה טענה (רק בדיקת HPLC מוצהרת)",
      "₪0.77 ל-3 גרם"
    ),
    insightLine: "5 גרם מונוהידראט למנה, עם טענת בדיקת HPLC בלבד (לא בדיקת צד-שלישי מוסמכת) — ₪0.77 ל-3 גרם.",
    rowVerdict: "מינון הוגן — 5 גרם מונוהידראט. טענת HPLC בלבד, לא בדיקת צד-שלישי מוסמכת. ₪0.77 ל-3 גרם.",
    confidence: "verified",
    expansion: {
      nutrition: null,
      ingredients: null,
      confidenceLabel: "מבוסס על נתוני לוח אחורי — קמעונאי",
      servingNote: "למנה יומית",
      positiveSignals: ["מונוהידראט במינון גבוה (5 גרם)"],
      limitingFactors: ["טענת HPLC אינה בדיקת צד-שלישי מוסמכת (NSF / Informed Sport)"],
    },
  },
  {
    id: "5055534302002",
    name: "Impact Creatine (250 g)",
    brand: "MyProtein",
    imageUrl: null,
    score: null,
    grade: null,
    creatineBadges: mkBadge(
      "מונוהידראט", "3.0 גרם", "honest", DOSE_HONESTY_LABEL.honest,
      "manufacturer_stated", "מוצהר על-ידי היצרן (Informed Choice)",
      "₪1.03 ל-3 גרם"
    ),
    insightLine: "3 גרם מונוהידראט, בדיוק רצפת הטווח שנחקר — ₪1.03 ל-3 גרם, עם טענת Informed Choice מוצהרת.",
    rowVerdict: "מינון הוגן — 3 גרם מונוהידראט, ברצפת הטווח שנחקר. Informed Choice מוצהר. ₪1.03 ל-3 גרם.",
    confidence: "verified",
    expansion: {
      nutrition: null,
      ingredients: null,
      confidenceLabel: "מבוסס על נתוני לוח אחורי — קמעונאי",
      servingNote: "למנה יומית",
      positiveSignals: ["מונוהידראט במינון הוגן (3 גרם)", "מחיר סביר לגרם אפקטיבי"],
      limitingFactors: ["טענת Informed Choice לא אומתה מול מאגר הבודק"],
    },
  },
  {
    id: "7290019766223",
    name: "אבקת קריאטין",
    brand: "All In",
    imageUrl: null,
    score: null,
    grade: null,
    creatineBadges: mkBadge(
      "מונוהידראט", "3.0 גרם", "honest", DOSE_HONESTY_LABEL.honest,
      null, "לא נמצאה טענה",
      "₪1.20 ל-3 גרם"
    ),
    insightLine: "3 גרם מונוהידראט למנה, ברצפת הטווח שנחקר — ₪1.20 ל-3 גרם, ללא טענת בדיקת צד-שלישי.",
    rowVerdict: "מינון הוגן — 3 גרם מונוהידראט. ₪1.20 ל-3 גרם. ללא טענת בדיקת צד-שלישי.",
    confidence: "verified",
    expansion: {
      nutrition: null,
      ingredients: null,
      confidenceLabel: "מבוסס על נתוני לוח אחורי — קמעונאי",
      servingNote: "למנה יומית",
      positiveSignals: ["מונוהידראט במינון הוגן (3 גרם)"],
      limitingFactors: ["לא נמצאה טענת בדיקת צד-שלישי"],
    },
  },
  {
    id: "748927023855",
    name: "Micronized Creatine Powder",
    brand: "Optimum Nutrition",
    imageUrl: null,
    score: null,
    grade: null,
    creatineBadges: mkBadge(
      "מונוהידראט", "5.0 גרם", "honest", DOSE_HONESTY_LABEL.honest,
      "manufacturer_stated", "מוצהר על-ידי היצרן (Informed Choice)",
      "₪0.61 ל-3 גרם"
    ),
    insightLine: "5 גרם מונוהידראט, עם טענת Informed Choice מוצהרת — ₪0.61 ל-3 גרם.",
    rowVerdict: "מינון הוגן — 5 גרם מונוהידראט. Informed Choice מוצהר. ₪0.61 ל-3 גרם.",
    confidence: "verified",
    expansion: {
      nutrition: null,
      ingredients: null,
      confidenceLabel: "מבוסס על נתוני לוח אחורי — קמעונאי",
      servingNote: "למנה יומית",
      positiveSignals: ["מונוהידראט במינון גבוה (5 גרם)", "מחיר נמוך לגרם אפקטיבי"],
      limitingFactors: ["טענת Informed Choice לא אומתה מול מאגר הבודק"],
    },
  },
  {
    id: "693749006350",
    name: "Creatine",
    brand: "Thorne",
    imageUrl: null,
    score: null,
    grade: null,
    creatineBadges: mkBadge(
      "מונוהידראט", "5.0 גרם", "honest", DOSE_HONESTY_LABEL.honest,
      "manufacturer_stated", "מוצהר על-ידי היצרן (NSF Certified for Sport)",
      "₪0.89 ל-3 גרם"
    ),
    insightLine: "5 גרם מונוהידראט. Thorne טוענת NSF Certified for Sport — הרישום האמריקאי אומת מול מאגר, אך רישום ה-iHerb הישראלי לא נבדק בנפרד, ולכן מוצג כמוצהר.",
    rowVerdict: "מינון הוגן — 5 גרם מונוהידראט. NSF Certified for Sport מוצהר (הרישום האמריקאי אומת בטבלת הייחוס העולמית; רישום ה-iHerb הישראלי לא נבדק בנפרד). ₪0.89 ל-3 גרם.",
    confidence: "verified",
    expansion: {
      nutrition: null,
      ingredients: null,
      confidenceLabel: "מבוסס על נתוני לוח אחורי — קמעונאי",
      servingNote: "למנה יומית",
      positiveSignals: ["מונוהידראט במינון גבוה (5 גרם)", "Thorne מאומת מול מאגר NSF בארה\"ב"],
      limitingFactors: ["רישום ה-iHerb הישראלי לא נבדק בנפרד מול מאגר NSF"],
    },
  },
  {
    id: "898220022830",
    name: "Sport Pure Creatine (capsules)",
    brand: "California Gold Nutrition",
    imageUrl: null,
    score: null,
    grade: null,
    creatineBadges: mkBadge(
      "מונוהידראט (כמוסות)", "0.75 גרם לכמוסה", "below_floor", DOSE_HONESTY_LABEL.below_floor,
      "manufacturer_stated", "מוצהר על-ידי היצרן (iTested)",
      "₪0.97 ל-3 גרם"
    ),
    insightLine: "0.75 גרם לכמוסה — מספר הכמוסות היומי הנדרש להגיע ל-3 גרם לא מפורט, כך שהמינון היומי בפועל לא ידוע.",
    rowVerdict: "מוצהר, מתחת לרצפה — 0.75 גרם לכמוסה בודדת; כמות הכמוסות היומית לא מפורטת. ₪0.97 ל-3 גרם (מחושב).",
    confidence: "partial",
    expansion: {
      nutrition: null,
      ingredients: null,
      confidenceLabel: "מבוסס על נתונים חלקיים — כמות כמוסות יומית לא מפורטת",
      servingNote: "לכמוסה",
      positiveSignals: ["מונוהידראט"],
      limitingFactors: ["מינון 0.75 גרם לכמוסה בלבד; כמות הכמוסות היומית הנדרשת לא מפורטת על התווית"],
    },
  },
  {
    id: "myprotein-creatine-gummies",
    name: "Creatine Gummies",
    brand: "MyProtein",
    imageUrl: null,
    score: null,
    grade: null,
    creatineBadges: mkBadge(
      "מונוהידראט (גומי)", "3.0 גרם (3×1 גרם)", "honest", DOSE_HONESTY_LABEL.honest,
      null, "לא נמצאה טענה",
      null
    ),
    insightLine: "3 גרם מונוהידראט בשלוש סוכריות גומי — מינון הוגן בפורמט לא-שגרתי.",
    rowVerdict: "מינון הוגן — 3 גרם מונוהידראט (3×1 גרם גומי). מחיר לגרם אפקטיבי לא חושב (סופר כמות חבילה לא מלאה בדוח המקור).",
    confidence: "verified",
    expansion: {
      nutrition: null,
      ingredients: null,
      confidenceLabel: "מבוסס על נתוני לוח אחורי — קמעונאי",
      servingNote: "למנה יומית",
      positiveSignals: ["מונוהידראט במינון הוגן (3 גרם)", "פורמט גומי — חלופה למי שמתקשה עם אבקה"],
      limitingFactors: ["לא נמצאה טענת בדיקת צד-שלישי", "מחיר לגרם אפקטיבי לא חושב"],
    },
  },
  {
    id: "myprotein-creatine-elite",
    name: "Creatine Monohydrate Elite",
    brand: "MyProtein",
    imageUrl: null,
    score: null,
    grade: null,
    creatineBadges: mkBadge(
      "מונוהידראט (כללי, לא Creapure)", "3.0 גרם", "honest", DOSE_HONESTY_LABEL.honest,
      "manufacturer_stated", "מוצהר על-ידי היצרן (Informed Choice)",
      null
    ),
    insightLine: "3 גרם מונוהידראט כללי — לא Creapure, למרות השם. אותו מוצר בגרסה העולמית (Elite) מפרט 3.4 גרם למנה; אלה שני רישומים אזוריים של אותו SKU ולא סתירת נתונים.",
    rowVerdict: "מינון הוגן — 3 גרם מונוהידראט כללי (לא Creapure). Informed Choice מוצהר.",
    confidence: "verified",
    expansion: {
      nutrition: null,
      ingredients: null,
      confidenceLabel: "מבוסס על נתוני לוח אחורי — קמעונאי",
      servingNote: "למנה יומית",
      positiveSignals: ["מונוהידראט במינון הוגן (3 גרם)"],
      limitingFactors: [
        "שם המוצר \"Elite\" עלול להישמע כמו Creapure — זהו מונוהידראט כללי",
        "טענת Informed Choice לא אומתה מול מאגר הבודק",
      ],
      caveats: [
        "אותה סדרה \"Creatine Monohydrate Elite\" מופיעה גם בטבלת הייחוס העולמית במפרט 3.4 גרם למנה (רישום myprotein.co.uk). מדובר באותו מוצר שנסרק בשני רישומים אזוריים בשני מעברי איסוף נתונים — לא סתירה בנתונים; שני המספרים מעל רצפת ה-3 גרם.",
      ],
    },
  },
  {
    id: "myprotein-creatine-creapure",
    name: "THE Creatine Creapure",
    brand: "MyProtein",
    imageUrl: null,
    score: null,
    grade: null,
    creatineBadges: mkBadge(
      "מונוהידראט (Creapure)", "3.0 גרם", "honest", DOSE_HONESTY_LABEL.honest,
      "manufacturer_stated", "מוצהר על-ידי היצרן (Informed Choice)",
      null
    ),
    insightLine: "3 גרם מונוהידראט Creapure — סדרה נפרדת מ-Elite, בפועל אותה עדות מדעית כמו כל מונוהידראט אחר.",
    rowVerdict: "מינון הוגן — 3 גרם מונוהידראט Creapure. Informed Choice מוצהר.",
    confidence: "verified",
    expansion: {
      nutrition: null,
      ingredients: null,
      confidenceLabel: "מבוסס על נתוני לוח אחורי — קמעונאי",
      servingNote: "למנה יומית",
      positiveSignals: ["מונוהידראט במינון הוגן (3 גרם)", "Creapure — מקור מונוהידראט מתועד"],
      limitingFactors: ["אין עדות אנושית ליתרון של Creapure על פני מונוהידראט כללי באותו מינון", "טענת Informed Choice לא אומתה מול מאגר הבודק"],
    },
  },

  // ── disclosed, below floor — HCl (2 products), sorted by price-per-3g ascending ──
  {
    id: "850045966478",
    name: "Creatine HCl",
    brand: "Kaged",
    imageUrl: null,
    score: null,
    grade: null,
    creatineBadges: mkBadge(
      "HCl", "0.75 גרם", "below_floor", DOSE_HONESTY_LABEL.below_floor,
      "manufacturer_stated", "מוצהר על-ידי היצרן (Informed Sport)",
      "₪4.75 ל-3 גרם"
    ),
    insightLine: "HCl ב-0.75 גרם למנה — דפוס מינון נמוך אופייני לצורת HCl, עולה כמעט פי חמישה לגרם אפקטיבי לעומת מונוהידראט הוגן.",
    rowVerdict: "מוצהר, מתחת לרצפה — 0.75 גרם HCl. ₪4.75 ל-3 גרם, פי כמה יקר יותר ממונוהידראט באותו מינון אפקטיבי.",
    confidence: "verified",
    expansion: {
      nutrition: null,
      ingredients: null,
      confidenceLabel: "מבוסס על נתוני לוח אחורי — קמעונאי",
      servingNote: "למנה יומית",
      positiveSignals: [],
      limitingFactors: [
        "0.75 גרם למנה — מתחת לרצפת הטווח שנחקר (3 גרם)",
        "HCl — אין עדות אנושית ליתרון על פני מונוהידראט, והמחיר לגרם אפקטיבי גבוה משמעותית",
      ],
    },
  },
  {
    id: "682676700646",
    name: "Creatine HCl",
    brand: "Con-Cret",
    imageUrl: null,
    score: null,
    grade: null,
    creatineBadges: mkBadge(
      "HCl", "0.75 גרם", "below_floor", DOSE_HONESTY_LABEL.below_floor,
      "manufacturer_stated", "מוצהר על-ידי היצרן (NSF Certified for Sport)",
      "₪5.38 ל-3 גרם"
    ),
    insightLine: "HCl ב-0.75 גרם — היקר ביותר לגרם אפקטיבי במדף הישראלי, פי עשר בערך ממונוהידראט זול.",
    rowVerdict: "מוצהר, מתחת לרצפה — 0.75 גרם HCl. ₪5.38 ל-3 גרם, המחיר הגבוה ביותר לגרם אפקטיבי במדף.",
    confidence: "verified",
    expansion: {
      nutrition: null,
      ingredients: null,
      confidenceLabel: "מבוסס על נתוני לוח אחורי — קמעונאי",
      servingNote: "למנה יומית",
      positiveSignals: [],
      limitingFactors: [
        "0.75 גרם למנה — מתחת לרצפת הטווח שנחקר (3 גרם)",
        "HCl — אין עדות אנושית ליתרון על פני מונוהידראט, והמחיר לגרם אפקטיבי הגבוה ביותר במדף",
      ],
      caveats: [
        "התווית טוענת \"NSF Certified for Sport\" בדף ה-iHerb הישראלי — זו טענת הדף הקמעונאי, לא אומתה מול מאגר עבור ה-SKU הישראלי הספציפי, ולכן מוצגת כמוצהר על-ידי היצרן.",
      ],
    },
  },

  // ── disclosed, below floor — partial capsule dose (1 product) ──
  {
    id: "myprotein-creapure-capsules",
    name: "Creapure Micronised Capsules",
    brand: "MyProtein",
    imageUrl: null,
    score: null,
    grade: null,
    creatineBadges: mkBadge(
      "מונוהידראט (Creapure, כמוסות)", "2.8 גרם", "below_floor", DOSE_HONESTY_LABEL.below_floor,
      null, "לא נמצאה טענה",
      null
    ),
    insightLine: "2.8 גרם — קרוב לרצפת הטווח שנחקר אך לא בתוכו.",
    rowVerdict: "מוצהר, מתחת לרצפה — 2.8 גרם מונוהידראט Creapure, מתחת לרצפת ה-3 גרם.",
    confidence: "verified",
    expansion: {
      nutrition: null,
      ingredients: null,
      confidenceLabel: "מבוסס על נתוני לוח אחורי — קמעונאי",
      servingNote: "למנה יומית",
      positiveSignals: ["Creapure — מקור מונוהידראט מתועד"],
      limitingFactors: ["2.8 גרם למנה — מתחת לרצפת הטווח שנחקר (3 גרם), חלקית"],
    },
  },

  // ── undisclosed dose (4 products): 3 Shufersal grocery + 1 MyProtein tablet ──
  {
    id: "7290014386006",
    name: "קריאטין מונוהידראט ענבים",
    brand: "Super Effect",
    imageUrl: null,
    score: null,
    grade: null,
    creatineBadges: mkBadge(
      "מונוהידראט", "לא מפורט", "undisclosed", DOSE_HONESTY_LABEL.undisclosed,
      null, "לא נמצאה טענה",
      null
    ),
    insightLine: "המילה קריאטין מופיעה על האריזה, אך אין שום מספר גרם למנה — אי אפשר לחשב מהתווית כמה קריאטין באמת מקבלים.",
    rowVerdict: "לא מפורט — התווית לא מציינת מספר גרם קריאטין למנה. פער שקיפות אמיתי (רשת שופרסל).",
    confidence: "partial",
    expansion: {
      nutrition: null,
      ingredients: null,
      confidenceLabel: "מבוסס על נתונים חלקיים — מינון לא מפורט על התווית",
      servingNote: "למנה יומית",
      positiveSignals: [],
      limitingFactors: ["מינון קריאטין למנה אינו מפורט על האריזה — לא ניתן לחשב מחיר לגרם אפקטיבי"],
    },
  },
  {
    id: "7290016392005",
    name: "קריאטין מונוהידראט פירות",
    brand: "Super Effect",
    imageUrl: null,
    score: null,
    grade: null,
    creatineBadges: mkBadge(
      "מונוהידראט", "לא מפורט", "undisclosed", DOSE_HONESTY_LABEL.undisclosed,
      null, "לא נמצאה טענה",
      null
    ),
    insightLine: "המילה קריאטין מופיעה על האריזה, אך אין שום מספר גרם למנה — אי אפשר לחשב מהתווית כמה קריאטין באמת מקבלים.",
    rowVerdict: "לא מפורט — התווית לא מציינת מספר גרם קריאטין למנה. פער שקיפות אמיתי (רשת שופרסל).",
    confidence: "partial",
    expansion: {
      nutrition: null,
      ingredients: null,
      confidenceLabel: "מבוסס על נתונים חלקיים — מינון לא מפורט על התווית",
      servingNote: "למנה יומית",
      positiveSignals: [],
      limitingFactors: ["מינון קריאטין למנה אינו מפורט על האריזה — לא ניתן לחשב מחיר לגרם אפקטיבי"],
    },
  },
  {
    id: "7290010081288",
    name: "אבקת קריאטין מונוהידראט",
    brand: "Sport GS",
    imageUrl: null,
    score: null,
    grade: null,
    creatineBadges: mkBadge(
      "מונוהידראט", "לא מפורט", "undisclosed", DOSE_HONESTY_LABEL.undisclosed,
      null, "לא נמצאה טענה",
      null
    ),
    insightLine: "המילה קריאטין מופיעה על האריזה, אך אין שום מספר גרם למנה — אי אפשר לחשב מהתווית כמה קריאטין באמת מקבלים.",
    rowVerdict: "לא מפורט — התווית לא מציינת מספר גרם קריאטין למנה. פער שקיפות אמיתי (רשת שופרסל).",
    confidence: "partial",
    expansion: {
      nutrition: null,
      ingredients: null,
      confidenceLabel: "מבוסס על נתונים חלקיים — מינון לא מפורט על התווית",
      servingNote: "למנה יומית",
      positiveSignals: [],
      limitingFactors: ["מינון קריאטין למנה אינו מפורט על האריזה — לא ניתן לחשב מחיר לגרם אפקטיבי"],
    },
  },
  {
    id: "myprotein-creatine-tablets",
    name: "Creatine Monohydrate Tablets",
    brand: "MyProtein",
    imageUrl: null,
    score: null,
    grade: null,
    creatineBadges: mkBadge(
      "מונוהידראט (טבליות)", "לא מפורט", "undisclosed", DOSE_HONESTY_LABEL.undisclosed,
      null, "לא נמצאה טענה",
      null
    ),
    insightLine: "המילה קריאטין מופיעה על האריזה, אך אין שום מספר גרם למנה — מוצר טבליות מיובא ללא פירוט מינון.",
    rowVerdict: "לא מפורט — התווית לא מציינת מספר גרם קריאטין למנה. מוצר טבליות מיובא.",
    confidence: "partial",
    expansion: {
      nutrition: null,
      ingredients: null,
      confidenceLabel: "מבוסס על נתונים חלקיים — מינון לא מפורט על התווית",
      servingNote: "לטבליה",
      positiveSignals: [],
      limitingFactors: ["מינון קריאטין למנה אינו מפורט על האריזה — לא ניתן לחשב מחיר לגרם אפקטיבי"],
    },
  },
];

export const creatineIsraeliProducts: BariProductVM[] = creatineIsraeliProductsRaw.map((product) =>
  normalizeProductBrandDisplay(product)
);

// ─── Worldwide benchmark — 13 products, 6 regions (§1.3) ─────────────────────
// Sorted: 6 directory-verified (NSF) first, then manufacturer-stated, then the
// uncertified comparator (ESN) last — corpus order stable within each tier.
// bandNote marks the directory-verified sub-group boundary (mirrors magnesium's
// UL_EXCEED bandNote pattern).

const creatineWorldwideProductsRaw: BariProductVM[] = [
  {
    id: "wb-thorne-creatine",
    name: "Thorne Creatine (Micronized)",
    brand: "Thorne",
    imageUrl: null,
    score: null,
    grade: null,
    bandNote: "המוצרים הבאים אומתו ישירות מול מאגר NSF Certified for Sport",
    creatineBadges: mkBadge(
      "מונוהידראט", "5 גרם", "honest", DOSE_HONESTY_LABEL.honest,
      "directory_verified", "אומת מול מאגר (NSF, id 1204244)",
      "~$0.27 ל-3 גרם"
    ),
    insightLine: "5 גרם מונוהידראט, NSF Certified for Sport מאומת ישירות מול מאגר nsfsport.com — ~$0.27 ל-3 גרם.",
    rowVerdict: "מינון הוגן — 5 גרם מונוהידראט. NSF Certified for Sport אומת מול מאגר. ~$0.27 ל-3 גרם.",
    confidence: "verified",
    expansion: {
      nutrition: null,
      ingredients: null,
      confidenceLabel: "מבוסס על מאגר NSF + דף מותג",
      servingNote: "למנה יומית",
      positiveSignals: ["מונוהידראט במינון גבוה (5 גרם)", "אומת ישירות מול מאגר NSF Certified for Sport"],
      limitingFactors: [],
    },
  },
  {
    id: "wb-momentous-creatine",
    name: "Momentous Creatine Monohydrate",
    brand: "Momentous",
    imageUrl: null,
    score: null,
    grade: null,
    creatineBadges: mkBadge(
      "מונוהידראט (לא Creapure)", "5 גרם", "honest", DOSE_HONESTY_LABEL.honest,
      "directory_verified", "אומת מול מאגר (NSF, id 1285010)",
      "~$0.19–0.26 ל-3 גרם"
    ),
    insightLine: "5 גרם מונוהידראט, NSF מאומת מול מאגר. דף המותג מבהיר שהמקור אינו Creapure — למרות שכותרת משנית אצל משווק מסוים עדיין נושאת את המילה.",
    rowVerdict: "מינון הוגן — 5 גרם מונוהידראט (לא Creapure, לפי דף המותג). NSF אומת מול מאגר. ~$0.19–0.26 ל-3 גרם.",
    confidence: "verified",
    expansion: {
      nutrition: null,
      ingredients: null,
      confidenceLabel: "מבוסס על מאגר NSF + דף מותג",
      servingNote: "למנה יומית",
      positiveSignals: ["מונוהידראט במינון גבוה (5 גרם)", "אומת ישירות מול מאגר NSF Certified for Sport"],
      limitingFactors: [],
      caveats: [
        "כותרת משנית אצל משווק (Vitacost) עדיין נושאת את המילה \"Creapure\" — זהו רישום ישן; דף המותג הנוכחי הוא המקור הסמכותי וקובע שהמקור אינו Creapure.",
      ],
    },
  },
  {
    id: "wb-klean-athlete-creatine",
    name: "Klean Athlete — Klean Creatine",
    brand: "Klean Athlete",
    imageUrl: null,
    score: null,
    grade: null,
    creatineBadges: mkBadge(
      "מונוהידראט", "5 גרם", "honest", DOSE_HONESTY_LABEL.honest,
      "directory_verified", "אומת מול מאגר (NSF, id 1121640)",
      null
    ),
    insightLine: "5 גרם מונוהידראט, NSF Certified for Sport מאומת מול מאגר. מחיר לא נאסף בסבב זה.",
    rowVerdict: "מינון הוגן — 5 גרם מונוהידראט. NSF Certified for Sport אומת מול מאגר.",
    confidence: "partial",
    expansion: {
      nutrition: null,
      ingredients: null,
      confidenceLabel: "מבוסס על מאגר NSF — מחיר לא נאסף בסבב זה",
      servingNote: "למנה יומית",
      positiveSignals: ["מונוהידראט במינון גבוה (5 גרם)", "אומת ישירות מול מאגר NSF Certified for Sport"],
      limitingFactors: ["מחיר לא נאסף בסבב איסוף זה — לא ניתן לחשב מחיר לגרם אפקטיבי"],
    },
  },
  {
    id: "wb-bpn-creatine",
    name: "Creatine Monohydrate",
    brand: "BPN",
    imageUrl: null,
    score: null,
    grade: null,
    creatineBadges: mkBadge(
      "מונוהידראט", "5 גרם", "honest", DOSE_HONESTY_LABEL.honest,
      "directory_verified", "אומת מול מאגר (NSF, id 1635096)",
      "~$0.16–0.21 ל-3 גרם"
    ),
    insightLine: "5 גרם מונוהידראט, NSF מאומת מול מאגר — מהמחירים הנמוכים ביותר בטבלת הייחוס העולמית.",
    rowVerdict: "מינון הוגן — 5 גרם מונוהידראט. NSF Certified for Sport אומת מול מאגר. ~$0.16–0.21 ל-3 גרם.",
    confidence: "verified",
    expansion: {
      nutrition: null,
      ingredients: null,
      confidenceLabel: "מבוסס על מאגר NSF + דף מותג",
      servingNote: "למנה יומית",
      positiveSignals: ["מונוהידראט במינון גבוה (5 גרם)", "אומת ישירות מול מאגר NSF Certified for Sport", "מחיר נמוך לגרם אפקטיבי"],
      limitingFactors: [],
    },
  },
  {
    id: "wb-megafood-creatine",
    name: "MegaFood — Micronized Creatine Monohydrate",
    brand: "MegaFood",
    imageUrl: null,
    score: null,
    grade: null,
    creatineBadges: mkBadge(
      "מונוהידראט", "5 גרם", "honest", DOSE_HONESTY_LABEL.honest,
      "directory_verified", "אומת מול מאגר (NSF)",
      null
    ),
    insightLine: "5 גרם מונוהידראט, NSF Certified for Sport מאומת מול מאגר (רישום פעיל). מחיר לא נאסף בסבב זה.",
    rowVerdict: "מינון הוגן — 5 גרם מונוהידראט. NSF Certified for Sport אומת מול מאגר.",
    confidence: "partial",
    expansion: {
      nutrition: null,
      ingredients: null,
      confidenceLabel: "מבוסס על מאגר NSF — מחיר לא נאסף בסבב זה",
      servingNote: "למנה יומית",
      positiveSignals: ["מונוהידראט במינון גבוה (5 גרם)", "אומת ישירות מול מאגר NSF Certified for Sport"],
      limitingFactors: ["מחיר לא נאסף בסבב איסוף זה — לא ניתן לחשב מחיר לגרם אפקטיבי"],
    },
  },
  {
    id: "wb-sports-research-creatine",
    name: "Sports Research — Creatine Monohydrate Unflavored",
    brand: "Sports Research",
    imageUrl: null,
    score: null,
    grade: null,
    creatineBadges: mkBadge(
      "מונוהידראט", "5 גרם", "honest", DOSE_HONESTY_LABEL.honest,
      "manufacturer_stated", "מוצהר על-ידי היצרן (NSF Certified for Sport)",
      null
    ),
    insightLine: "5 גרם מונוהידראט. דף המותג טוען NSF Certified for Sport, אך ה-SKU הספציפי לא אותר במאגר בסבב זה — מוצג כמוצהר. סדרת Creapure נפרדת של המותג היא טענת דף בלבד ואינה מעורבבת עם רישום זה.",
    rowVerdict: "מינון הוגן — 5 גרם מונוהידראט. NSF Certified for Sport מוצהר; ה-SKU הספציפי לא נמצא במאגר בסבב זה.",
    confidence: "partial",
    expansion: {
      nutrition: null,
      ingredients: null,
      confidenceLabel: "מבוסס על דף מותג — לא אותר במאגר NSF בסבב זה",
      servingNote: "למנה יומית",
      positiveSignals: ["מונוהידראט במינון גבוה (5 גרם)"],
      limitingFactors: ["טענת NSF Certified for Sport — ה-SKU הספציפי לא אותר במאגר בסבב זה", "מחיר לא נאסף בסבב איסוף זה"],
      caveats: [
        "סדרת Creapure נפרדת של Sports Research מוזכרת בדף המותג בלבד — אינה מעורבבת עם רישום זה.",
      ],
    },
  },
  {
    id: "wb-biosteel-creatine",
    name: "BioSteel — Creatine (72 servings)",
    brand: "BioSteel",
    imageUrl: null,
    score: null,
    grade: null,
    creatineBadges: mkBadge(
      "מונוהידראט", "2.5 גרם", "below_floor", DOSE_HONESTY_LABEL.below_floor,
      "directory_verified", "אומת מול מאגר (NSF, id 1292599)",
      "~$0.17–0.24 ל-3 גרם (במנה בודדת)"
    ),
    insightLine: "2.5 גרם במדידה יחידה — מתחת לרצפת הטווח שנחקר, המקרה הברור ביותר בטבלה של תת-מינון בכמות המתויגת, למרות אימות NSF מלא.",
    rowVerdict: "מוצהר, מתחת לרצפה — 2.5 גרם למדידה יחידה, מתחת לרצפת ה-3 גרם. NSF Certified for Sport אומת מול מאגר.",
    confidence: "verified",
    expansion: {
      nutrition: null,
      ingredients: null,
      confidenceLabel: "מבוסס על מאגר NSF + דף מותג",
      servingNote: "למדידה אחת",
      positiveSignals: ["אומת ישירות מול מאגר NSF Certified for Sport"],
      limitingFactors: ["2.5 גרם במדידה אחת — מתחת לרצפת הטווח שנחקר (3 גרם); אין להשוות למוצרי 5 גרם באותה קטגוריה"],
    },
  },
  {
    id: "wb-naked-creatine",
    name: "Naked Nutrition — Naked Creatine",
    brand: "Naked Nutrition",
    imageUrl: null,
    score: null,
    grade: null,
    bandNote: "המוצרים הבאים מציגים טענת בדיקת צד-שלישי שלא אומתה ישירות מול מאגר",
    creatineBadges: mkBadge(
      "מונוהידראט", "5 גרם", "honest", DOSE_HONESTY_LABEL.honest,
      "manufacturer_stated", "מוצהר על-ידי היצרן (\"NSF-certified\")",
      "~$0.17–0.22 ל-3 גרם"
    ),
    insightLine: "5 גרם מונוהידראט. דף המותג טוען \"NSF-certified\", אך לא אותר רישום תואם במאגר — מוצג כמוצהר בלבד.",
    rowVerdict: "מינון הוגן — 5 גרם מונוהידראט. טענת NSF מוצהרת, לא נמצא רישום תואם במאגר. ~$0.17–0.22 ל-3 גרם.",
    confidence: "verified",
    expansion: {
      nutrition: null,
      ingredients: null,
      confidenceLabel: "מבוסס על דף מותג — לא אומת מול מאגר",
      servingNote: "למנה יומית",
      positiveSignals: ["מונוהידראט במינון גבוה (5 גרם)", "מחיר נמוך לגרם אפקטיבי"],
      limitingFactors: ["טענת \"NSF-certified\" — לא אותר רישום תואם במאגר NSF"],
    },
  },
  {
    id: "wb-applied-nutrition-creatine",
    name: "Applied Nutrition — Creatine Monohydrate (100%)",
    brand: "Applied Nutrition",
    imageUrl: null,
    score: null,
    grade: null,
    creatineBadges: mkBadge(
      "מונוהידראט", "5 גרם", "honest", DOSE_HONESTY_LABEL.honest,
      "manufacturer_stated", "מוצהר על-ידי היצרן (Informed-Sport)",
      "~$0.14–0.19 ל-3 גרם"
    ),
    insightLine: "5 גרם מונוהידראט. Informed-Sport מוצהר בדף המותג — אתר הבודק חסם גישה לאימות בכל הניסיונות, כך שלא ניתן לאמת מול מאגר.",
    rowVerdict: "מינון הוגן — 5 גרם מונוהידראט. Informed-Sport מוצהר (לא ניתן לאימות — אתר הבודק חסם גישה). ~$0.14–0.19 ל-3 גרם.",
    confidence: "verified",
    expansion: {
      nutrition: null,
      ingredients: null,
      confidenceLabel: "מבוסס על דף מותג — מאגר Informed-Sport לא נגיש לאימות",
      servingNote: "למנה יומית",
      positiveSignals: ["מונוהידראט במינון גבוה (5 גרם)", "מחיר נמוך לגרם אפקטיבי"],
      limitingFactors: ["טענת Informed-Sport לא ניתנת לאימות מול מאגר — אתר הבודק חסם גישה בכל הניסיונות"],
    },
  },
  {
    id: "wb-myprotein-elite",
    name: "MyProtein — Creatine Monohydrate Elite",
    brand: "MyProtein",
    imageUrl: null,
    score: null,
    grade: null,
    creatineBadges: mkBadge(
      "מונוהידראט (כללי, לא Creapure)", "3.4 גרם", "honest", DOSE_HONESTY_LABEL.honest,
      "manufacturer_stated", "מוצהר על-ידי היצרן (Informed-Sport)",
      "~$0.37 ל-3 גרם"
    ),
    insightLine: "3.4 גרם מונוהידראט כללי — לא Creapure למרות השם. אותו מוצר במדף הישראלי מפרט 3.0 גרם; שני רישומים אזוריים של אותו SKU.",
    rowVerdict: "מינון הוגן — 3.4 גרם מונוהידראט כללי (לא Creapure). Informed-Sport מוצהר. ~$0.37 ל-3 גרם.",
    confidence: "verified",
    expansion: {
      nutrition: null,
      ingredients: null,
      confidenceLabel: "מבוסס על דף מותג",
      servingNote: "למנה יומית",
      positiveSignals: ["מונוהידראט במינון הוגן (3.4 גרם)"],
      limitingFactors: ["שם המוצר \"Elite\" עלול להישמע כמו Creapure — זהו מונוהידראט כללי", "טענת Informed-Sport לא ניתנת לאימות מול מאגר"],
      caveats: [
        "אותה סדרה מופיעה גם במדף הישראלי (myprotein.co.il) במפרט 3.0 גרם למנה. שני הרישומים הם אותו מוצר שנסרק בשני מעברי איסוף נתונים אזוריים — לא סתירה; שני המספרים מעל רצפת ה-3 גרם.",
      ],
    },
  },
  {
    id: "wb-myprotein-creapure",
    name: "MyProtein — THE Creatine (Creapure)",
    brand: "MyProtein",
    imageUrl: null,
    score: null,
    grade: null,
    creatineBadges: mkBadge(
      "מונוהידראט (Creapure)", "3.4 גרם", "honest", DOSE_HONESTY_LABEL.honest,
      "manufacturer_stated", "מוצהר על-ידי היצרן (Informed Choice)",
      "~$0.44 ל-3 גרם"
    ),
    insightLine: "3.4 גרם מונוהידראט Creapure — סדרה נפרדת מ-Elite; אותה עדות מדעית כמו כל מונוהידראט אחר.",
    rowVerdict: "מינון הוגן — 3.4 גרם מונוהידראט Creapure. Informed Choice מוצהר. ~$0.44 ל-3 גרם.",
    confidence: "verified",
    expansion: {
      nutrition: null,
      ingredients: null,
      confidenceLabel: "מבוסס על דף מותג",
      servingNote: "למנה יומית",
      positiveSignals: ["מונוהידראט במינון הוגן (3.4 גרם)", "Creapure — מקור מונוהידראט מתועד"],
      limitingFactors: ["אין עדות אנושית ליתרון של Creapure על פני מונוהידראט כללי באותו מינון", "טענת Informed Choice לא ניתנת לאימות מול מאגר"],
    },
  },
  {
    id: "wb-switch-nutrition-creatine",
    name: "Switch Nutrition — Perform Purest Creatine",
    brand: "Switch Nutrition",
    imageUrl: null,
    score: null,
    grade: null,
    creatineBadges: mkBadge(
      "מונוהידראט", "3 גרם", "honest", DOSE_HONESTY_LABEL.honest,
      "manufacturer_stated", "מוצהר על-ידי היצרן (HASTA)",
      null
    ),
    insightLine: "3 גרם מונוהידראט, ברצפת הטווח שנחקר. HASTA מוצהר בדף המותג — מאגר ההסמכה לא נבדק בסבב זה.",
    rowVerdict: "מינון הוגן — 3 גרם מונוהידראט, ברצפת הטווח שנחקר. HASTA מוצהר (מאגר לא נבדק).",
    confidence: "partial",
    expansion: {
      nutrition: null,
      ingredients: null,
      confidenceLabel: "מבוסס על דף מותג — מאגר HASTA לא נבדק בסבב זה",
      servingNote: "למנה יומית",
      positiveSignals: ["מונוהידראט במינון הוגן (3 גרם)"],
      limitingFactors: ["3 גרם — ברצפת הטווח, לא ב-5 גרם הטיפוסיים של רוב המוצרים בטבלה", "טענת HASTA לא נבדקה מול מאגר בסבב זה", "מחיר לא נאסף בסבב איסוף זה"],
    },
  },
  {
    id: "wb-esn-creatine",
    name: "ESN — Ultrapure Creatine Monohydrate",
    brand: "ESN",
    imageUrl: null,
    score: null,
    grade: null,
    bandNote: "ההשוואה הישרה: מוצר ללא כל טענת בדיקת צד-שלישי",
    creatineBadges: mkBadge(
      "מונוהידראט, מיקרופיין", "3.5 גרם", "honest", DOSE_HONESTY_LABEL.honest,
      null, "לא מוסמך (ללא טענה)",
      "~$0.34 ל-3 גרם"
    ),
    insightLine: "3.5 גרם מונוהידראט, ללא כל טענת הסמכה — ההשוואה ההוגנת ביותר בטבלה למי שלא צריך תג בדיקת צד-שלישי.",
    rowVerdict: "מינון הוגן — 3.5 גרם מונוהידראט. ללא טענת בדיקת צד-שלישי (מוצג כהשוואה הוגנת, לא כחיסרון מוסתר). ~$0.34 ל-3 גרם.",
    confidence: "verified",
    expansion: {
      nutrition: null,
      ingredients: null,
      confidenceLabel: "מבוסס על דף מותג",
      servingNote: "למנה יומית",
      positiveSignals: ["מונוהידראט במינון הוגן (3.5 גרם)", "ללא טענת הסמכה שלא ניתנת לאימות — שקיפות מלאה על מה שכן ומה שלא נבדק"],
      limitingFactors: ["ללא בדיקת צד-שלישי מוסמכת"],
    },
  },
];

export const creatineWorldwideProducts: BariProductVM[] = creatineWorldwideProductsRaw.map((product) =>
  normalizeProductBrandDisplay(product)
);

// Combined corpus (Israeli + worldwide), used by ComparisonPageSeo / any consumer that
// needs the full 31-product set rather than the two rendered sections separately.
export const creatineProducts: BariProductVM[] = [
  ...creatineIsraeliProducts,
  ...creatineWorldwideProducts,
];
