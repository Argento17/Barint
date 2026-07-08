"use client";

import { ExternalLink } from "lucide-react";
import { motion, useReducedMotion } from "framer-motion";

import type { ClaimAuditItem, ClaimStatus } from "@/lib/news/of-poultry-report-content";
import { cn } from "@/lib/utils";

/**
 * ClaimStatusCard — the spine of an honest-broker news piece: one claim, one
 * verification-status chip, one inline source.
 *
 * Visually mirrors the blog shared FindingCard (src/components/blog/shared/finding-card.tsx —
 * same rounded card, same padding, same title/body/sub-label rhythm) with one
 * addition: a status chip reusing the amber "unverified/caution" pill already
 * established in the blog design language (src/components/blog/food-dyes-reference-table.tsx)
 * plus its existing green (verified) and red (#C0392B, already used in
 * food-dyes-article-hero.tsx for an unverified stat) counterparts. No new
 * colors invented — all three come from hex/classes already in the codebase.
 */
const STATUS_STYLE: Record<ClaimStatus, { chip: string; dot: string }> = {
  "מאומת": {
    chip: "border-[#1F8F6A]/30 bg-[#167A58]/10 text-[#167A58]",
    dot: "bg-[#167A58]",
  },
  "שנוי במחלוקת": {
    chip: "border-amber-200/60 bg-amber-50 text-[#9A6A00]",
    dot: "bg-amber-500",
  },
  "לא אומת": {
    chip: "border-red-200/60 bg-red-50 text-[#C0392B]",
    dot: "bg-[#C0392B]",
  },
};

function ClaimStatusChip({ status }: { status: ClaimStatus }) {
  const style = STATUS_STYLE[status] ?? STATUS_STYLE["לא אומת"];
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-[0.68rem] font-bold",
        style.chip
      )}
    >
      <span className={cn("size-1.5 rounded-full", style.dot)} aria-hidden />
      {status}
    </span>
  );
}

export function ClaimStatusCard({ item, index }: { item: ClaimAuditItem; index: number }) {
  const reduceMotion = useReducedMotion();
  return (
    <motion.li
      initial={reduceMotion ? false : { opacity: 0, y: 12 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ delay: index * 0.05 }}
      className="rounded-[1.2rem] border border-black/[0.07] bg-[#FFFFFF] px-6 py-6 md:px-8 md:py-7"
    >
      <div className="flex items-start justify-between gap-4">
        <p className="text-base font-semibold leading-relaxed text-[#111318] md:text-lg">
          {item.claim}
        </p>
        <span className="shrink-0">
          <ClaimStatusChip status={item.status} />
        </span>
      </div>

      {item.note && (
        <p className="mt-3 text-sm leading-relaxed text-[#4E5663]">{item.note}</p>
      )}

      <div className="mt-4 flex flex-wrap items-center gap-1.5 border-t border-black/[0.05] pt-3 text-xs text-[#7A817C]">
        <span className="font-bold text-[#7A9450]">מקור · </span>
        <span>{item.sourceLabel}</span>
        {item.sourceUrl && item.sourceUrl !== "#" && (
          <a
            href={item.sourceUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1 font-semibold text-[#167A58] hover:underline"
          >
            קישור למקור
            <ExternalLink className="size-3" aria-hidden />
          </a>
        )}
      </div>
    </motion.li>
  );
}
