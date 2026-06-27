import type { Metadata } from "next";

import { HashvaotCategoryLanding } from "@/components/hashvaot/hashvaot-category-landing";
import { PERSONAL_CARE_COMING_SOON_SUBTEXT } from "@/lib/hashvaot/hashvaot-categories";

export const metadata: Metadata = {
  title: "טיפוח אישי | Bari",
  description: "טיפוח אישי — בבנייה.",
  robots: { index: false, follow: false },
};

export default function PersonalCareCategoryPage() {
  return (
    <HashvaotCategoryLanding
      eyebrow="Bari comparisons · טיפוח אישי"
      title="טיפוח אישי"
      buildingSubtext={PERSONAL_CARE_COMING_SOON_SUBTEXT}
    />
  );
}
