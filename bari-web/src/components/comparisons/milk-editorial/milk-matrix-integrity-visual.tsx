"use client";

import { motion, useReducedMotion } from "framer-motion";

import { EditorialSection } from "@/components/comparisons/milk-editorial/editorial-section";
import { formatDecimal } from "@/lib/format/numbers";
import { DEGRADATION_LABELS } from "@/lib/comparisons/milk-page-data";
import { maxEngineeringIntensity } from "@/lib/comparisons/milk-editorial-content";
import type { MilkComparisonProduct } from "@/lib/comparisons/milk-types";
import { cn } from "@/lib/utils";

function FragmentBlocks({ intensity, max }: { intensity: number; max: number }) {
  const count = Math.min(12, Math.max(3, Math.round((intensity / max) * 10) + 3));
  const reduceMotion = useReducedMotion();

  return (
    <div className="flex flex-wrap gap-1.5" aria-hidden>
      {Array.from({ length: count }).map((_, i) => (
        <motion.span
          key={i}
          className={cn(
            "rounded-sm border border-[#1F8F6A]/30 bg-[#1F8F6A]/15",
            i % 3 === 0 ? "h-8 w-10" : i % 3 === 1 ? "h-6 w-14" : "h-10 w-8"
          )}
          initial={reduceMotion ? false : { opacity: 0, scale: 0.8 }}
          whileInView={{ opacity: 1 - i * 0.04, scale: 1 }}
          viewport={{ once: true }}
          transition={{ delay: i * 0.04 }}
        />
      ))}
    </div>
  );
}

export function MilkMatrixIntegrityVisual({
  product,
  allProducts,
}: {
  product: MilkComparisonProduct;
  allProducts: MilkComparisonProduct[];
}) {
  const m = product.matrix_integrity;
  const maxEng = maxEngineeringIntensity(allProducts);
  const integrityPct = Math.round(m.matrix_integrity_score);
  const reconPct = Math.min(100, m.reconstruction_depth * 18);
  const levelLabel =
    DEGRADATION_LABELS[m.structural_degradation_level] ?? m.structural_degradation_level;
  const reduceMotion = useReducedMotion();

  return (
    <EditorialSection
      id="matrix-integrity"
      eyebrow="שלמות מבנית"
      title="עד כמה המוצר נשאר שלם?"
      description="מדדים שמדברים על פירוק, עומק הרכבה מחדש ועוצמת הנדסה — לא רק על «רמת עיבוד» ככותרת."
      tone="light"
    >
      <div className="grid gap-8 lg:grid-cols-[1fr_1.1fr] lg:gap-12">
        <div className="space-y-6">
          <div>
            <div className="mb-2 flex justify-between text-sm font-semibold">
              <span className="text-[#4E5663]">שלמות מבנית</span>
              <span className="tabular-nums text-[#111318]">{integrityPct}%</span>
            </div>
            <div className="h-2 overflow-hidden rounded-full bg-black/[0.06]">
              <motion.div
                className="h-full rounded-full bg-[#1F8F6A]"
                initial={reduceMotion ? { width: `${integrityPct}%` } : { width: 0 }}
                whileInView={{ width: `${integrityPct}%` }}
                viewport={{ once: true }}
                transition={{ duration: 1, ease: [0.22, 1, 0.36, 1] }}
              />
            </div>
          </div>
          <div>
            <div className="mb-2 flex justify-between text-sm font-semibold">
              <span className="text-[#4E5663]">עומק הרכבה מחדש</span>
              <span className="tabular-nums text-[#111318]">{m.reconstruction_depth}</span>
            </div>
            <div className="h-2 overflow-hidden rounded-full bg-black/[0.06]">
              <motion.div
                className="h-full rounded-full bg-[#5A9E7E]"
                initial={reduceMotion ? { width: `${reconPct}%` } : { width: 0 }}
                whileInView={{ width: `${reconPct}%` }}
                viewport={{ once: true }}
                transition={{ duration: 1, delay: 0.1 }}
              />
            </div>
          </div>
          <p className="text-sm text-[#7A817C]">
            {levelLabel} · עוצמת הנדסה {formatDecimal(m.engineering_intensity, 1)}
          </p>
          <p className="rounded-xl border border-black/[0.06] bg-[#FFFFFF] px-4 py-3 text-sm leading-relaxed text-[#4E5663]">
            {product.displayTitle ?? product.shortName} — {product.mainIngredient}
          </p>
        </div>

        <div className="rounded-[1.25rem] border border-black/[0.08] bg-[#111318] p-6 md:p-8">
          <p className="text-xs font-bold uppercase tracking-[0.2em] text-[#1F8F6A]">
            פירוק מבני · ויזואלי
          </p>
          <p className="mt-2 text-sm text-[#C8CDC9]">
            ככל שהעוצמה עולה, המבנה נראה מפורק ליותר יחידות.
          </p>
          <div className="mt-8">
            <FragmentBlocks intensity={m.engineering_intensity} max={maxEng} />
          </div>
        </div>
      </div>
    </EditorialSection>
  );
}
