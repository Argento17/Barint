import type { LucideIcon } from "lucide-react";
import {
  Apple,
  Award,
  Baby,
  Beef,
  BookOpen,
  Coffee,
  Cookie,
  Microscope,
  Milk,
  Sandwich,
  Shield,
  TrendingUp,
  Users,
  Zap,
} from "lucide-react";

export const heroTrust: { icon: LucideIcon; label: string }[] = [
  { icon: Award, label: "קריטריונים ברורים" },
  { icon: Microscope, label: "זיהוי דפוסים במוצרים" },
  { icon: Shield, label: "מקורות גלויים ורמת ביטחון" },
];

export const categories: {
  icon: LucideIcon;
  name: string;
  href: string;
  products: string;
  insight: string;
  signals: [number, number, number];
}[] = [
  {
    icon: Beef,
    name: "ניתוח חלבונים",
    href: "#comparisons",
    products: "184 מוצרים",
    insight: "פערים גדולים באיכות מקור",
    signals: [42, 68, 35],
  },
  {
    icon: Sandwich,
    name: "לחמים ודגנים",
    href: "#comparisons",
    products: "312 מוצרים",
    insight: "עומס עיבוד משתנה",
    signals: [58, 74, 46],
  },
  {
    icon: Coffee,
    name: "דגני בוקר",
    href: "#comparisons",
    products: "128 מוצרים",
    insight: "פערי סוכר ותוספים בולטים",
    signals: [76, 63, 82],
  },
  {
    icon: Apple,
    name: "משקאות ותחליפים",
    href: "#comparisons",
    products: "246 מוצרים",
    insight: "הבדלים חדים ברכיבים",
    signals: [51, 57, 69],
  },
  {
    icon: Zap,
    name: "תוספי תזונה",
    href: "#comparisons",
    products: "96 מוצרים",
    insight: "רמת ביטחון תלויה מקור",
    signals: [36, 52, 61],
  },
  {
    icon: Cookie,
    name: "השוואות חטיפים",
    href: "/categories/snacks",
    products: "275 מוצרים",
    insight: "תוספים ועיבוד נפוצים",
    signals: [82, 71, 78],
  },
  {
    icon: Milk,
    name: "גבינות ומוצרי חלב",
    href: "#comparisons",
    products: "167 מוצרים",
    insight: "חלבון ושומן משנים הקשר",
    signals: [39, 66, 43],
  },
  {
    icon: Baby,
    name: "מזון לילדים",
    href: "#comparisons",
    products: "203 מוצרים",
    insight: "פערים גדולים בין מותגים",
    signals: [69, 62, 74],
  },
];

