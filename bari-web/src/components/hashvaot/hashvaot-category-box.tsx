import Link from "next/link";
import { ChevronLeft, Clock } from "lucide-react";

import { cn } from "@/lib/utils";
import type { HashvaotCategory } from "@/lib/hashvaot/hashvaot-categories";

const INACTIVE_SURFACE = "#EDEAE3";

function BuildingCard({ category }: { category: HashvaotCategory }) {
  const inner = (
    <div
      role="status"
      aria-label={`קטגוריית ${category.title} — בבנייה, עדיין לא זמינה`}
      className="relative flex min-h-[10rem] flex-col gap-3 rounded-2xl px-6 py-5"
      style={{ backgroundColor: INACTIVE_SURFACE }}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex min-w-0 items-center gap-2.5">
          <Clock className="size-4 shrink-0 text-[#7A817C]" aria-hidden />
          <h2 className="text-lg font-bold text-[#4E5663]">{category.title}</h2>
        </div>
        <span className="shrink-0 rounded-full bg-[#D8D5CD] px-2.5 py-0.5 text-[0.65rem] font-bold text-[#5E6560]">
          בקרוב
        </span>
      </div>

      {category.comingSoonSubtext ? (
        <p className="text-sm leading-relaxed text-[#7A817C]">{category.comingSoonSubtext}</p>
      ) : null}
    </div>
  );

  if (category.href) {
    return (
      <Link
        href={category.href}
        className="block rounded-2xl transition-opacity hover:opacity-90 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#1F8F6A]"
        aria-label={`קטגוריית ${category.title} — בבנייה`}
      >
        {inner}
      </Link>
    );
  }
  return inner;
}

function LiveCard({ category }: { category: HashvaotCategory }) {
  return (
    <Link
      href={category.href!}
      className={cn(
        "group flex min-h-[10rem] flex-col gap-4 rounded-2xl bg-white px-6 py-5",
        "shadow-[0_10px_40px_-16px_rgba(17,19,24,0.14)]",
        "transition-[transform,box-shadow] duration-200",
        "hover:-translate-y-0.5 hover:shadow-[0_16px_48px_-14px_rgba(17,19,24,0.18)]",
        "focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#1F8F6A]"
      )}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0 space-y-1">
          <h2 className="text-lg font-extrabold tracking-[-0.02em] text-[#111318]">
            {category.title}
          </h2>
          {category.heroStat ? (
            <p className="flex flex-wrap items-baseline gap-x-1.5 gap-y-0 leading-tight">
              <span
                className="text-2xl font-black tabular-nums tracking-[-0.04em]"
                style={{ color: category.accent }}
              >
                {category.heroStat.value}
              </span>
              <span className="text-sm font-medium text-[#5E6560]">
                {category.heroStat.label}
              </span>
            </p>
          ) : null}
        </div>
        <span
          className="shrink-0 rounded-full px-2.5 py-0.5 text-[0.65rem] font-bold text-white"
          style={{ backgroundColor: category.accent }}
        >
          זמין
        </span>
      </div>

      {category.description ? (
        <p className="flex-1 text-sm leading-relaxed text-[#4E5663]">{category.description}</p>
      ) : null}

      <span
        className={cn(
          "mt-auto inline-flex w-fit items-center gap-2 rounded-xl px-4 py-2.5",
          "text-sm font-bold text-white",
          "transition-[filter] duration-200 group-hover:brightness-105"
        )}
        style={{ backgroundColor: category.accent }}
      >
        לכל ההשוואות
        <ChevronLeft className="size-4 stroke-[2.5]" aria-hidden />
      </span>
    </Link>
  );
}

export function HashvaotCategoryBox({ category }: { category: HashvaotCategory }) {
  if (category.status === "building") {
    return <BuildingCard category={category} />;
  }
  return <LiveCard category={category} />;
}
