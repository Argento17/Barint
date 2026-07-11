// TASK-557 — Sweetener guide (/madrichim/sweeteners). UNAPPROVED DRAFT.
//
// Copy source of truth: C:\Bari\02_products\guides\sweetener_guide_he_draft_v1.md
// (source sha256 at this port: 811e6c22417bd1f6a2b07ab5d966b5d6033df46dd21df8f080158230d00fbaa6
// — version 13, Gate 2 pass 10: PASS, 0 CRITICAL / 0 HIGH).
//
// Every Hebrew string in `sections` and `sources` below is ported VERBATIM from the
// CONSUMER-COPY sentinel region of that file — strictly the text between
// `<!-- BARI:CONSUMER-COPY:BEGIN -->` and `<!-- BARI:CONSUMER-COPY:END -->`, located by those
// sentinels, never by line range. Edits applied: stripping the markdown "## N. " heading-number
// prefix, and stripping the markdown "- ", "**...**", and backtick code-span markup from the
// sources block (pure markdown syntax, not prose) — no word was added, removed, or reordered.
//
// This port REPLACES the prior v7 port in full. v8–v13 restructured the argument after the
// glycemic-index table (§§3–7) around explicit "therefore" bridges between sections (owner
// instruction; see the source file's own "תיקון גרסה 4" changelog). Paragraph counts and
// wording changed materially and are not diffable against the old v7 text section-by-section.
// Two v7-era defects are gone as a result of the full replacement, not patched individually:
// the acesulfame-K "sits almost entirely in yogurt" distribution claim (unsupported, deleted
// upstream), and a missing-yod spelling error in the Stevia label term (see the sources-block
// comment below for the specific fix).
//
// `structuralStrings` below is a SEPARATE provenance class — see its own block comment. It is
// out of scope for this port (not part of the CONSUMER-COPY band) and is left unchanged.
//
// NO product data, NO scores, NO corpus counts — this is a pure educational guide. A
// prevalence/product-count chart is intentionally NOT modelled here (consumer copy may
// never narrate Bari's data; a visual count would reintroduce it).

export interface SweetenerGuideSection {
  /** Stable key for React lists + section anchors. */
  id: string;
  /** Verbatim section heading (markdown "N. " number prefix stripped). */
  heading: string;
  /** Verbatim body paragraphs, in source order. */
  paragraphs: string[];
  /**
   * Optional statutory package warning, quoted character-for-character. Rendered by the
   * page as a distinct "label print" element set apart from the body prose, NOT as prose.
   */
  statutoryWarning?: string;
  /** When true, the page renders the glycemic-index table after this section's paragraphs. */
  showGlycemicTable?: boolean;
}

export interface SweetenerGlycemicRow {
  /** Sweetener name (verbatim label term). */
  name: string;
  /** Glycemic index value. */
  gi: number;
}

export interface SweetenerSourcesBlock {
  heading: string;
  /**
   * NO intro sentence. The provenance sentence that named the internal fact-base file is not
   * part of the consumer band; the block opens directly on `items[0]`. Left optional (not
   * removed from the type) so a future SIGNED intro could be added without a shape change —
   * currently unset, and must stay unset until Content authors one.
   */
  intro?: string;
  items: string[];
}

// ── Statutory warnings — VERBATIM, character-for-character (do NOT edit for style) ──────
// §2 polyol warning and §6 aspartame warning, exactly as they appear inside the quoted
// spans of the consumer copy. Confirmed byte-exact against the v13 band at this port. Kept
// as named constants so the "label print" rendering and any future verbatim check reference
// a single source.
export const SWEETENER_STATUTORY_WARNINGS = {
  polyols: "צריכה מופרזת עלולה לגרום לפעילות מעיים מוגברת",
  aspartame: "מכיל אספרטיים (מקור של פנילאלנין)",
} as const;

