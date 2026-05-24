import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft, Layers3 } from "lucide-react";

import { FeaturedMilkIntelligenceCard } from "@/components/hashvaot/featured-milk-intelligence-card";
import { HomeContainer } from "@/components/home/section-frame";
import { milkProducts } from "@/lib/comparisons/milk-page-data";
import { cn } from "@/lib/utils";
import { siteHeaderOffsetClass } from "@/lib/site-layout";

export const metadata: Metadata = {
  title: "השוואות | Bari",
  description:
    "השוואות אינטליגנציית מזון אינטראקטיביות — ניתוח רב-פרמטרי של מוצרים דומים.",
};

const MILK_COMPARISON_HREF = "/hashvaot/milk-comparison";

const upcomingComparisons = [
  {
    title: "יוגורטים ומוצרי חלבון",
    description: "בקרוב — השוואה קטגורית עם פרמטרים מותאמים.",
  },
  {
    title: "חטיפי אנרגיה וחטיפי חלבון",
    description: "בקרוב — ניתוח שובע, עיבוד ופשטות רכיבים.",
  },
] as const;

export default function HashvaotIndexPage() {
  const productCount = milkProducts.length;
  const milkDescription = `השוואה בין ${productCount} מוצרי חלב ומשקאות חלב פופולריים בישראל — כולל חלב פרה, סויה, שיבולת שועל, שקדים ומוצרים עתירי חלבון. Bari מנתחת רכיבים, ערכים תזונתיים, רמת עיבוד ותוספים כדי להציג את הטריידאופים בין המוצרים.`;

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

        <div className="mt-16">
          <h2 className="text-sm font-bold uppercase tracking-[0.18em] text-[#7A817C]">בקרוב</h2>
          <div className="mt-6 grid gap-4 md:grid-cols-2">
            {upcomingComparisons.map((item) => (
              <div
                key={item.title}
                className="rounded-[1.35rem] border border-black/[0.08] bg-[#FFFFFF]/60 p-5 opacity-80"
              >
                <Layers3 className="mb-3 size-5 text-[#7A817C]" aria-hidden />
                <h3 className="font-extrabold text-[#111318]">{item.title}</h3>
                <p className="mt-2 text-sm text-[#4E5663]">{item.description}</p>
              </div>
            ))}
          </div>
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
