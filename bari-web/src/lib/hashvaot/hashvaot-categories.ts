/**
 * Hashvaot category registry.
 * DRAFT subtext below is pending Content + QA sign-off.
 */

export type HashvaotCategoryStatus = "live" | "building";

export interface HashvaotCategory {
  id: string;
  title: string;
  status: HashvaotCategoryStatus;
  countLabel?: string;
  href?: string;
  description?: string;
  comingSoonSubtext?: string;
  accent: string;
  heroStat?: { value: string; label: string };
}

// DRAFT — pending Content + QA sign-off
export const RAW_FOODS_COMING_SOON_SUBTEXT =
  "ירקות, פירות, דגנים וקטניות — לפני שמישהו אורז אותם.";

// DRAFT — pending Content + QA sign-off
export const PERSONAL_CARE_COMING_SOON_SUBTEXT =
  "קרמים, שמפו ומוצרי טיפוח — ניתוח מרכיבים ותוויות, כמו בכל קטגוריה אחרת.";

export const HASHVAOT_CATEGORIES: HashvaotCategory[] = [
  {
    id: "supermarket",
    title: "מוצרי סופרמרקט",
    status: "live",
    countLabel: "16 השוואות",
    href: "/hashvaot/supermarket",
    description: "חלב, לחם, דגני בוקר, גבינות, חטיפים ועוד — מהמדף הישראלי.",
    accent: "#BC6A33",
    heroStat: { value: "16", label: "השוואות פעילות" },
  },
  {
    id: "supplements",
    title: "תוספי תזונה",
    status: "live",
    countLabel: "1 השוואה",
    href: "/hashvaot/supplements",
    description: "תוספים מנותחים לפי ספיגה בפועל, לא לפי הכמות שעל הקופסה.",
    accent: "#4A7B8C",
    heroStat: { value: "18", label: "מוצרי מגנזיום נבדקו" },
  },
  {
    id: "raw-foods",
    title: "מזון גולמי",
    status: "building",
    href: "/hashvaot/raw-foods",
    comingSoonSubtext: RAW_FOODS_COMING_SOON_SUBTEXT,
    accent: "#7A8C5E",
  },
  {
    id: "personal-care",
    title: "טיפוח אישי",
    status: "building",
    href: "/hashvaot/personal-care",
    comingSoonSubtext: PERSONAL_CARE_COMING_SOON_SUBTEXT,
    accent: "#8B7BA8",
  },
];

export function getHashvaotCategory(id: string): HashvaotCategory | undefined {
  return HASHVAOT_CATEGORIES.find((c) => c.id === id);
}
