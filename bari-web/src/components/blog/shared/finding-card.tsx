"use client";

import { motion, useReducedMotion } from "framer-motion";

/**
 * FindingCard — rounded card with title, finding, and "למה זה משנה" sub-label.
 * Extracted from olive-oil-article.tsx to shared/ for TASK-200 (second article).
 */
export function FindingCard({
  title,
  finding,
  whyItMatters,
  index,
}: {
  title: string;
  finding: string;
  whyItMatters: string;
  index: number;
}) {
  const reduceMotion = useReducedMotion();
  return (
    <motion.li
      initial={reduceMotion ? false : { opacity: 0, y: 12 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ delay: index * 0.05 }}
      className="rounded-[1.2rem] border border-black/[0.07] bg-[#FFFFFF] px-6 py-6 md:px-8 md:py-7"
    >
      <h3 className="text-xl font-extrabold tracking-[-0.03em] text-[#111318] md:text-2xl">
        {title}
      </h3>
      <p className="mt-3 text-base leading-relaxed text-[#111318]">{finding}</p>
      <p className="mt-4 text-sm leading-relaxed text-[#4E5663]">
        <span className="font-bold text-[#7A9450]">למה זה משנה · </span>
        {whyItMatters}
      </p>
    </motion.li>
  );
}
