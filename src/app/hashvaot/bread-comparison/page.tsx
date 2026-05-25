import type { Metadata } from "next";

import { BreadComparisonPage } from "@/components/comparisons/bread-comparison-page";

export const metadata: Metadata = {
  title: "ניתוח מדף הלחמים | Bari",
  description:
    "32 מוצרי לחם, קרקר וקריספ — ניתוח קטגורי לפי מבנה הדגן, איכות התסיסה, מקור הסיבים ורמת עיבוד. Bari מראה מה מסתתר מאחורי הטענות.",
};

export default function BreadComparisonRoute() {
  return <BreadComparisonPage />;
}
