import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";

import { FeaturedBreadIntelligenceCardLite } from "@/components/hashvaot/featured-bread-intelligence-card-lite";
import { FeaturedHummusIntelligenceCard } from "@/components/hashvaot/featured-hummus-intelligence-card";
import { FeaturedMilkIntelligenceCard } from "@/components/hashvaot/featured-milk-intelligence-card";
import { FeaturedSnacksIntelligenceCard } from "@/components/hashvaot/featured-snacks-intelligence-card";
import { FeaturedYogurtsIntelligenceCard } from "@/components/hashvaot/featured-yogurts-intelligence-card";
import { HomeContainer } from "@/components/home/section-frame";
import { BREAD_COMPARISON_HREF } from "@/lib/blog/bread-analysis-content";
import { SNACK_COMPARISON_HREF } from "@/lib/blog/snack-analysis-content";
import { breadProducts } from "@/lib/comparisons/bread-page-data";
import { SNACK_REPORT_STATS } from "@/lib/comparisons/snack-page-data";
import { snacksProducts } from "@/lib/comparisons/snacks-comparison-page-data";
import { hummusProducts, hummusPrologueSentences } from "@/lib/comparisons/hummus-comparison-page-data";
import { yogurtsPrologueSentences } from "@/lib/comparisons/yogurts-comparison-page-data";
import { milkProducts } from "@/lib/comparisons/milk-page-data";
import { cn } from "@/lib/utils";
import { siteHeaderOffsetClass } from "@/lib/site-layout";

export const metadata: Metadata = {
  title: "השוואות | Bari",
  description:
    "השוואות אינטליגנציית מזון אינטראקטיביות — ניתוח רב-פרמטרי של מוצרים דומים.",
};

const HUMMUS_COMPARISON_HREF = "/hashvaot/hummus";
const MILK_COMPARISON_HREF = "/hashvaot/milk-comparison";
const YOGURTS_COMPARISON_HREF = "/hashvaot/yogurts";

export default function HashvaotIndexPage() {
  const productCount = milkProducts.length;
  const milkDescription = `השוואה בין ${productCount} מוצרי חלב ומשקאות חלב פופולריים בישראל — כולל חלב פרה, סויה, שיבולת שועל, שקדים ומוצרים עתירי חלבון. Bari מנתחת רכיבים, ערכים תזונתיים, רמת עיבוד ותוספים כדי להציג את הטריידאופים בין המוצרים.`;
  const breadDescription = `דוח השוואה מאוחד ללחם, פיתות וקרקרים: 256 מוצרים נסרקו, 81 קיבלו מספיק נתונים לניתוח מהימן, ו-${breadProducts.length} נבחרו להצגה העריכתית בדף.`;
  const snacksDescription = `דוח השוואה לחטיפי המדף: ${SNACK_REPORT_STATS.scraped} נסרקו ב${SNACK_REPORT_STATS.retailer}, ${snacksProducts.length} מוצרים בדף ההשוואה.`;
  const hummusDescription = `${hummusPrologueSentences[0]} ${hummusProducts.length} מוצרים בדף ההשוואה.`;
  const yogurtsDescription = yogurtsPrologueSentences.join(" ");

  return (
    <main
      className={cn(
        "relative min-h-screen bg-[#F7F7F2] text-[#111318]",
        siteHeaderOffsetClass
      )}
    >
      <HomeContainer className="py-14 md:py-20">
        <p className="text-xs font-bold uppercase tracking-[0.22em] text-[#1F8F6A]/80">
          Bari comparisons
        </p>
        <h1 className="mt-3 max-w-3xl text-balance text-4xl font-extrabold tracking-[-0.05em] md:text-5xl">
          השוואות אינטליגנציית מזון
        </h1>
        <p className="mt-5 max-w-2xl text-pretty text-lg leading-relaxed text-[#4E5663]">
          חוויות השוואה אינטראקטיביות — לא מאמרים סטטיים. כל דף בוחן מוצרים דומים לפי פרמטרים
          ומציג טריידאופים בהקשר הנכון.
        </p>

        <div className="mt-12 space-y-6">
          <h2 className="text-sm font-bold uppercase tracking-[0.18em] text-[#7A817C]">
            השוואה מומלצת
          </h2>

          <FeaturedMilkIntelligenceCard href={MILK_COMPARISON_HREF} description={milkDescription} />

          <p className="text-sm text-[#4E5663]">
            רוצים את הסיפור מאחורי הממצאים?{" "}
            <Link
              href="/blog/milk-analysis"
              className="font-semibold text-[#1F8F6A] underline-offset-2 hover:underline"
            >
              קראו את הניתוח בבלוג
            </Link>
            — המאמר משלים את מנוע ההשוואה, לא מחליף אותו.
          </p>
        </div>

        <div className="mt-12 space-y-6">
          <h2 className="text-sm font-bold uppercase tracking-[0.18em] text-[#7A817C]">
            ניתוח עדכני
          </h2>
          <FeaturedBreadIntelligenceCardLite href={BREAD_COMPARISON_HREF} description={breadDescription} />
          <FeaturedSnacksIntelligenceCard href={SNACK_COMPARISON_HREF} description={snacksDescription} />
          <FeaturedYogurtsIntelligenceCard
            href={YOGURTS_COMPARISON_HREF}
            description={yogurtsDescription}
          />
          <FeaturedHummusIntelligenceCard
            href={HUMMUS_COMPARISON_HREF}
            description={hummusDescription}
          />
        </div>

        <Link
          href="/"
          className="mt-12 inline-flex items-center gap-2 text-sm font-semibold text-[#4E5663] transition-colors hover:text-[#111318]"
        >
          <ArrowLeft className="size-4" aria-hidden />
          חזרה לדף הבית
        </Link>
      </HomeContainer>
    </main>
  );
}
