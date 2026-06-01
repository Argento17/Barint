import Link from "next/link";

import { Button } from "@/components/ui/button";

import { HomeContainer } from "./section-frame";

export function HomeFinalCta() {
  return (
    <section className="relative overflow-hidden bg-[#F7F7F2] py-20 md:py-24">
      <HomeContainer className="relative text-center">
        <p className="mb-4 text-sm font-bold text-[#1F8F6A]">הצעד הבא</p>
        <h2 className="text-balance text-3xl font-extrabold leading-tight tracking-[-0.045em] text-[#111318] md:text-5xl">
          התחילו מחקירה אחת —
          <br />
          או ממפת הקטגוריות
        </h2>
        <p className="mx-auto mt-6 max-w-2xl text-pretty text-base leading-relaxed text-[#4E5663] md:text-lg">
          הבלוג מסביר דפוסים; מנוע ההשוואה מציג מוצרים בפירוט. מידע בלבד — לא המלצה.
        </p>
        <div className="mt-10 flex flex-col items-stretch justify-center gap-4 sm:flex-row sm:items-center sm:justify-center sm:gap-5">
          <Button
            size="lg"
            className="h-12 rounded-2xl border border-[#1F8F6A]/10 bg-[#1F8F6A] px-10 text-base font-bold text-[#F7F7F2] shadow-xl shadow-slate-900/10 hover:bg-[#1F8F6A] sm:min-w-44"
            asChild
          >
            <Link href="/blog" className="inline-flex items-center justify-center">
              כל הניתוחים
            </Link>
          </Button>
          <Button
            size="lg"
            variant="outline"
            className="h-12 rounded-2xl border border-black/[0.08] bg-[#FFFFFF]/68 px-10 text-base font-semibold text-[#111318] backdrop-blur-sm hover:bg-[#FFFFFF]/82 sm:min-w-44"
            asChild
          >
            <Link href="/hashvaot" className="inline-flex items-center justify-center">
              מנוע ההשוואות
            </Link>
          </Button>
        </div>
      </HomeContainer>
    </section>
  );
}
