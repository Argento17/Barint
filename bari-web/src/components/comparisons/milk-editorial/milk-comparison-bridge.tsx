import Link from "next/link";
import { ChevronLeft } from "lucide-react";

import { HomeContainer } from "@/components/home/section-frame";

export function MilkComparisonBridge() {
  return (
    <section className="border-b border-black/[0.06] bg-[#F7F7F2] py-12 md:py-16">
      <HomeContainer>
        <div className="mx-auto max-w-2xl text-right">
          <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.28em] text-[#1F8F6A]/80">
            ניתוח
          </p>
          <p className="mt-4 text-lg leading-relaxed text-[#4E5663]">
            רוצים את הסיפור המלא מהמדף — מפת המוצרים, דפוסים וטריידאופים? הניתוח העיתונאי נמצא
            בבלוג. כאן למטה: השוואה אינטראקטיבית של כל 18 המוצרים.
          </p>
          <Link
            href="/blog/milk-analysis"
            className="mt-6 inline-flex items-center gap-2 text-sm font-bold text-[#1F8F6A] hover:underline"
          >
            לניתוח המדף בבלוג
            <ChevronLeft className="size-4" aria-hidden />
          </Link>
        </div>
      </HomeContainer>
    </section>
  );
}