// ── Glycemic-index table — real tabular data (§2). Order per the source's own listing:
// sucrose 65, then the shelf's polyols. Values cross-checked against v13's §2 prose (sucrose
// 65, maltitol 35, xylitol 13, sorbitol 9, isomalt 9, erythritol 0) — consistent, unchanged
// at this port. Rendered as a horizontally-scrollable, tabular-nums table (NOT a chart).
export const SWEETENER_GLYCEMIC_ROWS: SweetenerGlycemicRow[] = [
  { name: "סוכר", gi: 65 },
  { name: "מלטיטול", gi: 35 },
  { name: "קסיליטול", gi: 13 },
  { name: "סורביטול", gi: 9 },
  { name: "איזומלט", gi: 9 },
  { name: "אריתריטול", gi: 0 },
];

// ── Sections 1–7, verbatim from the consumer-copy sentinel region (v13 port) ────────────
export const SWEETENER_SECTIONS: SweetenerGuideSection[] = [
  {
    id: "opening",
    heading: "פתיח: מה זה ממתיק ומה באמת נמצא על המדף",
    paragraphs: [
      "ממתיק הוא חומר שנותן טעם מתוק במקום סוכר, או לצד מעט סוכר. תפגשו ממתיקים בעיקר במוצרים שכתוב עליהם \"ללא סוכר\", \"מופחת סוכר\" או \"דיאט\", וגם בממתיקים השולחניים שמוסיפים לקפה.",
      "בכותרות מדברים בעיקר על אספרטיים, סכרין ולאחרונה אריתריטול. על המדף עצמו הסיפור שונה: בין הממתיקים הנפוצים ביותר נמצאים דווקא מלטיטול וסוכרלוז, שמות אחרים לגמרי.",
      "המדריך הזה עושה שלושה דברים. הוא אומר לכם איזה ממתיק אתם צורכים, בשם שבו הוא כתוב על התווית. הוא מראה באילו מוצרים הוא מופיע. והוא מביא את מה שידוע עליו מהמחקר, לשם היכרות.",
    ],
  },
  {
    id: "polyols",
    heading: "סוכרים כוהליים (רב-כוהליים)",
    paragraphs: [
      "קחו לדוגמה את \"עוגת הבית שיש אסם\". הרכיב הראשון ברשימה שלה הוא סוכר, ובכל זאת מופיע בה גם סורביטול. סורביטול הוא סוג של סוכר כוהלי, וכאן תפקידו לשמור על העוגה רכה. וזו נקודה ששווה לזכור: סוכר כוהלי יכול להופיע גם במוצרים מתוקים רגילים, בדיוק כמו בעוגה הזאת.",
      "הסוכרים הכוהליים הם משפחה כימית אחת. מלטיטול, סורביטול, אריתריטול, קסיליטול ואיזומלט שייכים כולם אליה. הגוף מעכל אותם אחרת מסוכר רגיל, ובשפת החוק הם נקראים \"רב-כוהליים\". מלטיטול הוא הנפוץ מביניהם, וזה שכן משמש כדי למתק. תפגשו בו בשוקולד, בעוגיות ובחטיפי חלבון, והוא נותן בערך חצי מהקלוריות של סוכר רגיל.",
      "אם קניתם מוצר עם סוכרים כוהליים, אולי ראיתם עליו משפט קטן: \"צריכה מופרזת עלולה לגרום לפעילות מעיים מוגברת\". זו אזהרה שהחוק מחייב. היא מופיעה כשמשקל הסוכרים הכוהליים שנוספו למוצר עולה על עשירית ממשקלו. בחפיסה של 100 גרם, זה יותר מ-10 גרם. על ממתיק שולחני היא מופיעה בכל כמות.",
      "הסיבה מאחוריה פשוטה. חלק מהסוכר הכוהלי לא נספג במעי הדק. מה שנשאר ממשיך אל המעי הגס, מושך אליו מים, וחיידקים מפרקים אותו שם. בכמות גדולה אפשר להרגיש את זה בבטן. לכן המחוקק ביקש לציין את זה על האריזה.",
      "יש עוד הבדל בין הסוכרים הכוהליים ששווה להכיר. האינדקס הגליקמי מודד כמה מהר חומר מעלה את הסוכר בדם. מספר נמוך אומר שהסוכר בדם עולה לאט יותר, וזה כל מה שהוא אומר. לסוכר רגיל האינדקס הוא 65. למלטיטול הוא 35, נמוך יותר אבל רחוק מאפס. לאריתריטול הוא 0. אצל שאר הסוכרים הכוהליים שעל המדף האינדקס נמוך אף יותר: סורביטול ואיזומלט סביב 9, וקסיליטול סביב 13. מלטיטול הוא היחיד מהם שנמצא בטווח הנמוך; כל השאר בטווח הנמוך מאוד. לכן הוא מקבל כאן פסקה משלו. הוא מהנפוצים ביותר, והוא גם החריג בקבוצה.",
    ],
    statutoryWarning: SWEETENER_STATUTORY_WARNINGS.polyols,
    showGlycemicTable: true,
  },
  {
    id: "high-intensity",
    heading: "ממתיקים בעצימות גבוהה: סוכרלוז ואצסולפאם-K",
    paragraphs: [
      "טבלת שוקולד מריר ללת\"ס של שוקולד פרה מצהירה על שלושה ממתיקים על אותה אריזה: אריתריטול, מלטיטול וסוכרלוז. אריתריטול ומלטיטול הם סוכרים כוהליים. סוכרלוז שייך למשפחה אחרת.",
      "וזאת הקבוצה השנייה על המדף: הממתיקים בעצימות גבוהה. סוכרלוז ואצסולפאם-K ממתקים חזק מאוד, אבל הם אינם סוכרים כוהליים. וכאן העיקר: האזהרה שראינו כתובה על משפחה אחת בלבד, הסוכרים הכוהליים. סוכרלוז ואצסולפאם-K לא שייכים אליה, ולכן החוק לא מגיע אליהם כלל, בשום כמות.",
      "וכך גם על מוצר אחד יכולים להופיע ממתיק שהחוק לא נוגע בו וממתיק שהחוק כן נוגע בו. זה מה שקורה בטבלת שוקולד מריר ללת\"ס.",
      "הנפוץ מבין השניים הוא סוכרלוז. בפברואר 2026 בדקה הרשות האירופית לבטיחות מזון (EFSA) את סוכרלוז מחדש, ואישרה שוב את הכמות היומית המותרת לשימושים המאושרים היום: 15 מיליגרם לכל קילוגרם משקל גוף ביום.",
      "אחריו אצסולפאם-K, שתפגשו למשל בדנונה פרו לת\"ס בננה טופי, יחד עם סוכרלוז על אותה תווית. גם אותו בדקה EFSA מחדש, ב-2025, וקבעה כמות יומית מותרת של 15 מיליגרם לכל קילוגרם משקל גוף ביום, במקום 9 שהיה קודם.",
    ],
  },
  {
    id: "plant-derived",
    heading: "ממתיקים ממקור צמחי: סטיביה ופרי הנזיר",
    paragraphs: [
      "גם הממתיקים ממקור צמחי אינם סוכרים כוהליים, ולכן גם עליהם החוק לא חל. זו קבוצה שלישית על המדף, וההבדל מהקודמות הוא המקור: כאן הוא צמח.",
      "הבולט בהם הוא סטיביה. על התווית היא כתובה בשם המדויק \"גליקוזידים של סטיביול\", וזה השם שכדאי לחפש ברשימת הרכיבים. אלה החומרים המתוקים שמפיקים מעלי הצמח, והם אינם סוכר כוהלי, ולכן החוק לא מגיע אליהם בשום כמות.",
      "אותם תפגשו למשל בגרנולה תותים ללת\"ס של טרו. אותה גרנולה מצהירה גם על אריתריטול, שהוא כן סוכר כוהלי. שני הממתיקים מוצהרים יחד על אותה תווית.",
      "פרי הנזיר פחות נפוץ על המדף. החומרים המתוקים בו נקראים מוגרוזידים, וגם הם אינם סוכר כוהלי. אותם תפגשו למשל ב\"עוגיות קיטו שקד לוז\" של קיטו, לצד אריתריטול על אותה תווית.",
    ],
  },
  {
    id: "erythritol-headline",
    heading: "הכותרת של אריתריטול: מה נמצא ומה לא",
    paragraphs: [
      "כל אלה דרכים לעקוף את המחיר של הסוכרים הכוהליים. אבל בתוך הקבוצה עצמה יש אחד שחמק מאי-הנוחות הזאת: אריתריטול. האינדקס הגליקמי שלו אפס, והגוף סופג אותו כמעט כולו כבר במעי הדק. לכן הרבה פחות ממנו מגיע אל המעי הגס, המקום שממנו באה אי-הנוחות של שאר הקבוצה. תפגשו בו למשל ב\"עוגיות קיטו שקד לוז\" של קיטו.",
      "ודווקא הוא, הממתיק שחמק מאי-הנוחות, הוא זה שקיבל בשנים האחרונות כותרות שקשרו אותו לבריאות הלב. כדאי להבין מה הכותרות מדדו ומה לא. המחקרים שעוררו אותן מדדו את רמת האריתריטול בדם בצום. והנה נקודה חשובה: הגוף מייצר אריתריטול גם בעצמו. לכן רמה גבוהה בדם משקפת שני דברים ביחד: גם את מה שנאכל, וגם את מה שהגוף ייצר בכוחות עצמו.",
      "היה גם מחקר שבו אנשים אכלו אריתריטול ממש, מנה גדולה אחת, ונמדדה בו עלייה בפעילות הטסיות בדם. המנה שנבדקה הייתה גדולה בהרבה מהכמות שיש במוצר רגיל.",
      "מחקר אחר בדק את השאלה בדרך אחרת. הוא נשען על הבדלים גנטיים טבעיים בין אנשים, כדי לבדוק אם אריתריטול עצמו גורם למחלות לב וחילוף חומרים. הוא לא מצא עדות שתומכת בכך. אף רשות רגולטורית לא שינתה את עמדתה בעקבות הממצאים האלה.",
      "קסיליטול הופיע בדיווחים דומים באותה תקופה, ועליו חלה אותה הבחנה בדיוק. יש הבדל בין מה שנמדד בדם לבין מה שנאכל במזון. מה שנמדד בדם, מה שנאכל, ומה שהגוף מייצר בעצמו הם שלושה דברים שונים, וההבחנה ביניהם היא לב העניין.",
    ],
  },
  {
    id: "not-in-products",
    heading: "מה לא נמצא במוצרים האלה",
    paragraphs: [
      "רוב השמות שסביבם סובבת השיחה הציבורית כמעט לא נמצאים על המדף הזה. היוצא מן הכלל הוא אריתריטול, שנמצא גם בכותרות וגם על המדף. אבל אספרטיים וסכרין, שני הוותיקים של הוויכוח, אינם בשימוש במוצרים שכאן, וגם אלולוז לא.",
      "על אספרטיים כדאי לדעת עוד דבר, למקרה שתפגשו בו במוצר אחר. החוק בישראל מחייב מוצר שמכיל אותו לשאת אזהרה: \"מכיל אספרטיים (מקור של פנילאלנין)\". המשפט הזה הוא חלק מדרישות התיוג בישראל למוצרים שמכילים אספרטיים.",
    ],
    statutoryWarning: SWEETENER_STATUTORY_WARNINGS.aspartame,
  },
  {
    id: "not-yet-known",
    heading: "מה עדיין לא ידוע",
    paragraphs: [
      "לסיום, כמה דברים שאי אפשר לדעת מהתווית או מהמחקר. הכמות המדויקת של הממתיק במוצר כמעט אף פעם לא כתובה על התווית. אפשר לדעת אילו ממתיקים יש במוצר, אבל לא בכמה.",
      "יש לכך חריג אחד: אזהרת הסוכרים הכוהליים. היא לא נוקבת בגרמים, אבל עצם הופעתה על מוצר מזון מסמנת שמשקל הסוכרים הכוהליים בו עבר עשירית ממשקל המוצר. זה אות המינון היחיד שהתווית באמת נותנת.",
      "הרגישות של מערכת העיכול משתנה מאדם לאדם, וסף אי-הנוחות אינו זהה לכולם. והממצאים על הלב שהוזכרו כאן אינם קובעים שצריכת הכמויות שיש במוצרים גורמת נזק. זה מה שהמחקר הראה עד עכשיו, וזה גם מה שהוא עדיין לא הראה.",
    ],
  },
];

