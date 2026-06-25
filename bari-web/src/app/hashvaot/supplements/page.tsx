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

// TASK-384 / TASK-374: card description — Content Agent authored, Naturalness gate
// (Layer 1 + independent Track-C judge, F1=4/F2=4) PASS 2026-06-24. Numbers carried
// from current committed magnesium-page-data.ts; re-author if TASK-384 model moves them.
const MAGNESIUM_DESCRIPTION =
  "בדקנו 18 תוספי מגנזיום מהמדף הישראלי, והצורה הכימית היא שמכריעה: ציטראט וביסגליצינט נספגים טוב יותר, ולכן הם שמובילים את הדירוג, בעוד שהאוקסיד הזול והנפוץ יושב בתחתית — הגוף פשוט קולט ממנו פחות. ארבעה מוצרי אוקסיד אף חורגים מהגבול העליון לתוספים ומקבלים אזהרת מינון ברורה. מה שהציון מודד הוא כמה מגנזיום הגוף סופג בפועל, וזה תלוי בצורה הרבה יותר מאשר בספרה שעל הקופסה.";

export default function SupplementsIndexPage() {
  return (
    <div
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
          הגוף לא סופג את כל המינרל שעל הקופסה. כמה באמת מגיע פנימה תלוי במינון היסודי, בצורה הכימית שנספגת, ובחוזק העדויות לייעוד. המספר הגדול על הקופסה הוא נקודת הפתיחה בלבד, ומשם ברי בודקת את מה שבאמת קובע. לכן ברי מודדת כל תוסף לפי מה שמגיע באמת לגוף — שם נקבע אם הוא שווה את מה שהובטח על הקופסה.
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
    </div>
  );
}
