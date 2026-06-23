// Supplements comparison index.
// Kept separate from the food Hashvaot index so supplements never mix into the
// food grid (different scoring logic). Magnesium published 2026-06-23.

import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";

import { FeaturedMagnesiumIntelligenceCard } from "@/components/hashvaot/featured-magnesium-intelligence-card";
import { HomeContainer } from "@/components/home/section-frame";
import { cn } from "@/lib/utils";
import { siteHeaderOffsetClass } from "@/lib/site-layout";

export const metadata: Metadata = {
  title: "תוספי תזונה | Bari",
  description:
    "השוואות תוספי תזונה — ניתוח מינון, צורת ספיגה ועדות מדעית. מידע, לא המלצה.",
};

// TASK-384 v3 rebuild: updated description. [PLACEHOLDER] Content to finalize.
const MAGNESIUM_DESCRIPTION =
  "בדקנו 18 תוספי מגנזיום מהמדף הישראלי — 4 בציון B, 4 בציון C, 6 בציון D ו-1 בציון E. הצורה הכימית קובעת את הציון: ציטראט וביסגליצינט נספגים טוב יותר מאוקסיד. ארבעה מוצרים מכילים מגנזיום מעל הגבול המומלץ לתוספים — ומקבלים אזהרה ברורה.";

export default function SupplementsIndexPage() {
  return (
    <main
      className={cn(
        "relative min-h-screen bg-[#F7F7F2] text-[#111318]",
        siteHeaderOffsetClass
      )}
    >
      <HomeContainer className="py-14 md:py-20">
        <p className="text-xs font-bold uppercase tracking-[0.22em] text-[#1F8F6A]/80">
          Bari comparisons · תוספי תזונה
        </p>
        <h1 className="mt-3 max-w-3xl text-balance text-4xl font-extrabold tracking-[-0.05em] md:text-5xl">
          תוספי תזונה
        </h1>
        <p className="mt-5 max-w-2xl text-pretty text-lg leading-relaxed text-[#4E5663]">
          השוואות תוספי תזונה — ניתוח מינון, צורת ספיגה ועדות מדעית.
          לוגיקת הדירוג שונה ממזון: הציון מודד כמה מגנזיום הגוף סופג בפועל, לא הכמות על האריזה.
        </p>

        <div className="mt-12 space-y-6">
          <h2 className="text-sm font-bold uppercase tracking-[0.18em] text-[#7A817C]">
            זמין לצפייה
          </h2>
          <FeaturedMagnesiumIntelligenceCard
            href="/hashvaot/magnesium"
            description={MAGNESIUM_DESCRIPTION}
          />
        </div>

        <div className="mt-12 flex flex-col gap-3 sm:flex-row sm:items-center sm:gap-6">
          <Link
            href="/hashvaot"
            className="inline-flex items-center gap-2 text-sm font-semibold text-[#4E5663] transition-colors hover:text-[#111318]"
          >
            <ArrowLeft className="size-4" aria-hidden />
            חזרה להשוואות המזון
          </Link>
          <Link
            href="/"
            className="inline-flex items-center gap-2 text-sm font-semibold text-[#4E5663] transition-colors hover:text-[#111318]"
          >
            <ArrowLeft className="size-4" aria-hidden />
            חזרה לדף הבית
          </Link>
        </div>
      </HomeContainer>
    </main>
  );
}