// ── Sources block — verbatim from the consumer-copy region (§ מקורות), v13 port ─────────
// One item fixed at this port: the Hebrew-label-names item's Stevia term corrected from
// "גליקוזידים של סטביול" (missing yod, a defect) to "גליקוזידים של סטיביול" — the correct
// label spelling, matching the term used in §4's prose above.
//
// NOTE (unresolved, carried forward): this block still renders full English academic
// citations (author/journal/DOI/PMID). The source file's own gate zone still marks that
// render-form as an unresolved editorial decision (draft EXCEPTION-005, not committed to the
// live exception registry) — flagged again here, unchanged from the prior port.
export const SWEETENER_SOURCES: SweetenerSourcesBlock = {
  heading: "מקורות",
  items: [
    "תקנות הגנה על בריאות הציבור (מזון) (סימון מזון המכיל ממתיק מסוגים מסוימים), התשע״ט-2018 (בתוקף מ-1 בינואר 2021). מקור לנוסח האזהרה המחייבת על רב-כוהליים (\"צריכה מופרזת עלולה לגרום לפעילות מעיים מוגברת\"), לסף של מעל 10 אחוזים ממשקל המזון, לכלל שהאזהרה חלה על ממתיק שולחני בכל כמות, ולנוסח אזהרת האספרטיים (\"מכיל אספרטיים (מקור של פנילאלנין)\"). אומת מול Nevo ומול Wikisource.",
    "EFSA, הערכה מחודשת של סוכרלוז (E955), פברואר 2026 — EFSA Journal 2026;24:e9854. DOI 10.2903/j.efsa.2026.9854, PMID 41710869. מקור לאישור מחדש של הצריכה היומית המותרת של סוכרלוז לשימושים המאושרים כיום, 15 מ\"ג לכל ק\"ג משקל גוף ליום.",
    "EFSA, הערכה מחודשת של אצסולפאם-K (E950), 2025. DOI 10.2903/j.efsa.2025.9317. מקור לעדכון הצריכה היומית המותרת ל-15 מ\"ג לכל ק\"ג משקל גוף ליום, במקום 9 מ\"ג שנקבע קודם לכן (SCF, 2000).",
    "Livesey G. Health potential of polyols as sugar replacers, with emphasis on low glycaemic properties. Nutr Res Rev 2003;16(2):163–191. DOI 10.1079/nrr200371, PMID 19087388. מקור לערכי האינדקס הגליקמי (סוכר 65, מלטיטול 35, אריתריטול 0, סורביטול 9, איזומלט 9, קסיליטול 13) ולערך הקלורי של מלטיטול (כמחצית מזה של סוכר).",
    "Witkowski M. et al. Ingestion of the Non-Nutritive Sweetener Erythritol… ATVB 2024. DOI 10.1161/ATVBAHA.124.321019. מקור לממצא שאכילת מנה גדולה בודדת של אריתריטול העלתה את פעילות הטסיות. מדובר במחקר אכילה, במינון גבוה בהרבה מהצריכה הרגילה.",
    "Khafagy R, Paterson AD, Dash S. Erythritol as a Potential Causal Contributor to Cardiometabolic Disease: A Mendelian Randomization Study. Diabetes 2024;73(2):325–331. DOI 10.2337/db23-0330, PMID 37939167. מקור לממצא שלא נמצאה עדות תומכת לקשר סיבתי בין רמת אריתריטול במחזור הדם לבין תחלואה לבבית-מטבולית.",
    "Witkowski M. et al. Eur Heart J 2024. DOI 10.1093/eurheartj/ehae244, לצד ביקורת שפורסמה DOI 10.1093/eurheartj/ehaf058. מקור לאזכור קסיליטול באותה תקופה ולאותה הבחנה בין רמה נמדדת בדם לבין צריכה במזון.",
    "שמות התווית העברית (מלטיטול, סורביטול, אריתריטול, קסיליטול, איזומלט, סוכרלוז, \"גליקוזידים של סטיביול\", מוגרוזידים של פרי הנזיר, אספרטם/אספרטיים) — כפי שהם מופיעים על התווית בעברית.",
    "המידע כאן הוא לצורך היכרות בלבד ואינו תחליף לייעוץ רפואי.",
  ],
};

