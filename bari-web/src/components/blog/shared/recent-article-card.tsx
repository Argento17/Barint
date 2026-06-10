"use client";

import Link from "next/link";
import { ChevronLeft } from "lucide-react";

/**
 * RecentArticleCard — linked or "coming soon" article teaser card.
 * Extracted from olive-oil-article.tsx to shared/ for TASK-200 (second article).
 */
export function RecentArticleCard({
  href,
  title,
  description,
  category,
  readTime,
  cta,
  comingSoon,
}: {
  href: string;
  title: string;
  description: string;
  category: string;
  readTime: string;
  cta: string;
  comingSoon?: boolean;
}) {
  return (
    <li className="rounded-[1.1rem] border border-black/[0.07] bg-[#FFFFFF] p-5">
      <p className="text-[0.65rem] font-bold uppercase tracking-[0.12em] text-[#7A817C]">
        {category} · {readTime}
      </p>
      <h3 className="mt-2 text-base font-extrabold leading-snug tracking-[-0.02em] text-[#111318]">
        {title}
      </h3>
      <p className="mt-2 text-sm leading-relaxed text-[#4E5663]">{description}</p>
      {comingSoon ? (
        <p className="mt-4 text-xs font-bold text-[#7A817C]">בקרוב</p>
      ) : (
        <Link
          href={href}
          className="mt-4 inline-flex items-center gap-1.5 text-xs font-bold text-[#1F8F6A] hover:underline"
        >
          {cta}
          <ChevronLeft className="size-3.5" aria-hidden />
        </Link>
      )}
    </li>
  );
}
