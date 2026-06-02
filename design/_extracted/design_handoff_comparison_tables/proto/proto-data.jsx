// Bari — One-Table Prototype · data
// Real hummus products (names / scores / grades / protein / sodium / ingredients /
// confidence) from src/data/comparisons/hummus_frontend_v2.json. The v2 display
// fields the corpus does not yet expose — rowReason (+/−), additive_count, base_pct —
// are authored here as illustrative values to demonstrate the layout (flagged in the UI).

const IMG = "https://res.cloudinary.com/shufersal/image/upload/f_auto,q_auto/v1551800922/prod/product_images/products_zoom";

window.HUMMUS_PRODUCTS = [
  {
    id: "p1", name: "חומוס", type: "חומוס", img: `${IMG}/UFL56_Z_P_7296073733324_1.png`,
    score: 86, grade: "A", confidence: "verified",
    metrics: { protein: 22.0, additives: 0, base: 100, sodium: 23, energy: 351 },
    rowReason: { positive: "100% גרגרי חומוס — רכיב יחיד", limiting: null },
    insightLine: "100% גרגרי חומוס — רכיב יחיד",
    expansion: {
      positive: ["רכיב יחיד: 100% גרגרי חומוס, ללא תוספים", "חלבון גבוה (22 ג׳ ל-100 ג׳)", "נתרן נמוך מאוד (23 מ״ג)"],
      limiting: [],
      bottom: "ההרכב הנקי ביותר בקטגוריה — אין מה לנקות ממנו.",
      ingredients: "100% חומוס (עלול להכיל גלוטן חיטה).", serving: "ל-100 גרם",
    },
  },
  {
    id: "p2", name: "חומוס ענק", type: "חומוס", img: `${IMG}/UFS54_Z_P_7296073733331_1.png`,
    score: 86, grade: "A", confidence: "verified",
    metrics: { protein: 22.0, additives: 0, base: 100, sodium: 23, energy: 351 },
    rowReason: { positive: "גרגרי חומוס ענק — ללא תוספות", limiting: null },
    insightLine: "גרגרי חומוס ענק — ללא תוספות",
    expansion: {
      positive: ["רכיב יחיד, ללא תוספות", "חלבון גבוה (22 ג׳)", "נתרן נמוך"],
      limiting: [],
      bottom: "זהה בהרכבו לחומוס המוביל — גודל גרגר שונה בלבד.",
      ingredients: "100% חומוס (עלול להכיל גלוטן חיטה).", serving: "ל-100 גרם",
    },
  },
  {
    id: "p3", name: "חומוס לבן ענק שופרסל", type: "חומוס", img: `${IMG}/KDE64_Z_P_7296073005889_1.png`,
    score: 85, grade: "A", confidence: "verified",
    metrics: { protein: 19.3, additives: 0, base: 100, sodium: 24, energy: 339 },
    rowReason: { positive: "סיבים גבוהים (17.4 ג׳), ללא תוספים", limiting: null },
    insightLine: "גרגרי חומוס לבן גדולים — ללא תוספים",
    expansion: {
      positive: ["רכיב יחיד, ללא תוספים", "סיבים תזונתיים גבוהים (17.4 ג׳)", "חלבון 19.3 ג׳"],
      limiting: [],
      bottom: "בולט בסיבים — מבין הגבוהים בקטגוריה.",
      ingredients: "גרגרי חומוס. ערכים ל-100 ג׳: 17.4 ג׳ סיבים, 19.3 ג׳ חלבון, 24 מ״ג נתרן.", serving: "ל-100 גרם",
    },
  },
  {
    id: "p4", name: "חומוס גדול שופרסל", type: "חומוס", img: `${IMG}/KIA46_Z_P_7296073006015_1.png`,
    score: 85, grade: "A", confidence: "verified",
    metrics: { protein: 19.3, additives: 0, base: 100, sodium: 24, energy: 339 },
    rowReason: { positive: "רכיב יחיד, סיבים גבוהים", limiting: null },
    insightLine: "גרגרי חומוס גדולים — ללא תוספים",
    expansion: {
      positive: ["רכיב יחיד, ללא תוספים", "סיבים גבוהים (17.4 ג׳)"],
      limiting: [],
      bottom: "מקביל לחומוס הלבן — הרכב נקי, סיבים גבוהים.",
      ingredients: "גרגירי חומוס. ערכים ל-100 ג׳: 17.4 ג׳ סיבים, 19.3 ג׳ חלבון.", serving: "ל-100 גרם",
    },
  },
  {
    id: "p5", name: "חומוס מוקפא", type: "חומוס", img: `${IMG}/FBM56_Z_P_7296073705505_1.png`,
    score: 85, grade: "A", confidence: "verified",
    metrics: { protein: 8.4, additives: 0, base: 100, sodium: 6, energy: 121 },
    rowReason: { positive: "רכיב יחיד, נתרן נמוך מאוד", limiting: "חלבון נמוך יחסית (ערך מבושל)" },
    insightLine: "גרגרי חומוס קפואים — רכיב יחיד",
    expansion: {
      positive: ["רכיב יחיד, ללא תוספים", "נתרן נמוך מאוד (6 מ״ג)"],
      limiting: ["חלבון נמוך יחסית — הערכים נמדדו על מוצר מבושל"],
      bottom: "נקי לחלוטין; הערכים הנמוכים נובעים ממדידה במצב מבושל.",
      ingredients: "חומוס. ערכים ל-100 ג׳ מבושל: 8.4 ג׳ חלבון, 5.1 ג׳ סיבים, 6 מ״ג נתרן.", serving: "ל-100 גרם (מבושל)",
    },
  },
  {
    id: "p6", name: "הקיסר חומוס ענק", type: "חומוס", img: `${IMG}/QXJ64_Z_P_7290018359686_1.png`,
    score: 80, grade: "A", confidence: "partial",
    metrics: { protein: 7.0, additives: 1, base: 92, sodium: 150, energy: 137 },
    rowReason: { positive: "גרגרים שלמים בשימור", limiting: "רשימת רכיבים מלאה לא אומתה" },
    insightLine: "גרגרי חומוס ענק בשימור — מידע רכיבים מלא לא אומת",
    expansion: {
      positive: ["גרגרי חומוס שלמים", "נתרן בינוני (150 מ״ג)"],
      limiting: ["רשימת הרכיבים המלאה לא הופיעה במקור — לא ניתן לאמת תוספים"],
      bottom: "סביר להניח שנקי, אך חסר מידע רכיבים לאימות מלא.",
      ingredients: null, serving: "ל-100 גרם",
    },
  },
  {
    id: "p7", name: "סלט חומוס", type: "חומוס", img: `${IMG}/GJK34_Z_P_6666307_1.png`,
    score: 80, grade: "A", confidence: "verified",
    metrics: { protein: 18.2, additives: 1, base: 75, sodium: 480, energy: 257 },
    rowReason: { positive: "חלבון גבוה (18.2 ג׳)", limiting: "נתרן גבוה (480 מ״ג); חומר משמר אחד" },
    insightLine: "גרגירי חומוס, טחינה ותבלינים — רשימה קצרה עם חומר משמר אחד",
    expansion: {
      positive: ["חלבון גבוה (18.2 ג׳)", "רשימת רכיבים קצרה: חומוס, טחינה, תבלינים"],
      limiting: ["נתרן גבוה (480 מ״ג)", "חומר משמר אחד (E202)"],
      bottom: "הרכב טוב לסלט חומוס; הנתרן הוא הגורם המגביל העיקרי.",
      ingredients: "גרגירי חומוס, טחינה שומשומין, מים, תבלינים, חומר משמר E202.", serving: "ל-100 גרם",
    },
  },
  {
    id: "p8", name: "מסבחה גרגרים", type: "מסבחה", img: `${IMG}/GJK34_Z_P_6666307_1.png`,
    score: 72, grade: "B", confidence: "verified",
    metrics: { protein: 14.0, additives: 2, base: 70, sodium: 410, energy: 232 },
    rowReason: { positive: "גרגרים שלמים, טחינה אמיתית", limiting: "נתרן גבוה; שני תוספים" },
    insightLine: "מסבחה גרגרים שלמים — טחינה אמיתית עם שני תוספים",
    expansion: {
      positive: ["גרגרי חומוס שלמים", "טחינה אמיתית ברשימה"],
      limiting: ["נתרן גבוה (410 מ״ג)", "שני תוספי מזון"],
      bottom: "בסיס טוב; הנתרן והתוספים מורידים אותו מקבוצת ה-A.",
      ingredients: "גרגירי חומוס, טחינה, מים, מלח, חומצת לימון, חומר משמר.", serving: "ל-100 גרם",
    },
  },
  {
    id: "p9", name: "חומוס עם תוספת שמן", type: "חומוס", img: `${IMG}/UFL56_Z_P_7296073733324_1.png`,
    score: 64, grade: "C", confidence: "verified",
    metrics: { protein: 12.0, additives: 2, base: 62, sodium: 520, energy: 288 },
    rowReason: { positive: "חלבון סביר", limiting: "נתרן גבוה; שמן ומייצב מוספים" },
    insightLine: "חומוס במרקם חלק — שמן ומייצב מוספים, נתרן גבוה",
    expansion: {
      positive: ["חלבון סביר (12 ג׳)"],
      limiting: ["נתרן גבוה (520 מ״ג)", "שמן מוסף ומייצב מרקם"],
      bottom: "מרקם חלק במחיר של שמן מוסף ונתרן גבוה.",
      ingredients: "גרגירי חומוס, מים, שמן חמניות, טחינה, מלח, מייצב.", serving: "ל-100 גרם",
    },
  },
  {
    id: "p10", name: "חומוס ביתי בטעמים", type: "חומוס", img: `${IMG}/KDE64_Z_P_7296073005889_1.png`,
    score: 58, grade: "C", confidence: "verified",
    metrics: { protein: 9.0, additives: 3, base: 55, sodium: 540, energy: 301 },
    rowReason: { positive: "מגוון טעמים", limiting: "שלושה תוספים; נתרן גבוה" },
    insightLine: "חומוס בטעמים — שלושה תוספים ונתרן גבוה",
    expansion: {
      positive: ["מגוון טעמים על אותו בסיס"],
      limiting: ["שלושה תוספי מזון", "נתרן גבוה (540 מ״ג)", "אחוז גרגר נמוך יחסית"],
      bottom: "הטעמים מגיעים עם רשימת רכיבים ארוכה יותר ונתרן גבוה.",
      ingredients: "גרגירי חומוס, מים, שמן, טחינה, מלח, תבלינים, מייצב, חומר משמר.", serving: "ל-100 גרם",
    },
  },
  {
    id: "p11", name: "ממרח חומוס לחיך", type: "חומוס", img: `${IMG}/KIA46_Z_P_7296073006015_1.png`,
    score: 49, grade: "D", confidence: "partial",
    metrics: { protein: 7.0, additives: 4, base: 48, sodium: 610, energy: 312 },
    rowReason: { positive: null, limiting: "ארבעה תוספים; נתרן גבוה מאוד" },
    insightLine: "ממרח חומוס מעובד — ארבעה תוספים ונתרן גבוה מאוד",
    expansion: {
      positive: [],
      limiting: ["ארבעה תוספי מזון", "נתרן גבוה מאוד (610 מ״ג)", "אחוז גרגר נמוך (48%)"],
      bottom: "מעובד יחסית: אחוז גרגר נמוך, נתרן גבוה וריבוי תוספים.",
      ingredients: "מים, גרגירי חומוס, שמן, טחינה, מלח, מייצבים, חומרי טעם, חומר משמר.", serving: "ל-100 גרם",
    },
  },
];

// Score bands (v2 spec §3) — derived from score, contiguous in corpus order.
window.SCORE_BANDS = [
  { id: "b80", label: "80+", min: 80, max: 200, tone: "#1F8F6A" },
  { id: "b70", label: "70–79", min: 70, max: 79, tone: "#3FA07E" },
  { id: "b60", label: "60–69", min: 60, max: 69, tone: "#9A9A5E" },
  { id: "b50", label: "50–59", min: 50, max: 59, tone: "#C49A4A" },
  { id: "b00", label: "מתחת ל-50", min: 0, max: 49, tone: "#C77F5A" },
];

window.bandOf = function bandOf(score) {
  return window.SCORE_BANDS.find((b) => score >= b.min && score <= b.max) || window.SCORE_BANDS[window.SCORE_BANDS.length - 1];
};
