import type { LucideIcon } from "lucide-react";
import {
  Apple,
  Award,
  Baby,
  Beef,
  BookOpen,
  Coffee,
  Cookie,
  MessageCircle,
  Microscope,
  Milk,
  Sandwich,
  Shield,
  Sparkles,
  TrendingUp,
  Users,
  Zap,
} from "lucide-react";

export const heroTrust: { icon: LucideIcon; label: string }[] = [
  { icon: Award, label: "השוואות חדשות מדי שבוע" },
  { icon: Microscope, label: "מדריכי רכיבים ומחקרים" },
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

export const rankings: { title: string; score: string; note: string }[] = [
  { title: "משקאות סויה — פאנל Bari", score: "עדכני", note: "12 מותגים" },
  { title: "חטיפי חלבון — דירוג שקיפות תווית", score: "חדש", note: "9 מותגים" },
  { title: "יוגורטים עם פחות סוכר", score: "מעודכן", note: "קטגוריה" },
  { title: "דגני בוקר — סיבים ותוספים", score: "בבדיקה", note: "מדריך" },
];

export const methodology: {
  icon: LucideIcon;
  title: string;
  description: string;
}[] = [
  {
    icon: Microscope,
    title: "מחקר מעמיק",
    description:
      "כל השוואה ודירוג מתחילים מניתוח רכיבים, תזונה ל־100 גרם והקשר רגולטורי — בלי קיצורי דרך.",
  },
  {
    icon: Shield,
    title: "אובייקטיביות",
    description: "קריטריונים ברורים, ציון עם רמת ביטחון ותאריך — בלי ניסוחים שיווקיים.",
  },
  {
    icon: BookOpen,
    title: "תוכן חינוכי",
    description: "מדריכים והסברים שמחברים בין המספרים למה שחשוב לכם בפועל.",
  },
];

export const ingredients: {
  name: string;
  status: string;
  description: string;
  color: string;
  bgColor: string;
  badge: string;
}[] = [
  {
    name: "E171 (טיטניום דו־חמצני)",
    status: "שנוי במחלוקת",
    description:
      "צבע מאכל לבן שנמצא במוצרים רבים. נאסר באיחוד האירופי ב־2022; בישראל הסטטוס עשוי להשתנות — עקבו אחרי עדכוני הרשות.",
    color: "from-orange-600 to-red-600",
    bgColor: "from-orange-50 to-red-50",
    badge: "מבוסס מקורות",
  },
  {
    name: "אינולין (Inulin)",
    status: "מוסבר בקצרה",
    description:
      "סיב תזונתי טבעי המופק מצמחים. שימושי להבנת רשימת רכיבים — לא המלצה אישית.",
    color: "from-emerald-600 to-green-700",
    bgColor: "from-emerald-50 to-green-50",
    badge: "נבדק ע״י צוות Bari",
  },
];

export const trustPillars: { icon: LucideIcon; label: string; desc: string }[] = [
  { icon: Shield, label: "ללא ניגודי עניינים", desc: "עקרון עצמאות תוכן" },
  { icon: Microscope, label: "מבוסס מקורות", desc: "תווית + רגולציה" },
  { icon: BookOpen, label: "מתודולוגיה גלויה", desc: "כל קריטריון מוסבר" },
  { icon: Users, label: "קהילת קוראים", desc: "דיונים ושאלות" },
];

export const community: {
  icon: LucideIcon;
  title: string;
  body: string;
  cta: string;
  href: string;
}[] = [
  {
    icon: MessageCircle,
    title: "פורום דיונים",
    body: "שאלות על רכיבים, קריאת תווית והשוואות בין קטגוריות — עם ניטור איכות תוכן.",
    cta: "לכניסה לפורום",
    href: "#comparisons",
  },
  {
    icon: Sparkles,
    title: "מדריכי קהילה",
    body: "סיכומים קצרים של קוראים לצד עורכים — כדי ללמוד מהר בלי לזנוח את המקורות.",
    cta: "למדריכים",
    href: "#guides",
  },
  {
    icon: Users,
    title: "ניוזלטר שבועי",
    body: "דירוגים חדשים, השוואות שעלו לאוויר וזרקור רכיב — בלי רעש.",
    cta: "להרשמה",
    href: "#newsletter",
  },
];
