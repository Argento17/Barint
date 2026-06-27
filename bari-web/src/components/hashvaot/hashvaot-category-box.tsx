import Link from "next/link";
import { Clock } from "lucide-react";

import { cn } from "@/lib/utils";
import type { HashvaotCategory } from "@/lib/hashvaot/hashvaot-categories";

export function HashvaotCategoryBox({ category }: { category: HashvaotCategory }) {
  if (category.status === "building") {
    return (
      <div
        role="status"
        aria-label={`קטגוריית ${category.title} — בבנייה, עדיין לא זמינה`}
        className={cn(
          "flex min-h-[9rem] cursor-default flex-col gap-3 rounded-2xl border border-dashed",
          "border-[#7A817C]/30 bg-white/40 px-6 py-5 opacity-60"
        )}
      >
        <div className="flex items-center gap-3">
          <Clock className="size-5 shrink-0 text-[#7A817C]" aria-hidden />
          <h2 className="text-base font-semibold text-[#4E5663]">{category.title}</h2>
          <span className="rounded-full border border-[#7A817C]/30 px-3 py-0.5 text-[0.68rem] font-semibold text-[#7A817C]">
            בבנייה
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
        לצפייה ←
      </span>
    </Link>
  );
}
