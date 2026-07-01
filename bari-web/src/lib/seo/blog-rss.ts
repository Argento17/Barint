import { absoluteUrl } from "@/lib/site-url";

export type BlogRssEntry = {
  title: string;
  description: string;
  path: string;
  pubDate: string;
};

/** RSS entries for published blog articles (ISO 8601 pubDate). */
export const BLOG_RSS_ENTRIES: BlogRssEntry[] = [
  {
    title: "נסטלה מסירה צבעי מאכל סינתטיים בארה״ב — ומה עם ישראל?",
    path: "/blog/food-dyes",
    description:
      "חוק, התחייבות וולונטרית ותווית אזהרה — שלושה דברים שמתערבבים. ולמה הסרת צבע היא שינוי קוסמטי ולא תזונתי.",
    pubDate: "2026-06-30T08:00:00Z",
  },
  {
    title: "מה באמת קורה בחלב בישראל?",
    path: "/blog/milk-analysis",
    description:
      "ניתוח מעמיק על חלב ומוצרי חלב מעובדים בישראל — עקביות, טריות והשוואה אסטרטגית.",
    pubDate: "2026-05-01T08:00:00Z",
  },
  {
    title: "20 שמני זית. 10 מותגים.",
    path: "/blog/shemen-zayit",
    description: "סקירת שמני זית מרכזיים במדף הישראלי.",
    pubDate: "2026-06-01T08:00:00Z",
  },
  {
    title: "סוכרים אלכוהוליים בחטיפי חלבון",
    path: "/blog/sugar-alcohols",
    description: "מלטיטול וחבריו — מה מופיע על המדף ומה כדאי לדעת.",
    pubDate: "2026-06-15T08:00:00Z",
  },
  {
    title: "חומוס בשוק הישראלי",
    path: "/blog/hummus",
    description: "מפת חומוס מבוססת השוואת Bari.",
    pubDate: "2026-06-10T08:00:00Z",
  },
  {
    title: "יוגורט בישראל",
    path: "/blog/yogurt",
    description: "מה מבדיל בין יוגורטים במדף.",
    pubDate: "2026-06-08T08:00:00Z",
  },
  {
    title: "לחם בשוק הישראלי",
    path: "/blog/lechem",
    description: "סקירת לחמים ומה משפיע על הציון.",
    pubDate: "2026-06-05T08:00:00Z",
  },
  {
    title: "לחם יומיומי",
    path: "/blog/bread-everyday",
    description: "לחמים לשימוש יומיומי — ממצאים מהמדף.",
    pubDate: "2026-06-12T08:00:00Z",
  },
  {
    title: "לחמים בולטים",
    path: "/blog/bread-standouts",
    description: "מוצרים שבולטים לטובה ולרעה.",
    pubDate: "2026-06-12T09:00:00Z",
  },
  {
    title: "פער ה-wellness בלחם",
    path: "/blog/bread-wellness-gap",
    description: "פער בין שיווק wellness לבין הרכב בפועל.",
    pubDate: "2026-06-12T10:00:00Z",
  },
  {
    title: "ניתוח לחם (ארכיון)",
    path: "/blog/bread-analysis",
    description: "מפנה לסדרת מאמרי הלחם.",
    pubDate: "2026-06-01T08:00:00Z",
  },
];

export function blogRssAbsoluteUrl(path: string): string {
  return absoluteUrl(path);
}