// ── Structural strings ────────────────────────────────────────────────────────────────
// Two different provenance classes — kept explicitly distinct, do not merge them.
//
// (A) CONTENT-AUTHORED, pulled verbatim from the source file's gate-zone section
//     "מחרוזות מבניות מהפרונטאנד — עותק שחובר על ידי Content (v4)". These are draft copy,
//     same as everything else in this file and subject to the same second gate — but they
//     are Content's words now, not a Frontend placeholder:
//       - eyebrow: "מדריכים" — Content's own description: the site's category label, tied
//         to the site's label registry.
//       - title: "מדריך הממתיקים".
//       - deck: one sentence, Content marked it "recommended, not required" and noted the
//         opening section stands on its own if Design omits it. Rendered as an optional
//         hero subtitle.
//       - GI table: column 1 "ממתיק", column 2 "אינדקס גליקמי", plus an optional caption
//         sentence for below the table. Content also offered an optional third-column
//         header "טווח" for a low/very-low marking column — NOT used, this table has no
//         such column, so it is not force-fit in.
//
// (B) STILL FRONTEND-OWNED / UNSIGNED — explicitly NOT resolved by Content's block, and not
//     silently swapped for something adjacent:
//       - draftBanner: Content's own note states this string is "NOT consumer copy... an
//         internal pre-launch status marker... must come down before go-live" and declines
//         to author consumer text for it. Kept as the same developer-authored string as
//         before — now cross-confirmed as out of Content's scope, not assumed.
//       - The statutory-warning label kicker ("נוסח האזהרה על האריזה", the small caption
//         over each verbatim warning box) is a DIFFERENT UI element from the hero eyebrow.
//         Content's own note hedges exactly on this case: "if the kicker tags a different
//         element (card/section), Design/Frontend will show me what it tags and I'll attach
//         a dedicated default." This page's kicker labels the statutory-warning box, not the
//         hero — Content has not seen that specific element, so its eyebrow string is NOT
//         substituted in and no new string is invented here either. It stays the same
//         developer-authored placeholder as the prior round; flagged again in this return
//         for a follow-up Content pass once they can see which element it labels.
export interface SweetenerStructuralStrings {
  eyebrow: string;
  title: string;
  /** Optional per Content's own instruction — render only if present. */
  deck: string | null;
  giTable: {
    columnName: string;
    columnGi: string;
    /** Optional caption below the table — render only if present. */
    caption: string | null;
  };
}

