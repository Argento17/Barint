"use client";

import { motion, useReducedMotion } from "framer-motion";

import type { MilkComparisonProduct } from "@/lib/comparisons/milk-types";
import { PRIMARY_DIMENSION_KEYS } from "@/lib/comparisons/milk-page-data";
import { cn } from "@/lib/utils";

const DIM_LABELS: Record<string, string> = {
  processing_quality: "מבנה ועיבוד (הקשרי)",
  nutrient_density: "תרומה תזונתית צפופה",
  protein_quality: "חלבון בפרופיל",
  additive_quality: "תוספים / מייצבים",
  fat_quality: "פרופיל שומן",
  glycemic_quality: "השפעה גליקמית",
  whole_food_integrity: "קרבה למזון שלם",
};

export function DimensionBars({
  product,
  muted = false,
}: {
  product: MilkComparisonProduct;
  muted?: boolean;
}) {
  const reduceMotion = useReducedMotion();

  return (
    <div className={cn("space-y-2.5", muted && "opacity-50")}>
      {PRIMARY_DIMENSION_KEYS.map((key) => {
        const dim = product.dimensions[key];
        if (!dim) return null;
        const scoreRounded = Math.round(dim.score);
        return (
          <div key={key}>
            <div className="mb-1 flex justify-between text-[0.7rem] font-semibold">
              <span className="text-[#4E5663]">{DIM_LABELS[key] ?? dim.display_name}</span>
              <span className="tabular-nums text-[#111318]">{scoreRounded}</span>
            </div>
            <div className="h-1.5 overflow-hidden rounded-full bg-[#F7F7F2]">
              <motion.div
                className="h-full rounded-full bg-[#1F8F6A]/85"
                initial={reduceMotion ? { width: `${scoreRounded}%` } : { width: 0 }}
                animate={{ width: `${scoreRounded}%` }}
                transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
              />
            </div>
          </div>
        );
      })}
    </div>
  );
}
