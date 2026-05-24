"use client";

import Image from "next/image";
import { motion, useReducedMotion } from "framer-motion";

import { BariGradeBadge } from "@/components/comparisons/bari-grade-badge";
import {
  countIngredients,
  getProductByBarcode,
  milkComparisonNarratives,
} from "@/lib/blog/milk-analysis-chart-data";
import { milkAnalysisArticle } from "@/lib/blog/milk-analysis-content";
import type { MilkComparisonProduct } from "@/lib/comparisons/milk-types";

function InvestigationPanel({
  product,
  ingredientDelta,
  scoreDelta,
}: {
  product: MilkComparisonProduct;
  ingredientDelta?: string;
  scoreDelta?: { delta: number; higherName: string };
}) {
  const title = product.displayTitle ?? product.shortName;

  return (
    <div className="flex-1 rounded-[1.1rem] border border-black/[0.07] bg-[#FFFFFF] p-4 md:p-5">
      <div className="flex items-start gap-3">
        <div className="relative h-[5rem] w-[3.5rem] shrink-0">
          {product.image_url ? (
            <Image
              src={product.image_url}
              alt={product.name_he}
              fill
              className="object-contain"
              sizes="56px"
            />
          ) : null}
        </div>
        <div className="min-w-0 flex-1 text-right">
          <p className="text-[0.65rem] font-bold text-[#1F8F6A]">{product.productTypeLabel}</p>
          <h4 className="mt-0.5 text-sm font-extrabold leading-snug text-[#111318] md:text-base">
            {title}
          </h4>
          <div className="mt-2 flex flex-wrap items-center gap-2">
            <span className="text-[0.6rem] font-bold text-[#7A817C]">ציון Bari</span>
            <BariGradeBadge
              score={product.score}
              grade={product.grade}
              gradeLabel={product.grade_label}
              size="sm"
            />
          </div>
          {ingredientDelta ? (
            <p className="mt-2 text-xs font-semibold text-[#4E5663]">{ingredientDelta}</p>
          ) : null}
          {scoreDelta ? (
            <p className="mt-1 text-xs text-[#7A817C]">
              הפרש ציון:{" "}
              <span className="font-bold text-[#111318]">+{scoreDelta.delta}</span> לטובת{" "}
              {scoreDelta.higherName}
            </p>
          ) : null}
        </div>
      </div>
    </div>
  );
}

function ComparisonBlock({
  narrative,
  index,
}: {
  narrative: (typeof milkComparisonNarratives)[number];
  index: number;
}) {
  const left = getProductByBarcode(narrative.leftBarcode);
  const right = getProductByBarcode(narrative.rightBarcode);
  const reduceMotion = useReducedMotion();

  if (!left || !right) return null;

  const leftCount = countIngredients(left);
  const rightCount = countIngredients(right);
  const delta =
    rightCount === leftCount
      ? `אותו מספר רכיבים (${leftCount}) — ההבדל ברכיבים עצמם`
      : `פער מורכבות: ${leftCount} רכיבים לעומת ${rightCount}`;

  const scoreGap = Math.abs(left.score - right.score);
  const higherName =
    left.score >= right.score
      ? (left.displayTitle ?? left.shortName)
      : (right.displayTitle ?? right.shortName);
  const scoreDeltaInfo =
    scoreGap > 0 ? { delta: scoreGap, higherName } : undefined;

  return (
    <motion.article
      initial={reduceMotion ? false : { opacity: 0, y: 14 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ delay: index * 0.06 }}
      className="rounded-[1.25rem] border border-black/[0.08] bg-[#FFFFFF] p-5 md:p-7"
    >
      <h3 className="text-lg font-extrabold tracking-[-0.03em] text-[#111318] md:text-xl">
        {narrative.title}
      </h3>
      <p className="mt-1 text-sm text-[#4E5663]">{narrative.subtitle}</p>
      <p className="mt-4 text-base leading-relaxed text-[#111318]">{narrative.story}</p>

      <div className="relative mt-6 flex flex-col gap-3 md:flex-row md:items-stretch">
        <InvestigationPanel
          product={left}
          ingredientDelta={`${leftCount} רכיבים ברשימה`}
          scoreDelta={scoreDeltaInfo}
        />
        <div className="relative flex items-center justify-center py-3 md:absolute md:inset-y-0 md:left-1/2 md:flex md:-translate-x-1/2 md:py-0">
          <span className="relative z-10 rounded-full border border-black/[0.08] bg-[#F7F7F2] px-3 py-1 text-xs font-bold text-[#7A817C]">
            לעומת
          </span>
          <div className="absolute inset-x-0 top-1/2 h-px bg-black/[0.06] md:hidden" />
        </div>
        <InvestigationPanel
          product={right}
          ingredientDelta={`${rightCount} רכיבים ברשימה`}
          scoreDelta={scoreDeltaInfo}
        />
      </div>

      <dl className="mt-6 space-y-3 border-t border-black/[0.06] pt-5 text-sm">
        <div>
          <dt className="font-bold text-[#1F8F6A]">למה התפצלו</dt>
          <dd className="mt-1 leading-relaxed text-[#4E5663]">{narrative.divergence}</dd>
        </div>
        <div>
          <dt className="font-bold text-[#111318]">מה ההבדל בהרכב</dt>
          <dd className="mt-1 leading-relaxed text-[#4E5663]">{narrative.formulationNote}</dd>
        </div>
        <div>
          <dt className="font-bold text-[#111318]">מה משתנה כשבוחרים</dt>
          <dd className="mt-1 leading-relaxed text-[#4E5663]">{narrative.whatChanged}</dd>
        </div>
        <div className="rounded-lg bg-[#F7F7F2]/80 px-3 py-2 text-xs font-semibold text-[#4E5663]">
          {delta}
        </div>
      </dl>
    </motion.article>
  );
}

export function MilkAnalysisComparisons() {
  const { comparisons } = milkAnalysisArticle;

  return (
    <section id="comparisons" className="scroll-mt-24">
      <header className="mb-8">
        <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#1F8F6A]/85">
          חקירה ממוקדת
        </p>
        <h2 className="mt-2 text-2xl font-extrabold tracking-[-0.04em] text-[#111318] md:text-3xl">
          {comparisons.title}
        </h2>
        <p className="mt-3 max-w-2xl text-base leading-relaxed text-[#4E5663]">
          {comparisons.subtitle}
        </p>
      </header>

      <div className="space-y-6">
        {milkComparisonNarratives.map((narrative, i) => (
          <ComparisonBlock key={narrative.id} narrative={narrative} index={i} />
        ))}
      </div>
    </section>
  );
}
