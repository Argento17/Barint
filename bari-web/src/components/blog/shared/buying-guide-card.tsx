"use client";

/**
 * BuyingGuideCard — 2-col signal card for shelf-reading guidance.
 * Extracted from olive-oil-article.tsx to shared/ for TASK-200 (second article).
 */
export function BuyingGuideCard({
  signal,
  what,
  availability,
}: {
  signal: string;
  what: string;
  availability: string;
}) {
  return (
    <li className="rounded-[1rem] border border-black/[0.07] bg-[#FFFFFF] px-5 py-5">
      <p className="text-xs font-bold uppercase tracking-[0.12em] text-[#7A9450]">{signal}</p>
      <p className="mt-2 text-sm font-semibold leading-snug text-[#111318]">{what}</p>
      <p className="mt-2 text-xs leading-relaxed text-[#7A817C]">
        <span className="font-bold">זמינות: </span>
        {availability}
      </p>
    </li>
  );
}
