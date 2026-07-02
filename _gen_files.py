import os, pathlib

base = pathlib.Path("C:/Bari/bari-web/src")

# -- 1. hashvaot-categories.ts -----------------------------------------------
(base / "lib/hashvaot").mkdir(parents=True, exist_ok=True)
(base / "lib/hashvaot/hashvaot-categories.ts").write_text("""\
/**
 * Hashvaot category registry.
 * DRAFT subtext below is pending Content + QA sign-off.
 */

export type HashvaotCategoryStatus = "live" | "building";

export interface HashvaotCategory {
  id: string;
  title: string;
  status: HashvaotCategoryStatus;
  countLabel?: string;
  href?: string;
  description?: string;
  comingSoonSubtext?: string;
}

// DRAFT \u2014 pending Content + QA sign-off
export const RAW_FOODS_COMING_SOON_SUBTEXT =
  "\u05d9\u05e8\u05e7\u05d5\u05ea, \u05e4\u05d9\u05e8\u05d5\u05ea, \u05d3\u05d2\u05e0\u05d9\u05dd \u05d5\u05e7\u05d8\u05e0\u05d9\u05d5\u05ea \u2014 \u05dc\u05e4\u05e0\u05d9 \u05e9\u05de\u05d9\u05e9\u05d4\u05d5 \u05d0\u05d5\u05e8\u05d6 \u05d0\u05d5\u05ea\u05dd.";

// DRAFT \u2014 pending Content + QA sign-off
export const PERSONAL_CARE_COMING_SOON_SUBTEXT =
  "\u05e7\u05e8\u05de\u05d9\u05dd, \u05e9\u05de\u05e4\u05d5 \u05d5\u05de\u05d5\u05e6\u05e8\u05d9 \u05d8\u05d9\u05e4\u05d5\u05d7 \u2014 \u05e0\u05d9\u05ea\u05d5\u05d7 \u05de\u05e8\u05db\u05d9\u05d1\u05d9\u05dd \u05d5\u05ea\u05d5\u05d5\u05d9\u05d5\u05ea, \u05db\u05de\u05d5 \u05d1\u05db\u05dc \u05e7\u05d8\u05d2\u05d5\u05e8\u05d9\u05d4 \u05d0\u05d7\u05e8\u05ea.";

export const HASHVAOT_CATEGORIES: HashvaotCategory[] = [
  {
    id: "supermarket",
    title: "\u05de\u05d5\u05e6\u05e8\u05d9 \u05e1\u05d5\u05e4\u05e8\u05de\u05e8\u05e7\u05d8",
    status: "live",
    countLabel: "16 \u05d4\u05e9\u05d5\u05d5\u05d0\u05d5\u05ea",
    href: "/hashvaot/supermarket",
    description: "\u05d7\u05dc\u05d1, \u05dc\u05d7\u05dd, \u05d3\u05d2\u05e0\u05d9 \u05d1\u05d5\u05e7\u05e8, \u05d2\u05d1\u05d9\u05e0\u05d5\u05ea, \u05d7\u05d8\u05d9\u05e4\u05d9\u05dd \u05d5\u05e2\u05d5\u05d3 \u2014 \u05de\u05d4\u05de\u05d3\u05e3 \u05d4\u05d9\u05e9\u05e8\u05d0\u05dc\u05d9.",
  },
  {
    id: "supplements",
    title: "\u05ea\u05d5\u05e1\u05e4\u05d9 \u05ea\u05d6\u05d5\u05e0\u05d4",
    status: "live",
    countLabel: "1 \u05d4\u05e9\u05d5\u05d5\u05d0\u05d4",
    href: "/hashvaot/supplements",
    description: "\u05ea\u05d5\u05e1\u05e4\u05d9\u05dd \u05de\u05e0\u05d5\u05ea\u05d7\u05d9\u05dd \u05dc\u05e4\u05d9 \u05e1\u05e4\u05d9\u05d2\u05d4 \u05d1\u05e4\u05d5\u05e2\u05dc, \u05dc\u05d0 \u05dc\u05e4\u05d9 \u05d4\u05db\u05de\u05d5\u05ea \u05e9\u05e2\u05dc \u05d4\u05e7\u05d5\u05e4\u05e1\u05d4.",
  },
  {
    id: "raw-foods",
    title: "\u05de\u05d6\u05d5\u05df \u05d2\u05d5\u05dc\u05de\u05d9",
    status: "building",
    comingSoonSubtext: RAW_FOODS_COMING_SOON_SUBTEXT,
  },
  {
    id: "personal-care",
    title: "\u05d8\u05d9\u05e4\u05d5\u05d7 \u05d0\u05d9\u05e9\u05d9",
    status: "building",
    comingSoonSubtext: PERSONAL_CARE_COMING_SOON_SUBTEXT,
  },
];

export function getHashvaotCategory(id: string): HashvaotCategory | undefined {
  return HASHVAOT_CATEGORIES.find((c) => c.id === id);
}
""", encoding="utf-8")

print("hashvaot-categories.ts written")

