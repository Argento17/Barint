import type { Metadata } from "next";

import { MilkComparisonPage } from "@/components/comparisons/milk-comparison-page";

export const metadata: Metadata = {
  title: "השוואת חלב ואלטרנטיבות | Bari",
  description:
    "השוואת מוצרים אמיתיים ממדפי סופרים — ציון Bari, חלבון, סוכר, תוספים ופרשנות מוצר. מידע, לא המלצה.",
};

export default function MilkComparisonRoute() {
  return <MilkComparisonPage />;
}
