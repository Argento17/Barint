"use client";

import Image from "next/image";
import { motion, useReducedMotion } from "framer-motion";

import { AnimatedScoreRing } from "@/components/comparisons/milk-editorial/animated-score-ring";
import { EditorialSection } from "@/components/comparisons/milk-editorial/editorial-section";
import { GRADE_COLORS } from "@/lib/comparisons/milk-page-data";
import { getFlagshipProducts } from "@/lib/comparisons/milk-editorial-content";
import type { MilkComparisonProduct } from "@/lib/comparisons/milk-types";
import { cn } from "@/lib/utils";

export function MilkProductStrip({
  selectedBarcode,
  onSelect,
}: {
  selectedBarcode: string;
  onSelect: (product: MilkComparisonProduct) => void;
}) {
  const products = getFlagshipProducts();
  const reduceMotion = useReducedMotion();

  return (
    <EditorialSection
      id="product-strip"
      eyebrow="מדף · השוואה"
      title="שישה מוצרים, שישה מבנים"
      description="לחצו על מוצר לעומק הניתוח — ציון, דרגה ותובנה קצרה מהמדף."
      tone="canvas"
      fullWidth
    >
      <div className="-mx-5 overflow-x-auto px-5 pb-2 sm:-mx-6 sm:px-6 md:overflow-visible">
        <div className="flex gap-4 md:grid md:grid-cols-3 md:gap-5 lg:grid-cols-3">
          {products.map((product, i) => {
            const selected = product.barcode === selectedBarcode;
            const colors = GRADE_COLORS[product.grade];
            const title = product.displayTitle ?? product.shortName;

            return (
              <motion.button
                key={product.barcode}
                type="button"
                onClick={() => onSelect(product)}
                initial={reduceMotion ? false : { opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.08, duration: 0.5 }}
                className={cn(
                  "group relative min-w-[17rem] shrink-0 overflow-hidden rounded-[1.35rem] border text-right transition-[border-color,box-shadow,transform] duration-500 md:min-w-0",
                  selected
                    ? "border-[#1F8F6A]/35 bg-[#111318] shadow-[0_32px_80px_-40px_rgba(31,143,106,0.35)] ring-1 ring-[#1F8F6A]/25"
                    : "border-black/[0.08] bg-[#FFFFFF]/90 shadow-[0_20px_60px_-48px_rgba(17,19,24,0.25)] hover:-translate-y-1 hover:border-[#1F8F6A]/20"
                )}
              >
                <div
                  className="pointer-events-none absolute inset-0 opacity-0 transition-opacity duration-500 group-hover:opacity-100"
                  style={{
                    background: `radial-gradient(circle at 80% 20%, ${colors.bg}22, transparent 55%)`,
                  }}
                  aria-hidden
                />
                <div className="relative flex flex-col gap-4 p-5 md:p-6">
                  <div className="flex items-start justify-between gap-3">
                    <div className="relative h-28 w-20 shrink-0">
                      {product.image_url ? (
                        <Image
                          src={product.image_url}
                          alt={product.name_he}
                          fill
                          className="object-contain drop-shadow-md"
                          sizes="80px"
                        />
                      ) : null}
                    </div>
                    <AnimatedScoreRing score={product.score} grade={product.grade} size={76} />
                  </div>
                  <div>
                    <p
                      className={cn(
                        "text-xs font-bold",
                        selected ? "text-[#1F8F6A]" : "text-[#7A817C]"
                      )}
                    >
                      {product.productTypeLabel}
                    </p>
                    <h3
                      className={cn(
                        "mt-1 text-base font-extrabold leading-snug tracking-[-0.03em]",
                        selected ? "text-[#F7F7F2]" : "text-[#111318]"
                      )}
                    >
                      {title}
                    </h3>
                    <p
                      className={cn(
                        "mt-2 line-clamp-2 text-sm leading-relaxed",
                        selected ? "text-[#C8CDC9]" : "text-[#4E5663]"
                      )}
                    >
                      {product.consumerTakeaway}
                    </p>
                  </div>
                </div>
              </motion.button>
            );
          })}
        </div>
      </div>
    </EditorialSection>
  );
}
