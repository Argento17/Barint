"use client";

import { motion, useReducedMotion } from "framer-motion";

import { EditorialSection } from "@/components/comparisons/milk-editorial/editorial-section";
import { editorialDimensionKeys } from "@/lib/comparisons/milk-editorial-content";
import type { MilkComparisonProduct } from "@/lib/comparisons/milk-types";

export function MilkDimensionStory({ product }: { product: MilkComparisonProduct }) {
  const reduceMotion = useReducedMotion();
  const title = product.displayTitle ?? product.shortName;

  return (
    <EditorialSection
      id="dimensions"
      eyebrow="פרמטרים במקביל"
      title={`מימדים · ${title}`}
      description="פירוק לפי מבנה, שלמות, תוספים ופרופיל — בלי רדאר, בלי מספר בודד שמספר הכול."
      tone="canvas"
    >
      <div className="space-y-5">
        {editorialDimensionKeys.map(({ key, label }, i) => {
          const dim = product.dimensions[key];
          if (!dim) return null;
          const value = Math.round(dim.score);

          return (
            <div key={key}>
              <div className="mb-2 flex justify-between gap-4 text-sm font-semibold">
                <span className="text-[#4E5663]">{label}</span>
                <span className="tabular-nums text-[#111318]">{value}</span>
              </div>
              <div className="h-2 overflow-hidden rounded-full bg-black/[0.06]">
                <motion.div
                  className="h-full rounded-full bg-gradient-to-l from-[#1F8F6A] to-[#5A9E7E]"
                  initial={reduceMotion ? { width: `${value}%` } : { width: 0 }}
                  whileInView={{ width: `${value}%` }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.7, delay: i * 0.05, ease: [0.22, 1, 0.36, 1] }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </EditorialSection>
  );
}
