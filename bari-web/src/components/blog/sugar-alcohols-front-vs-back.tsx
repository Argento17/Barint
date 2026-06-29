"use client";

import { motion, useReducedMotion } from "framer-motion";

import { frontVsBack } from "@/lib/blog/sugar-alcohols-article-content";

/**
 * Front vs. Back — three real bars centerpiece component.
 *
 * Task: TASK-379 Phase 2
 * Strings: S-47 (heading), S-48 (intro), S-49/S-50/S-51 (per-bar lines).
 * Source: sugar_alcohols_blog_copy_v1.md §7b; figures locked in spec §9.
 *
 * Design intent:
 *   - High-impact per-bar contrast: front-of-pack sugar vs back-of-pack polyol total.
 *   - WIN + אול אין: hasLegalWarning=true → "נושא אזהרה חוקית" badge (amber warning tone).
 *   - פרו שטראוס: hasLegalWarning=false → "האזהרה לא אומתה" state (neutral, not warning).
 *   - RTL layout, frozen design tokens, mobile-first (375px primary).
 */

interface BarEntry {
  readonly id: string;
  readonly text: string;
  readonly hasLegalWarning: boolean;
}

function WarningBadge({ confirmed }: { confirmed: boolean }) {
  if (confirmed) {
    return (
      <span className="inline-flex items-center gap-1 rounded-full border border-amber-300/70 bg-amber-50 px-2.5 py-0.5 text-[0.65rem] font-bold uppercase tracking-[0.1em] text-[#7A6A00]">
        <span aria-hidden className="text-amber-500">⚠</span>
        נושא אזהרה חוקית
      </span>
    );
  }
  return (
    <span className="inline-flex items-center gap-1 rounded-full border border-[#B0B8C4]/60 bg-[#F7F7F2] px-2.5 py-0.5 text-[0.65rem] font-bold uppercase tracking-[0.1em] text-[#7A817C]">
      <span aria-hidden className="opacity-60">?</span>
      האזהרה לא אומתה
    </span>
  );
}

function BarCard({ bar, index }: { bar: BarEntry; index: number }) {
  const reduceMotion = useReducedMotion();
  return (
    <motion.div
      initial={reduceMotion ? false : { opacity: 0, y: 12 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-20px" }}
      transition={{ duration: 0.45, delay: index * 0.08 }}
      className="rounded-[1rem] border border-black/[0.07] bg-[#FFFFFF] px-5 py-5 text-right md:px-6"
    >
      {/* Warning status badge — top-right in RTL */}
      <div className="mb-3 flex justify-end">
        <WarningBadge confirmed={bar.hasLegalWarning} />
      </div>

      {/* Bar line text */}
      <p className="text-sm leading-[1.85] text-[#111318] md:text-base">
        {bar.text}
      </p>
    </motion.div>
  );
}

export function SugarAlcoholsFrontVsBack() {
  return (
    <section id="front-vs-back" className="border-t border-black/6 bg-[#F7F7F2] py-14 md:py-20">
      <div className="mx-auto max-w-3xl px-4 md:px-6">
        {/* Section header */}
        <header className="mb-8 text-right">
          <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#C0392B]/80">
            מול המדף — שלוש חטיפות אמיתיות
          </p>
          <h2 className="mt-2 text-3xl font-extrabold tracking-tighter text-[#111318] md:text-4xl">
            {frontVsBack.heading}
          </h2>
          {/* Intro */}
          <p className="mt-4 text-base leading-[1.85] text-[#4E5663] md:text-lg">
            {frontVsBack.intro}
          </p>
        </header>

        {/* Per-bar cards */}
        <div className="space-y-4">
          {frontVsBack.bars.map((bar, i) => (
            <BarCard key={bar.id} bar={bar} index={i} />
          ))}
        </div>

        {/* Legend */}
        <div className="mt-6 flex flex-wrap justify-end gap-4 text-right">
          <div className="flex items-center gap-1.5">
            <span className="inline-flex items-center gap-1 rounded-full border border-amber-300/70 bg-amber-50 px-2 py-0.5 text-[0.6rem] font-bold uppercase tracking-[0.08em] text-[#7A6A00]">
              <span aria-hidden className="text-amber-500">⚠</span>
              נושא אזהרה חוקית
            </span>
            <span className="text-xs text-[#7A817C]">— האזהרה מודפסת על האריזה (מעל 10% כוהלי סוכר)</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="inline-flex items-center gap-1 rounded-full border border-[#B0B8C4]/60 bg-[#F7F7F2] px-2 py-0.5 text-[0.6rem] font-bold uppercase tracking-[0.08em] text-[#7A817C]">
              <span aria-hidden className="opacity-60">?</span>
              האזהרה לא אומתה
            </span>
            <span className="text-xs text-[#7A817C]">— לא הצלחנו לאמת על האריזה הפיזית</span>
          </div>
        </div>
      </div>
    </section>
  );
}
