import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";

import { HomeContainer } from "@/components/home/section-frame";
import { HashvaotCategoryBox } from "@/components/hashvaot/hashvaot-category-box";
import { HASHVAOT_CATEGORIES } from "@/lib/hashvaot/hashvaot-categories";
import { cn } from "@/lib/utils";
import { siteHeaderOffsetClass } from "@/lib/site-layout";

export const metadata: Metadata = {
  title: "השוואות | Bari",
  description:
    "השוואות אינטראקטיביות מהמדף — מזון, תוספים ועוד. ניתוח רב-פרמטרי של מוצרים דומים.",
};

export default function HashvaotIndexPage() {
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
          השוואות מהמדף
        </h1>
        <p className="mt-5 max-w-2xl text-pretty text-lg leading-relaxed text-[#4E5663]">
          חוויות השוואה אינטראקטיביות — לא מאמרים סטטיקיים. כל דף בוחן מוצרים דומים לפי פרמטרים ומציג טריידאופים בהקשר הנכון.
        </p>

        <div className="mt-12 grid gap-5 sm:grid-cols-2">
          {HASHVAOT_CATEGORIES.map((cat) => (
            <HashvaotCategoryBox key={cat.id} category={cat} />
          ))}
        </div>

        <Link
          href="/"
          className="mt-10 inline-flex items-center gap-2 text-sm font-semibold text-[#4E5663] transition-colors hover:text-[#111318]"
        >
          <ArrowLeft className="size-4" aria-hidden />
          חזרה לדף הבית
        </Link>
      </HomeContainer>
    </main>
  );
}
