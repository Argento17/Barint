import Link from "next/link";
import { ChevronLeft, Clock } from "lucide-react";

import { cn } from "@/lib/utils";
import type { HashvaotCategory } from "@/lib/hashvaot/hashvaot-categories";

export function HashvaotCategoryBox({ category }: { category: HashvaotCategory }) {
  const isLive = category.status === "live";

  const inner = (
    <>
      <div className="flex items-start justify-between gap-3">
        <h2 className="text-xl font-extrabold tracking-[-0.03em] text-[#111318] md:text-2xl">
          {category.title}
        </h2>
        <span
          className={cn(
            "shrink-0 rounded-full px-2.5 py-0.5 text-[0.65rem] font-bold",
            isLive
              ? "bg-[#1F8F6A] text-[#F7F7F2]"
              : "border border-[#7A817C]/30 bg-white/70 text-[#7A817C]"
          )}
        >
          {isLive ? "זמין" : "בבנייה"}
        </span>
      </div>

      {category.countLabel ? (
        <p className="mt-2 text-xs font-semibold uppercase tracking-[0.14em] text-[#7A817C]">
          {category.countLabel}
        </p>
      ) : null}

      <p className="mt-3 flex-1 text-pretty text-sm leading-relaxed text-[#4E5663] md:text-base">
        {category.description ?? category.comingSoonSubtext}
      </p>

      <p
        className={cn(
          "mt-5 flex items-center gap-1 text-sm font-bold",
          isLive ? "text-[#1F8F6A]" : "text-[#7A817C]"
        )}
      >
        {isLive ? (
          <>
            לכל ההשוואות
            <ChevronLeft className="size-4" aria-hidden />
          </>
        ) : (
          <>
            <Clock className="size-4" aria-hidden />
            בקרוב
          </>
        )}
      </p>
    </>
  );

  const shellClass = cn(
    "flex h-full min-h-[11rem] flex-col rounded-[1.35rem] border p-6 transition md:min-h-[12.5rem] md:p-7",
    isLive
      ? "border-black/[0.08] bg-white/80 hover:-translate-y-0.5 hover:border-[#1F8F6A]/25 hover:bg-white hover:shadow-[0_24px_60px_-40px_rgba(31,143,106,0.28)]"
      : "border-dashed border-[#7A817C]/30 bg-white/40 opacity-[0.78] hover:border-[#7A817C]/45 hover:bg-white/55"
  );

  if (!category.href) {
    return <div className={shellClass}>{inner}</div>;
  }

  return (
    <Link
      href={category.href}
      className={cn(
        shellClass,
        "group focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#1F8F6A]"
      )}
    >
      {inner}
    </Link>
  );
}
