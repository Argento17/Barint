"use client";

import { motion, useReducedMotion } from "framer-motion";

import { ProductThumbnail } from "@/components/comparisons/product-thumbnail";
import {
  getProductByBarcode,
  shelfAnchors,
} from "@/lib/blog/milk-analysis-chart-data";
import { milkAnalysisArticle } from "@/lib/blog/milk-analysis-content";

export function MilkAnalysisShelfSpectrum() {
  const { shelfSpectrum } = milkAnalysisArticle;
  const reduceMotion = useReducedMotion();

  return (
    <section id="shelf-spectrum" className="scroll-mt-24">
      <header className="mb-8">
        <h2 className="text-2xl font-extrabold tracking-[-0.04em] text-[#111318] md:text-3xl">
          {shelfSpectrum.title}
        </h2>
        <p className="mt-3 max-w-2xl text-base leading-relaxed text-[#4E5663]">
          {shelfSpectrum.subtitle}
        </p>
      </header>

      <div className="flex gap-4 overflow-x-auto pb-2 snap-x snap-mandatory md:grid md:grid-cols-5 md:overflow-visible">
        {shelfAnchors.map((anchor, i) => {
          const product = getProductByBarcode(anchor.barcode);
          if (!product) return null;

          return (
            <motion.article
              key={anchor.id}
              initial={reduceMotion ? false : { opacity: 0, y: 14 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.06 }}
              className="min-w-[11.5rem] shrink-0 snap-center rounded-[1.1rem] border border-black/[0.07] bg-[#FFFFFF] p-4 md:min-w-0"
            >
              <ProductThumbnail
                product={product}
                wrapperClassName="mx-auto h-20 w-14 rounded-[1rem] shadow-none"
                imageClassName="p-0.5"
                imageSizes="56px"
              />
              <p className="mt-3 text-[0.65rem] font-bold uppercase tracking-wide text-[#1F8F6A]">
                {anchor.title}
              </p>
              <p className="mt-1 text-sm font-extrabold leading-snug text-[#111318]">
                {anchor.subtitle}
              </p>
              <p className="mt-2 text-xs leading-relaxed text-[#4E5663]">{anchor.insight}</p>
            </motion.article>
          );
        })}
      </div>
    </section>
  );
}
