"use client";

import { useMemo } from "react";
import { motion, useReducedMotion } from "framer-motion";

import { EditorialSection } from "@/components/comparisons/milk-editorial/editorial-section";
import {
  getFlagshipProducts,
  processingTimelineSteps,
  productTimelineIndex,
} from "@/lib/comparisons/milk-editorial-content";
import type { MilkComparisonProduct } from "@/lib/comparisons/milk-types";
import { cn } from "@/lib/utils";

export function MilkProcessingTimeline({
  selectedBarcode,
  onSelect,
}: {
  selectedBarcode: string;
  onSelect: (product: MilkComparisonProduct) => void;
}) {
  const products = useMemo(() => getFlagshipProducts(), []);
  const reduceMotion = useReducedMotion();
  const steps = processingTimelineSteps;

  return (
    <EditorialSection
      id="processing-timeline"
      eyebrow="ספקטרום עיבוד"
      title="מהמקור ועד האריזה"
      description="מוצרים ממוקמים על ציר התהליך — לא כדי לקבוע «טוב» או «רע», אלא להראות כמה שלבים עברו בדרך."
      tone="dark"
    >
      <div className="relative overflow-x-auto pb-4">
        <div className="min-w-[640px] px-2 md:min-w-0">
          <div className="relative flex justify-between gap-2">
            <div
              className="absolute top-5 inset-x-4 h-px bg-gradient-to-l from-[#1F8F6A]/50 via-white/20 to-[#1F8F6A]/30"
              aria-hidden
            />
            {steps.map((step, i) => (
              <motion.div
                key={step.id}
                className="relative z-10 flex flex-1 flex-col items-center text-center"
                initial={reduceMotion ? false : { opacity: 0, y: 8 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.06 }}
              >
                <span className="flex size-10 items-center justify-center rounded-full border border-[#1F8F6A]/35 bg-[#0D0F12] text-[0.65rem] font-bold text-[#1F8F6A]">
                  {i + 1}
                </span>
                <span className="mt-2 max-w-[4.5rem] text-[0.65rem] font-semibold leading-tight text-[#C8CDC9] md:max-w-none md:text-xs">
                  {step.label}
                </span>
              </motion.div>
            ))}
          </div>

          <ul className="mt-12 space-y-3">
            {products.map((product) => {
              const stepIdx = productTimelineIndex(product);
              const selected = product.barcode === selectedBarcode;
              const pct = (stepIdx / (steps.length - 1)) * 100;

              return (
                <li key={product.barcode}>
                  <button
                    type="button"
                    onClick={() => onSelect(product)}
                    className={cn(
                      "w-full rounded-xl border px-4 py-3 text-right transition-colors duration-300",
                      selected
                        ? "border-[#1F8F6A]/40 bg-[#1F8F6A]/10"
                        : "border-white/10 bg-white/[0.04] hover:border-white/20"
                    )}
                  >
                    <div className="flex items-center justify-between gap-3">
                      <span
                        className={cn(
                          "text-sm font-bold",
                          selected ? "text-[#F7F7F2]" : "text-[#C8CDC9]"
                        )}
                      >
                        {product.displayTitle ?? product.shortName}
                      </span>
                      <span className="shrink-0 font-mono text-xs text-[#7A817C]">
                        {steps[stepIdx]?.label}
                      </span>
                    </div>
                    <div className="relative mt-3 h-1.5 overflow-hidden rounded-full bg-white/10">
                      <motion.div
                        className="absolute inset-y-0 start-0 rounded-full bg-[#1F8F6A]"
                        initial={reduceMotion ? { width: `${pct}%` } : { width: 0 }}
                        whileInView={{ width: `${pct}%` }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.8 }}
                      />
                    </div>
                  </button>
                </li>
              );
            })}
          </ul>
        </div>
      </div>
    </EditorialSection>
  );
}
