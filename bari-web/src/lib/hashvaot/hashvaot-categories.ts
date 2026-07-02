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
    id: "supplements",
    title: "תוספי תזונה — ספיגה ואפקטיביות, לא רק מה שעל הקפסולה",
    status: "live",
    countLabel: "1 השוואה",
    href: "/hashvaot/supplements",
    description: "תוספי תזונה מנותחים באופן שונה ממוצרי מזון — ספיגה, אפקטיביות ועוד",
    accent: "#1F8F6A",
    heroStat: { value: "השוואות פעילות", label: "תוספי תזונה" },
  },
  {
    id: "supermarket",
    title: "מה שכתוב על האריזה — ומה שכתוב ברכיבים",
    status: "live",
    countLabel: "16 השוואות",
    href: "/hashvaot/supermarket",
    description: "חלב, לחם, חטיפים, עוגות, גבינות ועוד",
    accent: "#A63F2A",
    heroStat: { value: "השוואות פעילות", label: "מוצרי סופרמרקט" },
  },
  {
    id: "personal-care",
    title: "טיפוח אישי",
    status: "building",
    href: "/hashvaot/personal-care",
    comingSoonSubtext: PERSONAL_CARE_COMING_SOON_SUBTEXT,
    accent: "#8B7BA8",
  },
  {
    id: "raw-foods",
    title: "מזון גולמי",
    status: "building",
    href: "/hashvaot/raw-foods",
    comingSoonSubtext: RAW_FOODS_COMING_SOON_SUBTEXT,
    accent: "#7A8C5E",
  },
];

export function getHashvaotCategory(id: string): HashvaotCategory | undefined {
  return HASHVAOT_CATEGORIES.find((c) => c.id === id);
}
