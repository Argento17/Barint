"use client";

import { motion, useReducedMotion } from "framer-motion";

import { EditorialSection } from "@/components/comparisons/milk-editorial/editorial-section";
import { ingredientStructureExamples } from "@/lib/comparisons/milk-editorial-content";
import { cn } from "@/lib/utils";

function LayerStack({
  layers,
  variant,
}: {
  layers: readonly string[];
  variant: "simple" | "complex";
}) {
  const reduceMotion = useReducedMotion();

  return (
    <div className="flex flex-col gap-2">
      {layers.map((layer, i) => (
        <motion.div
          key={layer}
          initial={reduceMotion ? false : { opacity: 0, x: variant === "simple" ? 0 : 12 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
          transition={{ delay: i * 0.08, duration: 0.45 }}
          className={cn(
            "rounded-xl border px-4 py-3 text-sm font-semibold",
            variant === "simple"
              ? "border-[#1F8F6A]/25 bg-[#1F8F6A]/10 text-[#F7F7F2]"
              : "border-white/10 bg-white/[0.06] text-[#E8EBE9]"
          )}
          style={
            variant === "complex"
              ? { marginInlineStart: `${i * 8}px`, opacity: 1 - i * 0.06 }
              : undefined
          }
        >
          {layer}
        </motion.div>
      ))}
    </div>
  );
}

export function MilkIngredientStructure() {
  const { dairy, plant } = ingredientStructureExamples;

  return (
    <EditorialSection
      id="ingredient-structure"
      eyebrow="מבנה רכיבים"
      title="מזון פשוט מול הרכבה מחדש"
      description="לא שיפוט מוסרי — רק הבדל במבנה: כמה שכבות נדרשו כדי שהמוצר יגיע למדף."
      tone="dark"
    >
      <div className="grid gap-10 md:grid-cols-2 md:gap-12">
        <div className="rounded-[1.25rem] border border-[#1F8F6A]/20 bg-[#1F8F6A]/[0.08] p-6 md:p-8">
          <p className="text-sm font-bold text-[#1F8F6A]">{dairy.label}</p>
          <div className="mt-6">
            <LayerStack layers={dairy.layers} variant="simple" />
          </div>
        </div>
        <div className="rounded-[1.25rem] border border-white/10 bg-white/[0.04] p-6 md:p-8">
          <p className="text-sm font-bold text-[#C8CDC9]">{plant.label}</p>
          <div className="mt-6">
            <LayerStack layers={plant.layers} variant="complex" />
          </div>
        </div>
      </div>
    </EditorialSection>
  );
}