export const comparisons: {
  title: string;
  category: string;
  products: string;
  readTime: string;
  updated: string;
  gradient: string;
  score: number;
  confidenceLevel: "high" | "mediumHigh" | "medium";
  confidenceLabel: string;
  sourceLabel: string;
  signals: string[];
  benchmark: string;
  rankingReason: string;
  criteria: {
    label: string;
    value: string;
    context: string;
    impact: "positive" | "neutral" | "caution";
  }[];
}[] = [
  {
    title: "חלב שקד: איזה מותג מוביל?",
    category: "משקאות צמחיים",
    products: "אלפרו, שופרסל, נטורה, טרה",
    readTime: "6 דקות",
    updated: "עודכן השבוע",
    gradient: "from-zinc-50 to-emerald-50",
    score: 86,
    confidenceLevel: "high",
    confidenceLabel: "ביטחון גבוה",
    sourceLabel: "מקורות זמינים",
    signals: ["סוכר נמוך", "רכיבים קצרים", "ביטחון גבוה"],
    benchmark: "יחסית לקטגוריית משקאות צמחיים",
    rankingReason:
      "מדורג גבוה יותר בעיקר בזכות סוכר נמוך מהממוצע ורשימת רכיבים קצרה יותר; חלבון אינו יתרון מרכזי כאן.",
    criteria: [
      {
        label: "סוכר",
        value: "נמוך מהממוצע",
        context: "פער עקבי מול רוב המתחרים",
        impact: "positive",
      },
      {
        label: "חלבון",
        value: "קרוב לממוצע",
        context: "לא מקבל משקל עודף בדירוג",
        impact: "neutral",
      },
      {
        label: "רכיבים",
        value: "רשימה קצרה יותר",
        context: "פחות מייצבים וממתיקים",
        impact: "positive",
      },
    ],
  },
  {
    title: "יוגורט יווני מול יוגורט רגיל",
    category: "מוצרי חלב",
    products: "השוואה מעמיקה",
    readTime: "5 דקות",
    updated: "השוואה מתעדכנת",
    gradient: "from-zinc-50 to-emerald-50",
    score: 81,
    confidenceLevel: "mediumHigh",
    confidenceLabel: "ביטחון בינוני-גבוה",
    sourceLabel: "נתוני תווית",
    signals: ["חלבון גבוה", "שובע", "סוכר בינוני"],
    benchmark: "יחסית ליוגורטים באותה קטגוריית שומן",
    rankingReason:
      "הדירוג עולה כשהחלבון גבוה והסוכר נשאר בשליטה; מוצרים עם תוספות מתוקות יורדים למרות ערך חלבון טוב.",
    criteria: [
      {
        label: "חלבון",
        value: "גבוה מהממוצע",
        context: "יתרון עקבי ל־100 גרם",
        impact: "positive",
      },
      {
        label: "סוכר",
        value: "בינוני",
        context: "דורש בדיקה לפי טעם ותוספות",
        impact: "neutral",
      },
      {
        label: "שובע",
        value: "אות חיובי",
        context: "שילוב חלבון ומרקם צפוף יותר",
        impact: "positive",
      },
    ],
  },
  {
    title: "חטיפי חלבון: האם באמת בריאים?",
    category: "חלבון וחטיפים",
    products: "יולו, פרוטאין קומפני, טעים",
    readTime: "8 דקות",
    updated: "דורש קריאה ביקורתית",
    gradient: "from-zinc-50 to-emerald-50",
    score: 74,
    confidenceLevel: "medium",
    confidenceLabel: "ביטחון בינוני",
    sourceLabel: "מקורות זמינים",
    signals: ["עיבוד גבוה", "ממתיקים", "חלבון"],
    benchmark: "יחסית לחטיפי חלבון שנמכרים בישראל",
    rankingReason:
      "חלבון גבוה לא מספיק כדי להוביל אם רמת העיבוד, הממתיקים ורשימת הרכיבים יוצרים אותות סותרים.",
    criteria: [
      {
        label: "חלבון",
        value: "גבוה",
        context: "יתרון ברור מול חטיפים רגילים",
        impact: "positive",
      },
      {
        label: "עיבוד",
        value: "גבוה",
        context: "רשימת רכיבים ארוכה יחסית",
        impact: "caution",
      },
      {
        label: "ממתיקים",
        value: "נפוצים",
        context: "משפיעים על שקיפות ההשוואה",
        impact: "caution",
      },
    ],
  },
];

export const productComparisonExample = {
  category: "חלב שיבולת שועל",
  sticker: "בחירה עדיפה בקטגוריה",
  basis: "דירוג יחסי לקטגוריית חלב שיבולת שועל · מבוסס על נתוני תווית זמינים",
  summary:
    "Bari משווה מוצרים דומים ומבליטה את הסיבה להעדפה: פחות סוכר, פחות תוספים ופרופיל רכיבים נקי יותר בתוך אותה קטגוריה.",
  products: [
    {
      name: "חלב שיבולת שועל A",
      label: "מוביל יחסי",
      score: "גבוה",
      tone: "preferred",
      signals: ["פחות סוכר", "פחות תוספים", "רכיבים קצרים", "ביטחון גבוה"],
      note: "מקבל יתרון בגלל שילוב עקבי של סוכר נמוך ורשימת רכיבים קצרה יותר.",
    },
    {
      name: "חלב שיבולת שועל B",
      label: "חלופה סבירה",
      score: "בינוני",
      tone: "baseline",
      signals: ["סוכר גבוה יותר", "יותר מייצבים", "רכיבים דומים", "ביטחון בינוני"],
      note: "נשאר רלוונטי להשוואה, אך מפסיד במדדי סוכר ותוספים יחסית למוצר A.",
    },
  ],
  criteria: [
    { label: "סוכר", winner: "A", detail: "פער יחסי לטובת מוצר A" },
    { label: "תוספים", winner: "A", detail: "רשימה קצרה ונקייה יותר" },
    { label: "מקורות", winner: "A/B", detail: "מבוסס על נתוני תווית זמינים" },
  ],
} as const;

