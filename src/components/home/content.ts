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
  { icon: Award, label: "השוואות חדשות מדי שבוע" },
  { icon: Microscope, label: "ניתוח מוצרים ומחקרים" },
  { icon: Shield, label: "דירוגים שקופים ומבוססי קריטריונים" },
];

export const categories: {
  icon: LucideIcon;
  name: string;
  color: string;
  bg: string;
}[] = [
  { icon: Beef, name: "חלבון", color: "from-red-500 to-orange-500", bg: "from-red-50 to-orange-50" },
  { icon: Sandwich, name: "לחמים", color: "from-amber-500 to-yellow-600", bg: "from-amber-50 to-yellow-50" },
  { icon: Coffee, name: "דגני בוקר", color: "from-yellow-600 to-amber-700", bg: "from-yellow-50 to-amber-50" },
  { icon: Apple, name: "משקאות", color: "from-blue-500 to-cyan-500", bg: "from-blue-50 to-cyan-50" },
  { icon: Zap, name: "תוספי תזונה", color: "from-emerald-500 to-green-600", bg: "from-emerald-50 to-green-50" },
  { icon: Cookie, name: "חטיפים", color: "from-purple-500 to-pink-500", bg: "from-purple-50 to-pink-50" },
  { icon: Milk, name: "גבינות", color: "from-indigo-500 to-blue-500", bg: "from-indigo-50 to-blue-50" },
  { icon: Baby, name: "מוצרים לילדים", color: "from-pink-500 to-rose-500", bg: "from-pink-50 to-rose-50" },
];

export const comparisons: {
  title: string;
  category: string;
  products: string;
  readTime: string;
  updated: string;
  gradient: string;
}[] = [
  {
    title: "חלב שקד: איזה מותג הכי בריא?",
    category: "משקאות צמחיים",
    products: "אלפרו, שופרסל, נטורה, טרה",
    readTime: "6 דקות",
    updated: "עודכן השבוע",
    gradient: "from-amber-50 to-orange-50",
  },
  {
    title: "יוגורט יווני מול יוגורט רגיל",
    category: "מוצרי חלב",
    products: "השוואה מעמיקה",
    readTime: "5 דקות",
    updated: "נבדק ע״י צוות Bari",
    gradient: "from-blue-50 to-cyan-50",
  },
  {
    title: "חטיפי חלבון: האם באמת בריאים?",
    category: "חלבון וחטיפים",
    products: "יולו, פרוטאין קומפני, טעים",
    readTime: "8 דקות",
    updated: "מבוסס מקורות",
    gradient: "from-purple-50 to-pink-50",
  },
];

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
  title: string;
  description: string;
}[] = [
  {
    icon: BookOpen,
    title: "איסוף נתונים",
    description:
      "מוצרים, רכיבים וערכים תזונתיים נאספים ממקורות זמינים ומאורגנים למבנה אחיד.",
  },
  {
    icon: Microscope,
    title: "ניתוח אלגוריתמי",
    description:
      "המערכת מזהה דפוסים כמו צפיפות קלורית, איכות רכיבים, רמות סוכר, חלבון, סיבים ועיבוד.",
  },
  {
    icon: Shield,
    title: "דירוג והשוואה",
    description:
      "המוצרים מדורגים ומושווים בתוך קטגוריות דומות, כדי שההשוואה תהיה הוגנת ושימושית.",
  },
];

export const trustPillars: { icon: LucideIcon; label: string; desc: string }[] = [
  { icon: Shield, label: "ללא ניגודי עניינים", desc: "עקרון עצמאות תוכן" },
  { icon: Microscope, label: "מבוסס מקורות", desc: "תווית + רגולציה" },
  { icon: BookOpen, label: "מתודולוגיה גלויה", desc: "כל קריטריון מוסבר" },
  { icon: Users, label: "קהילת קוראים", desc: "דיונים ושאלות" },
];
