export const SNACK_COMPARISON_HREF = "/hashvaot/snacks";

export const snackComparisonMeta = {
  title: "השוואת חטיפים | Bari",
  description:
    "מנוע השוואה חקירתי לחטיפי המדף: מבנה, עיבוד, סוכר, תוספות ופערי מיצוב במקום רשימת קניות.",
} as const;

/** Shelf methodology lines — stats, data-gap disclosure, natural-sugar caveat, closing disclaimer. No NOVA/BSIP/cap vocabulary. */
export const snacksShelfMethodologyLines = [
  "ניתחנו את מדף חטיפי הדגנים בשופרסל — שמות, רכיבים וערכי תזונה ל-100 גרם ישירות מדף המוצר.",
  "כל ערך תזונה עבר בדיקת סבירות ל-100 גרם; פאנלים לא־סבירים הוצאו מהדירוג.",
  "מוצרים שנתוני התווית שלהם לא הספיקו לחישוב עקבי לא נוקדו ואינם מוצגים.",
  "בחטיפי תמרים, הסוכר הגבוה מגיע מהפרי עצמו ולא מסוכר שנוסף — הציון מתחשב בהבדל, אך ערכי סוכר גבוהים עדיין משפיעים על מיקום המוצר.",
  "חטיפי חלבון (פרוטאין) נמדדים בקטגוריה נפרדת ומוצגים בעמוד משלהם.",
  "ציוני Bari מתעדים מבנה מוצר ואינם המלצה תזונתית.",
] as const;