export const guides: {
  title: string;
  type: string;
  icon: LucideIcon;
  time: string;
}[] = [
  { title: "במבה: האם באמת בריאה לילדים?", type: "ניתוח מוצר", icon: Microscope, time: "4 דקות" },
  { title: "דירוג: קורנפלקס מול חלופות", type: "דירוג", icon: Award, time: "7 דקות" },
  { title: "מה באמת בגבינות קוטג' בישראל", type: "מדריך", icon: BookOpen, time: "6 דקות" },
  { title: "לחם מלא: איך לבחור נכון", type: "השוואה", icon: TrendingUp, time: "5 דקות" },
];

export const methodology: {
  icon: LucideIcon;
  step: string;
  title: string;
  description: string;
  signals: string[];
  metric: string;
}[] = [
  {
    icon: BookOpen,
    step: "01",
    title: "איחוד נתוני מוצר",
    description:
      "שם, קטגוריה, רכיבים וערכים תזונתיים עוברים למבנה אחיד כדי שמוצרים דומים יהיו באמת בני־השוואה.",
    signals: ["שם מוצר", "קטגוריה", "נתוני תווית"],
    metric: "Normalization",
  },
  {
    icon: TrendingUp,
    step: "02",
    title: "Benchmark קטגורי",
    description:
      "כל מוצר נמדד מול מוצרים מאותה קטגוריה, כדי שהדירוג לא יעניש או יתגמל בלי הקשר תחרותי.",
    signals: ["מוצרים דומים", "פער יחסי", "הקשר שוק"],
    metric: "Category-relative",
  },
  {
    icon: Microscope,
    step: "03",
    title: "זיהוי אותות תזונתיים",
    description:
      "המערכת בודקת דפוסים כמו סוכר, חלבון, סיבים וצפיפות קלורית ומציגה את האותות שמשפיעים על ההשוואה.",
    signals: ["סוכר", "חלבון", "סיבים"],
    metric: "Nutrition signals",
  },
  {
    icon: Zap,
    step: "04",
    title: "ניתוח רכיבים ועיבוד",
    description:
      "רשימת הרכיבים נבחנת לפי אורך, תוספים, ממתיקים וסימני עיבוד כדי להוסיף שכבת הסבר מעבר לערכים המספריים.",
    signals: ["תוספים", "ממתיקים", "עיבוד"],
    metric: "Processing signals",
  },
  {
    icon: Shield,
    step: "05",
    title: "רמת ביטחון והסבר",
    description:
      "כל מסקנה מוצגת עם בסיס מקור איכותי ונימוק קצר שמסביר למה מוצר אחד עדיף בתוך ההשוואה.",
    signals: ["מקורות", "ביטחון", "נימוק"],
    metric: "Evidence basis",
  },
];

export const trustPillars: { icon: LucideIcon; label: string; desc: string }[] = [
  { icon: Shield, label: "ללא ניגודי עניינים", desc: "עקרון עצמאות תוכן" },
  { icon: Microscope, label: "מבוסס מקורות", desc: "תווית + רגולציה" },
  { icon: BookOpen, label: "מתודולוגיה גלויה", desc: "כל קריטריון מוסבר" },
  { icon: Users, label: "קהילת קוראים", desc: "דיונים ושאלות" },
];