# -- 2. hashvaot-category-box.tsx ---------------------------------------------
(base / "components/hashvaot").mkdir(parents=True, exist_ok=True)
(base / "components/hashvaot/hashvaot-category-box.tsx").write_text("""\
import Link from "next/link";
import { Clock } from "lucide-react";

import { cn } from "@/lib/utils";
import type { HashvaotCategory } from "@/lib/hashvaot/hashvaot-categories";

export function HashvaotCategoryBox({ category }: { category: HashvaotCategory }) {
  if (category.status === "building") {
    return (
      <div
        role="status"
        aria-label={`\u05e7\u05d8\u05d2\u05d5\u05e8\u05d9\u05d9\u05ea ${category.title} \u2014 \u05d1\u05d1\u05e0\u05d9\u05d9\u05d4, \u05e2\u05d3\u05d9\u05d9\u05df \u05dc\u05d0 \u05d6\u05de\u05d9\u05e0\u05d4`}
        className={cn(
          "flex min-h-[9rem] cursor-default flex-col gap-3 rounded-2xl border border-dashed",
          "border-[#7A817C]/30 bg-white/40 px-6 py-5 opacity-60"
        )}
      >
        <div className="flex items-center gap-3">
          <Clock className="size-5 shrink-0 text-[#7A817C]" aria-hidden />
          <h2 className="text-base font-semibold text-[#4E5663]">{category.title}</h2>
          <span className="rounded-full border border-[#7A817C]/30 px-3 py-0.5 text-[0.68rem] font-semibold text-[#7A817C]">
            \u05d1\u05d1\u05e0\u05d9\u05d9\u05d4
          </span>
        </div>
        {category.comingSoonSubtext ? (
          <p className="text-sm leading-relaxed text-[#7A817C]">{category.comingSoonSubtext}</p>
        ) : null}
      </div>
    );
  }

  return (
    <Link
      href={category.href!}
      className={cn(
        "group flex min-h-[9rem] flex-col gap-3 rounded-2xl border border-[#E8E6DF] bg-white px-6 py-5",
        "transition-all hover:border-[#1F8F6A]/40 hover:shadow-md hover:shadow-[#1F8F6A]/6"
      )}
    >
      <div className="flex items-center justify-between gap-2">
        <h2 className="text-base font-bold text-[#111318] group-hover:text-[#1F8F6A]">
          {category.title}
        </h2>
        {category.countLabel ? (
          <span className="shrink-0 rounded-full border border-[#1F8F6A]/25 bg-[#1F8F6A]/6 px-2.5 py-0.5 text-[0.65rem] font-semibold uppercase tracking-[0.1em] text-[#1F8F6A]">
            {category.countLabel}
          </span>
        ) : null}
      </div>
      {category.description ? (
        <p className="text-sm leading-relaxed text-[#4E5663]">{category.description}</p>
      ) : null}
      <span className="mt-auto text-xs font-semibold text-[#1F8F6A] opacity-0 transition-opacity group-hover:opacity-100">
        \u05dc\u05e6\u05e4\u05d9\u05d9\u05d4 \u2190
      </span>
    </Link>
  );
}
""", encoding="utf-8")

print("hashvaot-category-box.tsx written")

# -- 3. hashvaot-category-landing.tsx -----------------------------------------
(base / "components/hashvaot/hashvaot-category-landing.tsx").write_text("""\
import type { ReactNode } from "react";
import Link from "next/link";
import { ArrowLeft, Clock } from "lucide-react";

import { cn } from "@/lib/utils";
import { siteHeaderOffsetClass } from "@/lib/site-layout";
import { HomeContainer } from "@/components/home/section-frame";

interface HashvaotCategoryLandingProps {
  /** Eyebrow line, e.g. "Bari comparisons \xb7 \u05e1\u05d5\u05e4\u05e8\u05de\u05e8\u05e7\u05d8" */
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
        <p className="text-xs font-bold uppercase tracking-[0.22em] text-[#1F8F6A]/80">
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
            aria-label={`\u05e7\u05d8\u05d2\u05d5\u05e8\u05d9\u05d9\u05ea ${title} \u2014 \u05d1\u05d1\u05e0\u05d9\u05d9\u05d4`}
            className="mt-12 flex min-h-[5rem] cursor-default items-center gap-4 rounded-[1.35rem] border border-dashed border-[#7A817C]/30 bg-white/40 px-5 py-4 opacity-[0.62]"
          >
            <Clock className="size-5 shrink-0 text-[#7A817C]" aria-hidden />
            <div className="min-w-0">
              <div className="flex flex-wrap items-center gap-2">
                <p className="text-sm font-semibold text-[#4E5663]">{title}</p>
                <span className="rounded-full border border-[#7A817C]/30 px-3 py-1 text-[0.7rem] font-semibold text-[#7A817C]">
                  \u05d1\u05d1\u05e0\u05d9\u05d9\u05d4
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
          \u05d7\u05d6\u05e8\u05d4 \u05dc\u05db\u05dc \u05d4\u05e7\u05d8\u05d2\u05d5\u05e8\u05d9\u05d5\u05ea
        </Link>
      </HomeContainer>
    </main>
  );
}
""", encoding="utf-8")

print("hashvaot-category-landing.tsx written")
print("All files written OK")
