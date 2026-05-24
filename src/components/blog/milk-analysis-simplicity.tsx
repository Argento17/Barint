"use client";

import Image from "next/image";
import { motion, useReducedMotion } from "framer-motion";

import { countIngredients } from "@/lib/blog/milk-analysis-chart-data";
import {
  getSimplicityLadderProducts,
  milkAnalysisArticle,
} from "@/lib/blog/milk-analysis-content";

const MAX_INGREDIENTS = 12;

export function MilkAnalysisSimplicity() {
  const { simplicity } = milkAnalysisArticle;
  const products = getSimplicityLadderProducts();
  const reduceMotion = useReducedMotion();
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
        {products.map((product, i) => {
          const count = countIngredients(product);
          const widthPct = Math.min(100, (count / maxCount) * 100);
          const title = product.displayTitle ?? product.shortName;

          return (
            <motion.li
              key={product.barcode}
              initial={reduceMotion ? false : { opacity: 0, x: -8 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.05 }}
              className="flex flex-col gap-3 rounded-[1.1rem] border border-black/[0.06] bg-[#FFFFFF] p-4 sm:flex-row sm:items-center sm:gap-5"
            >
              <div className="flex min-w-0 flex-1 items-center gap-4">
                <div className="relative h-16 w-11 shrink-0">
                  {product.image_url ? (
                    <Image
                      src={product.image_url}
                      alt=""
                      fill
                      className="object-contain"
                      sizes="44px"
                    />
                  ) : null}
                </div>
                <div className="min-w-0 text-right">
                  <p className="text-[0.65rem] font-bold text-[#1F8F6A]">
                    {product.productTypeLabel}
                  </p>
                  <p className="text-sm font-extrabold text-[#111318]">{title}</p>
                </div>
              </div>
              <div className="flex-1 sm:max-w-md">
                <div className="mb-1.5 flex justify-between text-xs font-semibold text-[#7A817C]">
                  <span>{simplicity.layersLabel}</span>
                  <span className="tabular-nums text-[#111318]">{count}</span>
                </div>
                <div className="h-2 overflow-hidden rounded-full bg-black/[0.06]">
                  <motion.div
                    className="h-full rounded-full bg-gradient-to-l from-[#1F8F6A] to-[#5A9E7E]"
                    initial={reduceMotion ? { width: `${widthPct}%` } : { width: 0 }}
                    whileInView={{ width: `${widthPct}%` }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.6, delay: i * 0.06 }}
                  />
                </div>
                <p className="mt-2 line-clamp-1 text-[0.65rem] text-[#7A817C]">
                  {product.ingredients_display.length > MAX_INGREDIENTS * 4
                    ? `${product.ingredients_display.slice(0, 48)}…`
                    : product.ingredients_display}
                </p>
              </div>
            </motion.li>
          );
        })}
      </ul>
    </section>
  );
}
