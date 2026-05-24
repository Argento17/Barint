import Image from "next/image";
import Link from "next/link";
import { ChevronLeft } from "lucide-react";

import { HomeContainer } from "@/components/home/section-frame";
import { milkProducts } from "@/lib/comparisons/milk-page-data";
import { featuredArticle } from "@/lib/blog/blog-index-content";

const PREVIEW_PACKS = milkProducts.filter((p) => p.image_url).slice(0, 4);

export function HomeFlagshipAnalysis() {
  return (
    <section className="border-y border-black/[0.06] bg-[#FFFFFF] py-12 md:py-16">
      <HomeContainer>
        <div className="grid items-center gap-10 lg:grid-cols-[1.1fr_0.9fr] lg:gap-14">
          <div className="text-right">
            <p className="text-sm font-bold text-[#1F8F6A]">ניתוח מוביל · מדף ישראלי</p>
            <h2 className="mt-3 text-3xl font-extrabold leading-tight tracking-[-0.04em] text-[#111318] md:text-4xl">
              {featuredArticle.title}
            </h2>
            <p className="mt-4 max-w-xl text-base leading-relaxed text-[#4E5663] md:text-lg">
              {featuredArticle.description}
            </p>
            <p className="mt-2 text-sm text-[#7A817C]">{featuredArticle.metaLine}</p>

            <div className="mt-8 flex flex-wrap gap-3">
              <Link
                href="/blog/milk-analysis"
                className="inline-flex items-center justify-center gap-2 rounded-full bg-[#1F8F6A] px-6 py-3 text-sm font-bold text-[#F7F7F2] shadow-sm transition hover:-translate-y-0.5"
              >
                קריאת הניתוח
                <ChevronLeft className="size-4" aria-hidden />
              </Link>
              <Link
                href="/hashvaot/milk-comparison"
                className="inline-flex items-center justify-center gap-2 rounded-full border border-black/[0.08] bg-[#F7F7F2] px-6 py-3 text-sm font-bold text-[#111318] transition hover:border-[#1F8F6A]/25"
              >
                דוח ההשוואה
              </Link>
            </div>
          </div>

          <div className="relative overflow-hidden rounded-[1.35rem] border border-black/[0.06] bg-[#F7F7F2] p-6 md:p-8">
            <p className="mb-4 text-center text-xs font-bold text-[#4E5663]">
              18 מוצרים · מפת מדף · השוואות ממוקדות
            </p>
            <div className="flex items-end justify-center gap-3 md:gap-4">
              {PREVIEW_PACKS.map((p) => (
                <div key={p.barcode} className="relative h-20 w-12 md:h-24 md:w-14">
                  {p.image_url ? (
                    <Image
                      src={p.image_url}
                      alt=""
                      fill
                      className="object-contain drop-shadow-md"
                      sizes="56px"
                    />
                  ) : null}
                  {p.grade ? (
                    <span className="absolute bottom-0 left-1/2 -translate-x-1/2 rounded-full bg-[#111318] px-1.5 py-0.5 text-[0.55rem] font-extrabold leading-none text-[#F7F7F2]">
                      {p.grade}
                    </span>
                  ) : null}
                </div>
              ))}
            </div>
            <blockquote className="mt-5 border-r-2 border-[#1F8F6A] pr-4">
              <p className="text-base font-extrabold leading-snug tracking-[-0.02em] text-[#111318]">
                מוצרים שנראים דומים על המדף — מתפצלים ברכיבים, בעיבוד ובתזונה.
              </p>
              <p className="mt-1 text-xs text-[#7A817C]">
                מסקנה מניתוח 18 מוצרי חלב ושתייה צמחית
              </p>
            </blockquote>
          </div>
        </div>
      </HomeContainer>
    </section>
  );
}
