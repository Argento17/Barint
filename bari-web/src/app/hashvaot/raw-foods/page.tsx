import type { Metadata } from "next";

import { HashvaotCategoryLanding } from "@/components/hashvaot/hashvaot-category-landing";
import { RAW_FOODS_COMING_SOON_SUBTEXT } from "@/lib/hashvaot/hashvaot-categories";

export const metadata: Metadata = {
  title: "מזון גולמי | Bari",
  description: "מזון גולמי — בבנייה.",
  robots: { index: false, follow: false },
};

export default function RawFoodsCategoryPage() {
  return (
    <HashvaotCategoryLanding
      eyebrow="Bari comparisons · מזון גולמי"
      title="מזון גולמי"
      buildingSubtext={RAW_FOODS_COMING_SOON_SUBTEXT}
    />
  );
}