export const SWEETENER_STRUCTURAL_STRINGS: SweetenerStructuralStrings = {
  eyebrow: "מדריכים",
  title: "מדריך הממתיקים",
  deck: "מה באמת נמצא על המדף, בשם שבו זה מופיע על התווית.",
  giTable: {
    columnName: "ממתיק",
    columnGi: "אינדקס גליקמי",
    caption: "אינדקס גליקמי מודד כמה מהר החומר מעלה את הסוכר בדם. סוכר = 65.",
  },
};

// ── Page assembly VM ───────────────────────────────────────────────────────────────────
export interface SweetenerGuideVM {
  /** Build-status marker (frontend-owned, NOT editorial copy — see block comment above). */
  draftBanner: string;
  structuralStrings: SweetenerStructuralStrings;
  sections: SweetenerGuideSection[];
  glycemicRows: SweetenerGlycemicRow[];
  sources: SweetenerSourcesBlock;
}

export const sweetenerGuide: SweetenerGuideVM = {
  draftBanner: "טיוטה · לא לפרסום · העמוד טרם אושר",
  structuralStrings: SWEETENER_STRUCTURAL_STRINGS,
  sections: SWEETENER_SECTIONS,
  glycemicRows: SWEETENER_GLYCEMIC_ROWS,
  sources: SWEETENER_SOURCES,
};
