"use client";

import { useState } from "react";
import { motion, useReducedMotion } from "framer-motion";
import { ChevronDown } from "lucide-react";

import { BariGradeBadge } from "@/components/comparisons/bari-grade-badge";
import { BariProductThumbnail } from "@/components/comparisons/bari-product-thumbnail";
import { BARI_COMPARISON_TOKENS } from "@/lib/design/bari-comparison-tokens";
import type { BariGrade, BariProductVM } from "@/lib/view-models";
import { cn } from "@/lib/utils";

const GRADE_LABELS: Record<BariGrade, string> = {
  A: "מצוין",
  B: "טוב",
  C: "בינוני",
  D: "חלש",
  E: "נמוך",
};

const LABEL_POSITIVE = "מה עובד לטובת המוצר?";
const LABEL_LIMITING = "מה מגביל את הציון?";
const LABEL_UNKNOWNS = "מה שלא ניתן לאמת";
const LABEL_CAVEATS = "הערות";
const LABEL_BOTTOM = "בשורה התחתונה";
const LABEL_COMPARISON = "הקשר במדף";

export function BariProductShelfRow({
  product,
  rank,
}: {
  product: BariProductVM;
  rank: number;
}) {
  const [expanded, setExpanded] = useState(false);
  const [advanced, setAdvanced] = useState(false);
  const reduceMotion = useReducedMotion();
  const { expansion } = product;
  const hasPositive = (expansion.positiveSignals?.length ?? 0) > 0;
  const hasLimiting = (expansion.limitingFactors?.length ?? 0) > 0;
  const hasUnknowns = (expansion.unknowns?.length ?? 0) > 0;
  const hasCaveats = (expansion.caveats?.length ?? 0) > 0;
  const hasTechnical =
    Boolean(expansion.ingredients?.trim()) ||
    (expansion.nutrition != null &&
      Object.values(expansion.nutrition).some((value) => value != null));

  return (
    <motion.article
      layout={!reduceMotion}
      className={BARI_COMPARISON_TOKENS.rows.zebraRowClass}
    >
      <div className="flex flex-col gap-4 p-4 sm:flex-row sm:items-start sm:gap-5">
        <div className="flex min-w-0 flex-1 items-start gap-4">
          <span className="hidden w-6 shrink-0 pt-2 text-center text-xs font-bold tabular-nums text-[#7A817C] sm:block">
            {rank}
          </span>
          <BariProductThumbnail product={product} size="lg" />
          <div className="min-w-0 flex-1 pt-0.5">
            <p className="text-base font-extrabold leading-snug text-[#111318] sm:text-lg">
              {product.name}
            </p>
          </div>
        </div>

        <div className="flex shrink-0 items-center gap-3 sm:flex-col sm:items-end sm:pt-1">
          {product.score != null && product.grade != null ? (
            <BariGradeBadge
              score={product.score}
              grade={product.grade}
              gradeLabel={GRADE_LABELS[product.grade]}
              size="md"
              context="row"
            />
          ) : null}
        </div>
      </div>

      {product.insightLine ? (
        <p className="px-4 pb-3 text-sm leading-relaxed text-[#4E5663] sm:pl-14">
          <span className="font-bold text-[#111318]">בקצרה: </span>
          {product.insightLine}
        </p>
      ) : null}

      <div className="space-y-2 px-4 pb-4 sm:pl-14">
        <button
          type="button"
          onClick={() => setExpanded((value) => !value)}
          className="flex w-full items-center justify-between rounded-lg border border-black/[0.08] bg-[#FFFFFF] px-3 py-2.5 text-sm font-semibold text-[#111318] hover:border-[#1F8F6A]/25"
          aria-expanded={expanded}
        >
          למה קיבל את הציון?
          <ChevronDown
            className={cn("size-4 text-[#7A817C] transition-transform", expanded && "rotate-180")}
          />
        </button>

        <motion.div
          initial={false}
          animate={{ height: expanded ? "auto" : 0, opacity: expanded ? 1 : 0 }}
          transition={{ duration: reduceMotion ? 0 : 0.28 }}
          className="overflow-hidden"
        >
          <div className="space-y-4 rounded-xl border border-black/[0.08] bg-[#FFFFFF]/90 p-4">
            {hasPositive ? (
              <div>
                <h4 className="text-xs font-bold text-[#1F8F6A]">{LABEL_POSITIVE}</h4>
                <ul className="mt-1.5 list-inside list-disc space-y-1 text-sm text-[#4E5663]">
                  {expansion.positiveSignals!.map((line) => (
                    <li key={line}>{line}</li>
                  ))}
                </ul>
              </div>
            ) : null}

            {hasLimiting ? (
              <div>
                <h4 className="text-xs font-bold text-[#111318]">{LABEL_LIMITING}</h4>
                <ul className="mt-1.5 list-inside list-disc space-y-1.5 text-sm leading-relaxed text-[#4E5663]">
                  {expansion.limitingFactors!.map((line) => (
                    <li key={line}>{line}</li>
                  ))}
                </ul>
              </div>
            ) : null}

            {hasUnknowns ? (
              <div>
                <h4 className="text-xs font-bold text-[#111318]">{LABEL_UNKNOWNS}</h4>
                <ul className="mt-1.5 list-inside list-disc space-y-1.5 text-sm leading-relaxed text-[#7A817C]">
                  {expansion.unknowns!.map((line) => (
                    <li key={line}>{line}</li>
                  ))}
                </ul>
              </div>
            ) : null}

            {hasCaveats ? (
              <div>
                <h4 className="text-xs font-bold text-[#111318]">{LABEL_CAVEATS}</h4>
                <ul className="mt-1.5 list-inside list-disc space-y-1.5 text-sm leading-relaxed text-[#7A817C]">
                  {expansion.caveats!.map((line) => (
                    <li key={line}>{line}</li>
                  ))}
                </ul>
              </div>
            ) : null}

            {expansion.bottomLine?.trim() ? (
              <p className="rounded-lg border border-black/[0.06] bg-[#F7F7F2]/70 px-3 py-2.5 text-sm leading-relaxed text-[#4E5663]">
                <span className="font-bold text-[#111318]">{LABEL_BOTTOM}: </span>
                {expansion.bottomLine}
              </p>
            ) : null}

            {expansion.comparisonContext?.trim() ? (
              <div>
                <h4 className="text-xs font-bold text-[#111318]">{LABEL_COMPARISON}</h4>
                <p className="mt-1.5 text-sm leading-relaxed text-[#4E5663]">
                  {expansion.comparisonContext}
                </p>
              </div>
            ) : null}

            {hasTechnical ? (
              <>
                <button
                  type="button"
                  onClick={() => setAdvanced((value) => !value)}
                  className="text-xs font-semibold text-[#1F8F6A] hover:underline"
                >
                  {advanced ? "הסתר נתונים טכניים" : "הצג נתונים טכניים (מתקדם)"}
                </button>

                {advanced ? (
                  <div className="space-y-3 border-t border-black/[0.06] pt-4 text-sm text-[#4E5663]">
                    {expansion.ingredients?.trim() ? (
                      <div>
                        <p className="text-xs font-bold text-[#111318]">רכיבים</p>
                        <p className="mt-1.5 leading-relaxed">{expansion.ingredients}</p>
                      </div>
                    ) : null}
                    {expansion.servingNote ? (
                      <p className="text-xs text-[#7A817C]">{expansion.servingNote}</p>
                    ) : null}
                  </div>
                ) : null}
              </>
            ) : null}

            <p className="text-[10px] text-[#AAAAAA]">{expansion.confidenceLabel}</p>
          </div>
        </motion.div>
      </div>
    </motion.article>
  );
}
