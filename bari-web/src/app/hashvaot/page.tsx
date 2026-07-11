import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";

import { HomeContainer } from "@/components/home/section-frame";
import { HashvaotCategoryBox } from "@/components/hashvaot/hashvaot-category-box";
import { HASHVAOT_CATEGORIES } from "@/lib/hashvaot/hashvaot-categories";
import { BlogEditorialBackdrop } from "@/components/blog/blog-editorial-backdrop";
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
        "relative overflow-hidden min-h-screen bg-[#F7F7F2] text-[#111318]",
        siteHeaderOffsetClass
      )}
    >
      <BlogEditorialBackdrop />

      <HomeContainer className="relative py-14 md:py-20">
        <div className="flex items-start justify-between gap-6">
          <div className="min-w-0">
            <p className="text-xs font-bold uppercase tracking-[0.24em] text-[#167A58]">
              Bari comparisons
            </p>
            <h1 className="mt-2 max-w-3xl text-balance text-4xl font-extrabold tracking-[-0.05em] md:text-5xl">
              השוואות מהמדף
            </h1>
            <p className="mt-4 max-w-2xl text-pretty text-lg leading-relaxed text-[#4E5663]">
              בארי בודקת מוצרים אמיתיים מהסופרמרקט ובתי המרקחת כדי לתת לכם חווית השוואה אינטראקטיבית בין מוצרים. כל דף השוואה בוחן מוצרים דומים לפי פרמטרים מוגדרים מראש על ידי אלגוריתם מכונה לומדת ומציג חסרונות ויתרונות בהקשר הנכון.
            </p>
          </div>

          {/* LUMO — the leaf, Bari's Investigator. Decorative. */}
          <Image
            src="/mascots/mascot-leaf.png"
            alt=""
            width={848}
            height={932}
            aria-hidden
            className="pointer-events-none -mt-2 hidden h-[9.375rem] w-auto shrink-0 select-none md:block"
            priority
          />
        </div>

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
