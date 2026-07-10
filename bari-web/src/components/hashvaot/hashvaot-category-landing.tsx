import type { ReactNode } from "react";
import Link from "next/link";
import { ArrowLeft, Clock } from "lucide-react";

import { cn } from "@/lib/utils";
import { siteHeaderOffsetClass } from "@/lib/site-layout";
import { HomeContainer } from "@/components/home/section-frame";

interface HashvaotCategoryLandingProps {
  /** Eyebrow line, e.g. "Bari comparisons · סופרמרקט" */
  eyebrow: string;
  title: string;
  intro?: ReactNode;
  /** Live category children (comparison cards, etc.) */
  children?: ReactNode;
  /** When status=building, shows coming-soon tray instead of children */
  buildingSubtext?: string;
}

export function HashvaotCategoryLanding({
  eyebrow,
  title,
  intro,
  children,
  buildingSubtext,
}: HashvaotCategoryLandingProps) {
  return (
    <main
      className={cn(
        "relative min-h-screen bg-[#F7F7F2] text-[#111318]",
        siteHeaderOffsetClass
      )}
    >
      <HomeContainer className="py-14 md:py-20">
        <p className="text-xs font-bold uppercase tracking-[0.22em] text-[#176F53]">
          {eyebrow}
        </p>
        <h1 className="mt-3 max-w-3xl text-balance text-4xl font-extrabold tracking-[-0.05em] md:text-5xl">
          {title}
        </h1>

        {intro ? (
          <div className="mt-5 max-w-2xl text-pretty text-lg leading-relaxed text-[#4E5663]">
            {intro}
          </div>
        ) : null}

        {buildingSubtext ? (
          <div
            role="status"
            aria-label={`קטגוריית ${title} — בבנייה`}
            className="mt-12 flex min-h-[5rem] cursor-default items-center gap-4 rounded-[1.35rem] border border-dashed border-[#7A817C]/30 bg-white/40 px-5 py-4 opacity-[0.62]"
          >
            <Clock className="size-5 shrink-0 text-[#7A817C]" aria-hidden />
            <div className="min-w-0">
              <div className="flex flex-wrap items-center gap-2">
                <p className="text-sm font-semibold text-[#4E5663]">{title}</p>
                <span className="rounded-full border border-[#7A817C]/30 px-3 py-1 text-[0.7rem] font-semibold text-[#7A817C]">
                  בבנייה
                </span>
              </div>
              <p className="mt-1 text-pretty text-sm leading-relaxed text-[#7A817C]">{buildingSubtext}</p>
            </div>
          </div>
        ) : (
          <div className="mt-12">{children}</div>
        )}

        <Link
          href="/hashvaot"
          className="mt-10 inline-flex items-center gap-2 text-sm font-semibold text-[#4E5663] transition-colors hover:text-[#111318]"
        >
          <ArrowLeft className="size-4" aria-hidden />
          חזרה לכל הקטגוריות
        </Link>
      </HomeContainer>
    </main>
  );
}
