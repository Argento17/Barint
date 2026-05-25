"use client";

import { useMemo } from "react";
import { motion, useReducedMotion } from "framer-motion";

import { ProductThumbnail } from "@/components/comparisons/product-thumbnail";
import {
  countIngredients,
  parseIngredientsDisplay,
} from "@/lib/blog/milk-analysis-chart-data";
import {
  getSimplicityLadderProducts,
  milkAnalysisArticle,
} from "@/lib/blog/milk-analysis-content";
import type { MilkComparisonProduct } from "@/lib/comparisons/milk-types";

const MAX_VISIBLE_CHIPS = 10;

function IngredientChips({ display }: { display: string }) {
  const { ingredientChips, totalCount, overflowCount } = useMemo(() => {
    const all = parseIngredientsDisplay(display);
    return {
      ingredientChips: all.slice(0, MAX_VISIBLE_CHIPS),
      totalCount: all.length,
      overflowCount: Math.max(0, all.length - MAX_VISIBLE_CHIPS),
    };
  }, [display]);

  if (totalCount === 0) {
    return null;
  }

  return (
    <div className="mt-3 w-full min-w-0" dir="rtl">
      <div className="flex flex-wrap justify-end gap-1.5">
        {ingredientChips.map((chip) => (
          <span
            key={chip}
            title={chip}
            className="inline-block max-w-full break-words rounded-lg border border-black/[0.06] bg-[#F7F7F2] px-2.5 py-1 text-right text-[0.7rem] leading-snug text-[#4E5663] sm:max-w-[calc(50%-0.375rem)]"
          >
            {chip}
          </span>
        ))}
        {overflowCount > 0 ? (
          <span className="inline-block rounded-lg border border-black/[0.06] bg-[#F7F7F2] px-2.5 py-1 text-[0.7rem] font-bold leading-snug text-[#7A817C]">
            +{overflowCount} נוספים
          </span>
        ) : null}
      </div>
    </div>
  );
}

function SimplicityProductRow({
  product,
  index,
  maxCount,
  layersLabel,
  reduceMotion,
}: {
  product: MilkComparisonProduct;
  index: number;
  maxCount: number;
  layersLabel: string;
  reduceMotion: boolean;
}) {
  const count = countIngredients(product);
  const widthPct = Math.min(100, (count / maxCount) * 100);
  const title = product.displayTitle ?? product.shortName;
  const ingredientsDisplay = product.ingredients_display ?? "";

  return (
    <motion.li
      initial={reduceMotion ? false : { opacity: 0, x: -8 }}
      whileInView={{ opacity: 1, x: 0 }}
      viewport={{ once: true }}
      transition={{ delay: index * 0.05 }}
      className="flex flex-col gap-4 rounded-[1.1rem] border border-black/[0.06] bg-[#FFFFFF] p-4 md:p-5"
    >
      <div className="flex items-center gap-4">
        <ProductThumbnail
          product={product}
          wrapperClassName="h-16 w-11 shrink-0 rounded-[0.9rem] shadow-none"
          imageClassName="p-0.5"
          imageSizes="44px"
        />
        <div className="min-w-0 flex-1 text-right">
          <p className="text-[0.65rem] font-bold text-[#1F8F6A]">{product.productTypeLabel}</p>
          <p className="text-sm font-extrabold text-[#111318]">{title}</p>
        </div>
      </div>

      <div className="w-full min-w-0">
        <div className="mb-1.5 flex justify-between gap-4 text-xs font-semibold text-[#7A817C]">
          <span>{layersLabel}</span>
          <span className="shrink-0 tabular-nums text-[#111318]">{count}</span>
        </div>
        <div className="h-2 overflow-hidden rounded-full bg-black/[0.06]">
          <motion.div
            className="h-full rounded-full bg-[#1F8F6A]"
            initial={reduceMotion ? { width: `${widthPct}%` } : { width: 0 }}
            whileInView={{ width: `${widthPct}%` }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: index * 0.06 }}
          />
        </div>
        <IngredientChips display={ingredientsDisplay} />
      </div>
    </motion.li>
  );
}

export function MilkAnalysisSimplicity() {
  const { simplicity } = milkAnalysisArticle;
  const products = getSimplicityLadderProducts();
  const reduceMotion = useReducedMotion() ?? false;
  const maxCount = Math.max(...products.map(countIngredients), 1);

  return (
    <section id="simplicity" className="scroll-mt-24">
      <header className="mb-8">
        <h2 className="text-2xl font-extrabold tracking-[-0.04em] text-[#111318] md:text-3xl">
          {simplicity.title}
        </h2>
        <p className="mt-3 max-w-2xl text-base leading-relaxed text-[#4E5663]">
          {simplicity.subtitle}
        </p>
      </header>

      <ul className="space-y-4">
        {products.map((product, i) => (
          <SimplicityProductRow
            key={product.barcode}
            product={product}
            index={i}
            maxCount={maxCount}
            layersLabel={simplicity.layersLabel}
            reduceMotion={reduceMotion}
          />
        ))}
      </ul>
    </section>
  );
}
